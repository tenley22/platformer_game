# go to terminal (@ bottom of screen) and write "pip install pygame" after PS C: line
import pygame
import sprites
from settings import *


############################################################
############################################################

pygame.init()


def start_screen():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    text_object = FONT.render(f"Press Space to Begin", True, WHITE)
    text_rect = text_object.get_rect()
    text_rect.center = 300, 350

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

        screen.fill(BLACK)

        text_object = FONT.render(f"Press Space to Begin", True, WHITE)
        screen.blit(text_object, text_rect)

        pygame.display.flip()

        clock.tick(FPS)


def level_1():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Platform")

    # card_list = card.load_grid_images(4, 14, x_margin, x_pad, y_margin, y_pad)
    # print(card_list)

    # sprite groups
    all_sprites = pygame.sprite.Group()
    layout_group = pygame.sprite.Group()

    layout = sprites.Level(TILE_SIZE)
    layout_list = layout.get_layout()
    layout_group.add(layout)

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

        screen.fill(BG)

        # update
        all_sprites.update()
        layout_group.update()

        pygame.display.flip()


start_screen()

pygame.quit()
