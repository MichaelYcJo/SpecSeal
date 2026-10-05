# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 27756646 |
| Ran by | unknown — the spawn prompt did not name the model, and a segment does not name itself |

## What this phase was asked

The reading and the row. `chain_check.py` gains the constants
`FIX_OF_A_FIX`, `FOF_NO`/`FOF_FIRST`/`FOF_SECOND`, `REFRAME_FROM`, `REFRAME_RE`
and the one reader `fix_of_a_fix_count`. `round_record.py new` derives the row
from the previous record's `Fix range` and `New units` and the report's open
rows at the target, refuses an unresolvable range, writes the row between
`New units` and `Needs a fix`, prints the stop on `second`, and refuses a
record after an unreframed `second`. The template, `docs/round-record-spec.md`,
the protocol's field table, `templates/config.md`'s governs list and
`_literal_strings` carry the field. S1–S7 are cases, each seen red.

## What this phase found

**The AST comparison is its own reading, not a fourth element of
`top_units`.** `plan.md` said `top_units` would keep enough of each node to
compare. Its value is a three-tuple that `measure`, `enclosing_unit`,
`depth_two` and `call_sites` unpack, so `unit_dumps` keys the same names to an
`ast.dump` instead and nothing that reads `top_units` moved.

**The `New units` row is not read; the range's two ends are.** The spec's
reading names both. `close` writes `New units` from exactly the units present
at `b` and absent at `a`, so re-deriving them from the ends gives the same set
WITH the path the row does not carry, and a unit name that two files share
cannot land in the wrong file. A hand-edited row is the one case where the two
differ, and the gate's count reads the `Fix of a fix` row as declared either
way. `questions.md` holds this as a divergence row.

**Q2 is answered: a file only the heuristic reads never lands.**
`fix_pass_units` reads Python files the AST parses at both ends and nothing
else, so a heuristic-read file contributes no unit.

**`new` prints nothing at `first`.** The row names the landing; S2 asks that
nothing about a stop be printed, and a second printed sentence would be one
more for §14 to pin with nothing reading it.

**The record after a `second` reads `no` whatever the stop's range holds.**
The guard is explicit rather than left to the zero-commit range a correct stop
writes: a `second` is the end of its run, and the parametrised S7 case puts a
code commit inside the stop's range to pin that.

**§15, shown red by mutation.** Each unit added was broken once with
`mutation-check` and its cases run: `landings` (three breaks), `fix_pass_units`
(two), `unit_dumps` (two — one swaps `ast.dump` for the name, one includes
line attributes, which turns the re-commented `v` into a landing),
`current_run`, `reframed_after`, the count in `build`, the stop guard, the
closed-row skip, the range refusal, the stop print, `fof_count_of`, and in
`chain_check.py` `fix_of_a_fix_count` (two) and `frame_foot`. All red. Two
breaks survived first: a `says_none` guard the regex below it already covered
(removed, `6b87acb9`), and the no-range return, which had no case where the
previous record commissioned nothing (case added, `27756646`, then red).

**Phase 2 inherits a fixture cost.** `REFRAME_FROM` is below
`1799000000`, the id every hand-written record fixture in the chain-check
modules uses, so the absent-row refusal reaches all of them once phase 2
lands. Records `new` writes carry the row already.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
