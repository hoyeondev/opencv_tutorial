
import cv2
import numpy as np

space = np.zeros((500, 1000), dtype=np.uint8)
line_color = 255
space = cv2.line(space, (100,100), (800,400), line_color, 3, 1)

cv2.imshow('Line', space)  # Display the image with the line

cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()  # Close all OpenCV windows

