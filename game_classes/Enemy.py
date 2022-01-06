import pygame as pp
import math


class Enemy(pp.sprite.Sprite):
    size = 40

    def __init__(self, coord, group_collide):
        pp.sprite.Sprite.__init__(self)
        self.image1 = pp.image.load('data/images/player.png')
        self.image2 = pp.image.load('data/images/player_left.png')
        self.image = self.image1
        self.rect = pp.Rect(*coord, self.size, self.size)
        self.x = coord[0]
        self.y = coord[1]
        self.hp = 100
        self.group_collide = group_collide
        self.hand = 0

        self.radar = pp.sprite.Sprite()
        side = self.size * 12
        self.radar.image = pp.Surface((side, side), pp.SRCALPHA, 32)
        pp.draw.rect(self.radar.image, pp.Color("red"), (0, 0, side, side), 5)
        self.radar.rect = pp.Rect(*self.rect.center, side, side)
        self.radar.rect.center = self.rect.center
        self.radar.x = (self.radar.rect.width - self.rect.width) // 2
        self.radar.y = (self.radar.rect.height - self.rect.height) // 2
        group_collide.add(self.radar)

    def update(self):
        velocity = 1.6
        dx = 0
        dy = 0
        sprites_collides = pp.sprite.spritecollide(self.radar, self.group_collide, dokill=False)
        if len(sprites_collides):
            for sprite in sprites_collides:
                if sprite.__class__.__name__ == "Player":
                    katx = (sprite.x - self.x)
                    katy = (sprite.y - self.y)
                    angle = math.atan2(katy, katx)
                    max_dist = pow(katx ** 2 + katy ** 2, 0.5)
                    sx = math.cos(angle)
                    sy = math.sin(angle)
                    ps = [(sx * i + self.x, sy * i + self.y) for i in range(1, round(max_dist), 20)]

                    dx = math.cos(angle) * velocity
                    dy = math.sin(angle) * velocity
                    val = False
                    for spr in self.group_collide:
                        rect = pp.Rect(spr.x, spr.y, spr.rect.width, spr.rect.height)
                        val = any(map(lambda p: rect.collidepoint(p) and getattr(spr, "concerning",
                                                                                 False), ps))
                        if val:
                            dx = dy = 0
                            break
        self.x += dx
        self.y += dy
        self.rect.x += dx
        self.rect.y += dy
        sprites_collides = pp.sprite.spritecollide(self, self.group_collide, dokill=False)
        self.rect.x -= dx
        self.rect.y -= dy
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
        self.x += dx
        self.y += dy
        self.radar.x = self.x - (self.radar.rect.width - self.rect.width) // 2
        self.radar.y = self.y - (self.radar.rect.height - self.rect.height) // 2

    def get_cords(self):
        return [self.x, self.y]
