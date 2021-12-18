import pygame as pp


class Player(pp.sprite.Sprite):
    def __init__(self, screen):
        pp.sprite.Sprite.__init__(self)
        self.rect = pp.Rect(0, 0, 40, 40)
        self.screen = screen

    def update(self):
        pp.draw.rect(self.screen, (0, 0, 255), self.rect)
        key = pp.key.get_pressed()
        if key[pp.K_LEFT]:
            self.rect.x -= 2
        if key[pp.K_RIGHT]:
            self.rect.x += 2
        if key[pp.K_UP]:
            self.rect.y -= 2
        if key[pp.K_DOWN]:
            self.rect.y += 2
