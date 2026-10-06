# 1791240748-reverify-computes-once-and-judges-in-one-place — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 047eac5d |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

The records (D6 probe 3, D7, S13–S15). `survivor-check --range
e6d5a055..HEAD` with a `survivors.md` row per place that stays true. This
item's fragment through `bin/evidence-check --reverify --into
seal/ledger/<this id>.md --checked <date>`, each cited claim read before the
date is typed; the same run through the base script in a scratch copy, the
two fragments and outputs diffed and classified. The `Corrected ·` rows of
D7. The `changelog.md` fragment. Questions Q3 measured.

## What this phase found

**D6 probe 3, executed.** `--reverify --into seal/ledger/<this id>.md
--checked 2026-10-06` over this repository at `1f4d6cfc`, the base script
in one `git archive` copy and this branch's in another: both exit 1, 18.7 s
each. The two fragments are byte-identical, 46 rows. Stdout differs in one
line's position: the `LEFT` line for `0.18.1.md:417`'s `current_hash`,
which `released_drift` orders by `str(file_identity)`, that is by inode,
and the copies' inodes differ. A copy's artefact, as probe 2's first version
found; unexplained: 0. The same command in the worktree wrote the same bytes
as the second copy.

**Questions Q3, measured.** The re-read owes 46 released rows: 46 `Re-read ·`
rows written, 12 BROKEN coordinates left on 6 of those rows. Of the rows it
re-read, 16 carry a drifted `reverify`, 10 `main`, 7 `classify` and 6
`reverify_into`; none carries a drifted `check_text`, `family_view` or
`released_drift`, which this item did not edit. 11 rows cite the home's
section and 2 the pact's.

**The 46 claims were read before the date was typed.** 38 hold at this tree
and kept their `Re-read ·` row. Eight do not, or rest on a removed unit, and
their `Re-read ·` rows were replaced by `Corrected ·` rows carrying every
coordinate the claim rests on: `0.18.1:417` (`current_hash`), `0.18.2:86`
(E3, the walk), `:87` (E4, the move-then-BROKEN fold), `:90` (a renamed
case and `cited_first`), `0.18.3:6` (A1, the held coordinate's own reading
and `left_because`), `:8` (A3, `walked_outcome`), `:10` (A5, a docstring
sentence phase 2 rewrote) and `0.4.0:59` (round 6's rule, narrowed to a row
with no claim). `0.18.0:24` takes none: `0.18.1:417` already supersedes it.
The `Corrected ·` rows were written with placeholder hashes and a second
`--reverify --into` re-stamped them in the fragment, in place: 103
coordinates, 0 citing rows written, 0 released rows left, exit 0.

**Survivors, executed.** `survivor-check --range e6d5a055..1f4d6cfc` named 50
places; each is excused by a row of `survivors.md` with a quote and its
grounds, and the re-run says *every survivor is excused by a row above
(50)*. They are other work items' records, released rows (three of them
corrected above), and sentences this range wrote or kept that are true.

**The records arm read this item's own records.** `--strict` refused 25
names its records carry and the tree no longer does:
`first_old`, `walked_move` and `owed_moves` (NAME NOT IN TREE). Each line now carries the
`NAME NOT IN TREE` marker, `spec.md`'s and `plan.md`'s lines included,
which is the remedy the refusal names.

**Checks, executed.** `bin/evidence-check --strict .`: exit 0, `6054 ok · 0
drifted · 0 broken`, `0 refused`. `bin/test tests/test_no_real_identifiers.py
tests/test_one_word_one_meaning.py tests/test_a_folded_statement_names_what_enforces_it.py
tests/test_the_ledger_fragments_fold_at_release.py
tests/test_no_passage_is_pasted_into_a_second_file.py tests/test_docs_line_wrap.py -q`:
exit 0, 171 passed. `bin/unverified-check` over `overview.md`: exit 0, 3 open
items, each with its answerer.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase wrote records and removed nothing from the tree | none |
