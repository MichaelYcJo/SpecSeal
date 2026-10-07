# 1791384162-the-macos-test-leg-runs-in-shards — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | e43c461e (the shards, the reader and the sentences are ea43bac7) |
| Ran by | unknown — the spawn prompt named the agent, `smith`, and not the model; the orchestrator fills this row |

## What this phase was asked

Build phase 1 of `plan.md` and hand back, because phase 2 reads a CI run only
the orchestrator can start. The three `macos-latest` shard entries at
`timeout: 35`; `pytest_matrix` beside `jobs` with its fixture cases; the four
private slices of the `pytest` job moved onto `jobs` and the helper; the shard
module widened to a table of sharded systems with its first case renamed;
every sentence that said macOS is one job; every new or changed case seen red.
Close with the `plan.md` Status commit, this record and any ledger rows in
this work item's fragment. Narrow verification only: the modules that read
`test.yml` and the files changed, never the full suite. No push, no dispatch,
no pull request.

## What this phase found

**The frame holds, with four corrections.** Each is a divergence row in
`overview.md`.

1. **The rename leaves 0.20.0's S4 BROKEN, not DRIFTED, so its `Corrected ·`
   row is written here.** `plan.md` §*The ledger* says that between this
   phase's commit and phase 2's fragment `evidence-check .` reads DRIFTED and
   nothing BROKEN. Executed at ea43bac7: `BROKEN
   tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py#test_every_group_of_the_windows_split_runs_exactly_once
   locator not found`, exit 2. The CI `ledger` job exits on 2 or more (`if [
   "$code" -ge 2 ]; then exit "$code"; fi`), so the run phase 2 reads would
   have carried a red `ledger` job. The `Corrected · S4` row in
   `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md` re-points S4
   to the renamed case and carries every coordinate S4 rests on, plus
   `pytest_matrix`, which the case now reads through. Its hashes were stamped
   by `evidence-check --reverify --ledger <the fragment> --checked
   2026-10-08`. After it, `evidence-check .` exits 1: 10 drifted, 0 broken.
2. **The collection figure names the wrong run.** `spec.md` Scope 1 puts the
   counts "at 5623d728" on "run 37577753583's job logs". That run's head is
   12d576b5 (`gh run view 37577753583 --json headSha`, executed); the run at
   5623d728 is 37580460950, `main` after the merge. Both give 12,819 on every
   leg (executed, each job's summary line): at 5623d728 ubuntu 12,739 + 80,
   macOS 12,731 + 88, the four Windows shards 2,717 + 17, 6,707 + 35,
   1,019 + 101 and 2,157 + 66. The workflow comment cites 37580460950.
3. **Two more sentences said only Windows is divided**, outside the spec's
   enumeration: the comment above the pip line in `test.yml` (*pytest-split
   divides the Windows leg into its shards*) and the comment on
   `.test_durations` in `tests/test_the_release_check_watches_what_ships.py`.
   Both now name both legs (contract §12).
4. **More released rows drift than S1, S2, S4 and S8.**
   `test_ci_installs_the_parser_the_runner_pins` and
   `test_ci_runs_the_suite_at_the_floor_the_runner_holds` are also cited by
   older rows. `evidence-check .` after the fragment reads 10 drifted
   coordinates in six released files, 0.8.2, 0.9.5, 0.16.0, 0.18.0, 0.18.1
   and 0.20.0, with S1, S2 and S8 among them. Phase 2's `--reverify --into` writes a `Re-read ·` row
   for each of those released rows, not only for S1, S2 and S8; read each
   cited row first, as the command's own help asks.

**For phase 2, two more things.** `evidence-check`'s records section reads
`plan.md` lines 152 and 153 DRIFTED, because they quote the `pytest` job's
and the timeout case's released hashes, `f453cc43` and `b32fe58d`. `plan.md`
`Verified by` for phase 2 is `evidence-check --strict .` exit 0, so those two
quotations need settling before it passes. And the `Corrected · S4` row cites
`.github/workflows/test.yml#pytest`, which phase 2's budget edit drifts, so
that row is re-stamped in place with the fragment.

**The reader's shape.** `pytest_matrix(text)` takes comments off through
`conftest.code_lines`, finds the job through `jobs`, and reads the items under
the one `include:` key until a line at a shallower indent, or at the same
indent that is not a `-` item. That second condition ends the list at a
sibling key such as `exclude:`. Each item must be `- { … }` on one line. Its
pairs are split on commas outside quotes, and each value comes back with its
quotes off through `conftest._unquote`. It raises `ValueError` naming the line
for a block-style item, a nested `{}` or `[]`, a key written twice, an
unclosed quote or a bare scalar. It also raises for a workflow with no
`pytest` job, a job without exactly one `include:`, and an `include:` with no
entry. A `- {` item at the same indent as `include:` is read as an item,
because YAML allows it.

**Q3, the seam for #835.** #835's registry has not landed on
`release/v0.21.0`. The docstring of
`tests/test_ci_gives_the_checks_what_they_need.py#pytest_matrix` names its
input class (*owned*) and what it refuses. #835's build adds the row for it
there, beside `conftest.py`'s readers.

**Seen red (§15), and the units mutated.** All are executed 2026-10-08.

- The renamed shard case was red against the unsharded macOS entry of
  822a8cbf's workflow, before `test.yml` was edited: `a macos-latest leg that
  is not a shard`.
- Twenty breaks went through `bin/mutation-check`, each restored and each
  `red`:
  - the shard case under five matrix breaks: a macOS group named twice, a
    group named by no entry, a macOS count that disagrees, a Windows entry
    with no split, and a ubuntu entry carrying one;
  - the timeout case with one macOS `timeout` removed;
  - the pytest-line case with `${{ matrix.split }}` taken off the line;
  - the floor case with one macOS shard at `"3.11"`;
  - the pins case with `pytest-split==0.10.0` on the pip line;
  - in `pytest_matrix` and `_flow_mapping`, eleven breaks: the block-style
    refusal deleted, comments not taken off, nested values not refused, a key
    written twice not refused, an unclosed quote not refused, the quotes left
    on, the no-entry refusal deleted, the `include:` count check weakened, the
    missing-job refusal deleted, the sibling-key end of the list removed, and
    commas not splitting pairs.

**Verified, executed 2026-10-08.**

- `bin/test` over the eight modules that name `test.yml`, together with
  `tests/test_ci_gives_the_checks_what_they_need.py`,
  `tests/test_a_workflow_is_read_the_one_way.py` and
  `tests/test_the_release_check_watches_what_ships.py`: 397 passed and 2
  skipped, exit 0, at ea43bac7's tree. The helper module ran again after the
  fixture commit: 10 passed.
- `grep -rn 'index("  pytest:")' tests/` printed nothing, exit 1.
- `uvx ruff check` and `uvx ruff format --check` passed over the six Python
  files changed.
- `evidence-check .` exited 1, with 0 broken, after the fragment.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `pytest_job` and `matrix_entries` in the shard module, `pytest_job` in `tests/test_a_slow_case_names_itself.py`, and the two inline slices in `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` (NAME NOT IN TREE: the two helpers this phase removed) | `tests/test_ci_gives_the_checks_what_they_need.py#jobs` and `#pytest_matrix` |
| `test_every_group_of_the_windows_split_runs_exactly_once`, by name | `test_every_group_of_each_sharded_leg_runs_exactly_once`; the `Corrected · S4` row re-points 0.20.0's S4 to it |
| the `WORKFLOW` constants of those three modules | `read("test.yml")` in the helper's module |
