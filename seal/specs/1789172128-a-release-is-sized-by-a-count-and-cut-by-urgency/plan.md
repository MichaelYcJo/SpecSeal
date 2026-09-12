# Implementation Plan: a release is sized by what has to be in effect next, and the count is named as a ceiling

<!-- seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/plan.md —
HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-12 by the repository owner, when `smith` was spawned.

The approval is the question batch this plan's alternatives table is the menu for: Q1 chose how the two releases are cited, which is the choice the
whole shape turns on, and Q2, Q3 and Q4 settled the label's spelling, who
writes to the tracker, and whether the milestone descriptions are in scope.
All four are recorded in `questions.md` with their grounds.

## Summary

One paragraph of `docs/issues-and-milestones.md` is rewritten so a release's
size is decided by a criterion instead of a count, a second paragraph in the
same document gains the label that writes that criterion down per ticket, and a
case holds both against the wording they replace. No script, no workflow, no
tracker write.

The work is small and its shape is decided by one thing: **the ticket asks the
rule to cite two releases by number, and the repository's own checker refuses
both.** That is `questions.md` Q1, it is the owner's, and one of its answers
turns a prose ticket into a gate change. Phase 1 does not write a sentence
until it is answered.

## Technical context

**What is being edited, and its exact coordinates.**
`docs/issues-and-milestones.md:24-30` holds the sizing rule inside
§*A milestone answers* when*, and takes three shapes*. Lines 49–55 hold
§*A label answers what it is about, and survives the move*, which is where the
label is reconciled. The two are 25 lines apart in one file, so this work item
is a single edit region; #359, which shipped from the same milestone, edited
§*One thing reads a milestone* at line 113 onward, and the ticket's claim that
the two do not collide at the squash holds — #359 is already merged at
`7e17f5e` and this branch is cut from it.

**The model sentence already exists.** `docs/review-chain-spec.md:53` reads
*Five is a ceiling, not a target.* and line 70 adds *The numbers above are a
ceiling and say nothing about when to stop under one*. The sizing rule is
brought to that wording rather than a second phrasing being invented for the
same idea, which is what `tests/test_one_word_one_meaning.py` exists to stop
one level down.

**The constraint that decides everything.** `docs/` is inside
`tests/test_release_hygiene.py`'s `LOADED`, `timers_in` refuses every
version-shaped token at or above the running `0.11.0`, and the two releases the
rule wants to cite are 0.11.0 and 0.11.1. Read from the constants; phase 1
measures it before a word of prose is written, because the whole citation
decision rests on it.

**The off-by-one behind it, stated so it is not rediscovered.** `plugin.json`
is bumped at the release-preparation commit, so between that commit and the
next bump the running version is the one that already shipped. `v0.11.0` is
tagged, on `main`, and recorded in `CHANGELOG.md`, and a loaded document still
may not name it. `timers_in`'s own docstring argues the ceiling from *below
`running` is history and is kept*, and for one release's length the version
immediately below is history the check refuses. Whether this work item repairs
that is Q1; whether it is filed regardless is Q1's secondary half.

**What existing work this touches.** One ledger row —
`seal/ledger/1789100139-…md` S3 — cites the unit being edited. `spec.md`
§*The ledger row this edit moves* holds the reading: the heading survives so
the row drifts rather than breaking, and `.github/workflows/test.yml:70-93`
warns on drift and fails only at exit 2. Hygiene, not a blocker.

**Failure scenario of the chosen approach, in six months.** The criterion is a
judgment, where the count was a measurement, and a judgment can be argued
either way by two people. That is the trade `skills/implement/SKILL.md` §3
already makes for the SDD ladder itself and the same defence applies: a
judgment about the right thing beats a measurement of the wrong one. What is
genuinely lost is the one thing a count gave for free — a reader could tell at
a glance that a nine-item milestone was wrong. Under the criterion they cannot,
which is why the count survives as a named ceiling rather than being deleted.
The second risk is the label: it is spent the moment the release ships, so
nothing stops it accumulating on tickets it is no longer true of, and there is
no checker for it. The document says nothing reads the label, so a stale one
costs a reader a wrong answer and costs no automation anything — which is the
same cost the same document says a wrong milestone used to have, before #359
made it a blocked release.

## Alternatives considered

