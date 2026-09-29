# 1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there — phase 3

<!-- seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 2e205343 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 3, the records. The ledger fragment gets new rows for
S1–S4, S7 and §17; the changelog fragment is written; rows the edits drift are
re-read in place, with `seal/releases/0.15.1.md` S2 and `seal/releases/0.4.0.md`
named as citing `docs/commit-review-gate-spec.md`'s headings; and, only if Q3
moved the reader, rows A1–A3 of `seal/releases/0.15.5.md` and W3 of
`seal/releases/0.15.6.md` are removed and re-claimed. The spawn prompt added
that this repository writes fragments, never the shared file.

## What this phase found

**Q3 moved nothing, so no row was removed.** The reader is imported in place,
and A1–A3 and W3 stand as they were.

**The drift was one section, not the ones the plan named.**
`bin/evidence-check .` over the whole ledger named two drifted rows across
`seal/releases/0.12.0.md` and `seal/releases/0.15.5.md`, three rows in all,
every one anchored on `skills/implement/orchestration.md`'s routing section,
which phase 2's sentence changed. The rows the plan named against
`docs/commit-review-gate-spec.md`'s headings were not drifted, because none of
them anchors a heading the edits reached. Each of the three was re-read
against the edit and its claim holds: the asking is still homed in the
spawning session, the routing decision's spelling is untouched
(`tests/test_review_axes.py` and `tests/test_waiver_decided_at_start.py`, 37
passed), and Question 1's labels are untouched (the labels case passed). Each
took a dated **Re-read** note, and `--reverify` moved its hash from
`ec41c96f` to `f4f6c79a`. After it the whole ledger reads 2696 ok, nothing
drifted, and exit 0.

**The frame's own spec named five things the tree does not carry.** The
records half of `evidence-check` refused `spec.md`'s name for a transcript
entry's type and its four transcript tool-use ids, which exist only in a session transcript. Each
line now says NAME NOT IN TREE, as the check asks, and nothing else in the
spec changed.

**The fragment holds E1–E9**, one row per claim rather than one per case, so
each anchor set is what a later edit would drift: E1–E7 the gate, E8 §17, E9
the policy. Every anchor resolved on the first read (34 drifted from the
placeholder hash, none broken), and `--reverify` stamped them.

**What the other checks said.** `rider_check.py` exit 0. `survivor-check
--range origin/release/v0.16.0..HEAD`: no removed wording is still standing.
`correction-check --range origin/release/v0.16.0...HEAD`: exit 0.
`gather_changelog.py --check` exits 1 naming this fragment and work item
C's, which is what it says of any fragment before release preparation
gathers it. `tests/test_release_hygiene.py`,
`tests/test_a_merge_cannot_silently_drop_a_correction.py`,
`tests/test_chain_hooks_hardening.py` and `tests/test_no_real_identifiers.py`:
163 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
