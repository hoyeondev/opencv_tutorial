import cv2

# 얼굴 검출용 Haar Cascade 분류기 로드
face_cascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_default.xml')

# 카메라 캡쳐 활성화
cap = cv2.VideoCapture(0)
rate = 15  # 모자이크 정도를 설정하는 비율 (숫자가 클수록 더 뭉개짐)

use_mosaic = True  # 모자이크 적용 여부 초기값

while cap.isOpened():
    ret, img = cap.read()
    
    if not ret:
        break

    img = cv2.flip(img, 1)  # 좌우 반전
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(80,80))

    for (x, y, w, h) in faces:
        if use_mosaic:
            # 모자이크 처리
            roi = img[y:y+h, x:x+w]
            small = cv2.resize(roi, (w // rate, h // rate))
            mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_AREA)
            img[y:y+h, x:x+w] = mosaic
        else:
            # 사각형만 그림
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 안내 텍스트 표시
    cv2.putText(img, "ESC: Exit", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(img, "ENTER: Toggle Mosaic", (10, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Face Mosaic', img)

    key = cv2.waitKey(5) & 0xFF
    if key == 27:  # ESC 키
        break
    elif key == 13:  # Enter 키
        use_mosaic = not use_mosaic  # 모자이크 적용 여부 전환

cap.release()
cv2.destroyAllWindows()
