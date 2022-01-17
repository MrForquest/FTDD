import pygame as pp
import math
from data_file import all_sprites, enemies


class Projectile(pp.sprite.Sprite):
    def __init__(self, coord, course, velocity, size, player, group_collide, damage, image=None):
        pp.sprite.Sprite.__init__(self, all_sprites)
        self.size = size

        if image is None:
            self.image = pp.Surface((self.size, self.size),
                                    pp.SRCALPHA, 32)
            pp.draw.rect(self.image, pp.Color("red"), (0, 0, self.size, self.size))
        else:
            self.image = pp.transform.scale(image, (self.size, self.size))

        self.rect = pp.Rect(*coord, self.size, self.size)
        self.x = coord[0]
        self.y = coord[1]
        self.course = course
        self.velocity = velocity
        angle = self.course
        self.vx = math.cos(angle) * self.velocity
        self.vy = math.sin(angle) * self.velocity
        self.player = player
        self.group_collide = group_collide
        self.live = True
        self.count = 0
        self.layer_ = 13
        self.damage = damage

    def check_hit(self, sprite):
        if sprite.__class__.__name__ == "Enemy":
            if self.player.__class__.__name__ == "Player":
                sprite.hp -= self.damage
                self.live = False
        if sprite.__class__.__name__ == "Player":
            if self.player.__class__.__name__ == "Enemy":
                sprite.hp -= self.damage
                self.live = False

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
                self.check_hit(sprite)

        self.count += 1
        if not self.live:
            self.kill()
        if self.count > self.velocity * 5:
            self.kill()


class EmperorProjectile(Projectile):
    def __init__(self, *args):
        super(EmperorProjectile, self).__init__(*args)

    def update(self):
        dx = 0
        dy = 0

        if len(enemies):
            nearest_enemy = min(enemies, key=lambda enemy: ((enemy.x - self.x) ** 2 + (
                enemy.y - self.y) ** 2) ** 0.5)
            katx = (nearest_enemy.x - self.x) + nearest_enemy.rect.width // 2
            katy = (nearest_enemy.y - self.y) + nearest_enemy.rect.height // 2
            angle = math.atan2(katy, katx)

            dx = math.cos(angle) * self.velocity
            dy = math.sin(angle) * self.velocity

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
                self.check_hit(sprite)
        self.count += 1
        if not self.live:
            self.kill()
        if self.count > self.velocity * 50:
            self.kill()


class WNProjectile(Projectile):
    def __init__(self, *args):
        super(WNProjectile, self).__init__(*args)
        self.image = pp.Surface((self.size, self.size),
                                pp.SRCALPHA, 32)
        pp.draw.circle(self.image, pp.Color("white"), (self.size // 2, self.size // 2),
                       self.size // 2)
        self.image = pp.transform.scale(self.image, (self.size, self.size))
        self.count_explode = 0
        self.damage = 2

    def update(self):
        ds = 0
        dx = self.vx
        dy = self.vy
        if self.count_explode > 0:
            self.layer_ = 100
            dx = dy = 0
            ds = 2.5
            self.size += round(ds * 2)
            self.image.fill(pp.Color(0, 0, 0, 0))
            pp.draw.circle(self.image, pp.Color("white"), (self.size / 2 - 2, self.size / 2 - 2),
                           self.size / 2 - 2)
            self.image = pp.transform.scale(self.image, (self.size, self.size))
            self.rect = pp.Rect(self.rect.x, self.rect.y, self.size, self.size)
        self.x += dx - ds
        self.y += dy - ds
        self.rect.x += dx - ds
        self.rect.y += dy - ds
        sprites_collides = pp.sprite.spritecollide(self, self.group_collide, dokill=False)
        if len(sprites_collides):
            for sprite in sprites_collides:
                if hasattr(sprite, "concerning"):
                    if sprite.concerning:
                        self.live = False
                self.check_hit(sprite)

        self.count += 1
        if not self.live:
            self.vx = 0
            self.vy = 0
            self.count_explode += 1
        if self.count > self.velocity * 70:
            self.live = False
        if self.count_explode > 50:
            self.kill()
