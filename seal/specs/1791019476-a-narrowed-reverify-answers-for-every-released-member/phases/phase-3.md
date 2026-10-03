# 1791019476-a-narrowed-reverify-answers-for-every-released-member — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | e7c09bf7 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Make the ledger true under the freeze. Correct L4 in
`seal/ledger/1790993138-….md` in place with a `Corrected <date>` note: the
deferred clause goes, and the claim says what D1 and D4 do. Write N1 and N2
into `seal/ledger/1791019476-….md`. Read every row citing a drifted
coordinate, then run `evidence-check --reverify --into <this work item's
fragment> --checked <date>`. Then run `bin/survivor-check --range
2b1dcb1f...HEAD` and judge anything it keeps in `survivors.md`. Answer W2.
The parallel integration branch re-stamps rows in #736's fragment; build on
the base until told to merge `origin/release/v0.18.0` in, and never edit a
released file.

## What this phase found

**W2, answered by the work: the edits drifted 15 coordinates on 10 rows of
#736's fragment, and 6 released rows, all through that fragment.** Read off
`evidence-check --strict .` after phases 1 and 2:

- `#main` on L4 and on the `Re-read ·` rows at lines 15, 17, 26, 30 and 32,
  which re-read the released rows in `0.16.0.md` (two), `0.4.0.md`,
  `0.8.3.md` and `0.9.0.md`. The spec's ceiling was six in the fragment and
  five released; the sixth fragment row is the `Corrected ·` row at line 25,
  which cites `#main` too.
- `#family_view` on L1 and on line 25; `#released_drift` and
  `#reverify_into` on L4.
- the home's section on L9 and on line 57.

The released rows came back DRIFTED only as families of two, each with its
`Re-read ·` row in #736's fragment. Re-stamping that row in place gives the
family its newest reading again, so `--into` owed no `Re-read ·` row:
`0 citing rows written · 0 released rows left`. This work item's fragment
holds N1 and N2 alone. The 0.18.0 fold has not landed, so L4 is still a
fragment row and was corrected in place.

**Each row was read against the edit before the re-stamp (read).** The
claims citing `#main` are about `OVERFLOW`'s grading, `--checked`'s
refusal, `display_name`, the records arm and a fix-pass close in 0.4.0.
#740's edit to `main` touches the freeze branch's argument and a comment,
so each still holds. L1 and line 25 hold: the family rule and the
de-duplication are unchanged, and the new `reading` helper changes words
only. L9 and line 57 hold: the two sentences added to the home state no
rule a carrier must not restate.

**The rows the four squashed items drifted in each other were left as the
base has them.** `--reverify` narrowed to #736's fragment also rewrote seven
hashes the integration branch's `bb2f3400` writes: the citations at lines
12, 18, 29, 30, 45 and 60, and `templates/config.md` at line 29. Each
value it wrote matched `bb2f3400`'s. They were set back to the base, because
this work did not read those rows and the integration branch did. So
`evidence-check --strict .` still reads 9 drifted, exit 2: those seven, the
`templates/config.md` reading of the `0.5.0.md` row line 29 re-reads, and
`docs/branch-and-release.md` in #733's fragment. All nine are the
integration branch's, and the merge of `origin/release/v0.18.0` clears
them. S8's "0 drifted" holds only after that merge. Lines 29 and 30, and
17 and 18, are adjacent edits on the two sides, so that merge will conflict
there. Each conflict is resolved by reading both sides: the integration
branch's citation hash and this branch's `#main` hash.

**Executed at this commit:**

- `evidence-check --strict .`: 4,017 ok, 9 drifted, exit 2, the nine above.
  The records arm refuses 4 lines, all in `1790993137`'s records (phase 1).
- `git diff --name-only 2b1dcb1f...HEAD -- seal/releases seal/ledger.md`:
  empty.
- `correction-check --range 2b1dcb1f...HEAD`: no merge commit, and no
  released ledger file changed.
- `survivor-check --range 2b1dcb1f...HEAD`: 675 files examined against 22
  removed sentences, and no removed wording is still standing. No
  `survivors.md` was needed.
- `bin/test` over `test_no_real_identifiers.py`, `test_release_hygiene.py`,
  `test_a_script_says_which_interpreter_it_needs.py`,
  `test_one_word_one_meaning.py`, `test_the_ledger_fragments_fold_at_release.py`,
  `test_a_merge_cannot_silently_drop_a_correction.py`,
  `test_a_record_states_what_the_tree_has.py` and
  `test_chain_hooks_hardening.py`: 394 passed, 1 failed, the base failure
  phase 1 records.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| L4's clause saying a narrowing that reads only another member of the family answers nothing and exits 0, deferred | L4's rewritten claim and its `Corrected 2026-10-03` note, and N1 |
