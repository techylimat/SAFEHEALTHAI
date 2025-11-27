import os
os.environ["ULTRALYTICS_NO_CHECK"] = "1"


from ultralytics import YOLO

def train_model():
    model = YOLO('yolov8s.pt')

    results = model.train(
        data="C:/Users/USER/PycharmProjects/PythonProject1/datasets/data.yaml",
        epochs=50,
        imgsz=320,
        batch=8,
        workers=0,
        name="safehealth_model",
        pretrained=True
    )

    print("Training complete! Model stored in runs/detect/safehealth_model")

if __name__ == "__main__":
    train_model()
