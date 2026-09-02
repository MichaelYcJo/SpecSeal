# Feature Specification: one bar misreads two of the three segment kinds

<!-- specs/1788277657-one-bar-misreads-two-of-the-three-segment-kinds/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §The goal a design is chosen against | the bars must stay a lens no gate applies — a rule that stops a small honest round to ask is the more expensive design, and the difference would have to be argued |
| `docs/review-handoff-protocol.md` §While the implementer runs | the meter (`session_cost.py`) is already pointed at from here; the bars that interpret its numbers belong beside the pointer |
| `specs/1788224363-…/questions.md` Q1 | the advisory threshold (1.2) and the acceptance bar (1.8) are different instruments; the answer that keeps them apart is the owner's, recorded there |

## Scope

**In:**

1. The per-segment acceptance bars become written rules, with issue #51
   observation 1's numbers verbatim: a reviewing segment is judged on tools
   per turn ≥ 1.8; an implementing segment on `repeats = 0` and calls per
   deliverable, not on tools per turn; a verifying segment is exempt. Plus
   the small-round nuance: at very small rounds (a 23-call round read 1.64)
   the ratio has few independent batches to rise on, so the bar reads rounds
   of ordinary size and refuses nothing.
2. A written rule that a fix pass resumes the implementing session rather
   than spawning a fresh one, carrying its three measurements.
3. Q1 of `specs/1788224363-a-subagent-rediscovers-what-the-session-established/questions.md`
   marked answered: keep 1.2, chosen by the repository owner on 2026-09-01.

**Out:** any change to `skills/verify/scripts/session_cost.py`'s behavior,
any new checker, any new question to a person, edits to `agents/smith.md`
and `agents/warden.md` — their existing sentences (the serial-loop caveat at
1.08–1.17, the batching expectation at 1.89) already agree with the bars,
and consistency is kept by quoting the same measured ranges rather than by
editing them.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| An orchestrator judges a reviewing segment | Given a transcript of ordinary size, when the meter reports tools per turn, then the protocol names ≥ 1.8 as the bar and the measured 1.29–1.89 range as its grounds | grep `docs/review-handoff-protocol.md` for the bar |
| An orchestrator judges an implementing segment | The segment is judged on `repeats = 0` and calls per deliverable; tools per turn is named as the number that does NOT judge it | read the segment table |
| A small round is measured | A 23-call round reading 1.64 is refused by nothing — the section says the bar is a lens for rounds of ordinary size, never a refusal threshold | read the nuance paragraph |
| A round's findings need fixes | The orchestrator resumes the session that built the branch; the fresh spawn is named as the fallback for a session that no longer exists | grep `skills/code-review/SKILL.md` |
| A reader opens Q1 | Status is ✅ with the answer (keep 1.2), the date, and who answered — in that file's own row shape | read the questions file |

## Data & interfaces

None — documents only. No schema, no endpoint, no script changes.

## Open questions → questions.md

The batch before the first edit found nothing open; the delegations it
recorded are in `questions.md`.
