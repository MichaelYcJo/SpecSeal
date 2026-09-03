# Release flow

A checklist for the tickets in flight. Tick a box when the ticket's pull
request has merged into its release branch. **A shipped version's section is
deleted, not kept** — the design record, the CHANGELOG and the tickets are the
durable copies, and a list long enough to scroll costs the reading it exists
to save. Delete the file only when nothing is scheduled.

Each release branch is cut from `main`; each ticket is a branch cut from the
release branch and squashed back; the release branch merges into `main` as a
merge commit (`docs/branch-and-release.md`).

## 0.7.0 — records and measurement, and nothing else

The channel a build phase has never had, built first; the machine that
measures it, second. A change to `templates/`, `agents/` or `skills/` binds
no session until the release is tagged and the plugin updated, so anything
built beside these three is built without them — which is why 0.7.0 is three
items and not the ten once staged here.

- [x] **#121 + #119, one branch — a build phase gets `round-N`'s equivalent, and the record says what it was asked.** `#121`: the review chain hands the next round a committed record (`rounds/round-N.md`) and a build phase hands the next phase a conversation — measured on #107, where four discoveries reached the next phase only because the orchestrator retyped them by hand and a fifth reached nobody and a rule was deleted. `#119`: the record also says what the segment was asked and under which version of the rules it ran. They land in the same files (`templates/sdd-plan.md`, `templates/sdd-round.md`, `agents/smith.md`), so one branch. #119 carries two items marked "needs a second look" before either is built.
- [x] **#109 — measuring a segment and recording what it says becomes automatic.** After #121+#119, so it measures a channel that already exists rather than building the channel and the measurement at once. Its third part — the release closes this version's log and opens the next — is what makes 0.8.0's measurement issue exist without anybody opening it.
- [ ] #89 — the log, until #109 replaces it with a versioned one.

## 0.8.0 — the first version built under both machines

What 0.6.0 (the contract) and 0.7.0 (the phase channel and automatic
measurement) hand it. Not ordered beyond the one pair that must stay
together.

- [ ] **#110 + #117 — when a review run stops, and how deep a fix may pin.** One branch, because apart they undo each other: #110 removes the late rounds, and the late rounds are where the previous round's pins get read.
- [ ] #97 — the three pin levers left after #117 took the fourth. Each changes pins that already exist, so each needs a question batch.
- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows.
- [ ] #111 — `git()` reads every failure as `""`, and in `seal import` that empty string switches off the refusal that keeps another project's records out.
- [ ] #98 — three sentences say `-z` is what turns git's path quoting off, and the instruction they give is right while the reason they give for it is false. One line, and it rides whichever branch of this release is open.

Its measurement log is the first one taken without anybody being told to
take it — #109's own test.

## 0.9.0 — the agent set

In this order, and the third is not optional.

- [ ] **#30 — `sealer` owns the one full-suite run.** Today the smith and the warden are both forbidden it and nobody is assigned it.
- [ ] **#84 — `framer` writes the frame the smith fills**, so the writer of the contract is not its executor. Needs #121's phase channel — a framer that draws the plan and never authors the half of a phase prompt only building can teach is a partial answer.
- [ ] **#120 — the agent contract is settled against five agents rather than three, and it lands before either of the two above is released.** Three of its sixteen sections apply to all five; §2 forbids the broad gate the sealer exists to run, and §6 forbids the durable record the framer and the sealer both write. A release that ships five agents under a contract contradicting two of them is the release that teaches readers the contract has exceptions.

**Why 0.9.0 and not sooner.** #84 needs the channel 0.7.0 builds. These three
are designed and #120's table is already counted, which is why they have a
release at all while 0.7.0's and 0.8.0's later tickets — what the
measurements themselves ask for — do not yet: those are not written down,
so they cannot be scheduled, and arrive as their own tickets sized when they
exist.

## Later — not scheduled

- [ ] #83 `settle` · #85 the orphan branch as the ledger's home · #101 the export's size — the root's later steps.
- [ ] #88 — the routing question asks three boxes and has no way to say "all three".

## Order inside a ticket

1. Branch from the release branch; write `routing.md` before the first edit.
2. spec · plan (framer, once #84 exists; the session until then) → smith → warden rounds → sealer → pull request.
3. The pull request body carries `Closes #N`; the release workflow closes the ticket when the release reaches `main`.
