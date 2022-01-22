import pygame
import random
from data_file import all_sprites, textures
from game_classes.utilities import Line


class GCell(pygame.sprite.Sprite):
    size = 40

    def __init__(self, coord, concerning, biome, type_id=None):
        super().__init__(all_sprites)
        self.type_id = type_id
        self.concerning = concerning
        # self.rect.size = self.size
        if self.concerning is False:
            if biome is None:
                self.image = textures["grass1"]
                self.image = pygame.transform.rotate(self.image, random.randrange(0, 360, 90))

            elif biome == 'hell':
                self.image = textures["hell_tile"]
                self.image = pygame.transform.rotate(self.image, random.randrange(0, 360, 90))
        else:
            self.image = self.image = textures["wall"]

        self.rect = pygame.Rect(*coord, self.size, self.size)
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        self.x = coord[0]
        self.y = coord[1]
        if self.concerning:
            self.layer_ = 4
        else:
            self.layer_ = 3
        self.line1 = Line((self.x, self.y), (self.x + self.rect.width, self.y + self.rect.height))
        self.line2 = Line((self.x, self.y + self.rect.height), (self.x + self.rect.width, self.y))

    def draw(self, sc):
        sc.blit(self.image, self.rect)


class Grid:
    def __init__(self, w, h, coord, grid=None):
        self.height = h
        self.width = w
        self.coord = coord
        if grid is None:
            self.grid = pygame.sprite.Group()
            for i in range(self.width * self.height):
                self.grid.add(GCell((i % self.width, i % self.height), True))
        else:
            self.grid = grid

    def draw(self, sc, coord_center):
        self.grid.draw(sc)
