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
| Probe | Temporary test to settle what reading can't | You write it, run it, **delete it** (name `test_tmp_*`). The verified fact goes into the report |
| Regression test | Test that should exist but doesn't | **You don't write it.** Hand it over as a list with the target file per row |

Batch probe cases into one file and run once. Never probe what reading answers
— schema constraints, enums, defaults settle "can this state even exist"
claims without running anything. Don't touch `test_tmp_*` files another
session created.

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
the two todo files by the orchestrator (reviewer workers never write here —
parallel writers overwrite each other, and worker findings are
pre-verification). One of them gets a directory and
two do not: `round-N` is the only member of the set that is plural and
unbounded, so the two todo files sit at the work item's own level, beside
`rounds/` rather than inside it. The release guard reads `evidence-todo.md`
there (`.github/scripts/fold_ledger.py`, `seal/specs/*/evidence-todo.md`), and
one written a directory deeper is one it cannot see; `tests-todo.md` keeps it
company because the layout is one rule rather than two:

| File | Contents |
|---|---|
| `rounds/round-N.md` | target commit SHA (mandatory — branches move between rounds), verdict table with the grounds behind each verdict, **executed probe results**, the coordinates carried in from earlier rounds, **deferrals** — what this round took out of scope and the durable home each went to — the **broad-gate state**, `not yet` or the SHA the one full-suite run happened at, **who checked the fixes** (below), the **fix surface** — the `Contract changes` and `New units` of this round's fixes (below) — **whether anything it opened needs a fix** — the reviewer's own `Needs a fix` line, copied rather than re-derived from the verdict table — and **whether anything it found leaves the root or crashes**, the reviewer's `Loses a record or crashes` line, which is the floor under the cap, and **what ran the round** — the `Ran by` row, the agent and the model, filled by the session that spawned it (below) |
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

## Orchestrator: a fix pass resumes the implementer

A round's findings are closed by fixes written after it ends, and the session
that writes them is obtained by **resuming the session that built the branch**
— never by spawning a fresh one while that session still exists. The resumed
session's context already holds what the fixes need: the files it wrote, the
tests it ran, the grounds it recorded. A fresh spawn holds none of it and
re-establishes all of it before the first fix lands — the rediscovery cost the
handoff before round 1 exists to bound, paid again in full for a pass that
needed none of it.

