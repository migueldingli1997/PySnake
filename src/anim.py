import pygame as pg
from pygame.surface import Surface


class Animation:
    def __init__(self, sprite_sheet: Surface, fps: float):
        # Sheet assumed to be horizontal
        self.size_per_sprite = sprite_sheet.get_height()
        self.no_of_sprites = sprite_sheet.get_width() / self.size_per_sprite

        if int(self.no_of_sprites) != self.no_of_sprites:
            raise Exception("Invalid sprite sheet")
        self.no_of_sprites = int(self.no_of_sprites)

        sps = self.size_per_sprite  # alias
        self.sprites = []
        for i in range(self.no_of_sprites):
            self.sprites.append(
                sprite_sheet.subsurface(pg.Rect(i * sps, 0, sps, sps)))

        fpms = fps / 1000  # frames per ms
        self.mspf = 1 / fpms  # ms per frame

        self.time = 0
        self.sprite_index = 0

    def move(self, dt: int):
        self.time += dt

        while self.time > self.mspf:
            self.time -= self.mspf
            self.next_sprite()

    def next_sprite(self):
        self.sprite_index = (self.sprite_index + 1) % self.no_of_sprites

    def get_sprite(self):
        return self.sprites[self.sprite_index]
