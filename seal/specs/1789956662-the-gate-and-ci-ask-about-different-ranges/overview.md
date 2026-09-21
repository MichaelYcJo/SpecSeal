# 1789956662-the-gate-and-ci-ask-about-different-ranges — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `seal/specs/1789956662-.../routing.md`, `spec.md`, `plan.md`,
            `questions.md`; `CLAUDE.md` §*The goal a design is chosen
            against*, §*a change writes fragments*, §*no real identifiers*;
            `CONTRIBUTING.md` §*What a change to a gate must carry*;
            `skills/verify/SKILL.md` §*The broad gate — after the rounds*;
            `agents/sealer.md` §*The command*; `agent-contract` §§1, 2, 8, 9,
            12, 14, 15; issue #423 and its comment
· evidence: `seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md`
· verified: executed — the two gate modules and the resolver's cases, with
            every new case seen red first and every unit mutated; read —
            nothing claimed as passing that was not run. The full suite, the
            repository lint and the typecheck are `unverified` here and are
            the sealer's one run

## Why this work exists

The broad gate resolved `--base` to the LOCAL ref where CI resolves it to the
remote-tracking one, so a branch whose checkout had fallen behind sealed green
over a question nobody asked and CI then refused the same commit; the gate now
asks what CI will ask and says when resolving moved the answer.

## Prompt budget: zero

No question is added to any session. Where resolving moves the answer the gate
prints one line and runs anyway; where it does not, nothing extra is printed.
`CONTRIBUTING.md` §*What a change to a gate must carry* says this is the one
clause of the four a passing suite cannot report, so it is stated here and in
the pull request body.

**Failure direction: each arm moves toward CI's answer, and that is not one
direction.** This sentence said *the gate blocks more, never less* until round
1 measured the other half. Wording the base itself removed leaves the range,
so the survivor arm can pass where it used to refuse; the branch's replacement
of base wording enters it, so the arm can refuse where it used to pass. The
two baselines should move the same way — a baseline carried forward drops the
rows the base's own newer commits added — and that half is **read, not
executed**. The survivor arm is the half that was measured, in both
directions, and the repository owner answers whether the baseline half is
worth a case of its own. `spec.md` §*What is wrong* already made this claim
and the three operational sentences contradicted it: what a stale base
guarantees is a disagreement rather than a direction.

