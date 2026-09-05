# Review Handoff Protocol — draft 1.2

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

In this plugin's implementation that directory is `seal/specs/<work-item-id>/`.
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

The record is written by `round_record.py new` from the reviewer's report and
closed by `round_record.py close` from the implementer's fix table; the
orchestrator writes the round paragraph of the spawn prompt, which `new`
copies in, and nothing else in it. This file owns the format the two
subcommands produce.

| Field | Required | Content |
|---|---|---|
| Target SHA | yes | commit(s) the round actually reviewed — branches move between rounds; record both if HEAD moved mid-review. **Never rewritten after a squash** — see below |
| Ran by | yes, for work items begun after a project adopts it | what ran this round: the agent and the model, written as `agent on model`. `unknown — <why>` where the session cannot name one, and a bare `unknown` is not an answer. Filled by the session that SPAWNED the round, never by the round's own agent. See below |
| Pass | yes | a checkbox — `- [ ] Pass` or `- [x] Pass`. Checked means no finding in this round's verdict table is still open. See below |
| Fixes checked by | yes | who opened the fixes that closed this round's findings: a later round, `no fixes to check`, or `nobody` with the reason. `Pass` answers whether the findings were closed; this answers whether the closing was read by anyone. See below |
| Needs a fix | yes, from the round that wrote it | whether this round opened anything that needs one — the reviewer's own answer, copied rather than re-derived from the verdict table. It is one of two conditions a run ends on, and a finding the implementer answers with grounds does not make it `yes`. See below |
| Loses a record or crashes | yes, for work items begun after a project adopts it | whether anything this round found leaves the root or crashes — the reviewer's own answer again, in the same `no` / `yes — <what>` shape. It is the FLOOR under a round cap: `no` stops the run whatever is left of the cap. See below |
| Contract changes | yes, for work items begun after a project adopts it | every unit whose signature, return arity, return type, or set of returnable values this round's fixes changed — each with the call sites its contract reaches. `none` is an answer, with or without a reason. See below |
| New units | yes, for work items begun after a project adopts it | the top-level definitions and constants this round's fixes added, each with the depth it was added at — `unit (depth N)`, one entry per unit, entries separated by `;`. The verifying round's finding surface. `none` is an answer. See below |
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

#### The fix-surface rows — what the fixes changed, and what they created

A round's fixes are written after the round ends, so the record that
describes the round is also the only durable place to describe its fixes.
Two rows carry that, filled in when the fixes land — the same reach-back
that sets `Fixes checked by` — by the session that already has the fix diff
open, which is why the rows cost no question to anyone.

**`Contract changes` names the reach, because the diff cannot.** The largest
class of regression measured across one work item's seven finding rounds was
a fix that changed a unit's contract — signature, return arity, return type,
or set of returnable values — while not every place that contract reaches
was revisited. The diff names the changed signature; only a search names the
reach; a person reading the diff missed every one of the four. So each
changed unit is listed **with the call sites it reaches**, and a conforming
tool refuses a unit listed without them — the unit alone restates what the
diff already shows, and the reach is the half that went unchecked.

**`New units` names the verifying round's finding surface.** A verifying
round's job is the answers rather than new findings, and read literally that
skips the one set of units nobody has ever reviewed: the definitions and
constants the fixes created. One measured fix commit created eight new
units, and four carried defects. What this row names is treated as a finding
surface — *is this correct* — rather than a verification surface.

Both rows accept `none`, with or without a reason after it: `none — the
fixes are not yet written` is the honest value while a round is still
running. A record whose work item predates a project's adoption of the rows
prints rather than fails, keyed the same way as `Fixes checked by`'s
grandfathering — the timestamp already in the work item's directory name —
and for the same reason: a merged record has no honest repair, and writing
reach rows for fixes nobody re-read fabricates a review. A row that is
present and malformed fails on any record, because formatting is always the
author's to fix.

**The depth inside `New units` is adopted separately, and the depth has a
cutoff of its own.** A project can be past the cutoff for the rows and before
the one for the depth, and then its records owe the row and not the depth in
it — they were written when the row named units alone, and deriving a depth
now for fixes nobody re-read fabricates the answer the same way a reach row
would. A conforming tool that refuses a second-level unit says in the failure
where the unit goes instead; a refusal with no exit stops the chain rather
than the unit.

#### Loses a record or crashes — the floor under a round cap

