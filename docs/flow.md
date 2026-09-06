# Release flow

A checklist for the tickets in flight.

**A branch writes this file for the rows its own work created or closed**, in
the pull request that earns them — its own box ticked, and a row for any
ticket that work opened. So the change lands in the same merge that makes it
true, and a file every ticket touches stops collecting a pull request of its
own each time. What still gets its own branch is housekeeping no branch
earned: deleting a shipped version's section, or moving items between
releases.

**A shipped version's section is deleted, not kept** — the design record, the
CHANGELOG and the tickets are the durable copies, and a list long enough to
scroll costs the reading it exists to save. Delete the file only when nothing
is scheduled.

Each release branch is cut from `main`; each ticket is a branch cut from the
release branch and squashed back; the release branch merges into `main` as a
merge commit (`docs/branch-and-release.md`).

## 0.8.3 — three of eight, and every one of them measured its own chain

Shipped 2026-09-07. Five items were carried to 0.9.0 rather than rushed; the
list below is what the release actually holds, and the paragraph after it is
what the run learned, because that is the only part a later reader cannot
re-derive from the CHANGELOG.

- [x] #163 — the printed ledger name collapsed `lnk/..` through `relpath`, so a BROKEN row was reported under a different existing file. Two rounds. The issue named four print sites; the class was closed by following where a ledger path can reach, and there were five.
- [x] #177 — an unwritable `.venv` turned `bin/test`'s refusal into a traceback, because #156's round 2 moved the ignore onto every exit of `ensure` including the two whose whole product is a sentence. Three rounds, one reopening. What the branch was actually about is two ledger rows found under-specified rather than falsified.
- [x] #175 — a zero span and a naive timestamp still ended `session_cost`'s report, and #170's row claimed a class its enumeration had not covered. Four rounds, capped.

**Every 🔴 in this release came from the fix before it, and #175 is where that
is measured rather than asserted.** Its round 1 found a deferral resting on one
reading of one field — the single usage field that never reaches the site that
raises. Round 2 found round 1's guard had broken a shape that worked, through a
residual the fix pass had written into its own record *in the same commit that
created it*, without re-running the walk. Round 3 found that the funnel answers
for a value and nothing answers for what two values make. Round 4 was told to
walk round 3's downstream rather than guess it, did, and found one more.

The rule that came out of it, and that the next release's prompts carry: **when
you widen a guard, re-run the enumeration over what the widening itself added;
and when a record states a limit, the pass that writes it owes the check that
the limit is not already reachable.**

## 0.9.0 — what 0.8.0 deferred, what 0.8.3 could not reach, and what its rounds earned

Three sources now, and the middle one is the reason the list is long rather
than a sign it should be cut. Five items were carried here from 0.8.3 on
2026-09-07: the release shipped three of eight, and stopping was the call
rather than the failure — #175 alone ran four rounds and three of its findings
were 🔴. Not ordered; #98 rides whichever branch is open.

**Carried from 0.8.3, untouched.**

- [ ] #145 — the orchestrator is the most expensive segment in a chain and the only one measured by the whole session, so #51's observation 1 has bands for three segment kinds and none for it. #170's token line is what makes it answerable.
- [ ] #160 — four export cases fail on macOS and pass in CI, so a broad run cannot be read as a verdict. **The cause is settled**: 0.8.3's own broad gate reproduced it live at 00:21 KST against 15:21 UTC, and the branch it ran on touches neither file involved. It is #127 — the four cases build their expected name from the local date and `export()` writes it in UTC — and the two are one ticket. What is left is the owner's call on which side moves; 0.8.3 recorded its recommendation on #160.
- [ ] #167 — a closing keyword claims one issue, and a body naming two in one sentence loses the second silently.
- [ ] #180 — three written rules were each re-broken in one run; written down and arriving at the act are different states.
- [ ] #182 — the hider guard's enumeration names three copies where the property is every copy out of `raw`. `spec.md` and `plan.md` for it were drafted during 0.8.3 and are in this run's scratch, not in the tree.

**Earned by 0.8.3's own rounds.** Five of the six are the same sentence in
different clothes: *a record is written by a machine and then trusted like
one, while nothing checks what it says.*

