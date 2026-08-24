// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let timerInterval = null;
let elapsedSeconds = 0;
let currentDifficulty = 'Medium';
let gameCompleted = false;

function startTimer() {
  clearInterval(timerInterval);
  elapsedSeconds = 0;
  document.getElementById('timer').innerText = 'Time: 0 seconds';
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    document.getElementById('timer').innerText = `Time: ${elapsedSeconds} seconds`;
  }, 1000);
}

function getScores() {
  return JSON.parse(localStorage.getItem('sudokuScores')) || [];
}

function saveScore() {
  const playerName =
    document.getElementById('player-name').value.trim() || 'Anonymous';

  const scores = getScores();

  scores.push({
    name: playerName,
    time: elapsedSeconds,
    difficulty: currentDifficulty
  });

  scores.sort((a, b) => a.time - b.time);

  const topTen = scores.slice(0, 10);

  localStorage.setItem('sudokuScores', JSON.stringify(topTen));

  renderScores();
}

function renderScores() {
  const scoreList = document.getElementById('score-list');
  const scores = getScores();

  scoreList.innerHTML = '';

  scores.forEach((score) => {
    const item = document.createElement('li');

    item.textContent =
      `${score.name} - ${score.time} seconds - ${score.difficulty}`;

    scoreList.appendChild(item);
  });
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

function getCurrentBoard() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const value = inputs[i * SIZE + j].value;
      board[i][j] = value ? parseInt(value, 10) : 0;
    }
  }
  return board;
}

 async function newGame() {
 const difficulty = document.getElementById('difficulty').value;

 currentDifficulty = difficulty;
 gameCompleted = false;

 const res = await fetch(
   `/new?difficulty=${encodeURIComponent(difficulty)}`
 );
 const data = await res.json();
 renderPuzzle(data.puzzle);
 startTimer();
 document.getElementById('message').innerText = '';
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = getCurrentBoard();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
  msg.style.color = '#388e3c';
  msg.innerText = 'Congratulations! You solved it!';

  if (!gameCompleted) {
    gameCompleted = true;
    clearInterval(timerInterval);
    saveScore();
  }
} else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

async function requestHint() {
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board: getCurrentBoard()})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }

  const input = document.querySelector(
    `.sudoku-cell[data-row="${data.row}"][data-col="${data.col}"]`
  );
  input.value = data.value;
  input.disabled = true;
  input.className = 'sudoku-cell prefilled';
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint').addEventListener('click', requestHint);

  renderScores();
  newGame();
});