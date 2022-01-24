# go to terminal (@ bottom of screen) and write "pip install pygame" after PS C: line
import pygame
import sprites
from settings import *


############################################################
############################################################

pygame.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Platformer")

# card_list = card.load_grid_images(4, 14, x_margin, x_pad, y_margin, y_pad)
# print(card_list)

dodo = sprites.SpriteSheet("assets/dodo.png")


right_run_1 = dodo.image_at((1, 200, 45, 60), -1)
right_run_2 = dodo.image_at((50, 200, 45, 60), -1)
right_run_3 = dodo.image_at((95, 200, 45, 60), -1)

# sprite groups
all_sprites = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
left_run_group = pygame.sprite.Group()
right_run_group = pygame.sprite.Group()

# player
player = dodo.image_at((59, 50, 29, 40), -1)
player_group.add(player)
all_sprites.add(player)

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
            if event.key == pygame.K_LEFT:
                left_run = sprites.LeftRun(player.rect.center)
                left_run_group.add(left_run)
                all_sprites.add(left_run)

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
