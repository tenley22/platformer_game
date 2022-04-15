# go to terminal (@ bottom of screen) and write "pip install pygame" after PS C: line
import pygame
import sprites
from settings import *


############################################################
############################################################

pygame.init()
# initialize all game elements
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("New Game")
game_layout = sprites.Level(TILE_SIZE, LAYOUT)
layout_list = game_layout.get_layout()
player_group = pygame.sprite.Group()
player = sprites.Player(TILE_SIZE, WIN_HEIGHT - TILE_SIZE, TILE_SIZE, layout_list, SCREEN)
player_group.add(player)


def start_screen():
    # beginning screen
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Start Screen")
    clock = pygame.time.Clock()

    # press space to move on to level 1
    start_text1 = 'press space key to begin'
    start_text2 = 'or Q to quit'
    font = pygame.font.SysFont('Arial', 30, True, False)
    text1 = font.render(start_text1, True, WHITE)
    text2 = font.render(start_text2, True, BG)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                elif event.key == pygame.K_q:
                    quit()
        screen.fill(PURPLE)

        screen.blit(text1, [100, 100])
        screen.blit(text2, [200, 200])

        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("End Screen")
    clock = pygame.time.Clock()

    running = True
    end_text1 = 'game over! press Q to quit'
    font = pygame.font.SysFont('Arial', 30, True, False)
    text1 = font.render(end_text1, True, BLACK)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                elif event.key == pygame.K_q:
                    quit()
        screen.fill(PURPLE)

        screen.blit(text1, [100, 100])

        pygame.display.flip()
        clock.tick(FPS)


def reset_level(new_level):
    global player, player_group, game_layout, layout_list
    game_layout.blocks_group.empty()
    player_group.empty()

    # create new level
    game_layout.create_layout(new_level)
    layout_list = game_layout.get_layout()
    player_group = pygame.sprite.Group()
    player = sprites.Player(TILE_SIZE, WIN_HEIGHT - TILE_SIZE, TILE_SIZE, layout_list, SCREEN)
    player_group.add(player)

    return layout_list


def game():
    global player, player_group, game_layout, screen

    level = 1
    last_level = 2

    layout_list = reset_level(level)
    platforms = game_layout.get_groups()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # sprite groups
    all_sprites = pygame.sprite.Group()
    layout_group = pygame.sprite.Group()


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

        for tile in layout_list:
            if tile[1].colliderect(player.rect.x + 3, player.rect.y,
                                   player.rect.width, player.rect.height) and len(tile) == 3:
                level += 1
                if level <= last_level:
                    layout_list = reset_level(level)
                else:
                    playing = False

        screen.fill(BG)

        # update
        all_sprites.update()
        player.update()
        platforms.update(screen)

        pygame.display.flip()


running = True
start_screen()
while running:
    game()
    game_over()

pygame.quit()
