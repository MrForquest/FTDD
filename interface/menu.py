import pygame
from data_file import screen, all_sprites, enemies
from interface.button import Button
import os
import sys
from game_functions.sql_save import save
from game_classes.Player import Player


def pr():
    global pause
    pause[0] = False


def new_game():
    pause[0] = False
    for en in enemies.sprites():
        en.kill()
        en.hand.kill()
        en.radar.kill()
    portal = list(filter(lambda s: s.__class__.__name__ == "Portal", all_sprites.sprites()))
    if portal:
        portal[0].flg = 0


def sv():
    save(menu.pl)


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
    def __init__(self, size_m, player):
        self.make_menu(size_m)
        self.pl = player

    def make_menu(self, size_m):
        width_, height_ = size_m
        wall = load_image('data/images/main_wall.png')
        wall = pygame.transform.scale(wall, (int(0.5 * width_), int(0.57 * height_)))
        background = pygame.surface.Surface(size_m)
        background.blit(wall, (0, 0))
        background.blit(wall, (0.5 * width_, 0))
        wall = pygame.transform.flip(wall, False, True)
        background.blit(wall, (0, 0.565 * height_))
        background.blit(wall, (0.5 * width_, 0.565 * height_))

        magic_circle = load_image('data/images/magic_circle.png')
        magic_circle = pygame.transform.scale(magic_circle, (1 * height_, 1 * height_))
        background.blit(magic_circle, (0.53 * (width_ - height_), 0.02 * height_))
        dy = -0.11 * height_
        pygame.draw.rect(background, "#660000",
                         pygame.Rect(0.31 * width_, 0.21 * height_ + dy, 0.38 * width_,
                                     0.17 * height_),
                         border_radius=10)

        f = pygame.font.Font("data/other/windsor.ttf", round(0.05 * width_))
        text = f.render("Forty-Two", False, "#CC1100")
        background.blit(text, (width_ * 0.43, 0.21 * height_ + dy))

        text = f.render("Descents Down", False, "#CC1100")
        background.blit(text, (width_ * 0.4, 0.29 * height_ + dy))
        self.background = background
        text = f.render("Играть", False, "#CC1100")

        self.btns = list()
        self.btns.append(
            Button(width_ * 0.41, 0.29 * height_, 0.19 * width_, 0.09 * height_, pr, text))
        text = f.render("Сохранить", False, "#CC1100")
        self.btns.append(
            Button(width_ * 0.41, 0.39 * height_, 0.19 * width_, 0.09 * height_, sv, text))
        for b in self.btns:
            background.blit(b, b.rect.topleft)

    def update_btn(self, mouse_pos):
        for b in self.btns:
            b.check_press(*mouse_pos)


class EndMenu:
    def __init__(self, size):
        self.background = pygame.surface.Surface(size)
        self.background.fill((0, 0, 0))
        text_img = load_image("data/images/you_died_text.png", -1)
        self.background.blit(text_img, (
            (size[0] - text_img.get_width()) // 2, (size[1] - text_img.get_height()) // 2 - 100))
        width_, height_ = size
        f = pygame.font.Font("data/other/windsor.ttf", round(0.05 * width_))
        text = f.render("Возродиться", False, "#CC1100")

        self.btns = list()
        self.btns.append(
            Button(width_ * 0.41, 0.5 * height_, 0.19 * width_, 0.09 * height_, new_game, text))
        for b in self.btns:
            self.background.blit(b, b.rect.topleft)

    def update_btn(self, mouse_pos):
        for b in self.btns:
            b.check_press(*mouse_pos)


menu = MainMenu(screen.get_size(), None)
pause = list()
pause.append(True)
final = EndMenu(screen.get_size())
