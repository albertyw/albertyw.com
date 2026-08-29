// The three special bilge pieces.
//
//   Crab        immovable; scuttles off when it ends up above the water line.
//               Handled in water.ts, since surfacing is a water question.
//   Puffer fish clicking it makes it expand, clearing itself and the eight
//               pieces around it.
//   Jellyfish   swapping a coloured piece with it clears every piece of that
//               colour on the board.
//
// The original gates these behind rank ("star level").  There is no rank here,
// so all three are in play from the first move.  Their spawn rates are not
// documented anywhere, so the constants below are ours.

import {
  COLUMNS,
  Coord,
  Grid,
  NO_COLOR,
  ROWS,
  Random,
  crabPiece,
  jellyfishPiece,
  pieceColor,
  pufferPiece,
} from './board.js';
import { Water, isSubmerged } from './water.js';

export const JELLYFISH_SPAWN_CHANCE = 0.05;
export const PUFFER_SPAWN_CHANCE = 0.15;
export const CRAB_SPAWN_CHANCE = 0.12;

function randomColumn(random: Random): number {
  return Math.floor(random() * COLUMNS);
}

// A puffer fish clears itself and its eight neighbours, clipped at the edges
// of the board.
export function pufferBlast(grid: Grid, row: number, column: number): Coord[] {
  const cell = grid[row]?.[column];
  if (cell === undefined || cell === null || cell.kind !== 'puffer') {
    return [];
  }
  const cells: Coord[] = [];
  for (let r = Math.max(0, row - 1); r <= Math.min(ROWS - 1, row + 1); r++) {
    for (let c = Math.max(0, column - 1); c <= Math.min(COLUMNS - 1, column + 1); c++) {
      cells.push({ row: r, column: c });
    }
  }
  return cells;
}

export interface JellyfishSwap {
  // The colour the jellyfish was swapped against, and so the colour that is
  // about to be swept off the board.
  color: number;
  jellyfish: Coord;
}

// Inspects a horizontal swap *before* it happens.  Returns null unless exactly
// one side is a jellyfish and the other carries a colour.
export function jellyfishSwap(grid: Grid, row: number, column: number): JellyfishSwap | null {
  if (row < 0 || row >= ROWS || column < 0 || column + 1 >= COLUMNS) {
    return null;
  }
  const left = grid[row][column];
  const right = grid[row][column + 1];
  if (left === null || right === null) {
    return null;
  }
  const leftIsJelly = left.kind === 'jellyfish';
  const rightIsJelly = right.kind === 'jellyfish';
  if (leftIsJelly === rightIsJelly) {
    return null;
  }
  const other = leftIsJelly ? right : left;
  const color = pieceColor(other);
  if (color === NO_COLOR) {
    return null;
  }
  return {
    color: color,
    jellyfish: { row: row, column: leftIsJelly ? column : column + 1 },
  };
}

// Every piece of the given colour, plus the jellyfish that triggered it.
export function jellyfishSweep(grid: Grid, sweep: JellyfishSwap): Coord[] {
  const cells: Coord[] = [{ row: sweep.jellyfish.row, column: sweep.jellyfish.column }];
  for (let row = 0; row < ROWS; row++) {
    for (let column = 0; column < COLUMNS; column++) {
      if (pieceColor(grid[row][column]) === sweep.color) {
        cells.push({ row: row, column: column });
      }
    }
  }
  return cells;
}

// Puffers and jellyfish arrive from the top of the board with the refill.
// Always consumes exactly two random numbers so callers stay deterministic.
export function spawnFloatingSpecials(grid: Grid, random: Random): void {
  const roll = random();
  const column = randomColumn(random);
  const cell = grid[0][column];
  if (cell === null || cell.kind !== 'color') {
    return;
  }
  if (roll < JELLYFISH_SPAWN_CHANCE) {
    grid[0][column] = jellyfishPiece();
  } else if (roll < JELLYFISH_SPAWN_CHANCE + PUFFER_SPAWN_CHANCE) {
    grid[0][column] = pufferPiece(cell.color);
  }
}

// Crabs belong in the bilge, so they appear underwater rather than falling in
// from the top — a crab spawned above the water line would scuttle off
// immediately and be worth nothing.
export function spawnCrab(grid: Grid, water: Water, random: Random): boolean {
  const roll = random();
  const column = randomColumn(random);
  if (roll >= CRAB_SPAWN_CHANCE) {
    return false;
  }
  for (let row = ROWS - 1; row >= 0; row--) {
    if (!isSubmerged(water, row)) {
      return false;
    }
    const cell = grid[row][column];
    if (cell !== null && cell.kind === 'color') {
      grid[row][column] = crabPiece();
      return true;
    }
  }
  return false;
}
