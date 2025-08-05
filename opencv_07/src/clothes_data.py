import cv2
import numpy as np
import pandas as pd
import os

# 1. 분류할 옷 색상 정의 및 라벨 매핑
# 숫자 키(49~55)와 색상 이름, 그리고 해당 색상을 화면에 표시할 BGR 값
# 이 BGR 값은 화면에 라벨을 표시할 때 사용합니다.
label_map = {
    49: ('CAP', (0, 0, 255)),       # 1번 키
    50: ('T-shirt', (255, 0, 0)),      # 2번 키
    # 51: ('Green', (0, 255, 0)),     # 3번 키
    # 52: ('Yellow', (0, 255, 255)),  # 4번 키
    # 53: ('Black', (0, 0, 0)),       # 5번 키
    # 54: ('White', (255, 255, 255)), # 6번 키
    # 55: ('Gray', (128, 128, 128))   # 7번 키
}

# 2. 전역 변수
# 수집된 데이터를 저장할 리스트 (H, S, V, Label)
data = []
current_hsv = None

# 3. 마우스 클릭 이벤트 핸들러 작성
def mouse_event_handler(event, x, y, flags, param):
    """
    마우스 클릭 이벤트를 처리하여 클릭한 픽셀의 HSV 값을 추출합니다.
    """
    global current_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        # BGR 값을 HSV로 변환합니다.
        bgr_pixel = frame[y, x]
        hsv_pixel = cv2.cvtColor(np.uint8([[bgr_pixel]]), cv2.COLOR_BGR2HSV)[0][0]
        current_hsv = hsv_pixel
        print(f"클릭 위치: ({x}, {y}) | HSV 값: {current_hsv}")

def display_info(frame):
    """
    수집 과정에 필요한 정보를 화면에 실시간으로 표시합니다.
    """
    info_text = [
        f"Data points: {len(data)}",
        f"Last HSV: {current_hsv}" if current_hsv is not None else "Last HSV: N/A",
        "--- Press a number key (1-7) to label ---"
    ]
    
    y_offset = 30
    for text in info_text:
        cv2.putText(frame, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        y_offset += 30

    y_offset += 10
    for key_code, (name, color) in label_map.items():
        key_char = chr(key_code)
        # 텍스트 색상을 해당 라벨의 BGR 값으로 지정
        text_color = (0, 0, 0) if name in ['White', 'Yellow'] else (255, 255, 255)
        cv2.putText(frame, f"{key_char}: {name}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2, cv2.LINE_AA)
        y_offset += 30
        
    cv2.putText(frame, "Press 's' to save data, 'q' to quit", (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

# 4. 웹캠 연결 및 데이터 수집 루프
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("웹캠을 열 수 없습니다. 카메라 연결 상태를 확인해주세요.")

window_name = "Color Sample Collector"
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, mouse_event_handler)

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break
        
        frame = cv2.flip(frame, 1) # 좌우반전
        display_info(frame)
        cv2.imshow(window_name, frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # 숫자 키로 라벨 지정
        if key in label_map:
            if current_hsv is not None:
                label_name = label_map[key][0]
                data.append(list(current_hsv) + [label_name])
                print(f"[{label_name}] 라벨로 데이터 추가: {current_hsv}")
                current_hsv = None
            else:
                print("먼저 마우스로 색상을 클릭해주세요.")
        
        # 's' 키를 눌러 데이터 저장
        elif key == ord('s'):
            if data:
                # 데이터 프레임 생성 및 CSV 파일로 저장
                df = pd.DataFrame(data, columns=['H', 'S', 'V', 'Label'])
                file_path = 'color_dataset.csv'
                df.to_csv(file_path, index=False)
                print(f"데이터가 {file_path}에 성공적으로 저장되었습니다.")
            else:
                print("저장할 데이터가 없습니다.")
        
        # 'q' 키를 눌러 종료
        elif key == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()