A run bounded only by a cap spends the cap. The reviewer answers, in a line
of its own, whether anything it found leaves the root or crashes; `no` stops
the run whatever is left of the cap, and what the stopped round found that
still needs doing is deferred with a named answerer or becomes an issue.

It is not `Needs a fix` in other words. A round can open a 🔴 in a line a
person reads — which needs a fix and is neither a lost record nor a crash —
and that round ends the run with the finding handed over.

**A record that met the floor is followed by at most one more round record**,
the verifying round at the diff of the fixes that closed it. The one exception
is the reason `Needs a fix` is machine-read at all: a verifying round that
opens something is a finding round, its own fixes need a reader in turn, and
that reader is a third record. A conforming tool counts later records only up
to the first whose `Needs a fix` says the run reopened OR whose own verdicts
closed on a fix, that record included. The two rows answer different
questions — `Needs a fix` is what the reviewer opened, the verdict column is
whether fixes were written — and they come apart when the orchestrator fixes
a finding the reviewer said could be answered with grounds. Reading only the
first leaves such a run with no terminal record any exit accepts. Counting
blindly makes the sequence this protocol requires unwritable. That exception
is one: a second record closing on a fix after the floor is refused and the
run ends `capped` — `docs/review-chain-spec.md` §*The reopening — one, and
then the run is capped* owns the rule, the refusal and the exit.

Records predating a project's adoption print rather than fail, the same
grandfathering as above. `Needs a fix` is grandfathered WHOLE — absent, empty
or unreadable alike — because it carried free text from draft 0.5 until a tool
first read it, so a value written earlier was held to no vocabulary.

#### Ran by — what executed this segment

A record says what its segment was asked, what it found, and which commit it
looked at. It does not say what ran it, and that fact survives nowhere else:
the model is a spawn-time argument, and once the session ends it exists only
in a transcript. Measured in the reference implementation — every segment of
two consecutive work items was metered and posted to a measurement log, and
not one of the readings can be attributed to a runner afterwards.

**The cell names two things, not one.** An agent without a model cannot be
compared against another run of the same agent; a model without an agent
cannot be told apart from the orchestrating session's own turns. The two are
joined by the word `on` — `agent on model` — a word rather than a punctuation
mark, because a separator inside a code span splits the cell carrying it and
this protocol has already been bitten by that twice.

**The session that spawned the segment fills it, never the segment itself.**
An agent is told what it is, so a value it writes about itself is the value it
was told, and the orchestrator is the one that chose the model. This is the
same reach-back `Fixes checked by` and the fix-surface rows already make: a
session with a fact writes it into a record somebody else authored.

**`unknown — <why>` is an answer and a bare `unknown` is not.** A project may
genuinely not know: agent definitions pin no model, and a session spawning
through another harness may have no name for one. The reason is required for
the same cause it is required after `nobody` — without it the cell records
that something is missing and not what.

Records predating a project's adoption print rather than fail when the row is
ABSENT, the same grandfathering `Fixes checked by` carries. A row that is
present and unreadable is refused at any age: formatting is always the
author's, which is the split `Contract changes` already makes.

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
whose assertions constrain the wording, the runner incantation in the form
the round is to run it. What round N+1 inherits from round N, round 1 — and
the implementer before it — inherits from the orchestrator.

Four requirements, each bought by a measured failure:

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
- **A command with more than one form names the form, and says what the
  other one is for.** A flag that narrows what a check reads is right for
  one of its jobs and blinding for the other, and a handoff carrying the
  command carries neither job. The failure that bought this: a ledger check
  scoped to the work item's own fragment was handed to every segment of one
  work item, because that narrowing is what keeps a re-stamp off a row whose
  claim somebody else has to judge. Three review rounds and two fix passes
  all ran it and all reported a clean ledger; the unscoped read at the pull
  request found **fifteen drifted rows and one broken claim**, every one in
  a file the branch had touched. Naming the form alone is not enough — the
  reader who does not know what the other form buys deletes the narrowing,
  and the write then re-stamps the false claim.

One thing precedes the handoff rather than travelling in it: the draft pull
request is already open when round 1 is spawned, opened when the build's
last phase closes, because `skills/code-review/SKILL.md` §*Orchestrator: the
pull request opens before round 1, and a phase is re-run* owns that rule and
the platform legs it exists for.

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

### After a phase — the hand-back's claim is re-run

