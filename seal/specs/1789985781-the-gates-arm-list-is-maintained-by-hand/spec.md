# Feature Specification: the gate's arm list is maintained by hand (#468)

<!-- seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/spec.md — WHAT
this work delivers and how we'll know. The policy documents in docs/ outrank
this file; cite them, don't restate. -->

## What is wrong

`skills/verify/scripts/broad_gate.py#gate` runs five arms so that the sealer's
one run says what CI will say. `.github/workflows/hygiene.yml`'s `release` job
runs thirteen named steps. **Nothing holds the two lists against each other**,
and the gate's list is kept in step with the workflow's by whoever remembers.

0.12.2 is the release that made it bite. #424 added a step — *no merge on this
branch dropped a correction the ledger had made* — and the gate was not
extended, so from that merge onward a green seal covers a shorter list than
the merge is judged by. The reviewer that found it also found that **no case
in the suite goes red for the omission**: a coverage probe over the eight
structural modules that read those files reported 243 passed and 8 skipped
with the arm absent.

This is #423's defect from the other side. There, the gate asked a **smaller
question** than CI because a stale base narrowed its range. Here it asks a
**shorter list** of questions because a person maintains the list.

## What this frame measured, and what it deliberately did not

**Measured, by reading both files at `3878566`:**

| | |
|---|---|
| `broad_gate.py#gate`'s arms | five — the declared row, `evidence_check --strict`, `unverified_check`, `chain_check`, `survivor_check` |
| `hygiene.yml`'s `release` job | thirteen named steps |
| The step #424 added | *no merge on this branch dropped a correction the ledger had made* |

