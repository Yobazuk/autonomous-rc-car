import cv2


def main():
    print('space (or any other key) - continue\nz - don\'t save image\nc - select new ROI\nq - exit')

    # cap = cv2.VideoCapture(0)
    roi = (0, 0, 0, 0)
    image_count = 0
    i = 0
    save = True

    # video capture loop
    while True:

        image_count += 1
        save = True
        frame = cv2.imread(f'./images/{image_count}.jpg')  # cap.read()
        frame = cv2.flip(frame, 1)

        x, y, w1, h1 = roi[0], roi[1], roi[2], roi[3]
        f = cv2.rectangle(frame.copy(), (x, y), (x + w1, y + h1), (255, 0, 0), 3)
        cv2.imshow('before', f)

        key = cv2.waitKey(0)
        if key == ord('c'):
            roi = cv2.selectROI("select ROI", frame, False, False)
        elif key == ord('z'):
            save = False
        elif key == ord('q'):
            break

        if roi != (0, 0, 0, 0):
            frame = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
            print(roi)
        else:
            print('Not saved')

        if save:
            i += 1
            cv2.imshow('after crop', frame)
            cv2.imwrite(f'./cropped images/{i}.jpg', frame)

    cv2.destroyAllWindows()
    # cap.release()


if __name__ == '__main__':
    main()
