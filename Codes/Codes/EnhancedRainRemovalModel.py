# import tensorflow as tf
# from tensorflow.keras import layers, models
# import numpy as np
# import matplotlib.pyplot as plt
# import cv2
# import os
# import time
# from tensorflow.keras.models import load_model
# from skimage.metrics import peak_signal_noise_ratio as psnr
# from skimage.metrics import structural_similarity as ssim
# from sklearn.metrics import r2_score
#
# # Check and configure GPU
# physical_devices = tf.config.list_physical_devices('GPU')
# if physical_devices:
#     try:
#         tf.config.experimental.set_memory_growth(physical_devices[0], True)
#         print("GPU configured successfully:", physical_devices[0])
#     except:
#         print("Failed to configure GPU")
# else:
#     print("No GPU found, running on CPU")
#
# # Enable mixed precision for faster training on GPU
# tf.keras.mixed_precision.set_global_policy('mixed_float16')
#
# # Function to load high-resolution images
# def load_images(image_dir, target_size=(512, 512)):
#     images = []
#     filenames = sorted(os.listdir(image_dir))  # Ensure consistent order
#     for filename in filenames:
#         img_path = os.path.join(image_dir, filename)
#         img = cv2.imread(img_path)
#         if img is None:
#             continue
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         img = cv2.resize(img, target_size)
#         images.append(img)
#     return np.array(images, dtype=np.float32) / 255.0, filenames
#
# # SSIM + MSE Hybrid Loss
# def perceptual_loss(y_true, y_pred):
#     ssim_loss = 1 - tf.reduce_mean(tf.image.ssim(y_true, y_pred, max_val=1.0))
#     mse_loss = tf.reduce_mean(tf.keras.losses.MSE(y_true, y_pred))
#     return 0.8 * ssim_loss + 0.2 * mse_loss
#
# # U-Net Model with Attention Mechanism
# def build_unet(input_shape=(512, 512, 3)):
#     inputs = tf.keras.Input(input_shape)
#
#     def conv_block(x, filters):
#         x = layers.Conv2D(filters, (3, 3), padding='same')(x)
#         x = layers.BatchNormalization()(x)
#         x = layers.Activation('relu')(x)
#         x = layers.Conv2D(filters, (3, 3), padding='same')(x)
#         x = layers.BatchNormalization()(x)
#         x = layers.Activation('relu')(x)
#         return x
#
#     def attention_block(x, g, filters):
#         x1 = layers.Conv2D(filters, (1, 1), padding='same')(x)
#         g1 = layers.Conv2D(filters, (1, 1), padding='same')(g)
#         attn = layers.Add()([x1, g1])
#         attn = layers.Activation('relu')(attn)
#         attn = layers.Conv2D(1, (1, 1), padding='same', activation='sigmoid')(attn)
#         return layers.Multiply()([x, attn])
#
#     # Encoder
#     c1 = conv_block(inputs, 64)
#     p1 = layers.MaxPooling2D((2, 2))(c1)
#
#     c2 = conv_block(p1, 128)
#     p2 = layers.MaxPooling2D((2, 2))(c2)
#
#     c3 = conv_block(p2, 256)
#     p3 = layers.MaxPooling2D((2, 2))(c3)
#
#     c4 = conv_block(p3, 512)
#     p4 = layers.MaxPooling2D((2, 2))(c4)
#
#     # Bottleneck
#     c5 = conv_block(p4, 1024)
#
#     # Decoder with Attention
#     u6 = layers.UpSampling2D((2, 2))(c5)
#     a6 = attention_block(c4, u6, 512)
#     m6 = layers.Concatenate()([u6, a6])
#     c6 = conv_block(m6, 512)
#
#     u7 = layers.UpSampling2D((2, 2))(c6)
#     a7 = attention_block(c3, u7, 256)
#     m7 = layers.Concatenate()([u7, a7])
#     c7 = conv_block(m7, 256)
#
#     u8 = layers.UpSampling2D((2, 2))(c7)
#     a8 = attention_block(c2, u8, 128)
#     m8 = layers.Concatenate()([u8, a8])
#     c8 = conv_block(m8, 128)
#
#     u9 = layers.UpSampling2D((2, 2))(c8)
#     a9 = attention_block(c1, u9, 64)
#     m9 = layers.Concatenate()([u9, a9])
#     c9 = conv_block(m9, 64)
#
#     outputs = layers.Conv2D(3, (1, 1), activation='sigmoid', dtype='float32')(c9)
#
#     return models.Model(inputs, outputs)
#
# # Load data
# train_images, _ = load_images('data')  # Rainy images
# train_labels, _ = load_images('gt')    # Ground truth clean images
#
# # Model Compilation
# model = build_unet()
# model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
#               loss=perceptual_loss,
#               metrics=['mae', 'mse'])  # Added MSE as a metric
#
# # Split data into training and validation sets
# split = int(0.9 * len(train_images))
# train_rainy, val_rainy = train_images[:split], train_images[split:]
# train_clean, val_clean = train_labels[:split], train_labels[split:]
#
# # Train Faster with tf.data Pipelines
# def data_generator(images, labels, batch_size=8):
#     dataset = tf.data.Dataset.from_tensor_slices((images, labels))
#     dataset = dataset.shuffle(1000).batch(batch_size).prefetch(tf.data.experimental.AUTOTUNE)
#     return dataset
#
# train_dataset = data_generator(train_rainy, train_clean)
# val_dataset = data_generator(val_rainy, val_clean)
#
# # Train Model with GPU and Reduced Epochs
# start_time = time.time()
# history = model.fit(train_dataset, epochs=10, validation_data=val_dataset, verbose=1)
# end_time = time.time()
# print(f'Training Time: {end_time - start_time:.2f} seconds')
#
# # Predict on validation set
# predicted_images = model.predict(val_rainy)
#
# # Evaluation Metrics
# def evaluate_predictions(y_true, y_pred):
#     y_true_flat = y_true.reshape(-1, y_true.shape[-1])  # Flatten for R-squared
#     y_pred_flat = y_pred.reshape(-1, y_pred.shape[-1])
#
#     # MSE and MAE
#     mse = tf.keras.metrics.mean_squared_error(y_true_flat, y_pred_flat).numpy()
#     mae = tf.keras.metrics.mean_absolute_error(y_true_flat, y_pred_flat).numpy()
#
#     # R-squared
#     r2 = r2_score(y_true_flat, y_pred_flat)
#
#     # PSNR
#     psnr_values = [psnr(y_true[i] * 255, y_pred[i] * 255, data_range=255) for i in range(len(y_true))]
#     psnr_mean = np.mean(psnr_values)
#
#     # SSIM
#     ssim_values = [ssim(y_true[i] * 255, y_pred[i] * 255, data_range=255, channel_axis=2, win_size=7)
#                    for i in range(len(y_true))]
#     ssim_mean = np.mean(ssim_values)
#
#     # Contrast Improvement
#     contrast_improvements = []
#     for i in range(len(y_true)):
#         orig_gray = cv2.cvtColor(y_true[i] * 255, cv2.COLOR_RGB2GRAY)
#         pred_gray = cv2.cvtColor(y_pred[i] * 255, cv2.COLOR_RGB2GRAY)
#         orig_std = np.std(orig_gray)
#         pred_std = np.std(pred_gray)
#         contrast_improvement = (pred_std - orig_std) / orig_std * 100 if orig_std != 0 else 0
#         contrast_improvements.append(contrast_improvement)
#     contrast_mean = np.mean(contrast_improvements)
#
#     return {
#         'MSE': mse,
#         'MAE': mae,
#         'R-squared': r2,
#         'PSNR': psnr_mean,
#         'SSIM': ssim_mean,
#         'Contrast_Improvement': contrast_mean
#     }
#
# # Compute and display evaluation metrics
# metrics = evaluate_predictions(val_clean, predicted_images)
# print("\nEvaluation Metrics on Validation Set:")
# for metric, value in metrics.items():
#     print(f"{metric}: {value:.4f}")
#
# # Display results
# def display_images(original, ground_truth, predicted):
#     plt.figure(figsize=(15, 10))
#     for i in range(min(3, len(original))):
#         plt.subplot(3, 3, 3 * i + 1)
#         plt.imshow(original[i])
#         plt.title("Rainy Image")
#         plt.axis('off')
#
#         plt.subplot(3, 3, 3 * i + 2)
#         plt.imshow(ground_truth[i])
#         plt.title("Ground Truth")
#         plt.axis('off')
#
#         plt.subplot(3, 3, 3 * i + 3)
#         plt.imshow(predicted[i])
#         plt.title("Predicted")
#         plt.axis('off')
#     plt.tight_layout()
#     plt.show()
#
# display_images(val_rainy, val_clean, predicted_images)
#
# # Save Model
# model.save('rain_removal_model_enhanced.h5')


