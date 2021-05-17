import RPi.GPIO as GPIO
import time

TIMEOUT = 0.2   # [seconds]


class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin, speed_of_sound=34300):

        self._trig_pin = trigger_pin
        self._echo_pin = echo_pin
        self._speed_of_sound = speed_of_sound

        self.__setup__()

    def __setup__(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._trig_pin, GPIO.OUT)
        GPIO.setup(self._echo_pin, GPIO.IN)

    @staticmethod
    def exit():
        pass
        # GPIO.cleanup()

    def measure_distance(self):

        GPIO.output(self._trig_pin, 1)
        time.sleep(0.00001)
        GPIO.output(self._trig_pin, 0)

        timeout_start = time.time()
        while GPIO.input(self._echo_pin) == 0:
            if time.time() >= timeout_start + TIMEOUT:
                break

        start_time = time.time()

        timeout_start = time.time()
        while GPIO.input(self._echo_pin) == 1:
            if time.time() >= timeout_start + TIMEOUT:
                break
        stop_time = time.time()

        distance = (stop_time - start_time) * (self._speed_of_sound / 2)

        return distance
