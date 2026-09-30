# Implementation Plan: the guard and consent stop depending on the walk's order

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-30 by the orchestrating session, when `smith` was spawned.

## Summary

`walk_directories` answers each segment with the walk's directories and the
base thread's in one tuple, ordered by a rule. The commit gate judges every
entry. The worktree guard and the consent writer judge the first entry that
names a tree, so for them the rule decided the tree, and every version of the
rule met a new command. They now read the base thread alone, through
`cmdline.base_directories`, and their tree is `86256492`'s by construction.

## Technical context

- `hooks/cmdline.py#walk_directories` at `542f920b` computes both threads in
  one loop. The base thread's states (`base_states`, `base_parked`) already
  walk as `86256492` did: the base's landing, `understood` as it stood, a
  refused segment replaced, the same `STATE_CAP`. Only its reported
  directories carry one #674 addition, the second reading's unplacing where
  the first found no `git`, which exists for the gate (I14).
- The loop becomes `_walk`, which returns both answers. `walk_directories`
  returns the first, unchanged. `base_directories` returns the base thread's
  directories unplaced by the as-written reading alone.
- `hooks/worktree-guard.py#walk_command` and
  `hooks/worktree_consent.py#creation_directory` switch to
  `base_directories`. Nothing else in either file reads the walk's
  directories: `only_creates_a_worktree` ignores them, and `judgeable` and
  `classify` take one directory from the caller.
- What breaks in six months: a new reading added to the walk for the gate
  does not reach the guard, silently. That is the containment's point, and
  the 0.17.0 redesign is where the guard's reading is decided again.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. Order the two threads correctly for the guard (PR #690) | Each ordering met a new shape: I's round 2, I's Q7, #689's round 3, and #690's own rounds. The class is the order itself | Rejected by the owner under the 3+ Fix Rule |
| B. Vendor `86256492`'s whole walk as a second function | A second copy of the landing, the names and the cap, drifting from the first; the base thread already is that walk | Rejected |
| C. Read the base thread `walk_directories` already carries | A reading the thread shares with the walk (the expanded words, the `cd` target) could differ from `86256492`'s; the structural corpus measures that | Chosen |
| D. Also drop the ordering rule in `walk_directories` | The gate's deny names its first stopped target and lists unresolved ones in that order, so the reason text would change for the same commands | Rejected; measured in `overview.md` |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `base_directories`, the guard and the consent writer on it, the red-first cases, I13's guard case changed to the base's answer | the new cases red at `542f920b` and green here; the structural corpus against `86256492`; the gate corpus against `542f920b` | 97654799 |
| 2 | The policy sentences, I's ledger rows and changelog fragment corrected, this item's ledger and changelog fragments | `evidence-check --strict`, `unverified-check`, `survivor-check` | |

## Operational impact

None. No new dependency, environment variable or migration. The guard's answer
for a `cd` behind a redirection returns to the release base's, which is the
recorded cost.
