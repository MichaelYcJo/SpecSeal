# 1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 4910e445 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#591, the second of three phases. In `corrected`, a retired directory's
paths are read at `a` and their sentences join `gone` before
`paired_across_paths`. After the pairing, every departure under a retired
directory is dropped. The module docstring's §*A retirement is out of the
range* says the pairing runs first and why. `docs/review-chain-spec.md`'s
second statement names a fold's verbatim text as a move. Verified by spec S4
(red before the fix: exit 0); S5, the #517 block green and unedited; S6,
`survivor-check` over `f673e3b1..8e13036c` and `3c3f2342^..3c3f2342` at this
phase's commit, recorded here against the framer's measurement (0
survivors, 44 removed); and
`tests/test_unverified_rows_close.py#test_every_reader_of_a_retirement_calls_the_one_predicate`
green.

## What this phase found

- **S4 red at `4665def0`, executed.** That is phase 1's tip, and its
  retirement handling is the same as the base's. The fold case exited 0 and
  read `against 0 sentence(s)`. The correction in `docs/a.md` had paired
  with the fold's arrival in `docs/b.md`, so nothing was removed. Green
  after: exit 1, `docs/b.md:3` reported, `corrected` naming `docs/a.md:3`,
  and `against 1 sentence(s)`.
- **Phase 1's order decides this case.** The retired `spec.md` and
  `docs/a.md` each share one key with `docs/b.md`, so affinity ties. The
  retired side wins because it is gone at the tip, and a retired directory
  always is. Without that rank the tie falls to path order, and `docs/`
  sorts before `seal/`, so the arrival pairs with the correction again.
  Executed: with `origin in present` taken out of phase 2's order, the fold
  case is red. So phase 2 could not have been built alone, as `plan.md`
  says.
- **S6, executed.** Each range was run with the base's scripts, extracted
  from `2e0e2fa7` into the scratch directory, and with this phase's script.
  All four runs exited 0 over 350 files, against 44 removed sentences, and
  reported 0 places. That is the framer's measurement exactly. The issue's
  premise does not hold on this range, as `spec.md` judgment 4 recorded.
- **Mutations, one at a time, the file restored from a copy after each.**
  Dropping the retired paths before the pairing again turned the fold case
  red. Removing the drop after the pairing turned the fold case and #517's
  A8 red. In A8 the retired sentences became sources, and `docs/policy.md`'s
  restatements were reported.
- **The ledger.** Row G5 in `seal/releases/0.14.0.md` said a retired
  directory is *out of the range on both sides*, which is no longer exact.
  It was corrected in place with a `Corrected 2026-09-25` note. The
  eleven other rows anchored on `corrected` were re-read and re-stamped.
- **Q1 at this phase: unchanged.** `RELEASE_RANGES` passed unedited in the
  narrow run.
- **The narrow run.** The same 21 modules at `4910e445`, with this phase's
  ledger edits in the tree: 1271 passed, 1 skipped, 0 failed. `ruff check`
  and `ruff format --check` are clean on both Python files, and
  `bin/evidence-check .` exits 0 after the re-stamps.
- **Q3 at this phase: 2 more lines, 4 in all.** The document has 966 lines.
  The second statement's `Enforced by:` line also names `retired_directories`
  now. `bin/fold-check` exits 0.
- **CONTRIBUTING's four items.** Red test: above. Failure direction: toward
  reporting. Retired departures can only take pairings away from live ones,
  which keeps the live ones as sources and keeps their arrivals out of
  `written`. Prompt budget: 0. Platform: pure text over git blobs, and the
  retirement's own arms are unchanged.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the path-list filter in `corrected` that dropped retired directories before any blob was read | none — the same drop now runs on `gone` after the pairing, in the same function |
