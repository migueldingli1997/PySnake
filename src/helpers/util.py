import random
from typing import List, Tuple, Optional

import numpy as np
import pygame as pg
from pygame.mixer import Sound
from pygame.surface import Surface

from helpers.direction import Direction

Size2D = Tuple[int, int]
Coords = Tuple[int, int]
CoordsList = List[Coords]


def user_quit(event) -> bool:
    pressed = pg.key.get_pressed()
    alt_f4 = event.type == pg.KEYDOWN and event.key == pg.K_F4 \
             and (pressed[pg.K_LALT] or pressed[pg.K_LALT])
    return event.type == pg.QUIT or alt_f4


def get_next_xy(coords: Coords, direction: Direction, px: int = 1) -> Coords:
    x = coords[0]
    y = coords[1]

    if direction == Direction.UP:
        return x, y - px
    elif direction == Direction.DOWN:
        return x, y + px
    elif direction == Direction.LEFT:
        return x - px, y
    elif direction == Direction.RIGHT:
        return x + px, y
    else:
        raise NotImplementedError


class Util:

    def __init__(self, game_size_pixels: Size2D, game_size_tiles: Size2D,
                 img_folder: str, sfx_folder: str):
        self.width = game_size_pixels[0]
        self.height = game_size_pixels[1]

        self.tiles_x = game_size_tiles[0]
        self.tiles_y = game_size_tiles[1]

        self.tile_width = self.width / self.tiles_x
        self.tile_height = self.height / self.tiles_y

        self.img = str(self.width) + '.png'
        self.img_folder = img_folder
        self.sfx_folder = sfx_folder

    def get_img_path(self, folder: str) -> str:
        return self.img_folder + folder + self.img

    def get_sfx_path(self, file: str) -> str:
        return self.sfx_folder + file

    def load_img(self, img: str) -> Surface:
        return pg.image.load(self.get_img_path(img))

    def load_sfx(self, sfx: str, as_music: bool = False) -> Optional[Sound]:
        if as_music:
            pg.mixer.music.load(self.get_sfx_path(sfx))
            return None
        else:
            return pg.mixer.Sound(self.get_sfx_path(sfx))

    def get_xy(self, tile: Coords) -> Coords:
        adjusted_x = tile[0] * self.tile_width
        adjusted_y = tile[1] * self.tile_height
        return int(adjusted_x), int(adjusted_y)

    def get_xy_center(self, tile: Coords) -> Coords:
        adjusted_x = (tile[0] * self.tile_width) + (self.tile_width / 2)
        adjusted_y = (tile[1] * self.tile_height) + (self.tile_height / 2)
        return int(adjusted_x), int(adjusted_y)

    def is_xy_out_of_screen(self, xy: Coords) -> bool:
        return xy[0] < 0 or xy[0] > self.width or \
               xy[1] < 0 or xy[1] > self.height

    def get_xy_tile(self, xy: Coords) -> Coords:
        return int(xy[0] / self.tile_width), \
               int(xy[1] / self.tile_height)

    def get_random_tile(self) -> Coords:
        return (random.randint(0, self.tiles_x - 1),
                random.randint(0, self.tiles_y - 1))

    def get_random_tile_not_taken(self, taken: np.ndarray) -> Coords:
        while True:
            tile = self.get_random_tile()
            if not taken[tile[0]][tile[1]]:
                return tile

    def dir_to_ang(self, dir: Direction) -> int:
        return {
            Direction.UP: 0,
            Direction.LEFT: 90,
            Direction.DOWN: 180,
            Direction.RIGHT: 270,
        }[dir]

    def rotate_image(self, image: Surface, direction: Direction) -> Surface:
        # Zero-rotation direction assumed to be UP
        return pg.transform.rotate(image, self.dir_to_ang(direction))

    def get_next_tile(self, coords: Coords, direction: Direction) -> Coords:
        x = coords[0]
        y = coords[1]

        if direction == Direction.UP:
            newX = x
            newY = (y + (self.tiles_y - 1)) % self.tiles_y
        elif direction == Direction.DOWN:
            newX = x
            newY = (y + 1) % self.tiles_y
        elif direction == Direction.LEFT:
            newX = (x + (self.tiles_x - 1)) % self.tiles_x
            newY = y
        elif direction == Direction.RIGHT:
            newX = (x + 1) % self.tiles_x
            newY = y
        else:
            raise NotImplementedError

        return newX, newY
