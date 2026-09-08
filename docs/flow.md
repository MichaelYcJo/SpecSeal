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

## 0.9.x — six releases, and what decides which one a ticket sits in

Split on 2026-09-07 by the surface a branch has to open and by what one release
makes possible for the next, and **regrouped the same day**: 0.9.0's own two
chains ran to the reopening bound and put nine more tickets on the list, which
is what showed that the sizing had to count branches rather than numbers.

Two of the positions are forced rather than chosen. #179 had to be in 0.9.0,
because it goes red on the commit that raises the version to 0.9.0 and nowhere
earlier. #149 has to be last, because its own body says it waits for attributed
readings that do not exist yet — and after 0.9.4, because until then the
readings it would choose against are wrong.

The rest is ordered so that each release is cheaper for the one after it.
0.9.0 makes the round record trustworthy, and every release after it writes
round records. 0.9.3 replaces enumeration by reading with enumeration by
construction, which is the method the meter's own rounds then need. **0.9.4
stands before 0.9.5 for a reason found rather than planned**: both meter
defects were measured on 2026-09-07, and #145 and #149 are answered off the
table they corrupt.

The split is also a size decision, **and it is counted in work items rather
than in ticket numbers.** 0.8.3 shipped three of eight and carrying five
forward was the call rather than the failure, so a release here is three or
four items rather than nineteen.

That distinction was learned rather than designed. A run that reaches the
reopening bound turns every finding still open into an issue, which is right —
and it means one branch's leftovers arrive as four ticket numbers on one file,
which a reader counts as four releases' worth of work. On 2026-09-07, 0.9.1 had
grown to thirteen tickets that way; eight of them were three branches. The
sections below group a ticket set that will be one branch as one row.

## 0.9.1 — what an installed repository hits

Seven work items, and on 2026-09-07 three of the rows below arrived the way
this release is named: **reported from another repository running the plugin,
not from a review round of this one.** Every one of them was hit on 0.8.3 by
somebody doing ordinary work, which is the evidence this release exists to act
on and the kind the tracker has least of.

The sixth arrived on 2026-09-08 from this release's own run, and it is the same
kind of evidence one hop closer: the run needed six branches, so it called
`git worktree add` six times, and the guard held it six times. #237 is here on
the owner's call for that reason — a release run is the workload this project
names its first goal against, and it is where the guard's prompt budget stopped
being a cost and became the thing that ends the run.

**#111 is still the sharpest thing on the whole 0.9.x list**: a git call that
fails reads as a repository with no remote, and that reading switches off the
refusal keeping another project's records out.

The odd one is here on the owner's call: `Contract changes` answers wrongly in
two ways, and the two are one branch on one derivation. It is not user-facing,
and splitting the pair across two releases to make the theme clean would put
one branch in two of them. #227 joins it because it is the same file's
parsing, one row over.

