import pygame

pygame.init()


class NPC(pygame.sprite.Sprite):
    def __init__(self, diolog, coords, player, screen, thing, image):
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
        self.inventory = []
        self.layer = 23

    def update(self):
        self.word = self.diolog[self.count]
        key = pygame.key.get_pressed()
        if pygame.sprite.collide_rect(self, self.player):
            font = pygame.font.Font(None, 30)
            txt = font.render(self.word, True, (255, 255, 255))
            self.screen.blit(txt, pygame.Rect(self.rect.x - len(self.word) * 2, self.rect.y - 23, 20, 20))
            if key[pygame.K_q]:
                self.count = (self.count + 1) % len(self.diolog)
                pygame.time.delay(200)
        else:
            self.count = 0
