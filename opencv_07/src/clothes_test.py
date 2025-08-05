import cv2
import numpy as np
import pandas as pd
from collections import deque
import matplotlib.pyplot as plt

'''
웹캠으로 촬영한 옷의 종류를 K-NN 알고리즘으로 자동 분류
- 프로그램 종료 : ESC
- roi 크기 조정 : -, +
'''


# ---------------------------
# 1. 데이터 로드 및 KNN 학습
# ---------------------------
def load_color_dataset(csv_path='color_dataset.csv'):
    """CSV 파일에서 데이터를 로드하고, HSV 값과 라벨을 반환합니다."""
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"오류: '{csv_path}' 파일을 찾을 수 없습니다. 먼저 샘플을 수집해주세요.")
        return None, None
    
    # 'H', 'S', 'V' 컬럼이 이미 존재한다고 가정합니다.
    X = df[['H', 'S', 'V']].values.astype(np.float32)
    y = df['Label'].values
    
    # 정규화 (학습 데이터와 동일하게)
    # H(0-180), S(0-255), V(0-255)의 범위를 0-1로 정규화
    X[:, 0] /= 180.0
    X[:, 1] /= 255.0
    X[:, 2] /= 255.0
    
    return X, y

X, y = load_color_dataset()
if X is None:
    exit()

# 라벨 → 숫자 변환 (KNN은 숫자 라벨 필요)
labels_unique = np.unique(y)
label_to_int = {name: idx for idx, name in enumerate(labels_unique)}
int_to_label = {idx: name for name, idx in label_to_int.items()}

y_numeric = np.array([label_to_int[label] for label in y])

# KNN 학습
knn = cv2.ml.KNearest_create()
knn.train(X, cv2.ml.ROW_SAMPLE, y_numeric)

# ---------------------------
# 2. ROI 초기값 설정
# ---------------------------
roi_w, roi_h = 100, 100
roi_x, roi_y = 250, 150  # 기본 위치
dragging = False

# 예측 히스토리 (최근 10개)
history = deque(maxlen=10)

# ---------------------------
# 3. ROI 이동/크기 조절 콜백
# ---------------------------
def mouse_callback(event, x, y, flags, param):
    global roi_x, roi_y, dragging
    if event == cv2.EVENT_LBUTTONDOWN:
        if roi_x <= x <= roi_x + roi_w and roi_y <= y <= roi_y + roi_h:
            dragging = True
    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        roi_x, roi_y = x - roi_w // 2, y - roi_h // 2
    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False

# ---------------------------
# 4. 웹캠 열기
# ---------------------------
cap = cv2.VideoCapture(0)
cv2.namedWindow('Cloth Detection')
cv2.setMouseCallback('Color Detection', mouse_callback)

# ---------------------------
# 5. 메인 루프
# ---------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1) # 좌우반전
    # ROI 좌표 안전하게 제한
    roi_x = max(0, min(frame.shape[1] - roi_w, roi_x))
    roi_y = max(0, min(frame.shape[0] - roi_h, roi_y))

    roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
    
    # BGR -> HSV 변환
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # HSV ROI의 평균 계산
    avg_hsv = np.mean(hsv_roi.reshape(-1, 3), axis=0).astype(np.float32)

    # 예측 샘플 정규화 (학습 데이터와 동일하게)
    normalized_sample = avg_hsv.copy()
    normalized_sample[0] /= 180.0
    normalized_sample[1] /= 255.0
    normalized_sample[2] /= 255.0

    # KNN 예측
    sample = normalized_sample.reshape(1, -1)
    ret, result, neighbours, dist = knn.findNearest(sample, k=3) # 정확도 측정값 기반
    predicted_idx = int(result[0][0])
    predicted_label = int_to_label[predicted_idx]
    
    # 신뢰도 계산
    counts = np.bincount(neighbours.astype(int).flatten(), minlength=len(labels_unique))
    probs = counts / counts.sum()

    # 히스토리 저장
    history.append(predicted_label)
    # print('history : ', history)

    # ROI와 결과 표시
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
    cv2.putText(frame, f"Cloth : {predicted_label}", (roi_x, roi_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow('Color Detection', frame)

    # ---------------------------
    # 6. 신뢰도 바 차트 시각화
    # ---------------------------
    plt.clf()
    plt.bar(labels_unique, probs * 100, color='skyblue')
    plt.title('Prediction Probabilities')
    plt.ylabel('Confidence (%)')
    plt.xticks(rotation=45)
    plt.pause(0.01)

    # 키 이벤트 처리
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('+'):  # ROI 크기 증가
        roi_w += 10
        roi_h += 10
    elif key == ord('-'):  # ROI 크기 감소
        roi_w = max(20, roi_w - 10)
        roi_h = max(20, roi_h - 10)

cap.release()
cv2.destroyAllWindows()
plt.close('all')