# 1790138190-settle-leaves-twelve-directories-with-no-way-out — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | bc7a869 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

A fold is not a work item. `skills/settle/SKILL.md` gains the rule (no
directory, no routing question, `: '[no-review]';` on every commit, judged at
its pull request) and §*What a fold branch owes* loses the range-row and
*Nothing in `seal/ledger.md` moves* (`questions.md` Q3's default);
`docs/release-checklist.md` §2b; `docs/the-evidence-ledger.md`; a dated
section in `docs/one-root-by-lifetime.md` and `.ko.md`; `seal/README.md` and
`templates/seal-README.md`, byte for byte. Every pin those sentences had
moves with them —
`test_the_skill_carries_the_survivors_row_a_fold_branch_owes` among them.
Verified by the settle module's document cases,
`tests/test_first_setup_asks_once.py`, `tests/test_docs_line_wrap.py`,
`tests/test_release_hygiene.py`, `tests/test_one_word_one_meaning.py`; each
moved pin seen red with its new sentence deleted.

## What this phase found

**Every moved pin seen red** (executed, the seven documents stashed, then
restored): `6 failed` — the fold-is-not-a-work-item case, the ledger case,
both editions of the new dated-section case, the two-editions comparison,
and the checklist case. The seal README pin, added after, `2 failed` with
the two READMEs stashed.

**The two-editions pin was bounded to its own section.** It measured
everything after the 2026-09-22 heading, so any later dated section would
have been counted into that one's rows and cells. It now reads each dated
section up to the next `## ` heading and compares it with its twin, for both
sections; the English and Korean new sections hold ten cell separators each.

**The Korean edition's word for the survivor sweep is 조각 검사**, from its
own 2026-09-22 row, so the new section uses it rather than a new coinage.

**One slice failure reached a commit, and was repaired in the next one.**
`98e1183` went in with `tests/test_no_document_names_the_old_roots.py`
red, because the command that committed did not stop on the test run's exit
code: the skill spelled the marker `<!-- specs/<id> -->`, and the old-roots
check allows only the canonical `<!-- specs/<work-item-id> -->`. `bc7a869`
spells it that way; the slice was then run with its exit code read — `239
passed`, exit 0.

**`evidence-check --strict` refused two names in this work item's own
records**, which is its unreleased-record arm: `plan.md` names the pin this
phase replaced, and that line now carries `NAME NOT IN TREE` rather than a
rewrite of the approved plan; `phases/phase-5.md` had shortened a case name,
corrected to `test_this_repository_has_one_root_laid_out_by_lifetime`.

**Slice** (executed on `bc7a869`): the settle module,
`tests/test_first_setup_asks_once.py`, `tests/test_docs_line_wrap.py`,
`tests/test_release_hygiene.py`, `tests/test_one_word_one_meaning.py`,
`tests/test_no_document_names_the_old_roots.py` — `239 passed`, exit 0.
`seal/README.md` and `templates/seal-README.md`: `diff` empty.

**Rows**: `seal/ledger.md` S8/S14 on the template's heading re-read — the
switch commands and the both-places sentence are untouched — and
re-verified `b7bf099f -> eeef1c89`. `evidence-check --strict .` exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `skills/settle/SKILL.md` §*What a fold branch owes*: the `survivors.md` range-row, its `\| Range \| Grounds \|` example and the two-anchor paragraph | *No `survivors.md` row*, grounded on the sweep's exclusion (`survivor_check.py` docstring, phase 4) |
| the same section's *Nothing in `seal/ledger.md` moves* — false of both folds (Q3) | *`seal/ledger.md` changes only by removal and re-verification*, which is what `docs/the-evidence-ledger.md` now says too |
| `docs/release-checklist.md` §2b's *a `survivors.md` range-row* among what a fold owes | the same paragraph: a fold is not a work item and owes no range row |
| the 2026-09-22 design-record row *the fold of the accumulated work items is its own work item* — overturned by D1, not edited | the new dated section in both editions |
| `tests/test_settle_reads_before_it_removes.py#test_the_skill_carries_the_survivors_row_a_fold_branch_owes` | `test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row` and `test_the_skill_says_what_a_fold_does_to_the_ledger` |
