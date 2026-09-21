# 1789985781-the-gates-arm-list-is-maintained-by-hand — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `CLAUDE.md` (the goal a design is chosen against, the merge-method
            table, the fragment rule, the anchor rules), `CONTRIBUTING.md`
            §*What a change to a gate must carry* and §*House rules*,
            `skills/verify/SKILL.md` §*The broad gate*, `skills/agent-contract/SKILL.md`
            §§1, 2, 9, 12, 14, 15, this item's `routing.md`, `spec.md` A1–A7,
            `plan.md`, `questions.md` Q1/M1/W1, `seal/follow-up.md`,
            `seal/config.md`, and GitHub issue #468
· evidence: `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md`,
            rows G1–G8. Three rows of the shared ledger re-read and re-stamped
            (S7, S12, the `not_as_written` row) and two of this release's
            fragment rows (R2, R5), each with its `Re-read` marker
· verified: executed — the new module (24 cases: 20 at the build, 3 in round
            1's fix pass, 1 in round 2's), the four modules that read
            `broad_gate.py`, the document rules, `evidence-check .`,
            `survivor-check` over each range, and 25 mutations each applied
            alone and restored from bytes kept outside git — 19 at the build,
            4 in round 1's fix pass and 2 in round 2's. One more missed its
            anchor: it replaced an unrelated `except (OSError, ValueError)`
            earlier in the file and reported a surviving mutant, which is the
            *assert what the substitution matched* lesson arriving through a
            probe rather than through an edit. Round 2 swept the file for the
            same trap and found three ambiguous anchors, of which only that
            one lands silently. Not executed — the full suite, the
            repository-wide lint and the typecheck, which are the sealer's
            one run

## Why this work exists

The gate's arm list was kept in step with the workflow's by whoever
remembered, so a branch could seal green and then meet a red leg; it is now a
declared partition of every step of that workflow's `release` job, held
against the file by a case that goes red from both sides.

## What `CONTRIBUTING.md` §*What a change to a gate must carry* asks

This changes a gate, so the four clauses are answered here and the pull
request body carries them.

- **A test seen red.** Every case was red before the code it holds existed,
  and the reds are quoted in the phase records. Two are worth naming: A1 and
  A2 opened at `AttributeError: module … has no attribute 'PARTITION'` with 10
  failed, and A5 — the branch whose merge dropped a correction — came back
  **exit 0 with the stamp drawn**, which is the defect itself rather than a
  test scaffold. Nineteen mutations were applied one at a time and restored
  from bytes kept outside git; one of them survived and took a unit out of the
  tree with it (`phases/phase-1.md`).
- **A stated failure direction: the gate refuses more.** It gains two arms and
  loses none, and a step added to the workflow now fails the suite until
  somebody classifies it. A wrong refusal costs a sealer one run and a
  sentence; the wrong allow is what shipped — a green seal over a shorter list
  than the merge is judged by, which is only found at the pull request, after
  the rounds have settled and the gate has been spent.
- **A prompt budget: zero.** No question is put to anybody, in any session.
  The partition is read by a case and printed by the gate; the two questions
  this work raised went to `questions.md` Q2 and `seal/follow-up.md`, where a
  person answers them when they choose to rather than when a run stops.
- **Platform honesty.** Everything here reads text out of a file and runs
  Python scripts already on the gate's path. Run on macOS only; the fixtures
  are ordinary `git init` repositories and the matrix legs are the answerer.
  One platform-shaped detail was checked rather than assumed: `seal.py mode`
  takes no `--root` and resolves from the working directory, which `run`
  already sets to the tree being gated.

## What `questions.md` M1 measured

**Six**, not one. Thirteen steps in `hygiene.yml`'s `release` job; three were
mirrored before this work; of the ten that were not, **six have a local answer
and four have none**. Two of the six are now arms. The frame refused to state
this number and was right to: the issue's own title points at one step, and
"it is one" would have been wrong by five.

| | Steps | Which |
|---|---|---|
| mirrored before this work | 3 | unverified · chain · survivors |
| mirrored now | 5 | + corrections · mode |
| no local answer | 4 | the pull request's body · a fetch of the pull-request namespace · the tracker · a step that only warns |
| local answer, no arm | 4 | three run `.github/scripts/…`, which no plugin ships; one is inline shell with no script either side can share |

