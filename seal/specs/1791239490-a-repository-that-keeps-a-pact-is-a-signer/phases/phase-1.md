# 1791239490-a-repository-that-keeps-a-pact-is-a-signer — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | d6bcdd36 |
| Ran by | unknown — the spawn prompt named no agent or model, and this record is not where a segment names itself |

## What this phase was asked

The readers, the printed lines, the tests and the policy (`plan.md` phase 1).
`hooks/config.py`: `SIGNER_HEADER`, `pact_signers` reading `Signer` and then
the old header and returning which it read, `pact_reviews` the same, `_signer`,
the old tuple and the rename sentence in one unit. `pact_check.py` printing the
rename line in no exit class and `N of M signer(s) read`; `chain_check.py`
counting `signers` and appending the sentence where the header was old; every
comment in the four scripts. The four test files moved with `git mv`, the
fifteen functions renamed, every fixture header `Signer` but the compatibility
cases, new cases S1, S2, S4, S5 and S6's old header seen red first.
`templates/pact.md` and `templates/pact-review.md` begin with `Signer`.
`docs/the-pact.md` whole, with the new statement in fold shape under this work
item's marker. The spawn prompt added that `questions.md` W1 and W2 are the
work's to decide and record, and that nobody answers a question mid-run.

## What this phase found

- **W1 is a tuple.** `pact_signers` and `pact_reviews` return `(…, refusals,
  header)`, where `header` is the tuple read (`SIGNER_HEADER`,
  `PACT_REVIEW_HEADER` or the old one) or `None` where the text holds
  neither. Both go through one new unit, `hooks/config.py#read_table`, which
  tries the new header and falls back only on the `holds no ` refusal, so a
  `Signer` table that will not read is refused as it stands. The old header
  and the sentence live in `hooks/config.py#renamed_header`, and the old
  tuple is derived there from the new one, so the word is written once. Phase
  2's sweep excludes that unit by name.
- **S4 needs a heading between the two tables.** A `| Signatory |` table
  written directly below a `| Signer |` one, with no heading between, is not
  ignored: `gfm_table` refuses any `| … |` line past the table's end and
  before the next heading as a row the walk never reaches. That is the walk's
  rule since #735 and this work does not move it. The S4 case pins all three
  shapes: old table under its own heading below (read from `Signer`), old
  table above (read from `Signer`), and old table directly below (refused).
- **`pact-check`'s own sentences about the pact's table name the header the
  pact holds**, `the \`Signatory\` table lists every OTHER signer`, so the
  person told to edit the table finds it. `pact_reviews` in `pact_check.py`
  takes `(signers, table)` and `(found, say)` to carry that and the rename
  line.
- **`chain-check`'s notice** appends `. The pact heads its table …` to the
  sentence it already prints; `PACT_NOT_HERE` ends without a period, so the
  appended sentence supplies one.
- **`tests/test_one_word_one_meaning.py` moved in this phase, not phase 2,
  for its identifiers and the pinned sentence only.** `PACT_PRINTED` named
  `pact_signatories` and `_signatory`, which this phase removed, and the · NAME NOT IN TREE
  pinned definition sentence is the one `docs/the-pact.md` changed here.
  Leaving them for phase 2 would have committed a red module. The sweep
  itself is phase 2's.
- **Two printed lines the frame did not list changed**: `evidence_check.py`'s
  two vendored-copy `LEFT` lines end `where the signer is checked out`. Each
  is now pinned whole in `tests/test_a_signer_records_a_pact_change.py`
  (§14).
- **M2: `fold-check` accepts the new statement.**
  `tests/test_a_folded_statement_names_what_enforces_it.py` passed in this
  phase's slice run with the statement and its four targets in place.
- **The corpus counts did not move.** `test_the_corpus_is_counted` still
  reads 5454 / 5455 / 5455 with the walker's fixtures headed `Signer`.

Seen red, each through `bin/mutation-check` on the committed tree at
`d6bcdd36` (verdict `red` every time):

| Mutation | Cases that went red |
|---|---|
| `read_table` never tries the old header (`old = None`) | the S2, S5 and walker old-header cases and both CI old-header cases, 12 in all |
| `SIGNER_HEADER = ("Signatory",)`, the pre-change reader | `test_s1_a_pact_headed_signer_reads_with_no_word_of_a_rename` |
| `read_table` always falls back | both S4 cases |
| `word = "Signer"` in `pact_signers` | `test_s2_every_refusal_under_the_old_header_names_it` |
| `chain_check.py` never appends the sentence | both `test_a_pact_headed_as_0_18_wrote_it_is_counted_and_the_rename_named` cases |
| the summary's plural dropped | `test_s7_the_summary_counts_two_signers` |
| `pact_check.py#renamed` prints nothing | the S2 pact case and both S5 cases |
| `pact_check.py`'s table name fixed at `Signer` | `test_s2_a_refusal_naming_the_table_names_the_header_the_pact_holds` |
| the review record's `renamed` call removed | both S5 cases |
| the two `LEFT` lines saying the old word | `test_a_vendored_copy_says_it_recorded_nothing`, all five `test_a_vendored_copy_under_a_notify_row_…` cases |
| `RENAMED_IN` not used in the sentence | `test_s2_a_pact_headed_as_0_18_wrote_it_reads_the_same_and_names_it` |

S8 (the template begins `Signer`) was seen red by the slice run itself, before
`templates/pact.md` was edited: `test_a_pact_with_no_table_or_an_unfilled_one_is_refused`
failed on `header == ("Signer",)`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/config.py#pact_signatories`, `SIGNATORY_HEADER`, `_signatory` | `#pact_signers`, `SIGNER_HEADER`, `#_signer`; the released ledger rows citing the first are re-pointed in phase 3 · NAME NOT IN TREE |
| the four `tests/test_a_signatory*.py` / `…_of_the_signatory.py` file names and the fifteen function names | the renamed files and functions; every `docs/the-pact.md` `Enforced by:` line follows in this commit, and the released ledger rows citing them are re-pointed in phase 3 |
| three `docs/the-pact.md` headings with the old word | the renamed headings; released rows citing them, phase 3 |
