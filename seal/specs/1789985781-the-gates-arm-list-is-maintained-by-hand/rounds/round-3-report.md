# round 3 — the verifying round, the gate's arm list is maintained by hand (#468)

Target SHA `eca3899ecdefc033a3292f0f64754def64c899b2`, branch
`fix/the-gates-arm-list-is-maintained-by-hand`, base `release/v0.12.2`,
draft pull request 472. The range read is `ad59548..b3f3dab`, two commits,
closing round 2's single finding. Rounds 1 and 2 were read whole — both
records and both reports — and their coordinates carried rather than their
verdicts.

Round 2 met the floor, so this round is the one that can end the run. Nothing
in the range needs a fix. Six corrections are recorded below, none of which
commissions a round: four are the run's own paperwork, one is a sentence in a
shipped skill, one is a characterisation that predates this range.

## What the range actually contains, against what the prompt said it contains

The prompt attributed the two ⬜ corrections — the widened ledger Claim cells
and the mixed-workflow case — to `b3f3dab`. Both landed in **`ee53b03`**.
`b3f3dab` touches one file and carries only the proof block's case and
mutation counts. This is a claim, not evidence, and it did not survive the
check: `git log --name-only ad59548..b3f3dab` names
`seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md`,
`.../changelog.md`, `.../questions.md`, `skills/verify/SKILL.md` and
`tests/test_the_gate_names_every_step_ci_runs.py` under `ee53b03`, and
`.../overview.md` alone under `b3f3dab`. The commit subject is what misled it;
correction ③ below is that subject.

## Round 2's finding 1 is closed, and the seventh copy is the last

I ran the enumeration from a **third angle**, independent of both the ones the
builder used. The builder grepped the class as prose and grepped the issue
number. Mine greps the **subject** — the behaviour the class is about, in the
words a writer would reach for without either the class phrase or a number:
`skips both`, `skips neither`, `unconditionally where`, `guards them on the
base`, `known non-equivalence`.

Outside the round records that angle returns exactly seven places, and every
one of them now names #473:

| # | Where | What it says |
|---|---|---|
| 1 | `skills/verify/SKILL.md:352-357` | #473 is the work item about that class |
| 2 | `seal/specs/…/spec.md:117-124` | #473 is the open home for the one live instance |
| 3 | `seal/specs/…/overview.md:99` | **#473 is its home.** #423 is not |
| 4 | `seal/specs/…/changelog.md:56-60` | #473 is the work item about that class |
| 5 | `seal/specs/…/questions.md:29-32` | That one is #473's |
| 6 | `seal/specs/…/phases/phase-2.md:31-40` | Its home is **#473** |
| 7 | `seal/ledger/1789985781-…md` G4 | Its home is **#473** |

The reciprocal grep for `473` adds nothing outside those seven and the round
records, and the grep for `423` leaves only historical references — the
prerequisite `#423` shipped, `#423`'s defect from the other side, `#423`'s
finding 4 — none of which is a live fact looking for a home. Pull request
472's body carries no copy of the class either; it names #423 once, for a
different thing (correction ⑥).

`gh issue view 473`: OPEN, milestone `backlog: gates & hooks`. `gh issue view
423`: OPEN, milestone `release: 0.12.2`, so it does close when this release
reaches `main`, which is what made the six attributions wrong in the first
place.

**So the branch has now named this class short three times and is not short a
fourth time.** The thing that closed it was enumerating by a property of the
claim rather than by the words the last fix happened to use, which is §12
working.

## The widened Claim cells do not over-claim, but they reach past their own coordinates

Round 2's ⬜ was that G6 and G7 under-claimed: the widening lived in Notes and
the Claim column, which is the checkable half, had not moved. The fix moved it.

**G6 does not over-claim.** Its new clause — *naming a step the partition
EXCLUDES with a reason apart from one it has no row for at all* — is exactly
what `coverage_line` does, and `coverage_line` is one of the row's own
coordinates, so a re-reader auditing G6 reaches the code that performs the
claim.

**G7 reaches two properties its own latin-1 case does not assert.** The
widened Claim reads *absent, or present and not UTF-8 — is sealed exactly as
it was: no panel row, no line, the same rows in the same order, and never a
traceback*. `test_a_workflow_that_is_not_utf8_leaves_the_run_as_it_was`
asserts four things: exit 0, `SEALED` on stdout, no `Traceback` on stderr, and
`not answered` absent from stdout. It does **not** assert the stderr line's
absence and does not compare the panel labels against `HISTORICAL_ROWS`, which
is what *no line* and *the same rows in the same order* mean; only
`test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before` does
that, and it is the absent-workflow shape.

