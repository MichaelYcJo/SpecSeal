# Review Handoff Protocol — draft 0.6

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
| Fixes checked by | yes | who opened the fixes that closed this round's findings: a later round, `no fixes to check`, or `nobody` with the reason. `Pass` answers whether the findings were closed; this answers whether the closing was read by anyone. See below |
| Needs a fix | yes, from the round that wrote it | whether this round opened anything that needs one — the reviewer's own answer, copied rather than re-derived from the verdict table. It is the run's terminal condition where a run ends at a verifying round, and a finding the implementer answers with grounds does not make it `yes`. See below |
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

#### The Fixes checked by field — who opened the closing

A round's findings are closed after the round ends, by whoever fixes them.
Every earlier round's fixes are therefore opened by the round that follows,
because each of that round's verdicts needs an answer there. The last round's
have no round after them.

Draft 0.4 was satisfied by a chain whose final fixes nobody read, and that is
not an edge case: it is how every review run ended. Measured in the reference
implementation across two consecutive work items — the round that did look at
the previous round's fixes found seven defects in them, and its own fixes then
went in with the checkbox ticked by the session that wrote them.

So `Pass` gets a companion, and the two say different things. `Pass` is about
the **findings**: none of them is still open. This field is about the
**answers**: who opened the work that closed them. Three values and no others,
because a field read loosely reports the reassuring half of an ambiguity:

| The cell says | What it means |
|---|---|
| `round-N` | that round opened these fixes and reported on them. N must be greater than this record's own number, and that record must exist — a round cannot be checked by itself, by one that ran before the fixes existed, or by one nobody wrote |
| `no fixes to check` | no finding in this record closed with a fix. A round whose verdicts are all `answered`, `withdrawn` or `not a defect` wrote no code for anyone to open |
| `nobody — <why>` | the gap, written down. The reason is required: without it the cell records that something is missing and not what |

Anything else is refused, a session's own name included. Read loosely, *the
session that wrote them* would pass as an answer to a field whose whole
purpose is refusing it.

Only a later round may be named, so the **last** record of a finished run can
only read `no fixes to check` or `nobody — <why>`. That is the shape of the
rule rather than a limitation of it: a run ends at a round that wrote no code
nobody read, or it ends with the gap in the diff where a reader will meet it.

**A conforming tool reads this on every record**, where it reads `Pass` on the
last one alone. The two scopes differ because the two facts do: `Pass` is a
verdict on the whole review, and the last round's speaks for it; this is a
fact about one round's own fixes, and every round has one. Reading only the
last record makes `round-N` unreachable — a checker has to be later, and the
last record has no later round.

What it refuses is what the repository can contradict: a missing row, a round
that does not exist or is not later, and `no fixes to check` beside a verdict
that closed with a fix. Whether it should also refuse a checked `Pass` beside
`nobody` is the project's call rather than this protocol's: the two are not a
contradiction inside one file, and a tool that fails for an honest disclosure
teaches people to write none.

A project that does choose to fail should **grandfather the records whose work
item began before it adopted the rule**. Those records are usually merged and
have no honest repair — a round record written for a review nobody ran is a
fabrication, and unticking `Pass` fails whatever rule says a ready change
request carries a passing review. A check whose first act is red on history
nobody can fix is a check people learn to skip, which loses the records it
could have caught in exchange for the ones it never could. What the cutoff is
keyed to has to be readable from the record itself; the reference
implementation uses the timestamp already in the work item's directory name.

#### The Needs a fix field — the answer a run ends on

Where a run ends at a round that opens nothing needing a fix, that answer is
the terminal condition, and it belongs to the reviewer rather than to whoever
reads the record afterwards.

It is not the verdict table said another way. A finding the implementer
answers with grounds is a finding, and it needs no fix, so a round can report
several and still end the run. Deriving the answer from the table gets that
case wrong in the direction that costs a round.

The reviewer writes one line — `Needs a fix: no`, or `yes` and what does — and
whoever writes the record copies it. Without the field the question is still
asked and the answer has nowhere to live, which puts a decision the run turns
on in a transcript that ends with the session.

**A record written before the field existed is left without it**, which is the
opposite of what this protocol asked for `Fixes checked by` and is the same
reasoning that makes the difference. That field asks who opened the fixes, and
the answer is in the repository: which round followed, and whether one did.
This one asks what the reviewer concluded, and a reviewer who was never asked
left no answer anywhere. Filling it in from the verdict table is exactly the
derivation the paragraph above refuses, so the honest migration is none.

### tests-todo.md — regression tests prescribed, not written

