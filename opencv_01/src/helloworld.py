import cv2
import numpy as np

new_height = 300
new_width = 300



image = cv2.imread('../img/like_lenna.png') # 이미지 로드
image_small = cv2.resize(image, (100, 100)) # 이미지 크기 조정

#cv2.imshow('img',image) # 이미지 출력
#cv2.imshow('img', image_small) # 크기 조정된 이미지 출력
# 이미지 원래대로 크기 조정
dst = np.zeros((new_height, new_width,3), dtype=np.uint8)
cv2.resize(image, (new_width, new_height), dst=dst)
# cv2.imshow('dst',dst)

# cv2.imshow('crop',image[:100,:100]) # 이미지 자르기
# cv2.imshow('crop2',image[50:150,50:150]) # 이미지 자르기(위치 조정)

# 이미지 일부분을 자르고 출력
croped_image = image[50:150,50:150]
croped_image[:] = 200
cv2.imshow('crop3',image)

cv2.waitKey(0)
# cv2.destroyAllwindows()
cv2.destroyAllWindows()