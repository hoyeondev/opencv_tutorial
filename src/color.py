import cv2
import numpy as np

# 기본값
img = cv2.imread('../img/like_lenna.png')
# bgr
bgr = cv2.imread('../img/like_lenna.png', cv2.IMREAD_COLOR)

# IMREAD_UNCHANGED 옵션
bgra = cv2.imread('../img/like_lenna.png', cv2.IMREAD_UNCHANGED)

# shape
print('default', img.shape, 'color', bgr.shape, 'unchanged', bgra.shape)

cv2.imshow('img', img)
cv2.imshow('bgr', bgr)

# 알파 채널만 표시
# 전경과 배경을 쉽게 분리해서 볼 수 있습니다.
# 이런 이유로 알파 채널은 마스크 채널(mask channel)이라고도 부름
cv2.imshow('bgra', bgra[:,:,3])

cv2.waitKey(0)
cv2.destroyAllWindows()