import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import time
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import r2_score

# Configure GPU
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    print("GPU configured:", physical_devices[0])
else:
    print("No GPU found, running on CPU")

# Enable mixed precision
tf.keras.mixed_precision.set_global_policy('mixed_float16')

# Load images
def load_images(image_dir, target_size=(512, 512)):
    images = []
    filenames = sorted(os.listdir(image_dir))
    for filename in filenames:
        img_path = os.path.join(image_dir, filename)
        img = cv2.imread(img_path)
        if img is None:
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, target_size)
        images.append(img)
    return np.array(images, dtype=np.float32) / 255.0, filenames

# Enhanced Loss Function: SSIM + MSE + Contrast
def perceptual_loss(y_true, y_pred):
    ssim_loss = 1 - tf.reduce_mean(tf.image.ssim(y_true, y_pred, max_val=1.0))
    mse_loss = tf.reduce_mean(tf.keras.losses.MSE(y_true, y_pred))
    y_true_gray = tf.image.rgb_to_grayscale(y_true)
    y_pred_gray = tf.image.rgb_to_grayscale(y_pred)
    contrast_loss = tf.reduce_mean(tf.abs(tf.image.sobel_edges(y_true_gray) - tf.image.sobel_edges(y_pred_gray)))
    return 0.6 * ssim_loss + 0.3 * mse_loss + 0.1 * contrast_loss

