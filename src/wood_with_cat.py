import cv2
import numpy as np

bg = cv2.imread('../img/forest.jpg')
cat = cv2.imread('../img/cat_chromakey.jpg')

# 배경 크기 조정
bg = cv2.resize(bg, (800, 600))

# 고양이 크기 줄이기 (예: 가로 300픽셀)
cat_width = 300
scale = cat_width / cat.shape[1]
cat_height = int(cat.shape[0] * scale)
cat = cv2.resize(cat, (cat_width, cat_height))

# 1. 고양이 그레이스케일 변환
gray = cv2.cvtColor(cat, cv2.COLOR_BGR2GRAY)

# 2. Threshold로 마스크 생성
_, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
mask_inv = cv2.bitwise_not(mask)

# 3. 고양이를 배치할 좌표 (예: 오른쪽 아래)
x_offset = bg.shape[1] - cat.shape[1] - 20
y_offset = bg.shape[0] - cat.shape[0] - 20

# 4. ROI 영역 추출
roi = bg[y_offset:y_offset+cat.shape[0], x_offset:x_offset+cat.shape[1]]

# 5. 마스크 적용
bg_region = cv2.bitwise_and(roi, roi, mask=mask_inv)
cat_fg = cv2.bitwise_and(cat, cat, mask=mask)

# 6. 합성
dst = cv2.add(bg_region, cat_fg)
bg[y_offset:y_offset+cat.shape[0], x_offset:x_offset+cat.shape[1]] = dst

cv2.imshow('Result', bg)
cv2.waitKey(0)
cv2.destroyAllWindows()
