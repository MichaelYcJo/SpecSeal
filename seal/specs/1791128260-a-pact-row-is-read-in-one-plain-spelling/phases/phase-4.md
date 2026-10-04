# 1791128260-a-pact-row-is-read-in-one-plain-spelling — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | bc2cd870 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The documents and the ledger. A new marked paragraph in `docs/the-pact.md`
§*How a signatory names the pact* with its `Enforced by:` line; the vendored
paragraph's rule and the blind side in §*What this does not see* (Q1 default
(a), no code); `templates/config.md` §*Pact*'s refused-row paragraph and the
`Absent` cell of `Pact notify`. A pin per sentence, each seen red with the
sentence deleted (S12). The released rows this item drifts re-read with
`evidence-check --reverify --into seal/ledger/<id>.md --checked 2026-10-05`,
and a `Corrected ·` row for 0.18.1 C1, whose `NOTIFY_ROW_SHAPE` coordinate
went BROKEN. The changelog fragment. Sibling E owns `docs/the-pact.md`
§*A signatory records a pact change* and the template's "Pact notify decides"
paragraph, so this phase stays out of both.

## What this phase found

**`evidence-check` named eleven released rows whose coordinates this item
moved**: 0.12.0:105 and 0.9.1:120 (`config_rows`), 0.5.0:107 (S8, the
template's first table), 0.18.0:6, :8 and :79, and 0.18.1:168, :170, :174,
:175 and :415. Framing's list was what it saw, and the run's is the set. Each
claim was read against the code before the run. Ten hold and were written as
`Re-read ·` rows, three of them with a note on how they hold now.

**0.18.1 C1 is corrected, not re-read.** Its `NOTIFY_ROW_SHAPE` coordinate is
BROKEN, and its vendored clause also stopped being true: it said the copy
found a row shape line by line as `str.splitlines` cuts the file. The
`--reverify` run left the row with the repair it prints and also wrote a
`Re-read · C1` row saying the claim holds. That row was replaced by a
`Corrected · C1` row carrying the claim as it now reads and every coordinate
it still rests on at its current hash (`NOTIFY_ROW_SHAPE` dropped,
`PACT_WORD`, `names_a_pact`, `notify_may_be_always` and three new cases
added). O1–O3 are this item's own claims.

**The evidence-check skill carried the vendored rule too.**
`skills/evidence-check/SKILL.md` §*Re-verifying is recomputing the hash*
stated the old rule, which this item made incomplete, so it gained the
refused-line clause. Its first wording repeated the doc's, and
`test_no_passage_is_pasted_into_a_second_file` measured the pair at 24 shared
runs against a baseline of 21. The skill's sentence is worded apart instead,
and the existing pins on both sentences
(`test_the_documents_say_what_the_writer_does`) follow them.

**`evidence-check --strict` refused seven record lines** that name #784's
units on purpose (#784's refusal renderer, its shape constant and line
shaper, its raw-HTML pattern and its item lookups) and one framing stamp in `spec.md` that the
template's edit moved. Each named line carries `NAME NOT IN TREE`, and the
stamp is written without the stamp form, keeping the hash framing saw. After
that the check exits 0.

**`tests/test_chain_hooks_hardening.py` wants the closing memo** once a work
item has a `spec.md`. `overview.md` is written at this phase's close.

**Seen red (§15).** Each of the eleven pinned sentences, the nine new pins
and the two moved vendored pins, was deleted once under `mutation-check`,
and its pin went red each time. The blind-side case went red, 6 of 8, with
`PACT_WORD` widened to let letters stand between the word's letters.

**The boundary run.** Nineteen modules at `bc2cd870` (the four pact modules,
the census, the S11 modules, the record and ledger checks and the docs
hygiene modules): 3,456 passed, and one failed on this record's own draft,
which then named #784's units in backticks; reworded, that module passes
(101). `ruff check` and `ruff format --check` are clean on the seven touched
Python files, `evidence-check --strict .` exits 0, and `survivor-check
--range 94d7b2e0..bc2cd870` reports no removed wording still standing.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The vendored sentence's old rule in `docs/the-pact.md` and `skills/evidence-check/SKILL.md` | the same sentences, reworded, and the `Corrected · C1` row in this item's ledger fragment |
