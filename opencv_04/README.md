# 📌 이미지 이동(Translation), 확대/축소(Scaling), 회전(Rotation)
- 참고 : [내용](https://bkshin.tistory.com/entry/OpenCV-13-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%9D%B4%EB%8F%99Translation-%ED%99%95%EB%8C%80%EC%B6%95%EC%86%8CScaling-%ED%9A%8C%EC%A0%84Rotation)
- OpenCV는 `cv2.warpAffine()` 또는 `cv2.warpPerspective()`를 사용해 다양한 변환을 지원한다.
- Affine 변환은 평행선 유지, Perspective 변환은 투시 왜곡까지 가능

## ✔ 이미지 이동 (Translation)
이미지를 x축, y축 방향으로 평행 이동시킴
```python
import cv2
import numpy as np

img = cv2.imread('image.jpg')
rows, cols = img.shape[:2]

# 이동 변환 행렬 (x: 100px, y: 50px 이동)
M = np.float32([[1, 0, 100],
                [0, 1, 50]])

translated = cv2.warpAffine(img, M, (cols, rows))
```

## ✔ 확대/축소(Scaling)
이미지 크기를 변경 (배율 조정)

### 1. `cv2.resize()` 함수 사용
```python
# 0.5배 축소
small = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

# 2배 확대
large = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
```
### 2. `cv2.warpAffine()` : 보간법 활용
보간법 : 이미지 크기를 변경하거나 회전, 변형할 때 새로운 픽셀 값을 계산하는 방법

```python
# --① 0.5배 축소 변환 행렬
m_small = np.float32([[0.5, 0, 0],
                       [0, 0.5,0]])  
# --② 2배 확대 변환 행렬
m_big = np.float32([[2, 0, 0],
                     [0, 2, 0]])  

# --③ 보간법 적용 없이 확대 축소
dst1 = cv2.warpAffine(img, m_small, (int(height*0.5), int(width*0.5)))
dst2 = cv2.warpAffine(img, m_big, (int(height*2), int(width*2)))

# --④ 보간법 적용한 확대 축소
dst3 = cv2.warpAffine(img, m_small, (int(height*0.5), int(width*0.5)), \
                        None, cv2.INTER_AREA)
dst4 = cv2.warpAffine(img, m_big, (int(height*2), int(width*2)), \
                        None, cv2.INTER_CUBIC)
```

### 3. `cv2.resize()`와 `cv2.warpAffine()`의 차이

| 항목         | **cv2.resize()**                                      | **cv2.warpAffine()**     |
| ---------- | ----------------------------------------------------- | ------------------------ |
| **주요 기능**  | 단순 크기 변경 (확대/축소)                                      | 아핀 변환 (이동, 회전, 확대, 기울이기) |
| **입력 방식**  | 목표 크기 `(dsize)` 또는 배율 `(fx, fy)` 지정                   | 2×3 아핀 변환 행렬 지정          |
| **지원 변환**  | ✅ 크기 변경만                                              | ✅ 이동, 회전, 확대, 기울이기 가능    |
| **코드 복잡도** | 간단, 직관적                                               | 복잡 (행렬 계산 필요)            |
| **속도**     | 빠름                                                    | 상대적으로 느림                 |
| **정밀 제어**  | 제한적                                                   | ✅ 매우 세밀한 제어 가능           |
| **사용 예시**  | 딥러닝 이미지 전처리, 썸네일 생성                                   | 카메라 캘리브레이션, 기울어진 이미지 보정  |

## ✔ 이미지 회전 (Rotation)



# 📌 이미지 뒤틀기(어핀 변환, 원근 변환)
- 참고 : [내용](https://bkshin.tistory.com/entry/OpenCV-14-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%92%A4%ED%8B%80%EA%B8%B0%EC%96%B4%ED%95%80-%EB%B3%80%ED%99%98-%EC%9B%90%EA%B7%BC-%EB%B3%80%ED%99%98)

# 📌자동차 번호판 추출 프로젝트

- 실습 가이드 : [링크](https://docs.google.com/document/d/1x4jZhxis_XxPGU_vg6CmdWW-eTib90MwQ7-Aj5irEJg/edit?tab=t.0#heading=h.9s9s6ejg8h8)

## 1. 목표
OpenCV 원근변환을 활용하여 기울어진 자동차 번호판을 마우스 클릭으로 추출하고 정면 이미지로 변환하는 프로그램 구현

<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/5fead1fb-9dee-448d-94e1-1891a7fc2f4c" />

## 2. 동작설명
