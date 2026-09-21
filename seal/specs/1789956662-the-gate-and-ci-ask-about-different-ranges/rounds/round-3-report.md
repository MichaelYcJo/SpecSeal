# 1789956662-the-gate-and-ci-ask-about-different-ranges — review round 3 report

Round 3, the verifying round over round 2's fix range: one commit,
`2f1010c9..11013826`, plus the record-closing commit `4d975be`. Target SHA
`4d975beac8a5cde4cb66da9d6e0c7dfa595f6cdc`, base `release/v0.12.2`, pull
request 459.

Rounds 1 and 2 were read whole — both records and both reports. Their fourteen
verdicts are carried and none is reopened: every fix that closed one does what
its cell says, and the six verification rows below say how each was checked.

**Two things the orchestrator has to act on before the record is written.**

- Finding 15 has no issue number yet. The run is capped, so its verdict closes
  on `deferred <home>` and the home is an issue that does not exist. Open it,
  then substitute its number into the verdict cell and into the `Deferred`
  table. Until that substitution the verdict row is not in the shape
  `round_record.py new` reads.
- Finding 16 is a correction in the run's own paperwork. Either home works:
  the coordinate goes into #464, or the orchestrator corrects `overview.md`
  by hand before the record is written and the cell then reads `answered`.

**`Needs a fix: yes` does not stop the seal on a capped run**, and this was
read rather than assumed: `round_record.py#seal`'s docstring records that the
refusal on a `yes` was removed in phase 5 of #30 because it made a capped run
unsealable, and that what answers *is a finding still open* is the `Pass` box,
from the verdict table. Every verdict below is closed, so `Pass` comes out
checked and `landing_values` gives `no fixes to check`.

## The findings

### 🟡 15 · the claim round 1's finding 3 opened is standing in three more places, all in one file

`tests/test_the_gate_asks_the_range_ci_will_ask.py:19`, `:68` and `:377`.

Round 1's finding 3 was that *a base with no remote-tracking counterpart
resolves to itself and nothing about that run changes* is false, because the
consumers are handed the resolved commit even where the resolution lands on
the ref as given. Round 2's finding 9 found the sentence surviving in the A8
case's docstring, and the commit under review corrected it there.

The same claim is stated three more times in that file, in a wording no grep
over the corrected sentence reaches. None has been touched since phase 1.

```
:19   A repository with no remote at all resolves to itself, which is what
      keeps every fixture in
      `tests/test_the_seal_is_taken_once_by_the_sealer.py` reading exactly
      as it did

:68   Every gate fixture in `tests/test_the_seal_is_taken_once_by_the_sealer.py`
      is built by a `git init` with no remote, which is why the fallback keeps
      that module byte-identical (A3).

:377  The fallback A3 rests on. Every gate fixture in the suite today is
      exactly this repository, so the answer here is what keeps that module
      reading as it did.
```

The middle one is the measurable form, and it is false:

```
git diff --stat release/v0.12.2..HEAD -- tests/test_the_seal_is_taken_once_by_the_sealer.py
  1 file changed, 8 insertions(+), 1 deletion(-)
bytes at release/v0.12.2   147448
bytes at 4d975be           147980
git diff --name-only release/v0.12.2..HEAD  names that file
```

The branch changed it at `c674ac2` — one assertion in
`test_the_gate_with_record_seals_the_item_and_counts_its_rounds` reads the
commit where it read the ref. That is not an accident of this branch. It is
the divergence row `overview.md` declares, the paragraph
`broad_gate.py#resolve_base` now carries, and the clause `spec.md` §Scope 2
was corrected to. The file that states the opposite three times is the file
whose own A8 docstring was corrected for it one round ago.

`phases/phase-1.md` also carries the superseded reading — *A3 is then
`git diff --name-only` over the branch not naming the old one* — but
`phases/phase-2.md` §*What this phase found* records the divergence in the
next record along, which is how a phase record is meant to be read in
sequence. It is not part of this finding.

**Why the sweeps missed it and the new `overview.md` section does not cover
it.** `survivor-check` looks for wording a range REMOVED that is still
standing; these three say the same thing in words nobody removed, so it is
right that it printed nothing. The new section's lesson is about the
population a grep runs over, and its own population was the sentence rather
than the claim — the commit under review corrected one coordinate in a file
that carries three more of them three hundred lines away.

**Severity.** The identical claim was rated 🟡 twice by this chain, at round 1
finding 3 and round 2 finding 9. A third copy of it is 🟡 for the same reason:
behaviour is right and the stated fact is wrong, and the reader it misleads is
the next one who opens this module to find out what A3 means.

### ⬜ 16 · correction — `overview.md`'s new section miscounts, and describes a body that has since been corrected

`seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/overview.md`
§*What the review chain kept finding, and it was not one cause*.

Two statements in the section the commit under review added.

