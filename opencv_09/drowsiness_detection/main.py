import cv2
import dlib
from basic_landmark import detect_faces


def main():

    # 초기화

    detector = dlib.get_frontal_face_detector()

    predictor = dlib.shape_predictor('../src/shape_predictor_68_face_landmarks.dat')

    cap = cv2.VideoCapture(0)

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:

            break

        frame = cv2.flip(frame, 1) # 카메라 좌우반전

        # 1단계: 얼굴 검출

        # faces = detect_faces(frame, detector)
        result_img = detect_faces(frame, detector, predictor, draw_landmarks=True)

        cv2.imshow('Drowsiness Detection', result_img)
        

        # if len(faces) > 0:

        #     # 2단계: 랜드마크 추출

        #     landmarks = get_landmarks(frame, faces[0], predictor)

            

        #     # 3단계: EAR 계산

        #     ear_value = calculate_ear_from_landmarks(landmarks)

            

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
