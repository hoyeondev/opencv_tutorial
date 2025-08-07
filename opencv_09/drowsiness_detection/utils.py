from scipy.spatial import distance

def calculate_ear_from_landmarks(landmarks, eye_indices):
    """
    눈의 EAR 계산
    :param landmarks: 얼굴 전체 68개 랜드마크 좌표
    :param eye_indices: 왼쪽 또는 오른쪽 눈의 인덱스 (6개)
    :return: EAR 값
    """
    eye = [landmarks[i] for i in eye_indices]
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear
