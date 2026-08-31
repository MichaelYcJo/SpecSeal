# Review Handoff Protocol — draft 0.4

A file convention for handing review work between agent sessions — across
time, machines, and tools. Tool-agnostic on purpose: nothing here requires
Claude Code or this plugin; any coding agent that can read and write files in
a git repo can conform.

## Problem

Review findings normally live in PR comments, written for humans. The next
agent session — a re-review round, or the session fixing the findings —
cannot reliably recover from comments: which axes were already judged, what
was empirically probed, which regression tests were prescribed and where.
Measured consequence: round *n* of a review costs *n* full walks of the same
code, and prescribed tests silently drop when only inline comments get acted
on.

## Layout

The records live **in the directory that holds the work item** — beside
whatever the project keeps there already, such as a specification or a plan.
One work item, one directory; parallel reviews never share a file.

```
<work-item-directory>/
├── rounds/
│   ├── round-1.md
│   └── round-N.md
├── tests-todo.md
└── evidence-todo.md
```

In this plugin's implementation that directory is `specs/<work-item-id>/`.
**That path is the implementation, not the protocol.** A project adopting this
convention puts the files wherever its work items already live.

`round-N` is the only member of this set that is plural and unbounded, so it
gets a directory and the two todo files do not. Six records beside six other
files was the worst case measured in the reference implementation, and a
reader scanning that directory could not tell at a glance which member grows.

The directory is **committed** — ignored files do not follow worktrees or
other machines — and it **outlives the merge**. It is closed, not deleted
(below).

### Why the work item, and not the change request

Draft 0.2 keyed the directory to a pull request: `PR-<id>/`, where `<id>` was
the PR number, MR id, or change-list id.

That key does not exist yet at the moment the records are written. A review
round happens **before** the pull request opens — often several of them — so
conformance rule 1, *reads before reviewing*, named a directory that could not
have been created. It was not a rule anyone was failing to follow; it was a
rule no correct session could satisfy.

Measured in the reference implementation: `.specseal/handoff/PR-<n>/` had
**never been created**, across every branch that ran review rounds. Three
unmerged branches each ran rounds, each produced findings, and none left a
committed record of what was open. The verdicts existed only in agent reports,
which end with the session.

A work item, by contrast, has a directory from its first commit. The pull
request number is still recorded — as a **field** inside `round-N.md`, filled
in when the PR opens. It stopped being the key, which is what made it
unusable.

**The cost of the move.** A project adopting this protocol now has to have
somewhere its work items live. Draft 0.2 needed only a PR number, which every
code host supplies. This is a real dependency and it is the price of records
that can be written before the change request exists.

### Why the records moved a second time

Draft 0.3 put them flat in the work item's directory. That was right about
which directory and wrong about the depth, and the cost showed up as soon as a
work item ran six rounds: twelve files in one place, six of them the SDD set
and six of them records, with nothing in the layout saying which half grows.

**No fallback ships with the move.** A reader that finds `rounds/` missing
does not fall back to the flat location — it says which file is in the wrong
place and where it goes, and stops. Two alternatives were rejected before
this one. Reading both locations permanently puts two places to look in the
one module every gate imports, forever. Reading both with an expiry ships a
date that nothing enforces, which is a comment.

What that trade costs is stated rather than left to be found: a project on
draft 0.3 that adopts 0.4 without moving its records gets a failure where it
used to get a pass. That is only bearable because the failure names the file
and the destination, so **a conforming tool's message for a record at the old
location must carry both.** Degraded to a generic "no round record", it
reports a review that never happened, which is false and unactionable at
once — and the trade stops being sound.

### Why the directory is not deleted

Draft 0.1 deleted it in a cleanup commit before the merge. Deletion was doing
one job worth keeping — it was the deadline that forced the draining — and
one that does not survive inspection: a round record carries the SHA it
reviewed, so unlike a task list it never asserts a present state and does not
go stale. What deletion cost was worse than what it bought. Items were pushed
out to durable homes because the directory was about to disappear, and those
homes sit outside what a reviewer reads, so a finding deferred in round 1 left
the inheritance range and round 2 raised it again.

## Files

### round-N.md — what this round did

| Field | Required | Content |
|---|---|---|
| Target SHA | yes | commit(s) the round actually reviewed — branches move between rounds; record both if HEAD moved mid-review. **Never rewritten after a squash** — see below |
| Pass | yes | a checkbox — `- [ ] Pass` or `- [x] Pass`. Checked means no finding in this round's verdict table is still open. See below |
| PR | when one exists | the change request this work went to. A field, not the key: it does not exist while the rounds that fill this file are running |
| Verdict table | yes | per finding: location, verdict, grounds |
| Executed probes | yes (may be "none") | what was RUN, with results — distinguished from what was read |
| Inherited axes | for N>1 | axes carried from earlier rounds, each with the coordinates it was judged at. The coordinates carry; the verdicts do not — a round opens what they name and reaches its own (Conformance 1) |
| Deferred | yes (may be "none") | findings this round neither fixed nor answered, each with the durable home it went to. The reviewer already opens this file; a row here is what keeps a deferral inside the inheritance range instead of being raised again next round |
| Broad gate | yes | whether the one full-suite run has happened: `not yet`, or the SHA it ran at and the base it was compared against. A session joining at round 3 watched none of rounds 1–2, and the code does not record which commands were run against it — without this field it either repeats a run that is already sealed or ships assuming someone else made it |

