import pygame as pg

from helpers.config import Config
from helpers.util import Util


class Text:
    def __init__(self, cfg: Config, util: Util):
        paused_font = pg.font.SysFont(cfg.font, int(cfg.width_px / 20))
        self.paused_text = paused_font.render('PAUSED', True, pg.Color('white'))
        self.paused_text_rect = self.paused_text.get_rect(center=util.center_px)

        restart_font = pg.font.SysFont(cfg.font, int(cfg.width_px / 30))
        self.restart_text = restart_font.render(' Restart ', True,
                                                pg.Color('white'))
        self.restart_text_rect = self.restart_text.get_rect()
        self.restart_text_rect.top = cfg.height_px - self.restart_text_rect.height
        self.restart_text_rect.left = cfg.width_px - self.restart_text_rect.width
