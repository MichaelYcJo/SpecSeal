# 1788486395-the-roll-opens-the-next-log-with-no-body — review round 2

| Field | Value |
|---|---|
| Target SHA | c79988a |
| PR | not yet opened |
| Broad gate | `9ee9827`, against `release/v0.8.0`. Full suite 1969 passed · 1 skipped; `ruff check .` and `ruff format --check .` clean; `chain_check --baseline main` exit 0 after `git fetch origin '+refs/pull/*/head:refs/remotes/pull/*/head'`, which is what the previous work item's round-3 target needed once its branch was squashed; `unverified-check` and `fold_ledger --dry-run` exit 0. `evidence-check` reports 499 ok and one drifted row, S8, which predates both work items |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no — three 🟡 opened, every one answerable with grounds and every one handed to issue #146 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round, at the diff of round 1's fixes — `git diff b1f7340..HEAD`
— with round 1's seven verdicts as the agenda and its two new units,
`landed_create` and `BASELINE_AMBIGUOUS_NOTE`, named as the finding surface.

Six things to try to break, in order, of which the implementer had named the
first three when it handed over: whether `_ladder_harness` returning a pair
and being unpacked by seven cases is still testing the ladder or testing
itself; whether the note's blame-a-rung wording survives being wrong; whether
the guard's own lookup exiting turns a tolerated failure into a fatal one;
the retry's sleep and the mutation the implementer had closed; the two
silences `find_baseline_issue` now separates; and whether the reworded skill
prose is pinned on what changed rather than on words having moved.

Two facts were handed over rather than left to be re-derived: `docs/flow.md`
is off this branch by design because PR #144 carries that tick, and
`evidence-check --reverify` is narrowed by `--ledger` even though it has no
row selector.

This is also the first round prompt in this session written without restating
`agent-contract` §6 and §2 or the reviewer's report format — the half
`skills/code-review/SKILL.md` says is not the orchestrator's to type.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | Round 1's 🔴, the landing guard | `roll_flow_measurement_issue.py` | answered | Re-broken in a clone: the guard stops excluding `closed_number` → `test_the_issue_main_just_closed_does_not_count_as_the_create_landing` red. The reviewer executed every one of round 1's seven fixes this way rather than carrying the verdicts |
| 🟢 2 | Round 1's 🟡 2, 3, 4, 5, 7 | four files | answered | Five mutations, five kills, each named in the round's table. 🟡 6 verified by absence: `git diff release/v0.8.0...HEAD -- docs/flow.md` is empty and `phases/phase-4.md` carries its commit |
| 🟢 3 | The harness is still testing the ladder | `tests/test_a_release_rolls_the_flow_measurement_issue.py` | answered | `_ladder_harness` mocks `list_open_issues`, which is what `landed_create` calls, so the exclusion filter and retry loop are real code on harness data and `closed_number` reaches the guard through the real `main` flow. One pre-existing leniency recorded rather than closed: readings never run out, so no case can pin the lookup count. The reviewer counted for real — three calls on an all-non-empty run |
| 🟢 4 | The note's blame-a-rung wording | `roll_flow_measurement_issue.py` | answered | It survives. A rung-1 network failure gives a rung-2 body saying the milestone could not be set on this issue, which is true because rung 2 omits it; the cause list can be wrong and the instruction it hangs off stays correct. `BASELINE_AMBIGUOUS_NOTE` has no such exposure — it comes from a parsed `len(issues) > 1`, an observation rather than an inference |
| 🟢 5 | The two silences | `roll_flow_measurement_issue.py` | answered | Seven readings executed — lookup failed, zero, one, two, three, not-JSON, empty string. All correct, and the note reaches the created body on all three rungs. Only the last rung's delivery is unpinned, which is 🟡 8 |
| 🟡 6 | The module docstring still teaches the guard the fix removed, and states the lag rule as an absolute that `landed_create` contradicts twelve lines away | `roll_flow_measurement_issue.py:43-45`, `:76-80` | answered — deferred | Every hunk of `1ead0b1` starts at line 129. `:43-45` is the sentence round 1's grounds name as what the first implementation leaned on, left in place with no tiebreaker. The reviewer wrote both replacement paragraphs |
| 🟡 7 | `assert slept == [m.RETRY_DELAY_SECONDS]` compares the constant against itself | `tests/test_a_release_rolls_the_flow_measurement_issue.py:366`, `:77` | answered — deferred | Executed: setting the constant to `0` leaves all 18 cases green — the immediate second read the case's own docstring says the sleep prevents. The shape predates this branch at `:77` |
| 🟡 8 | The ambiguous-ledger note's delivery is pinned on two of its three sites | `roll_flow_measurement_issue.py:347-349` | answered — deferred | Executed: dropping it from the ladder rungs is killed, dropping it from the final rung survives. §12 — F3 of the fragment records four kills for this class and enumerates two sites of three |

## Executed probes

| What was run | Result |
|---|---|
| ten mutations across round 1's seven fixes and the two new units | eight killed, two survived (🟡 7, 🟡 8) |
| a four-case probe: all seven baseline readings, the final-rung body, the guard's lookup-failure path, the real lookup count | in the grounds above |
| 32 cases across the two changed modules | exit 0 |
| `uvx ruff check` and `format --check`, three changed Python files | clean |
| both proposed regression cases, green at HEAD and red under their mutations | §15 satisfied before they are written |
| `evidence-check --ledger 'seal/ledger/1788486395-*.md' .` · `fold_ledger --dry-run` · `unverified-check` | exit 0 · exit 0 · exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `roll_flow_measurement_issue.py:43-45` | Round 1's grounds named this sentence as what produced the 🔴. Round 2 found it unchanged — 🟡 6 |
| round 1 | the ladder's three body-writing sites | Round 1 closed the note's delivery for two of them; the third is 🟡 8 |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 6, 🟡 7 and 🟡 8 — one concern: a fix landed and the file did not finish describing it | issue #146, with both replacement paragraphs and both test cases written out | the repository owner |
| Whether `landed_create` should tolerate its own lookup failing, rather than turning a tolerated create failure into a red release step | issue #146's context; the reviewer declined to call it a defect because the alternatives either open a second issue or lose the log silently | the smith, in one line of grounds |
| `gh issue create --milestone`'s real failure ordering, and how the body renders | `overview.md` §Not verified | the repository owner, at the 0.9.0 roll |
| `seal/ledger.md` S8 | work item `1788472135`'s memo | the repository owner |

**The run ends here, and it is the first time the floor has stopped one with
cheap fixes on the table.** All three 🟡 are one-line changes whose cases the
reviewer had already shown red under mutation. #110's rule says a round that
finds nothing that loses a record and nothing that crashes ends the run and
hands over what else it found, and taking an exception here on the branch
whose sibling shipped that rule would make it a preference rather than a rule.
The cost of stopping is visible and recorded in #146, which is what makes this
evidence for #110 rather than an exception to it.
