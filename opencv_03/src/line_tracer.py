import cv2

# 0번 카메라 연결
cap = cv2.VideoCapture(0)

# 해상도 설정 (640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if cap.isOpened():
    while True:
        ret, img = cap.read()  # 프레임 읽기
        if ret:
            img = cv2.flip(img, 1)  # 좌우 반전
            cv2.imshow('camera', img)

            # 'q' 키로 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print('no frame')
            break
else:
    print("can't open camera.")

cap.release()  # 자원 반납
cv2.destroyAllWindows()
