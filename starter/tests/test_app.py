import pytest

import app


@pytest.fixture
def client():
    app.app.config.update(TESTING=True)
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None
    with app.app.test_client() as test_client:
        yield test_client
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None


def test_index_renders_game_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data


def test_new_game_returns_puzzle_with_requested_clues(client):
    response = client.get('/new?clues=40')

    assert response.status_code == 200
    puzzle = response.get_json()['puzzle']
    assert len(puzzle) == app.sudoku_logic.SIZE
    assert sum(cell != app.sudoku_logic.EMPTY for row in puzzle for cell in row) == 40
    assert app.CURRENT['solution'] is not None


def test_new_game_easy_returns_45_clues(client):
    response = client.get('/new?difficulty=Easy')

    assert response.status_code == 200
    data = response.get_json()
    assert data['difficulty'] == 'Easy'
    assert sum(cell != app.sudoku_logic.EMPTY for row in data['puzzle'] for cell in row) == 45


def test_new_game_medium_returns_35_clues(client):
    response = client.get('/new?difficulty=Medium')

    assert response.status_code == 200
    data = response.get_json()
    assert data['difficulty'] == 'Medium'
    assert sum(cell != app.sudoku_logic.EMPTY for row in data['puzzle'] for cell in row) == 35


def test_new_game_hard_returns_25_clues(client):
    response = client.get('/new?difficulty=Hard')

    assert response.status_code == 200
    data = response.get_json()
    assert data['difficulty'] == 'Hard'
    assert sum(cell != app.sudoku_logic.EMPTY for row in data['puzzle'] for cell in row) == 25


def test_new_game_rejects_invalid_difficulty(client):
    response = client.get('/new?difficulty=Extreme')

    assert response.status_code == 400
    assert response.get_json() == {'error': 'Invalid difficulty'}


def test_hint_fills_one_empty_cell_with_solution_value(client):
    client.get('/new?difficulty=Hard')
    board = [row[:] for row in app.CURRENT['puzzle']]
    empty_cells = [
        (row, col)
        for row in range(app.sudoku_logic.SIZE)
        for col in range(app.sudoku_logic.SIZE)
        if board[row][col] == app.sudoku_logic.EMPTY
    ]

    response = client.post('/hint', json={'board': board})
    data = response.get_json()

    assert response.status_code == 200
    assert (data['row'], data['col']) == empty_cells[0]
    assert data['value'] == app.CURRENT['solution'][data['row']][data['col']]


def test_hint_does_not_return_a_cell_that_is_already_filled(client):
    client.get('/new')
    board = [row[:] for row in app.CURRENT['solution']]
    response = client.post('/hint', json={'board': board})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No empty cells available'}


def test_hint_requires_game_in_progress(client):
    response = client.post('/hint', json={'board': []})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_solution_reports_no_incorrect_cells_for_solution(client):
    client.get('/new')
    solution = app.CURRENT['solution']

    response = client.post('/check', json={'board': solution})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_check_solution_reports_incorrect_cell(client):
    client.get('/new')
    board = [row[:] for row in app.CURRENT['solution']]
    board[0][0] = (board[0][0] % app.sudoku_logic.SIZE) + 1

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json()['incorrect'] == [[0, 0]]


def test_check_solution_requires_game_in_progress(client):
    response = client.post('/check', json={'board': []})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}
