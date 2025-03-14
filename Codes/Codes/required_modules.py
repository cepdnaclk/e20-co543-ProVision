import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os


# Function to load all images from a folder
def load_images(image_dir, target_size=(256, 256)):
    images = []
    filenames = []

    for filename in os.listdir(image_dir):
        img_path = os.path.join(image_dir, filename)
        img = cv2.imread(img_path)
        if img is None:
            continue  # Skip unreadable files

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, target_size)
        images.append(img)
        filenames.append(filename)

    return np.array(images) / 255.0, filenames


# Function to build a simple UNet model
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


# Function to display and save outputs
def process_and_display_images(model, input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    rainy_images, filenames = load_images(input_folder)

    for i, img in enumerate(rainy_images):
        img_input = np.expand_dims(img, axis=0)  # Add batch dimension
        predicted_img = model.predict(img_input)[0]  # Get first image from batch
        predicted_img = (predicted_img * 255).astype(np.uint8)  # Convert back to 0-255

        # Save output image
        output_path = os.path.join(output_folder, filenames[i])
        cv2.imwrite(output_path, cv2.cvtColor(predicted_img, cv2.COLOR_RGB2BGR))

        # Display results
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(img)
        plt.title('Rainy Image')
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.imshow(predicted_img)
        plt.title('Predicted Clean Image')
        plt.axis('off')

        plt.show()


# Load trained model or train a new one
input_shape = (256, 256, 3)
model = build_unet(input_shape)
model.compile(optimizer='adam', loss='mean_squared_error')

# Load and process all images from 'data' folder
process_and_display_images(model, 'data', 'output')
