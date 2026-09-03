# Release flow

A checklist for the tickets in flight. Tick a box when the ticket's pull
request has merged into its release branch. **A shipped version's section is
deleted, not kept** — the design record, the CHANGELOG and the tickets are the
durable copies, and a list long enough to scroll costs the reading it exists
to save. Delete the file only when nothing is scheduled.

Each release branch is cut from `main`; each ticket is a branch cut from the
release branch and squashed back; the release branch merges into `main` as a
merge commit (`docs/branch-and-release.md`).

## 0.6.0 — the agent contract, and nothing else

**One work item, and the reason is that a rule in this tree binds no session.**
What is in force is the installed plugin, not this repository: measured
2026-09-03, what loads is the version cache under `~/.claude/plugins/cache/`, copied
from the marketplace clone at the `v0.5.0` tag, while this tree is on a 0.6.0
branch, and no `.claude/` here overrides it. So the contract changes
nothing a session does until `v0.6.0` is tagged and the plugin updated.
Shipping it by itself is what makes everything after it built **under** the
contract rather than beside it.

- [ ] **#107 — the rules that go to every agent move out of the prompt and into the plugin.** Framed at `c48bf65`; six phases, one smith spawn each. Its review chain is the last one this repository runs under hand-typed spawn prompts, so its segments are the before-figure everything in 0.7.0 is measured against.
- [ ] #98 — three sentences say `-z` is what turns git's path quoting off. One line, and it rides #107's branch.
- [ ] release: gather the changelog, fold the ledger, move `plugin.json`, merge to `main`, tag `v0.6.0` — **and update the installed plugin, then `/reload-plugins`** — that pair is what actually puts the contract in force. Preloaded skill bodies are read at session start and at `/reload-plugins`, never at spawn.

## 0.7.0 — the first version built under the contract

In this order. Each one stands on the one before it.

- [ ] **#109 — measuring a segment and recording what it says becomes automatic.** First, so the rest of the version is what tries it rather than 0.8.0 finding out. Its third part — the release closes this version's log and opens the next — is what makes 0.8.0's measurement issue exist without anybody opening it.
- [ ] **#119 — a segment's record says what it was asked, and under which version of the rules it ran.** After #109, because a record and its measurement are the same handoff. Two items were added to it in conversation and are marked in the issue as needing a second look before they are built.
- [ ] **#110 + #117 — when a review run stops, and how deep a fix may pin.** One branch, because apart they undo each other: #110 removes the late rounds, and the late rounds are where the previous round's pins get read.
- [ ] #97 — the three pin levers left after #117 took the fourth. Each changes pins that already exist, so each needs a question batch.
- [ ] #103 — the two defect shapes only Windows has caught are made visible without Windows.
- [ ] #111 — `git()` reads every failure as `""`, and in `seal import` that empty string switches off the refusal that keeps another project's records out.
- [ ] #89 — the log, until #109 replaces it with a versioned one.

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
