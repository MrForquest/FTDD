import pygame


class GCell(pygame.sprite.Sprite):
    def __init__(self, coord, concerning, type_id=None):
        super().__init__(self)
        self.type_id = type_id
        self.concerning = concerning
        self.rect.x = coord[0]
        self.rect.y = coord[1]

    def draw(self):
        pass


class Grid:
    def __init__(self, w, h, grid=None):
        self.height = w
        self.width = h
        if grid is None:
            self.grid =
        else:
            self.grid = grid

    def draw(self, sc):
