import pygame
from data_file import enemies, group, things, all_sprites, screen
from button import Button
import os, sys


def pr():
    print(12)


def load_image(name, colorkey=None):
    fullname = name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class MainMenu:
    def __init__(self, size_m):
        self.make_menu(size_m)

    def make_menu(self, size_m):
        width_, height_ = size_m
        wall = load_image('../data/images/main_wall.png')
        wall = pygame.transform.scale(wall, (0.5 * width_, 0.57 * width))
        background = pygame.surface.Surface(size)
        background.blit(wall, (0, 0))
        background.blit(wall, (0.5 * width_, 0))
        wall = pygame.transform.flip(wall, False, True)
        background.blit(wall, (0, 0.565 * height_))
        background.blit(wall, (0.5 * width_, 0.565 * height_))

        magic_circle = load_image('../data/images/magic_circle.png')
        magic_circle = pygame.transform.scale(magic_circle, (1 * height_, 1 * height_))
        background.blit(magic_circle, (0.53 * (width_ - height_), 0.02 * height_))
        dy = -0.11 * height_
        pygame.draw.rect(background, "#660000",
                         pygame.Rect(0.31 * width_, 0.21 * height_ + dy, 0.38 * width_,
                                     0.17 * height_),
                         border_radius=10)

        f = pygame.font.Font("../data/other/windsor.ttf", round(0.05 * width_))
        text = f.render("Forty-Two", False, "#CC1100")
        background.blit(text, (width_ * 0.43, 0.21 * height_ + dy))

        text = f.render("Descents Down", False, "#CC1100")
        background.blit(text, (width_ * 0.4, 0.29 * height_ + dy))
        self.background = background
        text = f.render("Начать", False, "#CC1100")

        self.btns = list()
        self.btns.append(
            Button(width_ * 0.41, 0.29 * height_, 0.19 * width_, 0.09 * height_, pr, text))

        for b in self.btns:
            background.blit(b, b.rect.topleft)

    def update_btn(self, mouse_pos):
        for b in self.btns:
            b.check_press(*mouse_pos)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 900, 900
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    size = width, height = screen.get_size()
    menu = MainMenu(size)
    pygame.display.set_caption('Движущийся квадрат')

    running = True
    x_pos = 0
    fps = 60
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    menu.update_btn(event.pos)

        screen.blit(menu.background, (0, 0))
        pygame.display.update()
    pygame.quit()