I went and checked whether the widened half is nevertheless true. It is, and
transitively rather than by luck: `broad_gate.py` reaches both properties
through one guard — `coverage = coverage_line(workflow) if workflow else None`
— and `workflow_text` returns `None` for both shapes, so any change that broke
*same rows, no line* for the latin-1 shape breaks it for the absent shape too,
where a case does assert it. The row's Notes are honest about what the third
case asserts: *the seal, no traceback and no panel row*, three things, not the
Claim's four.

**Verdict: accurate, resting on a transitive pin.** Not the sign-flipped
defect the prompt asked about. What it leaves is correction ① — the Claim's
new halves name behaviour whose pinning cases are in no Code-grounds cell of
either row, so `evidence-check` will not notice if those cases are renamed
away.

## The mixed-workflow case earns its keep, and by more than the builder claimed

Round 2 recorded this as a coverage note rather than a defect, on the grounds
that the two comprehensions are disjoint by construction. The builder
disagreed and planted the case anyway. **The builder was right, and its own
grounds understate the case.**

Both mutations the branch reports — either clause learning to claim every
unanswered step — redden the new case, and each also reddens one of round 1's
two cases, so neither reddens it alone. The ledger does not claim they do;
G6's Notes say only *red when either clause learns to claim every unanswered
step*, which is what I measured. Both anchors are unique in the file
(`count(old) == 1` asserted before the substitution, and `old` asserted gone
from the file after it), so neither landed where it was not aimed — the trap
round 2 swept for.

Then I looked for a mutation that reddens the new case **alone**, because that
is what decides whether it is decorative. Two do:

- the second clause rendered only when the first did not
- the first clause rendered only when the second did not

Both leave `UNCLASSIFIED_WORKFLOW` and this repository's own workflow rendering
exactly as before — each of those fixtures populates one clause and leaves the
other empty — so round 1's two cases stay green and only
`test_the_two_clauses_render_together_and_hold_the_right_names` goes red. The
joined sentence has a pin nothing else provides, and *disjoint by construction*
was an argument about the comprehensions rather than about the two `if` blocks
that render them.

## The proof block's counts are exact

24 cases: 24 test functions defined in the module, 24 passed. 20 at the build,
3 in round 1's fix pass, 1 in round 2's — the two records' `New units` rows
account for each. 25 mutations: 19 + 4 + 2, and I reproduced round 2's two.
The `evidence-check .` figure the block rests on is unchanged at 1398.

The block also went from *A 24th missed its anchor* to *One more missed its
anchor*, which keeps the arithmetic right under a moving total — 25 counted
plus 1 missed. The builder corrected this unprompted, and round 1's ⬜ was
that same line going stale; a line that has now gone stale twice was made to
stop naming an ordinal.

## Corrections

**① The widened Claim cells' new halves are pinned by cases no coordinate of
their rows names.** `seal/ledger/1789985781-…md` G6 and G7. G6's Claim now
covers the two-clause separation, pinned by
`test_a_step_no_row_classifies_is_not_said_to_carry_a_reason`,
`test_a_step_a_row_excludes_is_still_pointed_at_its_reason` and
`test_the_two_clauses_render_together_and_hold_the_right_names`; G7's now
covers the not-UTF-8 shape, pinned by
`test_a_workflow_that_is_not_utf8_leaves_the_run_as_it_was`. None of those four
is in either row's Code grounds. The repair is to add them there, which is what
makes the claim checkable rather than readable — and it is the work item's own
subject, since a claim whose pin can be renamed away without a checker
noticing is a statement that stops being true in silence.

**② The `Verified behavior` cells were not widened with the Claims.** Same two
rows. G7's still names two mutations, both about the absent shape; G6's still
names five, none about the two-clause split. The branch's own convention puts
later evidence in a `Re-read` marker inside Notes, and both rows carry one, so
this is a note rather than a repair — but a reader who takes the `Verified`
cell as the row's evidence gets the pre-round-1 answer for a post-round-2
Claim.

**③ `ee53b03`'s subject names one of the three things it does.** *two more
copies of the class sent readers to an issue that closes with this release*.
The commit also widened both ledger Claim cells and planted a new case — round
2's two ⬜ corrections, which is what a reader looking for them would grep the
log for. They then read `b3f3dab`'s subject, *the proof block's case and
mutation counts follow the fix passes*, go there, and find one file. This
round's own spawn prompt did exactly that.

**④ Pull request 472's verification numbers went stale with the fix passes.**
The body states **19 mutations** and **469 passed, 7 skipped**; the branch now
records 25 mutations and the module alone has gained 4 cases since. This is the
same class the proof-block correction closed in `b3f3dab` — the branch's
statement of its own verification — and the enumeration stopped at the tracked
files. `overview.md` says the four gate clauses are answered there *and the
pull request body carries them*, so the body is a required artifact of this
change rather than commentary. Nothing ships wrong: the changelog fragment
carries no count, and the record and the proof block both carry the true ones.
One `gh pr edit` before the pull request is marked ready closes it. It is the
orchestrator's to make — an agent posts nothing.

