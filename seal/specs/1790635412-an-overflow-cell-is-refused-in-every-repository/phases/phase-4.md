# 1790635412-an-overflow-cell-is-refused-in-every-repository — phase 4

<!-- seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 2f572f41 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s Phase 4, the ledger stays true.
`seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md`
holds the new claims: the arm and its reading, the advisor, and the two
rewritten claims C2 and L1 carried. Every row `evidence-check` reports
drifted by this branch is re-read in the file it stands in and gets a dated
note, or `Corrected <date>` where the edit made it false; hashes follow the
hazard rule in `plan.md`. The changelog fragment is complete.
`survivor-check` over the branch, with a `survivors.md` row for each
released text it reports. The spawn prompt added: fragments, never the
shared file.

## What this phase found

- **Q3, measured.** The unscoped lenient run after phase 3 named 36 drifted
  coordinates, all anchors this branch's diff touched, in 28 rows of 11
  release files: `0.4.0`, `0.5.0`, `0.8.0`, `0.8.3`, `0.9.0`, `0.11.3`,
  `0.14.0`, `0.15.1`, `0.15.3`, `0.15.4` and `0.15.5`. Two claims were made
  false and were corrected in place before the note: `0.11.3.md` row 23 and
  `0.15.5.md` S4 both quoted the notice's verdict list as `DRIFTED` and
  `MALFORMED`, and the notice names `OVERFLOW` too. The other 26 hold; each
  note says what the edit changed and why the claim still stands. Each row's
  `Checked` is today's date, appended after a `·` where the cell already
  held several.
- **The hazard rule held without hand-written hashes.** Every drifted row in
  those 11 files was one re-read here, so `--reverify` narrowed to exactly
  them rewrote 41 hashes (some coordinates stand twice in one file) and
  touched nothing else. The fragment was stamped the same way, alone.
- **One drift was a chain.** `0.13.1.md` row 66 anchors the section of
  `0.4.0.md` headed `1788331011-two-roots-hold-three-lifetimes`, and this
  phase's note on row 281 of that section changed it. 1790562543 met the
  same chain on 2026-09-28 and answered it with a re-read note; this one
  does the same, then re-stamps that file alone, where it was the only
  drift.
- **The records arm refused one line of the frame.** Once the fragment
  existed, `plan.md`'s *Alternatives* row naming the old case's walk was
  `NOT-IN-TREE`: the plan says the lines naming phase 3's removals carry the
  marker, and that one did not. It carries it now (`overview.md`).
- **The unscoped runs.** `bin/evidence-check .`: exit 0, `total: 2661 ok ·
  0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed · 0
  overflow`, and the records arm `1 work item read ... 0 refused`.
  `bin/evidence-check --strict .`: exit 0, the same totals.
- **Q4, measured.** `survivor-check --range a7f146a8..HEAD` reported nine
  places. Six are records of shipped or framing work quoting what they were
  written against, one is a dated note in a released row, and two are still
  true; each has a row in `survivors.md` with a quote and its grounds, and
  the run with `--exempt` exits 0, "every survivor is excused by a row above
  (9)". None of them presents the old enforcement as current, so nothing was
  corrected.
- **Narrow runs.** `bin/test tests/test_the_ledger_fragments_fold_at_release.py
  tests/test_a_record_states_what_the_tree_has.py
  tests/test_chain_hooks_hardening.py tests/test_release_hygiene.py
  tests/test_unverified_rows_close.py
  tests/test_a_merge_cannot_silently_drop_a_correction.py
  tests/test_a_corrected_sentence_survives_elsewhere.py
  tests/test_docs_line_wrap.py`: 650 passed. `bin/unverified-check .`:
  exit 0, this work item's memo `4 open · 0 closed`.
  `bin/correction-check --range a7f146a8...HEAD`: exit 0, no merge in the
  range.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
