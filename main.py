import pygame, sys
import consts
import pygame_gui
import game_func

global SET_HIGHLIGHT
global BOARD
SET_HIGHLIGHT = [0, 0]

################################################################################
"""
TO DO:
    - check board limits (so mouse click doesn't add false value): OK

"""
################################################################################


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
            #print("{}, {}: {}".format(i, j, tile_content))

            # Coordinates and W/H of the tiles
            rect_x = i*consts.BLOCK_WIDTH+consts.SIDE_SPACE
            rect_y = j*consts.BLOCK_HEIGHT+consts.TOP_SPACE
            myrect = pygame.Rect(rect_x, rect_y, consts.BLOCK_WIDTH, consts.BLOCK_HEIGHT)

            font = pygame.font.SysFont("Arial", 38)
            text = font.render(tile_content, True, consts.BLACK, None)
            text_x = rect_x + consts.BLOCK_WIDTH/2 - text.get_rect().width / 2
            text_y = rect_y + consts.BLOCK_HEIGHT/2 - text.get_rect().height / 2

            # Color the tiles
            pygame.draw.rect(surface, consts.LIGHT_GREY, myrect)
            """
            if j % 2 == 0:
                if i % 2 == 0:
                    pygame.draw.rect(surface, consts.LIGHT_GREY, myrect)
                else:
                    pygame.draw.rect(surface, consts.GREY, myrect)
            else:
                if i % 2 == 0:
                    pygame.draw.rect(surface, consts.GREY, myrect)
                else:
                    pygame.draw.rect(surface, consts.LIGHT_GREY, myrect)
            """

            # Draw highlight of currently used tile
            if int(SET_HIGHLIGHT[0]) == i and int(SET_HIGHLIGHT[1] == j):
                #print("DRAW I: " + str(i) + " = " + str(SET_HIGHLIGHT[0]) + " J: " + str(j) + " = " + str(SET_HIGHLIGHT[1]))
                draw_highlight(surface, SET_HIGHLIGHT[0], SET_HIGHLIGHT[1])
                #print("Set High on DRAW: " + str(SET_HIGHLIGHT))

            # Add numbers on the board
            if tile_content == '0':
                
                continue
            else:
                surface.blit(text, (text_x, text_y))


def draw_highlight(surface, pos_x, pos_y):
    less_top = 6
    less_bottom = 9
    rect_x = pos_x * consts.BLOCK_WIDTH + consts.SIDE_SPACE
    rect_y = pos_y * consts.BLOCK_HEIGHT + consts.TOP_SPACE
    #print("Pos in HIGHLIGHT: " + str(rect_x) + " xxx " + str(rect_y))

    #myrect_dark = pygame.Rect(rect_x, rect_y, consts.BLOCK_WIDTH, consts.BLOCK_HEIGHT)
    myrect_light = pygame.Rect(rect_x, rect_y, consts.BLOCK_WIDTH, consts.BLOCK_HEIGHT)

    #pygame.draw.rect(surface, consts.BACK_BLUE, myrect_dark)
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
    while running:

        for event in pygame.event.get():

            # Quit game
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            # >>>>> KEYSTROKES CONTROL <<<<< #

            # KEY DOWN
            if event.type == pygame.KEYDOWN:
                print('Key pressed down.')

                if event.key == pygame.K_ESCAPE:
                    running = False
                    sys.exit()

                if event.key == pygame.K_LEFT:
                    print('Left key pressed.')
                if event.key == pygame.K_RIGHT:
                    print('Right key pressed.')

                if event.type == pygame.K_SPACE:
                    print('Space key pressed')

            # KEY UP
            if event.type == pygame.KEYUP:
                print('Key released.')

                if event.key == pygame.K_LEFT or event.key == pygame.K_LEFT:
                    print('Key left or right released.')

            # MOUSE CONTROL
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    m_x = (pos[0] - consts.SIDE_SPACE) // consts.BLOCK_HEIGHT
                    #print("POS 0: " + str(pos[0]) + " TOP S: " + str(consts.TOP_SPACE))
                    m_y = (pos[1] - consts.TOP_SPACE) // consts.BLOCK_WIDTH
                    #print("POS 1: " + str(pos[1]) + " SIDE S: " + str(consts.SIDE_SPACE))
                    if check_board_limits(m_x, m_y):
                        SET_HIGHLIGHT[0] = m_x
                        SET_HIGHLIGHT[1] = m_y
                        print("Set high: " + str(SET_HIGHLIGHT))

                    print(m_x, m_y)
                    print(check_board_limits(m_x, m_y))
                    print(pos)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    pass
                    """
                    if event.ui_element == hello_button:
                        print('Hello World!')
                    """

        # Draw board and grid based on input
        draw_board(surface, board)
        draw_grid(surface)

        pygame.display.update()


def main():
    global BOARD
    BOARD = read_board(consts.GAME_FILE, 1)
    print_board(BOARD)

    surface = initialize_game()
    game_loop(surface, BOARD)
    pass


if __name__ == "__main__":
    main()
