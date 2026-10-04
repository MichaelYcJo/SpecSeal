# 1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Nothing here blocks the build.** No row needs a person. The run is
unattended (`routing.md`: `automation`), and the spawn prompt asked that every
open choice be decided from the tree and listed.

**What the tree answered for this frame, so nobody reopens it.** Each was
decided by the framer. A reviewer overturns one by opening its grounds.

| Judgment the issue left open | Decided | Answered by |
|---|---|---|
| Refuse the stale date, or name it | Name it: the row is `LEFT`, the run exits 1, and other rows still write | `evidence_check.py#reverify_into`'s docstring (*Exit 1 where a row was left*). The round-2 report's proposed repair. `plan.md` Alternatives |
| Where the refusal sits in W1's order | Step 1 (plan), inside `reverify_into`, before the row reaches `rows` and before its moves reach `moves`. Not step 0 | #756 spec W9 offers both options. Step 0 runs before the in-place re-stamp and would refuse runs that write no stale row (`plan.md` Alternatives, first row) |
| Whether kill-safety and record-first still hold | Yes, by construction. The refused row is in neither the plan nor the record, so no step can write it | #756 spec W1, W2, W4 |
| Older, or older-or-equal | Strictly older. A tie joins the union and clears | `docs/the-evidence-ledger.md` §*A released row is read again …*, 3rd paragraph |
| Per coordinate, or per row | Per row. Any drifted coordinate whose newest reading is later than `--checked` refuses the whole row | `INTO_VERIFIED` claims the whole row. *One row per row, never one per coordinate (spec D4)*, `reverify_into`'s docstring. W8 (no line claims what did not happen) |
| Exit 1 or exit 2 | 1 | Exit 2 is the invocation's refusal before anything is read (`--into` not a fragment, unreadable, `checked_refusal`). A stale date is one row's, and one `--checked` can be fine for one family and stale for another |
| Which date counts as the newest | The one `family_view` grades by: the newest calendar date in a member's `Checked` cell, over the members carrying the coordinate. It is shared, not computed twice | `evidence_check.py#family_view`'s `checked`. `#exit_code`'s docstring on a predicate that restates a rule |
| Whether an in-place re-stamp can be stale | No. `dated_cell` appends and `checked` takes the max, so a re-stamp never lowers its row's date | `evidence_check.py#dated_cell`, `#family_view` |
| Whether ⬜ 11 changes behaviour | No. It names the families and pins them | Issue #746's first checkbox. The round-2 report (*Only the sentence is this item's*) |
| Where the ⬜ 11 sentence goes | A bold-led paragraph replacing the trailing double-correction sentence of the section's last paragraph. The stale-date refusal goes in the `--into` paragraph | The last paragraph is about the unfrozen case, and the families span both modes |
| Whether the evidence-check `SKILL.md`, `templates/config.md` or a README changes | No. They summarise `--into` and point at the doc. None states the exit-0 promise this work corrects | `skills/evidence-check/SKILL.md` §*One fragment per work item*, `templates/config.md` §*The ledger freeze*, read |
| Whether the parallel chore's ten rows are taken | No | The spawn prompt |

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Beyond the three families in `spec.md` §*The class*, does any configuration leave `--reverify` at exit 0 while `--strict` exits non-zero for a family's coordinate? Candidates nobody has run: a citation whose released line changed, without the freeze; a `MALFORMED` citing row inside a family; a superseded root narrowed to; a coordinate whose newest reading has no calendar date | a measurement | The tree cannot answer it because the table in `spec.md` is `read`, and the report's grid (P1–P11) covered fragment and released carriers but not these. Phase 2's enumeration settles it. A cell that is found joins the S4 paragraph and gets a case. None found: the paragraph names three | the three | ⬜ |
| Q2 | Does `--strict` already refuse a ledger row whose `Checked` date is after today? | a measurement | One `--strict` run over a planted row settles it. Reading `family_view` and `calendar_date` shows no such refusal, but the records arm was not read for it. If it refuses, A7's tree also fails `--strict` for that reason, and the case asserts the `LEFT` line alone. If it does not, A7 stands as written | build A7 as written | ⬜ |
| Q3 | The exact wording of S3's `LEFT` line | the work | It cannot be known before the code exists, because the existing LEFT lines' shape and `where()`'s spelling decide it. Phase 1 writes it with the elements S3 lists, and its case pins it | — | ⬜ |
| Q4 | A stale-date axis on the 144-cell grid, or a focused sibling over `three_readings` | the work | The grid's cost per cell is unmeasured here. An axis that only runs in mode `freeze with --into` adds up to 96 cells. A sibling over `(m_at, n_at, carrier)` × {M's file, N's file, no `--ledger`} × {between, tie} is 48. Phase 1 times one cell and picks. Either one must be red at `edee5ca2` in the P5 cells | the sibling | ⬜ |
| Q5 | Whether this branch's `Re-read ·` rows and the parallel chore's rows conflict after both land on `release/v0.18.1` | the work | It cannot be known until both exist. Whichever branch integrates second runs `evidence-check --strict .` after merging the release branch in, and reads again any coordinate the other's later reading outranks | — | ⬜ |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
