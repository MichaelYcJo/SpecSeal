# review chain — behavior spec

Authority for the cycle contract the `code-review` and `legacy-parity` skills
participate in, and for the review run: its bound and its end, the two records
that say what was reviewed, and the survivor sweep. Two sibling documents
carry the rest of what this one used to hold.
`docs/commit-review-gate-spec.md` is the authority for
`hooks/commit-review-gate.py`, `hooks/review-history-guard.py` and the
implementer mark. `docs/round-record-spec.md` is the authority for the rows of
`rounds/round-N.md` as the pull-request check reads them, and for the
generator that writes them. Update spec and code together.

**Two words, and they are not the same size.** A **cycle** is the mark's own
unit: one mark written, one commit, one mark gone stale. A **review run** is
the whole thing a work item goes through — up to five rounds, ending at a pull
request. A cycle is what the hook counts; a review run is what a person means
by "the review". Both were spelled "cycle", and a bound stated in one unit
read as a bound in the other.

## The cycle — the mark's unit

```
changes accumulate → review runs → reviewed-HEAD mark written → commit allowed
commit moves HEAD  → mark no longer matches → next cycle starts unreviewed
```

- **Marks**: `<git-dir>/specseal-reviewed` holds the reviewed HEAD SHA,
  written by the review orchestrator as the `code-review` skill's closing
  step. In a ported repo, `<git-dir>/specseal-parity` holds the HEAD an
  actual comparison against the original was made at, written by the
  `legacy-parity` skill. Living under `.git/` keeps both uncommitted and
  per-worktree (each worktree has its own git-dir — no cross-worktree false
  sharing).
- **One review per cycle**: fixes made after the review, before the commit,
  do not re-arm the gate. Re-review is the user's call. The parity mark
  follows the same cycle rule.

## The review run has a bound, and an end

Rounds are capped at **three**, and at **five while a 🔴 is open**.

Three is the rule. A fourth round is normally not another finding; it is the
loop failing to converge, and that is a different problem — the same reading
the 3+ Fix Rule gives a bug that keeps moving.

The exception exists because the cap counts rounds and rounds are not all the
same thing (#51). A round that turns up a defect nobody had looked for is the
shape the cap was written for: stopping is right, because something structural
is being missed. A round that turns up a **regression the last fix made** —
coordinate named, patch already run — is not. Stopping there hands over a
branch with a known open blocker and no question for anyone to answer.

| Bound | When |
|---|---|
| three rounds | the ordinary case, and the only one for 🟡 and ❓ findings |
| up to five | **only while a 🔴 is open**, and only to close it |
| stop regardless | a round opens a new 🔴 at the same site as the one it was closing — that is the structure signal, whatever the count |

**Five is a ceiling, not a target.** The moment the last 🔴 closes, the run
ends; unused rounds are not spent on 🟡 findings. Those go to
`seal/follow-up.md` or the tracker with an answerer named, exactly as
they would at three.

🔴 is not a judgement layered on top of the cap. `code-review` already grades
by what a finding requires rather than by rank, and 🔴 means *blocks merge* —
so "a 🔴 is open" is a state the review already reports, readable from the
last round record's verdict table and its `Pass` checkbox.

### The cap bounds rounds, and not the fixes of the round it stopped

<!-- specs/1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys -->
**Three and five count rounds.** What they decide is whether another round is
spawned. What happens to the findings of the round they stopped at is decided
by the rule below, and reading the numbers as a bound on fixes is what files a
verified one-line repair instead of making it.

**A run the round cap stopped may still write a fix.** Writing one spends no
round: the fixes are read the way every other round's fixes are read, by one
verifying round at their diff, and a round that opens nothing needing a fix
does not consume the cap.

**What decides between a fix and a home is who owns the unit now.** A finding
inside a unit this run's own fixes created belongs to the branch that created
it, and the branch fixes it whatever round it surfaced in. A finding in code
that stood before the run belongs to whoever owns that code, and it takes the
filing ladder at the end of this section. The evidence is already written
down: each record's `New units` row names the units that round's fixes added,
so the question is answered by reading the run's own records rather than by
judging, and it costs nobody a question.

**`New units` names Python units, so a finding in a document is answered by
the fix range instead.** `round_record.py`'s `measure` skips every prose path
whole — `.md`, `.markdown`, `.txt`, `.rst`, before both the AST pass and the
diff-line heuristic — so a round whose fixes were documents writes
`New units | none` however much the branch wrote. An empty row is therefore
not evidence that the run created nothing, and reading it as *not a unit this
run created* sends a paragraph the run wrote three commits ago down the
ladder, which is the expensive direction this section exists to close. There
the evidence of ownership is the range itself: a paragraph this run's own
fixes added belongs to the branch on the same test, read off the diff rather
than off the row.

**The question asked in its place was *when did the defect start*.** That is
the substitution to watch for, and it fails in the expensive direction — it
sends work the branch owns to a tracker nobody schedules from. Measured: round
6 of `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/`
filed five findings on the grounds that the run was capped. Re-examined
against ownership, the unit one of them named had been created by round 4 of
that same work item and the character-level oracle another named was the
branch's outright, so all five were fixed on the branch, the record was
corrected in place, and one verifying round read them.
Enforced by: nothing — no case reads the opening yet. A pin on *Three and five count rounds* beside rule 13 in `tests/test_the_rules_have_one_owner.py` would; the ownership rule after it is held by `test_the_owner_states_the_rule` and `test_every_link_names_the_owner`.

<!-- specs/1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys -->
**Two bounds end a run `capped`, and only one of them permits a fix.** Say
which one ended the run, because the answer differs between them:

| The bound | Where it is stated | What its terminal record may do |
|---|---|---|
| the round cap | here — three rounds, and five while a 🔴 is open | write fixes for what the branch owns, and have one verifying round read them |
| the reopening bound | §*The reopening — one, and then the run is capped* | commission nothing. `chain_check.py` refuses a second fix-closing record after a floor `no`, so that record closes its open findings on homes alone |

**So what `Fixes checked by` reads at a round-cap exit depends on what the
record did.** A capped record that closed nothing on a fix reads `no fixes to
check`, and it is the last record of the run. A capped record that wrote fixes
reads `round-N` and is **not** the last record — the verifying round that read
those fixes is, and that one reads `no fixes to check`. `round_record.py seal`
refuses to write `Broad gate` on a last record whose cell reads anything else,
so the reader is required by the generator and not by this document alone.
Both shapes are in the tree, in the same work item named above: its round 6
wrote fixes and reads `round-7`, and its round 7 commissioned nothing.
Enforced by: tests/test_the_reopening_is_one.py::test_a_second_fix_closing_record_after_the_floor_is_refused, tests/test_the_reopening_is_one.py::test_a_capped_run_has_a_legal_end

### The bound has a floor, and a quiet round is where it stops

**Stop when a round finds nothing that leaves the root and nothing that
crashes.** Whatever else it found is deferred with a named answerer, or becomes
an issue — the same homes the table at the end of this section gives any other
leftover.

The numbers above are a ceiling and say nothing about when to stop under one,
so the cap was spent like a budget. #81 ran seven rounds: rounds 1 through 4
each found something that loses a record, and rounds 5, 6 and 7 found none of
either kind. That is roughly an hour of agent time on the flat part of the
curve, and the curve is not one chain's luck — the most expensive round in the
flow log (63 tool calls) was also the most productive (four 🔴), and cost per
finding rose in the late rounds, where the reviewer was searching a diff it had
already read three times.

Nothing new has to be measured for it. The evidence is the round's own verdict
table, which already separates what needs a fix from what does not, and the
answer goes into `round-N.md`'s `| Loses a record or crashes |` row — the
reviewer's own, given in a line of its own, exactly as `Needs a fix` is.

**A first round is never optional, and the floor does not make it one.** #104
looked small and cost four 🔴 in round 1, three of them losing a record or
sending a person down a path that does not work. What the floor makes optional
is the round after a quiet one.

**This is not the cap's arithmetic.** The next subsection carries a rule that
reads like this one said twice, and the two decide different things.

| Rule | What it decides |
|---|---|
| A round that opens nothing needing a fix does not consume the cap | whether a round that has already run counts toward three or five |
| Stop when a round finds nothing that leaves the root and nothing that crashes | whether the next round is spawned at all, with the cap nowhere near spent |

They also reach different rounds. A round that opened nothing needing a fix has
opened nothing that loses a record either, so it meets the floor as well. A
round that meets the floor may still have opened a 🔴 in a line a person reads,
and that round consumes the cap and ends the run in the same breath.

**The verifying round still runs.** The floor ends the finding rounds, not the
run's obligation to have somebody read its last set of fixes. A record that met
the floor is followed by at most one more round record: the verifying round
defined next, at the diff of the fixes that closed it. A second one is the run
carrying on past its own stopping rule.

### The last round verifies, and what it verifies is a diff

A run ends with a **verifying round**. It is spawned after the previous
round's fixes are committed, its target is the diff of those fixes, and its
job is the answers rather than new findings: for each verdict the last round
recorded as closed, is it actually closed.

That is what a round is already good at. `code-review` says an axis marked
clean in round 1 can be broken by the fixes made for round 2, and that
inheriting the verdict is how it goes unseen. The verifying round applies the
same sentence to the last set of fixes, which is the one set that rule never
reached — see *Two records* below for what it cost when nothing did.

| | A finding round | A verifying round |
|---|---|---|
| Target | the branch, or what the prompt narrows it to | the diff of the previous round's fixes |
| Asks | what is wrong here | is each closed finding actually closed |
| Ends the run | never on its own — its own fixes are unopened | when it opens nothing needing a fix |

**A round that opens nothing needing a fix does not consume the cap.** The cap
counts rounds that found something, because it exists to stop a loop that is
not converging, and a round that finds nothing is the loop having converged.
That is the distinction the numbers above could not make: a round that found
nothing and a round whose fixes nobody read looked identical to them, and the
run ended at both.

Nothing here can loop more than once, and the bound is written rather than
argued. A verifying round that opens something IS a finding round and consumes
the cap like any other, and its fixes need a reader — which is a verifying
round again, and may open something again. The first draft of this paragraph
said there was no third case to run away; that was the third case, and #161
measured fifteen rounds through it. So the reopening is one: after a record
that met the floor, one later record may close on a fix, a second is refused,
and the run ends `capped` — §*The reopening — one, and then the run is capped*
below owns the rule, the refusal and the exit. A verifying round that opens
nothing is by definition the last one, because the run ends at it.

What it costs is one extra spawn per work item, on a surface that is a diff
rather than a branch — the cheapest round of the run. What it does not cost is
a change to the numbers above.

**This is not the rule that a round has to find nothing.** A verifying round
that raises a 🟡 the smith answers with grounds has opened nothing needing a
fix, and the run ends there. The condition is *this round wrote no code
nobody read*, which is narrower than *this round was silent* and is what keeps
the bound a bound.

**A finding located in a record is a correction, not a round.** A finding
whose `Location` is under `seal/specs/`, `seal/ledger/`, `seal/releases/` or
`seal/ledger.md` is about the run's own paperwork rather than about the tool,
and it owes no fix pass and no reader. What `chain_check` or `evidence_check`
refuses is corrected in the closing commit; what neither reads is prose,
corrected in passing or not at all. `Needs a fix` does not count it, so a
verifying round that finds only such things has opened nothing needing a fix.
In the fix table such a row closes `answered` with `corrected at <sha>` as its
grounds, never `fixed`: `fixed` is a fix word, and a fix word commissions the
reader a correction does not owe.

**Two cells, not one.** The Verdict cell holds the word alone and the
correcting commit goes in `Commit or grounds` beside it. This section
prescribed `answered — corrected at <sha>` as one cell until the release that
corrected it, while
`agents/smith.md` prescribed the two-cell shape one file over — and the one
cell is refused by `round_record.py close`, so the repository shipped a
sentence naming a spelling its own generator would not take (#341). The
verdict cell is vocabulary and the grounds cell is free text; nothing
machine-reads a SHA out of an `answered` cell, because `chain_check` skips
every row whose verdict is not a fix word before it looks for a commit.

**A repair made outside the tree takes the same shape**, for the same reason.
A finding answered by editing a ticket or a pull request body produces no
commit in the branch, so `fixed` is unusable for it — `fix_table` demands a
commit in the third cell and `close` demands that commit lie inside the fix
range. It closes `answered`, with where the repair is in the grounds (#321).

**`already deferred` is grounds, never a verdict.** The verdict cell reads
`deferred <home>` and `already deferred in round N` goes beside it. The phrase
is not in `CLOSED_WORDS` and nothing tells a reviewer to put it in that cell —
`agents/warden.md` says it about `round-N.md`'s **Deferred** table, which
`verdict_of` does not read at all — and the two records in this repository
that met the case wrote the two-cell shape already (#273 part 2).

Measured on the
last branch (#161's second comment): 33 of its 65 findings were located in
records, and the records were 55 % of the diff — a loop reviewing the tool's
own paperwork, with a reader spawned for every correction.

### The floor — `Loses a record or crashes`, and what may follow it

<!-- specs/1788472135-the-run-outlives-its-last-finding -->
**The row is read on every record**, like `Fixes checked by` and the fix
surface's two rows in `docs/round-record-spec.md`, and for the same reason:
every round has its own answer, and the run's stopping point is a fact about
the round that met the floor rather than about the last one. The floor is
stated at the top of this document, and this is what the check makes of it.

| The row | The check |
|---|---|
| absent, work item begun on or after the cutoff | **fails**, naming the row and what it buys |
| absent, work item begun before the cutoff (or with no timestamp prefix) | prints — the grandfathering those rows use, keyed to `chain_check.py`'s `FLOOR_FROM`, whose value is the id of the work item that added the row |
| `no`, or `yes — <what>` | passes |
| an empty cell, or a word that is neither | **fails** on any record — a word the check cannot read is never the reassuring reading, and `nothing anybody can see` is a sentence rather than an answer |
| `yes` with nothing after it | **fails** on any record — the cell then records that something was found and not what |
| `no`, with two or more later round records counted — the count stopping at the first that reopened the run or closed on a fix, that record included | **fails**, naming the exit. One later record is the verifying round; a second is the run carrying on past its own stopping rule. A record whose own verdicts say `fixed` stops the count exactly as a reopening does — and a reopening in second place is still a second record: the first is the verifying round, the second is the one too many |
| the ABSENT row, or the run that went past it, work item with no timestamp prefix | prints — `item_began` has no second to compare, so the cutoff is below it and those two are excused permanently. **The three malformed states above are not**: `stopping_floor` appends their errors without consulting the work item's age at all |

Only the ABSENT row and the run that went past it are grandfathered, and they
are grandfathered for different reasons. The first is the reason those rows
are: the round is over, and a record written before the rule has no
honest repair. The second is one this document has not needed before — the
repair for a run that ran three rounds too long is a round that was never
spawned, which nobody can write now. A malformed row is refused at any age,
because formatting is always the author's.

**What the count counts, and why it is not simply *the records after this
one*.** A verifying round that opens something is a finding round, so its own
fixes need a reader, and that reader is a third record — which a blind count
refuses, making the only legal end to such a run unwritable. It did: the first
record ever held to this rule was this repository's own, and the sequence its
documents required could not be written. So the count stops at the first later
record whose `Needs a fix` says the run reopened, that record included. Every
record after a reopening answers to THAT round rather than to the one that met
the floor.

**And it stops at the first later record whose own verdicts closed on a fix —
a `fixed` cell — whatever its `Needs a fix` says.** The two rows answer
different questions: `Needs a fix` is the reviewer's, *what did I open*; the
bound needs *were fixes written that owe a reader*. They come apart in one
sequence, and it happened: the reviewer answers `no`, judging a 🟡 answerable
with grounds, and the orchestrator fixes it anyway because it ships — a false
count in a ledger fragment that `fold_ledger.py` copied into the shared ledger
at the release.
The row still reads `no`, the fixes exist, and a walk reading only that row
has no terminal record it accepts: the verifying round that reads the fixes
is a second uncounted record after the floor, and ending without it is
refused both ways, `no fixes to check` beside `fixed` and `nobody` beside a
ticked `Pass`. Measured on this repository's own seventh round. The record
already carries the fact in its verdict column, and the walk reads it there.
The direction is ALLOW, one record wider in that one sequence, and it is the
cheaper mistake: the other way to satisfy the old walk was rewriting `fixed`
to `answered` over fixes that exist.
Enforced by: tests/test_the_record_is_held_to_the_floor_and_the_depth.py::test_a_record_without_the_floor_row_fails, tests/test_the_record_is_held_to_the_floor_and_the_depth.py::test_three_quiet_rounds_after_the_floor_are_still_refused

### `Needs a fix` — the row the bound above rests on

It has been in the record since draft 0.5 of `docs/review-handoff-protocol.md`
and nothing read it until the bound above needed it. It is the reviewer's own
line, copied into the cell after the colon, and it takes the floor's
vocabulary.

| The row | The check |
|---|---|
| `no`, or `yes — <what>` | passes. A reason after `no` is an answer too, and 30 of this repository's own records are written that way |
| absent, empty, or a value that is neither, work item begun on or after `NEEDS_FROM` | **fails**, naming the row and the bound that rests on it |
| `yes` with nothing after it, work item begun on or after `NEEDS_FROM` | **fails** — `yes` alone is refused the way the floor row's is, *says `yes` and does not say what*, because this is the cell the bound above restarts its count at: a bare `yes` used to read as a reopening, so three characters bought the run a round past its own floor (#138). In the count it now reads as no reopening at all, the value an unreadable cell already has — a cell the check refuses must never be the thing that quiets a refusal |
| any of those four, work item begun before `NEEDS_FROM` (or with no timestamp prefix) | prints |

**This row is grandfathered WHOLE, where the floor above and the fix range and
the fix surface in `docs/round-record-spec.md` grandfather only an absent row,
and the difference is the row's history rather than an
inconsistency.** The floor and the fix surface arrived with their checks, so a
row present on a later record was written by an author who knew one would read
it and a malformed value is carelessness. This row carried free text for three
releases with nothing reading it, so a value written before the check was
never held to a vocabulary at all — refusing those would fail records for a
rule that did not exist when they were written, which is what every
grandfathering here exists to prevent.

`NEEDS_FROM` may never be later than `FLOOR_FROM`. Between the two, the bound
above would rest on a row no record was required to carry, which is a run
failed for a cell nobody asked its author for.

<!-- specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row -->
**A bare `yes` is refused at both ends of the record, and one reader says what
the cell means.** The table's bare-`yes` row is the checker's end.
`round_record.py new` is the writer's: it refuses a bare `yes` on either
terminal line, `Needs a fix` and `Loses a record or crashes`, before the record
exists, naming the label and that the line carries no reason. The printed
bound reads the cell through `chain_check.says_reopened`, the reader both count
walks use, so the line a session reads before spawning and the gate cannot
disagree about one cell. The ruling this replaced called the row's leniency
deliberate, its reason being the verdict table below it; that was decided while
nothing read the row, and stopped being true once the floor's bound did.
Enforced by: skills/code-review/scripts/chain_check.py::says_reopened, skills/code-review/scripts/round_record.py::terminal_value

### The reopening — one, and then the run is capped

The floor's count leaves one door open, and the last branch went through it
every time. A verifying round that opens something is a finding round, its
fixes need a reader, and that reader is a verifying round again, which may
open something again. Every record the count stops at is itself a record that
met the floor, so the count restarts there and nothing bounds the chain. #161
measured fifteen rounds on one branch, with the exception used by every
verifying round of it.

**After a record that met the floor, at most one later record may close on a
fix.** That one is the verifying round that reopened the run; the record that
reads its fixes ends the run whatever it finds. There the run is `capped`:
every finding still open takes the ladder in §*Where a leftover goes — the
ladder, and why a new issue is not the default*, its verdict reads `deferred
<home>` wherever a home was found — `deferred #N` where that home is an
issue — the record's `Fixes checked by` reads `no fixes to check`, and the
pull request says `chain: capped`.

**This is the reopening bound, and it is not the round cap.** Both exits end a
run `capped`, and the one word is why the two get read as one rule. What
separates them is what the terminal record may do. This bound's commissions
nothing, because the walk below refuses a second fix-closing record after the
floor — so `no fixes to check` is true of it by construction, and the sentence
above says it of this exit rather than of every capped record. The round cap's
terminal record may write fixes for what the branch owns, and then reads
`round-N` instead; §*The cap bounds rounds, and not the fixes of the round it
stopped* owns that permission. Granting it here would name a state this
subsection's own walk refuses.

| The records after a record whose floor row is `no` | The check |
|---|---|
| none, or one, whose verdicts closed on a fix | passes |
| two fix-closing records, work item begun on or after the cutoff | **fails**, naming the second by file and the floor record it follows, and the exit above — keyed to `chain_check.py`'s `REOPEN_FROM`, whose value is the id of the work item that added the rule |
| the same, work item begun before the cutoff (or with no timestamp prefix) | prints — the grandfathering above. The rounds it names are over, and no record anybody writes now un-spawns them |

This is a second walk over the same later records as the floor's count, and
the two decide different things. The count stops at the first later record
that reopened the run or closed on a fix and refuses a second record before
that point — a quiet round after the verifying round, #81's shape. This walk
never stops: it counts every later record whose verdicts closed on a fix,
wherever it sits, and refuses the second — a run reopened twice, however the
records between are shaped. `stopping_floor`'s docstring carries the same
table.

**`round_record.py new` says which of the three states this record is in, as
it writes it.** Not a fourth document restating the rule — the record already
knows, and until #207 it did not say. The line arrives at the moment the
orchestrator decides whether to spawn again, which is the moment the check
below does not reach: it runs at the broad gate, after every round of the run
has already been spawned. One work item ran rounds 3, 4 and 5 past this bound
with both documents open, wrote *"round N of a cap of five"* into every spawn
prompt it sent, and reverted 37.9 minutes of agent time.

| What `new` prints | When |
|---|---|
| nothing | no earlier record met the floor — the cap governs, and the cap is not this line's subject — or the gate grandfathers this work item, so there is no refusal to warn of |
| `one reopening remains` | an earlier record's floor row reads `no`, no later record has closed on a fix, and no floor record's count walk has fired — a running walk with a record already spent, or a stopped walk that reached two |
| `this record ends the run` | one later record closed on a fix — or every record after some floor record was quiet, so this one is the gate's second counted record — or some floor record's count walk already reached two — stopped there, or still running past it — so the gate returns an error at that record now, before this one exists (#218; the running case is its sibling, found by round 1 of the work item that fixed it) |

The floor record it names is the **earliest** whose row reads `no` — except
in the count branch, where it is the record the firing walk **started
from**. The two are usually the same record and come apart when an earlier
floor record's own count walk has already stopped: the line then names the
later floor record, which is where the gate returns its error and the only
record the count beside it is true of. Which record the RETURNED floor is,
is a separate question, and there the answer is still the earliest, for the
reason the count above gives: keyed to the latest, it restarts at every
record it stops at and bounds nothing.

**Each walk runs from EVERY record whose floor row reads `no`, and only the
count walk needs more than one start.** `stopping_floor` is read on every
record, so a second floor record starts its walks over the records after it.
The reopening walk never stops, so a later start's hits are all in an earlier
start's and the earliest start dominates. The count walk stops, which breaks
that: an earlier walk that stopped says nothing about a later floor record's
walk, which starts fresh. Reading the earliest alone printed `one reopening
remains` at round 4 of the work item that found this while the gate returned
an error at `round-2.md` — the reopening-walk defect above, one floor record
over, and the third instance of that class on one branch.

**It reads BOTH walks, because a quiet run is bounded by only one of them.**
Floor `no`, then two rounds that neither reopened nor closed on a fix: the
reopening walk finds nothing and the count walk reaches two, so the check
below refuses the third record. Reading the reopening walk alone printed
`one reopening remains` at round 2 and invited exactly the round the gate
would refuse — #207's own defect, made by the line written to end it. A
record that reopened the run without writing fixes stops the count walk, and
then this record is not one of the counted and nothing here ends the run.

**A work item the gate grandfathers prints nothing**, and the two walks are
grandfathered against different constants — the count from `FLOOR_FROM`, the
reopening from `REOPEN_FROM` — so a work item between them has one bound
really enforced and the other only noticed. One guard for both would silence
a bound that is enforced; no guard at all declares a run capped where the
gate merely prints. Silence rather than a hedged sentence: this line exists
to bound the decision to spawn again, and where the gate will not refuse
there is no bound to state.

**Failure direction: blocks more.** A run that reopens twice is refused where
it used to pass. What it lets through, stated rather than left to be found: a
defect the second reopening would have found ships as an issue rather than as
a round. That is the trade `questions.md` Q2 of the work item that added this
chose, with the alternative on the table — removing the exception entirely
would have shipped round 7's floor bug and three Windows defects of the last
branch as issues too, and bounded nothing the count did not.

**The vocabulary the exit needs.** `deferred <home>` is a closing word and not
a fix word: `deferred #170` and `deferred seal/follow-up.md` close a finding
on the issue or the file it went to, and produced no code — so `no fixes to
check` beside them is the truth, and a last record whose every verdict reads
that way may tick `Pass`. A bare `deferred`, the word with nothing after it,
stays OPEN — the direction every verdict the checker cannot read takes. It
says something was left and not where, which is the state a `nobody` with no
reason is refused for.

### Where a leftover goes — the ladder, and why a new issue is not the default

At the bound, or earlier when a round returns nothing blocking, the change
ends the same way whether or not everything was resolved. Nothing is dropped;
each kind of leftover has a home that outlives the session.

<!-- specs/1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys -->
**A finding is filed where somebody will act on it, and a new issue is the
third rung rather than the default.** An open finding takes the first rung
that fits, read top to bottom:

| Rung | When it fits | Where the finding goes |
|---|---|---|
| 1 | the branch owns the unit, or the smith answers the finding with grounds | the diff, or `round-N.md` with the grounds. §*The cap bounds rounds, and not the fixes of the round it stopped* says how ownership is read |
| 2 | an open issue already owns the ground | a comment on that issue, and the verdict reads `deferred #N`. `docs/issues-and-milestones.md` §*An issue is its body and its comments together* is what makes a comment the way a ticket grows here |
| 3 | the finding names a party who will act on it | a new issue, labelled `from-review`, and the verdict reads `deferred #N`. Where a repository has no tracker, `seal/follow-up.md` is the same rung and takes the same test |
| 4 | it names nobody | the round record alone, with the finding named in the pull request body |

**The test is agreement, not naming**, and it is the one `seal/follow-up.md`
already applies to itself: *nobody agreed to open `X`, so nobody answers*. A
row in that file names a person with no condition attached, which is the shape
the cell takes; what decides the rung is whether anybody agreed to it. So the
cell has to name somebody the finding gives a reason to act,
and an owner written because there was nobody else to write is rung 4's
answer rather than rung 3's. That distinction is the whole of the rung, and
it is why naming is not the test: the most common value this column already
holds is the repository owner, so a rung that stopped at *a person, with no
condition* would file exactly what is filed today. Nothing new is written to
answer it. The reviewer's `## Deferred` table already carries the column —
`Who answers it` — and the ladder reads that cell, so the decision costs no
field, no verdict word and no question. A cell reading *whoever picks it up*
is the same answer as an empty one.

**What rung 4 costs, stated rather than left to be found.** A real defect that
can name nobody stops being visible in the tracker. It lives in the round
record and in the pull request body, which is durable until `settle` retires
the work item's directory at a later release — after which the pull request
body is what carries it. `seal/follow-up.md` made that trade for its own file
first, on the grounds that an unowned row is not a plan, and the repository
owner is who overturns it.
Enforced by: tests/test_the_rules_have_one_owner.py::test_the_owner_states_the_rule, tests/test_the_rules_have_one_owner.py::test_every_link_names_the_owner

<!-- specs/1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys -->
**Two refusal messages still say a refused finding becomes an issue, and the
rules above are what they lag.** `CAPPED_EXIT` in `chain_check.py`, printed at
a round-cap exit, says *every finding still open becomes an issue* and that the
record's `Fixes checked by` reads `no fixes to check` — the second half is
true only of a capped record that wrote no fixes, which the cap subsection
says. The depth exit's `DEPTH_EXIT` in `round_record.py`, printed when `close`
refuses a depth-2 unit and repeated by `chain_check.py`, says *deferred with a
named answerer, or becomes an issue*. Under the ladder either finding may take
rung 2 or rung 4 instead, so both are imprecise where they were once exact.
The depth exit's wording also stands in prose: documents, agent definitions,
skills and the round-record template. Those carriers are found by searching for
*or becomes an issue* with whitespace collapsed, not by a list. Some spell the
clause before it without a comma, and a list goes stale the first time a
carrier is added. Not every carrier points at the ladder; some state the two
homes with no pointer at all. Rewording a line a person reads at a refusal
is a gate change, which the work that wrote the ladder was scoped out of.
Whether and how to reword the pair is the repository owner's decision; the two
messages move together, and every carrier the search finds moves with them.

**What the ladder is measured against.** Filing is cheap and acting on a
filing is not, so a ladder is what keeps the cheapest act from being the
default one. Measured on 2026-09-22 with
`gh issue list --label from-review --state all`: the label carried 89 issues,
43 of them closed — 48% — and 23 of the 46 still open had been opened inside
one three-day window. The count excludes the one issue this work item's own
run filed. **The date is part of the claim**, because the label set moves:
without it a reader re-taking the query cannot tell whether the tracker
changed or the number was wrong. Re-taking it is one query rather than a
reconstruction, which is why `docs/issues-and-milestones.md` documents the
label.

Two leftovers are not findings and take no rung:

| What is left | Where it goes |
|---|---|
| A decision only a person can make | `seal/specs/<item>/questions.md`, and named in the PR body |
| An original whose behavior is plainly wrong | both texts side by side per `legacy-parity`, and named in the PR body |

Then the `sealer` takes the broad gate once — spawned with the base and the
work item, running `broad-gate` and writing the last record's `Broad gate`
cell — and the change opens as a pull request. Where the gate has to be taken
again, the cell keeps every run: the newest entry first, each `<sha> against
<base>`, the earlier ones behind it as `earlier run` — so a run at a new
commit, or at the same commit against another base, is recorded beside the
first rather than over it, while the same comparison as the newest entry
replaces that entry — and the reader still takes the first SHA-shaped word as
the run (#174).

**The chain ends at a PR, never at a merge.** Those are two mistakes at the
same spot. A run that stops at a report leaves finished work where nobody
will find it — worst when nobody was watching, which is exactly when a run
goes long. A run that merges has decided something that was never its to
decide; the commit gate asks precisely because approving is a person's act.
Between them sits the PR: complete, reviewable, and waiting.

A PR opened with open items named is the correct end state, not a failure to
finish. What makes it correct is that the items are *named* — an unresolved
finding written into `follow-up.md` and quoted in the PR body has been handed
over. The same finding left only in a session's memory has not.
Enforced by: nothing — a record rather than a rule: it states that two refusal messages lag the ladder above, which is the rule, and that rewording them is the repository owner's decision.

## Two records, and what each of them says

The mark and the round record are both "this was reviewed", and they are not
interchangeable. Reading one for the other is how three branches came to have
no readable review state at all.

| | `<git-dir>/specseal-reviewed` | `seal/specs/<work-item-id>/rounds/round-N.md` |
|---|---|---|
| Says | **this tree, right now** is reviewed at this HEAD | **that SHA, back then** was reviewed, and what came of it |
| Lives | under the git directory, per worktree | in the tree, committed |
| Travels | nowhere — not to CI, not to another worktree, not to another machine | with the branch, into the diff, into CI |
| Ages | goes stale the instant HEAD moves, by design | never — it names the SHA it is about |

**The mark cannot be committed.** It asserts something about the current HEAD,
and committing it moves HEAD, so the assertion is false the moment it lands.
That is not a limitation to work around; it is what makes the mark honest
about a moving tree.

The consequence is that the mark can answer *may this commit go through* and
nothing else. It cannot answer *did this branch pass review* — and that is the
question someone holding several unmerged branches actually has. Measured: three
branches on this repository had each run review rounds, each carried fix
commits, and none of them could be told apart from an unreviewed branch by
anything in git. The verdicts existed only in agent reports, which end with
the session.

So the durable half is the round record, and the passing half of it is the
`Pass` checkbox (`docs/review-handoff-protocol.md`). The last round's checkbox
speaks for the whole review: earlier verdicts are not archived, every one of
them needs an answer in the round that follows, so nothing can be open in
round 1 and absent from round 3.

**That closes the findings and says nothing about the answers**, and the two
are not the same claim. A finding is closed by a fix, the fix is written after
the round ends, and the round that follows is what opens it. Every round has
one — except the last, whose fixes are written by the session that then ticks
its box.

Measured on two consecutive work items here (#33). Round 2 of the first found
**seven** defects inside round 1's own fixes, which is the entire hit rate on
the one set of fixes anybody looked at, and round 2's fixes then went in
unread. The work item after it recorded the same ending in a comment
(`seal/specs/1788184145-…/rounds/round-3.md`): four findings, fixed by the
orchestrator, opened by nobody, `- [x] Pass`.

So the record carries a second field, `| Fixes checked by |`, and it names a
later round, `no fixes to check`, or `nobody — <why>`. A round cannot be its
own checker, because only a number above its own is accepted and that round's
own `Target SHA` has to be later than this one's, and the pull-request check
refuses every claim git can contradict.

`nobody` with its reason is refused nothing on any record but the last. That
is not a contradiction inside one file, and a check that fails for an honest
disclosure teaches people to write none — the reasoning `unverified_check.py`
already runs on. On the run's LAST record beside a checked `Pass` it does
fail, for a work item begun on or after the cutoff, because that pair is the
review claiming to have passed rather than disclosing anything. The refusal
table under `docs/round-record-spec.md` §`Fixes checked by` holds both halves
and what each costs.

The field records the state. What keeps `nobody` rare rather than routine is
the verifying round, which is the run's own shape and sits with the bound
above.

### When the record was written — before the fixes it commissioned

<!-- specs/1788501054-a-check-reports-clean-while-something-is-missing -->
**A round record is committed before the fixes it commissions.**
`templates/sdd-round.md` says a record is written *right after it posts*, and
until this check nothing observed it. Measured twice in one release, four
minutes and two minutes after the fix commits those records commissioned, and
both times the reviewer's drafted replacement text lived only in a report and
the next segment rebuilt it from scratch. That is the failure a build phase's
own record was built to close, arriving on the review side of the chain.

**A record written late leaves no trace.** By the time a late record is
written the fixes have landed, so its verdict cells read `fixed at <sha>` — which
is exactly what a correctly written record looks like after its own update
pass. The two are indistinguishable in the file, and distinguishable in git.

**So the check reads the ADDING commit, never the last one.** A correct record
is committed with `open` cells when the round posts and updated when the fixes
land, so its LAST commit legitimately descends from the fix; refusing on that
would fail every well-written record. The commit that ADDED the file is the
distinguishing one.

Read on every record, like the floor above and like `Fixes checked by`, the
fix surface and `Ran by` in `docs/round-record-spec.md`, and for the same
reason: when a record was written is a fact about that round, and every round
has one. The
last record is the one **least** likely to be late, because nothing follows it
to commission anything — so a check reading the last record alone would read
the one record the defect cannot reach.

| The state | The check |
|---|---|
| the adding commit descends from a commit this record's own verdict names as the fix, work item begun on or after the cutoff | **fails**, naming the adding commit, the fix, and the row — keyed to `chain_check.py`'s `ORDER_FROM`, whose value is the id of the work item that added the rule |
| **the same, and the record's `Written late` row reads `yes — <why>`** | **prints**, quoting the reason beside the refusal it relaxes. The fourth exit, and the reasoning is the subsection below |
| the same, work item begun before the cutoff (or with no timestamp prefix) | prints — the grandfathering `Fixes checked by` already uses. A merged record has no honest repair: nobody can commit it earlier now |
| the record added with `open` cells and updated to `fixed at <sha>` afterwards | passes. This is the correct shape, and the whole reason the ADDING commit is what is read |
| a verdict closing with `answered`, `withdrawn`, `not a defect` or `deferred <home>` | passes, whatever commit sits in the cell — those close a finding and produce no code, so there is no fix the record could have been written after |
| a fix commit that is an ancestor of this record's own `Target SHA` | passes — the round already reviewed that commit, so it is a fix this round did not commission. Round N+1's record is committed after round N's fixes by construction, and reading those as commissioned would fail the second round of every run |
| a fix commit this repository cannot resolve | passes — after a squash that is the ordinary state of a reviewed commit, the reading `resolves_to` gives every other consumer |
| **a `fixed` verdict that names no commit at all** | passes, and this is the commonest of the pass states rather than an edge — measured across this repository's own records, 235 cells close with a fix word, 215 name a commit and **20 do not**. `\| fixed \|` and `\| fixed — round-2 read it \|` are house style, not malformed |
| a record DELETED and re-added on the branch | judged on the **latest** add, which is the only shape producing more than one. A stub committed on time, removed, and the real record written after the fixes is what makes a late record look early, and the version anybody reads was authored at the last add. The latest add is found across a merge and under a skewed clock: a side branch that re-adds the same bytes and merges back, and one whose commits are dated before the early add, both read the re-add. A merge is never itself the add. What it costs: a record accidentally deleted and restored after the fixes is refused, and the failure names the restoring commit |
| a record with no adding commit in `<baseline>..HEAD` | passes — it arrived before the base, and nothing is claimed about it. The same *no claim* the reachability requirement already makes for a record the pull request does not touch. This is also what a base moving under a long branch produces: the record's own adding commit leaves the range and the commit that UPDATED its verdicts stays inside it, so reading *any commit that touched the file* would refuse a record for doing exactly what a correct record does |

**So the refusal's reach is the commit a cell happens to carry, and that is a
limit rather than a choice about which column to read.** A record whose
`fixed` cells name no commit at all — the bolded row above — is invisible to
it however late it was committed. Two answers were weighed and the cheaper one is not a check:

- **Refuse a `fixed` cell that names no commit.** It would be a sixth refusal,
  owed its own cutoff and its own subsection, refusing a spelling 20 of this
  repository's own cells already use — and the value it would add is reach
  over records whose authors were never asked for the commit.
- **Ask for the commit where a person writes the cell.**
  `templates/sdd-round.md` does, beside the vocabulary, with the reason: a
  reader six months on has no other route to the change, and this refusal
  cannot see a cell without one. Records written afterwards carry it; the
  reach grows as they land, and nothing red is inherited.

The second is what shipped. What it costs, stated rather than buried: the
reach is a convention rather than a guarantee, so *this record passed* means
*no cell in it named a commit the record descends from* and never *this record
was written on time*.

**What a rebase does to this, stated rather than left to be found.** The
refusal reads a commit relationship and a rebase rewrites commits, so the
question is which direction it can move a verdict. The adding commit is read
in `<baseline>..HEAD` rather than in the repository's whole history, and a
rebase replays a branch's commits in order — so a record added before its fix
on the branch is still added before it afterwards, and a passing record cannot
be turned failing. What a rebase does change is the SHA the verdict cell
names: the rewritten fix has a new hash while the cell still holds the old
one, which resolves to nothing in a fresh clone and to an unreachable object
in a local one. Either way no claim is made, so a rebase can turn a **failing**
record passing.

That is the safe direction of the two, and it is taken knowingly. Closing it
would mean matching rewritten commits by patch id, which is a second mechanism
for a case nobody has met — where the cost of the other direction is an honest
record refused for a rebase its author did not connect to the failure.

**The fourth exit — a record that says why it was written late.** The refusal
above had three repairs and not one of them was honest: rewrite history so the
adding commit moves, merge over the red line, or invent a waiver nobody wrote
down. Work item `1789034970` met all three, took none, and ended with a pull
request red on a line no later commit could clear, its run capped and its
reverted fixes redistributed across six issues.

So the record can answer. `| Written late | yes — <why> |`, written by
`round_record.py new --written-late "<why>"`, and the check **prints** the
refusal with the reason quoted instead of failing on it. Four things buy
nothing and are judged exactly as they were before the row existed: the row
absent — which is every record written before this — the cell `no`, a bare
`yes`, and a value outside the vocabulary. A bare `yes` is refused at the point
of writing too: a relaxation bought with an empty cell is a waiver with no
author, which is the third of the three bad exits under a flag.

**The flag is not the only way the row gets there, and at the refusal it is
the wrong one.** `new` writes the row as it writes the record, which is a
moment that has already passed for anybody reading the refusal — their record
is committed, or the refusal would not be theirs to read. The check reads the
cell and never asks who wrote it, so the row may be added by hand and
committed like any other correction to a record already on the branch. The
refusal itself says so, because the person standing in that state reads it
there and nowhere else.

**It prints rather than passing in silence,** the same shape the grandfathering
row takes and for the same reason. The state is what the check exists to
surface, and what the reason buys is that the run can end and that the fact
survives in the record rather than in a session that has ended.

**It owes no cutoff of the `ORDER_FROM` kind, and the direction is why.** Those
cutoffs exist because a check whose first production act is red on history
nobody can fix is a check people learn to skip. This is a **relaxation**: no
record that already exists is judged more harshly for lacking a row nobody
asked its author for.

**`round_record.py new` is where a person learns they may need it.** It
compares the commit the round read against the branch's HEAD and prints the
commits between with their subjects where they differ — the last moment in the
sequence when anybody can still act, since the fix pass is a spawn with no
command for a check to sit on. It refuses nothing there, and that is measured
rather than chosen: over this repository's own pre-squash branches, 40 records
of 152 have a `Target SHA` that is not their adding commit's first parent, and
the commonest cause by far is the round's own paperwork committed between the
review and the record. A refusal would have fired on one correct run in four.

What no check can see is a record committed on time that carries nothing: the
file exists before the fixes and says only what the round found. This refusal
is about ORDER alone, and issue #150's own comment asks the narrower question
beside it. The next subsection answers it.
Enforced by: tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_record_added_after_its_own_fix_fails_after_the_cutoff, tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_record_updated_in_place_when_the_fixes_landed_passes, tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_re_add_merged_back_from_a_side_branch_is_the_latest_add, tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_re_add_on_a_side_branch_with_an_older_clock_is_the_latest_add

### What the record carries — a declaration, and why no check reads it

Writing the record first is necessary and not sufficient, and the measurement
that says so was taken on the round after the one above. `1788491830`'s round
2 was written **before** the fix pass it commissioned — the thing the refusal
asks for — and its executed-probes table reads:

> the round's proposed fixes for 🟡 6 and 🟡 7, unmutated then under three
> mutations each · green, then red in every case

**The record contains none of that code.** So it asserts a verification and
does not carry its artifact, and the implementer wrote its own replacement for
the second time running. It is the ticket's own opening observation arriving
one level in: a record that says it verified something it does not carry looks
complete.

**The rule.** An `Executed probes` row whose subject was a **proposed
replacement** rather than a command carries the replacement itself, in the
record, in a fenced block. A command is reproducible from its own text; a
patch is not. `templates/sdd-round.md` carries it beside the column.

**Whether it is checkable was asked before it was assumed, and the answer is
no.** Three readings were tried and each fails in a way this document or
`docs/round-record-spec.md` already refuses elsewhere:

| The check somebody would write | Why it is not written |
|---|---|
| a probe row naming a fix, with no fenced block anywhere in the file | *naming a fix* is a keyword match over free prose — an enumeration over an unbounded domain, the closing the arrow's and the comma's limits in `docs/round-record-spec.md` already decline. The column is a sentence a reviewer writes, and a rule about which sentences mean *patch* is a rule about English |
| every record carries at least one fenced block | fails every record whose probes were all commands, which is most of them. A check that refuses the ordinary case teaches people to write a block that says nothing |
| the block's content appears in the diff | the record is written BEFORE the fixes by the rule above, so at that moment the replacement is in no diff at all. Requiring it later would require re-editing the record after the fixes land, for a claim that is already true |

So it stays a declaration, the shape `New units`' depth and `Ran by`'s
provenance already take in `docs/round-record-spec.md`: written by the party
that knows, read by the party that holds the artifact beside the record — here
the fix pass, which is the one that would otherwise retype it. That is the
third declaration, the other two being that document's, and the count is
worth stating: what a check cannot reach, a reader
does, and saying which is which is what keeps the checks honest.

**The record is written by `round_record.py` now, from the two agents'
reports, and that changes who makes the declaration and not whether it is
one.** `new` copies the reviewer's `Executed probes` table row for row from
its report, so the declaration above is the reviewer's, made in the report,
and the generator carries it into the record unread, together with every
fenced block under that table — the replacement a probes row owes — and
nothing else of the section (`questions.md` A5 of the work item that added
the generator, narrowed by its round 2). `close` applies the implementer's fix
table. No orchestrator prose sits in a parsed cell.

**A moratorium for 0.8.x: no new parsed field in `round-N.md` and no new row
the ledger must carry.** Every field this document and
`docs/round-record-spec.md` describe arrived with a checker arm, a template
row, a protocol row and a cutoff, and each arm cost
rounds of the branch that added it. The work item that added the generator
added a subcommand and a verdict word — `deferred <home>` — and no field. What
a 0.8.x work item finds it needs goes to the tracker for the release after,
with the measurement that says a field is what it needs.

## The survivor sweep — a corrected sentence standing somewhere else

A fix corrects one coordinate. The fact behind it is usually written down in
more than one place, and the copies nobody touched come back as the next
round's finding. This is the check that names them.

<!-- specs/1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks -->
**`survivor-check --range <a>..<b>` reports every place in the tree still
carrying wording the range removed**, naming the path, the surviving sentence
and the corrected sentence it matched. It is run by the party whose range it
is about — the fix pass, and the implementer's verify phase — because nothing
downstream can run it for somebody else's range. A survivor that is a
deliberate carrier is exempted by a content-anchored row in the work item's
own `seal/specs/<id>/survivors.md`, so the exemption stops holding the moment
that text changes.
Enforced by: tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_reworded_sentence_reports_the_pin_it_left_behind, tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_report_names_the_sentence_that_was_corrected_too

<!-- specs/1788912166-red-for-following-the-documents-green-for-ignoring-one -->
**A range that removes a shipped section whole takes one row for the range
instead of one per sentence.** Every sentence of a deleted section stands in
the durable copies that are supposed to survive a deletion, so the sweep
reports all of them and every report is correct — one real range reported
153. Writing 153 rows is not an escape anybody takes, and the alternative to
a range row is turning the check off. The row is anchored on the range **and**
on the work item whose `survivors.md` holds it, so it cannot become a
standing *check nothing*.
Enforced by: tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_whole_range_row_excuses_the_survivors_of_that_range, tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_whole_range_row_does_not_reach_a_different_range

<!-- specs/1790174139-survivors-md-silences-what-it-quotes -->
<!-- specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording -->
**A declaration in `survivors.md` speaks to its own work item's runs and to
no other.** A file anywhere under `seal/specs/<id>/` belongs to that work
item, so a range row filed one directory deeper than the layout is printed
as `not yours` over a range that touches nothing there, instead of keeping
the unbounded reach the owner check exists to refuse. A range row that no
longer resolves prints `unresolved` only to a run that could have used it —
one whose range touches its work item, or one handed a file from outside any
work item. Every shipped `survivors.md` names a release branch deleted at
the release, and three such lines printed on every pull request and every
sealer run of one release, addressed to nobody. An unresolved row excuses
nothing whether printed or not, so leaving the line out costs no allow. In
local mode, where the owner is never in a range's diff, it is the `Branch`
row of the work item's `routing.md`: the row holds where the tip is on that
branch and on no local branch it was cut from.
Enforced by: skills/code-review/scripts/survivor_check.py::whole_range, skills/code-review/scripts/survivor_check.py::on_its_branch, tests/test_a_corrected_sentence_survives_elsewhere.py

<!-- specs/1789211172-a-round-record-disarms-survivor-check -->
**A round record is outside the sweep's corpus on both sides.** A record is
the write-up of a finding rather than a carrier of the claim, so a sentence
*removed* from one is not corrected wording any more than a sentence
surviving in one is an uncorrected copy. Excluding only the added side left
the check able to name a coordinate nobody should be asked to correct, which
is worse than not looking: a false name spends a round.
Enforced by: tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_record_of_a_past_round_is_not_a_survivor, tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_round_record_the_range_edited_does_not_become_a_source

### What a draft is excused, and what it is not

The same work item settles an asymmetry that runs through every arm of the
pull-request check, this document's and `docs/round-record-spec.md`'s.
**A draft pull request is not a request to merge**, so an arm whose subject is
a review still in progress prints its state instead of failing — the record
count is one of those, the way `Pass` already was. Pressing *Ready for
review* fires the event, the workflow re-runs, and the arm applies, so nothing
that can reach the default branch is exempt.

What a draft does **not** excuse is a claim that is wrong at every stage. A
record naming a checker the repository does not have, and a `Broad gate` cell
reading `not yet` or whose newest entry names a SHA that precedes that
record's own `Target SHA`, are both refused on a ready pull request and each says which of
the two it is — one is the run that never happened, the other the run spent
before the round it was meant to seal.

### What the sweep reads, and what it counts as written

<!-- specs/1790174139-survivors-md-silences-what-it-quotes -->
<!-- specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording -->
**The sweep reads only wording that still instructs somebody, and it reads
it the same way on both sides of the range and in the pool.** What is left
out is left out by its shape, never by a list of files. A file under a work
item that records a past state is out: a round record, the work item's own
`survivors.md`, and everything under its `phases/`. A released section of
the root `CHANGELOG.md` — every line under a heading that names a version —
is out, and so is a fragment whose fold marker stands in `CHANGELOG.md` at
the tip, because a released entry is not rewritten;
`## Unreleased` and an ungathered fragment stay in. In a `.py` file only
comments, docstrings and string literals are wording, every other token ends
a sentence, and a file the tokenizer refuses is read whole. Each of these
cost a check that went green by finding nothing or red over something
nobody could correct. A committed `survivors.md` subtracted the survivors
it quoted before `--exempt` was read and diluted the rest under the floor:
on three pull requests of one release, 36 rows were written and 7 were
consulted. Six of the twenty-one places the next release's four ranges
reported were function bodies matched on loop and `if` shapes.
Enforced by: skills/code-review/scripts/survivor_check.py::records_a_past_state, skills/code-review/scripts/survivor_check.py::a_gathered_fragment, skills/code-review/scripts/survivor_check.py::python_prose

<!-- specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording -->
<!-- specs/1790221963-a-release-writes-the-gathered-text-back -->
**Only wording the range itself wrote is subtracted from what it removed.**
That subtraction is what makes the score mean *removed*, so the question is
always whose writing a sentence is. A sentence moved verbatim to another
path, by a file moved whole or a document split, is held and never written,
because a move changes no sentence's author: a pure move removes nothing and
is silent for that reason, and a move that rewords one sentence measures it,
where git's rename detection hid both. A fragment's text gathered by a
release is held and never written, because the fragment's own branch wrote
it. Written, it subtracted the survivor a correction in the same commit left
in another file whenever the release also lost a sentence, and renaming
`## Unreleased` or rewording an entry as it is released both lose one. It
still splits a sentence `CHANGELOG.md` itself lost, and nothing else. A
release that loses no live sentence writes nothing it put under a version
heading, and that guard and the gathered-text filter are pinned by separate
cases, because either alone kept the shape the ticket first named green.
Enforced by: skills/code-review/scripts/survivor_check.py::corrected, skills/code-review/scripts/survivor_check.py::newly_released, skills/code-review/scripts/survivor_check.py::paired_across_paths

## Non-goals

- No Stop-hook turn blocking (v0.2): high false-positive cost in sessions
  that legitimately end without review; the commit gate is where an unreviewed
  commit is stopped and the choice put to a person. It is not a hard stop, and
  was never meant to be: the first attempt in a session denies and asks which
  way on, every attempt after that is a prompt where approving is the waiver,
  and `[no-review]` as a bare word silences it outright. Anyone who can answer
  a prompt can commit — the same limit `README.md` §Limits states.
- The gate does not verify review *quality* — only that the cycle carries a
  review mark. Quality lives in the `code-review` skill's procedure.
