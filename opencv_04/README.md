# 📌 이미지 이동(Translation), 확대/축소(Scaling), 회전(Rotation)
- 참고 : [내용](https://bkshin.tistory.com/entry/OpenCV-13-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%9D%B4%EB%8F%99Translation-%ED%99%95%EB%8C%80%EC%B6%95%EC%86%8CScaling-%ED%9A%8C%EC%A0%84Rotation)
- OpenCV는 `cv2.warpAffine()` 또는 `cv2.warpPerspective()`를 사용해 다양한 변환을 지원한다.
- Affine 변환은 평행선 유지, Perspective 변환은 투시 왜곡까지 가능

<details>
<summary>내용보기 🔽</summary>
  
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
이미지를 특정 각도로 회전
```python
# 중심점 (cols/2, rows/2), 각도 45도, 배율 1.0
M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1.0)
rotated = cv2.warpAffine(img, M, (cols, rows))
```

</details>


# 📌 이미지 뒤틀기(어핀 변환, 원근 변환)
- 참고 : [내용](https://bkshin.tistory.com/entry/OpenCV-14-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%92%A4%ED%8B%80%EA%B8%B0%EC%96%B4%ED%95%80-%EB%B3%80%ED%99%98-%EC%9B%90%EA%B7%BC-%EB%B3%80%ED%99%98)


<details>
<summary>내용보기 🔽</summary>

  
## ✔ 어핀 변환(Affine Transform)
- 직선은 직선으로 유지되며, 평행선도 평행 상태 유지
- 크기, 각도, 비율이 변할 수 있음 (즉, 뒤틀림 가능)
- 필요한 점: 3쌍의 대응점
```python
# 3개의 점 매칭
pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])

# 어핀 변환 행렬
M = cv2.getAffineTransform(pts1, pts2)

# 어핀 변환 적용
affine = cv2.warpAffine(img, M, (cols, rows))

cv2.imshow('Affine', affine)
cv2.waitKey(0)
```
## ✔ 원근 변환(Perspective Transform)
- 카메라 시점에서 보는 투시 왜곡까지 표현 가능
- 평행선이 소실점으로 모이는 효과
- 필요한 점: 4쌍의 대응점
```python
# 4개의 점 매칭
pts1 = np.float32([[100, 100], [300, 100], [100, 300], [300, 300]])
pts2 = np.float32([[80, 120], [310, 100], [100, 310], [300, 320]])

# 원근 변환 행렬
M = cv2.getPerspectiveTransform(pts1, pts2)

# 원근 변환 적용
perspective = cv2.warpPerspective(img, M, (cols, rows))

cv2.imshow('Perspective', perspective)
cv2.waitKey(0)
```
#### 마우스와 원근 변환으로 문서 스캔 효과내기
> <img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/10a73df0-6281-4026-a85e-fa1472f51402" />

</details>


# 📌자동차 번호판 추출 프로젝트

- 실습 가이드 : [링크](https://docs.google.com/document/d/1x4jZhxis_XxPGU_vg6CmdWW-eTib90MwQ7-Aj5irEJg/edit?tab=t.0#heading=h.9s9s6ejg8h8)

## 1. 목표
OpenCV 원근변환을 활용하여 기울어진 자동차 번호판을 마우스 클릭으로 추출하고 정면 이미지로 변환하는 프로그램 구현

<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/5fead1fb-9dee-448d-94e1-1891a7fc2f4c" />

## 2. 동작설명

### ✔ 주요 기능
- 폴더 내 이미지(car_*.jpg)를 순차적으로 불러옴
- 마우스로 4개의 점(번호판 코너)을 클릭하여 영역 지정
- 원근 변환(Perspective Transform) 적용 → 번호판을 정면 형태로 변환
- 변환된 이미지를 지정된 크기(300x150)로 저장
- ESC → 현재 이미지 스킵, Q → 프로그램 종료

### 1. 초기설정
- 처리완료 이미지 저장 폴더 설정
- GUI 윈도우 타이틀
- 이미지 데이터 셋

### 2. 이미지 파일 로드
- `../img/` 폴더에서 `car_*.jpg` 파일을 탐색하고, 리스트에 경로 저장
- 정렬하여 파일명 순서대로 처리
  
```python
for file in os.listdir("../img/"):
    if file.startswith("car_") and file.endswith(".jpg"):
        imgs.append(os.path.join("../img/", file))

imgs.sort()
```
### 3. 마우스 이벤트 콜백(`onMouse`)
- 마우스로 클릭할 때마다 좌표를 배열(pts)에 저장
- 4개의 점이 선택되면:
  - 클릭한 점을 기반으로 좌상단, 우상단, 우하단, 좌하단을 자동 판별
  - 원근 변환 행렬 계산
  - `cv2.warpPerspective()`로 번호판을 정면 이미지로 변환
  - 결과를 화면에 출력
  - PNG 형식으로 `../extracted_plates/` 폴더에 저장

```python
cv2.setMouseCallback(win_name, onMouse)
```
### 4. 원근 변환(Perspective Transform)
- `pts1`: 사용자가 클릭한 번호판 모서리 좌표
- `pts2`: 변환 후 위치 (정사각형 형태)
- width=300, height=150 (번호판 표준 비율 기반)

```python
pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])
pts2 = np.float32([[0,0],[width-1,0],[width-1,height-1],[0,height-1]])

mtrx = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(img, mtrx, (width, height))
```
### 5. 메인 루프
- 이미지 하나씩 불러와서 표시
- 사용자 입력 대기:
  - **4점 클릭** → 저장 후 다음 이미지
  - **ESC** → 스킵
  - **Q** → 전체 종료

```python
for path in imgs:
    img = cv2.imread(path)
    cv2.imshow(win_name, img)
```

## 3. 이미지 전처리 기능 추가
추출된 번호판 이미지를 OCR 인식을 위해 최적화 처리
- 그레이스케일 변환
- 대비 최적화
- 컨투어로 윤곽선 검출

<img width="799" height="127" alt="image" src="https://github.com/user-attachments/assets/b8b6e5b7-2f93-40ae-91ae-0e8505ac525b" />
