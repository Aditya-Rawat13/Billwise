import torch
import cv2
import pytesseract
import csv
import os

model = torch.hub.load(
    'ultralytics/yolov5',
    'custom',
    path=r'C:\Users\rawat\Documents\proramming\final_ocr\yolov5\runs\train\exp\weights\best.pt'
)

LABEL_TO_SECTION = {
    "company name": "Company",
    "company_name": "Company",
    "date": "Date",
    "total": "Total",
    "item name": "Item Name",
    "item_name": "Item Name"
}

def detect_bounding_boxes(image_path):
    img = cv2.imread(image_path)
    results = model(img)
    detected_info = {section: [] if section == "Item Name" else "" for section in LABEL_TO_SECTION.values()}
    for *box, conf, class_id in results.xyxy[0].cpu().numpy():
        label = model.names[int(class_id)]
        normalized_label = label.lower().replace(" ", "_")
        if normalized_label in LABEL_TO_SECTION:
            field_name = LABEL_TO_SECTION[normalized_label]
            x_min, y_min, x_max, y_max = map(int, box)
            cropped_img = img[y_min:y_max, x_min:x_max]
            extracted_text = pytesseract.image_to_string(cropped_img, config='--psm 6')
            if field_name == "Item Name":
                detected_info[field_name].append(extracted_text.strip())
            else:
                detected_info[field_name] = extracted_text.strip()
    detected_info["Item Name"] = ", ".join(detected_info["Item Name"])
    return detected_info

def save_to_csv(image_path, detected_info):
    csv_file = 'detected_information.csv'
    file_exists = False
    try:
        with open(csv_file, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Company", "Date", "Total", "Item Name"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(detected_info)

def extract_full_text(image_path):
    img = cv2.imread(image_path)
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text

def process_invoice(image_path):
    detected_info = detect_bounding_boxes(image_path)
    save_to_csv(image_path, detected_info)
    company = detected_info.get("Company", "")
    date = detected_info.get("Date", "")
    total = detected_info.get("Total", "")
    item_name = detected_info.get("Item Name", "")
    if not company or not date or not total or not item_name:
        return None
    return [company, date, total, item_name]

if __name__ == "__main__":
    test_image = "images/test2.jpg"
    process_invoice(test_image)
    results = model(test_image)
    results.show()
    results.save()
