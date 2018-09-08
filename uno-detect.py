import cv2
import numpy as np

uno_cascade = cv2.CascadeClassifier('uno-10-stages.xml')

cap = cv2.VideoCapture(0)

while True :
  ret, img = cap.read()
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  uno = uno_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 40)

  font = cv2.FONT_HERSHEY_SIMPLEX
  for (x, y, w, h) in uno :
    cv2.putText(img, 'UNO Card', (x,y), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)

  cv2.imshow('img', img)
  k = cv2.waitKey(30) & 0xFF
  if k == 27 :
    break

cap.release()
cv2.destroyAllWindows()
