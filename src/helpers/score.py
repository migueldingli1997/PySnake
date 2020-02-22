import shelve
from datetime import datetime

KEY = 'score'
MAX_SCORES = 10


class Score:
    def __init__(self, name: str, max_length: int,
                 level_reached: int, at: datetime):
        self.name = name
        self.max_length = max_length
        self.level_reached = level_reached
        self.at = at

    @property
    def score(self) -> int:
        return self.max_length + self.level_reached

    def __str__(self):
        return str({'name': self.name, 'score': self.score,
                    'level_reached': self.level_reached,
                    'max_length': self.max_length,
                    'at': self.at})


class ScoresList:
    def __init__(self, highscores_file: str):
        self.highscores_file = highscores_file
        self.scores_list = []

    def read(self):
        with shelve.open(self.highscores_file) as f:
            if KEY in f:
                self.scores_list = f[KEY]

    def write(self):
        with shelve.open(self.highscores_file) as f:
            f[KEY] = self.scores_list

    def add_score(self, new_score: Score):
        new_score_index = len(self.scores_list)
        for i, s in enumerate(self.scores_list):
            if new_score.score > s.score:
                new_score_index = i

        if new_score_index < MAX_SCORES:
            self.scores_list.insert(new_score_index, new_score)
            self.scores_list = self.scores_list[:MAX_SCORES]
