from ultralytics import YOLO

# Download a safe official YOLO model

model = YOLO("yolov8n.pt")
print("Model downloaded and loaded successfully!")
