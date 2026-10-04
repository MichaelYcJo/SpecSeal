# 1791119070-a-waiver-inside-a-here-document-body-is-data — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | d75638c7 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The records. The work item's ledger rows in
`seal/ledger/1791119070-a-waiver-inside-a-here-document-body-is-data.md`;
the re-reads of every released row phase 1's anchors moved, written by
`evidence-check --reverify --into` that fragment with `--checked 2026-10-04`
after each row was read, never re-stamped in place (the freeze is declared);
the changelog fragment; and the closing memo, whose *Not done* names the
worktree guard's read, filed as #780. Records name the mechanism and the code
coordinate, never a command string that gets past the gate. `evidence-check`
exits 0, and `tests/test_no_real_identifiers.py` and
`tests/test_one_word_one_meaning.py` pass.

## What this phase found

**31 released rows drifted, on six anchors, and the plan's list was a subset,
as it said it would be.** The anchors were `hooks/commit-review-gate.py#main`,
`#commit_invocations`, `hooks/tokens.py#given`,
`tests/test_the_old_spellings_reach_the_hook.py#test_a_token_is_a_bare_word_and_nothing_else`,
and the two policy headings. All 31 were read before the writer ran. `main`
and `commit_invocations` moved for comments alone, so every claim about what
counts as a commit, the press, the fallback and the recursion backstop holds.
E2's "that branch honours no other waiver" holds: the unreadable branch still
reads `[no-review]` alone, now outside bodies. G6 says what the carried word
waives and makes no claim about bodies. The writer folded the 31 into 15
citing rows, one per released claim. The G6 and C1 rows say what was read
rather than the writer's default sentence.

**The frame did not hold on two coordinates, and `evidence-check --strict`
exited 2 on this work item's own records.** `plan.md` §*Operational impact*
placed `classify` in `hooks/cmdline_base.py`. The tree has no `classify` there; the
only one is `hooks/worktree-guard.py#classify`. Sibling D's branch had no hook
commit to settle which one it meant. The same section wrote G6's anchor with
the hash it predicted would move, which the record check reads as a drifted
coordinate. Both were corrected in place at `d75638c7` and the sentences'
point is unchanged. The check's own text asks for the record to be corrected,
and a work item whose records keep the broad gate red cannot be sealed. The
overview's divergence row quoted the wrong coordinate in the same form, and
the check read the quote as a coordinate too. That row was reworded in the
commit that carries this record, after `d75638c7`.

**One of this phase's own coordinates was wrong before it was written.** The
W3 row first named a `test_the_waiver_can_be_typed` function, which that
module does not have. The anchor check caught it, and the row now cites
`test_an_apostrophe_beside_the_marker_does_not_silence_the_waiver`.

**The identifier checks were run on the staged tree.** They list files
through git's index, so a run before `git add` may not read a new file.
`tests/test_no_real_identifiers.py` and `tests/test_one_word_one_meaning.py`
were run again once the new records were staged, and passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
