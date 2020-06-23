import pygame
import sys

import constants
import solver
import features
import board
import game

global hint_used
hint_used = False


# --------------------------------------------------------------------------------------------
# CHECK VALIDITY OF INSERTED NUMS ON BOARD

def check_board_limits(pos_x, pos_y):
    if pos_x < 0 or pos_x > 8 or pos_y < 0 or pos_y > 8:
        return False
    return True


def insert_numkey(num):
    if solver.validate(board.BOARD, (game.SET_CURRENT[1], game.SET_CURRENT[0]), num) and int(
            board.ORIG_BOARD[game.SET_CURRENT[1]][game.SET_CURRENT[0]]) == 0:
        print("Num " + str(num) + " inserted.")
        board.BOARD[game.SET_CURRENT[1]][game.SET_CURRENT[0]] = str(num)
    else:
        features.STRIKES += 1
        print("Num " + str(num) + " not inserted, a strike added.")


# --------------------------------------------------------------------------------------------
# HANDLE EVENTS

def handle_events(reset_button, hint_button, solve_button, new_button, visu_button, generate_button, insert_button,
                  validate_button):
    global hint_used

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
                if int(board.ORIG_BOARD[game.SET_CURRENT[1]][game.SET_CURRENT[0]]) == 0:
                    board.BOARD[game.SET_CURRENT[1]][game.SET_CURRENT[0]] = str(0)

            # Move one tile in chosen direction (with arrows)
            if event.key == pygame.K_LEFT:
                if check_board_limits(game.SET_CURRENT[0] - 1, game.SET_CURRENT[1]):
                    game.SET_CURRENT[0] = game.SET_CURRENT[0] - 1

            if event.key == pygame.K_RIGHT:
                if check_board_limits(game.SET_CURRENT[0] + 1, game.SET_CURRENT[1]):
                    game.SET_CURRENT[0] = game.SET_CURRENT[0] + 1

            if event.key == pygame.K_UP:
                if check_board_limits(game.SET_CURRENT[0], game.SET_CURRENT[1] - 1):
                    game.SET_CURRENT[1] = game.SET_CURRENT[1] - 1

            if event.key == pygame.K_DOWN:
                if check_board_limits(game.SET_CURRENT[0], game.SET_CURRENT[1] + 1):
                    game.SET_CURRENT[1] = game.SET_CURRENT[1] + 1

        # key up
        if event.type == pygame.KEYUP:
            pass

            if event.key == pygame.K_LEFT or event.key == pygame.K_LEFT:
                pass

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MOUSE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #

        # MOUSE PRESS CONTROL
        pos_over = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            # Change color on hover
            features.change_color_on_hover(pos_over, reset_button)
            features.change_color_on_hover(pos_over, hint_button)
            features.change_color_on_hover(pos_over, solve_button)
            features.change_color_on_hover(pos_over, visu_button)
            features.change_color_on_hover(pos_over, generate_button)
            features.change_color_on_hover(pos_over, insert_button)
            #features.change_color_on_hover(pos_over, validate_button)

        if hint_used and pygame.mouse.get_pressed()[0]:
            print("Hint being shown.")
            hint_button.color = constants.GREEN
            hint_button.text = 'Hint Shown'

        if game.own_game:
            if insert_button.text == 'Click to Validate':
                insert_button.color = constants.LIGHTER_RED
                validate_button.text = '- Game Not Ready -'
                validate_button.color = constants.RED
                if insert_button.isOver(pos_over):
                    features.change_color_on_hover(pos_over, insert_button, red=True)

        if event.type == pygame.MOUSEBUTTONDOWN:

            # GET MOUSE POSITION
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                # Insert numbers
                m_x = (pos[0] - constants.SIDE_SPACE) // constants.BLOCK_HEIGHT
                m_y = (pos[1] - constants.TOP_SPACE) // constants.BLOCK_WIDTH
                if check_board_limits(m_x, m_y):
                    game.SET_CURRENT[0] = m_x
                    game.SET_CURRENT[1] = m_y

                print(m_x, m_y)
                print(pos)

            # IF MOUSE IS CLICKED

            # >>>>> ------------- reset -------------- <<<<< #
            if reset_button.isOver(pos_over):
                game.reset_game()

            # >>>>> ------------- show hint -------------- <<<<< #
            if hint_button.isOver(pos_over):
                print("Clicked hint.")
                game.save_hints()
                if not hint_used:
                    hint_used = True
                    hint_button.color = constants.GREEN
                    hint_button.text = 'Hint Shown'

            # >>>>> ------------- solve -------------- <<<<< #
            # with / without visualization
            if solve_button.isOver(pos_over):
                game.solve_game()
                if visu_button.text == 'X':
                    game.visu_block = True
                    game.visualization = True
                else:
                    game.visualization = False
                    game.visu_block = False

            if visu_button.isOver(pos_over):
                if visu_button.text == 'X':
                    visu_button.text = ''
                else:
                    visu_button.text = 'X'
                print("Visu clicked.")

            # >>>>> ------------- NEW GAME -------------- <<<<< #
            if new_button.isOver(pos_over):
                pass

            # >>>>> ------------- generate -------------- <<<<< #
            if generate_button.isOver(pos_over):
                game.reset_all()
                game.Game(rand=True)
                print('Generate button clicked.')

            # >>>>> ------------- insert own -------------- <<<<< #
            if insert_button.isOver(pos_over):

                # To validate game
                if not game.own_game:
                    game.own_game = True
                    game.reset_all()
                    print('Own true')
                    insert_button.text = 'Click to Validate'
                    insert_button.color = constants.LIGHTER_RED

                # To return to the initial state
                else:
                    print('Own false')
                    sb = board.copy_board(board.BOARD)
                    if not solver.solve(sb) or not board.isSolvable(board.BOARD):
                        validate_button.text = '- Game Not Ready -'
                        validate_button.color = constants.RED
                    else:
                        # If input game CAN BE SOLVED, then:
                        game.own_game = False
                        validate_button.text = '- Game Ready | Start -'
                        validate_button.color = constants.GREEN
                        insert_button.text = 'Insert Own Game'
                        insert_button.color = constants.GREY

                        # Save game and load new game
                        board.write_board(constants.GAME_FILE_OWN, board.BOARD)
                        game.Game(own=True)
                print('Insert button clicked.')

            # >>>>> ------------- validate own -------------- <<<<< #
            if validate_button.isOver(pos_over):
                print('Validate button clicked.')

        if event.type == pygame.MOUSEBUTTONUP:
            game.clear_hints()
            hint_used = False
            if hint_button.isOver(pos_over):
                hint_button.color = constants.LIGHTER_BLUE
                hint_button.text = 'Show Hint'
            else:
                hint_button.color = constants.GREY
                hint_button.text = 'Show Hint'

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
