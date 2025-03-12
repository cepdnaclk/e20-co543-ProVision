import torch
from .MPRNet import MPRNet
import cv2
import numpy as np

class RainRemovalModel:
    def __init__(self, model_path='model_deraining.pth', device=None):
        """
        Initialize the RainRemovalModel class.

        :param model_path: Path to the model checkpoint file.
        :param device: The device to run the model on ('cpu' or 'cuda'). If None, defaults to CUDA if available.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if device is None else torch.device(device)
        self.model = self._load_model(model_path)
        self.model.to(self.device)
        self.model.eval()

    def _load_model(self, model_path):
        """
        Load the MPRNet model from a checkpoint.

        :param model_path: Path to the model checkpoint file.
        :return: Loaded MPRNet model.
        """
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
            checkpoint = torch.load(model_path, map_location=self.device)
            if 'state_dict' in checkpoint:
                model.load_state_dict(checkpoint['state_dict'])
            else:
                model.load_state_dict(checkpoint)
        except FileNotFoundError:
            print(f"Error: Model checkpoint '{model_path}' not found.")
            return None
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
        
        return model

    def preprocess_image(self, input_img, img_size=(512, 384)):
        """
        Preprocess the input image to the format required by the model.

        :param input_img: The input image as a numpy array (BGR format).
        :param img_size: The target size to which the image should be resized.
        :return: A preprocessed tensor to feed into the model.
        """
        if input_img is None:
            raise ValueError(f"Image not found or unable to open.")

        # Convert BGR to RGB
        input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

        # Resize image
        input_img = cv2.resize(input_img, img_size)

        # Normalize the image
        input_img = input_img.astype(np.float32) / 255.0
        input_img = np.transpose(input_img, (2, 0, 1))  # Change to (C, H, W)

        # Convert to tensor
        input_tensor = torch.from_numpy(input_img).unsqueeze(0)
        return input_tensor.to(self.device)

    def remove_rain(self, input_img):
        """
        Perform rain removal on the input image.

        :param input_img: The input image as a numpy array (BGR format).
        :return: The processed image with rain removed (as a numpy array).
        """
        try:
            input_tensor = self.preprocess_image(input_img)
        except ValueError as e:
            print(e)
            return

        with torch.no_grad():
            output_tensor = self.model(input_tensor)[0]

        # Convert tensors to numpy arrays
        output_img = output_tensor.squeeze(0).cpu().numpy().transpose(1, 2, 0)

        # Clip the values and convert to uint8 for image processing
        output_img = (np.clip(output_img, 0, 1) * 255).astype(np.uint8)

        final_image = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)

        return final_image

