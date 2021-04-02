from components.motors import Motors
from components.joystick import Joystick
import pandas as pd
import os
import cv2
import json


with open('config.json') as f:
    config = json.load(f)

PAUSE_DATASET_BTN = config['PAUSE_DATASET_BTN']
RESUME_DATASET_BTN = config['RESUME_DATASET_BTN']
DATASET_PATH = os.path.join(os.getcwd(), 'dataset/')

saved_frames = []
saved_steering_info = []
collect_data = False
collecting_data = False
turn_sensitivity = config['turn_sensitivity']
folder_count = 0


def save_frame(frame, filename, joystick_value):
    global saved_frames, saved_steering_info

    cv2.imwrite(filename, frame)
    saved_frames.append(filename)
    saved_steering_info.append(joystick_value)


def save_log(path):
    global saved_frames, saved_steering_info
    data = {'image_path': saved_frames, 'steering': saved_steering_info}

    df = pd.DataFrame(data)
    df.to_csv(path, index=False, header=True)

    saved_frames = []
    saved_steering_info = []

    print(f'Log {path} saved')


def update_path():
    global folder_count, DATASET_PATH

    while os.path.exists(os.path.join(DATASET_PATH, f'SET{str(folder_count)}')):
        folder_count += 1
    return os.path.join(DATASET_PATH, f'SET{str(folder_count)}')


def main():
    global saved_frames, saved_steering_info, collect_data, collecting_data, turn_sensitivity

    joystick = Joystick()
    cam = cv2.VideoCapture(0)
    motors = Motors(*config['left_motor'].values(), *config['right_motor'].values())

    path = ''
    frame_count = 0

    while True:
        joystick_values = joystick.get_buttons()

        if joystick_values[PAUSE_DATASET_BTN]:
            collect_data = False

        if joystick_values[RESUME_DATASET_BTN]:
            collect_data = True

        if collect_data and not collecting_data:
            path = update_path()
            os.mkdir(path)
            collecting_data = True

        if not collect_data and collecting_data:
            save_log(path)
            collecting_data = False

        if collecting_data:
            _, frame = cam.read()
            save_frame(frame, os.path.join(path, str(frame_count), '.jpg'), joystick_values[config['turn_axis']])
            frame_count += 1

        motors.move(joystick_values[config['drive_axis']],
                    (joystick_values[config['turn_axis']] * turn_sensitivity), 0.1)


if __name__ == '__main__':
    main()
