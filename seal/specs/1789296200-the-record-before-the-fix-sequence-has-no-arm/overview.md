# 1789296200-the-record-before-the-fix-sequence-has-no-arm — overview

📋 implement applied
· spec:     `seal/specs/1789296200-…/{spec.md,plan.md,questions.md,routing.md}`; `CONTRIBUTING.md` §*What a change to a gate must carry* and §*House rules*; `CLAUDE.md` §*The goal a design is chosen against*, §*Repo rule — the merge method is fixed per direction*, §*a change writes fragments, never the shared file*, §*a thing more than one party can have is named with whose*; `docs/review-chain-spec.md` §*When the record was written — before the fixes it commissioned*; `skills/code-review/orchestration.md` §*And commit the record before commissioning the fixes*; `skills/agent-contract/SKILL.md` §§2, 4, 5, 7, 8, 9, 12, 14, 15
· evidence: `seal/ledger/1789296200-the-record-before-the-fix-sequence-has-no-arm.md`
· verified: see `## Not verified` below, and each phase record's own account

## Why this work exists

`round_record.py new` is the last command before the fix pass is dispatched, it
knows both the commit the reviewer read and the branch's HEAD, and it compared
them for nothing — so a record written after its own fixes was first said out
loud at the pull request, on a line no later commit could clear.

## What the gate change carries

`CONTRIBUTING.md` §*What a change to a gate must carry* applies twice here, and
this section is where the pull request body draws from.

### The new line at `new` — what it costs a correct run

**It costs no run anything, because it refuses nothing.** Phase 1 measured the
frequency the refusal shape would have fired at and the criterion set in
`questions.md` Q1 before the number was taken — *0 or 1 differing record →
refuse; 2 or more → print and continue* — resolved to **print**.

**The number: 40 differing records out of 152 measurable ones — 26% of correct
runs.** `phases/phase-1.md` holds the method, the exclusions, the stated bias,
and the 40 named individually. The two opened by hand both differ because the
round's own paperwork landed between the review and the record (`docs: round
1's paragraph is recorded before the round runs`), not because a fix pass ran
early. A refusal would have fired on one correct run in four.

- **Failure direction: neither.** The observation prints and returns the exit
  code it returned before, so the gate neither blocks more nor allows more.
  What changes is what a reader is told.
- **Prompt budget: zero added.** No question reaches a person, per session or
  otherwise. This is the axis `CLAUDE.md`'s first goal is argued on, and the
  measurement is what moved the design onto the free side of it.
- **A test seen red:** `phases/phase-2.md` says how.
- **Platform honesty:** the observation is `git rev-parse HEAD` through the
  helper `round_record.py` already uses for every other git call, so it carries
  no platform assumption the rest of the file does not already carry.

### The new pass state in `written_late` — what it lets through

**A round record that was written after its own fixes and says why.** Today
that record fails the pull request on a line no later commit can clear, which
is where work item 1789034970 ended: three bad exits — rewrite history, merge
red, or invent an undocumented waiver. Q2 is the owner's answer authorising the
fourth.

- **What it does NOT let through:** a late record with no reason, and a late
  record whose reason is empty. Both are judged exactly as they are today —
  `phases/phase-4.md` and acceptance A6 pin it, and A6's pin is the existing
  case, still green and unmodified.
- **Failure direction: allows more**, deliberately and by exactly one state.
  It is the cheaper mistake because the thing it allows is a record that has
  written down a fact nothing else in the tree records, and the alternative it
  replaces is not a stricter tree — it is a history rewrite or a merge over
  red, both of which lose the fact entirely.
- **Prompt budget: zero added.**
- **A test seen red:** `phases/phase-4.md` says how.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where phase 1's measurement is taken | `plan.md` phase 1: *Over every `rounds/round-N.md` under `seal/specs/`* — which reads as the tree this branch stands in | the pre-squash refs (`refs/remotes/pull/N/head` and the local feature branches) | On `main` the answer is 0 same / 0 measurable: a feature branch squashes into its release branch (`CLAUDE.md` §*Repo rule — the merge method is fixed per direction*), so the commit the reviewer read was discarded with the branch. The moment the question is about exists only inside a live branch — which is the same fact `chain_check.added_on_branch` is built around. `phases/phase-1.md` holds the numbers both ways |
| A2's verdict at `new` | `spec.md` A2: *Then it refuses* | prints and continues | `spec.md`'s own clause under that table: *A2's verdict — refuse, or print and continue — is set by phase 1's measurement, not by this table*, and `plan.md`'s alternatives row *Print a line, refuse nothing* held as phase 1's fallback. The measurement resolved it |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator — `agent-contract` §2 makes the broad gate one act with one owner, and it is not this segment's |

## Not done

Nothing yet.

## Fed back into the spec

none
