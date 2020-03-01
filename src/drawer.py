from src.game import Game
from src.helpers.anim import SpriteSheetAnimation
from src.helpers.colours import *
from src.helpers.config import Config
from src.helpers.img import ImgHolder
from src.helpers.text import Text
from src.helpers.util import rotate_image, Util
from src.snake import Snake


class Drawer:
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
            screen.fill(BLACK)
            screen.blit(self.img.background, (0, 0))

        def draw_snake_parts(snake: Snake):
            # Draw snake parts (tail and head)
            snake_img = self.img.snake_ghost \
                if snake.is_ghost_on \
                else self.img.snake_normal
            for s in snake:
                screen.blit(snake_img, self.util.get_xy(s))
            if snake.head is not None:
                screen.blit(
                    rotate_image(self.img.snake_eyes,
                                 snake.last_direction_moved),
                    self.util.get_xy(snake.head))

        def draw_shielded_snake(snake: Snake):
            # Draw shield on top of snake if has shield on
            if snake.is_shield_on:
                for s in snake:
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
                pg.draw.circle(screen, YELLOW, b.coords, 4)

        def draw_hud(snake: Snake, y_offset: int = 0) -> int:
            # Draw current level
            level_text = '({}) Current level: {}'.format(
                snake.player.name, game.level)
            level_surface = self.hud_font.render(level_text, True, WHITE)
            screen.blit(level_surface, (self.cfg.width_px, y_offset))
            y_offset += level_surface.get_height()

            # Draw current length
            curlen_text = '({}) Current length: {}'.format(
                snake.player.name, len(snake))
            curlen_surface = self.hud_font.render(curlen_text, True, WHITE)
            screen.blit(curlen_surface, (self.cfg.width_px, y_offset))
            y_offset += curlen_surface.get_height()

            # Draw max length
            maxlen_text = '({}) Max length: {}'.format(
                snake.player.name, snake.max_length_reached)
            maxlen_surface = self.hud_font.render(maxlen_text, True, WHITE)
            screen.blit(maxlen_surface, (self.cfg.width_px, y_offset))
            y_offset += maxlen_surface.get_height()

            # Draw bullets indicator
            if snake.bullets > 0:
                bullets_text = '({}) Bullets: {}'.format(
                    snake.player.name, snake.bullets)
                bullets_surface = self.hud_font.render(bullets_text, True,
                                                       WHITE)
                screen.blit(bullets_surface, (self.cfg.width_px, y_offset))
                y_offset += bullets_surface.get_height()

            # Draw ghost indicator
            if snake.ghost_ms > 0:
                ghost_seconds = snake.ghost_ms / 1000
                ghost_text = '({}) Ghost: {:.1f}'.format(
                    snake.player.name, ghost_seconds)
                ghost_surface = self.hud_font.render(ghost_text, True, WHITE)
                screen.blit(ghost_surface, (self.cfg.width_px, y_offset))
                y_offset += ghost_surface.get_height()

            # Draw shield indicator
            if snake.is_shield_on:
                shield_text = '({}) Shield: ON'.format(snake.player.name)
                shield_surface = self.hud_font.render(shield_text, True, WHITE)
                screen.blit(shield_surface, (self.cfg.width_px, y_offset))
                y_offset += shield_surface.get_height()

            return y_offset

        draw_background()

        for s in game.live_snakes:
            draw_snake_parts(s)
            draw_shielded_snake(s)

        draw_apple()
        draw_powerups()
        draw_enemies()
        draw_poisons()
        draw_bullets()

        hud_y_offset = 0
        for s in game.live_snakes:
            hud_y_offset = draw_hud(s, hud_y_offset)

    def draw_game_over_overlay(self, screen, alpha: int, score_saved: bool):
        # Game over image
        self.img.game_over.set_alpha(alpha)
        screen.blit(self.img.game_over, (0, 0))

        # Restart button
        screen.blit(self.txt.restart, self.txt.restart_rect)
        if self.txt.restart_rect.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(screen, WHITE, self.txt.restart_rect, 2)

        # Save score button (or score saved text if score saved)
        if not score_saved:
            screen.blit(self.txt.save_score, self.txt.save_score_rect)
            if self.txt.save_score_rect.collidepoint(pg.mouse.get_pos()):
                pg.draw.rect(screen, WHITE, self.txt.save_score_rect, 2)
        else:
            screen.blit(self.txt.score_saved, self.txt.score_saved_rect)

    def draw_paused_overlay(self, screen):
        screen.blit(self.txt.paused, self.txt.paused_rect)

    def draw_fps(self, screen, fps: float):
        fps_surface = self.hud_font.render(str(int(fps)), True, YELLOW)
        screen.blit(fps_surface, (0, 0))
