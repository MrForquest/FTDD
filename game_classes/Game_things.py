import pygame


class Thing(pygame.sprite.Sprite):
    def __init__(self, cords, pl):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.x, self.y = cords[0], cords[1]
        self.player = pl

    def get_cords(self):
        return [self.x, self.y]

    def update(self):
        key = pygame.key.get_pressed()
        if pygame.sprite.collide_mask(self, self.player) and key[pygame.K_q]:
            pass
