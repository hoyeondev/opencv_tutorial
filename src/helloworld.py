import cv2

image = cv2.imread('../img/like_lenna.png') # 이미지 로드
cv2.imshow('img',image) # 이미지 출력
cv2.waitKey(0)
cv2.destroyAllwindows()