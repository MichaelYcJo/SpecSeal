# 1788224363-a-subagent-rediscovers-what-the-session-established — review round 1

| Field | Value |
|---|---|
| Target SHA | `01c8fda` |
| PR | not yet |
| Broad gate | not yet |
| Fixes checked by | `round-2` |
| Needs a fix | yes — three 🟡, no 🔴 |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A shipped contract compares the corrected meter's 1.89 against the broken meter's structural floor — *"uninstructed rounds sat near 1.00"* — in one sentence. The same transcripts re-counted correctly read 1.29 and 1.31, and this diff's own CHANGELOG says old-meter readings are not comparable to new ones | `agents/warden.md:166-168` | **fixed** `8b79b46` | Verified by the orchestrator before the fix, read. The reviewer's replacement was applied verbatim; the 88-column wrap and both needle strings survive, executed |
| 🟡 2 | A ledger note claims its row *"Reads DRIFTED until re-stamped"*, and it reads OK. The drifted set is decided in baseline line numbering (`skills/evidence-check/scripts/evidence_check.py:100-105`), these rows carry HEAD-numbered coordinates on a base stamp, so which four trip is accidental hunk overlap — the tripwire does not actually watch the cited lines | `.specseal/map.md`, the meter section's second row | **fixed** `8b79b46` | Verified by the orchestrator, executed — the four drifted rows are `session_cost.py:64-141` and three contract/doc rows; the model-time row is not among them. The smith amended the reviewer's wording in one place, using the full path in the note so the ledger's own coordinate extractor cannot mint a BROKEN row from an abbreviation — disclosed, and evidence_check re-ran clean: 32 ok · 4 drifted · 0 broken. `overview.md`'s two sentences about the drift mapping corrected the same way |
| 🟡 3 | Nothing pins `message.id` outranking the row `uuid`. Flipping `session_cost.py:93` to uuid-first passed all 13 cases, and real rows carry both keys — the mutant reads batching as 1.0 on real data while every fixture stays green | `skills/verify/scripts/session_cost.py:93` | **fixed** `8b79b46` | The reviewer executed the escape; the smith reproduced it, planted the case, and showed it red under exactly that mutation with the other 13 green, then reverted and re-checked 14/14 |
| 🟢 4 | The meter fix itself, the six pre-red cases, the six handoff-doc cases, the piece-3 no-op (the contract-override clause has shipped since `9829412`), and the smith's self-measured 1.27 | across the diff | answered | The reviewer executed all of it: six meter cases exactly red pre-fix; six doc cases red at base; `test_broad_gate_rule` 11 passed with no collision; an independent set-based recount of the smith's transcript read **1.25** over the full 79 calls, supporting the 1.27-at-phase-4 account |
| ❓ 5 | Whether "five runs measured exactly 1.00" is five — the count has no in-repo source to check against, though docstring, spec and CHANGELOG agree with each other | the diff's prose | answered | The five readings are in this session's transcript and the issue #29 comment of 2026-09-01; outside the repository by nature. Recorded here rather than chased |
| ❓ 6 | Q1 — does the batching advisory threshold stay 1.2 or align with the 2.0 acceptance bar | `questions.md` Q1 | answered — stays ⬜ | The repository owner's. Note for the answer: the 2.0 bar itself was set against the broken meter, and the corrected baselines are 1.08–1.31 (smith) and 1.29–2.0 (warden), so the recalibration goes to the post-release performance issue the owner has asked for |

## Executed probes

| What was run | Result |
|---|---|
| The six new meter cases against the pre-fix code (reviewer) | exactly those six FAILED |
| The six handoff-doc cases with the docs reverted to base (reviewer) | all six red; the needles absent from all four base files by grep |
| `test_broad_gate_rule.py` (reviewer) | 11 passed — the no-op on piece 3 confirmed, no collision with the new batching prose |
| An independent recount of the smith transcript, set-based (reviewer) | 79 calls · 19.3m · **1.25** tools per turn |
| uuid-first mutation at `session_cost.py:93` (reviewer, then smith) | 13/13 green before the planted case; with it, only the new case red; reverted, 14/14 green |
| `evidence_check.py` before and after the note fix (orchestrator and smith) | 31→32 ok · 4 drifted · 0 broken; the drifted four match the note's new claim |
| Synthetic transcripts: split message sharing `message.id`, missing keys, unresolved `tool_use`, non-monotonic timestamps (reviewer) | four parser facts, folded into the ledger with executed/read labels |
| The reviewer's own segment, with the meter this branch fixed | **19 calls · 7 turns ≈ 2.0 tools per turn · 10.2m · repeats 0** — the first segment to hit the acceptance bar. One round trip lost to runner discovery: the spawn prompt omitted the runner incantation the new protocol section says to hand over |

The full suite and tree-wide ruff did not run — the broad gate is the
orchestrator's, once, after the rounds settle.

## Inherited coordinates

Round 1 inherits nothing. For round 2: the three fixes live in `8b79b46`
(`agents/warden.md:163-169` · `.specseal/map.md` meter section and Evidence
drift · `tests/test_session_cost.py`), the plan pin in `8c38a34`.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The acceptance bar (≥2.0) was set against the broken meter and needs recalibrating per agent kind | the post-release performance issue the owner has asked for, with this run's corrected table | the repository owner |
| The runner incantation belongs in every spawn prompt; its omission cost the reviewer one round trip | the same issue — an orchestrator habit, already documented in the protocol section this branch adds | the orchestrator |
| Seven pre-existing ledger stamps orphaned by the #48 squash | fixed on `release/v0.0.2` by #49 while this round ran; this branch picks it up at the merge before the broad gate | closed |
| Q1 | `questions.md`, ⬜ | the repository owner |