- [ ] #187 — the round record carries the reviewer's tables and drops the paste-ready fix the findings format requires. Measured: a fix pass re-derived a verified artefact from scratch, and its first re-derivation was wrong.
- [ ] #189 — a bare pipe inside a Verdicts cell truncates the row, and nothing sees it. Two paste-ready fixtures were invisible in a rendered record; a later fix pass then hit it again after being warned.
- [ ] #190 — a record states a figure or a stamp the next commit moves, and no check reads it. Closed three times on one work item by enumerating carriers, and back each time.
- [ ] #192 — a funnel answers for the values that enter, and nothing answers for what two of them make. #175's round 3, measured at the base as well as on the branch.
- [ ] #193 — a third the file could not compute is charged 0, and the context line takes that 0 for a baseline. Carries a verified patch and a case seen red, plus two smaller ones as a comment.
- [ ] #194 — `Contract changes` compares arities, so a unit returning a new *meaning* reads as `none`. That row exists for #57's largest regression class and read `none` on a live instance of it.

**The five that were 0.8.0's**, sitting here since 2026-09-04 for the reason
the section above states rather than because the list was long.

- [ ] #97 — the three pin levers left after #117 took the fourth. Each changes pins that already exist, so each needs a question batch.
- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows.
- [ ] #111 — `git()` reads every failure as `""`, and in `seal import` that empty string switches off the refusal that keeps another project's records out.
- [ ] #134 — the update notice names a restart and never the reload this repository measured and wrote down. One notice and one skill.
- [ ] #98 — three sentences say `-z` is what turns git's path quoting off, and the instruction they give is right while the reason they give for it is false. One line, and it rides whichever branch of this release is open.
- [ ] **#149 — a record says what a segment COST and not what its output cost the next reader.** #137's second half, split off when its first half shipped. Five candidate signals and no evidence which of them survive contact: surviving mutations, defects the next round found inside this segment's output, `New units` depth, fix passes needed, and divergences from the plan. It waits for the accumulation the `Ran by` row now makes possible — an outcome column chosen before there are attributed readings to choose it against is the mistake #110's *Not this* refuses on the review side.
- [ ] #151 — the preset tells a session to create the root, and the question that was supposed to come first lives in a skill it never loads. Reported from a repository's first work item: `seal/` appeared and nobody was asked about shared or local mode. Not this release's own work — it rode in on the flow update that closed #137.

## 0.10.0 — the agent set

In this order, and the third is not optional.

- [ ] **#30 — `sealer` owns the one full-suite run.** Today the smith and the warden are both forbidden it and nobody is assigned it.
- [ ] **#84 — `framer` writes the frame the smith fills**, so the writer of the contract is not its executor. Needs #121's phase channel — a framer that draws the plan and never authors the half of a phase prompt only building can teach is a partial answer.
- [ ] **#120 — the agent contract is settled against five agents rather than three, and it lands before either of the two above is released.** Three of its sixteen sections apply to all five; §2 forbids the broad gate the sealer exists to run, and §6 forbids the durable record the framer and the sealer both write. A release that ships five agents under a contract contradicting two of them is the release that teaches readers the contract has exceptions.

**Why last, and why the number moved.** #84 needs the channel 0.7.0 builds and
the attribution #137 builds. These three were 0.9.0 until 2026-09-04, when the
two releases above took their numbers; nothing about the set changed. They are
designed and #120's table is already counted, which is why they have a release
at all while the rest of what the measurements ask for does not yet: what is
not written down cannot be scheduled, and arrives as its own ticket sized when
it exists. Three arrived that way in one afternoon — #136, #137 and #134, out
of the segments of 0.8.0's own first work item — which is the rate this
paragraph should be read at.

## Later — not scheduled

- [ ] #83 `settle` · #85 the orphan branch as the ledger's home · #101 the export's size — the root's later steps.
- [ ] #88 — the routing question asks three boxes and has no way to say "all three".
- [ ] #135 — `user-invocable: false` sits in the copy that loads and the skill is listed as a command anyway. One measurement decides whether it has a fix or only a correction to the record.

## Order inside a ticket

1. Branch from the release branch; write `routing.md` before the first edit.
2. spec · plan (framer, once #84 exists; the session until then) → smith → the draft pull request opens (`skills/code-review/SKILL.md` §*Orchestrator: the pull request opens before round 1, and a phase is re-run* owns when) → warden rounds → sealer → the pull request is marked ready.
3. The pull request body carries `Closes #N`; the release workflow closes the ticket when the release reaches `main`.

