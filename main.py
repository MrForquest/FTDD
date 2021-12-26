import pygame
from game_classes.GameGrid import Grid, GCell
from game_classes.Player import Player, Camera
from game_classes.Projectile import Projectile
from game_classes.Game_things import Thing, Weapon
from game_functions.Generating_level import generate_level

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся квадрат')
    size = width, height = 800, 700
    screen = pygame.display.set_mode(size)
    group = pygame.sprite.Group()
    things = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(generate_level(group))
    grid = Grid(20, 20, (0, 0), grid=group)
    player = Player((300, 300), all_sprites)
    thing = Thing((200, 400), player, 'Обычный класс вещи', screen)
    weapon = Weapon((300, 400), player, 'Оружие', screen, 20)
    all_sprites.add(thing, weapon)
    group.add(thing, weapon)
    proj = Projectile((80, -40), 30, 2, 20, True, all_sprites)
    all_sprites.add(player)
    all_sprites.add(proj)
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
                    player.inventory['weapons'][0].shoot(event.pos, all_sprites)
        screen.fill((0, 0, 0))

        player_coord = player.get_cords()
        camera.draw(screen, player_coord, all_sprites)

        all_sprites.update()

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
