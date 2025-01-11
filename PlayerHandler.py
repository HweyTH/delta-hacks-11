import json

class PlayerHandler():
    def __init__(self, duration):
        self.duration = duration
        self.time = 1
        self.index = 0
        self.all_wpm = [] # add wpm to list each second
        self.current_wpm = 0
        self.highest_wpm = 0
        self.accuracy = 0
        self.mistakes = 0 # count
        self.words_typed = []
        self.current_string = None

    # Call every second
    def update_wpm(self):
        self.current_wpm = self.current_wpm / (self.time/60)
        self.all_wpm.append(self.current_wpm)
        if self.current_wpm > self.highest_wpm: self.highest_wpm = self.current_wpm

    def save_stats(self):
        avg_wpm = sum(self.all_wpm) / self.duration # divide by duration to get average wpm
        old_data = json.load(open('data/scores.json', 'r'))
        old_data['games_played'] += 1
        stats = {
            old_data['games_played']: {
            'avg_wpm': avg_wpm,
            'highest_wpm': self.highest_wpm,
            'accuracy': self.accuracy,
            'mistakes': self.mistakes,
            'words_typed': self.words_typed
            }
        }
        old_data.update(stats)
        with open('data/scores.json', 'w', encoding='utf-8') as file:
            json.dump(old_data, file, indent=4)
        
        print('saved data')

