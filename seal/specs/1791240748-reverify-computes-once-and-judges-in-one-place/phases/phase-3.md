# 1791240748-reverify-computes-once-and-judges-in-one-place — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | bd537ba8 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

The documents (S12, §14). `docs/the-evidence-ledger.md`'s fifth item and
*left*-reasons sentence; `docs/the-pact.md`'s in-place sentence, one sentence
(see `plan.md` §*Overlap with #822*); `skills/evidence-check/SKILL.md`
§*Re-verifying* re-read and edited only where false; every pin updated and
seen red with its sentence deleted or reverted. Questions Q4 decided by the
work.

## What this phase found

**The home.** The fifth item now says why one run over every ledger leaves
no citation drifted: each coordinate naming a ledger line, a citation or any
other, is hashed against the text the run will write. A self-citing release
file settles in that same run. The narrowed-run sentence is kept word for
word and extended to a non-citation coordinate (D4). A new sentence after the
list puts the row that does not settle outside the five things, because it
exits 1. The *left*-reasons sentence says the reason is the sentence
`--strict` prints for that coordinate, and *a file the run could not read*
became *a file not found*, the check's own words.

**The pact.** The in-place clause says a move is from the row's own hash to
the hash the run writes, and BROKEN at the row's own hash where the run
leaves it, because nothing is written for a coordinate left. It is one
sentence, and it carries no `signatory` word, so #822's rename of the
section does not touch the same line.

**Questions Q4, decided: `skills/evidence-check/SKILL.md` §*Re-verifying*
is left as it is.** Re-read whole at bd537ba8: it says nothing about walks,
and no sentence there is false after phase 2. The new `LEFT` line for a row
that does not settle is named in the home's paragraph, which the skill does
not restate for any other leaving of that paragraph either. #822 edits the
same section, so an edit here would buy a conflict and no correction.

**Pins, seen red.** Every changed or added pin was run against the base's
documents and docstring (the scratchpad's `git archive` of `e6d5a055`): 12
red, 20 green, and the green ones are the sentences this phase did not
change. Executed.

**Slice, executed.** `bin/test tests/test_a_released_row_is_read_again_in_a_fragment.py
tests/test_a_signatory_records_a_pact_change.py tests/test_the_ledger_rules_have_one_home.py
tests/test_a_merge_cannot_silently_drop_a_correction.py
tests/test_no_passage_is_pasted_into_a_second_file.py tests/test_docs_line_wrap.py -q`:
exit 0, 702 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the home's *because it walks a cited file before every file citing it* and *is walked again until it settles* | the same item, restated for one plan judged against the text it writes |
| the pact's *however many walks re-stamp it* and *BROKEN after it at the hash it holds where a later walk leaves it* | the same sentence, restated as before and after |
