from util import Coords, Direction, get_next_xy, Util

BULLET_TILES_PER_SECOND = 30


class Bullet:

    def __init__(self, coords: Coords, direction: Direction, util: Util):
        self.coords = coords
        self.direction = direction

        tpms = BULLET_TILES_PER_SECOND / 1000  # tiles per ms
        ppms = tpms * util.tile_width  # pixels per ms
        self.mspp = 1 / ppms  # ms per pixel

        self.time = 0

    def move(self, dt: int):
        self.time += dt

        px = 0
        while self.time > self.mspp:
            self.time -= self.mspp
            px += 1

        if px > 0:
            self.coords = get_next_xy(self.coords, self.direction, px)
