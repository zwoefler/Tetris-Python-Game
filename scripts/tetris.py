"""A Python Tetris game"""
import random
import pygame

# Disable all the no-member violations in this function
# pylint: disable=no-member

pygame.font.init()

# Global variables
S_WIDTH = 800
S_HEIGHT = 700
PLAY_WIDTH = 300            # 300 // 10 = 30 width per block
PLAY_HEIGHT = 600           # 600 // 20 = 30 height per block
BLOCK_SIZE = 30
DESCRIPTION_FONT = pygame.font.SysFont('Arial', int(BLOCK_SIZE * 0.5))


# Global GRID Variables
ROWS = 20
COLUMNS = 10

TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) // 2 #250
TOP_LEFT_Y = S_HEIGHT - PLAY_HEIGHT     #100


# PIECE-SHAPES

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
SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (0, 191, 255),
    (255, 20, 147),
    (255, 255, 0),
    (190, 190, 190)]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY_BORDER = (191, 191, 191)
TRANSPARENT_BLACK = (0, 0, 0, 0)
BORDER_COLOR = GRAY_BORDER
# index 0 - 6 represent shape

def create_grid(locked_positions):
    """Creates the 20 x 10 playing GRID"""
    grid = [[BLACK for x in range(COLUMNS)] for x in range(ROWS)]

    for i, _row in enumerate(grid):
        for j, _column in enumerate(grid[i]):
            if (j, i) in locked_positions:
                key = locked_positions[(j, i)]
                grid[i][j] = key
    return grid


def draw_grid(surface, row, column):
    """Draws the GRID on to the surface"""
    start_x = TOP_LEFT_X
    start_y = TOP_LEFT_Y
    for i in range(row):
        pygame.draw.line(surface, TRANSPARENT_BLACK, (start_x, start_y + i * 30),
                         (start_x + PLAY_WIDTH, start_y + i * 30)) #horizontal lines
        for j in range(column):
            pygame.draw.line(surface, TRANSPARENT_BLACK,
                             (start_x + j * 30, start_y),
                             (start_x + j * 30, start_y + PLAY_HEIGHT)) #vertical lines


def draw_window(surface, grid):
    """Draws the window"""
    surface.fill(BLACK)
    # Tetris Title
    font = pygame.font.SysFont('Arial', 60)
    label = font.render('Tetris', 1, WHITE)

    surface.blit(label, (TOP_LEFT_X+ PLAY_WIDTH / 2 - (label.get_width() / 2), 30))
    for i, _ in enumerate(grid):
        for j, _ in enumerate(grid[i]):
            pygame.draw.rect(surface, grid[i][j],
                             (TOP_LEFT_X + j * 30, TOP_LEFT_Y + i * 30, 30, 30), 0)

    #draw grid and border
    draw_grid(surface, ROWS, COLUMNS)
    pygame.draw.rect(surface, BORDER_COLOR, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)


def draw_score_preview(surface, score, level, lines):
    """Draws the rectangle to preview the next piece, show the score and the current level"""
    # Rectangle Positions
    x_pos_rect = 0.1 * S_WIDTH
    y_pos_rect = 0.25 * S_HEIGHT
    # Rectangle dimensions
    rect_width = PLAY_WIDTH * 0.3
    rect_height = rect_width * 2

    # Font settings
    score_font = DESCRIPTION_FONT.render('Score', 1, BLACK)
    level_font = DESCRIPTION_FONT.render('Level', 1, BLACK)
    lines_font = DESCRIPTION_FONT.render('Lines', 1, BLACK)
    current_score_font = DESCRIPTION_FONT.render(str(score), 1, BLUE)
    current_level_font = DESCRIPTION_FONT.render(str(level), 1, BLUE)
    current_lines_font = DESCRIPTION_FONT.render(str(lines), 1, BLUE)

    # Code for the Preview Rectangle
    pygame.draw.rect(
        surface,
        GRAY_BORDER,
        (x_pos_rect, y_pos_rect, rect_width, rect_height))


    # Print "Score" and dummy for the actual score
    surface.blit(score_font, (x_pos_rect * 1.05, y_pos_rect * 1.05))
    surface.blit(current_score_font, (x_pos_rect * 1.15, y_pos_rect * 1.15))

    # Print "Level" and a dummy for the current level
    surface.blit(level_font, (x_pos_rect * 1.05, y_pos_rect * 1.25))
    surface.blit(current_level_font, (x_pos_rect * 1.15, y_pos_rect * 1.35))

    # Print "Lines" and a dummy for cleared lines so far
    surface.blit(lines_font, (x_pos_rect * 1.05, y_pos_rect * 1.45))
    surface.blit(current_lines_font, (x_pos_rect * 1.15, y_pos_rect * 1.55))


def draw_next_shape(preview_piece, window):
    """Draws the next shape in the given box"""
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, WHITE)

    start_x = TOP_LEFT_X + PLAY_WIDTH + 50
    start_y = TOP_LEFT_Y + PLAY_HEIGHT/2 -100
    piece = preview_piece["shape"]
    piece_format = piece[preview_piece["rotation"] % len(piece)]

    for i, line in enumerate(piece_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(
                    window,
                    preview_piece["color"],
                    (start_x + j*30, start_y + i*30, 30, 30), 0)

    window.blit(label, (start_x + 10, start_y - 30))

def clear_rows(grid, locked_positions):
    """Clears the rows, moves down the remaining ones on top and counts the score up"""
    rows_cleared = 0

    for i in range(len(grid) -1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            rows_cleared += 1
            # Since the row is cleared, the position is removed from the locked positions
            ind = i
            for j in range(len(row)):
                del locked_positions[(j, i)]

    # Move all the rows above the cleared row down
    if rows_cleared > 0:
        for key in sorted(list(locked_positions), key=lambda x: x[1])[::-1]:
            x_pos, y_pos = key
            if y_pos < ind:
                new_key = (x_pos, y_pos + rows_cleared)
                locked_positions[new_key] = locked_positions.pop(key)

    return rows_cleared


def transform_shape_into_grid_positions(shape):
    """Transforms the given shape into positions in the Playing GRID"""
    position = []
    # Gets the current shape of the piece (S, T, Z, L, etc.)
    piece_shape = shape["shape"]
    # Gets the current rotation status of the given piece
    shape_rotation = piece_shape[shape["rotation"] % len(piece_shape)]

    for i, line in enumerate(shape_rotation):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                position.append((shape["x_coordinate"] + j, shape["y_coordinate"] + i))

    for i, pos in enumerate(position):
        position[i] = (pos[0] - 2, pos[1] - 4)

    return position


def draw_text_middle(text, size, color, surface):
    """Prints a given text in bold in the middle of the screen,
    with the given attriburtes color and size"""
    font = pygame.font.SysFont('Arial', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, label.get_rect())


def get_random_piece():
    """Gets a ranom shape piece"""
    piece_shape = random.choice(SHAPES)
    shape_color = SHAPE_COLORS[SHAPES.index(piece_shape)]

    piece = {
        "x_coordinate": 5,
        "y_coordinate": 0,
        "shape": piece_shape,
        "color": shape_color,
        "rotation": 0
    }
    return piece


def valid_space(piece, grid):
    """Checks if the piece is within its boundaries and doesn't hit another piece"""
    accepted_positions = [
        [(j, i) for j in range(COLUMNS) if grid[i][j] == BLACK] for i in range(ROWS)]
    accepted_positions = [
        number for accepted_tuple in accepted_positions for number in accepted_tuple]
    formatted_shape = transform_shape_into_grid_positions(piece)

    for pos in formatted_shape:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def has_lost(locked_positions):
    """Checks weather the player stacked too high"""
    for pos in locked_positions:
        if pos[1] < 1:
            return True
    return False


def keyboard_interaction_while_playing(current_piece, grid):
    """Handlerfunction for the keyboard interaction"""
    # Keyboard interaction with the keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            return run

        # Piece Actions
        if event.type == pygame.KEYDOWN:
            #Key press left - move piece to the left
            if event.key == pygame.K_LEFT:
                current_piece["x_coordinate"] -= 1
                if not valid_space(current_piece, grid):
                    current_piece["x_coordinate"] += 1
            #Key press right - move piece to the right
            elif event.key == pygame.K_RIGHT:
                current_piece["x_coordinate"] += 1
                if not valid_space(current_piece, grid):
                    current_piece["x_coordinate"] -= 1
            # Key press up - rotate piece clockwise
            elif event.key == pygame.K_UP:
                current_piece["rotation"] -= 1
                if not valid_space(current_piece, grid):
                    current_piece["rotation"] += 1

            # Key press down - move peace down
            if event.key == pygame.K_DOWN:
                while valid_space(current_piece, grid):
                    current_piece["y_coordinate"] += 1
                current_piece["y_coordinate"] -= 1
    return True


def main():
    """The main game function function"""

    locked_positions = {}
    grid = create_grid(locked_positions)
    level = 1
    lines = 0
    change_piece = False
    run = True
    current_piece = get_random_piece()
    next_piece = get_random_piece()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.99
    score = 0


    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Falling piece code
        if fall_speed > 0.15:
            fall_speed -= 0.005

        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece["y_coordinate"] += 1

            # get new piece when in locked position or hits the ground
            if not valid_space(current_piece, grid) and current_piece["y_coordinate"] > 0:
                current_piece["y_coordinate"] -= 1
                change_piece = True

        #Navigation with the keyboard
        if not keyboard_interaction_while_playing(current_piece, grid):
            pygame.display.quit()
            quit()

        shape_position = transform_shape_into_grid_positions(current_piece)

        # Draw the falling piece to the canvas
        for pos in shape_position:
            if pos[1] > -1:
                grid[pos[1]][pos[0]] = current_piece["color"]


        # Draw next piece once the piece hits the ground or other pieces
        if change_piece:
            for pos in shape_position:
                locked_pos = (pos[0], pos[1])
                locked_positions[locked_pos] = current_piece["color"]
            current_piece = next_piece
            next_piece = get_random_piece()
            change_piece = False

            # Check for cleared rows
            rows_cleared = clear_rows(grid, locked_positions)
            if rows_cleared > 0:
                score += 10 * rows_cleared
                lines += rows_cleared

         # Draw the window
        draw_window(WINDOW, grid)
        draw_next_shape(next_piece, WINDOW)
        draw_score_preview(WINDOW, score, level, lines)
        pygame.display.update()

        # Check if user lost, stacked too high
        if has_lost(locked_positions):
            run = False


    # Once the loop is left, show the message and wait 2 seconds
    # until jumping back to the main menu
    draw_text_middle("You lost the game", 20, WHITE, WINDOW)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    """The main menu of the tetris game"""
    run = True
    while run:
        WINDOW.fill(BLACK)
        draw_text_middle('Press any key to begin', 60, WHITE, WINDOW)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


WINDOW = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('Tetris')

main_menu() # start the game
