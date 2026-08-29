// Board model for the Bilging puzzle from Yohoho! Puzzle Pirates.
//
// The defining rule, and the one that separates bilging from Bejeweled-style
// match-3: pieces are only ever swapped horizontally, with their immediate
// right-hand neighbour.  There is no vertical swap.

export const COLUMNS = 6;
export const ROWS = 12;
export const COLOR_COUNT = 6;
export const MIN_RUN = 3;

export type PieceKind = 'color' | 'crab' | 'puffer' | 'jellyfish';

export interface Piece {
  kind: PieceKind;
  // Index into the colour palette.  Crabs and jellyfish carry NO_COLOR because
  // they never take part in a matching run.
  color: number;
}

export const NO_COLOR = -1;

// A cell is empty only transiently, while pieces are falling into it.
export type Cell = Piece | null;

// grid[row][column], with row 0 at the top of the board.
export type Grid = Cell[][];

export type Random = () => number;

export interface Coord {
  row: number;
  column: number;
}

export type Orientation = 'row' | 'column';

// A single run of three or more identical pieces.  Scoring reads the runs
// rather than the flattened cells so it can tell a 5-in-a-row from an
// intersection of a 3-row and a 3-column.
export interface Run {
  orientation: Orientation;
  row: number;
  column: number;
  length: number;
}

// One resolution step: everything that cleared simultaneously.  A chain
// produces several steps, each triggered by the collapse of the one before it.
export interface ClearStep {
  runs: Run[];
  cells: Coord[];
}

export function colorPiece(color: number): Piece {
  return { kind: 'color', color: color };
}

export function crabPiece(): Piece {
  return { kind: 'crab', color: NO_COLOR };
}

export function pufferPiece(color: number): Piece {
  return { kind: 'puffer', color: color };
}

export function jellyfishPiece(): Piece {
  return { kind: 'jellyfish', color: NO_COLOR };
}

// Crabs are fixtures of the board; they cannot be dragged around, and only
// leave when they surface above the water line.
export function isMovable(cell: Cell): boolean {
  return cell !== null && cell.kind !== 'crab';
}

// Only coloured pieces form runs.  A puffer fish keeps a colour so it can be
// caught up in a run, but it is the click that makes it useful.
export function pieceColor(cell: Cell): number {
  if (cell === null) {
    return NO_COLOR;
  }
  if (cell.kind === 'color' || cell.kind === 'puffer') {
    return cell.color;
  }
  return NO_COLOR;
}

function randomColor(random: Random): number {
  return Math.floor(random() * COLOR_COUNT);
}

export function emptyGrid(): Grid {
  const grid: Grid = [];
  for (let row = 0; row < ROWS; row++) {
    grid.push(new Array<Cell>(COLUMNS).fill(null));
  }
  return grid;
}

// Builds a full board that has no runs already on it, so the player is never
// handed free points at the start of a game.
export function createGrid(random: Random): Grid {
  const grid = emptyGrid();
  for (let row = 0; row < ROWS; row++) {
    for (let column = 0; column < COLUMNS; column++) {
      grid[row][column] = colorPiece(randomColor(random));
    }
  }
  removeExistingRuns(grid, random);
  return grid;
}

// Re-rolls any piece that sits inside a run until the board is quiet.  Each
// re-roll can only shorten runs, so this settles quickly.
export function removeExistingRuns(grid: Grid, random: Random): void {
  let runs = findRuns(grid);
  while (runs.length > 0) {
    for (const coord of runCells(runs)) {
      const cell = grid[coord.row][coord.column];
      if (cell !== null && cell.kind === 'color') {
        cell.color = randomColor(random);
      }
    }
    runs = findRuns(grid);
  }
}

