from pytesseract import image_to_string
import cv2

def detect_bounding_boxes(image_path):
    import torch

    # Load YOLO model
    model = torch.hub.load(
    'ultralytics/yolov5', 
    'custom', 
    path=r'C:\Users\rawat\Documents\proramming\chatgpt\yolov5\yolov5-training\invoice_experiment4\weights\best.pt'
)
    img = cv2.imread(image_path)

    # Run YOLO detection
    results = model(img)
    detections = results.xyxy[0].cpu().numpy()  # Get bounding box results

    detected_info = []
    for detection in detections:
        x1, y1, x2, y2, conf, cls = detection  # YOLO bbox coordinates and class
        bbox = [int(x1), int(y1), int(x2), int(y2)]

        # Crop the bounding box from the image
        cropped_img = img[int(y1):int(y2), int(x1):int(x2)]

        # Extract text using OCR
        text = image_to_string(cropped_img, lang='eng').strip()

        # Map class to field name
        field = map_class_to_field(int(cls))  # Implement a mapping function if needed
        detected_info.append({'field': field, 'text': text, 'bbox': bbox})

    return detected_info

def map_class_to_field(cls):
    field_mapping = {
        0: 'company',
        1: 'date',
        2: 'total'
    }
    return field_mapping.get(cls, 'unknown')


def process_invoice(image_path):
    # Step 1: Run YOLO detection
    detected_info = detect_bounding_boxes(image_path)
    print("Detected Information:", detected_info)  # Debugging output

    # Initialize fields
    company_name = ""
    invoice_date = ""
    total_amount = ""

    # Step 2: Extract detected text for fields
    for detection in detected_info:
        field = detection['field']
        text = detection['text']

        if field == 'company':
            company_name = text
        elif field == 'date':
            invoice_date = text
        elif field == 'total':
            total_amount = text

   

    # Debugging outputs
    print(f"Company: {company_name}, Date: {invoice_date}, Total: {total_amount}")

    # Step 4: Save to CSV
   
if __name__ == "__main__":
    process_invoice("234.jpg")  # Replace with the path to your test invoice image
