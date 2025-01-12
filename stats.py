import matplotlib.pyplot as plt
import json
from PIL import Image

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

    # Could maybe be more efficient
    seconds = []
    time = 1
    for _ in range(duration):
        seconds.append(time)
        time += 1

    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.figure(figsize=(7, 3))
    plt.plot(seconds, all_wpms, color="#d79921", linewidth=2)
    plt.gca().set_facecolor('#282828')
    plt.gcf().set_facecolor('#282828')
    plt.gca().spines['top'].set_color('#645a52')
    plt.gca().spines['bottom'].set_color('#645a52')
    plt.gca().spines['left'].set_color('#645a52')
    plt.gca().spines['right'].set_color('#645a52')
    plt.gca().spines['top'].set_linewidth(2)
    plt.gca().spines['bottom'].set_linewidth(2)
    plt.gca().spines['left'].set_linewidth(2)
    plt.gca().spines['right'].set_linewidth(2)
    plt.tick_params(axis='x', colors='#645a52')
    plt.tick_params(axis='y', colors='#645a52')
    plt.ylabel('Words Per Minute', fontname='Arial', fontsize=10, color='#d79921')
    plt.tight_layout()
    plt.gcf().canvas.draw()
    image = Image.frombytes('RGB', 
                           plt.gcf().canvas.get_width_height(),
                           plt.gcf().canvas.tostring_rgb())
    return image

def get_stats():
    with open('data/scores.json', encoding='utf-8') as file:
        scores_data = json.load(file)
        current_game_number = scores_data['games_played']
        game_stats = scores_data[str(current_game_number)]
        avg_wpm = game_stats['avg_wpm']
        accuracy = game_stats['accuracy']

    return avg_wpm, accuracy

