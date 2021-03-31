import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import cv2
import tensorflow as tf
from imgaug import augmenters as iaa
import matplotlib.image as mpimg


def read_image(path, label):
    image = tf.io.read_file(path)
    image = tf.image.decode_image(image, channels=3, dtype=tf.float32)
    # image = mpimg.imread(path)
    return image, label


def augment_image(image, label):
    if np.random.choice([0, 1]):
        # Translation
        ''' OpenCV method
        translation_matrix = np.float32([[1, 0, np.random.randint(-15, 16)], [0, 1, np.random.randint(-15, 16)]])
        image = cv2.warpAffine(image, translation_matrix, image.shape[:2][::-1])
        '''
        translation = iaa.Affine(translate_percent={"x": (-0.05, 0.05), "y": (-0.05, 0.05)})
        image = translation.augment_image(image)

    if np.random.choice([0, 1]):
        # Zoom
        ''' OpenCV method
        scale = np.random.randint(30)
        image = image[0+scale:image.shape[0]-scale, 0+scale:image.shape[1]-scale]
        image = cv2.resize(image, image.shape[:2][::-1])
        '''
        zoom = iaa.Affine(scale=(1, 1.2))
        image = zoom.augment_image(image)

    if np.random.choice([0, 1]):
        # Brightness
        brightness = iaa.Multiply((0.5, 1.2))
        image = brightness.augment_image(image)

    if np.random.choice([0, 1]):
        # Flip
        image = cv2.flip(image, 1)
        label = -label

    return image, label


def visualize_data(data):
    plt.hist(data['steering'], 30, color='#916cad', align='mid')

    plt.axhline(300, color='#adf182', linewidth=3)
    plt.title('Data Visualization')
    plt.xlabel('Steering Angle')
    plt.ylabel('Number of Samples')
    plt.show()


def balance_data(data):
    # balance data
    return data


def preprocess(image):
    # image = image[54:120, :, :]
    image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    # image = cv2.resize(image, (200, 66))
    # image = image / 255
    return image


def data_generator(image_paths, steering_list, batch_size):
    while True:
        images_batch = []
        steering_batch = []

        for i in range(batch_size):
            # index = np.random.randint(0, len(image_paths) - 1)
            img, steering = augment_image(read_image(image_paths[i]), steering_list[i])
            img = preprocess(img)
            images_batch.append(img)
            steering_batch.append(steering)
        yield np.asarray(images_batch), np.asarray(steering_batch)
