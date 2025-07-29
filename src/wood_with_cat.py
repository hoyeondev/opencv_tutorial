import cv2
import numpy as np
import random

#--- 이미지 불러오기
cat1 = cv2.imread('../img/cat1.jpg')
cat2 = cv2.imread('../img/cat2.jpg')
cat3 = cv2.imread('../img/cat3.jpg')
bg = cv2.imread('../img/forest.jpg')

#--- 배경 크기 조정
bg = cv2.resize(bg, (800, 600))

#--- 크로마키 마스크 생성 함수
def create_mask(img, offset=20):
    # HSV 변환
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    chromakey = img[:10, :10, :]  # 좌상단 샘플
    hsv_chroma = cv2.cvtColor(chromakey, cv2.COLOR_BGR2HSV)

    # H 값 기반 범위 설정
    chroma_h = hsv_chroma[:, :, 0]
    lower = np.array([max(chroma_h.min() - offset, 0), 80, 80])
    upper = np.array([min(chroma_h.max() + offset, 179), 255, 255])

    mask = cv2.inRange(hsv_img, lower, upper)
    mask_inv = cv2.bitwise_not(mask)
    return mask, mask_inv

#--- 크로마키 합성 함수
def chroma_add(bg, fg, x, y):
    h, w = fg.shape[:2]
    roi = bg[y:y+h, x:x+w]
    mask, mask_inv = create_mask(fg)
    fg_part = cv2.bitwise_and(fg, fg, mask=mask_inv)
    bg_part = cv2.bitwise_and(roi, roi, mask=mask)
    combined = cv2.add(fg_part, bg_part)
    bg[y:y+h, x:x+w] = combined

#--- 메인 처리: 랜덤으로 고양이 추가
for _ in range(5):
    # 랜덤으로 cat1 또는 cat2 선택
    cat_img = random.choice([cat1, cat2, cat3])

    # 크기 조정: cat1은 300픽셀, cat2는 100픽셀로 조정
    if cat_img is cat1 or cat_img is cat3:
        new_width = 300  # cat1은 300픽셀
    else:
        new_width = 100

    scale = new_width / cat_img.shape[1]
    new_height = int(cat_img.shape[0] * scale)
    resized_cat = cv2.resize(cat_img, (new_width, new_height))

    # 랜덤 위치 계산 (ROI가 배경 안에 들어가도록)
    max_x = bg.shape[1] - new_width
    #max_y = bg.shape[0] - new_height
    
    x = random.randint(0, max_x)
    #y = random.randint(0, max_y)

    y_min = bg.shape[0] - int(bg.shape[0] * 0.4)
    y_max = bg.shape[0] - new_height
    y = random.randint(y_min, y_max)

    # 합성
    chroma_add(bg, resized_cat, x, y)

#--- 결과 출력
cv2.imshow('Result', bg)
cv2.waitKey(0)
cv2.destroyAllWindows()
