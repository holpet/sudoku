import pygame
import pygame_gui
import sys
import time

import consts
import solver

global SET_CURRENT  # Keeps track of current position on the board based on user input
global BOARD  # Board that changes values based on user input
global ORIG_BOARD  # To keep track of user input against changing BOARD
global STRIKES  # Counter of bad answers
SET_CURRENT = [0, 0]
STRIKES = 0


def print_board(board):
    for i in board:
        print(i)


def chunks(lst):
    for i in range(0, 81, 9):
        yield lst[i:i + 9]


# Read numbers from a file to prepare a game
def read_board(filename, num):
    with open(filename, 'r') as f:
        for i, line in enumerate(f, start=1):
            if i == num:
                lst = line.split()
                f.close()
                break
    return list(chunks(lst))


def choose_board():
    pass


def draw_board(surface, board):
    for j, tile in enumerate(board):
        for i, tile_content in enumerate(tile):

            # Coordinates and W/H of the tiles
            rect_x = i*consts.BLOCK_WIDTH+consts.SIDE_SPACE
            rect_y = j*consts.BLOCK_HEIGHT+consts.TOP_SPACE
            myrect = pygame.Rect(rect_x, rect_y, consts.BLOCK_WIDTH, consts.BLOCK_HEIGHT)

            font = pygame.font.SysFont("Arial", 38)
            text_black = font.render(tile_content, True, consts.BLACK, None)
            text_blue = font.render(tile_content, True, consts.DARK_BLUE, None)

            text_x = rect_x + consts.BLOCK_WIDTH/2 - text_black.get_rect().width / 2
            text_y = rect_y + consts.BLOCK_HEIGHT/2 - text_black.get_rect().height / 2

            # Color the tiles
            if ((j <= 2 or j >= 6) and (i <= 2 or i >= 6)) or (3 <= j <= 5 and 3 <= i <= 5):
                pygame.draw.rect(surface, consts.LIGHT_GREY, myrect)
            else:
                pygame.draw.rect(surface, consts.GREY, myrect)

            # Draw highlight of currently used tile
            if int(SET_CURRENT[0]) == i and int(SET_CURRENT[1] == j):
                draw_highlight(surface, SET_CURRENT[0], SET_CURRENT[1])

            # Add numbers on the board
            if tile_content == '0':
                
                continue
            else:
                # If the text is input, validate it in blue
                if int(ORIG_BOARD[j][i]) == 0:
                    surface.blit(text_blue, (text_x, text_y))
                else:
                    surface.blit(text_black, (text_x, text_y))


def draw_highlight(surface, pos_x, pos_y):
    rect_x = pos_x * consts.BLOCK_WIDTH + consts.SIDE_SPACE
    rect_y = pos_y * consts.BLOCK_HEIGHT + consts.TOP_SPACE
    myrect_light = pygame.Rect(rect_x, rect_y, consts.BLOCK_WIDTH, consts.BLOCK_HEIGHT)
    pygame.draw.rect(surface, consts.LIGHTER_BLUE, myrect_light)


def draw_grid(surface):
    for i in range(consts.NUMBER_OF_BLOCKS_ROW + 1):
        new_W = round(i * consts.BLOCK_WIDTH) + consts.SIDE_SPACE
        new_H = round(i * consts.BLOCK_HEIGHT) + consts.TOP_SPACE
        # COL/ROW LINES (start pos) (end pos)
        if i % 3 == 0:
            pygame.draw.line(surface, consts.BLACK, (new_W, consts.TOP_SPACE), (new_W, consts.BLOCK_WIDTH*consts.NUMBER_OF_BLOCKS_ROW + consts.TOP_SPACE), 5)
            pygame.draw.line(surface, consts.BLACK, (consts.SIDE_SPACE, new_H), (consts.BLOCK_WIDTH * consts.NUMBER_OF_BLOCKS_COL + consts.SIDE_SPACE, new_H), 5)
        else:
            pygame.draw.line(surface, consts.BLACK, (new_W, consts.TOP_SPACE), (new_W, consts.BLOCK_WIDTH*consts.NUMBER_OF_BLOCKS_ROW + consts.TOP_SPACE), 2)
            pygame.draw.line(surface, consts.BLACK, (consts.SIDE_SPACE, new_H), (consts.BLOCK_WIDTH * consts.NUMBER_OF_BLOCKS_COL + consts.SIDE_SPACE, new_H), 2)


def check_board_limits(pos_x, pos_y):
    if pos_x < 0 or pos_x > 8 or pos_y < 0 or pos_y > 8:
        return False
    return True


def solve_board():
    pass


def insert_numkey(num):
    global STRIKES
    if solver.validate(BOARD, (SET_CURRENT[1], SET_CURRENT[0]), num) and int(ORIG_BOARD[SET_CURRENT[1]][SET_CURRENT[0]]) == 0:
        print("Num " + str(num) + " inserted.")
        BOARD[SET_CURRENT[1]][SET_CURRENT[0]] = str(num)
    else:
        STRIKES += 1
        print("Num " + str(num) + " not inserted.")


def format_time(secs):
    sec = secs % 60
    min = secs // 60
    hour = min // 60
    if len(str(sec)) == 1:
        sec = "0" + str(sec)
    else:
        sec = str(sec)
    if len(str(min)) == 1:
        min = "0" + str(min)
    else:
        min = str(min)
    if len(str(hour)) == 1:
        hour = "0" + str(hour)
    else:
        hour = str(hour)
    timer = hour + ":" + min + ":" + sec
    return timer


