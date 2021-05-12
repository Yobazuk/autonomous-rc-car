import argparse

parser = argparse.ArgumentParser(description='Start autonomous RC car in driving or data collection mode')

parser.add_argument('-p', '--preview', action='store_true', dest='preview', help='Display camera feed')

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('-d', '--drive', action='store_true', dest='mode', help='Start car in driving mode')
group.add_argument('-c', '--collect_data', action='store_false', dest='mode',
                   help='Start car in data collection mode')
parser.set_defaults(mode=True, preview=False)
args = parser.parse_args()

from components.motors import Motors
from components.joystick import Joystick
from components.camera import Camera
from components.ultrasonic_sensor import UltrasonicSensor
from components.data_collector import DataCollector
import RPi.GPIO as gpio
import json
import os
import numpy as np
from training.steering.utils import preprocess
import tensorflow as tf

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

with open('config.json') as f:
    config = json.load(f)

PAUSE_DATASET_BTN = config['PAUSE_DATASET_BTN']
RESUME_DATASET_BTN = config['RESUME_DATASET_BTN']
DATASET_PATH = os.path.join(os.getcwd(), 'dataset/')
TURN_SENSITIVITY = config['turn_sensitivity']
IDLE_THROTTLE = config['idle_throttle']
STEERING_MODEL_PATH = r'training\steering\steering_model.tflite'


class AutonomousCar:
    def __init__(self, steering_model='', dataset_path=''):
        self.motors = Motors(*config['left_motor'].values(), *config['right_motor'].values())
        self.camera = Camera()
        self.ultrasonic_sensor = UltrasonicSensor(*config['ultrasonic_sensor'].values())
        self.joystick = None

        if not args.mode:
            self.joystick = Joystick()

        self.dataset_path = dataset_path
        if not dataset_path:
            self.dataset_path = os.path.join(os.getcwd(), 'dataset/')

        if steering_model:
            self.interpreter = tf.lite.Interpreter(model_path=steering_model)
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.interpreter.allocate_tensors()

    def drive(self):
        print('Driving motors...')
        self.motors.start()

        while True:
            frame = self.camera.get_frame(preview=args.preview)

            steering = self.predict_steering(frame)
            throttle = IDLE_THROTTLE

            if self.ultrasonic_sensor.measure_distance() <= 0.1:
                throttle = 0

            print(f'Steering: {steering}')

            self.motors.move(throttle, (steering * TURN_SENSITIVITY), 0.1)

    def collect_dataset(self):
        print('Collecting dataset...')

        data_collector = DataCollector(self.dataset_path)
        self.motors.start()
        collect_data = False
        collecting_data = False

        while True:
            joystick_values = self.joystick.get_buttons()

            throttle = joystick_values[config['drive_axis']]

            if joystick_values[PAUSE_DATASET_BTN]:
                collect_data = False

            if joystick_values[RESUME_DATASET_BTN]:
                collect_data = True

            if collect_data and not collecting_data:
                data_collector.start()
                collecting_data = True

            if not collect_data and collecting_data:
                data_collector.stop()
                collecting_data = False

            if collecting_data:
                frame = self.camera.get_frame(preview=args.preview)
                data_collector.save_frame(frame, joystick_values[config['turn_axis']])
                throttle = IDLE_THROTTLE

            self.motors.move(throttle, (joystick_values[config['turn_axis']] * TURN_SENSITIVITY), 0.1)

    def predict_steering(self, frame):
        frame = frame.astype(np.float32) / 255.0
        frame, _ = preprocess(frame)

        self.interpreter.set_tensor(self.input_details[0]['index'], [frame])
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        return float(output_data)

    def exit(self):
        self.motors.exit()
        self.ultrasonic_sensor.exit()
        self.camera.exit()
        gpio.cleanup()


def main():
    car = AutonomousCar(steering_model=STEERING_MODEL_PATH)
    try:
        if args.mode:
            car.drive()
        else:
            car.collect_dataset()
    except KeyboardInterrupt:
        car.exit()
        print('Car ended')


if __name__ == '__main__':
    main()
