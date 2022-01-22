import pygame


def load_texture():
    textures = dict()
    textures["average_bow"] = pygame.image.load('data/images/average_bow.png')
    textures["dark_flame"] = pygame.image.load('data/images/dark_flame.png')
    textures["average_magic_stick"] = pygame.image.load('data/images/average_magic_stick.png')
    textures["enderperl"] = pygame.image.load('data/images/enderperl.png')
    textures["white_nova"] = pygame.image.load('data/images/white_nova.png')
    textures["heal_potion"] = pygame.image.load('data/images/heal_potion.png')
    textures["mana_potion"] = pygame.image.load('data/images/mana_potion.png')
    textures["emperor"] = pygame.image.load('data/images/emperor.png')
    textures["emperor_projectile"] = pygame.image.load('data/images/emperor_projectile.png')
    textures["health_frame"] = pygame.image.load('data/images/health_frame.png')
    textures["wall"] = pygame.image.load('data/images/wall.png')
    textures["hell_tile"] = pygame.image.load('data/images/hell_tile.png')
    textures["grass1"] = pygame.image.load('data/images/grass1.png')
    return textures
