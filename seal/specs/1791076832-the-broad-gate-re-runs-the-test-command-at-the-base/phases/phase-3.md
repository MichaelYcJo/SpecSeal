# 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | b8c3e032 |
| Ran by | unknown — the spawn prompt did not hand the value over, and the segment does not source it from its own idea of what it is |

## What this phase was asked

#747, the comparison: `compare_at_base` tries prefixes, keeps
`suite-at-base-<k>.txt`, reads `FAILED`/`ERROR` and the two banners at the
base, and gives `new?` with a reason where nothing measured; `first_command`
removed; end-to-end cases A1, A2, A4, A5, A6, each seen red against
`e141980a` where the spec says so; the S2 cases' `new\b` assertions tightened
where touched (A2, A3, A8). Q1 is built on its default, yes: a base `ERROR`
line naming the file reads `failing on base too`. Q3 is measured here and Q4
is written here. The per-attempt `run(..., shell=True)` stays in
`compare_at_base`'s own body.

## What this phase found

- **Q3, measured against pytest 9.1.1** (the `.venv` `bin/test` builds), in
  a scratch directory that was then deleted:
  - a collection error without xdist prints `ERROR tests/x.py` and then
    `!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection
    !!!!!!!!!!!!!!!!!!!!`, or `… 2 errors during collection …` for two;
  - the same under `-n 2` is NOT interrupted: every other file runs, and
    the line reads `ERROR tests/x.py - ImportError while importing test
    module …`;
  - a fixture error in setup prints `ERROR tests/x.py::test_d - RuntimeError:
    x`;
  - `-x` prints `!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures
    !!!!!!!!!!!!!!!!!!!!!!!!!!!`, and under xdist a second rule, `!!!!!!!!!!!!
    xdist.dsession.Interrupted: stopping after 1 failures !!!!!!!!!!!!!`;
  - a path that does not exist prints `no tests ran in 0.00s`, which
    `suite_counts` does not read as a summary.

  All five are pinned as `MEASURED_ENDINGS`, the cases of
  `test_the_base_run_is_read_off_what_pytest_printed`.
- **The early stop is read as the `!` rule, not as the two texts.** Read in
  the installed `_pytest/terminal.py`: a `!` separator is written for
  `session.shouldfail` (maxfail), for `session.shouldstop` (stepwise, xdist)
  and for an interrupt (`_report_keyboardinterrupt` · NAME NOT IN TREE, which collection errors
  and `pytest.exit` reach), and otherwise only under `--collect-only`, which
  runs no test. So `STOPPED_EARLY_RE` is `^!{3,} .+ !{3,}$`. This narrows
  `plan.md`'s six-month risk: a reworded banner still reads as a stop, and
  only a stop written WITHOUT a `!` rule would read as a whole run.
- **Q4, the two reasons**, both starting `new? not measured`:
  `NO_RUNNER` — `new? not measured: no part of the row printed a pytest
  summary at the base (each part tried is kept as suite-at-base-<k>.txt)`;
  `STOPPED_EARLY` — `new? not measured: the run at the base stopped before
  every test ran, and it does not name this file`.
- **Seen red against `e141980a`, executed.** The new cases were run with
  that commit's `broad_gate.py` swapped in, the three new constants appended
  to it so that every case compares words rather than failing on a missing
  name. The old gate gave: A1 `new` (expected `failing on base too`); A4
  **`failing on base too`**, a measured-looking word from a row that ran no
  pytest at all; A5 `new`; A6 `new` for the file the base could not collect;
  the maxfail case `new`. A2 stays green there, as the spec expects: the old
  gate also says `new`, and A2 exists to keep the fix from saying `new?`.
  The first swap without the constants failed three cases on
  `AttributeError` alone, and that run was not counted as red.
- **Seen red by mutation, executed:** 19 mutations of the new units —
  `verdicts_at_base`'s three branches and its two readings, both alternatives
  of `ERROR_RE`, `STOPPED_EARLY_RE`, the summary test, the `break`, the
  grammar argument, the prefix handed to `run`, the prefix list, and
  `handed_to_shell`'s call to `cmd_exe_reads`. One survived: `ERROR_RE`'s
  `$` alternative, because a short-summary line is always followed by a
  newline and `\s` matches it. The alternative was removed (`b8c3e032`), and
  the two left were each mutated red.
- **Three cases were added beyond the spec's list**, each because a mutation
  needed something to hold it: `test_a_runner_first_row_runs_once_at_the_base`
  (A3's "only one base run is kept", which no existing S2 case could show
  because `SUITE_ROW` is one part), `test_a_row_is_cut_at_the_semicolon_its_shell_reads`
  (the grammar argument; skipped where `cmd.exe` runs the row), and the
  measured-endings unit above (the `ERROR` shapes xdist prints, which no
  end-to-end case reaches because the fixture row runs without `-n`).
- **A consequence of the frame, named:** a prefix ending at a part that is
  not the runner runs that part with the failing files as arguments —
  `uvx ruff check . tests/x.py` in this repository. It runs in the scratch
  worktree, which is removed afterwards. A part that deletes or rewrites its
  arguments could cost the runner its files there, and the result is `new?`
  rather than a false word, because pytest handed a missing path prints no
  summary.
- **`gate`'s comment above `not_as_written` was rewritten here rather than in
  phase 4**, because it named the function this phase removed. Its argument
  is restated for prefixes: every prefix is a substring of the row the
  refusal passed, cut before an operator, so none ends in the `&` the
  refusal is for.
- **Green, executed:** the three touched modules whole —
  `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` and
  `tests/test_the_commit_gate_decides_at_the_commit.py` — `696 passed, 79
  skipped`. The one-shell-site case is among them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `broad_gate.py#first_command` | `broad_gate.py#row_prefixes` and the prefix loop in `compare_at_base`; `seal/releases/0.10.0.md` S5 cites it, and its re-read lands in this work item's ledger fragment in phase 4 |
| the single kept file `suite-at-base.txt` | `suite-at-base-<k>.txt`, one per prefix tried |
