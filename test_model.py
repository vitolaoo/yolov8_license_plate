import os
import cv2
from ultralytics import YOLO
from read_text import read_license_plate

"""
Este codigo serve como uma forma visual para testar o modelo recem treinado, atraves dele voce pode colocar
um video para validacao e ele vai criar um video com os recortes do modelo bem como as deteccoes do OCR,
"""

# Diretorio dos videos
VIDEOS_DIR = os.path.join('.', 'videos')
# Nome do video
video_path = os.path.join(VIDEOS_DIR, 'carro_entrando.mp4')
video_path_out = '{}_out.mp4'.format(video_path)

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
H, W, _ = frame.shape
fps = int(cap.get(cv2.CAP_PROP_FPS))
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

# Caminho do Modelo
model_path = os.path.join('.', 'runs', 'detect', 'train12', 'weights', 'best.pt')
model = YOLO(model_path) 
threshold = 0.5


while ret:
    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            
            license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2)]
            
            # processed_image = preprocess_image(license_plate_crop)
            plate_class = int(class_id) 
            plate_text, confidence, processed_image = read_license_plate(license_plate_crop, plate_class)

            if plate_text:
                cv2.putText(frame, plate_text, (int(x1), int(y2 +30)),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                print(f"Placa detectada: {plate_text} (Confianca: {confidence:.2f})")

            thumb_width, thumb_height = 150, 50
            thumb = cv2.resize(processed_image, (thumb_width, thumb_height))
            if len(thumb.shape) == 2:
                thumb = cv2.cvtColor(thumb, cv2.COLOR_GRAY2BGR)
            margin = 5
            if int(y1) - thumb_height - margin > 0:
                pos_y = int(y1) - thumb_height - margin
            else:
                pos_y = int(y2) + margin
            pos_x = int(x1)
            if pos_x + thumb_width > W:
                pos_x = W - thumb_width - margin

            frame[pos_y:pos_y+thumb_height, pos_x:pos_x+thumb_width] = thumb

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()