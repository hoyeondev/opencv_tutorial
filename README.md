- 소스 참고 : https://github.com/dltpdn/insightbook.opencv_project_python/tree/master

## 📌 이미지 프로세싱 기초
### 1. 이미지 색상 표현 방식(BGR, HSV, YUV) : [참고링크](https://bkshin.tistory.com/entry/OpenCV-7-%E3%85%87%E3%85%87)
  
#### ✔ BGR, BGRA
- `BGR` : OpenCV에서 기본적으로 사용하는 색상 공간
  - 각 픽셀은 Blue(파란색), Green(초록색), Red(빨간색) 3개의 값으로 구성
  - 각 채널 값 범위: 0 ~ 255
  - 예: (255, 0, 0) → 파란색
- `BGRA` : 투명도(Alpha) 채널을 추가한 4채널 색상 공간
  - A(Alpha): 불투명도 (0 = 완전 투명, 255 = 완전 불투명)
  - 예: (255, 0, 0, 128) → 파란색 + 반투명
- 카메라·이미지 파일의 기본 저장 방식은 대부분 RGB지만, OpenCV는 BGR 순서를 기본 사용.
- 알파 채널은 PNG 같은 투명 배경 이미지에서 자주 사용.

#### ✔ HSV (Hue, Saturation, Value)
- 인간의 시각적 특성을 반영한 색상 모델
- 색상(H)과 밝기(V)를 분리 → 조명 변화에 강함
- 크로마키(배경 제거), 색상 기반 추적에 자주 사용

>```python
>hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
>```

  
#### ✔ YUV, YCbCr
- 영상 신호 처리에서 자주 쓰이는 색상 공간
- `YUV` : 아날로그 TV 등에서 사용
- `YCbCr` : 디지털 비디오/이미지 압축(JPEG, MPEG)에서 사용
- 장점: 휘도(Y)와 색차(Cb, Cr)를 분리 → 압축 효율 ↑
- 활용
  - JPEG, MPEG 압축
  - 얼굴 인식 (Y 채널을 사용해 조명 변화에 강인)

#### ✔ 요약

| 색상 공간         | 구성 요소                  | 특징                   |
| ------------- | ---------------------- | -------------------- |
| **BGR**       | Blue, Green, Red       | OpenCV 기본, 디스플레이에 적합 |
| **BGRA**      | BGR + Alpha            | 투명도 지원               |
| **HSV**       | Hue, Saturation, Value | 색상 처리에 강점, 조명 변화에 강함 |
| **YUV/YCbCr** | Y(밝기), U/Cb, V/Cr(색차)  | 압축 및 방송용, 조명 보정 유리   |


---

### 2. 스레시홀딩(Thresholding), 오츠의 알고리즘(Otsu's Method) : [참고링크](https://bkshin.tistory.com/entry/OpenCV-8-%EC%8A%A4%EB%A0%88%EC%8B%9C%ED%99%80%EB%94%A9Thresholding)
이미지 처리에서 **스레시홀딩(Thresholding)** 은 이미지를 이진화하는 대표적인 기법 <br>
기준 값(Threshold)을 기준으로 픽셀 값을 두 가지(0 또는 255)로 나누는 과정

#### ✔ 스레시홀딩(Thresholding)
- 픽셀 값이 특정 임계값(threshold)보다 크면 1(또는 255), 아니면 0으로 설정하는 기법
- 목적 : 이미지를 이진화하여 객체(전경)와 배경을 구분
>```python
>_, dst = cv2.threshold(src, thresh, maxValue, type)
>```


#### ✔ 전역 스레시홀딩(Global Thresholding)
- 전체 이미지에 **하나의 임계값(T)** 을 적용
- 배경과 객체의 명암 차이가 명확할 때 효과적
- 단점: 조명 변화, 그림자, 불균일한 배경에서는 성능 저하
>```python
>ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
>```
<img width="575" height="275" alt="image" src="https://github.com/user-attachments/assets/bd3ddbca-c48d-40c3-a546-c7b1db4c8c35" />


