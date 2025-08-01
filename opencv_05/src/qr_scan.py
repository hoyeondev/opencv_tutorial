import cv2
import matplotlib.pyplot as plt
import pyzbar.pyzbar as pyzbar

img = cv2.imread('../img/frame.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# plt.imshow(img)
# plt.imshow(gray, cmap='gray')
# plt.show()

# 디코딩
decoded = pyzbar.decode(gray)
print(decoded)

for d in decoded:
    print(d.data.decode('utf-8'))
    print(d.type)
    barcode_data = d.data.decode('utf-8')
    barcode_type = d.type
    text = f'Data: {barcode_data}\nType: {barcode_type}'

    cv2.rectangle(img, (d.rect[0], d.rect[1]),(d.rect[0] + d.rect[2], d.rect[1] + d.rect[3]), (0, 255, 0), 20)
    cv2.putText(img, text, (d.rect[0], d.rect[3]), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)

plt.imshow(img)
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()