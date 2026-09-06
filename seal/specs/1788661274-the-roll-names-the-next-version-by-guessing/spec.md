# Feature Specification: the roll fires when it is due, and names what it knows

<!-- seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/spec.md -->

Closes #155.

## What happened, measured

**[read, #155's own comment of 2026-09-05]** at the 0.8.1 release the script
computed `next_version("0.8.1") -> "0.9.0"`, so the roll **closed #166** —
already titled *chore: flow measurement — 0.9.0*, opened at the 0.8.0
release — and opened **#172 with the identical title**. Two issues, same
name, one closed. It cost two things rather than the one the issue predicted:

1. The measurements posted during 0.8.1 went to #166, which was open when they
   were written and closed by the tag twenty minutes later. They were carried
   to #172 by hand.
2. **The roll fired at a patch release at all.** #166 was opened for 0.9.0 and
   0.8.1 is not 0.9.0, so nothing was due to roll — the log the release closed
   was the log the next release still needs.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/branch-and-release.md` — *whether the number is a minor or a patch is known at the end, not at the cut* | the script guesses at the one moment the repository's own rule says the answer is available |
| `CLAUDE.md` §*The goal a design is chosen against* | the documented fallback is *a human retitles it by hand*, which is a person remembering at a moment nobody is watching, on an artifact created by automation |
| #155 §*Not this* | retitling by hand is refused as the answer |
| `skills/agent-contract/SKILL.md` §14 | the roll's own printed lines are what a release reader sees, so they ship with cases |

## Scope

**In — the owner's two halves, from #155's comment.**

1. **A roll happens when the version the open issue names has shipped, not on
   every push to `main`.** If the open issue names `0.9.0` and the tree says
   `0.8.1`, there is nothing to roll: **exit 0, say so, leave it.** That is the
   condition the script never had, and it is why a patch release closed a log
   that had not been used yet.
2. Verbatim: *"The title comes from the version rather than from a guess: read
   `.claude-plugin/plugin.json` in the checked-out tree, **and name the NEXT
   version by the same arithmetic the release actually used**."*

   **The build went against the bolded clause, deliberately.** The tree is
   read for the just-shipped version, which `read_version` already does; the
   next version is not named at all, because the title states the version the
   log rolled FROM. The grounds are #155's own body, which delegates the
   choice — *"What could tell it instead of guessing. **Named, not chosen —
   the trade is what the work item settles**"* — and lists this shape as one
   of the four candidates: *"Do not name a version at all. Title the log by
   the version it rolls from — `chore: flow measurement — after 0.8.0` —
   which is a fact rather than a prediction."* The comment's arithmetic
   clause and the body's delegation are the same person a day apart, and the
   body is the one that hands the fork over.

   <!-- This bullet quoted the comment with the arithmetic clause removed,
        which made half 2 read as a half the build satisfied rather than one
        it settled against. Corrected in round 1's fix pass (finding 9). -->

   The scenario table below carries the second half of the same divergence,
   and `overview.md` §Divergence is where both are judged.

**The fork this work item settles**, which #155 names but does not choose.
Half 1 needs the version the open issue names, and the script's own docstring
says the mechanism *finds its issue by label and open state, never by parsing
the title*. So either the title becomes readable, or the version is carried
somewhere else. And once the roll is due, the next log still needs a name, and
the next version after a shipped one is exactly the thing nobody knows.

| Shape | What it costs |
|---|---|
| Parse the version out of the open issue's title | the script writes that title, so the format is its own — but it makes the title load-bearing where the docstring promises it is not, and every existing log has to match |
| Title by the version it rolls **from** — *flow measurement — after 0.8.2* | never predicts anything; a fact rather than a guess. Costs a rename of the convention and every existing log reads the other way |
| Keep predicting, but only when the prediction has been confirmed by a shipped version | the roll stops firing early, and a wrong name still gets written once at each release |

**Settle it in `plan.md` §Alternatives with the failure scenario of each**, and
whichever wins, #155's third *Done when* holds: **if a prediction cannot be
made, the title says so instead of predicting.**

**Out.**

- **Retitling by hand.** #155 §*Not this*.
- **Changing the one-open invariant or its single retry.** Both are correct and
  one of them caught a real fault on the run that measured this — a work item
  labelled `flow-measurement` by hand made the job fail `found 2`, loudly and
  rightly.
- **Moving what the durable `flow-baseline` log does.** Untouched.
- **Backfilling the existing logs' titles.** If the convention changes, say in
  the change what the old titles mean; do not rewrite closed issues.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A patch release rolls nothing | Given the open log names a version the tree has not shipped · when the roll runs · then it exits **0**, says nothing was due, and closes no issue | a case over `main` with a faked `gh` |
| A due release rolls | Given the open log names the version the tree just shipped · when the roll runs · then it closes that issue and opens the next | a case, same shape |
| The name is never a bare guess | Given any roll · when the new title is written · then it is derived from a version the tree states, or it says it is not a prediction | a case pinning the title's form |
| The exit says which happened | Given either outcome · when the job finishes · then a reader of the release log can tell *rolled* from *nothing due* without opening GitHub | a case over the printed lines |
| The invariant still fails loudly | Given zero or two open logs · when the roll runs · then it exits non-zero naming the count, with the single retry on zero unchanged | the existing cases stay green |

## Data & interfaces

No API. One script, `.github/scripts/roll_flow_measurement_issue.py`, and
whatever `skills/verify/SKILL.md` or `docs/issues-and-milestones.md` says about
the log's title if the convention moves.

## Open questions → questions.md
