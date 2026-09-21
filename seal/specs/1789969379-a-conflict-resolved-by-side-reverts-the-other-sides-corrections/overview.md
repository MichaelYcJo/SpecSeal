# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. -->

📋 implement applied
· spec:     `spec.md` A1–A9 and §*The class, enumerated by construction`;
            `plan.md` §*Technical context* and §*Alternatives considered*;
            `questions.md` Q1, Q2, M1, M2, W1; `CLAUDE.md` §*a change writes
            fragments, never the shared file*, §*A ledger coordinate names
            content, never a position*, §*A row whose anchor a change removes
            is REMOVED, not re-pointed*, §*The goal a design is chosen
            against*; `CONTRIBUTING.md` §*House rules*; `agent-contract` §2,
            §5, §7, §9, §12, §15
· evidence: `seal/ledger/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections.md`
· verified: see §*Not verified*; the per-phase record is in `phases/`

## Why this work exists

A correction lost when somebody resolves a `seal/ledger.md` conflict by taking
a side is invisible by construction — the reverted row is byte-identical to a
row nobody touched — so `correction-check` makes the loss loud at the pull
request, and the two documents that state the fragment rule's exception now
say what to do at the conflict.

## What the measurements answered

**M1 — merges of the ledger in this repository's reachable history, and how
many dropped a marker.** Measured in phase 1 over 37 merge commits reachable
from every ref, 24 of which had a parent carrying a ledger with markers:

| Rule | Merges reporting | Markers |
|---|---|---|
| `spec.md` §Scope 1 as written (either parent, row survives) | 1 | 5 |
| with the merge-base test the build added | **0** | **0** |

The one merge the spec's rule reported is `87eced1`, the v0.9.3 release merge,
and opening it showed correct work: `release/v0.9.3` re-anchored a row whose
section had moved file, rewrote its Notes cell to say *Re-anchored, not
re-verified*, and dropped four historical `Re-read` sentences with the prose
it replaced. The merge took that rewrite; one parent had already decided it.
That is what drove the first divergence row below.

**The incident the ticket is about is not in reachable history**, because the
branch that carried it squashed and no `refs/pull/*` namespace is fetched in
a clone. `spec.md` §*What this repair cannot see* predicted exactly that, and
it is why M2 is a measurement rather than an assumption.

**M2 — are the merge commits still reachable where the CI leg runs.**
Measured in phase 4, and the answer is **yes**, so nothing moved. Two cases
in `tests/test_a_merge_cannot_silently_drop_a_correction.py` build #424's own
shape — a feature branch that merges its release branch in and resolves by
taking a side — and read the check's answer at two commits:

| Where | What the check says |
|---|---|
| the merge ref a `pull_request` job checks out (`origin/<base>...HEAD`) | exit 1, the dropped `Corrected` marker named |
| after the branch squashes into its release branch | exit 0, `no merge commit in this range` |

The merge ref is the part that could have made the answer no. A
`pull_request` job sits on the head already merged into the base, not on the
head commit, so the fixture builds that merge rather than checking out the
branch.

## What a change to a gate must carry

`CONTRIBUTING.md` §*What a change to a gate must carry* applies — this adds a
CI leg — and the four answers are here so the pull request body can carry
them.

**A test seen red.** Every case in the new module was seen red before it was
committed, and the handback lists each with what red said. Three rounds of
mutation went further: eight mutations over phase 1's units, eight over phase
2's, four over phase 3's, and one per document for A8. Two of those found
cases that were green while the thing they were about was broken — A3 against
a permissive `standing`, and `_index`'s ambiguity guard with nothing behind
it — and both were closed before the phase was committed rather than noted.

**A stated failure direction: the check blocks more.** A lost correction is
silent today, so anything at all is stricter than nothing, and the risk is a
false refusal. That is what the row-survival test exists to bound, and A3 is
the acceptance row that pins it. The merge-base test narrows it further — it
was added because a measurement showed the spec's rule refusing correct work
over this repository's own history. Neither direction reaches an outage: the
leg refuses one pull request and names the marker, and a repository with no
merges in the range gets one line and exit 0.

**A prompt budget: zero.** No question is put in front of a person, per
session or otherwise. The check prints and the CI leg goes red; the reading
it asks for is the reading somebody was already doing at the conflict. It
adds no hook, so no gate prompt exists to count.

**Platform honesty.** `git rev-list`, `git merge-base`, `git cat-file` and
`git ls-tree` are git behaviour rather than OS behaviour, and the fixtures
use `subprocess` with no shell. Not run on Linux or Windows from this
machine — CI's matrix is the answerer, and `§Not verified` carries the row.

**The frame's measurement had one side of the date on it, and round 1
found the other.** `spec.md` §*What the markers actually look like* counted
the spellings AFTER the date, found three, and stated it with a count — which
made *the variation lives there* read as measured when only one side had been
looked at. It varies before the date too: 39 of `seal/ledger.md`'s 404
markers put a qualifier in between, in ten spellings, and one row carries no
other. The check was silent on a qualified correction reverted at a merge —
#424's own incident — and red on a resolution rewording `Re-read <date>` into
`Re-read again <date>`, which is A7 broken. **The same false fact was
standing in nine places**, not the six the round enumerated: the three it
missed are this work item's `changelog.md`, its `plan.md`, and two docstrings
in the test module. All nine are corrected, `spec.md`, `plan.md` and
`questions.md` in place with the round and finding named.

**Round 2 found the same error one layer down, and the shape is worth more
than the digit.** The census that set round 1's bound at four words was taken
**with the widened pattern itself**, so a spelling the pattern could not see
was invisible to the measurement justifying it — the frame counted one side
of the date, and the fix counted with the instrument it was calibrating. The
tenth spelling is five words long and sits at line 1172 of `seal/ledger.md`.
Re-measured with an instrument that is not the pattern and has no bound: 404
occurrences on 190 rows, 39 qualified, ten spellings, and run lengths of 0, 1,
2, 3 and 5 — **no run of four**, so the bound that shipped matched exactly
what a bound of three would have. Fourteen statements were false by then, not
the three the round named; all fourteen are corrected, `spec.md` and ledger
row C1 in place.

**What that does not close.** Both fixes pin one literal spelling each, so an
eleventh spelling of six words would be invisible again and the case would
stay green — the same way twice already. What would close it is a case that
takes the independent census over the real ledger files and asserts the bound
covers every candidate site. That is a corpus walk, which a fix pass may not
add (`skills/code-review/orchestration.md`), so it is named here rather than
built. **Answerer: the repository owner, as an issue.**

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What makes a dropped marker a LOSS | `spec.md` §Scope 1: "a marker present in **either parent's** ledger text and absent from the merge result, **while the row carrying it survives**". The code also reads the merge base and stays silent where a parent deleted the marker relative to it | the merge-base test | M1 measured the spec's rule over this repository's whole reachable history and it reported one merge, five markers, and no defect — a deliberate re-anchoring rewrite that the merge merely carried. `spec.md` §Scope 2 says the check exists to separate a loss from a removal and that "a check that fires on a legitimate removal is a check people learn to skip"; a parent's deliberate deletion is a removal by that argument. The refinement only narrows, and A1/A2/A3/A6 are untouched because no fixture's base carries a marker |
| The marker counts in the frame | `spec.md` §*What the markers actually look like*: `Corrected` 10, `Re-read` 185 in `seal/ledger.md` | both, stated as what they are | Those are **row** counts (`grep -c`, one line per row); the occurrence counts are 12 and 353 for a `<verb> <date>` pattern and **404 over 190 rows** for the file as it is actually spelled — a row can carry a marker in more than one cell, and a marker can carry a qualifier between the verb and the date (round 1, finding 1). Nothing in the frame's conclusions turns on it — `Re-read` dominates either way — but the check counts markers per row, so the distinction had to be written down where a later reader meets it |
| A blob the check cannot read | `plan.md` is silent; the code passed it in silence | named under `not judged`, and the run continues | Found by mutation rather than by reading. `read_blobs` returned an unreadable blob as absent and said why in its docstring, and nothing downstream acted on the difference — so a ledger over the size cap read as a ledger with no rows and the run printed *no correction marker was dropped*. `skills/verify/SKILL.md` §*The Seal Test*: a check that answers where it cannot see is a counterfeit. It prints rather than refusing, following `survivor_check.py`'s `unresolved` rows, because refusing a whole run over one unreadable blob turns a check about corrections into a check about file sizes |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the sealer — `agent-contract` §2 leaves the broad gate to the agent whose definition assigns it, and this one is not it |
| that the CI leg behaves on a real pull request — the workflow step is read and its command is exercised locally against constructed merges, never on a runner | CI, at this branch's pull request |
| that the fixtures and the check behave on Linux and Windows | CI's matrix — `git show`, `git rev-list` and `git cat-file` are git behaviour rather than OS behaviour, and that is the reasoning rather than a run |

## Not done

**Q1 is left where it was.** The rider at `evidence_check.py#reverify` still
owns the question of whether `--reverify` should refuse a row whose `Checked`
predates the hash it is replacing. `evidence_check.py` is unchanged by this
work, as `spec.md` §*Data & interfaces* requires.

**Nothing is backfilled.** The three rows the #424 incident reverted were
repaired when it was found; this work is about the next one.

**The broad gate does not run `correction-check`, and that is the one thing
here worth a ticket.** `skills/verify/scripts/broad_gate.py` mirrors five of
the hygiene workflow's arms — the suite, `evidence-check --strict`,
`unverified-check`, `chain_check.py` and `survivor-check` — so the sealer's
one broad run says what CI will say. This branch adds a sixth arm and the
gate does not mirror it, which means a branch can seal green and then meet a
red leg at the pull request. That is the #423 class one work item later: the
gate and CI asking one branch different questions.

It is deliberately not fixed here. `spec.md` §*Data & interfaces* names every
coordinate this work touches and `broad_gate.py` is not among them, so adding
an arm to the gate is a second subject with its own failure modes — the gate
would need the base it resolves, and #423 is the work item that exists
because that resolution was wrong. Nothing in the suite goes red for the gap:
no case holds the gate's check list against the workflow's arms, which is
itself part of what the ticket would be about. **Answerer: the repository
owner, as an issue opened from this pull request.**

**`templates/hygiene.yml` does not gain the leg.** That template carries five
steps against this workflow's fourteen and has no survivor step either, so it
ships the subset a new repository needs rather than a mirror. Adding one arm
of the difference and not the rest would make the subset look deliberate in a
way it is not.

**The check does not read a `Checked` date going backwards**, which is the
ticket's second direction. `spec.md` says why in a section of its own: no
machine reads that column, so it is new mechanism on a surface a standing
rider already owns.

## Fed back into the spec

**The merge-base test** — inferred during implementation, from M1's
measurement. `spec.md` §Scope 1 states the rule without it, and the
divergence row above is the record. A planner may overturn it, but only
against the measurement: without it the check reports `87eced1`, and
`87eced1` is correct work.
