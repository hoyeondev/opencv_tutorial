import cv2
import numpy as np
import matplotlib.pyplot as plt

# ------------------- 초기 세팅 -------------------
# 0번 카메라 연결
cap = cv2.VideoCapture(0)
# 해상도 설정 (640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

plt.ion()
fig, ax = plt.subplots()

# 히스토그램
def plot_histogram(gray_img):
    ax.clear()
    hist = cv2.calcHist([gray_img], [0], None, [256], [0,256])
    ax.plot(hist, color='black')
    ax.set_xlim([0, 256])
    ax.set_xlabel('Pixel value')
    ax.set_ylabel('Frequency')
    ax.set_title('Grayscale Histogram')
    plt.draw()
    plt.pause(0.001)

# -------------------------------------------------

if cap.isOpened():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("no frame")
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 오츠 알고리즘으로 임계값 자동 계산
        # otsu_thresh_val, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # 히스토그램 표시
        plot_histogram(gray)

        # 결과 표시
        cv2.imshow('Original', frame)
        cv2.imshow('Gray', gray)
        # cv2.imshow(f'Binary Threshold (Otsu: {otsu_thresh_val:.2f})', binary)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
plt.close()
