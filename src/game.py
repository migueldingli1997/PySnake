import random

import numpy as np
import pygame as pg

from snake import Snake
from util import Size2D, Direction, Util, Coords

STARTING_LEVEL = 1  # starting level
BASE_SPEED = 3  # moves/sec at level 1
ACCELERATION = 0.2  # extra moves/sec per level
SAFE_ZONE_TILES = 999  # empty tiles in front after eating apple
GHOST_TIMER_MS = 10000.0  # milliseconds
CLEAR_SKULLS_EVERY_LEVEL = False  # whether to create new skulls per level
CLEAR_POWERUPS_IF_NOT_PICKED_UP = True  # whether to clear uncollected powerups


class Game:
    def __init__(self, util: Util, game_size_tiles: Size2D):
        # Util
        self.util = util

        # Game
        self.game_size_tiles = game_size_tiles
        self.game_over = False
        self.level = STARTING_LEVEL
        self.paused = False

        # Timing
        self.base_speed = BASE_SPEED  # moves/sec at level 1 (modifiable)
        self.time_ms = 0  # milliseconds since last snake move

        # Entities
        self.snake = Snake(game_size_tiles, util)
        self.enemies = []
        self.poisons = []
        self.apple = None
        self.pow_shield = None
        self.pow_ghost = None
        self.pow_bomb = None

        # Minus enemies (due to bomb)
        self.minus_enemies = 0
        self.minus_poisons = 0

        # Audio
        self.sfx_apple = util.load_sfx('apple.wav')
        self.sfx_poison = util.load_sfx('poison.wav')
        self.sfx_powerup = util.load_sfx('powerup.wav')
        self.sfx_shield_off = util.load_sfx('shield_off.wav')

        # Generate first apple
        self.new_objects()

    @property
    def moves_per_sec(self) -> float:
        return self.base_speed + (ACCELERATION * (self.level - 1))

    @property
    def ms_per_move(self) -> float:
        return 1000 / self.moves_per_sec

    @property
    def no_of_enemies(self) -> float:
        return (self.level / 2) - self.minus_enemies

    @property
    def no_of_poisons(self) -> float:
        return (self.level - 1) - self.minus_poisons

    def should_spawn_shield(self) -> bool:
        # Coin toss on even levels > 6 if shield not on
        return self.level > 0 and self.level % 2 == 0 \
               and bool(random.getrandbits(1)) \
               and not self.snake.is_shield_on

    def should_spawn_ghost(self) -> bool:
        # Coin toss on odd levels > 10 if ghost not on
        return self.level > 10 and self.level % 2 == 1 \
               and bool(random.getrandbits(1)) \
               and not self.snake.is_ghost_on

    def should_spawn_bomb(self) -> bool:
        # Every 10n'th level for n > 1
        return self.level > 0 and self.level % 20 == 0

    def press_key(self, key: int):
        if key == pg.K_UP:
            self.snake.set_direction(Direction.UP)
        elif key == pg.K_DOWN:
            self.snake.set_direction(Direction.DOWN)
        elif key == pg.K_LEFT:
            self.snake.set_direction(Direction.LEFT)
        elif key == pg.K_RIGHT:
            self.snake.set_direction(Direction.RIGHT)
        elif key in [pg.K_ESCAPE, pg.K_SPACE]:
            self.trigger_pause()
        elif key in [pg.K_LSHIFT, pg.K_RSHIFT]:
            self.base_speed *= 3

    def release_key(self, key: int):
        if key in [pg.K_LSHIFT, pg.K_RSHIFT]:
            self.base_speed /= 3

    def trigger_pause(self):
        self.paused = not self.paused

    def get_free_tile(self, taken: np.ndarray) -> Coords:
        tile = self.util.get_random_tile_not_taken(taken)
        taken[tile[0]][tile[1]] = True
        return tile

    def new_objects(self):
        taken = np.zeros(self.game_size_tiles, dtype=bool)

        # Objects that will not change position
        for s in self.snake:
            taken[s[0]][s[1]] = True
        if not CLEAR_POWERUPS_IF_NOT_PICKED_UP:
            for powerup in [self.pow_shield, self.pow_ghost, self.pow_bomb]:
                taken[powerup[0]][powerup[1]] = powerup is not None
        if not CLEAR_SKULLS_EVERY_LEVEL:
            for e in self.enemies:
                taken[e[0]][e[1]] = True
            for p in self.poisons:
                taken[p[0]][p[1]] = True

        # Clear previous objects
        if CLEAR_POWERUPS_IF_NOT_PICKED_UP:
            self.pow_shield = self.pow_ghost = self.pow_bomb = None
        if CLEAR_SKULLS_EVERY_LEVEL:
            self.enemies.clear()
            self.poisons.clear()

        # New apple
        self.apple = self.get_free_tile(taken)

        # New shield powerup
        if self.should_spawn_shield():
            self.pow_shield = self.get_free_tile(taken)

        # New ghost powerup
        if self.should_spawn_ghost():
            self.pow_ghost = self.get_free_tile(taken)

        # New bomb powerup
        if self.should_spawn_bomb():
            self.pow_bomb = self.get_free_tile(taken)

        # Mark front of snake taken to avoid immediately hitting enemies/poison
        to_mark = self.snake.head
        for i in range(SAFE_ZONE_TILES):
            to_mark = self.util.get_next_tile(to_mark, self.snake.direction)
            taken[to_mark[0]][to_mark[1]] = True

        # Match enemies list with expected number of enemies
        while len(self.enemies) < int(self.no_of_enemies):
            self.enemies += [self.get_free_tile(taken)]
        while len(self.enemies) > int(self.no_of_enemies):
            self.enemies = self.enemies[:-1]

        # Match poisons list with expected number of poisons
        while len(self.poisons) < int(self.no_of_poisons):
            self.poisons += [self.get_free_tile(taken)]
        while len(self.poisons) > int(self.no_of_poisons):
            self.poisons = self.poisons[:-1]

    def check_hits(self):
        # Check if hit itself, apple, power-ups
        head = self.snake.head
        if head in self.snake.tail and not self.snake.is_ghost_on:
            self.game_over = True
        elif head == self.apple:
            self.level += 1
            self.snake.grow_by_one()
            self.new_objects()
            self.sfx_apple.play()
        elif head == self.pow_shield:
            self.snake.set_shield(True)
            self.pow_shield = None
            self.sfx_powerup.play()
        elif head == self.pow_ghost:
            self.snake.set_ghost(GHOST_TIMER_MS)
            self.pow_ghost = None
            self.sfx_powerup.play()
        elif head == self.pow_bomb:
            self.minus_enemies += self.no_of_enemies
            self.minus_poisons += self.no_of_poisons
            self.enemies.clear()
            self.poisons.clear()
            self.pow_shield = self.pow_ghost = self.pow_bomb = None
            self.sfx_powerup.play()

        # Check if hit enemy
        if not self.snake.is_ghost_on:
            try:
                self.enemies.remove(next(e for e in self.enemies if e == head))
                if self.snake.is_shield_on:
                    self.snake.set_shield(False)
                    self.sfx_shield_off.play()
                else:
                    self.game_over = True
            except StopIteration:
                pass

        # Check if hit poison
        if not self.snake.is_ghost_on:
            try:
                self.poisons.remove(next(e for e in self.poisons if e == head))
                if self.snake.is_shield_on:
                    self.snake.set_shield(False)
                    self.sfx_shield_off.play()
                else:
                    self.snake.shrink(1)
                    if len(self.snake) < 1:
                        self.game_over = True
                    else:
                        self.sfx_poison.play()
            except StopIteration:
                pass

    def move(self, dt: int):
        self.time_ms += dt

        # Return if not enough time elapsed for at least one move
        if self.time_ms < self.ms_per_move:
            return

        # FPS-independent moves (loop just in case game needs to catch up)
        while self.time_ms > self.ms_per_move:
            # Single move consumes single time chunk
            self.time_ms -= self.ms_per_move

            # Move snake
            self.snake.move(self.ms_per_move)

        # Check if hit something
        self.check_hits()