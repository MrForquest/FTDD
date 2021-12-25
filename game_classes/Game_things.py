import pygame

pygame.init()


class Thing(pygame.sprite.Sprite):
    def __init__(self, cords, pl, name, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((20, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.x, self.y = cords[0], cords[1]
        self.rect.x, self.rect.y = self.x, self.y
        self.player = pl
        self.name = name
        self.screen = screen

    def get_cords(self):
        return [self.x, self.y]

    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            font = pygame.font.Font(None, 22)
            txt = font.render(self.name, False, (255, 255, 255))
            self.screen.blit(txt, (self.rect.x - len(self.name * 3), self.rect.y - 15))
