import pygame as pg
from pygame.time import Clock

from drawer import Drawer
from game import Game
from helpers.config import Config
from helpers.img import ImgLoader
from helpers.sfx import SfxHolder
from helpers.text import Text
from helpers.util import Util, user_quit

TILES_X = 30
TILES_Y = 30

GAME_TITLE = 'PySnake'
GAME_ICON = 'img/icon.png'
IMG_FOLDER = 'img/'
SFX_FOLDER = 'sfx/'

CFG = Config('config.ini')
CFG.read()


def game_over() -> bool:
    # Audio
    SFX.game_over.play()

    # Fade-in game over screen
    for i in range(255):
        pg.event.get()  # dummy get
        DRAWER.draw_game(screen, game, 0)  # draw game
        DRAWER.draw_game_over_overlay(screen, i)  # fade-in game over image
        clock.tick(60)  # slow-down the fade-in

        # Refresh screen
        pg.display.flip()

        # Check for quit or restart events
        for event in pg.event.get():
            if user_quit(event):
                return False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if TXT.restart_text_rect.collidepoint(*event.pos):
                    return True

    # Wait till user quits or restarts
    while True:
        for event in pg.event.get():
            if user_quit(event):
                return False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if TXT.restart_text_rect.collidepoint(*event.pos):
                    return True


def main() -> bool:
    # Dump first tick to ignore past
    clock.tick(CFG.frames_per_second)

    while True:
        # Get change in time
        dt = clock.tick(CFG.frames_per_second)

        # Loop over events (quit, key down, key up)
        for event in pg.event.get():
            if user_quit(event):
                return False
            elif event.type == pg.KEYDOWN:
                if event.key in CFG.all_keys:
                    game.press_key(event.key)
            elif event.type == pg.KEYUP:
                if event.key in CFG.all_keys:
                    game.release_key(event.key)

        if not game.paused:
            # Move and draw game
            game.move(dt)
            if not game.game_over:
                DRAWER.draw_game(screen, game, dt)
        else:
            DRAWER.draw_paused_overlay(screen)

        # Update display
        pg.display.update()

        # Break if game no longer running
        if game.game_over:
            return True


if __name__ == '__main__':
    # Initialise all imported pygame modules and clock
    pg.mixer.pre_init(44100, -16, 2, 1024)
    pg.init()
    clock = Clock()

    # Utils and helpers
    UTIL = Util((CFG.width_px, CFG.height_px), (TILES_X, TILES_Y),
                IMG_FOLDER, SFX_FOLDER)
    IMG = ImgLoader(UTIL)
    SFX = SfxHolder(UTIL)
    TXT = Text(CFG)
    DRAWER = Drawer(UTIL, IMG, TXT, CFG)

    # Title and icon
    icon = pg.image.load(GAME_ICON)
    pg.display.set_caption(GAME_TITLE)
    pg.display.set_icon(icon)

    # Create screen
    screen: pg.Surface = pg.display.set_mode(
        (CFG.width_px, CFG.height_px), pg.FULLSCREEN if CFG.full_screen else 0)
    IMG.post_init()  # final steps now that video mode has been set

    running = True
    while running:
        # Create and run game
        game = Game(UTIL, CFG, SFX, (TILES_X, TILES_Y))
        running = main()  # runs game loop

        # Game over sequence (if game still running)
        if running:
            running = game_over()
