# 1789956662-the-gate-and-ci-ask-about-different-ranges — review round 3

| Field | Value |
|---|---|
| Target SHA | 4d975beac8a5cde4cb66da9d6e0c7dfa595f6cdc |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 459 |
| Broad gate | 7a9513f against release/v0.12.2 |
| Fixes checked by | no fixes to check |
| Fix range | `4d975beac8a5cde4cb66da9d6e0c7dfa595f6cdc..50c5abb5800d11caeba1168cdf37f56b610da3ff`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 15 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, the round the chain's own arithmetic had already made the last:
`round_record.py new` said when it wrote round 2's record that one reopening
remained, and round 2's verdicts closed on a fix. The reviewer was told that
before it started — not to look less hard, but because severity is the only
thing left that changes an outcome once the record after this one cannot
exist.

Its target was one commit, `11013826`, the whole of round 2's fix range, which
closed round 2's finding 9. Three judgments in that commit were handed over as
the round's own rather than as facts: whether the third assertion the round-2
report offered was rightly NOT planted, since the builder measured that it
cannot fail while the two above it pass; whether the builder's correction to
round 2's own account of the cause is the true one, the population rather than
the pronoun; and whether any of the five ⬜ findings deferred to #461, #462,
#463 and #464 should have blocked instead — the one judgment I would rather
hear now than at the pull request.

Beyond the commit, the work item as a whole was asked about: whether the
documents agree with the code, whether any statement the three rounds
disproved is still standing anywhere, and whether the ledger fragment's rows
say what the code does. The pull request body was named as a surface no check
reads, so the reviewer was told to open the live one.

`evidence_check.py .` unscoped. Exit codes read directly. The report's verdict
table was told the shape round 2's had been sent back for: a verification row
is 🟢 with `not a defect`, never an empty id with `answered`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 15 | 🟡 round 1 finding 3's claim is standing in three more places, one of them the measurable form | `tests/test_the_gate_asks_the_range_ci_will_ask.py:68` | deferred #465 | Executed: the branch changed the sealer's fixture module at `c674ac2`, 8 insertions and 1 deletion, 147448 to 147980 bytes, and `git diff --name-only` over the branch names it — so *byte-identical* at `:68`, *reading exactly as it did* at `:19` and *keeps that module reading as it did* at `:377` are all false. `survivor-check` is right to print nothing: no range removed this wording. The claim was rated 🟡 at round 1 finding 3 and again at round 2 finding 9. The run is capped, so the home is a new issue and the number goes in this cell |
| 16 | ⬜ correction — the new `overview.md` section miscounts round 1's corrections and describes a corrected body in the present tense | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/overview.md` | answered | Executed at `327ef1f`: the sentence stood in `changelog.md`, `spec.md` §Scope 2, `broad_gate.py` and the test module, and round 1 corrected three of them at `e1dc0bc1` and `9abf7a6`. `overview.md` §*Fed back into the spec* read `none` there and never carried the sentence. The count came from round 2's report. Pull request 459's body no longer says *its* run. Paperwork, so it is out of `Needs a fix`; a hand correction before the record is written closes it `answered` instead |
| 🟢 | round 2 finding 9 verified — the A8 docstring, and the third assertion rightly not planted | `tests/test_the_gate_asks_the_range_ci_will_ask.py#test_a_base_with_no_remote_counterpart_resolves_to_itself` | not a defect | Executed three arms: planted with the fallback mutated to hand the ref, the failure is the assertion ABOVE it; planted against correct code, exit 0. It cannot fail, so `skills/verify/SKILL.md` §*The Seal Test* is the right clause and the comment in its place states what was measured. The corrected docstring says what the assertions already pin |
| 🟢 | the corrected account of the cause verified | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/overview.md` | not a defect | Executed: `git show e1dc0bc1^:tests/…` carries *nothing about that run changes* verbatim at line 336, and `e1dc0bc1` touched two files while its message names three. The population is the right diagnosis, the pronoun belongs to the pull request body, and both table rows are right. The count is finding 16 |
| 🟢 | the five deferrals verified — each home says what the finding said | `skills/verify/scripts/broad_gate.py#names_a_branch` | not a defect | Read #461, #462, #463 and #464 against round 2's five verdict rows: each carries the measurement, the coordinate and the reason it is ⬜. Nothing in the code moved for any of them and all four squares still stand, which is what the verdicts say. None should have blocked — #462 is the closest and is a test helper that fails closed over a workflow that is correct today |
| 🟢 | pull request 459's body verified | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/rounds/round-2.md` | not a defect | Read live with `gh pr view 459`: the remote-less paragraph states the moved half in the sentence after it, and the verification section names three survivor rows with none firing. Round 2's two complaints about the body are answered |
| 🟢 | the ledger fragment verified on the claims, not the hashes | `seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md` | not a defect | `evidence_check.py .` unscoped: exit 0, the fragment 8 ok, 1370 ok in total. Each of R1 to R7 read against the code it anchors. R1 says *a spelling `git check-ref-format --branch` accepts* and does not repeat the docstring's class claim, so #461 does not reach the ledger |
| 🟢 | the records are well formed for the sealer | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/rounds/round-2.md` | not a defect | Executed `chain_check.py --baseline origin/release/v0.12.2`: exit 1 on two conditions only — `Broad gate` is `not yet`, and `Pass` is checked beside `Fixes checked by: nobody`. This record closes the second and the sealer closes the first |

## Paste-ready fixes

```python
"""...
This module holds the repair. Three halves, and they go red for different
edits:

  the resolver    `resolve_base` reaches for what CI will read — the given
                  ref's upstream where the checkout declares one, else
                  `refs/remotes/origin/<base>`, else the ref as given. A
                  repository with no remote at all resolves to itself, which
                  is what keeps all but ONE assertion of
                  `tests/test_the_seal_is_taken_once_by_the_sealer.py`
                  reading as it did. The one that moved is the `Broad gate`
                  cell's base half: the consumers are handed the resolved
                  commit even where the resolution lands on the ref as given
                  (round 1, finding 3, and the A3 row of `overview.md`)
"""
```
```python
# --- fixtures: a repository that actually has a remote ----------------------
#
# Every gate fixture in `tests/test_the_seal_is_taken_once_by_the_sealer.py`
# is built by a `git init` with no remote, which is why the fallback leaves
# almost all of that module alone (A3). It is NOT byte-identical: one
# assertion in `test_the_gate_with_record_seals_the_item_and_counts_its_rounds`
# reads the commit where it read the ref, because the consumers take the
# resolved commit even where the resolution lands on the ref as given
# (round 1, finding 3). A remote is new work, and it is built here rather than
# there so that one moved reading stays checkable by reading the diff.
```
```python
def test_a_repository_with_no_remote_at_all_resolves_to_the_ref_as_given(tmp_path):
    """The fallback A3 rests on. Every gate fixture in the suite today is
    exactly this repository, so the answer here is what keeps all but one
    assertion of `tests/test_the_seal_is_taken_once_by_the_sealer.py` reading
    as it did. What still moves there is the spelling the consumers get, which
    is round 1's finding 3."""
