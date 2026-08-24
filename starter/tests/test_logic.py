from sudoku_logic import EMPTY, SIZE, create_empty_board, generate_puzzle, is_safe


def _has_valid_rows_and_columns(board):
    for index in range(SIZE):
        row_values = [value for value in board[index] if value != EMPTY]
        if len(set(row_values)) != len(row_values):
            return False
        col_values = [board[row][index] for row in range(SIZE) if board[row][index] != EMPTY]
        if len(set(col_values)) != len(col_values):
            return False
    return True


def _has_valid_boxes(board):
    for start_row in range(0, SIZE, 3):
        for start_col in range(0, SIZE, 3):
            values = []
            for row in range(start_row, start_row + 3):
                for col in range(start_col, start_col + 3):
                    value = board[row][col]
                    if value != EMPTY:
                        values.append(value)
            if len(set(values)) != len(values):
                return False
    return True


def test_create_empty_board_is_nine_by_nine_and_empty():
    board = create_empty_board()

    assert len(board) == SIZE
    assert all(len(row) == SIZE for row in board)
    assert all(value == EMPTY for row in board for value in row)


def test_is_safe_rejects_conflicts_in_row_column_and_box():
    board = create_empty_board()

    assert is_safe(board, 0, 0, 5) is True

    board[0][0] = 5
    board[0][1] = 5
    board[1][0] = 5
    board[1][1] = 5

    assert is_safe(board, 0, 2, 5) is False
    assert is_safe(board, 2, 0, 5) is False
    assert is_safe(board, 0, 1, 5) is False
    assert is_safe(board, 2, 2, 5) is False


def test_generate_puzzle_returns_valid_puzzle_and_solution():
    puzzle, solution = generate_puzzle(35)

    assert len(puzzle) == SIZE
    assert all(len(row) == SIZE for row in puzzle)
    assert len(solution) == SIZE
    assert all(len(row) == SIZE for row in solution)
    assert sum(cell != EMPTY for row in puzzle for cell in row) == 35
    assert _has_valid_rows_and_columns(solution)
    assert _has_valid_boxes(solution)
    assert _has_valid_rows_and_columns(puzzle)
    assert _has_valid_boxes(puzzle)
