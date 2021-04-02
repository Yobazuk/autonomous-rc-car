from components.motors import Motors
from components.joystick import Joystick
from components.camera import Camera
import pandas as pd
import os
import cv2


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


def create_new_set(self, path, event, joystick_values):
    os.mkdir(path)
    i = 0

    while not event.isSet():
        self.save_frame(os.path.join(path, str(i) + '.jpg'), joystick_values[config['drive_axis']])
        i += 1

    print('saved all frames')
    self.save_log(os.path.join(path, f'data.csv'))


def main():
    joystick = Joystick()
    camera = Camera()


if __name__ == '__main__':
    main()
