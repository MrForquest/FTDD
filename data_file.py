import pygame
from game_classes.utilities import LayerGroup

enemies = LayerGroup()
group = LayerGroup()
things = LayerGroup()
all_sprites = LayerGroup()
size = width, height = 800, 700
weapons = []
screen = pygame.display.set_mode(size)
textures = dict()
flag = 1
