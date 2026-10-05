# an in-place `--reverify` leaves history alone and reports each row once (#785, #792, #781) — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/{spec,plan,questions,routing}.md (D1–D5, S1–S16, Q1–Q3); docs/the-evidence-ledger.md §A released row is read again in the branch's fragment (the family, `--into`, *Without the row* and five-things paragraphs); skills/evidence-check/SKILL.md §Re-verifying is recomputing the hash; docs/the-pact.md §A signatory records a pact change; issues #785, #792 and its comment, #781; the 0.18.2 item's post-review-check.md and post-review-check-2.md
· evidence: seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md — A1–A6, 30 `Re-read ·` rows written by `--reverify --into` as this branch builds it, and a `Corrected ·` row over seal/releases/0.18.2.md:91
· verified: executed — every new case seen red at a3aa139a or under a mutation, every added unit mutated through `bin/mutation-check` (one equivalent test removed), the Q3 probe, the evidence-check, pact, re-read, correction, one-home, paste, wrap, identifier, word and folded-statement modules, `bin/evidence-check --strict .`, `bin/survivor-check`; read — the 31 released claims, 30 re-dated and one corrected

## Why this work exists

An in-place `--reverify` re-stamped and re-dated readings `--strict` no longer judges, and printed lines a later walk or its own walk made false; now it leaves those readings alone, prints each coordinate's outcome once, and names only a remedy the run supports.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A held coordinate on a row the run dates | Spec D1: *Left alone means: its hash is not rewritten … A row with other coordinates the run does re-stamp is dated as today, once.* | A held coordinate rides its row where the run dates that row for another move: re-stamped with it, its move handed to MOVES. Elsewhere it is left alone, as D1 says | `docs/the-evidence-ledger.md`, the family paragraph: *only the readings with the newest `Checked` date count*. The date makes the row the newest reading of the held coordinate, so left at an outranked hash it reads DRIFTED: `--strict` exit 2 where the base exits 0. Measured in `test_a_held_coordinate_on_a_row_the_run_dates_is_re_stamped_with_it` (`phases/phase-1.md`) |
| A held coordinate no one place holds | Spec D1 is silent; phase 1 left it with no line on every row | Left with no line where the run does not date its row; on a row the run dates for another coordinate, named `left` in the check's own terms and handed MOVES a BROKEN part (round 1, yellow 1), unless one of its places, for a claim exactly one, holds what the row recorded, which reads as unchanged (round 2, yellow 1); where its only place is one the declaration rule is unsure of and it has no claim, re-pointed onto its one provable destination, or left `, and no destination is provable` (#808) | The rider rule above: the date makes the row that coordinate's newest reading, so `--strict` reads it BROKEN, and the run says so as it does for any coordinate no one place holds; where one place holds the recorded content, or for a coordinate with no claim several do, the check calls it OK, and the run agrees; a claim two places hold is a tie the check calls BROKEN, and since #808 both `reverify` sites name it so. An unsure place with no claim is read as the ordinary path reads it, destination scan included, which keeps the base's heal (#808). `test_a_held_coordinate_with_two_places_on_a_dated_row_is_left_and_named`, `test_a_held_coordinate_one_of_whose_places_holds_it_rides_a_dated_row_silently`, `test_a_held_coordinate_with_an_unsure_place_on_a_dated_row_heals_to_its_destination`, `test_a_held_claim_two_places_tie_on_a_dated_row_is_left_and_named` |
| A held coordinate naming a line of a ledger the run writes | Spec D1, *Why it is judged before the walk*: *The walk changes ledger lines, never code* | Never judged held; re-stamped as before #785 (round 1, yellow 2) | The walk moves that line, so the judgment made before it is about a line that no longer stands; left at the old hash, `--strict` read the family DRIFTED where the base read it clean. `test_a_held_ledger_coordinate_the_run_moves_is_re_stamped` |
| When a `left` line is printed | Spec, Class 2: *a `left` line iff the last walk that was not `unchanged` left it* | Exactly where the last walk left the coordinate, which is where MOVES gets a BROKEN part | S9 in the same spec forbids a line for left then unchanged, and `walked_move`'s docstring: *a walk reading the coordinate unchanged clears a BROKEN an earlier walk left* (#791). Enumerated in `test_every_walk_sequence_prints_what_the_file_holds` (`phases/phase-2.md`) |
| Which readings decide reason (i) | Spec D3: *(i) Outside the run. A member reading of the coordinate that does not hold sits in a file this run did not write* | The newest-dated readings only, for (i) and (ii) both | The family paragraph counts only the newest readings, so an older reading outside the narrowing is one a run without `--ledger` would re-stamp to no effect. `test_an_older_reading_outside_the_narrowing_names_no_ledger_remedy` (`phases/phase-2.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository lint and the typecheck at this branch's head | the sealer, after the review rounds settle |

## Not done

**An outranked reading in a *drifted* family is still re-stamped and dated.**
Spec §*Out* leaves it: re-stamping only the newest reading needs a rule for a
newest reading the run cannot write, released under the freeze or in a file
the narrowing left out. It is a new design, for a new issue if the owner
wants it.

**`seal/follow-up.md`'s row on several rows citing one unit is unchanged.**
D1 narrows it only where those rows are one family, so its open options
stand, and this item does not edit the shared file.

**Two shapes the capped review found are deferred.** A non-citation ledger
coordinate whose file the walk reaches before the file it names is left
drifted (#806, walk order). An unsure place with a claim that does not hold
the row's hash is handed a BROKEN part where the check reads DRIFTED (#809),
a design question for the evidence-check maintainer; the output is the
base's.

## Fed back into the spec

- `spec.md` D1, *Why it is judged before the walk*: the exception for a coordinate naming a line of a ledger the run writes, and the dated-row rule for a held coordinate no one place holds, marked *inferred during implementation, round 1*.
