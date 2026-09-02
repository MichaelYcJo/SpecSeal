# 1788305134-the-reader-stops-where-it-need-not — review round 3

<!-- The verifying round over round 2's fix (the diff 1688b04..5957122). It
closed both round-2 findings and opened one 🔴 of its own on the changed
branch of `_nesting`. The repository owner decided on 2026-09-02 to record
that finding rather than fix it in this item — it predates the branch, and it
is the third special case in a row on the same `)` rule — so the run ends
here, with the finding's durable home named below. -->

| Field | Value |
|---|---|
| Target SHA | 5957122 — the fix diff `1688b04..5957122`, four files, not the branch |
| PR | none yet |
| Broad gate | not yet — it follows this record |
| Fixes checked by | no fixes to check |
| Contract changes | none — the round opened nothing that was fixed |
| New units | none |
| Needs a fix | yes — N3 (reviewer): a subshell whose first statement is a subshell pops the outer `(`. Overridden by the repository owner on 2026-09-02: recorded as issue #72, not fixed in this item |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | Round 2's 🔴 N1 — a spaced `)` of `SB=( a b )`, `SB=$( pwd )`, `<( … )` popped the subshell | `hooks/cmdline.py:1059-1065` | answered — closed by 5957122, which predates this round; this round reproduced the closure | W1–W3 prompt (bash `/one`); W5–W7 resolve to `/three` (bash `/three`); the `)` skip mutated to `if False` reddens the W1 pin and a stack case. Orchestrator reproduced W1, W2, W5–W7 through the gate's pipeline |
| 🟢 2 | Round 2's 🟡 N2 — `usable_bash` caught `OSError` only | `tests/test_the_reader_agrees_with_bash.py:40-42` | answered — closed by 5957122; the reviewer injected `TimeoutExpired` and the guard returned False | executed; the Windows half stays ❓ for the PR's CI |
| 🟢 3 | The third cost the fix wrote down — `SB=( a b ) )` with both closers in one segment leaves the subshell open | `hooks/cmdline.py:1027-1034`, ledger row 5 Notes | pass | executed: that shape prompts (bash `/three`); the glued `SB=(a b) )` resolves. The docstring and the Notes say exactly this and nothing more changed |
| 🔴 N3 | A subshell whose FIRST statement is itself a subshell: `( ( echo hi ); SB=/three; true ); git -C "$SB"`. The inner `(` at position 1 is not counted (`_leads` does not read a leading `(` as a pass-through word), so the inner `)` pops the outer subshell and the assignment after it binds at top level. bash `/one`; reader `/three`. Every reader since the rewrite answers the same, so it is not a regression of this branch | `hooks/cmdline.py:978-993`, `:1059-1067` | answered — the repository owner decided to record it rather than fix it here; issue #72 carries the shape, the reviewer's one-line fix, and the orchestrator's prototype of a single rule that replaces the three special cases (33 shapes against bash: wrong answers 5 → 2, documented costs 3 → 1) | reviewer's N-d, N-d2, N-d3, N-d6; orchestrator reproduced N-d2, N-d3, N-d6 on the current reader and on a prototype copy |
| 🟢 4 | Contract and units: `_nesting(tokens, stack) -> list` and `usable_bash()` unchanged; no new `def` or constant in the diff; the two callers of `_nesting` unchanged | `git diff 1688b04..5957122` | pass | grep |

## Executed probes

| What was run | Result |
|---|---|
| pytest (3.12) — six reader files + the differential | 302 passed · 0 skipped (reviewer) |
| mutation: the `)` skip → `if False and any(` | 2 failed (W1 pin, `after("OT=( a b )", ["("])`); restored |
| `usable_bash()` with `TimeoutExpired` injected / for real | False / True |
| `evidence_check.py --strict .` | 43 ok in this fragment · 114 ok tree-wide · 0 broken |
| `ruff check` / `ruff format --check` on three files | clean |
| reviewer's N-d family (9 shapes) against dd7e45e, 5957122 and bash | N-d, N-d2, N-d3, N-d6 → `/three` on every reader, bash `/one`; N-d7, N-d8 → `/three`, bash `/three` |
| orchestrator's prototype (unmatched-paren rule) against 33 shapes and bash 3.2.57 | current reader: 5 shapes answer where bash disagrees (3 nested-subshell, 2 quote-provenance); prototype: 2 (quote-provenance only); prompts 18 on both |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-2 | `hooks/cmdline.py#_nesting` closer branch | the line N1's fix and N3 both live on; issue #72 names its replacement |
| round-1 | `tests/test_the_reader_agrees_with_bash.py` | the in-tree oracle; the Windows leg of the PR answers whether it runs or skips there |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🔴 N3 — the nested subshell's first statement, and the three special cases on `)` that one rule would replace | issue #72; `overview.md` §Not done; `questions.md` Q4; the `_nesting` row's Notes in the ledger fragment | the repository owner, who chose the deferral |
| 🟡 N2's Windows half — whether the differential runs or skips on windows-latest | the pull request's CI | the windows leg |
