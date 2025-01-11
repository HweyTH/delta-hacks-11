import matplotlib.pyplot as plt
import numpy as np
import json

"""
Creates a graph to show WPM at each second, mistakes, and accuracy.
"""
def visualize_stats():
    with open('data/scores.json', encoding='utf-8') as file:
        scores_data = json.load(file)
        current_game_number = scores_data['games_played']
        game_stats = scores_data[str(current_game_number)]
        avg_wpm = game_stats['avg_wpm']
        highest_wpm = game_stats['highest_wpm']
        all_wpms = game_stats['all_wpms']
        accuracy = game_stats['accuracy']
        mistakes = game_stats['mistakes']
        words_typed = game_stats['words_typed']
        duration = game_stats['duration']

    # Neither of these cases should happen but this is needed for the graph
    diff = abs(len(all_wpms) - duration)
    if len(all_wpms) > duration:
        # Trim extra wpms 
        all_wpms = all_wpms[:-diff]

    elif len(all_wpms) < duration:
        for _ in range(diff):
            all_wpms.append(all_wpms[-1])

    # wpms = np.arange(all_wpms)

    # Could maybe be more efficient
    seconds = []
    time = 1
    for _ in range(duration):
        seconds.append(time)
        time += 1

    print(seconds)
    fig, ax = plt.subplots()
    ax.plot(seconds, all_wpms)

    ax.set(xlabel='Seconds', ylabel='Words Per Minute',
        title='Typing Test Results')
    ax.grid()
    fig.savefig('name.png')
    plt.show()

def get_stats():
    with open('data/scores.json', encoding='utf-8') as file:
        scores_data = json.load(file)
        current_game_number = scores_data['games_played']
        game_stats = scores_data[str(current_game_number)]
        avg_wpm = game_stats['avg_wpm']
        accuracy = game_stats['accuracy']

    return avg_wpm, accuracy