# 1789985781-the-gates-arm-list-is-maintained-by-hand — review round 2

| Field | Value |
|---|---|
| Target SHA | 9637b43eaa4f5f664f032a1594ec1c721dcc62fd |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 472 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `ad5954875dd0794fe875c8294d94a39f0fdc6d89..b3f3dab2ebc0feabc1773842133816beddaf807d`, 2 commits |
| Contract changes | none |
| New units | MIXED_WORKFLOW (depth 1); test_the_two_clauses_render_together_and_hold_the_right_names (depth 1) |
| Needs a fix | yes — finding 1, the two uncorrected copies of the class round 1's finding 2 repaired, one of which ships in `skills/verify/SKILL.md` |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round: round 1's fixes, opened by somebody. The
reviewer inherited round 1's committed record and was told its five verdicts
are closed and the range is `8ac8dd9..c0b0d71`, three commits.

It was told that **round 1 did not meet the floor** — its second terminal line
read `Loses a record or crashes: yes`, for the crash — so this round reads the
fixes for a round that found one, and the floor line had to be answered
explicitly rather than inherited.

Finding 5's fix was named as the one to verify **by reaching it rather than by
reading the diff**.

Four judgments were handed over. The mutation that survived because its anchor
landed at another occurrence of the same line, with the instruction to check
EVERY mutation this branch reports for the same trap — a mutation that lands
somewhere other than where it was aimed reports a passing case as evidence of
a pin that does not exist, and this work item's earlier passes made that
report eight times. The case that arrived green, and whether finding 3 would
close with the pointer deleted if that case were absent. The builder's
divergence from the reviewer's own paste-ready fix on finding 2, declining a
`seal/follow-up.md` row because #473 exists. And the trailing-comment gap
recorded rather than fixed, on the grounds that it is shared with the reader
it was copied from.

On the reviewer's own account: whether the new `UNCLASSIFIED_WORKFLOW` path
can print something a reader misreads, whether `workflow_text` now swallows an
error it should surface, and whether the ledger fragment's rows still say what
the code does after three of its own coordinates drifted and were re-verified
in the same pass.

