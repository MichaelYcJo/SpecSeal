# 1788305134-the-reader-stops-where-it-need-not — review round 1

| Field | Value |
|---|---|
| Target SHA | 9eee4cd |
| PR | none yet |
| Broad gate | not yet — the one full run follows the chain |
| Fixes checked by | round-2 |
| Contract changes | `hooks/cmdline.py#_nesting` `(tokens) -> int` became `(tokens, stack) -> list` → `walk_directories` (`:1744`), `tests/test_a_path_the_command_wrote_out.py::test_what_opens_a_body_and_what_closes_one`; `#_bind` empties a name whose value starts with `(` → `walk_directories`; `#_forget` forgets `((NAME=`, every `let` operand's leading name, and `${NAME:=`/`${NAME=` in any token → `walk_directories`; `#_unseen` treats `let` the same → `walk_directories` |
| New units | `hooks/cmdline.py#_leads`, `#CLOSES` (and `CLOSERS` derived from it), `#_definitions`; `tests/test_the_reader_agrees_with_bash.py` (`usable_bash`, `WRAPPERS`, `STATEMENTS`, `answers`, `bash_answers`, two tests); in `tests/test_a_path_the_command_wrote_out.py`: `test_what_opens_a_body_and_what_closes_one`, `test_an_array_assignment_empties_the_name`, `test_a_call_to_a_function_the_string_defined_empties_the_environment`, `test_the_writers_round_one_found_are_forgotten` |
| Needs a fix | yes — 🔴 2 (a multi-line `case` arm's `pattern )` closes the body count, so the arm's assignment binds) and 🔴 3 (`f(){` is not counted as an opener, so the body's second statement binds); with them the record fixes 🟡 1, 🟡 5, 🟡 6 |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Stage 1: `spec.md` states what the item became (a verification, and the defect it found) and the overview names who answers each Not-verified row; but the grounding row citing `_heredoc_split — … 51 shapes` quotes a sentence this tree does not carry (the measurements near it read six and eight shapes) | `specs/1788305134-the-reader-stops-where-it-need-not/spec.md:14` | fixed — round-2 read the fix diff (f0442a7, 3cf7856) and reproduced the closure | `grep -n '51 shapes' hooks/cmdline.py` returns nothing; the sentence travelled from the orphaned branch. Re-point the row at what the tree says |
| 🔴 2 | A multi-line `case` whose arm pattern stands on its own line — `a )` — is read as a subshell closer because `)` counts when it is the segment's last token; the count drops to 0 before the arm body, and `SB=/three` in a non-matching arm binds. bash: `/one`; reader: `/three`, a commit let through unasked | `hooks/cmdline.py:986` | fixed — round-2 read the fix diff (f0442a7, 3cf7856) and reproduced the closure | orchestrator reproduced through the gate's own pipeline (`drop_heredoc_bodies` → `split_segments_with_separators` → `walk_directories` → `parse_git` → `compose`): `['/three']`. The one-line spelling `case x in a ) SB=/three ;; esac` prompts; the difference is the newline alone. Reviewer's fix: keep a stack of open bodies instead of an integer and let `)` close only when `(` is on top |
| 🔴 3 | `f(){ echo hi; SB=/three; }` — the glued `f(){` is neither in `OPENERS` nor a `(`-prefixed token, so no body opens and the second statement binds at depth 0. bash: `/one`; reader: `/three` | `hooks/cmdline.py:984` | fixed — round-2 read the fix diff (f0442a7, 3cf7856) and reproduced the closure | orchestrator reproduced: `['/three']`; the splitter yields `['f(){', 'echo', 'hi']`. Reviewer's fix: a token ending in `(){` opens a `{` body |
| 🟡 4 | A function defined, then a top-level assignment, then the call: `f() { SB=/three; }; SB=/one; f; git -C "$SB"` — bash `/three`, reader `/one`. The call `f` passes `understood` as a simple command and nothing forgets `SB`. Pre-dates this branch; the rewritten comment calls it the alias open edge, but the function's name is in the string and the reader can see it | `hooks/cmdline.py:1631-1640`, `:1175` | fixed — round-2 read the fix diff (f0442a7, 3cf7856) and reproduced the closure | reviewer's probe C, old and new reader alike. Fix shape: collect `NAME()` / `function NAME` definitions and, when that name arrives in command position, empty the environment as `OPAQUE` does |
| 🟡 5 | Q4's record says both remaining costs are prompts; measured, any command inside a body whose last argument is `")"` closes the body early and the assignment after it binds (`if false; then echo ")"; SB=/three; fi` → reader `/three`, bash `/one`). The stack fix closes the `")"` case; a bare `"fi"` in command position remains, and the record has to say exactly that | `specs/…/questions.md:272`, `specs/…/spec.md:66-69`, `.specseal/map/1788305134-the-reader-stops-where-it-need-not.md:342` | fixed — round-2 read the fix diff (f0442a7, 3cf7856) and reproduced the closure | reviewer's probes D and E; orchestrator reproduced D |
| 🟡 6 | "No new prompt on a shape that resolved correctly before" is not what the diff does: nested `if`, `elif`, `git commit -m "(wip) x"; SB=/two`, `grep -c '(' f; SB=/two`, `time { …; }` resolved before and prompt now, because a `(`-prefixed token counts as an opener anywhere. Safe direction, wrong sentence; narrowing `(` to command position (or after a reserved word / prefix) would remove the two everyday cases | `specs/…/plan.md:248-252`, `hooks/cmdline.py:984` | fixed — round-2 read the fix diff (f0442a7, 3cf7856) and reproduced the closure | reviewer's probes G, J, P, Q, R against the dd7e45e reader |
| 🟡 7 | An array assignment `SB=(/three)` binds the value `(/three)`, so `git -C "$SB"` composes `/session/(/three)`; bash uses `/three`. `_bind`'s docstring says unmodelled shapes empty the name, and a `(`-initial value is not among them. Pre-dates the branch | `hooks/cmdline.py:1030-1033` | fixed — round-2 read the fix diff (f0442a7, 3cf7856) and reproduced the closure | reviewer's probe M. One line: bind only when the value does not start with `(`, else `env.pop(name, None)` |
| 🟡 8 | Three name-writing forms not modelled: ① `((SB=3))` and `let "SB = 3"` (reader keeps `/one`; bash `3`); ② `: "${SB:=/three}"` — `${NAME:=…}`/`${NAME=…}` writes the name from any argument position (reader `/session`, bash `/three`); ③ `declare -n ref=SB; ref=/three` — nameref, bash ≥ 4.3, not executable here. `NAME_WRITERS` otherwise covers `read`, `mapfile`/`readarray`, `getopts`, `let`, `printf -v`, `unset`; `declare`/`local`/`export` fall to the `=` scan | `hooks/cmdline.py:778`, `:783-836` | fixed for ① and ② — round-2 reproduced; ③ answered — deferred to the overview's Not verified for a bash 5 machine | reviewer's probes F, F2, L; ③ read only |
| 🟢 9 | `understood` narrows and its single caller inherits fail-closed: `False` becomes `Unresolved(CONSTRUCT)` and the environment goes through `_unseen`; `_runs` does not call it | `hooks/cmdline.py:1234`, `:1538-1544` | pass | read; `time for` and `! for` prompt |
| 🟢 10 | Tests: 297 passed in the six files that import the reader, 0 skipped; no `bash` spawn in the new tests; the smith's two mutations re-run red (`depth = 0` → 2 failed; `understood` guard → `if False:` → 1 failed) | `tests/test_a_path_the_command_wrote_out.py:743-866` | pass (executed) | reviewer's run |
| 🟢 11 | Ledger fragment: 33 anchors resolve, 104 ok tree-wide; rows 4, 5, 6 opened and their claims match the code — row 5's Notes carry the 🟡 5 sentence | `.specseal/map/1788305134-the-reader-stops-where-it-need-not.md:341-343` | pass (executed) | `evidence_check.py --strict .` |
| 🟢 12 | Repo rules: no `CHANGELOG.md` / `.specseal/map.md` append; no legacy issue numbers in the diff; commit subjects in form; fragment in the siblings' shape. Outside the diff, the same test file's lines 4, 14, 126, 313, 350 still carry `Issue #82` / `issue #56` from the legacy repository | `git diff dd7e45e..9eee4cd` | answered | not this diff's fault; the fix pass touches that file and drops them |
| 🟡 13 | The differential generator (26 wrappers × 70 statements against bash) lives in a session scratchpad, not the tree; `plan.md` says a next reader can re-run it. Its 26 wrappers are all one-line, which is why 🔴 2 and 🔴 3 escaped it. A guarded test (`usable_bash`, multi-line wrappers) is the regression net | `specs/…/plan.md:200-202`, `overview.md:162` | fixed — round-2 read the fix diff (f0442a7, 3cf7856) and reproduced the closure | read; scratchpad file confirmed |

## Executed probes

| What was run | Result |
|---|---|
| pytest (3.12, xdist) — the six files `grep -l cmdline tests/*.py` names | 297 passed, 0 skipped (reviewer) |
| `evidence_check.py --strict .` | 104 ok · 0 drifted · 0 broken (reviewer) |
| mutation `depth = max(0, …)` → `depth = 0` | 2 failed (`bodys_later_statement`, `glued_closer`); restored |
| mutation `understood`'s new guard → `if False:` | 1 failed (`reserved_word_behind_a_prefix`); restored, `git diff --quiet` |
| reviewer's 26 shapes `SB=/one; <middle>; git -C "$SB" commit -m x` against bash 3.2.57 | 🔴 A, A2, B; 🟡 C, D, E, F, F2, L, M answer where bash disagrees; G, J, P, Q, R newly prompt; N fixed; the rest agree or prompt |
| reviewer's stack-based patch on a copy | A, A2, B, D, S all prompt; the smith's 16 BODIES shapes and 7 body-ends shapes unchanged; cost: a matching `case` arm (A3) prompts too |
| orchestrator: shapes A, B, D, U, N through the gate's pipeline | A `['/three']`, B `['/three']`, D `['/three']`, U `['/session/$SB']` (prompt), N `['/session/$SB']` (prompt) — 🔴 2, 🔴 3, 🟡 5 confirmed |

## Prescribed regression tests

| Asserts | Destination | Grounds |
|---|---|---|
| `BODIES` gains the multi-line `case` with `a )`, `f(){ echo hi; SB=/three; }`, and `if false; then echo ")"; SB=/three; fi` — `$SB` must stay unresolved | `tests/test_a_path_the_command_wrote_out.py::BODIES` | 🔴 2, 🔴 3, 🟡 5 |
| after `esac` an assignment binds again (multi-line `case`, then `SB=/three`) | same file, `test_the_body_ends_at_its_closer` | the stack pops `case` at `esac` |
| `f() { SB=/three; }; SB=/one; f; git -C "$SB"` prompts | same file | 🟡 4, if fixed |
| `SB=(/three); git -C "$SB"` prompts | same file, beside the `_bind` tests | 🟡 7 |
| a differential test: wrappers × statements, compared with bash only when `usable_bash()`; whatever the reader answers must equal bash's answer; wrappers include multi-line `case` (`a )`, `a)`, `(a)`), `f(){`, nested `if`, `elif` | new `tests/test_the_reader_agrees_with_bash.py`, guard as in `tests/test_evidence_check.py::usable_bash` | 🟡 13 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 8 ③ — nameref (`declare -n`) on bash ≥ 4.3 | `specs/…/overview.md` Not verified | a maintainer with bash 5 |

Everything else goes to the fixing session (smith, resumed).
