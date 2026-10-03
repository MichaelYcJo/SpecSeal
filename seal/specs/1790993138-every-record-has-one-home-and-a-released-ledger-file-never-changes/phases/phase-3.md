# 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | fe253c4f |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`correction-check`: a dropped `Corrected ·` citing row is a loss, and the
freeze arm with the cutoff, the exemptions and the one-line report (D5). The
box-3 cases. Scenarios S6–S10: new cases in
`tests/test_a_merge_cannot_silently_drop_a_correction.py` for S8–S10, and a
two-branch module for S6 and S7, driven from Python; S6 red with 233f0455's
in-place `--reverify`; S7 red against a newest-wins variant.

## What this phase found

**The frame holds for this phase.** `#ledger_listing`, `#rows`, `#MARKER` and
the merge walk in `#examine` stand where `plan.md` puts them. The freeze arm
needed no listing of its own: two `git diff` calls over the range (added
`routing.md` paths, and `--name-status` over `seal/ledger.md` and
`seal/releases`) answer it, and the cutoff is read from `seal/config.md` at
the range's tip through `hooks/config.py#config_rows`, loaded by path beside
the fence reader and refused the same way where it is missing.

**How a dropped correction is identified.** A `Corrected ·` row by its
citation with the hash dropped (`correction_check.py#corrections`), which no
edit to the row moves. The merge result is read across every ledger path, so
a row a fold moved is not dropped; a row a parent deleted relative to the
base is honoured, as a marker is; a row whose cited release file the result
no longer has is not judged, because the released row is what still stands.
The report prints such a row under `dropped`, with the merge, the parent and
the row it corrects, and says why it matters in its own sentence.

**The base's own version is read off the range as written.** `A...B` is
resolved to a merge base before the arm runs, and a commit has no name, so
`frozen_changes` reads `release/vX.Y.Z` from the left side of `--range` to
allow #540's join of `X.Y.Z.md`. The hygiene step passes
`origin/<base>...HEAD`, which carries the name; the step does not change, as
D5 says.

**Box 3, as cases (executed).** `tests/test_two_branches_re_read_one_released_row.py`:
two branches each edit a unit a released row cites and run `--reverify
--into` into their own fragment; both `git merge` calls exit 0 and
`--strict` exits 0 (S6). The control is the rule this replaces, a case of its
own: the same two re-reads written in place without the freeze row, and the
second merge conflicts on `seal/releases/0.1.0.md`. That control is S6's
red, kept as a case rather than run once against 233f0455, because the
in-place path is still the shipped behaviour without the row. S7: both
branches edit lines of `f`, git merges them, and the merged tree reports
DRIFTED on `a.py#f` alone.

**S7's red, and why newest-wins does not reach it.** Read: under a "newest
re-read wins" reading S7 is DRIFTED too, because neither re-read holds the
merged `f`; what turns S7 green is a variant where a reading's existence
vouches without its hash. That variant — `held` falling back to any other
reading — was the break, and S7 went red. S6 is the scenario a newest-wins
whole-row snapshot fails (A's `f` is dropped when B's row, which carries only
`g`, is newest).

**M3 for phase 3 (executed): 3 released rows drifted**, C6 and C9 of
`0.12.2` and D3 of `0.12.3`, all citing `correction_check.py#examine`, which
gained one line after its marker loop. Each was read: the unreadable-blob
branch, the one-report grouping and the first-parent tie are untouched, so
all three claims hold. `--reverify --into` wrote 3 rows, exit 0; `--strict .`
exit 0.

**Seen red (§15).** Before any code: 5 failed, 62 passed in the two
modules. S6, S7 and the control passed, because phases 1 and 2 had built what
they hold; S6's red is the control and S7's is the break above. Every unit
this phase added was broken with `mutation-check`, 19 breaks; one survived —
the empty-row branch of `cutoff_at`, whose case had no `seal/config.md` at
all — and went red against
`test_a_config_with_other_rows_and_no_freeze_row_leaves_the_arm_off`, the
state every installed repository with any other row is in. Three loss-arm
units had no case before their breaks were written, and each got one: a row a
parent deleted, a row both parents carried, a citation whose file is gone.

**Narrow runs (executed).** The seven modules that name `correction_check`
or `correction-check` plus the two-branch module: 320 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