**⑤ `skills/verify/SKILL.md:355` says *this repository* in a file that ships to
every installation.** The new sentence reads *the one live instance this
repository has: the gate runs the `survivors` and `corrections` arms
unconditionally where the workflow skips both steps on a `main` base*. Read
from a plugin cache, *this repository* has no referent but the reader's own,
and the sentence then tells them their workflow guards two steps on a `main`
base. The paragraph is fenced by `#473`, `#424` and `hygiene.yml`, all of which
are SpecSeal's, so the misreading needs a reader who skips the anchors — which
is why this is a correction and not a finding. `CLAUDE.md`'s *a thing more than
one party can have is named with whose* is the rule; *SpecSeal's own `release`
job* is the repair, and the same swap is available at `:360`, which the same
section already spells the same ambiguous way.

**⑥ *half a pin, which is #423's finding 4* characterises that finding as
something else.** `seal/specs/…/spec.md:52`,
`tests/test_the_gate_names_every_step_ci_runs.py:14`, and pull request 472's
body. #423's round 1 finding 4 is *the drift pin reads three of the workflow's
base spellings, not all of them* — a **narrow** reader, and the finding names
both directions explicitly, including a false red when a step is refactored to
`--baseline "$BASE"`. *A reader that only one side can break* is a different
property, and it is the one A1/A2 hold here. The same test module at `:29`
attributes *a reader nothing drives is a reader nobody can tell is partial* to
**#424's** finding 4, which is the closer fit for what #423's finding 4 said.
This predates the range under review and neither earlier round opened it; the
coordinate stays reachable after the merge, since it is a committed record and
only the issue closes. Recorded so a reader who opens finding 4 expecting
one-sidedness is not left thinking the record is wrong.

## What this round did not do

The broad gate — the full suite, the repository-wide lint and the typecheck —
was not run. It is the sealer's one act, `agent-contract` §2 keeps it out of
every review round, and the last round record's `Broad gate` cell is the
sealer's to write. **It has now come due:** this report leaves nothing needing
a fix, so what is next is the sealer's spawn, not a run for the session
reading this to assemble.

`seal/ledger.md` was not read whole, by instruction. It was read at the rows
the greps returned.

## The seal judgment asked for

Taking the work item as a whole rather than the range:

- **The documents agree with the code.** `coverage_line` rendered against the
  real workflow gives 13 steps, 8 unanswered, 5 answered, and the second clause
  empty. `changelog.md` says *8 of 13 not answered*; `questions.md` W1 says the
  panel value is 20 columns of the 23 it has, and it measures 20; `spec.md`,
  `overview.md` and `skills/verify/SKILL.md` say six steps had a local answer
  and two became arms, and `PARTITION` has 13 rows of which 5 are arms.
- **No statement the rounds disproved is still standing.** *Six of the eight*
  survives nowhere but the round records' own quotations of the finding. The
  jobs-that-do-not-exist sentence is corrected at both coordinates and the test
  module at `:287` now says `hygiene.yml` declares one job. The six #423
  attributions are all #473.
- **The fragment's rows say what the code does.** `evidence_check.py .`
  unscoped: exit 0, `1398 ok · 0 drifted · 0 broken`, the fragment's own 13
  coordinates all ok. G1–G8 read against the code; G6 and G7 carry corrections
  ① and ②, which are about where the evidence is cited rather than about
  whether the claim is true.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

Needs a fix: no
Loses a record or crashes: no

## Proof block

Opened: `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/rounds/round-1.md`,
`rounds/round-1-report.md`, `rounds/round-2.md`, `rounds/round-2-report.md`,
`overview.md`, `spec.md`, `questions.md`, `changelog.md`, `phases/phase-2.md`;
`seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md`;
`seal/follow-up.md`; `skills/verify/SKILL.md`;
`skills/verify/scripts/broad_gate.py`;
`tests/test_the_gate_names_every_step_ci_runs.py`;
`seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/rounds/round-1.md`
and `rounds/round-1-report.md` at finding 4;
`seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/rounds/round-1.md`
at finding 4; `seal/ledger.md` at the rows the greps returned, never whole;
`.github/workflows/hygiene.yml`; `CLAUDE.md`; issues 423, 468 and 473; pull
request 472's body.

Executed in a `git clone --no-local` at the target SHA and nowhere else. Two
probe scripts were written, run and deleted; the clone and its virtual
environment went with them.
