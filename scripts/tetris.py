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

# Preview Rectangle constants
# Rectangle Positions
X_POS_RECT = 0.1 * S_WIDTH
Y_POS_RECT = 0.25 * S_HEIGHT
# Rectangle dimensions
RECT_WIDTH = PLAY_WIDTH * 0.3
RECT_HEIGHT = RECT_WIDTH * 2

# Global GRID Variables
ROWS = 20
COLUMNS = 10

TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) // 2 #250
TOP_LEFT_Y = S_HEIGHT - PLAY_HEIGHT     #100


# PIECE-SHAPES as matrices
S = [[0, 1, 1], [1, 1, 0]]
Z = [[1, 1, 0], [0, 1, 1]]
I = [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]
O = [[1, 1], [1, 1]]
J = [[0, 1, 0], [0, 1, 0], [1, 1, 0]]
L = [[0, 1, 0], [0, 1, 0], [0, 1, 1]]
T = [[0, 0, 0], [1, 1, 1], [0, 1, 0]]


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


class Piece():
    """This is a class of the pieces used in tetris"""
    def __init__(self, x_coordinate, y_coordinate, shape):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0
        self.rotation_state = self.shape


    def rotate_piece(self):
        """Rotates the piece clockwise once"""
        if self.shape == O:
            return

        if self.shape == (S or Z):
            reversed_shape = list(reversed(self.rotation_state))
            counterclockwise_rotated_piece = [list(i) for i in zip(*reversed_shape)]
            self.rotation_state = counterclockwise_rotated_piece
        else:
            counterclockwise_rotated_piece = [
                list(i) for i in list(zip(*self.rotation_state))[::-1]]
            self.rotation_state = counterclockwise_rotated_piece

        return


    def transform_shape_into_grid_positions(self):
        """Transforms the given shape into positions in the Playing GRID"""
        position = []
        # Gets the current shape of the piece (S, T, Z, L, etc.)
        # Gets the current rotation status of the given piece

        for i, line in enumerate(self.rotation_state):
            row = list(line)
            for j, column in enumerate(row):
                if column == 1:
                    position.append((self.x_coordinate + j, self.y_coordinate + i))

        return position


    def valid_space(self, grid):
        """Checks if the piece is within its boundaries and doesn't hit another piece"""
        accepted_positions = [
            [(j, i) for j in range(COLUMNS) if grid[i][j] == BLACK] for i in range(ROWS)]
        accepted_positions = [
            number for accepted_tuple in accepted_positions for number in accepted_tuple]
        formatted_shape = self.transform_shape_into_grid_positions()

        for pos in formatted_shape:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False

        return True


    def draw_next_shape(self, window, x_pos, y_pos):
        """Draws the next shape in the given box"""
        start_x = x_pos
        start_y = y_pos
        # piece_shape = self.shape
        # shape_rotation = piece_shape[self.rotation % len(piece_shape)]

        for i, line in enumerate(self.rotation_state):
            row = list(line)
            for j, column in enumerate(row):
                if column == 1:
                    pygame.draw.rect(
                        window,
                        self.color,
                        (start_x + j*10, start_y + i*10, 10, 10), 0)



class Variables():
    """This class holds the score for the game and its functions"""
    def __init__(self):
        """The standard values at the start of the game"""
        self.level = 1
        self.lines = 0
        self.score = 0


    def increase_score_for_cleared_lines(self, cleared_rows):
        """Increases the score with the formula 100*2^(cleared_rows-1)"""
        self.score += 100*(2**(cleared_rows - 1))


    def lines_cleared_count(self, lines_cleared):
        """Increases the amount of lines cleard in the Variables object"""
        self.lines += lines_cleared


    def get_level(self):
        """Returns the current level of the game"""
        return self.level


    def get_score(self):
        """Returns the current score"""
        return self.score


    def get_lines(self):
        """Returns the amount of lines cleared"""
        return self.lines


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


