from helpers.util import Util


class ImgHolder:
    def __init__(self, util: Util):
        self.game_icon = util.load_img('icon.png')
        self.apple = util.load_img_from_folder('apple/')
        self.background = util.load_img_from_folder('background/')
        self.enemy = util.load_img_from_folder('skulls/enemy/')
        self.poison = util.load_img_from_folder('skulls/poison/')
        self.shield = util.load_img_from_folder('powerups/shield/')
        self.ghost = util.load_img_from_folder('powerups/ghost/')
        self.bomb = util.load_img_from_folder('powerups/bomb/')
        self.bullets = util.load_img_from_folder('powerups/bullets/')
        self.snake_normal = util.load_img_from_folder('snake/snake/')
        self.snake_eyes = util.load_img_from_folder('snake/eyes/')
        self.snake_ghost = util.load_img_from_folder('snake/ghost/')
        self.snake_shielded = util.load_img_from_folder('snake/shielded/')
        self.game_over = util.load_img_from_folder('game_over/')
        self.powerups_marker = util.load_img_from_folder('powerups/marker/')

    def post_init(self):
        self.game_over = self.game_over.convert()