```
```markdown
## What the review chain kept finding, and it was not one cause

One sentence — *nothing about that run changes* — stood in four places, and
round 1 corrected three: `changelog.md` and `resolve_base`'s docstring at
`e1dc0bc1`, `spec.md` §Scope 2 at `9abf7a6`. It survived in the A8 case's
docstring and in pull request #459's body. One claim about the workflow
reader was corrected in two places and survived in a third. Both times the
pass reached for the class rather than the coordinate, so `agent-contract`
§12 is not what it ran into. It enumerated the class over a population that
could not hold every member, and the population was wrong in a different way
each time.

| Survivor | Why the sweep could not reach it |
|---|---|
| the A8 case's docstring | The finding-3 pass grepped `nothing about that run` over **three named files** — the two it was editing and the spec. The test module carried the phrase verbatim, so the pattern would have matched it; the file list is what excluded it |
| pull request #459's body | Outside the tree, so no grep over the repository reaches it at all, and it said *its* run where every corrected copy says *that* run — a tree-wide search for the corrected phrasing would have missed it too. Corrected from the orchestrator's side during round 2 |
| `phases/phase-4.md`'s claim | Inside the tree and inside this work item, found only because `survivor-check` ran over the fix pass's own range afterwards |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_gate_asks_the_range_ci_will_ask.py tests/test_the_seal_is_taken_once_by_the_sealer.py -q`, in a clone at the target SHA | exit 0 — 152 passed in 72s |
| `evidence_check.py .` unscoped, same clone | exit 0 — 1370 ok · 0 drifted · 0 broken · 0 external · 0 old-format; this work item's fragment 8 ok; the records arm 100 names read · 0 refused |
| `survivor_check.py --range 2f1010c9...HEAD`, no `--exempt` | exit 0 — 1 sentence removed by round 2's fix range, none still standing |
| `survivor_check.py --range origin/release/v0.12.2...HEAD`, no `--exempt` | exit 0 — 19 sentences removed, none still standing |
| `chain_check.py --baseline origin/release/v0.12.2`, same clone | exit 1 — `Broad gate` is `not yet`, and `Pass` is checked beside `Fixes checked by: nobody`. Both are this moment in the chain; no record is malformed |
| `deferral_check.py`, same clone | exit 0 |
| probe — the third assertion planted, the resolver's fallback mutated to hand the consumers the ref | exit 1 at `assert base.commit == short(work, "never-pushed")`, the line above it. Planted against correct code, exit 0. Unreachable as a failure. Verifies the fix commit's judgment |
| probe — `git show e1dc0bc1^:tests/test_the_gate_asks_the_range_ci_will_ask.py` | *nothing about that run changes* verbatim at line 336. The pattern would have matched; the file list excluded it. Finding 16's other half |
| probe — `git diff --stat` and a byte count of `tests/test_the_seal_is_taken_once_by_the_sealer.py` over `release/v0.12.2..HEAD` | 8 insertions, 1 deletion; 147448 to 147980 bytes; `git diff --name-only` names the file. Finding 15 |
| probe — the sentence's copies at `327ef1f` and the removals across `327ef1f..da117184` | four copies, three removals. Finding 16 |
| the broad gate — the full suite, the repository-wide lint and the typecheck | not yet, in as many words. It is the sealer's one run and it comes due now: this round closes every verdict, so the rounds have settled (`agent-contract` §2). CI's `lint`, `ledger`, `release` and three `pytest` legs are green on this branch, which is a different act |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md` | round 1's 1 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py#moved_line` | round 1's 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#resolve_base` | round 1's 3 — fixed |
| round-1 | `tests/test_the_gate_asks_the_range_ci_will_ask.py#workflow_base_arguments` | round 1's 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#panel` | round 1's 5 — fixed |
| round-1 | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/spec.md` | round 1's 8 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py#gate` | round 1's 🟢 — not a defect |
| round-1 | `skills/code-review/scripts/chain_check.py#broad_gate` | round 1's 🟢 — not a defect |
| round-1 | `tests/test_the_gate_asks_the_range_ci_will_ask.py#says_what_the_base_resolves_to` | round 1's 🟢 — not a defect |
| round-1 | `seal/ledger.md` | round 1's 🟢 — not a defect |
| round-2 | `tests/test_the_gate_asks_the_range_ci_will_ask.py:340` | round 2's 9 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py#names_a_branch` | round 2's 10 — deferred |
| round-2 | `tests/test_the_gate_asks_the_range_ci_will_ask.py#BASE_ARGUMENT` | round 2's 11 — deferred |
| round-2 | `tests/test_the_gate_asks_the_range_ci_will_ask.py#base_spellings` | round 2's 12 — deferred |
| round-2 | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/rounds/round-1.md` | round 2's 🟢 — not a defect |
| round-2 | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/survivors.md` | round 2's 🟢 — not a defect |
| round-2 | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/phases/phase-4.md` | round 2's 🟢 — not a defect |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 15 — the claim standing at `tests/test_the_gate_asks_the_range_ci_will_ask.py:19`, `:68` and `:377` | #465, opened before this record was written | the repository owner |
| 16 — the new `overview.md` section's count and its present-tense row about the pull request body | corrected by the orchestrator at `50c5abb5`, in the closing commit, so it went to no issue | the orchestrator |
| round 2's 10, 11, 12, 13 and 14 | #461, #463, #462, #464 and #464 | the repository owner; already deferred in round 2 and the homes are verified above |
| M1 — whether a green gate can still meet a red CI because the base moved after the branch last took it in | `questions.md` M1, named as a standing limit in `spec.md` §*What this repair cannot see* | a measurement; already deferred in the frame |
| P1 — whether a refusal should survive anywhere in the gate | `questions.md` P1 | the repository owner. Answered by its default under this run's `Automation = yes`; already deferred in rounds 1 and 2 |
| widening `records_a_past_round` to exclude a work item's `phases/` records the way it excludes `rounds/` | a follow-up named in `survivors.md`'s first row and in `phases/phase-4.md` | a later work item; already deferred in round 2 |
| the new fixtures on Windows and Linux | this branch's pull request | CI's matrix; already deferred in rounds 1 and 2 |
