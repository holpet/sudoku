# Return idx tuples with no solution
def find_empty_pos(board):
    for i in range(9):
        for j in range(9):
            if int(board[i][j]) == 0:
                return i, j
    return False


# Go through the list, when you encounter 0, try to solve.
def solve(board):
    empty_pos = find_empty_pos(board)
    if empty_pos is False:
        return board
    else:
        for num in range(1, 10):
            if validate(board, empty_pos, num):
                board[empty_pos[0]][empty_pos[1]] = str(num)
                if solve(board):
                    return board
                board[empty_pos[0]][empty_pos[1]] = '0'
        return False


# Take in idx as tpl and list of values to check for validity.
def validate(board, pos, num):
    # Check on horizontal
    for i in range(9):
        if num == int(board[pos[0]][i]):
            return False

    # Check on vertical
    for j in range(9):
        if num == int(board[j][pos[1]]):
            return False

    # Check on group 3x3
    row = pos[0] // 3
    col = pos[1] // 3

    for k in range(3):
        for h in range(3):
            if int(board[row * 3 + k][col * 3 + h]) == num:
                return False

    return True
