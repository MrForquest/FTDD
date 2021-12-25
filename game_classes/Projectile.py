import pygame as pp
import math


class Projectile(pp.sprite.Sprite):
    def __init__(self, coord, course, velocity, size, player, group_collide):
        pp.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pp.Surface((self.size, self.size),
                                pp.SRCALPHA, 32)
        pp.draw.rect(self.image, pp.Color("red"), (0, 0, self.size, self.size))
        self.rect = pp.Rect(*coord, self.size, self.size)
        self.x = coord[0]
        self.y = coord[1]
        self.course = -course
        self.velocity = velocity
        angle = self.course
        self.vx = math.cos(angle) * self.velocity
        self.vy = math.sin(angle) * self.velocity
        self.player = player
        self.group_collide = group_collide
        self.live = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x += self.vx
        self.rect.y += self.vy
        sprites_collides = pp.sprite.spritecollide(self, self.group_collide, dokill=False)

        if len(sprites_collides):
            for sprite in sprites_collides:
                if hasattr(sprite, "concerning"):
                    if sprite.concerning:
                        self.live = False
        if not self.live:
            self.kill()
