from helpers.colours import *
from helpers.config import Config
from helpers.util import Util


class Text:
    def __init__(self, cfg: Config, util: Util):
        # Centered 'PAUSED'' text
        paused_font = pg.font.SysFont(cfg.font, int(cfg.width_px / 20))
        self.paused = paused_font.render('PAUSED', True, WHITE)
        self.paused_rect = self.paused.get_rect(center=util.center_px)

        y_offset = cfg.height_px

        # Bottom right 'Save Score' text
        save_score_font = pg.font.SysFont(cfg.font, int(cfg.width_px / 30))
        self.save_score = save_score_font.render(' Save Score ', True, WHITE)
        self.save_score_rect = self.save_score.get_rect()
        self.save_score_rect.top = y_offset - self.save_score_rect.height
        self.save_score_rect.left = cfg.width_px - self.save_score_rect.width
        y_offset -= self.save_score_rect.height

        # Save Score text once score has been saved (uses same y-coord [.top])
        self.score_saved = save_score_font.render(' Score Saved ', True, GRAY)
        self.score_saved_rect = self.score_saved.get_rect()
        self.score_saved_rect.top = self.save_score_rect.top
        self.score_saved_rect.left = cfg.width_px - self.score_saved_rect.width

        # Bottom right 'Restart' text
        restart_font = pg.font.SysFont(cfg.font, int(cfg.width_px / 30))
        self.restart = restart_font.render(' Restart ', True, WHITE)
        self.restart_rect = self.restart.get_rect()
        self.restart_rect.top = y_offset - self.restart_rect.height
        self.restart_rect.left = cfg.width_px - self.restart_rect.width
        y_offset -= self.restart_rect.height
