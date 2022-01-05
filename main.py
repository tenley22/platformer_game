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
x_margin = 5
y_margin = 8
x_pad = 22
y_pad = 4
dodo_1 = dodo.image_at((4, 40, 45, 130))
print(dodo_1)

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
    screen.blit(dodo_1, (100, 100))

    pygame.display.flip()

pygame.quit()