### How the two releases are cited — this is Q1's menu

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Name the releases in prose, with no version-shaped token** — *the release that shipped the framer*, *the release that replaced the deleted checklist with a gate* | A reader cannot get from the sentence to a version without grepping `CHANGELOG.md`, which is one command but is indirection. And the reason for the indirection expires: once 0.11.2 ships both numbers become history and are allowed, so a later author replaces the descriptions with numbers and is right to — unless the paragraph says why they are written this way, which the document already models for the illustrative `1.2.3` | **the default the frame proposes.** It ships no gate change, the prompt budget is zero, and it satisfies the `## Done when` row with a citation a reader can resolve |
| **Correct the checker: a version the repository has shipped is history, whatever the running version is** | Two sub-shapes and one of them has a hole. Derived from `CHANGELOG.md` headings, it breaks the check: the release-preparation commit adds `## X.Y.Z` and bumps `plugin.json` in one commit, so the version being cut reads as shipped exactly when the check is meant to refuse it. Derived from git **tags** it is sound — a tag exists only after `main` moves, and `docs/issues-and-milestones.md` §*Reconstructing a missing milestone* already ratifies *the signal is the tag, not the branch* — but a checkout without tags then answers "nothing shipped" and the check goes maximally strict, which fails closed and is the safe direction. Either way it only unblocks 0.11.0; 0.11.1 has not shipped and stays refused, correctly | **the owner's call, and the frame does not take it.** It is a change to a gate, so `CONTRIBUTING.md`'s four items land on a prose ticket, and the honest version is a second work item. Recommended as its own issue whichever way Q1 goes |
| **Put the measurement in a dated `docs/experiments/` record and cite the path** | `docs/experiments/README.md` defines those files as an experiment that settled a question reading could not, and this is not one. Worse, the prefix exemption was deliberately narrowed in #179's round 1 so a document could not join the exemption *by choosing where it sits* — and this is that move, one directory over | **rejected** |
| **Cite the two milestone descriptions on the tracker as the evidence** | The tracker is outside `LOADED` and unconstrained, so it works mechanically. But a milestone description is editable by anybody, is not versioned, and one of the two is already false — `release: 0.11.1`'s reads *Eight issues, about five work items* while the milestone holds three. Evidence that can be silently rewritten is not evidence | **rejected** |
| **State the criterion now and defer the citation until 0.11.2 ships** | Fails the `## Done when` row outright: without the evidence the rule reads as a proposal, which is the thing the ticket says it must not read as. And the deferral names no answerer, which is how *someone will look at it* becomes nobody did | **rejected** |

