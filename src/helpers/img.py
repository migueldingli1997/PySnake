from helpers.util import Util


class ImgHolder:
    def __init__(self, util: Util):
        # Game window
        self.game_icon = util.load_img('icon.png')

        # Whole-screen
        self.game_over = util.load_img_from_folder('game_over/')
        self.background = util.load_img_from_folder('background/')

        # Apple and skulls
        self.apple = util.load_img_from_folder('apple/')
        self.enemy = util.load_img_from_folder('skulls/enemy/')
        self.poison = util.load_img_from_folder('skulls/poison/')

        # Powerups
        self.shield = util.load_img_from_folder('powerups/shield/')
        self.ghost = util.load_img_from_folder('powerups/ghost/')
        self.bomb = util.load_img_from_folder('powerups/bomb/')
        self.bullets = util.load_img_from_folder('powerups/bullets/')

        # Snake
        self.snake_normal = util.load_img_from_folder('snake/snake/')
        self.snake_eyes = util.load_img_from_folder('snake/eyes/')
        self.snake_ghost = util.load_img_from_folder('snake/ghost/')
        self.snake_shielded = util.load_img_from_folder('snake/shielded/')

        # Animation sheets
        self.powerups_marker = util.load_img_from_folder('powerups/marker/')

    def post_init(self):
        self.game_over = self.game_over.convert()
