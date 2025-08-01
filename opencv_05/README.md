# 📌 실시간 카메라 QR 코드 스캐너 (URL 자동 열기)

## 1. 목표
- 웹캠을 이용해 QR 코드를 실시간으로 인식
- 인식된 QR 코드가 URL일 경우 기본 웹 브라우저에서 자동으로 열기
- 동일 URL을 반복해서 열지 않도록 중복 방지 로직 추가
- 인식 상태를 화면에 시각적으로 표시 (사각형 + 텍스트)
<img width="575" height="374" alt="image" src="https://github.com/user-attachments/assets/7208078e-0e89-414f-8822-71ae6ed363ce" />

## 2. 동작 설명

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

## 3. 실행
```python
# src
python qr_scan.py
```
