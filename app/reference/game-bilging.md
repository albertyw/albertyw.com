Bilging

game-bilging

1787988519

Bilging is one of the duty puzzles from [Yohoho! Puzzle Pirates](https://yppedia.puzzlepirates.com/Bilging),
the 2003 MMO built entirely out of puzzle minigames.  Aboard a ship, bilging is
the job of working the pump: water collects in the hold, and somebody has to
clear it before the vessel goes down.

At a glance it looks like every other match-3 game, and it is not.  Two rules
make it its own thing:

- **Swaps are horizontal only.**  The cursor is a two-cell target, and clicking
  exchanges those two pieces left-for-right.  There is no vertical swap, so a
  column has to be built by walking pieces sideways into place.
- **A swap does not have to make a match.**  You are free to shuffle pieces
  around the board, which turns the puzzle from "spot the match" into
  "assemble the shape you want".

The water is the clock.  It rises on its own, and the only thing that pushes it
back down is clearing pieces.

```
   swap ──▶ runs of 3+ clear ──▶ survivors fall ──▶ refill from the top
                   │                                        │
                   │ pieces cleared                         │ may form new runs
                   ▼                                        ▼
             water pumped down                       chain reaction
                   ▲                                        │
                   └────────────────────────────────────────┘

   ░░░░░░  ← water rises on a timer
   ██████  ← clear below the line to pump it back down
```

Scoring is not about how many pieces you removed.  It is about the *shape* of
the clear — specifically how many runs crossed each other in one go.  A row of
three and a column of three sharing a cell beats the same six pieces cleared
separately, and the game gives each shape a name:

| Combo | What triggers it |
| --- | --- |
| Good | 4 in a line |
| Great | 5 in a line |
| Arrr! | crossing runs spanning 3x3 or 3x4 |
| Har! | 4x4 |
| Yarrr! | anything crossing a run of 5 |
| Bingo! | three runs crossing at once |
| Sea Donkey! | several separate crossings in one clear |
| Vegas! | three crossing runs including a 5 |

Three special pieces turn up:

- **Crab** — immovable; it cannot be swapped.  It scuttles off when it ends up
  above the water line, which in practice means you free it by pumping the
  water down past it.  A crab freed from a nearly-dry bilge is worth very
  little; one freed while the ship is close to swamped is worth a great deal.
- **Puffer fish** — click it and it expands, clearing itself and the eight
  pieces around it.
- **Jellyfish** — swap a coloured piece into it and every piece of that colour
  leaves the board at once.

<div id="bilging"></div>

## What is not faithful

The rules above are all documented.  A few things are not, and rather than
guess quietly, here is what I picked myself:

- **Board size.**  6 columns by 12 rows.  Widely repeated, never confirmed.
- **The pieces.**  The original uses illustrated sea junk.  These are plain
  coloured tiles.
- **Point values and rates.**  The combo ladder's *ordering* is documented; the
  numbers behind it are not, so the scores, the rate the water rises at, and
  how much a clear pumps out are all tuned by feel.
- **Special piece spawn rates.**  Undocumented, so invented.

Two things are deliberately left out, because they only mean anything inside
the game they came from: rank gating, which in the original withholds puffer
fish until 3-star and jellyfish until 6-star, and the ship, whose accumulated
damage is what really decides how fast the water climbs.
