import cv2
import dlib
from basic_landmark import detect_faces
import utils

# 눈 인덱스
LEFT_EYE_IDX = [36, 37, 38, 39, 40, 41]
RIGHT_EYE_IDX = [42, 43, 44, 45, 46, 47]

EAR_THRESHOLD = 0.25
CLOSED_EYES_FRAME_THRESHOLD = 150  # 5초 기준 (30fps 가정)

def main():

    # 초기화
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('../src/shape_predictor_68_face_landmarks.dat')
    cap = cv2.VideoCapture(0)
    closed_eyes_frame_count = 0
    drowsy = False

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:

            break

        frame = cv2.flip(frame, 1) # 카메라 좌우반전

        # 1단계: 얼굴 검출 및 랜드마크 추출

        # faces = detect_faces(frame, detector)
        faces, landmarks, frame = detect_faces(frame, detector, predictor, draw_landmarks=True)

        # 안내 메세지 출력
        cv2.putText(frame, "ESC: Exit", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Drowsiness Detection', frame)
        

        if len(faces) > 0:

            # print(len(faces))

            # 2단계: EAR 계산
            # print(landmarks)
            # ear_value = calculate_ear_from_landmarks(landmarks)
            left_ear = utils.calculate_ear_from_landmarks(landmarks, LEFT_EYE_IDX)
            right_ear = utils.calculate_ear_from_landmarks(landmarks, RIGHT_EYE_IDX)
            avg_ear = (left_ear + right_ear) / 2.0

            # print(avg_ear)

            # 3단계: 졸음 판단

            if avg_ear < EAR_THRESHOLD:
                closed_eyes_frame_count += 1
            else:
                closed_eyes_frame_count = 0
                drowsy = False

            if closed_eyes_frame_count >= CLOSED_EYES_FRAME_THRESHOLD:
                drowsy = True
            
            # 4단계: 결과 표시
            print(drowsy)
            if drowsy:
                cv2.putText(frame, "졸음 감지! 주의하세요!", (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        #     # 4단계: 졸음 판단

        #     drowsy_state = check_drowsiness(ear_value)

            

        #     # 5단계: 결과 표시

        #     draw_results(frame, landmarks, ear_value, drowsy_state)

        

        # cv2.imshow('Drowsiness Detection', frame)

        if cv2.waitKey(1) == 27:  # ESC 키

            break

            
    cap.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":

    main()
