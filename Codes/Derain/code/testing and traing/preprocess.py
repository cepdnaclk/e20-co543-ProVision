import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

# Path to input and target images
input_dir = '/path/to/input/images'
target_dir = '/path/to/target/images'

def load_images(input_dir, target_dir, img_size=(256, 256)):
    input_images = []
    target_images = []

    for filename in os.listdir(input_dir):
        # Read the input and target images
        input_img = cv2.imread(os.path.join(input_dir, filename))
        target_img = cv2.imread(os.path.join(target_dir, filename))

        if input_img is not None and target_img is not None:
            # Resize the images
            input_img = cv2.resize(input_img, img_size)
            target_img = cv2.resize(target_img, img_size)

            # Normalize the images
            input_images.append(input_img / 255.0)
            target_images.append(target_img / 255.0)

    # Convert to numpy arrays
    input_images = np.array(input_images)
    target_images = np.array(target_images)

    return input_images, target_images

# Load the images
input_images, target_images = load_images(input_dir, target_dir)

# Split into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(input_images, target_images, test_size=0.2, random_state=42)

# Save the preprocessed data as a numpy file for later use
np.save('X_train.npy', X_train)
np.save('X_val.npy', X_val)
np.save('y_train.npy', y_train)
np.save('y_val.npy', y_val)
