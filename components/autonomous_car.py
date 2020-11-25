from components.motors import Motors
from components.joystick import Joystick
from components.camera import Camera
from components.ultrasonic_sensor import UltrasonicSensor
from _thread import start_new_thread

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
        self.joystick_values = {}
        self.sensor_distance = 0

    def drive(self):
        start_new_thread(self.get_joystick_buttons, ())
        start_new_thread(self.camera.capture_frames, ())
        start_new_thread(self.measure_distance, ())
        start_new_thread(self.drive_motors, ())

    def drive_motors(self):
        self.motors.start()
        drive = True
        try:
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
        except KeyboardInterrupt:
            print('Motors stopped')
            self.motors.exit()

    def get_joystick_buttons(self):
        try:
            while True:
                self.joystick_values = self.joystick.get_buttons()
        except KeyboardInterrupt:
            print('Joystick stopped')

    def measure_distance(self):
        try:
            while True:
                self.sensor_distance = self.ultrasonic_sensor.measure_distance()
        except KeyboardInterrupt:
            print('Ultrasonic sensor stopped')
            self.ultrasonic_sensor.exit()

    def camera_preview(self):
        try:
            self.camera.capture_frames()
        except KeyboardInterrupt:
            print('Camera preview stopped')

    def exit(self):
        self.motors.exit()
        self.ultrasonic_sensor.exit()


def main():
    car = AutonomousCar(Motors(25, 24, 23, 22, 27, 17), Joystick(), Camera(), UltrasonicSensor(15, 14))
    car.drive()


if __name__ == '__main__':
    main()
