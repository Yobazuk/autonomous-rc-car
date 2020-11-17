from motors import Motors
from joystick import Joystick
from time import sleep


def main():
    motors = Motors(25, 24, 23, 22, 17, 27)
    motors.start()
    joystick = Joystick()

    while True:
        js_value = joystick.get_buttons()
        print(js_value)
        motors.move(js_value['axis2'], js_value['axis1'], 0.1)


if __name__ == '__main__':
    main()
