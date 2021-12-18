import pygame


class GCell(pygame.sprite.Sprite):
    size = 40

    def __init__(self, coord, concerning, type_id=None):
        super().__init__()
        self.type_id = type_id
        self.concerning = concerning
        # self.rect.size = self.size
        self.rect = pygame.Rect(coord, (self.size, self.size))
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        self.x = coord[0]
        self.y = coord[1]

    def draw(self, sc):
        pygame.draw.rect(sc, (0, 0, 255), self.rect)


class Grid:
    def __init__(self, w, h, coord, grid=None):
        self.height = h
        self.width = w
        self.coord = coord
        if grid is None:
            self.grid = pygame.sprite.Group()
            for i in range(self.width * self.height):
                self.grid.add(GCell((i % self.width, i % self.height), False))
        else:
            self.grid = grid

    def shift(self, coord_center):
        dx = self.coord[0] - coord_center[0]
        dy = self.coord[1] - coord_center[1]
        for cell in self.grid.sprites():
            cell.rect.x = cell.x + dx
            cell.rect.y = cell.y + dy

    def draw(self, sc, coord_center):
        self.shift(coord_center)
        for cell in self.grid.sprites():
            pygame.draw.rect(sc, (0, 255, 0), cell.rect)
        # self.grid.draw(sc)
