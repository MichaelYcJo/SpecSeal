# 1788277657-one-bar-misreads-two-of-the-three-segment-kinds — review round 2

<!-- The verifying round the run ends on: it opened nothing needing a fix, so
it does not consume the cap. -->

| Field | Value |
|---|---|
| Target SHA | 3a91096 (fix diff b80c2a5..3a91096; record commit 26705c7 between, records only) |
| PR | none yet |
| Broad gate | not yet — the orchestrator's one full run follows this record; its SHA lands here |
| Fixes checked by | no fixes to check |
| Contract changes | none — this round wrote no fixes |
| New units | none |
| Needs a fix | no |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1-1 | round-1 🔴 1 (Status line 0.7 under a 0.8 title) | `docs/review-handoff-protocol.md:415` | answered — the fix is round-1's, this round reproduced its closure | the line now reads `Draft 0.8, extracted`; the draft-equality pin failed under mutation (0.8→0.7) and passes at HEAD |
| 🟢 1-2 | round-1 🟡 2 (range read as the complete record) | `docs/review-handoff-protocol.md:367` | answered — the fix is round-1's | the sentence now scopes itself ("not the complete record: the same issue holds a 2.0 baseline and a later chain at 1.10–1.54"); both figures match what round 1 verified against the issue; the bar is unchanged |
| 🟢 1-3 | round-1 🟡 3 (stale Checked date) | `.specseal/map.md:97` | answered — the fix is round-1's | Checked → 2026-09-02; the row's hash and the fragment's bars-row hash both moved with 🟡 2's edit and were recomputed post-fix — `evidence_check.py --strict .` at 3a91096: 69 ok · 0 drifted · 0 broken, executed this round |
| 🟢 1-4 | the four new test functions, judged as code (round-1's New units surface) | `tests/test_the_handoff_before_round_one.py:115`, `tests/test_review_axes.py:128` | answered — judged correct | executed: one mutation probe with four simultaneous mutations (bar ≥1.8→≥1.9, Status 0.8→0.7, session_cost constant 1.2→1.3, resume sentence reworded) — 4 failed, each on exactly its own target, 13 pre-existing undisturbed; clean rerun 28 passed. Read: the cross-instrument regex binds session_cost.py:269 and nothing else (275 is `<=`, 289 is `>=`); first-match rebinding is a recorded brittleness that still fails toward a mismatch, never a silent pass |

## Executed probes

| What was run | Result |
|---|---|
| mutation probe: four simultaneous mutations, then `git restore` (tree confirmed clean) | 4 failed — each pin on its own target — 13 passed |
| clean rerun of the two pin files + wrap tests at 3a91096 | 28 passed |
| `evidence_check.py --strict .` at 3a91096 | 69 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/review-handoff-protocol.md#"## The handoff before round 1"` | the bars section lives inside this anchored region; any later edit drifts the map.md row, by design |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain.
