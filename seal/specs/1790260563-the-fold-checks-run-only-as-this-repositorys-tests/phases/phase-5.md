# 1790260563-the-fold-checks-run-only-as-this-repositorys-tests — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | cf992859 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

The documents that describe what phases 2 to 4 built:
`skills/settle/SKILL.md` §2 and §*What a fold branch owes*,
`docs/release-checklist.md` §*2b*, the cheat-sheet row in `README.md` and
`README.ko.md`, the evidence-ledger sentence about what the check pins, and
the changelog fragment. `test_settle_owns_the_shape_rule` was to be updated
to the new §2 sentence and seen red against the old one. The README-pair,
wrap and script-reach modules were to run, and `bin/evidence-check .` with
each drifted row re-read and re-stamped. Every test module that reads an
edited document runs; the count of such modules is the count run.

## What this phase found

- **Q2 answered: one row outside the fragment drifted.** It is 0.14.0's D1,
  anchored on §*What a fold branch owes*. Its claim — that the ledger
  changes only by removal and re-verification — is untouched, so it holds;
  it was noted `Re-read 2026-09-25` and re-stamped. §2's edits drifted no
  released row, because the two rows that anchored inside §2, 0.14.0's S1
  and P1, had left in phase 2.
- **53 modules read a document this phase edited,** found by grep over
  `tests/*.py` for each edited path and for the walkers over `docs/` and the
  shipped roots. All 53 ran. Two were red on the first run:
  - `test_settle_owns_the_shape_rule`, because its new phrase did not carry
    the line break the document has;
  - `test_a_record_states_what_the_tree_has`, because this work item's own
    records name units it removed (`SHAPE_CUTOFF`, `LINE_CEILING`, the old
    prose pin, the old command case). Each such line in `spec.md`,
    `plan.md`, `overview.md` and `phases/phase-3.md` now ends
    ` · NAME NOT IN TREE`, which is the checker's own exemption for a record
    that means a name the tree no longer has. `spec.md` and `plan.md` are
    the framer's. The edit there is the marker alone, on the lines the
    check named (two in `spec.md`, one in `plan.md`), and no wording moved.

  Both were green after the corrections.
- **The pin holds both halves (§14).** The new phrase present: red against
  the old §2. The old sentence absent: red with *It ships no checker for the
  shape* put back beside the new text.
- **The ceiling statement's `Enforced by:` line now names two targets**, the
  second being the prose pin at 135 columns. That is the first real line
  phase 4's skip lets through, and the shape check and the wrap test are
  both green on it.
- **`correction-check --range origin/release/v0.15.3...HEAD`** exits 0: no
  merge commit in the range, so no correction can have been dropped at one.
- **`CLAUDE.md` holds no sentence this work makes false.** It names no fold
  check, no cutoff and no ceiling, and the fragment rules it states are the
  ones this work followed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| settle §2's *It ships no checker for the shape … writes its own check* | the same paragraph, now saying the plugin ships `fold-check` and the repository states its values as rows; `templates/config.md` §*The fold's values* holds what each row accepts |
| the evidence ledger's *The check also pins the cutoff, the ceiling and the empty list against its constants* | the same statement: the values are `seal/config.md` rows, and a pin holds them and the section to the same numbers |
