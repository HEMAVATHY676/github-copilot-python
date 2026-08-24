import sudoku_logic


def test_create_empty_board_has_expected_shape_and_values():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_fill_board_creates_a_valid_solution():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board) is True
    assert all(cell in range(1, sudoku_logic.SIZE + 1) for row in board for cell in row)

    for row in board:
        assert len(set(row)) == sudoku_logic.SIZE
    for column in zip(*board):
        assert len(set(column)) == sudoku_logic.SIZE
    for row_start in range(0, sudoku_logic.SIZE, 3):
        for col_start in range(0, sudoku_logic.SIZE, 3):
            box = [
                board[row][col]
                for row in range(row_start, row_start + 3)
                for col in range(col_start, col_start + 3)
            ]
            assert len(set(box)) == sudoku_logic.SIZE


def test_count_solutions_stops_at_two_for_an_empty_board():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.count_solutions(board) == 2
    assert board == sudoku_logic.create_empty_board()


def test_count_solutions_returns_one_for_a_solved_board():
    board = sudoku_logic.create_empty_board()
    sudoku_logic.fill_board(board)

    assert sudoku_logic.count_solutions(board) == 1


def test_generate_puzzle_returns_puzzle_and_matching_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35
    assert all(
        puzzle[row][col] in (sudoku_logic.EMPTY, solution[row][col])
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
    )
    assert sudoku_logic.count_solutions(puzzle) == 1


def test_generated_puzzle_has_exactly_one_solution():
    puzzle, _ = sudoku_logic.generate_puzzle()

    assert sudoku_logic.count_solutions(puzzle) == 1


def test_easy_puzzle_has_45_clues_and_one_solution():
    puzzle, _ = sudoku_logic.generate_puzzle_for_difficulty('Easy')

    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 45
    assert sudoku_logic.count_solutions(puzzle) == 1


def test_medium_puzzle_has_35_clues_and_one_solution():
    puzzle, _ = sudoku_logic.generate_puzzle_for_difficulty('Medium')

    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35
    assert sudoku_logic.count_solutions(puzzle) == 1


def test_hard_puzzle_has_25_clues_and_one_solution():
    puzzle, _ = sudoku_logic.generate_puzzle_for_difficulty('Hard')

    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 25
    assert sudoku_logic.count_solutions(puzzle) == 1
