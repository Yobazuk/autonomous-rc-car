import cv2


class Camera:
    def __init__(self, cap_num=0):
        self._cap_num = cap_num

    def capture_frames(self, show_preview=True, save_frames=False, path='./', flipped=True, max_frames=-1, joystick_value=0):
        cap = cv2.VideoCapture(self._cap_num)

        frame_num = 0

        while cap.isOpened() and max_frames != 0:
            ret, frame = cap.read()

            if ret:
                max_frames -= 1
                frame_num += 1

                if flipped:
                    frame = cv2.flip(frame, 1)

                if show_preview:
                    cv2.imshow('frame', frame)

                if save_frames:
                    cv2.imwrite(f'{path}{frame_num}.jpg', frame)
                    with open('data.txt', 'w+') as file:
                        turn_value = 'No Data'
                        if joystick_value:
                            turn_value = joystick_value
                        file.write(f'{path}{frame_num}.jpg,{turn_value}')

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            else:
                print(f'Frame #{frame_num} not captured')

        cap.release()
        cv2.destroyAllWindows()

    def capture_image(self, filename, path='./'):
        cap = cv2.VideoCapture(self._cap_num)
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(f'{path}{filename}.jpg', frame)
        else:
            print(f'Image capture failed')

    def capture_video(self, filename, path='./', codec='XVID', fps=30, res=(640, 480), show_preview=True, flipped=True):
        cap = cv2.VideoCapture(self._cap_num)

        fourcc = cv2.VideoWriter_fourcc(*f'{codec}')
        out = cv2.VideoWriter(f'{path}{filename}', fourcc, fps, res)

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                if flipped:
                    frame = cv2.flip(frame, 1)

                out.write(frame)

                if show_preview:
                    cv2.imshow(f'{filename}', frame)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            else:
                print(f'Video capture failed')

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    @staticmethod
    def exit():
        cv2.destroyAllWindows()
