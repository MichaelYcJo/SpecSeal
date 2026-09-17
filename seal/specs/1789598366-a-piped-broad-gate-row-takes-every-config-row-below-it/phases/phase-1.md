# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | ed090be1 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

Teach `hooks/config.py#CONFIG_ROW`'s two cells markdown's escape and reduce
`\|` to one literal pipe in what `config_rows` returns, so that a `Broad gate`
row holding a pipe is a row and the rows written below it still arrive.
`skills/implement/scripts/seal.py#table_span` inherits it through the alias,
and the case that matters is the one pinning reader and writer still agreeing
about which line is the `Mode` row. Take the three measurements `questions.md`
M1–M3 ask for and record them with their populations.

Two things were added to the phase by the spawn prompt rather than by
`plan.md`. Q1's answer carries a constraint the owner attached and measured —
**the reduction is exactly the two characters `\|`, never a general backslash
unescape** — so a case pins that a value carrying Windows path separators
reads back unchanged, beside the case that pins the pipe.

## What this phase found

**M1 is true, and it is executed rather than read.** `plan.md` and
`questions.md` both carried it as *read, not executed*. Measured 2026-09-17
over `seal.py#write_row`, which is the unit `seal mode` calls when the row
reads as undeclared: a config whose `Mode` row sits below a piped
`Broad gate` row comes back **two `Mode` rows deep**.

```
| Record language | English |
| Mode | shared |              ← written by the command, above the piped line
| Broad gate | bin/test -q | tee out.txt |
| Mode | shared |              ← the person's own row, below it
```

`declared_mode` answered `('none', '')` for a file whose own row says
`shared`, `table_span` returned `(-1, 5)`, and `with_row` inserted at the end
it could see. That is the outcome `table_span`'s own comment says no command
can bring back into agreement, and it is the strongest argument for this
phase. The case that pins it is
`test_seal_mode_writes_one_row_where_the_mode_row_sits_below_a_piped_row` in
`tests/test_the_mode_question_is_asked_once.py`, red against the reverted
cell with the two-rows-deep file printed in the failure.

**The defect needs a parseable row ABOVE the piped one, and no document said
so.** `config_rows` breaks on an unparseable line only once it has found a
row; with nothing found yet it steps past the line as furniture and keeps
reading. Measured both ways round on 2026-09-17:

| Table | Before this phase |
|---|---|
| `Record language`, then the piped `Broad gate`, then `Mode` | `[('Record language', 'English')]` — `Mode` is gone |
| the piped `Broad gate` FIRST, then `Mode` | `[('Mode', 'shared')]` — `Mode` survives |

So *it takes every row below it* is true only where a row above it already
parsed. `spec.md` A1 happens to be right — its piped row is the table's
second — and A3 is the one that does not say it, which is why every fixture
in this phase's new section states the rule in a comment above it rather than
leaving it to be rediscovered. #415's own measurement is the first shape: its
four-row table had `Mode` first.

**M3: nothing moved.** Population: 1,449 tracked files read in full, ten of
which hold a readable `| Item | Value |` table. Every row of all ten is
byte-identical before and after the change (`diff` over the two dumps, exit
0). A6's *nothing else moved* half holds, and there is no divergence row to
write.

**M2 stands as the frame restated it, not as #415 wrote it.** No production
path reads `Record language` or `Commit and pull request language` through
`config_rows`; the only code reader is the test-local copy phase 3 closes.
What a piped row actually takes today is `Mode` and `Broad gate`. The two
language rows are a hazard for a future code reader, and the records this
work item writes say that rather than repeating the ticket's sentence.

**The Windows constraint is a live behaviour, not a hypothetical.** Measured
against the reader as it stood, a `Broad gate` row holding
`C:\Python\python.exe -m pytest` already comes back with its separators
intact. The case pinning it
goes red under a general `re.sub(r"\\(.)", r"\1", value)`, which returns
`C:UsersxPythonpython.exe -m pytest` — a path to nothing.

**A third case was added that no scenario asks for.** Widening what a cell
may hold must not widen what a ROW is, so
`test_a_three_column_row_still_ends_the_table` pins that `| x | y | z |`
still ends the table. It is red under a greedy last cell, which is the alternative `plan.md` rejects — and
nothing else in the suite would have caught that rejection being undone.

**For phase 4, found while reading the frame:** `plan.md`'s phase 4
verification command names `tests/test_the_seal_is_taken_once_by_the_sealer.py`
and `tests/test_the_settings_have_a_front_door.py`, and the case that pins
the template's pipe sentence is in neither — it is
`test_the_allowed_list_says_a_pipe_cannot_reach_the_row_at_all` <!-- NAME NOT IN TREE: work item 1789598366 (#415) renamed it — `test_the_allowed_list_says_how_a_pipe_is_written`. -->, in
`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`. And
`test_a_candidate_carrying_a_pipe_is_refused_where_candidates_are_derived` <!-- NAME NOT IN TREE: work item 1789598366 (#415) renamed it — `test_a_candidate_carrying_a_pipe_is_escaped_where_candidates_are_derived`. -->,
in `tests/test_first_setup_asks_once.py`, pins the same claim in
`skills/implement/orchestration.md`. Phase 4 runs both in addition.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the cell pattern widened and nothing came out of the tree | none |
