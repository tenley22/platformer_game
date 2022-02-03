import pygame
from settings import *


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


class Level:
    def __init__(self, size):
        self.size = size
        tile_sheet = SpriteSheet('assets/Ground.png')
        block = tile_sheet.image_at((32, 0, 33, 33))
        flower = tile_sheet.image_at((0, 0, 30, 30))
        water = tile_sheet.image_at((35, 35, 30, 30))
        sand = tile_sheet.image_at((0, 32, 33, 33))
        block = pygame.transform.scale(block, (size, size))
        flower = pygame.transform.scale(flower, (size, size))
        water = pygame.transform.scale(water, (size, size))
        sand = pygame.transform.scale(sand, (size, size))

        self.tile_list = []

        for i, row in enumerate(LAYOUT):
            for j, col in enumerate(row):
                x_val = j * size
                y_val = i * size

                if col == "1":
                    image_rect = block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile1 = (block, image_rect)
                    self.tile_list.append(tile1)

                if col == "2":
                    image_rect = flower.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile2 = (flower, image_rect)
                    self.tile_list.append(tile2)

                if col == "3":
                    image_rect = water.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile3 = (water, image_rect)
                    self.tile_list.append(tile3)

                if col == "4":
                    image_rect = sand.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile4 = (sand, image_rect)
                    self.tile_list.append(tile4)

    def update(self):
        for tile in self.tile_list:
            SCREEN.blit(tile[0], tile[1], tile[2], tile[3])

    def get_layout(self):
        return self.tile_list


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, tile_set, display):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
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
        self.last = pygame.time.get_ticks()
        self.delay = 100
        self.current_frame = 0
        self.right = True
        self.left = False

        self.velocity_y = 0
        self.jumping = False
        self.falling = False

    def update(self):
        # create deltas
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.right = True
            self.left = False
            dx = 5
            now = pygame.get_ticks()
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
            now = pygame.get_ticks()
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
        if keys[pygame.K_SPACE] and not self.jumping and not self.falling:
            self.jumping = True
            dy = -10
        if not keys[pygame.K_SPACE]:
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

        # tiles in layout list
        for tile in self.tile_set:
            if tile[1].colliderect(self.image_rect.x+dx,self.image_rect.y,self.image_rect.width,self.image_rect.height):
                dx = 0
            if tile[1].colliderect(self.image_rect.x,self.image_rect.y+dy,self.image_rect.width,self.image_rect.height):
                # collision bottom of platform and top of player
                if self.jumping:
                    dy = tile[1].bottom - self.image_rect.top
                    self.velocity_y = 0
                    self.falling = True
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
        left_run_1 = dodo.image_at((4, 80, 45, 50), -1)
        self.run_left_list.append(left_run_1)
        left_run_2 = dodo.image_at((50, 75, 45, 50), -1)
        self.run_left_list.append(left_run_2)
        self.stand_left = left_run_2
        left_run_3 = dodo.image_at((100, 80, 45, 50), -1)
        self.run_left_list.append(left_run_3)

        right_run_1 = dodo.image_at((1, 200, 45, 60), -1)
        self.run_right_list.append(right_run_1)
        right_run_2 = dodo.image_at((50, 200, 45, 60), -1)
        self.run_right_list.append(right_run_2)
        self.stand_right = right_run_2
        right_run_3 = dodo.image_at((95, 200, 45, 60), -1)
        self.run_right_list.append(right_run_3)

