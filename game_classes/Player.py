import pygame as pp
import math


class Player(pp.sprite.Sprite):
    size = 40

    def __init__(self, screen, coord, group_collide):
        pp.sprite.Sprite.__init__(self)
        self.image = pp.Surface((self.size, self.size),
                                pp.SRCALPHA, 32)
        pp.draw.rect(self.image, pp.Color("blue"), (0, 0, self.size, self.size))

        self.rect = pp.Rect(*coord, self.size, self.size)
        self.x = 90
        self.y = 150
        self.screen = screen
        self.hp = 100
        self.group_collide = group_collide
        self.inventory = {'weapons': [],
                          'magicshit': []}

    def update(self):
        # pp.draw.rect(self.screen, (0, 0, 255), self.rect)
        dx = 0
        dy = 0
        key = pp.key.get_pressed()
        if key[pp.K_a] and self.rect.x > 0:
            dx = -2
        if key[pp.K_d] and self.rect.x < 500:
            dx = 2
        if key[pp.K_w] and self.rect.y > 0:
            dy = -2
        if key[pp.K_s] and self.rect.y < 500:
            dy = 2
        self.x += dx
        self.y += dy
        self.rect.x += dx
        self.rect.y += dy
        sprites_collides = pp.sprite.spritecollide(self, self.group_collide, dokill=False)
        self.rect.x -= dx
        self.rect.y -= dy
        count = 0
        if len(sprites_collides):
            for sprite in sprites_collides:
                if hasattr(sprite, "concerning"):
                    if sprite.concerning:
                        x1, y1, w1, h1 = self.rect
                        x2, y2, w2, h2 = sprite.rect
                        ddx = abs(max(x1, x2) - min(x1 + w1, x2 + w2))
                        ddy = abs(max(y1, y2) - min(y1 + h1, y2 + h2))
                        if ddx < ddy:
                            dx = math.copysign(ddx + 1, (x1 - x2))
                        else:
                            dy = math.copysign(ddy + 1, (y1 - y2))

                        count += 1

        self.x += dx
        self.y += dy

    def get_cords(self):
        return [self.x, self.y]


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.lx = 0
        self.ly = 0

    def draw(self, screen, coord, group):
        self.x, self.y = coord
        self.x -= screen.get_width() // 2
        self.y -= screen.get_height() // 2
        for spr in group.sprites():
            spr.rect.x = spr.x - self.lx
            spr.rect.y = spr.y - self.ly
        group.draw(screen)
        self.lx = self.x
        self.ly = self.y
