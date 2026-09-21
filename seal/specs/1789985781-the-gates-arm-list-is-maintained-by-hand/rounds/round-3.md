# 1789985781-the-gates-arm-list-is-maintained-by-hand — review round 3

| Field | Value |
|---|---|
| Target SHA | eca3899ecdefc033a3292f0f64754def64c899b2 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 472 |
| Broad gate | 7feb72d against release/v0.12.2 |
| Fixes checked by | no fixes to check |
| Fix range | `eca3899ecdefc033a3292f0f64754def64c899b2..eca3899ecdefc033a3292f0f64754def64c899b2`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, over one range — `ad59548..b3f3dab`, two commits — closing round 2's
single finding. Round 2 met the floor where round 1 did not, so the reopening
bound was live and the reviewer was told to expect the generator to call this
the last record, and to be exact about severity rather than to look less hard.

**The enumeration was named as the thing to check, not the three edits.** The
branch had named a class short three times by then: the reviewer's two
coordinates widened to four and reported as the class, then six named by round
2, then seven found by the builder's own grep — the seventh being
`changelog.md`, which states the class, names no issue, and gathers into
`CHANGELOG.md` at the release, making it the only copy a user reads. The round
was asked to re-run that enumeration from both sides itself and to find a
third angle if one existed.

Three judgments were handed over on the reviewer's own account. Whether the
widened Claim cells of ledger rows G6 and G7 now over-claim in the other
direction, since round 2 had found them under-claiming and a correction that
overshoots is the same defect with the sign flipped — which is this work
item's own subject. Whether `MIXED_WORKFLOW`'s two mutations really redden it
alone, given both were asserted unique with `count(old) == 1` first, and
whether that assertion was over the right string. And whether anything in the
branch still attributes a class, a rule or a measurement to a coordinate that
will not exist after this release merges.

Then the work item as a whole, for the seal: documents against code, nothing
the rounds disproved still standing, and the fragment's rows saying what the
code does.