**The count.** It says the sentence *was corrected in four places by round 1*.
Measured at `327ef1f`, the round 1 target, the sentence stood in four places:
`changelog.md`, `spec.md` §Scope 2, `broad_gate.py#resolve_base` and the test
module. Round 1 corrected **three** of them — `e1dc0bc1` took the first two
and `9abf7a6` took `spec.md`. The fourth place round 2's report named,
`overview.md`, never carried the sentence at all: its §*Fed back into the
spec* read `none` at `327ef1f`, and `9abf7a6` gave it the record of the
correction rather than a correction of its own. The count came from round 2's
report; the commit under review corrected that report's account of the CAUSE
and carried its arithmetic forward unchecked.

**The tense.** The table row for pull request 459's body reads *it says `its`
run where every corrected copy says `that` run*, in the present. The body was
corrected from the orchestrator's side and no longer says it — checked with
`gh pr view 459`. A present-tense claim about a corrected state is the shape
this work item already paid for twice in `phases/phase-4.md`.

Neither is behaviour. Both are in the run's own paperwork, so this row is a
correction and is out of `Needs a fix`.

## What was verified and found sound

**The third assertion was rightly not planted (judgment 1).** Round 2's
paste-ready fix offered `assert base.commit != base.ref` as a third assertion
in `test_a_base_with_no_remote_counterpart_resolves_to_itself`. I planted it
and measured all three arms:

```
arm 1  assertion planted, the fallback mutated to hand the consumers the ref
       exit 1 — assert base.commit == short(work, "never-pushed")
                AssertionError: assert 'never-pushed' == 'bcd10d1'
       the failure is the line ABOVE the planted assertion; it is never reached
arm 2  assertion planted, code as committed          exit 0 — 1 passed
arm 3  tree as committed, same mutation              exit 1 — same line
```

It cannot fail. If the two assertions above it pass, `base.commit` is a hash
and `base.ref` is `never-pushed`, so the inequality holds by construction; and
the mutation that would make it interesting stops one line earlier. Declining
to plant it is what `skills/verify/SKILL.md` §*The Seal Test* asks, and the
comment left in its place says what was not planted, why, and how it was
measured. The absence is correct and so is the comment.

**The corrected account of the cause is the true one (judgment 2).** The
builder's claim is that the test module carried the literal corrected phrasing
at the time, so the pattern would have matched and the file list is what
excluded it. Verified at the commit:

```
git show e1dc0bc1^:tests/test_the_gate_asks_the_range_ci_will_ask.py | grep -n "nothing about"
  336:    false, so nothing about that run changes."""
git show --stat e1dc0bc1
  changelog.md | broad_gate.py    2 files changed
```

The phrase was verbatim in a file the commit did not open, and `e1dc0bc1`'s
own message names exactly three files — `resolve_base`'s docstring, the
changelog, and `spec.md` §Scope 2 for finding 8. So the population is the
right diagnosis and the pronoun is not; the pronoun belongs to pull request
459's body, which is where round 2's report put it. The corrected account is
right about both rows. Its count is finding 16.

**The five deferrals say what the findings said (judgment 3), and none of them
should have blocked.** Each issue was read against its verdict row:

| Round 2 | Home | Does the home say what the finding said |
|---|---|---|
| 10 — `names_a_branch`'s docstring names a class the command does not refuse | #461 | yes, with the measured table and the `origin/@{-1}` consequence |
| 11 — an empty baseline returns `None` and the caller raises | #463 | yes, and it names the widening that admits it |
| 12 — the reader counts a commented flag and any `BASE:` line | #462 | yes, and it names what makes the `BASE:` rule decidable |
| 13 — `panel`'s docstring leads with a retired argument | #464 | yes, including the `origin/` assumption in the elision's grounds |
| 14 — the baseline half of the direction claim has no label | #464 | yes, and it names the three operational statements |

Nothing in the code moved for any of them, which is what the verdicts say.
All four squares are still standing in the tree, at
`broad_gate.py#names_a_branch`, `broad_gate.py#panel`, the module-level
`BASE_ARGUMENT` and `base_spellings` in the test module, and the three
operational statements.

#462 is the only one worth arguing, and it stays ⬜. The reader it names is a
test helper; the workflow it reads carries one `BASE:` line and three flags and
all four are genuine, so nothing is red today; and the wrong answer is red
rather than green, so no seal is taken over it. A false refusal in this
repository's own suite costs a branch one commit, and the release ships no
defect if it stands.

**Pull request 459's body.** Read live. It carries the corrected wording — *the
arms then behave exactly as they did. What does change even there is what the
consumers are HANDED* — with the moved half stated in the next sentence, and
the verification section now says `survivors.md` carries three rows and none
of them fires. Round 2's two complaints about the body are both answered.

**The ledger fragment.** Seven rows, eight anchors, all resolving. Each claim
was read against the code rather than against its hash: R1's three-step rule
and the `check-ref-format --branch` guard match `resolve_base` as it stands;
R2's structural claim matches one read of `args.base`; R4's four promises match
`moved_line`'s two fillings, its second-remote branch and its named distance;
R5 matches `PANEL_VALUE_WIDTH`, `ELISION` and the tail-keeping elision in
`panel`; R6 matches `base_spellings` and `SHELL_VARIABLE`. R1's wording is
narrower than `names_a_branch`'s docstring and does not carry #461's
over-claim, so the fragment is clean where the docstring is not.