`evidence_check.py .` unscoped, exit codes read directly, `seal/ledger.md` off
limits to a whole read, and the verdict-table shape spelled out after three
rounds in this session were sent back for an unkeyed row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The class round 1's finding 2 corrected has two more instances, and the fix reached neither. Both attribute *whether a mirrored arm asks its step's question* to #423, which is milestone `release: 0.12.2` and closes with this release; #473 is the home the same fix pass opened. `skills/verify/SKILL.md` ships to every installation | `skills/verify/SKILL.md:352-355`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/questions.md:29` | **fixed** `ee53b03` | fixed at ee53b03 — enumerated by grepping the claim from both sides, which found a seventh copy both rounds missed; Both lines are new on this branch. `gh issue view 423` — OPEN, milestone `release: 0.12.2`; `gh issue view 473` — OPEN, milestone `backlog: gates & hooks`, body naming both arms and the guard. The four coordinates the fix did reach say the opposite of these two, so the branch states both things |
| 🟢 | Round 1's finding 5 is closed, reached rather than read | `skills/verify/scripts/broad_gate.py:1423` | answered | **Executed.** `workflow_text` driven against a latin-1 `release` job in both versions of the file, the pre-fix one written out of git: `8ac8dd9` raised `UnicodeDecodeError ... byte 0xe9 in position 45`; the target SHA returned `None`, and `coverage_line` on that answer returned `None`. The case is red against `except OSError` alone and is the only case that is |
| 🟢 | Round 1's finding 1 is closed, and the audit behind it holds rather than only the edit | `skills/verify/scripts/broad_gate.py:1310` | answered | **Executed and read.** `Six of the eight` survives nowhere but round 1's own quotation of the finding. The 4/4 split checked step by step against the workflow: *both READMEs move together* emits `::warning::` and never exits non-zero; `issue_claims_check.py`'s only exit is `return 0`; the version-bump step is inline `bash` with no script; three steps run `.github/scripts/` scripts. Two copies tightened from an `or`, five already exact |
| 🟢 | Round 1's finding 3 is closed, and both halves are pinned | `skills/verify/scripts/broad_gate.py:1467`, `tests/test_the_gate_names_every_step_ci_runs.py:781` | answered | **Executed.** Merging the two populations back reddens `test_a_step_no_row_classifies_is_not_said_to_carry_a_reason` and nothing else; deleting the `PARTITION` pointer from the excluded half reddens `test_a_step_a_row_excludes_is_still_pointed_at_its_reason` and nothing else. Without the second case the first stays green through the pointer deletion, so the second is load-bearing rather than decorative |
| 🟢 | Round 1's finding 4 is closed | `tests/test_the_gate_names_every_step_ci_runs.py:284`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/spec.md:79` | answered | **Read.** `.github/workflows/hygiene.yml` declares `jobs:` at `:24` with `release:` as its only key; `lint`, `pytest` and `ledger` are jobs of `.github/workflows/test.yml`. Both corrected sentences say exactly that |
| 🟢 | Round 1's finding 2 is closed for the four coordinates the fix reached, and #473 is a durable home | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` G4 | answered | `gh issue view 473`: OPEN, milestone `backlog: gates & hooks`, body carrying the measurement and naming both arms. The two coordinates the fix did NOT reach are finding 1 above |
| 🟢 | No other mutation this branch reports could have landed silently somewhere other than where it was aimed | `skills/verify/scripts/broad_gate.py` | answered | **Executed.** The file carries three ambiguous anchors a reported mutation could have used. `    except (OSError, ValueError):` lands at `:463` in `config_text` and leaves the module GREEN — the silent trap, and the one the branch found. `            return handle.read()` lands at `:462` and reddens 7 cases; `        CORRECTIONS_NAME,` lands at `:1373` in `PARTITION` and reddens 12. Both of those fail too loudly to have been written up as *reddens it alone* |
| 🟢 | The new `UNCLASSIFIED_WORKFLOW` path prints nothing a reader misreads | `skills/verify/scripts/broad_gate.py:1467` | answered | **Executed** on both shapes. Against the real workflow one clause; against a mixed repository two, with no step name in both and each clause saying plainly which population it holds. The panel count is unchanged and says only how many are unanswered, which is true whatever the reason |
| 🟢 | `workflow_text` swallows no error it should surface, and the widened catch is the file's own idiom | `skills/verify/scripts/broad_gate.py:1408` | answered | **Read.** The `try` holds `os.path.join`, `open` and `read` alone; the only other reachable `ValueError` is `open`'s embedded-null-byte refusal for a root the rest of the gate could not use. `config_text` at `:458` has caught `(OSError, ValueError)` since before this work item |
| 🟢 | The builder's divergence from the paste-ready fix on finding 2 is sound | `seal/follow-up.md` | answered | **Read.** That file's own header admits a schedulable item only *in a repository with no tracker*; #473 is open and durable, and a second home for one fact is the state finding 2 was about. The row this branch did add there names no ticket, so it is the shape the file admits |
| 🟢 | The trailing-comment gap is shared with the reader `job_steps` follows, so the branch did not open it | `tests/test_ci_gives_the_checks_what_they_need.py:37` | answered | **Read.** `strip_comments` keeps a line unless `line.lstrip().startswith("#")`, so a trailing ` # why` survives it exactly as it survives `job_steps`. Recording it and writing it into the docstring is the right disposal |
| 🟢 | The ledger fragment rows resolve after the three re-anchorings, and round 1's line-number correction holds | `seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md` R2 | answered | **Executed.** `evidence_check.py .` unscoped: exit 0, `1398 ok · 0 drifted · 0 broken`. `resolve_base(root, args.base)` occurs once; `args.base` three times at `:1611`, `:1665`, `:1670`, exactly one a read. The line the row used to name has already moved to 1670, so the rot the correction removed was live |
| ⬜ | Two ledger fragment rows say the fix pass *widened the claim*, and no Claim cell was edited. G7 still reads *A repository with no `.github/workflows/hygiene.yml`*, which a latin-1 workflow is not; G6's claim says nothing about the two populations. The widening lives in Notes only | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` G6, G7 | correction | Under-claim rather than over-claim, so nothing in the ledger is false — but a re-reader auditing G7 against its Claim never reaches the case the third test pins, and the Claim column is the checkable half |
| ⬜ | No case renders both clauses of the new coverage sentence together. `UNCLASSIFIED_WORKFLOW` leaves `excluded` empty and the real workflow leaves `unknown` empty, so the joined sentence a mixed repository actually gets is pinned by nothing | `tests/test_the_gate_names_every_step_ci_runs.py:743` | correction | Driven by hand and correct — the two comprehensions are disjoint by construction, so this is a coverage note and not a defect. Recorded because the mixed sentence is the one a reader has to parse |

