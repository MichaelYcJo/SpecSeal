---
name: code-review
description: |
  Two-stage review methodology (spec compliance, then quality) with comparison axes,
  cross-session review records, and re-review inheritance.
  Use when: reviewing a PR or diff, re-reviewing after fixes, orchestrating reviewer agents.
  NOT for: implementing fixes (use `implement`), style-only linting a formatter
  can do, or a plain bug-and-cleanup sweep of a diff — Claude Code's built-in
  `/code-review` covers that. This one judges spec compliance before quality and
  carries earlier rounds' coordinates across sessions.
---

# code-review — spec first, then quality

Loaded by the `warden` agent; also drives the orchestrator running a
review. The default assumption is **"this code has defects"** — try to find
them, not to prove their absence. An ungrounded LGTM is forbidden; when
uncertain, write a question, not a pass.

## The orchestrator's half is a file of its own

**If you are orchestrating a review run rather than reviewing a diff, read
`skills/code-review/orchestration.md` before round 1.** The five sections
this file used to carry under an `Orchestrator:` prefix are there, verbatim
and under the same headings: how a fix pass is obtained, how a run ends, when
the pull request opens, what to check before posting, and how the cycle
closes.

**A reviewer never opens it**, and that is why it is a path rather than an
entry in a `skills:` list. Deciding whether a run ends, resuming an
implementer, opening or marking a pull request, and posting are four acts
`agents/warden.md` forbids the reviewer — so 24,948 characters of procedure
reached every `warden` spawn with no act of its own to apply them to (#265).

Everything else in this file is the reviewer's, and the orchestrator reads it
too: a run is judged against the same two stages and the same axes as the
diff it reviews.

## The language the round records are written in

The prose in `rounds/round-N.md` — its cell contents and the text beneath its
tables — follows `Record language` in `config.md`, English when the row is
absent. The root is `<repo>/seal/` where that directory exists and
`$(git rev-parse --git-common-dir)/seal/` otherwise.

What stays English regardless: every field name, section heading and
vocabulary word the checkers match, listed in `templates/config.md` under
*What no row governs*. `chain_check.py` reads those strings literally, so a
translated `## Verdicts` or `Verdict` column is not a translation — it is a
record the checker cannot read.

**The report you post to the pull request is not a record.** It is prose for
whoever opens that pull request, and follows `Commit and pull request
language` instead, per `commit-pr-convention`. Posting and recording are
separate acts producing different texts, which is why the two rows split
here.

## Two stages, in order

1. **Spec compliance** — actual code vs. the written spec (`docs/` policies
   first, then `seal/specs/` SDD). Look for both missing *and* unrequested extra
   behavior. Do not trust the implementer's report; read the code.
2. **Quality** — only after stage 1 passes: correctness, error handling,
   security, performance, test quality.

The SDD set includes the work item's `overview.md`, which arrives in the diff
rather than needing a search — the change writes it. It is the implementer's
account, so stage 1 governs it: read the code, never adopt what it concludes.
Three sections carry that account. **Where spec and implementation diverged**
declares where the code left the document; **Not verified** is the author's own
list of claims nobody has checked; **Fed back into the spec** holds clauses the
implementer added to the spec set during this change, which is why an account
citing them is citing itself.
Settle what you can and report each result; what only a person can answer stays
open, and the report says which of the two happened. Reviewers do not edit the
file.

Review scope is not limited to changed files. New code that calls into
untouched files makes *their* query conditions and boundary operators take
effect for the first time — follow every call the change introduces.

## Comparison axes

Fix the axes before starting and cover **all** of them; picking whatever
catches the eye misses something different every time.

| Axis | Compare |
|---|---|
| Inputs | names, types, required/optional, defaults, accepted ranges |
| Authorization | who acts/queries as whom; self/admin/other branches |
| Query scope | which set is targeted: period, ownership, status filters |
| Exclusions & boundaries | excluded states, overlap conditions, **boundary values** (rarely written down — most frequent divergence point) |
| Deliberate non-exclusions | what the spec intentionally does *not* filter; new code tends to "clean it up" |
| Ordering, dedup, response shape | sort keys, tie-breaking, dedup basis, included/excluded fields |
| Error paths | failure conditions, codes, messages; failure vs. empty result. Count **new failure paths the change introduces** separately — someone must classify each as fix or regression |
| State transitions | against the spec's state machine, if one exists |
| Concurrency & atomicity | what can change between the read that decides and the write that acts: state held across an external call or `await`, transaction boundary against lock scope, whether a retry executes twice |
| Security | who can reach this path and as whom; the trust of every input that crosses an OS or process boundary; whether each failure fails open or closed; what a crafted name, path, or payload reaches |

Every axis above the last two is settled by reading a single request from end
to end. The concurrency axis is not: it asks what a *second* actor does while
the first is mid-flight, and no amount of following one path answers it. It was
added after a review walked all eight of the others cleanly and a second
reviewer, working from no list at all, found a window where a reservation was
mutated while an external call was in flight.

The security row earned its place the same way. Stage 2 has always named
security, and the table is what makes an axis mandatory — an axis that lives
in prose leaves no `❓` when nobody walks it. It also shares the concurrency
row's exemption on its own grounds: it asks what an input
nobody sends in good faith does, and no amount of following the request in
front of you answers it. Three of one round's four
blocking findings had a stronger security frame than the one they were given,
and one was a fail-open — an error path that answered "nothing to see" — in a
repository that keeps `tests/test_gates_do_not_fail_open.py` for that class
alone.

### The table is a floor, not a ceiling

A fixed list covers the same ground on a bad day as on a good one, which is
what it is for. The cost is the other half: an axis nobody wrote down is not
reported as unjudged, it leaves no trace at all. `❓ out of verified scope`
records that you looked and could not decide — there is no mark for what was
never on the list.

So name this change's own axes before starting, in the round's first minutes,
the way the base branch and the review-chain marker are settled there. Read the
diff for what could go wrong that the table does not ask about — money and
rounding, time zones, resource lifetime, migration ordering, pagination
stability while writes land — and add those rows for this round. An axis you
name here is walked and reported like any other; the ones above are the
minimum, not the set.

Distinguish findings from reading vs. findings from execution, always.
Something you did not run is never reported as passing.

### Probes vs. regression tests

| | What | Handling |
|---|---|---|
| Probe | Temporary test to settle what reading can't | You write it, run it, **delete it** (name `test_tmp_*`) — and everything else it made goes with it. The verified fact goes into the report |
| Regression test | Test that should exist but doesn't | **You don't write it.** Hand it over as a list with the target file per row |

Batch probe cases into one file and run once. Never probe what reading answers
— schema constraints, enums, defaults settle "can this state even exist"
claims without running anything. Don't touch `test_tmp_*` files another
session created.

**The file is not the whole of it.** Contract §7 is about leavings, not files:
a worktree, a branch, a checkout, a scratch clone or a virtual environment your
probe made for itself is a leaving too, and the probe is not over until every
one of them is gone. Deleting the named file and stopping there is what left a
git worktree behind through a whole review chain — the report said the probe
files were deleted, and there was nothing wrong with that sentence. It surfaced
two work items later, when `git switch` refused a branch a worktree already
held.

**A fixture chain is `&&`, never `|`.** A pipe between two commands does not
sequence them, it feeds the first one's output to the second, and a chain
built that way can sit waiting on stdin with nothing ever arriving. One
review round lost **68 minutes to a single such call** — `mkdir … | cd t3 &&
git init …` — while every other call it made totalled thirty-five seconds. The
hang exceeded the tool's own maximum timeout, so nothing cut it off, and the
parent's meter showed a healthy segment the whole time because a child's
command time is invisible to it.

So: build fixtures with `&&`, and give any call that could run long a timeout
you chose rather than one you assumed. A probe that hangs costs more than
every probe that round put together.

## Cross-session records — `seal/specs/<work-item-id>/`

**Before starting**, read this directory if it exists. Axes a previous round
already judged are not re-walked — unchanged code keeps its verdict. Probes a
previous round ran are only re-checked for "is it fixed now".

The records used to be keyed by a pull request number, at
`.specseal/handoff/PR-<n>/`. That number does not exist while the rounds that
would fill the directory are running, so no correct session could create it
and none ever did; `docs/review-handoff-protocol.md` carries the reasoning.
The work item is the key now, and its `routing.md` names the branch.

**Right after posting the report**, three files are written at the work item:
`rounds/round-N.md` by `round_record.py new`, from the reviewer's report, and
the two todo files by the orchestrator. Reviewer workers write none of those
three — parallel writers overwrite each other, and worker findings are
pre-verification.

**The reviewer does write one file, and it is not a record.**
`rounds/round-N-report.md` is the report itself, left where
`round_record.py new` reads it when `--report` is absent, and it carries
neither of the properties that sentence protects: it is one file per round
rather than a shared one, and it is the pre-verification text rather than
something that asserts a verdict has been checked. Before it existed the
report reached the orchestrator as chat text and a transcript, and the
orchestrator **retyped** it to have a file to pass — a lossy copy of the one
document whose whole value is that it is exact (#228). The fixer side had
`rounds/round-N-fixes.md` all along; this is the other half of that
convention. One of them gets a directory and
two do not: `round-N` is the only member of the set that is plural and
unbounded, so the two todo files sit at the work item's own level, beside
`rounds/` rather than inside it. The release guard reads `evidence-todo.md`
there (`.github/scripts/fold_ledger.py`, `seal/specs/*/evidence-todo.md`), and
one written a directory deeper is one it cannot see; `tests-todo.md` keeps it
company because the layout is one rule rather than two:

| File | Contents |
|---|---|
| `rounds/round-N.md` | target commit SHA (mandatory — branches move between rounds), verdict table with the grounds behind each verdict, **executed probe results**, the coordinates carried in from earlier rounds, **deferrals** — what this round took out of scope and the durable home each went to — the **broad-gate state**, `not yet` or the SHA the one full-suite run happened at, **who checked the fixes** (below), the **fix surface** — the `Contract changes` and `New units` of this round's fixes (below) — **whether anything it opened needs a fix** — the reviewer's own `Needs a fix` line, copied rather than re-derived from the verdict table — and **whether anything it found leaves the root or crashes**, the reviewer's `Loses a record or crashes` line, which is the floor under the cap, and **what ran the round** — the `Ran by` row, the agent and the model, filled by the session that spawned it (below) |
| `rounds/round-N-report.md` | the reviewer's report as the reviewer wrote it — written by the reviewer, read by `round_record.py new`, committed by the orchestrator beside the record it produced. Not a record: nothing reads a verdict out of it, and every reader of `rounds/` selects records by name. That commit is also what puts a reviewer's prose in front of whatever scans the tree — `agents/warden.md` §Report says what it costs, and it is the reviewer who has to know |
| `tests-todo.md` | regression tests to plant, with the destination file per row |
| `evidence-todo.md` | verified facts to merge into `seal/ledger.md` |

**A round record starts from `templates/sdd-round.md`** in shape, and
`round_record.py new` writes it: every field named above, already spelled,
from a source that is not prose, and the template says beside each one what
its values may be. A round that opens a blank file instead writes the fields
it happens to remember, and the one it forgets is the one nobody notices is
missing.

**What goes into `round-N.md`'s `## What this round was asked` section is
the round-specific content of the spawn prompt that started it** — never the
boilerplate `agent-contract` and `agents/warden.md` already carry, which
every round gets told by definition and none of them need repeated in its
own record. `round_record.py new` copies it in from `--asked <file>`
right after posting the report, and it is the one thing you write by hand for
the record: what the spawn prompt told this round, specifically, to attack,
in what order, and which facts arrived as coordinates rather than as
something still to verify. #81's round 1 is the
measured reason — the cheapest round on record, because its prompt named
eight specific things to try to break, and that fact today survives only in
a transcript.

Skipping this step makes review round *n* cost *n* full walks — the next
round re-finds every coordinate from scratch.

The directory is **closed at merge, not deleted**: the drained rows move to
their durable homes and a closing note says what went where. A deferral that
leaves this directory leaves what the next round reads, and comes back as a
finding — which is why it is also a row in `round-N.md` rather than only a
line in `seal/follow-up.md`.

What carries is **where to look, not what was concluded**. A later round opens
those coordinates and reaches its own verdict; an axis marked clean in round 1
can be broken by the fixes made for round 2, and inheriting that verdict is
exactly how it goes unseen. Earlier verdicts set the agenda — every one needs
an answer this round, on this round's grounds.

Re-deriving the verdict is not re-walking the code. Finding the coordinates is
the expensive half, and both the ledger and `round-N.md` exist so it is paid
once; a later round opens what they name instead of searching again. The cost
added is a re-read at known locations, which is what keeps a round-1 pass from
covering for a round-2 regression.

The test for what may be carried is whether staleness is detectable, not
whether the fact feels durable. A ledger coordinate carries because
`evidence-check` fails when the cited lines move; what the original does
carries because `seal/parity.md` pins the baseline SHA it was read at. Both
are re-established when their check fails, or when `parity.md` lists the path
under coordinate-trust exceptions. A verdict on current code carries nothing —
no check exists that would tell you it went stale, which is exactly why the
round has to reach it again.
## Findings format

Severity names carry the required action, not just a rank:

```
🔴 blocks merge     — spec violation or defect; fix before merge
🟡 fix or justify   — a defect the release would ship: the tool does something wrong, or tells a person something wrong; fix or justify
⬜ note             — reads badly while the behaviour and the fact stay right; fixed in passing or not at all, never counted by Needs a fix
🟢 pass             — verified equivalent (different implementation, same behavior, is a pass)
❓ out of verified scope — could not judge; never silently counted as pass
```

The line between 🟡 and ⬜ is *would the release ship a defect*. Half of the
last branch's 53 🟡 were true sentences about prose, and each cost a fix pass
and a reader; `Needs a fix` counts 🔴 and 🟡 only.

**Number the findings 1..N — the id is a bare integer.** The marker may lead
it (`🔴 1`, `⬜ 13`); nothing else may. `R2-1`, `1-1`, `1b` and `A2` are
refused by `round_record.py`, which names the format and quotes the row. Do
not put the round in the id: `rounds/round-N.md`'s own file name carries it,
and a prefixed id used to collapse eight findings toward one key in silence
(#227, `docs/review-chain-spec.md` §*The finding id*).

**This is the one format choice a reviewer makes that another agent pays
for.** The fix pass copies your numbering into its `## Fixes` table, so a
numbering the generator refuses surfaces at the orchestrator — one hop from
you, and one hop from the fixer, neither of whom is there to fix it.

Every finding carries `file:line`, what is wrong, why it matters, and a
paste-ready fix for 🔴/🟡. The report is written for posting as a PR comment,
but **the user posts it** — publishing externally is the user's call.

**Paste-ready means the snippet cannot mislead on its own.** A fix often needs
a name the tree does not have yet — a field the schema never defined, a helper
nobody wrote. Saying so in the paragraph above does not travel: people copy the
block, not the prose around it. Mark every such name inside the snippet, at the
line that uses it:

```python
if requester != order["paid_by"]:   # NAME NOT IN TREE — no order schema found
    raise PermissionError(...)
```

An invented identifier that reads as verified is worse than no suggestion. If
too many names are missing for a snippet to stand, describe the change in
sentences and say which document would have to exist for the code to be
written.

**The same marker is what a record says a gone name with, and it is read.**
`evidence-check` refuses a compound backticked identifier in the records of a
work item that has not shipped when nothing outside `seal/specs/` carries it
(#190) — a record naming a unit the next commit deleted is a claim nothing
was reading. Writing `NAME NOT IN TREE` on that line is the whole of the
exemption, in either of its two meanings: a name a fix is proposing, and a
name a record is deliberately calling gone — *`stale_helper` deleted and its
one call site moved — NAME NOT IN TREE*. The example name is invented on
purpose: writing a real gone name here would put it back in the tree the
check compares against, and silence the very records it was meant to catch.
It exempts the LINE and not the
name, so the same name still has to exist everywhere else it is claimed, and
the exemption stays with the person who knows the name is absent rather than
becoming a list in the checker.

**Every one of those blocks goes under `## Paste-ready fixes`, and that is
the only place a fix survives the session.** `round_record.py new` copies the
report's tables and takes every fenced block under that heading; prose it
does not take. A fix written into the findings paragraphs alone reaches no
file, and the record is what the fix pass opens instead of the report —
*the report is a message in a session that ends; the record is a file the
next segment opens.* Measured (#187): a 162-line report carried three
executed snippets, the record came out at 80 lines with none of them, and the
fix pass rebuilt all three from a description. Its first reproduction was
wrong. A round that opened nothing needing a fix writes no section, and the
record says so.

**The report is a file now, and that changes what the sentence above is
saying rather than retiring it.** `rounds/round-N-report.md` survives the
session, so a fix pass that wants the report's own words can open it. What is
unchanged is which file the fix pass is *told* to open and which one anything
downstream reads: `chain_check.py` reads the record, `close` writes the
record, and the next round inherits from the record. So a fix that exists
only in the report's prose still reaches nothing that acts on it — the loss
is no longer *the words are gone* but *the words are in the file nobody is
pointed at*, which costs the same fix pass. Fence it under
`## Paste-ready fixes` regardless.

A Grounds cell is not the place either. It is one line of one table row, a
paste-ready fix is a fenced block with comments in it, and a `|` inside that
cell used to truncate the row without a word (#189).

**A fix touching an OS boundary states its assumed precondition.** The
premises are the ones a snippet assumes without a line to show for them —
path resolution, file modes, symlinks, subprocess working directory,
encoding — and a sketch that assumes one reads as paste-ready and is not. The
clause
above covers invented *names*; this covers unexamined *premises*. State the
precondition beside the line that relies on it, the way a missing name is
marked, or in one sentence under the snippet — and "it has none" is a
statement worth making, because silence and "none" read alike. Three of one
round's four blocking findings arrived as sketches that read as paste-ready
and were not.

### Verdicts that close too early

Three shapes of closing recur, and each is written down here because each was
measured costing rounds.

**An enumeration over an unbounded domain is a recorded limit, not a closed
finding.** A fix that answers a finding by enumerating cases — keywords,
spellings, constructs — from a domain nothing bounds has narrowed the
finding, not closed it. The verdict says so, and the limit goes where it will
be read again: the skill's Known limits, the ledger, or the record's Deferred
row. Measured: one such rule cost three rounds and two owner decisions, and
closed only when the uncertainty moved out of the classifier instead of being
argued inside it.

**A mutation score licenses *tested*, never *safe* — say so where the number
is reported.** A score like `12/12 killed` establishes that the pins
discriminate — the fix is *tested* — and says nothing about whether it is
*safe*. Three consecutive rounds each reported a perfect score, and all three
were rounds whose fixes opened findings.

**A document claim gets a pin.** A claim a fix writes into a document — a
limit, a vocabulary, a behaviour — closes when a test pins the document, not
when the sentence lands. The same class of finding returned one round apart
because no test pinned any of the three documents involved, and the moment
pins existed they found a fourth file nobody had covered.

End with the proof block. Fill it only with files actually opened; write
`none — <reason>` otherwise:

```
📋 code-review applied
· spec:     <policy/SDD files and clauses read>
· compared: <files opened for comparison, file:line>
· verdict:  🔴 n · 🟡 n · 🟢 n · ❓ n
```
