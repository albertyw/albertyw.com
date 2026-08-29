// Bilging game state.
//
// Holds the board, the water, the score and the two-cell cursor, and drives a
// move through to a settled board.  Contains no DOM: render.ts draws whatever
// this produces, which keeps the rules testable on their own.

import {
  COLUMNS,
  Grid,
  ROWS,
  Random,
  applyGravity,
  clearCells,
  createGrid,
  refill,
  resolve,
  swap,
} from './board.js';
import {
  Water,
  createWater,
  drain,
  isFlooded,
  rise,
  surfacedCrabs,
} from './water.js';
import {
  jellyfishSweep,
  jellyfishSwap,
  pufferBlast,
  spawnCrab,
  spawnFloatingSpecials,
} from './specials.js';
import {
  ComboName,
  MOVE_PENALTY,
  classifyStep,
  comboRank,
  crabPoints,
  scoreStep,
} from './scoring.js';

// Set off deliberately rather than matched into, so they pay a flat rate
// instead of a combo value.
export const PUFFER_POINTS = 60;
export const JELLYFISH_POINTS_PER_PIECE = 12;

export interface GameState {
  grid: Grid;
  water: Water;
  score: number;
  moves: number;
  // Best combo of the last move, and how many links its chain ran to.
  combo: ComboName | null;
  chainLength: number;
  // The cursor covers (cursorRow, cursorColumn) and the cell to its right.
  cursorRow: number;
  cursorColumn: number;
  over: boolean;
  random: Random;
}

export function createGame(random: Random): GameState {
  return {
    grid: createGrid(random),
    water: createWater(),
    score: 0,
    moves: 0,
    combo: null,
    chainLength: 0,
    cursorRow: ROWS - 1,
    cursorColumn: 0,
    over: false,
    random: random,
  };
}

export function setCursor(state: GameState, row: number, column: number): void {
  state.cursorRow = Math.min(ROWS - 1, Math.max(0, row));
  state.cursorColumn = Math.min(COLUMNS - 2, Math.max(0, column));
}

export function moveCursor(state: GameState, rowDelta: number, columnDelta: number): void {
  setCursor(state, state.cursorRow + rowDelta, state.cursorColumn + columnDelta);
}

// Runs the board to a standstill: clear runs, let the collapse set off further
// clears, then free any crab the falling pieces carried above the water line —
// which can itself start the whole thing again.
function settle(state: GameState): void {
  let chainIndex = 0;
  let best: ComboName | null = null;
  for (;;) {
    for (const step of resolve(state.grid, state.random)) {
      state.score += scoreStep(step, chainIndex);
      drain(state.water, step.cells.length);
      const name = classifyStep(step);
      if (best === null || comboRank(name) > comboRank(best)) {
        best = name;
      }
      chainIndex++;
    }
    const crabs = surfacedCrabs(state.grid, state.water);
    if (crabs.length === 0) {
      break;
    }
    state.score += crabs.length * crabPoints(state.water);
    clearCells(state.grid, crabs);
    applyGravity(state.grid);
    refill(state.grid, state.random);
  }
  state.chainLength = chainIndex;
  state.combo = best;
  spawnFloatingSpecials(state.grid, state.random);
  spawnCrab(state.grid, state.water, state.random);
}

function spendMove(state: GameState): void {
  state.moves++;
  state.score -= MOVE_PENALTY;
}

// The player's one move: swap the two pieces under the cursor.  A jellyfish
// caught in the swap sweeps its partner's colour off the board instead.
export function performSwap(state: GameState): boolean {
  if (state.over) {
    return false;
  }
  const row = state.cursorRow;
  const column = state.cursorColumn;

  const sweep = jellyfishSwap(state.grid, row, column);
  if (sweep !== null) {
    const cells = jellyfishSweep(state.grid, sweep);
    spendMove(state);
    state.score += JELLYFISH_POINTS_PER_PIECE * cells.length;
    drain(state.water, cells.length);
    clearCells(state.grid, cells);
    applyGravity(state.grid);
    refill(state.grid, state.random);
    settle(state);
    return true;
  }

  if (!swap(state.grid, row, column)) {
    return false;
  }
  spendMove(state);
  settle(state);
  return true;
}

// Clicking a puffer fish pops it, taking the eight pieces around it with it.
export function popPuffer(state: GameState, row: number, column: number): boolean {
  if (state.over) {
    return false;
  }
  const cells = pufferBlast(state.grid, row, column);
  if (cells.length === 0) {
    return false;
  }
  spendMove(state);
  state.score += PUFFER_POINTS;
  drain(state.water, cells.length);
  clearCells(state.grid, cells);
  applyGravity(state.grid);
  refill(state.grid, state.random);
  settle(state);
  return true;
}

// Time passing is the only thing that raises the water here.  In the original
// the rate depends on how badly the ship has been shot up.
export function tick(state: GameState, seconds: number): void {
  if (state.over) {
    return;
  }
  rise(state.water, seconds);
  if (isFlooded(state.water)) {
    state.over = true;
  }
}
