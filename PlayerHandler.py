import json
from functions import get_words
import numpy as np
import cv2
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from tf_keras.utils import load_img, img_to_array
from tf_keras.models import load_model
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image
import tensorflow as tf


class PlayerHandler():
    def __init__(self, duration):
        self.duration = duration
        self.time = 1
        self.letter_index = 0
        self.word_index = 0
        self.all_wpm = [] # Add wpm to list each second
        self.current_wpm = 0
        self.highest_wpm = 0
        self.mistakes = 0 # Total count of mistakes made
        self.words_typed = []
        self.current_string = get_words(10000) # Get a bunch of words so we don't have to keep fetching more
        self.current_word = self.current_string[0]
        self.total_inputs = 1


    # Call every second
    def update_wpm(self):
        self.time += 1 # Should maybe be in its own place
        self.current_wpm = self.current_wpm / (self.time/60)
        self.all_wpm.append(self.current_wpm)
        if self.current_wpm > self.highest_wpm: self.highest_wpm = self.current_wpm

    def save_stats(self):
        avg_wpm = sum(self.all_wpm) / self.duration # Divide by duration to get average wpm
        accuracy = self.mistakes / self.total_inputs
        old_data = json.load(open('data/scores.json', 'r'))
        old_data['games_played'] += 1
        stats = {
            old_data['games_played']: {
            'avg_wpm': avg_wpm,
            'highest_wpm': self.highest_wpm,
            'all_wpms': self.all_wpm,
            'accuracy': accuracy,
            'mistakes': self.mistakes,
            'words_typed': self.words_typed,
            'duration': self.duration
            }
        }

        old_data.update(stats)
        with open('data/scores.json', 'w', encoding='utf-8') as file:
            json.dump(old_data, file, indent=4)
        
        print('saved data')

    """
    Returns True if detected letter matches the letter that needs to be typed, returns False if it does not.
    Returns None if detected letter is delete.
    """

    def predict_image(self, image, model):
        # Convert QImage to NumPy array
        if isinstance(image, QImage):
            image = image.convertToFormat(QImage.Format_RGB888)  # Ensure consistent format
            width, height = image.width(), image.height()
            bytes_per_line = image.bytesPerLine()
            
            # Create NumPy array from QImage
            img_array = np.frombuffer(image.bits().asstring(image.byteCount()), dtype=np.uint8)
            img_array = img_array.reshape((height, width, 3))  # Format_RGB888 has 3 channels (R, G, B)

            # Convert to PIL Image for further processing
            image = Image.fromarray(img_array)

        # Resize image to match the model's input shape
        target_size = (64, 64)  # Target size expected by the model
        image = image.resize(target_size)

        # Convert PIL Image to array
        image_array = img_to_array(image) / 255.0
        image_array = tf.expand_dims(image_array, axis=0)  # Add batch dimension

        # Perform predictions
        predictions = model.predict(image_array)

        # Define label mapping
        label_map = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
            8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 
            16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 
            24: 'Y', 25: 'Z', 26: 'del', 27: 'nothing', 28: 'space'
        }

        # Get the predicted class
        predicted_class = label_map[np.argmax(predictions[0])]
        return predicted_class


    def process_frame(self, frame):
        """
        Process the input frame, predict the letter, and update the game state.
        """
        path = 'sign_language_model.h5'
        model = load_model(path)
        detected_letter = self.predict_image(frame, model)  # Predict the letter

        print(f"Detected Letter: {detected_letter}")  # Debug: Log detected letter
        print(f"Current Word: {self.current_word}")  # Debug: Log the current word
        print(f"Letter Index: {self.letter_index}")  # Debug: Log the current letter index

        if detected_letter:  # Ensure detected_letter is valid
            self.total_inputs += 1

            # Finished typing the word correctly
            if (
                self.letter_index == len(self.current_word) - 1
                and detected_letter == self.current_word[self.letter_index]
            ):
                print(f"Word Completed: {self.current_word}")  # Debug: Word completed
                self.words_typed.append(self.current_word)
                self.word_index += 1

                # Check if there are more words to type
                if self.word_index < len(self.current_string):
                    self.current_word = self.current_string[self.word_index]
                    self.letter_index = 0  # Reset letter index for the new word
                else:
                    print("No more words to type.")  # Debug: All words completed
                    return

            # Handle delete logic
            elif detected_letter == 'backspace':  # Assuming 'backspace' is returned for deletion
                self.letter_index = max(0, self.letter_index - 1)  # Prevent negative index
                colorized_text = color_text(self.current_word, self.letter_index, 'grey')
                self.update_display(colorized_text)  # Update display with grey color
                return None

            # Match detected letter with the current letter in the word
            elif (
                self.letter_index < len(self.current_word)
                and detected_letter == self.current_word[self.letter_index]
            ):
                self.letter_index += 1
                print(f"Correct Letter: {detected_letter}")  # Debug: Correct letter typed
                colorized_text = color_text(self.current_word, self.letter_index, 'green')
                self.update_display(colorized_text)  # Update display with green color

            # Incorrect letter detected
            else:
                self.mistakes += 1
                print(f"Incorrect Letter: {detected_letter}")  # Debug: Incorrect letter typed
                colorized_text = color_text(self.current_word, self.letter_index, 'red')
                self.update_display(colorized_text)  # Update display with red color

            # Ensure letter_index does not exceed the length of the current_word
            self.letter_index = min(self.letter_index, len(self.current_word) - 1)
