import cv2


sign_cascade = cv2.CascadeClassifier('./stopsign_classifier.xml')

color = 150
counter = 0
cap = cv2.VideoCapture(0)

# video capture loop
while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    img = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cv2.imshow('Stop sign detection', img)
    cv2.imshow('original', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    print(counter)

cv2.destroyAllWindows()
cap.release()
