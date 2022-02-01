# go to terminal (@ bottom of screen) and write "pip install pygame" after PS C: line
import pygame
import sprites
from settings import *


############################################################
############################################################

pygame.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Platform")

# card_list = card.load_grid_images(4, 14, x_margin, x_pad, y_margin, y_pad)
# print(card_list)

#player = sprites.Player(100, 100, TILE_SIZE, LAYOUT, screen)
# sprite groups
all_sprites = pygame.sprite.Group()
platform_group = pygame.sprite.Group()

# left_run_list = dodo.load_grid_images(1, 3, x_margin, x_pad, y_margin, y_pad, width, height, -1)
# right_run_list = [pg.transform.flip(player, True, False) for player in left_run_list]

layout = sprites.Level()

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

    screen.fill(BLUE)
    # screen.blit(left_run_1, (100, 100))
    # screen.blit(left_run_2, (150, 100))
    # screen.blit(left_run_3, (200, 100))
    # screen.blit(right_run_1, (100, 200))
    # screen.blit(right_run_2, (150, 200))
    # screen.blit(right_run_3, (200, 200))

    # draw sprites
    platform_group.draw(screen)
    # update
    all_sprites.update()
    layout.update()

    pygame.display.flip()

pygame.quit()