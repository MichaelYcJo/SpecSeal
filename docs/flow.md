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

## 0.9.x — four releases, and what decides which one a ticket sits in

Nineteen tickets, split on 2026-09-07 by the surface a branch has to open and
by what one release makes possible for the next. It is the list the single
0.9.0 section held, plus #198 which the split itself opened, minus #97 which
moved to the unscheduled section for the reason given there.

Two of the positions are forced rather than chosen. #179 has to be in 0.9.0,
because it goes red on the commit that raises the version to 0.9.0 and nowhere
earlier. #149 has to be last, because its own body says it waits for
attributed readings that do not exist yet.

The rest is ordered so that each release is cheaper for the one after it.
0.9.0 makes the round record trustworthy, and every release after it writes
round records. 0.9.2 replaces enumeration by reading with enumeration by
construction, which is the method 0.9.3's rounds then use on the meter.

The split is also a size decision. 0.8.3 shipped three of eight and carrying
five forward was the call rather than the failure, so these are sized at four
or five rather than at nineteen.

## 0.9.0 — a record is written by a machine and trusted like one

Six tickets on one surface, `round_record.py` and `chain_check.py`, and four
of them are what 0.8.3's own rounds earned. #207 is the sixth and this
release's own: it was earned by #179's chain overrunning the reopening bound,
and its repair sits in the same file as the rest. They are the same sentence in
different clothes: nothing reads what the record says. #179 is that sentence
about a document rather than a record, which is why it sits with them and not
only because the version forces the date.

- [x] #179 — a loaded file naming a real version is a timer. `docs/issues-and-milestones.md` named `0.9.0` in a sentence about milestones, and the check refused the running version only. Green today, red on this release's own preparation commit — after the broad gate has already run. Closed by widening it to every version at or above the running one, as `test_no_loaded_file_names_a_version_at_or_above_the_running_one`.
- [x] #187 — the round record carries the reviewer's tables and drops the paste-ready fix the findings format requires. Measured: a fix pass re-derived a verified artefact from scratch, and its first re-derivation was wrong.
- [x] #189 — a bare pipe inside a Verdicts cell truncates the row, and nothing sees it. Two paste-ready fixtures were invisible in a rendered record; a later fix pass then hit it again after being warned. Compounds with #187, which makes that cell the only durable home a paste-ready fix has.
- [ ] #207 — the record knows the bound the next round is under and does not say it, so a session carries the cap instead. #179's own chain ran three rounds past the reopening bound; the gate caught it at the broad run, after 37.9 minutes and 180 calls that were then reverted.
- [ ] #190 — a record states a figure or a stamp the next commit moves, and no check reads it. Closed three times on one work item by enumerating carriers, and back each time.
- [ ] #194 — `Contract changes` compares arities, so a unit returning a new *meaning* reads as `none`. That row exists for #57's largest regression class and read `none` on a live instance of it.
- [x] #98 — three sentences say `-z` is what turns git's path quoting off, and the instruction they give is right while the reason they give for it is false. One line, and it rides whichever branch of this release is open.

## 0.9.1 — what a repository using SpecSeal actually hits

Four of these are met by someone who installed the plugin and never reads this
tracker, and #111 is the sharpest thing on the whole list: a git call that
fails reads as a repository with no remote, and that reading switches off a
refusal. The fifth is this repository meeting the same class about itself.

- [ ] #203 — nothing observes the refused lines, the running version or the reason in what the version check prints; the ledger row recorded a narrower residual than the measurements support. Three passes each enumerated the parts and each stopped one short.
- [ ] #204 — an uppercase `V0.9.0` is this plugin's version and the check cannot see it, and the guard beside it has no written argument.
- [ ] #205 — two records say a narrower prefix written later stopped working, and it never did in either implementation.
- [ ] #206 — the tracker document says the version check refuses a version whether it has shipped, where it refuses at or above the running one.
- [ ] #111 — `git()` reads every failure as `""`, and in `seal import` that empty string switches off the refusal that keeps another project's records out. Four callers were left after #104 taught two of them to check the return code.
- [ ] #151 — the preset tells a session to create the root, and the question that was supposed to come first lives in a skill it never loads. Reported from a repository's first work item: `seal/` appeared and nobody was asked about shared or local mode.
- [ ] #134 — the update notice names a restart and never the reload this repository measured and wrote down. One notice and one skill.
- [ ] #167 — a closing keyword claims one issue, and a body naming two in one sentence loses the second silently.
- [ ] #198 — a release closes its flow-measurement log with nothing written in it, and nothing notices. 0.8.3 ran three work items and twelve rounds and left its cycle log empty, which is the same shape as #150: a mechanism built, used once, then not, with nothing in the way to say so. It lands here rather than in 0.9.3 because #145 and #149 are the two tickets that eat the data it protects.

