import json
from functions import get_words
import numpy as np
import cv2
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from tf_keras.utils import load_img, img_to_array
from tf_keras.models import load_model
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image


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
        # Ensure the input image is in the correct color format for processing (if it's a QImage/QPixmap)

        # Convert PIL Image to NumPy array for OpenCV processing (if it's already a PIL Image)
        img = np.array(image)  # Convert the image to NumPy array (if it's not already)
        
        # Convert the image from BGR to RGB (OpenCV uses BGR by default)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert the NumPy array to a PIL Image
        im_pil = Image.fromarray(img)
        
        # Continue with the rest of the prediction code
        img_array = np.array(im_pil) / 255.0  # Normalize the image data
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        
        predictions = model.predict(img_array)
        
        # Define label mapping
        label_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
                    8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 
                    16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 
                    24: 'Y', 25: 'Z', 26: 'del', 27: 'nothing', 28: 'space'}
        
        # Get the predicted class
        predicted_class = label_map[np.argmax(predictions[0])]
        return predicted_class


    def process_frame(self, frame):
        path = 'sign_language_model.h5'
        model = load_model(path)
        detected_letter = self.predict_image(frame,model) # Replace with the actual letter detection function 
        if detected_letter:
            self.total_inputs += 1



        # Finished typing word
        if self.letter_index == len(self.current_word) - 1 and detected_letter == self.current_word[self.letter_index]:
            # Only move to the next word if the current word was typed correctly
            self.words_typed.append(self.current_word)
            self.word_index += 1
            self.current_word = self.current_string[self.word_index]

        if detected_letter == 'del':
            self.letter_index -= 1
            return None
        
        self.letter_index += 1
        if self.current_string[self.letter_index] == detected_letter:
            return True
        else:
            self.mistakes += 1
            return False
    
