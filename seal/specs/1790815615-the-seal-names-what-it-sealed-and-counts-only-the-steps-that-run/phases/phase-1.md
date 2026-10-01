# 1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run — phase 1

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 15f6ff39 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model; the orchestrator fills this row |

## What this phase was asked

`plan.md` phase 1 (S1, S2): the `SEALED`/`NOT SEALED` heads and the hook's
label name the branch, the base's ref and the pull request, in the
`<branch> @ <tree> against <ref> @ <commit>` shape with the detached and
bare-commit collapses; the values file gains `branch` and `pr`, the `PR` row
read through `chain_check.PR_RE`; one new constant printed after the `SEALED`
line on a recorded seal. A values file without `branch` draws today's label,
and `tests/test_a_gate_that_fails_says_so.py`'s old-shape file stays green
unchanged. Docs: `agents/sealer.md`'s exit-0 bullet,
`skills/code-review/orchestration.md` §*The stamp is drawn for you*, the
`broad_gate.py` docstring paragraph on the failure form. The spawn added: the
whole run is under `automation`, every edit through `Edit`/`Write`, every
commit `git -C <worktree>` in a call of its own, narrow tests only.

## What this phase found

- **The frame holds, with three corrections** (said before the build, per
  `agents/smith.md` phase 1):
  1. `chain_check.verdict_of` does NOT hand back `deferred <home>` with the
     home — it returns the bare word `deferred` for a homed deferral and
     `deferred (no home)` for a bare one. `spec.md` §Grounding (the
     `review-chain-spec.md` row) and S4 say otherwise. Phase 3 reads the home
     off the verdict cell after the word, with `chain_check`'s own
     `EMPHASIS`/`SEPARATORS`, only for rows `verdict_of` already called
     `deferred`.
  2. `spec.md` A3 says a repository with no remote collapses the ref like a
     bare SHA. It does not: `resolve_base` step 3 returns the ref as given,
     which is a branch name, so the head reads `against base @ <commit>`.
     Only a ref spelled in hex that is a prefix of the commit collapses
     (`overview.md`, divergence 1).
  3. `plan.md` phase 4 says `test_the_gate_reads_the_given_base_exactly_once`
     moves because `base.given` gains readers. That case counts `args.base`,
     not `base.given`, and `args.base` stays read once.
- **One record reader for phases 1 and 3.** `sealed_record` loads
  `round_record.py` by path and asks `seal_home` which file the cell went
  into — the same function that chose it — and reads it with `chain_check`'s
  `table_rows`. Phase 3 asks the same `Record` its `Needs a fix` and verdict
  table, so no second reader exists.
- **The commit-the-cell line asks git.** It prints where `git status
  --porcelain` names the cell's file, so it cannot say *not committed* over a
  clean file (`overview.md`, divergence 2). It also follows the stamp on a
  terminal run, which S2 did not name (divergence 3). Paths are compared by
  realpath: on macOS `tmp` is `/private/var/…` to git and `/var/…` as
  typed, and `relpath` between the two spellings is `../../…`.
- **A version number in a docstring is a timer.**
  `tests/test_release_hygiene.py` refuses a loaded file naming a version at
  or above the running one; `label`'s docstring said *from 0.17.0 on* and now
  names #666 instead.
- **Seen red (§15):** every new and moved case — 26 of them, listed in the
  run — was run against `d6a79a03`'s `broad_gate.py`, `seal_stamp.py`,
  `agents/sealer.md` and `orchestration.md` (restored from kept bytes after),
  and all 26 failed. Then each of 19 mutations, one at a time with the
  bytecode beside the file cleared between them, turned its cases red; none
  survived.
- **Pins moved (Q5):** the sealer test's green-tree and recorded-pipe heads
  (`head_of`), the failing-test head, the range test's A6/A7 heads, and the
  stamp test's five label pins (`LABEL`). `test_a_gate_that_fails_says_so.py`
  line 621 is unchanged and green.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
