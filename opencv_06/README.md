# 📌 이미지 매칭 (평균 해시 매칭, 템플릿 매칭)
- 참고 : [내용](https://bkshin.tistory.com/entry/OpenCV-25-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%A7%A4%EC%B9%AD-%ED%8F%89%EA%B7%A0-%ED%95%B4%EC%8B%9C-%EB%A7%A4%EC%B9%AD-%ED%85%9C%ED%94%8C%EB%A6%BF-%EB%A7%A4%EC%B9%AD)
- 서로 다른 두 이미지를 비교해서 짝이 맞는 형태의 객체가 있는지 찾아내는 기술
- 이미지 간 유사도를 측정하는 작업

## ✔ 평균 해시 매칭

## ✔ 템플릿 매칭

# 📌 이미지의 특징점(Keypoints) 검출
- 참고 : [내용](https://bkshin.tistory.com/entry/OpenCV-26-%EC%9D%B4%EB%AF%B8%EC%A7%80%EC%9D%98-%ED%8A%B9%EC%A7%95%EA%B3%BC-%ED%82%A4-%ED%8F%AC%EC%9D%B8%ED%8A%B8?category=1148027)
- 이미지끼리 서로 매칭이 되는지 확인을 할 때 각 이미지에서의 특징이 되는 부분끼리 비교를 한다.
- 보통 특징점이 되는 부분은 물체의 모서리나 코너

## ✔ 해리스 코너 검출


# 📌 상품라벨 스캐너

## 1. 목표
1. 라벨 스캔 → 상품을 카메라 앞에 위치
2. ROI 생성 → 스페이스바 + 마우스 드래그로 라벨 영역 선택
3. 매칭 테스트 → 같은/다른 상품으로 인식 성능 확인

#### 이미지 매칭 성공
> <img width="450" height="497" alt="image" src="https://github.com/user-attachments/assets/523b3a32-30f2-4b6d-8885-c686bf469566" />

#### 이미지 매칭 실패
> <img width="450" height="489" alt="image" src="https://github.com/user-attachments/assets/c13ba9a8-be6d-4429-82b0-cf509cf97078" />
