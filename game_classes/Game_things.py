import pygame
import math

pygame.init()
from game_classes.Projectile import Projectile


class Thing(pygame.sprite.Sprite):
    def __init__(self, cords, pl, name, screen, image=None):
        pygame.sprite.Sprite.__init__(self)
        if image is None:
            self.image = pygame.surface.Surface((20, 20))
            self.image.fill((255, 255, 255))
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.x, self.y = cords[0], cords[1]
        self.rect.x, self.rect.y = self.x, self.y
        self.player = pl
        self.name = name
        self.screen = screen
        self.belong = False

    def get_cords(self):
        return [self.x, self.y]

    def update(self):
        key = pygame.key.get_pressed()
        if self.belong:
            self.rect.x = self.player.rect.x + 10
            self.rect.y = self.player.rect.y + 10
            self.x = self.player.x + 10
            self.y = self.player.y + 10
        if pygame.sprite.collide_rect(self, self.player) and \
                self not in self.player.inventory and \
                self.belong is False:
            if key[pygame.K_p]:
                self.player.inventory['just things'].append(self)
                self.belong = True
            font = pygame.font.Font(None, 22)
            txt = font.render(self.name, False, (255, 255, 255))
            self.screen.blit(txt, (self.rect.x - len(self.name * 3), self.rect.y - 15))


class Weapon(Thing):
    def __init__(self, cords, pl, name, screen, damage, image=None):
        Thing.__init__(self, cords, pl, name, screen)
        self.damage = damage
        if image is None:
            self.image = pygame.surface.Surface((20, 20))
            self.image.fill((255, 255, 255))
        else:
            self.image = image

    def update(self):
        key = pygame.key.get_pressed()
        if self.belong:
            self.rect.x = self.player.rect.x + 40
            self.rect.y = self.player.rect.y + 30
            self.x = self.player.x + 40
            self.y = self.player.y + 30
        if pygame.sprite.collide_rect(self, self.player) and \
                self not in self.player.inventory and \
                self.belong is False:
            if key[pygame.K_p]:
                self.player.inventory['weapons'].append(self)
                self.belong = True
            font = pygame.font.Font(None, 22)
            txt = font.render(self.name, False, (255, 255, 255))
            self.screen.blit(txt, (self.rect.x - len(self.name * 3), self.rect.y - 15))

    def shoot(self, pos, group):
        katx = abs(self.x - pos[0])
        katy = abs(self.y - pos[1])
        gip = (katx ** 2 + katy ** 2) ** 0.5
        co = math.asin(katy / gip)
        print(co)
        group.add(Projectile(self.get_cords(), co, 10, 20, True, group))