## 0.9.2 — the enumeration was done by reading

Three tickets on one method rather than one file, and the method is what
observation 6 on #51 found eight times without a single instance caught by
reading. #170's round 2 is the positive case: a fix pass re-enumerated its
class by construction and found a second crash site where the finding named
one.

Standing before 0.9.3 is deliberate. The rounds that answer the meter are the
rounds most likely to enumerate a class and miss a member of it.

- [ ] #182 — the hider guard's enumeration names three copies where the property is every copy out of `raw`. `spec.md` and `plan.md` for it were drafted during 0.8.3 and are in that run's scratch, not in the tree.
- [ ] #192 — a funnel answers for the values that enter, and nothing answers for what two of them make. #175's round 3, measured at the base as well as on the branch.
- [ ] #180 — three written rules were each re-broken in one run; written down and arriving at the act are different states.

## 0.9.3 — a run finished, and what it says cannot be taken for a verdict

Two halves of one question. The meter measures a segment and charges 0 for
what it could not compute, and the gates finish green where green does not
mean the code is right. #149 is here because this is the release by which the
`Ran by` rows have accumulated enough for it to choose an outcome column
against readings rather than against a guess.

- [ ] #200 — the meter's `test` family names five runners and not this repository's, so fourteen `./bin/test` runs read as `other` and the one call it charged to `test` was a file write containing the word. Opened by 0.9.0's own first segment reading. It stands before the two below it because both are answered off that table.
- [ ] #145 — the orchestrator is the most expensive segment in a chain and the only one measured by the whole session, so #51's observation 1 has bands for three segment kinds and none for it. #170's token line is what makes it answerable.
- [ ] #193 — a third the file could not compute is charged 0, and the context line takes that 0 for a baseline. Carries a verified patch and a case seen red, plus two smaller ones as a comment.
- [ ] #149 — a record says what a segment cost and not what its output cost the next reader. #137's second half, split off when its first half shipped. Five candidate signals and no evidence which of them survive contact: surviving mutations, defects the next round found inside this segment's output, `New units` depth, fix passes needed, and divergences from the plan.
- [ ] #160 — four export cases fail on macOS and pass in CI, so a broad run cannot be read as a verdict. The cause is settled and #127 is folded in here: the cases build their expected zip name from the local date and `export()` writes it in UTC. What is left is the owner's call on which side moves.
- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows.

## 0.10.0 — the agent set

In this order, and the third is not optional.

- [ ] **#30 — `sealer` owns the one full-suite run.** Today the smith and the warden are both forbidden it and nobody is assigned it.
- [ ] **#84 — `framer` writes the frame the smith fills**, so the writer of the contract is not its executor. Needs #121's phase channel — a framer that draws the plan and never authors the half of a phase prompt only building can teach is a partial answer.
- [ ] **#120 — the agent contract is settled against five agents rather than three, and it lands before either of the two above is released.** Three of its sixteen sections apply to all five; §2 forbids the broad gate the sealer exists to run, and §6 forbids the durable record the framer and the sealer both write. A release that ships five agents under a contract contradicting two of them is the release that teaches readers the contract has exceptions.

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
- [ ] #97 — the three pin levers left after #117 took the fourth. Each changes pins that already exist, so each needs a question batch, which is why it carries no release rather than a late one.

## Order inside a ticket

1. Branch from the release branch; write `routing.md` before the first edit.
2. spec · plan (framer, once #84 exists; the session until then) → smith → the draft pull request opens (`skills/code-review/SKILL.md` §*Orchestrator: the pull request opens before round 1, and a phase is re-run* owns when) → warden rounds → sealer → the pull request is marked ready.
3. The pull request body carries `Closes #N`; the release workflow closes the ticket when the release reaches `main`.

