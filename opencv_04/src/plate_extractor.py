# 마우스와 원근 변환으로 문서 스캔 효과 내기 (perspective_scan.py)

import cv2
import numpy as np
import os

# 저장할 폴더
save_dir = "../extracted_plates"
os.makedirs(save_dir, exist_ok=True)  # 폴더 없으면 생성
file_count = 0  # 파일 이름을 위한 카운터

win_name = "License Plate Extractor"
# img = cv2.imread("../img/car_02.jpg")
# ../img/ 폴더 내에 있는 'car_'로 시작하는 이미지 파일을 읽어오기
for file in os.listdir("../img/"):
    if file.startswith("car_") and file.endswith(".jpg"):
        img = cv2.imread(os.path.join("../img/", file))
        break

rows, cols = img.shape[:2]
draw = img.copy() # 점을 그릴 이미지 복사본
pts_cnt = 0 # 클릭한 점의 개수
pts = np.zeros((4,2), dtype=np.float32) # 클릭한 점의 좌표를 저장할 배열


def onMouse(event, x, y, flags, param):  #마우스 이벤트 콜백 함수 구현 ---① 
    global  pts_cnt                     # 마우스로 찍은 좌표의 갯수 저장
    if event == cv2.EVENT_LBUTTONDOWN:  # 좌클릭 이벤트
        cv2.circle(draw, (x,y), 10, (0,255,0), -1) # 좌표에 초록색 동그라미 표시
        cv2.imshow(win_name, draw)

        pts[pts_cnt] = [x,y]            # 마우스 좌표 저장
        pts_cnt+=1
        if pts_cnt == 4:                       # 좌표가 4개 수집됨 
            # 좌표 4개 중 상하좌우 찾기 ---② 
            sm = pts.sum(axis=1)                 # 4쌍의 좌표 각각 x+y 계산
            diff = np.diff(pts, axis = 1)       # 4쌍의 좌표 각각 x-y 계산

            topLeft = pts[np.argmin(sm)]         # x+y가 가장 값이 좌상단 좌표
            bottomRight = pts[np.argmax(sm)]     # x+y가 가장 큰 값이 우하단 좌표
            topRight = pts[np.argmin(diff)]     # x-y가 가장 작은 것이 우상단 좌표
            bottomLeft = pts[np.argmax(diff)]   # x-y가 가장 큰 값이 좌하단 좌표

            # 변환 전 4개 좌표 
            pts1 = np.float32([topLeft, topRight, bottomRight , bottomLeft])

            # 변환 후 좌표 (비율 유지한 원본 크기)
            width = 300
            height = 150
            pts2 = np.float32([[0, 0], [width - 1, 0],
                               [width - 1, height - 1], [0, height - 1]])

            # 변환 행렬 계산 & 원근 변환
            mtrx = cv2.getPerspectiveTransform(pts1, pts2)
            result = cv2.warpPerspective(img, mtrx, (width, height))

            # 결과 이미지 출력
            cv2.imshow('scanned', result)

            # 저장 (PNG 형식)
            existing_files = len(os.listdir("../extracted_plates/"))
            filename = f"extracted_plates/plate_{existing_files+1:03d}.png"

            cv2.imwrite(filename, result)
            print(f"Saved: {filename}")


# for 문으로 이미지 파일 읽어오기
for car in img:
    cv2.imshow(win_name, img)  # 원본 이미지 출력
    cv2.setMouseCallback(win_name, onMouse)  # 마우스 콜백 함수 등록 ---③
    cv2.waitKey(0)  # 키 입력 대기
    draw = img.copy()  # 다음 이미지 클릭을 위해 draw 초기화

# cv2.imshow(win_name, img)
# cv2.setMouseCallback(win_name, onMouse)    # 마우스 콜백 함수를 GUI 윈도우에 등록 ---④
# cv2.waitKey(0)
cv2.destroyAllWindows()