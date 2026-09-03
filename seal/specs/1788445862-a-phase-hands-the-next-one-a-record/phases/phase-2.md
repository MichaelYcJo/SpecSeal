# 1788445862-a-phase-hands-the-next-one-a-record — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | a59a9c2 |

## What this phase was asked

Build phase 2 only, of the 4-phase table in `plan.md`: give `agents/smith.md`
phase 3 ("Implement") one instruction — at each phase's close, also write
`phases/phase-N.md` from `templates/sdd-phase.md`. Give
`skills/implement/SKILL.md` three things — a row for `phase-N.md` in the SDD
file-set table (§3); the instruction that the phase-specific content of the
spawn or task, never the boilerplate the contract, the skill, and
`agents/smith.md` already carry, is copied into "What this phase was asked";
and `phases/phase-N.md` added to the `Record language`-governed file list
beside `rounds/round-N.md`. Add the plan's Phase 2 test cases to
`tests/test_a_phase_hands_the_next_one_a_record.py`: `agents/smith.md` and
`skills/implement/SKILL.md` carry the required phrases, plus a
carrier-consistency check that `phases/phase-N.md` is spelled identically
across all four files phase 1 and 2 touch. Every new case shown red first.
Phase 3 and 4 were explicitly out of scope: stop once phase 2's own scope is
committed and its narrow verification is green.

One extra step beyond the plan's own Phase 2 row, same as phase 1: once the
new `agents/smith.md`/`skills/implement/SKILL.md` instruction existed, use it
— rather than improvise — to write this file, and report whether that
instruction reads as self-sufficient or needed today's explicit reminder to
produce it.

## What this phase found

**`templates/sdd-phase.md`'s own path comment does not spell "phase-N.md"
the way the three prose files do — and that is not a bug.** The
carrier-consistency check in `plan.md`'s Phase 2 row names
`templates/sdd-phase.md` as one of "all four files" that must spell
`phases/phase-N.md` identically. Read literally, that check fails:
`templates/sdd-phase.md`'s own header comment (written in phase 1) spells
its own path `phases/phase-<N>.md`, with the bracket — mirroring
`templates/sdd-round.md`'s own header, which spells its path
`rounds/round-<N>.md`, also bracketed, and never once writes the bracket-free
`round-N.md` anywhere in its own text. Every file that instead *points at*
either record from prose — `docs/review-handoff-protocol.md`,
`skills/code-review/SKILL.md`, `agents/warden.md` on the round side;
`templates/sdd-plan.md`, `agents/smith.md`, `skills/implement/SKILL.md` on
the phase side — uses the bracket-free form. The bracket marks a template's
own self-description of a path with a number still to be filled in, matching
the `<unix-epoch-seconds>-<slug>` placeholder already in the same sentence;
dropping it in `templates/sdd-phase.md` alone would make that one file
inconsistent with its own sibling template and with the rest of its own path
comment, to satisfy a literal string match against three files that are
doing a different job (pointing a reader at the file, not describing the
file's own name to itself).

So the carrier-consistency test this phase adds is two checks, not one: the
three prose carriers (`templates/sdd-plan.md`, `agents/smith.md`,
`skills/implement/SKILL.md`) pinned to the identical bracket-free
`phases/phase-N.md`, and `templates/sdd-phase.md`'s own header pinned
separately to `phases/phase-<N>.md`, with the test's comment naming why the
split is deliberate rather than an oversight. `plan.md`'s Phase 2 row is not
wrong about the substance — the four files do need to agree on how this
record is named — it just undercounts the one legitimate exception its own
model (`templates/sdd-round.md`) had already set.

**Whether the new `agents/smith.md` instruction is self-sufficient.** The
paragraph added this phase names the file
(`seal/specs/<work-item-id>/phases/phase-N.md`), the template
(`templates/sdd-phase.md`), the timing (each phase's close), a one-line
summary of what each section holds, and points to
`skills/implement/SKILL.md` §3 for the boilerplate/specific split. Read cold,
it carries everything a spawned smith needs to act without a second prompt.
It was not tested cold, though: this phase's own task explicitly repeated
"same extra step as phase 1 … this is the second live test" in the same
breath as the rest of the phase 2 scope, so this session read the
instruction already primed to look for it rather than discovering it
unprompted at a phase boundary. Phase 3's own close is the first point where
a smith reaches "write `phases/phase-N.md`" without that scaffolding already
in the prompt that spawned it, and that is the real test of whether the
instruction stands alone.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | — |
