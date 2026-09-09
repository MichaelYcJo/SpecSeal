# code-review — the orchestrator's half

The five sections `skills/code-review/SKILL.md` used to carry under an
`Orchestrator:` prefix. They are the procedure for **running** a review run:
obtaining a fix pass, ending the run, opening the pull request, verifying the
reviewer's report, and closing the cycle.

**Read this if you are orchestrating a review run.**
`skills/code-review/SKILL.md` is the other half and holds the review itself —
the two stages, the comparison axes, the probe rules, the cross-session
records and the findings format. An orchestrator reads both; a `warden` spawn
preloads that one and never this.

Nothing here changed when it moved. The headings keep the `Orchestrator:`
prefix they were written with, so a reference to one of these sections names
the section it always named and only the file it names changed (#265).

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

**Then ask what the fixes left standing, with the same range.**

```
survivor-check --range <a>..<b> --exempt seal/specs/<work-item-id>/survivors.md
```

A fix repairs the coordinate a finding named. The fact the finding was about is
usually stated in more than one place, so the other statements survive and
arrive as a later round — that is contract §12, and it has been re-broken seven
times by parties that had read it. This reports every place at the range's tip
still carrying wording the range removed, names each with the standing text and
the corrected sentence it matched, and exits 1 while one is unanswered.

Two things make it the fix pass's step rather than a round's. **No round can
run it**: §2 reserves the broad gate for you, and #269 is one sentence reworded
whose pin stayed behind in a test module that was red from that commit through
two rounds and past two gates. And **the range is already typed** — it is
`close`'s own `--range`, so nothing new has to be worked out to run this.

Each report is corrected, or answered in `survivors.md` with a quote from the
standing text and the grounds. The quote is the anchor, so an exemption stops
holding the moment the text changes.

**A range that DELETES a shipped section gets one row for the whole range
(#297)**, `| Range | Grounds |`, because per-survivor rows do not scale to
that case: every sentence of the section stands in the durable copies that
are supposed to survive a deletion, and #293's range reported 153 of them,
all correct as reports and none a defect. The range is the anchor there, so
the row stops holding the moment the check runs over a different range, and
the grounds are still a written sentence somebody reads.

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

**`round-N-report.md` goes in that same commit**, because the reviewer left
it uncommitted and it is what the record was derived from. A record committed
without it leaves `Fixes checked by` pointing at a round whose report nobody
can open, which is the audit line the record exists to hold. It sits in the
same directory, so the commit that adds one has the other a line away in
`git status`.

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

**That window used to be red and is not any more (#296).** The `release` leg
failed from the draft's opening until round 1's record committed — the
declaration named the chain and `rounds/` held no record yet — and this
paragraph said so, as *the window's expected state, not a failure to chase*.
A check that is red for following the document beside it is a check people
learn to skip, so `chain_check` reads the draft state on that arm now: on a
draft the missing record prints and the run exits 0, and pressing *Ready for
review* fires `ready_for_review`, re-runs the check and fails the pull
request if the record is still missing. Nothing that can reach `main` is
exempt.

It is red once more from `close` ticking `Pass` until the verifying
round's record commits, for the reason the check prints — `Pass` beside
`nobody` on the last record — and that window is expected.

**The last record's `Broad gate` cell is read at a READY pull request
(#295).** So the sequence has one more step before the draft goes ready: run
the one full-suite pass now that the rounds have settled, and write the SHA
it ran at and the base it was compared against into the last record's cell
with `round_record.py close --broad-gate '<sha> against <base>'`. A cell
still reading `not yet` fails the pull request, and so does a SHA the
record's own `Target SHA` descends from — a run spent before the round it was
meant to seal. Work items begun before `chain_check.GATE_FROM` print instead
of failing.

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
