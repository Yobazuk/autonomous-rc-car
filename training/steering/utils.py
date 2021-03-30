import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import cv2
import tensorflow as tf
from random import randint


def read_image(path, label):
    image = tf.io.read_file(path)
    image = tf.image.decode_image(image, channels=3, dtype=tf.float32)
    return image, label


def augment_image(image, label):
    # do augmentation
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