#### ✔ 오츠의 이진화 알고리즘(Otsu's Method)
- 이미지 히스토그램을 기반으로 자동으로 최적 임계값을 계산
- 이미지가 두 개의 피크(전경과 배경)를 가진다고 가정한다.
- OpenCV에서 `cv2.THRESH_OTSU` 플래그를 추가하면 사용 가능
>```python
>ret, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
>```

<img width="577" height="268" alt="image" src="https://github.com/user-attachments/assets/91b0f6c6-7b6b-438d-96b8-03012b8ed02d" />


#### ✔ 적응형 스레시홀딩(Adaptive Thresholding)
- 이미지의 국소 영역마다 임계값을 다르게 설정.
- 조명 불균형, 그림자에 강함.
- OpenCV 함수: `cv2.adaptiveThreshold()`
>```python
>adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
>                                 cv2.THRESH_BINARY, 11, 2)
>
>```

#### ✔ 활용 예
- 문서 스캔 → 이진화 (텍스트 추출)
- 객체 검출 전 전처리
- OCR(문자인식) 단계

---

### 3. 이미지 연산 (합성, 알파 블렌딩, 마스킹) : [참고링크](https://bkshin.tistory.com/entry/OpenCV-9-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%97%B0%EC%82%B0)

#### ✔ 이미지 연산
- 픽셀 단위로 덧셈, 뺄셈, 비트 연산을 수행.
- 기본 연산: `cv2.add()`, `cv2.subtract()`, `cv2.bitwise_and()` 등.
- 활용:
  - 두 이미지 결합
  - ROI(Region of Interest) 설정
  - 마스킹 기반 합성
>```python
>result = cv2.add(img1, img2)
>```


#### ✔ 이미지 합성
- 두 이미지를 하나로 결합하는 기법.
- 조건: 같은 크기 & 같은 채널 수 필요.
- 방법:
  - 단순 합성 (`cv2.add`)
  - 알파 블렌딩 (`cv2.addWeighted()`) : 가중합 사용
  
#### ✔ 비트와이즈 연산
- 마스크(mask)를 이용한 이미지 조합
- 활용:
  - 특정 영역 추출
  - 크로마키 (배경 제거)
 
#### ✔ 이미지 합성과 마스킹
- 마스크: 특정 영역을 선택하는 흑백 이미지 (255: 사용, 0: 제거)
- ROI와 마스크를 활용해 이미지 일부만 합성 가능.

#### ✔ 활용 예
- 크로마키 영상 합성
- 투명 PNG 이미지 합성
- 로고 삽입, 워터마크 처리
  
---

### 4. 이미지 내 관심영역(Region of Interest, ROI) : [참고링크](https://bkshin.tistory.com/entry/OpenCV-6-dd)
#### ✔ ROI란?
- 이미지에서 특정 관심 있는 영역을 의미합니다.
- 예: 얼굴 인식에서 얼굴 부분, 물체 탐지에서 물체가 있는 영역.
- OpenCV에서는 Numpy 배열 슬라이싱으로 간단히 ROI를 추출할 수 있음

#### ✔ ROI 추출 방법
>```python
>import cv2
>import numpy as np
>
># 관심영역 표시
>img = cv2.imread('../img/sunset.jpg')
>
>x=320; y=150; w=50; h=50        # roi 좌표
>roi = img[y:y+h, x:x+w]         # roi 지정        ---①
>
>print(roi.shape)                # roi shape, (50,50,3)
>cv2.rectangle(roi, (0,0), (h-1, w-1), (0,255,0)) # roi 전체에 사각형 그리기 ---②
>cv2.imshow("img", img)
>
>key = cv2.waitKey(0)
>print(key)
>cv2.destroyAllWindows()
>```
> <img width="595" height="346" alt="image" src="https://github.com/user-attachments/assets/a70bb9ef-ec2c-4b50-b175-f149419bc0df" />


#### ✔ 특징
- 원본 이미지와 연결: ROI는 복사본이 아닌 뷰(View)이므로 값 변경 시 원본에도 반영됨.
- 복사 필요 시: roi.copy() 사용

