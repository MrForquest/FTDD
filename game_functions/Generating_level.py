import random
from game_classes import GameGrid
from game_classes.NPC import NPC
import pygame


def generate_level(group, screen, size, biome=None):
    for i in group.sprites():
        i.kill()
    for i in range(size + 1):
        group.add(GameGrid.GCell((i * 40, 0), True, biome))
        group.add(GameGrid.GCell((i * 40, (size + 1) * 40), True, biome))
        for j in range(1, size + 1):
            group.add(GameGrid.GCell((i * 40, j * 40), False, biome))
    for i in range(size + 1):
        if i in range(6, 10) and biome is None:
            pass
        else:
            group.add(GameGrid.GCell((0, i * 40), True, biome))
            group.add(GameGrid.GCell((size * 40, i * 40), True, biome))
    if biome is None:
        wizard_NPC = NPC(['Здравствуй, странник', 'Тебе помочь?', '20 монет'], (400, 300),
                         None, screen, 0, pygame.image.load('data/images/wizard.png'))
        group.add(wizard_NPC)
    return group
