import sudoku_logic
from app import CURRENT, app


def test_index_route_renders_main_page():
    client = app.test_client()

    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data


def test_new_route_generates_puzzle_and_stores_solution():
    client = app.test_client()

    response = client.get('/new?clues=30')

    assert response.status_code == 200
    payload = response.get_json()
    assert 'puzzle' in payload
    assert len(payload['puzzle']) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in payload['puzzle'])
    assert sum(value != sudoku_logic.EMPTY for row in payload['puzzle'] for value in row) == 30
    assert CURRENT['solution'] is not None
    assert len(CURRENT['solution']) == sudoku_logic.SIZE


def test_check_route_rejects_when_no_game_is_in_progress():
    client = app.test_client()
    CURRENT['solution'] = None
    CURRENT['puzzle'] = None

    response = client.post('/check', json={'board': [[0] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_route_reports_incorrect_positions():
    client = app.test_client()
    puzzle, solution = sudoku_logic.generate_puzzle(35)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    wrong_board = [row[:] for row in solution]
    current_value = wrong_board[0][0]
    wrong_board[0][0] = 1 if current_value == 9 else current_value + 1

    response = client.post('/check', json={'board': wrong_board})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [[0, 0]]}
