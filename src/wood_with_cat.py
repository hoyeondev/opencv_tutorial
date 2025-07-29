import cv2
import numpy as np


# 숲 위에 있는 고양이 이미지와 배경 합성하기

bg = cv2.imread('forest.jpg')
cat = cv2.imread('고양이.png')

# 1. 고양이 이미지를 그레이스케일로 변환


# 2. Threshold로 마스크 생성


# 3. 마스크 반전 (고양이 영역만)

# 4. 배경과 고양이 분리


# 5. 합성


# 실행
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()