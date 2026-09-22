# 1790076080-every-orchestrator-rule-is-a-sentence — review round 3

| Field | Value |
|---|---|
| Target SHA | 54198d71e2dc586b3b13a3e24de31ebeb8a4848e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 498 |
| Broad gate | e339586d against 6d410023 |
| Fixes checked by | no fixes to check |
| Fix range | `54198d71e2dc586b3b13a3e24de31ebeb8a4848e..feef8b7c82cbc2bb7daba64ce2ced1f55229c02b`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no — the one 🟡 round 2 opened is closed on this round's own grounds, and all three corrections are made. The three findings above are records, they commission nothing, and the run ends here. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last record of the run. The reopening was spent at round 2, so whatever
this round found, no fourth round follows it — anything needing a fix would be
deferred with a named answerer or become an issue, and the round was told so
before it started.

Target: the diff of round 2's fixes, `39732781..efa1f82a`, one commit, with
rounds 1 and 2 both inherited. `New units` read none, so there was no
unreviewed finding surface and the job was the answers.

Four claims were handed over. That the docstring the round-2 fix repaired now
enumerates what the module holds rather than what the paste-ready block said,
with no name split across a line break — the shape that hid the old name, not
only the instance. That the fix commissioned a fourth correction of its own,
because removing the name left a record naming it with nowhere to resolve and
the records arm went to exit 2, the marker exempting the line and not the name.
And three record corrections, one of them a count that had been wrong twice in
the same direction.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 2's 🟡 1, first half — the docstring enumerated four directions where more stand | `tests/test_every_orchestrator_act_names_its_delivery.py`, the module docstring | **answered** | Counted by construction off the AST, not read: 13 tests, exactly 10 plant a tree, 8 of those assert one named finding and 2 assert none. The block lists all ten and says what it is a list of. The fix completed the list to eight past the paste-ready block's five, which listed five where the module has eight |
| 🟢 | Round 2's 🟡 1, second half — the block named a case that is in no file | `tests/test_every_orchestrator_act_names_its_delivery.py`, the module docstring | **answered** | Twelve backticked `test_` names in the block: eleven are functions in this module, the twelfth is the neighbour module it imports from. No name is split across a line break — every name sits alone on its own line, so no docstring line carries an odd number of backticks. The shape that hid the old name is gone rather than the instance |
| 🟢 | The fourth correction the fix commissioned — the not-in-tree marker's placement | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/rounds/round-2-report.md` line 148, `skills/evidence-check/scripts/evidence_check.py#claim_lines` | confirmed | The exemption sits where the arm reads it, shown by taking it away: marker at the paragraph end gives exit 2 naming `round-2-report.md:148` with `1 refused`; as shipped, exit 0. The first attempt at this probe came back a false green because the probe file lived inside the clone and `tree_names` read the name out of it |
| 🟢 | The citation count restated with its method | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`, `phases/phase-3.md` | confirmed | Re-derived, not read. Twelve files outside `CHANGELOG.md` and `seal/specs/`, ten single-line and the two wrap-only ones exactly as named; four test modules; nine rows in `seal/ledger.md`; 49 wrap-tolerant and 40 single-line at `39732781`. Every figure matches except one clause, below |
| 🟢 | The denominator is thirteen in the two places that read fourteen | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md` line 23, `phases/phase-1.md` line 63 | confirmed | Counted the acts table myself: 20 rows, 8 `check:`, 5 `command:`, 5 `still a sentence`, 2 `part of its parent's act`, thirteen delivered. The word *fourteen* survives nowhere in this work item's files |
| 🟢 | O7 moved below O6 | `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` | confirmed | The fragment runs O1 through O7 in order and the header comment above the table is true of it |
| ⬜ | The corrected citation sentence gives 37 for `73e71c1a`, where 37 is `238dbeaf`'s figure, and calls a one-commit distance four | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/phases/phase-3.md` line 65 | correction | Single-line at `73e71c1a` is 39; 37 is the count at `238dbeaf`, which is where round 2's own probe row puts it. `git rev-list --count` gives 1 for `73e71c1a..39732781`; four is the length of round 2's fix range, a different pair. The paragraph's own subject is pinning a total to a tree |
| ⬜ | The fix pass removed a number from round 2's committed report and its correction note covers only the marker move | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/rounds/round-2-report.md` lines 145–165 | correction | *"the four planted cases"* became *"the planted cases"*. The direction is right — the module has eight — but the `<!-- Corrected -->` comment names the marker's placement and nothing else, so the record and the report now differ in one of round 2's own miscounts with only the report moved. Three blank lines left at 163–165 |
| ⬜ | §*Not done* says a *twentieth* act where the table already carries twenty rows | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md` line 55 | correction | An act written without the prefix would be the twenty-first, which is how round 2's deferred row states it. Pre-existing at `39732781` and outside this round's target diff; reported because this sentence is what the issue will be scoped from |
| ❓ | out of verified scope — the full suite, the repository-wide lint and the typecheck | the branch | out of scope | Contract §2 leaves the broad gate to the definition that assigns it, and this one assigns none. The sealer answers it, once, after the rounds settle. This round did not run it, and nothing in this report holds it back |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `pytest` over `tests/test_every_orchestrator_act_names_its_delivery.py` and `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`, the module the diff edits and the module it imports from, in a clone at the target SHA | 23 passed |
| The same plus `tests/test_session_cost_post.py` | 51 passed |
| `bin/evidence-check .` unscoped, in the clone at the target SHA | exit 0 · 1451 ok · 0 drifted · 0 broken · 0 refused. Records arm: 1 work item read · 93 names read · 0 refused |
| §15 probe — the not-in-tree marker moved back to the end of the paragraph, the name left bare on its own line, run from **outside** the clone | exit 2, `NOT-IN-TREE  …/rounds/round-2-report.md:148`, `1 refused`. Restored: exit 0, `0 refused`. The placement is load-bearing |
| The same probe written inside the clone | False green — exit 0 both ways. `tree_names` read the name out of the probe file itself; a control name invented for the test resolved too, which is what exposed it |
| The module's cases classified off the AST: which call `_tree`, and what each asserts | 13 tests · 10 plant a tree · 8 assert one named finding · 2 assert none. The docstring's eight-and-two is the class exactly |
| Every backticked `test_` name in the docstring resolved against the module and the tree | 12 names · 11 functions in this module · 1 the neighbour module it imports from · 0 unresolved · 0 split across a line break |
| Files naming the flow-log heading, counted at `238dbeaf`, `73e71c1a`, `39732781` and the target SHA, single-line and wrap-tolerant | 37/47 · 39/48 · 40/49 · 40/49. Outside `CHANGELOG.md` and `seal/specs/` at the target: 12 wrap-tolerant, 10 single-line, 4 test modules, 9 rows in `seal/ledger.md` |
| The acts table counted mechanically off `skills/implement/orchestration.md` | 20 rows: 8 `check:`, 5 `command:`, 5 `still a sentence`, 2 `part of its parent's act`. Thirteen delivered |
| `git rev-list --count` for `73e71c1a..39732781`, `..efa1f82a`, `..54198d71` | 1, 2, 3. No reading gives four |
| The word *fourteen* searched across every tracked file | No occurrence in this work item's files. The remaining hits belong to other work items and to `seal/ledger.md` |
| The broad gate — the full suite, the repository-wide lint, the typecheck | not yet, and not run here. It is the sealer's, once, after the rounds settle |

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
| round-2 | `skills/verify/scripts/session_cost.py#emit` | round 2's 🟢 — answered |
| round-2 | `tests/test_every_orchestrator_act_names_its_delivery.py#_delivery`, `#_tree` | round 2's 🟢 — answered |
| round-2 | `skills/verify/scripts/session_cost.py#emit`, `tests/test_every_orchestrator_act_names_its_delivery.py#_delivery` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/questions.md` Q3 | round 2's 🟢 — confirmed |
| round-2 | `tests/test_every_orchestrator_act_names_its_delivery.py`, the docstring's §*Red-first* block, lines 38–46 | round 2's 🟡 1 — fixed |
| round-2 | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`, `phases/phase-3.md` | round 2's ⬜ — correction |
| round-2 | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md` line 23, `phases/phase-1.md` line 63 | round 2's ⬜ — correction |
| round-2 | `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` | round 2's ⬜ — correction |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Nothing pins the module docstring's enumeration to the module. It is correct at this commit and a case added next month makes it wrong silently — confirmed against the checker: the records arm reads `.md` under a live work item, so a Python docstring is outside everything that runs. A case comparing the block's names against the module's own AST would close it, and a case is mechanism a fix pass may not add | `overview.md` §*Not done*, with the two already there. I agree it belongs with them: it is the same shape — an enumeration the tree does not hold in step — and it is what round 2's 🟡 was an instance of | the repository owner, with the two beside it. It is a small case rather than a design choice, so it is the cheapest of the three to close |
| The row rule cannot reach an act addressed to the orchestrator outside the two orchestration files, which the flow-log act is | `overview.md` §*Not done*, already deferred in rounds 1 and 2, named for an issue | the repository owner — choosing between the two shapes is a person's |
| The table reads the marker and not the meaning, so an act written without the prefix is counted by nobody | `overview.md` §*Not done*, already deferred in rounds 1 and 2 | the repository owner, with the above |
| Whether a network-writing arm needs a row of its own in `CONTRIBUTING.md` (Q3) | `overview.md` §*Not verified*, shipped as default (a), already deferred in rounds 1 and 2 | the repository owner, who owns that list |
