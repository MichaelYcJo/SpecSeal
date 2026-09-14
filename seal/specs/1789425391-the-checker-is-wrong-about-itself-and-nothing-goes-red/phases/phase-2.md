# 1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `2901671` |
| Ran by | specseal:smith on Claude Opus 5 (1M context) |

## What this phase was asked

#395's behaviour. The verdict-column arm from `7b2c0d7` back, bounded at
`VERDICT_COL` (not the header width), with the open word ended on **a space or
a comma**. Six shapes refused; the four-cell row that merely lacks its grounds
still written short at exit 0; `new` and `close` both refusing a numbered short
row at exit 2 rather than raising `IndexError`. The `assert code in (0, 2)`
hedge becomes one answer. A case pins that widening `chain.SEPARATORS` does not
widen the open verdict.

Verified by `tests/test_a_finding_id_is_a_bare_integer.py`, then by phase 1's
repaired walkers over this repository's own records — at this boundary, not at
the pull request.

## What this phase found

**The seam is rebuilt on top of round 4's findings rather than shipped and then
fixed.** `7b2c0d7` and `fec2c88` were read with `git show` and applied, and
round 4's four paste-ready corrections applied with them: the boundary is
`OPEN_BOUNDARY` rather than `chain.SEPARATORS`, the `OPEN_WORD` comment no
longer says *exact*, the four-cell case asserts `code == 0`, and no figure was
carried across — see the divergence below.

**The two mutation directions are what make the bound a decision rather than a
guess.** Both were run:

| Bound | What goes red |
|---|---|
| back to `NUMBER_COL` (the crash) | all three short-row cases |
| widened to the header width (round 3's proposal) | the four-cell case **and** `test_a_short_row_with_a_comment_pipe_is_not_padded_into_a_full_one` in `tests/test_the_record_is_generated.py` |

So `VERDICT_COL` is the only bound that refuses what crashes without turning a
shipped decision red. Round 4 stated that; it is executed here.

**The boundary's coupling runs in both directions, and each is half of the
finding.** Borrowing `chain.SEPARATORS` over-refused, because `-` and `:` are
already in the shared set — `open-ended question` and `open: see 5` read as the
open verdict and the refusal named a word the cell does not carry. And it tied
what counts as open to a constant five other readers may widen. S5 exists
because a boundary change alone closes only the first half; the case that
mutates the constant and asserts the reader is unmoved closes the second.

**Divergence from `plan.md`, stated: the `close` half of S2 had no case and now
has one.** Round 4 verified by probe that a two-cell numbered row hand-edited
into a record and run through `close` exits 2 with the new refusal, and left it
as a probe. `plan.md` phase 2 asks for `new` **and** `close`, and `spec.md` S2
says *cases on both subcommands*, so
`test_a_numbered_short_row_is_refused_at_close_too` is added rather than the
probe being re-run.

**Divergence from `plan.md`, stated: no corpus figure is written in this
phase.** `plan.md` splits behaviour from prose because *the figure cannot be
re-taken until the reader it is taken through is the reader that ships*. That
reader lands here, so every docstring this phase writes states the mechanism
and carries **no count at all** — rather than carrying round 4's `95 / 7 / 88`,
which was taken at `151792e` against a corpus this branch has already grown.
Phase 3 takes the figure with its population, date and reader. Writing a
placeholder would have been a stub in a core path.

**Q4's answer for this phase, and it is smaller than `plan.md` forecast.** The
plan counted `verdict_rows`, `finding_number`, `build` and `id_refusal` moving,
with 1 + 2 + 4 + 1 shared-ledger rows anchored there. Executed: `build` and
`id_refusal` did not move at all — the arm needed no change in either — and
`evidence-check` named **two** drifted rows, not three:

| Row | Anchor that moved | Re-read |
|---|---|---|
| `seal/ledger.md` R1 | `finding_number`, docstring only | The clause is narrowed a third time and the narrowing is in the CALLER. `finding_number` still admits a no-digit cell that is neither empty nor 🔴/🟡; `verdict_rows` refuses it a second way. So *unless it is empty or carries 🔴 or 🟡* no longer enumerates the exceptions, and the third one is a row of this work item's fragment |
| `seal/ledger.md`, the folded `1789356180` row about a `#` cell with no digit | `finding_number` and `verdict_rows` | Its *what still fails* paragraph is exactly what this phase changes: a row carrying 🟢, ❓ or ⬜ that IS open is now caught where its Verdict cell says so. Every figure in the row is untouched |

Both were re-read on substance and re-stamped in one write; `evidence-check
--strict` is exit 0 at 1234 ok · 0 drifted · 0 broken.

**A frame defect, found by the gate and not by reading.** Once this work item's
ledger fragment existed, `evidence-check --strict` began reading the work
item's own records and refused `spec.md:138`: S11 cites `SUMMARY_WORDS`, and
**the tree does not hold that name** — #30's own round 2 renamed it to
`SUMMARY_TAIL` (its 🟡 13). `quote`, the other name on the same line, is real
(`skills/verify/scripts/broad_gate.py#quote`). The line is annotated
`NAME NOT IN TREE` with what the name became, which is the convention
`1789002694`'s own records already use for the same rename; no claim of S11
changes, and phase 5 builds the case on the shape that round measured. This is
in the hand-back, not back to the framer.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `assert code in (0, 2)` hedge in `test_a_row_missing_only_its_grounds_is_still_written_short`, and the comment saying the row *IS refused* | Nowhere — both were false. The row is admitted and written short, which the case now asserts as one answer |
| The claim, in three carriers this phase rewrote, that a vocabulary test is what *the verdict word cannot do this job* argues against reading at all | `OWED_MARKERS`' comment, `finding_number`'s docstring and `test_a_no_digit_cell_whose_severity_owes_an_answer_is_refused`'s docstring, each of which now says *a VOCABULARY test* and points at the arm that reads the one word. The remaining carriers — `docs/review-chain-spec.md` and the ledger sentence — are phase 3's |
