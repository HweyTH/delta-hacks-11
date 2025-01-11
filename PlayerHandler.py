"""
scores.json format:
{
    "games_played": 1,
    "1": {"wpm": 0, "accuracy": 0, "words_typed": []},
}
"""

import json

class PlayerHandler():
    def __init__(self):
        self.index = 0
        self.wpm = 0
        self.accuracy = 0
        self.words_typed = []
        self.current_string = None

    def save_stats(self):
        old_data = json.load(open('data/scores.json', 'r'))
        old_data['games_played'] += 1
        stats = {old_data['games_played']: {'wpm': self.wpm, 'accuracy': self.accuracy, 'words_typed': self.words_typed}}
        old_data.update(stats)
        with open('data/scores.json', 'w', encoding='utf-8') as file:
            json.dump(old_data, file, indent=4)
        
        print('saved data')

