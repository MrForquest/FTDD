import pygame
import random
from data_file import all_sprites


class GCell(pygame.sprite.Sprite):
    size = 40

    def __init__(self, coord, concerning, biome, type_id=None):
        super().__init__(all_sprites)
        self.type_id = type_id
        self.concerning = concerning
        # self.rect.size = self.size
        if self.concerning is False:
            if biome is None:
                self.image = pygame.image.load('data/images/grass1.png')
                self.image = pygame.transform.rotate(self.image, random.randrange(0, 360, 90))
            elif biome == 'hell':
                self.image = pygame.image.load('data/images/hell_tile.png')
                self.image = pygame.transform.rotate(self.image, random.randrange(0, 360, 90))
        else:
            self.image = self.image = pygame.image.load('data/images/wall.png')

        self.rect = pygame.Rect(*coord, self.size, self.size)
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        self.x = coord[0]
        self.y = coord[1]
        self.layer_ = 3

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
