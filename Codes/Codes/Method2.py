import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# Define the DnCNN model architecture (adjust if needed)
class DnCNN(nn.Module):
    def __init__(self, channels=1, num_layers=17):
        super(DnCNN, self).__init__()
        layers = [nn.Conv2d(channels, 64, kernel_size=3, padding=1), nn.ReLU(inplace=True)]
        for _ in range(num_layers - 2):
            layers.append(nn.Conv2d(64, 64, kernel_size=3, padding=1))
            layers.append(nn.BatchNorm2d(64))
            layers.append(nn.ReLU(inplace=True))
        layers.append(nn.Conv2d(64, channels, kernel_size=3, padding=1))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return x - self.model(x)  # Residual learning for rain removal


# Load the trained model
model_path = "model.pth"  # Update path if needed
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = DnCNN(channels=3)  # Assuming the model was trained on RGB images
model.load_state_dict(torch.load(model_path, map_location=device), strict=False)

model.to(device)
model.eval()


# Function to preprocess the image
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((64, 64)),  # Resize to match training input
        transforms.ToTensor()
    ])
    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0).to(device)  # Add batch dimension


# Function to remove rain from an image
def remove_rain(image_path):
    input_image = preprocess_image(image_path)
    with torch.no_grad():
        output_image = model(input_image).clamp(0, 1)

    output_np = output_image.squeeze(0).cpu().permute(1, 2, 0).numpy()
    return output_np


# Test on an example image
input_image_path = "Test_images/3_rain.png"  # Update with your image path
output_image = remove_rain(input_image_path)

# Display results
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(Image.open(input_image_path))
plt.title("Rainy Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(output_image)
plt.title("De-rained Image")
plt.axis("off")

plt.show()
