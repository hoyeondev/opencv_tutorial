import cv2
import numpy as np
import random
import time

new_height = 500
new_width = 500

image = cv2.imread('../img/like_lenna.png') # 이미지 로드
image_small = cv2.resize(image, (100, 100)) # 이미지 크기 조정

#cv2.imshow('img',image) # 이미지 출력
#cv2.imshow('img', image_small) # 크기 조정된 이미지 출력
# 이미지 원래대로 크기 조정
dst = np.zeros((new_height, new_width,3), dtype=np.uint8)
cv2.resize(image, (new_width, new_height), dst=dst)

# 빨간색 선
cv2.line(dst, (260, 220), (280, 240), (0,0,230), 5)
cv2.line(dst, (280, 220), (300, 240), (0,0,230), 5)
cv2.line(dst, (300, 220), (320, 240), (0,0,230), 5)

# 파란색 원
cv2.circle(dst, (190, 250), 10, (255,0,0), -1)
# 노란색 원
cv2.circle(dst, (190, 240), 3, (0,255,255), -1)

# sarif + italic
cv2.putText(dst, "Hello Lenna", (50, 470), \
            cv2.FONT_HERSHEY_COMPLEX | cv2.FONT_ITALIC, 1, (0, 0, 0), 3) 




cv2.imshow('hello_lenna',dst)

# 마지막 화면 유지
cv2.waitKey(0)
cv2.destroyAllWindows()