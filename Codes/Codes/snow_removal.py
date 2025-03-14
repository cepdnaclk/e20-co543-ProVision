import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

# Load snowy and clean images
def load_images(image_dir, target_size=(256, 256)):
    images = []
    for filename in os.listdir(image_dir):
        img = cv2.imread(os.path.join(image_dir, filename))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, target_size)
        images.append(img)
    return np.array(images) / 255.0

snowy_images = load_images('path_to_snowy_images')
clean_images = load_images('path_to_clean_images')

# Build U-Net model (same as rain removal)
def build_unet(input_shape):
    inputs = tf.keras.Input(shape=input_shape)
    # Encoder
    conv1 = layers.Conv2D(64, 3, activation='relu', padding='same')(inputs)
    conv1 = layers.Conv2D(64, 3, activation='relu', padding='same')(conv1)
    pool1 = layers.MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = layers.Conv2D(128, 3, activation='relu', padding='same')(pool1)
    conv2 = layers.Conv2D(128, 3, activation='relu', padding='same')(conv2)
    pool2 = layers.MaxPooling2D(pool_size=(2, 2))(conv2)
    # Bottleneck
    conv3 = layers.Conv2D(256, 3, activation='relu', padding='same')(pool2)
    conv3 = layers.Conv2D(256, 3, activation='relu', padding='same')(conv3)
    # Decoder
    up1 = layers.UpSampling2D(size=(2, 2))(conv3)
    concat1 = layers.concatenate([conv2, up1], axis=-1)
    conv4 = layers.Conv2D(128, 3, activation='relu', padding='same')(concat1)
    conv4 = layers.Conv2D(128, 3, activation='relu', padding='same')(conv4)
    up2 = layers.UpSampling2D(size=(2, 2))(conv4)
    concat2 = layers.concatenate([conv1, up2], axis=-1)
    conv5 = layers.Conv2D(64, 3, activation='relu', padding='same')(concat2)
    conv5 = layers.Conv2D(64, 3, activation='relu', padding='same')(conv5)
    # Output
    outputs = layers.Conv2D(3, 3, activation='sigmoid', padding='same')(conv5)
    model = models.Model(inputs, outputs)
    return model

# Build and compile the model
input_shape = (256, 256, 3)
snow_model = build_unet(input_shape)
snow_model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
split = int(0.9 * len(snowy_images))
train_snowy, val_snowy = snowy_images[:split], snowy_images[split:]
train_clean, val_clean = clean_images[:split], clean_images[split:]
history = snow_model.fit(train_snowy, train_clean, epochs=50, batch_size=8, validation_data=(val_snowy, val_clean))

# Save the model
snow_model.save('snow_removal_model.h5')

# Predict and display results
predicted_images = snow_model.predict(val_snowy)
def display_images(snowy, clean, predicted, num_images=3):
    plt.figure(figsize=(15, 5))
    for i in range(num_images):
        plt.subplot(3, num_images, i+1)
        plt.imshow(snowy[i])
        plt.title('Snowy Image')
        plt.axis('off')
        plt.subplot(3, num_images, i+1 + num_images)
        plt.imshow(clean[i])
        plt.title('Clean Image')
        plt.axis('off')
        plt.subplot(3, num_images, i+1 + 2*num_images)
        plt.imshow(predicted[i])
        plt.title('Predicted Image')
        plt.axis('off')
    plt.show()
display_images(val_snowy, val_clean, predicted_images)