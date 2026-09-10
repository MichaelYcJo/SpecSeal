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

## 0.11.0 — the framer

**Moved out of 0.10.0 on 2026-09-10, on the owner's call, once #30 had merged
and #120 was the release's last item.** A release is sized in work items and
three is the size; 0.10.0's two were large — 43 files and 48 files — and this
one adds a fifth agent, a channel a phase hands the next one, and a `Planning`
row in `routing.md`. It earns its own release rather than a fourth slot.

**What the move costs is that the contract is settled at four agents and not
five**, and #120 is where the grounds are — its `questions.md` Q2, and the
section that stated them here went with the shipped release. What it buys is that the
framer arrives against a contract whose §6 already reads *what you write is
named in your own definition* — so the agent that writes three durable records
meets a rule that permits them, instead of arriving as the fourth exception to
a sentence that forbids them.

- [ ] **#84 — `framer` writes the frame the smith fills**, so the writer of the contract is not its executor. Needs #121's phase channel — a framer that draws the plan and never authors the half of a phase prompt only building can teach is a partial answer.

**And the owner's decision of 2026-09-10 goes with it**: `routing.md` gains a
`Planning` row, `framer` · `the session`, the shape the `Implementation` row
already has. #88 is the near neighbour to read first — it asks how the routing
question says *all of them* — because a fourth checkbox and a preset over the
three are answers to the same question.

## 0.11.1 — the three 0.9.5 planned and did not reach

Moved here on 2026-09-10, when 0.9.5 was cut at five: eight was over the size,
the five that shipped were the ones the release's own run produced, and these
three were the ones it was planned around.

**Renumbered twice, and the second time was the order correcting the number.**
It was 0.9.6 until 2026-09-10, when the agent set took 0.10.0 and this became
0.10.1 — the owner's call, because the agent set was the main line of the work
rather than a detour from it. It became **0.11.1** on 2026-09-11, when 0.10.0
shipped and the framer's release was cut: this section sits BELOW 0.11.0 in
the order these ship, and a 0.10.1 released after a 0.11.0 is a number going
backwards. The content did not move; only the number it will carry did. What the order costs is written down rather than
left to be discovered: #103 makes the two defect shapes only Windows catches
visible without Windows, and 0.10.0 widens exactly that surface — five agent
definitions and new record paths are all path-spelling candidates — so 0.10.0
will learn about them at its own pull request. **It did, three times, and the
local gate found none of them**: a path helper that raises across drives, two
`bin/` wrappers a shebang makes unrunnable there, and a `skipif` standing in
front of a third. The row below is what stops the fourth release paying it. #198 protects the measurement
of a cycle, and the cycle that changes the agent set from three to five is the
one with most to measure.

**#149 is last here too, and for the reason it was last there.** It waits on
attributed readings, 0.9.5 is the release that produces them, and this is the
first release that can read them rather than the first that could have.

- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows. **A third arrived in 0.9.0**: a coordinate the records arm built printed with the platform separator, and the Windows leg was red on it from the commit that added the arm through three review rounds and two broad gates, all of which ran on macOS where the fix is a no-op.
- [ ] #198 — a release closes its flow-measurement log with nothing written in it, and nothing notices. It sits with these because #145 and #149 are the two tickets that eat the data it protects, and this is the release they land in.
- [ ] #330 — every rule an agent follows arrives by mechanism, and every rule the orchestrator follows arrives as a sentence it has to remember. The repository has already run the experiment on itself: three acts that were sentences were given a command and stopped being forgotten, and the three still written as sentences each have a measured miss — the broad gate, the flow-log posting, and the routing question, which was broken by a session that had the one-batch rule loaded. Opened during 0.10.0's first two work items, and it sits here because #30 closes the first instance and is the template: what is left is whether the shape generalises to acts that need a person, which a command can print a question for but cannot ask.
- [ ] #331 — every ambiguous word this repository has fixed was found by a person reading, one at a time. `tests/test_one_word_one_meaning.py` holds five of them, and `seal` is the sixth: it named the warden's review mark, the sealer's stamp and the smith's proof block at once, and it turned up in conversation rather than through anything in the tree. Nothing enumerates the seventh. The census in the ticket reads 968 twelve-word runs shared across two or more of `skills/`, `agents/` and `docs/` — an upper bound and not a defect count, because this repository's own rule has one carrier state a rule and every other quote enough of it to name the owner, so a link is right and a restatement is the defect, and the sweep has to tell them apart. **It sits here rather than in 0.10.0 because the census has to be taken after the agent set settles**: a sweep run while two of the five definitions do not exist and #120 is about to re-home a third of the contract decides every word twice. The fifth agent is also what made the sixth word visible — `seal` read one way while the warden was the only agent keeping one.
- [ ] #333 — a depth-2 refusal names the finding and the unit by file alone. It stopped the right commit for the wrong reasons: the message sent a reader to a unit it must keep. Opened by #30's round-2 fix pass, which measured the cause in `depth_two`'s own walk.
- [ ] #334 — the gate reads a literal another package prints, and changing that print turns nothing red. Measured at 130 passed with the two ends disagreeing. Nothing is wrong today; what is missing is the thing that would notice.
- [ ] #335 — `seal` accepts a `round-N` checker whose shape is right and whose position on a last record makes it false, and writes the cell before the chain check refuses it. The three of these are what 0.10.0's own review chain opened, which is the rate this list should be read at.
- [ ] #339 — the guard that makes a round record's terminal-line join safe passes the prose it was written to stop and truncates a continuation beginning with an issue number, which this repository writes at the head of a line constantly. **A regression 0.10.0 shipped**, in a parser that release changed twice in opposite directions, and the corrected pattern was already in the tree at `.github/scripts/issue_claims_check.py:116` with a comment naming the trap. It sits here rather than in the list below because it is this release's own regression and because #335 is already here and is the same module. **#340 travels with it** — the protocol that defines a conforming tool never learned that a wrapped terminal line is one value, so a second implementation truncates where this one no longer does.
- [ ] #149 — a record says what a segment cost and not what its output cost the next reader. #137's second half. Five candidate signals and no evidence which of them survive contact: surviving mutations, defects the next round found inside this segment's output, `New units` depth, fix passes needed, and divergences from the plan.

## Later — not scheduled

- [ ] #83 `settle` · #85 the orphan branch as the ledger's home · #101 the export's size — the root's later steps.
- [ ] #88 — the routing question asks three boxes and has no way to say "all three".
- [ ] #135 — `user-invocable: false` sits in the copy that loads and the skill is listed as a command anyway. One measurement decides whether it has a fix or only a correction to the record.
- [ ] #264 — three review rounds each found an arithmetic error inside the previous round's fix, and the cause was two unlabelled denominators. Opened by 0.9.2's #209 · #210 run; all five findings are corrected there. It carries no release because its own body leaves the shape open — whether a declared counting basis is worth building, or only the narrower refusal of a Notes cell whose subtraction does not reconcile.
- [ ] #337 — the runner will not install `xdist` because it does not pass `-n auto`, and does not pass `-n auto` because `xdist` is not installed. Opened from use during 0.10.0.
- [ ] #341 · #342 · #344 — three ways a round record and the tree disagree, all opened by 0.10.0's own chain: the reviewer is told to put an earlier round's closures in a table the generator cannot accept and two work items have paid a hand-edit for it; `inherited_rows` is never revisited, so two records committed together state the same eight findings `open` and `fixed`; and five places where a record says something the tree does not, with nothing that reads a record against the tree the way `evidence-check` reads the ledger.
- [ ] #343 · #345 — **#330's near neighbours, and whoever takes #330 should read them first.** One is that two review rounds spawned agents against §6 and nothing noticed either time, in the work item that rewrote §6 — the rule arrived by mechanism and the act went the other way, so the missing half is not delivery. The other is that the record-before-the-fix sequence is an orchestrator's habit, performed correctly twice and wrongly once in one session, where the check that knows the sequence only speaks at the pull request.
- [ ] #97 — the three pin levers left after #117 took the fourth. Each changes pins that already exist, so each needs a question batch, which is why it carries no release rather than a late one.

## Order inside a ticket

1. Branch from the release branch; write `routing.md` before the first edit.
2. spec · plan (framer, once #84 exists; the session until then) → smith → the draft pull request opens (`skills/code-review/orchestration.md` §*Orchestrator: the pull request opens before round 1, and a phase is re-run* owns when) → warden rounds → sealer → the pull request is marked ready.
3. The pull request body carries `Closes #N`; the release workflow closes the ticket when the release reaches `main`.

