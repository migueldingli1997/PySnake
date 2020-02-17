from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def direction_to_angle(dir: Direction) -> int:
    return {
        Direction.UP: 0,
        Direction.LEFT: 90,
        Direction.DOWN: 180,
        Direction.RIGHT: 270,
    }[dir]
