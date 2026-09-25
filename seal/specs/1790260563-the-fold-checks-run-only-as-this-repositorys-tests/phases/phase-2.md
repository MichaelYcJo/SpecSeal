# 1790260563-the-fold-checks-run-only-as-this-repositorys-tests — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | b8d01f79 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

Ship `skills/settle/scripts/fold_check.py`, flag-driven. It holds the
functions moved out of the two test modules, with `bound` and
`shape_problems` taking the cutoff as a parameter. It adds
`enforced_lines(text)`, a CLI with `--root`, `--shape-from` and `--ceiling`,
exits 0/1/2 and the interpreter-floor guard, and comes with `bin/fold-check`
and `.cmd`, executable. Both test modules import from it and keep their
planted cases, unchanged in what they assert. The two `Enforced by:` lines in
`docs/the-evidence-ledger.md` re-point to the script. The release-file rows
whose anchors left `tests/` are REMOVED there and written anew in this work
item's fragment. `bin/fold-check --shape-from 1790154761 --ceiling 1000` is 0
on this tree, and there is one CLI case per exit code over a planted root.

## What this phase found

- **Q1 answered by measurement: 115, not 101.** `fold-check --shape-from 0`
  reads 136 statements in 14 documents; 21 are bound at `1790154761`, and
  the other 115 are named, each for carrying no `Enforced by:` line (26 of
  them also for not opening bold). The prose's 101 counts the statements
  folded before #520. The other 14 are statements of work items released
  with it or waiting from before it, which the same prose sentence also
  excludes. #565 starts from 115; this work item corrects no prose about
  101, per Q1's default.
- **The root resolver phase 3 will use is `hooks/optin.py#home_at`, not a
  copy of `broad_gate.py#seal_home`.** `settle.py#main` already loads it by
  path, and it answers the same two places in the same order, plus the
  opt-out marker. The plan said to copy the shape and not the code; loading
  the one resolver writes no second one at all.
- **An empty `Enforced by:` value keeps today's message.** The first draft
  of `names_targets` returned false for an empty value, which would have
  reported it as `says nothing and gives no reason` where the moved code
  says `an empty target`. The predicate is now exactly the old branch
  condition, and `enforced_lines` asks the same one, so the lines a wrap
  limit skips (phase 4) are the lines this reads as paths.
- **Only 0.14.0's two rows were removed here, not 0.15.1's S1.** Every
  anchor of 0.15.1's S1 — `OVER_CEILING`, `FROZEN_IDS_DIGEST`, the prose
  pin — still stands after this phase, because the constants go in phase 3.
  It is removed in the phase that removes its anchors.
- **The messages that name `FROZEN_IDS_DIGEST` are unchanged here.** They
  still name a constant this phase leaves standing. Phase 3 replaces the
  constant with the `Over the ceiling` row, and the messages change there,
  pinned anew (§14).
- **A formatter hook stripped two imports.** Appending the command cases
  after the edit that needed `subprocess` and `sys` let the hook drop them
  as unused. The next run failed with a `NameError`, and the imports went
  back in.
- **Seen red (§15).** The new command and floor cases were written against
  the finished script, so each was shown red by mutation at `0a739888`
  (listed in the fragment's F1–F4). One mutation stayed green:
  `marker_digest` without `sorted`, because no fixture reorders markers. The
  unit was moved, not added, and the overview's Not done carries it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `statements`, `bound`, `target_problem`, `shape_problems`, `HEADING`, `BOLD_OPENING`, `ENFORCED`, `NOTHING` from `tests/test_a_folded_statement_names_what_enforces_it.py` | `skills/settle/scripts/fold_check.py`, same names |
| `markers`, `marker_digest`, `documents`, `ceiling_problems` from `tests/test_a_document_has_room_for_the_next_fold.py` | `skills/settle/scripts/fold_check.py`, same names |
| `seal/releases/0.14.0.md` rows S1 and P1 | `seal/ledger/1790260563-the-fold-checks-run-only-as-this-repositorys-tests.md` rows F1 and F2, and a note in 0.14.0's own comment saying where they went |
