# 1791076834-the-changelog-is-one-file-per-release — phase 4

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 72e32e96 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The words: `skills/update/SKILL.md` step 3 (scope 6); every prose site in
`spec.md` §*The readers and writers* — the docs, `CONTRIBUTING.md`,
`skills/verify/SKILL.md`, the `session_cost.py` printed line with its pin,
the `settle.py` and `fold_ledger.py` docstrings, the workflow comments, the
two `seal/follow-up.md` coordinates; `docs/the-record-layout.md` F2 marked
built and its rows rewritten (scope 9); `docs/release-checklist.md` §2's
staging line (D9); the work item's `changelog.md` fragment and its ledger
fragment. Then the phase-0 greps again, every remaining hit either in a
record or justified in `overview.md`.

## What this phase found

**The update skill's step 3 (scope 6)** reads the release files of every
version after the old one up to the new one, from the marketplace clone, and
says `CHANGELOG.md` beside them is only the index. Step 2b is unchanged (D2).

**The staging line (D9).** `docs/release-checklist.md` §2 now ends its
command block with `git add -A changelog/ CHANGELOG.md seal/
.claude-plugin/plugin.json` and says why: the suite lists files through the
index, and the gather creates a file the index does not have yet.

**`seal/follow-up.md` (Q4).** The two rows' three citations of the released
`CHANGELOG.md` §0.12.2 now read `changelog/0.12.2.md`. One of them also
quoted `CONTRIBUTING.md`'s rule as *one branch edits `CHANGELOG.md`*, a rule
this phase reworded to *one branch does write the changelog*; the quote was
brought to the rule's present wording, since it is the rule's citation and
not the row's decision. The decision and the answerer are untouched.

**The printed line (contract §14).** `session_cost.py`'s #377 line names
*its file under `changelog/`* where it named `CHANGELOG.md`, re-wrapped to
the block's width, and `tests/test_session_cost.py` pins the new phrase. Seen
red with the old phrase restored through `mutation-check` (executed).

**The evidence.** Six new rows in
`seal/ledger/1791076834-the-changelog-is-one-file-per-release.md`. The
build drifted 79 coordinates across 71 released rows; every one of those
rows was read (their claims, extracted into one listing). 57 still hold and
are `Re-read ·` rows written by `evidence-check --reverify --into`. Ten
named `CHANGELOG.md` where the code now reads the release files, and are
`Corrected ·` rows instead: 0.13.0's S2, 0.15.0's P3, 0.15.1's C2, F1 and
H1, 0.15.3's P3-3, 0.15.6's N5, 0.16.0's G1 and G6, and 0.4.0's marker row.
`evidence-check --strict .` then read 4,304 ok and nothing else (executed).

**The survivor sweep over the build range** (executed, `e141980a..72e32e96`):
147 sentences removed, four places reported, all in released ledger files
that are never edited. Each is in `survivors.md` with its quote and grounds;
two are the rows corrected above. Rerun with `--exempt`: every survivor
excused.

**The greps of phase 0, again** (executed on `72e32e96`, less the records,
`changelog/`, the 0.4.0 design record of `docs/one-root-by-lifetime*.md` and
the sweep's own one-file fixtures, which the spec keeps): every remaining
hit names the index for what the index still is — its first heading, its
release dates, the file the gather heads — or names both shapes, and
`overview.md` says so.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/the-record-layout.md`'s bullet naming `CHANGELOG.md` over the size target | the paragraph under the remaining bullet, saying it was the second until F2, with the measured size of the largest release file |
