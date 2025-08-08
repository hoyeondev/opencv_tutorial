
# 📌 졸음방지 시스템

## 1. 목표
- 눈 깜빡임을 분석하여 **실시간으로 졸음을 감지하는 시스템** 을 구현한다.
- 일정 시간 이상 눈을 감고 있을 경우 경고 메세지를 화면에 출력한다.

## 2. 사용 기술 및 도구
| 도구/기술              | 설명                   |
| ------------------ | -------------------- |
| Python             | 프로젝트 개발 언어           |
| OpenCV             | 이미지 처리 및 얼굴 인식 라이브러리 |
| Haar Cascade       | 얼굴 검출용 분류기       |
| dlib      |  얼굴 검출 및 68개 얼굴 랜드마크를 추출       |
| SciPy      |  EAR 계산에 필요한 유클리드 거리(Euclidean distance)를 구하는 데 사용    |



## 3. 주요 기능
- 얼굴 검출: 웹캠 영상에서 사용자의 얼굴 영역을 실시간으로 감지한다.
- 눈 랜드마크 추출: 감지된 얼굴에서 눈의 랜드마크(landmark) 좌표를 추출한다.
- EAR(Eye Aspect Ratio) 계산: 추출된 랜드마크를 기반으로 눈의 종횡비(EAR)를 계산하여 눈이 감긴 상태를 수치화한다.
- 졸음 판단: EAR 값이 사전에 정의된 임계값보다 낮아지면 눈을 감았다고 판단하고, 일정 시간 이상 눈을 감고 있을 경우 졸음으로 간주한다.
- 경고 알림: 졸음이 감지되면 화면 또는 소리 등으로 사용자에게 경고 메세지를 출력한다.

## 4. 출력 예시

#### 졸음 감지 인식
졸음 감지 시 `Don't fall asleep!!!!` 메세지 출력
> <img width="400" height="289" alt="image" src="https://github.com/user-attachments/assets/1ff4b308-fd4a-41fb-9545-ac581638102e" />

#### 졸지 않는 상태 인식

> <img width="400" height="262" alt="image" src="https://github.com/user-attachments/assets/dda85914-0231-42ae-82c7-4a0c7625f527" />


## 5. 실행
```bash
#./drowsiness_detection
py main.py
```
