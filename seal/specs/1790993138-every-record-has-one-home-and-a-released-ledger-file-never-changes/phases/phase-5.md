# 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 2ff114b5 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`docs/the-record-layout.md` (D8): every kind of record with its home, size
target and index, the per-place index tables, the D7 cut, and F1–F4 marked as
not built, each with the issue the orchestrator filed — F1 = #727, F2 =
#728, F3 = #729, F4 = #730. Scenario S13, with
`tests/test_docs_line_wrap.py`, the `docs/` ceiling case and
`tests/test_both_editions_carry_the_same_folds.py` run. The orchestrator then
corrected when each lands: F1 in 0.18.0, after #716; F2, F3 and F4 in
0.18.1.

## What this phase found

**The frame holds for this phase.** The document is plain prose under no
fold marker: a work item writes policy here by Q4's decision, and
`fold-check` binds only marked statements, so `settle` folds this item's
spec later like any other. It has no `.ko.md` edition, so the editions case
has nothing to pair.

**What it carries, against S13.** A summary table with one row per kind —
the evidence ledger, the changelog, a work item's files, the repository's
rules, the configuration, the follow-up list — each with its home, size
target and index; then the size target and the three kinds over it; then one
table per place (`docs/`, `seal/`, `seal/specs/<work-item-id>/`, the root
records), each row naming a file and the one question it answers; then the
D7 cut and F1–F4 with their issues and releases. The size figures (37
release files, 2.42 MB, 148 sections at most 58 KB, `CHANGELOG.md` at
549 KB, the 8,831-character row) are the frame's measurements at 233f0455,
and the document dates them so.

**It is also the fragment rule's home**, as spec §*The classes, enumerated*
assigns it: the `Instead of / Write` table, with a third row for a re-read
or a correction of a released row, the gathering at the release, and the
fold's own fragment. It points at a section phase 6 writes,
`docs/the-evidence-ledger.md` §*A released row is read again in the
branch's fragment*, so phase 6 must use that heading.

**The work-item file list was taken from the tree, not from the template.**
At this phase's tip the 48 directories under `seal/specs/` hold `routing.md`
48 times, `overview.md` 48, `changelog.md` 46, `spec.md` and `plan.md` 45,
`questions.md` 44, `survivors.md` 31, `handoff.md` 2 and `pr.ko.md` once,
with `phases/` in 45 and `rounds/` in 46. `handoff.md` and `pr.ko.md` are one
work item's own and are not indexed; `tests-todo.md`, `evidence-todo.md` and
`broad-gate.md` are, from `skills/implement/SKILL.md` §5 and the routing
template, though none stands in the tree today.

**One stale home left as the frame says.** `seal/config.md`'s `Over the
ceiling` row and `docs/the-evidence-ledger.md`'s ceiling statement name
#715 as the issue that splits `docs/commit-review-gate-spec.md`, and the
split moved to #727. D7: "The freeze row stays as it is until then", and
F1's change removes the row. A pin holds the row and the prose to one home,
so re-pointing it is a three-file edit the frame declined. It is in
`overview.md` under *Not done*.

**M3 for phase 5: 0.** A new document is cited by no ledger row; a frozen
`--reverify .` names nothing new.

**Narrow runs (executed).** The three named cases: 86 passed. Every test
module that walks `docs/`, 53 of them, with `tests/test_no_real_identifiers.py`:
2,330 passed and 69 skipped, then 834 passed and 1 skipped for the thirteen
the first command's list left out.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
