import cv2
import pytesseract

# Perform OCR on the entire image
def ocr_full_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

# Perform OCR on a cropped region (bounding box)
def ocr_cropped_region(image, bbox):
    x, y, w, h = bbox
    cropped = image[y:y+h, x:x+w]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray)