The second line of that measurement is the one the frame did not name: **six**
is the count before the line between a shipped check and this repository's own
is drawn, and **two** is what a gate that ships to every installation can
actually run. Both numbers are stated here because either alone is a count
taken on one axis.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `questions.md` W1 offers a count **or** the names | *A count fits; names do not* | both, on different streams | A6 asks that a reader can tell **which** steps the seal did not answer, and a count alone sends them back to the two files this work removes the need to open. The panel takes the count because `PANEL_VALUE_WIDTH` is 23; `coverage_line` writes the names to stderr beside the line already naming the repository's own command |
| `spec.md` §Scope 3, *the arms the partition finds missing are added, however many* | six steps have a local answer and no arm | two added, four excluded with reasons | Three of the four run `.github/scripts/…` and the fourth is inline shell. `broad_gate.py` ships to every repository that installs the plugin, so an arm reaching for a script only this repository has is an arm that fails everywhere else; `seal/config.md`'s `Broad gate` row is the declared home for a repository's own checks. `questions.md` Q2 puts the remaining choice to the owner rather than taking it here |
| `plan.md` §*Technical context* retypes the thirteen step names | its own copy says it will rot | the reader takes them from `hygiene.yml` | The plan says so itself, and #424's finding 4 is the precedent. One name in that list is already short of the file's — the plan writes *the unverified record is readable* where the workflow says *the unverified record is readable, and rows leave it closed* |
| the new arms mirror their steps' **range**, not their steps' **guard** | the workflow skips the survivor and correction steps when the base is `main`; the gate skips neither | left as it is | The survivor arm has had this difference since it was added, and making the correction arm behave differently from its neighbour would put two readings of one question inside one function. The class is *whether a mirrored arm asks its step's question*, which `spec.md` §*What this repair cannot see* puts outside this item. **#473 is its home.** #423 is not — that work item is about the base the gate resolves and it ships in this release, so a deferral pointing at it would have lived only in a closed record (round 1, finding 2) |

## The seal was taken twice, and the second run is why

`agents/sealer.md` has the sealer run `broad-gate`, which on the Bash tool's
PATH resolves to the **installed plugin cache** — at the time of this work
item, `…/plugins/cache/specseal/specseal/0.12.1/bin/broad-gate`, whose wrapper
reaches its own sibling script. So the gate that sealed this branch was the
released five-arm gate, not the seven-arm gate this branch had just written.
The sealer read the resolution off the wrapper and said so rather than reading
the stamp; #475 is the issue.

The orchestrator then ran the checkout's copy directly, at the same tree and
the same base, with no `--record` so the cell was left as the sealer wrote it.
It sealed: `suite 3953 passed, 9 skipped`, `row exit 0`, `ledger 1398 ok · 0
broken`, `chain exit 0`, and the two rows this release built, printing in a
real run for the first time rather than in a fixture:

```
from     origin/release/v0.12.2
workflow 8 of 13 not answered
```

with the eight named in full above the stamp. So both gates pass over this
tree, and the `Broad gate` cell records the run the sealer took.

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck over this branch | the sealer, in the one broad run after the rounds settle |
| the new arms on Linux and Windows | CI's matrix legs, at the pull request |
| how long the two new arms add to a seal in a large repository — `correction-check` over this repository's history is sub-second, and no other tree was measured | the repository owner, if a seal ever reads slow |
| whether `round_record.py` and `correction_check.py` deduplicate a repeated coordinate the way `evidence-check`'s drift report does | the repository owner, through the `seal/follow-up.md` row this work added |

## Not done

**The four excluded steps with a local answer were not moved into the `Broad
gate` row.** That row decides what every sealer run in this repository
executes, which is a decision about the repository's own command rather than
about the gate's arm list; `questions.md` Q2 states the options and the
default.

**The exclusion loophole was not closed**, because nothing closes it: a future
editor can answer a red A1 with a written reason instead of an arm, and the
partition is then total with the seal still short. `plan.md` §*The failure
scenario at six months* names it, the case docstring names it, and the trade —
a written wrong answer over an unwritten one — is the one #423's comment
already argued for.

**The `release` job is the only job the partition covers.** A check added to
`ledger`, to `test.yml` or to a new job is outside it and the case will not
notice. `spec.md` §*What this repair cannot see* says so; widening the subject
is how a bounded work item stops being one.

## Fed back into the spec

**A partition row's reason must name something out of the gate's reach** —
inferred during implementation. `spec.md` A4 asks only that a reason be prose
rather than a category, and prose that names nothing (*this one is not worth
the trouble right now*) passes that and answers nobody. The second case holds
the stronger reading against a vocabulary of what the kinds of unreachable
thing are called here, and a fifth kind is a word to add rather than a case to
delete. A planner may overturn it.

**A step's classification turns on whether the plugin ships the check, not on
whether the check has a local answer** — inferred during implementation.
Nothing in `spec.md` draws that line; it fell out of the classification, and
it is what makes the difference between six missing arms and two.
