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

## 0.9.x — what decides which release a ticket sits in

0.9.1 through 0.9.4 shipped and their sections are gone — a shipped version's
section is deleted rather than kept, and the CHANGELOG, the design records
under `seal/specs/` and the tickets themselves are the durable copies.

Two things the split left behind, because they still decide what is below.

**#149 is last, and it is the one forced position left.** Its own body says it
waits for attributed readings that did not exist when it was written, and it
had to come after 0.9.4 — until the meter was fixed, the readings it would
choose against were wrong.

**A release is sized in work items rather than in ticket numbers, and three or
four is the size.** A run that reaches the reopening bound turns every finding
still open into an issue, which is right — and it means one branch's leftovers
arrive as four ticket numbers on one file, which a reader counts as four
releases' worth of work. 0.8.3 shipped three of eight, and carrying five
forward was the call rather than the failure. The sections below group a
ticket set that will be one branch as one row.

## 0.9.5 — what the readings answer, and what a green gate means

Seven work items, and every move of the count has come from the release's own
run rather than from planning. #103 and #198 joined without the sentence below
being widened to hold them. **[#296 · #295 · #297] arrived on 2026-09-09** —
one found by following `orchestration.md` and watching CI go red for it, one
by measuring how often the broad gate's row is left open, and one by deleting
what the file above says to delete. **#300 arrived the same day, out of #145's
own round 3.** And **#160 left**: its four cases pass on macOS at this commit,
because the repair landed in `1dedd1e` a release and a half ago and nobody
closed the ticket — the ticket's own reading, a symlinked temporary root, was
never the cause, and the row said the owner still had a call to make when the
call had been made.

**#145 and #149 are the questions #51 has been holding open for a measurement
it can trust.** #262, #160 and #103 are the other half of the same sentence —
a gate finishing green where green does not mean the code is right. **#198
sits with them because it protects the data the first two eat**: a release
cycle that measures nothing is a cycle #145 and #149 cannot use, and 0.8.3 is
already one of them.

Seven is over the size the section above states, and the count is left
standing rather than resolved by moving a row: which item leaves 0.9.5 is not
a bookkeeping decision. What is worth reading in it is where the items came
from — four of the seven were opened by this release's own work, and one was
closed by discovering it had already shipped. A release that measures itself
finds more than a release that is planned, and the size rule is what says so
out loud rather than a target to be met by moving rows.

- [x] #145 — the orchestrator is the most expensive segment in a chain and the only one measured by the whole session, so #51's observation 1 has bands for three segment kinds and none for it. #170's token line is what makes it answerable — after 0.9.4.
- [ ] #149 — a record says what a segment cost and not what its output cost the next reader. #137's second half. Five candidate signals and no evidence which of them survive contact: surviving mutations, defects the next round found inside this segment's output, `New units` depth, fix passes needed, and divergences from the plan.
- [ ] #262 — nine arms of the pre-merge guard are watched by no case, and a written list of them rots the way #210's did. Opened by 0.9.2's #209 · #210 run, which closed four of the thirteen and measured the rest. It sits with these because the module is green with any of the nine deleted, which is this release's sentence: the durable close is a checker that enumerates a module's arms from its own source and mutates them, not nine hand-written cases.
- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows. **A third arrived in 0.9.0**: a coordinate the records arm built printed with the platform separator, and the Windows leg was red on it from the commit that added the arm through three review rounds and two broad gates, all of which ran on macOS where the fix is a no-op.
- [ ] #198 — a release closes its flow-measurement log with nothing written in it, and nothing notices. It sits with these because #145 and #149 are the two tickets that eat the data it protects, and this is the release they land in.
- [ ] #300 — the rows' spans do not partition the time, and three printed sentences are wrong about it. Opened by #145's round 3, which ends that run: assigning a call to a window by its START is what makes the CALLS partition, and it leaves a call that outlives its row's cut covering seconds the next row covers too. Two of the three are inside 0.9.5's own new mode — the refusal names a spawn's result where the head row's cut is the first spawn's START, and a sub-three-second overlap prints `by 0.0m` as the grounds for withholding a figure — and the third is pre-existing, in the PLAIN report every published segment reading goes through: `command 16.8m 101%`. **The fix is written, verified and paste-ready** in that work item's `rounds/round-3-report.md`, with a case seen red; a fix pass could not take it because `orchestration.md` refuses depth 2, and a `# RIDER:` is refused by measurement — four ledger rows anchor at `#report_spawns` and two at `#analyse`.
- [x] **[#296 · #295 · #297] — one branch, what CI reads at a pull request into a release branch.** All three came out of this release's own run and none of them was found by reading. #296: `chain_check`'s `Pass` arm tells the author *"Open it as a draft while the rounds run"* and the record-count arm a hundred lines later has no draft state in it, so a draft opened where `orchestration.md` says to open one is red until round 1's record lands — seen on #294. #295: the one-broad-run rule is written in five places and nothing checks that it arrives, which is 47 of 63 `Not verified` rows still open — and **the home already exists and nothing opens it**, since every round record carries `| Broad gate |`, `not yet` or the SHA the run happened at. #297: deleting a shipped section, which this file's own rule asks for, reads as 153 uncorrected survivors, so #293 merged red. The three share the argument `hygiene.yml:221` already makes for exempting the release range — *a range no fix pass wrote*.

## 0.10.0 — the agent set

In this order, and the third is not optional.

- [ ] **#30 — `sealer` owns the one full-suite run.** Today the smith and the warden are both forbidden it and nobody is assigned it.
- [ ] **#84 — `framer` writes the frame the smith fills**, so the writer of the contract is not its executor. Needs #121's phase channel — a framer that draws the plan and never authors the half of a phase prompt only building can teach is a partial answer.
- [ ] **#120 — the agent contract is settled against five agents rather than three, and it lands before either of the two above is released.** Three of its sixteen sections apply to all five; §2 forbids the broad gate the sealer exists to run, and §6 forbids the durable record the framer and the sealer both write. A release that ships five agents under a contract contradicting two of them is the release that teaches readers the contract has exceptions.
- [ ] **#292 — a payload is written again on every spawn, and nothing measures which of it the agent acts on.** Measured 2026-09-09 over 49 subagent spawns: `cache_creation` of 40,259–75,737 tokens on every one of them, with `cache_read` a constant that covers only the harness prefix — so an agent's own payload, its definition and the skill bodies its `skills:` list injects, is not amortised across spawns. **It is fourth and its meter comes before the third's trimming**, because #120 removes sections from a payload and a before-and-after number is what says whether that worked. `implement` is the largest payload now — 46,249 B of `smith`'s 113,633, where #265 measured `code-review` and left it at 78,109 for the warden.

**Which delegate a step goes to, and the one question that decides it.**
Written after 0.9.2, off #263's side-by-side and the comments on it, because
this set is where the answer stops being academic — three agents become five
and #120 settles a contract against all of them.

The axis is **not** *delegate or do it myself*. It is **is this work finding
out, or writing down**, and the two sit on opposite sides of a subagent
boundary for a structural reason:


| Kind of work  | Shape                      | Why the boundary helps or hurts                                                                                                              |
| ------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| discovery     | large input → small output | the delegate pays the reading and the parent receives coordinates. A subagent boundary IS a compression boundary, and this is what it is for |
| transcription | small input → large output | the parent already holds the input. A prompt can be handed over; a context cannot — so the delegate buys the discovery a second time         |


#263 measured the second row without naming it: `smith` #1 · #2 · #3 spent
378k · 474k · 555k tokens and 141 · 43 · 35 tool calls against a parent doing
the same class of change in 8–14 calls, and that issue's own reading is *the
files were already read — that, not reasoning speed, is the dominant cost*.
Neither of the two things it credits to delegation was `smith` writing code:
the only genuine security finding was `warden`, in twelve minutes, and the
third-repository field mapping was discovery by a run that was killed before
it implemented anything.

**So `smith` is the role this set empties out**, because after the split its
whole remit is the transcription step. Three answers are live — keep it as the
default, retire it, or re-scope it as a **conditional** executor — and the
recommendation is the third, with the criterion written into `routing.md`
first, where the axis already exists and has no stated criterion:

> Finding out goes to `scribe`. Writing down stays with the session — unless
> the expected diff is large enough to threaten what the orchestrator still
> has to hold, which is the one case `smith` answers.

That last clause is the only number nobody has, and it is not a cost question:
the orchestrator is the single participant a release cannot replace mid-run, so
the case for a delegate there is **replaceability**, on a different axis from
everything measured above.

**#84 has a falsifiable success test and it is `smith`'s token count.** The
documents a frame needs already exist — `spec.md`, `plan.md`, `phases/`, and
whatever a `scribe` wrote — so the cost is not intrinsic to delegation but to
spawning with a prompt instead of a dossier. If the frame is complete, `smith`
reads the frame rather than the repository and 378k / 141 falls; if it does not
fall, the frame was not complete. What a frame cannot remove is the fixed part
`#265` measured, ~30k tokens before the first tool call, so the gap narrows
toward that floor and never to zero.

**And the ordering `#120` states is right for `sealer` and `framer` and wrong
for `smith`.** A contract that scopes a role whose scope is unsettled is the
most expensive place to be wrong, because it is paid on every spawn of every
agent. Settle §2 and §6 here; let `smith`'s sections be the one thing that
waits.

**Why last, and why the number moved.** #84 needs the channel 0.7.0 builds and
the attribution #137 builds. These three were 0.9.0 until 2026-09-04, when the
work above took that number and the three after it; nothing about the set
changed. They are designed and #120's table is already counted, which is why
they have a release
at all while the rest of what the measurements ask for does not yet: what is
not written down cannot be scheduled, and arrives as its own ticket sized when
it exists. Three arrived that way in one afternoon — #136, #137 and #134, out
of the segments of 0.8.0's own first work item — which is the rate this
paragraph should be read at.

## Later — not scheduled

- [ ] #83 `settle` · #85 the orphan branch as the ledger's home · #101 the export's size — the root's later steps.
- [ ] #88 — the routing question asks three boxes and has no way to say "all three".
- [ ] #135 — `user-invocable: false` sits in the copy that loads and the skill is listed as a command anyway. One measurement decides whether it has a fix or only a correction to the record.
- [ ] #264 — three review rounds each found an arithmetic error inside the previous round's fix, and the cause was two unlabelled denominators. Opened by 0.9.2's #209 · #210 run; all five findings are corrected there. It carries no release because its own body leaves the shape open — whether a declared counting basis is worth building, or only the narrower refusal of a Notes cell whose subtraction does not reconcile.
- [ ] #97 — the three pin levers left after #117 took the fourth. Each changes pins that already exist, so each needs a question batch, which is why it carries no release rather than a late one.

## Order inside a ticket

1. Branch from the release branch; write `routing.md` before the first edit.
2. spec · plan (framer, once #84 exists; the session until then) → smith → the draft pull request opens (`skills/code-review/orchestration.md` §*Orchestrator: the pull request opens before round 1, and a phase is re-run* owns when) → warden rounds → sealer → the pull request is marked ready.
3. The pull request body carries `Closes #N`; the release workflow closes the ticket when the release reaches `main`.

