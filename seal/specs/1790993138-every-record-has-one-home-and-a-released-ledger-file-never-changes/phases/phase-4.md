# 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 28851fb3 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The fold and `settle` (D6): `--split` removed with its cases, `--version`
older than the newest release file refused, the fold-branch fragment
`seal/ledger/<unix-seconds>-fold.md`, `skills/settle/SKILL.md` §*What a fold
branch owes*, `settle.py`'s per-row guidance, and `docs/release-checklist.md`
§2's `--split` lines and paragraph. Scenario S11 and measurement M1, with
`tests/test_the_ledger_fragments_fold_at_release.py` and
`tests/test_settle_reads_before_it_removes.py` run, the refusal red first,
and M1's probe answer recorded here.

## What this phase found

**The frame holds, and one consequence it did not state is built.** D6 asks
for `settle.py`'s guidance to become *write a `Corrected ·` row, never remove
the row*. `settle --retire` keeps a directory while any ledger row anchors
into it, and reads every line to decide, so a released row answered that way
would still hold its directory forever. `anchored_rows` now asks the
checker's `family_view` which rows a correction supersedes and skips them:
the checker no longer reads such a row's anchor, so the removal breaks
nothing. The new verdict, `released`, applies only where `seal/config.md`
declares the freeze and the row sits in a released file; a repository
without the row keeps REMOVED and narrow, and the existing case for that
(`test_a_row_anchored_inside_a_candidate_keeps_that_directory`) is
unchanged.

**What `--split` left behind.** Its four units (`split`, `release_sections`,
`body_rows`, `rewrite_self_anchors`), `SELF_ANCHOR_RE`, the option, and the
twelve cases between its heading and *the checker cannot tell*. Two other
places named it: `fold_ledger.py#version_headings`' docstring and a bullet in
`unverified_check.py#fence_opener`'s list of fence walks, which named three
of the removed units; both are corrected. `--check`'s repair for a release
heading left in `seal/ledger.md` now says to move the section into its
release's file in the change that wrote it. `CONTRIBUTING.md`'s `--split`
lines are phase 6's, which edits that file for the rule move.

**A shipped script runs under Python 3.9.** `settle.py` notes that every
shipped script is measured to compile under 3.9; phase 3's
`zip(..., strict=True)` in `correction_check.py` compiles there and raises
at runtime, so the loop was rewritten without it. The new code in
`evidence_check.py`, `correction_check.py` and `settle.py` uses nothing newer.

**M1, answered: yes.** Executed with a one-time probe (`tests/test_tmp_*`,
deleted): a tree with `seal/ledger/1790000000-fold.md` and no matching
`seal/specs/` directory. `fold_ledger.py --version` folded it under `###
1790000000-fold` and `--check` exited 0; `settle`'s report and `--retire`
named nothing about it; `evidence-check --strict` exited 0 over a plain row
in it (`1 unread` is the fixture's directory with no fragment), and its
records arm skips an id with no directory by design
(`evidence_check.py#unshipped`). Read: `unverified-check --baseline` and
`chain-check` open no fragment at all — `folded_items` reads only top-level
`docs/` markers, and `chain_check.py` names no `seal/ledger` path — so
neither can refuse one. The fold fragment is kept as D6 names it.

**M3 for phase 4 (executed): 27 released rows**, 18 drifted and 2 BROKEN
rows (P1 and P2 of `0.15.1`, nine coordinates on the removed units and
cases). Each was read. Seven claims are false now, and each took a
`Corrected ·` row citing it: G3's two-verdict list and D1's *only by removal
and re-verification* of `0.14.0`; F2, D1, C1, P1 and P2 of `0.15.1`, the last
three with the citation alone, because their subject went with `--split`.
The other thirteen still hold, and `--reverify --into` wrote them, exit 0;
G3's `anchored_rows` row says the guard now skips a superseded row.
`--strict .`: exit 0.

**Seen red (§15).** Before the code: 3 failed (the `--split` option, the
older-version refusal, the repair text) and the two settle cases. The join
case and the fold-fragment case passed, because #540's join is unchanged and
the fold already accepts any fragment — the second is M1's first answer.
Breaks with `mutation-check`, 8: the older-version refusal, `<` against
`<=`, the repair text, the `released` verdict, the superseded skip, the
freeze condition and the file kinds, and the skill's pinned sentence. The
repair text survived its first break, because the refusal's heading line
already carried `seal/releases/<X.Y.Z>.md`; the case now asserts the
repair's own words and went red.

**Narrow runs (executed).** The 64 modules naming `fold_ledger`, `settle`,
`release-checklist`, `unverified_check` or `correction_check`: 3,377 passed,
7 skipped, 1 failed, `test_the_skill_says_what_a_fold_does_to_the_ledger`,
which pinned the sentence D6 replaces. Moved to the two halves the skill now
states, and seen red with the new sentence replaced. Its policy half,
`docs/the-evidence-ledger.md`'s *A fold is not a work item, and it adds
nothing to the ledger*, is phase 6's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `fold_ledger.py --split` and `#split`, `#release_sections`, `#body_rows`, `#rewrite_self_anchors`, `SELF_ANCHOR_RE` | nowhere: the one-time move ran at 0.15.1's preparation; `fold_ledger.py`'s docstring and `docs/release-checklist.md` §2 say so |
| the twelve `--split` cases of `tests/test_the_ledger_fragments_fold_at_release.py` | nowhere: they held the removed units; `test_split_is_no_longer_an_option` holds the removal |
| the release checklist's before-and-after readings around `--split` (§2's block, §3's paragraph) | nowhere: they were that release's |
| *a fold changes a released ledger file only by removal and re-verification*, as the whole rule | `skills/settle/SKILL.md` §*What a fold branch owes*, now in two halves; the policy half is phase 6's |