**The records.** `chain_check.py --baseline origin/release/v0.12.2` comes back
1 with exactly two conditions, and both are this moment rather than a defect:
`Broad gate` reads `not yet` on the last record, and `Pass` is checked beside
`Fixes checked by: nobody`. Writing round 3's record closes the second and the
sealer's run closes the first. No record is malformed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 15 | 🟡 round 1 finding 3's claim is standing in three more places, one of them the measurable form | `tests/test_the_gate_asks_the_range_ci_will_ask.py:68` | deferred | Executed: the branch changed the sealer's fixture module at `c674ac2`, 8 insertions and 1 deletion, 147448 to 147980 bytes, and `git diff --name-only` over the branch names it — so *byte-identical* at `:68`, *reading exactly as it did* at `:19` and *keeps that module reading as it did* at `:377` are all false. `survivor-check` is right to print nothing: no range removed this wording. The claim was rated 🟡 at round 1 finding 3 and again at round 2 finding 9. The run is capped, so the home is a new issue and the number goes in this cell |
| 16 | ⬜ correction — the new `overview.md` section miscounts round 1's corrections and describes a corrected body in the present tense | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/overview.md` | deferred #464 | Executed at `327ef1f`: the sentence stood in `changelog.md`, `spec.md` §Scope 2, `broad_gate.py` and the test module, and round 1 corrected three of them at `e1dc0bc1` and `9abf7a6`. `overview.md` §*Fed back into the spec* read `none` there and never carried the sentence. The count came from round 2's report. Pull request 459's body no longer says *its* run. Paperwork, so it is out of `Needs a fix`; a hand correction before the record is written closes it `answered` instead |
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
| round-1 | `skills/verify/scripts/broad_gate.py#resolve_base` | round 1's 3 — fixed; the paragraph that names the three consumers is the true statement the three in finding 15 contradict |
| round-2 | `tests/test_the_gate_asks_the_range_ci_will_ask.py:340` | round 2's 9 — fixed; the corrected docstring, and the comment standing in for the assertion |
| round-2 | `skills/verify/scripts/broad_gate.py#names_a_branch` | round 2's 10 — deferred #461 |
| round-2 | `tests/test_the_gate_asks_the_range_ci_will_ask.py#base_spellings` | round 2's 11 and 12 — deferred #463 and #462 |
| round-2 | `skills/verify/scripts/broad_gate.py#panel` | round 2's 13 — deferred #464 |
| round-2 | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md` | round 2's 14 — deferred #464 |
| round-2 | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/survivors.md` | round 2's 🟢 — the three rows may stand; re-measured exit 0 with no `--exempt` over both ranges this round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 15 — the claim standing at `tests/test_the_gate_asks_the_range_ci_will_ask.py:19`, `:68` and `:377` | a new issue, to be opened before this record is written; its number substitutes into the verdict cell | the repository owner |
| 16 — the new `overview.md` section's count and its present-tense row about the pull request body | #464, unless the orchestrator corrects `overview.md` by hand first | the orchestrator |
| round 2's 10, 11, 12, 13 and 14 | #461, #463, #462, #464 and #464 | the repository owner; already deferred in round 2 and the homes are verified above |
| M1 — whether a green gate can still meet a red CI because the base moved after the branch last took it in | `questions.md` M1, named as a standing limit in `spec.md` §*What this repair cannot see* | a measurement; already deferred in the frame |
| P1 — whether a refusal should survive anywhere in the gate | `questions.md` P1 | the repository owner. Answered by its default under this run's `Automation = yes`; already deferred in rounds 1 and 2 |
| widening `records_a_past_round` to exclude a work item's `phases/` records the way it excludes `rounds/` | a follow-up named in `survivors.md`'s first row and in `phases/phase-4.md` | a later work item; already deferred in round 2 |
| the new fixtures on Windows and Linux | this branch's pull request | CI's matrix; already deferred in rounds 1 and 2 |

Needs a fix: yes — finding 15
Loses a record or crashes: no

## Proof

Opened this round: `seal/specs/1789956662-.../rounds/round-1.md`,
`round-1-report.md`, `round-2.md`, `round-2-report.md`, `routing.md`,
`overview.md`, `survivors.md`, `changelog.md`, `spec.md`, `plan.md`,
`phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-4.md`,
`seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md`,
`skills/verify/scripts/broad_gate.py`,
`tests/test_the_gate_asks_the_range_ci_will_ask.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (at two revisions),
`skills/code-review/scripts/round_record.py` (the `seal` and `landing_values`
docstrings), `bin/test`, issues #461, #462, #463, #464, and pull request 459's
live body.

The clone was made with `git clone --no-local` at the target SHA and every run
above was taken in it. The probe file was deleted and the clone's working tree
is clean.
