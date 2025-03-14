import numpy as np
import tensorflow as tf

# Load preprocessed data
X_val = np.load('X_val.npy')
y_val = np.load('y_val.npy')

# Load the trained model
model = tf.keras.models.load_model('rain_removal_model.h5')

# Evaluate the model on validation data
val_loss, val_acc = model.evaluate(X_val, y_val)

print(f'Validation Loss: {val_loss}')
print(f'Validation Accuracy: {val_acc}')