def draw_timer(surface, timer):
    font = pygame.font.Font(consts.FONT_MONO, 19, bold=True)
    text = font.render(format_time(timer), 1, (0, 0, 0))
    text_x = consts.SCREEN_WIDTH - text.get_rect().width - consts.SIDE_SPACE
    text_y = consts.TOP_SPACE / 3 + 5
    cl = pygame.image.load(consts.CLOCK_ICON)
    cl = pygame.transform.scale(cl, (text.get_rect().height - 2, text.get_rect().height - 3))
    cl_x = consts.SCREEN_WIDTH - text.get_rect().width - consts.SIDE_SPACE - cl.get_rect().width - 10
    cl_y = consts.TOP_SPACE / 3 + 5
    surface.blit(cl, (cl_x, cl_y))
    surface.blit(text, (text_x, text_y))


def draw_strikes(surface):
    font = pygame.font.Font(consts.FONT_MONO, 21, bold=True)
    text = font.render((str(STRIKES)), True, consts.BLACK, None)
    td = pygame.image.load(consts.DOWN_ICON)
    td = pygame.transform.scale(td, (text.get_rect().height - 2, text.get_rect().height - 3))
    td_x = consts.SIDE_SPACE + consts.BLOCK_WIDTH*5 + 5
    td_y = consts.TOP_SPACE / 3 + 3
    text_x = consts.SIDE_SPACE + td.get_rect().width + 8 + consts.BLOCK_WIDTH*5 + 5
    text_y = consts.TOP_SPACE / 3 + 3
    surface.blit(td, (td_x, td_y))
    surface.blit(text, (text_x, text_y))


def draw_title(surface):
    font1 = pygame.font.SysFont("Arial", 18, bold=True)
    font2 = pygame.font.SysFont("Arial", 20, bold=True)
    text2 = font1.render("SUDOKU", True, consts.DARK_GREY)
    text1 = font2.render("SOLVER", True, consts.BLACK)
    text_x = consts.SIDE_SPACE
    text_y_a = consts.TOP_SPACE / 2
    text_y_b = consts.TOP_SPACE / 4
    surface.blit(text1, (text_x, text_y_a))
    surface.blit(text2, (text_x, text_y_b))


def initialize_game():
    pygame.init()

    surface = pygame.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
    surface.fill(consts.LIGHT_BLUE)

    # Title and Icon
    pygame.display.set_caption(consts.GAME_TITLE)
    icon = pygame.image.load(consts.GAME_ICON)
    pygame.display.set_icon(icon)

    return surface


def game_loop(surface, board):
    running = True
    start = time.time()

    while running:

        play_time = round(time.time() - start)

        for event in pygame.event.get():

            # Exit game with X
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            # >>>>> KEYS & MOUSE <<<<< #

            # GENERAL KEY CONTROL
            if event.type == pygame.KEYDOWN:

                # Exit game with ESC
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sys.exit()

                # Delete inserted numbers on board
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    if int(ORIG_BOARD[SET_CURRENT[1]][SET_CURRENT[0]]) == 0:
                        BOARD[SET_CURRENT[1]][SET_CURRENT[0]] = str(0)

                # Move one tile in chosen direction (with arrows)
                if event.key == pygame.K_LEFT:
                    if check_board_limits(SET_CURRENT[0]-1, SET_CURRENT[1]):
                        SET_CURRENT[0] = SET_CURRENT[0]-1

                if event.key == pygame.K_RIGHT:
                    if check_board_limits(SET_CURRENT[0]+1, SET_CURRENT[1]):
                        SET_CURRENT[0] = SET_CURRENT[0]+1

                if event.key == pygame.K_UP:
                    if check_board_limits(SET_CURRENT[0], SET_CURRENT[1]-1):
                        SET_CURRENT[1] = SET_CURRENT[1]-1

                if event.key == pygame.K_DOWN:
                    if check_board_limits(SET_CURRENT[0], SET_CURRENT[1]+1):
                        SET_CURRENT[1] = SET_CURRENT[1]+1

            # key up
            if event.type == pygame.KEYUP:
                pass

                if event.key == pygame.K_LEFT or event.key == pygame.K_LEFT:
                    pass

            # MOUSE PRESS CONTROL
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    m_x = (pos[0] - consts.SIDE_SPACE) // consts.BLOCK_HEIGHT
                    m_y = (pos[1] - consts.TOP_SPACE) // consts.BLOCK_WIDTH
                    if check_board_limits(m_x, m_y):
                        SET_CURRENT[0] = m_x
                        SET_CURRENT[1] = m_y

                    print(m_x, m_y)
                    print(pos)

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

            # USER EVENTS
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    pass
                    """
                    if event.ui_element == hello_button:
                        print('Hello World!')
                    """

        # Clear the screen before drawing
        surface.fill(consts.LIGHT_BLUE)

        # Draw board and grid and other features
        draw_board(surface, board)
        draw_grid(surface)
        draw_timer(surface, play_time)
        draw_strikes(surface)
        draw_title(surface)

        # Update the window
        pygame.display.update()


def main():
    global BOARD, ORIG_BOARD
    BOARD = read_board(consts.GAME_FILE, 1)
    ORIG_BOARD = read_board(consts.GAME_FILE, 1)
    print_board(BOARD)

    surface = initialize_game()
    game_loop(surface, BOARD)
    pass


if __name__ == "__main__":
    main()
