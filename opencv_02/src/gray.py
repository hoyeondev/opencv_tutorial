# BGR 색상 이미지를 회색조 이미지로 변환

import cv2
import numpy as np

img = cv2.imread('../img/like_lenna.png')

# 계산하는 방법
img2 = img.astype(np.uint16) # astype를 이용하여 uint16로 변환
b,g,r = cv2.split(img2) # 채널별로 분류
gray1 = ((b+g+r)/3).astype(np.uint8) # 평균값을 이용한 그레이스케일 변환

# 함수사용하는 방법
gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # BGR에서 그레이스케일로 변환


cv2.imshow('original', img)
cv2.imshow('gray1', gray1)
cv2.imshow('gray2', gray2)

cv2.waitKey(0)
cv2.destroyAllWindows()