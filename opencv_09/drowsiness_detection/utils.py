import numpy as np

def calculate_ear_from_landmarks(landmarks, eye_indices):
    """
    눈의 EAR 계산
    :param landmarks: 얼굴 전체 68개 랜드마크 좌표
    :param eye_indices: 왼쪽 또는 오른쪽 눈의 인덱스 (6개)
    :return: EAR 값
    """
    # landmarks: [[(x0, y0), ..., (x67, y67)]] 형태라면 먼저 꺼낸다
    if isinstance(landmarks[0], tuple):  # [(x0, y0), ...] 형태인 경우
        pts = landmarks
    else:
        pts = landmarks[0]  # [[(x, y), ...]] 형태면 한 단계 풀기

    # 필요한 눈 좌표 추출
    eye = [pts[i] for i in eye_indices]

    # EAR 계산 공식 적용
    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))  # |p2 - p6|
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))  # |p3 - p5|
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))  # |p1 - p4|

    ear = (A + B) / (2.0 * C)
    return ear
