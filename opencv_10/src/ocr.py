import easyocr
import cv2
import matplotlib.pyplot as plt

# EasyOCR Reader 생성 (중국어 번체 + 영어)
reader = easyocr.Reader(['ch_tra', 'en'], gpu=False)

# 이미지 경로 및 로딩
img_path = '../img/chinese_tra.jpg'
img = cv2.imread(img_path)

# 이미지 색상 BGR → RGB 변환 및 출력
plt.figure(figsize=(8, 8))
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

result = reader.readtext(img_path)