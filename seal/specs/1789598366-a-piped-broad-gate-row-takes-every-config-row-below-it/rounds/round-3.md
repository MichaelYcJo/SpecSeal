# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — review round 3

| Field | Value |
|---|---|
| Target SHA | 6b49dedb4d0d937ec90aae61c2b9f3e398df6896 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 428 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last record of this run. Round 1 met the floor and round 2 spent the one
reopening the chain allows, so this record reads round 2's fixes and ends the
run whatever it finds — anything still open leaves as an issue with a verdict
of `deferred #N`, not as another round. It was asked to spend itself on the
diff `5137e934..c61bed39` rather than on the branch: whether the rewritten
walk closes the class the round named — *a sentence about the table computed
from one line of it* — or only its five measured members; whether the two new
cases go red on WHICH line a sentence describes rather than on the sentence
existing; whether the seven ledger notes were written by somebody who read the
claims; and one shape the orchestrator measured and did not hand to the fix
pass — a `Broad gate` line written last in its table, where the refusal still
says every row below it is lost and there are none.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | the cost sentence asks only the stopping line and never the rows, so a `Broad gate` line written last in its table is told every row below it was lost when none was written | `skills/verify/scripts/broad_gate.py:363` | deferred #430 | Executed: over a two-row file ending in the refused line, `below` is `[]` and the message says every row below is lost. Both cases pinning that sentence use files with nothing below it. The run is capped, so this leaves as an issue rather than as a fix |
| 2 | `config_rows` reads the first `\| Item \| Value \|` header in the file, so a fenced example table above the live one is the table the gate runs | `hooks/config.py:105` | deferred #429 | Executed: `broad_command` returns the fenced example's value and the live row is never reached. Predates the branch — the walk is unchanged over `0995f62f..HEAD` — and is named in no record |
| ⬜ | the fix record's claim that the limitation case's list of four records cannot be pinned is too strong | `tests/test_the_mode_question_is_asked_once.py:358` | correction | Read: the completeness of the list cannot be pinned, but its coordinates can — resolve the four paths, assert each exists, build the message from the same list |
| ⬜ | two byte-identical refused lines are quoted as *this is it* and as *stopped LOWER DOWN* | `skills/verify/scripts/broad_gate.py:363` | correction | Executed: every fact in the message is correct and the reader cannot tell the two quotations apart |
| ⬜ | a `Broad gate` row below a blank line or prose under the stopping line is reported absent | `hooks/config.py:152` | deferred `spec.md` §*What this repair cannot see* | Executed over four shapes. `below` is exactly what the stopping line cost, so this is the reader's own rule rather than an under-report; `spec.md` names *a row after a blank line* by name |
| 🟢 | round 2's 🟡 1 is closed on all five members the fix pass enumerated | `hooks/config.py:152`, `skills/verify/scripts/broad_gate.py:351` | confirmed | Executed: all fifteen shapes reach the sentence naming the line their own facts are about, but for finding 1 |
| 🟢 | the two new cases are red on WHICH line the sentence describes, not on a sentence existing | `tests/test_the_seal_is_taken_once_by_the_sealer.py:1094`, `:1170` | confirmed | Executed: the reviewer's chooser reddens both on the one-bad-line half, the collapse reddens both on the two-bad-line half, and `5137e934` reddens both on the absent-row message |
| 🟢 | §15 holds for both new cases | `tests/test_the_seal_is_taken_once_by_the_sealer.py:1094`, `:1170` | confirmed | Executed: both units restored to the commit before the fix redden both cases |
| 🟢 | all seven re-anchored ledger rows carry a note whose grounds hold against the section | `seal/ledger.md`, `skills/implement/orchestration.md` §*Orchestrator: Bootstrap* | confirmed | Read the section and executed the diffs: one paragraph edited by two commits, inside numbered item 1; every claim each note makes about where it sits is true |
| 🟢 | `overview.md`'s disclosure agrees with the count | `seal/specs/1789598366-…/overview.md:37` | confirmed | Read: thirteen in `seal/ledger.md` and five in the previous work item's fragment, seven of the thirteen noted in round 2's fix pass |
| 🟢 | the survivor exemptions were inert for two independent causes, as the fix record says | `skills/code-review/scripts/survivor_check.py:891` | confirmed | Read `exempted` — a `path:line` cell matches neither by equality nor by suffix. Executed: six runs over three ranges, with and without `--exempt`, all exit 0 with identical output |
| 🟢 | CRLF, indentation and three-column stoppers are all read correctly | `hooks/config.py:152` | confirmed | Executed: the CRLF file's sentences are identical to the LF file's; an indented refused line comes back with its indentation; a three-column stopper reaches the *never reached it* branch |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_seal_is_taken_once_by_the_sealer.py` and `tests/test_the_mode_question_is_asked_once.py`, at the target SHA, in the clone | exit 0 · 145 passed |
| fifteen config shapes through `refusal`, `missing_row`, `refused_broad_row` and `broad_command`, against an instrumented copy of `config_rows` as the truth oracle | fourteen correct; the `Broad gate` line last in its table is told every row below it was lost |
| a fenced `\| Item \| Value \|` table written above the live one | `broad_command` returned the fenced example's value; the live row was never reached |
| the cost chooser keyed on `below` — the round 2 reviewer's own proposal | exit 1 · both new cases, on the one-bad-line half |
| the cost chooser collapsed back to two cases | exit 1 · both new cases, on the two-bad-line half |
| the hidden-row branch gated on the first refused line being the stopper | exit 1 · `test_a_second_refused_line_is_what_decides_what_a_first_one_cost` |
| `refused_broad_row` asking only the first refused line | exit 1 · `test_the_gate_reads_every_refused_line_and_not_only_the_first` |
| the walk giving up at prose above the table's first row | exit 1 · the same case |
| every refused line reported as reached | exit 1 · the same case |
| `hooks/config.py` and `skills/verify/scripts/broad_gate.py` restored to `5137e934`, the commit before the fix | exit 1 · both new cases, on *has no `Broad gate` row* |
| each of the two restored from bytes, every `__pycache__` cleared between runs | exit 0 · 145 passed each |
| `git diff` of `skills/implement/orchestration.md` over `0995f62f..HEAD`, and per commit | one paragraph, two commits; six `templates/config.md` mentions at the base and six at HEAD, unchanged |
| `git diff --stat` of `CLAUDE.md` over `0995f62f..HEAD` | empty — untouched, as the S11 note claims |
| `bin/survivor-check` over `5137e934..c61bed39`, `5137e934..HEAD` and `0995f62f..HEAD`, each with and without `--exempt` | exit 0 in all six · identical output with and without the file |
| `bin/evidence-check --strict .` | exit 0 · 0 refused · 0 drifted |
| `bin/unverified-check seal/specs/` | exit 0 |
| The full suite, the repository-wide lint, the typecheck | **not yet** — the sealer's one broad run, which this round's close is what makes due (`agent-contract` §2) |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:283` | round 1's 1 — fixed |
| round-1 | `hooks/config.py:70` | round 1's 2 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py:265` | round 1's 3 — fixed |
| round-1 | `seal/specs/1789598366-…/changelog.md:20` | round 1's 4 — answered |
| round-1 | `hooks/config.py:156` | round 1's ⬜ — correction |
| round-1 | `tests/test_the_mode_question_is_asked_once.py:189` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_pull_request_language_is_the_repositorys.py:711` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_mode_question_is_asked_once.py:225` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:684` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1789445605-…md` | round 1's 🟢 — confirmed |
| round-1 | `hooks/mode-gate.py` | round 1's 🟢 — confirmed |
| round-2 | `hooks/config.py:152` | round 2's 1 — fixed |
| round-2 | `seal/specs/1789598366-…/changelog.md:49` | round 2's ⬜ — correction |
| round-2 | `seal/ledger.md`, `seal/specs/1789598366-…/overview.md:37` | round 2's ⬜ — correction |
| round-2 | `tests/test_the_mode_question_is_asked_once.py:332` | round 2's ⬜ — correction |
| round-2 | `hooks/config.py:204` | round 2's ⬜ — correction |
| round-2 | `skills/verify/scripts/broad_gate.py:328` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:352` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1789598366-…/overview.md` §*Not done* | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_mode_question_is_asked_once.py:230`, `:332` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the cost sentence says rows below were lost where none were written | a new issue — the run is capped (`docs/review-chain-spec.md` §*The reopening*) | the repository owner. The paste-ready fix below is one branch and two fixture edits |
| a fenced example table above the live one is the table the gate reads | a new issue | the repository owner. Predates this branch; `spec.md` §*What this repair cannot see* names the neighbouring shapes and not this one |
| a `Broad gate` row below a blank line or prose is reported absent | `spec.md` §*What this repair cannot see* | already deferred there — the repository owner |
| `survivors.md` silences nothing at the range the fix pass runs | `seal/follow-up.md`, the `#371` / `#308` row | already deferred in round 2 — the repository owner. Re-measured here over three ranges, six runs |
| a file already two `Mode` rows deep is repaired by nothing | `overview.md` §*Not done* | already deferred by round 1's fix pass — the repository owner |
| a pull-request arm reporting a malformed `seal/config.md` | `spec.md` §Out, by name | already deferred in the frame |
