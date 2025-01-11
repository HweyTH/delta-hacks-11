import random

def get_words(amount):
    with open('data/words.txt', 'r', encoding='utf-8') as words_file:
        words = words_file.read()
        words = words.split()
        return random.sample(words, amount)

