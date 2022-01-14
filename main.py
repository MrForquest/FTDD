import pygame
from game_classes.GameGrid import Grid, GCell
from game_classes.Player import Player, Camera
from game_classes.Game_things import Thing, Weapon, Emperor
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

    all_sprites.add(generate_level(group))
    grid = Grid(20, 20, (0, 0), grid=group)
    player = Player((250, 300), all_sprites)
    for i in group.sprites():
        if isinstance(i, NPC):
            i.player = player
    weapon = Weapon((300, 400), player, 'Обычный лук', screen, 20,
                    25, pygame.image.load('data/images/average_bow.png'))
    weapon2 = Weapon((350, 400), player, 'Обычный лук', screen, 20,
                     25, pygame.image.load('data/images/average_magic_stick.png'))
    group.add(Portal(pygame.image.load('data/images/portal1.png'), (0, 8 * 40), player, group, screen, all_sprites))
    all_sprites.add(*group.sprites())

    all_sprites.add(weapon, weapon2)

    all_sprites.add(Emperor((500, 400), player, 'Emperor', screen, 20,
                            pygame.image.load('data/images/average_bow.png')))
    all_sprites.add(weapon)
    group.add(weapon)

    inventory = Inventory(player)
    all_sprites.add(player)
    all_sprites.add(enemies)
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
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    inventory.slot_use = (inventory.slot_use + 1) % 4
                    inventory.update(screen)
                elif event.y < 0:
                    inventory.slot_use = (inventory.slot_use - 1) % 4
                    inventory.update(screen)
        screen.fill((0, 0, 0))

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
