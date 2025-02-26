from ultralytics import YOLO

"""
Codigo para treinar um modelo yolo, voce precisara colocar um modelo pre treinado ou um novo, neste caso
estamos usando um modelo novo e em seguida criar um arquivo 'config.yaml' contendo o caminho dos seus dados,
nesse caso o arquivo deve ficar assim:

path: C:/Caminho/para/data
# caminho relativo do path para imagens de treino e validacao abaixo
train: images/train 
val: images/val

# labels do modelo
names:
  0: cars-br
  1: cars-me
  2: motorcycles-br
  3: motorcycles-me
"""

# Load Model
model = YOLO("yolov8n.yaml")

# Use Model
results = model.train(data="config.yaml", epochs=350)