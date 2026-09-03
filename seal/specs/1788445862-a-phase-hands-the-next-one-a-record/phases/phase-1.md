# 1788445862-a-phase-hands-the-next-one-a-record — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | d7c323c |

## What this phase was asked

Build phase 1 only, of the 4-phase table in `plan.md`: a new
`templates/sdd-phase.md` mirroring `templates/sdd-round.md`'s shape — a
field table (`Phase`, `Commit`), then `## What this phase was asked`,
`## What this phase found`, `## What this phase removes`, each with its own
HTML comment naming the measured failure it answers (`plan.md`'s Phase 1
row names which #107 failure the removal table's comment specifically has
to carry). Also add a one-sentence pointer in `templates/sdd-plan.md` naming
`seal/specs/<work-item-id>/phases/phase-N.md`, and write the new test module
`tests/test_a_phase_hands_the_next_one_a_record.py` per the plan's Phase 1
row, with every new case shown red first — the section deleted or
commented out, the assertion watched failing, then restored — before being
called done. Phase 2, 3, and 4 were explicitly out of scope: stop once
phase 1's own scope is committed and its narrow verification (the command
in the Phase 1 row) is green, not once the whole work item is done.

One extra step beyond the plan's own Phase 1 row: once
`templates/sdd-phase.md` existed, use it to write this file — this branch's
own phase 1 — documenting what this phase was asked and what it found,
specific to this phase rather than the boilerplate the agent contract
already carries. This is the first real use of the mechanism the whole work
item exists to build, used on itself.

## What this phase found

**Why the field table carries only `Phase` and `Commit`.** Every other row
in `templates/sdd-round.md`'s field table exists to support something a
build phase does not have: `Target SHA` and `PR` exist because a round is
read by a later round and eventually a pull request; `Broad gate` and
`Fixes checked by` exist because the review chain reaches back into a
round's fixes from a later one; `Contract changes` and `New units` are the
fix surface a *verifying* round reads; `Pass` closes a verdict table a phase
record does not have, because a phase is not reviewing anything — it is
reporting on itself. None of that reach-back machinery applies to a build
phase, which is read forward by the next phase and never re-opened by a
verifier the way a round is.

**Section order — asked, then found, then removes.** `round-N.md` leads
with its Verdicts table because a round's central act is judging; a phase's
central act is building, so the record leads with what it was told to build
(asked), then what building it taught (found), before the smaller,
often-`none` question of what it displaced (removes). Putting `removes` last
also matches its own comment's #107 story: a reader who has already read
what this phase was asked and found is the reader in the position to notice
a bare `none` looks wrong.

**What surprised me in `test_the_template_rows_are_rows_a_session_can_copy`'s
pattern.** My first draft of the field-table test over-collected: it scanned
every line starting with `|` for the whole file, so the removal table's
placeholder row (also a pipe table, two sections down) got read as part of
the `Phase`/`Commit` field table and the test failed for the wrong reason.
`templates/sdd-round.md`'s equivalent test never hits this, because that
file's field table is immediately followed by a `- [ ] Pass` checkbox line —
not another pipe table — before the next `## ` heading, so a naive "every
line starting with `|`" scan never crosses into a second table.
`templates/sdd-phase.md` has two pipe tables in one file (the field table
and the removal table), so the reader has to bound itself to the section
between one heading and the next `## ` heading rather than scanning the
whole file. Fixed by finding the first `## ` heading after the field table
and slicing to it before collecting rows.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | — |
