// Bilging scoring.
//
// The interesting part is naming the clear.  Bilging does not score a clear by
// how many pieces went away; it scores the *shape*, and specifically how many
// runs crossed each other.  A row of three and a column of three that share a
// cell are worth far more than the six pieces they cover.
//
// The combo ladder is documented on YPPedia.  The point values behind it are
// not, so the numbers below are ours.

import { BASELINE_ROWS, Water } from './water.js';
import { ClearStep, ROWS, Run } from './board.js';

export type ComboName =
  | 'Clear'
  | 'Good'
  | 'Great'
  | 'Arrr!'
  | 'Har!'
  | 'Yarrr!'
  | 'Bingo!'
  | 'Sea Donkey!'
  | 'Vegas!';

// Ascending value.  Index into this array is a combo's rank.
export const COMBO_ORDER: ComboName[] = [
  'Clear',
  'Good',
  'Great',
  'Arrr!',
  'Har!',
  'Yarrr!',
  'Bingo!',
  'Sea Donkey!',
  'Vegas!',
];

export const COMBO_POINTS: Record<ComboName, number> = {
  'Clear': 10,
  'Good': 25,
  'Great': 50,
  'Arrr!': 80,
  'Har!': 130,
  'Yarrr!': 200,
  'Bingo!': 300,
  'Sea Donkey!': 400,
  'Vegas!': 600,
};

export const POINTS_PER_PIECE = 2;
// Each further link of a chain adds half the base value again.
export const CHAIN_BONUS = 0.5;
// Scoring rewards efficiency, so every move made costs a little.  Clearing the
// same pieces in fewer moves therefore scores higher.
export const MOVE_PENALTY = 3;
export const CRAB_BASE_POINTS = 20;
export const CRAB_FLOOD_POINTS = 180;

export function comboRank(name: ComboName): number {
  return COMBO_ORDER.indexOf(name);
}

// Two runs intersect when a row run and a column run share a cell.  Runs of
// the same orientation are always disjoint — an overlap would have been found
// as one longer run.
function intersects(a: Run, b: Run): boolean {
  if (a.orientation === b.orientation) {
    return false;
  }
  const row = a.orientation === 'row' ? a : b;
  const column = a.orientation === 'row' ? b : a;
  return column.column >= row.column &&
    column.column < row.column + row.length &&
    row.row >= column.row &&
    row.row < column.row + column.length;
}

// Splits a step's runs into connected clusters.  Each cluster is one combo.
export function groupRuns(runs: Run[]): Run[][] {
  const groups: Run[][] = [];
  const assigned = new Array<boolean>(runs.length).fill(false);
  for (let index = 0; index < runs.length; index++) {
    if (assigned[index]) {
      continue;
    }
    const group: Run[] = [];
    const queue = [index];
    assigned[index] = true;
    while (queue.length > 0) {
      const current = queue.pop() as number;
      group.push(runs[current]);
      for (let other = 0; other < runs.length; other++) {
        if (!assigned[other] && intersects(runs[current], runs[other])) {
          assigned[other] = true;
          queue.push(other);
        }
      }
    }
    groups.push(group);
  }
  return groups;
}

export function classifyGroup(group: Run[]): ComboName {
  const longest = Math.max(...group.map((run) => run.length));
  const shortest = Math.min(...group.map((run) => run.length));
  if (group.length === 1) {
    if (longest >= 5) {
      return 'Great';
    }
    return longest === 4 ? 'Good' : 'Clear';
  }
  if (group.length === 2) {
    if (longest >= 5) {
      return 'Yarrr!';
    }
    return shortest >= 4 ? 'Har!' : 'Arrr!';
  }
  return longest >= 5 ? 'Vegas!' : 'Bingo!';
}

// The name shown for a whole step.  Several separate crossings in one clear
// earn their own name, which outranks any one of them alone.
export function classifyStep(step: ClearStep): ComboName {
  const groups = groupRuns(step.runs);
  if (groups.length === 0) {
    return 'Clear';
  }
  const names = groups.map(classifyGroup);
  let best = names[0];
  for (const name of names) {
    if (comboRank(name) > comboRank(best)) {
      best = name;
    }
  }
  const crossings = names.filter((name) => name === 'Arrr!').length;
  if (crossings >= 2 && comboRank('Sea Donkey!') > comboRank(best)) {
    return 'Sea Donkey!';
  }
  return best;
}

// chainIndex is 0 for the clear the player caused directly, 1 for the clear
// its collapse set off, and so on.
export function scoreStep(step: ClearStep, chainIndex: number): number {
  const name = classifyStep(step);
  const base = COMBO_POINTS[name] + POINTS_PER_PIECE * step.cells.length;
  return Math.round(base * (1 + CHAIN_BONUS * chainIndex));
}

// A crab is worth almost nothing when the bilge is nearly dry and a great deal
// when the ship is close to going down.
export function crabPoints(water: Water): number {
  const span = ROWS - BASELINE_ROWS;
  const flooded = Math.min(1, Math.max(0, (water.level - BASELINE_ROWS) / span));
  return Math.round(CRAB_BASE_POINTS + CRAB_FLOOD_POINTS * flooded);
}
