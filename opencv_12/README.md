
# 📌 YOLO(You Only Look Once)

- 참고 : [내용](https://bkshin.tistory.com/entry/%EC%BB%B4%ED%93%A8%ED%84%B0-%EB%B9%84%EC%A0%84-11-YOLO-v1-v2-v3-%EA%B0%9C%EC%9A%94%EC%99%80-%EC%8B%A4%EC%8A%B5)
- 컴퓨터 비전 분야에서 실시간 **객체 탐지(Object Detection)** 에 사용되는 딥러닝 모델

## ✔ 특징
- 단일 신경망: YOLO는 객체 영역 후보 생성과 분류를 한 번에 처리하는 단일 신경망을 사용한다. 덕분에 여러 단계를 거치는 모델들보다 훨씬 빠르게 작동한다.
- 그리드 시스템: 이미지를 여러 개의 **그리드 셀(Grid Cell)** 로 나누고, 각 셀이 자체적으로 객체의 존재 여부, 위치, 크기, 그리고 객체의 종류를 예측한다.
- 고속 처리: YOLO는 실시간 처리가 필요한 자율 주행 자동차 🚗, 드론 🚁, 보안 카메라 📹 등 다양한 분야에서 활용된다.
- 높은 정확도: 초기 버전들은 다른 모델들에 비해 정확도가 다소 낮았지만, 이후 버전(YOLOv3, YOLOv4, YOLOv5, YOLOv8 등)들이 계속해서 발전하며 높은 정확도를 달성하고 있다.

## ✔ [Ultralytics](https://www.ultralytics.com/)
- 컴퓨터 비전, 특히 YOLO(You Only Look Once) 모델 개발 및 배포에 특화된 기술 회사
- YOLO 모델의 선도적인 개발사
- 다양한 컴퓨터 비전 작업 지원
- 폭넓은 활용 분야 : 자율주행, 보안 및 감시, 제조업, 농업, 의료

---

# 📌 YOLO를 활용하여 객체 탐지하기

## 1. 목표
- 객체를 탐지할 영상을 구한다.
- 객체를 탐지하되 내가 원하는 객체만 탐지하도록 한다.
  -  `Ultralytics`, `YOLO11n` 사용

<div>
<p align="center">
  <img src="https://github.com/RizwanMunawar/ultralytics/assets/62513924/5ab3bbd7-fd12-4849-928e-5f294d6c3fcf" width="45%" alt="YOLOv8 region counting visual 1">
  <img src="https://github.com/RizwanMunawar/ultralytics/assets/62513924/e7c1aea7-474d-4d78-8d48-b50854ffe1ca" width="45%" alt="YOLOv8 region counting visual 2">
</p>
</div>

 
## 2. 개발 과정

#### 1. 객체 탐지용 샘플 영상 구하기

- YOLO를 사용해서 영상 내의 영역에서 객체 수를 구하고자 함
- [AI 허브](https://www.aihub.or.kr/aihubdata/data/view.do?pageIndex=1&currMenu=115&topMenu=100&srchOptnCnd=OPTNCND001&searchKeyword=&srchDetailCnd=DETAILCND001&srchOrder=ORDER003&srchPagePer=20&srchDataRealmCode=REALM001&aihubDataSe=data&dataSetSn=489) 에서 적절한 샘플을 찾아 다운로드.
> <img width="400" height="387" alt="image" src="https://github.com/user-attachments/assets/b97cb92a-7ca0-42a0-966f-f7a3e21af818" />

#### 2. YOLO 공식문서 예제 활용
- [영역 내 객체 수 세기 문서 참고](https://docs.ultralytics.com/ko/guides/region-counting/#how-do-i-run-the-region-based-object-counting-script-with-ultralytics-yolo11)
- [예제 소스코드 github](https://github.com/ultralytics/ultralytics/blob/main/examples/YOLOv8-Region-Counter/README.md?plain=1)

#### 3. 객체 추출 class 인자값 조정
- 사람만 탐지하도록 클래스를 `[0]`으로 조정
- [YOLO 객체 탐지 데이터셋 참조](https://docs.ultralytics.com/ko/datasets/detect/coco/#applications)

## 3. 동작 흐름

#### 1. 커맨드라인 옵션 파싱 (`parse_opt` 함수)
- argparse를 이용해 실행 시 전달되는 인자들을 파싱
- 주요 옵션
  - `--weights`: YOLO 모델 가중치 파일 경로 (기본: "yolo11n.pt")
  - `--device`: 처리할 디바이스 설정 (예: "cpu", "0" 등)
  - `--source`: 입력 비디오 파일 경로 (필수)
  - `--view-img`: 결과 화면 표시 여부 (플래그)
  - `--save-img`: 결과 영상 저장 여부 (플래그)
  - `--exist-ok`: 기존 결과 폴더 덮어쓰기 여부 (플래그)
  - `--classes`: 탐지할 클래스 필터, 기본 `[0]` (사람 클래스)
  - `--line-thickness`: 바운딩 박스 두께
  - `--track-thickness`: 추적선 두께
  - `--region-thickness`: 영역 경계선 두께

#### 2. 메인 함수 실행 (`main` 함수)
- `parse_opt()`로 옵션을 받아 `run` 함수에 키워드 인자로 전달
- `run(**vars(options))` 형태로 실행

#### 3. `run` 함수 상세 흐름

##### 초기 설정
- 입력 비디오 경로 존재 여부 확인, 없으면 예외 발생
- YOLO 모델 로드 및 디바이스(CPU 또는 CUDA) 설정
- 모델 클래스 이름(`names`) 추출
- OpenCV `VideoCapture`를 통해 비디오 열기 및 영상 정보(가로, 세로, FPS) 읽기

##### 마우스 이벤트 콜백 등록
- 첫 프레임 표시 시 OpenCV 창 생성 및 마우스 콜백 함수 `mouse_callback` 등록
	→ 영역(폴리곤) 드래그 및 이동 기능 제공

##### 영상 프레임 반복 처리
- 프레임 단위로 영상 읽기
- YOLO 모델로 객체 탐지 및 ByteTrack 기반 추적 수행(`model.track`)
- 탐지 결과 중 트랙킹된 박스 정보(좌표, ID, 클래스) 추출
- `Annotator`를 사용해 박스와 클래스명 라벨 그리기
- 각 트랙 ID 별로 중심점 좌표 기록 후 이동 경로 그리기 (최대 30프레임 분량)
- 각 탐지 중심점이 속하는 영역(폴리곤) 확인 후 해당 영역 카운트 증가


##### 화면 출력 및 종료 조건
- `--view-img` 옵션이 켜져 있으면 프레임을 OpenCV 창에 띄움
- `q` 키 입력 시 반복 종료


#### 4. 마우스 콜백 함수 (`mouse_callback`)
- 마우스 좌클릭 시 영역 내 좌표를 체크하여 드래그 시작
- 드래그 중 좌표 변화량을 영역 폴리곤 좌표에 반영하여 영역 이동
- 마우스 버튼 놓으면 드래그 종료
> <img width="400" height="450" alt="image" src="https://github.com/user-attachments/assets/02db8a27-74b4-4c30-84b6-d58a600c76e6" />


## 4. 실행방법
```bash
# yolo용 가상환경 생성
python -m venv yolovenv

# 가상환경 실행
source yolovenv/Scripts/activate

# pip 패키지 다운로드
pip install ultralytics

# yolo_test.py 스크립트를 실행하여,
# 상위 폴더 video 내의 sample.mp4 영상을 YOLO 모델로 처리하고,
# 처리 결과를 실시간으로 화면에 띄워서 보여준다.
python yolo_test.py --source ../video/sample.mp4 --view-img
```

---
