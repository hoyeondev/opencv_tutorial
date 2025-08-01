# 📌 실시간 카메라 QR 코드 스캐너 (URL 자동 열기)

## 1. 목표
- 웹캠을 이용해 QR 코드를 실시간으로 인식
- 인식된 QR 코드가 URL일 경우 기본 웹 브라우저에서 자동으로 열기
- 동일 URL을 반복해서 열지 않도록 중복 방지 로직 추가
- 인식 상태를 화면에 시각적으로 표시 (사각형 + 텍스트)
> <img width="575" height="374" alt="image" src="https://github.com/user-attachments/assets/7208078e-0e89-414f-8822-71ae6ed363ce" />

## 2. 활용 라이브러리
- openCV, matplotlib, pyzbar, webbrowser

## 3. 동작 설명

### 1. 카메라 입력 처리

- `cv2.VideoCapture(0)`을 사용해 기본 웹캠에서 프레임을 읽기
- `cv2.flip(img, 1)`로 좌우 반전하여 자연스러운 카메라 화면 제공

### 2. QR 코드 인식

- `pyzbar.decode()`를 사용해 각 프레임에서 QR 코드를 탐지
- 탐지된 QR 코드의 영역 좌표 (x, y, w, h)를 받아 사각형 그리기
- QR 데이터(`d.data.decode('utf-8')`)와 타입(`d.type`)을 텍스트로 화면에 표시

#### pyzbar
바코드(Barcode)와 QR 코드(Quick Response Code)를 디코딩(해석)하는 역할을 하는 Python 라이브러리


### 3. URL 자동 열기

- QR 데이터가 http 또는 https로 시작하면 URL로 판단한다.
- `webbrowser.open(barcode_data)`를 통해 기본 웹 브라우저에서 해당 주소로 이동
- 이미 열었던 URL은 opened_urls 집합에 저장해 중복 실행 방지

### 4. 종료

- 카메라 영상에서 q 키를 누르면 while 루프 종료

## 4. 실행
```python
# src
python qr_scan.py
```

---

# 📌 Aruco Marker를 이용한 위치추정

## 1. Aruco Marker란?
- Rafael Muñoz와 Sergio Garrido가 개발한 정사각형 패턴이며, 로봇비전, 증강현실, 자동화 공정등에 널리 사용되고 있다.
- 비전 기술을 접목하여 비접촉으로 가까운 거리 또는 적당한 거리(수미터내)에서 적당한 측정 정확도가 mm ~ cm 를 제공할 수 있다.

> <img width="250" alt="image" src="https://github.com/user-attachments/assets/6251c2b0-4c15-4aec-a0f9-2650dd26ff84" />


#### 비전를 이용하여 Aruco marker의 위치 추정
Aruco marker를 이용하여 위치와 자세를 추정하기 위해서는 다음과 같은 과정을 거쳐야 한다.

- 카메라 파라메터(Camera parameter) 와 렌즈 왜곡(Lens distortion) 얻기
- Aruco marker 생성
  - 인식 가능한 고유 마커를 만들어 출력(프린트) 후 사용
- Aruco marker 검출
  - 입력된 영상에서 마커 위치(코너점)와 ID를 인식
- PnP(Persepective-n-Point)
  - 마커의 2D 이미지상 좌표 → 3D 실제 좌표 변환 (위치 및 자세 추정)

## 2. 목표
- 웹캠으로 체커보드를 촬영해 카메라와 렌즈 왜곡 파라메터를 얻는다.
  - 카메라나 렌즈 왜곡 파라메터는 제조사에서 제공하지 않는 이상 알기 어려우므로
- Aruco marker 생성 및 검출 후 카메라와 마커 간의 거리를 계산한다.
- 임계 거리 설정 후 Go, Stop 안내를 표시한다.

## 3. 실행결과

### Go
설정한 임계 거리 이상으로 카메라와 아루코 마커가 멀어졌을 때
> <img width="344" height="225" alt="image" src="https://github.com/user-attachments/assets/219327eb-803d-4393-869c-5811b7873fc6" />

### Stop
카메라와 아루코 마커가 임계거리 이상으로 가까워졌을 때
> <img width="344" height="255" alt="image" src="https://github.com/user-attachments/assets/99acbc5e-2cbc-419d-ba24-b33bcfa50ac7" />


##  Aruco Marker 활용 분야
- 증강현실(AR): 마커 위에 3D 오브젝트 배치
- 로봇 내비게이션: 실내에서 마커 기반 로컬라이제이션
- 드론 제어: 마커를 기준으로 정확한 착륙 수행
- 카메라 보정: 3D 공간에서 정확한 좌표 추정














