import torch
import torch.nn as nn
import torch.nn.functional as F
from Deraining.MPRNet import DownSample, SkipUpSample, ORSNet, MPRNet
import cv2
import numpy as np
import matplotlib.pyplot as plt

# [Previous class definitions remain unchanged: conv, CALayer, CAB, Encoder, Decoder, SAM, MPRNet]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def preprocess_image(input_img_path, img_size=(512, 384), device=device):
    print("Reading image from:", input_img_path)

    # Attempt to load the image
    input_img = cv2.imread(input_img_path)
    if input_img is None:
        raise ValueError(f"Image not found or unable to open at path: {input_img_path}")

    # Convert BGR to RGB
    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

    # Resize image
    input_img = cv2.resize(input_img, img_size)

    # Normalize the image
    input_img = input_img.astype(np.float32) / 255.0
    input_img = np.transpose(input_img, (2, 0, 1))  # Change to (C, H, W)

    # Debug: Print type and shape
    print(f"Input type: {type(input_img)}, Shape: {input_img.shape}")

    # Alternative approaches to convert to tensor
    try:
        # Method 1: Direct torch.from_numpy
        input_tensor = torch.from_numpy(input_img)
    except TypeError as e:
        print(f"torch.from_numpy failed: {e}")
        # Method 2: Convert via numpy array explicitly
        input_tensor = torch.tensor(np.array(input_img, dtype=np.float32))

    # Add batch dimension and move to device
    input_tensor = input_tensor.unsqueeze(0)
    return input_tensor.to(device)


def display_images(input_img, output_img):
    input_img = input_img.squeeze(0).cpu().numpy().transpose(1, 2, 0)
    output_img = output_img.squeeze(0).cpu().numpy().transpose(1, 2, 0)

    input_img = (np.clip(input_img, 0, 1) * 255).astype(np.uint8)
    output_img = (np.clip(output_img, 0, 1) * 255).astype(np.uint8)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(input_img)
    plt.title('Input Image')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(output_img)
    plt.title('Output Image')
    plt.axis('off')
    plt.show()


def remove_rain(input_img_path, model, device):
    try:
        input_img = preprocess_image(input_img_path, device=device)
    except ValueError as e:
        print(e)
        return

    with torch.no_grad():
        output_img = model(input_img)[0]

    display_images(input_img, output_img)


def main():
    model = MPRNet(
        in_c=3,
        out_c=3,
        n_feat=40,
        scale_unetfeats=20,
        scale_orsnetfeats=16,
        num_cab=8,
        kernel_size=3,
        reduction=4,
        bias=False
    )

    try:
        checkpoint = torch.load('model_deraining.pth', map_location=device)
        if 'state_dict' in checkpoint:
            model.load_state_dict(checkpoint['state_dict'])
        else:
            model.load_state_dict(checkpoint)
    except FileNotFoundError:
        print("Error: Model checkpoint 'model_deraining.pth' not found")
        return
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    model.to(device)
    model.eval()
    for i in ['input/input/13.jpg','input/input/38.jpg','input/input/565.jpg','input/input/13704.jpg','input/input/13641.jpg']:
        input_img_path = i
        remove_rain(input_img_path, model, device)


if __name__ == "__main__":
    main()