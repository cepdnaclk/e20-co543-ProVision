import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Load the trained model
model = tf.keras.models.load_model('rain_removal_model.h5')

def display_images(input_img, output_img):
    # Convert images from range [0,1] to [0,255] for visualization
    input_img = (input_img * 255).astype(np.uint8)
    output_img = (output_img * 255).astype(np.uint8)

    # Display original and output images side by side
    plt.figure(figsize=(10, 5))

    # Plot input image
    plt.subplot(1, 2, 1)
    plt.imshow(input_img)
    plt.title('Input Image')
    plt.axis('off')

    # Plot output image
    plt.subplot(1, 2, 2)
    plt.imshow(output_img)
    plt.title('Denoised Image')
    plt.axis('off')

    plt.show()

def remove_rain(input_img_path, img_size=(256, 256)):
    input_img = cv2.imread(input_img_path)
    input_img = cv2.resize(input_img, img_size) / 255.0
    input_img = np.expand_dims(input_img, axis=0)  # Add batch dimension

    predicted_img = model.predict(input_img)

    # Display the results
    display_images(input_img[0], predicted_img[0])

# Test the model with a new image
remove_rain('/path/to/new/input/image.jpg')