A phase's hand-back says what it ran and what the output was, and by §5 of
the contract that is prose until somebody opens it. Before spawning the next
phase the orchestrator runs the closed phase's suite and the lint of its
changed files itself and reads the output; the broad gate still runs once,
after the rounds settle. `skills/code-review/SKILL.md` §*Orchestrator: the
pull request opens before round 1, and a phase is re-run* owns the rule. Its
grounds are one step from this document: §*verify before posting* said the
reviewer's report is a claim and nothing said it of the implementer's, and
the work item that added the rule was checked that way from its first phase
(its `spec.md`, rule 9).

### After the run — the per-segment bars

The meter's numbers mean nothing without a bar, and the bar depends on
which kind of segment produced the transcript. One bar misreads two of the
three kinds: a ratio that is the right question for a reviewer is the wrong
one for an edit-test loop, and asking it there is a demand the work cannot
meet (issue #51, whose transcripts these numbers come from).

| Segment | Judged on | Grounds |
|---|---|---|
| reviewing | tools per turn **≥ 1.8** | a review's reads are independent — coordinates inherited from earlier rounds, files named by one handoff — so they can go out together. The rounds that set the bar measured 1.29–1.89 — not the complete record: the same issue holds a 2.0 baseline and a later chain at 1.10–1.54 — and the one round instructed to batch (1.89) was the fastest measured |
| implementing | **`repeats = 0`** and calls per deliverable — never tools per turn | an edit-test loop is inherently serial (measured 1.08–1.17): a call whose input depends on the last result cannot go out with it, so the ratio reports task shape, not waste. What does report waste: a command re-run unchanged, and how many calls one deliverable took |
| verifying | exempt | it targets the diff of the last fixes and is the cheapest round of the run by design; a segment that small is the nuance below in its every case |

**At very small rounds the ratio has few independent batches to rise on** —
a 23-call round read 1.64 while doing everything right. The bar is a lens
for rounds of ordinary size, never a refusal threshold: no gate fails a
round on it, and a small honest round that reads under it has nothing to
fix.

The bar and the meter's own advisory are different instruments.
`session_cost.py` prints its batching advisory below 1.2 and stays there:
the script cannot tell a reviewer's transcript from an edit-test loop, so
its threshold sits where it does not nag the serial case — the repository
owner's answer to Q1 of
`seal/specs/1788224363-a-subagent-rediscovers-what-the-session-established/questions.md`.
The bars above are the orchestrator's, applied knowing the segment kind.

**The bars judge a segment against its kind; the run-level table judges a
run against the last run measured.** A bar reads one transcript — a review
against reviews, an edit-test loop against edit-test loops — and says
nothing about the run those segments belong to. The table asks the other
question: rounds, wall clock, commits, findings and tokens, this run beside
the last one, in the same rows every time.

Its rows and where each one is taken from are `skills/verify/SKILL.md`
§*Measure the segment, and feed the flow log*, which is also where it goes.
That is **not a destination of its own** — the table joins the segment
readings in the rolling log that section already names.

## What every spawn prompt used to carry

The section above says what a handoff owes about the *work*. This one used to
say what it owes about the *method*, and it carried that half in full because
nowhere else did.

**It said so at the time, and named what would end it.** The rules belonged in
the agent definitions and in a contract file all of them read — issue #107 —
and they sat here until that landed, because a rule kept only in whoever last
wrote a prompt goes missing without a trace. It already had, twice: one rule
arrived at round 2 of a seven-round chain and round 1 ran without it, and
another arrived at round 3 after two rounds had each rediscovered it.

That work is done, so what follows is a pointer and nothing else. Restating
any of it here would put a second copy in front of the same reader, which is
the duplication the move was made to end.

### Where each half went

**The rules every agent is bound by are `skills/agent-contract/SKILL.md`.**
The harness injects it into each agent at startup through the `skills:` list
in that agent's definition, so nothing is typed and no path is resolved. Its
sections are numbered, and a number is never reused or re-ordered, so a
prompt and a round record can both cite one. What stood here under *Every
agent* is §1 to §4 — how an exit code is read, what an agent must not run,
what a prompt may narrow and may not widen, and which labels a report keeps
apart. What stood here as four method lessons the review chain paid for is
§12 to §15.

**An agent's own rules are in `agents/<name>.md`.** The list that stood here
under *The warden* is absorbed into `agents/warden.md` in full — where it
works, the `uv` venv, the report format, the verifying round's re-derivation,
and the records it must not write. The list under *The smith* is
`agents/smith.md` and the `implement` skill it loads.

Nothing that was a rule here reaches an agent by being typed any more. A
prompt that repeats one is redundant rather than wrong, and a prompt that
forgets one changes nothing — which is the whole of what this move bought.

### What a prompt is left holding

**A prompt carries what is specific to the round and nothing else.** The
branch and base, the target SHA and what the diff contains, the acceptance
criteria, the class to enumerate *for this change*, the shapes to try to
break, corrections the orchestrator has to hand over, and any state the agent
needs. Everything specific, nothing general.

The general half now arrives on its own, so a prompt that states it is
retyping what a file already holds — and what is retyped can be retyped
wrong. That is not a style preference: it is the failure the two paragraphs
above are the record of.

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

Draft 1.2, extracted from the convention this plugin's `code-review` and
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

Draft 0.6 adds the handoff before round 1: the coordinates-carry rule
applied to the step that starts the work, the three labels a handoff fact
arrives under, and the progress channel an orchestrator reads while the
implementer runs. No conformance rule is added: a spawn prompt is not a file
this protocol can check, so the requirement stays at the level of what a
conforming handoff carries.

0.7 adds the fix-surface rows, `Contract changes` and `New units`, because
the fixes that close a round's findings are the code most likely to open the
next round's — measured at four regressions of ten for an unrevisited
contract reach — and the record was the one durable place with no row for
them. Records predating a project's adoption print rather than fail, the
same grandfathering `Fixes checked by` carries.

0.8 adds the per-segment bars, because the meter draft 0.6 pointed at had
numbers and no rule about what they mean, and the one figure that existed
anywhere (an acceptance bar on an issue) was a single bar for three kinds of
segment — right for the reviewing kind and wrong for the other two. No
conformance rule is added: the bars judge a transcript, not a file this
protocol can check, and the section itself says they refuse nothing.

0.9 gives up the method half of a spawn prompt. The section that held it
called itself an interim home and named the issue that would end it; that
issue closed, and what stood there now lives in a contract every agent
receives at startup and in each agent's own definition. A pointer replaces it,
because a document that keeps a copy beside the pointer puts two answers in
front of one reader — the failure the move was made to end, arriving from the
fix. What is stated here instead is the rule about the prompt itself: it
carries what is specific to the round and nothing else. No conformance rule
changes, for the reason 0.6 gave when it added none — a spawn prompt is not a
file this protocol can check.

1.0 adds `Loses a record or crashes` — a floor under the round cap, because a
run bounded only by a ceiling spends the ceiling: one measured run went seven
rounds and its last three found nothing that leaves the root and nothing that
crashes. It also gives `New units` the depth each entry was added at, because
a fix pass adds the unit that pins it and that unit ships unreviewed in the
same commit — three consecutive rounds of one measured run found their finding
inside the previous round's fixes. `Needs a fix` stops being write-only in the
same draft: the floor's bound on what may follow a stopped round is wrong
without it, since a verifying round that reopens the run needs a reader for
its own fixes. Records predating a project's adoption print rather than fail,
the grandfathering `Fixes checked by` carries — and `Needs a fix` is
grandfathered whole rather than only when absent, because it carried free text
from draft 0.5 until this draft first read it. The reference implementation
fails on all three, for work items begun after it adopted them.

1.1 adds `Ran by`, because a record said what its segment was asked and what
it cost and never what executed it — and the meter draft 0.8 pointed at
produces readings that cannot be attributed once the session ends. Two things
the row settles rather than leaves to the author: it names the agent AND the
model, since either alone answers neither question anyone has of the numbers;
and it is filled by the spawning session, since an agent asked what it is
answers with what it was told. `unknown — <why>` is an answer for projects
that cannot name a model, in the shape `nobody — <why>` already has. An absent
row on a record predating adoption prints rather than fails, the
grandfathering `Fixes checked by` carries; a present and malformed one is
refused at any age, the split `Contract changes` already makes.

1.2 adds the fourth handoff requirement, because *the runner incantation*
turned out to name a thing that can have two forms and the handoff kept
carrying whichever one somebody last found useful. A narrowing adopted for a
write was handed to three rounds as a read, and each of them reported clean
on a ledger it had not opened. No conformance rule is added, for the reason
0.6 gave when it added none: a spawn prompt is not a file this protocol can
check. What a conforming handoff carries is what changes.

0.3 also states the path as this implementation's choice rather than as the
protocol. Draft 0.2 claimed to be tool-agnostic while naming a directory
inside one plugin's own state folder — a claim its own location contradicted.
Portability comes from the file shapes, which read the same to any agent
wherever they sit.