#### Target SHA after a squash

A feature branch squashes into the release branch
(`docs/branch-and-release.md`), and the
commits a round reviewed are exactly what a squash discards. So the field's
answer stops resolving in the branch that carries the record.

**It is not rewritten to the squash commit.** A rider stamp answers *"which
published commit was this checked against"*, and any reachable commit is a
truthful answer to that — which is why round 4 of the work item that moved
these files rewrote the stamps and could not rewrite this. `Target SHA`
answers *"which commit did this round actually review"*, and the squash commit
did not exist when the round ran.

What holds instead is that the commit is still on the branch the work item
declared. `chain_check.py` reads `routing.md`'s `| Branch |` row and accepts an
ancestor of HEAD **or** of that branch, and it makes no claim at all about a
record the pull request does not touch. Two consequences, both load-bearing:

- **Keep the feature branch until its release reaches `main`.** Deleting it
  earlier turns that one pull request red. The window is a single pull request
  — the release one: in the feature → release pull request the target is an
  ancestor of HEAD by construction, and once the release merges, the next
  release branch is cut from a `main` that already holds the record. Inside
  that one window, the branch is evidence.
- A record already merged is history. No claim is made about where its
  commits are — everything else is still read, including that the `Target SHA`
  row is present and that `Pass` is consistent with its own table. The review
  it records was enforced at the pull request that added it.

#### The Pass checkbox — what it is for

"Was this reviewed" and "did it pass" are different questions, and only the
first was answerable from the tree. Someone holding three unmerged branches
could not tell which of them was safe to merge without opening every round
record and reading prose.

A checkbox answers it in one grep across every work item, and — unlike prose —
a check can enforce it.

**It is the last round's checkbox that speaks for the whole review.** Earlier
verdicts are not archived; every one of them needs an answer in the round that
follows, so an open 🔴 from round 1 cannot be absent from round 3's table. One
file is the state.

**A checked Pass beside an unanswered blocking finding is wrong**, and because
both live in the same file a check can say so. The reference implementation
fails its pull request for exactly that combination, and fails the same way for
a verdict table it cannot read: a tolerant reader reports no open findings
there, and no open findings is indistinguishable from all of them closed.

### tests-todo.md — regression tests prescribed, not written

One row per test: what it asserts · **destination file** · grounds · status.
The reviewer prescribes; the implementer plants. Prescriptions embedded in
fix-suggestion snippets get lost (measured) — this file is the contract.

### evidence-todo.md — verified facts awaiting the ledger

One row per fact: the fact · destination ledger row · status. Reviewers do
not write the ledger directly: parallel writers clobber each other, and
worker findings are pre-verification.

## Conformance

A tool claiming to support this protocol:

1. **Reads before reviewing** — an existing work-item directory is prior
   state: a judged axis hands over its coordinates, not its verdict — open
   what it names and reach this round's own. Executed probes are re-checked,
   not re-run. This is the rule draft 0.2 made unsatisfiable by keying the
   directory to an identifier that does not exist yet.
2. **Writes after posting** — the session that posted a review writes
   round-N and the two todo files immediately; it is the only moment the
   verdicts and probe results still exist anywhere.
3. **Closes before merging** — every unresolved row moves to a durable home
   (the repo's evidence ledger, follow-up list, or open-questions section),
   and the directory records what went where, or `nothing to drain`. The
   directory then stays. Merging without closing leaves prescribed tests
   unplanted and facts unmerged, which is the failure this protocol exists to
   prevent; the closing note is what makes that visible in the diff instead of
   only in someone's memory.

## Non-goals

- Not a memory system: no automatic capture, no embeddings, no store beyond
  the repo. Structured handoff for one workflow (review), nothing broader.
- Not a comment replacement: human-facing findings still go to the code
  host; this directory is for the next session, and the two audiences never
  share a file.

## Status

Draft 0.4, extracted from the convention this plugin's `code-review` and
`implement` skills already operate (they are its reference implementation).
Field names and layout may change; the three conformance rules are stable in
shape. 0.2 changed the third from *delete after draining* to *close and keep*.
0.3 moved the directory off the change-request number and onto the work item,
which is what made rule 1 satisfiable at all, and added the `Pass` field so
that "was it reviewed" and "did it pass" stop being the same question. 0.4
gives the records their own `rounds/` subdirectory and requires a conforming
tool to name a record left at the old location rather than passing over it.

0.3 also states the path as this implementation's choice rather than as the
protocol. Draft 0.2 claimed to be tool-agnostic while naming a directory
inside one plugin's own state folder — a claim its own location contradicted.
Portability comes from the file shapes, which read the same to any agent
wherever they sit.
