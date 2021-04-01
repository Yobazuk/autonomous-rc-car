from components.motors import Motors
from components.joystick import Joystick
from components.camera import Camera
from components.ultrasonic_sensor import UltrasonicSensor
import RPi.GPIO as gpio
import json
import os
import threading
from time import sleep

with open('config.json') as f:
    config = json.load(f)

EXIT_BTN = config['EXIT_BTN']
PAUSE_MOTORS_BTN = config['PAUSE_MOTORS_BTN']
PAUSE_DATASET_BTN = config['PAUSE_DATASET_BTN']


class AutonomousCar:
    def __init__(self, motors, joystick, camera, ultrasonic_sensor, dataset_path='', turn_sensitivity=0.7):
        self.motors = motors
        self.joystick = joystick
        self.camera = camera
        self.ultrasonic_sensor = ultrasonic_sensor

        self.exit_event = threading.Event()
        self.pause_motors_event = threading.Event()
        self.pause_dataset_event = threading.Event()

        self.pause_dataset_event.set()

        self.dataset_path = dataset_path
        if not dataset_path:
            self.dataset_path = os.path.join(os.getcwd(), 'dataset/')

        self.turn_sensitivity = turn_sensitivity
        self.joystick_values = {'a': 0, 'b': 0, 'x': 0, 'y': 0, 'L1': 0, 'R1': 0, 'L2': 0, 'R2': 0,
                                'share': 0, 'options': 0, 'axis1': 0., 'axis2': 0., 'axis3': 0., 'axis4': 0.}
        self.sensor_distance = 0

    def drive(self):
        joystick_t = threading.Thread(target=self.get_joystick_buttons, args=(), daemon=True)
        camera_t = threading.Thread(target=self.camera_preview, args=(), daemon=True)
        distance_t = threading.Thread(target=self.measure_distance, args=(), daemon=True)
        motors_t = threading.Thread(target=self.drive_motors, args=(), daemon=True)

        joystick_t.start()
        camera_t.start()
        distance_t.start()
        motors_t.start()

        self.exit_event.wait()

        # Kill all threads
        self.exit()

    def collect_dataset(self):

        joystick_t = threading.Thread(target=self.get_joystick_buttons, args=())
        motors_t = threading.Thread(target=self.drive_motors, args=())

        joystick_t.start()
        motors_t.start()

        folder_count = 0

        while not self.exit_event.isSet():

            while os.path.exists(os.path.join(self.dataset_path, f'SET{str(folder_count)}')):
                folder_count += 1
            path = os.path.join(self.dataset_path, f'SET{str(folder_count)}')

            t = threading.Thread(target=self.camera.create_new_set, args=(path, self.pause_dataset_event, self.joystick_values))

            while self.pause_dataset_event.isSet():
                pass

            t.start()
            t.join()

            self.pause_dataset_event.wait()

        self.exit()

    def drive_motors(self):
        print('starting motors...')
        self.motors.start()

        while True:
            '''if self.joystick_values[EXIT_MOTORS_BTN]:
                self.motors.exit()
                break'''
            if not self.pause_motors_event.isSet():
                self.motors.move(self.joystick_values[config['drive_axis']],
                                 (self.joystick_values[config['turn_axis']] * self.turn_sensitivity), 0.1)

    def get_joystick_buttons(self):
        print('getting joystick buttons...')
        while True:
            self.joystick_values = self.joystick.get_buttons()

            # Handle buttons events
            if self.joystick_values[EXIT_BTN]:
                if self.exit_event.isSet():
                    self.exit_event.clear()
                else:
                    self.exit_event.set()
            if self.joystick_values[PAUSE_MOTORS_BTN]:
                if self.pause_motors_event.isSet():
                    self.pause_motors_event.clear()
                else:
                    self.pause_motors_event.set()
            if self.joystick_values[PAUSE_DATASET_BTN]:
                if self.pause_dataset_event.isSet():
                    self.pause_dataset_event.clear()
                    print('CLEARED')
                else:
                    self.pause_dataset_event.set()
                    print('PAUSED')

            sleep(0.1)

    def measure_distance(self):
        print('measuring distance...')
        while True:
            self.sensor_distance = self.ultrasonic_sensor.measure_distance()
            print('Measured distance = %.1f cm', self.sensor_distance)

    def camera_preview(self):
        print('getting camera preview...')
        self.camera.capture_frames()

    def get_camera_frames(self, show_preview=False, save_frames=True, path='./images/', flipped=True, max_frames=-1):
        print('getting camera frames...')
        self.camera.capture_frames(show_preview, save_frames, path, flipped, max_frames,
                                   joystick_value=self.joystick_values[config['turn_axis']])

    def exit(self):
        self.motors.exit()
        self.ultrasonic_sensor.exit()
        self.camera.exit()
        gpio.cleanup()


def main():
    car = AutonomousCar(Motors(*config['left_motor'].values(), *config['right_motor'].values()), Joystick(),
                        Camera(), UltrasonicSensor(*config['ultrasonic_sensor'].values()))
    try:
        car.drive()
        while True:
            pass
    except KeyboardInterrupt:
        car.exit()
        print('Car ended')


if __name__ == '__main__':
    main()
