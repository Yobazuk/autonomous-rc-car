import cv2
import os
import pandas as pd


class DataCollector:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.saved_frames = []
        self.saved_steering_info = []
        self.current_path = ''
        self.folder_count = 0
        self.frame_count = 0

    def save_frame(self, frame, joystick_value):
        filename = os.path.join(self.current_path, (str(self.frame_count) + '.jpg'))
        cv2.imwrite(filename, frame)
        self.saved_frames.append(filename)
        self.saved_steering_info.append(joystick_value)
        self.frame_count += 1

    def save_log(self):
        data = {'image_path': self.saved_frames, 'steering': self.saved_steering_info}

        df = pd.DataFrame(data)
        df.to_csv(os.path.join(self.current_path, 'data.csv'), index=False, header=True)

        self.saved_frames = []
        self.saved_steering_info = []

    def update_path(self):
        while os.path.exists(os.path.join(self.dataset_path, f'SET{str(self.folder_count)}')):
            self.folder_count += 1
        return os.path.join(self.dataset_path, f'SET{str(self.folder_count)}')

    def start(self):
        self.current_path = self.update_path()
        os.mkdir(self.current_path)
        print(f'Created new set {self.current_path}')

    def stop(self):
        self.save_log()
        print(f'Log {self.current_path} saved with {self.frame_count} frames')
        self.frame_count = 0
