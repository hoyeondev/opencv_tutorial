import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 경로
img_path = '../img/load_line.jpg'

# 이미지 읽기
img = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# ---------------------------
# 1. 데이터 준비
# ---------------------------
data = img.reshape((-1, 3)).astype(np.float32)

# ---------------------------
# 2. K-means 적용 (대표 색상 3개)
# ---------------------------
K = 3
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
ret, labels, centers = cv2.kmeans(data, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# 중심값 정수형 변환 (대표 색상)
centers = np.uint8(centers)
labels = labels.flatten()

# 클러스터링 이미지 생성
res = centers[labels]
clustered_img = res.reshape((img.shape))

# ---------------------------
# 3. 대표 색상 팔레트 시각화
# ---------------------------
# 각 색상의 픽셀 수
counts = np.bincount(labels)

# 비율 계산
ratios = counts / sum(counts)

# 팔레트 이미지
palette_height = 50
palette = np.zeros((palette_height, img.shape[1], 3), dtype=np.uint8)

start = 0
for i, (color, ratio) in enumerate(zip(centers, ratios)):
    end = start + int(ratio * img.shape[1])
    palette[:, start:end, :] = color
    start = end

# ---------------------------
# 4. 상세 분석 출력
# ---------------------------
print("\n[대표 색상 상세 분석]")
for i, (color, cnt, ratio) in enumerate(zip(centers, counts, ratios)):
    print(f"색상 {i+1}: BGR={tuple(int(c) for c in color)}, 픽셀 수={cnt}, 비율={ratio*100:.2f}%")

# ---------------------------
# 5. 결과 시각화 (Matplotlib)
# ---------------------------
fig = plt.figure(figsize=(10, 8))

# (1) 원본 + 클러스터링 이미지 병합
merged = np.hstack((img_rgb, clustered_img))
ax1 = fig.add_subplot(3, 1, 1)
ax1.imshow(merged)
ax1.set_title('Original + Clustered Image')
ax1.axis('off')

# (2) 색상 팔레트
ax2 = fig.add_subplot(3, 1, 2)
ax2.imshow(cv2.cvtColor(palette, cv2.COLOR_BGR2RGB))
ax2.set_title('Color Palette (Top 3 Colors)')
ax2.axis('off')

# (3) 비율 바 차트
ax3 = fig.add_subplot(3, 1, 3)
colors_rgb = [tuple(map(lambda x: x/255, c[::-1])) for c in centers]  # BGR → RGB로 변환 후 0~1 범위
ax3.bar(range(K), ratios*100, color=colors_rgb)
ax3.set_xticks(range(K))
ax3.set_xticklabels([f'Color {i+1}' for i in range(K)])
ax3.set_ylabel('Percentage (%)')
ax3.set_title('Color Distribution')

plt.tight_layout()
plt.show()
