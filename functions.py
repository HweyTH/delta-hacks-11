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

def color_text(word, index, color):
    """
    Colorize the text of the given word based on the index and color.

    Args:
        word (str): The word to colorize.
        index (int): The index of the letter to color.
        color (str): The color to use ('red' or 'green').

    Returns:
        str: The colorized HTML string of the word.
    """
    green_span = "<span style='color: green;'>{}</span>"
    red_span = "<span style='color: red;'>{}</span>"
    grey_span = "<span style='color: grey;'>{}</span>"

    colored_text = ''

    # Add letters before the index
    for i in range(min(index, len(word))):  # Ensure we don't exceed bounds
        colored_text += green_span.format(word[i])

    # Check if index is valid before coloring
    if 0 <= index < len(word):
        if color == 'red':
            colored_text += red_span.format(word[index])
        elif color == 'green':
            colored_text += green_span.format(word[index])

    # Add letters after the index
    for i in range(index + 1, len(word)):
        colored_text += grey_span.format(word[i])

    return colored_text


