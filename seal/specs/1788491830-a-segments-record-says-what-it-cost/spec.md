# Feature Specification: a segment's record says what it cost

<!-- seal/specs/1788491830-a-segments-record-says-what-it-cost/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file;
cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `templates/sdd-phase.md` §*What this phase was asked* | #119 made the SCOPE a segment was given durable. What executed that scope is the same class of fact and has no row |
| `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* | It measures every segment and posts the numbers. Nothing in the posting says what produced them, so a reading cannot be attributed afterwards |
| `docs/review-handoff-protocol.md` §*Files* | It owns the round record's format and carries a `Required` column for every field. A new field belongs in that table or record authors will not know it exists |
| `CLAUDE.md` §*The goal a design is chosen against* | The row is filled by whoever spawns the segment, who already knows the answer, so it adds no question to anyone |

## Scope

**In.**

- A row in `templates/sdd-phase.md` and `templates/sdd-round.md` naming what
  ran the segment: the agent and the model.
- The same field in `docs/review-handoff-protocol.md`'s field table, with its
  `Required` column answered and the drafts log moved.
- `ROUND_RECORD_FIELDS` in `tests/test_the_pull_request_language_is_the_repositorys.py`,
  which is hand-copied from the round template and pins it.
- Whether `chain_check.py` reads the row, and if so what it refuses — decided
  in the plan, with the grandfathering shape this repository already uses.
- Tests, a changelog fragment, and a ledger fragment.

**Out.**

- **The outcome column** — what a segment's output cost the next reader. #137
  names five candidate signals and refuses to pick a format before knowing
  which survive contact. It becomes its own ticket for the next release, and
  this branch writes its row in `docs/flow.md`.
- Any acceptance band for a segment kind. That needs #145's boundary first,
  and #110's *Not this* refuses a budget decided before the evidence exists.
- Changing what `session_cost.py` measures.

## What the row has to survive

**A segment does not always know what ran it.** An agent can be told, but a
value the agent types is a value the agent can get wrong, and the orchestrator
is the one that chose it. The row is therefore the spawning session's to fill,
the same way `Fixes checked by` and the fix-surface rows are — written by the
session that has the fact, reaching back into a record somebody else wrote.

**A repository that does not know either.** `agents/*.md` pins no model; the
model is a spawn-time argument, and a session spawning through some other
harness may have no name for it. So `unknown — <why>` has to be an answer, in
the shape `nobody — <why>` already has.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A phase says what built it | Given a build phase closes · When its record is written · Then the record names the agent and the model that ran it | `tests/test_a_phase_hands_the_next_one_a_record.py` grows a case; the template carries the row |
| A round says what reviewed it | Given a review round closes · When the orchestrator writes the record · Then the same | `ROUND_RECORD_FIELDS` grows the name and its existing parametrised case pins the template |
| The protocol knows the field | Given a session writes a record from the protocol rather than the template · When it fills the field table · Then the row is there with its `Required` column answered | `tests/test_the_fixes_name_their_surface.py`'s protocol case, extended — the same pin two earlier fields already have |
| An unknown runner is an answer | Given a session that cannot name the model · When it writes the record · Then `unknown — <why>` is accepted and the reason is required | a case, mirroring `nobody — <why>` |
| An old record is not made red | Given a work item begun before this rule · When its records omit the row · Then whatever the check does, it prints rather than fails | a cutoff case at the boundary second, mirroring `SURFACE_FROM` and `NEEDS_FROM` |
| Nobody is asked anything | Given the whole change · When a chain runs end to end · Then no step puts a question in front of a person | the prompt budget stated in the PR body: zero |

## Data & interfaces

One row, in both record templates. Its exact spelling is the plan's to settle;
what the spec fixes is that it names **two things and not one** — an agent
without a model cannot be compared against another run of the same agent, and
a model without an agent cannot be told from the orchestrator's own turns.

## Open questions → questions.md

One, answered in the batch before the first edit: this work item builds the
record row and not the outcome column beside it.
