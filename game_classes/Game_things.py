import pygame
import math
from game_classes.Projectile import Projectile, EmperorProjectile, WNProjectile
from data_file import enemies, group, things, all_sprites
from game_classes.Enemy import Enemy

pygame.init()


class Thing(pygame.sprite.Sprite):
    def __init__(self, cords, pl, name, screen, image=None):
        pygame.sprite.Sprite.__init__(self)
        if image is None:
            self.image = pygame.surface.Surface((20, 20))
            self.image.fill((255, 255, 255))
        else:
            self.image1 = image
            self.image2 = pygame.transform.flip(self.image1, True, False)
            self.image = self.image1
        self.rect = self.image.get_rect()
        self.x, self.y = cords[0], cords[1]
        self.rect.x, self.rect.y = self.x, self.y
        self.player = pl
        self.name = name
        self.screen = screen
        self.belong = False
        self.layer_ = 24

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
            if key[pygame.K_x]:
                self.player.inventory['just things'].append(self)
                self.belong = True
            font = pygame.font.Font(None, 22)
            txt = font.render(self.name, False, (255, 255, 255))
            self.screen.blit(txt, (self.rect.x - len(self.name * 3), self.rect.y - 15))

    def draw(self):
        if self.player.image is self.player.image1:
            if self.image is self.image2:
                self.image = self.image1
            self.rect.x = self.player.rect.x + 25
            self.rect.y = self.player.rect.y + 10
            self.x = self.player.x + 25
            self.y = self.player.y + 10
        if self.player.image is self.player.image2:
            if self.image is self.image1:
                self.image = self.image2
            self.rect.x = self.player.rect.x - 25
            self.rect.y = self.player.rect.y + 10
            self.x = self.player.x - 25
            self.y = self.player.y + 10


class Weapon(Thing):
    def __init__(self, cords, pl, name, screen, damage, price, mana, image=None,
                 image_projectile=None,
                 size_projectile=20, velocity_projectile=10):
        Thing.__init__(self, cords, pl, name, screen)
        self.damage = damage
        self.price = price
        self.size_projectile = size_projectile
        self.velocity_projectile = velocity_projectile
        self.mana = mana
        if image is None:
            self.image = pygame.surface.Surface((20, 20))
            self.image1 = self.image
            self.image2 = self.image
            self.image.fill((255, 255, 255))
        else:
            self.image1 = image
            self.image2 = pygame.transform.flip(self.image1, True, False)
            self.image = self.image1
        self.throwed = False
        self.image_projectile = image_projectile

    def update(self):
        if self.throwed:
            self.image = pygame.Surface((1, 1))
        key = pygame.key.get_pressed()
        if pygame.sprite.collide_rect(self, self.player) and self not in self.player.inventory and \
                self.belong is False:
            if key[pygame.K_x] and len(self.player.inventory['weapons']) < 2:
                self.player.inventory['weapons'].append(self)
                self.belong = True
            font = pygame.font.Font(None, 22)
            txt = font.render(self.name, False, (255, 255, 255))
            self.screen.blit(txt, (self.rect.x - len(self.name * 3), self.rect.y - 15))

    def shoot(self, pos, group):
        katx = (pos[0] - self.rect.center[0])
        katy = (pos[1] - self.rect.center[1])
        co = math.atan2(katy, katx)
        group.add(Projectile(self.get_cords(), co, self.velocity_projectile, self.size_projectile,
                             self.player, group,
                             self.damage,
                             self.image_projectile))


class Potion(Thing):
    def __init__(self, cords, screen, effect, name, price, pl, image):
        Thing.__init__(self, cords, pl, name, screen)
        self.image1 = image
        self.image2 = pygame.transform.flip(self.image1, True, False)
        self.image = image
        self.price = price
        self.effect = effect
        self.throwed = False

    def update(self):
        if self.throwed:
            self.image = pygame.Surface((1, 1))
        key = pygame.key.get_pressed()
        if pygame.sprite.collide_rect(self, self.player) and \
                self not in self.player.inventory and \
                self.belong is False:
            if key[pygame.K_x]:
                self.player.inventory['magicshit'].append(self)
                self.belong = True
            font = pygame.font.Font(None, 22)
            txt = font.render(self.name, False, (255, 255, 255))
            self.screen.blit(txt, (self.rect.x - len(self.name * 3), self.rect.y - 15))

    def use(self):
        if self.effect[0] == 'hp':
            if self.player.hp + self.effect[1] <= 300:
                self.player.hp += self.effect[1]
                print('healed')
        elif self.effect[0] == 'mn':
            if self.player.mana + self.effect[1] <= 500:
                self.player.mana += self.effect[1]
                print('mana')


class Emperor(Weapon):
    def shoot(self, pos, group_):
        katx = (pos[0] - self.rect.center[0])
        katy = (pos[1] - self.rect.center[1])
        co = math.atan2(katy, katx)
        group_.add(
            EmperorProjectile(self.get_cords(), co, 10, 15, self.player, group_, self.damage,
                              self.image_projectile))


class WhiteNova(Weapon):
    def shoot(self, pos, group_):
        katx = (pos[0] - self.rect.center[0])
        katy = (pos[1] - self.rect.center[1])
        co = math.atan2(katy, katx)
        group_.add(
            WNProjectile(self.get_cords(), co, 2, 15, self.player, group_, self.damage,
                         self.image_projectile))
