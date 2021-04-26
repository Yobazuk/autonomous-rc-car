import cv2
import numpy as np
import tensorflow as tf
from utils import *
import matplotlib.pyplot as plt

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

model_path = r'steering_model.tflite'
cam = cv2.VideoCapture(0)

interpreter = tf.lite.Interpreter(model_path=model_path)
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
interpreter.allocate_tensors()

while True:
    # frame = cv2.imread(r'dataset\SET3\64.jpg')
    _, frame = cam.read()
    frame = frame.astype(np.float32) / 255.0

    frame, _ = preprocess(frame)

    plt.title('test')
    plt.imshow(frame)
    plt.show()

    # cv2.imshow('f', frame.numpy())

    interpreter.set_tensor(input_details[0]['index'], [frame])

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])

    steering = float(output_data)
    print(steering)

    cv2.waitKey(1)
