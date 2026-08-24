# Sudoku Project Copilot Instructions

## Project Overview

This is a Flask-based Sudoku web application.

The backend is written in Python using Flask.
The Sudoku game logic is implemented in `sudoku_logic.py`.
The frontend uses HTML, CSS, and vanilla JavaScript.

## Project Structure

- `app.py` - Flask application and API routes
- `sudoku_logic.py` - Sudoku generation, validation, and solving logic
- `templates/index.html` - main web page
- `static/main.js` - frontend game interaction
- `static/styles.css` - frontend styling
- `tests/` - automated tests

## Coding Standards

- Use clear, readable Python and JavaScript.
- Prefer small, focused, reusable functions.
- Avoid unnecessary duplication.
- Add comments for non-obvious logic.
- Preserve existing functionality when refactoring.
- Handle invalid user input and API errors gracefully.
- Do not introduce unnecessary dependencies.

## Sudoku Requirements

- Every generated puzzle must have exactly one valid solution.
- Difficulty levels must control the number of prefilled cells.
- Prefilled cells must not be editable.
- User-entered values must be validated.
- Incorrect entries should receive clear visual feedback.
- Hints must provide a valid value for an empty cell.
- A completed puzzle must display a success message.

## Frontend Requirements

- Use semantic HTML where appropriate.
- Keep the interface responsive on desktop and mobile.
- Maintain keyboard accessibility.
- Ensure text and controls remain readable in light and dark modes.
- Use clear visual states for selected, prefilled, incorrect, and hinted cells.

## Testing

- Use pytest for Python tests.
- Run the complete test suite after significant changes.
- Do not consider a feature complete until its behavior has been tested.
- Preserve existing tests while adding new tests for new functionality.

## Important Development Rule

Before accepting a Copilot suggestion, review the proposed code for correctness, security, maintainability, and compatibility with the existing project.

Reject or modify suggestions that do not satisfy the project requirements.