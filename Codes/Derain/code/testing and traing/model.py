import tensorflow as tf
from tensorflow.keras import layers, models

def build_model(input_shape):
    model = models.Sequential()

    # U-Net like architecture
    model.add(layers.InputLayer(input_shape=input_shape))

    # Encoder (Downsampling)
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2)))

    # Bottleneck (Latent Space)
    model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))

    # Decoder (Upsampling)
    model.add(layers.Conv2DTranspose(128, (3, 3), strides=2, activation='relu', padding='same'))
    model.add(layers.Conv2DTranspose(64, (3, 3), strides=2, activation='relu', padding='same'))

    # Output layer (Restoring to original size)
    model.add(layers.Conv2D(3, (3, 3), activation='sigmoid', padding='same'))

    return model

# Load preprocessed data
import numpy as np
X_train = np.load('X_train.npy')
X_val = np.load('X_val.npy')
y_train = np.load('y_train.npy')
y_val = np.load('y_val.npy')

# Build the model
model = build_model(X_train.shape[1:])
model.summary()

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50, batch_size=16)

# Save the trained model
model.save('rain_removal_model_1.h5')
