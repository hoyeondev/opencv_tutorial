# 📌 TensorFlow
- 참고 : [내용](https://bkshin.tistory.com/entry/%EC%BB%B4%ED%93%A8%ED%84%B0-%EB%B9%84%EC%A0%84-5-%EC%96%BC%EA%B5%B4-%EC%9D%B4%EB%AF%B8%EC%A7%80%EC%97%90%EC%84%9C-%EA%B0%90%EC%A0%95-%EB%B6%84%EB%A5%98Emotion-Classification), [공식문서](https://www.tensorflow.org/about?hl=ko)
- Google Brain 팀에서 개발한 오픈소스 머신러닝/딥러닝 프레임워크
- 주로 딥러닝 모델 설계, 학습, 추론에 사용
- GPU, TPU, CPU에서 병렬 연산 지원
- Python, C++, JavaScript 등 다양한 언어 API 제공

## ✔ TensorFlow 주요 구성 요소

| 구성 요소                  | 설명                         |
| ---------------------- | -------------------------- |
| **Keras**              | 딥러닝 모델을 쉽게 만들 수 있는 고수준 API |
| **TensorBoard**        | 모델 학습 과정 및 성능 시각화 도구       |
| **TensorFlow Lite**    | 모바일/IoT 환경에 최적화된 경량 모델     |
| **TensorFlow Serving** | 학습된 모델을 배포·서비스하는 플랫폼       |
| **TF Datasets**        | 표준 데이터셋 로드 및 전처리 도구        |


## ✔ 기본 동작 흐름
1. 데이터 준비 → 전처리, 배치 처리
2. 모델 정의 → Keras API 또는 Custom Layer로 설계
3. 모델 컴파일 → 손실 함수, 옵티마이저, 메트릭 지정
4. 모델 학습 → `model.fit()` 사용
5. 모델 평가/예측 → `model.evaluate()`, `model.predict()`
6. 모델 저장/배포 → `model.save()` 또는 TF Serving
