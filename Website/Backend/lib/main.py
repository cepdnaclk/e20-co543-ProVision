from derain.rain_model import *
import matplotlib.pyplot as plt

# Example usage of the class:
if __name__ == "__main__":
    # Initialize the model
    model = RainRemovalModel(model_path='derain/model_deraining.pth')

    # Read an example image
    img = cv2.imread("46.jpg")

    # Remove rain from the image
    processed_img = model.remove_rain(img)

    # Display the processed image
    plt.imshow(processed_img)
    plt.show()
