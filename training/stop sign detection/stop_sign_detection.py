import cv2
from time import sleep


sign_cascade = cv2.CascadeClassifier('./stopsign_classifier.xml')

color = (150, 0, 0)
counter = 0
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))

    signs = sign_cascade.detectMultiScale(frame)

    for (x, y, w, h) in signs:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        area = w*h
        print(area)

    cv2.imshow('original', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
