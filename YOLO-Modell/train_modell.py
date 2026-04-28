from ultralytics import YOLO

# Vortrainiertes YOLOv11-Modell laden
model = YOLO("yolo11n.pt")

# Training starten
model.train(
    data="dataset/dataset.yaml",  # Pfad zur YAML
    epochs=50,                 # Anzahl der Trainingsdurchläufe
    imgsz=640,                  #Bildegröße                     
)