import pygame as pg

from game import Game
from helpers.anim import SpriteSheetAnimation
from helpers.config import Config
from helpers.img import ImgHolder
from helpers.text import Text
from helpers.util import rotate_image, Util


class Drawer():
    def __init__(self, util: Util, img: ImgHolder, txt: Text, cfg: Config):
        self.util = util
        self.img = img
        self.txt = txt
        self.cfg = cfg

        self.hud_font = pg.font.SysFont(cfg.font, int(self.cfg.width_px / 40))
        self.pup_anim = SpriteSheetAnimation(img.powerups_marker, 40)
        self.pup_imgs = [img.shield, img.ghost, img.bomb, img.bullets]

    def draw_game(self, screen, game: Game, dt: int):
        def draw_background():
            screen.blit(self.img.background, (0, 0))

        def draw_snake_parts():
            # Draw snake parts (tail and head)
            snake_img = self.img.snake_ghost \
                if game.snake.is_ghost_on \
                else self.img.snake_normal
            for s in game.snake:
                screen.blit(snake_img, self.util.get_xy(s))
            if game.snake.head is not None:
                screen.blit(
                    rotate_image(self.img.snake_eyes,
                                 game.snake.last_direction_moved),
                    self.util.get_xy(game.snake.head))

        def draw_shielded_snake():
            # Draw shield on top of snake if has shield on
            if game.snake.is_shield_on:
                for s in game.snake:
                    screen.blit(self.img.snake_shielded, self.util.get_xy(s))

        def draw_apple():
            if game.apple is not None:
                screen.blit(self.img.apple, self.util.get_xy(game.apple))

        def draw_powerups():
            # Move powerup animation
            self.pup_anim.move(dt)

            # Draw powerups
            powerups = [game.pow_shield, game.pow_ghost,
                        game.pow_bomb, game.pow_bullets]
            for powerup, image in zip(powerups, self.pup_imgs):
                if powerup is not None:
                    screen.blit(self.pup_anim.get_sprite(),
                                self.util.get_xy(powerup))
                    screen.blit(image, self.util.get_xy(powerup))

        def draw_enemies():
            for e in game.enemies:
                screen.blit(self.img.enemy, self.util.get_xy(e))

        def draw_poisons():
            for p in game.poisons:
                screen.blit(self.img.poison, self.util.get_xy(p))

        def draw_bullets():
            for b in game.fired_bullets:
                pg.draw.circle(screen, pg.Color('Yellow'), b.coords, 4)

        def draw_hud():
            y_offset = 0

            # Draw current level
            level_text = 'Current level: {}'.format(game.level)
            level_surface = self.hud_font.render(level_text, True,
                                                 pg.Color('white'))
            screen.blit(level_surface, (0, y_offset))
            y_offset += level_surface.get_height()

            # Draw current length
            curlen_text = 'Current length: {}'.format(len(game.snake))
            curlen_surface = self.hud_font.render(curlen_text, True,
                                                  pg.Color('white'))
            screen.blit(curlen_surface, (0, y_offset))
            y_offset += curlen_surface.get_height()

            # Draw max length
            maxlen_text = 'Max length: {}'.format(game.snake.max_length_reached)
            maxlen_surface = self.hud_font.render(maxlen_text, True,
                                                  pg.Color('white'))
            screen.blit(maxlen_surface, (0, y_offset))
            y_offset += maxlen_surface.get_height()

            # Draw bullets indicator
            if game.snake.bullets > 0:
                bullets_text = 'Bullets: {}'.format(game.snake.bullets)
                bullets_surface = self.hud_font.render(bullets_text, True,
                                                       pg.Color('white'))
                screen.blit(bullets_surface, (0, y_offset))
                y_offset += bullets_surface.get_height()

            # Draw ghost indicator
            if game.snake.ghost_ms > 0:
                ghost_seconds = game.snake.ghost_ms / 1000
                ghost_text = 'Ghost: {:.1f}'.format(ghost_seconds)
                ghost_surface = self.hud_font.render(ghost_text, True,
                                                     pg.Color('white'))
                screen.blit(ghost_surface, (0, y_offset))
                y_offset += ghost_surface.get_height()

            # Draw shield indicator
            if game.snake.is_shield_on:
                shield_text = 'Shield: ON'
                shield_surface = self.hud_font.render(shield_text, True,
                                                      pg.Color('white'))
                screen.blit(shield_surface, (0, y_offset))
                y_offset += shield_surface.get_height()

        draw_background()
        draw_snake_parts()
        draw_shielded_snake()
        draw_apple()
        draw_powerups()
        draw_enemies()
        draw_poisons()
        draw_bullets()
        draw_hud()

    def draw_game_over_overlay(self, screen, alpha: int):
        # Game over image
        self.img.game_over.set_alpha(alpha)
        screen.blit(self.img.game_over, (0, 0))

        # Restart button
        screen.blit(self.txt.restart_text, self.txt.restart_text_rect)
        if self.txt.restart_text_rect.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(screen, pg.Color('White'),
                         self.txt.restart_text_rect, 2)

    def draw_paused_overlay(self, screen):
        screen.blit(self.txt.paused_text, self.txt.paused_text_rect)
