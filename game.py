import collections

import pygame
import sys
import time

import constants
import solver
import features
import board

global SET_CURRENT  # Keeps track of current position on the board based on user input
SET_CURRENT = [0, 0]
global visualization
visualization = False
global resetter
resetter = False
global visu_block
visu_block = True


def check_board_limits(pos_x, pos_y):
    if pos_x < 0 or pos_x > 8 or pos_y < 0 or pos_y > 8:
        return False
    return True


def insert_numkey(num):
    if solver.validate(board.BOARD, (SET_CURRENT[1], SET_CURRENT[0]), num) and int(board.ORIG_BOARD[SET_CURRENT[1]][SET_CURRENT[0]]) == 0:
        print("Num " + str(num) + " inserted.")
        board.BOARD[SET_CURRENT[1]][SET_CURRENT[0]] = str(num)
    else:
        features.STRIKES += 1
        print("Num " + str(num) + " not inserted.")


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


def solve_game():
    sb = copy_board(board.ORIG_BOARD)
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
    clear_board(board.tmp_BOARD)
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
        clear_board(board.X_BOARD)


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


def redraw_button(surface, reset_button, hint_button, solve_button, new_button, visu_button):
    # Clear the screen before drawing
    reset_button.draw_button(surface, constants.BLACK)
    hint_button.draw_button(surface, constants.BLACK)
    solve_button.draw_button(surface, constants.BLACK)
    new_button.draw_button(surface, constants.BLACK)
    visu_button.draw_button(surface, constants.BLACK)


def handle_events(reset_button, hint_button, solve_button, new_button, visu_button):
    global visualization
    global visu_block

    for event in pygame.event.get():

        # Exit game with X
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> KEYS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #

        # GENERAL KEY CONTROL
        if event.type == pygame.KEYDOWN:

            # Exit game with ESC
            if event.key == pygame.K_ESCAPE:
                running = False
                sys.exit()

            # Delete inserted numbers on board
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                if int(board.ORIG_BOARD[SET_CURRENT[1]][SET_CURRENT[0]]) == 0:
                    board.BOARD[SET_CURRENT[1]][SET_CURRENT[0]] = str(0)

            # Move one tile in chosen direction (with arrows)
            if event.key == pygame.K_LEFT:
                if check_board_limits(SET_CURRENT[0] - 1, SET_CURRENT[1]):
                    SET_CURRENT[0] = SET_CURRENT[0] - 1

            if event.key == pygame.K_RIGHT:
                if check_board_limits(SET_CURRENT[0] + 1, SET_CURRENT[1]):
                    SET_CURRENT[0] = SET_CURRENT[0] + 1

            if event.key == pygame.K_UP:
                if check_board_limits(SET_CURRENT[0], SET_CURRENT[1] - 1):
                    SET_CURRENT[1] = SET_CURRENT[1] - 1

            if event.key == pygame.K_DOWN:
                if check_board_limits(SET_CURRENT[0], SET_CURRENT[1] + 1):
                    SET_CURRENT[1] = SET_CURRENT[1] + 1

        # key up
        if event.type == pygame.KEYUP:
            pass

            if event.key == pygame.K_LEFT or event.key == pygame.K_LEFT:
                pass

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MOUSE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #

        # MOUSE PRESS CONTROL
        pos_over = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            if reset_button.isOver(pos_over):
                reset_button.color = constants.LIGHTER_BLUE
            else:
                reset_button.color = constants.GREY
            if hint_button.isOver(pos_over):
                hint_button.color = constants.LIGHTER_BLUE
            else:
                hint_button.color = constants.GREY
            if solve_button.isOver(pos_over):
                solve_button.color = constants.LIGHTER_BLUE
            else:
                solve_button.color = constants.GREY

        if event.type == pygame.MOUSEBUTTONDOWN:

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                # Insert numbers
                m_x = (pos[0] - constants.SIDE_SPACE) // constants.BLOCK_HEIGHT
                m_y = (pos[1] - constants.TOP_SPACE) // constants.BLOCK_WIDTH
                if check_board_limits(m_x, m_y):
                    SET_CURRENT[0] = m_x
                    SET_CURRENT[1] = m_y

                print(m_x, m_y)
                print(pos)

            # Click buttons
            if reset_button.isOver(pos_over):
                reset_game()
            if hint_button.isOver(pos_over):
                print("Clicked hint.")

            if solve_button.isOver(pos_over):
                solve_game()
                if visu_button.text == 'X':
                    visu_block = True
                    visualization = True
                else:
                    visualization = False
                    visu_block = False

            if new_button.isOver(pos_over):
                print("Clicked new.")

            if visu_button.isOver(pos_over):
                if visu_button.text == 'X':
                    visu_button.text = ''
                else:
                    visu_button.text = 'X'
                print("Visu clicked.")


        # NUMBERS CONTROL
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                insert_numkey(1)

            if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                insert_numkey(2)

            if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                insert_numkey(3)

            if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                insert_numkey(4)

            if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                insert_numkey(5)

            if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                insert_numkey(6)

            if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                insert_numkey(7)

            if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                insert_numkey(8)

            if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                insert_numkey(9)

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

    while running:

        play_time = round(time.time() - start)
        if resetter:
            start = time.time()
            resetter = False

        handle_events(reset_button, hint_button, solve_button, new_button, visu_button)

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
        redraw_button(surface, reset_button, hint_button, solve_button, new_button, visu_button)

        if visualization:
            pygame.time.wait(15)

        # Update the window
        pygame.display.update()

# --------------------------------------------------------------------------------------------


class Game:

    def __init__(self):
        # Read file and print it
        board.BOARD = board.read_board(constants.GAME_FILE, 1)
        board.ORIG_BOARD = board.read_board(constants.GAME_FILE, 1)
        board.print_board(board.BOARD)

        # Initiate additional boards
        board.X_BOARD = [[0 for j in range(constants.NUMBER_OF_BLOCKS_COL)] for i in range(constants.NUMBER_OF_BLOCKS_ROW)]
        board.tmp_BOARD = [[0 for j in range(constants.NUMBER_OF_BLOCKS_COL)] for i in range(constants.NUMBER_OF_BLOCKS_ROW)]
        board.LAST_USER_BOARD = [[0 for j in range(constants.NUMBER_OF_BLOCKS_COL)] for i in
                           range(constants.NUMBER_OF_BLOCKS_ROW)]

        # Initialize game and run game loop
        brd = board.Board()
        surface = initialize_game()
        game_loop(surface, board.BOARD, brd)

