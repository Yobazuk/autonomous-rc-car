from components.joystick import Joystick


def main():
    joystick = Joystick()

    while True:
        print(joystick.get_buttons())


if __name__ == '__main__':
    main()
