import cv2
import numpy as np
import matplotlib.pylab as plt

# Otsu's Thresholding : 이미지의 히스토그램을 분석하여 최적의 임계값을 자동으로 선택하는 기법
# Otsu 알고리즘은 이미지의 픽셀 값 분포를 기반으로 최적의 임계값을 계산하여 이진화를 수행한다.

# 이미지를 그레이 스케일로 읽기
img = cv2.imread('../img/like_lenna.png', cv2.IMREAD_GRAYSCALE) 
# 경계 값을 130으로 지정  ---①
_, t_130 = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)        
# 경계 값을 지정하지 않고 OTSU 알고리즘 선택 ---②
t, t_otsu = cv2.threshold(img, -1, 255,  cv2.THRESH_BINARY | cv2.THRESH_OTSU) 
print('otsu threshold:', t)                 # Otsu 알고리즘으로 선택된 경계 값 출력

imgs = {'Original': img, 't:130':t_130, 'otsu:%d'%t: t_otsu}
for i , (key, value) in enumerate(imgs.items()):
    plt.subplot(1, 3, i+1)
    plt.title(key)
    plt.imshow(value, cmap='gray')
    plt.xticks([]); plt.yticks([])

plt.show()