### The rest of the shape

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Delete the count and state only the criterion** | The count is the one thing that let a reader see at a glance that a milestone had grown wrong. Deleting it leaves the criterion with no bound at all, and the ticket asks for the ceiling to be *named as a ceiling* rather than removed | **rejected**; the count survives, demoted |
| **A priority scale or tier list instead of one label** | A taxonomy with four levels is one nobody maintains, and the tracker already carries the receipt: `docs/issues-and-milestones.md` spends the milestone field on *when* precisely so a label does not have to. Two states is the whole proposal | **rejected** (the ticket's own reasoning, recorded here so it is not re-argued) |
| **A second milestone shape for urgent work** | `docs/issues-and-milestones.md` defines three milestone prefixes and #359 just made a milestone machine-read. A fourth shape would mean the completeness gate has a new case to judge, which is a gate change for a scheduling signal | **rejected** |
| **Automate something that reads the label** — a workflow that composes the next milestone from it | It becomes a gate, owing `CONTRIBUTING.md`'s four items and a prompt budget, and it would decide scheduling, which is the act the owner stopped a session for proposing. The document states that nothing reads it, and that statement is part of the deliverable | **rejected**, and stated in the document as out |
| **Rewrite into a new section of its own rather than in place** | The rule is a fact about what a `release:` milestone may hold, and #351 put it in that paragraph deliberately. A new section also removes the unit S3's ledger row is anchored to, turning a DRIFTED row into a REMOVED one for no gain | **rejected**; edited in place |
| **This work item creates and applies the label** | Applying a criterion to thirty-five open issues is a tracker write and it is the class the owner stopped twice on 2026-09-11. #361 exists because of it | **rejected**; `questions.md` Q3 puts the act in front of the owner |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The measurements that decide the prose, before any prose exists.** A single `test_tmp_*` probe calling `timers_in` with both candidate tokens against the running version, deleted before handover (`agent-contract` §7); the sweep command run and its output recorded; `bin/evidence-check .` run to capture S3's state before the edit. Records which route Q1 took, and states in `phases/phase-1.md` whether S11 applies | Q5, Q6, Q7 answered with exit codes read directly, never through a pipe (§1). No file under `docs/` is edited in this phase | `6de3f54` |
| 2 | **The sizing paragraph**, rewritten in place at `docs/issues-and-milestones.md:24-30`: the criterion, the ceiling in `review-chain-spec.md:53`'s wording, the evidence in Q1's form, and the what-does-not-change clauses. `0.8.3` kept as history | S1, S2, S5, S8, S9 — the release-hygiene case and the wrap case run on this phase's own edit, before the next phase adds to the same file | |
| 3 | **The label's definition and its reconciliation** with §*A label answers what it is about*, naming `flow-measurement` as the standing precedent for a label that is not a topic. Name per Q2. The criterion is applied to **#362** here and the answer recorded | S4, S6; `tests/test_one_word_one_meaning.py` still green — the reconciliation edits a section that case reads | |
| 4 | **The case that holds the sweep**, and the ledger. The case asserts the new wording present and *three or four is the size* absent, **seen red against `HEAD` before phase 2's edit is applied** — shown by reverting the sentence, not by reasoning (§15). Then S3's row handled per Q8, and this item's rows written into `seal/ledger/<id>.md` in one pass | S3, S7, S10. `bin/evidence-check .` re-run, exit code compared with phase 1's | |
| 5 | `seal/specs/<id>/changelog.md` and the closing memo. `## Not verified` is a `\| Item \| Who must answer \|` table or the line `none — <why>`; prose inside it exits 1, and a previous session hit that three times in a row | The fragment conventions in `CLAUDE.md`; `unverified_check` on the memo | |

**Phase 1 is not optional and not foldable into phase 2.** Its whole job is to
stop a sentence being written against an unmeasured constraint, and the
constraint is the one this work item is mostly about. A phase that wrote the
paragraph first would discover the refusal at the broad gate, after the prose
had been argued.

**Phases 2 and 3 edit the same file and are still separate**, because they
answer different `## Done when` bullets and phase 3 depends on Q2 while phase 2
does not. If Q2 comes back against the name, phase 2 still ships.

What each phase discovers and the next needs goes to
`seal/specs/<id>/phases/phase-N.md`, from `templates/sdd-phase.md`.

## What a change to a gate must carry

**Conditional, and the condition is Q1.** Under the frame's default — prose
citation — this work item changes no gate and owes none of the four. Under the
checker route it owes all four, and they are answerable now rather than
discovered later:

- **A test seen red** — a case asserting a shipped version is allowed in a
  loaded file, seen failing against the unmodified checker.
- **A failure direction** — the change **allows more**, which is the dangerous
  direction here. The mitigation is that the boundary moves from *running* to
  *tagged*, and a tag exists only after `main` moves, so the interval the check
  was built for is untouched.
- **A prompt budget** — zero under either route. Nothing asks anybody
  anything; the criterion is a judgment a person already makes once per
  release, and the label is where that judgment stops being remade.
- **Platform honesty** — no process inspection and no path spelling under the
  default. Under the checker route, reading tags means a `subprocess` git call
  in a test module that already makes one (`tracked()` calls `git ls-files`),
  and a checkout without tags must be measured rather than assumed.

## Operational impact

- **No `plugin.json` bump.** `hygiene.yml`'s version step greps
  `^(skills|agents|hooks|templates|bin|\.claude-plugin)/`; this work touches
  `docs/`, `tests/` and `seal/` only. Nothing that ships changes.
- **A ledger row drifts** — S3 in another work item's fragment. Exit 1 from
  `evidence_check.py` is a CI warning by `test.yml`'s own thresholds, not a
  failure. Q8 decides whether it is re-verified or replaced.
- **One tracker act is left with the owner and nothing proceeds without it.**
  The label does not exist until somebody creates it, and the document will
  describe a label that is not yet there. Q3 is where that ordering is
  settled; the document being merged before the label exists is a real state
  and has to be an accepted one or a blocked one, not an unnoticed one.
- **This work item merging is what lets 0.11.1 ship.** #361 sits in
  `release: 0.11.1`, and the completeness gate #359 shipped refuses the release
  pull request while the milestone claims an open issue the release branch does
  not carry.
</content>
