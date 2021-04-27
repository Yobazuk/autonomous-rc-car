import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from utils import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


def main():

    dataset_path = r'C:\Users\yobaz\Desktop\dataset'

    df = []

    for directory in os.listdir(dataset_path):
        df.append(pd.read_csv(os.path.join(dataset_path, directory, 'data.csv')))

    df = pd.concat(df)

    visualize_data(df)

    image_paths = df['image_path'].values
    steering = df['steering'].values

    for i in range(len(image_paths)):
        image_paths[i] = os.path.join(dataset_path, image_paths[i].split('/')[-2], image_paths[i].split('/')[-1])

    images_train, images_val, steering_train, steering_val = train_test_split(image_paths, steering,
                                                                              test_size=0.2, random_state=10)

    images_train, steering_train = balance_data(images_train, steering_train)
    visualize_data({'steering': steering_train})

    ds_train = tf.data.Dataset.from_tensor_slices((images_train, steering_train))
    ds_train = ds_train.map(read_image).map(augment_image).map(preprocess).batch(2)

    ds_validate = tf.data.Dataset.from_tensor_slices((images_val, steering_val))
    ds_validate = ds_validate.map(read_image).map(augment_image).map(preprocess).batch(2)

    model = Sequential([
                        # Convolutional feature maps
                        Convolution2D(24, (5, 5), (2, 2), input_shape=(200, 66, 3), activation='elu'),
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

    model.compile(Adam(lr=0.0001), loss='mse', metrics=["accuracy"])

    model.fit(ds_train, epochs=10, validation_data=ds_validate, verbose=1)

    if input('Save the model? (y/n): ').lower() == 'y':
        model.save('steering_model.h5')
        print('model saved')


if __name__ == '__main__':
    main()
