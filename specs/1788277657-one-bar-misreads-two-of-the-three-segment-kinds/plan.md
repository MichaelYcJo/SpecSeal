# Implementation Plan: one bar misreads two of the three segment kinds

<!-- specs/1788277657-one-bar-misreads-two-of-the-three-segment-kinds/plan.md —
HOW, in phases. This work alters what sessions read and act on, so approval
of this plan is the gate; the owner's overnight authorization delegates that
approval (recorded in questions.md). -->

## Summary

Three decisions the repository owner made on 2026-09-01 become written rules
where their readers already look: the per-segment acceptance bars go beside
the meter pointer in `docs/review-handoff-protocol.md`, the resume-not-respawn
rule for fix passes goes in `skills/code-review/SKILL.md`'s orchestrator
sections, and Q1 of the 1788224363 work item is marked answered (keep 1.2).
No code changes.

## Technical context

- `docs/review-handoff-protocol.md` §While the implementer runs — ends at the
  paragraph pointing at `session_cost.py` ("It sat unreferenced through a
  full day of measurements nobody took"). The bars section lands directly
  after it, inside `## The handoff before round 1`. The draft number moves
  (0.7 → 0.8) per the document's own Status convention.
- `skills/code-review/SKILL.md` — the orchestrator sections say when the
  verifying round runs ("after the fixes … are committed") and carry no
  sentence about how the fixing session is obtained. The new section lands
  between `## Cross-session records` and `## Orchestrator: the run ends with
  a verifying round`, as a `##` of its own so the anchored regions on either
  side keep their content. This file is line-wrap covered (88 columns).
- `agents/smith.md` step 5 carries the serial-loop caveat — "measured at
  1.08–1.17 tools per turn where review rounds read 1.29–1.89 — and it is
  not forced to fake a batch". The bars quote the same ranges, so the two
  stay consistent without editing the agent contract (and without drifting
  the four ledger rows whose minor anchors sit in that section).
- Ledger rows that will drift and be re-verified: `.specseal/map.md`'s
  `docs/review-handoff-protocol.md#"## The handoff before round 1"` row
  (this work edits inside that region and re-reads it).

**Failure scenario of the chosen approach** (what breaks in 6 months): the
bars (1.8) live in the protocol while the advisory (1.2) lives in the
script, and a reader meeting both without the sentence tying them together
reads a contradiction. The bars section carries that sentence — the script
cannot tell segment kinds apart, so its advisory sits where it does not nag
the serial case — and if the script's threshold ever moves, that sentence is
the single place to update.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Bars in `agents/warden.md` + `agents/smith.md`, each party self-judging | the orchestrator is the party doing the judging, and it reads the protocol's meter paragraph; bars split across two contracts drift apart on the next edit to either | rejected |
| Bars enforced inside `session_cost.py`, per-segment warnings | the script cannot tell a reviewer's transcript from an edit-test loop (Q1's own grounds), so it nags the serial case — and the script is out of scope by the owner's decision | rejected |
| Resume rule in the protocol document | the protocol is tool-agnostic file shapes; obtaining a session is runtime procedure, which is what the code-review skill's orchestrator sections hold | rejected |
| Bars in the protocol (§After the run), resume rule in the code-review skill | the split-instrument confusion above — mitigated by the tying sentence | **chosen** |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | SDD set (spec, plan, questions) committed | files in the tree at the phase commit | c37cccb |
| 2 | per-segment bars in the protocol, draft 0.8 | `pytest tests/test_the_handoff_before_round_one.py` green; wrap/one-word/identifier tests on touched files | 8e81271 |
| 3 | resume rule in the code-review skill | `pytest tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py tests/test_no_real_identifiers.py` green (file is wrap-covered) | 14a5702 |
| 4 | Q1 marked answered; changelog + ledger fragments; overview; drifted row re-verified | `evidence_check.py --strict .` clean | 9f75df3 |

## Operational impact

None — documents only. No migrations, no env vars, no dependencies, no
compatibility breaks.
