from typing import Optional, Iterator

from src.helpers.config import Player
from src.helpers.util import Direction, Coords, CoordsList, Size2D, Util

STARTING_LENGTH = 3  # Starting length
RAND_NAME = "_rand_name_"


class Snake:

    def __init__(self, game_size_tiles: Size2D, util: Util,
                 player: Player):
        self.tiles_x = game_size_tiles[0]
        self.tiles_y = game_size_tiles[1]
        self.util = util
        self.player = player

        self.direction = Direction.RIGHT
        self.last_direction_moved = self.direction
        self.is_shield_on = False
        self.ghost_ms = 0.0
        self.bullets = 0

        self.coords = []
        for _ in range(STARTING_LENGTH):
            self.coords += [(0, 0)]
        self.max_length_reached = len(self.coords)

        self.alive = True

    def __contains__(self, item):
        return item in self.coords

    def __len__(self) -> int:
        return len(self.coords)

    def __iter__(self) -> Iterator[Coords]:
        return iter(self.coords)

    @property
    def head(self) -> Optional[Coords]:
        if len(self) > 0:
            return self.coords[0]
        else:
            return None

    @property
    def tail(self) -> CoordsList:
        if len(self) > 1:
            return self.coords[1:]
        else:
            return []

    @property
    def is_ghost_on(self) -> bool:
        return self.ghost_ms > 0

    @property
    def has_bullets(self) -> bool:
        return self.bullets > 0

    def set_direction(self, new_dir: Direction) -> bool:
        # e.g. If new direction is UP, cannot have just moved DOWN
        illegal = [
            (Direction.UP, Direction.DOWN),
            (Direction.DOWN, Direction.UP),
            (Direction.LEFT, Direction.RIGHT),
            (Direction.RIGHT, Direction.LEFT),
        ]
        if new_dir == self.last_direction_moved or \
                (new_dir, self.last_direction_moved) in illegal:
            return False
        else:
            self.direction = new_dir
            return True

    def shrink(self, count: int) -> None:
        self.coords = self.coords[:len(self.coords) - count]

    def grow_by_one(self):
        self.coords += [self.coords[-1]]
        if len(self.coords) > self.max_length_reached:
            self.max_length_reached = len(self.coords)

    def set_shield(self, shield: bool) -> None:
        self.is_shield_on = shield

    def set_ghost(self, ghost_ms: float) -> None:
        self.ghost_ms = ghost_ms

    def add_bullets(self, bullets: int) -> None:
        self.bullets += bullets

    def use_bullet(self) -> None:
        self.bullets -= 1

    def move(self):
        # New head
        newHead = self.util.get_next_tile(self.head, self.direction)

        # Add new head and remove old tip
        self.coords = [newHead] + self.coords[:-1]

        # Last direction moved
        self.last_direction_moved = self.direction

    def move_time(self, dt: float):
        # Deduct time from ghost powerup
        if self.is_ghost_on:
            self.ghost_ms = max(0, self.ghost_ms - dt)

    def is_alive(self) -> bool:
        return self.alive

    def kill(self) -> None:
        self.alive = False
