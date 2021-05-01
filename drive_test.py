from components.motors import Motors
import cv2
import json
from training.steering.utils import preprocess
import numpy as np
import tensorflow as tf
import RPi.GPIO as GPIO

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

with open('config.json') as f:
    config = json.load(f)

turn_sensitivity = config['turn_sensitivity']
idle_throttle = config['idle_throttle']
model_path = r'training\steering\steering_model.tflite'


def main():
    interpreter = tf.lite.Interpreter(model_path=model_path)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.allocate_tensors()

    cam = cv2.VideoCapture(0)
    motors = Motors(*config['left_motor'].values(), *config['right_motor'].values())
    motors.start()

    while True:
        _, frame = cam.read()

        frame = frame.astype(np.float32) / 255.0
        frame, _ = preprocess(frame)

        interpreter.set_tensor(input_details[0]['index'], [frame])
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        steering = float(output_data)
        print(f'steering: {steering}')

        motors.move(idle_throttle,
                    (steering * turn_sensitivity), 0.1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('car ended')
