import cv2
import dlib

# 얼굴 검출기와 랜드마크 검출기 생성 --- ①
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor('../src/shape_predictor_68_face_landmarks.dat')


def detect_faces(frame, detector, predictor, draw_landmarks=True):
    """
    얼굴 검출 및 랜드마크 표시 함수
    :param frame: BGR 이미지 프레임
    :param draw_landmarks: True일 경우 얼굴과 랜드마크를 이미지에 그림
    :return: 얼굴 좌표 리스트 [(x, y, w, h)], 랜드마크 좌표 리스트 [[(x1, y1), ..., (x68, y68)]], 결과 이미지
    """
    img = frame.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 얼굴 영역 검출
    faces = detector(gray)
    face_boxes = []
    landmarks_all = []

    for rect in faces:
        # 얼굴 영역을 좌표로 변환 후 사각형 표시
        x, y = rect.left(), rect.top()
        w, h = rect.right() - x, rect.bottom() - y
        face_boxes.append((x, y, w, h))

        # 얼굴 랜드마크 검출
        shape = predictor(gray, rect)
        landmarks = [(shape.part(i).x, shape.part(i).y) for i in range(68)]
        landmarks_all.append(landmarks)

        if draw_landmarks:
            # 부위별 좌표 추출 및 표시
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            for (px, py) in landmarks:
                cv2.circle(img, (px, py), 2, (0, 0, 255), -1)

    return faces, landmarks_all, img


# 테스트 코드
# cap = cv2.VideoCapture(0)
#cap.set(cv2.cv2.CAP_PROP_FRAME_WIDTH, 480)
#cap.set(cv2.cv2.CAP_PROP_FRAME_HEIGHT, 320)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)

#     faces, landmarks, result_img = detect_faces(frame, draw_landmarks=True)

#     cv2.imshow("Face Landmarks", result_img)
#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