# Enhanced U-Net Model with Attention and Residual Connections
def build_unet(input_shape=(512, 512, 3)):
    inputs = tf.keras.Input(input_shape)

    def conv_block(x, filters, dilation_rate=1):
        x_skip = x  # For residual connection
        x = layers.Conv2D(filters, (3, 3), padding='same', dilation_rate=dilation_rate)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Conv2D(filters, (3, 3), padding='same', dilation_rate=dilation_rate)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        if x_skip.shape[-1] == filters:
            x = layers.Add()([x, x_skip])  # Residual connection
        return x

    def attention_block(x, g, filters):
        x1 = layers.Conv2D(filters, (1, 1), padding='same')(x)
        g1 = layers.Conv2D(filters, (1, 1), padding='same')(g)
        attn = layers.Add()([x1, g1])
        attn = layers.Activation('relu')(attn)
        attn = layers.Conv2D(1, (1, 1), padding='same')(attn)
        attn = layers.Activation('sigmoid')(attn)
        return layers.Multiply()([x, attn])

    # Encoder
    c1 = conv_block(inputs, 96)  # Increased filters
    p1 = layers.MaxPooling2D((2, 2))(c1)

    c2 = conv_block(p1, 192)
    p2 = layers.MaxPooling2D((2, 2))(c2)

    c3 = conv_block(p2, 384)
    p3 = layers.MaxPooling2D((2, 2))(c3)

    c4 = conv_block(p3, 768)
    p4 = layers.MaxPooling2D((2, 2))(c4)

    # Bottleneck with Dilated Convolution
    c5 = conv_block(p4, 1536, dilation_rate=2)

    # Decoder with Attention
    u6 = layers.UpSampling2D((2, 2))(c5)
    a6 = attention_block(c4, u6, 768)
    m6 = layers.Concatenate()([u6, a6])
    c6 = conv_block(m6, 768)

    u7 = layers.UpSampling2D((2, 2))(c6)
    a7 = attention_block(c3, u7, 384)
    m7 = layers.Concatenate()([u7, a7])
    c7 = conv_block(m7, 384)

    u8 = layers.UpSampling2D((2, 2))(c7)
    a8 = attention_block(c2, u8, 192)
    m8 = layers.Concatenate()([u8, a8])
    c8 = conv_block(m8, 192)

    u9 = layers.UpSampling2D((2, 2))(c8)
    a9 = attention_block(c1, u9, 96)
    m9 = layers.Concatenate()([u9, a9])
    c9 = conv_block(m9, 96)

    outputs = layers.Conv2D(3, (1, 1), activation='sigmoid', dtype='float32')(c9)
    return models.Model(inputs, outputs)

# Load data
train_images, _ = load_images('data')
train_labels, _ = load_images('gt')
assert len(train_images) == len(train_labels), "Mismatch between rainy and ground truth images"

# Split data
split = int(0.9 * len(train_images))
train_rainy, val_rainy = train_images[:split], train_images[split:]
train_clean, val_clean = train_labels[:split], train_labels[split:]

# Data Pipeline
def data_generator(images, labels, batch_size=8):
    dataset = tf.data.Dataset.from_tensor_slices((images, labels))
    dataset = dataset.shuffle(1000).batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return dataset

