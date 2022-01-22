import random
from game_classes import GameGrid
from game_classes.NPC import NPC
from game_classes.Enemy import Enemy
from game_classes.Game_things import Weapon
from data_file import enemies, textures, group
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
        wizard_NPC = NPC(['Здравствуй, странник', 'Тебе помочь?', 'Зелье здоровья', '20 монет'],
                         (400, 300),
                         None, screen, 0,
                         pygame.transform.flip(pygame.image.load('data/images/wizard.png'), True,
                                               False))
        group.add(wizard_NPC)
    elif biome == 'hell':
        for i in range(10):
            enemies.add(
                Enemy((random.randrange(50, size * 40, 50), random.randrange(50, size * 40, 50)),
                      Weapon((350, 400), None, 'Вражеский лук', screen, 20,
                             25, 1, image=textures["average_magic_stick"])))
        return group


class Cell:
    def __init__(self, x, y, num, val):
        self.x = x
        self.y = y
        self.num = num
        self.val = val
        self.s = {self}

    def set_val(self, val):
        self.val = val

    def __hash__(self):
        return hash(self.num)


class Matrix:
    m = 9

    def __init__(self, x, y, w, h, labyrinth):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.labyrinth = labyrinth

    def division_matrix(self):
        if self.w < self.m or self.h < self.m:
            return list()
        d = (self.m + 1) // 2
        sx, ex = self.x + d, self.x + self.w - d
        sy, ey = self.y + d, self.y + self.h - d
        if sx >= ex or sy >= ey:
            return list()
        wx = random.choice(range(self.x + d, self.x + self.w - d, 2))
        wy = random.choice(range(self.y + d, self.y + self.h - d, 2))

        for x in range(self.x, self.x + self.w):
            self.labyrinth[wy][x].set_val(1)
        for y in range(self.y, self.y + self.h):
            self.labyrinth[y][wx].set_val(1)

        wns = set(range(0, 4))
        wns.remove(random.randint(0, 3))
        for wn in wns:
            dx = dy = 0
            if wn == 0:
                dx = random.randint(self.x, wx - 1)
                dy = wy
            elif wn == 1:
                dy = random.randint(self.y, wy - 1)
                dx = wx
            elif wn == 2:
                dx = random.randint(wx + 1, self.x + self.w - 1)
                dy = wy
            elif wn == 3:
                dy = random.randint(wy + 1, self.y + self.h - 1)
                dx = wx
            self.labyrinth[dy][dx].set_val(0)
        new_mats = [Matrix(self.x, self.y, wx - self.x, wy - self.y, self.labyrinth),
                    Matrix(wx + 1, self.y, self.w - (wx - self.x) - 1, wy - self.y, self.labyrinth),
                    Matrix(self.x, wy + 1, wx - self.x, self.h - (wy - self.y) - 1, self.labyrinth),
                    Matrix(wx + 1, wy + 1, self.w - (wx - self.x) - 1, self.h - (wy - self.y) - 1,
                           self.labyrinth)]
        res = list()
        for m_ in new_mats:
            if m_.w >= self.m and m_.h >= self.m:
                res.append(m_)
        return res


def division_rec(ms_):
    for m in ms_:
        division_rec(m.division_matrix())


def generate_labyrinth():
    a = 21
    labyrinth = [[Cell(i, j, i * j, 0) for i in range(0, a)] for j in range(0, a)]
    for c in labyrinth[0]:
        c.set_val(1)
    for c in labyrinth[-1]:
        c.set_val(1)
    for i in range(0, a):
        labyrinth[i][0].set_val(1)
        labyrinth[i][-1].set_val(1)
    matrix = Matrix(1, 1, a - 2, a - 2, labyrinth)
    ms = matrix.division_matrix()
    division_rec(ms)
    # for line in labyrinth:
    #    print("".join(map(lambda s: str(s.val), line)).replace("0", "⬛").replace("1", "⬜"))
    for i in group.sprites():
        i.kill()
    size = GameGrid.GCell.size
    for y in range(a):
        for x in range(a):
            if labyrinth[y][x].val == 1:
                group.add(GameGrid.GCell((x * size, y * size), True, None))
            else:
                group.add(GameGrid.GCell((x * size, y * size), False, None))

    return group
