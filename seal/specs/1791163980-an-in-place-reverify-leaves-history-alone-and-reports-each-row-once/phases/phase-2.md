# 1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 9c7e0bf7 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#792 (D2, D3). First S8, S9, S10 and S12, each seen red, and S11's assertion
tightened. Then D2's collected `left` lines, printed once from the fold MOVES
uses, after the walks and outside `told`; the new keyword list `main` reads;
and D3's remedy clause chosen per coordinate by reason (i) or (ii), not by
whether `--ledger` was passed. The *Without the row* paragraph gains the
unnarrowed half. `reverify`'s docstring loses *a walk after the first names
nothing the first one named* and says every `left` line goes through the
fold. Pins follow, each seen red. Questions Q3 measured in a scratch tree.

## What this phase found

**Spec Class 2's wording of the fold disagrees with S9 and with the MOVES
rule, and the code follows S9.** Class 2 says a `left` line is printed
*iff the last walk that was not `unchanged` left it*. Under that rule, left
then unchanged prints a `left` line, which is exactly what S9 forbids, and
`walked_move` says *a walk reading the coordinate unchanged clears a BROKEN
an earlier walk left* (#791). The rule built, and enumerated over the 36
sequences, is: a `left` line exactly where the last walk left the
coordinate, with that walk's reason, which is where `owed_moves` hands MOVES
a BROKEN part. The S8 case asserts both, so the two cannot drift apart.

**The unit is `walked_outcome`, and it is small on purpose.** Its pair is
`walked_move`'s state and the walk's own line. A walk that does not leave the
coordinate passes no line, so a later walk that reads it unchanged or moves
it takes the line back without a test of its own. A first draft tested
`state[2]` before keeping the line; `bin/mutation-check` showed that test
equivalent, because a walk that leaves always ends BROKEN, and it was
removed.

**Every walk's move is folded in one place**, from the walk's `pending`
list after its rows are settled, rather than at the two sites that make a
move (a plain re-stamp and a rename). One site is what one case,
`test_a_left_line_a_later_walk_takes_back_is_not_printed[moved]`, can pin.
A move whose row is left whole, or a held move whose row is not dated,
still takes the line back: the coordinate resolved on that walk, and what
the run says about the row is the `undatable` line, or nothing.

**Reason (i) is decided by the newest readings, not by every reading.** D3
says *a member reading of the coordinate that does not hold sits in a file
this run did not write*. Counting every member, an older reading outside the
narrowing gives the `--ledger` clause, and a run without `--ledger` would
re-stamp that older reading and clear nothing, because the family paragraph
counts only the newest. So both reasons are read off the newest-dated
readings (`why_still_drifted`). Held by
`test_an_older_reading_outside_the_narrowing_names_no_ledger_remedy`, red
with every reading counted.

**Reason (ii) covers a row left whole as well as a coordinate left.** A
released row outside every family, in a table with no date column, is left
whole by `--checked`, stays DRIFTED, and is named with the run's own
leaving. Held by
`test_a_row_left_whole_for_want_of_a_date_cell_is_named_as_left_by_the_run`.

**Q3, measured: a family with neither reason exists, and it is a ledger the
run cannot read strictly.** The two shapes the frame named do not reach it.
A probe (one `test_tmp_` file, run once and deleted) built R1 and one
fragment re-read with `Checked` cells of `2026-13-45` / `2026-14-01`,
`2026-13-45` / `2026-02-01` and `2026-01-01` / `2026-13-45`, each with and
without `--checked`, each over every ledger and narrowed to R1's file: 12
runs, and none printed a family line with neither reason. A member reached
only through a citation cannot be outside the run's view, because the view
always adds every ledger the repository carries and a citation names only a
released file. The shape that does reach it is a fragment holding the
newest reading with a byte that is not UTF-8: the run cannot write it, the
lenient view still reads it, and no `--ledger` would help. The line then
names the coordinate and no remedy, beside the `ledger unreadable` line.
Held by `test_a_family_no_remedy_clears_is_named_without_one`.

**The (ii) clause's words, Q1.** *this run left X where it stands, and the
line naming it above says why*. The `left` lines and the `undatable` line
print inside `reverify`, before `main` prints the family lines, so *above*
is true for both.

**Seen red.** At the phase-1 head and at a3aa139a (the paths are the same
there): the 36 S8 sequences, S9, S10 both trees, S12, the no-remedy case
and the six document pins. S11's tightened assertion is green at the base,
as the frame says it should be. Through `bin/mutation-check`, each went red:
`walked_outcome` keeping the first walk's reason (S8), `still` not folding
(S9), the move fold removed (S9, moved), the left-whole collection (the
undatable case), the collection of left coordinates and the hand-over to
LEFT_BY_RUN (S10), each of the three reason branches, the newest-reading
restriction, and the printing of the folded lines.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `say = quiet if repeat else print` and `quiet`, the first-walk-only printing | `walked_outcome` and the print loop at the end of `reverify` |
| `reverify`'s docstring sentence *a walk after the first names nothing the first one named* | The docstring's fold paragraph, which says every `left` line goes through `walked_outcome` |
| The family `LEFT` line's fixed `run it without --ledger` ending in `main` | `still_drifted_line`, one clause per reason |
