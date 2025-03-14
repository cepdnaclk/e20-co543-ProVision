import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os


# Function to load images
def load_images(image_dir, target_size=(256, 256)):
    images = []
    filenames = sorted(os.listdir(image_dir))  # Ensure consistent order
    for filename in filenames:
        img_path = os.path.join(image_dir, filename)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, target_size)
        images.append(img)
    return np.array(images) / 255.0, filenames  # Return filenames for reference


# Post-processing: Bilateral filtering and sharpening
def enhance_output(image):
    image = (image * 255).astype(np.uint8)  # Convert to 8-bit format

    # Apply bilateral filter (smooths rain artifacts)
    filtered = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

    # Apply sharpening kernel
    sharpening_kernel = np.array([[0, -1, 0],
                                  [-1, 5, -1],
                                  [0, -1, 0]])
    sharpened = cv2.filter2D(filtered, -1, sharpening_kernel)

    return sharpened


# Load trained model
model = load_model('rain_removal_model_RD.h5')

for i in ['Test_images','Test_images1','Test_images2']:
    # Load test images
    test_images, filenames = load_images(i)

    # Predict output
    predicted_images = model.predict(test_images)

    # Display original and enhanced output
    num_images = min(3, len(test_images))  # Display up to 3 images
    plt.figure(figsize=(10, num_images * 5))

    for i in range(num_images):
        enhanced_output = enhance_output(predicted_images[i])

        # Original Image
        plt.subplot(num_images, 2, 2 * i + 1)
        plt.imshow(test_images[i])
        plt.title(f'Original: {filenames[i]}')
        plt.axis('off')

        # Enhanced Output Image
        plt.subplot(num_images, 2, 2 * i + 2)
        plt.imshow(enhanced_output)
        plt.title('Enhanced Output')
        plt.axis('off')

    plt.tight_layout()
    plt.show()
