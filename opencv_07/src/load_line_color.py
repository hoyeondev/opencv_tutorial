import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 경로
img_path = '../img/load_line.jpg'

# 이미지 읽기
img = cv2.imread(img_path)
if img is None:
    raise FileNotFoundError("이미지를 찾을 수 없습니다.")

# 가로 크기를 600으로 조정 (비율 유지)
target_width = 600
scale = target_width / img.shape[1]
resized_img = cv2.resize(img, (target_width, int(img.shape[0] * scale)))

# ---------------------------
# ROI 선택 (리사이즈된 이미지 기준)
# ---------------------------
x, y, w, h = cv2.selectROI("Select ROI", resized_img, False)
cv2.destroyWindow("Select ROI")

if w == 0 or h == 0:
    raise ValueError("ROI가 선택되지 않았습니다.")

# ROI 좌표를 원본 이미지 비율로 변환
orig_x = int(x / scale)
orig_y = int(y / scale)
orig_w = int(w / scale)
orig_h = int(h / scale)

roi = img[orig_y:orig_y+orig_h, orig_x:orig_x+orig_w]
roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

# ---------------------------
# 1. HSV 변환 및 데이터 준비
# ---------------------------
roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
data = roi_hsv.reshape((-1, 3)).astype(np.float32)

# ---------------------------
# 2. K-means 적용 (대표 색상 4개)
# ---------------------------
K = 4
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
ret, labels, centers_hsv = cv2.kmeans(data, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# HSV 중심값을 BGR로 변환
centers_bgr = cv2.cvtColor(np.uint8([centers_hsv]), cv2.COLOR_HSV2BGR)[0]

# 레이블 평탄화
labels = labels.flatten()

# ---------------------------
# 3. 클러스터링 이미지 생성 (BGR 기반)
# ---------------------------
res = centers_bgr[labels]
clustered_img = res.reshape((roi.shape))
clustered_img_rgb = cv2.cvtColor(clustered_img, cv2.COLOR_BGR2RGB)

# ---------------------------
# 4. 대표 색상 분석
# ---------------------------
counts = np.bincount(labels)
ratios = counts / sum(counts)

print("\n[대표 색상 상세 분석]")
for i, (color, cnt, ratio) in enumerate(zip(centers_bgr, counts, ratios)):
    print(f"색상 {i+1}: BGR={tuple(int(c) for c in color)}, 픽셀 수={cnt}, 비율={ratio*100:.2f}%")

# ---------------------------
# 5. 팔레트 생성
# ---------------------------
palette_height = 50
palette = np.zeros((palette_height, img.shape[1], 3), dtype=np.uint8)
start = 0
for color, ratio in zip(centers_bgr, ratios):
    end = start + int(ratio * img.shape[1])
    palette[:, start:end, :] = color
    start = end

# ---------------------------
# 6. 시각화 (Matplotlib)
# ---------------------------
fig = plt.figure(figsize=(10, 8))

# (1) 원본 ROI + 클러스터링 결과 병합
merged = np.hstack((roi_rgb, clustered_img_rgb))
ax1 = fig.add_subplot(3, 1, 1)
ax1.imshow(merged)
ax1.set_title('Original ROI + Clustered Image (HSV-based)')
ax1.axis('off')

# (2) 색상 팔레트
ax2 = fig.add_subplot(3, 1, 2)
ax2.imshow(cv2.cvtColor(palette, cv2.COLOR_BGR2RGB))
ax2.set_title('Color Palette (Top 4 Colors)')
ax2.axis('off')

# (3) 색상 비율 바 차트
ax3 = fig.add_subplot(3, 1, 3)
colors_rgb = [tuple(map(lambda x: x / 255, c[::-1])) for c in centers_bgr]  # BGR → RGB
bars = ax3.bar(range(K), ratios * 100, color=colors_rgb)
ax3.set_xticks(range(K))
ax3.set_xticklabels([f'Color {i+1}' for i in range(K)])
ax3.set_ylabel('Percentage (%)')
ax3.set_title('Color Distribution')

# 막대 내부 텍스트 추가
for i, bar in enumerate(bars):
    bgr = tuple(int(c) for c in centers_bgr[i])
    pixel_count = counts[i]
    ratio_percent = ratios[i] * 100
    text = f"BGR={bgr}\n{pixel_count} px\n{ratio_percent:.2f}%"
    ax3.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() / 2,
        text,
        ha='center',
        va='center',
        fontsize=9,
        color='white' if bar.get_height() > 20 else 'black'
    )

plt.tight_layout()
plt.show()
