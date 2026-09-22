# 1790076080-every-orchestrator-rule-is-a-sentence — review round 2

| Field | Value |
|---|---|
| Target SHA | 73e71c1a7a86b3b1139a6311a29d7173b08955e6 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 498 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `39732781bedc2db5288250acb54c063f01bbbb03..efa1f82a7d1fe0788eda28852767fd0e973ce644`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1, the docstring block of `tests/test_every_orchestrator_act_names_its_delivery.py`. The three corrections are records and commission nothing. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round, at the diff of round 1's fixes rather than at the branch —
`238dbeaf..da35172f`, four commits — with round 1's record as the agenda and
its verdicts inherited.

The job was the answers, not new findings: for each of round 1's four closed
verdicts, is it actually closed. One surface in that diff was exempt and read
as a finding surface instead — the five units round 1's `New units` row names,
which nobody has reviewed — together with the two contract changes' reach,
`emit(args, render)` → `emit(args, render, path=None)` and `_delivery(act, …)`
→ `_delivery(root, act, …)`, checked at every site rather than at the
signature.

Four things the fix pass claimed were handed over as claims: that the red
finding was answered by a rule reaching all three places rather than by
patching two lines, with the residual stated; that one of round 1's own four
planted red directions had been demonstrating something weaker than its name,
and that the floor beneath them is now clean for the right reason rather than
by a second leak; that three aggregates were corrected, one of them round 1's
own report; and that the survivor sweep found the Q3 misreading standing one
column over and it was corrected rather than exempted.

The broad gate was withheld, and the round was told the run ends at it if
nothing needing a fix is opened.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 1's 🔴 1 — the posted body carried the transcript's absolute path | `skills/verify/scripts/session_cost.py#emit`, `#report_segments`, `#report_spawns` | **answered** | Closed by a rule at the seam rather than two patched lines. Enumeration checked independently: the only two body lines that can carry a path print the one `path` argument, `--latest`'s line is printed outside the buffer, and `segment_label` falls back to a field `measure_segments` stores through `os.path.relpath`. Executed: both new cases red against `238dbeaf`, green at the target SHA |
| 🟢 | Round 1's 🟡 2 — an empty `--says` posted a comment with no judgment | `skills/verify/scripts/session_cost.py#emit` | **answered** | Exit 1, nothing posted, and the refusal moved ahead of the render — further than round 1's paste-ready fix went, with the reason in a comment. Executed: both cases red against `238dbeaf`. The second pins the refusal at the `gh` seam, so it does not depend on the tracker answering |
| 🟢 | Round 1's 🟡 3 — `_delivery` resolved against `ROOT`, so the floor case was green by leak | `tests/test_every_orchestrator_act_names_its_delivery.py#_delivery`, `#_tree` | **answered** | Clean for the right reason, checked by taking the repair away: resolution repaired with the planted file removed turns nine cases red including the floor; both undone reproduces the leak on `assert 0 == 1`. The new case separates the two readings with a path the repository has and the tree does not |
| 🟢 | Round 1's 🟡 4 — row 14's grounds named no part its delivery does not reach | `skills/implement/orchestration.md#"## Orchestrator: which of these acts runs itself"` | **answered** | The row now names the surface `New units` cannot reach. Counted the table myself rather than reading the correction: 20 rows, 8 checks and 5 commands, twelve of the thirteen delivered rows carry a limit sentence |
| 🟢 | Both contract changes reach every call site | `skills/verify/scripts/session_cost.py#emit`, `tests/test_every_orchestrator_act_names_its_delivery.py#_delivery` | confirmed | `emit` has three callers, all in `main`, all passing `path`; `_delivery` has one, updated. Neither is read from outside its own module, checked across every tracked Python file |
| 🟢 | Q3's two option cells now describe the list by what it is a list of | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/questions.md` Q3 | confirmed | Opened `CONTRIBUTING.md` 277–289: *"Two hooks reach the network"* and three hook-shaped limits. Both cells now scope the list to hooks; the survivor the sweep found is corrected rather than exempted |
| 🟡 1 | The module docstring enumerates four red directions where five stand, and names a case that is in no file | `tests/test_every_orchestrator_act_names_its_delivery.py`, the docstring's §*Red-first* block, lines 38–46 | **fixed** `efa1f82a` | fixed at efa1f82a; The fix pass added a fifth planted direction and left the four-way list alone. The block also points at a case whose name exists nowhere in the tree — pre-existing at `238dbeaf`, written across a line break so a single-line search misses it. Nothing catches either: the not-in-tree arm reads `.md` under a live work item, not a Python docstring |
| ⬜ | *Thirty-three files* and *nine outside the records* are a count of something narrower than the sentence says, and both understate | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`, `phases/phase-3.md` | correction | A single-line search gives 39 at the commit that wrote it and 37 at the reviewed commit; 33 needs the work item's own six files dropped. Tolerating the line wraps this repository's prose uses, the count is 48, and two of the extras are live files — `.github/scripts/roll_flow_measurement_issue.py` and `skills/commit-pr-convention/SKILL.md`. The conclusion is unchanged and gets stronger |
| ⬜ | Two statements of the corrected denominator survived the correction | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md` line 23, `phases/phase-1.md` line 63 | correction | Both still read *fourteen* where the delivered rows are thirteen. `phases/phase-1.md` now contradicts itself: its tally table reads 8 and 5, and its corrected passage at line 82 says thirteen. `survivor-check` cannot see it, because nothing removed the word |
| ⬜ | The new ledger row O7 is written between O5 and O6 | `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` | correction | The header comment says O7 is the last row and it is written sixth. Nothing reads the order, so this costs a reader a second look when `fold_ledger.py` moves the fragment at the release |
| ❓ | out of verified scope — the full suite, the repository-wide lint and the typecheck | the branch | out of scope | Contract §2 leaves the broad gate to the definition that assigns it, and this one assigns none. The sealer answers it, once, after the rounds settle. This round did not run it |

