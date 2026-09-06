# 1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading — review round 2

| Field | Value |
|---|---|
| Target SHA | 3d5ba51 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 181 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | COMMENT_NEVER_CLOSED (depth 1); ASKED_COMMENT_NEVER_CLOSED (depth 1); UNCLOSED_COMMENT_ASKED (depth 1); COMMENT_INSIDE_A_FENCE (depth 1); test_an_unclosed_html_comment_in_the_round_paragraph_is_refused (depth 1); UNCLOSED_COMMENT_REPORT (depth 1); test_an_unclosed_html_comment_in_the_report_names_the_comment (depth 1) |
| Needs a fix | yes |
| Loses a record or crashes | yes — finding 7 writes a round record whose four sections below the round paragraph are unreadable to every downstream reader |

- [x] Pass

## What this round was asked

Round 2, the verifying round, against `3d5ba51`, targeting the diff of round 1's
fixes — `861ad16..09d6bcb`, five commits. Three probes were handed over as
re-checks, and six claims of the fix pass were named as claims under §5: that the
two texts differ only in HTML comment content and that four things ride on them
agreeing; that a fourth shape was found and deliberately not fixed, with the
reason recorded and a rider left at the coordinate; that the pass corrected
itself mid-way about whether an unterminated comment is a silent loss or a
message defect; that 🟡 2 was extended with the partial case left open at a
stated cost; that both narrowing clauses of the new row rule had no case and
stayed green while broken; and five mutations recorded as killed.

The round was told that this item's own trap is that the branch changes the
record generator and validates its own records in CI, so every guard it adds
must accept the records this work item itself produced — and that its own report
may carry neither a fence closing after a later heading nor a fence opener
inside an HTML comment, both of which are now refusals in the code under review.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's 🔴 1 — the never-closed raise removed as unreachable | `skills/code-review/scripts/round_record.py#fenced_after` | answered | re-executed at `3d5ba51`: the input is refused, no record written, and the message names the asymmetry. Deleting the restored raise turns its case red and no other |
| 2 | Round 1's 🟡 2 — a fence takes a table's rows while its heading stands | `skills/code-review/scripts/round_record.py#swallowed` | answered | re-executed: dropping either narrowing clause turns the acceptance case red and nothing else. The partial-row limit is stated with its cost and is deferred, not missing |
| 3 | Round 1's 🟡 3 — the round paragraph never passed through the guard | `skills/code-review/scripts/round_record.py#build` | answered | closed for the fence half; deleting the check turns its case red and no other. The comment half is open as finding 7 |
| 4 | Round 1's ⬜ 4 — the unreachability sentence | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/phases/phase-1.md` | answered | read at `3d5ba51`: the replacement names contract §13 and the assumption that was never removed |
| 5 | Round 1's ⬜ 5 — F2's Notes named the repair as the tidy-up to resist | `seal/ledger/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading.md` | answered | the row now separates *necessary* from *sufficient*; all eighteen anchors of the fragment resolve |
| 6 | Round 1's ⬜ 6 — the completeness claim | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/changelog.md` | answered | corrected in all three files; the enumeration is now qualified to its partition and the axes it had not been applied to are named |
| 🔴 7 | the round-paragraph guard reads the comment-stripped text while the record splices the text verbatim; an unterminated opener writes a record whose four sections are unreadable and blames the writer for a section they wrote | `skills/code-review/scripts/round_record.py#build` | **fixed** `c7ebb29` | fixed at c7ebb29 — the comment question is asked of both texts, and **before** the fence question in each. The order has executed grounds rather than taste: an open comment blanks the closing fence of every block under it, so asking the fence first names a fence that is closed as written. The report side was a message defect rather than a loss, and its wording moved with it; executed at `3d5ba51`: record written, only the round paragraph resolves, and the failure names the wrong cause. The fix is validated in a clone and restored |
| ⬜ 8 | the straddling comment's deferral is measured on a Deferred row, where no section follows; the instance that loses sections is a verdict row and was not measured | `skills/code-review/scripts/round_record.py#swallowed` | answered | corrected at `01c9075` — the deferral stands on the reason it always had; only its recorded cost was wrong. A **verdict**-row straddle loses three whole sections, where the Deferred-row measurement was vacuous because nothing follows that section. The rider, `overview.md` §Not done and the fragment's row now carry the verdict-row number |
| ⬜ 9 | `fix_table` removes the sha from inside its own code span and leaves both backticks | `skills/code-review/scripts/round_record.py#fix_table` | deferred `skills/code-review/scripts/round_record.py#fix_table` — a `# RIDER:` at the coordinate, not `seal/follow-up.md`. That file's own header says a coordinate-tied item is a rider and that this repository has a tracker, so it should hold neither. The rider names the repair site too: the `note` line, **not** `chain.SEPARATORS`, which is shared with the `deferred` home reader and would strip backticks from a home written as a code span | `skills/code-review/scripts/round_record.py#fix_table` — a `# RIDER:` at the coordinate, not `seal/follow-up.md`. That file's own header says a coordinate-tied item is a rider and that this repository has a tracker, so it should hold neither. The rider names the repair site too: the `note` line, **not** `chain.SEPARATORS`, which is shared with the `deferred` home reader and would strip backticks from a home written as a code span |

