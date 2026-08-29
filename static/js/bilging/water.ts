// Bilge water level.
//
// Every bilge puzzle starts with three rows of water at the bottom.  That
// baseline cannot be pumped away; it is the floor the level returns to when
// the player is doing well.  Poor play lets the water climb, and the puzzle is
// lost when it reaches the top of the board.
//
// In the original the rise rate is driven by how badly the ship has been
// damaged.  There is no ship here, so the rate is a constant.

import { Coord, Grid, ROWS } from './board.js';

// Rows of water that can never be cleared.
export const BASELINE_ROWS = 3;

// Tuning constants.  The wiki documents the ordering of these effects but no
// numbers, so these are chosen by feel and kept together to stay adjustable.
export const RISE_ROWS_PER_SECOND = 0.025;
export const DRAIN_ROWS_PER_PIECE = 0.09;

export interface Water {
  // Height of the water in rows, measured up from the bottom of the board.
  level: number;
}

export function createWater(): Water {
  return { level: BASELINE_ROWS };
}

export function rise(water: Water, seconds: number): void {
  water.level = Math.min(ROWS, water.level + seconds * RISE_ROWS_PER_SECOND);
}

// Clearing pieces works the pump.  The level never falls below the baseline,
// so a good run banks nothing for later — it just buys time.
export function drain(water: Water, pieceCount: number): void {
  const drained = water.level - pieceCount * DRAIN_ROWS_PER_PIECE;
  water.level = Math.max(BASELINE_ROWS, drained);
}

export function isSubmerged(water: Water, row: number): boolean {
  return row >= ROWS - water.level;
}

// The topmost row that is fully underwater.  Equals ROWS when the board is dry.
export function waterLineRow(water: Water): number {
  return Math.ceil(ROWS - water.level);
}

export function isFlooded(water: Water): boolean {
  return water.level >= ROWS;
}

// Crabs scuttle off the board once they are no longer underwater.  They are
// immovable, so the only way to free one is to clear the pieces beneath it and
// let it ride the collapse upwards — or to pump the water down past it.
export function surfacedCrabs(grid: Grid, water: Water): Coord[] {
  const surfaced: Coord[] = [];
  for (let row = 0; row < ROWS; row++) {
    if (isSubmerged(water, row)) {
      continue;
    }
    for (let column = 0; column < grid[row].length; column++) {
      const cell = grid[row][column];
      if (cell !== null && cell.kind === 'crab') {
        surfaced.push({ row: row, column: column });
      }
    }
  }
  return surfaced;
}