## Paste-ready fixes

```markdown
**What the count does not say** is whether a mirrored arm asks the same
question its step asks. The partition says a step is on the list; two readers
of one question can still disagree about what they are checking. **#473 is
the work item about that class**, opened with the one live instance this
repository has: the gate runs the `survivors` and `corrections` arms
unconditionally where the workflow skips both steps on a `main` base.
```
```markdown
- **This is not the class of whether a mirrored arm asks its step's
  question.** That one is #473's; this one is whether the step is on the list
  at all. The frame wrote #423 here and review round 1 corrected it: #423 is
  about the base the gate resolves, and it ships in this release.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_gate_names_every_step_ci_runs.py -q` in a `git clone --no-local` at the target SHA | exit 0 — `23 passed in 8.59s` |
| `evidence_check.py .` unscoped, no `--ledger`, same clone | exit 0 — `total: 1398 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm `3 work items read · 92 unread · 223 names read · 0 refused · 0 drifted` |
| `workflow_text` driven against a latin-1 `release` job, pre-fix and post-fix, the pre-fix module written out of git | pre-fix raised `UnicodeDecodeError ... byte 0xe9 in position 45`; post-fix returned `None`, and `coverage_line` on it returned `None` |
| Mutation: `workflow_text` back to `except OSError`, anchored on its own body | exit 1 — red: `test_a_workflow_that_is_not_utf8_leaves_the_run_as_it_was`, alone |
| Mutation: the naive first-occurrence form of the same substitution | landed at `broad_gate.py:463` in `config_text`; exit 0, **nothing red** — the silent trap reproduced |
| Mutation: `coverage_line`'s two populations merged back into one | exit 1 — red: `test_a_step_no_row_classifies_is_not_said_to_carry_a_reason`, alone |
| Mutation: the `PARTITION` pointer deleted from the excluded half | exit 1 — red: `test_a_step_a_row_excludes_is_still_pointed_at_its_reason`, alone |
| Mutation: naive first-occurrence `return handle.read()` → `return None` | landed at `:462` in `config_text`; exit 1, 7 cases red — loud |
| Mutation: naive first-occurrence delete of `        CORRECTIONS_NAME,` | landed at `:1373` inside `PARTITION`; exit 1, 12 cases red — loud |
| `coverage_line` rendered against the real workflow and against a mixed fixture | both clauses correct and disjoint; panel count `3 of 4` on the mixed fixture |
| The broad gate — the full suite, the repository-wide lint and the typecheck | **not yet.** It is the sealer's one run, after the rounds settle; `agent-contract` §2 keeps it out of this round, and the last round record's `Broad gate` cell is the sealer's to write. It comes due once finding 1 is answered |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
