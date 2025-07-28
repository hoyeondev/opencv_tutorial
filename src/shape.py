
import cv2
import numpy as np

# space = np.zeros((500, 1000), dtype=np.uint8)
space = np.zeros((768, 1388), dtype=np.uint8)
color = 255
# space = cv2.line(space, (100,100), (800,400), color, 3, 1) # 라인
# space = cv2.circle(space, (600,200), 100, color, 4, 1) # 원
# space = cv2.rectangle(space, (500, 200), (800, 400), color, 5, 1)  # 사각형
# space = cv2.ellipse(space, (500, 300), (300, 200), 0, 90, 250, color, 2)  # 타원

# 다각형
# obj1 = np.array([[300, 500], [500, 500], [400, 600], [200, 600]])
# obj2 = np.array([[600, 500], [800, 500], [700, 200]])
# space = cv2.polylines(space, [obj1], True, color, 3) # 다각형 그리기
# space = cv2.fillPoly(space, [obj2], color, 1) # 다각형 채우기

# 격자 간격 및 색상 설정
grid_spacing = 50
grid_color = 225

# 이미지에 격자 그리기
for x in range(0, space.shape[1], grid_spacing):
    cv2.line(space, (x, 0), (x, space.shape[0]), grid_color, 1)

for y in range(0, space.shape[0], grid_spacing):
    cv2.line(space, (0, y), (space.shape[1], y), grid_color, 1)

cv2.imshow('shape', space)  # Display the image with the line

cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()  # Close all OpenCV windows

