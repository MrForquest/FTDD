import pygame
from game_classes.GameGrid import Grid, GCell
from game_classes.Player import Player, Camera
from game_classes.Game_things import Thing, Weapon, Emperor, WhiteNova
from game_functions.Generating_level import generate_level
from game_classes.Inventory import Inventory
from game_classes.NPC import NPC
from game_classes.Enemy import Enemy
from game_classes.portal import Portal
from data_file import enemies, group, things, all_sprites

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся квадрат')
    size = width, height = 800, 700
    screen = pygame.display.set_mode(size)

    generate_level(group, screen, 15)
    grid = Grid(20, 20, (0, 0), grid=group)
    player = Player((250, 300), all_sprites)
    for i in group.sprites():
        if isinstance(i, NPC):
            i.player = player
    weapon = Weapon((300, 400), player, 'Лук тёмного пламени', screen, 40,
                    25, pygame.image.load('data/images/average_bow.png'),
                    pygame.image.load('data/images/dark_flame.png'), 40, 7)
    weapon2 = Weapon((350, 400), player, 'Посох Эндера', screen, 20,
                     25, pygame.image.load('data/images/average_magic_stick.png'),
                     pygame.image.load('data/images/enderperl.png'), 30, 10)
    weapon3 = WhiteNova((700, 400), player, 'White Nova', screen, 20,
                        25, pygame.image.load('data/images/white_nova.png'))
    weapon_enemy = Weapon((350, 400), player, 'Вражеский лук', screen, 25,
                          25, pygame.image.load('data/images/average_magic_stick.png'))
    all_sprites.add(
        Portal(pygame.image.load('data/images/portal1.png'), (-80, 8 * 40), player, group, screen,
               all_sprites))
    all_sprites.add(*group.sprites())

    all_sprites.add(weapon, weapon2, weapon3, weapon_enemy)

    all_sprites.add(Emperor((500, 400), player, 'Emperor', screen, 20, 25,
                            pygame.image.load('data/images/emperor.png'),
                            pygame.image.load('data/images/emperor_projectile.png')))
    all_sprites.add(weapon)
    group.add(weapon)
    enemy = Enemy((250, 600), weapon_enemy)

    inventory = Inventory(player)
    all_sprites.add(player)
    camera = Camera()

    running = True
    x_pos = 0
    fps = 60
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and player.inventory['weapons'] != []:
                    if isinstance(player.hand, Weapon):
                        player.hand.shoot(event.pos, all_sprites)

            if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 5 or event.button == 4):
                if event.button == 5:
                    inventory.slot_use = (inventory.slot_use + 1) % 4
                    inventory.update(screen)
                elif event.button == 4:
                    inventory.slot_use = (inventory.slot_use - 1) % 4
                    inventory.update(screen)
        screen.fill((33, 33, 33))

        player_coord = player.get_cords()
        camera.draw(screen, player_coord, all_sprites)

        try:
            for i in player.inventory['weapons']:
                i.remove(all_sprites)
            if isinstance(player.hand, Thing):
                all_sprites.add(player.hand)
        except Exception:
            pass

        group.update()
        all_sprites.update()
        inventory.update(screen)

        clock.tick(fps)
        pygame.display.update()
    pygame.quit()
