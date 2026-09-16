# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — review round 1

| Field | Value |
|---|---|
| Target SHA | 028f71ad8c588d8b3f08b94104fabd79ce4015a1 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 428 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 1, 2, 3 and 4 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

The reviewer was pointed hardest at whether these repairs are blind one layer
down. Four work items in this release have now turned out to be checks that
could not fail, and the pattern that produced them is the one this work item
repeats in shape: a reader is taught something, and the case that proves it
reads the same thing the reader does. Specifically asked for: whether phase
1's mutation goes red on the **row count** rather than on the value alone;
whether phase 2's new sentence can be produced by a fixture that was never
refused; whether phase 3's `__code__.co_filename` identity can hold while a
copy survives under another name; and whether the Windows-path case — the
constraint `questions.md` records and `plan.md`'s phase 1 row does not —
is pinned by something that fails when the unescape widens. Also asked: the
narrowing nobody had written down, that `config_rows` breaks on an unparseable
line only once it has found a row, so a piped FIRST row survives; and whether
`hooks/mode-gate.py` being deliberately untouched leaves a silence the branch
claims to have closed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The refusal says every row below the refused line is lost, without the condition the branch measured; false when that line is the table's first row | `skills/verify/scripts/broad_gate.py:283` | open | Executed: `config_rows` returned the two rows below it while the refusal said they were lost. Same sentence in `skills/config/SKILL.md:89`, `skills/implement/orchestration.md:159`, and pinned by `tests/test_first_setup_asks_once.py:222` |
| 2 | A value ending in a backslash before the closing pipe stopped being a row; `plan.md` and `questions.md` M3 say a widened pattern can only make more lines into rows | `hooks/config.py:70` | open | Executed: old pattern read `('Broad gate', 'C:\Users\x\tools\')`, new pattern reads no row. M3's measurement is sound; the generalisation past its population is not |
| 3 | A `Broad gate` row below a refused line naming another item is still reported ABSENT — the wrong-cause message, one item over | `skills/verify/scripts/broad_gate.py:265` | open | Executed: a config that read three rows before the branch now refuses with *has no `Broad gate` row*. `agent-contract` §12; the case at line 952 uses a fixture with no such row |
| 4 | `seal mode` still writes a second `Mode` row for a bare pipe, and three of four disclosure sites read as if it were closed | `seal/specs/1789598366-…/changelog.md:20` | open | Executed: `write_row` left the file two `Mode` rows deep. `templates/config.md:224` says so; the changelog, `overview.md` §*Not done* and `spec.md` do not |
| ⬜ | `refused_row` steps past a second header where `config_rows` breaks, and its docstring describes a stricter rule than the code has | `hooks/config.py:156` | correction | Executed: a refused line from a second table came back as this table's; an indented line is accepted although the docstring says a line must begin with a pipe |
| 🟢 | Phase 1's mutation is red on the row COUNT, asserted before the value | `tests/test_the_mode_question_is_asked_once.py:189` | confirmed | Executed: *the table has four rows and 1 came back* |
| 🟢 | Phase 3's `__code__.co_filename` assertion distinguishes a faithful copy from the one reader | `tests/test_the_pull_request_language_is_the_repositorys.py:711` | confirmed | Executed: red against a byte-faithful reimplementation compiled in the test file |
| 🟢 | The Q1 constraint — exactly the two characters — is pinned | `tests/test_the_mode_question_is_asked_once.py:225` | confirmed | Executed: red under a general backslash unescape |
| 🟢 | A5: the absent-row message was not swallowed by the new branch | `tests/test_the_seal_is_taken_once_by_the_sealer.py:684` | confirmed | Read the fixture (`row=False`, no unparseable line), then executed the branch mutation |
| 🟢 | Two ledger claims REMOVED and rewritten into this work item's fragment, nothing re-pointed | `seal/ledger/1789445605-…md` | confirmed | Read: header 8 → 7, the pipe row gone, the new claim in this work item's own fragment |
| 🟢 | `hooks/mode-gate.py` is untouched and still answers the home or `""` | `hooks/mode-gate.py` | confirmed | Executed as part of the module run; the case at `tests/test_the_mode_question_is_asked_once.py:290` asserts it |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the six modules this branch touches, at the target SHA | exit 0 · 338 passed |
| Phase 1's mutation — `CONFIG_ROW`'s value cell back to `[^\|]*?` | exit 1 · 3 failed, first on the row count |
| Phase 2's mutation — the new branch in `missing_row` made unreachable | exit 1 · 1 failed |
| Phase 3's mutation — `items` replaced by a byte-faithful local copy | exit 1 · 1 failed on `__code__.co_filename` |
| Q1's mutation — `unescaped` widened to a general backslash unescape | exit 1 · 1 failed |
| Phase 4's mutation — the template's old pipe sentence restored | exit 1 · 1 failed |
| `refused_broad_row`'s first-cell reading dropped | exit 1 · 1 failed |
| Behaviour probe: a refused `Broad gate` line as the table's FIRST row | the two rows below it were returned while the refusal said they were lost |
| Behaviour probe: a value ending in a backslash, old pattern against new | a row before this branch, no row after it |
| Behaviour probe: `write_row` over a bare-piped config | the file came back two `Mode` rows deep |
| `bin/evidence-check --strict .` | exit 0 |
| The full suite, the repository-wide lint, the typecheck | **not yet** — the sealer's one broad run, after the rounds settle (`agent-contract` §2) |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A file already two `Mode` rows deep is repaired by nothing | not recorded anywhere in this branch — finding 4 asks for the row | the repository owner |
| A pull-request arm reporting a malformed `seal/config.md` | `spec.md` §Out, by name | already deferred in the frame |
