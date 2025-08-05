import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# 1. 데이터 전처리 및 학습/테스트 데이터 분할
def preprocess_and_split_data(file_path, test_size=0.2):
    """
    CSV 파일을 읽고 데이터를 전처리한 후 학습/테스트 데이터로 분할합니다.
    scikit-learn의 train_test_split 기능을 직접 구현합니다.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다. 먼저 색상 샘플을 수집해주세요.")
        return None, None, None, None

    # HSV 값을 H, S, V 열로 분리
    # df[['H', 'S', 'V']] = df['hsv'].str.strip('[]').str.split(',', expand=True).astype(float)
    
    # 정규화 (0-255 값을 0-1로)
    # H(0-180), S(0-255), V(0-255)의 범위를 0-1로 정규화
    df['H'] = df['H'] / 180.0
    df['S'] = df['S'] / 255.0
    df['V'] = df['V'] / 255.0

    # 특성(X)과 라벨(y) 분리
    X = df[['H', 'S', 'V']].values
    y = df['Label'].values
    
    # 데이터 인덱스를 섞기
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(X))
    X = X[shuffled_indices]
    y = y[shuffled_indices]

    # 학습/테스트 데이터 분할
    test_set_size = int(len(X) * test_size)
    X_train, X_test = X[test_set_size:], X[:test_set_size]
    y_train, y_test = y[test_set_size:], y[:test_set_size]
    
    print(f"총 데이터 수: {len(X)}")
    print(f"학습 데이터 수: {len(X_train)}")
    print(f"테스트 데이터 수: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test

# 2. K-NN 알고리즘 직접 구현
def euclidean_distance(x1, x2):
    """두 벡터(픽셀) 사이의 유클리드 거리를 계산합니다."""
    return np.sqrt(np.sum((x1 - x2)**2))

class KNN:
    """K-NN 분류기 클래스입니다."""
    def __init__(self, k=3):
        self.k = k

    def fit(self, X_train, y_train):
        """학습 데이터를 저장합니다."""
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test):
        """테스트 데이터에 대한 예측을 수행합니다."""
        y_pred = [self._predict_single_point(x) for x in X_test]
        return np.array(y_pred)

    def _predict_single_point(self, x_test):
        """테스트 데이터의 한 점에 대해 예측합니다."""
        # 훈련 데이터와의 모든 거리 계산
        distances = [euclidean_distance(x_test, x_train) for x_train in self.X_train]

        # 거리가 가장 가까운 k개의 이웃 찾기
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]

        # 가장 많은 표를 얻은 라벨 반환 (다수결)
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

# 3. 모델 성능 평가 함수 직접 구현
def calculate_accuracy(y_true, y_pred):
    """정확도를 계산합니다."""
    return np.sum(y_true == y_pred) / len(y_true)

def plot_confusion_matrix(y_true, y_pred, labels):
    """혼동 행렬을 시각화합니다."""
    # 유니크한 라벨을 기준으로 혼동 행렬 생성
    unique_labels = sorted(list(set(labels)))
    cm = np.zeros((len(unique_labels), len(unique_labels)), dtype=int)
    label_to_index = {label: i for i, label in enumerate(unique_labels)}
    
    for true_label, pred_label in zip(y_true, y_pred):
        true_idx = label_to_index[true_label]
        pred_idx = label_to_index[pred_label]
        cm[true_idx, pred_idx] += 1
        
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(len(unique_labels))
    plt.xticks(tick_marks, unique_labels, rotation=45)
    plt.yticks(tick_marks, unique_labels)

    fmt = 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], fmt),
                     ha="center", va="center",
                     color="white" if cm[i, j] > thresh else "black")
    
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.show()

# 메인 실행 부분
if __name__ == '__main__':
    # 1. 데이터 전처리 및 분할
    X_train, X_test, y_train, y_test = preprocess_and_split_data('color_dataset.csv')
    
    if X_train is not None:
        # 2. 최적 K값 탐색 및 모델 학습
        k_values = [3, 5, 7, 9]
        accuracies = []

        for k in k_values:
            print(f"\n--- K={k}으로 모델 학습 ---")
            knn_model = KNN(k=k)
            knn_model.fit(X_train, y_train)
            y_pred = knn_model.predict(X_test)
            
            accuracy = calculate_accuracy(y_test, y_pred)
            accuracies.append(accuracy)
            print(f"K={k}일 때 정확도: {accuracy:.4f}")

        best_k = k_values[np.argmax(accuracies)]
        print(f"\n가장 높은 정확도를 보인 최적의 K값: {best_k} (정확도: {max(accuracies):.4f})")
        
        # 3. 최종 모델 성능 평가
        print("\n--- 최종 모델 성능 평가 (K={}) ---".format(best_k))
        final_knn_model = KNN(k=best_k)
        final_knn_model.fit(X_train, y_train)
        y_pred_final = final_knn_model.predict(X_test)
        
        final_accuracy = calculate_accuracy(y_test, y_pred_final)
        print(f"최종 모델 정확도: {final_accuracy:.4f}")
        
        # 각 색상별 분류 성능 분석을 위한 혼동 행렬 시각화
        all_labels = sorted(list(set(y_train) | set(y_test)))
        plot_confusion_matrix(y_test, y_pred_final, all_labels)