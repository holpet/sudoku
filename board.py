import pygame
import constants
import game
import random

global BOARD  # Board that changes values based on user input
global ORIG_BOARD  # To compare user input against BOARD
global X_BOARD  # To show incorrect user input when solving
global tmp_BOARD  # To show processing of input when solving
global LAST_USER_BOARD  # Image of the last user board before clicking "solve"
global HINT_DICT  # Holds values of hints for current board


# --------------------------------------------------------------------------------------------
# READ FILE AND PRINT BOARD #

def print_board(board):
    for i in board:
        print(i)


def chunks(lst):
    for i in range(0, 81, 9):
        yield lst[i:i + 9]


def read_board(filename, num):
    with open(filename, 'r') as f:
        for i, line in enumerate(f, start=1):
            if i == num:
                lst = line.split()
                f.close()
                return list(chunks(lst))
    f.close()
    return False


def write_board(filename, brd):
    text = ''
    for array in brd:
        for elem in array:
            text += ' '.join(elem) + ' '
    with open(filename, 'w+') as f:
        f.write(text)
        f.close()


def isSolvable(brd):
    ctn = 0
    for array in brd:
        for elem in array:
            if elem != 0 and elem != '0':
                ctn += 1
    # The smallest number of starting clues should be 17 for a human to be able to solve a Sudoku
    if ctn >= 17:
        return True
    return False


def read_random_board(filename):
    num_of_lines = len(open(filename).readlines())
    num = random.randint(1, num_of_lines)
    print('Random line: ' + str(num))
    return read_board(filename, num)


# --------------------------------------------------------------------------------------------
# CLEAR & COPY BOARD

def clear_board(bo):
    for i in range(constants.NUMBER_OF_BLOCKS_ROW):
        for j in range(constants.NUMBER_OF_BLOCKS_COL):
            bo[i][j] = '0'


def copy_board(bo):
    sb = [[0 for j in range(constants.NUMBER_OF_BLOCKS_COL)] for i in range(constants.NUMBER_OF_BLOCKS_ROW)]
    for i in range(constants.NUMBER_OF_BLOCKS_ROW):
        for j in range(constants.NUMBER_OF_BLOCKS_COL):
            sb[i][j] = bo[i][j]
    return sb


# --------------------------------------------------------------------------------------------
# DRAWING BOARD

