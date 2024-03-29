import pygame as pg
from pygame.time import Clock

from src.drawer import Drawer
from src.game import Game
from src.utils.config import Config
from src.utils.score import ScoresList
from src.utils.sfx import SfxHolder
from src.utils.text import Text
from src.utils.util import Util, user_quit


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

            # Move and draw game (with possible paused screen and fps)
            if not game.paused:
                game.move(dt)
            if not game.game_over:
                self.drawer.draw_game(screen, game, dt)
            if game.paused:
                self.drawer.draw_paused_overlay(screen)
            if self.cfg.draw_fps:
                self.drawer.draw_fps(screen, self.clock.get_fps())

            # Update display
            pg.display.update()

            # Break if game no longer running
            if game.game_over:
                return True

    def game_over(self, screen, game: Game, scores: ScoresList) -> bool:
        score_saved = False  # not saved yet
        self.sfx.game_over.play()  # play audio

        i = 0
        while True:
            # Fade-in game over screen
            if i < 256:
                pg.event.get()  # dummy get
                self.drawer.draw_game(screen, game, 0)  # draw game
                self.drawer.draw_game_over_overlay(
                    screen, i, score_saved)  # fade-in game over screen
                self.clock.tick(60)  # slow-down the fade-in

                # Refresh screen
                pg.display.flip()
                i += 1

            # Check for quit or restart events
            for event in pg.event.get():
                if user_quit(event):
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.txt.restart_rect.collidepoint(*event.pos):
                        return True
                    elif not score_saved and \
                            self.txt.save_score_rect.collidepoint(*event.pos):
                        for score in game.get_scores():
                            scores.add_score(score)
                        scores.write()
                        score_saved = True