One row per test: what it asserts · **destination file** · grounds · status.
The reviewer prescribes; the implementer plants. Prescriptions embedded in
fix-suggestion snippets get lost (measured) — this file is the contract.

### evidence-todo.md — verified facts awaiting the ledger

One row per fact: the fact · destination ledger row · status. Reviewers do
not write the ledger directly: parallel writers clobber each other, and
worker findings are pre-verification.

## The handoff before round 1

Everything above hands one round's state to the next. The same boundary
exists one step earlier and had no rule: the session that decides the work
hands it to the session that does it, in a spawn prompt whose format nothing
constrains. Measured across six agent segments that were deliberately handed
coordinates (issue #29): every segment reported its coordinates held and
nothing needed rediscovering — and the one fact that travelled as prose cost
a full review round.

So the orchestrator→implementer handoff follows the rule `Inherited axes`
already states for rounds: **coordinates rather than prose.** The exact line
the prose to extend sits on, the grep that returned nothing, the test files
whose assertions constrain the wording, the runner incantation. What round
N+1 inherits from round N, round 1 — and the implementer before it —
inherits from the orchestrator.

Three requirements, each bought by a measured failure:

- **A fact carries the coordinate that makes it falsifiable, or it is
  marked as an assertion nobody has opened.** The labels are the three
  `verify` puts on completion claims — **executed / read / unverified** —
  and they work unchanged on a handoff. The failure that bought this: **an
  aggregate is not a coordinate.** A spawn prompt carried a count as if it
  were checkable; the number could be counted, the claim it stood for could
  not, and it reached five documents before a review round found it false.
- **A coordinate reaches the rule, not its neighbourhood.** A line four
  lines below the rule looks like an answer, so it stops the search; two
  rounds were spent widening one.
- **A claim that flips on measurement point says where to measure**, beside
  the coordinate. Two findings in one work item flipped their answer on the
  measurement point alone — whole file against partial patch, above against
  below a particular line — and a passing measurement taken at the wrong
  point proves nothing about the claim.

### While the implementer runs

The orchestrator cannot see a running session. Twice, on two consecutive
work items, "is 40 minutes normal" was answered by reconstructing `git log`
by hand. The readout already exists and is written during the run, by the
party being watched, at no extra cost: `plan.md`'s Phases table has a
**Status column** the implementer fills with the commit that closed each
phase (`templates/sdd-plan.md`). Open it rather than asking; the stall
signal is **time since it last advanced** — wall clock cannot separate a
40-minute run that is finishing from a 12-minute one that is wedged, and
this can.

After a run, `skills/verify/scripts/session_cost.py` reads the transcript
(subagent segments included, under `<session-id>/subagents/`) and separates
command time, model time, batching and repeats, because each has a
different fix. It sat unreferenced through a full day of measurements
nobody took; this paragraph is what points at it.

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

Draft 0.6, extracted from the convention this plugin's `code-review` and
`implement` skills already operate (they are its reference implementation).
Field names and layout may change; the three conformance rules are stable in
shape. 0.2 changed the third from *delete after draining* to *close and keep*.
0.3 moved the directory off the change-request number and onto the work item,
which is what made rule 1 satisfiable at all, and added the `Pass` field so
that "was it reviewed" and "did it pass" stop being the same question. 0.4
gives the records their own `rounds/` subdirectory and requires a conforming
tool to name a record left at the old location rather than passing over it.
Draft 0.5 adds `Fixes checked by`, because 0.3 split "was it reviewed" from "did it
pass" and left a third question inside the second: who opened the fixes that
made it pass. No conformance rule is added for it: whether an unread set of
fixes fails a change request or only prints is a project's call, so the
field's own section states both — with the grandfathering a project that
fails has to carry — and the requirement stays at the level of the field
being present and honest. The reference implementation now fails, for work
items begun after it adopted the rule. 0.5 also adds `Needs a fix`, because a
run that ends when a round opens nothing needing a fix turns on an answer the
record had no room for.

0.6 adds the handoff before round 1: the coordinates-carry rule applied to
the step that starts the work, the three labels a handoff fact arrives
under, and the progress channel an orchestrator reads while the implementer
runs. No conformance rule is added: a spawn prompt is not a file this
protocol can check, so the requirement stays at the level of what a
conforming handoff carries.

0.3 also states the path as this implementation's choice rather than as the
protocol. Draft 0.2 claimed to be tool-agnostic while naming a directory
inside one plugin's own state folder — a claim its own location contradicted.
Portability comes from the file shapes, which read the same to any agent
wherever they sit.