## Paste-ready fixes

```python
Red-first, per the contract's §15, five ways. Each planted tree below builds
a temp root with one defect in it, and `test_a_clean_planted_tree_is_clean`
is the floor beneath them -- the same tree without the defect, which has to
be clean for any of the five to mean anything. The case that asserts the
check can fail against the REAL tree is
`test_every_orchestrator_act_names_its_delivery` itself, which the five
below are what make able to fail:

  a marked heading with no row               `test_an_act_with_no_row_is_named`
  a row naming a heading no file carries     `test_a_row_naming_no_heading_is_named`
  a row naming a command that does not exist `test_a_named_command_must_exist`
  a row naming a path the tree under check
  lacks and the repository has               `test_a_named_path_is_resolved_against_the_tree_under_check`
  `still a sentence` with empty grounds      `test_a_sentence_row_carries_grounds`
```

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_every_orchestrator_act_names_its_delivery.py tests/test_a_section_marked_for_one_role_reaches_only_that_role.py tests/test_session_cost_post.py`, in a clone at the target SHA | 51 passed — matches the orchestrating session's reading |
| §15 probe A — `skills/verify/scripts/session_cost.py` restored to `238dbeaf`, the four new cases kept | 4 failed. All four of round 1's new posting cases are red against the reviewed commit |
| §15 probe B — `_delivery`'s root threading and `_tree`'s planted `SELF` file both undone, the new case kept | `test_a_named_path_is_resolved_against_the_tree_under_check` fails on `assert 0 == 1`. The leak reproduces |
| §15 probe C — resolution repaired, the planted `SELF` file left out | 9 failed, 5 passed. The floor case is among the nine, naming the file the tree does not carry, so it is clean for the right reason rather than by a second leak |
| The acts table counted mechanically off `skills/implement/orchestration.md` | 20 rows: 8 `check:`, 5 `command:`, 5 `still a sentence`, 2 `part of its parent's act`. Thirteen delivered |
| Every call site of `emit` and `_delivery`, searched across all tracked Python files | 3 and 1, all updated; no caller outside either module |
| Files naming the flow-log heading, counted at `238dbeaf`, `ef010857`, `da35172f` and the target SHA, single-line and wrap-tolerant | 37 / 39 / 39 / 39 single-line, 48 wrap-tolerant. Ten outside `CHANGELOG.md` and the work-item spec directories single-line, twelve wrap-tolerant |
| A search of every tracked file for the case the module docstring names | No match anywhere in the tree. Finding 1 |
| The broad gate — full suite, repository-wide lint, typecheck | not yet, and not run here. It is the sealer's, once, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py#emit`, `#report_segments`, `#report_spawns` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py#emit`, `#comment_body` | round 1's 2 — fixed |
| round-1 | `tests/test_every_orchestrator_act_names_its_delivery.py#_delivery` | round 1's 3 — fixed |
| round-1 | `skills/implement/orchestration.md#"## Orchestrator: which of these acts runs itself"` | round 1's 4 — fixed |
| round-1 | `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` O1, `overview.md`, `phases/phase-1.md` | round 1's ⬜ — correction |
| round-1 | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`, `questions.md` Q3 | round 1's ⬜ — correction |
| round-1 | `skills/implement/orchestration.md`, `tests/test_every_orchestrator_act_names_its_delivery.py#test_the_table_reads_the_section_that_holds_it` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger.md` | round 1's 🟢 — confirmed |
| round-1 | the branch | round 1's ❓ — out of scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The row rule cannot reach an act addressed to the orchestrator outside the two orchestration files, which the flow-log act is | `overview.md` §*Not done*, already deferred in round 1, named for an issue rather than built here | the repository owner — choosing between the two shapes is a person's |
| The table reads the marker and not the meaning, so a twenty-first act written without the prefix is counted by nobody | `overview.md` §*Not done*, already deferred in round 1 | the repository owner, with the above |
| Whether a network-writing arm needs a row of its own in `CONTRIBUTING.md` (Q3) | `overview.md` §*Not verified*, shipped as default (a), already deferred in round 1. This round confirmed the corrected grounds against the section | the repository owner, who owns that list |
