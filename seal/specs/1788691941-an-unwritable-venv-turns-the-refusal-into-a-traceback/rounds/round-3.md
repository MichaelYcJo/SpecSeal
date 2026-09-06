# 1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback — review round 3

| Field | Value |
|---|---|
| Target SHA | 8232a07 |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 188 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item `1788691941`, the **run's last record**. Surface is the diff of round 2's fixes, `96b2084..HEAD`, not the branch. Base `origin/release/v0.8.3`, draft pull request #188, issue #177.

**This round ends the run whatever it finds** — `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped*. Round 1 met the floor, round 2 was the one reopening the chain allows, and this record reads round 2's fixes. Nothing you find here is fixed by a fourth round: anything open becomes an issue, its verdict reads `deferred #N`, and the pull request is labelled `chain: capped`. So report what is true and size each finding by whether the release would ship a defect, not by whether it can be closed tonight.

`close` derived `New units | SCOPE_BOUNDARIES (depth 1); own_returns (depth 1)` and `Contract changes | none`. **Those two units were reviewed by nobody** — treat them as *is this correct*, not as *did it close the finding*. Verify the derivation itself rather than inheriting it.

What round 2 recorded closed:

1. **🟡 6 — `reach_values` walked nested scopes.** `own_returns` now reads one scope's own returns and stops at every node that opens another. The pass **narrowed the reviewer's four-member boundary set to two**, on the grounds that `ClassDef` and `Lambda` are members no mutation can kill — a lambda body is an expression and cannot hold a `Return`, and a method is a `FunctionDef` the walk already stops at, so a class is reached *through* a boundary rather than past one. Both are kept as deliberate survivors in the mutation run. **Ask:** is that argument true of Python as it is, not as it reads — a lambda cannot hold a `Return` node, but check what `own_returns` does when one appears in a comprehension's scope, in a decorator, in a default argument, in a nested `async` comprehension, and in a `TypeAlias` or a `match` statement's body. And ask whether two members is a decomposition of *what can hold a return belonging to another function* or a list of the two that came to mind.
2. **⬜ 7 — the recorded limit.** Two corrections the pass measured rather than adopted: a `Starred` loses only a value reached *solely* through the unpacking, and the shadowing is a **second over-reach** rather than a miss — which the pass says made the one-over-reach claim false independently of finding 6. **Ask:** is the shadowing analysis right, and do the three live carriers now say two over-reaches in a way each one's own reader can act on.
3. **⬜ 8, 9, 10 — three records corrected**, with markers. **Ask:** does each corrected record now state something true of the code as it stands, and is any fourth record still carrying a superseded figure. Round 2's finding 8 existed because a two-item list was used where a grep was needed; the pass reports it closed this class by `git grep` and names the pattern. Judge the pattern, not the count.
4. **⬜ 11 — the separator.** One escaped in `rounds/round-1.md`. **Ask:** whether every Verdicts row in both records is five cells once escapes are accounted for, and whether the escape reads correctly to a Markdown renderer rather than merely to a splitter. The wider repair is issue **#189** and is deliberately not built.

Facts, labelled:

- **executed by the orchestrator at `f37abf1`** — `./bin/test tests/test_the_fixes_name_their_surface.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q` → 106 passed, exit 0. `uvx ruff check .` → All checks passed. `./bin/evidence-check .` unscoped → 701 ok · 2 drifted · 0 broken, the two being `templates/config.md#"# Repository config"` and `round_record.py#swallowed`, both the base's. Row widths re-counted independently with escapes removed: no six-cell row in either record.
- **read** — `.venv` carries no `ruff` module; use `uvx ruff`. The suite runs through `./bin/test`. Do not touch this repository's own `.venv`. A byte-length-identical mutation leaves a stale `.pyc` behind — round 2 was contaminated by one and recorded the warning; scrub `__pycache__` or use `python -B` between mutations.
- **unverified** — everything in the four items above.

