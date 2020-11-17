from ultrasonic_sensor import UltrasonicSensor
from time import sleep


def main():
    sensor = UltrasonicSensor(1, 2)

    try:
        while True:
            dist = sensor.measure_distance()
            print("Measured Distance = %.1f cm" % dist)
            sleep(0.5)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        sensor.exit()


if __name__ == '__main__':
    main()
