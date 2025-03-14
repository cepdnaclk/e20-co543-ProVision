import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

# Function to load high-resolution images
def load_images(image_dir, target_size=(512, 512)):
    images = []
    filenames = sorted(os.listdir(image_dir))  # Ensure consistent order
    for filename in filenames:
        img_path = os.path.join(image_dir, filename)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, target_size)
        images.append(img)
    return np.array(images, dtype=np.float32) / 255.0, filenames  # Return filenames for reference

# Post-processing: Bilateral filtering, sharpening, and contrast enhancement
def enhance_output(image):
    image = (image * 255).astype(np.uint8)  # Convert to 8-bit format

    # Apply bilateral filter with optimized parameters
    filtered = cv2.bilateralFilter(image, d=7, sigmaColor=75, sigmaSpace=75)

    # Unsharp Masking
    gaussian_blur = cv2.GaussianBlur(filtered, (0, 0), 2)
    sharpened = cv2.addWeighted(filtered, 1.7, gaussian_blur, -0.7, 0)

    # Contrast Enhancement using CLAHE
    lab = cv2.cvtColor(sharpened, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    return enhanced

# Load trained model
model = load_model('rain_removal_model_RD.h5')

# Load test images
test_images, filenames = load_images('Test_images')

# Predict output
predicted_images = model.predict(test_images, batch_size=4)

# Display original and enhanced output
num_images = min(3, len(test_images))  # Display up to 3 images
plt.figure(figsize=(12, num_images * 5))

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
