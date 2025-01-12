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