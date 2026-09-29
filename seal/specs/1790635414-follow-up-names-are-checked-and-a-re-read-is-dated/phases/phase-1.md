# 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated — phase 1

<!-- seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 18ac24e9 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 1 on a branch where the rebase was already done as a
merge of `release/v0.16.0` at `3911a8cf` (work item A's squash, #585) at
`56e53c90`. What was left of the phase: re-read A's diff to
`evidence_check.py` for Q2 and every coordinate in *Technical context*; write
the fragment's first row so the arm reads this work item's records from the
start; F1–F8, which are the follow-up read before the early return, the file
out of the corpus in both walks, `UNREADABLE`, and the heading, summary line
and refusal detail; D2's lines about `seal/follow-up.md`; and Q1 measured on
the merged tree.

## What this phase found

- **The frame holds, with one stale name and one stale fact.**
  - *Technical context* says `grounds_cells` follows "the same five-column
    rule for a row under no header that `tests/test_release_hygiene.py`'s
    `overwide_rows` counts against". A's squash removed that function · NAME NOT IN TREE
    (`tests/test_release_hygiene.py` now reads the shipped arm through
    `overflowing_rows`), and the rule lives in `evidence_check.py`'s
    `overflow_rows` against `LEDGER_COLUMNS`. The plan line is a
    coordinate-form name the phase 2 reader will refuse, so it is corrected
    in phase 2's commit, with the reader that refuses it.
  - M1 ("`seal/ledger/` does not exist … 0 live") stopped being true at the
    merge: A's fragment is on disk, so A's records are read. The plan already
    expected this, which is why Q1 re-measures.
  - The RIDER on `reverify` is still there. A re-stamped it
    (`Verified 2026-09-29 against reverify@69267bf1`, where the plan quotes
    the 2026-09-25 stamp); its text is unchanged.
- **Q2 is answered by A's diff: reuse.** A moved the table walk out of
  `grounds_cells` into `ledger_table_rows`, which yields
  `(line_number, header, cells)` for every body row, through `unquoted` and
  `gfm_lines`, with `header` None under no header. That is the row reader
  phase 3's date-cell finder needs, and the line number is the splice point's
  line, so there is no second reader beside `grounds_cells`.
- **One reader for a record and the follow-up file.** The per-file loop of
  `check_records` became `file_claims`, and the follow-up path is appended to
  the list of files it reads. A second loop for the follow-up would have been
  the place where the two come apart.
- **`lexists`, not `isfile`, decides whether the file is there.** A directory
  or a dangling link under that name is there and unreadable, which is
  `UNREADABLE` and exit 2; absent is the only quiet answer. The case builds a
  directory under the name rather than refusing the read, because the read
  is not what distinguishes the two.
- **The heading is a constant and cannot say "was read" per run.** It names
  `seal/follow-up.md` as part of what the arm reads; the summary line is what
  says what happened: `seal/follow-up.md read`, `no seal/follow-up.md`, or
  `seal/follow-up.md unreadable`. The state goes at the END of the line, so
  the pinned prefix `N work items read · M unread · K names read` every
  existing reader matches is unchanged.
- **Q1 at the end of phase 1: 0 refused.** `bin/evidence-check .` on
  `18ac24e9`: `2 work items read · 24 unread · 278 names read · 0 stamps read
  · 0 refused · 0 drifted · 0 external · seal/follow-up.md read`. The same
  run before the change read 270 names, so the file contributes 8, all of
  them names the tree carries. The ledger arm's six DRIFTED rows are this
  phase's own edits (`main` four times, `tree_names`, `check_records`), and
  phase 4 re-reads and re-stamps them.
- **How each case was seen red.** The base checker was extracted with
  `git archive 56e53c90 skills hooks` into the scratchpad, and a probe pytest
  plugin rebound the module's `SCRIPT` to it: 9 of the 14 new cases failed.
  The other 5 are the not-read direction (no file, and four claim-rule
  exemptions), which pass on a checker that reads nothing; each was shown red
  by a mutant instead. Six mutants over the new units, each restored with
  `git diff` empty afterwards: the corpus skip removed (5 red), an absent file
  read as present (2), the refusal naming `seal/ledger` twice (1), an
  unreadable file said as read (1), an absent file said as read (1), and names
  read past `claim_lines` (the four exemptions red).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the per-file loop body inside `check_records` | `file_claims`, which both the records and the follow-up file go through |
| the refusal detail naming two places the corpus leaves out | `left_out_of_corpus`, which names all three |
