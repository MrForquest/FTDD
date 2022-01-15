import pygame as pp
import math
from game_classes.utilities import Line
from data_file import all_sprites
from game_classes.Projectile import Projectile


class Enemy(pp.sprite.Sprite):
    size = 40

    def __init__(self, coord, weapon):
        pp.sprite.Sprite.__init__(self)
        self.image1 = pp.image.load('data/images/player.png')
        self.image2 = pp.image.load('data/images/player_left.png')
        self.image = self.image1
        self.rect = pp.Rect(*coord, self.size, self.size)
        self.x = coord[0]
        self.y = coord[1]
        self.hp = 100
        self.inventory = dict()
        self.hand = weapon
        self.hand.player = self
        self.hand.belong = True
        self.layer = 23
        self.effect_dist = self.size * 5
        self.count_shooting = 0

        self.radar = pp.sprite.Sprite()
        side = self.size * 17
        self.radar.image = pp.Surface((side, side), pp.SRCALPHA, 32)
        pp.draw.rect(self.radar.image, pp.Color("red"), (0, 0, side, side), 5)
        self.radar.rect = pp.Rect(*self.rect.center, side, side)
        self.radar.rect.center = self.rect.center
        self.radar.x = (self.radar.rect.width - self.rect.width) // 2
        self.radar.y = (self.radar.rect.height - self.rect.height) // 2
        all_sprites.add(self.radar)
        self.cooldown_count = 60
        self.cooldown_flag = True

    def update(self):
        if self.hp <= 0:
            self.radar.kill()
            self.kill()
        velocity = 0.8
        dx = 0
        dy = 0
        sprites_collides = pp.sprite.spritecollide(self.radar, all_sprites, dokill=False)
        if len(sprites_collides):
            for sprite in sprites_collides:
                if sprite.__class__.__name__ == "Player":
                    katx = (sprite.x - self.x)
                    katy = (sprite.y - self.y)
                    angle = math.atan2(katy, katx)

                    boxes = filter(lambda b: getattr(b, "concerning", False), sprites_collides)
                    lines = list()
                    [lines.extend(
                        [Line((b.x, b.y), (b.x + b.rect.width, b.y + b.rect.height)),
                         Line((b.x, b.y + b.rect.height), (b.x + b.rect.width, b.y))])
                        for b in boxes]
                    visual_line = Line((self.x, self.y), (sprite.x, sprite.y))
                    inters = set(map(lambda li: visual_line.intersection(li), lines))
                    if inters:
                        inters.discard(False)
                        if inters:
                            continue
                    dist = pow(katx ** 2 + katy ** 2, 0.5)
                    if dist >= self.effect_dist:
                        dx = math.cos(angle) * velocity
                        dy = math.sin(angle) * velocity
                    else:
                        self.count_shooting+=1
                        if self.count_shooting >= 20:
                            self.hand.shoot(sprite.rect.center, all_sprites)
                            self.count_shooting = 0
        if dx > 0:
            self.image = self.image1
        elif dx < 0:
            self.image = self.image2

        self.x += dx
        self.y += dy
        self.rect.x += dx
        self.rect.y += dy
        sprites_collides = pp.sprite.spritecollide(self, all_sprites, dokill=False)
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
                if sprite.__class__.__name__ == 'Projectile' and \
                        self.cooldown_flag and \
                        self.cooldown_count == 60:
                    self.cooldown_count = 0
                    self.cooldown_flag = False
                    self.hp -= sprite.damage
                if self.cooldown_flag is False:
                    self.cooldown_count += 1
                if self.cooldown_count == 60:
                    self.cooldown_flag = True

        self.x += dx
        self.y += dy
        self.radar.x = self.x - (self.radar.rect.width - self.rect.width) // 2
        self.radar.y = self.y - (self.radar.rect.height - self.rect.height) // 2
        self.hand.draw()

    def get_cords(self):
        return [self.x, self.y]
