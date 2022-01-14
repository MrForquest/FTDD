import pygame
import pygame as pp
import math
from game_classes.Game_things import Weapon


class Player(pp.sprite.Sprite):
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
        self.inventory = {'weapons': [],
                          'magicshit': []
                          }
        self.hand = None

    def update(self):
        dx = 0
        dy = 0
        vel = 2
        key = pp.key.get_pressed()
        if isinstance(self.hand, Weapon):
            self.hand.draw()
        if key[pp.K_a] and self.rect.x > 0:
            dx = -vel
            self.image = self.image2
        if key[pp.K_d] and self.rect.x < 500:
            dx = vel
            self.image = self.image1
        if key[pp.K_w] and self.rect.y > 0:
            dy = -vel
        if key[pp.K_s] and self.rect.y < 500:
            dy = vel
        if dx != 0 and dy != 0:
            vel = pow(vel, 0.5)
            dx = math.copysign(vel, dx)
            dy = math.copysign(vel, dy)
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
