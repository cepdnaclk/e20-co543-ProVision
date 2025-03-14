# import torch
#
# model_path = "model.pth"
# checkpoint = torch.load(model_path, map_location="cpu")
# print(checkpoint.keys())  # To check what keys exist in the checkpoint


import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print(tf.config.list_physical_devices('GPU'))