`evidence_check.py .` unscoped, exit codes read directly, `seal/ledger.md` off
limits to a whole read, and the floor line to be answered explicitly.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 2's finding 1 is closed, and the seventh copy is the last — checked from a third angle the builder did not use | `skills/verify/SKILL.md:352`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/questions.md:29`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/changelog.md:56` | answered | **Executed.** Enumerated by the SUBJECT rather than by the class phrase or the number — `skips both`, `skips neither`, `unconditionally where`, `guards them on the base`, `known non-equivalence`. Seven places outside the round records, all seven naming #473. The reciprocal `473` grep adds nothing; the `423` grep leaves only historical references. Pull request 472's body carries no copy. `gh issue view 473` OPEN, `backlog: gates & hooks`; `gh issue view 423` OPEN, `release: 0.12.2` |
| 🟢 | `changelog.md:56` is the copy that matters most and it is corrected — it is the one a user reads | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/changelog.md:56` | not a defect | **Read.** The fragment gathers into `CHANGELOG.md` at the release, so its `#473` is permanent; #473 sits in `backlog: gates & hooks` and does not close with 0.12.2. The fragment carries no count that can go stale — the numbers it states (13 steps, 8 unanswered, two arms added, four excluded) all reproduce against the code |
| 🟢 | G7's widened Claim does not over-claim — round 2's under-claim was repaired without flipping the sign | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` G7 | not a defect | **Executed and read.** The Claim's *no line* and *same rows in the same order* are not asserted by the latin-1 case, which asserts exit 0, `SEALED`, no `Traceback` and no `not answered`. Both hold transitively: `coverage = coverage_line(workflow) if workflow else None` is one guard for both shapes and `workflow_text` returns `None` for both, so a break in the latin-1 shape breaks the absent shape, where `test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before` compares the panel labels against `HISTORICAL_ROWS` |
| 🟢 | G6's widened Claim does not over-claim | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` G6 | not a defect | **Executed.** `coverage_line` rendered against a mixed fixture names an excluded step in the reasoned clause and an unclassified one in the unknown clause, and neither in the other. `coverage_line` is one of the row's own coordinates, so the claim's performer is reachable from the row |
| 🟢 | The mixed-workflow case is load-bearing, not decorative, and the builder's divergence from round 2's *correct by construction* reading was right | `tests/test_the_gate_names_every_step_ci_runs.py:811` | not a defect | **Executed.** Two mutations redden it ALONE: the second clause rendered only when the first did not, and the first only when the second did not. Both leave `UNCLASSIFIED_WORKFLOW` and the real workflow rendering unchanged, so round 1's two cases stay green. *Disjoint by construction* is an argument about the two comprehensions and says nothing about the two `if` blocks that render them |
| 🟢 | The two mutations the branch reports for that case land where they were aimed, and the ledger does not claim they redden it alone | `skills/verify/scripts/broad_gate.py:1438` | not a defect | **Executed.** `count(old) == 1` asserted before each substitution and `old` asserted absent from the file after it. Clause A claiming every unanswered step reddens the new case plus `test_a_step_no_row_classifies_is_not_said_to_carry_a_reason`; clause B reddens it plus `test_a_step_a_row_excludes_is_still_pointed_at_its_reason`. G6's Notes say *red when either clause learns to claim every unanswered step*, which is what happens, and the proof block's *each applied alone* is about application, not about redness |
| 🟢 | The proof block's corrected counts are exact | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/overview.md:19` | not a defect | **Executed and read.** 24 test functions defined, 24 passed; 20 + 3 + 1 accounted for by the two records' `New units` rows. 19 + 4 + 2 = 25 mutations, of which round 2's two were reproduced here. Dropping the ordinal — *A 24th* became *One more* — is what stops this line going stale a third time |
| 🟢 | Nothing else on the branch sends a live fact to a home that closes with this release | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/spec.md:22`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/questions.md:24` | not a defect | **Read.** Every surviving `#423` reference is historical — the prerequisite that shipped, the defect seen from the other side, a past review finding — and each resolves to a committed round record that outlives the issue. `seal/follow-up.md`'s new row names the repository owner with no condition attached, which is the shape that file admits |
| 🟢 | The fragment's rows resolve and the documents agree with the code | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` | not a defect | **Executed.** `evidence_check.py .` unscoped, no `--ledger`: exit 0, `total: 1398 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, the fragment's 13 coordinates all ok. `coverage_line` against the real workflow: 13 steps, 8 unanswered, panel value `8 of 13 not answered` at 20 of `PANEL_VALUE_WIDTH`'s 23 — the figures `changelog.md` and `questions.md` W1 state |
| 🟢 | No statement the rounds disproved is standing | `tests/test_the_gate_names_every_step_ci_runs.py:287` | not a defect | **Executed.** `Six of the eight` returns only the round records' quotations of round 1's finding. The test module's docstring at `:287` says `hygiene.yml` declares one job, which is round 1's finding 4 closed at its second coordinate |
| ⬜ | G6 and G7's widened Claims name behaviour whose pinning cases are in neither row's Code grounds, so `evidence-check` cannot notice if those cases are renamed away | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` G6, G7 | correction | The four cases are `test_a_step_no_row_classifies_is_not_said_to_carry_a_reason`, `test_a_step_a_row_excludes_is_still_pointed_at_its_reason`, `test_the_two_clauses_render_together_and_hold_the_right_names` and `test_a_workflow_that_is_not_utf8_leaves_the_run_as_it_was`. Round 2's ⬜ was that the Claim column is the checkable half; the Claim moved and the coordinate column did not, so a re-reader auditing either row still reaches those cases through Notes prose alone |
| ⬜ | The `Verified behavior` cells of the same two rows were not widened with their Claims | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` G6, G7 | correction | G7's names two mutations, both about the absent-workflow shape; G6's names five, none about the two-clause split. The branch's convention puts later evidence in a `Re-read` marker inside Notes and both rows carry one, so this is a note rather than a repair — a reader who takes `Verified` as the row's evidence gets a pre-round-1 answer beside a post-round-2 Claim |
| ⬜ | `ee53b03`'s subject names one of the three things the commit does, and the omitted two are round 2's ⬜ corrections | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/rounds/round-2.md` Fix range | correction | The commit also widened both ledger Claim cells and planted `test_the_two_clauses_render_together_and_hold_the_right_names`; `b3f3dab`, whose subject is about the counts, touches `overview.md` alone. This round's own spawn prompt attributed the corrections to `b3f3dab` and was wrong, which is the demonstrated cost |
| ⬜ | Pull request 472's body states verification numbers the fix passes moved — 19 mutations against 25, and 469 passed against a module that has gained 4 cases | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/overview.md:41` | correction | The same class `b3f3dab` closed in the proof block; the enumeration stopped at the tracked files. `overview.md` §*What `CONTRIBUTING.md` asks* says the four gate clauses are answered there **and the pull request body carries them**, so the body is a required artifact of this change. Nothing ships wrong — the changelog fragment carries no count. One `gh pr edit` before the pull request is marked ready, and it is the orchestrator's: an agent posts nothing |
| ⬜ | `skills/verify/SKILL.md` says *this repository* twice in a section describing SpecSeal's own CI, in a file that ships to every installation | `skills/verify/SKILL.md:355`, `skills/verify/SKILL.md:360` | correction | Read from a plugin cache the phrase has no referent but the reader's own repository, and the sentence then tells them their workflow guards two steps on a `main` base. The paragraph is fenced by `#473`, `#424` and `hygiene.yml`, so the misreading needs a reader who skips the anchors — hence a correction and not a finding. `CLAUDE.md`'s *a thing more than one party can have is named with whose* is the rule; *SpecSeal's own `release` job* is the repair |
| ⬜ | *half a pin, which is #423's finding 4* characterises that finding as something it did not say | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/spec.md:52`, `tests/test_the_gate_names_every_step_ci_runs.py:14` | correction | #423's round 1 finding 4 is *the drift pin reads three of the workflow's base spellings, not all of them* — a narrow reader, and it names both directions, including a false red when a step is refactored to `--baseline "$BASE"`. The same test module at `:29` attributes the closer sentence to **#424's** finding 4. Predates this range; neither earlier round opened it. The coordinate outlives the merge, since it is a committed record and only the issue closes |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the repository at the target SHA, then `bin/test tests/test_the_gate_names_every_step_ci_runs.py -q` | exit 0 — `24 passed in 8.74s` |
| `evidence_check.py .` unscoped, no `--ledger`, same clone, exit code read directly | exit 0 — `total: 1398 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; the work item's own fragment `13 ok`; records arm `3 work items read · 92 unread · 290 names read · 0 refused · 0 drifted` |
| Enumeration angle 3 — the class's SUBJECT rather than its phrasing or its number | seven places outside the round records, all seven naming #473; the reciprocal `473` grep adds none; the `423` grep leaves only historical references |
| `gh issue view 423`, `gh issue view 473` | 423 OPEN, milestone `release: 0.12.2`; 473 OPEN, milestone `backlog: gates & hooks` |
| `gh pr view 472` body read for an eighth copy of the class | none — it names #423 once, for a different claim (correction ⑥) |
| Mutation: clause A learns to claim every unanswered step, anchor asserted unique and asserted gone after substitution | exit 1 — red: `test_the_two_clauses_render_together_and_hold_the_right_names` and `test_a_step_no_row_classifies_is_not_said_to_carry_a_reason` |
| Mutation: clause B learns to claim every unanswered step, same assertions | exit 1 — red: `test_the_two_clauses_render_together_and_hold_the_right_names` and `test_a_step_a_row_excludes_is_still_pointed_at_its_reason` |
| Mutation: the second clause rendered only when the first did not | exit 1 — red: `test_the_two_clauses_render_together_and_hold_the_right_names` **alone** |
| Mutation: the first clause rendered only when the second did not | exit 1 — red: `test_the_two_clauses_render_together_and_hold_the_right_names` **alone** |
| Mutation: round 1's two-populations-merged substitution, re-run | exit 1 — red: the new case and `test_a_step_no_row_classifies_is_not_said_to_carry_a_reason`; `broad_gate.py` restored from bytes kept outside the edit and the module re-run green each time |
| `coverage_line` and `unanswered` rendered against this repository's own workflow | 13 steps, 8 unanswered, 5 answered; the unknown clause empty; panel value `8 of 13 not answered`, 20 columns of `PANEL_VALUE_WIDTH`'s 23 |
| The broad gate — the full suite, the repository-wide lint and the typecheck | **not yet.** It is the sealer's one run, `agent-contract` §2 keeps it out of every review round, and the last round record's `Broad gate` cell is the sealer's to write. It has come due: this report leaves nothing needing a fix |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:1300` | round 1's 1 — fixed |
| round-1 | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/spec.md:119`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/overview.md:91` | round 1's 2 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py:1446` | round 1's 3 — fixed |
| round-1 | `tests/test_the_gate_names_every_step_ci_runs.py:284`, `tests/test_the_gate_names_every_step_ci_runs.py:296` | round 1's 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1398` | round 1's 5 — fixed |
| round-1 | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/overview.md:19` | round 1's ⬜ — correction |
| round-1 | `skills/verify/scripts/broad_gate.py:1237` | round 1's ⬜ — correction |
| round-1 | `seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md:4` | round 1's ⬜ — correction |
| round-1 | `skills/verify/scripts/broad_gate.py:1310` | round 1's 🟢 — not a defect |
| round-1 | `skills/verify/scripts/broad_gate.py:1226` | round 1's 🟢 — not a defect |
| round-1 | `seal/ledger.md:1945`, `seal/ledger.md:1949`, `seal/ledger.md:2230` | round 1's 🟢 — not a defect |
| round-1 | `skills/verify/scripts/broad_gate.py:1697` | round 1's 🟢 — not a defect |
| round-1 | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/plan.md` | round 1's 🟢 — not a defect |
| round-2 | `skills/verify/SKILL.md:352-355`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/questions.md:29` | round 2's 1 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:1423` | round 2's 🟢 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:1467`, `tests/test_the_gate_names_every_step_ci_runs.py:781` | round 2's 🟢 — answered |
| round-2 | `tests/test_the_gate_names_every_step_ci_runs.py:284`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/spec.md:79` | round 2's 🟢 — answered |
| round-2 | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` G4 | round 2's 🟢 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py` | round 2's 🟢 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:1467` | round 2's 🟢 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:1408` | round 2's 🟢 — answered |
| round-2 | `seal/follow-up.md` | round 2's 🟢 — answered |
| round-2 | `tests/test_ci_gives_the_checks_what_they_need.py:37` | round 2's 🟢 — answered |
| round-2 | `seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md` R2 | round 2's 🟢 — answered |
| round-2 | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` G6, G7 | round 2's ⬜ — correction |
| round-2 | `tests/test_the_gate_names_every_step_ci_runs.py:743` | round 2's ⬜ — correction |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