#### ✔ 활용 예
- 객체 추출 : 이미지에서 특정 부분(예: 얼굴, 자동차 번호판)만 잘라내어 저장하거나 분석
- 이미지 합성(로고 삽입)
- 특정 영역에만 블러, 엣지 검출 등 이미지 처리 적용

---

### 5. 히스토그램과 정규화(Normalize), 평탄화(Equalization), CLAHE : [참고링크](https://bkshin.tistory.com/entry/OpenCV-10-%ED%9E%88%EC%8A%A4%ED%86%A0%EA%B7%B8%EB%9E%A8)

#### ✔ 히스토그램
- 정의: 이미지 픽셀 값(밝기 또는 색상)의 분포를 나타내는 그래프.
- 용도:
  - 이미지의 밝기, 대비 분석
  - 명암비 향상 전처리
>```python
>hist = cv2.calcHist([img], [0], None, [256], [0,256])
>```

#### ✔ 정규화(Normalization)
- 목적: 픽셀 값 범위를 0~255 등 특정 범위로 스케일링
- 대비 향상 또는 다른 이미지와의 비교 시 사용
>```python
>norm = cv2.normalize(src, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
>```

#### ✔ 평탄화(Equalization)
- 정의: 픽셀 값의 누적분포를 활용해 히스토그램을 고르게 분포시키는 기법.
- 효과: 어두운 이미지 → 밝게, 대비 향상
>```python
>gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
>equalized = cv2.equalizeHist(gray)
>```

#### ✔ CLAHE (Contrast Limited Adaptive Histogram Equalization)
- 정의: 국소 영역마다 히스토그램 평탄화를 적용, 대비를 제한(Clip Limit)해 과도한 밝기 변화 방지.
- 장점: 국소 영역에서 대비 향상 + 자연스러운 결과
>```python
>clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
>cl_img = clahe.apply(gray)
>```

#### ✔ 활용 예
- 의료 영상 (X-ray, CT) → 뼈 구조 강화.
- 문서 스캔 → 글자 대비 향상.
- 야간 영상 처리 → 어두운 영역의 디테일 향상.

---

### 6. 2차원 히스토그램과 역투영(back project) : [참고링크](https://bkshin.tistory.com/entry/OpenCV-11-2%EC%B0%A8%EC%9B%90-%ED%9E%88%EC%8A%A4%ED%86%A0%EA%B7%B8%EB%9E%A8%EA%B3%BC-%EC%97%AD%ED%88%AC%EC%98%81back-project)

#### ✔ 2차원 히스토그램 (2D Histogram)
- 두 개의 채널 값(예: Hue와 Saturation)의 조합 빈도를 나타내는 히스토그램
- 1차원 히스토그램과 다르게 축이 2개이고, 각 축이 만나는 지점의 개수를 표현한다.
- 활용
  - 색상 기반 객체 탐지 (예: 특정 색 영역 찾기)
  - 조명 변화에 강인한 색 분포 분석
>```python
>hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
>```

#### ✔ 역투영(Back Projection)
- 특정 히스토그램을 기준으로 원본 이미지에서 해당 히스토그램과 유사한 픽셀을 찾아내는 기법
- 원리
  - ROI(관심영역)에서 히스토그램 생성
  - 원본 이미지에서 각 픽셀이 ROI 히스토그램과 얼마나 유사한지 계산
  - 결과는 확률 맵 형태 (밝을수록 유사)
- 단점
  - 조명 변화에 취약
  - ROI와 비슷한 색상을 가진 다른 객체나 배경이 있으면 잘못 추적(오탐) 가능
  - 노이즈에 민감
>```python
>dst = cv2.calcBackProject([hsv], [0, 1], roi_hist, [0, 180, 0, 256], 1)
>```


#### ✔ 활용 예
- 객체 추적 (CamShift, MeanShift)
  - ROI 색상 히스토그램을 기반으로 프레임마다 객체 위치 추정
- 색 기반 분할
  - 특정 색상 영역을 강조해 마스킹
- 영상 검색
  - 히스토그램 비교 기반 유사 영상 검색

