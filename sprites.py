import pygame
from settings import *
import random


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)
        # try/accept stops program from crashing if there is an error

    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        """rectangle is a tuple with (x, y, x+offset, y+offset)"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0,
            y_margin=0, y_padding=0, width = None, height = None, colorkey = None):
        """Load a grid of images.
        x_margin is the space between the top of the sheet and top of the first
        row. x_padding is space between rows. Assumes symmetrical padding on
        left and right.  Same reasoning for y. Calls self.images_at() to get a
        list of images.
        """

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y.
        if width and height:
            x_sprite_size = width
            y_sprite_size = height
        else:
            x_sprite_size = (sheet_width - 2 * x_margin
                              - (num_cols - 1) * x_padding) / num_cols
            y_sprite_size = (sheet_height - 2 * y_margin
                              - (num_rows - 1) * y_padding) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        return self.images_at(sprite_rects, colorkey)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, tile_set, display):
        pygame.sprite.Sprite.__init__(self)
        self.tile_size = tile_size
        self.tile_set = tile_set
        self.display = display
        self.run_right_list = []
        self.run_left_list = []
        self.load_images()
        self.stand_right = self.run_right_list[1]
        self.stand_left = None
        self.load_images()
        self.image = self.run_right_list[1]
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.last = pygame.time.get_ticks()
        self.delay = 100
        self.current_frame = 0
        self.right = True
        self.left = False

        self.velocity_y = 0
        self.jumping = False
        self.falling = False
        self.tile_velocity = 0

    def update(self):
        # create deltas
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.right = True
            self.left = False
            dx = 5
            now = pygame.time.get_ticks()
            if now - self.last >= self.delay:
                self.last = now
                if self.current_frame >= len(self.run_right_list):
                    self.current_frame = 0
                    self.current_frame = (self.current_frame + 1)
                self.image = self.run_right_list[self.current_frame]
                self.current_frame += 1
        elif keys[pygame.K_LEFT]:
            self.right = False
            self.left = True
            dx = -5
            now = pygame.time.get_ticks()
            if now - self.last >= self.delay:
                self.last = now
                if self.current_frame >= len(self.run_left_list):
                    self.current_frame = 0
                    self.current_frame = (self.current_frame + 1)
                self.image = self.run_left_list[self.current_frame]
                self.current_frame += 1
        else:
            dx = 0
            self.current_frame = 0
            if self.right:
                self.image = self.stand_right
            elif self.left:
                self.image = self.stand_left
        if keys[pygame.K_UP] and not self.jumping and not self.falling:
            self.jumping = True
            dy = -30
        if not keys[pygame.K_UP]:
            self.jumping = False

        self.velocity_y += 1
        if self.velocity_y < 0:
            self.jumping = True
            self.falling = False
        else:
            self.jumping = False
            self.falling = True

        # terminal velocity
        if self.velocity_y >= 10:
            self.velocity_y = 10

        # update delta with velocity
        dy += self.velocity_y

        # CAMERA SCROLL
        if self.image_rect.x <= 10 and self.left and keys[pygame.K_LEFT]:
            dx = 0
            self.tile_velocity = 5
        elif self.image_rect.x >= WIN_WIDTH - 60 and self.right and keys[pygame.K_RIGHT]:
            dx = 0
            self.tile_velocity = -5
        else:
            self.tile_velocity = 0
        for tile in self.tile_set:
            tile[1][0] += self.tile_velocity
            # tile[1] gets the rectangle with x,y coordinate and [0] gets just the x coordinate to add velocity to

            # tiles in layout list
        for tile in self.tile_set:
            if tile[1].colliderect(self.image_rect.x+dx, self.image_rect.y, self.image_rect.width,
                                   self.image_rect.height):
                dx = 0
            if tile[1].colliderect(self.image_rect.x, self.image_rect.y+dy, self.image_rect.width,
                                   self.image_rect.height):
                # collision bottom of platform and top of player
                if dy < 0:
                    dy = tile[1].bottom - self.image_rect.top
                    self.velocity_y = 0
                    self.jumping = False
                # collision top of platform and bottom of player
                elif self.falling:
                    dy = tile[1].top - self.image_rect.bottom
                    self.velocity_y = 0
                    self.falling = False

        self.image_rect.x += dx
        self.image_rect.y += dy

        self.display.blit(self.image, self.image_rect)

    def load_images(self):
        dodo = SpriteSheet("assets/dodo.png")
        right_run_1 = dodo.image_at((4, 80, 45, 50), -1)
        self.run_right_list.append(right_run_1)
        right_run_2 = dodo.image_at((50, 75, 45, 50), -1)
        self.run_right_list.append(right_run_2)
        self.stand_right = right_run_2
        right_run_3 = dodo.image_at((100, 80, 45, 50), -1)
        self.run_right_list.append(right_run_3)

        left_run_1 = dodo.image_at((1, 200, 45, 60), -1)
        self.run_left_list.append(left_run_1)
        left_run_2 = dodo.image_at((50, 200, 45, 60), -1)
        self.run_left_list.append(left_run_2)
        self.stand_left = left_run_2
        left_run_3 = dodo.image_at((95, 200, 45, 60), -1)
        self.run_left_list.append(left_run_3)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, display, value, tile_set, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.display = display
        self.tile_set = tile_set
        self.tile_size = tile_size
        self.enemy_right_list = []
        self.enemy_left_list = []
        self.value = value
        self.load_images()
        self.image = self.enemy_left_list[1]
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.last = pygame.time.get_ticks()
        self.delay = 100
        self.current_frame = 0
        self.right = True
        self.left = False

        self.dx = 0
        self.dy = 0
        self.jumping = False
        self.falling = False

    def update(self):
        # make movement of the enemy more random or in opposite direction of player movement
        # & jumping/falling & collision

        if self.value > 0:
            self.right = True
            self.left = False
            self.dx = self.value
            self.falling = True
            self.jumping = False
            self.dy = 15

        elif self.value < 0:
            self.right = False
            self.left = True
            self.dx = self.value
            self.falling = True
            self.jumping = False
            self.dy = 15

        else:
            self.right = True
            self.left = False
            self.dx = 0
            self.falling = True
            self.jumping = False
            self.dy = 15

        for tile in self.tile_set:
            if tile[1].colliderect(self.image_rect.x+self.dx, self.image_rect.y, self.image_rect.width,
                                   self.image_rect.height):
                self.dy = -self.tile_size/8
                self.jumping = True
                self.falling = False
            if tile[1].colliderect(self.image_rect.x, self.image_rect.y + self.dy, self.image_rect.width,
                                   self.image_rect.height):
                if self.dy < 0:
                    self.dy = tile[1].bottom - self.image_rect.top
                    self.dy = 0
                    self.jumping = False
                    self.falling = True
                elif self.falling:
                    self.dy = tile[1].top - self.image_rect.bottom
                    self.dy = 0
                    self.falling = False

        self.image_rect.x += self.dx
        self.image_rect.y += self.dy

        self.display.blit(self.image, self.image_rect)

    def load_images(self):
        enemy_d = SpriteSheet("assets/dodo_enemy.png")
        enemy_right_1 = enemy_d.image_at((4, 80, 45, 50), -1)
        self.enemy_right_list.append(enemy_right_1)
        enemy_right_2 = enemy_d.image_at((50, 75, 45, 50), -1)
        self.enemy_right_list.append(enemy_right_2)
        enemy_right_3 = enemy_d.image_at((100, 80, 42, 50), -1)
        self.enemy_right_list.append(enemy_right_3)

        enemy_left_1 = enemy_d.image_at((1, 200, 45, 55), -1)
        self.enemy_left_list.append(enemy_left_1)
        enemy_left_2 = enemy_d.image_at((50, 200, 45, 55), -1)
        self.enemy_left_list.append(enemy_left_2)
        enemy_left_3 = enemy_d.image_at((95, 200, 45, 55), -1)
        self.enemy_left_list.append(enemy_left_3)


class Level(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.tile_sheet = SpriteSheet('assets/Ground.png')
        self.ground = self.tile_sheet.image_at((32, 0, 33, 33))
        self.water = self.tile_sheet.image_at((35, 35, 30, 30))
        self.sand = self.tile_sheet.image_at((0, 32, 33, 33))
        self.ground = pygame.transform.scale(self.ground, (size, size))
        self.water = pygame.transform.scale(self.water, (size, size))
        self.sand = pygame.transform.scale(self.sand, (size, size))
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.GroupSingle()
        self.tile_velocity = 0

        self.tile_list = []

        for i, row in enumerate(LAYOUT):
            for j, col in enumerate(row):
                x_val = j * size
                y_val = i * size

                if col == "1":
                    image_rect = self.ground.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.ground, image_rect)
                    self.tile_list.append(tile)

                if col == "2":
                    image_rect = self.water.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.water, image_rect)
                    self.tile_list.append(tile)

                if col == "3":
                    image_rect = self.sand.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.sand, image_rect)
                    self.tile_list.append(tile)

                if col == "P":
                    player = Player(TILE_SIZE, WIN_HEIGHT - TILE_SIZE, TILE_SIZE, self.tile_list, SCREEN)
                    player.image_rect.x = x_val
                    player.image_rect.y = y_val
                    self.player_group.add(player)

                if col == "E":
                    enemy = Enemy(TILE_SIZE, WIN_HEIGHT - TILE_SIZE, SCREEN, -3, self.tile_list, TILE_SIZE)
                    enemy.image_rect.x = x_val
                    enemy.image_rect.y = y_val
                    self.enemy_group.add(enemy)

    def update(self):
        for tile in self.tile_list:
            SCREEN.blit(tile[0], tile[1])

        #player_enemy_collide = pygame.sprite.groupcollide(self.player_group, self.enemy_group, True, True)
        #if player_enemy_collide:
            #stop the level and move to the game over screen

        self.player_group.update()
        self.enemy_group.update()

    def get_layout(self):
        return self.tile_list

