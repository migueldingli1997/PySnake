from helpers.util import Util


class SfxHolder:
    def __init__(self, util: Util) -> None:
        self.apple = util.load_sfx('apple.wav')
        self.poison = util.load_sfx('poison.wav')
        self.powerup = util.load_sfx('powerup.wav')
        self.shield_off = util.load_sfx('shield_off.wav')
        self.bullet_hit_skull = util.load_sfx('bullet_hit_skull.wav')
        self.bullet_hit_snake = util.load_sfx('bullet_hit_snake.wav')
        self.game_over = util.load_sfx('game_over.wav')
