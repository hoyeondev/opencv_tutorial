import cv2
import numpy as np
import os, glob

# 변수 설정 ---①
base_dir = './faces'
min_accuracy = 85

# LBP 얼굴 인식기 및 케스케이드 얼굴 검출기 생성 및 훈련 모델 읽기 ---②
face_classifier = cv2.CascadeClassifier(\
                '../data/haarcascade_frontalface_default.xml')
model = cv2.face.LBPHFaceRecognizer_create()
model.read(os.path.join(base_dir, 'all_face.xml'))

# 스마일 검출 xml 추가
smile = cv2.CascadeClassifier(\
                '../data/haarcascade_smile.xml')

# 디렉토리 이름으로 사용자 이름과 아이디 매핑 정보 생성 ---③
dirs = [d for d in glob.glob(base_dir+"/*") if os.path.isdir(d)]
names = dict([])
for dir in dirs:
    dir = os.path.basename(dir)
    name, id = dir.split('_')
    names[int(id)] = name

# 카메라 캡처 장치 준비 
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("no frame")
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # 얼굴 검출 ---④
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # 얼굴 영역 표시하고 샘플과 같은 크기로 축소 ---⑤
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        # LBP 얼굴 인식기로 예측 ---⑥
        label, confidence = model.predict(face)
        # print(names)
        if confidence < 400:
            # 정확도 거리를 퍼센트로 변환 ---⑦
            accuracy = int( 100 * (1 -confidence/400))
            if accuracy >= min_accuracy:
                msg =  '%s(%.0f%%)'%(names[label], accuracy)
            else:
                msg = 'Unknown'

        # 얼굴 내부에서 smile 검출
        face_roi_gray = gray[y:y+h, x:x+w]
        detected_smile = smile.detectMultiScale(face_roi_gray, scaleFactor=1.7, minNeighbors=22)

        # 스마일 정보 출력
        if len(detected_smile) > 0 and accuracy >= min_accuracy:
            smile_text = "~~~ SMILE ~~~"
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 2.5
            thickness = 4
            text_size, _ = cv2.getTextSize(smile_text, font, font_scale, thickness)

            # 화면 중앙 좌표 계산
            text_x = int((frame.shape[1] - text_size[0]) / 2)
            text_y = 80  # 화면 상단에서 약간 아래

            # 텍스트 배경 박스 (선택 사항)
            cv2.rectangle(frame, 
                        (text_x - 10, text_y - text_size[1] - 10), 
                        (text_x + text_size[0] + 10, text_y + 10), 
                        (0, 255, 255), 
                        cv2.FILLED)

            # SMILE 메시지 출력
            cv2.putText(frame, smile_text, (text_x, text_y), font, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)

        # 사용자 이름과 정확도 결과 출력 ---⑧
        txt, base = cv2.getTextSize(msg, cv2.FONT_HERSHEY_PLAIN, 1, 3)
        cv2.rectangle(frame, (x,y-base-txt[1]), (x+txt[0], y+txt[1]), \
                    (0,255,255), -1)
        cv2.putText(frame, msg, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, \
                    (200,200,200), 2,cv2.LINE_AA)
    cv2.imshow('Face Recognition', frame)
    if cv2.waitKey(1) == 27: #esc 
        break
cap.release()
cv2.destroyAllWindows()     