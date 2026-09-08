# 1788844400-a-body-naming-two-issues-claims-one — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 4b62203, and 6b81d10 for what the mutations found |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Pin the check's behaviour with cases, wire the step into
`.github/workflows/hygiene.yml`, and mutation-test every unit added — one at a
time, committing before mutating, restoring from kept bytes rather than from
HEAD, clearing `tests/__pycache__` between mutations.

## What this phase found

**Two cases were red on their first run, both for real reasons.**

`test_a_hard_wrapped_sentence_is_still_one_sentence` failed because
`BLOCK_START` was the naive class `[-*+>|#]`, which reads `#22` at the start
of a line as a markdown heading. `#22` at the start of a line **is this defect
hard-wrapped** — the one thing the module exists to see. Every marker
CommonMark requires a space after now asks for one; `>` and `|` take none in
the markdown either. This was found by the case rather than by reading.

`test_the_check_imports_the_closers_definition_rather_than_restating_it`
failed on `KEYWORDS is KEYWORDS` while `CLOSING is CLOSING` passed. The case
was loading the sibling a second time by path, which builds a second module
object — so the identity was false for a module that had imported it
correctly. `CLOSING` passed either way, because `re.compile` caches by pattern
and flags and hands both loads the same object: **the two regex identities are
true whether the import happened or not, and only the tuple asks the
question.** The case now takes the sibling from `sys.modules`, where the
check's own import put it.

## The mutation log

Sixteen mutations, one at a time, restored from bytes held in the runner.
**Zero survivors**, and the module is green before and after
(`28 passed`).

| Mutation | Verdict | Caught by |
|---|---|---|
| rule 1 — `.!?;` no longer ends a segment | RED 2 failed | `test_a_new_sentence_is_a_new_segment`, `test_a_trailing_full_stop_after_a_number_still_closes_the_segment` |
| rule 2 — a blank line no longer ends a segment | RED 2 failed | `test_a_blank_line_ends_the_segment`, `test_a_fence_does_not_splice_the_line_above_it_onto_the_line_below` |
| rule 3 — a new markdown block no longer ends a segment | RED 2 failed | `test_a_list_item_ends_the_segment_without_a_blank_line`, `test_a_table_row_ends_the_segment` |
| rule 3 — the naive marker class, which reads `#22` as a heading | RED 1 failed | `test_a_hard_wrapped_sentence_is_still_one_sentence` |
| the mask collapses code to one space | RED 1 failed | `test_the_warning_quotes_the_sentence_as_the_author_wrote_it` |
| no masking at all | RED 2 failed | the fence and inline-span cases |
| the FIRST claim is named, not the nearest | RED 1 failed | `test_the_nearest_claim_is_the_one_named` |
| a number BEFORE the claim earns a warning too | RED 2 failed | `test_a_number_before_the_keyword_is_not_the_shape`, `test_the_nearest_claim_is_the_one_named` |
| an anchor is read as an issue number | RED 1 failed | `test_an_anchor_is_not_an_issue_number` |
| a claimed number is warned about | RED 3 failed | `test_a_number_the_body_claims_elsewhere_is_never_warned_about`, `test_a_second_keyword_loses_nothing`, `test_the_nearest_claim_is_the_one_named` |
| the mention list no longer excludes what was claimed | RED 4 failed | `test_the_sentence_that_lost_an_issue` and three others |
| the warning quotes the masked copy | RED 1 failed | `test_the_warning_quotes_the_sentence_as_the_author_wrote_it` |
| a step handed no body is green | RED 1 failed | `test_a_step_that_examined_nothing_is_not_green` |
| an empty body reads as no body at all | RED 1 failed | `test_an_empty_body_is_a_body` |
| the module keeps its own copy of the keyword list | RED 13 failed | thirteen of twenty-eight |

**The first run of the loop had one survivor and two untrustworthy results,
and both were the loop's own defect rather than the module's.**

The survivor was an **equivalent mutation**: deleting `m.start(1) in
claimed_at` from a condition whose other half was `m.group(1) in claimed`.
Every claimed position holds a number that is in `claimed`, so the position
test was dead beside the value test — in both places it appeared. A case
cannot be written for a branch that cannot be reached, so the redundant guard
was removed instead (`6b81d10`), and the mutation that empties the remaining
guard goes red.

The two untrustworthy results were **stale bytecode**. The loop cleared
`tests/__pycache__` and not `.github/scripts/__pycache__`, and a `.pyc` header
keys on the source mtime in **whole seconds** plus its size — so two mutations
of the same length written inside one second reuse the earlier one's
bytecode. `return 2` → `return 0` is the same length as the mutation before
it, and it reported the previous mutation's failing test. The tell was a red
case that had nothing to do with the line that had been changed. Both caches
are cleared now and `PYTHONDONTWRITEBYTECODE` is set for the run; the table
above is from the corrected loop.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `claimed_at` position guard in `read()`, in both the mention loop and the warning loop — NAME NOT IN TREE, which is the point of this row | Nowhere — it was subsumed by the value guard beside it in both places, which the mutation proved. A comment at the surviving guard records why a position test is not wanted back |
