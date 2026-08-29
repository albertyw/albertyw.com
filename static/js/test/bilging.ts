import { expect } from 'chai';

import {
  COLUMNS,
  ROWS,
  Cell,
  Grid,
  Random,
  applyGravity,
  clearCells,
  colorPiece,
  crabPiece,
  createGrid,
  emptyGrid,
  findRuns,
  isMovable,
  jellyfishPiece,
  pufferPiece,
  refill,
  resolve,
  runCells,
  swap,
} from '../bilging/board.js';
import {
  BASELINE_ROWS,
  DRAIN_ROWS_PER_PIECE,
  RISE_ROWS_PER_SECOND,
  createWater,
  drain,
  isFlooded,
  isSubmerged,
  rise,
  surfacedCrabs,
  waterLineRow,
} from '../bilging/water.js';
import {
  CRAB_SPAWN_CHANCE,
  JELLYFISH_SPAWN_CHANCE,
  PUFFER_SPAWN_CHANCE,
  jellyfishSweep,
  jellyfishSwap,
  pufferBlast,
  spawnCrab,
  spawnFloatingSpecials,
} from '../bilging/specials.js';

// Deterministic generator so board tests never depend on Math.random.
export function seededRandom(seed: number): Random {
  let state = seed >>> 0;
  return (): number => {
    state = (state + 0x6d2b79f5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function parseCell(character: string): Cell {
  if (character === '.') {
    return null;
  }
  if (character === 'C') {
    return crabPiece();
  }
  if (character === 'J') {
    return jellyfishPiece();
  }
  return colorPiece(Number(character));
}

// Builds a full-height board from a handful of bottom rows.  Everything above
// is padded with a diagonal pattern that cannot form a run of its own, so a
// test only has to write the rows it cares about.
export function gridFromBottomRows(rows: string[]): Grid {
  const grid = emptyGrid();
  const firstRow = ROWS - rows.length;
  for (let row = 0; row < ROWS; row++) {
    for (let column = 0; column < COLUMNS; column++) {
      if (row < firstRow) {
        grid[row][column] = colorPiece((row + column) % COLUMNS);
      } else {
        grid[row][column] = parseCell(rows[row - firstRow][column]);
      }
    }
  }
  return grid;
}

describe('bilging board', function() {
  describe('gridFromBottomRows', function() {
    it('pads with a pattern that contains no runs', function() {
      expect(findRuns(gridFromBottomRows([]))).to.deep.equal([]);
    });
  });

  describe('createGrid', function() {
    it('fills every cell', function() {
      const grid = createGrid(seededRandom(1));
      expect(grid.length).to.equal(ROWS);
      for (const row of grid) {
        expect(row.length).to.equal(COLUMNS);
        for (const cell of row) {
          expect(cell).to.not.equal(null);
        }
      }
    });

    it('never starts with a run already on the board', function() {
      for (let seed = 0; seed < 25; seed++) {
        expect(findRuns(createGrid(seededRandom(seed)))).to.deep.equal([]);
      }
    });
  });

  describe('swap', function() {
    it('exchanges a piece with its right-hand neighbour', function() {
      const grid = gridFromBottomRows(['012345']);
      expect(swap(grid, ROWS - 1, 2)).to.equal(true);
      expect(grid[ROWS - 1][2]).to.deep.equal(colorPiece(3));
      expect(grid[ROWS - 1][3]).to.deep.equal(colorPiece(2));
    });

    it('refuses to swap off the right edge', function() {
      const grid = gridFromBottomRows(['012345']);
      expect(swap(grid, ROWS - 1, COLUMNS - 1)).to.equal(false);
      expect(grid[ROWS - 1][COLUMNS - 1]).to.deep.equal(colorPiece(5));
    });

    it('refuses to swap outside the board', function() {
      const grid = gridFromBottomRows(['012345']);
      expect(swap(grid, ROWS, 0)).to.equal(false);
      expect(swap(grid, -1, 0)).to.equal(false);
      expect(swap(grid, ROWS - 1, -1)).to.equal(false);
    });

    it('refuses to move a crab', function() {
      const grid = gridFromBottomRows(['01C345']);
      expect(swap(grid, ROWS - 1, 1)).to.equal(false);
      expect(swap(grid, ROWS - 1, 2)).to.equal(false);
      expect(grid[ROWS - 1][2]).to.deep.equal(crabPiece());
    });

    it('refuses to move an empty cell', function() {
      const grid = gridFromBottomRows(['01.345']);
      expect(swap(grid, ROWS - 1, 2)).to.equal(false);
    });
  });

  describe('isMovable', function() {
    it('rejects crabs and empty cells but accepts everything else', function() {
      expect(isMovable(colorPiece(0))).to.equal(true);
      expect(isMovable(jellyfishPiece())).to.equal(true);
      expect(isMovable(crabPiece())).to.equal(false);
      expect(isMovable(null)).to.equal(false);
    });
  });

  describe('findRuns', function() {
    it('finds a horizontal run of three', function() {
      const runs = findRuns(gridFromBottomRows(['222345']));
      expect(runs).to.deep.equal([
        { orientation: 'row', row: ROWS - 1, column: 0, length: 3 },
      ]);
    });

    it('finds a run longer than three as a single run', function() {
      const runs = findRuns(gridFromBottomRows(['222245']));
      expect(runs).to.deep.equal([
        { orientation: 'row', row: ROWS - 1, column: 0, length: 4 },
      ]);
    });

    it('finds a vertical run', function() {
      const runs = findRuns(gridFromBottomRows([
        '301234',
        '312345',
        '340123',
      ]));
      expect(runs).to.deep.equal([
        { orientation: 'column', row: ROWS - 3, column: 0, length: 3 },
      ]);
    });

    it('ignores runs of two', function() {
      expect(findRuns(gridFromBottomRows(['220345']))).to.deep.equal([]);
    });

    it('does not match crabs against each other', function() {
      expect(findRuns(gridFromBottomRows(['CCC345']))).to.deep.equal([]);
    });

    it('does not match jellyfish against each other', function() {
      expect(findRuns(gridFromBottomRows(['JJJ345']))).to.deep.equal([]);
    });

    it('lets a puffer fish take part in a run of its own colour', function() {
      const grid = gridFromBottomRows(['221345']);
      grid[ROWS - 1][2] = pufferPiece(2);
      expect(findRuns(grid)).to.deep.equal([
        { orientation: 'row', row: ROWS - 1, column: 0, length: 3 },
      ]);
    });

    it('does not treat empty cells as a run', function() {
      expect(findRuns(gridFromBottomRows(['...345']))).to.deep.equal([]);
    });
  });

  describe('runCells', function() {
    it('expands a run into its cells', function() {
      const cells = runCells([
        { orientation: 'row', row: 4, column: 1, length: 3 },
      ]);
      expect(cells).to.deep.equal([
        { row: 4, column: 1 },
        { row: 4, column: 2 },
        { row: 4, column: 3 },
      ]);
    });

    it('counts the shared cell of two crossing runs only once', function() {
      const cells = runCells([
        { orientation: 'row', row: 4, column: 1, length: 3 },
        { orientation: 'column', row: 3, column: 2, length: 3 },
      ]);
      expect(cells).to.have.length(5);
      expect(cells.filter((c) => c.row === 4 && c.column === 2)).to.have.length(1);
    });
  });

  describe('applyGravity', function() {
    it('drops pieces into the gap below them', function() {
      const grid = gridFromBottomRows([
        '012345',
        '......',
      ]);
      expect(applyGravity(grid)).to.equal(true);
      expect(grid[ROWS - 1][0]).to.deep.equal(colorPiece(0));
      // The whole column slides down, so the gap ends up at the very top.
      expect(grid[0][0]).to.equal(null);
    });

    it('reports when nothing moved', function() {
      expect(applyGravity(gridFromBottomRows(['012345']))).to.equal(false);
    });

    it('drops crabs like any other piece', function() {
      const grid = gridFromBottomRows([
        'C12345',
        '.12345',
      ]);
      applyGravity(grid);
      expect(grid[ROWS - 1][0]).to.deep.equal(crabPiece());
    });
  });

  describe('clearCells and refill', function() {
    it('empties the given cells and then fills every gap', function() {
      const grid = gridFromBottomRows(['012345']);
      clearCells(grid, [{ row: ROWS - 1, column: 0 }]);
      expect(grid[ROWS - 1][0]).to.equal(null);
      refill(grid, seededRandom(7));
      expect(grid[ROWS - 1][0]).to.not.equal(null);
    });
  });

  describe('resolve', function() {
    it('does nothing on a quiet board', function() {
      expect(resolve(gridFromBottomRows([]), seededRandom(3))).to.deep.equal([]);
    });

    it('clears a run and leaves the board full and quiet', function() {
      const grid = gridFromBottomRows(['222345']);
      const steps = resolve(grid, seededRandom(11));
      expect(steps.length).to.be.at.least(1);
      expect(steps[0].cells).to.have.length(3);
      expect(findRuns(grid)).to.deep.equal([]);
      for (const row of grid) {
        for (const cell of row) {
          expect(cell).to.not.equal(null);
        }
      }
    });

    it('reports each link of a chain as its own step', function() {
      // The run of 0s in the bottom row clears first.  Columns 2, 3 and 4 then
      // fall by one, which slides another 1 into the bottom row alongside the
      // two already there and sets off a second clear.
      const grid = gridFromBottomRows([
        '201210',
        '110002',
      ]);
      const steps = resolve(grid, seededRandom(5));
      expect(steps.length).to.be.at.least(2);
      expect(steps[0].runs).to.deep.include({
        orientation: 'row', row: ROWS - 1, column: 2, length: 3,
      });
      expect(steps[1].runs).to.deep.include({
        orientation: 'row', row: ROWS - 1, column: 0, length: 3,
      });
    });
  });
});

describe('bilging water', function() {
  describe('createWater', function() {
    it('starts at the uncleaerable baseline', function() {
      expect(createWater().level).to.equal(BASELINE_ROWS);
    });
  });

  describe('rise', function() {
    it('climbs at a steady rate', function() {
      const water = createWater();
      rise(water, 10);
      expect(water.level).to.be.closeTo(BASELINE_ROWS + 10 * RISE_ROWS_PER_SECOND, 1e-9);
    });

    it('never climbs past the top of the board', function() {
      const water = createWater();
      rise(water, 100000);
      expect(water.level).to.equal(ROWS);
    });
  });

  describe('drain', function() {
    it('falls in proportion to the pieces cleared', function() {
      const water = { level: 6 };
      drain(water, 4);
      expect(water.level).to.be.closeTo(6 - 4 * DRAIN_ROWS_PER_PIECE, 1e-9);
    });

    it('stops at the baseline no matter how much is cleared', function() {
      const water = { level: 6 };
      drain(water, 1000);
      expect(water.level).to.equal(BASELINE_ROWS);
    });
  });

  describe('isSubmerged and waterLineRow', function() {
    it('puts the baseline water under the bottom three rows', function() {
      const water = createWater();
      expect(waterLineRow(water)).to.equal(ROWS - BASELINE_ROWS);
      expect(isSubmerged(water, ROWS - 1)).to.equal(true);
      expect(isSubmerged(water, ROWS - BASELINE_ROWS)).to.equal(true);
      expect(isSubmerged(water, ROWS - BASELINE_ROWS - 1)).to.equal(false);
    });

    it('treats a partly covered row as above the line', function() {
      const water = { level: 3.5 };
      expect(isSubmerged(water, ROWS - 4)).to.equal(false);
      expect(waterLineRow(water)).to.equal(ROWS - 3);
    });
  });

  describe('isFlooded', function() {
    it('only reports a loss once the water reaches the top', function() {
      expect(isFlooded({ level: ROWS - 0.01 })).to.equal(false);
      expect(isFlooded({ level: ROWS })).to.equal(true);
    });
  });

  describe('surfacedCrabs', function() {
    it('finds crabs sitting above the water line', function() {
      const grid = gridFromBottomRows([
        'C12345',
        '012345',
        '012345',
        '01234C',
      ]);
      // Baseline water covers the bottom three rows, so only the upper crab
      // has surfaced.
      expect(surfacedCrabs(grid, createWater())).to.deep.equal([
        { row: ROWS - 4, column: 0 },
      ]);
    });

    it('finds nothing when the water covers every crab', function() {
      const grid = gridFromBottomRows(['C12345']);
      expect(surfacedCrabs(grid, createWater())).to.deep.equal([]);
    });

    it('surfaces a crab once the water is pumped down past it', function() {
      const grid = gridFromBottomRows(['C12345']);
      const water = createWater();
      expect(surfacedCrabs(grid, water)).to.deep.equal([]);
      water.level = 0;
      expect(surfacedCrabs(grid, water)).to.deep.equal([
        { row: ROWS - 1, column: 0 },
      ]);
    });
  });
});

// Feeds a fixed sequence of numbers so spawn rolls can be pinned down exactly.
function scriptedRandom(values: number[]): Random {
  let index = 0;
  return (): number => values[index++];
}

describe('bilging specials', function() {
  describe('pufferBlast', function() {
    it('clears the puffer and its eight neighbours', function() {
      const grid = gridFromBottomRows([]);
      grid[5][3] = pufferPiece(1);
      const cells = pufferBlast(grid, 5, 3);
      expect(cells).to.have.length(9);
      expect(cells).to.deep.include({ row: 4, column: 2 });
      expect(cells).to.deep.include({ row: 5, column: 3 });
      expect(cells).to.deep.include({ row: 6, column: 4 });
    });

    it('clips the blast at the corner of the board', function() {
      const grid = gridFromBottomRows([]);
      grid[0][0] = pufferPiece(1);
      expect(pufferBlast(grid, 0, 0)).to.have.length(4);
    });

    it('does nothing when the cell is not a puffer', function() {
      const grid = gridFromBottomRows([]);
      expect(pufferBlast(grid, 5, 3)).to.deep.equal([]);
      expect(pufferBlast(grid, -1, 0)).to.deep.equal([]);
    });
  });

  describe('jellyfishSwap', function() {
    it('reads the colour when the jellyfish is on the left', function() {
      const grid = gridFromBottomRows(['J12345']);
      expect(jellyfishSwap(grid, ROWS - 1, 0)).to.deep.equal({
        color: 1,
        jellyfish: { row: ROWS - 1, column: 0 },
      });
    });

    it('reads the colour when the jellyfish is on the right', function() {
      const grid = gridFromBottomRows(['1J2345']);
      expect(jellyfishSwap(grid, ROWS - 1, 0)).to.deep.equal({
        color: 1,
        jellyfish: { row: ROWS - 1, column: 1 },
      });
    });

    it('ignores a swap with no jellyfish in it', function() {
      const grid = gridFromBottomRows(['012345']);
      expect(jellyfishSwap(grid, ROWS - 1, 0)).to.equal(null);
    });

    it('ignores two jellyfish swapped together', function() {
      const grid = gridFromBottomRows(['JJ2345']);
      expect(jellyfishSwap(grid, ROWS - 1, 0)).to.equal(null);
    });

    it('ignores a jellyfish swapped with a colourless piece', function() {
      const grid = gridFromBottomRows(['JC2345']);
      expect(jellyfishSwap(grid, ROWS - 1, 0)).to.equal(null);
    });

    it('ignores a swap with an empty cell or off the board', function() {
      const grid = gridFromBottomRows(['J.2345']);
      expect(jellyfishSwap(grid, ROWS - 1, 0)).to.equal(null);
      expect(jellyfishSwap(grid, ROWS - 1, COLUMNS - 1)).to.equal(null);
    });
  });

  describe('jellyfishSweep', function() {
    it('collects every piece of the colour plus the jellyfish itself', function() {
      const grid = gridFromBottomRows(['J12145']);
      const sweep = jellyfishSwap(grid, ROWS - 1, 0);
      expect(sweep).to.not.equal(null);
      const cells = jellyfishSweep(grid, sweep!);
      expect(cells).to.deep.include({ row: ROWS - 1, column: 0 });
      expect(cells).to.deep.include({ row: ROWS - 1, column: 1 });
      expect(cells).to.deep.include({ row: ROWS - 1, column: 3 });
      for (const cell of cells) {
        const piece = grid[cell.row][cell.column];
        const isTheJellyfish = cell.row === ROWS - 1 && cell.column === 0;
        expect(isTheJellyfish || piece!.color === 1).to.equal(true);
      }
    });
  });

  describe('spawnFloatingSpecials', function() {
    it('turns a top-row piece into a jellyfish on a low roll', function() {
      const grid = gridFromBottomRows([]);
      spawnFloatingSpecials(grid, scriptedRandom([0, 2 / COLUMNS]));
      expect(grid[0][2]!.kind).to.equal('jellyfish');
    });

    it('turns a top-row piece into a puffer of the same colour', function() {
      const grid = gridFromBottomRows([]);
      const color = grid[0][2]!.color;
      spawnFloatingSpecials(grid, scriptedRandom([JELLYFISH_SPAWN_CHANCE, 2 / COLUMNS]));
      expect(grid[0][2]!.kind).to.equal('puffer');
      expect(grid[0][2]!.color).to.equal(color);
    });

    it('leaves the board alone on a high roll', function() {
      const grid = gridFromBottomRows([]);
      const roll = JELLYFISH_SPAWN_CHANCE + PUFFER_SPAWN_CHANCE;
      spawnFloatingSpecials(grid, scriptedRandom([roll, 2 / COLUMNS]));
      expect(grid[0][2]!.kind).to.equal('color');
    });

    it('never replaces a piece that is already special', function() {
      const grid = gridFromBottomRows([]);
      grid[0][2] = crabPiece();
      spawnFloatingSpecials(grid, scriptedRandom([0, 2 / COLUMNS]));
      expect(grid[0][2]!.kind).to.equal('crab');
    });
  });

  describe('spawnCrab', function() {
    it('drops a crab into the bilge below the water line', function() {
      const grid = gridFromBottomRows([]);
      const placed = spawnCrab(grid, createWater(), scriptedRandom([0, 2 / COLUMNS]));
      expect(placed).to.equal(true);
      expect(grid[ROWS - 1][2]!.kind).to.equal('crab');
    });

    it('does nothing on a high roll', function() {
      const grid = gridFromBottomRows([]);
      const roll = CRAB_SPAWN_CHANCE;
      expect(spawnCrab(grid, createWater(), scriptedRandom([roll, 2 / COLUMNS]))).to.equal(false);
      expect(grid[ROWS - 1][2]!.kind).to.equal('color');
    });

    it('gives up when the whole submerged column is already crabs', function() {
      const grid = gridFromBottomRows([
        'C12345',
        'C12345',
        'C12345',
      ]);
      expect(spawnCrab(grid, createWater(), scriptedRandom([0, 0]))).to.equal(false);
    });

    it('gives up when a fully flooded column has no room left', function() {
      const grid = gridFromBottomRows([]);
      for (let row = 0; row < ROWS; row++) {
        grid[row][2] = crabPiece();
      }
      const flooded = { level: ROWS };
      expect(spawnCrab(grid, flooded, scriptedRandom([0, 2 / COLUMNS]))).to.equal(false);
    });
  });
});
