from components.motors import Motors
from components.joystick import Joystick
import cv2
import json
from training.steering.utils import *
import numpy as np
import tensorflow as tf

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

with open('config.json') as f:
    config = json.load(f)

turn_sensitivity = config['turn_sensitivity']
model_path = r'training\steering\steering_model.tflite'


def main():
    interpreter = tf.lite.Interpreter(model_path=model_path)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.allocate_tensors()

    joystick = Joystick()
    cam = cv2.VideoCapture(0)
    motors = Motors(*config['left_motor'].values(), *config['right_motor'].values())
    motors.start()

    while True:
        joystick_values = joystick.get_buttons()
        _, frame = cam.read()

        frame = frame.astype(np.float32) / 255.0
        frame, _ = preprocess(frame)

        interpreter.set_tensor(input_details[0]['index'], [frame])
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        motors.move(float(output_data),
                    (joystick_values[config['drive_axis']] * turn_sensitivity), 0.1)


if __name__ == '__main__':
    main()