- [x] #111 — `git()` reads every failure as `""`, and in `seal import` that empty string switches off the refusal that keeps another project's records out. Four callers were left after #104 taught two of them to check the return code.
- [x] #134 — the update notice names a restart and never the reload this repository measured and wrote down. One notice and one skill.
- [x] **[#225 · #151] — one branch, local mode from first setup to the gate.** `round_record.py` derives the root from the item path and refuses an item under `.git/seal/`, and `chain_check` then reports the routing declaration missing while it sits at `.git/seal/specs/<item>/routing.md` — a false *no declaration* is indistinguishable from a genuinely undeclared work item, so the one signal the gate exists to give stops meaning anything in local mode. #151 is the other end of the same path: the mode is chosen without the question being asked. **#158 is deliberately NOT here** — it asks whether the root should live under `.git` at all, where these two make the mode work as documented, and folding them would put a design question inside a bug fix.
- [x] #226 — `round_record.py` dies on python 3.9 with a bare interpreter traceback (`zip(..., strict=True)`), after argument parsing and the report read have already succeeded, so the failure reads as a bug in the report rather than an unmet requirement. macOS still ships 3.9 as `/usr/bin/python3`, and a repository pinning a newer interpreter does not help because the script is invoked directly. Reported from another repository on 0.8.3.
- [x] **[#211 · #194 · #227] — one branch, `round_record.py`'s derivation and id rows.** `Contract changes` reads `no call site found` for a pytest test function, and it compares arities, so a unit returning a new *meaning* reads as `none`. #194 moved here from 0.9.0 on 2026-09-07: a second measured instance arrived during #187's chain and it is a shape the ticket's proposed literal-set comparison does not catch — `is_a_record_of_a_moment` changed which inputs map to which of the two values it already returned, with signature, arity, return type and returnable set all unchanged. #227 joined on 2026-09-07 from another repository: round-prefixed finding ids (`R2-1` … `R2-8`) collapse toward one key, and the refusal names neither the format it wants nor the rows it read — the reviewer picks the numbering and the fixer copies it, so the refusal surfaces at the orchestrator, one hop from either agent that could have avoided it.
- [x] #237 — `hooks/worktree-guard.py` answers worktree creation with `ask` at every site that reaches it, and the `[worktree-ok]` site says in writing that this is not a choice: the token is written into the command by whoever issues it, so it is not evidence that a person answered, and reading it as consent would turn the guard off with nobody asked. So there is no path through this guard that costs zero prompts, and a run needing six worktrees pays six hard stops — measured on this release's own run, which is where it was reported. What separates the first creation from the sixth is available without trusting the token: the harness only runs a `git worktree add` that was approved, so a `PostToolUse` observation of one that actually ran is consent the command text cannot forge. The budget goes from one per worktree to **one per session**, and the first creation is still a question.
- [x] **#239 — a stamp names content, not a commit. The owner put this first, on 2026-09-08, because it has been costing a cycle rather than an incident.** `skills/evidence-check/SKILL.md` gives four grounds for deriving a ledger anchor from content instead of writing a marker into the source, and the fourth is this repository's own rider comments: they carried commit SHAs, a squash orphaned them, and a patch release exists because of it. `CLAUDE.md` then states the rule that came out of it — a row carries no line number and no commit SHA — and closes the reasoning with *so a squash orphaned the stamp*. **So the mechanism that supplied the evidence is the one mechanism that never got the repair.** It is not a wrong button either: a fix pass works on a feature branch, a feature branch squashes into its release branch by rule, so the only commits it has to name are the ones that stop existing — and the check then fails on the release branch, where whoever repairs it is never whoever caused it. Three cycles of measurement: `0946350` is a commit whose whole job was re-pointing three stamps after a rewrite, the release-to-`main` direction cost a patch release, and `release/v0.9.1` went red again the moment #226 merged. Scope is 13 rider stamps across 10 files, plus 135 round records carrying a `Target SHA` the same squash orphans — the second half may be right to leave alone, since nothing resolves it, but that is to be answered in this change rather than assumed. #240 is the instance repair and is not this.

## 0.9.2 — what the chain found about itself, in the units it found them in

Four work items, and six of the ticket numbers below belong to two of them.
A capped run turns every finding still open into an issue, which is right — and
it means one branch's leftovers arrive as four ticket numbers on one file. They
are grouped here as the branches they will actually be.

**#228 is the newest and it is the one this release is named for.** The chain's
own artifact — the reviewer's report — never reaches a file, so the orchestrator
retypes it. That was measured across four rounds of one work item in another
repository, and reproduced here on 2026-09-07: 0.9.0's own #190 · #207 run
retyped rounds 2 and 3 into files by hand before `round_record.py new` could
read them.

- [x] **[#203 · #204 · #205 · #206] — one branch, `tests/test_release_hygiene.py`.** #179's run hit the reopening bound with these open: nothing observes what the version check prints, an uppercase `V0.9.0` is invisible, two records describe an order bug that never happened, and the tracker document states the check wider than it is.
- [x] **[#209 · #210] — one branch, the pre-merge guard.** Its reader has a failure arm no case watches, and its parametrized case is a class over two literals rather than over the reader's passes.
- [x] #167 — a closing keyword claims one issue, and a body naming two in one sentence loses the second silently.
- [x] #228 — `round_record.py new` takes `--report <path>`, a file. The reviewer returns its report as its final message and the orchestrator is told not to open the agent transcript, so the report exists in two places and neither is a file — and the orchestrator retypes it. **A lossy copy of a document whose whole value is that it is exact**: verdict rows carry coordinates, and a coordinate typed from memory is worse than no coordinate. It compounds per round, because re-review inheritance carries the paraphrase forward, and it breaks the audit line the record holds — `Fixes checked by` points at a round whose report is not the report the reviewer wrote. The fixer already writes its fix table to a path under the work item, so the shape exists and the reviewer side is the half that is missing.

## 0.9.3 — the enumeration was done by reading

**Five work items, and four of them are the one the section is named for.**
That method — enumerating a class by construction rather than by reading it —
is what observation 6 on #51 found eight times without a single instance
caught by reading. #170's round 2 is the positive case: a fix pass
re-enumerated its class by construction and found a second crash site where
the finding named one.

**#272 is the fifth and it is here for a different reason**, which is worth
saying rather than hiding behind the count. It is not a missed enumeration; it
is the release itself getting more expensive the more work items it carries,
at roughly the square of them. So it goes first and squashes first, and the
other four inherit the repair instead of each paying for it — which is the
only ordering constraint in this section.

0.9.0's own two chains are the second measurement and they are larger: nine
instances on one branch and seven on the next, every one found by mutating code
rather than by reading it, and each one inside the fix for the one before.

- [x] #272 — `unverified_check` took its baseline from the pull request's base, and that branch moves: the moment one work item squashed into the release branch, every sibling cut before that squash read the squashed item's `overview.md` as *rows that left the record*. The refusal was right about what it measured and wrong about what happened. **Three of 0.9.2's four branches paid it**, each a release-branch merge, a re-run broad gate, a re-pushed pull request and a `docs/flow.md` conflict, and the cost is roughly quadratic in the items a release carries. The baseline is now the merge base of the base ref and `HEAD` — the fork point — so what landed on the base after the fork is not this branch's removal. **First of the five and squashed first**, so the other four merge a release branch that already holds it. `docs/release-checklist.md` step 0's workaround goes with the repair; the never-rebase rule that was written inside it stays, as the standing rule it always was.
- [x] #182 — the hider guard's enumeration names three copies where the property is every copy out of `raw`. The answer is a property about the **destination** rather than a fourth row: every copy lands in one artefact, so `round_record.py` reads a record back through the shared reader before it writes, and the completeness argument is a case walking the module's own syntax tree for every writer. Measured at the base, against the ticket's own account: the loss does not re-enter the chain, and what is reachable is one step earlier and silent at exit 0.
- [x] #192 — a funnel answers for the values that enter, and nothing answers for what two of them make. #175's round 3, measured at the base as well as on the branch.
- [x] #265 — a warden spawn reads ~110,000 characters, about 30k tokens, before its first tool call, and **53% of `code-review/SKILL.md` is addressed to the orchestrator** — five sections the file itself prefixes `Orchestrator:`, 24,948 characters measured at this branch's base, which a reviewer never acts on. They were one contiguous block, lines 236–653, and they moved verbatim to `skills/code-review/orchestration.md`; the three `writing-style` sections that are not a reviewer's moved to `skills/writing-style/outside-the-review.md`. A warden spawn drops from 108,399 bytes to 78,109, measured with `wc -c` over the three files its `skills:` list names plus its own definition. Both of #255's supporting enumerations were taken by grep and both were short: the grep for the literal `Orchestrator:` saw the five `##` headings and none of the seven `###` subsections under them, so it missed four live references including one in `agents/smith.md`; and *eleven test modules that pin the path* is eleven by path and 21 in fact, because ten name the file as a Python tuple. Six of the eleven needed nothing and five modules the ticket never named broke.
- [x] #180 — three written rules were each re-broken in one run; written down and arriving at the act are different states. **Seven instances now.** The fifth is the reopening bound itself — a rule the acting session had read, restated as the cap, and propagated five times. The sixth arrived on 2026-09-07 as #229, folded here and closed: the first measurement of this class **outside this repository**, over a documentation work item of fifteen files whose findings per round ran 13 → 8 → 5 → **6** and never converged, with 3 of its 4 rounds repeating an earlier finding in a different file. The seventh is 0.9.0's own #190 · #207 run — the printed bound fixed three times in three places, each fix inside the one before, and `claim_lines` fixed twice. The rule already written for all seven is `agent-contract` §12, *do not fix the coordinate*, and it reaches every agent at startup. **The repair this ticket takes is the check, not another instruction**: after a fix pass, grep the changed sentences' distinguishing terms across the rest of the corpus and report the survivors — a thing that can fail, where a widened instruction is one more sentence in the state that has now failed seven times.

## 0.9.4 — the instrument, before anything reads it

Four work items. The first three are the ordering the section is named for:
**#145 and #149 are answered off a table that is wrong today.** Both meter
defects were found on 2026-09-07 by taking this release line's own segment
readings, and every per-segment reading this repository has published carries
them.

**The fourth is not a meter defect and carries no ordering.** #256 and #257
arrived from the 0.9.2 release run, on one branch and one file, and they were
held out of 0.9.2 because that release was already running and does not take
new items. They sit here because 0.9.3 shipped without them and the next
release is where a finished branch lands, not because they belong to the
instrument. Both were found by *using* the worktree guard rather than by
reading it, and #256's repair had to discard the direction its own ticket
settled — the discriminator that ticket names was measured false, and the
measurement needed a positive control the ticket's own probe did not have.

- [x] #200 — the meter's `test` family names five runners and not this repository's, so fourteen `./bin/test` runs read as `other` and the one call it charged to `test` was a file write containing the word.
- [x] #202 — a streamed message is counted at its first partial row, so a round that wrote a full report reads as 62 output tokens. The error is not a scale factor: 3.2x on one segment and 334x on another, the same day, with nothing in the printed report saying which.
- [x] #193 — a third the file could not compute is charged 0, and the context line takes that 0 for a baseline. Carries a verified patch and a case seen red, plus two smaller ones as a comment. **The three shipped as one branch, because they are one file and one theme** — every per-segment reading this repository has published carries all three — and because the section's ordering constraint is against 0.9.5, not among themselves. What each ticket said and what the measurement said parted twice: #200 names one file write charged to `test` and there are **644**, with `lint/type` and `build` carrying the same kind; and #202's *keep the last row or take the maximum* is a choice its own corpus cannot decide, since the two agree on all 13,425 messages with 0 rows out of order, so the case separating them was built rather than found. **The decision #200 left open was answered with a fourth shape none of its three was**: the widened pattern is the cheap one and its own objection is *no sign of it*, so the report now names the slowest command it could not classify whenever `other` leads. The `seal/config.md` row stays unbuilt with the condition under which it becomes right written down.
- [x] **[#256 · #257] — one branch, `hooks/worktree-guard.py`.** Both came out of the 0.9.2 release run's own worktree friction. #256: the guard's last liveness arm reads a fresh transcript with no matching process as a live session, and an exited session presents identically, so the tree read as concurrent for five minutes after every session in the project ended — a hard deny on `git switch`, steering work into worktrees nobody needed. **The ticket's settled direction was measured false and not built.** No live `claude` holds its transcript open, including one writing its own file seconds earlier, so the open-descriptor probe would have answered *not held* for every session and collapsed the arm to always-idle; no terminal marker exists either. The ticket's own probe had no positive control, which is what let a true reading stand for a discriminator that never discriminated. The repair needed no new signal: `fresh_leases` had already retired that session's lease on positive evidence its pid was gone, and the arm was putting it back. #257: with a consent record present, a command that creates a worktree *and anything else* still asked, where the Agent path already answered `silent` for the same shape with the argument written beside it — two of five confirmations on the 0.9.2 run, both triggered by the batching this repository's own `CLAUDE.md` asks for.

## 0.9.5 — what the readings answer, and what a green gate means

Four work items. The first two are the questions #51 has been holding open for
a measurement it can trust; the last two are the other half of the same
sentence — a gate finishing green where green does not mean the code is right.

- [ ] #145 — the orchestrator is the most expensive segment in a chain and the only one measured by the whole session, so #51's observation 1 has bands for three segment kinds and none for it. #170's token line is what makes it answerable — after 0.9.4.
- [ ] #149 — a record says what a segment cost and not what its output cost the next reader. #137's second half. Five candidate signals and no evidence which of them survive contact: surviving mutations, defects the next round found inside this segment's output, `New units` depth, fix passes needed, and divergences from the plan.
- [ ] #262 — nine arms of the pre-merge guard are watched by no case, and a written list of them rots the way #210's did. Opened by 0.9.2's #209 · #210 run, which closed four of the thirteen and measured the rest. It sits with these because the module is green with any of the nine deleted, which is this release's sentence: the durable close is a checker that enumerates a module's arms from its own source and mutates them, not nine hand-written cases.
- [ ] #160 — four export cases fail on macOS and pass in CI, so a broad run cannot be read as a verdict. The cause is settled and #127 is folded in here: the cases build their expected zip name from the local date and `export()` writes it in UTC. What is left is the owner's call on which side moves.
- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows. **A third arrived in 0.9.0**: a coordinate the records arm built printed with the platform separator, and the Windows leg was red on it from the commit that added the arm through three review rounds and two broad gates, all of which ran on macOS where the fix is a no-op.
- [ ] #198 — a release closes its flow-measurement log with nothing written in it, and nothing notices. It sits with these because #145 and #149 are the two tickets that eat the data it protects, and this is the release they land in.

## 0.10.0 — the agent set

In this order, and the third is not optional.

- [ ] **#30 — `sealer` owns the one full-suite run.** Today the smith and the warden are both forbidden it and nobody is assigned it.
- [ ] **#84 — `framer` writes the frame the smith fills**, so the writer of the contract is not its executor. Needs #121's phase channel — a framer that draws the plan and never authors the half of a phase prompt only building can teach is a partial answer.
- [ ] **#120 — the agent contract is settled against five agents rather than three, and it lands before either of the two above is released.** Three of its sixteen sections apply to all five; §2 forbids the broad gate the sealer exists to run, and §6 forbids the durable record the framer and the sealer both write. A release that ships five agents under a contract contradicting two of them is the release that teaches readers the contract has exceptions.

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

