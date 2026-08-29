// DOM rendering and input for the bilging puzzle.
//
// All the rules live in the other modules in this directory; this file only
// draws them and turns clicks and key presses into moves.

import '../../css/bilging.css';

import { COLUMNS, Cell, ROWS } from './board.js';
import { GameState, createGame, moveCursor, performSwap, popPuffer, setCursor, tick } from './game.js';

const CONTAINER_ID = 'bilging';
// A tab switch can hand back an enormous delta; cap it so the bilge does not
// flood while the page was in the background.
const MAX_FRAME_SECONDS = 0.25;

const SPECIAL_GLYPHS: Record<string, string> = {
  crab: '\u{1F980}',
  puffer: '\u{1F421}',
  jellyfish: '\u{1F30A}',
};

interface View {
  frame: HTMLDivElement;
  cells: HTMLDivElement[];
  water: HTMLDivElement;
  score: HTMLElement;
  moves: HTMLElement;
  combo: HTMLElement;
  overlay: HTMLDivElement;
  finalScore: HTMLElement;
}

function element<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  className: string,
  text?: string,
): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  node.className = className;
  if (text !== undefined) {
    node.textContent = text;
  }
  return node;
}

function statBlock(label: string): { block: HTMLDivElement; value: HTMLElement } {
  const block = element('div', 'bilging-stat');
  block.appendChild(element('span', 'bilging-stat-label', label));
  const value = element('strong', 'bilging-stat-value', '0');
  block.appendChild(value);
  return { block: block, value: value };
}

function buildView(container: HTMLElement): View {
  container.textContent = '';

  const frame = element('div', 'bilging-frame');
  // Focusable so arrow keys and space reach the board without stealing them
  // from the rest of the page.
  frame.tabIndex = 0;

  const hud = element('div', 'bilging-hud');
  const score = statBlock('Score');
  const moves = statBlock('Moves');
  const combo = statBlock('Combo');
  combo.value.textContent = '—';
  hud.append(score.block, moves.block, combo.block);

  const board = element('div', 'bilging-board');
  const water = element('div', 'bilging-water');
  const cellLayer = element('div', 'bilging-cells');
  const cells: HTMLDivElement[] = [];
  for (let row = 0; row < ROWS; row++) {
    for (let column = 0; column < COLUMNS; column++) {
      const cell = element('div', 'bilging-cell');
      cell.dataset.row = String(row);
      cell.dataset.column = String(column);
      cells.push(cell);
      cellLayer.appendChild(cell);
    }
  }

  const overlay = element('div', 'bilging-overlay');
  overlay.appendChild(element('p', 'bilging-overlay-title', 'Sunk!'));
  const finalScore = element('p', 'bilging-overlay-score', '');
  overlay.appendChild(finalScore);
  const again = element('button', 'bilging-again', 'Play again');
  again.type = 'button';
  overlay.appendChild(again);

  board.append(water, cellLayer, overlay);
  frame.append(hud, board);
  frame.appendChild(element(
    'p',
    'bilging-help',
    'Click the board, then move with the mouse or arrow keys and swap with ' +
    'click or space. Swaps are horizontal only. Click a puffer fish to pop it.',
  ));
  container.appendChild(frame);

  return {
    frame: frame,
    cells: cells,
    water: water,
    score: score.value,
    moves: moves.value,
    combo: combo.value,
    overlay: overlay,
    finalScore: finalScore,
  };
}

export function cellClass(cell: Cell): string {
  if (cell === null) {
    return 'bilging-cell';
  }
  if (cell.kind === 'color') {
    return `bilging-cell bilging-color-${cell.color}`;
  }
  if (cell.kind === 'puffer') {
    return `bilging-cell bilging-color-${cell.color} bilging-special`;
  }
  return `bilging-cell bilging-${cell.kind} bilging-special`;
}

function draw(state: GameState, view: View): void {
  for (let row = 0; row < ROWS; row++) {
    for (let column = 0; column < COLUMNS; column++) {
      const cell = state.grid[row][column];
      const node = view.cells[row * COLUMNS + column];
      let className = cellClass(cell);
      const underCursor = row === state.cursorRow &&
        (column === state.cursorColumn || column === state.cursorColumn + 1);
      if (underCursor) {
        className += ' bilging-cursor';
      }
      if (node.className !== className) {
        node.className = className;
      }
      const glyph = cell === null ? '' : (SPECIAL_GLYPHS[cell.kind] ?? '');
      if (node.textContent !== glyph) {
        node.textContent = glyph;
      }
    }
  }

  view.water.style.height = `${(state.water.level / ROWS) * 100}%`;
  view.score.textContent = String(state.score);
  view.moves.textContent = String(state.moves);
  view.combo.textContent = state.combo === null ? '—' :
    state.chainLength > 1 ? `${state.combo} x${state.chainLength}` : state.combo;
  view.overlay.classList.toggle('bilging-overlay-shown', state.over);
  view.finalScore.textContent = `${state.score} points in ${state.moves} moves`;
}

function coordOf(target: EventTarget | null): { row: number; column: number } | null {
  if (!(target instanceof HTMLElement)) {
    return null;
  }
  const cell = target.closest('.bilging-cell');
  if (!(cell instanceof HTMLElement) || cell.dataset.row === undefined) {
    return null;
  }
  return { row: Number(cell.dataset.row), column: Number(cell.dataset.column) };
}

function bindInput(state: GameState, view: View, restart: () => void): void {
  view.frame.addEventListener('mousemove', (event) => {
    const coord = coordOf(event.target);
    if (coord !== null) {
      setCursor(state, coord.row, coord.column);
    }
  });

  view.frame.addEventListener('click', (event) => {
    if (event.target instanceof HTMLElement && event.target.closest('.bilging-again')) {
      restart();
      return;
    }
    const coord = coordOf(event.target);
    if (coord === null) {
      return;
    }
    // A click straight onto a puffer fish pops it; anything else is a swap.
    if (!popPuffer(state, coord.row, coord.column)) {
      setCursor(state, coord.row, coord.column);
      performSwap(state);
    }
  });

  view.frame.addEventListener('keydown', (event) => {
    switch (event.key) {
    case 'ArrowLeft':
      moveCursor(state, 0, -1);
      break;
    case 'ArrowRight':
      moveCursor(state, 0, 1);
      break;
    case 'ArrowUp':
      moveCursor(state, -1, 0);
      break;
    case 'ArrowDown':
      moveCursor(state, 1, 0);
      break;
    case ' ':
    case 'Enter':
      performSwap(state);
      break;
    default:
      return;
    }
    event.preventDefault();
  });
}

export function main(): void {
  const container = document.getElementById(CONTAINER_ID);
  if (container === null) {
    return;
  }
  const view = buildView(container);
  const state = createGame(Math.random);
  // Reset in place rather than rebinding, so the handlers and the frame loop
  // keep pointing at the live game.
  const restart = (): void => {
    Object.assign(state, createGame(Math.random));
  };
  bindInput(state, view, restart);

  // Paint once up front so the board is there immediately rather than blank
  // until the first animation frame lands.
  draw(state, view);

  let previous = performance.now();
  const step = (now: number): void => {
    // Stop the loop if the board has been taken off the page.
    if (!container.isConnected) {
      return;
    }
    const seconds = Math.min(MAX_FRAME_SECONDS, (now - previous) / 1000);
    previous = now;
    tick(state, seconds);
    draw(state, view);
    window.requestAnimationFrame(step);
  };
  window.requestAnimationFrame(step);
}
