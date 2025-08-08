 
 
# 📌 EasyOCR 

- 참고 : [튜토리얼](https://www.jaided.ai/easyocr/tutorial/), [공식Github](https://github.com/JaidedAI/EasyOCR)
-  파이썬 기반의 광학 문자 인식 (OCR: Optical Character Recognition) 라이브러리
-  딥러닝 기반의 문자 인식 모델을 사용하여 다양한 언어의 텍스트를 이미지에서 추출할 수 있도록 설계
-  PyTorch 기반으로 동작하며, GPU 및 CPU 모두 지원

> <img width="500" height="450" alt="image" src="https://github.com/user-attachments/assets/5b5ce1eb-1078-4beb-b5f1-b918ede9525c" />

## ✔ 설치방법
```bash
pip install easyocr
```

## ✔ 기본 사용법
```python
import easyocr
import cv2
import matplotlib.pyplot as plt

# Reader 객체 생성 (한글 + 영어 지원)
reader = easyocr.Reader(['ko', 'en'], gpu=False)

# 이미지 로드
img_path = '../img/ko_sign.png'
img = cv2.imread(img_path)

# 텍스트 인식
result = reader.readtext(img_path)

# 결과 출력
for bbox, text, confidence in result:
    print(f'Text: {text}, Confidence: {confidence:.2f}')

```

---
