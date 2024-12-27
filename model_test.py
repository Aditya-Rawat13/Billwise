import torch

# Load the trained model
model = torch.hub.load(
    'ultralytics/yolov5', 
    'custom', 
    path=r'C:\Users\rawat\Documents\proramming\final_ocr\yolov5\runs\train\exp\weights\best.pt'
)
  # Replace with your model path
# Load the image
img = 'images\test2.jpg'  # Path to your image

# Perform inference
results = model(img)
# Results (bounding boxes, labels, and confidence)
results.show()  # This will show the image with boxes drawn
results.save()  # Save the output image with detections




