# 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 48d340b3 |
| Ran by | unknown — the spawn prompt did not hand the value over, and the segment does not source it from its own idea of what it is |

## What this phase was asked

#748 first, because it is one test and stands alone: the row-bound case in
`tests/test_the_commit_gate_decides_at_the_commit.py` polls per `spec.md`
Scope 7–8 instead of sleeping half a second once (B1). Verified by the case
alone three times, and by the group-kill mutation — `os.killpg(proc.pid,
signal.SIGKILL)` in `_run_bounded` replaced with `proc.kill()` — run once and
seen red, then reverted.

## What this phase found

- **The frame holds for the whole work item, read before the first edit.**
  Every coordinate `plan.md` §*Technical context* names was where it said at
  `836fd7b2`: `first_command` and its one caller, the single
  `run("suite-at-base", …, shell=True)` in `compare_at_base`, the shell-site
  case `test_the_one_shell_site_is_run_and_it_applies_the_rewrite`, rule 3 of
  `templates/config.md` at line 333 beside the lint-first example row, the
  fixture comment at line 750 of `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  and `seal/releases/0.10.0.md`'s S5 sentence "What it re-runs is what stands
  before the row's first `&&`".
- **The poll lives in a helper, `_stays_gone`, with its two numbers named**
  (`GONE_WINDOW = 1.0`, `GONE_DEADLINE = 5.0`). The deadline is measured from
  the moment `_run_bounded` returns, which is the bound as the case sees it.
- **Seen red, executed:** `bin/mutation-check` with the replacement above
  reported `red: the cases failed against the mutation (exit 1)`, and the
  failure read `AssertionError: the row's loop outlived the bound`. The file
  came back from `mutation-check`'s own copy, hash-compared.
- **Green, executed:** the case alone, three runs, each `1 passed` in about
  2.4 s — one window, because the group kill leaves nothing to touch the
  marker.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the fixed `time.sleep(0.5)` after the bound | none — `_stays_gone` replaces it |
