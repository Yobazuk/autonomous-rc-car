from autonomous_car import AutonomousCar
from components.motors import Motors
from components.joystick import Joystick
from components.camera import Camera
from components.ultrasonic_sensor import UltrasonicSensor


def main():
    car = AutonomousCar(Motors(25, 24, 23, 22, 27, 17), Joystick(), Camera(), UltrasonicSensor(15, 14))
    try:
        car.collect_dataset()
        while True:
            pass
    except KeyboardInterrupt:
        car.exit()
        print('Car ended')


if __name__ == '__main__':
    main()
