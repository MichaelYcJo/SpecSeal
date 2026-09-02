# 1788310269-the-implementer-leaves-a-mark — review round 2

<!-- Opened by the broad gate, not by a reviewer: PR #75's first CI run failed
one test on all three OS after round 1 had closed. The orchestrator fixed it
and this round read the fix. It opened nothing needing a fix, so the run ends
here and it does not consume the cap. -->

| Field | Value |
|---|---|
| Target SHA | a50157f — the fix diff `976a3f5..a50157f`, one test plus a re-hashed anchor, not the branch |
| PR | #75 |
| Broad gate | 976a3f5 vs origin/release/v0.3.0 locally (1200 passed · 1 skipped, ruff clean, `--strict` 141 ok, chain/unverified exit 0); the edit after it touched one test file only, and PR #75's CI at a50157f is the broad evidence for this HEAD: lint, ledger, release, pytest on ubuntu, macos and windows all green |
| Fixes checked by | no fixes to check |
| Contract changes | none — a test's session ids changed; no unit moved |
| New units | none |
| Needs a fix | no |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | The S13 test compared the worktree guard's output across three dispatch calls under one session id; the guard is stateful per session (`already_asked`: one two-option `deny`, then the short `ask` fallback), so `after != intact` was the guard's own state, not the mark gate. CI's runner has no ps/lsof and reaches that site; macOS reached another and never showed it | `tests/test_the_implementer_is_recorded.py:185-204`, `hooks/worktree-guard.py:1206-1278` | answered — closed by a50157f (fresh session id per call), which predates this round; this round reproduced the mechanism and the closure | reviewer, thin PATH: same id ×3 → `deny, ask, ask`; fresh ids ×3 → `deny` ×3, byte-identical, the reason naming ps/lsof. Orchestrator: thin PATH, the test failed before the change and passed after |
| 🟢 2 | With fresh ids the comparison is the guard's full first-call `deny` body with the mark gate intact, unparseable and absent — a heavier comparison than the fallback text CI had been comparing, and nothing the test claimed is lost | same | pass | read and executed |
| 🟢 3 | No other guard state leaks across the three calls: the only file the guard writes is keyed by session and scope; the lease is written by `session-lease.py` in the post groups, which `pre-agent` never runs; the mark file the first call leaves is not read by a broken gate and produces no output when intact | `hooks/worktree-guard.py:1230-1235`, `hooks/session-lease.py:112-119`, `hooks/dispatch.py:37` | pass | executed: after three calls the git dir holds `specseal-implementer` and `specseal-worktree-choice/create/` only |
| 🟢 4 | The re-hashed anchor on the S13 test resolves | `.specseal/map/1788310269-the-implementer-leaves-a-mark.md:13` | pass | `--strict` 141 ok · 0 broken |
| 🟡 5 | The pull-request bodies said the chain was one round; with this round that sentence is false | `specs/1788310269-the-implementer-leaves-a-mark/pr.ko.md:35-38`, the English body | answered — both bodies now say two rounds and what the second read | orchestrator edited both in this commit |

## Executed probes

| What was run | Result |
|---|---|
| normal PATH — the new test file + `test_dispatch.py` | 32 passed (reviewer and orchestrator) |
| thin PATH (python3, git, uv only; `which ps`/`lsof` None) — S13 alone, then the two files | 1 passed; 32 passed |
| thin PATH — `pre-agent` ×3 under one session id, then under three ids | `deny, ask, ask`; `deny` ×3 byte-identical |
| orchestrator, thin PATH — S13 before the fix / after | 1 failed / 1 passed |
| `evidence_check.py --strict .` | 141 ok · 0 drifted · 0 broken |
| PR #75 CI at a50157f | six checks green, windows included |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/dispatch.py:37` — the `pre-agent` group | the guard and the mark gate share it; S13 is the pin that they do not see each other |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain — round 1's deferrals stand as recorded there.
