import collections

import board
import solver
import constants

CATCH_DICT = collections.defaultdict(list)
CATCH_DICT = {(0, 1): [],
              (0, 3): []}
VISU_LIST = []

def pop_visu_el():
    for i in range(len(VISU_LIST)):
        el = VISU_LIST.pop(0)
        print(el)
        return el[0], el[1], el[2], el[3]

print(pop_visu_el())
print(VISU_LIST)


def pop_dict_el():
    for i in range(constants.NUMBER_OF_BLOCKS_ROW):
        for j in range(constants.NUMBER_OF_BLOCKS_COL):
            if (i, j) in CATCH_DICT:
                if len(CATCH_DICT.get((i, j))) != 0 or CATCH_DICT.get((i, j)) is None:
                    val1 = CATCH_DICT.get((i, j))[0][0]
                    val2 = CATCH_DICT.get((i, j))[0][1]
                    print("Vals: {} {}".format(val1, val2))
                    el = CATCH_DICT.get((i, j)).pop(0)
                    #print(el)
                    return i, j, val1, val2


def draw_solve_progress(brd):
    pop_dict_el()


#b = [[0 for j in range(constants.NUMBER_OF_BLOCKS_COL)] for i in range(constants.NUMBER_OF_BLOCKS_ROW)]
#board.print_board(b)

#print(pop_dict_el())
#print(CATCH_DICT)
#print(len(CATCH_DICT.get((0, 1))))