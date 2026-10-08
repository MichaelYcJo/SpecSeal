# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 5c24f534 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The migration path: S7 as a case — a `Corrected ·` row holding its citation
and a node id supersedes the released row, an edit to the root's unit
produces no finding, and `--reverify --into` writes no `Re-read ·` row for
it — and S9's one summary sentence in `reverify_into`, pinned. If S7 needed
a change in `family_view` or `left_alone`, one branch, named here.
`questions.md` Q2 (does the supersede already carry it) and Q4 (does
`hooks/evidence-advisor.py` carry a repair sentence of its own) were this
phase's to answer.

## What this phase found

**Q2, measured: the supersede already carries it, and nothing in
`family_view` or `left_alone` changed.** The S7 case
(`tests/test_a_released_row_is_read_again_in_a_fragment.py::test_a_released_row_moved_onto_its_test_never_drifts_again`)
passed at its first run on 48d201ad. The released row's family is in
`superseded`, so its `handler` coordinate is not graded; the correcting row
has no code coordinate, so its own family grades nothing; `released_drift`
skips the superseded root, so `--into` writes nothing and prints
`0 citing rows written · 0 released rows left`. `--strict` totals `2 ok`:
the citation, and the test through phase 1's arm. Seen red by
`bin/mutation-check` removing `if top in superseded: continue` from
`family_view`: the case went red.

**Q4, read: the hook carries its own sentence.** `hooks/evidence-advisor.py`
prints the checker's BROKEN, OLD-FORMAT, MALFORMED and OVERFLOW lines as they
come, so phase 1's new findings reach a commit with no change there. But for
a broken row under the freeze it closes with `FROZEN_REPAIR`, its own words,
which named a `Corrected ·` row carrying "every coordinate the claim still
rests on" and `--reverify --into` for drift. That sentence now names the
other form in the same breath — "or, where a test holds the claim, names
that test instead, `tests/test_x.py::test_y`, and no later edit drifts it" —
pinned by `test_the_commit_advisor_names_the_test_row_as_a_repair` and seen
red with the clause removed. The hook's docstring paragraph that restates
the sentence was brought along. Its heading line still says *anchors broken*
when the broken row is a test; a broken test is also a citation that does
not resolve, and the line is the hook's count of BROKEN findings, so it was
left.

**The S9 sentence is `INTO_HELD`**, printed on the line after
`N citing rows written · M released rows left`, by a run that wrote at least
one `Re-read ·` row and by no other. `spec.md` D5 says "unconditionally",
S9 and §*Data & interfaces* say "printed once per run that writes a
`Re-read ·` row"; the build follows S9, since a run that wrote nothing owes
no reader a second repair. Seen red both ways through `bin/mutation-check`:
the sentence removed, and the sentence printed by every run.

Executed, output read: the new module, the released-row module and
`tests/test_evidence_check.py`, 554 passed; every module that reads the
advisor (`test_a_gate_that_fails_says_so`, `test_a_row_points_by_content`,
`test_dispatch`, `test_local_mode_resolves_under_the_git_dir`,
`test_the_ledger_rules_have_one_home` and the two above), 797 passed;
`uvx ruff check` and `uvx ruff format --check` on the four files.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
