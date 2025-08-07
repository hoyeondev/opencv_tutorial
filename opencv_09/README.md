# 📌 하르 캐스케이드 얼굴 검출 (Haar Cascade Face Detection)

<details>
<summary>내용보기 🔽</summary>

  - 참고 : [내용1](http://atonrq.synology.me:1700/hypha/haarcascade), [내용2](https://bkshin.tistory.com/entry/%EC%BB%B4%ED%93%A8%ED%84%B0-%EB%B9%84%EC%A0%84-1-%ED%95%98%EB%A5%B4-%EC%BA%90%EC%8A%A4%EC%BC%80%EC%9D%B4%EB%93%9C-%EC%96%BC%EA%B5%B4-%EA%B2%80%EC%B6%9C-Haar-Cascade-Face-Detection)
- 개발자가 집접 머신러닝 학습 알고리즘을 사용하지 않고도 객체를 검출할 수 있도록 OpenCV가 제공하는 대표적인 상위 레벨 API
- OpenCV는 케스케이드 분류기에서 사용할 수 있는 훈련된 검출기를 xml 파일 형태로 제공한다.


> <img width="450" height="500" alt="image" src="https://github.com/user-attachments/assets/e077cc7b-0e0e-4b37-9188-96c19b452d75" />


</details>

# 📌 LBPH(Local Binary Patterns Histograms) 알고리즘


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