def draw_score_preview(surface, score_instance, next_shape):
    """Draws the rectangle to preview the next piece, show the score and the current level"""
    # Font settings
    score_font = DESCRIPTION_FONT.render("Score", 1, BLACK)
    level_font = DESCRIPTION_FONT.render("Level", 1, BLACK)
    lines_font = DESCRIPTION_FONT.render("Lines", 1, BLACK)
    preview_font = DESCRIPTION_FONT.render("Next", 1, BLACK)
    current_score_font = DESCRIPTION_FONT.render(str(score_instance.score), 1, BLUE)
    current_level_font = DESCRIPTION_FONT.render(str(score_instance.level), 1, BLUE)
    current_lines_font = DESCRIPTION_FONT.render(str(score_instance.lines), 1, BLUE)

    # Code for the Preview Rectangle
    pygame.draw.rect(
        surface,
        GRAY_BORDER,
        (X_POS_RECT, Y_POS_RECT, RECT_WIDTH, RECT_HEIGHT))


    # Print "Score" and dummy for the actual score
    surface.blit(score_font, (X_POS_RECT * 1.05, Y_POS_RECT * 1.05))
    surface.blit(current_score_font, (X_POS_RECT * 1.15, Y_POS_RECT * 1.15))

    # Print "Level" and a dummy for the current level
    surface.blit(level_font, (X_POS_RECT * 1.05, Y_POS_RECT * 1.25))
    surface.blit(current_level_font, (X_POS_RECT * 1.15, Y_POS_RECT * 1.35))

    # Print "Lines" and a dummy for cleared lines so far
    surface.blit(lines_font, (X_POS_RECT * 1.05, Y_POS_RECT * 1.45))
    surface.blit(current_lines_font, (X_POS_RECT * 1.15, Y_POS_RECT * 1.55))

    # Print "Next" as indication for the next comming piece
    f_width, _f_height = DESCRIPTION_FONT.size("Next")
    surface.blit(preview_font, (X_POS_RECT + f_width, Y_POS_RECT * 1.65))
    # Aligning the preview shape beneeth the "Next" text
    next_shape.draw_next_shape(WINDOW, X_POS_RECT + f_width / 1.5, Y_POS_RECT * 1.75)


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


def draw_text_middle(text, size, color, surface):
    """Prints a given text in bold in the middle of the screen,
    with the given attriburtes color and size"""
    font = pygame.font.SysFont('Arial', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, label.get_rect())


def get_random_piece():
    """Gets a ranom shape piece"""
    return Piece(5, 0, random.choice(SHAPES))


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
            pygame.quit()

        # Piece Actions
        if event.type == pygame.KEYDOWN:
            #Key press left - move piece to the left
            if event.key == pygame.K_LEFT:
                current_piece.x_coordinate -= 1
                if not current_piece.valid_space(grid):
                    current_piece.x_coordinate += 1
            #Key press right - move piece to the right
            elif event.key == pygame.K_RIGHT:
                current_piece.x_coordinate += 1
                if not current_piece.valid_space(grid):
                    current_piece.x_coordinate -= 1
            # Key press up - rotate piece clockwise
            elif event.key == pygame.K_UP:
                # if rotation is illegal, the before rotation state gets called
                before_rotation = current_piece.rotation_state
                current_piece.rotate_piece()
                if not current_piece.valid_space(grid):
                    current_piece.rotation_state = before_rotation

            # Key press down - move peace down
            if event.key == pygame.K_DOWN:
                while current_piece.valid_space(grid):
                    current_piece.y_coordinate += 1
                current_piece.y_coordinate -= 1
    return True


def main():
    """The main game function function"""
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_random_piece()
    next_piece = get_random_piece()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.99
    game_score = Variables()


    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Falling piece code
        if fall_speed > 0.25:
            fall_speed -= 0.005

        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y_coordinate += 1

            # get new piece when in locked position or hits the ground
            if not current_piece.valid_space(grid) and current_piece.y_coordinate > 0:
                current_piece.y_coordinate -= 1
                change_piece = True

        #Navigation with the keyboard
        if not keyboard_interaction_while_playing(current_piece, grid):
            pygame.display.quit()
            quit()

        shape_position = current_piece.transform_shape_into_grid_positions()

        # Draw the falling piece to the canvas
        for pos in shape_position:
            if pos[1] > -1:
                grid[pos[1]][pos[0]] = current_piece.color


        # Draw next piece once the piece hits the ground or other pieces
        if change_piece:
            for pos in shape_position:
                locked_pos = (pos[0], pos[1])
                locked_positions[locked_pos] = current_piece.color
            current_piece = next_piece
            next_piece = get_random_piece()
            change_piece = False

            # Check for cleared rows
            rows_cleared = clear_rows(grid, locked_positions)
            if rows_cleared > 0:
                game_score.increase_score_for_cleared_lines(rows_cleared)
                game_score.lines_cleared_count(rows_cleared)

         # Draw the window
        draw_window(WINDOW, grid)
        draw_score_preview(WINDOW, game_score, next_piece)
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
