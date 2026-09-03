# Release flow

A checklist for the tickets in flight. Tick a box when the ticket's pull
request has merged into its release branch. **A shipped version's section is
deleted, not kept** — the design record, the CHANGELOG and the tickets are the
durable copies, and a list long enough to scroll costs the reading it exists
to save. Delete the file only when nothing is scheduled.

Each release branch is cut from `main`; each ticket is a branch cut from the
release branch and squashed back; the release branch merges into `main` as a
merge commit (`docs/branch-and-release.md`).

## 0.6.0 — the flow measures itself, and stops when it should

In this order. Each one stands on the one before it, and taking them the other
way round means undoing work.

- [ ] **#107 — the rules that go to every agent move out of the prompt and into a file.** First, because everything after it is a comparison: while half of each spawn prompt is retyped from memory, two segments differ by what the orchestrator happened to recall and the numbers cannot be read against each other. It is also the file #30 and #84 need before either adds an agent.
- [ ] **#109 — measuring a segment and recording what it says becomes automatic.** Second, so #110 and #117 are what tries the machinery, rather than 0.7.0 finding out whether it works. Its third part — the release closes this version's log and opens the next — is what makes 0.7.0's measurement issue exist without anybody opening it. First act: #89 carries no version in its title, and #109 requires exactly one open versioned issue at a time.
- [ ] **#110 + #117 — when a review run stops, and how deep a fix may pin.** One branch, because apart they undo each other. #110 gives the cap the floor it never had; #117 bounds what a single fix pass may create. The late rounds #110 removes are the rounds where the pins get read, so the floor without the bound cuts the eyes and leaves the generation.
- [ ] #98 — three sentences say `-z` is what turns git's path quoting off. One line, and it rides whichever branch is open.
- [ ] #89 — the running log. It is read rather than done, and it closes at the release.

## 0.7.0 — the first version measured under the machinery above

Not ordered yet. The 0.6.0 log is what orders them.

- [ ] #97 — the three pin levers left after #117 took the fourth: what is worth pinning at all, whether a pin must derive rather than duplicate, and whether a pin waits for a ticket of its own. Each changes pins that already exist, so each needs a question batch.
- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows.
- [ ] #111 — `git()` reads every failure as `""`, and in `seal import` that empty string switches off the refusal that keeps another project's records out.

## Later — not scheduled

- [ ] #30 and #84 — the agent set: `sealer` owns the one full-suite run, `framer` writes the frame the smith fills. Both want #107's file first.
- [ ] #83 `settle` · #85 the orphan branch as the ledger's home · #101 the export's size — the root's later steps.
- [ ] #88 — the routing question asks three boxes and has no way to say "all three".

## While the flow runs

After every smith or warden segment, measure its transcript and add the
numbers and what they say to the version's measurement issue.

**#109 deletes this section.** Moving that instruction into
`skills/verify/SKILL.md` is #109's first part, and an instruction that lives
only where somebody has to remember to read it is the defect #109 names.

## Order inside a ticket

1. Branch from the release branch; write `routing.md` before the first edit.
2. spec · plan (framer, once #84 exists; the session until then) → smith → warden rounds → sealer → pull request.
3. The pull request body carries `Closes #N`; the release workflow closes the ticket when the release reaches `main`.
