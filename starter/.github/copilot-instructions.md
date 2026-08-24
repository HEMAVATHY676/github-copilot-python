# Sudoku Game Development Instructions

## Project Context
This project is a Flask-based Sudoku game with a JavaScript frontend.

## Coding Guidelines
- Keep the existing Flask routes and project structure intact.
- Use clear and simple Python and JavaScript.
- Reuse existing functions instead of duplicating logic.
- Keep frontend and backend responsibilities separate.
- Validate user input before processing it.
- Return clear JSON responses from Flask APIs.
- Handle invalid requests with appropriate HTTP status codes.

## Sudoku Rules
- The Sudoku board must remain a valid 9x9 grid.
- Generated puzzles must have exactly one valid solution.
- Prefilled cells must not be editable by the user.
- User-entered values must be checked against the solution.
- Hints should fill only an empty editable cell.

## Testing
- Add or update pytest tests when backend behavior changes.
- Run the complete test suite after making changes.
- Do not consider a feature complete until the relevant tests pass.

## Code Review
Before accepting a Copilot suggestion:
1. Check whether it matches the existing project structure.
2. Check whether it introduces unnecessary changes.
3. Verify the logic with tests or manual testing.
4. Reject or modify suggestions that do not satisfy these requirements.