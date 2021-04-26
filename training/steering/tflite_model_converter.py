import tensorflow as tf
from tensorflow.keras.models import load_model

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Convert the model
converter = tf.lite.TFLiteConverter.from_keras_model(load_model(r'steering_model.h5'))
tflite_model = converter.convert()

# Save the model.
with open('steering_model.tflite', 'wb') as file:
  file.write(tflite_model)
