import cv2
import os

def resize_image(input_image_path, output_directory, target_size=(512, 384)):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Read the image from the specified path
    image = cv2.imread(input_image_path)

    if image is None:
        print(f"Error: Could not read the image from {input_image_path}")
        return

    # Resize the image to the target size (512x384)
    resized_image = cv2.resize(image, target_size)

    # Get the filename from the input path and create a new output path in the directory
    filename = os.path.basename(input_image_path)
    output_image_path = os.path.join(output_directory, filename)

    # Save the resized image to the output path
    cv2.imwrite(output_image_path, resized_image)

    print(f"Image resized successfully and saved to {output_image_path}")

# Example usage:
input_image_path = 'resized/images.jpg'  # Replace with your image file path
output_directory = 'resized'  # Replace with your desired directory path

resize_image(input_image_path, output_directory)
