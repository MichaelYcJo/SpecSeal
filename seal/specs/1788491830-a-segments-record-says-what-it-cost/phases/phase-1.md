# 1788491830-a-segments-record-says-what-it-cost — phase 1

<!-- seal/specs/1788491830-a-segments-record-says-what-it-cost/phases/phase-1.md — what
this phase of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | e9e463b |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Build phase 1 only, of the four-phase table in `plan.md`: the row naming what
ran a segment, in both record templates and in
`docs/review-handoff-protocol.md`'s field table with its `Required` column
answered and the drafts log moved, and `ROUND_RECORD_FIELDS` grown. Nothing
reads the row this phase; phase 2 is where the check arrives.

Coordinates given rather than searched for:

- `templates/sdd-phase.md:16-17`, two rows today.
- `templates/sdd-round.md:11-19`, eight rows.
- `tests/test_the_pull_request_language_is_the_repositorys.py:955`
  `ROUND_RECORD_FIELDS`, hand-copied from the round template and pinning it.
  **The direction is list → template**: a name absent from the list cannot be
  parametrised over, so the list grows first and the red is watched with the
  template still short. The last two additions were done that way and the
  prompt got the direction backwards both times.
- `docs/review-handoff-protocol.md`, the field table with its `Required`
  column and the drafts log.
  `tests/test_the_fixes_name_their_surface.py`'s protocol case enforces a
  row, a `Required` value starting `yes`, and a bumped draft for exactly this
  class of change — extend it rather than writing a parallel case.
- `tests/test_a_phase_hands_the_next_one_a_record.py`, the phase template's
  own pins.

Two constraints on the row's shape, from `spec.md`: the subject cannot fill it
(an agent is told what it is, so the value it writes is the value it was told,
and the orchestrator chose the model), and a repository may not know it at all
(`agents/*.md` pins no model), so `unknown — <why>` is an answer and a bare
`unknown` is not. The row names the agent **and** the model, never one of
them.

## What this phase found

**The row's two halves are joined by the word `on`, not by punctuation.** The
value is `agent on model` — `specseal:smith on Opus 5 (1M context)`. That was
chosen against the defect this repository found twice in the two work items
before this one: a separator inside a code span splits the cell carrying it,
once as a literal `;` in a `Contract changes` entry and once as a literal `|`
in a memo table row. A separator that is a word cannot split a cell, so the
whole class is absent by construction rather than avoided by care.

**The exclusion list has two derivations, not one, and the second was not in
the plan's coordinates.** `templates/config.md`'s *What no row governs* is
checked from two directions:
`test_the_exclusion_list_holds_every_string_a_checker_matches` reads module
constants out of the checkers, and
`test_the_exclusion_list_holds_every_field_a_pinned_case_reads` reads
`ROUND_RECORD_FIELDS` — the very list this phase grew. So growing that list
turned `templates/config.md` red before `chain_check.py` was touched at all.
Phase 2 adds constants and will meet the first derivation the same way; it
needs `RAN_BY`, and the `on` and `unknown` words, in `_literal_strings()`.

**`Ran by` sits directly after the row naming the commit, in both templates.**
`Target SHA` for a round and `Commit` for a phase. That is the parallel worth
having: the two rows together say what this record is a record OF — what was
looked at, and what looked. Putting it last in the round template would have
placed it after the two rows that are the reviewer's own answers, which are a
different kind of cell.

**The phase template's field-table pin is an exact-list equality**, so it goes
red whichever order the template and the list move in — unlike
`ROUND_RECORD_FIELDS`, which is a membership check and only goes red in one
direction. Worth knowing before phase 2 touches either.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