Measured three times, with no counterexample: as a fresh spawn, one fix pass
cost 282 calls and 45 minutes (#33); as a resume, 30 calls and 3.9 minutes
(#29) and 26 calls and 5.2 minutes (the #57 chain).

When the implementing session no longer exists — a new day, another machine —
the fresh spawn is the only option left, and what it takes is the handoff
before round 1 (`docs/review-handoff-protocol.md`): coordinates rather than
prose, each fact labelled. The rule decides which to reach for while both
options exist.

**The fix pass hands back a `## Fixes` table, and `close` applies it.** The
handover carries `| # | Verdict | Commit or grounds |`, one row per open
finding, the verdict `fixed`, `answered` or `deferred <home>`; you run
`round_record.py close --item <dir> --round N --fixes <file> --range <a>..<b>`
and the record's verdict cells, `Contract changes` and `New units` are written
from that table and the fix range. The pass writes no `phases/phase-N.md` and
no `plan.md` row — `agents/smith.md` owns that rule, and this sentence is the
link to it.

**The half of a prompt that does not change between rounds is not yours to
type.** `skills/agent-contract/SKILL.md` reaches every agent you spawn at
startup, through the `skills:` list in its definition, and each agent's own
half is in `agents/<name>.md`. So the prompt is left holding what is specific
to this round and nothing else. That half used to be retyped from memory every
round and drifted without a trace: one rule arrived at round 2 of a seven-round
chain and round 1 ran without it.

**That contract binds you too, and only if you load it.** An orchestrator
reads this skill and never `agents/*.md`, so the file reaches it by being
opened rather than by arriving — `user-invocable: false` permits the load and
does not oblige it. #107's headline failure is an orchestrator breaking a rule
it had put into every prompt it sent, which no rule reaching only the agents
would have caught.

## Orchestrator: the run ends with a verifying round

A round's findings are closed after it ends, by whoever writes the fixes. Every
round but the last has a reader for those fixes — the round that follows, since
each of its verdicts needs an answer there. The last round's fixes are read by
nobody, and the box saying the review passed is ticked by the session that
wrote them.

That is not an occasional slip. It is how every run ended, and it was measured
twice in a row: the one round that did open the previous round's fixes found
**seven** defects in them, and its own fixes then went in unread.

So a run ends with a **verifying round**, and three things define it.

| | What |
|---|---|
| When | **after the fixes** for the previous round are committed — never before, or it reviews what has already been reviewed |
| Target | the **diff of those fixes**, not the branch. That is what keeps it bounded: it is the cheapest round of the run |
| Job | the answers, not new findings. For each verdict the previous round recorded as closed, is it actually closed |

One surface in that diff is exempt from *the answers, not new findings*: what
the previous record's `New units` row names. A unit the fixes created has
been reviewed by nobody, so the verifying round treats it as a finding
surface — *is this correct* — rather than a verification surface. Measured:
one fix commit created eight new units, and four carried defects.

The reviewer answers the third one in a line of its own — `Needs a fix: no`,
or `yes` and what does — and that line is one of the two the run ends on, the
floor below being the other. Copy it into `round-N.md`'s `| Needs a fix |` row
rather than re-deriving it from the verdict table: a 🟡 the smith answers with
grounds is `no`, so a round can report findings and still end the run. The row
is read by `chain_check.py`, and what reads it is the floor's bound below: a
`yes` is what says the run reopened, which is what keeps that bound from
refusing the verifying round's own reader. A `fixed` verdict does the same
whatever the row says — the reviewer may answer `no` and the orchestrator may
fix the 🟡 anyway because it ships, and those fixes owe a reader too. The bound
reads the verdict column for that, so the row stays the reviewer's.

**A round that opens nothing needing a fix does not consume the cap.** The cap
counts rounds that found something, because it exists to stop a loop that is
not converging, and a round that finds nothing is the loop having converged.
A verifying round that opens something IS a finding round and consumes the cap
like any other, and one that opens nothing is by definition the last one,
because the run ends at it.

What this paragraph used to add — that nothing here runs away — was false.
The fixes of a verifying round that opened something need a reader, that
reader is a verifying round again, and #161 measured fifteen rounds through
that door. So the reopening is **one**: after a record that met the floor, one
later record may close on a fix, a second is refused, and the run ends
`capped` — every finding still open becomes an issue, its verdict reads
`deferred #N`, the record's `Fixes checked by` reads `no fixes to check`, and
the pull request is labelled `chain: capped`. `docs/review-chain-spec.md`
§*The reopening — one, and then the run is capped* owns the rule, the refusal
and its cutoff.

The condition is not *this round found nothing* — that would be unbounded, and
it was considered and rejected. A verifying round that raises a 🟡 the smith
answers with grounds has opened nothing needing a fix, and the run ends there.

**A finding located in a record is a correction, not a round.** A finding
whose `Location` is under `seal/specs/`, `seal/ledger/` or `seal/ledger.md`
owes no fix pass and no reader: what `chain_check` or `evidence_check` refuses
is corrected in the closing commit, and what neither reads is prose, corrected
in passing or not at all. `Needs a fix` does not count it.
`docs/review-chain-spec.md` §*The last round verifies* owns the rule and the
count behind it — 33 of the last branch's 65 findings were located in records.

### The cap is a ceiling, and this is the floor it never had

**Stop when a round finds nothing that leaves the root and nothing that
crashes.** Whatever else it found is deferred with a named answerer, or becomes
an issue. `docs/review-chain-spec.md` owns the definition and the measurement
behind it; what matters where you decide to spawn another round is that three
and five are a ceiling rather than a budget to spend down.

The reviewer answers this in a line of its own too — `Loses a record or
crashes: no`, or `yes` and what does — and it is copied into `round-N.md`'s row
of the same name, after the colon. It is a second terminal condition and not
the first one reworded:

| The reviewer's line | What it says | What follows |
|---|---|---|
| `Needs a fix: no` | this round wrote no code nobody read | the run ends, and the round does not consume the cap |
| `Loses a record or crashes: no` | nothing this round found leaves the root or crashes | the run ends, and the round counts toward the cap if it found anything needing a fix |

The paragraph above is about the cap's arithmetic — whether a round that has
already run counts toward three or five. This is about whether the next round
is spawned at all. A round that reported a 🔴 in a line a person reads answers
`yes` to the first question and `no` to the second, and that round ends the run
with the finding handed over rather than chased.

**Spawn the verifying round anyway.** The floor stops the finding rounds; the
last set of fixes still needs a reader, and the round above is it. A record
that met the floor is followed by at most one more round record, and the one
exception — a verifying round that reopens the run, so that its own fixes need
a reader — is bounded to one reopening, after which the run ends `capped`;
`docs/review-chain-spec.md` §*The reopening — one, and then the run is capped*
owns the count, the bound and the exit. `chain_check.py` walks both, reading
`Needs a fix` and the verdict column, which is why that row is read rather
than only written.

### A fix pass adds the unit that pins it, and that unit ships unreviewed

**A unit a fix pass may not add has somewhere to go.** It is deferred with a
named answerer, or becomes an issue — the two homes the floor above already
gives whatever a stopped round found. That sentence comes first on purpose: a
rule that refuses without saying where the refused work goes stops the chain
at a wall.

**A fix pass may not add mechanism.** Not a rule, not a checker, not a
template section, not a walk. A finding that can be closed only by one is an
issue, and its verdict reads `deferred #N`. This is the first level, and the
depth below is the second: that one refuses a unit added to pin a unit, this
one refuses the fix pass building the thing that would need pinning at all.
Measured on the branch that shipped the release before this one (#153 and
#150): round 4's fix pass built a rule, a reader and two cases to close one
🟡, which cost round 5's 🔴, a revert (#159) and half of round 6.

**A fix pass may add a unit. That unit's fix may not.**

Depth one, stated rather than discovered. A fix answering a finding in code
that predates the run may add the helper or the case that pins it, and that
unit is depth 1. A fix answering a finding *inside* a unit an earlier round's
fixes created may not add another to pin it — that would be depth 2, and it
takes the exit above.

The reason is in the commits. The fix is read by the round that follows; the
unit it added to pin the fix is read by nobody, and the two ship together.
Measured across four rounds of #82: round 1's fixes added `configured_language`
and a templates check, and round 2 found the defect reproduced in both; round
2's fixes added `mirror_to_refuse` and a widened glob, and round 3 found the
glob out of step with its corpus; round 3's fixes added `as_language_name`,
`ROUND_RECORD_FIELDS` and a `git ls-files` helper, and round 4 found a
subprocess without `check=True` and a list hand-copied from the file it checks.
Three consecutive rounds found their finding inside the previous round's fixes.

The floor above is what turns this from tidy into required. The rounds the
floor removes are the rounds that were reading those units, so shipping the
floor alone cuts the eyes and leaves the generation.

`round-N.md`'s `New units` row carries the depth, one per entry —
`unit (depth N)`, entries separated by `;`. Per entry rather than per round,
because a single fix pass can answer a finding in code that predates the run
and a finding inside an earlier unit in the same breath, and one number for the
round would be false of one of them.

### Then say who checked them, in the record

`round-N.md` carries `| Fixes checked by |` beside `Pass`, and the two answer
different questions. `Pass` says no finding in this round's table is still
open. This says who opened the work that closed them. Three values, and
`chain_check.py` refuses everything else:

| The cell | When |
|---|---|
| `round-N` | a **later** round opened these fixes and reported on them. It has to exist, a round can never name itself, and its own `Target SHA` has to be later than this record's — a number is cheap and a round is not, so two records sitting at one commit are refused however they are numbered |
| `no fixes to check` | nothing here closed with a fix. This is the verifying round's own terminal value |
| `nobody — <why>` | the gap, written down. It prints on every CI run, and on the run's **last** record beside a checked `Pass` it fails the pull request — a review cannot have passed while its own fixes went unread. Work items begun before the rule landed are excused and only print |

`round_record.py new --item <dir> --round N …` sets it: when it writes round
N's record it sets round N-1's cell to `round-N`, touches nothing else, and
commits nothing — the commit is yours, made from a record you have read. That
used to be the last act of a round, done by hand, and it was forgotten five
times on the last branch. `round_record.py close` writes `no fixes to check`
into a record whose fix table closed nothing on a fix — a capped run's last
record, whose every verdict reads `deferred <home>` and which has no next
round to set the cell. Every record carries the row, not only the newest —
`Pass` is a verdict on the whole review and the last round's speaks for it,
while this is a fact about one round's own fixes. `docs/review-chain-spec.md`
holds the rule and what each refusal costs.

### And name the fix surface, in the same record

Two more rows, and `round_record.py close --range <a>..<b>` derives both from
the fix range: `Contract changes` from an AST comparison of every top-level
Python unit the range touches, with the call sites found by search, and `New
units` from the same comparison with a depth per entry. It refuses depth 2
before writing any cell. The rows cost no question to anyone, because the diff
answers them.

| The row | What goes in it |
|---|---|
| `Contract changes` | every unit whose signature, return arity, return type, or set of returnable values this round's fixes changed — each with the call sites it reaches, `unit → site, site`, units separated by `;`. The diff names the changed signature and `grep` names the reach; the largest regression class issue #57 measured — four findings of ten — was a contract change whose reach was never revisited |
| `New units` | the top-level definitions and constants the fixes added, each with the depth it was added at — `unit (depth N)`, one entry per unit, entries separated by `;`. The verifying round's finding surface above. A fix pass may add a unit; that unit's fix may not, so depth 2 or above is refused and the unit is deferred with a named answerer or becomes an issue |

Both accept `none`, with or without a reason after it. `chain_check.py`
refuses a record without the rows and a unit listed without its reach, for
work items begun on or after its `SURFACE_FROM`; records of earlier work
items print instead — the grandfathering `Fixes checked by` already uses.

**Forgetting the second step is silent, and it is no longer a habit to
remember.** The ordering rule above requires the record to be committed before
its fixes exist, so both rows begin at `none — the fixes are not yet written`
— and a record that never gets the second step reads exactly like one whose
fixes added nothing. A verifying round opening it sees no finding surface at
all. Measured on the work item that added the ordering rule: its own round 1
record sat that way for two rounds, and the six units its fix pass created
reached the next round only because a reviewer went and looked. Now `close`
writes both rows from the diff, so the second step is one command rather than
one pass a session has to remember.

So `chain_check.py` refuses that value on a record whose `Fixes checked by`
names a `round-N` — a later round opened those fixes, so they exist — for
work items begun on or after `ORDER_FROM`. While the cell still reads
`nobody — <why>`, *not yet written* is true and nothing refuses it.

**Which means the refusal reaches the session that filled `Fixes checked by`
and stopped, and not the one that filled nothing.** All three cells left at
their starting values escape it, and so does `no fixes to check` beside a
pending row — for a round that commissioned no fixes, *not yet written* is
false the moment it is written. Both states print instead, and a reworded
cell is not the only thing that escapes: three spellings carry the template's
words unchanged. `docs/review-chain-spec.md` names them and says why the
answer was to write the limit down rather than widen the match. What makes all
of it moot is the generator: `close` writes the two surface rows from the fix
diff, and `new` for the next round sets the checker cell.

The depth inside `New units` has a cutoff of its own, `DEPTH_FROM`, later
than that one: a work item between the two owes the row and not the depth in
it, because its records were written when the row named units alone.

### And say what ran the round

One more row, `| Ran by |`, and it is the spawning session's rather than the
reviewer's, for a sharper reason than the two above. An agent is told what it
is, so a value it writes about itself is the value it was told; and the model
is a spawn-time argument the orchestrator chose, which `agents/*.md` pins
nowhere.

`round_record.py new` writes it from `--ran-by "<agent> on <model>"` — the
agent and the model, joined by the word `on`, and the value is the one you
chose at the spawn:

```
| Ran by | specseal:warden on <the model it was spawned with> |
```

**Both, never one.** An agent without a model cannot be compared against
another run of the same agent, and a model without an agent cannot be told
apart from the orchestrating session's own turns. `unknown — <why>` is the
answer where neither is knowable — a session spawning through another harness
may have no name for a model — and a bare `unknown` is refused the way a bare
`nobody` is, because without the reason the cell records that something is
missing and not what.

`chain_check.py` refuses a record without the row for work items begun on or
after its `RUNNER_FROM`, and records of earlier work items print instead. A
row that is present and unreadable is refused at any age: formatting is always
the author's, which is the split the fix-surface rows already make.

What it buys is the question the measurement log could not answer. Every
segment of two work items was metered and posted, and not one of the readings
says what produced it — so the log knows what a segment cost and cannot say
whether the cost was the model's, the agent's, or the scope's.

### And commit the record before commissioning the fixes

The record is the fix pass's agenda, so it has to exist before the fix pass
does. `round_record.py new` writes `round-N.md` when the round posts, with its
verdict cells reading `open`, and commits nothing — commit it then. The fixes
land next, and `close` updates the cells to `fixed at <sha>` afterwards, from
the fix table the pass hands back, in the same command that writes the fix
surface.

**A record written late leaves no trace**, which is why this is a gate rather
than a reminder. By the time a late record is committed the fixes have landed,
so its cells read `fixed at <sha>` — indistinguishable from a correct record
after its own update pass. Measured twice in one release, four minutes and two
minutes after the fix commits those records commissioned, and both times the
reviewer's drafted replacement text lived only in a report and the next
segment rebuilt it from scratch.

`chain_check.py` refuses a record whose **adding** commit descends from a
commit its own verdicts name as the fix, for work items begun on or after its
`ORDER_FROM`; earlier ones print. It is the adding commit and never the last
one, because a correct record IS updated after its fixes land.

The cheapest way to satisfy it is also the one that pays: commission the fix
pass **from the committed record** rather than from the reviewer's report. The
report is a message in a session that ends; the record is a file the next
segment opens.

### The check a round runs reads everything, and only a write is narrowed

`evidence-check` takes `--ledger`, and the flag is right for one of its two
jobs and blinding for the other. Hand the round the unscoped read, and keep
the narrowing for the write:

| The form | What it is for |
|---|---|
| `evidence_check.py .`, no `--ledger` | **reading.** It opens `seal/ledger.md` and every fragment, which is the only way a branch learns it falsified a row it does not own — and those are the rows with the longest reach, cited by work that shipped releases ago |
| `evidence_check.py --ledger '<this work item's fragment>' --reverify .` | **writing.** `--reverify` re-stamps every drifted row it reads, so the narrowing is what keeps it off a row whose claim somebody else has to judge |

Measured (#153): one work item's three review rounds and two fix passes all
ran the scoped form and all reported a clean ledger. The unscoped read at the
pull request found **fifteen drifted rows and one broken claim** — a row this
repository's own rule says must be removed rather than re-pointed, which
nobody had been told they had falsified.

Neither instruction was wrong about its own subject. Scoping was the
correction that shipped, for the write; it was then carried into the read,
where it blinds. So do not answer this by deleting the narrowing — that puts
`--reverify` back onto somebody else's false claim, which is the defect the
scoping was adopted to fix.

A session that narrows on its own initiative reads none of the above, which
is why the tool announces it too: a `--ledger` run names the ledgers it did
not read, and says how to read them.

## Orchestrator: the pull request opens before round 1, and a phase is re-run

**The draft pull request opens at the end of the build, before round 1.** The
platform legs — the suite on the operating systems the session is not on — run
only at the pull request, so a chain that opens it at the end reviews for a
dozen rounds on one platform and meets the others afterwards. Measured on the
last branch: three Windows-only defects arrived after round 12. Open it as a
draft when the build's last phase closes, and the legs run beside the chain
from round 1.

**A session that has compacted hands the next round to a fresh one, and the
generated record is the handoff.** A compacted context holds a summary of what
it read, and a round run from a summary either re-reads what the summary
dropped or trusts it. The record `round_record.py new` wrote carries the
target, the verdicts, the probes and the deferrals as the reviewer wrote them,
so the fresh session opens the record and its coordinates rather than the
summary.

**A hand-back's verification claim is a claim.** Before spawning the next
phase, run the closed phase's suite and the lint of its changed files yourself
and read the output: a phase that reports green has reported, and a next phase
built on that report is built on prose. The section below already says this
of the reviewer's report; nothing said it of the implementer's until
2026-09-05. The broad gate still runs once, after the rounds settle
(`agent-contract` §2) — this is the narrow run at each phase boundary, and it
is yours rather than the phase's.

## Orchestrator: verify before posting

Never post reviewer output as-is. Check, by opening the coordinates yourself:

1. Coordinates behind every highest-severity finding — heaviest, hardest to retract.
2. "This state can occur" claims — constraints/enums/defaults may forbid the state.
3. Spec citations (clause numbers move while a review runs).
4. Test-pass claims — run them; count skips, which masquerade as passes.

Also check whether HEAD moved during the review; if source changed, those
verdicts need a re-pass. Record both SHAs in `round-N.md`.

## Orchestrator: closing the cycle

Once the report is verified, mark the reviewed state so the commit gate (this
plugin's PreToolUse hook) can recognize the cycle. Reviewer workers never write
this mark — a review that certifies itself is what the gate exists to catch.

```bash
git rev-parse HEAD > "$(git rev-parse --git-dir)/specseal-reviewed"
```

A commit closes the cycle; the next change starts an unreviewed one.

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
