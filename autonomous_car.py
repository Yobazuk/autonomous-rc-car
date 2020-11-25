from components.motors import Motors
from components.joystick import Joystick
from components.camera import Camera
from components.ultrasonic_sensor import UltrasonicSensor
from _thread import start_new_thread
import RPi.GPIO as gpio

EXIT_MOTORS_BTN = 'x'
STOP_JOYSTICK_BTN = 'a'
RESUME_MOTORS_BTN = 'b'


class AutonomousCar:
    def __init__(self, motors, joystick, camera, ultrasonic_sensor, turn_sensitivity=0.7):
        self.motors = motors
        self.joystick = joystick
        self.camera = camera
        self.ultrasonic_sensor = ultrasonic_sensor

        self.turn_sensitivity = turn_sensitivity
        self.joystick_values = {'a': 0, 'b': 0, 'x': 0, 'y': 0, 'L1': 0, 'R1': 0, 'L2': 0, 'R2': 0,
                                'share': 0, 'options': 0, 'axis1': 0., 'axis2': 0., 'axis3': 0., 'axis4': 0.}
        self.sensor_distance = 0

    def drive(self):
        start_new_thread(self.get_joystick_buttons, ())
        start_new_thread(self.camera_preview, ())
        start_new_thread(self.measure_distance, ())
        start_new_thread(self.drive_motors, ())

    def drive_motors(self):
        print('starting motors...')
        self.motors.start()
        drive = True

        while True:
            if self.joystick_values[EXIT_MOTORS_BTN]:
                self.motors.exit()
                break
            if self.joystick_values[STOP_JOYSTICK_BTN]:
                drive = False
            if self.joystick_values[RESUME_MOTORS_BTN]:
                drive = True
            if drive:
                self.motors.move(self.joystick_values['axis1'],
                                 (self.joystick_values['axis2'] * self.turn_sensitivity), 0.1)

    def get_joystick_buttons(self):
        print('getting joystick buttons...')
        while True:
            self.joystick_values = self.joystick.get_buttons()

    def measure_distance(self):
        print('measuring distance...')
        while True:
            self.sensor_distance = self.ultrasonic_sensor.measure_distance()
            print('Measured distance = %.1f cm', self.sensor_distance)

    def camera_preview(self):
        print('getting camera preview...')
        self.camera.capture_frames()

    def exit(self):
        self.motors.exit()
        self.ultrasonic_sensor.exit()
        gpio.cleanup()


def main():
    car = AutonomousCar(Motors(25, 24, 23, 22, 27, 17), Joystick(), Camera(), UltrasonicSensor(15, 14))
    try:
        car.drive()
        while True:
            pass
    except KeyboardInterrupt:
        car.exit()
        print('Car ended')


if __name__ == '__main__':
    main()
