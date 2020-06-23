import collections

global CATCH_DICT  # To show solving path (red/green values)
CATCH_DICT = collections.defaultdict(list)
global VISU_LIST
VISU_LIST = []


# Return idx tuples with no solution
def find_empty_pos(bo):
    for i in range(9):
        for j in range(9):
            if int(bo[i][j]) == 0:
                return i, j
    return False


# Go through the list, when you encounter 0, try to solve.
def solve(bo):
    empty_pos = find_empty_pos(bo)
    if empty_pos is False:
        return bo
    else:
        for num in range(1, 10):
            if validate(bo, empty_pos, num):
                bo[empty_pos[0]][empty_pos[1]] = str(num)
                catch_options(empty_pos[0], empty_pos[1], num, 'G')
                VISU_LIST.append([empty_pos[0], empty_pos[1], num, 'G'])
                if solve(bo):
                    return bo
                bo[empty_pos[0]][empty_pos[1]] = '0'
                catch_options(empty_pos[0], empty_pos[1], num, 'R')
                VISU_LIST.append([empty_pos[0], empty_pos[1], num, 'R'])
        return False


# Take in idx as tpl and list of values to check for validity.
def validate(bo, pos, num):
    # Check on horizontal
    for i in range(9):
        if num == int(bo[pos[0]][i]):
            return False

    # Check on vertical
    for j in range(9):
        if num == int(bo[j][pos[1]]):
            return False

    # Check on group 3x3
    row = pos[0] // 3
    col = pos[1] // 3

    for k in range(3):
        for h in range(3):
            if int(bo[row * 3 + k][col * 3 + h]) == num:
                return False

    return True


# ------------------------------------------------------------------------------------------

def catch_options(i, j, num, s):
    # {(1, 2): [[5, 'G'], [8, 'R']]}...
    tpl = (i, j)
    CATCH_DICT[tpl].append([num, s])
    #print(CATCH_DICT)
