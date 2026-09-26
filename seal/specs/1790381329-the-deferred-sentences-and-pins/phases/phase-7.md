# 1790381329-the-deferred-sentences-and-pins — phase 7

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | 500f2a0 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Close. The changelog fragment, one entry per issue, saying what a user of the
plugin sees change. New ledger rows, if any, in the work item's fragment.
`overview.md` with its `## Not verified` table (Q2's row at least). A last
`evidence-check` over the whole ledger to catch a drift a phase missed, and
the spawn's two handoff checks: `evidence-check --strict .` and
`survivor-check --range origin/release/v0.15.5...HEAD`.

## What this phase found

- **The ledger rows were written phase by phase, not here.** C1 and C2
  (phase 1), C3 (3), C4 (5) and C5 (6) are in
  `seal/ledger/1790381329-the-deferred-sentences-and-pins.md`, each written
  with the commit that closed its phase so no reviewer meets code without
  its rows. Phases 2 and 4 wrote none: their claims sit on existing rows,
  re-read with dated notes.
- **`overview.md` was opened in phase 3**, because
  `test_every_spec_directory_that_reached_the_ladder_has_an_overview` reads
  every directory that holds a `spec.md`. It now holds the proof block,
  seven divergences, Q2's row under *Not verified*, and *Not done*.
- **`survivor-check` reported two places**, both read and neither a
  sentence this branch made false: `docs/release-checklist.md` step 0
  (true on a branch checkout and at the merge ref) and the frame's own
  quote of the old config sentence in `spec.md`. Both are in `survivors.md`
  with a quote from the standing text and the grounds; with `--exempt`, the
  check exits 0.
- **The fragment gathers.** `gather_changelog.py --version 0.15.5
  --dry-run` prints it under its marker, and
  `tests/test_the_changelog_is_gathered_at_release.py` is green.
- **Verified by (executed, 2026-09-26):** `evidence-check --strict .` at
  `ed9635af`: exit 0, 2406 ok, 0 drifted, 0 broken, 0 malformed, 0 records
  refused. `survivor-check --range origin/release/v0.15.5...HEAD --exempt
  …/survivors.md` at `500f2a0`: exit 0, 2 exempt. `correction-check --range
  origin/release/v0.15.5...HEAD`: exit 0, no merge commit in the range.
  `unverified-check --baseline origin/release/v0.15.5 seal/specs/`: exit 0.
  `tests/test_a_record_states_what_the_tree_has.py`,
  `tests/test_chain_hooks_hardening.py` and
  `tests/test_the_changelog_is_gathered_at_release.py`: 158 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
