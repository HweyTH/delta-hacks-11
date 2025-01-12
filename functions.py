import math
import random
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QImage

# def get_words(amount):
#     with open('data/words.txt', 'r', encoding='utf-8') as words_file:
#         words = words_file.read()
#         words = words.split()
#         return random.sample(words, amount)
    
def get_words(amount):
    words = [
        'apple', 'hi', 'game', 'sign', 
        'fig', 'grape', 'honeydew', 'kiwi', 'lemon'
    ]
    return words



def pil_to_pixmap(pil_image):
    pil_image = pil_image.convert("RGBA")
    data = pil_image.tobytes("raw", "RGBA")
    qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
    return QPixmap.fromImage(qimage)

def color_text(word, index, typed_colors):
    """
    Colorize the text of the given word based on the correctness of each letter.

    Args:
        word (str): The word to colorize.
        index (int): The index of the letter currently being typed.
        typed_colors (list[str]): List of colors ('green', 'red', or 'grey') for each letter.

    Returns:
        str: The colorized HTML string of the word.
    """
    green_span = "<span style='color: green;'>{}</span>"
    red_span = "<span style='color: red;'>{}</span>"
    grey_span = "<span style='color: grey;'>{}</span>"

    colored_text = ''

    for i, letter in enumerate(word):
        if i < index:  # Letters before the current index
            if typed_colors[i] == 'green':
                colored_text += green_span.format(letter)
            elif typed_colors[i] == 'red':
                colored_text += red_span.format(letter)
        elif i == index:  # Current letter
            if typed_colors[i] == 'red':  # If already marked as incorrect, stay red
                colored_text += red_span.format(letter)
            else:
                colored_text += grey_span.format(letter)  # Default to grey if not marked yet
        else:  # Letters after the current index
            colored_text += grey_span.format(letter)

    return colored_text

def qimage_to_numpy(qimage):
    width = qimage.width()
    height = qimage.height()
    
    ptr = qimage.constBits()
    ptr.setsize(height * width * 3)
    
    arr = np.array(ptr).reshape(height, width, 3)
    return arr

def handle_face(frame):
    frame = qimage_to_numpy(frame)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_classifier.detectMultiScale(
        frame, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )
    if len(faces) > 0:
        print(f'{len(faces)} face(s) found')
        for (x, y, w, h) in faces:
            center_x = x + w//2
            center_y = y + h//2
            radius = int(np.sqrt(w*w + h*h) / 2)
            cv2.circle(img=frame, center=(center_x, center_y), radius=(math.floor(radius * 0.8)), color=(255, 255, 255), thickness=-1)
    else:
        print('no faces detected')

    return QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)