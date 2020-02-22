import pygame as pg

from helpers.config import Config
from helpers.util import Util


class Text:
    def __init__(self, cfg: Config, util: Util):
        WHITE = pg.Color('White')

        # Centered 'PAUSED'' text
        paused_font = pg.font.SysFont(cfg.font, int(cfg.width_px / 20))
        self.paused = paused_font.render('PAUSED', True, WHITE)
        self.paused_rect = self.paused.get_rect(center=util.center_px)

        # Bottom right 'Restart' text
        restart_font = pg.font.SysFont(cfg.font, int(cfg.width_px / 30))
        self.restart = restart_font.render(' Restart ', True, WHITE)
        self.restart_rect = self.restart.get_rect()
        self.restart_rect.top = cfg.height_px - self.restart_rect.height
        self.restart_rect.left = cfg.width_px - self.restart_rect.width
