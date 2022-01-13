# go to terminal (@ bottom of screen) and write "pip install pygame" after PS C: line
import pygame
import sprites
from settings import *


############################################################
############################################################

pygame.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Card Game")

# card_list = card.load_grid_images(4, 14, x_margin, x_pad, y_margin, y_pad)
# print(card_list)

dodo = sprites.SpriteSheet("assets/dodo.png")
x_margin = 3
y_margin = 81
x_pad = 7
y_pad = 0
width = 50
height = 50
left_run_1 = dodo.image_at((4, 80, 45, 50), -1)
left_run_2 = dodo.image_at((50, 75, 45, 50), -1)
left_run_3 = dodo.image_at((100, 80, 45, 50), -1)
right_run_1 = dodo.image_at((1, 200, 45, 60), -1)
right_run_2 = dodo.image_at((50, 200, 45, 60), -1)
right_run_3 = dodo.image_at((95, 200, 45, 60), -1)

# sprite groups
all_sprites = pygame.sprite.Group()
platform_group = pygame.sprite.Group()

# platform
start_locations = [50, 350, 120, 400]
for start in start_locations:
    for row_index, row in enumerate(BLOCKS):
        # print(row_index, row)
        for col_index, col in enumerate(row):
            if col == 'x':
                x_pos = col_index * PLATFORM_W + start
                y_pos = row_index * PLATFORM_H + start//2
                platform = sprites.Platform(screen, x_pos, y_pos, BROWN)
                platform_group.add(platform)
                all_sprites.add(platform_group)
start_locations = [200, 550, 300, 700]
for start in start_locations:
    for row_index, row in enumerate(BLOCKS):
        # print(row_index, row)
        for col_index, col in enumerate(row):
            if col == 'x':
                x_pos = col_index * PLATFORM_W + start//2
                y_pos = row_index * PLATFORM_H + start
                platform = sprites.Platform(screen, x_pos, y_pos, BROWN_2)
                platform_group.add(platform)
                all_sprites.add(platform_group)
# left_run_list = dodo.load_grid_images(1, 3, x_margin, x_pad, y_margin, y_pad, width, height, -1)
# right_run_list = [pg.transform.flip(player, True, False) for player in left_run_list]

playing = True

clock = pygame.time.Clock()

while playing:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:    # allow for q key to quit the game
            if event.key == pygame.K_q:
                playing = False

    screen.fill(PURPLE)
    screen.blit(left_run_1, (100, 100))
    screen.blit(left_run_2, (150, 100))
    screen.blit(left_run_3, (200, 100))
    screen.blit(right_run_1, (100, 200))
    screen.blit(right_run_2, (150, 200))
    screen.blit(right_run_3, (200, 200))
    '''
    screen.blit(left_run_list[0], (100, 100))
    screen.blit(left_run_list[1], (180, 100))
    screen.blit(left_run_list[2], (260, 100))
    how to call w/ list thing
    '''
    # draw sprites
    platform_group.draw(screen)
    # update
    all_sprites.update()

    pygame.display.flip()

pygame.quit()
