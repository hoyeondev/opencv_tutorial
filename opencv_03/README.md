# 📌 컨투어(Contour)
- 참고 : [내용](https://bkshin.tistory.com/entry/OpenCV-22-%EC%BB%A8%ED%88%AC%EC%96%B4Contour), [소스](https://github.com/BaekKyunShin/OpenCV_Project_Python/tree/master/07.segmentation)

**컨투어(Contour)** 는 동일한 색상이나 강도를 가진 픽셀을 연결해 만든 곡선으로<br>
객체의 외곽선을 나타내며, 이미지에서 물체의 모양을 분석하거나 경계 추출할 때 사용한다.

<details>
<summary>내용보기 🔽</summary>


## ✔ 컨투어 함수
### 1. `cv2.findContours()` : 이미지에서 컨투어를 찾는 함수
>```python
>contours, hierarchy = cv2.findContours(image, mode, method)
>```
**매개변수**

- `image`: 이진화된 이미지 (흰색: 객체, 검정: 배경)

- `mode`: 컨투어 검색 방식

	- `cv2.RETR_EXTERNAL` → 가장 바깥쪽 컨투어만 검색

	- `cv2.RETR_LIST` → 모든 컨투어 검색, 계층 관계 무시

	- `cv2.RETR_TREE` → 모든 컨투어 검색, 계층 구조 저장

- `method`: 근사화 방법
	- `cv2.CHAIN_APPROX_NONE` → 모든 점 저장
  - `cv2.CHAIN_APPROX_SIMPLE` → 꼭짓점만 저장 (메모리 절약)
 
**반환값**
- `contours`: 컨투어 리스트 (각 컨투어는 좌표 배열)

- `hierarchy`: 계층 정보 배열

### 2. `cv2.drawContours()` : 컨투어를 이미지에 그리는 함수
>```python
>cv2.drawContours(image, contours, contourIdx, >color, thickness)
>```
**매개변수**
- `image`: 출력할 이미지

- `contours`: 컨투어 리스트

- `contourIdx`: 그릴 컨투어 인덱스 (-1 → 모두)

- `color`: (B, G, R)

- `thickness`: 선 두께 (-1 → 내부 채우기)

### 3. `cv2.contourArea()` : 컨투어의 면적을 계산
>```python
>perimeter = cv2.arcLength(contour, closed=True)
>```

### 4. `cv2.arcLength()` : 컨투어의 둘레(길이)를 계산
>```python
>perimeter = cv2.arcLength(contour, closed=True)
>```

### 5. `cv2.boundingRect()` : 컨투어를 감싸는 최소 사각형 좌표
>```python
>x, y, w, h = cv2.boundingRect(contour)
>```

### 6. `cv2.minEnclosingCircle()` : 컨투어를 감싸는 최소 원
>```python
>(x, y), radius = cv2.minEnclosingCircle(contour)
>```

### 7. `cv2.moments()` : 컨투어의 모멘트 계산 (무게중심, 형태 분석)
>```python
>M = cv2.moments(contour)
>cx = int(M['m10']/M['m00'])
>cy = int(M['m01']/M['m00'])
>```


## ✔ 컨투어 활용
- 라인 트레이싱 (예: 검정 테이프 따라가기)
- 특정 물체(형태) 추적
  - 드론이 빨간색 패널을 따라 비행
  - 로봇팔이 특정 색 물체 집기
- 경로 계획 및 장애물 회피 : 카메라로 주변 환경 인식
- 실시간 제어 흐름
  - 카메라 영상 수집 → ROI 설정 → 모터 제어 명령 송선(ROS, 시리얼 통신 등)

</details>

---

# 📌 OpenCV 라인 트레이싱 프로젝트

- 실습개요 : [링크](https://docs.google.com/document/d/1Swvm-nxyCb2-P3JxoNNlZMnuLJe77RqzjoXh6IvTGqY/edit?tab=t.0#heading=h.b171i0dol1vx)

## 1. 목표
- 기본 객체인식 : 웹캠을 통해 검정색 라인을 인식하고 시각화하기
- 히스토그램 분석으로 객체 특성 파악
- 객체 이진화 및 검출
- 객체 정보 추출 및 시각화

<img width="400" height="350" alt="image" src="https://github.com/user-attachments/assets/71b2c4d6-a179-40fc-b4ea-e22cda600dcf" />

## 2. 동작설명

### 1. 기본 설정
- 카메라 연결
- 해상도 설정

### 2. `Matplotlib` 실시간 히스토그램 설정
- 히스토그램 시각화 함수 정의
>```python
>def plot_histogram(gray_img):
>    hist = cv2.calcHist([gray_img], [0], None, [256], [0,256])
>    ax.plot(hist)
>```
<img width="600" height="400" alt="histogram" src="https://github.com/user-attachments/assets/ccb4840e-b2f8-44af-9c5a-01cb2483ad81" />

→ ROI(관심 영역)의 그레이스케일 값 분포를 실시간으로 그려줌

### 3. ROI 영역 설정(검정색 라인)
- ROI 영역 지정
>```python
>roi_x, roi_y = int(width * 0.2), int(height * 0.2)
>roi_w, roi_h = int(width * 0.6), int(height * 0.6)
>roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
>```
- 시각화
>```python
>cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (0, 255, 0), 2)
>
→ ROI 영역을 녹색 사각형으로 표시

### 4. ROI에서 이진화 및 중심점 계산
- 그레이스케일 변환 → 이진화(Threshold)
>```python
>gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
>_, binary = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
>```

- 무게중심(중앙점) 계산 : `moments`함수 사용
>```python
>M = cv2.moments(binary)
>cx = int(M["m10"] / M["m00"])
>cy = int(M["m01"] / M["m00"])
>```

### 5. 화면 출력
- 원본 이미지 + ROI + 중심점 출력
>```python
>cv2.imshow('Original with ROI', frame)
>```

- 종료 조건
>```python
>if cv2.waitKey(1) & 0xFF == ord('q'):
>   break
>```


