import random
import pygame

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
shape_colors = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 0, 255),
    (128, 0, 128)]
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


def convert_shape_format(shape):
    """Converts the shape in the above shape lists into computer readable format"""
    positions = []
    s_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(s_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] -2, pos[1] - 4)

    return positions

def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for _i in range(10)] for _i in range(20)]
    # What if there are already blocks. Draw them
    # Check locked position

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                key = locked_pos[(j, i)]
                grid[i][j] = key
    return grid


def valid_space(shape, grid):
    """Check if the shape is within the windows playing borders"""
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formated_shape = convert_shape_format(shape)

    for pos in formated_shape:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    """Check if you stacked too high"""
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def lost_procedure(window, score):
    """This function does a certain procedure after you lost the game"""
    draw_text_middle(window, "You lost the game", 80, (0, 255, 255))
    pygame.display.update()
    pygame.time.delay(1500)
    update_score(score)


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2),
        top_left_y + play_height / 2 - label.get_height()))


def get_random_shape():
    """Returns a random shape from the shapes list"""
    return Piece(5, 0, random.choice(shapes))


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Piece', 1, (255, 255, 255))

    # Place the preview right to the tetris grid
    start_x = top_left_x + play_width + 50
    start_y = top_left_y + play_height/2 - 100
    s_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(s_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                    (start_x + j * block_size,
                    start_y + i * block_size,
                    block_size,
                    block_size),
                    0)

    surface.blit(label, (start_x + 10, start_y - 30))


def draw_grid(surface, grid):
    """Draws the grid in the window"""
    start_x = top_left_x
    start_y = top_left_y
    color = (128, 128, 128)

    #Drawing the grid with certain color
    for i in range(len(grid)):
        pygame.draw.line(surface, color, (start_x, start_y + i * block_size),
                                            (start_x + play_width,
                                            start_y + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, color,
                            (start_x + j * block_size, start_y),
                            (start_x + j * block_size, start_y + play_height))


def clear_rows(grid, locked):
    """Clears rows when they are completly filled"""
    inc = 0 # how many rows have been cleared
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def draw_window(surface, grid, score = 0):
    """Draws the Tetris window on screen"""
    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 30))

    # Showing the score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: '+ str(score), 1, (255,255,255))

    # Place the preview right to the tetris grid
    start_x = top_left_x + play_width + 50
    start_y = top_left_y + play_height/2 - 100

    surface.blit(label, (start_x + 10, start_y + 170))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)


def update_score(newscore):
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    with open('scores.txt', 'w') as f:
        if int(score) > newscore:
            f.write(str(score))
        else:
            f.write(str(newscore))


def main(win):
    """The main function which runs the actuall game"""
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_pieces = False
    run = True
    current_piece = get_random_shape()
    next_piece = get_random_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        # need to constantly check if there were locked positions
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()        # Get the amount of time since last clock.tick()
        level_time += clock.get_rawtime()
        clock.tick()

        # Increasing the fall speed
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_pieces = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece -= 1

        shape_pos = convert_shape_format(current_piece)

        for i_tuple in shape_pos:
            x, y = i_tuple
            if y > -1:
                grid[y][x] = current_piece.color

        if change_pieces:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_random_shape()
            change_pieces = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            lost_procedure(win, score)
            run = False

    pygame.display.quit()

def main_menu(window):
    """The main menu function for the tetris game from which the original game is started"""
    run = True
    while run:
        window.fill((0, 0, 0))
        draw_text_middle(window, 'Press any key to play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(window)

    pygame.display.quit()


WIN = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(WIN)