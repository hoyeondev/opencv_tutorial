import cv2

# 얼굴 검출용 Haar Cascade 분류기 로드
face_cascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_default.xml')

# 카메라 캡쳐 활성화
cap = cv2.VideoCapture(0)
rate = 15  # 모자이크 정도를 설정하는 비율 (숫자가 클수록 더 뭉개짐)

while cap.isOpened():
    ret, img = cap.read()
    
    if not ret:
        break

    img = cv2.flip(img, 1)  # 좌우 반전
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(80,80))

    for (x, y, w, h) in faces:
        # 얼굴 영역만 추출
        roi = img[y:y+h, x:x+w]

        # 얼굴 영역 축소 → 확대하여 모자이크 효과
        small = cv2.resize(roi, (w // rate, h // rate))
        mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_AREA)

        # 원본 이미지에 모자이크 영역 덮어쓰기
        img[y:y+h, x:x+w] = mosaic

    cv2.imshow('Face Mosaic', img)

    if cv2.waitKey(5) == 27:  # ESC 키 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
