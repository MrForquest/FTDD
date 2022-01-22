import pygame
from game_classes.GameGrid import Grid, GCell
from game_classes.Player import Player, Camera
from game_classes.Game_things import Thing, Weapon, Emperor, WhiteNova, Potion
from game_functions.Generating_level import generate_level, generate_labyrinth
from game_classes.Inventory import Inventory
from game_classes.NPC import NPC
from game_classes.Enemy import Enemy
from game_classes.portal import Portal
from data_file import enemies, group, things, all_sprites, screen, textures
from game_functions.Load_texture import load_texture
from data_file import enemies, group, things, all_sprites, screen, weapons
from interface.menu import menu, pause
from game_functions.sql_save import sql_load

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся квадрат')

    textures.update(load_texture())
    # generate_level(group, screen, 15)
    generate_labyrinth()
    grid = Grid(20, 20, (0, 0), grid=group)
    player = Player((250, 300), all_sprites)
    for i in group.sprites():
        if isinstance(i, NPC):
            i.player = player
    weapon = Weapon((300, 400), player, 'Лук тёмного пламени', screen, 40,
                    25, 0, textures["average_bow"],
                    textures["dark_flame"], 40, 7)
    weapon2 = Weapon((350, 400), player, 'Посох Эндера', screen, 20,
                     25, 0, textures["average_magic_stick"],
                     textures["enderperl"], 30, 10)
    weapon3 = WhiteNova((700, 400), player, 'White Nova', screen, 20,
                        25, 15, textures["white_nova"])
    weapon_enemy = Weapon((350, 400), player, 'Вражеский лук', screen, 25,
                          25, 0, textures["average_magic_stick"])
    weapons.extend([weapon, weapon2, weapon3])
    all_sprites.add(
        Portal(pygame.image.load('data/images/portal1.png'), (-80, 8 * 40), player, group, screen,
               all_sprites))
    hp_pot = Potion((460, 400), screen, ('hp', 25), 'Зелье здоровья',
                    20, player, textures["heal_potion"])
    Potion((440, 400), screen, ('mn', 25), 'Зелье маны',
           20, player, textures["mana_potion"])
    all_sprites.add(*group.sprites())

    emperor = Emperor((500, 400), player, 'Emperor', screen, 20, 25, 2,
                      textures["emperor"],
                      textures["emperor_projectile"])
    weapons.append(emperor)
    group.add(weapon)
    enemy = Enemy((250, 600), weapon_enemy)

    inventory = Inventory(player)
    all_sprites.add(player)
    camera = Camera()
    hp_im = textures["health_frame"]
    menu.pl = player

    running = True
    x_pos = 0
    fps = 60
    clock = pygame.time.Clock()
    sql_load(player)
    cur = pygame.image.load('data/images/cursor.png')
    while running:
        pygame.mouse.set_visible(False)
        key = pygame.key.get_pressed()
        if pause[0] is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause[0] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and player.inventory['weapons'] != []:
                        if isinstance(player.hand, Weapon) and player.mana >= player.hand.mana:
                            player.hand.shoot(event.pos, all_sprites)
                            player.mana -= player.hand.mana

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
            screen.blit(hp_im, pygame.Rect(180, 620, 20, 20))
            screen.blit(hp_im, pygame.Rect(608, 620, 20, 20))
        elif pause[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause[0] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        menu.update_btn(event.pos)
            screen.blit(menu.background, (0, 0))
        if pygame.mouse.get_focused():
            cur.set_colorkey((0, 0, 0, 0))
            screen.blit(cur, pygame.mouse.get_pos())
        clock.tick(fps)
        pygame.display.update()
        print(clock.get_fps())
    pygame.quit()