// Swaps the piece at (row, column) with its right-hand neighbour.  Returns
// false, leaving the grid untouched, when the swap is not legal.
export function swap(grid: Grid, row: number, column: number): boolean {
  if (row < 0 || row >= ROWS || column < 0 || column + 1 >= COLUMNS) {
    return false;
  }
  const left = grid[row][column];
  const right = grid[row][column + 1];
  if (!isMovable(left) || !isMovable(right)) {
    return false;
  }
  grid[row][column] = right;
  grid[row][column + 1] = left;
  return true;
}

function scanLine(
  grid: Grid,
  orientation: Orientation,
  fixed: number,
  length: number,
): Run[] {
  const runs: Run[] = [];
  let start = 0;
  let color = NO_COLOR;
  const cellAt = (index: number): Cell => (
    orientation === 'row' ? grid[fixed][index] : grid[index][fixed]
  );

  const flush = (end: number): void => {
    if (color !== NO_COLOR && end - start >= MIN_RUN) {
      runs.push({
        orientation: orientation,
        row: orientation === 'row' ? fixed : start,
        column: orientation === 'row' ? start : fixed,
        length: end - start,
      });
    }
  };

  for (let index = 0; index < length; index++) {
    const current = pieceColor(cellAt(index));
    if (current !== color) {
      flush(index);
      start = index;
      color = current;
    }
  }
  flush(length);
  return runs;
}

// Every run of three or more matching pieces currently on the board.
export function findRuns(grid: Grid): Run[] {
  const runs: Run[] = [];
  for (let row = 0; row < ROWS; row++) {
    runs.push(...scanLine(grid, 'row', row, COLUMNS));
  }
  for (let column = 0; column < COLUMNS; column++) {
    runs.push(...scanLine(grid, 'column', column, ROWS));
  }
  return runs;
}

// Flattens overlapping runs into the set of cells they cover.  Two runs that
// cross share a cell, and that cell must only be counted once.
export function runCells(runs: Run[]): Coord[] {
  const seen = new Set<number>();
  const cells: Coord[] = [];
  for (const run of runs) {
    for (let offset = 0; offset < run.length; offset++) {
      const row = run.orientation === 'row' ? run.row : run.row + offset;
      const column = run.orientation === 'row' ? run.column + offset : run.column;
      const key = row * COLUMNS + column;
      if (!seen.has(key)) {
        seen.add(key);
        cells.push({ row: row, column: column });
      }
    }
  }
  return cells;
}

export function clearCells(grid: Grid, cells: Coord[]): void {
  for (const coord of cells) {
    grid[coord.row][coord.column] = null;
  }
}

// Settles pieces downwards into empty cells.  Crabs fall like everything else;
// they are immovable by the player, not immune to gravity.
export function applyGravity(grid: Grid): boolean {
  let moved = false;
  for (let column = 0; column < COLUMNS; column++) {
    let target = ROWS - 1;
    for (let row = ROWS - 1; row >= 0; row--) {
      const cell = grid[row][column];
      if (cell === null) {
        continue;
      }
      if (row !== target) {
        grid[target][column] = cell;
        grid[row][column] = null;
        moved = true;
      }
      target--;
    }
  }
  return moved;
}

export function refill(grid: Grid, random: Random): void {
  for (let row = 0; row < ROWS; row++) {
    for (let column = 0; column < COLUMNS; column++) {
      if (grid[row][column] === null) {
        grid[row][column] = colorPiece(randomColor(random));
      }
    }
  }
}

// Clears runs, drops the survivors, refills from the top, and repeats for as
// long as the collapse keeps producing new runs.  Each iteration is one link
// of a chain, and is returned separately so scoring can reward the chain.
export function resolve(grid: Grid, random: Random): ClearStep[] {
  const steps: ClearStep[] = [];
  for (;;) {
    const runs = findRuns(grid);
    if (runs.length === 0) {
      return steps;
    }
    const cells = runCells(runs);
    steps.push({ runs: runs, cells: cells });
    clearCells(grid, cells);
    applyGravity(grid);
    refill(grid, random);
  }
}