def draw_highlight(surface, pos_x, pos_y, color):
    rect_x = pos_x * constants.BLOCK_WIDTH + constants.SIDE_SPACE
    rect_y = pos_y * constants.BLOCK_HEIGHT + constants.TOP_SPACE
    myrect_light = pygame.Rect(rect_x, rect_y, constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
    pygame.draw.rect(surface, color, myrect_light)


def draw_grid(surface):
    for i in range(constants.NUMBER_OF_BLOCKS_ROW + 1):
        new_W = round(i * constants.BLOCK_WIDTH) + constants.SIDE_SPACE
        new_H = round(i * constants.BLOCK_HEIGHT) + constants.TOP_SPACE
        # COL/ROW LINES (start pos) (end pos)
        if i % 3 == 0:
            pygame.draw.line(surface, constants.BLACK, (new_W, constants.TOP_SPACE),
                             (new_W, constants.BLOCK_WIDTH * constants.NUMBER_OF_BLOCKS_ROW + constants.TOP_SPACE), 5)
            pygame.draw.line(surface, constants.BLACK, (constants.SIDE_SPACE, new_H),
                             (constants.BLOCK_WIDTH * constants.NUMBER_OF_BLOCKS_COL + constants.SIDE_SPACE, new_H), 5)
        else:
            pygame.draw.line(surface, constants.BLACK, (new_W, constants.TOP_SPACE),
                             (new_W, constants.BLOCK_WIDTH * constants.NUMBER_OF_BLOCKS_ROW + constants.TOP_SPACE), 2)
            pygame.draw.line(surface, constants.BLACK, (constants.SIDE_SPACE, new_H),
                             (constants.BLOCK_WIDTH * constants.NUMBER_OF_BLOCKS_COL + constants.SIDE_SPACE, new_H), 2)


# --------------------------------------------------------------------------------------------


class Tile:

    # Construct indices and tile content (num)
    def __init__(self, row, col, num):
        self.row = row
        self.col = col
        self.num = num

    def draw_tile(self, surface):
        # Coordinates and W/H of the tiles
        rect_x = self.row * constants.BLOCK_WIDTH + constants.SIDE_SPACE
        rect_y = self.col * constants.BLOCK_HEIGHT + constants.TOP_SPACE
        myrect = pygame.Rect(rect_x, rect_y, constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)

        # General text/font controls
        font = pygame.font.SysFont("Arial", 38)
        text_black = font.render(self.num, True, constants.BLACK, None)
        text_blue = font.render(self.num, True, constants.DARK_BLUE, None)
        text_zero = font.render('', True, constants.DARK_BLUE, None)

        text_x = rect_x + constants.BLOCK_WIDTH / 2 - text_black.get_rect().width / 2
        text_y = rect_y + constants.BLOCK_HEIGHT / 2 - text_black.get_rect().height / 2

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #

        # Color the tiles
        if ((self.col <= 2 or self.col >= 6) and (self.row <= 2 or self.row >= 6)) or (
                3 <= self.col <= 5 and 3 <= self.row <= 5):
            pygame.draw.rect(surface, constants.LIGHT_GREY, myrect)
        else:
            pygame.draw.rect(surface, constants.GREY, myrect)

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #

        # Draw green/red for correct/incorrect inputs
        if X_BOARD[self.col][self.row] == 'X':
            draw_highlight(surface, self.row, self.col, constants.GREEN)
        if tmp_BOARD[self.col][self.row] == 'G':
            draw_highlight(surface, self.row, self.col, constants.GREEN)
        if tmp_BOARD[self.col][self.row] == 'R':
            draw_highlight(surface, self.row, self.col, constants.RED)

        # Draw highlight on currently used tile
        if int(game.SET_CURRENT[0]) == self.row and int(game.SET_CURRENT[1] == self.col) and game.visualization is False:
            draw_highlight(surface, game.SET_CURRENT[0], game.SET_CURRENT[1], constants.LIGHTER_BLUE)

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #

        # Add numbers on the board
        if self.num == '0' or self.num == 0:
            surface.blit(text_zero, (text_x, text_y))
        else:
            # If the text is input, validate it in blue
            if (ORIG_BOARD[self.col][self.row] == 0 or ORIG_BOARD[self.col][self.row] == '0') and not game.visualization:
                surface.blit(text_blue, (text_x, text_y))
            else:
                surface.blit(text_black, (text_x, text_y))

    def draw_hint(self, surface):
        if not HINT_DICT:
            return False
        rect_x = self.row * constants.BLOCK_WIDTH + constants.SIDE_SPACE
        rect_y = self.col * constants.BLOCK_HEIGHT + constants.TOP_SPACE
        font = pygame.font.SysFont("Arial", 12)
        ctn = 0
        for i in range(3):
            for j in range(3):
                ctn += 1
                if ctn in HINT_DICT[(self.col, self.row)]:
                    text = font.render(str(ctn), True, constants.BLACK, None)
                    t_x = rect_x + (constants.BLOCK_WIDTH / 3)*(j+1) - text.get_rect().width / 2 - 7
                    t_y = rect_y + (constants.BLOCK_HEIGHT / 3)*(i+1) - text.get_rect().height / 2 - 7
                    surface.blit(text, (t_x, t_y))
        return True

    def __repr__(self):
        return 'Test("%d","%d", "%d")' % (self.row, self.col, self.num)

    def __str__(self):
        return "Tile -> Row: " + str(self.row) + ", Col: " + str(self.col) + ", Num: " + str(self.num)


class Board:

    def __init__(self):
        self.tiles = [[Tile(i, j, '0') for j in range(constants.NUMBER_OF_BLOCKS_COL)] for i in
                      range(constants.NUMBER_OF_BLOCKS_ROW)]

    def draw_board(self, surface, board):
        for j, tile in enumerate(board):
            for i, tile_content in enumerate(tile):
                self.tiles[i][j] = Tile(i, j, tile_content)
                self.tiles[i][j].draw_tile(surface)
                # print(self.tiles[i][j])
                self.tiles[i][j].draw_hint(surface)
        draw_grid(surface)
        return self.tiles
