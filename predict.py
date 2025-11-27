from ultralytics import YOLO
import cv2

model = YOLO('C:/Users/USER/PycharmProjects/PythonProject1/runs/detect/safehealth_model4/weights/best.pt')

# choose a test image
image_path = "C:/Users/USER/PycharmProjects/PythonProject1/datasets/test/images/pexels-emmet-35167-128421_jpg.rf.4f1dc4e12538f067ec3962d23ab69905.jpg"

results = model(image_path, conf=0.05)

# Save result
results[0].save(filename="prediction.jpg")
