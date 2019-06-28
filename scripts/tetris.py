import pygame
import random

pygame.font.init()

# Global variables
s_width = 800
s_height = 700
play_width = 300            # 300 // 10 = 30 width per block
play_height = 600           # 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) //2
top_left_y = s_height - play_height


# SHAPES

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

# Call this class a lot of times
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        # Getting the index of the shape within the shape_colors list
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos = {}):
    grid = [[(0,0,0) for _i in range(10)] for _i in range(20)]
    # What if there are already blocks. Draw them
    # Check locked position

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                key = locked_pos[(j, i)]
                grid[i][j] = key
    return grid


def get_random_shape():
    """Returns a random shape from the shapes list"""
    return Piece(5, 0, random.choice(shapes))


def draw_grid(surface, grid):
    """Draws the grid in the window"""
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)
    pygame.display.update()


def draw_window(surface, grid):
    """Draws the Tetris window on screen"""
    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 30))
    draw_grid(surface, grid)
    pygame.display.update()


def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_pieces = False
    run = True
    current_piece = get_random_shape()
    next_piece = get_random_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1