Run the ledger check unscoped.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 2's 🟡 6 — the walk descended into nested scopes | `tests/test_the_fixes_name_their_surface.py` `own_returns` and `SCOPE_BOUNDARIES` | answered | Closed, and the two-member set is a decomposition. **Executed** at `8232a07` in a `--no-local` clone, eight mutations one at a time with `__pycache__` scrubbed and `-B` between them: drop `ast.FunctionDef` exit 1 (2 failed); drop `ast.AsyncFunctionDef` exit 1 (1); delete the boundary skip exit 1 (3); delete the yield of the child's value exit 1 (12); delete the recursion exit 1 (3); iterate `ast.walk` instead of `ast.iter_child_nodes` exit 1 (19); revert the call site to the blanket `ast.walk` exit 1 (3), which reproduces the record's *three of the four new fixtures red* exactly. Both boundary members are individually killable, which the four-member version could not say. **Executed**, 24 shapes the prompt named or implied, all correct: a decorator, a default argument and a return annotation on a nested `def` derive nothing; a nested `class` inside a `class`, and an `async def` method, derive nothing; a `match` statement, a `while/else`, a `try/finally`, a `type` alias and a nested `def` inside a `try` all read the enclosing scope's return correctly; a lambda returned, a lambda in a returned list, a comprehension, an `async` comprehension, a generator expression, a walrus, a subscript, a `BoolOp`, a dict value, a `Starred`-only element and an `await` all derive nothing. Only a function body may hold a `Return` in compilable Python, so the set is complete for every module this can be handed |
| 2 | Round 2's ⬜ 7 — the recorded limit and the shadowing | `tests/test_the_fixes_name_their_surface.py` `reach_values` docstring | answered | Every shape the docstring records is true of the code as it stands. **Executed** at `8232a07`: the six second-class under-reaches each return the empty set — a `Starred`-only element, a dict value, a comprehension, a `BoolOp`, a walrus and a subscript; a `+` between a name and a list reads the word and an `or` between them does not, so the stated asymmetry is real; a local shadowing a module constant derives the module's value. The five original under-reaches were re-measured against the rebuilt walk rather than carried, each returning the empty set — a bare local, an attribute constant, an `AnnAssign`, a `yield` and another function's value — and the call-arm over-reach is unchanged. Against the real module with no argument the derivation gives the three constants and nothing else |
| 3 | Round 2's ⬜ 8 and ⬜ 10 — the two superseded-wording markers | `seal/specs/1788691941-…/phases/phase-1.md:148-156`, `…/phases/phase-2.md:156-162` | answered | Both markers landed, in the form the reviewer suggested and the form this work item already used twice. **Read**, with one limit worth recording: both are HTML comments, so no rendered view of either file shows them, and the reader finding 8 was written for still meets the superseded sentence unmarked. It is the commissioned fix and the house convention, so it is not a new finding — changing the form is a repository decision rather than this branch's |
| 4 | Round 2's ⬜ 9 — the changelog's mutation count | `seal/specs/1788691941-…/changelog.md:78-80` | answered | The count is corrected to ten over the derivation's branches and eight over the walk, and the over-wide line is rewrapped. **Executed**: the fragment's longest line is now 80 columns against a limit of 88, and `tests/test_docs_line_wrap.py`'s COVERED list holds no `seal/` path, so nothing was going to catch it either way. The *each now killed by a named case* half is where finding 6 of this round applies |
| 5 | Round 2's ⬜ 11 — the lost half-cell | `seal/specs/1788691941-…/rounds/round-1.md:45` | answered | Closed, and the escape reads correctly to more than a splitter. **Executed** at `8232a07`: every table row in both records reads at the width its own header declares when the escape is honoured — round-1 gives 25 two-cell, 5 three-cell and 7 five-cell rows, round-2 gives 26, 10 and 13 — and the single naive six-cell row is the escaped one. Run through the repository's own reader, `skills/verify/scripts/unverified_check.py` `split_row`, round-1 row 2 reads five cells with the operator restored intact, so the tool round-trips it; `close` proved that at `8232a07` by rewriting that record's header and leaving the escape untouched. **Read** — the GFM tables extension unescapes an escaped separator inside a code span, which is the one place backslash escapes are not otherwise recognised, so the cell renders on GitHub as the operator rather than as a backslash |
| 6 | ⬜ The ledger fragment's mutation-run summary names two deliberate survivors where the module records three, and its *changes nothing on any shape* is falsified by a measured shape. The changelog carries the same claim into `CHANGELOG.md` | `seal/ledger/1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback.md:40` (R2 Verified behavior), `seal/specs/1788691941-…/changelog.md:79-80` | answered | corrected at `0cb4177` — the fragment's R2 now says three deliberate survivors, names the third as the type guard `own_returns`' docstring already disclosed, and narrows *on any shape* to *on any shape a compilable module can hold*, with round 3's two measurements as its grounds. Located under `seal/ledger/`, so it owes no fix pass and no reader |
| 7 | ⬜ `overview.md` names a stamp value the tree does not carry, and its verified roll-up stops one fix pass short | `seal/specs/1788691941-…/overview.md:5` and `:6` | answered | corrected at `0cb4177` — `overview.md` line 5 now carries both stamps and names `6182d405` as the value the tree holds, and the verified roll-up gains round 2's fix pass with its own figures. Located under `seal/specs/` |
| 8 | ⬜ `phase-2.md`'s round-1 marker sends a reader to a record whose figure has moved twice since | `seal/specs/1788691941-…/phases/phase-2.md:186-191` | answered | corrected at `0cb4177` — the marker no longer promises current figures; it points at the round records for the current shape and says outright that round 2's fix pass moved the count without touching it. Located under `seal/specs/` |
| 9 | The two units this range created, judged as code rather than as a fix | `tests/test_the_fixes_name_their_surface.py` `SCOPE_BOUNDARIES`, `own_returns` | answered | Correct, and the `New units` derivation is right. **Executed**: parsing the module at both ends of the range gives exactly `SCOPE_BOUNDARIES` and `own_returns` added and nothing removed, so `New units` is complete for the range. `Contract changes` reading `none` is correct by construction — the range touches only `seal/` and `tests/`. `own_returns` recurses into a `Return` node after yielding its value, which is dead work rather than a defect, since no expression can hold a statement. The `child.value is not None` conjunct is behaviour-neutral, confirmed by the surviving mutation: `handed_back` returns the empty set on a `None` through its fallthrough. The docstring says all of this itself, including the survivor, which is the disclosure the ledger row is missing |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the repository checked out at `8232a07`; every probe below ran in it and it was deleted afterwards | clone at `8232a0781ec475da6fd14e4bd26dd4501f8569c5`, main tree never written |
| `./bin/test tests/test_the_fixes_name_their_surface.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q`, exit code read directly | `106 passed`, exit `0` — the orchestrator's figure reproduced at the target |
| `./bin/evidence-check .` unscoped, exit code read directly | exit `1`; `701 ok · 2 drifted · 0 broken · 0 external · 0 old-format`. The two drifted are `templates/config.md#"# Repository config"` and `round_record.py#swallowed`, both the base's. The two fragments read `10 ok` and `12 ok`, the second having grown by the two new anchors |
| Eight mutations over `own_returns` and `SCOPE_BOUNDARIES`, one at a time, `__pycache__` scrubbed and `python -B` between them | seven dead, one alive. Drop `FunctionDef` exit 1 (2 failed); drop `AsyncFunctionDef` exit 1 (1); delete the boundary skip exit 1 (3); delete the yield exit 1 (12); delete the recursion exit 1 (3); `ast.walk` for `ast.iter_child_nodes` exit 1 (19); revert the call site to the blanket walk exit 1 (3). **Alive**: drop the `child.value is not None` conjunct, exit `0`, 55 passed — finding 6 |
| `SCOPE_BOUNDARIES` widened back to four members, then the module run | exit `0`, 55 passed — the record's deliberate-survivor claim confirmed for every fixture in the suite |
| The four-member set against a `call_sites` holding a class body whose statement is a `return` | two-member set derives the word, four-member set derives the empty set — the one shape on which the two differ. `ast.parse` accepts the source; `compile` raises a `SyntaxError`. Finding 6 |
| `reach_values` against 24 shapes not in the fixture table — decorator, default argument, return annotation, lambda returned, lambda in a list, `match`, `while/else`, `try/finally`, nested `def` in a `try`, `async def` method, nested class in class, comprehension, `async` comprehension, `type` alias, walrus, `Starred` alone, `Starred` beside a name, `BoolOp`, dict value, subscript, shadowing local, generator expression, `await`, nested `def` with a same-name local | every one correct against the docstring. Two notable: the shadowing local derives the module's value, and a `Starred` beside a plain name still reads the plain name |
| The five recorded under-reaches re-measured against the rebuilt walk rather than carried from round 2 | each returns the empty set with no complaint; the call-arm over-reach still derives the word; the real module with no argument derives exactly the three constants |
| Row widths of both records, through the repository's own `split_row` | round-1 gives 25 two-cell, 5 three-cell and 7 five-cell rows; round-2 gives 26, 10 and 13 — every row at its header's width, and round-1 row 2 reads five cells with the operator restored |
| The fixture table's length, and the module's units at both ends of the range | 18 fixtures; added `SCOPE_BOUNDARIES` and `own_returns`, removed nothing |
| `skills/code-review/scripts/chain_check.py --baseline origin/release/v0.8.3` | exit `1`, on `Pass` checked beside `Fixes checked by: nobody` in `round-2.md` — the mid-run state this record closes, not a defect. It flags none of this round's three findings |
| `uvx ruff format --check tests/test_the_fixes_name_their_surface.py` | exit `0`, already formatted |
| `uvx ruff check .` | exit `0`, all checks passed. **Disclosed rather than claimed**: `agent-contract` §2 puts the repository-wide lint in the orchestrator's broad gate and I ran it anyway, unprompted. It is seconds of cost, but it is a widening I chose, and the record should carry that rather than the number alone |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `seal/ledger.md:1088` (R8 Notes), `seal/ledger/1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback.md:30` (R2 Notes), `seal/specs/1788691941-…/changelog.md:53`, `tests/test_the_fixes_name_their_surface.py:584-586`, `seal/specs/1788691941-…/overview.md:21`, `seal/specs/1788691941-…/phases/phase-2.md:131` | round 1's 1 — fixed |
| round-1 | `tests/test_the_fixes_name_their_surface.py:568-571` | round 1's 2 — fixed |
| round-1 | `.github/scripts/run_tests.py:159-163` | round 1's 3 — fixed |
| round-1 | `seal/specs/1788691941-…/phases/phase-2.md:165` | round 1's 4 — answered |
| round-1 | `tests/test_the_fixes_name_their_surface.py:538-548` (`reach_values` docstring) | round 1's 5 — fixed |
| round-2 | `tests/test_the_fixes_name_their_surface.py:45-49,711-718`, `seal/ledger.md:1088`, `seal/ledger/1788691941-…md:38`, `seal/specs/1788691941-…/changelog.md:56-63`, `overview.md:21,59-60`, `phases/phase-2.md:135-141` | round 2's 1 — answered |
| round-2 | `tests/test_the_fixes_name_their_surface.py:592-620` (`handed_back`) | round 2's 2 — answered |
| round-2 | `tests/test_the_fixes_name_their_surface.py:664-671`, `REACH_REFUSAL` at 480-485 | round 2's 3 — answered |
| round-2 | `.github/scripts/run_tests.py:165-172`, `seal/ledger/1788691941-…md:37`, `changelog.md:10-16` | round 2's 4 — answered |
| round-2 | `phases/phase-2.md:165-172`, `tests/test_the_fixes_name_their_surface.py:648-663` | round 2's 5 — answered |
| round-2 | `tests/test_the_fixes_name_their_surface.py:697-700`; the false claim at `:664-671` (*the one remaining way*), `seal/ledger/1788691941-…md:38` (*a call's positional arguments are read*), `seal/specs/1788691941-…/changelog.md:77-78` (*one shape reads a value*) | round 2's 6 — fixed |
| round-2 | `tests/test_the_fixes_name_their_surface.py:648-663` | round 2's 7 — fixed |
| round-2 | `seal/specs/1788691941-…/phases/phase-1.md:152-154` | round 2's 8 — fixed |
| round-2 | `seal/specs/1788691941-…/changelog.md:83-84` | round 2's 9 — fixed |
| round-2 | `seal/specs/1788691941-…/phases/phase-2.md:151-153` | round 2's 10 — fixed |
| round-2 | `seal/specs/1788691941-…/rounds/round-1.md:45` | round 2's 11 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A record here names a figure or a hash that the next commit moves, and nothing notices. Three closings by enumeration — round 1's grep, round 2's three named files, and this round's three more — and the class has returned each time. The mechanism sibling of #189: a check that reads a record's stated count or stamp and compares it with the thing it counts | a new issue against the repository | the orchestrator |
| The three ⬜ corrections above, all under `seal/specs/` and `seal/ledger/` — nothing needing a fix, so nothing to commission | this record, as corrections in the closing commit | the 0.8.3 release preparation |