<!-- CORRECTED 2026-09-21 by work item 1789996775 (#464). What stood here:
"The two baselines move the same way — a baseline carried forward drops the
rows the base's own newer commits added." It is not false, and that is the
point: round 1's report labelled that half read rather than executed, and it
stood here beside the measured half with no label and no answerer, which
`skills/agent-contract/SKILL.md` §4 is the rule against. Round 2's finding 14
(`rounds/round-2-report.md`:195) names the three sites and its
§*Paste-ready fixes* carries this replacement; `seal/ledger.md`'s R3 row of
this work item is where the distinction survived. Corrected in place with the
issue named, never deleted silently: a record of a past state that quietly
becomes true is a record nobody can audit. -->

The clause survives three times, so the label does too — `changelog.md` and
`plan.md` §*Operational impact* carry the same correction under the same
marker.

**So the argument is not that the gate is stricter.** It is that the resolved
answer is the one the merge is judged by. The cheaper mistake is still this
one — a gate that answers a question the merge is not judged by is worse than
a gate that errs either way, because its stamp reads as a pass.

**Platform honesty.** `git rev-parse <ref>@{upstream}` and
`refs/remotes/origin/<ref>` are git behaviour rather than OS behaviour, and
nothing added here inspects processes or paths in a way that differs by
platform. The new fixtures run `git clone` and `git worktree`, which the suite
already does on every matrix leg. Not run on Windows or Linux from this
machine — CI is the answerer.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many times `args.base` is read | `spec.md` §*The class, enumerated by construction* enumerates six consumers; the code read it **seven** times | the count case asserts **one** read after the change | The seventh read is the refusal sentence for a base that does not resolve, which quotes the spelling rather than consuming it. The table is right about consumers and is not a count of reads |
| The `Broad gate` cell's base half | `spec.md` §*Out, and why each*: *The cell already names commits, which is the property #423's comment asks for* | the cell's base half moves from the ref as typed to the commit — `2cc9f1a against base` becomes `2cc9f1a against b9cdec0` | True of the tree half, false of the base half, which is the half the ticket's comment is about. `spec.md` §Scope 3 requires all six consumers to take the resolved commit and names this cell among them, so the §Out sentence is grounds that do not hold rather than a scope boundary. Both parsers read the FIRST SHA-shaped word, which is the tree, so neither sees the change (measured) |
| A3, *nothing else moved* | `spec.md` A3: `tests/test_the_seal_is_taken_once_by_the_sealer.py` stays green with nothing edited in it | one assertion in `test_the_gate_with_record_seals_the_item_and_counts_its_rounds` now reads the commit instead of the ref | The fixture whose reading moved, named as A3's own paragraph asks. 119 of the module's 121 cases never went red; the second failure was mine, `panel` still being handed the `Base` object, and was a defect rather than a reading. The resolution itself moved nothing — that fixture has no remote, so it resolves to the ref as given |
| W1, a panel value cut at 23 columns | `questions.md` W1's default: the panel carries the short form and the printed line is authoritative | the panel gains a `from` row, and a ref too long for it is elided in the row itself with the tail kept — `...se/2026-09-21-hotfix` | The printed line is authoritative only where resolving MOVED the answer, because A4 requires silence otherwise, so on an agreeing run there is no second statement to correct a cut. Round 1's finding 5 measured what that costs: `seal_stamp.letter` cuts at the frame with no marker, so a 32-column ref rendered as `origin/release/2026-09-` and read as a whole ref. `broad_gate.PANEL_VALUE_WIDTH` states where the frame cuts and a case measures `letter` to hold it there |
| The moved-line has two fillings, not one | `spec.md` §Scope 4: *the given ref and the resolved ref are different commits*, so the line names both SHAs | the line also covers a given spelling that names **no** commit in this checkout | A clone that never made a local branch for its base is an ordinary checkout and today exits 2 there. Silence would be the defect this work item is about, so `moved` is `commit != given_commit` and `None` differs from a hash. The second filling says the given spelling names no commit here instead of printing a SHA that does not exist |

## What the review chain kept finding, and it was not one cause

One sentence — *nothing about that run changes* — was corrected in three
places by round 1 and survived in two more, and round 3 then found three
further statements of the same claim, in different words, standing in the
test module since phase 1 (#465). One claim about the workflow
reader was corrected in two places and survived in a third. Both times the
pass reached for the class rather than the coordinate, so `agent-contract`
§12 is not what it ran into. It enumerated the class over a population that
could not hold every member, and the population was wrong in a different way
each time.

| Survivor | Why the sweep could not reach it |
|---|---|
| the A8 case's docstring | The finding-3 pass grepped `nothing about that run` over **three named files** — the two it was editing and the spec. The test module carried the phrase verbatim, so the pattern would have matched it; the file list is what excluded it |
| pull request #459's body | Outside the tree, so no grep over the repository reaches it at all, and it said *its* run where every corrected copy says *that* run — a tree-wide search for the corrected phrasing would have missed it too. Corrected from the orchestrator's side after round 2 |
| `phases/phase-4.md`'s claim | Inside the tree and inside this work item, found only because `survivor-check` ran over the fix pass's own range afterwards |

Round 3's correction to the count is part of the lesson rather than a
footnote to it: *four places* was carried forward from round 2's report
without being checked, in the same paragraph that was correcting the cause
beside it. At `327ef1f` the sentence stood in `changelog.md`, `spec.md`
§Scope 2, `broad_gate.py` and the test module; `overview.md` never carried
it.

**The lesson is about the population, not about grepping harder.** A sweep
over the files a pass happens to be editing can only ever confirm what that
pass already knows. The three readings that did find these were a sweep over
the whole tree, a check run over the pass's own commit range, and a reviewer
opening the case a sentence is about — and only the second is something a
pass can run on itself, which is why `agents/smith.md` puts `survivor-check`
at the end of a fix pass rather than trusting the pass's own enumeration.

## The branch shipped its own defect in a docstring

`names_a_branch`'s docstring illustrated an accepted branch name with
`release/v0.12.2`. It was true the day it was written and stopped being true
when that release branch was cut, and the broad gate is what found it —
`tests/test_release_hygiene.py` went red on the version the line names, and
all three `pytest` legs of the pull request agreed.

**That is this work item's own subject, one level down.** #423 is a question
asked by a NAME — `--base release/v0.12.0` — answered later against something
that name no longer pointed at. A docstring naming a concrete release branch
is the same shape in prose: the example is pinned to a moment, the moment
passes, and nothing says so until a checker asks. The repair is the one the
repository already prescribes for the other instances of it, `release/vX.Y.Z`,
which satisfies the version rule **by construction** rather than by sitting on
an allowlist and cannot rot when the branch it named is deleted.

**Two rules point at that line and only one of them was red.**
`tests/test_release_hygiene.py` catches a version at or above the running one,
so it fires on the day that version ships and not before. `CLAUDE.md`'s rule
against naming a concrete release branch is the one with the general reason,
and it is pinned only on contributor-facing surfaces —
`tests/test_the_contributor_has_a_procedure.py` reads the two READMEs, the
contribution guide and the pull request template. A script the gate loads is
not one of those, so the sentence rotted in a file no rule was watching for
that reason. Named here rather than widened: widening the pin is mechanism,
and this run is capped.

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the `sealer`, in its one broad run after the review rounds settle (`agent-contract` §2) |
| M1 — whether a green gate can still meet a red CI because the base moved after the branch last took it in | a measurement, deferred by `questions.md` M1's own default: the limit is real, stays named in `spec.md` §*What this repair cannot see*, and this work does not try to close it |
| the new fixtures on Windows and Linux | CI's matrix, at this branch's pull request |

## Not done

**The refusal direction is not built.** `questions.md` P1's default (a) is
what this branch implements: the gate resolves, prints where resolving moved
the answer, and never refuses over a stale base. Moving to (b) later is
additive — the resolution stays and a refusal is a branch above it — so
nothing built here is wasted if the owner overturns it.

**No shared base resolver.** `bin/survivor-check`, `bin/unverified-check` and
`chain_check.py` typed by hand still take the ref a person writes.
`spec.md` §*Out* has the grounds: #423's comment measured that the gate's base
is the one place a resolution difference seals something.

**`unverified_check.py#base_label` reads slightly worse for a commit.**
`questions.md` W2 asked whether each interface should get the ref where it
prints its baseline back. All six take the commit, per W2's default, so a
report can now read *the merge-base of 58014fe4 and HEAD* where it used to
read *the merge-base of release/v0.12.0 and HEAD*. The ticket's comment asks
that evidence name a commit rather than a ref, and a commit a reader can open
beats a ref that re-resolves under them.

## Fed back into the spec

This section read `none` until round 1's finding 8, on the reasoning that a
correction to a spec's grounds is not a clause the work added. That left two
sentences standing in `spec.md` which the tree disproves, and the spec is
where a later round looks first — a ratified-looking sentence nobody marked.
Both are now corrected in place, marked with the round and finding that
measured them, and both are *inferred during implementation*: a planner may
overturn either.

- **§Scope 2** said a base with no remote-tracking counterpart *resolves to
  itself and nothing about that run changes*. The resolution does land on the
  ref as given; what the consumers are handed still moves from the ref to its
  commit. A3 and the divergence table above said so from the first build.
- **§Out, and why each** said of the `Broad gate` cell that *the cell already
  names commits*. True of the tree half, false of the base half — which is
  the half #423's comment is about. §Scope 3 names that cell among the six
  that must take the resolved commit, so the spec disagreed with itself and
  the build took the repairing side. What stays out of scope is widening the
  cell to carry the ref as well, and that is what the row now says.

**The corrections are marked rather than silent**, because a spec that
quietly becomes true is a spec nobody can audit — the same reason
`phases/phase-4.md`'s over-strong sentence is corrected in place rather than
deleted.