train_dataset = data_generator(train_rainy, train_clean)
val_dataset = data_generator(val_rainy, val_clean)

# Build and compile model
model = build_unet()
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0002),  # Slightly increased LR
              loss=perceptual_loss,
              metrics=['mae', 'mse', tf.keras.metrics.MeanIoU(num_classes=2)])

# Train model
start_time = time.time()
history = model.fit(train_dataset, epochs=50, validation_data=val_dataset, verbose=1)
end_time = time.time()
print(f'Training Time: {end_time - start_time:.2f} seconds')

# Predict
predicted_images = model.predict(val_rainy)

# Evaluation Metrics
def evaluate_predictions(y_true, y_pred):
    y_true_flat = y_true.reshape(-1, y_true.shape[-1])
    y_pred_flat = y_pred.reshape(-1, y_pred.shape[-1])

    mse = tf.keras.metrics.mean_squared_error(y_true_flat, y_pred_flat).numpy()
    mae = tf.keras.metrics.mean_absolute_error(y_true_flat, y_pred_flat).numpy()
    r2 = r2_score(y_true_flat, y_pred_flat)
    psnr_values = [psnr(y_true[i] * 255, y_pred[i] * 255, data_range=255) for i in range(len(y_true))]
    psnr_mean = np.mean(psnr_values)
    ssim_values = [ssim(y_true[i] * 255, y_pred[i] * 255, data_range=255, channel_axis=2, win_size=7)
                   for i in range(len(y_true))]
    ssim_mean = np.mean(ssim_values)
    contrast_improvements = []
    for i in range(len(y_true)):
        orig_gray = cv2.cvtColor(y_true[i] * 255, cv2.COLOR_RGB2GRAY)
        pred_gray = cv2.cvtColor(y_pred[i] * 255, cv2.COLOR_RGB2GRAY)
        orig_std = np.std(orig_gray)
        pred_std = np.std(pred_gray)
        contrast_improvement = (pred_std - orig_std) / orig_std * 100 if orig_std != 0 else 0
        contrast_improvements.append(contrast_improvement)
    contrast_mean = np.mean(contrast_improvements)

    return {
        'MSE': mse,
        'MAE': mae,
        'R-squared': r2,
        'PSNR': psnr_mean,
        'SSIM': ssim_mean,
        'Contrast_Improvement': contrast_mean
    }

metrics = evaluate_predictions(val_clean, predicted_images)

# Visualization of Metrics
def visualize_metrics(metrics):
    plt.figure(figsize=(12, 6))
    metrics_names = list(metrics.keys())
    metrics_values = list(metrics.values())
    bars = plt.bar(metrics_names, metrics_values, color=['blue', 'green', 'red', 'purple', 'orange', 'cyan'])
    plt.title('Evaluation Metrics on Validation Set', fontsize=14)
    plt.ylabel('Value', fontsize=12)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.4f}', ha='center', va='bottom')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Training History Graphs
def plot_training_history(history):
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Loss Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid()

    plt.subplot(1, 3, 2)
    plt.plot(history.history['mae'], label='Training MAE')
    plt.plot(history.history['val_mae'], label='Validation MAE')
    plt.title('MAE Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('MAE')
    plt.legend()
    plt.grid()

    plt.subplot(1, 3, 3)
    plt.plot(history.history['mse'], label='Training MSE')
    plt.plot(history.history['val_mse'], label='Validation MSE')
    plt.title('MSE Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

# Display images
def display_images(original, ground_truth, predicted):
    plt.figure(figsize=(15, 10))
    for i in range(min(3, len(original))):
        plt.subplot(3, 3, 3 * i + 1)
        plt.imshow(original[i])
        plt.title("Rainy Image")
        plt.axis('off')

        plt.subplot(3, 3, 3 * i + 2)
        plt.imshow(ground_truth[i])
        plt.title("Ground Truth")
        plt.axis('off')

        plt.subplot(3, 3, 3 * i + 3)
        plt.imshow(predicted[i])
        plt.title("Predicted")
        plt.axis('off')
    plt.tight_layout()
    plt.show()

# Execute visualizations
print("\nEvaluation Metrics on Validation Set:")
for metric, value in metrics.items():
    print(f"{metric}: {value:.4f}")
visualize_metrics(metrics)
plot_training_history(history)
display_images(val_rainy, val_clean, predicted_images)

# Save model
model.save('rain_removal_model_enhanced_plots.h5')