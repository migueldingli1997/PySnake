import pygame as pg
from pygame.time import Clock

from drawer import Drawer
from game import Game
from helpers.config import Config
from helpers.sfx import SfxHolder
from helpers.text import Text
from helpers.util import Util, user_quit


class Loop:
    def __init__(self, util: Util, cfg: Config, sfx: SfxHolder, txt: Text,
                 drawer: Drawer):
        self.util = util
        self.cfg = cfg
        self.sfx = sfx
        self.txt = txt
        self.drawer = drawer
        self.clock = Clock()

    def main(self, screen, game: Game) -> bool:
        # Dump first tick to ignore past
        self.clock.tick(self.cfg.frames_per_second)

        while True:
            # Get change in time
            dt = self.clock.tick(self.cfg.frames_per_second)

            # Loop over events (quit, key down, key up)
            for event in pg.event.get():
                if user_quit(event):
                    return False
                elif event.type == pg.KEYDOWN:
                    if event.key in self.cfg.all_keys:
                        game.press_key(event.key)
                elif event.type == pg.KEYUP:
                    if event.key in self.cfg.all_keys:
                        game.release_key(event.key)

            if not game.paused:
                # Move and draw game
                game.move(dt)
                if not game.game_over:
                    self.drawer.draw_game(screen, game, dt)
            else:
                self.drawer.draw_paused_overlay(screen)

            # Update display
            pg.display.update()

            # Break if game no longer running
            if game.game_over:
                return True

    def game_over(self, screen, game: Game) -> bool:
        # Audio
        self.sfx.game_over.play()

        # Fade-in game over screen
        for i in range(255):
            pg.event.get()  # dummy get
            self.drawer.draw_game(screen, game, 0)  # draw game
            self.drawer.draw_game_over_overlay(screen, i)  # fade-in game over image
            self.clock.tick(60)  # slow-down the fade-in

            # Refresh screen
            pg.display.flip()

            # Check for quit or restart events
            for event in pg.event.get():
                if user_quit(event):
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.txt.restart_rect.collidepoint(*event.pos):
                        return True

        # Wait till user quits or restarts
        while True:
            for event in pg.event.get():
                if user_quit(event):
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.txt.restart_rect.collidepoint(*event.pos):
                        return True
