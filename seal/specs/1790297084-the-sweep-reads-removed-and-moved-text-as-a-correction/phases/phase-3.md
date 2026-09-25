# 1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 9bb204df |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#603, the last of three phases. A predicate, named by the builder and a
`def` so `Enforced by:` can name it, returns the ledger rows a range removed.
A row qualifies when it is a live table row at `a` in a ledger path shape,
its line is not in that file at `b`, and at least one `ANCHOR_RE` anchor in
it resolves at `a` and not at `b` through `resolve_unit`. `evidence_check.py`
is read and never edited on this branch, because work item E edits it in
parallel. It is loaded by path only when the range holds a ledger path, and
a missing sibling is exit 2 with a sentence. `corrected` drops those rows'
departures after the pairing, beside phase 2's drop. The module docstring's
§*What is excluded* gains the paragraph. `docs/review-chain-spec.md`'s
first statement gains the clause, and its `Enforced by:` line the predicate.
One changelog fragment covers all three issues. Verified by spec S7–S13, a
case holding the four path shapes against `default_patterns`, a case for the
missing-sibling refusal, the whole module green, `RELEASE_RANGES` re-run
(Q1), Q2's squashes measured at the base and at this phase, `bin/evidence-check`
clean with drifted rows re-read, and `bin/fold-check` clean.

## What this phase found

- **The frame's three conditions let a corrected row go silent, measured on
  #589's squash (Q2).** `16b77284` corrected `seal/releases/0.15.1.md` R1 in
  place, and in the same commit renamed one of the tests the row cites. The
  old name resolved at `a` and not at `b`, so under conditions (a) to (c)
  the corrected claim took the exit. `spec.md` judgment 1 rests on a row
  corrected in place keeping its anchors, and this row did not. Nothing was
  reported on that range before or after: 0 places both ways, and the
  removed count fell from 73 to 70. But the direction was the silent one,
  which judgment 1 exists to avoid.
- **So the predicate has a fourth condition, which `plan.md` does not
  name.** A row that a live row of the same file at `b` still cites by every
  anchor that resolves there still stands, re-pointed, and stays measured.
  Measured over the six 0.15.3 squashes before it was written: it named
  #589's R1 and none of #587's three rows. Those three kept 4, 4 and 1 live
  anchors, and no row at `b` cited all of any one row's live anchors. It only
  keeps rows measured, so it moves toward reporting. A reviewer may overturn
  it: without it, the corrected row on #589 goes silent again.
  `test_a_row_corrected_in_place_while_an_anchor_is_renamed_is_a_correction`
  pins it. It was red at `afb03a4c` (exit 0).
  `test_a_removed_row_sharing_one_live_anchor_with_another_row_takes_the_exit`
  pins "every anchor" against "any anchor".
- **Red first, executed at `4910e445`.** The removed-row case and the
  one-anchor case exited 1. `58629718^..58629718` exited 1 with 8 places
  against 98 removed sentences, which is the framer's measurement. The shapes
  case, the refusal case and the line-base case failed because the units did
  not exist yet. The corrected-in-place case, the both-anchors-standing case,
  the fence and comment cases and the fragment-carry case were green there,
  as the spec says. Each is shown red by a mutation below.
- **Mutations: thirteen, run one at a time over sixteen cases, the file
  restored from a copy after each.** Every mutation turned at least one case
  red:
  - every removed row line exiting;
  - the standing-line test, the live-line test, and each half of the anchor
    condition, each taken out;
  - "every live anchor" read as "any", the still-standing test taken out,
    and the empty-set guard taken out;
  - lines counted from 0;
  - the drop moved before the pairing;
  - the releases shape taken out;
  - the refusal taken out.

  "Every anchor must leave" first went green, because the mutation was
  written wrong. Rewritten as `not live`, it turned three cases red.
- **Two conditions had nothing behind them until a case was added.** The
  first run of mutations left the standing-line test and the left-end half
  of the anchor condition green. Each got a case:
  - a row that stood twice and lost one copy;
  - a row anchored on a path this repository never held, a cross-repository
    row.

  The duplicate-row case at first scored under the floor. The standing copy
  is a second carrier of every phrase, so it needs `MORE_FILLER`'s pool, as
  #563's two-copy cases do. That was a fixture fault, recorded in its
  docstring.
- **The line base holds.** `removed_ledger_rows` counts from 1, and the
  sentences `segments` reads from a table row carry the same number.
  `test_a_removed_rows_cells_are_the_lines_the_row_stood_on` holds the two
  against each other. It goes red when the count starts at 0.
- **Q1 at this phase: unchanged.** `RELEASE_RANGES` passed unedited. None
  of the four ranges removed a ledger row that qualifies.
- **Q2, executed.** Each 0.15.3 squash was run with the base's scripts,
  extracted from `2e0e2fa7` into scratch, and with the final script. The
  table is in `questions.md`. #587 goes from 8 places to 0, and every other
  squash reports what it reported at the base. #593's report is the same
  places, sources and scores, with one block in a different position among
  entries tied at 1.77. `score` iterates a `set` of strings, so the order of
  tied entries follows Python's hash seed and was never stable. That
  predates this work.
- **Q3 at this phase: 2 more lines, 6 in all.** The document has 968 of its
  1000 lines. The first statement's `Enforced by:` line names
  `removed_ledger_rows`. `bin/fold-check` exits 0.
- **The narrow run.** Every module that names a file this branch changed was
  run: the readers of `docs/review-chain-spec.md` and `survivor_check.py`,
  and the readers of ledger files, changelog fragments, memos and phase
  records. That is 52 modules at `9bb204df`: 2440 passed, 1 skipped, 0
  failed. The modules that read records were run again after this record
  and the memo were written. `ruff check` and `ruff format --check` are
  clean on both Python files.
- **The ledger.** Row S3 in `seal/releases/0.9.3.md` defines when a sentence
  is corrected, and named the move as its one exception. It was corrected in
  place with a `Corrected 2026-09-25` note that names the second exception.
  The other rows anchored on `corrected` were re-read and re-stamped.
- **CONTRIBUTING's four items.** Red test: above. Failure direction: reports
  less, for rows whose anchor left and that nothing at `b` still cites. A
  row retracted as false in a range that happens to remove one of its
  anchors goes silent. The ledger's rules route a false claim to correction
  in place instead, and the fourth condition keeps that path measured even
  when an anchor is renamed. Prompt budget: 0. Platform: pure text over git
  blobs, with paths from git with `/`. `resolve_unit` is the checker's own
  code, and it runs on every OS the checker does.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
