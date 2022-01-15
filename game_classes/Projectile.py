import pygame as pp
import math


class Projectile(pp.sprite.Sprite):
    def __init__(self, coord, course, velocity, size, player, group_collide, damage):
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
        self.count = 0
        self.layer = 13
        self.damage = damage

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
        self.count += 1
        if not self.live:
            self.kill()
        if self.count > self.velocity * 50:
            self.kill()


class EmperorProjectile(Projectile):
    def __init__(self, *args):
        super(EmperorProjectile, self).__init__(*args[:len(args) - 1])
        self.enemies = args[-1]

    def update(self):
        dx = 0
        dy = 0

        if len(self.enemies):
            nearest_enemy = min(self.enemies, key=lambda enemy: ((enemy.x - self.x) ** 2 + (
                enemy.y - self.y) ** 2) ** 0.5)
            katx = (nearest_enemy.x - self.x)
            katy = (nearest_enemy.y - self.y)
            angle = math.atan2(katy, katx)

            dx = math.cos(angle) * self.velocity
            dy = math.sin(angle) * self.velocity
            if abs(katx) < 5 and abs(katy) < 5:
                self.live = False
        else:
            self.live = False
        self.x += dx
        self.y += dy
        self.rect.x += dx
        self.rect.y += dy
        sprites_collides = pp.sprite.spritecollide(self, self.group_collide, dokill=False)
        if len(sprites_collides):
            for sprite in sprites_collides:
                if hasattr(sprite, "concerning"):
                    if sprite.concerning:
                        self.live = False
        self.count += 1
        if not self.live:
            self.kill()
        if self.count > self.velocity * 50:
            self.kill()
