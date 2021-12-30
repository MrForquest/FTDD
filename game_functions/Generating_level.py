import random
from game_classes import GameGrid
import pygame


def generate_level(group):
    for i in range(31):
        if i in range(13, 18):
            pass
        else:
            group.add(GameGrid.GCell((i * 40, 0), True))
            group.add(GameGrid.GCell((i * 40, 30 * 40), True))
        for j in range(1, 30):
            group.add(GameGrid.GCell((i * 40, j * 40), False))
    for i in range(30):
        if i in range(13, 18):
            pass
        else:
            group.add(GameGrid.GCell((0, i * 40), True))
            group.add(GameGrid.GCell((30 * 40, i * 40), True))
    return group
