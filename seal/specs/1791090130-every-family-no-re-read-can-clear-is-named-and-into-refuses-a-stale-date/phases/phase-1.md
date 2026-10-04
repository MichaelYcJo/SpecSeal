# 1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 4c148310 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

⬜ 12 of #743's round 2: S1–S3 and S6. A refusal in `reverify_into`, per row,
in step 1 (the plan), so a refused row reaches neither `rows` nor `moves`; a
`LEFT` line at exit 1; the newest-date rule shared with `family_view`; the
`--into` sentence in `docs/the-evidence-ledger.md` and one usage clause;
cases A1–A7, each new one seen red, and the ones pinning present behaviour
red by mutation. The fragment rows for S1, and the released rows the phase
drifts read again into this item's fragment. Q2, Q3 and Q4 are this phase's.

## What this phase found

**The frame holds.** `reverify_into`, `family_view`, `released_drift` and
`main` read at `edee5ca2` as `plan.md` §*Technical context* describes them.
Nothing in the frame's coordinates was wrong.

**The shared rule is a function plus one returned field.** `family_view`'s
nested `checked` became the module-level `reading_date(header, cells)`, and
`family_view` returns `newest = {root: {coordinate: (date, row)}}` beside
`held`. `later_reading` is the one reader: for a family root it takes
`newest`, and for a released row outside every family it calls
`reading_date` on that row's cell. `released_drift` needed no change: its
`wanted` loop yields the row, and the row's own cell is its one reading.

**The plan's choice holds against the code.** A refused row's coordinate
loop never runs, so no `current_hash` is taken and no move is appended. That
includes a coordinate with no one place to hash: in a refused row it is not
recorded `BROKEN` this run either, and a run with a date that reaches the
newest reading records it.

**Q2, measured:** `--strict` over a released row whose `Checked` cell is
`2099-01-01` and whose hash holds exits 0. No check refuses a date after
today, so A7 stands as written.

**Q3, the wording:** `<label> — `--checked D` is older than the newest
reading of <coordinate>, N at <file>:<line>, so a `Re-read ·` row dated D
would not outrank it and the row would stay DRIFTED; nothing was written or
recorded for this row — read the code again and run it with the date of that
reading`. Where N is after today the tail reads `, which is after today (T),
and `--checked` takes no date after today, so no `Re-read ·` row can outrank
it; nothing was written or recorded for this row — a `Corrected ·` row in
your own fragment supersedes the row and every reading of it`. Where several
coordinates are outranked, the latest reading is the one named: it is the
date a new reading must reach. A case pins that choice.

**Q4, measured:** one stale cell (three readings, the freeze, `--into`,
`--strict`) took 0.55 s. The sibling was chosen, as the default said: 48
cells over placement × carrier × narrowing {M's file, N's file, none} × date
{between, on N}. 16 of them were red at `edee5ca2`, all at the between
date.

**The pact-change cases were writing this phase's stale row.** Their `row()`
helper dated every row 2026-10-01 while every run passed `--checked`
2026-09-04 to 2026-09-06. So each released row they re-read was outranked by
its own reading, and S8 and four other cases pinned an exit 0 that `--strict`
would have read DRIFTED. The helper now dates rows 2026-09-01, before every
run. No assertion about the record changed.

**S7 did not hold for two released rows, and they were corrected instead.**
L4 (`seal/releases/0.18.0.md`) claims `--into` writes *one `Re-read ·` row
per released row a re-read owes*, and N1 claims *under the freeze `--into`
writes the re-read citing the root*. A stale `--checked` now writes neither.
A `Re-read ·` row says *the cited row's claim holds*, which would have been
a false row. Each therefore takes a `Corrected ·` row carrying its claim with
the narrowing and every coordinate it rested on. That supersedes
`1791076833`'s `Re-read · L4` and `Re-read · N1`, which are left as their
author wrote them. The other released rows the edit drifted (L1, L9, the
`check_text` correction, the freeze correction, N2) were read against the
change, still hold, and took `Re-read ·` rows. `1791076833`'s C1 and W8 cite
`reverify_into` and still hold, so their hash was re-stamped in place, by an
asserted script edit. `--reverify` narrowed to that fragment would have
re-stamped the chore's rows in the same file.

**The chore's rows were kept out by hand.** `--into` narrowed to
`seal/releases/0.18.0.md` wrote a `Re-read ·` row for C4 and for S8, whose
coordinates (`VERSIONS_OF_ANOTHER_PRODUCT`, `templates/config.md`) are two
of the chore's ten. Both rows were deleted from this fragment before the
commit. `--strict .` at `4c148310` reads exactly those ten DRIFTED and
nothing else.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `family_view`'s nested `checked` body | `evidence_check.py#reading_date`, which `checked` now calls |
| the pact-change fixture date `2026-10-01` in `row()` | `row(…, checked="2026-09-01")`, with the reason in its docstring |
