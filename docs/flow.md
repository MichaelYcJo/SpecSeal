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

0.9.1 through 0.9.5 shipped and their sections are gone — a shipped version's
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

## 0.10.1 — the three 0.9.5 planned and did not reach

Moved here on 2026-09-10, when 0.9.5 was cut at five: eight was over the size,
the five that shipped were the ones the release's own run produced, and these
three were the ones it was planned around.

**Renumbered from 0.9.6 the same day, and the agent set goes first.** That was
the owner's call and the reason is that 0.10.0 is the main line of the work
rather than a detour from it. What the order costs is written down rather than
left to be discovered: #103 makes the two defect shapes only Windows catches
visible without Windows, and 0.10.0 widens exactly that surface — five agent
definitions and new record paths are all path-spelling candidates — so 0.10.0
will learn about them at its own pull request. #198 protects the measurement
of a cycle, and the cycle that changes the agent set from three to five is the
one with most to measure.

**#149 is last here too, and for the reason it was last there.** It waits on
attributed readings, 0.9.5 is the release that produces them, and this is the
first release that can read them rather than the first that could have.

- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows. **A third arrived in 0.9.0**: a coordinate the records arm built printed with the platform separator, and the Windows leg was red on it from the commit that added the arm through three review rounds and two broad gates, all of which ran on macOS where the fix is a no-op.
- [ ] #198 — a release closes its flow-measurement log with nothing written in it, and nothing notices. It sits with these because #145 and #149 are the two tickets that eat the data it protects, and this is the release they land in.
- [ ] #330 — every rule an agent follows arrives by mechanism, and every rule the orchestrator follows arrives as a sentence it has to remember. The repository has already run the experiment on itself: three acts that were sentences were given a command and stopped being forgotten, and the three still written as sentences each have a measured miss — the broad gate, the flow-log posting, and the routing question, which was broken by a session that had the one-batch rule loaded. Opened during 0.10.0's first two work items, and it sits here because #30 closes the first instance and is the template: what is left is whether the shape generalises to acts that need a person, which a command can print a question for but cannot ask.
- [ ] #331 — every ambiguous word this repository has fixed was found by a person reading, one at a time. `tests/test_one_word_one_meaning.py` holds five of them, and `seal` is the sixth: it named the warden's review mark, the sealer's stamp and the smith's proof block at once, and it turned up in conversation rather than through anything in the tree. Nothing enumerates the seventh. The census in the ticket reads 968 twelve-word runs shared across two or more of `skills/`, `agents/` and `docs/` — an upper bound and not a defect count, because this repository's own rule has one carrier state a rule and every other quote enough of it to name the owner, so a link is right and a restatement is the defect, and the sweep has to tell them apart. **It sits here rather than in 0.10.0 because the census has to be taken after the agent set settles**: a sweep run while two of the five definitions do not exist and #120 is about to re-home a third of the contract decides every word twice. The fifth agent is also what made the sixth word visible — `seal` read one way while the warden was the only agent keeping one.
- [ ] #149 — a record says what a segment cost and not what its output cost the next reader. #137's second half. Five candidate signals and no evidence which of them survive contact: surviving mutations, defects the next round found inside this segment's output, `New units` depth, fix passes needed, and divergences from the plan.

## 0.10.0 — the agent set

**Next, on the owner's call of 2026-09-10: this is the main line of the work.**
0.9.6's three moved to 0.10.1 for it, and what that costs is written in that
section rather than left to be discovered.

In this order, and the third is not optional.

**The order has one constraint that is not the list's order, and it is worth
stating because two documents look like they disagree.** #292's row below says
its meter comes before #120's trimming, and #120's own body says the opposite
of what this section's third bullet says — *"Not a request to split the
contract now. The two agents do not exist... The line gets drawn when there is
something to draw it against."*

Both are true at once, and only one reading makes them so: **#120 lands before
either of the two above is RELEASED, not before either is BUILT.** So the
sequence inside the release is

> #292's meter · #30 · #84 · then #120 settled against all five agents.

The meter first because a before-and-after number is the only thing that says
whether #120's trimming worked, and #120 last because a contract scoped
against a design rather than against a file is the mistake #107 already made
once — it specified `docs/agent-contract.md`, and
`docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` measured
that the location cannot work.

- [x] **#30 — `sealer` owns the one full-suite run.** Today the smith and the warden are both forbidden it and nobody is assigned it.
- [ ] **#84 — `framer` writes the frame the smith fills**, so the writer of the contract is not its executor. Needs #121's phase channel — a framer that draws the plan and never authors the half of a phase prompt only building can teach is a partial answer.
- [ ] **#120 — the agent contract is settled against five agents rather than three, and it lands before either of the two above is released.** Three of its sixteen sections apply to all five; §2 forbids the broad gate the sealer exists to run, and §6 forbids the durable record the framer and the sealer both write. A release that ships five agents under a contract contradicting two of them is the release that teaches readers the contract has exceptions.
- [x] **#292 — a payload is written again on every spawn, and nothing measures which of it the agent acts on.** Measured 2026-09-09 over 49 subagent spawns: `cache_creation` of 40,259–75,737 tokens on every one of them, with `cache_read` a constant that covers only the harness prefix — so an agent's own payload, its definition and the skill bodies its `skills:` list injects, is not amortised across spawns. **It is fourth and its meter comes before the third's trimming**, because #120 removes sections from a payload and a before-and-after number is what says whether that worked. `implement` is the largest payload now — 46,249 B of `smith`'s 113,633, where #265 measured `code-review` and left it at 78,109 for the warden. **Built, and two things #120 reads before it trims.** The payload IS cached across spawns of one agent, for five minutes, and re-written on every spawn further apart than that — which in a chain is every one, so the sentence above is narrower than it reads (`seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/spec.md` §*Measured before the first edit*). And every per-file token figure the meter prints is an estimate from a per-agent ratio — 2.87, 3.41 and 3.44 B/token for smith, warden and scribe — until that work item's `questions.md` Q4 probe, one agent definition per file spawned once, replaces it; a measured after-number needs a spawn taken after the trim, and given none the meter keeps the before-ratio and says so.

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

