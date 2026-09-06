# 1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading — review round 3

| Field | Value |
|---|---|
| Target SHA | c8d2907 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 181 |
| Broad gate | c8d2907, against 774e76b — 2370 passed, 2 skipped, 0 failed. `uvx ruff check .` and `format --check .` clean over 108 files |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | yes — finding 10 writes a record whose section below the inherited row is unreadable to every downstream reader with nothing said. The run is capped, so it leaves as issue #182 rather than as a fourth round |

- [x] Pass

## What this round was asked

Round 3, a verifying round, against `c8d2907`, targeting the diff of round 2's
fixes — `aed3ca0..01c9075`, two commits. It was told this record ends the run
whatever it finds, since round 2 had already spent the one reopening, and that
it should therefore not hunt for a reason to continue but should state anything
it did find so an issue could carry it.

Three probes were handed over as re-checks, and the fix pass's own list of five
things to READ rather than re-hunt was passed through: the order of the two
questions and whether the order assertions are green only in that order; the
grid's third row argued as forced rather than sampled, with the note that a
counterexample there would be a sixth member; the verdict-row straddle number
and whether four documents carry it; the two hand-stamps against the value the
scoped run reported; and the home given to a pre-existing finding.

The round was asked to judge the completeness argument itself — a two-axis grid
whose columns are the reader's two passes and whose rows are the generator's
three copies — on the grounds that it was the branch's third enumeration and the
first two had each been one member short. Its own report was held to the same
refusals the code under review now makes.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | round 1's 🔴 1 — `fenced_after`'s never-closed raise | `skills/code-review/scripts/round_record.py#fenced_after` | answered | carried from round 2, whose re-execution closed it. This diff does not touch the function body; 55 cases green at `c8d2907` |
| 2 | round 1's 🟡 2 — a fence takes a table's rows while its heading stands | `skills/code-review/scripts/round_record.py#swallowed` | answered | carried from round 2. This diff adds the comment question above the walk and changes no index |
| 3 | round 1's 🟡 3 — the round paragraph never passed through the guard | `skills/code-review/scripts/round_record.py#build` | answered | the fence half closed in round 1; its comment half is finding 7, verified below |
| 4 | round 1's ⬜ 4 — the unreachability sentence | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/phases/phase-1.md` | answered | carried from round 2; untouched by this diff |
| 5 | round 1's ⬜ 5 — F2's Notes named the repair as the tidy-up to resist | `seal/ledger/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading.md` | answered | F2 was rewritten this pass and re-stamped; all 22 anchors of the fragment resolve at `c8d2907` |
| 6 | round 1's ⬜ 6 — the completeness claim | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/changelog.md` | answered | the round-1 claim is corrected. The round-2 claim that replaced it is finding 12 |
| 7 | round 2's 🔴 7 — the round-paragraph guard read the comment-stripped text while the record splices verbatim | `skills/code-review/scripts/round_record.py#build` | answered | executed at `c8d2907`: the unterminated opener is refused, no record, and the message names the comment, the splice and the closer. Four mutations each turn exactly one case red |
| 8 | round 2's ⬜ 8 — the straddle's cost was measured on a Deferred row | `skills/code-review/scripts/round_record.py#swallowed` | answered | executed: a verdict-row straddle loses three sections, the number all four documents carry. The number is right; its reach is finding 10 |
| 9 | round 2's ⬜ 9 — `fix_table`'s empty code span, and where the deferral belongs | `skills/code-review/scripts/round_record.py#fix_table` | answered | read at `c8d2907`: the rider is at the coordinate, carries its date and SHA, and names the `note` line rather than the shared separator set |
| 🔴 10 | `inherited_rows` copies raw cells out of an earlier record with no hider question — a fourth copy the grid has no row for, writing a record whose section below it is unreadable with nothing said | `skills/code-review/scripts/round_record.py#inherited_rows` | deferred #182 | executed at `c8d2907` twice — through two rounds from a straddling report, and from a record corrected in place. Record written, the section resolves to 0 occurrences, and the run prints nothing; `chain_check` reads only `## Verdicts` among sections |
| 🟡 11 | a comment that opens inside a copied block and closes outside it is refused by naming a fence that is closed as written | `skills/code-review/scripts/round_record.py#swallowed` | deferred #182 | executed at `c8d2907`: refused as *a fenced block in the report is never closed*, and every fence in the report closes. Neither new case reaches this shape |
| ⬜ 12 | the *a fourth copy would add a row … neither exists* claim is false in four places | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/overview.md` | deferred #182 | read at `c8d2907`; the same sentence stands in the test file's grid comment, in the changelog fragment, and as ledger row F2's verified claim |

## Executed probes

| What was run | Result |
|---|---|
| handed probe 1 — an `--asked` file ending in an unterminated comment opener | refused, no record; the message names the comment, the verbatim splice and the closer |
| handed probe 2 — the generator's own module | 55 passed, confirmed |
| handed probe 3 — unscoped `evidence_check.py .`, exit read directly | exit 1 · 686 ok · 2 drifted · 0 broken, confirmed. Both drifts stand at the base, shown by an empty diff over both files against `774e76b`. This branch's fragment 22 ok · 0 drifted |
| four mutations — the comment question deleted and the order swapped, in each of the two guards, each alone and restored by digest | each turns exactly one case red, and the two cases are the two the pass names. The order is load-bearing |
| the verdict-row straddle, re-measured | record written, three sections each 0 occurrences — the number all four documents carry |
| the same straddle carried into a second round whose own report is clean | the second record written, its Deferred section 0 occurrences, the inherited row carrying the unterminated opener |
| a `round-1.md` corrected in place with an unterminated opener in a Location cell, then the next round generated | the record written; the section present in the bytes, 0 occurrences to the reader; the whole run output naming nothing |
| a comment opening inside a fenced block under the probes table and closing after it | refused as *a fenced block in the report is never closed* — and the block closes |
| the third row's *unreachable*, argued from fence-state parity over `raw` rather than sampled | no counterexample: a closer outside a block leaves an odd marker count and is refused; inside a block it is itself copied, so the record's slice is balanced |
| `seal/ledger.md` R1 and R9, and the fragment's F2 | both hand-stamps move the same anchor and nothing else; `seal/ledger.md` 565 ok · 1 drifted, the drift being `templates/config.md` |
| the full suite, the repository-wide lint, the typecheck | not run — contract §2 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py#fenced_after` | round 1's 🔴 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#swallowed` | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#main` | round 1's 🟡 3 — fixed |
| round-1 | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/phases/phase-1.md` | round 1's ⬜ 4 — answered |
| round-1 | `seal/ledger/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading.md` | round 1's ⬜ 5 — answered |
| round-1 | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/changelog.md` | round 1's ⬜ 6 — answered |
| round-2 | `skills/code-review/scripts/round_record.py#build` | round 2's 3 — answered |
| round-2 | `skills/code-review/scripts/round_record.py#fix_table` | round 2's ⬜ 9 — deferred |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| findings 10, 11 and 12 | **issue #182**, opened by the orchestrator after reproducing finding 10 by reading `inherited_rows` and `chain_check`'s single section read | the repository owner |
| the full suite, the repository-wide lint and the typecheck | the broad gate, immediately after this round | the orchestrator |
| a fence taking SOME of a table's rows beside a standing table | already deferred by round 1's fix pass to `overview.md` §Not done, with its cost stated | the orchestrator, if the limit is revisited |
| the comment straddling a copied row | already deferred to the rider in `swallowed`; finding 10 is the part of its cost that rider does not carry | the repository owner, in #182 |
