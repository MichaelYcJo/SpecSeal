# 1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in — review round 3

<!-- seal/specs/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in/rounds/round-3.md —
the verifying round the run ends on, a second time: round 2 had ended it,
then PR #95's windows leg opened 🔴 M after the record. This round opened
that fix (f3d15ca..46c658d) and nothing needing a fix, so it does not
consume the cap. Written by the review orchestrator after the report was
verified and the broad gate ran again. -->

| Field | Value |
|---|---|
| Target SHA | 319ea92 (the fix diff is f3d15ca..46c658d; 319ea92 is round-2's record edit only) |
| PR | #95 |
| Broad gate | 319ea92 vs origin/release/v0.5.0 — `pytest tests/ -n auto` 1369 passed · 1 skipped, `ruff check .` clean, `ruff format --check .` 80 files formatted, `evidence_check.py --strict .` 299 ok · 0 drifted · 0 broken, `unverified_check.py --baseline` exit 0 (14 overviews · 32 open · 15 closed · 0 unreadable). Run again because 46c658d edited a test file after the ab66282 run; the delta after this run is this record, round-2's `Fixes checked by` cell, one Evidence sentence in `seal/ledger.md` and one clause in `overview.md` — docs-only, the non-invalidating class |
| Fixes checked by | no fixes to check |
| Contract changes | none — this round wrote no fixes |
| New units | none |
| Needs a fix | no |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 2-M | round-2 🔴 M (the second gate-prompt assertion spelled the path with slashes; the windows leg failed) | `tests/test_routing_is_recorded.py#test_the_second_prompt_names_it_too` | answered — the fix is 46c658d's, this round reproduced its closure | executed: the five-file slice 195 passed; `ntpath.join` of the four parts contains the old literal → False and the new expression → True, `posixpath` both True, so the old assertion failed only on Windows and the new one holds on both; the finding itself re-read from run 33643327406's log (one failure, 1347 passed, 22 skipped); `git show --stat 46c658d`: three files, no hook line |
| 🟢 grep | the smith's claim that no other `/`-literal compares a hook's printed path | `tests/*.py` | truthful | 79 hits of the first grep and 55 of a wider one classified by the reviewer: fixture writes, document text, negative assertions, `pathlib` checks, docstrings; `root-migrate.py` prints posix spellings from its constants and its cases passed on the windows leg |
| 🟢 fix-surface | round-2's `Contract changes: none` / `New units: none` for 🔴 M | `rounds/round-2.md` | truthful | the diff holds one assertion, one ledger row, one overview clause |
| 🟡 A | the re-hashed ledger row's Evidence cell cited the 947-case run at the old hash as if it covered the new assertion | `seal/ledger.md` (the routing-recorded row) | answered — the Evidence sentence now says which run covered which assertion; a ledger sentence in this record's commit, no code | read |
| 🟢 B | `overview.md`'s Windows row said "every other case passed on that leg"; 22 were skipped by their own platform guards | `overview.md` Not verified | answered — the clause added in this record's commit | read (the CI log) |
| carried | round-2's other verdicts (🔴 1-1 … 🟢 D) | — | carried, not re-judged | the fix diff touched none of their surfaces |

## Executed probes

| What was run | Result |
|---|---|
| the five gate-and-path test files, `-q -n auto` | 195 passed |
| `ntpath.join` / `posixpath.join` of the four parts against the old literal and the new expression | ntpath: old False · new True; posixpath: both True |
| `evidence_check.py --strict .` | 299 ok · 0 drifted · 0 broken |
| `gh api …/runs/33643327406/jobs`, `gh run view --log-failed` | windows only, at f3d15ca, exactly the one case; 1 failed · 1347 passed · 22 skipped |
| `git show --stat 46c658d`, `git log -S` for both assertions | three files, no hook; the first assertion moved at 018f0c2, the second at 46c658d |
| two greps over `tests/*.py`, classified | no printed-path literal left |
| the broad gate at 319ea92 (orchestrator) | see the field above |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-2 | `hooks/commit-review-gate.py#declaration_hint` | every assertion on the hint follows this unit's spelling |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ❓ 1-8 the REMOVED rule and multi-anchor rows | the PR body | the repository owner |
| S11 the two-drive shape on a real Windows machine; Q9 the template on a runner; `evidence-check .` by CLI from a linked worktree | the PR body's Not verified | CI / the owner |
