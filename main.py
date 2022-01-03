# go to terminal (@ bottom of screen) and write "pip install pygame" after PS C: line
import pygame
import math
import random

# color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 180)
SKY = (143, 205, 255)

tile_size = 5
# math constants

# game constants
DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 500
FPS = 60

############################################################
############################################################

pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for row in range(1,DISPLAY_WIDTH//tile_size):
        for column in range(1, DISPLAY_HEIGHT//tile_size):


    screen.fill(SKY)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
