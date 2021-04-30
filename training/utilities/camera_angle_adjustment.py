import cv2


def empty(a):
    pass


def main():

    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Line Height")
    cv2.resizeWindow("Line Height", 640, 30)
    cv2.createTrackbar("Line Height", "Line Height", 240, 480, empty)

    while True:
        _, frame = cam.read()

        line_height = cv2.getTrackbarPos("Line Height", "Line Height")
        frame = cv2.line(frame, (0, line_height), (frame.shape[1], line_height), (0, 0, 255), 2)
        frame = cv2.circle(frame, (320, 240), 5, (0, 255, 0), 2)

        cv2.imshow('frame', frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
