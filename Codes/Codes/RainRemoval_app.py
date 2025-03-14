# import tensorflow as tf
# from tensorflow.keras.models import load_model
# import numpy as np
# import matplotlib.pyplot as plt
# import cv2
# import os
#
#
# # Function to load images
# def load_images(image_dir, target_size=(256, 256)):
#     images = []
#     filenames = sorted(os.listdir(image_dir))  # Ensure consistent order
#     for filename in filenames:
#         img_path = os.path.join(image_dir, filename)
#         img = cv2.imread(img_path)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         img = cv2.resize(img, target_size)
#         images.append(img)
#     return np.array(images) / 255.0, filenames  # Return filenames for reference
#
#
# # Post-processing: Bilateral filtering and sharpening
# def enhance_output(image):
#     image = (image * 255).astype(np.uint8)  # Convert to 8-bit format
#
#     # Apply bilateral filter with reduced parameters
#     filtered = cv2.bilateralFilter(image, d=5, sigmaColor=50, sigmaSpace=50)
#
#     # Unsharp Masking
#     gaussian_blur = cv2.GaussianBlur(filtered, (0, 0), 3)
#     sharpened = cv2.addWeighted(filtered, 1.5, gaussian_blur, -0.5, 0)
#
#     # Contrast Enhancement using CLAHE
#     lab = cv2.cvtColor(sharpened, cv2.COLOR_RGB2LAB)
#     l, a, b = cv2.split(lab)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     l = clahe.apply(l)
#     lab = cv2.merge((l, a, b))
#     enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
#
#     return enhanced
#
#
#
# # Load trained model
# model = load_model('rain_removal_model.h5')
#
# # Load test images
# test_images, filenames = load_images('Test_images2')
#
#
# # Predict output
# predicted_images = model.predict(test_images)
#
# # Display original and enhanced output
# num_images = min(3, len(test_images))  # Display up to 3 images
# plt.figure(figsize=(10, num_images * 5))
#
# for i in range(num_images):
#     enhanced_output = enhance_output(predicted_images[i])
#
#     # Original Image
#     plt.subplot(num_images, 2, 2 * i + 1)
#     plt.imshow(test_images[i])
#     plt.title(f'Original: {filenames[i]}')
#     plt.axis('off')
#
#     # Enhanced Output Image
#     plt.subplot(num_images, 2, 2 * i + 2)
#     plt.imshow(enhanced_output)
#     plt.title('Enhanced Output')
#     plt.axis('off')
#
# plt.tight_layout()
# plt.show()
#
#
#
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

# Preprocessing: Noise reduction and normalization
def preprocess_image(image, target_size=(256, 256)):
    # Convert to RGB
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Resize
    img = cv2.resize(img, target_size)
    # Noise reduction with bilateral filter
    img = cv2.bilateralFilter(img, d=5, sigmaColor=50, sigmaSpace=50)
    # Normalization
    img = img.astype(np.float32) / 255.0
    return img

# Function to load images with preprocessing
def load_images(image_dir, target_size=(256, 256)):
    images = []
    filenames = sorted(os.listdir(image_dir))  # Ensure consistent order
    for filename in filenames:
        img_path = os.path.join(image_dir, filename)
        img = cv2.imread(img_path)
        if img is None:
            continue
        img = preprocess_image(img, target_size)
        images.append(img)
    return np.array(images), filenames

# Post-processing: Enhanced bilateral filtering, sharpening, and contrast adjustment
def enhance_output(image):
    image = np.clip(image * 255, 0, 255).astype(np.uint8)  # Ensure valid range

    # Bilateral filter with optimized parameters
    filtered = cv2.bilateralFilter(image, d=7, sigmaColor=75, sigmaSpace=75)

    # Sharpening with unsharp masking
    gaussian_blur = cv2.GaussianBlur(filtered, (0, 0), 2.0)
    sharpened = cv2.addWeighted(filtered, 1.8, gaussian_blur, -0.8, 0)

    # Contrast enhancement with CLAHE
    lab = cv2.cvtColor(sharpened, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))  # Increased clipLimit
    l_enhanced = clahe.apply(l)
    lab_enhanced = cv2.merge((l_enhanced, a, b))
    enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2RGB)

    # Gamma correction for brightness adjustment
    gamma = 1.2
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    enhanced = cv2.LUT(enhanced, table)

    return enhanced

# Evaluation metrics
def evaluate_image(original, enhanced):
    orig_float = original.astype(np.float32) * 255  # Undo normalization for metrics
    enhanced_float = enhanced.astype(np.float32)

    # PSNR
    psnr_value = psnr(orig_float, enhanced_float, data_range=255)

    # SSIM
    ssim_value = ssim(orig_float, enhanced_float, data_range=255, channel_axis=2, win_size=7)

    # Contrast Improvement
    orig_gray = cv2.cvtColor(orig_float, cv2.COLOR_RGB2GRAY)
    enhanced_gray = cv2.cvtColor(enhanced_float, cv2.COLOR_RGB2GRAY)
    orig_contrast = np.std(orig_gray)
    enhanced_contrast = np.std(enhanced_gray)
    contrast_improvement = (enhanced_contrast - orig_contrast) / orig_contrast * 100 if orig_contrast != 0 else 0

    return {
        'PSNR': psnr_value,
        'SSIM': ssim_value,
        'Contrast_Improvement': contrast_improvement
    }

# Load trained model
model = load_model('rain_removal_model.h5')

# Load test images with preprocessing
test_images, filenames = load_images('Test_images3')

# Predict output
predicted_images = model.predict(test_images)

# Display and evaluate original and enhanced output
num_images = min(3, len(test_images))  # Display up to 3 images
plt.figure(figsize=(12, num_images * 5))

for i in range(num_images):
    enhanced_output = enhance_output(predicted_images[i])
    metrics = evaluate_image(test_images[i], enhanced_output)

    # Original Image
    plt.subplot(num_images, 3, 3 * i + 1)
    plt.imshow(test_images[i])
    plt.title(f'Original:')
    plt.axis('off')

    # Predicted Output (before enhancement)
    plt.subplot(num_images, 3, 3 * i + 2)
    plt.imshow(predicted_images[i])
    plt.title('Predicted Output')
    plt.axis('off')



plt.tight_layout()
plt.show()