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

## 0.9.0 — a record is written by a machine and trusted like one

Five tickets on one surface, `round_record.py` and `chain_check.py`, and four
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
- [x] #98 — three sentences say `-z` is what turns git's path quoting off, and the instruction they give is right while the reason they give for it is false. One line, and it rides whichever branch of this release is open.

## 0.9.1 — what an installed repository hits

Four work items. Three of them are met by somebody who installed the plugin and
never reads this tracker, and **#111 is the sharpest thing on the whole 0.9.x
list**: a git call that fails reads as a repository with no remote, and that
reading switches off the refusal keeping another project's records out.

The fourth is the odd one and it is here on the owner's call: `Contract
changes` answers wrongly in two ways, and the two are one branch on one
derivation. It is not user-facing, and splitting the pair across two releases
to make the theme clean would put one branch in two of them.

- [ ] #111 — `git()` reads every failure as `""`, and in `seal import` that empty string switches off the refusal that keeps another project's records out. Four callers were left after #104 taught two of them to check the return code.
- [ ] #151 — the preset tells a session to create the root, and the question that was supposed to come first lives in a skill it never loads. Reported from a repository's first work item: `seal/` appeared and nobody was asked about shared or local mode.
- [ ] #134 — the update notice names a restart and never the reload this repository measured and wrote down. One notice and one skill.
- [ ] **[#211 · #194] — one branch, `round_record.py`'s derivation rows.** `Contract changes` reads `no call site found` for a pytest test function, and it compares arities, so a unit returning a new *meaning* reads as `none`. #194 moved here from 0.9.0 on 2026-09-07: a second measured instance arrived during #187's chain and it is a shape the ticket's proposed literal-set comparison does not catch — `is_a_record_of_a_moment` changed which inputs map to which of the two values it already returned, with signature, arity, return type and returnable set all unchanged.

## 0.9.2 — what the chain found about itself, in the units it found them in

Three work items, and six of the ticket numbers below belong to two of them.
A capped run turns every finding still open into an issue, which is right — and
it means one branch's leftovers arrive as four ticket numbers on one file. They
are grouped here as the branches they will actually be.

- [ ] **[#203 · #204 · #205 · #206] — one branch, `tests/test_release_hygiene.py`.** #179's run hit the reopening bound with these open: nothing observes what the version check prints, an uppercase `V0.9.0` is invisible, two records describe an order bug that never happened, and the tracker document states the check wider than it is.
- [ ] **[#209 · #210] — one branch, the pre-merge guard.** Its reader has a failure arm no case watches, and its parametrized case is a class over two literals rather than over the reader's passes.
- [ ] #167 — a closing keyword claims one issue, and a body naming two in one sentence loses the second silently.

## 0.9.3 — the enumeration was done by reading

Three work items on one method rather than one file, and the method is what
observation 6 on #51 found eight times without a single instance caught by
reading. #170's round 2 is the positive case: a fix pass re-enumerated its
class by construction and found a second crash site where the finding named
one.

0.9.0's own two chains are the second measurement and they are larger: nine
instances on one branch and seven on the next, every one found by mutating code
rather than by reading it, and each one inside the fix for the one before.

- [ ] #182 — the hider guard's enumeration names three copies where the property is every copy out of `raw`. `spec.md` and `plan.md` for it were drafted during 0.8.3 and are in that run's scratch, not in the tree.
- [ ] #192 — a funnel answers for the values that enter, and nothing answers for what two of them make. #175's round 3, measured at the base as well as on the branch.
- [ ] #180 — three written rules were each re-broken in one run; written down and arriving at the act are different states. Five instances now, and the fifth is the reopening bound itself — a rule the acting session had read, restated as the cap, and propagated five times.

## 0.9.4 — the instrument, before anything reads it

Three work items, and the ordering is the whole point: **#145 and #149 are
answered off a table that is wrong today.** Both meter defects were found on
2026-09-07 by taking this release line's own segment readings, and every
per-segment reading this repository has published carries them.

- [ ] #200 — the meter's `test` family names five runners and not this repository's, so fourteen `./bin/test` runs read as `other` and the one call it charged to `test` was a file write containing the word.
- [ ] #202 — a streamed message is counted at its first partial row, so a round that wrote a full report reads as 62 output tokens. The error is not a scale factor: 3.2x on one segment and 334x on another, the same day, with nothing in the printed report saying which.
- [ ] #193 — a third the file could not compute is charged 0, and the context line takes that 0 for a baseline. Carries a verified patch and a case seen red, plus two smaller ones as a comment.

## 0.9.5 — what the readings answer, and what a green gate means

Four work items. The first two are the questions #51 has been holding open for
a measurement it can trust; the last two are the other half of the same
sentence — a gate finishing green where green does not mean the code is right.

- [ ] #145 — the orchestrator is the most expensive segment in a chain and the only one measured by the whole session, so #51's observation 1 has bands for three segment kinds and none for it. #170's token line is what makes it answerable — after 0.9.4.
- [ ] #149 — a record says what a segment cost and not what its output cost the next reader. #137's second half. Five candidate signals and no evidence which of them survive contact: surviving mutations, defects the next round found inside this segment's output, `New units` depth, fix passes needed, and divergences from the plan.
- [ ] #160 — four export cases fail on macOS and pass in CI, so a broad run cannot be read as a verdict. The cause is settled and #127 is folded in here: the cases build their expected zip name from the local date and `export()` writes it in UTC. What is left is the owner's call on which side moves.
- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows.
- [ ] #198 — a release closes its flow-measurement log with nothing written in it, and nothing notices. It sits with these because #145 and #149 are the two tickets that eat the data it protects, and this is the release they land in.

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

