# Haze remover

import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim


class ImageDehazer:
    def __init__(self, window_size=25, airlight_percentile=0.02, transmission_bound=0.9, gamma=1.0):
        self.window_size = window_size  # Reduced back for balance
        self.airlight_percentile = airlight_percentile  # Slightly increased for better airlight
        self.transmission_bound = transmission_bound  # Adjusted for detail retention
        self.gamma = gamma  # Set to 1.0 to minimize over-brightening

    def preprocess_image(self, image):
        """Preprocess the input image"""
        # Maintain aspect ratio while resizing
        h, w = image.shape[:2]
        scale = min(self.target_size[0] / w, self.target_size[1] / h)
        new_size = (int(w * scale), int(h * scale))
        resized = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

        # Pad to target size if necessary
        padded = np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.uint8)
        y_off = (self.target_size[1] - new_size[1]) // 2
        x_off = (self.target_size[0] - new_size[0]) // 2
        padded[y_off:y_off + new_size[1], x_off:x_off + new_size[0]] = resized

        # Noise reduction
        denoised = cv2.bilateralFilter(padded, 9, 75, 75)

        # Normalization
        normalized = cv2.normalize(denoised, None, 0, 255, cv2.NORM_MINMAX)
        return normalized

    def calculate_dark_channel(self, image):
        dark_channel = np.min(image, axis=2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.window_size, self.window_size))
        dark_channel = cv2.erode(dark_channel, kernel)
        return dark_channel

    def estimate_airlight(self, image, dark_channel):
        num_pixels = image.shape[0] * image.shape[1]
        flat_image = image.reshape(num_pixels, 3)
        flat_dark = dark_channel.ravel()
        num_brightest = int(num_pixels * self.airlight_percentile)
        indices = np.argsort(flat_dark)[-num_brightest:]
        airlight = np.mean(flat_image[indices], axis=0)
        return airlight

    def guided_filter(self, I, p, r, epsilon):
        mean_I = cv2.boxFilter(I, -1, (r, r))
        mean_p = cv2.boxFilter(p, -1, (r, r))
        mean_Ip = cv2.boxFilter(I * p, -1, (r, r))
        cov_Ip = mean_Ip - mean_I * mean_p
        mean_II = cv2.boxFilter(I * I, -1, (r, r))
        var_I = mean_II - mean_I * mean_I
        a = cov_Ip / (var_I + epsilon)
        b = mean_p - a * mean_I
        mean_a = cv2.boxFilter(a, -1, (r, r))
        mean_b = cv2.boxFilter(b, -1, (r, r))
        q = mean_a * I + mean_b
        return q

    def estimate_transmission_with_guided_filter(self, image, airlight, window_size=15):
        normalized = image / (airlight + 1e-6)
        dark_channel = np.min(normalized, axis=2)
        transmission = 1 - 0.9 * dark_channel  # Adjusted to balance haze removal and detail
        gray_guide = cv2.cvtColor(normalized.astype(np.float32), cv2.COLOR_RGB2GRAY)
        refined_transmission = self.guided_filter(gray_guide, transmission, window_size,
                                                  0.01)  # Increased epsilon for smoothness
        refined_transmission = np.clip(refined_transmission, 0.1, self.transmission_bound)
        return refined_transmission

    def recover_image(self, hazy_image, transmission, airlight):
        transmission = np.expand_dims(transmission, axis=2)
        transmission = np.repeat(transmission, 3, axis=2)
        airlight = airlight.reshape(1, 1, 3)
        recovered = ((hazy_image.astype(float) - airlight) / np.maximum(transmission, 0.1)) + airlight
        recovered = np.clip(recovered, 0, 255).astype(np.uint8)
        return recovered

    def apply_gamma_correction(self, image):
        invGamma = 1.0 / self.gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    def enhance_contrast(self, image):
        # Denoise slightly to reduce noise amplification
        denoised = cv2.fastNlMeansDenoisingColored(image, None, 5, 5, 7, 21)

        # Contrast enhancement with moderated CLAHE
        lab = cv2.cvtColor(denoised, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))  # Reduced clipLimit for balance
        l_enhanced = clahe.apply(l)
        lab_enhanced = cv2.merge((l_enhanced, a, b))
        enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2RGB)

        # Controlled sharpening
        blurred = cv2.GaussianBlur(enhanced, (0, 0), 1.5)
        sharpened = cv2.addWeighted(enhanced, 1.3, blurred, -0.3, 0)  # Softer sharpening
        return sharpened

    def evaluate_result(self, original, dehazed):
        orig_float = original.astype(float)
        dehazed_float = dehazed.astype(float)

        psnr_value = psnr(orig_float, dehazed_float, data_range=255)
        ssim_value = ssim(orig_float, dehazed_float,
                          win_size=7,
                          data_range=255,
                          channel_axis=2,
                          gaussian_weights=True)

        orig_gray = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        dehazed_gray = cv2.cvtColor(dehazed, cv2.COLOR_RGB2GRAY)
        orig_contrast = np.std(orig_gray)
        dehazed_contrast = np.std(dehazed_gray)

        return {
            'PSNR': psnr_value,
            'SSIM': ssim_value,
            'Contrast_Improvement': (dehazed_contrast - orig_contrast) / orig_contrast * 100
        }

    def dehaze(self, image):
        if image is None:
            raise ValueError("Could not load image")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        dark_channel = self.calculate_dark_channel(image)
        airlight = self.estimate_airlight(image, dark_channel)
        transmission = self.estimate_transmission_with_guided_filter(image, airlight)
        dehazed = self.recover_image(image, transmission, airlight)

        enhanced = self.enhance_contrast(dehazed)
        final_result = self.apply_gamma_correction(enhanced)

        final_image = cv2.cvtColor(final_result, cv2.COLOR_BGR2RGB)

        return final_image
