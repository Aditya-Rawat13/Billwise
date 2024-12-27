import cv2
import numpy as np

# Load the image
img = cv2.imread('jayesh3.jpeg')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Light denoising
denoised = cv2.GaussianBlur(gray, (5, 5), 0)

# Normalize lighting
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
background = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
normalized = cv2.divide(denoised, background, scale=255)

ret, binary = cv2.threshold(normalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
erode_kernel = np.ones((2, 2), np.uint8)
eroded = cv2.erode(binary, erode_kernel, iterations=1)

# Optional: Dilation after opening to enhance text thickness
dilation_kernel = np.ones((1, 1), np.uint8)
dilated = cv2.dilate(eroded, dilation_kernel, iterations=1)

# Display results
cv2.imshow('Original', img)
cv2.imshow('Normalized', normalized)
cv2.imshow('Eroded', eroded)
cv2.imshow('Dilated', dilated)
cv2.imshow('Binary', binary)

cv2.waitKey(0)
cv2.destroyAllWindows()
