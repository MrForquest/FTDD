import random
from game_classes import GameGrid


def generate_level(group):
    rooms = random.randrange(4, 12, 2)
    for j in range(rooms):
        for i in range(15):
            group.add(GameGrid.GCell((i * 40, 0), True))
            group.add(GameGrid.GCell((i * 40, 600), True))
        for i in range(16):
            group.add(GameGrid.GCell((0, i * 40), True))
            group.add(GameGrid.GCell((600, i * 40), True))
    return group
