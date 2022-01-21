import pygame

pygame.init()


class Button(pygame.surface.Surface):
    def __init__(self, x, y, w, h, func, text):
        super(Button, self).__init__((w, h))
        self.rect = pygame.Rect(x, y, w, h)
        # self.set_alpha(0)
        colorkey = self.get_at((0, 0))
        pygame.draw.rect(self, "#660000",
                         pygame.Rect(0, 0, w, h),
                         border_radius=10)
        self.set_colorkey(colorkey)
        wt, ht = text.get_size()
        dx = (w - wt) / 2
        self.blit(text, (dx, 0))
        self.text = text
        self.func_button = func

    def check_press(self, mouse_x, mouse_y):
        x1, y1 = self.rect.topleft
        x2, y2 = self.rect.bottomright
        if mouse_x in range(x1, x2 + 1) and mouse_y in range(y1, y2 + 1):
            if self.func_button:
                self.func_button()
            return True
        else:
            return False
