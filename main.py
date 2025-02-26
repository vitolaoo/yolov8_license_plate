import cv2
import os
import serial
from read_text import read_license_plate
from database import verificar_placa
from ultralytics import YOLO
import time

"""
Este main funciona de um jeito parecido com o test_model.py, exceto pelo fato de ele nao criar um video "output"
para visualizacao das deteccoes, entretanto aqui precisamos de uma coneccao com arduino bem como o banco de dados
por se tratar do codigo principal do projeto, caso deseje apenas testar o projeto recomendo utilizar o test_model
pois ele fara basicamente a mesma coisa que esse codigo porem sem precisar do arduino configurado nem da DB
"""

# Configuração da porta serial
arduino_port = 'COM5'
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)

# Teste dos LEDs
ser.write(b'G')
time.sleep(0.3)  
ser.write(b'O') 
ser.write(b'R')
time.sleep(0.3) 
ser.write(b'O') 

# Diretório do vídeo
VIDEOS_DIR = os.path.join('.', 'videos')
video_path = os.path.join(VIDEOS_DIR, 'carro_entrando.mp4')

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

# Carregar modelo YOLO
model_path = os.path.join('.', 'runs', 'detect', 'train12', 'weights', 'best.pt')
model = YOLO(model_path) 
threshold = 0.5 

if not ret:
    print("Erro ao carregar o vídeo.")
    exit()

while ret:
    # Detecção da placa usando YOLO
    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            # Realizar o corte da placa da imagem
            license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2)]
            plate_class = int(class_id)  # Classe da placa detectada (cars-me, cars-br, motorcycle-me ou motorcycle-br)

            # Realiza a leitura da placa com OCR
            plate_text, confidence, _ = read_license_plate(license_plate_crop, plate_class)

            if plate_text:
                print(f"Placa detectada: {plate_text} (Confiança: {confidence:.2f})")

                # Verificar no banco de dados se a placa está cadastrada
                if verificar_placa(plate_text):
                    print("Cancela aberta")
                    ser.write(b'G')
                    time.sleep(5)
                    ser.write(b'O')
                else:
                    print("Acesso negado")
                    ser.write(b'R')
                    time.sleep(5)
                    ser.write(b'O')

    ret, frame = cap.read()

cap.release()
cv2.destroyAllWindows()

ser.close()