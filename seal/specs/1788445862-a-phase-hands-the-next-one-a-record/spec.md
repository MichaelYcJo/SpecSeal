# Feature Specification: a phase hands the next one a record

<!-- seal/specs/1788445862-a-phase-hands-the-next-one-a-record/spec.md — WHAT
this work delivers and how we'll know. The policy documents in docs/ outrank
this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-handoff-protocol.md` §Files, `round-N.md` — what this round did | The model this work copies for the build side: a committed, per-segment record naming what was asked, what carries forward, and what only that segment could see |
| `docs/review-handoff-protocol.md` §Non-goals — "Structured handoff for one workflow (review), nothing broader" | Grounds for NOT extending that protocol document to cover build phases. `templates/sdd-phase.md` gets its own wiring in `templates/sdd-plan.md` and `agents/smith.md` instead, at the same status `plan.md`'s own Status column already has — a plugin convention, not a cross-tool protocol |
| `CONTRIBUTING.md` §What a change to a gate must carry | Does not apply. This work adds no gate, hook, or refusal logic — the repository owner chose enforcement level 2 of 3 (template blank + skill instruction), explicitly not level 3 (a `chain_check.py` refusal), so no red test / failure-direction / prompt-budget / platform-honesty writeup is owed |
| `skills/implement/SKILL.md` §3 The SDD file set — "A template that no shipped document names is a template a session cannot find" | Why `templates/sdd-phase.md` is wired into `templates/sdd-plan.md`'s pointer sentence, `agents/smith.md`'s Implement phase, and `skills/implement/SKILL.md`'s file-set table, rather than left to be discovered |

## Scope

**In:**
- `templates/sdd-phase.md`, new — the per-phase record, shaped after
  `templates/sdd-round.md`: what this phase was asked, what it found that the
  next phase needs, what it removes from the tree that another phase must
  place.
- `templates/sdd-plan.md` — a pointer sentence: phase records live at
  `seal/specs/<work-item-id>/phases/phase-N.md`, written when a phase closes.
- `agents/smith.md` §Implement (phase 3) — the instruction to write
  `phases/phase-N.md` at each phase's close.
- `skills/implement/SKILL.md` — a row for `phases/phase-N.md` in the SDD
  file-set table; the instruction that the phase-specific content of the
  spawn/task — not the boilerplate the contract, this skill, and
  `agents/smith.md` already carry — is copied into "What this phase was
  asked"; `phases/phase-N.md` added to the list of files `Record language`
  governs.
- `templates/sdd-round.md` — a new "What this round was asked" section,
  explicit rather than only implicit in the Verdicts table's grounds.
- `skills/code-review/SKILL.md` — the instruction that the round-specific
  content of the spawn prompt is copied into that section when the
  orchestrator writes `round-N.md` after posting.
- `questions.md` — the two #119 add-ons recorded as explicitly deferred.
- New test coverage pinning the above, following this repository's own
  carrier-consistency convention (`tests/test_the_fixes_name_their_surface.py`
  is the model named for this work).

**Out:**
- Any change to `hooks/*.py`, `skills/*/scripts/chain_check.py`, or any other
  refusal/exit-code logic. The owner decided level 2 (template + skill
  instruction), not level 3 (a gate) — see Grounding.
- `docs/review-handoff-protocol.md` itself — its own Non-goals excludes the
  build side.
- Naming which plugin version/commit was in force for a segment (#119
  add-on 1) — deferred, `questions.md`.
- A `CONTRIBUTING.md` paragraph on the version-cache confusion (#119
  add-on 2) — deferred, `questions.md`.
- `templates/config.md`'s "What no row governs" list. That list is derived
  from the checkers' own constants; nothing checks a `phase-N.md` field, so
  nothing is added there.
- #84's framer channel. #121 names it as needing this work; building for it
  is explicitly out of scope here.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A phase closes and the next phase needs what it discovered | Given a work item mid-build, when a phase's implementation ends, then `seal/specs/<id>/phases/phase-N.md` exists, written from `templates/sdd-phase.md`, naming what building it taught that the diff alone does not show | Read: the template ships the required sections outside HTML comments; `agents/smith.md` and `skills/implement/SKILL.md` instruct writing it at phase close |
| A phase's diff removes something and its only other home is removed later, unnoticed | Given the #107 measured failure — phase 4 moved a rule out of `agents/smith.md`, phase 5 removed the interim home it had never actually reached, deleting it from the repository with nothing recording that it had gone missing — when a phase's diff removes something from the tree, then the record's removal table names it and where it must land | Read: the template's removal table exists, with the #107 shape as its own worked example in the surrounding comment |
| A round or phase record is opened later with no memory of the spawn prompt behind it | Given `round-N.md` or `phase-N.md` committed, when someone opens the record, then a "What this round/phase was asked" section holds the prompt's specific content, not the boilerplate the contract, the skill, and the agent definition already carry | Read: the section exists in both templates; `skills/code-review/SKILL.md` and `skills/implement/SKILL.md` instruct the orchestrator to copy it in |
| A repository with no `Record language` row writes these records | Given `seal/config.md` here carries no such row | Prose in every new/changed section is English, matching every other SDD document in this tree and the default the `implement` skill states for an absent row |

## Data & interfaces

No schema, endpoint, or payload — this work is documentation and template
surface only. The new file `seal/specs/<work-item-id>/phases/phase-N.md` is
shaped after `seal/specs/<work-item-id>/rounds/round-N.md`
(`docs/review-handoff-protocol.md` §Files); its field list is in `plan.md`.

## Open questions → questions.md

Both #119 add-ons — naming which plugin version/commit was in force for a
segment, and a `CONTRIBUTING.md` paragraph on the version-cache confusion —
are recorded there as explicitly deferred, per the owner's own scoping of
issue #119.
