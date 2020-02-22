import sys

from helpers.score import ScoresList

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Incorrect number of arguments')
        sys.exit(-1)
    else:
        scores = ScoresList(sys.argv[1])
        scores.read()

    if len(scores.scores_list) == 0:
        print('Highscores list is empty.')

    for i, score in enumerate(scores.scores_list):
        print('{}: {}'.format(i, score))
