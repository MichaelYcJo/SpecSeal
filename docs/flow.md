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

## 0.8.0 — the chain's own machinery, and nothing else

Three items, and the shape of the list is the argument. A change to
`templates/`, `agents/` or `skills/` binds no session until the release is
tagged and the plugin updated, so **anything built beside these three is built
without them** — a review chain with no floor reviewing the branch that adds
one, a segment measured by a meter that cannot say what ran it. That is the
sentence 0.7.0 wrote here when it cut ten items to three, and 0.8.0 is the
first release to be planned against it rather than to discover it.

- [x] **#110 + #117 — when a review run stops, and how deep a fix may pin.** One branch, because apart they undo each other: #110 removes the late rounds, and the late rounds are where the previous round's pins get read.
- [x] **#136 — the roll opens the next measurement log with no body and no index, and this release is what fires it.** Two issues collect the same shape of comment, one of them is deleted every release, and nothing says which gets what. It has to land before 0.8.0 reaches `main`: that push runs the roll, and after it the 0.9.0 log is already open, empty and unlabelled, with the next chance a release away.
- [x] **#137 — a segment's record says what it cost, and not what ran it or what its output cost the next reader.** Every segment measured before this lands is one nothing can attribute afterwards, which is a deadline with no date on it. It is also what #84 needs before its own last line can be answered. **Narrowed to its first half**: the `Ran by` row shipped, and the outcome column beside it moved to 0.9.0 below — #137's own body refuses to pick a format for it before knowing which of five candidate signals survive contact.
- [ ] #145 — the orchestrator is the most expensive segment in a chain and the only one measured by the whole session, so #51's observation 1 has bands for three segment kinds and none for it. Last of this release, because it is what the other two make answerable.

Its measurement log is the first one taken without anybody being told to
take it — #109's own test.

## 0.9.0 — the five that were 0.8.0's, built under 0.8.0's machines

These sat in 0.8.0 until 2026-09-04 and moved down one, for the reason the
section above states rather than because the list was long. Not ordered; #98
rides whichever branch is open.

- [ ] #97 — the three pin levers left after #117 took the fourth. Each changes pins that already exist, so each needs a question batch.
- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows.
- [ ] #111 — `git()` reads every failure as `""`, and in `seal import` that empty string switches off the refusal that keeps another project's records out.
- [ ] #134 — the update notice names a restart and never the reload this repository measured and wrote down. One notice and one skill.
- [ ] #98 — three sentences say `-z` is what turns git's path quoting off, and the instruction they give is right while the reason they give for it is false. One line, and it rides whichever branch of this release is open.
- [ ] **#149 — a record says what a segment COST and not what its output cost the next reader.** #137's second half, split off when its first half shipped. Five candidate signals and no evidence which of them survive contact: surviving mutations, defects the next round found inside this segment's output, `New units` depth, fix passes needed, and divergences from the plan. It waits for the accumulation the `Ran by` row now makes possible — an outcome column chosen before there are attributed readings to choose it against is the mistake #110's *Not this* refuses on the review side.

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
2. spec · plan (framer, once #84 exists; the session until then) → smith → warden rounds → sealer → pull request.
3. The pull request body carries `Closes #N`; the release workflow closes the ticket when the release reaches `main`.

