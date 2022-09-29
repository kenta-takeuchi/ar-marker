import cv2
import numpy as np

v = cv2.VideoCapture(0)

while v.isOpened():
    r, f = v.read()
    if not r:
        break
    cv2.imshow("", f)
    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

v.release()
cv2.destroyAllWindows()
