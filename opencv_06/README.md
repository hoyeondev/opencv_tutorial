# 📌 이미지 매칭 (평균 해시 매칭, 템플릿 매칭)
- 참고 : [내용](https://bkshin.tistory.com/entry/OpenCV-25-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%A7%A4%EC%B9%AD-%ED%8F%89%EA%B7%A0-%ED%95%B4%EC%8B%9C-%EB%A7%A4%EC%B9%AD-%ED%85%9C%ED%94%8C%EB%A6%BF-%EB%A7%A4%EC%B9%AD)
- 서로 다른 두 이미지를 비교해서 짝이 맞는 형태의 객체가 있는지 찾아내는 기술
- 이미지 간 유사도를 측정하는 작업

## ✔ 평균 해시 매칭
- 이미지를 **작게 축소**하고, 그레이스케일로 변환 후 픽셀 평균값 계산.
- 평균보다 크면 1, 작으면 0으로 이진화 → **해시값 생성**
- 두 이미지의 해시값을 비교 (해밍 거리 이용)
- **장점**: 간단하고 빠름  
- **단점**: 회전, 스케일 변화에 약함

## ✔ 템플릿 매칭
- 큰 이미지에서 **작은 템플릿 이미지 위치를 찾는 기법**
- `cv2.matchTemplate()` 사용
- 유사도 측정 방법: **NCC(Normalized Cross-Correlation)** 등
- **단점**: 회전, 크기 변화에 취약

---

# 📌 이미지 특징점(Keypoints) 검출
- 참고 : [내용](https://bkshin.tistory.com/entry/OpenCV-26-%EC%9D%B4%EB%AF%B8%EC%A7%80%EC%9D%98-%ED%8A%B9%EC%A7%95%EA%B3%BC-%ED%82%A4-%ED%8F%AC%EC%9D%B8%ED%8A%B8?category=1148027)
- 이미지끼리 서로 매칭이 되는지 확인을 할 때 각 이미지에서의 특징이 되는 부분끼리 비교를 한다.
- 보통 특징점이 되는 부분은 물체의 모서리나 코너

## ✔ 해리스 코너 검출 (Harris Corner Detection)
- 코너란 **모든 방향으로 변화가 큰 영역**
- `cv2.cornerHarris()` 사용
- 회전에 강하지만, 밝기 변화에 약함

## ✔ 시-토마시 검출 (Shi & Tomasi Detection)
- 해리스 코너 개선 → **품질 좋은 코너만 선택**
- `cv2.goodFeaturesToTrack()` 사용
- 영상 추적용으로 적합

## ✔ 특징점 검출기
- **SIFT (Scale-Invariant Feature Transform)**  
  크기, 회전 변화에도 강인  
- **SURF (Speeded-Up Robust Features)**  
  SIFT보다 빠름, 특허 문제  
- **ORB (Oriented FAST and BRIEF)**  
  오픈소스, 실시간 처리 가능

---

# 📌 상품라벨 스캐너

## 1. 목표
1. 라벨 스캔 → 상품을 카메라 앞에 위치
2. ROI 생성 → 스페이스바 + 마우스 드래그로 라벨 영역 선택
3. 매칭 테스트 → 같은/다른 상품으로 인식 성능 확인

## 2. 기능 설명
- **카메라로 실시간 입력되는 영상**에서 사용자가 선택한 ROI(참조 이미지)와 현재 프레임의 특정 물체가 동일한지 매칭하는 프로그램  
- **ORB 특징점 검출**과 **FLANN 기반 매칭**을 활용하며, 원근 변환(Homography)을 통해 위치까지 확인한다.

## 3. 동작 설명
### 1. 카메라 연결 및 프레임 설정
- `cv2.VideoCapture(0)` : 기본 카메라 연결
- 해상도 설정: 640x480

### 2. ORB 특징점 검출기 생성
- `cv2.ORB_create(1000)`  
  → 한 이미지에서 최대 1000개의 특징점 검출  
- ORB는 **크기(scale)와 회전(rotation)에 강인한 특징점 검출 알고리즘**

### 3. FLANN 매칭기 생성
- FLANN(FLexible ANN) : 빠른 근사 최근접 매칭 알고리즘
- LSH(Locality Sensitive Hashing) 기반 매칭 설정
  ```python
  index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
  search_params = dict(checks=32)
  ```

### 4. ROI선택
- 스페이스바(' ') → `cv2.selectROI()`로 참조 이미지 선택
- 선택된 ROI는 `img1`로 저장
- 
### 5. 특징점 추출 및 매칭
- ORB를 이용해 `img1`(ROI)과 `img2`(현재 프레임)에서 특징점과 디스크립터 추출
```python
kp1, desc1 = detector.detectAndCompute(gray1, None)
kp2, desc2 = detector.detectAndCompute(gray2, None)
```
- `FLANN`의 knnMatch()로 두 이미지 간 매칭 수행 (k=2)

  
### 6. 좋은 매칭점 선별 (Lowe's Ratio Test)
- 매칭 결과에서 1등과 2등 거리 비교
```python
if m.distance < n.distance * 0.75:
    good_matches.append(m)
```

### 7. 원근 변환(Homography)
- 좋은 매칭점이 `MIN_MATCH` 이상인 경우:
  - `cv2.findHomography()`로 두 이미지 좌표 관계 계산
  - `cv2.perspectiveTransform()`으로 ROI 위치를 프레임에 표시

### 8. 결과 출력
- `cv2.drawMatches()`로 매칭점 시각화
- 동일 제품 여부 텍스트 표시:
  -  SAME PRODUCT (녹색)
  -  DIFFERENT PRODUCT (빨간색)

## 4. 실행 결과
#### 이미지 매칭 성공
> <img width="450" height="497" alt="image" src="https://github.com/user-attachments/assets/523b3a32-30f2-4b6d-8885-c686bf469566" />

#### 이미지 매칭 실패
> <img width="450" height="489" alt="image" src="https://github.com/user-attachments/assets/c13ba9a8-be6d-4429-82b0-cf509cf97078" />
