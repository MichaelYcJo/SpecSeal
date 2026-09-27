# 1790550713-what-the-0.15.5-rounds-deferred — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 61fbc03 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Write the work item's `changelog.md` as `spec.md` §*Data & interfaces* gives
it: `evidence-check`'s statement of when `#` and `@` count as one coordinate
now says the `@` must follow the `#`, and 0.15.5's entry left that out. Close
`overview.md` per `skills/implement/SKILL.md` §4. Run the sweeps over
`origin/release/v0.15.6...HEAD`: `survivor-check`, `correction-check`,
`evidence-check` and `gather_changelog.py --check`. No full suite and no broad
gate.

## What this phase found

- **The sweeps, executed at `61fbc03`, each exit read directly:**
  - `bin/survivor-check --range origin/release/v0.15.6...HEAD` exits 0. It
    examined 437 files against 43 sentences the range removed, and no
    removed wording is still standing, so no `survivors.md` was written;
  - `bin/correction-check --range origin/release/v0.15.6...HEAD` exits 0,
    with no merge commit in the range;
  - `bin/evidence-check .` exits 0: 2469 ok, 0 drifted, 0 broken,
    0 malformed, 0 refused;
  - `bin/unverified-check --baseline origin/release/v0.15.6 seal/specs/`
    exits 0, and this work item's one open row is the broad gate, answered
    by the sealer.
- **`gather_changelog.py --check` exits 1, and that is its right answer
  here.** It names this work item's fragment as never having reached
  `CHANGELOG.md`. A fragment is gathered at release preparation, and the
  check runs on the release pull request alone (`seal/releases/0.4.0.md`,
  the row "no other pull request runs the check"). `plan.md`'s "exits 0"
  cannot hold on a feature branch. `overview.md` records it as a divergence.
- **The first `survivor-check` call exited 2** because the `--exempt` file
  did not exist, not because of a finding. Run without it, it exits 0 as
  above.
- **The scratchpad is shared with the concurrent sessions of this
  milestone.** It holds files this session did not write, one named
  `test_tmp_mutate.py` among them. They are not this work's to delete. This
  work's own probe, `test_tmp_rewrap.py`, was deleted after its one run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
