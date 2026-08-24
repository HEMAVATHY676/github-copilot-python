import copy
import random

SIZE = 9
EMPTY = 0
DIFFICULTY_CLUES = {
    'Easy': 45,
    'Medium': 35,
    'Hard': 25,
}

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def count_solutions(board, limit=2):
    """Count board solutions, stopping when the supplied limit is reached."""
    if limit < 1:
        return 0

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                solutions = 0
                for candidate in range(1, SIZE + 1):
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        solutions += count_solutions(board, limit - solutions)
                        board[row][col] = EMPTY
                        if solutions >= limit:
                            return solutions
                return solutions
    return 1

def remove_cells(board, clues):
    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    cells_to_remove = SIZE * SIZE - clues

    for row, col in cells:
        if board[row][col] != EMPTY:
            removed_value = board[row][col]
            board[row][col] = EMPTY
            if count_solutions(board) != 1:
                board[row][col] = removed_value
            else:
                cells_to_remove -= 1
            if cells_to_remove == 0:
                break

def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution

def generate_puzzle_for_difficulty(difficulty):
    if difficulty not in DIFFICULTY_CLUES:
        raise ValueError('Difficulty must be Easy, Medium, or Hard')
    return generate_puzzle(clues=DIFFICULTY_CLUES[difficulty])
