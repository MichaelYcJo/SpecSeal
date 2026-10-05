# an in-place `--reverify` leaves history alone and reports each row once (#785, #792, #781) — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     filled when the work item closes
· evidence: filled when the work item closes
· verified: filled when the work item closes

## Why this work exists

An in-place `--reverify` re-stamped and re-dated readings `--strict` no longer judges, and printed lines a later walk or its own walk made false; now it leaves those readings alone, prints each coordinate's outcome once, and names only a remedy the run supports.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A held coordinate on a row the run dates | Spec D1: *Left alone means: its hash is not rewritten … A row with other coordinates the run does re-stamp is dated as today, once.* | A held coordinate rides its row where the run dates that row for another move: re-stamped with it, its move handed to MOVES. Elsewhere it is left alone, as D1 says | `docs/the-evidence-ledger.md`, the family paragraph: *only the readings with the newest `Checked` date count*. The date makes the row the newest reading of the held coordinate, so left at an outranked hash it reads DRIFTED: `--strict` exit 2 where the base exits 0. Measured in `test_a_held_coordinate_on_a_row_the_run_dates_is_re_stamped_with_it` (`phases/phase-1.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository lint and the typecheck at this branch's head | the sealer, after the review rounds settle |

## Not done

nothing

## Fed back into the spec

none
