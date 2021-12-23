import pygame
from game_classes.GameGrid import Grid, GCell
from game_classes.Player import Player, Camera

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся квадрат')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    group = pygame.sprite.Group()
    group.add(GCell((0, 0), True))
    group.add(GCell((0, 100), True))
    group.add(GCell((0, 160), True))
    group.add(GCell((100, 0), True))
    group.add(GCell((160, 0), True))
    group.add(GCell((140, 140), True))
    group.add(GCell((280, 140), True))
    group.add(GCell((360, 140), True))
    all_sprites = pygame.sprite.Group(*group.sprites())
    print(len(all_sprites))
    grid = Grid(20, 20, (0, 0), grid=group)
    player = Player(screen, (400, 200), all_sprites)
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
        screen.fill((0, 0, 0))

        all_sprites.update()

        player_coord = player.get_cords()
        camera.draw(screen, player_coord, all_sprites)

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
