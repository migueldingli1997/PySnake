import random
from datetime import datetime

import numpy as np

from helpers.config import Config
from helpers.score import Score
from helpers.sfx import SfxHolder
from helpers.util import Size2D, Direction, Util, Coords
from projectile import Bullet
from snake import Snake

STARTING_LEVEL = 1  # starting level
BASE_SPEED = 3  # moves/sec at level 1
BOOST_MULTIPLIER = 3  # multiplier when boost button pressed
ACCELERATION = 0.2  # extra moves/sec per level
SAFE_ZONE_TILES = 999  # empty tiles in front after eating apple
GHOST_TIMER_MS = 10000.0  # milliseconds
INIT_NO_OF_BULLETS = 10  # initial number of bullets after picking up powerup
CLEAR_SKULLS_EVERY_LEVEL = False  # whether to create new skulls per level
CLEAR_POWERUPS_IF_NOT_PICKED_UP = True  # whether to clear uncollected powerups


class Game:
    def __init__(self, util: Util, cfg: Config, sfx: SfxHolder,
                 game_size_tiles: Size2D):
        self.util = util
        self.cfg = cfg
        self.sfx = sfx

        # Game
        self.game_size_tiles = game_size_tiles
        self.game_over = False
        self.level = STARTING_LEVEL
        self.paused = False

        # Timing
        self.base_speed = BASE_SPEED  # moves/sec at level 1 (modifiable)
        self.time_ms = 0  # milliseconds since last snake move

        # Entities
        self.snakes = [Snake(game_size_tiles, util),
                       Snake(game_size_tiles, util),
                       Snake(game_size_tiles, util),
                       Snake(game_size_tiles, util),
                       Snake(game_size_tiles, util)]
        # TODO: configurable number of snakes
        self.enemies = []
        self.poisons = []
        self.apple = None
        self.pow_shield = None
        self.pow_ghost = None
        self.pow_bomb = None
        self.pow_bullets = None
        self.fired_bullets = []

        # Minus enemies (due to bomb)
        self.minus_enemies = 0
        self.minus_poisons = 0

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

    def get_score(self) -> Score:
        snake = self.snakes[0]  # TODO: consider for each snake
        return Score(
            self.cfg.player_name, snake.max_length_reached,
            self.level, datetime.now())

    def should_spawn_shield(self) -> bool:
        snake = self.snakes[0]  # TODO: consider all snakes or none at all
        # Coin toss on even levels > 6 if shield not on
        return self.level > 0 and self.level % 2 == 0 \
               and bool(random.getrandbits(1)) \
               and not snake.is_shield_on

    def should_spawn_ghost(self) -> bool:
        snake = self.snakes[0]  # TODO: consider all snakes or none at all
        # Coin toss on odd levels > 10 if ghost not on
        return self.level > 10 and self.level % 2 == 1 \
               and bool(random.getrandbits(1)) \
               and not snake.is_ghost_on

    def should_spawn_bomb(self) -> bool:
        # Every 20n'th level for n >= 1
        return self.level > 0 and self.level % 20 == 0

    def should_spawn_bullets(self) -> bool:
        # Every 10n'th level for n >= 1
        return self.level > 0 and self.level % 10 == 0

    def press_key(self, key: int):
        snake = self.snakes[0]  # TODO: consider for each snake
        if key in self.cfg.ctrl_up:
            snake.set_direction(Direction.UP)
        elif key in self.cfg.ctrl_down:
            snake.set_direction(Direction.DOWN)
        elif key in self.cfg.ctrl_left:
            snake.set_direction(Direction.LEFT)
        elif key in self.cfg.ctrl_right:
            snake.set_direction(Direction.RIGHT)
        elif key in self.cfg.ctrl_pause:
            self.trigger_pause()
        elif key in self.cfg.ctrl_boost:
            self.base_speed *= BOOST_MULTIPLIER
        elif key in self.cfg.ctrl_shoot and snake.has_bullets:
            snake.use_bullet()
            self.fired_bullets.append(
                Bullet(self.util.get_xy_center(snake.head),
                       snake.last_direction_moved, self.util))

    def release_key(self, key: int):
        if key in self.cfg.ctrl_boost:
            self.base_speed /= BOOST_MULTIPLIER

    def trigger_pause(self):
        self.paused = not self.paused

    def get_free_tile(self, taken: np.ndarray) -> Coords:
        tile = self.util.get_random_tile_not_taken(taken)
        taken[tile[0]][tile[1]] = True
        return tile

    def new_objects(self):
        taken = np.zeros(self.game_size_tiles, dtype=bool)

        # Objects that will not change position
        for snake in self.snakes:
            for s in snake:
                taken[s[0]][s[1]] = True
        if not CLEAR_POWERUPS_IF_NOT_PICKED_UP:
            for powerup in [self.pow_shield, self.pow_ghost,
                            self.pow_bomb, self.pow_bullets]:
                # Set to taken if powerup is not none
                taken[powerup[0]][powerup[1]] = powerup is not None
        if not CLEAR_SKULLS_EVERY_LEVEL:
            for e in self.enemies:
                taken[e[0]][e[1]] = True
            for p in self.poisons:
                taken[p[0]][p[1]] = True

        # Clear previous objects
        if CLEAR_POWERUPS_IF_NOT_PICKED_UP:
            self.pow_shield = self.pow_ghost = \
                self.pow_bomb = self.pow_bullets = None
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

        # New bullets powerup
        if self.should_spawn_bullets():
            self.pow_bullets = self.get_free_tile(taken)

        # Mark front of snake taken to avoid immediately hitting enemies/poison
        for snake in self.snakes:
            to_mark = snake.head
            for i in range(SAFE_ZONE_TILES):
                to_mark = self.util.get_next_tile(to_mark, snake.direction)
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

    def check_snake_hits(self, snake: Snake):
        # Check if hit itself, apple, power-ups
        head = snake.head
        if head in snake.tail and not snake.is_ghost_on:
            self.game_over = True
        elif head == self.apple:
            self.level += 1
            snake.grow_by_one()
            self.new_objects()
            self.sfx.apple.play()
        elif head == self.pow_shield:
            snake.set_shield(True)
            self.pow_shield = None
            self.sfx.powerup.play()
        elif head == self.pow_ghost:
            snake.set_ghost(GHOST_TIMER_MS)
            self.pow_ghost = None
            self.sfx.powerup.play()
        elif head == self.pow_bomb:
            self.minus_enemies += self.no_of_enemies
            self.minus_poisons += self.no_of_poisons
            self.enemies.clear()
            self.poisons.clear()
            self.pow_shield = self.pow_ghost = self.pow_bomb = None
            self.sfx.powerup.play()
        elif head == self.pow_bullets:
            snake.add_bullets(INIT_NO_OF_BULLETS)
            self.pow_bullets = None
            self.sfx.powerup.play()

        # Check if hit enemy
        if not snake.is_ghost_on:
            try:
                self.enemies.remove(next(e for e in self.enemies if e == head))
                if snake.is_shield_on:
                    snake.set_shield(False)
                    self.sfx.shield_off.play()
                else:
                    self.game_over = True
            except StopIteration:
                pass

        # Check if hit poison
        if not snake.is_ghost_on:
            try:
                self.poisons.remove(next(e for e in self.poisons if e == head))
                if snake.is_shield_on:
                    snake.set_shield(False)
                    self.sfx.shield_off.play()
                else:
                    snake.shrink(1)
                    if len(snake) < 1:
                        self.game_over = True
                    else:
                        self.sfx.poison.play()
            except StopIteration:
                pass

    def check_bullet_hits(self, snake: Snake):
        # Check if bullets hit an enemy, poison, or snake
        hits = []
        for b in self.fired_bullets:
            bullet_tile = self.util.get_xy_tile(b.coords)
            if bullet_tile in self.enemies:
                hits.append(b)
                self.enemies.remove(bullet_tile)
                self.minus_enemies += 1
                self.sfx.bullet_hit_skull.play()
            elif bullet_tile in self.poisons:
                hits.append(b)
                self.poisons.remove(bullet_tile)
                self.minus_poisons += 1
                self.sfx.bullet_hit_skull.play()
            elif bullet_tile in snake.coords \
                    and bullet_tile != snake.head:
                hits.append(b)
                if snake.is_shield_on:
                    snake.set_shield(False)
                    self.sfx.shield_off.play()
                else:
                    snake.shrink(1)
                    self.sfx.bullet_hit_snake.play()

        # Hits means bullet can be removed
        for h in hits:
            self.fired_bullets.remove(h)

    def move(self, dt: int):
        self.time_ms += dt

        # Move snake if enough time elapsed for at least one move
        if self.time_ms >= self.ms_per_move:
            # FPS-independent moves (loop just in case game needs to catch up)
            while self.time_ms > self.ms_per_move:
                # Single move consumes single time chunk
                self.time_ms -= self.ms_per_move

                # Move snake
                for snake in self.snakes:
                    snake.move(self.ms_per_move)

            # Check if snake hit something
            for snake in self.snakes:
                self.check_snake_hits(snake)

        # Remove bullets if out of screen
        bullets_to_remove = [b for b in self.fired_bullets
                             if self.util.is_xy_out_of_screen(b.coords)]
        for b in bullets_to_remove:
            self.fired_bullets.remove(b)

        # Move bullets
        for b in self.fired_bullets:
            b.move(dt)

        # Check if bullets hit something
        for snake in self.snakes:
            self.check_bullet_hits(snake)
