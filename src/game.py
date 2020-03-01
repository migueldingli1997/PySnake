import random
from datetime import datetime
from typing import List

import numpy as np

from src.helpers.config import Config
from src.helpers.score import Score
from src.helpers.sfx import SfxHolder
from src.helpers.util import Size2D, Direction, Util, Coords
from src.projectile import Bullet
from src.snake import Snake

STARTING_LEVEL = 1  # starting level
BASE_SPEED = 3  # moves/sec at level 1
SPEED_BOOST = 2 * BASE_SPEED  # extra moves/sec when boost button pressed
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

        # Snakes
        initial_speed = self.get_moves_per_ms_by_level()
        self.live_snakes = []
        for p in cfg.players:
            self.live_snakes.append(
                Snake(game_size_tiles, util, p, initial_speed))
        self.all_snakes = self.live_snakes  # backup list of all snakes

        # If multiple snakes, make ghosts so that they don't immediately collide
        for s in self.live_snakes:
            s.set_ghost(GHOST_TIMER_MS)

        # Enemies, apple, powerups, bullets
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

    def get_moves_per_ms_by_level(self) -> float:
        moves_per_sec = BASE_SPEED + (ACCELERATION * (self.level - 1))
        return moves_per_sec / 1000

    def update_snakes_moves_per_ms(self) -> None:
        ms_per_move = self.get_moves_per_ms_by_level()
        for s in self.live_snakes:
            s.set_base_moves_per_ms(ms_per_move)

    @property
    def no_of_enemies(self) -> float:
        return (self.level / 2) - self.minus_enemies

    @property
    def no_of_poisons(self) -> float:
        return (self.level - 1) - self.minus_poisons

    def get_scores(self) -> List[Score]:
        timestamp = datetime.now()
        return [Score(snake.player.name, snake.max_length_reached,
                      self.level, timestamp) for snake in self.all_snakes]

    def should_spawn_shield(self) -> bool:
        # Coin toss on even levels > 6 if shield not on
        return self.level > 0 and self.level % 2 == 0 \
               and bool(random.getrandbits(1))

    def should_spawn_ghost(self) -> bool:
        # Coin toss on odd levels > 10 if ghost not on
        return self.level > 10 and self.level % 2 == 1 \
               and bool(random.getrandbits(1))

    def should_spawn_bomb(self) -> bool:
        # Every 20n'th level for n >= 1
        return self.level > 0 and self.level % 20 == 0

    def should_spawn_bullets(self) -> bool:
        # Every 10n'th level for n >= 1
        return self.level > 0 and self.level % 10 == 0

    def press_key(self, key: int):  # TODO: investigate how to optimise
        for s in self.live_snakes:
            if key not in s.player.all_keys:
                continue
            if key in s.player.ctrl_up:
                s.set_direction(Direction.UP)
            elif key in s.player.ctrl_down:
                s.set_direction(Direction.DOWN)
            elif key in s.player.ctrl_left:
                s.set_direction(Direction.LEFT)
            elif key in s.player.ctrl_right:
                s.set_direction(Direction.RIGHT)
            elif key in s.player.ctrl_pause:
                self.trigger_pause()
            elif key in s.player.ctrl_boost:
                s.set_boost_moves_per_ms(SPEED_BOOST / 1000)
            elif key in s.player.ctrl_shoot and s.has_bullets:
                s.use_bullet()
                self.fired_bullets.append(
                    Bullet(self.util.get_xy_center(s.head),
                           s.last_direction_moved, self.util))

    def release_key(self, key: int):
        for s in self.live_snakes:
            if key in s.player.ctrl_boost:
                s.set_boost_moves_per_ms(0)

    def trigger_pause(self):
        self.paused = not self.paused

    def get_free_tile(self, taken: np.ndarray) -> Coords:
        tile = self.util.get_random_tile_not_taken(taken)
        taken[tile[0]][tile[1]] = True
        return tile

    def new_objects(self):
        taken = np.zeros(self.game_size_tiles, dtype=bool)

        # Objects that will not change position
        for snake in self.live_snakes:
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
        for snake in self.live_snakes:
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

    def check_snake_hits(self, snake: Snake, other_snakes: List[Snake]):
        # Check if hit itself, apple, power-ups
        head = snake.head
        if head in snake.tail and not snake.is_ghost_on:
            snake.kill()
            return
        elif head == self.apple:
            self.level += 1
            snake.grow_by_one()
            self.update_snakes_moves_per_ms()
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

        # Check if hit other snake
        if not snake.is_ghost_on:
            for s in other_snakes:
                if head in s:
                    snake.kill()
                    return

        # Check if hit enemy
        if not snake.is_ghost_on:
            try:
                self.enemies.remove(next(e for e in self.enemies if e == head))
                if snake.is_shield_on:
                    snake.set_shield(False)
                    self.sfx.shield_off.play()
                else:
                    snake.kill()
                    return
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
                        snake.kill()
                        return
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
        # Progress snakes' time and move
        any_snake_moved = False
        for s in self.live_snakes:
            s.move_time(dt)
            if s.can_move():
                s.move()
                any_snake_moved = True

        # Once any snakes moved, if any, check hits
        if any_snake_moved:
            # Check if snake hit something
            for i, snake in enumerate(self.live_snakes):
                other_snakes = self.live_snakes[0:i] + \
                               self.live_snakes[i + 1:len(self.live_snakes)]
                self.check_snake_hits(snake, other_snakes)

            # Exclude any dead snakes from game
            before = len(self.live_snakes)
            self.live_snakes = [s for s in self.live_snakes if s.is_alive()]
            after = len(self.live_snakes)

            # Game over if no more snakes; sound effect if snake died
            if len(self.live_snakes) == 0:
                self.game_over = True
            elif after < before:
                self.sfx.snake_death.play()

        # Remove bullets if out of screen
        bullets_to_remove = [b for b in self.fired_bullets
                             if self.util.is_xy_out_of_screen(b.coords)]
        for b in bullets_to_remove:
            self.fired_bullets.remove(b)

        # Move bullets
        for b in self.fired_bullets:
            b.move()

        # Check if bullets hit something
        for snake in self.live_snakes:
            self.check_bullet_hits(snake)
