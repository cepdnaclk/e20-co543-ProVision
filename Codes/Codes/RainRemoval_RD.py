from Rain_Removal import display_images
from required_modules import *
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from tensorflow.keras.models import load_model

# Load rainy and clean images
rainy_images = load_images('data')
clean_images = load_images('gt')

# Build RIDNet model
def build_ridnet(input_shape):
    inputs = tf.keras.Input(shape=input_shape)

    # Initial Convolution
    x = layers.Conv2D(64, 3, activation='relu', padding='same')(inputs)

    # Residual Dense Blocks (RDBs)
    def rdb_block(x, filters=64):
        r = layers.Conv2D(filters, 3, activation='relu', padding='same')(x)
        r = layers.Conv2D(filters, 3, activation='relu', padding='same')(r)
        r = layers.Conv2D(filters, 3, activation='relu', padding='same')(r)
        return layers.Add()([x, r])  # Residual Connection

    x = rdb_block(x)
    x = rdb_block(x)
    x = rdb_block(x)

    # Bottleneck layer
    x = layers.Conv2D(64, 3, activation='relu', padding='same')(x)

    # Reconstruction layer
    outputs = layers.Conv2D(3, 3, activation='sigmoid', padding='same')(x)

    model = models.Model(inputs, outputs)
    return model

# Build the model
input_shape = (256, 256, 3)
model = build_ridnet(input_shape)
model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()

# Split the data into training and validation sets
split = int(0.9 * len(rainy_images))
train_rainy, val_rainy = rainy_images[:split], rainy_images[split:]
train_clean, val_clean = clean_images[:split], clean_images[split:]

# Train the model
history = model.fit(train_rainy, train_clean, epochs=50, batch_size=8, validation_data=(val_rainy, val_clean))

# Predict on validation set
predicted_images = model.predict(val_rainy)

display_images(val_rainy, val_clean, predicted_images)

model.save('rain_removal_model_RD.h5')
