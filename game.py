import pygame
import time
import collections

import constants
import solver
import features
import board
import event_handler

global SET_CURRENT  # Keeps track of current position on the board based on user input
SET_CURRENT = [0, 0]
global visualization
visualization = False
global resetter
resetter = False
global visu_block
visu_block = True
global own_game
own_game = False


# --------------------------------------------------------------------------------------------
# FUNCTIONS: RESET, SOLVE, HINT...

def reset_game():
    global visualization
    global resetter
    visualization = False
    for i in range(constants.NUMBER_OF_BLOCKS_ROW):
        for j in range(constants.NUMBER_OF_BLOCKS_COL):
            board.BOARD[i][j] = board.ORIG_BOARD[i][j]
            board.X_BOARD[i][j] = '0'
            board.tmp_BOARD[i][j] = '0'
    features.STRIKES = 0
    features.TIMER = 0
    resetter = True
    board.print_board(board.ORIG_BOARD)


def reset_timer_strikes():
    features.STRIKES = 0
    features.TIMER = 0


def reset_all():
    for i in range(constants.NUMBER_OF_BLOCKS_ROW):
        for j in range(constants.NUMBER_OF_BLOCKS_COL):
            board.ORIG_BOARD[i][j] = '0'
    reset_game()


def load_initial_game():
    board.BOARD = board.read_board(constants.GAME_FILE, 1)
    board.ORIG_BOARD = board.copy_board(board.BOARD)
    board.print_board(board.BOARD)


def load_random_game():
    board.BOARD = board.read_random_board(constants.GAME_FILE)
    board.ORIG_BOARD = board.copy_board(board.BOARD)
    board.print_board(board.BOARD)


def load_own_game():
    board.BOARD = board.read_random_board(constants.GAME_FILE_OWN)
    board.ORIG_BOARD = board.copy_board(board.BOARD)
    board.print_board(board.BOARD)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #

def solve_game():
    sb = board.copy_board(board.ORIG_BOARD)
    return solver.solve(sb)


# Compare user input (if unfinished) and the correct solution to the game.
# Incorrect input mark as 'X'.
def draw_solved_game():
    # copy board so ORIG_BOARD is not changed
    solved_board = solve_game()

    # solve the board values
    if solved_board:
        for i in range(constants.NUMBER_OF_BLOCKS_ROW):
            for j in range(constants.NUMBER_OF_BLOCKS_COL):
                if solved_board[i][j] != board.BOARD[i][j]:
                    board.X_BOARD[i][j] = 'X'
                    board.BOARD[i][j] = solved_board[i][j]
    board.clear_board(board.tmp_BOARD)
    board.print_board(board.X_BOARD)


def pop_visu_el():
    for i in range(len(solver.VISU_LIST)):
        el = solver.VISU_LIST.pop(0)
        return el[0], el[1], el[2], el[3]


def draw_solve_progress(brd):
    global visualization
    global visu_block
    if visualization:
        vals = pop_visu_el()
        if vals is None:
            visualization = False
            solver.VISU_LIST = []
            draw_solved_game()
            return
        row = vals[0]
        col = vals[1]
        num = vals[2]
        color = vals[3]
        brd.tiles[row][col].row = row
        brd.tiles[row][col].col = col
        board.BOARD[row][col] = str(num)
        board.tmp_BOARD[row][col] = color
    if not visu_block:
        visu_block = True
        solver.VISU_LIST = []
        draw_solved_game()
        board.clear_board(board.X_BOARD)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #

def save_hints():
    dict = collections.defaultdict(list)
    for i in range(constants.NUMBER_OF_BLOCKS_ROW):
        for j in range(constants.NUMBER_OF_BLOCKS_COL):
            if board.BOARD[i][j] == 0 or board.BOARD[i][j] == '0':
                for num in range(10):
                    if solver.validate(board.BOARD, (i, j), num):
                        dict[(i, j)].append(num)
    board.HINT_DICT = dict
    return dict


def clear_hints():
    board.HINT_DICT.clear()


# --------------------------------------------------------------------------------------------

def initialize_game():
    pygame.init()

    surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    surface.fill(constants.LIGHT_BLUE)

    # Title and Icon
    pygame.display.set_caption(constants.GAME_TITLE)
    icon = pygame.image.load(constants.GAME_ICON)
    pygame.display.set_icon(icon)

    return surface


# --------------------------------------------------------------------------------------------


def game_loop(surface, bo, brd):
    global visualization
    global resetter
    running = True
    start = time.time()

    buttons = features.init_buttons(surface)
    reset_button = buttons[0]
    hint_button = buttons[1]
    solve_button = buttons[2]
    new_button = buttons[3]
    visu_button = buttons[4]
    generate_button = buttons[5]
    insert_button = buttons[6]
    validate_button = buttons[7]

    while running:

        play_time = round(time.time() - start)
        if resetter:
            start = time.time()
            resetter = False

        event_handler.handle_events(reset_button, hint_button, solve_button, new_button, visu_button, generate_button, insert_button, validate_button)

        # Clear the screen before drawing
        surface.fill(constants.LIGHT_BLUE)

        # If solve button is pressed, show visualization of the solution
        draw_solve_progress(brd)

        # Draw board and other features
        brd.draw_board(surface, bo)

        features.draw_timer(surface, play_time)
        features.draw_strikes(surface)
        features.draw_title(surface)
        features.init_buttons(surface)
        features.redraw_button(surface, reset_button, hint_button, solve_button, new_button, visu_button, generate_button, insert_button, validate_button)

        if visualization:
            pygame.time.wait(15)

        # Update the window
        pygame.display.update()

# --------------------------------------------------------------------------------------------


class Game:

    def __init__(self, rand=False, own=False):

        # Read file, load game and print board
        if rand:
            load_random_game()
        else:
            load_initial_game()

        # Prepare for inserting user input on board
        if own:
            load_own_game()

        # Initiate additional boards
        board.X_BOARD = [[0 for j in range(constants.NUMBER_OF_BLOCKS_COL)] for i in range(constants.NUMBER_OF_BLOCKS_ROW)]
        board.tmp_BOARD = [[0 for j in range(constants.NUMBER_OF_BLOCKS_COL)] for i in range(constants.NUMBER_OF_BLOCKS_ROW)]
        board.LAST_USER_BOARD = [[0 for j in range(constants.NUMBER_OF_BLOCKS_COL)] for i in
                           range(constants.NUMBER_OF_BLOCKS_ROW)]
        board.HINT_DICT = collections.defaultdict(list)

        # Initialize game and run game loop
        brd = board.Board()
        surface = initialize_game()
        game_loop(surface, board.BOARD, brd)

