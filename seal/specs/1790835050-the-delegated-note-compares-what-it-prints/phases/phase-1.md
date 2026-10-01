# 1790835050-the-delegated-note-compares-what-it-prints — phase 1

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | a0c98f29 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 1: the fix and its case. `report_spawns` compares
`round(delegated_max / 60, 1) < 1.0` in place of `delegated_max < 60`, with a
comment naming the cause and #701. `tests/test_session_cost.py` gains one case
beside `test_a_delegated_column_of_seconds_says_which_of_two_things_it_is`: a
59.6 s spawn prints `1.0m` and no *never reaches a minute* (red at the base),
and a 57.0 s spawn prints `0.9m` and *57s at most* (shown red with the
comparison mutated to `< 0.9`, then restored). This record carries both reds
and the `--json` reading of the S1 fixture. The spawn prompt added: say first
whether the frame holds, mutate what is added with `bin/mutation-check`, run
narrow tests only.

## What this phase found

**The frame holds.** Every coordinate `spec.md` and `plan.md` name was opened
at `e83db346` before the first edit: `delegated_max < 60` at
`session_cost.py:2219`, `minutes` at `:1970`, the two #640 comparisons at
`:2109` and `:2519`, the existing cases at `tests/test_session_cost.py:2609`
and `:2638`, the round-3 report's paste-ready fix (🟡 10), and the issue's two
boxes. The seven ledger rows anchored at `report_spawns`, hash `15595f59`, are where
the spec says (`seal/releases/0.9.5.md` lines 11, 13, 14, 16, 45, 46;
`seal/releases/0.11.3.md` line 50), counted by `grep -n "report_spawns@"` over
`seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md`. Nothing in
`seal/follow-up.md` names this module's note.

**The class sweep, re-read rather than trusted.** Every `<`, `>`, `<=`, `>=`
site in `session_cost.py` at `e83db346` was listed by grep and judged. The
spec's table holds: `:2219` is the one defect; `:2109`, `:2141` and `:2519`
already compare the printed figure (#640); `:2115` is the same shape and
left on the spec's grounds; the rest are existence, sign, integer, length or
unprinted comparisons. The grep found a handful of sites the table does not
list by line, and each is a length or count with no rounded print beside it:
`:412` and `:592` (token parsing), `:1157` and `:1425-1426` (list lengths and
a positive filter), `:2396` (a path's length against a width), `:2893` and
`:3201` (counts). None changes the verdict.

**The rounding edge, measured on two interpreters.** `round(x / 60, 1)` and
`f"{x / 60:.1f}"` agreed at 56.9, 56.99, 57.0, 57.001, 57.01, 57.02, 59.5,
59.6, 59.99 and 60.0 on CPython 3.14.4 (one arithmetic line, nothing left
behind), and the case asserts the `0.9m` cell beside the note at 57.0 s on
CPython 3.13.9, the interpreter `bin/test`'s virtualenv runs. 57.001 already
gives `1.0`, so the band in which the note's presence moves is (57.0, 60)
seconds, as framed. That answers `questions.md` Q1 on these two interpreters;
the CI matrix is the pull request's run (`overview.md` §*Not verified*).

**How the case reads the column.** The case asserts the `delegated` cell
itself, read by the header's right edge (`delegated_cells`), rather than
searching the page for `1.0m` — the `span` column prints `1.0m` on the same
row of the 59.6 s fixture, so a page-wide search would pass for the wrong
reason. The helper skips a `no call in this window` row (the empty head
row's text reaches into the column's slice) and stops at the blank line
after the table.

**Seen red (contract §15).**

- The 59.6 s half, against the unfixed module, with the case written first:
  exit 1 at `assert "never reaches a minute" not in out` — the cell read
  `1.0m` and the note printed *60s at most* under it.
- The 57.0 s half, with the fix's comparison mutated to `< 0.9` by
  `bin/mutation-check`: red at `assert "… — 57s at most" in out`, the cell
  assertion `["0.9m"]` passing above it.

**Mutations, each through `bin/mutation-check` (restore and hash compare its
own), seven, all red:** the comparison to `< 0.9`, back to `delegated_max <
60`, to two places `round(…, 2)`, and to `<= 1.0`; in the helper, the `—`
filter removed, the `no call in this window` skip removed, and the stop at
the blank line turned into `continue`. Every run was the module's delegated
cases (`-k delegated`, four cases) and every one failed the new case alone.

**`--json` on the S1 fixture.** Executed inside the case: the spawn row's
`delegated_s` is `59.6`. Read: `main` calls `report_spawns` only under
`args.spawns and not args.json` and prints `data` before it, so no key
describes the note and nothing in the fix reaches `--json`.

**Verified, executed:** `bin/test tests/test_session_cost.py
tests/test_a_derived_number_reaching_an_int_carries_a_guard.py
tests/test_the_handoff_before_round_one.py -q` at the fix, 210 passed, exit 0
read directly; `uvx ruff check` and `uvx ruff format --check` over the two
touched files, exit 0. The full suite and the repository-wide lint are the
sealer's and were not run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the raw comparison `delegated_max < 60` | replaced in place by `round(delegated_max / 60, 1) < 1.0`; the claim moves to `seal/ledger/1790835050-the-delegated-note-compares-what-it-prints.md` in phase 2 |
