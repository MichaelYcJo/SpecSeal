# 1790683267-a-rider-read-ends-where-the-hasher-cuts — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 28e9bdb2 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build the plan's one phase as `spec.md` and `plan.md` say, approach C.
`riders_in` is built from the hasher's blocks. `comment_blocks`' TEXT path
and `gfm_places`' second value are removed. The touched docstrings are made
true. `questions.md` Q1–Q3 are answered from what was run.

- Write S1–S5 first and see each red at `6321dbdc`'s `rider_check.py`,
  after confirming that file is byte-identical to the release head's. See S4
  red against its named mutant. Run S6 and S7 as the spec describes. Kill at
  least one mutant per changed branch.
- Keep the floor: no `zip(` with `strict=`, no `.UTC`, no bare `zip`, and no
  `itertools.pairwise`. Build pairs by index.
- Ledger: K1 and K2 go in this item's fragment. Re-read G13, S2 and S3.
  Correct P5-1 and R1-1 in place with `Corrected 2026-09-29` notes. Re-read
  every drifted row before `--reverify --checked 2026-09-29`.
  `bin/evidence-check --strict .` must end with 0 drifted and 0 refused.
- Write the changelog fragment, this record, `plan.md`'s phase Status and
  `overview.md`. Run `bin/survivor-check --range origin/release/v0.16.0...HEAD`.
- Run narrow checks only: the three rider modules, the interpreter-floor
  module, `tests/test_a_record_states_what_the_tree_has.py`, ruff on the
  changed files and `rider_check.py --root .`. No full suite and no push.

## What this phase found

**The base is the release head, byte for byte.** `.github/scripts/rider_check.py`
is blob `cf2d977a` at `6321dbdc`, `7ffa520c`, `346b4af7` (`release/v0.16.0`)
and this branch's start. So the new cases were seen red simply by running
them before the fix. They were committed red at `a5e482af`.

**Q1: all eight characters reproduce both shapes.** At the base the class
case is red for all 16 parameters of the two #682 shapes, and green for
round 2's three shapes (24) and the differential (8). The verdict case is red
for all 16. The markdown shape reads `(0 ok, 1 drifted, [DRIFTED])` where its
space twin reads `(0, 0, [BROKEN])`. The Python shape carries a DRIFTED second
rider on the `b = 2` line, and its twin does not.

**Q2: the six strings are the default** — `""`, `" "`, `"  "`, `"\t"`,
`" \t"` and `"\t "`, fixed as `AROUND` in the case. They give 6 × 8 × 6 × 2 =
576 texts, which the probe asserted.

**Q3: the comparison is severity and sentence, with the location left out.**
A problem is `(where, severity, sentence)`. `where` is `rel:line`, and the
sentence carries the path and no line number. So the case compares
`(ok, drifted, sorted((severity, sentence)))` and leaves out `where` whole.
That separates drifted from BROKEN by severity. It also separates the extra
Python rider by count.

**Q1's gap in the class case, found by a mutant.** The first class case
asserted where each rider starts and that it lies inside a cut block. A
reader whose riders each ran to the block's end still passed all 323 cases.
That mutant is not equivalent. With two riders on one GFM line, a stampless
first rider would read the second's stamp and never report "no verification
stamp". S3 says a marker piece "starts exactly one rider". So the case now
also asserts that no piece after a rider's first carries the marker
(`04c60acd`), and the mutant turns 8 red.

**Mutants, one per changed branch.** Each was run over the three rider
modules (323 cases) and restored from a copy kept outside the tree:

| Unit, mutant | Red |
|---|---|
| `riders_in`, a rider starts only at a piece that begins its GFM line (S4's named mutant) | 83, the differential 8 and the verdict case 16 among them. The probe: 576 of 576 differential texts read no rider |
| `riders_in`, every piece in a block starts a rider | 92 |
| `riders_in`, each rider runs to the block's end | 8, after `04c60acd`; 0 before it |
| `riders_in`, the block's last GFM line left out | 92 |
| `riders_in`, the reader's own blocks over `str.splitlines` pieces | 97 |
| `gfm_places`, every piece a line of its own | 84 |
| `comment_blocks`, `quoted_lines` replaced by an empty set | 14 |
| `inferred_anchor`, the rider on its own numbers | 3 |

**S6 and S7, probed with the base reader loaded beside the new one.** The
probe was a `test_tmp_` file in the scratchpad, and it has been deleted.

- The 576-text differential reads 0 riders off the cut at either version, and
  0 texts differ between the two. The new reader reads exactly one rider, on
  GFM line 2, in all 576.
- Texts holding none of the eight give identical `(start, end, body)`
  riders at both, with 0 off the cut. That covers the 25 tree files that
  carry the marker, 84 texts from the 28 marker-carrying string constants in
  the three rider test modules (each read as `.py`, `.yml` and `.md`), and
  60,000 generated texts. The generated texts come from 20,000 seeded draws,
  each read as the three types. They mix both comment kinds, back-to-back
  riders, fences, headings, closed and open HTML comments, and the marker in
  prose, table cells and strings, with LF, CRLF and lone-CR ends. The new
  reader read 86,508 riders in them.
- `rider_check.py --root .` at the base (run from a scratch mirror whose
  `skills/` and `hooks/` link to this tree) and after printed the same line,
  `18 ok · 0 drifted · 0 broken`, and both exited 0. The 18 riders of the
  tree are identical in process.

The frame's M7 said `19 ok` at `c7fef45f`. The tree has 18 riders now at
either version, so the count moved with the tree and not with the reader.

**The module comment above `_blocks` was already false at the base.** It said
the walk loads "at the first markdown file that carries the marker". G's
phase 6 made a Python file load it too, and the load is now in `riders_in`.
It now says "any type". The comment sits outside every anchored unit, so no
row moved.

**`region_lines`' own comment is left as it stands.** It says "No TEXT:" and
explains why a text would put the blocks one line off. `comment_blocks` can
no longer be handed one, but the sentence is still true of `quoted_lines`,
which it names through `walk_text`. The spec keeps `region_lines` unedited,
and editing the comment would move S2's anchor for a sentence that holds.

**The floor.** `rider_check.py` carries no `zip(`, no `pairwise` and no `.UTC`.
The only `zip` is `write_block`'s comment, "a strict zip", which the floor
pattern does not match. `test_no_shipped_script_needs_more_than_the_floor_without_saying_so`
passes, and ruff is clean. The pairs are built as
`ends = [*starts[1:], inside[-1] + 1]` and indexed over `range(len(starts))`.
There is no length check, because `ends` is built from `starts`.

**Survivors.** `survivor-check` over `origin/release/v0.16.0...HEAD` reported
two places sharing wording with the removed step-over paragraph. One is an
existing case's docstring and the other is P5-1's dated round-2 note. Both
still say something true, and both are recorded in `survivors.md` with a
quote and grounds.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `comment_blocks`' `text` parameter, its step-over (`places`, round 2's `cut` set) and the two docstring paragraphs about TEXT | `riders_in`, which takes `comment_blocks` over GFM lines and splits the blocks. `comment_blocks`' docstring now says its lines are GFM lines and that it is the one block rule. K1 holds the claim |
| `gfm_places`' second value (whether only whitespace stands before a piece) and its *Whitespace, not nothing* paragraph | the hasher's `lstrip` on the GFM line, which `riders_in` inherits by taking the hasher's blocks. `test_a_rider_behind_a_leading_break_is_still_read` still pins it: all 16 of its parameters turn red under S4's named mutant |
