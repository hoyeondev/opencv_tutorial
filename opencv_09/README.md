# 📌 하르 캐스케이드 얼굴 검출 (Haar Cascade Face Detection)

<details>
<summary>내용보기 🔽</summary>

- 참고 : [내용1](http://atonrq.synology.me:1700/hypha/haarcascade), [내용2](https://bkshin.tistory.com/entry/%EC%BB%B4%ED%93%A8%ED%84%B0-%EB%B9%84%EC%A0%84-1-%ED%95%98%EB%A5%B4-%EC%BA%90%EC%8A%A4%EC%BC%80%EC%9D%B4%EB%93%9C-%EC%96%BC%EA%B5%B4-%EA%B2%80%EC%B6%9C-Haar-Cascade-Face-Detection)
- 학습 모델 데이터 : [OpenCV github](https://github.com/opencv/opencv/tree/4.x/data/haarcascades)
- 개발자가 집접 머신러닝 학습 알고리즘을 사용하지 않고도 객체를 검출할 수 있도록 OpenCV가 제공하는 대표적인 상위 레벨 API
- OpenCV는 케스케이드 분류기에서 사용할 수 있는 훈련된 검출기를 xml 파일 형태로 제공한다.


> <img width="450" height="500" alt="image" src="https://github.com/user-attachments/assets/e077cc7b-0e0e-4b37-9188-96c19b452d75" />


</details>

---

# 📌 LBPH(Local Binary Patterns Histograms) 얼굴인식 알고리즘

<details>
<summary>내용보기 🔽</summary>

- 참고 : [내용1](http://atonrq.synology.me:1700/hypha/lbph), [내용2](https://bkshin.tistory.com/entry/%EC%BB%B4%ED%93%A8%ED%84%B0-%EB%B9%84%EC%A0%84-3-LBPHLocal-Binary-Patterns-Histograms-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98)
- 이미지를 픽셀 단위로 살펴보면서, 각 픽셀의 주변 이웃과의 밝기 차이를 기준으로 이진값(binary pattern)을 생성
- 중심 픽셀보다 크거나 같으면 1, 작으면 0을 부여하여 8비트의 이진 코드 생성

## ✔ 동작방식
1. 얼굴 이미지를 3x3 픽셀 크기의 셀로 나눈다.
2. 셀 중심의 픽셀과 이웃하는 8방향의 픽셀을 비교해서 중심 픽셀의 값이 이웃 픽셀보다 크면 0 아니면 1로 표시하는 8자리 이진수 만든다.
3. 모든 셀의 8비트 숫자로 히스토그램을 개산하면 256차원의 특징벡터가 만들어지고 이것을 분류기의 학습 데이터로 사용해서 사용자의 얼굴을 분류한다.

## ✔ 장단점
| 구분 | 장점 | 단점 |
|------|------|------|
| 🎯 정확도 | 적절한 조건에서는 높은 정확도 | 조명, 표정, 각도 변화에 민감 |
| ⚙️ 구현 | 간단하고 구현 쉬움 | 복잡한 환경에서 성능 저하 |
| 💻 리소스 | CPU에서도 잘 작동, 경량 | 대규모 데이터 처리에는 부적합 |
| 📦 학습 데이터 | 적은 데이터로도 학습 가능 | 다양한 표정·조명에는 데이터 부족 시 오류 발생 |
| ⏱ 실시간 처리 | 빠른 처리 속도 (실시간 가능) | 고정된 환경 외에는 적용 범위 제한 |
| 📡 의존성 | 딥러닝 프레임워크 불필요 | 얼굴 방향 변화에 취약 |


</details>

---

# 📌 사람인식 어플리케이션 (LBPH 활용)

## 1. 목표
- 얼굴이 웹캠에 감지되면 사용자 이름 인식
- 인식된 얼굴이 웃고 있다면 "smile~~" 메시지를 크게 표시
- 정확도 기반 사용자 구분 (정확도 미달 시 "Unknown")

## 2. 사용 기술 및 도구
| 도구/기술              | 설명                   |
| ------------------ | -------------------- |
| Python             | 프로젝트 개발 언어           |
| OpenCV             | 이미지 처리 및 얼굴 인식 라이브러리 |
| Haar Cascade       | 얼굴/스마일 검출용 분류기       |
| LBPHFaceRecognizer | LBP 기반 얼굴 인식 알고리즘    |

## 3. 동작 흐름

#### 1. 모델 불러오기
```python
model.read(os.path.join(base_dir, 'all_face.xml'))
```
#### 2. 웹캠에서 프레임 읽기 + 얼굴 검출
```python
faces = face_classifier.detectMultiScale(gray, 1.3, 5)
```
#### 3. LBP 얼굴 인식 + 정확도 계산
```python
label, confidence = model.predict(face)
accuracy = int(100 * (1 - confidence / 400))
```
#### 4. 스마일 감지
```python
detected_smile = smile.detectMultiScale(face_roi_gray, scaleFactor=1.7, minNeighbors=22)
```
#### 4. 조건에 따른 메시지 출력
- 정확도 기준 이상인 경우 이름과 퍼센트 출력
- 스마일 감지시 `~~~smile~~~`큰 텍스트 출력

## 4. 출력 예시

#### 얼굴 인식
> <img width="300" height="400" alt="image" src="https://github.com/user-attachments/assets/54889c28-b360-497a-ab3e-57e1f30d72e5" />

#### 웃는 모습(smile) 인식
> <img width="300" height="400" alt="image" src="https://github.com/user-attachments/assets/c49d4eaf-b1f6-4997-ad85-01d35c0cdbf0" />


## 5. 실행
```bash
# haarcascade_frontalface_default.xml
# OpenCV의 data/haarcascades 디렉토리에서 사용 가능
# ./src
python lbp_test.py
```
---

# 📌 실시간 영상 얼굴 인식 + 모자이크

## 1. 목표
- 얼굴 검출 기능 사용
- 웹캠으로 출력되는 영상에서 자동으로 얼굴 인식
- 인식된 얼굴에 roi 설정 후 모자이크 처리

## 2. 주요기능
- 얼굴 검출: `haarcascade_frontalface_default.xml` 사용
- 모자이크 적용 여부: `Enter` 키로 전환
- `ESC` 키로 프로그램 종료
- 모자이크 대신 사각형 그리기(roi)로 얼굴 시각화 선택 가능
- 화면 좌측 상단에 키보드 안내 텍스트 표시

## 3. 출력 예시
#### 모자이크
> <img width="300" height="400" alt="image" src="https://github.com/user-attachments/assets/18ea47d8-94b0-467f-8dc2-476c8ac87fe1" />

#### 모자이크 ❌
> <img width="300" height="400" alt="image" src="https://github.com/user-attachments/assets/464688b9-07a4-4955-91b3-0ef0d842a375" />

## 4. 실행
```bash
# haarcascade_frontalface_default.xml
# OpenCV의 data/haarcascades 디렉토리에서 사용 가능
# ./src
python mosaic_test.py
```

---

