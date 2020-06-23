import constants
import pygame

global STRIKES  # Counter of bad answers
STRIKES = 0


# --------------------------------------------------------------------------------------------
# TIME FORMAT

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


# --------------------------------------------------------------------------------------------
# DRAW FEATURES

def draw_timer(surface, timer):
    font = pygame.font.Font(constants.FONT_MONO, 19, bold=True)
    text = font.render(format_time(timer), 1, (0, 0, 0))
    text_x = constants.SCREEN_WIDTH - text.get_rect().width - constants.SIDE_SPACE
    text_y = constants.TOP_SPACE / 3 + 5
    cl = pygame.image.load(constants.CLOCK_ICON)
    cl = pygame.transform.scale(cl, (text.get_rect().height - 2, text.get_rect().height - 3))
    cl_x = constants.SCREEN_WIDTH - text.get_rect().width - constants.SIDE_SPACE - cl.get_rect().width - 10
    cl_y = constants.TOP_SPACE / 3 + 5
    surface.blit(cl, (cl_x, cl_y))
    surface.blit(text, (text_x, text_y))


def draw_strikes(surface):
    font = pygame.font.Font(constants.FONT_MONO, 21, bold=True)
    text = font.render((str(STRIKES)), True, constants.BLACK, None)
    td = pygame.image.load(constants.DOWN_ICON)
    td = pygame.transform.scale(td, (text.get_rect().height - 2, text.get_rect().height - 3))
    td_x = constants.SIDE_SPACE + constants.BLOCK_WIDTH * 5 + 5
    td_y = constants.TOP_SPACE / 3 + 3
    text_x = constants.SIDE_SPACE + td.get_rect().width + 8 + constants.BLOCK_WIDTH * 5 + 5
    text_y = constants.TOP_SPACE / 3 + 3
    surface.blit(td, (td_x, td_y))
    surface.blit(text, (text_x, text_y))


def draw_title(surface):
    # Sudoku title
    font1 = pygame.font.SysFont("Arial", 18, bold=True)
    font2 = pygame.font.SysFont("Arial", 20, bold=True)
    text2 = font1.render("SUDOKU", True, constants.DARK_GREY)
    text1 = font2.render("SOLVER", True, constants.BLACK)
    text_x = constants.SIDE_SPACE
    text_y_a = constants.TOP_SPACE / 2
    text_y_b = constants.TOP_SPACE / 4
    surface.blit(text1, (text_x, text_y_a))
    surface.blit(text2, (text_x, text_y_b))

    # Visualization title
    font = pygame.font.SysFont("Arial", 16, bold=False)
    text = font.render("Use visualization", True, constants.BLACK)
    height = constants.BLOCK_HEIGHT / 3 + 5
    text_x = constants.SIDE_SPACE + height + 5
    text_y = constants.TOP_SPACE + constants.BLOCK_HEIGHT*constants.NUMBER_OF_BLOCKS_COL + 25 + (height+5)*3 + 2
    surface.blit(text, (text_x, text_y))


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #


def redraw_button(surface, reset_button, hint_button, solve_button, new_button, visu_button, generate_button, insert_button, validate_button):
    # Clear the screen before drawing
    reset_button.draw_button(surface, constants.BLACK)
    hint_button.draw_button(surface, constants.BLACK)
    solve_button.draw_button(surface, constants.BLACK)
    new_button.draw_button(surface, constants.BLACK)
    visu_button.draw_button(surface, constants.BLACK)
    generate_button.draw_button(surface, constants.BLACK)
    insert_button.draw_button(surface, constants.BLACK)
    validate_button.draw_button(surface, constants.BLACK)


def change_color_on_hover(pos, btn, red=False):
    if btn.isOver(pos):
        btn.color = constants.LIGHTER_BLUE
    else:
        if btn.text == 'X' or btn.text == '':
            btn.color = constants.LIGHT_GREY
        else:
            btn.color = constants.GREY
    if red:
        btn.color = constants.LIGHTER_BLUE


# --------------------------------------------------------------------------------------------
# INIT FEATURES

def init_buttons(surface):
    x = constants.SIDE_SPACE
    y = constants.TOP_SPACE + constants.BLOCK_HEIGHT*constants.NUMBER_OF_BLOCKS_COL + 25
    width = constants.BLOCK_WIDTH*3 - 5
    height = constants.BLOCK_HEIGHT/3 + 5

    # COLUMN 1
    reset_button = Button(constants.GREY, x, y, width, height, "Reset Game")
    hint_button = Button(constants.GREY, x, y+height+5, width, height, "Show Hint")
    solve_button = Button(constants.GREY, x, y+(height+5)*2, width, height, "Solve Game")
    visu_button = Button(constants.LIGHT_GREY, x, y+(height+5)*3, height, height, "X")

    # COLUMN 2
    new_button = Button(constants.LIGHT_GREY, x+constants.BLOCK_WIDTH*3 + 5, y, width+constants.BLOCK_WIDTH - 5, height, "New Game:")
    generate_button = Button(constants.GREY, x+constants.BLOCK_WIDTH*3 + 5, y+height+5, width+constants.BLOCK_WIDTH - 5, height, "Generate Random Game", True)
    insert_button = Button(constants.GREY, x + constants.BLOCK_WIDTH * 3 + 5, y+(height+5)*2,
                             width + constants.BLOCK_WIDTH - 5, height, "Insert Own Game", True)
    validate_button = Button(constants.GREEN, x + constants.BLOCK_WIDTH * 3 + 5, y+(height+5)*3,
                             width + constants.BLOCK_WIDTH - 5, height, '- Game Ready | Start -', True)

    # DRAW BUTTONS
    reset_button.draw_button(surface, constants.BLACK)
    hint_button.draw_button(surface, constants.BLACK)
    solve_button.draw_button(surface, constants.BLACK)
    new_button.draw_button(surface, constants.BLACK)
    visu_button.draw_button(surface, constants.BLACK)
    generate_button.draw_button(surface, constants.BLACK)
    insert_button.draw_button(surface, constants.BLACK)
    validate_button.draw_button(surface, constants.BLACK)

    return reset_button, hint_button, solve_button, new_button, visu_button, generate_button, insert_button, validate_button


# --------------------------------------------------------------------------------------------
# FEATURE CLASSES

class Button:
    def __init__(self, color, x, y, width, height, text, text_small=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_small = text_small

    def draw_button(self, surface, outline=None):
        if outline:
            myrect_O = pygame.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4)
            pygame.draw.rect(surface, constants.BLACK, myrect_O)
        myrect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, myrect)

        if self.text != '':
            if self.text_small:
                font = pygame.font.SysFont("Arial", 13, bold=True)
            else:
                font = pygame.font.SysFont("Arial", 18, bold=True)
            text = font.render(self.text, True, constants.BLACK)
            surface.blit(text, (self.x + (self.width / 2 - text.get_rect().width / 2),
                                self.y + (self.height / 2 - text.get_rect().height / 2)))

    def isOver(self, pos):
        # Pos is position of a mouse or tuple coords
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def __str__(self):
        return "Button " + self.text
