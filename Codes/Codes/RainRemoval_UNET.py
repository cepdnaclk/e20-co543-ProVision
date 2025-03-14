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

# Build the model
input_shape = (256, 256, 3)
model = build_unet(input_shape)
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

model.save('rain_removal_model.h5')
