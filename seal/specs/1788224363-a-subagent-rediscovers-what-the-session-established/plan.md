# Implementation Plan: a subagent rediscovers what the session established

<!-- specs/1788224363-a-subagent-rediscovers-what-the-session-established/plan.md —
HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Approval

**Approval was given in advance**, by the repository owner, on 2026-09-01, as
the five-piece scope stated on issue #29 and in the spawn instruction. The
session does not stop for a go; anything that would otherwise be raised
becomes a `questions.md` row or a `# RIDER:` comment at the coordinate it is
about.

This work sits on the top rung twice over: it changes the output of a script
people act on (`session_cost.py` — a whole day's conclusions were drawn from
its 1.00), and it changes the instructions two agents read and act on.

One instruction is unusual and comes from the owner directly: **this work
item measures its own segments with the meter it fixes.** The meter fix is
phase 1 and commits first; every later segment — this run, each review
round — is then measured with corrected counting, and the readings open the
acceptance table in `overview.md`.

## Summary

Five runs measured exactly 1.00 tools per turn because the meter could not
read anything else: `session_cost.py:95` appends a turn per `tool_use`
block, so `len(calls)/len(turns)` is structurally ~1.00. Re-counted per
message, the same six transcripts read 1.08–1.89 — task shape dominates, and
the one instructed reviewer run (1.89) was the fastest round. The fix makes
the meter able to disagree with the rule it observes.

Around it, four smaller pieces move what issue #29 established into the
documents that outlive it: the pre-round-1 handoff gets the protocol section
round N→N+1 already has, the contract-override clause is verified where it
already landed, both contracts state the batching expectation honestly, and
the protocol tells the orchestrator where the progress readout already is.

## Technical context

- `skills/verify/scripts/session_cost.py:65-118` (`load`) — turns appended
  inside `for block in content:`; usage tokens appended per block, so a
  three-call message triples its tokens in `context_growth`.
- `session_cost.py:134-139` — model time is per-call gaps. An intra-turn
  positive gap (first result arrives before the second call's row) counts
  as model thinking; a batch whose last result is not the last-started call
  overstates the next gap.
- `session_cost.py:239-244` — the `batching` line prints below 1.2 and
  asserts "going out one at a time" at any value.
- `tests/test_session_cost.py` — fixture rows are one message each, so the
  existing cases hold under per-message counting unchanged.
- `docs/review-handoff-protocol.md` — draft 0.5; the new section moves it
  to 0.6, and the Status section records why.
- `agents/warden.md` is covered by `tests/test_docs_line_wrap.py` (88
  display columns); `agents/smith.md` is not, but new prose stays wrapped.
- Failure scenario of the chosen approach: a harness change that stops
  writing `message.id` degrades every row to its own turn — the reading
  falls back to 1.00, the pre-fix floor, rather than inflating. The
  degradation is in the safe direction and the fixture without ids pins it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Key turns on `message.id`, fall back to row `uuid`, then to the row itself | A transcript with none of the three reads one turn per row — the pre-fix floor, never an inflated ratio | **Chosen** |
| Cluster calls into turns by timestamp proximity | A slow batch reads as two turns; a fast serial pair reads as one. The meter would disagree with the transcript, not with the behaviour | Rejected |
| Count only Bash calls toward turns | Read/Edit batches are the common case the rule is about; the meter would miss exactly what it exists to see | Rejected |
| Model time: keep per-call gaps, document the caveat | The named case — first result before the second call's row — books the intra-turn wait as model thinking, which is the misattribution the owner asked checked. Fixing it is ~15 lines (tag calls with their turn, gap only across turns, from the turn's last end), which is separable, so it is built rather than deferred | Rejected in favour of turn-aware gaps |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `session_cost.py` counts turns per message, tokens once per message, turn-aware model time, honest `batching` wording | new cases in `tests/test_session_cost.py` shown red against the pre-fix code, then green; existing cases stay green; then this run measured with the fixed meter | `2a0e0fc` |
| 2 | the pre-round-1 handoff section in `docs/review-handoff-protocol.md` (coordinates not prose, the three labels, where to measure) and the progress-observability paragraph (Status column, stall signal, `session_cost.py`); pointers from `skills/implement/SKILL.md` and `agents/smith.md` | `tests/test_the_handoff_before_round_one.py` written first and shown red, then green; `test_handoff_outlives_the_merge.py`, `test_review_axes.py` stay green | `2a65ab7` |
| 3 | the batching expectation in both agent contracts — what goes out together in `agents/warden.md`, the same rule with the serial-loop caveat in `agents/smith.md`; piece 3 verified already present by executing its suite | same new suite; `test_broad_gate_rule.py`; `test_docs_line_wrap.py` for warden.md | `eb2219f` |
| 4 | ledger rows in `.specseal/map.md` (stamped, no unescaped pipes), the changelog entry under `## Unreleased`, the closing memo with this run's own corrected reading | `evidence_check.py`; `unverified_check.py`; executed `session_cost.py --latest` | `b7d5cda` |
| R1 | round-1 fixes — the warden sentence stops comparing corrected readings against the broken meter's floor; the drift note matches what the checker actually reports and why (baseline numbering); the id-over-uuid key priority pinned; round 1's four parser and checker facts folded into the ledger | the new case shown red under the uuid-first mutation at `session_cost.py:93` and green after reverting it; `test_session_cost.py`, `test_the_handoff_before_round_one.py`, `test_docs_line_wrap.py`, `test_broad_gate_rule.py` | `8b79b46` |

This table is also where the work records how far it got: Status is empty, or
the commit that closed the phase, filled in as each phase closes.

## Operational impact

None. No migrations, no new dependencies, no new environment variables.
`session_cost.py --json` keeps its field names; the values of
`tools_per_turn`, `model_s`, `gap_mean_s` and `context_growth` change meaning
from per-block to per-message counting, so readings taken before and after
the fix are not comparable — which is the point, and the changelog says so.
