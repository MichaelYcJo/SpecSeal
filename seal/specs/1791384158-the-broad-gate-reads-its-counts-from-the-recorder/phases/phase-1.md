# 1791384158-the-broad-gate-reads-its-counts-from-the-recorder — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 67cf7fb5 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 1: first Q-M1 on pytest 6.1, 7.0 and 9.1 (and 9.1 with
pytest-xdist 3.8 under `-n 2`), in throwaway environments outside the
worktree's `.venv`. Then the recorder writes `category` on every `test`
line, a `collect` line for a skipped collection, and `stopped` on the `end`
line from the keyboard-interrupt hook and `session.shouldfail` /
`session.shouldstop`, with its docstring's *What it writes* rewritten; the
gate's `RunRecord` gains `unread` and `counts`, `read_record` counts `unread`
per keyed file after the key check and reads `unended` by `spec.md` Scope 2's
rule, and `suite_counts(record)` stands beside the text form phase 3 removes.
Cases S4, S5 (recorder half), S6 (`read_record` half), S7–S10 (recorder and
`read_record` halves), and the `"kind": "end"` fixtures gain `stopped: []`.
Each new case red at 5623d728, and each new arm red under `bin/mutation-check`.

## What this phase found

**The frame holds.** Q-M1 answered yes on every build for every hook and
flag the design reads, so no `getattr` fallback and no floor sentence were
needed. Measured with a probe plugin and then with the recorder itself, each
through `uv run --no-project --python <v> --with pytest==<v>` in uv's own
cache (pytest 6.1.0 and 7.0.0 on Python 3.9, 9.1.1 on 3.12, xdist 3.8.0 on
9.1.1), scripts under the session's scratch directory and deleted after:

| Stop | 6.1.0 | 7.0.0 | 9.1.1 | 9.1.1, xdist `-n 2` |
|---|---|---|---|---|
| `pytest.exit(returncode=0)` in a test | exit 0, `exit` | exit 0, `exit` | exit 0, `exit` | exit 3, nothing |
| `pytest.exit(returncode=1)` | exit 1, `exit` | exit 1, `exit` | exit 1, `exit` | exit 3, nothing |
| `pytest.exit(returncode=5)` | exit 5, `exit` | exit 5, `exit` | exit 5, `exit` | exit 3, nothing |
| `pytest.exit()` | exit 2, `exit` | exit 2, `exit` | exit 2, `exit` | exit 2, `interrupt` (the worker's) |
| `KeyboardInterrupt` in a test | exit 2, `interrupt` | exit 2, `interrupt` | exit 2, `interrupt` | exit 2, `interrupt` (the worker's) |
| `-x`, a failing test | exit 1, `failures` | exit 1, `failures` | exit 1, `failures` | exit 2, `interrupt` + `failures` |
| `--maxfail=2` | exit 1, `failures` | exit 1, `failures` | exit 1, `failures` | exit 2, `interrupt` + `failures` |
| `-x`, broken file collected first | exit 1, `failures` | exit 1, `failures` | exit 1, `failures` | exit 2, `interrupt` + `failures` |
| `-x`, broken file collected last | exit 2, `interrupt` + `failures` | same | same | same |
| failed collection, no `-x` | exit 2, `interrupt` | exit 2, `interrupt` | exit 2, `interrupt` | exit 1, nothing: xdist runs the rest |
| `--stepwise`, a failing test | exit 2, `interrupt` + `stop` | same | same | same |

A cell's word is what the `end` line's `stopped` carried. Every row that
exits 0, 1 or 5 without xdist carries a stop, which is #852's two limits
closed. The xdist column is the measurement R3 asked for: a `pytest.exit()`
in a worker reaches the controller as an internal error, exit 3, with no
hook called, which `RAN_TO_ITS_END` still refuses; and `-x` under xdist is
observed as well as refused, because the controller's own `Session` counts
the reports xdist forwards and sets `shouldfail` — R3's *the stop flag is
`DSession.shouldstop`* holds for the exit and not for the flag.

The categories, over one module carrying a pass, a fail, a failed setup, an
xfail, an xpass, a strict xpass and a skip, beside a module that skips
itself and one that cannot import, run with
`--continue-on-collection-errors`: on all four builds the teststatus hook's
answers, counted with a failed collection as `error` and a skipped one as
`skipped`, equal the terminal reporter's own `stats` and its printed line,
`2 failed, 1 passed, 2 skipped, 1 xfailed, 1 xpassed, 2 errors`. The strict
xpass is `failed`, which is why alternative A2 would have drifted.

Q-M2, narrowed (see the hand-back): the recorder's variables set by hand
over `bin/test -q` on four modules under xdist printed `218 passed, 1 skipped`
and `suite_counts(record)` gave `218 passed, 1 skipped`, one session, no
unread line. S5's case makes the same comparison on every run, plain and
under `-n 2`, over the category tree above. The whole suite was not run:
that is the broad gate's, and the sealer's panel row is the comparison over
it.

Two judgments the frame left open, settled here:

- **A collection is counted once per session, a test line once per line.**
  `read_record` already reads a file's lines as a set because xdist can hand
  the controller one failed collect report per worker; counting a
  collection twice would print `2 errors` for one broken module. A test
  report is counted per line because pytest counts each report, `rerun`
  included.
- **`suite_counts` is None where no report was counted**, beside the two
  conditions `spec.md` names: a session that ran nothing has no count to
  print, and the panel then reads `exit <n>`, as it does today for pytest's
  `no tests ran`.

The text reader `suite_counts(text)` is renamed `summary_counts` for this
phase, so both can stand until phase 3 removes it; its two cases, the
pin in `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` and the registry
row moved with the name.

A `stopped` the recorder did not write — absent, or not a list — reads as
unended, so every hand-made `end` fixture in the gate's cases gained
`"stopped": []`. A record written by 0.20.0's recorder would read as unended
on every session, which no reader meets: the recorder and the gate ship
together.

Shown red: the 30 new and re-aimed cases were run against 5623d728's
recorder and gate (both files checked out over the committed ones, then
restored from the commit): 30 failed and the 8 that passed are the eight
parameters the unended case had before (exits 0–7 with nothing stopped),
which hold on both. Mutation: 9 mutants of the recorder's arms and 15 of
the gate's were each red through `bin/mutation-check`. Three survived on
first pass and were answered in 67cf7fb5: `Exit`'s `msg` and `returncode`
fallbacks and the flag's `str()` guard were unreachable on every build and
went; `category_of`'s two guards gained a unit case; the interrupt's
sentence gained an assertion.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `RunRecord.skipped`, counted over every file in the directory and read by nothing | `RunRecord.unread`, counted per keyed file; read by phases 2 and 3 |
| the name `suite_counts` for the text reader | `summary_counts`, until phase 3 retires it |
