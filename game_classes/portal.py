import pygame
from game_functions.Generating_level import generate_level


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

    def update(self):
        if pygame.sprite.collide_rect(self, self.pl):
            self.al.add(generate_level(self.group, self.sc, 25, 'hell'))
            self.pl.x, self.pl.y = 250, 300

