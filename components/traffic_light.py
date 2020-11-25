import RPi.GPIO as gpio
import time
from enum import Enum


class Light(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2


class TrafficLight:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.lights = {Light.RED: self.red, Light.YELLOW: self.yellow, Light.GREEN: self.green}
        self.__setup()

    def __setup(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.red, gpio.OUT)
        gpio.setup(self.yellow, gpio.OUT)
        gpio.setup(self.green, gpio.OUT)

    def activate(self, light):
        gpio.output(self.lights[light], 1)

    def deactivate(self, light):
        gpio.output(self.lights[light], 0)

    def pulse(self, light, t):
        self.activate(light)
        time.sleep(t)
        self.deactivate(light)
        time.sleep(t)


def main():
    r = 18
    y = 15
    g = 14

    tl = TrafficLight(r, y, g)

    for i in range(5):
        tl.pulse(Light.GREEN, 0.2)
        tl.pulse(Light.RED, 0.2)


if __name__ == '__main__':
    main()
    gpio.cleanup()
