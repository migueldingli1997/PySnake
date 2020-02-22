import pygame as pg

from drawer import Drawer
from game import Game
from helpers.config import Config
from helpers.img import ImgHolder
from helpers.sfx import SfxHolder
from helpers.text import Text
from helpers.util import Util
from loop import Loop

TILES_X = 30
TILES_Y = 30

GAME_TITLE = 'PySnake'
GAME_ICON = 'img/icon.png'
IMG_FOLDER = 'img/'
SFX_FOLDER = 'sfx/'

# Initialise all imported pygame modules and clock
pg.mixer.pre_init(44100, -16, 2, 1024)
pg.init()

# Initialise helper components
CFG = Config('config.ini')
CFG.read()  # read config
UTIL = Util((CFG.width_px, CFG.height_px), (TILES_X, TILES_Y),
            IMG_FOLDER, SFX_FOLDER)
IMG = ImgHolder(UTIL)
SFX = SfxHolder(UTIL)
TXT = Text(CFG, UTIL)

if __name__ == '__main__':
    # Initialise game drawer and game loop
    DRAWER = Drawer(UTIL, IMG, TXT, CFG)
    LOOP = Loop(UTIL, CFG, SFX, TXT, DRAWER)

    # Set title and icon
    pg.display.set_caption(GAME_TITLE)
    pg.display.set_icon(IMG.game_icon)

    # Create screen
    screen: pg.Surface = pg.display.set_mode(
        (CFG.width_px, CFG.height_px), pg.FULLSCREEN if CFG.full_screen else 0)
    IMG.post_init()  # final steps now that video mode has been set

    running = True
    while running:
        # Create and run game
        game = Game(UTIL, CFG, SFX, (TILES_X, TILES_Y))
        running = LOOP.main(screen, game)  # runs game loop

        # Game over sequence (if game still running)
        if running:
            running = LOOP.game_over(screen, game)
