# Implementation Plan: a segment's record says what it cost

## Summary

Issue #137, narrowed to its first half. Every segment of two work items was
measured this week and posted to the flow log, and **not one of the readings
says what produced it.** They all ran on the same model, and that fact exists
only in a session transcript.

#119 already made the other half of this durable — `## What this phase was
asked` records the scope a segment was given. What executed that scope is the
same class of fact, and the record has no row for it.

This changes the shape of a record every segment writes and a field table a
skill instructs sessions to fill, which is the top rung of the `implement`
skill's ladder, so this plan comes before implementation.

## Technical context

- `templates/sdd-phase.md:16-17` — the field table, two rows: `Phase` and
  `Commit`. The new row joins it.
- `templates/sdd-round.md:11-19` — the field table, eight rows.
- `tests/test_the_pull_request_language_is_the_repositorys.py:955`
  `ROUND_RECORD_FIELDS` — hand-copied from that template and pinning it. It
  grew twice this week and both times the parametrised case had to be run
  before the list changed, because a name absent from the list cannot be
  parametrised over. The direction is list → template.
- `docs/review-handoff-protocol.md` — the field table with its `Required`
  column, and the drafts log. `tests/test_the_fixes_name_their_surface.py`'s
  protocol case enforces a row, a `Required` value starting `yes`, and a
  bumped draft for exactly this class of change. It was extended for the floor
  row a week ago and is extended again here.
- `skills/code-review/scripts/chain_check.py:333` `STRICT_FROM`, `:373`
  `SURFACE_FROM`, `:459` `NEEDS_FROM` — three cutoffs, one shape: a unix
  second read from the work item's directory name. A fourth follows it if the
  row is checked at all.
- `tests/test_a_phase_hands_the_next_one_a_record.py` — the phase template's
  own pins.

**What breaks in six months.** A row whose only writer is a person is a row
that goes stale silently — the orchestrator knows the model at spawn time and
nothing makes it write the value down. The mitigation this plan takes is that
the row is refused when absent on a work item after the cutoff, so the record
cannot be written without answering; what it cannot do is tell a true answer
from a plausible one, and `unknown — <why>` exists so the honest answer is
available rather than only the confident one.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Have the agent write the row itself | The agent is told what it is, so the value it writes is the value it was told; and the orchestrator is the one that chose the model. A field the subject fills about itself cannot be checked against anything | Rejected — the spawning session fills it, like `Fixes checked by` |
| One row naming the model alone | A model without an agent cannot be told from the orchestrator's own turns, and #145 is precisely about the orchestrator being unattributable | Rejected — the row names both |
| Leave the row unchecked, like `Needs a fix` was | That row's own template says no check read it, and #110's review found the consequence: a row nothing reads is true only when somebody is awake. It cost a wall and a fix pass to correct | Rejected — the check reads it, grandfathered |
| Build the outcome column too | Five candidate signals and no evidence which survive contact. #137's body refuses to pick a format early, and #110's *Not this* refuses deciding before the evidence exists | Rejected — questions.md Q1; it becomes its own ticket |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The row in both templates and in `docs/review-handoff-protocol.md`'s field table, with the drafts log moved; `ROUND_RECORD_FIELDS` grown | the protocol case extended and seen red; the `ROUND_RECORD_FIELDS` case run before the list grows, per the direction that pins it | `e9e463b` |
| 2 | `chain_check.py` reads the row: absent is refused after a fourth cutoff and printed before it; present and unreadable is refused at any age; `unknown — <why>` is an answer and a bare `unknown` is not | each refusal seen red at a named SHA, mirroring the three cutoffs already in the file | `2a36737` |
| 3 | `skills/verify/SKILL.md` says the spawning session fills it, because it is the one that knows | a case pinning the sentence | `bf2eddc` |
| 4 | The fragments, and `docs/flow.md` — this ticket's box, and a row for the outcome-column ticket this work opens | `evidence-check --ledger`, `fold_ledger --dry-run`, `unverified-check` | |

Phase 1 before 2 for the reason this repository has now learned three times:
the sentence that tells somebody what to write lands before the check that
refuses them for not writing it.

## Operational impact

- **No migration, no environment variable, no dependency.**
- **A record written after the cutoff without the row fails a pull request.**
  Bounded by work-item id, the shape `STRICT_FROM`, `SURFACE_FROM` and
  `NEEDS_FROM` already take.
- **Failure direction: blocks more**, and the trade is the same one #110 took:
  a wrong refusal costs a message on a pull request somebody is reading.
- **Prompt budget: zero.** The value is known at spawn time by the session
  that writes it.
