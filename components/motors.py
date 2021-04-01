import RPi.GPIO as GPIO
from time import sleep


class Motor:
    def __init__(self, motor_pin, forward_pin, backwards_pin):
        self._motor = None
        self._motor_pin = motor_pin

        self._forward_pin = forward_pin
        self._backwards_pin = backwards_pin

        self._duty_cycle = 0

    def setup(self):
        GPIO.setup(self._motor_pin, GPIO.OUT)
        GPIO.setup(self._forward_pin, GPIO.OUT)
        GPIO.setup(self._backwards_pin, GPIO.OUT)
        self._motor = GPIO.PWM(self._motor_pin, 100)

    def start(self):
        self._motor.start(self._duty_cycle)

        self.go_forward()

    def go_forward(self):
        GPIO.output(self._forward_pin, GPIO.HIGH)
        GPIO.output(self._backwards_pin, GPIO.LOW)

    def go_backwards(self):
        GPIO.output(self._forward_pin, GPIO.LOW)
        GPIO.output(self._backwards_pin, GPIO.HIGH)

    def stop(self):
        self._motor.ChangeDutyCycle(0)

    def change_duty_cycle(self, duty_cycle):
        self._duty_cycle = duty_cycle
        self._motor.ChangeDutyCycle(self._duty_cycle)


class Motors:
    def __init__(self, motor1, forward_pin1, backwards_pin1, motor2, forward_pin2, backwards_pin2):

        self._motor1 = Motor(motor1, forward_pin1, backwards_pin1)  # Left motor
        self._motor2 = Motor(motor2, forward_pin2, backwards_pin2)  # Right motor

        self.__setup__()

    def __setup__(self):
        GPIO.setmode(GPIO.BCM)

        # Setup motor 1
        self._motor1.setup()

        # Setup motor 2
        self._motor2.setup()

    @staticmethod
    def exit():
        pass
        # GPIO.cleanup()

    def start(self):
        self._motor1.start()
        self._motor2.start()

    def stop(self, t=0):
        self._motor1.stop()
        self._motor2.stop()

        sleep(t)

    def move(self, speed=0, turn=0, t=0):
        speed *= 100
        turn *= 100
        left_speed = -self.normalize((speed - turn), minimum=-100, maximum=100)
        right_speed = -self.normalize((speed + turn), minimum=-100, maximum=100)

        self._motor1.change_duty_cycle(abs(left_speed))
        self._motor2.change_duty_cycle(abs(right_speed))

        # Control left motor
        if left_speed > 0:
            self._motor1.go_backwards()
        else:
            self._motor1.go_forward()

        # Control right motor
        if right_speed > 0:
            self._motor2.go_backwards()
        else:
            self._motor2.go_forward()

        sleep(t)

    @staticmethod
    def normalize(value, minimum, maximum):
        if value > maximum:
            return maximum
        elif value < minimum:
            return minimum
        return value
