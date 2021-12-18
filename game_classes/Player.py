import pygame as pp


class Player(pp.sprite.Sprite):
    def __init__(self, screen):
        pp.sprite.Sprite.__init__(self)
        self.rect = pp.Rect(0, 0, 40, 40)
        self.screen = screen
        self.hp = 100

    def update(self):
        pp.draw.rect(self.screen, (0, 0, 255), self.rect)
        key = pp.key.get_pressed()
        if key[pp.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 2
        if key[pp.K_RIGHT] and self.rect.x < 500:
            self.rect.x += 2
        if key[pp.K_UP] and self.rect.y > 0:
            self.rect.y -= 2
        if key[pp.K_DOWN] and self.rect.y < 500:
            self.rect.y += 2
