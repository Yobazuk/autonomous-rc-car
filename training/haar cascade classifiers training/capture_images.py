import cv2


def main():

    i = 0
    cap = cv2.VideoCapture(0)

    while cap.isOpened():

        i += 1
        ret, frame = cap.read()

        if ret:
            frame = cv2.flip(frame, 1)

            cv2.imshow('frame', frame)
            cv2.imwrite(f'./images/{i}.jpg', frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
