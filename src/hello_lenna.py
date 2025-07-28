import cv2
import numpy as np
import random
import time

new_height = 500
new_width = 500

image = cv2.imread('../img/like_lenna.png') # 이미지 로드

# 이미지 크기조정
dst = cv2.resize(image, (500, 500))

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


# 랜덤하게 별 그리기
# 1. 별 기본 좌표 (10개 점)
star_points = np.array([
    [250, 100], [280, 190], [370, 190], [300, 250],
    [320, 340], [250, 280], [180, 340], [200, 250],
    [130, 190], [220, 190]
], np.float32)

# 2. 별 5개 랜덤으로 그리기
for _ in range(10):
    # 랜덤 크기 (작게)
    scale = random.uniform(0.1, 0.3)
    points = star_points * scale

    # 랜덤 위치 (이미지 범위 내)
    move_x = random.randint(0, new_width - int(370 * scale))
    move_y = random.randint(0, new_height - int(340 * scale))
    points[:, 0] += move_x # 모든 x좌표에 move_x를 더함
    points[:, 1] += move_y # 모든 y좌표에 move_y를 더함

    # 정수 변환
    points = points.astype(np.int32).reshape((-1, 1, 2))

    # 랜덤 색상 (윤곽선 & 채우기 동일)
    color = random.choice([
        (0, 255, 255),   # 노란색
        (255, 255, 0),   # 밝은 노랑
        (0, 200, 255),   # 주황 계열
        (0, 255, 200),   # 청록 계열
        (255, 0, 255)    # 보라빛
    ])

    # 별 그리기 (채우기 + 윤곽선)
    cv2.fillPoly(dst, [points], color=color)
    cv2.polylines(dst, [points], isClosed=True, color=color, thickness=2)

    # 화면 갱신
    cv2.imshow('hello_lenna',dst)
    cv2.waitKey(1)  # OpenCV가 GUI 이벤트를 처리하게
    time.sleep(0.3) # 별이 나타나는 속도 (0.3초)

#cv2.imshow('hello_lenna',dst)

# 마지막 화면 유지
cv2.waitKey(0)
cv2.destroyAllWindows()