import configparser
from typing import Tuple

import pygame as pg
from pygame.time import Clock

from anim import Animation
from game import Game
from util import Util, user_quit

TILES_X = 30
TILES_Y = 30

GAME_TITLE = 'PySnake'
GAME_ICON = 'img/icon.png'
IMG_FOLDER = 'img/'
SFX_FOLDER = 'sfx/'

# Keys
GAME_KEYS = [
    pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT,  # snake control
    pg.K_ESCAPE, pg.K_SPACE,  # pause
    pg.K_LSHIFT, pg.K_RSHIFT  # boost
]


def draw_game(screen, game: Game, dt: int):
    # Background
    screen.blit(BG_IMG, (0, 0))

    # Draw snake parts (tail and head)
    snake_img = SNAKE_GHOST_IMG if game.snake.is_ghost_on else SNAKE_NORMAL_IMG
    for s in game.snake:
        screen.blit(snake_img, UTIL.get_xy(s))
    if game.snake.head is not None:
        screen.blit(
            UTIL.rotate_image(SNAKE_EYES_IMG, game.snake.last_direction_moved),
            UTIL.get_xy(game.snake.head))

    # Draw shield on top of snake if has shield on
    if game.snake.is_shield_on:
        for s in game.snake:
            screen.blit(SNAKE_SHIELDED_IMG, UTIL.get_xy(s))

    # Draw apple
    if game.apple is not None:
        screen.blit(APPLE_IMG, UTIL.get_xy(game.apple))

    # Draw powerups
    PUP_ANIM.move(dt)
    powerups = [game.pow_shield, game.pow_ghost, game.pow_bomb]
    for powerup, image in zip(powerups, POWERUP_IMGS):
        if powerup is not None:
            screen.blit(PUP_ANIM.get_sprite(), UTIL.get_xy(powerup))
            screen.blit(image, UTIL.get_xy(powerup))

    # Draw enemies
    for e in game.enemies:
        screen.blit(ENEMY_IMG, UTIL.get_xy(e))

    # Draw poisons
    for p in game.poisons:
        screen.blit(POISON_IMG, UTIL.get_xy(p))

    # Draw score
    score_font = pg.font.SysFont('arial', int(WIDTH / 40))
    score_text = 'Max length: {}'.format(game.snake.max_length_reached)
    score_surface = score_font.render(score_text, True, pg.Color('white'))
    screen.blit(score_surface, (0, 0))


def main() -> bool:
    # Dump first tick to ignore past
    clock.tick(FPS)

    running = True
    while running:
        # Get change in time
        dt = clock.tick(FPS)

        # Loop over events
        for event in pg.event.get():
            if user_quit(event):
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in GAME_KEYS:
                    game.press_key(event.key)
            elif event.type == pg.KEYUP:
                if event.key in GAME_KEYS:
                    game.release_key(event.key)

        if not game.paused:
            # Move and draw game
            game.move(dt)
            if not game.game_over:
                draw_game(screen, game, dt)
        else:
            screen.blit(paused_text, paused_text_rect)

        # Update display
        pg.display.update()

        # Break if game no longer running
        if game.game_over:
            break

    # False if user closed the game
    return running


def game_over() -> Tuple[bool, bool]:
    running, restart = True, False

    # Audio
    pg.mixer.music.play(0)

    # Fade-in game over screen
    for i in range(255):
        pg.event.get()  # dummy get
        draw_game(screen, game, 0)  # draw game

        # Fade-in game over screen
        GAME_OVER_IMG.set_alpha(i)
        screen.blit(GAME_OVER_IMG, (0, 0))
        clock.tick(60)

        # Restart button
        screen.blit(restart_text, restart_text_rect)

        # Refresh screen
        pg.display.flip()

        for event in pg.event.get():
            if user_quit(event):
                running = False
                break
            elif event.type == pg.MOUSEBUTTONDOWN:
                if restart_text_rect.collidepoint(*event.pos):
                    restart = True
                    break
        if not running or restart:
            break

    # False if user closed the game
    return running, restart


if __name__ == '__main__':
    # Read config
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    FULL_SCREEN = True if cfg['general']['full_screen'] == 'True' else False
    WIDTH = HEIGHT = int(cfg['general']['window_size'])
    FPS = int(cfg['general']['frames_per_second'])

    # Util class
    UTIL = Util((WIDTH, HEIGHT), (TILES_X, TILES_Y), IMG_FOLDER, SFX_FOLDER)

    # Images
    APPLE_IMG = UTIL.load_img('apple/')
    BG_IMG = UTIL.load_img('background/')
    ENEMY_IMG = UTIL.load_img('skulls/enemy/')
    POISON_IMG = UTIL.load_img('skulls/poison/')
    SHIELD_IMG = UTIL.load_img('powerups/shield/')
    GHOST_IMG = UTIL.load_img('powerups/ghost/')
    BOMB_IMG = UTIL.load_img('powerups/bomb/')
    SNAKE_NORMAL_IMG = UTIL.load_img('snake/snake/')
    SNAKE_EYES_IMG = UTIL.load_img('snake/eyes/')
    SNAKE_GHOST_IMG = UTIL.load_img('snake/ghost/')
    SNAKE_SHIELDED_IMG = UTIL.load_img('snake/shielded/')
    GAME_OVER_IMG = UTIL.load_img('theEnd/')

    # Powerup marker animation
    PUP_ANIM = Animation(UTIL.load_img('powerups/marker/'), 40)

    # Helpers
    POWERUP_IMGS = [SHIELD_IMG, GHOST_IMG, BOMB_IMG]

    # Initialise all imported pygame modules and clock
    pg.mixer.pre_init(44100, -16, 2, 1024)
    pg.init()
    clock = Clock()

    # Text
    paused_font = pg.font.SysFont('arial', int(WIDTH / 20))
    paused_text = paused_font.render('PAUSED', True, pg.Color('white'))
    paused_text_rect = paused_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    restart_font = pg.font.SysFont('arial', int(WIDTH / 30))
    restart_text = restart_font.render('Restart ', True, pg.Color('white'))
    restart_text_rect = restart_text.get_rect()
    restart_text_rect.top = HEIGHT - restart_text_rect.height
    restart_text_rect.left = WIDTH - restart_text_rect.width

    # Sound
    UTIL.load_sfx('endgame.wav', as_music=True)

    # Title and icon
    icon = pg.image.load(GAME_ICON)
    pg.display.set_caption(GAME_TITLE)
    pg.display.set_icon(icon)

    # Create screen
    screen: pg.Surface = pg.display.set_mode(
        (WIDTH, HEIGHT), pg.FULLSCREEN if FULL_SCREEN else 0)

    # Finishing touches
    GAME_OVER_IMG = GAME_OVER_IMG.convert()

    running = True
    while running:
        # Create and run game
        game = Game(UTIL, (TILES_X, TILES_Y))
        running = main()  # runs game loop
        restart = False

        # Game over sequence (if game still running)
        if running:
            running, restart = game_over()

        # Restart game
        if running and restart:
            continue

        # Wait till user quits or restarts (if game still running)
        while running and not restart:
            for event in pg.event.get():
                if user_quit(event):
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if restart_text_rect.collidepoint(*event.pos):
                        restart = True
