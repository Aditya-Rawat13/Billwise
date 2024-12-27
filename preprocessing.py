import cv2
import numpy as np

def preprocess_image(input_image_path, output_image_path):
    # Read the image
    image = cv2.imread(input_image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {input_image_path}")

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's Thresholding
    #_, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Dynamically determine kernel size and iterations based on image resolution
    height, width = gray_image.shape
    if height > 1000 or width > 1000:  # High-resolution image
        kernel_size = (5, 5)
        iterations = 1
    elif height > 500 or width > 500:  # Medium-resolution image
        kernel_size = (3, 3)
        iterations = 1
    else:  # Low-resolution image
        kernel_size = (2, 2)
        iterations = 1

    # Create the kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

    # Apply erosion
    eroded_image = cv2.erode(gray_image, kernel, iterations=iterations)

    # Apply dilation
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=iterations)

    # Save the preprocessed image
    cv2.imwrite(output_image_path, dilated_image)

    print(f"Preprocessed image saved at {output_image_path}")

# Example usage
preprocess_image("the-bill.jpg", "preprocessed_image.jpg")
