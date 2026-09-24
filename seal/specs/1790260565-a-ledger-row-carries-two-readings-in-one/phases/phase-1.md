# 1790260565-a-ledger-row-carries-two-readings-in-one — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 4744aa93 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#568: S4 (`seal/releases/0.9.2.md`) and G5 (`seal/releases/0.8.2.md`) each
hold one reading. The notes were to be a union by the halves rule in
`docs/the-evidence-ledger.md`: the shared opening once, every marker of both
halves in date order, one Checked date, then a dated `Re-read` note by this
work item. A claim the re-read found false was to be corrected in place with a
`Corrected 2026-09-24` note instead, with S4's claim cell and the tagged half
named as the case to judge (`questions.md` Q3). The eleven-modules row
(`seal/releases/0.9.3.md`) was to have its two escaped separators turned into
sentence boundaries, its wording otherwise unchanged. Each file was to be
re-stamped with `evidence-check --ledger <that file> --reverify .`, with no
other row re-stamped.

## What this phase found

- **Q2 is answered: nothing was drifted.** The lenient run over each of the
  three files, before the edit, reported 120, 40 and 47 rows `ok` and none
  drifted. The notes are not part of any anchored unit, so the edit moved no
  hash. `--reverify` over each file reported `0 rows re-verified`, and the
  diff is the three edited lines and nothing else.
- **Q3 is answered: S4's claim was false, and it is corrected.** The claim
  cell said the check refuses *at or above the running one* and keeps
  *below it*. Since #363 the check and `docs/issues-and-milestones.md` both
  say *at or above the running one and not yet tagged*, with a tagged version
  kept as history. The #363 note on the row described that change to the
  document and left the claim as it was. The claim now carries the tagged
  half, and the row's new note is `Corrected 2026-09-24 by work item
  1790260565 (#568)`. The count of two documents still holds:
  `docs/issues-and-milestones.md` and `docs/release-checklist.md` are the
  only files under `docs/`, `skills/`, `agents/`, `CONTRIBUTING.md` and
  `README.md` that contain "at or above the running".
- **G5 holds.** The title format is still in the tracker document,
  `skills/verify/SKILL.md` contains `chore: flow measurement` zero times, and
  the four cases the row cites still stand under their names.
- **The eleven-modules row's first join needed a period.** The first
  escaped separator followed "moved" with no full stop, so the join is ". ".
  The second followed "neither moved." and is a space.
- **Checked dates.** S4 and G5 now read 2026-09-24. They read 2026-09-22
  before, and so did both of their escaped second dates. The eleven-modules
  row already read 2026-09-24 and keeps it.
- **No marker was lost.** A `test_tmp_*` probe compared each changed line's
  marker multiset before and after, using `correction_check.markers`. G5
  gained one `(Re-read, 2026-09-24)`, S4 one `(Corrected, 2026-09-24)` and
  the eleven-modules row one `(Re-read, 2026-09-24)`, and each lost nothing.
  The probe is deleted.
- **The instrument returns one row, and it is not this class.** The
  instrument looks for a `\|` outside a code span in every table row of
  `seal/ledger.md` and `seal/releases/*.md`. With code spans paired by
  CommonMark's run-length rule, it found four rows before the edit and one
  after. The one left is `seal/releases/0.11.5.md`'s row on `seal`'s
  last-record refusal. It quotes `assert 'the only value \|`seal\|` accepts'`
  inside a single-backtick span, so the span closes at the inner backtick. The
  row carries one reading, which is not #568's shape, and it is left as it
  is. A first, cruder version of the instrument also named
  `seal/releases/0.11.4.md`'s fix-table row. That pipe is inside a code span,
  so it is a false report.
- **The work item needed its overview before any narrow run could be green.**
  `tests/test_unverified_rows_close.py::test_this_repositorys_own_overviews_are_all_readable`
  was red in this phase's first narrow run, before the overview existed:
  this directory is the only one under `seal/specs/`, and the checker said
  "no overview.md found … nothing was checked". So it is red at `0f5f537b`
  as well, by reading rather than by a run there. The overview was opened in
  this phase.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| G5's and S4's second copy of their Notes opening, and their second Checked date | none: the opening stands once in the same cell, and the date is superseded by this re-read's date |
