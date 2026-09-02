# 1788305134-the-reader-stops-where-it-need-not — review round 2

<!-- Spawned as the verifying round over round 1's fixes (the diff
cc30ee0..356d116). It closed every round-1 verdict and opened one 🔴 of its
own on the finding surface, so it is a finding round and consumes the cap;
round 3 verifies its fix. -->

| Field | Value |
|---|---|
| Target SHA | 356d116 — the fix diff `cc30ee0..356d116` (code at f0442a7), not the branch |
| PR | none yet |
| Broad gate | not yet — the one full run follows the chain |
| Fixes checked by | nobody — the fix pass for 🔴 N1 has not run yet; round 3 sets this |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — N1: inside a subshell body, a spaced `)` belonging to `SB=( a b )`, `SB=$( pwd )` or `<( … )` pops the subshell's `(`, so the assignment after it binds at top level (`hooks/cmdline.py:1046-1049`); N2's `TimeoutExpired` handling in `usable_bash` is optional |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | Round 1's 🔴 2 — a multi-line `case` arm's `a )` closed the count | `hooks/cmdline.py:1046-1049` | answered — closed by f0442a7, which predates this round; this round reproduced the closure | reviewer's probes A and A2 now prompt (bash `/one`); the matching arm A3 prompts too, the cost the record names. Orchestrator reproduced A through the gate's pipeline: `['/session/$SB']` |
| 🟢 2 | Round 1's 🔴 3 — `f(){` opened no body | `hooks/cmdline.py:1041-1042` | answered — closed by f0442a7; reproduced | probe B prompts; orchestrator reproduced: `['/session/$SB']` |
| 🟢 3 | Round 1's 🟡 1 — the `51 shapes` grounding row | `specs/…/spec.md:13` ↔ `hooks/cmdline.py:405-408` | answered — closed by 3cf7856; the quoted sentence is in the tree | read |
| 🟢 4 | Round 1's 🟡 4 — a defined function's call left the environment standing | `hooks/cmdline.py:1053-1075`, `:1682-1691` | answered — closed by f0442a7; reproduced | probe C prompts (bash `/three`); `command f`, a body-defined function called outside, both prompt; `echo "cd()"; SB=/two` still resolves |
| 🟢 5 | Round 1's 🟡 5 — Q4 said both remaining costs were prompts | `specs/…/questions.md:14`, `spec.md:82-88`, ledger row 5 Notes | answered — partly by code (probe D `echo ")"` prompts now), the rest by the record, which names the one shape that still answers where bash disagrees: a quoted closer as a sole command inside a body (`"fi"`) | probe E still `/three`; the record says exactly that |
| 🟢 6 | Round 1's 🟡 6 — "no new prompts" | `specs/…/plan.md:131-146` | answered — the paragraph was rewritten from a 2,109-input measurement and matches the probes: G, J, R prompt (bodies that do run); P, Q resolve again | executed against both readers |
| 🟢 7 | Round 1's 🟡 7 — array assignment bound `(/three)` | `hooks/cmdline.py:1121` | answered — closed by f0442a7; reproduced | probe M prompts |
| 🟢 8 | Round 1's 🟡 8 ①② — `((SB=3))`, `let`, `${SB:=…}` | `hooks/cmdline.py:815-825`, `:839-843` | answered — closed by f0442a7; reproduced | probes F, F2, L prompt; `let x=SB+1` and `${SB:-}` keep `/one`. ③ nameref stays in the overview's Not verified for a bash 5 machine |
| 🟢 9 | Round 1's 🟡 13 — the differential lived outside the tree | `tests/test_the_reader_agrees_with_bash.py` | answered — closed by f0442a7; the in-tree run is 675 inputs, 307 compared as answers, 0 disagreements, and each input runs in its own `( eval …; printf ) </dev/null` subshell so no name or `cd` leaks to the next | executed |
| 🔴 N1 | Inside a subshell body, a spaced `)` that belongs to `SB=( a b )`, `SB=$( pwd )` or `<( … )` is the segment's last token with `(` on top of the stack, so it pops the subshell; the assignment after it binds at top level. bash `/one`, reader `/three`. Not a regression of this fix (dd7e45e answered the same), but it is in the reviewed unit and in the class the item says it closed | `hooks/cmdline.py:1046-1049` | open | reviewer's W1–W3; orchestrator reproduced W1 and W2 through the gate's pipeline: `['/three']`. Fix (validated on a copy): a `)` is not the subshell's when an earlier token of the segment ends in `(` without starting with `(`; leaving the `(` open costs a prompt |
| 🟡 N2 | `usable_bash` catches `OSError` only; a `TimeoutExpired` at collection would be an error, not a skip. On windows-latest Git Bash is present, so the differential probably runs rather than skips there | `tests/test_the_reader_agrees_with_bash.py:33-44` | open (❓ on Windows — the PR's CI answers) | read; `test.yml:35-37` |
| 🟢 N3 | The differential's exemption is exact: only paths with `$` left are prompts; an absolute `-C` composed over an unresolved shell is an answer and is compared | `tests/test_the_reader_agrees_with_bash.py:143-166` | pass | executed: 675 inputs, 307 compared, 0 disagreements; the floor (`//4`) is a floor, not a pin |
| 🟢 N4 | `_leads`: a `(pattern)` on its own line pushes `(` that `esac` cannot pop, so the rest prompts — safe direction, consistent with the docstring's uncounted-opener argument | `hooks/cmdline.py:978-993` | pass | executed X1; mutation `return True` reddens the `(wip)` / `grep -c '('` pins |
| 🟢 N5 | `_definitions` collects `f()`, `f ()`, `f(){`, `function f`; the call check runs on `_runs`, so `then f`, `time f`, `command f`, `true && f` all reach it | `hooks/cmdline.py:1053-1075`, `:1682` | pass | executed X3, X4 |
| 🟢 N6 | Contract: `_nesting(tokens) -> int` became `(tokens, stack) -> list`; callers are `walk_directories:1744` and the renamed test only. `_leads` is called by `_nesting` alone, `_definitions` by `walk_directories:1745` alone. `walk_directories` signature unchanged. Legacy issue numbers gone from the test file | `git diff cc30ee0..356d116` | pass | grep |

## Executed probes

| What was run | Result |
|---|---|
| pytest (3.12) — six reader files + the differential | 302 passed · 0 skipped (reviewer) |
| mutation: `stack.pop()` removed | 2 failed (after-`esac` pin, `after("( echo hi )") == []`); restored |
| mutation: `_leads` → always True | 2 failed (`(wip)` / `grep -c '('` pins); restored |
| `evidence_check.py --strict .` | 43 ok in this fragment · 114 ok tree-wide · 0 broken |
| `ruff check` / `ruff format --check` on three files | clean |
| reviewer's shapes against dd7e45e, 356d116 and bash 3.2.57 | A, A2, B, C, D, F, F2, L, M → prompt; P, Q → `/two`; E → `/three` (the recorded remainder); W1–W3 → `/three` (N1) |
| N1 fix on a copy | W1–W3 prompt; W5–W7 keep `/three`; the 23 BODIES shapes prompt; 675-input differential 307 answers · 0 disagreements |
| orchestrator: W1, W2, A, B through the gate's pipeline | W1 `['/three']`, W2 `['/three']`, A and B `['/session/$SB']` |

## Prescribed regression tests

| Asserts | Destination | Grounds |
|---|---|---|
| W1 `( echo hi; SB=( a b ); OT=/three; true )` and W2 with `SB=$( pwd )` keep `$OT` unresolved | `tests/test_a_path_the_command_wrote_out.py::BODIES` | N1 |
| W5 `SB=( a b ); ( echo hi ); OT=/three` and W6 `X=$( pwd ); OT=/three` resolve to `/three` | same file, `test_the_body_ends_at_its_closer` | the fix must not swallow a top-level `)` |
| `STATEMENTS` gains `SB=( a b )` and `X=$( pwd ); SB=/three` | `tests/test_the_reader_agrees_with_bash.py` | so the `( {c} )` wrapper catches N1's class |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/cmdline.py#_nesting` (`:1046-1049`) | the `)` rule — N1 lives on the same line the stack fix rewrote |
| round-1 | `tests/test_the_reader_agrees_with_bash.py` | the in-tree oracle; N2's guard is its first lines |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 N2's Windows half — whether the differential runs or skips on windows-latest | the pull request's CI | the windows leg |

Everything else goes to the fixing session (smith, resumed).
