import cv2
import numpy as np
import matplotlib.pyplot as plt

# ------------------- 초기 세팅 -------------------
# 0번 카메라 연결
cap = cv2.VideoCapture(0)
# 해상도 설정 (640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Matplotlib 실시간 업데이트 설정
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
        height, width, _ = frame.shape

        # === A4 용지 영역(ROI) 설정 ===
        # 화면 중앙에 A4 크기 비슷한 사각형 ROI 지정
        roi_x, roi_y = int(width * 0.2), int(height * 0.2)
        roi_w, roi_h = int(width * 0.6), int(height * 0.6)
        roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # === ROI 마스크 생성 ===
        mask = np.zeros((height, width), dtype=np.uint8)
        mask[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w] = 255  # ROI 부분만 흰색

        # 마스크 적용된 그레이 이미지
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # masked_gray = cv2.bitwise_and(gray, gray, mask=mask)

        # 스레스홀딩 적용
        # _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        # cv2.imshow('Binary Threshold', binary)

        # # 적응형 스레스홀딩 적용
        # adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        #                                         cv2.THRESH_BINARY_INV, 11, 2)
        # cv2.imshow('Adaptive Threshold', adaptive_thresh)


        # === 오츠 이진화 ===
        # otsu_thresh_val, binary = cv2.threshold(masked_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # === ROI 사각형 시각화 ===
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (0, 255, 0), 2)
        
        # === ROI 영역에서 중심 찾기 ===
        # ROI 영역을 그레이스케일로 변환
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)

        # 이진화된 이미지에서 중심 찾기
        # 모멘트 계산ㅉ
        M = cv2.moments(binary)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])  # 중심 X 좌표
            cy = int(M["m01"] / M["m00"])  # 중심 Y 좌표

            # 중심 표시
            cv2.circle(roi, (cx, cy), 5, (0, 0, 255), -1)
            

        # === 히스토그램 표시 (ROI 영역만) ===
        roi_gray = gray[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
        plot_histogram(roi_gray)

        # === 결과 표시 ===
        cv2.imshow('Original with ROI', frame)
        # cv2.imshow('Masked Gray', masked_gray)
        # cv2.imshow(f'Binary (Otsu: {otsu_thresh_val:.2f})', binary)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
plt.close()
