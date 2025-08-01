import cv2 
import matplotlib.pyplot as plt
import pyzbar.pyzbar as pyzbar
import webbrowser

cap = cv2.VideoCapture(0)
opened_urls = set()  # 이미 연 URL 중복 방지

while cap.isOpened():
    ret, img = cap.read()

    if not ret:
        continue

    # 카메라 좌우반전
    img = cv2.flip(img, 1)

    # 흑백 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # QR 코드 디코딩
    decoded = pyzbar.decode(gray)

    for d in decoded:
        x, y, w, h = d.rect
        barcode_data = d.data.decode('utf-8')
        barcode_type = d.type
        text = '%s (%s)' % (barcode_data, barcode_type)

        # 사각형 및 텍스트 표시
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # QR 코드가 URL이면 웹브라우저 열기
        if barcode_data.startswith('http') and barcode_data not in opened_urls:
            print(f"Opening URL: {barcode_data}")
            webbrowser.open(barcode_data)
            opened_urls.add(barcode_data)  # 같은 URL 중복 열림 방지

    cv2.imshow('camera', img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
