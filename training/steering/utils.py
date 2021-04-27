import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf


def read_image(path, label):
    image = tf.io.read_file(path)
    image = tf.io.decode_image(image, channels=3, dtype=tf.float32)

    return image, label


def augment_image(image, label):

    # if np.random.choice([0, 1]):
    #     # Translation
    #     ''' OpenCV method
    #     translation_matrix = np.float32([[1, 0, np.random.randint(-15, 16)], [0, 1, np.random.randint(-15, 16)]])
    #     image = cv2.warpAffine(image, translation_matrix, image.shape[:2][::-1])
    #     '''
    #     translation = iaa.Affine(translate_percent={"x": (-0.05, 0.05), "y": (-0.05, 0.05)})
    #     image = translation.augment_image(image)
    #
    # if np.random.choice([0, 1]):
    #     # Zoom
    #     ''' OpenCV method
    #     scale = np.random.randint(30)
    #     image = image[0+scale:image.shape[0]-scale, 0+scale:image.shape[1]-scale]
    #     image = cv2.resize(image, image.shape[:2][::-1])
    #     '''
    #     zoom = iaa.Affine(scale=(1, 1.2))
    #     image = zoom.augment_image(image)
    #
    # if np.random.choice([0, 1]):
    #     # Brightness
    #     brightness = iaa.Multiply((0.5, 1.2))
    #     image = brightness.augment_image(image)
    #
    # if np.random.choice([0, 1]):
    #     # Flip
    #     image = cv2.flip(image, 1)
    #     label = -label if label else label

    image = tf.image.random_brightness(image, max_delta=0.15)

    image = tf.image.random_contrast(image, lower=0.8, upper=1.8)

    if np.random.choice([0, 1]):
        image = tf.image.flip_left_right(image)
        label = -label

    return image, label


def visualize_data(data):
    plt.hist(data['steering'], 30, color='#916cad', align='mid')

    plt.axhline(300, color='#adf182', linewidth=3)
    plt.title('Data Visualization')
    plt.xlabel('Steering Angle')
    plt.ylabel('Number of Samples')
    plt.show()


def balance_data(images, labels, num_to_remove=2900):
    # balance data

    for j in range(num_to_remove):
        index = np.random.randint(0, len(labels))
        if labels[index] == 0:
            labels = np.delete(labels, index)
            images = np.delete(images, index)

    return images, labels


def preprocess(image, label=0):
    image = tf.image.crop_to_bounding_box(image, offset_height=240, offset_width=0,
                                          target_height=240, target_width=640)
    image = tf.image.resize(image, (200, 66))

    return image, label
