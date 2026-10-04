# 1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

## Why this work exists

A `--reverify` run could exit 0 while `--strict` over the same ledgers then
exited 2. After this work a back-dated `--into` row is refused and named, and
the families no re-read can clear are named in the ledger home and held by a
case.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How the released rows the edit drifted are read again | S7: *Released rows whose code this work drifts are read again into that same fragment with `--reverify --into`*. L4 and N1 of `seal/releases/0.18.0.md` claim `--into` writes a row this work now refuses for a stale date | `Corrected ·` rows for L4 and N1, carrying the claim with the narrowing and every coordinate; `Re-read ·` rows for the five drifted rows that still hold | A `--into` row's Notes say *the cited row's claim holds* (`INTO_VERIFIED`), which is false for those two. `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*: *A re-read or a correction is a citing row in the branch's own fragment* |
| How many families the paragraph names | `spec.md` §*The class*: three families, a double correction, a BROKEN anchor in a family, a family rooted in a fragment whose statement is gone. S4: *plus any further family phase 2's enumeration finds* | Five: the three, with BROKEN widened to any row outside a released carrier under the freeze, plus a citing row refused `MALFORMED` and a citation whose released line changed | `spec.md` §*Out*: row-shape refusals stay out *unless phase 2's enumeration shows one of them inside a family exiting 0* — the marker refusal is inside a family; the enumeration is in `phases/phase-2.md` |
| How A10 and A8 were held | S5 and A10: *Existing cases are extended where one already builds the family*, naming `test_a_family_rooted_in_a_fragment_is_owed_no_released_re_read` and `test_a_released_row_corrected_by_two_rows_names_both` | Sibling cases, `test_a_correction_whose_anchored_statement_is_gone_is_named_only_released` and `test_a_double_correction_is_left_at_exit_0_and_read_at_exit_2`; the two named cases stand as they were | A10's own wording allows *extend … or a sibling*; the siblings carry the mode, narrowing and placement axes without rewriting what the two existing cases pin (`phases/phase-2.md`). Missing from this table until round 1, ⬜ 4 |
| What a refused row records | S1 and S6 as approved: *No move is appended for it, so the pact-change record gets nothing for it*, after #756's W9 | Its moves are recorded; it still gets no `Re-read ·` row, is named, and exits 1 | Round 1, 🟡 2, taken by the orchestrator under the owner's `automation` answer: the after-today repair is a `Corrected ·` row no later re-read reaches, so the dropped move was never recorded, and #756's first promise is that a pact change is never lost. S1, S3 and S6 are marked changed by round 1 |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint over the repository and the typecheck at the branch's head | the sealer, after the review rounds settle |

## Not done

The chore's ten drifted rows (`fake_venv`, `VERSIONS_OF_ANOTHER_PRODUCT`,
`templates/config.md`) are left to
`chore/0-18-1-the-three-wave-one-items-read-each-other-after-the-squash`, as
the spawn said. `--strict .` reads exactly those ten DRIFTED until that
branch lands on the release branch.

The unfrozen writer's own citation drift is named and pinned, not fixed.
Without the freeze, one `--reverify` over every ledger that re-stamps a
released row in place moves the line its fragment's `Re-read ·` rows cite,
so `--strict` reads their citations DRIFTED until a second run
(`phases/phase-2.md`). Fixing it changes a writer's behaviour, which
`spec.md` §*Out* leaves to an issue of its own. Whether to file one is the
orchestrator's to decide; this repository runs frozen and never meets it.

## Fed back into the spec

*Inferred during implementation*, and the planner may overturn them:
`docs/the-evidence-ledger.md`'s paragraph names a citing row refused
`MALFORMED` and a citation whose released line changed, beside the three
`spec.md` named, and it states BROKEN for any row rather than for a family
alone. Each rests on `phases/phase-2.md`'s enumeration.
