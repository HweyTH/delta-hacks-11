import random
from PyQt5.QtGui import QPixmap, QImage

def get_words(amount):
    with open('data/words.txt', 'r', encoding='utf-8') as words_file:
        words = words_file.read()
        words = words.split()
        return random.sample(words, amount)

def pil_to_pixmap(pil_image):
    pil_image = pil_image.convert("RGBA")
    data = pil_image.tobytes("raw", "RGBA")
    qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
    return QPixmap.fromImage(qimage)