## Executed probes

| What was run | Result |
|---|---|
| the 🔴's own input at `3d5ba51` | refused, no record; the message names the two texts and the comment |
| `--asked` carrying an unterminated comment opener | **record written**; only the round paragraph resolves; the failure blames a missing `## Verdicts` |
| `--asked` carrying a fence opener inside a balanced comment | succeeds, all five record sections readable — the copy-whole case is correctly accepted |
| a straddling comment in a **verdict** row | **record written**, the run fails; three sections resolve to nothing |
| a straddling comment in a **Deferred** row | **record written, exit 0**; the row below the straddle silently absent, every heading still resolving |
| `--asked` carrying a `## Verdicts` heading | record written, run fails, `chain_check` naming more than one such section — refused on the right cause |
| a report shaped like a reviewer's own — a comment plus a record-shaped fenced block with rows under a standing probes table | succeeds, all five sections readable; the new guards accept the records this work item itself produces |
| five mutations, each alone, restored byte-identically and asserted by digest | each turns exactly one case red: the restored raise, both narrowing clauses, the row loop, the round-paragraph check |
| finding 7's fix applied in a clone | the unterminated-comment case refused with no record; the balanced case still succeeds; the module's 53 cases green; restored byte-identically |
| six modules touching `round_record.py` | 256 passed. The handed-over figure of 128 named a set I was not given, so this is my own count over my own set rather than a confirmation of that number |
| unscoped `evidence_check.py .` at `3d5ba51`, exit read directly | exit 1 · 682 ok · 2 drifted · 0 broken; this branch's fragment 18 ok · 0 drifted. Both drifts stand at the base, confirmed by an empty diff over both files |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py#fenced_after` | round 1's 🔴 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#swallowed` | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#main` | round 1's 🟡 3 — fixed |
| round-1 | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/phases/phase-1.md` | round 1's ⬜ 4 — answered |
| round-1 | `seal/ledger/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading.md` | round 1's ⬜ 5 — answered |
| round-1 | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/changelog.md` | round 1's ⬜ 6 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the full suite, the repository-wide lint and the typecheck | contract §2 — not run in this round | the orchestrator, immediately after this round |
| a fence taking SOME of a table's rows beside a standing table | already deferred by round 1's fix pass to `overview.md` §Not done, with the cost stated | the orchestrator, if the limit is ever revisited |
| `fix_table` leaving an empty code span where the sha stood | pre-existing; `seal/follow-up.md` is the home the fix pass should name | the orchestrator |
