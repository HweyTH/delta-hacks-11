import json
from functions import get_words

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
    def process_frame(self, frame):
        # detected_letter = detect_letter(frame) # Replace with the actual letter detection function 
        detected_letter = 'a' # Temporary value
        if detected_letter:
            self.total_inputs += 1

        # Finished typing word
        if self.letter_index == len(self.current_word) - 1 and detected_letter == self.current_word[self.letter_index]:
            # Only move to the next word if the current word was typed correctly
            self.words_typed.append(self.current_word)
            self.word_index += 1
            self.current_word = self.current_string[self.word_index]

        if detected_letter == 'delete':
            self.letter_index -= 1
            return None
        
        self.letter_index += 1
        if self.current_string[self.letter_index] == detected_letter:
            return True
        else:
            self.mistakes += 1
            return False
    
