import easyocr
import cv2
import re

"""
Este codigo contem as funcoes para tratar a imagemda placa recortada, ler o seu conteudo
e validar caso a deteccao esteja em um formato diferente do formato das placas
"""

reader = easyocr.Reader(['en'], gpu=False)

dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

vehicle_classes = {
    0: ['L', 'L', 'L', 'D', 'D', 'D'], # cars-br
    1: ['L', 'L', 'L', 'D', 'L', 'D', 'D'], # cars-me 
    2: ['L', 'L', 'L', 'D', 'D', 'D'], # motorcycle-br
    3: ['L', 'L', 'L', 'D', 'L', 'D', 'D'] # motorcycle-me
}

def preprocess_image(image):
    """
    Aplicacao de pre-processamento para melhorar a qualidade
    da imagem para o OCR
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.medianBlur(image, 3)
    """
    
    image = cv2.equalizeHist(image)
    image = cv2.adaptiveThreshold(image, 255,
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY,
                                  11, 2)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    """
    return image

def validate_and_correct_plate(text, plate_class):
    """
    Recebe o texto reconhecido e tenta corrigir os caracteres, 
    validando se o resultado corresponde a uma placa brasileira válida.
    São considerados dois formatos:
      - Cinza: 3 letras seguidas de 3 dígitos (ex.: ABC123)
      - Mercosul: 3 letras, 1 dígito, 1 letra e 2 dígitos (ex.: ABC1D23)
    
    Retorna o texto corrigido se for válido ou None caso contrário.
    """
    candidate = "".join(text.split()).upper()

    if plate_class not in vehicle_classes:
        return None
    
    expected = vehicle_classes[plate_class]

    if len(candidate) != len(expected):
        return None
    
    candidate_list = list(candidate)

    for i, exp in enumerate(expected):
        char = candidate_list[i]
        if exp == 'L' and not char.isalpha():
            candidate_list[i] = dict_int_to_char.get(char, None)
        elif exp == 'D' and not char.isdigit():
            candidate_list[i] = dict_char_to_int.get(char, None)
        if candidate_list[i] is None:
            return None
    
    corrected = "".join(candidate_list)
    pattern = r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$' if plate_class in [1, 3] else r'^[A-Z]{3}[0-9]{4}$'

    return corrected if re.match(pattern, corrected) else None


def read_license_plate(license_plate_crop, plate_class):
    """
    Read the license plate text from the given cropped image.
    Args:
        license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

    Returns:
        tuple: Tuple containing the formatted license plate text and its confidence score.
    """
    processed_image = preprocess_image(license_plate_crop)
    detections = reader.readtext(processed_image, text_threshold=0.7)

    if detections:
        bbox, text, score = detections[0]
        candidate = validate_and_correct_plate(text, plate_class)
        print(plate_class)
        if candidate is not None and score >= 0.7:
            with open("plates.txt", "a") as f:
                f.write(f"{candidate} - {score:.2f} - {plate_class}\n")
            return candidate, score, processed_image
    
    return None, None, processed_image