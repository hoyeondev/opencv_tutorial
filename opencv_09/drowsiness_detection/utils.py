from scipy.spatial import distance as dist


def calculate_ear_from_landmarks(eye):
    """
    눈의 EAR 계산
    :param landmarks: 얼굴 전체 68개 랜드마크 좌표
    :param eye_indices: 왼쪽 또는 오른쪽 눈의 인덱스 (6개)
    :return: EAR 값
    """
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear