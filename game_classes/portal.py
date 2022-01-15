import pygame
from game_functions.Generating_level import generate_level
from data_file import enemies


class Portal(pygame.sprite.Sprite):
    def __init__(self, image, coords, player, group, scr, alll):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.pl = player
        self.group = group
        self.sc = scr
        self.x, self.y = self.rect.x, self.rect.y
        self.al = alll
        self.layer_ = 4
        self.count = 20

    def update(self):
        if self.count == 20:
            self.image = pygame.transform.rotate(self.image, 90)
            self.count = 0
        self.count += 1
        if pygame.sprite.collide_rect(self, self.pl):
            self.al.add(generate_level(self.group, self.sc, 25, 'hell'))
            self.pl.x, self.pl.y = 450, 400
            self.pl.rect.x, self.pl.rect.y = self.pl.x, self.pl.y
