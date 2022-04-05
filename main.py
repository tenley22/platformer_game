# go to terminal (@ bottom of screen) and write "pip install pygame" after PS C: line
import pygame
import sprites
from settings import *


############################################################
############################################################

pygame.init()


def start_screen():
    # beginning screen
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Start Screen")
    clock = pygame.time.Clock()

    # press space to move on to level 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False


        screen.fill(PURPLE)
        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("End Screen")
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    quit()
        screen.fill(PURPLE)
        pygame.display.flip()
        clock.tick(FPS)


def level_1():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Platform Level 1")

    # card_list = card.load_grid_images(4, 14, x_margin, x_pad, y_margin, y_pad)
    # print(card_list)

    # sprite groups
    all_sprites = pygame.sprite.Group()
    layout_group = pygame.sprite.Group()

    layout = sprites.Level(TILE_SIZE, LAYOUT)
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


def level_2():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Platform Level 2")

    # card_list = card.load_grid_images(4, 14, x_margin, x_pad, y_margin, y_pad)
    # print(card_list)

    # sprite groups
    all_sprites = pygame.sprite.Group()
    layout_group = pygame.sprite.Group()

    layout = sprites.Level(TILE_SIZE, LAYOUT_2)
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
while True:
    level_1()
    game_over()

pygame.quit()
