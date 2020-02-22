from helpers.util import Util


class ImgHolder:
    def __init__(self, util: Util):
        self.apple = util.load_img('apple/')
        self.background = util.load_img('background/')
        self.enemy = util.load_img('skulls/enemy/')
        self.poison = util.load_img('skulls/poison/')
        self.shield = util.load_img('powerups/shield/')
        self.ghost = util.load_img('powerups/ghost/')
        self.bomb = util.load_img('powerups/bomb/')
        self.bullets = util.load_img('powerups/bullets/')
        self.snake_normal = util.load_img('snake/snake/')
        self.snake_eyes = util.load_img('snake/eyes/')
        self.snake_ghost = util.load_img('snake/ghost/')
        self.snake_shielded = util.load_img('snake/shielded/')
        self.game_over = util.load_img('game_over/')
        self.powerups_marker = util.load_img('powerups/marker/')

    def post_init(self):
        self.game_over = self.game_over.convert()
