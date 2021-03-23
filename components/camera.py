import cv2
import pandas as pd
import os
import threading


class Camera:
    def __init__(self, cap_num=0):
        self._cap_num = cap_num
        self.cap = cv2.VideoCapture(self._cap_num)
        self.saved_frames = []
        self.saved_steering_info = []

    def save_frame(self, filename, joystick_value):
        if self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                frame = cv2.flip(frame, 1)
                cv2.imwrite(filename, frame)

                self.saved_frames.append(filename)
                self.saved_steering_info.append(joystick_value)

    def save_log(self, path):
        data = {'Image': self.saved_frames, 'Steering': self.saved_steering_info}

        df = pd.DataFrame(data)
        df.to_csv(path, index=False, header=False)

        self.saved_frames = []
        self.saved_steering_info = []

        print(f'Log {path} saved')

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
                    cv2.imwrite(f'{frame_num}.jpg', frame)
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

    def create_new_set(self, path, event):
        os.mkdir(path)
        i = 0

        while not event.isSet():
            self.save_frame(os.path.join(path, str(i) + '.jpg'), i / 10)
            i += 1
            # print(f'saved frame {i}')

        print('saved all frames')
        self.save_log(os.path.join(path, f'data.csv'))

    @staticmethod
    def exit():
        cv2.destroyAllWindows()
