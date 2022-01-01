import pygame


class Inventory(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('data/images/inventory.png')
        self.frame = pygame.image.load('data/images/inventory_frame.png')
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 620
        self.player = player
        self.slot = {0: None,
                     1: None,
                     2: None,
                     3: None}
        self.slot_use = self.player.hand
        self.frame_rect = self.frame.get_rect()

    def update(self, sc):
        sc.blit(self.image, self.rect)
        self.slot_use = self.player.hand
        try:
            self.slot[0] = self.player.inventory['weapons'][0]
            self.slot[1] = self.player.inventory['weapons'][1]
            self.slot[2] = self.player.inventory['magicshit'][0]
            self.slot[3] = self.player.inventory['magicshit'][1]
        except IndexError:
            pass
        self.frame_rect.x, self.frame_rect.y = self.rect.x + (5 + 100 * self.slot_use), self.rect.y + 5
        sc.blit(self.frame, self.frame_rect)
        if self.slot[0] is not None:
            sc.blit(self.slot[0].image1, pygame.Rect(self.rect.x + 25, self.rect.y + 8, 20, 20))

