import cv2
import numpy as np

#--① 이미지 불러오기
img1 = cv2.imread('../img/cat_chromakey.jpg')  # 고양이 이미지
img2 = cv2.imread('../img/forest.jpg')        # 자연 배경 이미지

#--② 크기 조정 (배경 크기 800x600)
img2 = cv2.resize(img2, (800, 600))

# 고양이 이미지 비율 유지하며 크기 조정
cat_width = 300
scale = cat_width / img1.shape[1]
cat_height = int(img1.shape[0] * scale)
img1 = cv2.resize(img1, (cat_width, cat_height))

#--③ ROI 선택을 위한 좌표 계산 (중앙 하단에 배치)
height1, width1 = img1.shape[:2]
height2, width2 = img2.shape[:2]
x = (width2 - width1) // 2
y = height2 - height1
w = x + width1
h = y + height1

#--④ 크로마키 배경 영역 지정 (10픽셀 영역 사용)
chromakey = img1[:10, :10, :]  # 고양이 이미지 상단 왼쪽 작은 영역
offset = 20  # HSV H 범위 여유 값

#--⑤ HSV 변환
hsv_chroma = cv2.cvtColor(chromakey, cv2.COLOR_BGR2HSV)
hsv_img = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

#--⑥ 크로마키 영역의 H값에서 offset 만큼 여유를 두어 범위 지정
chroma_h = hsv_chroma[:, :, 0]  # H 채널
lower = np.array([max(chroma_h.min() - offset, 0), 80, 80])
upper = np.array([min(chroma_h.max() + offset, 179), 255, 255])

#--⑦ 마스크 생성
mask = cv2.inRange(hsv_img, lower, upper)
mask_inv = cv2.bitwise_not(mask)

#--⑧ ROI 설정
roi = img2[y:h, x:w]

#--⑨ 합성 (고양이 전경 + 배경 ROI)
fg = cv2.bitwise_and(img1, img1, mask=mask_inv)
bg = cv2.bitwise_and(roi, roi, mask=mask)
added = fg + bg
img2[y:h, x:w] = added

#--⑩ 결과 출력
cv2.imshow('chromakey', img1)
cv2.imshow('added', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
