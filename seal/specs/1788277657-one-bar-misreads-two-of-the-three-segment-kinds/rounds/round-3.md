# 1788277657-one-bar-misreads-two-of-the-three-segment-kinds — review round 3

<!-- Opened by the broad gate, not by a reviewer: the one full run at 6dee2ca
failed a PR #67 pin that no targeted run had reached. The orchestrator fixed
it and this round read the fix. It opened nothing needing a fix, so the run
ends here and it does not consume the cap. -->

| Field | Value |
|---|---|
| Target SHA | 0b126c4 (fix diff 6dee2ca..0b126c4, one test file) |
| PR | none yet |
| Broad gate | 6dee2ca vs origin/release/v0.3.0 — 1142 passed · 1 failed (the finding below) · 1 skipped; ruff clean; evidence --strict 69 ok · 0 drifted; unverified/chain/gather exit 0. The delta to 0b126c4 touches only the failing test file, re-run in full after the fix (31 passed) — no production code in the delta |
| Fixes checked by | no fixes to check |

<!-- The 0b126c4 fix predates this record and is what this round READ — it was
opened by the broad gate between rounds, not by a finding of this round's
own, so this round closed nothing with a fix of its own. -->

| Contract changes | none — one assertion reworded inside an existing test function; no unit's signature or returns moved |
| New units | none |
| Needs a fix | no |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | PR #67's draft pin asserted the literal `Draft 0.7`, so completing the 0.8 bump (round-1 🔴 1's fix) broke it — the pin's own class of finding, met one work item later | `tests/test_the_fixes_name_their_surface.py:476` | answered — the fix (0b126c4) predates this round; this round reproduced its closure | executed: the file at 0b126c4, 31 passed. Read: the amended pin parses the title's draft and claims a floor (>= 0.7), keeping the original claim (the rows arrived with a bump) while surviving future bumps; the regex binds line 0 only; the float comparison's one failure mode (a hypothetical draft 0.10) fails loud and red, never silently green — answered with grounds, hardening optional |

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_the_fixes_name_their_surface.py -q` at 0b126c4 | 31 passed |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-2 | `docs/review-handoff-protocol.md#"## The handoff before round 1"` | the bars section; later edits drift the map.md row by design |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain.
