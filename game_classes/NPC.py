import pygame
from game_classes.Game_things import Thing
import random
from data_file import all_sprites

pygame.init()


class NPC(pygame.sprite.Sprite):
    def __init__(self, diolog, coords, player, screen, things, image):
        super().__init__()
        self.image = image
        self.diolog = diolog
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.player = player
        self.count = 0
        self.word = self.diolog[self.count]
        self.screen = screen
        self.x, self.y = self.rect.x, self.rect.y
        self.inventory = things
        self.layer_ = 23
        self.cooldown = 60
        self.cooldown_flag = False

    def update(self):
        key = pygame.key.get_pressed()
        a = random.choice(self.inventory)
        if pygame.sprite.collide_rect(self, self.player):
            if key[pygame.K_q] and self.cooldown == 60:
                if (self.count + 1) == len(self.diolog):
                    all_sprites.add(a)
                self.count = (self.count + 1) % len(self.diolog)
                if self.count + 1 == len(self.diolog):
                    self.word = a.name + ' - ' + str(a.price)
                else:
                    self.word = self.diolog[self.count]
                self.cooldown = 0
                self.cooldown_flag = True
            font = pygame.font.Font(None, 30)
            txt = font.render(self.word, True, (255, 255, 255))
            self.screen.blit(txt, pygame.Rect(self.rect.x - len(self.word) * 2, self.rect.y - 23, 20, 20))
            if self.cooldown_flag:
                self.cooldown += 1
            if self.cooldown == 60:
                self.cooldown_flag = False
        else:
            self.count = 0
