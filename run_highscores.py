import sys

from src.utils.score import ScoresList

if __name__ == '__main__':
    highscores_file = sys.argv[1] if len(sys.argv) > 1 else "highscores"
    scores = ScoresList(highscores_file)
    scores.read()

    if len(scores.scores_list) == 0:
        print('Highscores list is empty.')

    for i, score in enumerate(scores.scores_list):
        print('{}: {}'.format(i, score))
