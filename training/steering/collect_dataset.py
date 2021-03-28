from autonomous_car import AutonomousCar
from components.motors import Motors
from components.joystick import Joystick
from components.camera import Camera
from components.ultrasonic_sensor import UltrasonicSensor
import json

with open('config.json') as f:
    config = json.load(f)


def main():
    car = AutonomousCar(Motors(*config['left_motor'].values(), *config['right_motor'].values()), Joystick(),
                        Camera(), UltrasonicSensor(*config['ultrasonic_sensor'].values()))
    try:
        car.collect_dataset()
        while True:
            pass
    except KeyboardInterrupt:
        car.exit()
        print('Car ended')


if __name__ == '__main__':
    main()
