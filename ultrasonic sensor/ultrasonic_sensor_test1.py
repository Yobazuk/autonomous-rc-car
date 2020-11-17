import RPi.GPIO as gpio
import time


def distance():
    gpio.setmode(gpio.BCM)

    trig = 8
    echo = 10

    gpio.setup(trig, gpio.OUT)
    gpio.output(trig, 0)

    gpio.setup(echo, gpio.IN)

    time.sleep(0.1)

    print('Starting....')

    gpio.output(trig, 1)
    time.sleep(0.00001)
    gpio.output(trig, 0)

    while gpio.input(echo) == 0:
        pass

    start = time.time()

    while gpio.input(echo) == 1:
        pass

    stop = time.time()

    print(f"The distance is: {(stop - start) * 17000} cm")


if __name__ == '__main__':
    distance()
    gpio.cleanup()
