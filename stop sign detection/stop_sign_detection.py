import cv2


sign_cascade = cv2.CascadeClassifier('./stopsign_classifier.xml')

color = 150
counter = 0
cap = cv2.VideoCapture(0)

# video capture loop
while True:
    check, frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx=(3 / 4) * 2, fy=(3 / 4) * 2)
    img = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * 1.5)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * 1.5)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # draw center frame
    cv2.circle(frame, (int(w / 2), int(h / 2)), 16, (0, 0, 255))
    cv2.putText(frame, str(fps), (0 + 10, h - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # Detect signs
    signs = sign_cascade.detectMultiScale(img, 1.1, 4)

    if len(signs) > 0:
        counter += 1
    else:
        counter = 0

    if counter >= 10:
        cv2.putText(frame, 'STOP', (int(w/2) - 200, int(h/2)), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0, 255), 10)

    # Draw the rectangle around each face
    for (x, y, w1, h1) in signs:
        x, y, w1, h1 = x * 4, y * 4, w1 * 4, h1 * 4
        cv2.rectangle(frame, (x, y), (x + w1, y + h1), (color, 0, 0), 3)
        cv2.circle(frame, (int(x+(w1/2)), int(y+(h1/2))), 15, (0, 255, 0))
        cv2.arrowedLine(frame, (int(w / 2), int(h / 2)), (int(x+(w1/2)), int(y+(h1/2))), (255, 0, 230), 2)

    cv2.imshow('Stop sign detection', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    print(counter)

cv2.destroyAllWindows()
cap.release()