**Not measured, and the build must not inherit it as an assumption: how many
of the thirteen a gate COULD mirror.** Some plainly cannot be — a step that
asks GitHub which issues a pull request claims has no local answer. Others
plainly could. **The number of unmirrored-but-mirrorable steps is unknown to
this frame, and "it is one" is exactly the shape of claim that cost the
previous work item a 🔴.** Phase 1 enumerates the thirteen by construction and
classifies each; whatever falls out is the finding.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/verify/SKILL.md` §*The Seal Test* | A seal that covers less than the merge is judged by is a check that cannot fail in the direction that matters. That is the defect, stated in the plugin's own words |
| `CLAUDE.md` §*The goal a design is chosen against* | Nothing here may add a question a person answers. The pin must be a check, not a convention somebody is asked to follow |
| `skills/agent-contract/SKILL.md` §12 | The class is *every step of the release job*, not the one step #424 added. Enumerated by construction in phase 1 |
| `skills/agent-contract/SKILL.md` §14 | Whatever the gate prints about a step it does not mirror is read by a person deciding whether to trust a seal, so it ships with the case that pins it |
| `skills/agent-contract/SKILL.md` §15 | Every case seen red first, and the pin driven red **from both sides** — a reader that only one side can break is half a pin, which is #423's finding 4 |
| `docs/issues-and-milestones.md` §*A release is sized by…* | This is in 0.12.2 rather than the backlog because 0.12.2 opened the gap |

## Scope

### In

1. **A declared partition, in the gate, of every step of the workflow's
   `release` job.** Each step is either mirrored by a named arm, or excluded
   with a written reason. There is no third state and no silence.
2. **A structural case asserting the partition is total** — every step name in
   `hygiene.yml`'s `release` job appears in the gate's table. Adding a step to
   the workflow then fails the suite until somebody classifies it, which is
   what makes the seventh arm impossible to add silently.
3. **The arms the partition finds missing are added**, however many that turns
   out to be, including #424's `correction-check`.
4. **The gate says what it did not answer.** A seal covering fewer steps than
   the workflow runs is a fact a reader needs at the moment they read the
   stamp, not one they reconstruct from two files.
5. **A reason cell is prose a person wrote**, not a category. *Needs the pull
   request* and *needs the tracker* are reasons; `EXCLUDED` is not.

### Out, and why each

| Out | Why |
|---|---|
| Mirroring steps that have no local answer | A step that asks GitHub about the pull request cannot run in a gate with no pull request. It is excluded WITH ITS REASON, which is the deliverable, not skipped |
| The `ledger`, `lint` and `pytest` jobs of `.github/workflows/test.yml` | The gap is `hygiene.yml`'s `release` job list, and that workflow declares no other job. Those three are already answered by the declared row and the ledger arm, and widening the subject is how a bounded work item stops being one |
| Changing any step's behaviour | This work is about which list the gate runs, not about what any check decides |
| A generated gate that reads the workflow at runtime | The gate would then be correct by construction and unreadable — and it would import a YAML parse into a script that runs with no dependencies. The pin is a test, not a runtime coupling |
| Making the workflow read the gate | The workflow is the side the merge is judged by. It does not take its list from a script the branch can edit |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 | Given the workflow's `release` job, when the suite runs, then every one of its named steps appears in the gate's partition, mirrored or excluded-with-a-reason | a structural case; red when a step is added to the workflow and not classified |
| A2 | Given the gate's partition, when the suite runs, then every entry names a step the workflow actually has | the other direction; red when a step is renamed in the workflow, so the pin cannot rot into naming steps nobody runs |
| A3 | Given a step classified as mirrored, when the gate runs, then the arm it names actually runs | red when an arm is deleted from `gate()` while its partition row stands |
| A4 | Given an excluded step, when the suite runs, then its reason is prose rather than a bare marker | red against a reason cell reduced to a category word |
| A5 | Given a branch whose merge dropped a correction, when the gate runs, then it refuses — the arm #424's step needed | red against the gate as it stands today; this is the instance that started it |
| A6 | Given any successful run, when the stamp prints, then a reader can tell which of the workflow's steps the seal did not answer | a case over the rendered output, not only over the data; `seal_stamp.letter` cuts a value at 23 columns |
| A7 | Given the gate run in a repository with no `.github/workflows/hygiene.yml` at all, when it runs, then nothing about it changes | a case; the plugin ships to repositories that have no such workflow, and the partition is this repository's, not theirs |

**A7 is the one most likely to come back inconvenient.** The partition
describes *this* repository's workflow, and `broad_gate.py` ships to others. If
the partition cannot live in the gate without making the gate wrong elsewhere,
that is a divergence row naming where it moved to — a test fixture, a data
file beside the workflow — not a reason to drop A7.

## Data & interfaces

| Coordinate | What changes |
|---|---|
| `skills/verify/scripts/broad_gate.py#gate` | the arms the partition finds missing |
| `skills/verify/scripts/broad_gate.py` | the partition, and whatever prints what was not answered |
| `tests/` | the new module: A1–A7 |
| `.github/workflows/hygiene.yml` | **unchanged**, and held by A1 and A2 from both sides |
| `skills/verify/SKILL.md` | what the seal covers and what it does not |

## What this repair cannot see

- **A step the workflow runs in another job.** The partition is the `release`
  job's. A check added to `ledger` or to a new job is outside it, and the pin
  will not notice.
- **Whether a mirrored arm asks the same question as its step.** A1 holds that
  a step is classified; it cannot hold that the arm and the step agree about
  what they are checking. **#473 is the open home for the one live instance**
  — the gate runs the `survivors` and `corrections` arms unconditionally where
  the workflow skips both on a `main` base — and this work item does not close
  it. The frame named #423 here, and review round 1 corrected that: #423 is
  about the base the gate resolves, it ships in this release, and a fact whose
  only home is a closed record is a fact nobody finds.
- **A workflow on another branch.** The pin reads the tree it is in.

## Open questions → questions.md

One row needs a person — whether the partition lives in the gate or beside the
workflow. One is a measurement the build takes. Both carry the assumption the
build proceeds under.

Framed 2026-09-21 by the session, before the build.
