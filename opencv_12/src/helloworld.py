from ultralytics import YOLO

# yolo모델 설정
model = YOLO('yolo11n.pt')

results = model('https://ultralytics.com/images/bus.jpg')

results[0].show()