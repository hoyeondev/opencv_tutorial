# 색상 이미지 히스토그램

import cv2
import numpy as np
import matplotlib.pylab as plt

# 1. 이미지 읽기 및 출력
img = cv2.imread('../img/mountain.jpg')
cv2.imshow('Mountain', img)

channels = cv2.split(img)
colors = ('b', 'g', 'r')

# 2. 히스토그램 계산 및 그리기
for (ch, color) in zip(channels, colors):
    hist = cv2.calcHist([ch], [0], None, [256], [0, 256])
    plt.plot(hist, color=color)
plt.show()