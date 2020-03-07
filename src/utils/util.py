import random
from typing import List, Tuple, Optional

import numpy as np
import pygame as pg
from pygame.mixer import Sound
from pygame.surface import Surface

from src.utils.direction import Direction, direction_to_angle

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


def rotate_image(image: Surface, direction: Direction) -> Surface:
    # Zero-rotation direction assumed to be UP
    return pg.transform.rotate(image, direction_to_angle(direction))


class Util:

    def __init__(self, game_size_pixels: Size2D, game_size_tiles: Size2D,
                 img_folder: str, sfx_folder: str):
        self.width_px = game_size_pixels[0]
        self.height_px = game_size_pixels[1]
        self.center_px = int(self.width_px / 2), int(self.height_px / 2)

        self.tiles_x = game_size_tiles[0]
        self.tiles_y = game_size_tiles[1]

        self.tile_width_px = self.width_px / self.tiles_x
        self.tile_height_px = self.height_px / self.tiles_y

        self.width_img_name = str(self.width_px) + '.png'
        self.img_folder = img_folder
        self.sfx_folder = sfx_folder

    def get_sfx_path(self, file: str) -> str:
        return self.sfx_folder + file

    def load_img(self, img_path: str) -> Surface:
        return pg.image.load(self.img_folder + img_path)

    def load_img_from_folder(self, folder: str) -> Surface:
        return pg.image.load(self.img_folder + folder + self.width_img_name)

    def load_sfx(self, sfx: str, as_music: bool = False) -> Optional[Sound]:
        if as_music:
            pg.mixer.music.load(self.get_sfx_path(sfx))
            return None
        else:
            return pg.mixer.Sound(self.get_sfx_path(sfx))

    def get_xy(self, tile: Coords) -> Coords:
        adjusted_x = tile[0] * self.tile_width_px
        adjusted_y = tile[1] * self.tile_height_px
        return int(adjusted_x), int(adjusted_y)

    def get_xy_center(self, tile: Coords) -> Coords:
        adjusted_x = (tile[0] * self.tile_width_px) + (self.tile_width_px / 2)
        adjusted_y = (tile[1] * self.tile_height_px) + (self.tile_height_px / 2)
        return int(adjusted_x), int(adjusted_y)

    def is_xy_out_of_screen(self, xy: Coords) -> bool:
        return xy[0] < 0 or xy[0] > self.width_px or \
               xy[1] < 0 or xy[1] > self.height_px

    def get_xy_tile(self, xy: Coords) -> Coords:
        return int(xy[0] / self.tile_width_px), \
               int(xy[1] / self.tile_height_px)

    def get_random_tile(self) -> Coords:
        return (random.randint(0, self.tiles_x - 1),
                random.randint(0, self.tiles_y - 1))

    def get_random_tile_not_taken(self, taken: np.ndarray) -> Coords:
        while True:
            tile = self.get_random_tile()
            if not taken[tile[0]][tile[1]]:
                return tile

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
