import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam


def main():
    model = Sequential([
                        # Convolutional feature maps
                        Convolution2D(24, (5, 5), (2, 2), input_shape=(66, 200, 3), activation='elu'),
                        Convolution2D(36, (5, 5), (2, 2), activation='elu'),
                        Convolution2D(48, (5, 5), (2, 2), activation='elu'),
                        Convolution2D(64, (3, 3), activation='elu'),
                        Convolution2D(64, (3, 3), activation='elu'),

                        Flatten(),
                        # Fully connected layers
                        Dense(100, activation='elu'),
                        Dense(50, activation='elu'),
                        Dense(10, activation='elu'),
                        Dense(1)]
                       )

    model.compile(Adam(lr=0.0001), loss='mse')


if __name__ == '__main__':
    main()
