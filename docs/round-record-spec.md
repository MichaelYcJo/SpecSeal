# round record — behavior spec

Authority for the rows of `seal/specs/<work-item-id>/rounds/round-N.md` as the
pull-request check reads them, one section per row, and for
`skills/code-review/scripts/round_record.py`, the generator that writes them.
What sends a work item's records to this check is
`docs/commit-review-gate-spec.md` §*The declaration, and where the check went
instead*. The rows the review run's bound rests on — the floor, `Needs a fix`
and the reopening — and the record's own two subjects, when it was written and
what it carries, are `docs/review-chain-spec.md`'s. Update spec and code
together.

## `Pass` has to be checked, and a draft is the way to open one that is not

The chain runs **before** the pull request in this design — smith, then
warden, then the PR — so a checked `Pass` is the normal state of a work item
by the time one opens. An unchecked one means the chain was skipped or has not
finished, and neither is a state to ask for a merge in.

| The pull request | An unchecked `Pass` |
|---|---|
| ready | fails. The review did not finish, and the pull request says it did |
| draft | passes. A draft is not a request to merge, and a review still running has to have somewhere to be |
| not visible to the check at all | judged as **ready** |

That last row is the decision, and it is deliberately the strict one. The
draft state is read from the event payload the code host writes to disk, so a
run outside a pull-request event — a session running the check by hand — has
no pull request to read. Judged as a draft, "no pull-request context" would
become the quietest way past this check that exists, quieter than
`[no-review]`, which at least stays in the command where history keeps it. An
override flag was considered for the same case and rejected for the same
reason: an escape anyone can type is the same hole with a name.

What it must not do is pass in silence, so the check prints which state it
assumed and where it read that from, on every run.

**What it still cannot see** is whether the review was any good. A checked
`Pass` is a claim made by whoever wrote the round record. What is refused is
the claim that contradicts the table underneath it — the same limit the
commit gate has always carried.

## `Fixes checked by` has to name a checker the repository can confirm

<!-- specs/1788212517-the-last-rounds-fixes-are-reviewed-by-nobody -->
The draft excuse does not reach this row. `Pass` is excused in a draft because
a review still running has not reached its verdict; a record naming a checker
it does not have is wrong at every stage of a run.

| The cell says | The check |
|---|---|
| the row is absent | **fails.** Adding it is always available to the author, which is the line this check has always drawn |
| `round-N`, above this record's own number, that record is committed, and its own `Target SHA` is later than this record's | passes |
| `round-N`, at or below this record's own number | **fails** — the checker is this round, or one that ran before the fixes existed. That is the fixer certifying its own work, which is the state #33 measured |
| `round-N` above this record's number, whose `Target SHA` is the same commit this record's names or an ancestor of it | **fails** — the number is later and the review is not. Rounds are cheap to number and expensive to run, and a round that read what this round read opened none of the fixes that closed it. Where either row names two commits, the NEWEST on each side is what is compared |
| `round-N` naming a record git does not carry | **fails** — a claim git contradicts |
| `no fixes to check`, with no verdict cell closing on a fix | passes |
| `no fixes to check` beside a verdict cell reading a fix word | **fails** — a contradiction inside one file, the shape already refused for `Pass` beside an open 🔴 |
| `nobody — <why>` | prints on every run. **Fails** beside a checked `Pass` on the run's last record, for a work item begun on or after the cutoff below; passes everywhere else |
| `nobody` with nothing after it | **fails.** The reason is what makes the state readable; without it the cell records that something is missing and not what |
| anything else, `the session that wrote them` included | **fails**, naming the three values. Read loosely, a session's own name would pass as an answer, and that is precisely the state this field exists to refuse — the direction `CLOSED_WORDS` already takes for a verdict cell |

**The `<why>` is not one sentence, and `close` writes the second.** `new`
lands the cell on `nobody — the fixes are not yet written`, which is true for
as long as the round is running. `close` then applies a fix table, writes the
commits into this record's own verdict cells, and used to leave the cell
alone — so the record said the fixes were not written beside the commits that
wrote them (#273 part 1). It now rewrites the reason to say they are written
and no round has opened them. `nobody` is unchanged, because a checker has to
be a later round and none exists at that moment; and a cell already naming a
`round-N` is a later round's reading, which `close` does not touch.

Nothing reads the reason, which is why this is a change to a sentence rather
than to a gate. Measured over both arms before it was written: `checked_by`
splits `nobody` from its reason and requires only that a reason exist, and the
fix-surface arm below gates on `CHECKER_RE` — which matches `round-N` and
neither spelling of `nobody — <why>` — before applying `says_not_yet` to the
SURFACE row, a different row that `close` fills from the diff.

**A capped run's last record is what makes it worth correcting.** Every other
record's cell is replaced by the next round's `new`. That one has no next
round, so whatever stands in it stands permanently, and a permanently false
reason is read by whoever opens the record.

Two of those deserve their cost written down.

The first is `nobody — <why>`, and it is a disclosure rather than a claim. A
check that failed for an honest disclosure teaches people to write none, which
is the reasoning `unverified_check.py` already runs on, so the cell prints
wherever it appears and on any record but the last it is refused nothing.

What it may not do is stand beside a checked `Pass` on the run's last record.
That combination is the review saying it passed, and a run whose final fixes
nobody opened has not passed — #33 measured the one set anybody did open and
found seven defects inside it, which is every defect there was to find.

**The refusal reaches work items begun on or after the cutoff, and no others.**
The cutoff is a unix second, compared against the one in the work item's own
directory name, and its value is the id of the work item that added the rule
(`chain_check.py`'s `STRICT_FROM`). One number serves every repository: a fresh
install creates every work item after it, and a repository updating the plugin
has exactly its pre-existing items excused.

Why grandfather at all. A record written before the rule existed is usually
merged and has no honest repair — writing a `round-4.md` for a review nobody
ran fabricates one, and unticking `Pass` fails the ready-pull-request rule
instead. A check whose first production act is red on history nobody can fix
is a check people learn to skip, and skipping loses the records it could have
caught in exchange for the ones it never could.

What it costs is stated rather than left to be found: an old work item
reopened years from now still writes records under its original id and stays
excused. That is taken knowingly, rather than closed with a second rule about
how old is too old.

Nothing after the cutoff is stuck. One verifying round at the diff of those
fixes closes it, and a round that opens nothing needing a fix does not consume
the cap — so the way out costs no round, which is what the failure says.

The second cost is the scope. This is read on **every** record, where `Pass` is
read on the last one alone, and the two differ because the two facts do:
`Pass` is a verdict on the whole review and the last round's speaks for it,
while this is a fact about one round's own fixes and every round has one.
Reading only the last record makes `round-N` unreachable — a checker has to be
later, and the last record has none. What that costs is a repository updating
the plugin: every record in a work item whose declaration the pull request
touches needs the row, not just the newest.

## The finding id — a bare integer, behind an optional severity marker

The `#` cell of the verdict table, and of the `## Fixes` table that answers
it, holds **a bare integer**: an optional severity marker, then digits and
nothing else. `1`, `🔴 2`, `⬜ 13` are the shape; `R2-1`, `1-1`, `1b`, `A2`
and `r3 🟡 2` are not.

| The cell | What happens |
|---|---|
| digits, with or without a marker in front | read as that finding |
| **no digit, and the cell says the row commissions nothing** — `carried`, `🟢 fix-surface` | in the **verdict** table, copied through, never keyed, never asked for a closure, never counted toward `Pass`. In the **`## Fixes`** table, refused — there the row IS the commission |
| **no digit, and the cell is empty or carries 🔴 or 🟡** | **refused**, naming every such row. Those two severities mean somebody owes the row an answer, and an empty cell says nothing at all — either way the cell does not say the row commissions nothing |
| anything else | **refused**, naming the format and quoting **every** offending row of the table |
| two rows that resolve to the same integer | **refused**, quoting **both** rows |

Both readings happen at `new` as well as at `close`. `new` used to copy the
`#` cell through `copied_row`, which validates nothing, so a numbering the
reviewer chose surfaced two commands later at the orchestrator — one hop from
either agent that could have avoided it.

## A verdict row that commissions nothing

A row with no id is a shape reviewers reach for, and the evidence for it is
**seven rows**. Measured over the 207 committed records that parse, 51 of
1,989 verdict rows carry a `#` cell with no digit — and **44 of those are a
severity marker and a single letter**, `🔴 A` through `🟢 O`, which is a
finding id written in the wrong alphabet rather than a row commissioning
nothing. Seven are this shape: `carried`, `🟢 fix-surface`, `🟢 fragment`,
`🟢 grep`, `🟢 overview`. Neither `✅` nor a bare em dash occurs in a committed
record at all; the 21 bare em dashes are in reviewers' **reports**, which is a
different corpus. Three kinds:

- **a confirmation** this round verified and did not open;
- **an earlier round's closure**, carried into this round's table;
- **`❓ out of verified scope`**, the reviewer looking and not judging.

None can be referenced by a fix table, because none commissions anything. The
old rule made a reviewer number all of them, so a round that opened six
findings and confirmed six more read back as a twelve-finding round — and the
count is what a later round and the pull request read.

**An earlier round's number goes in the Finding cell**, which is prose:
`| 🟢 | round 2's finding 1, re-read | … |`. In the `#` cell it is digits, and
digits there are an id — `round 2's 1` keyed as finding **2** under the reader
that took the first digit run, colliding with this round's own 2.

**A carried closure is one worked row, and the row carries three
requirements** (#437) — the reviewer's two files, `agents/warden.md` and
`skills/code-review/SKILL.md`, show the same row:

```
| 🟢 | round N's blocking finding is closed — <what> | <location> | confirmed | <grounds> |
```

A bare marker in `#`, because the row commissions nothing and an empty cell
is refused. The verdict word `confirmed`, never `fixed`: `closed_with_a_fix`
reads `FIX_WORDS` across every row of the table, so a `fixed` carried forward
makes the record one that closed on a fix, which the reopening rule refuses
at the cap with no way forward the documents describe. And no 🔴 anywhere in
the row: `open_blocking` selects on the glyph in every cell, so the inherited
severity is written in words. #437 measured it at its filing, over the work
items then holding two or more records: three last records read as
closed-with-a-fix, and every one was a carried `fixed`. The count is the
ticket's and is not repeated here — it moves with every record the tree
gains, and a number without its tree state is not a coordinate.

**The severity is read as well as the `#` cell, and that is not decoration.**
A row admitted here is never keyed, never asked for a closure and never
counted toward `Pass` — so a `#` cell alone deciding the question ticked
`Pass` over an open finding, and the record then asserted that a review
passed while its own verdict table said otherwise. Measured: `| 🟡 A | … |
open |` came through `new` at exit 0, silently, with `Pass` checked, and
nothing downstream caught it because `chain_check.open_blocking` reads only
🔴 rows. All 26 no-digit cells carrying 🔴 or 🟡 in the committed records are
genuine findings.

**The record is read in two cells, not one.** The `#` cell says a row
commissions nothing; the Verdict cell can say it is open in as many letters.
Reading only the first admitted six shapes whose Verdict cell read `open` —
three of them carrying no severity marker at all — and each was written into a
record with `Pass` ticked over it. So a row whose Verdict cell reads `open` is
refused whatever its `#` cell says.

That is a match on the word — ended by a space, a comma, or nothing, the
boundary `verdict_of` uses for its own vocabulary, so `open — deferred` and
`open, comment only` are reached and `opened` is not — rather than a
vocabulary test, and the difference is what makes it free. `verified` is in no
vocabulary and therefore reads OPEN, so refusing everything outside
`CLOSED_WORDS` would refuse every confirmation row — one refusal traded for
another. Refusing the word `open` refuses none of them: of the 25 admitted
no-digit cells in the committed records, not one reads it.

The boundary is spelled out in `round_record.py` rather than borrowed from
`chain.SEPARATORS`. The shared constant is six characters wide and has five
other readers, so borrowing it made `open-ended question` and `open: see 5`
read as the open verdict — and tied what counts as open to a constant any of
those readers may widen.

**The direction this fails in, stated.** What is left takes two mistakes in one
row, in two different cells: a reviewer who writes 🟢, ❓ or ⬜ on a row that IS
an open finding **and** words its verdict as something other than `open`. That
row still writes a finding no fix table will be asked to close, and `close`
exits 0 over it. The other mistake — numbering a confirmation row — costs an
inflated count in one record, and the change is toward that one.

**The verdict word was ruled out once, and the ruling was too wide.** A
confirmation row reads `verified`, which is in no vocabulary and therefore
OPEN, so a test of the form *anything not closed* would refuse every
confirmation — one refusal traded for another. That is an argument against a
VOCABULARY test and not against reading the cell, which is why the rule above
reads one word and composes with the `#` cell rather than replacing it.

**`❓ out of verified scope` is a closing verdict**, in `chain_check.py`'s
`CLOSED_WORDS` and in neither `FIX_WORDS` nor `HOME_WORDS` — it closes without
commissioning, so nobody is asked to read fixes it did not produce. None of the
three words a fix pass may write is true of it: there is no defect to fix, the
round explicitly did not settle it, and nothing was deferred from a round it
was never in. #353 measured the cost twice inside one run: `close` refused the
row for want of a fix table entry, the orchestrator gave it `answered`, and the
record then said the round had settled the one check neither round ran. The
next round found exactly that and could not close its own copy except by
replacing the marker a second time, in a different word.

A severity marker leads a verdict cell and is not part of it, the same rule the
`#` cell has always used. Applied to all 1,989 committed verdict rows, stripping
a leading run of non-word characters changes the reading of exactly one cell,
and that cell is this one.

**The rule exists because the reader used to guess.** `round_record.py` took
the first digit run anywhere in the cell, so `R2-1` and `R2-2` were both `2`
and a reviewer who numbered eight findings `R2-1` … `R2-8` — the round in the
id, so a finding stays unambiguous when three rounds are read side by side —
got *the fix table has two rows for finding 2* out of a table holding one
`R2-1` and one `R2-2`. The first read is that the table is malformed, not
that the ids are, and with eight rows and no coordinate the pair had to be
found by hand (#227).

**The refusal is the repair rather than an accepted prefix, and the corpus is
why.** Every committed `round-N.md` was run through both rules before the
format was fixed: of 130 that parse, 82 pass under either, 46 already refuse
today, and 2 pass today only by miscounting — `r3 🟡 2` keys as finding **3**,
out of the `3` in `r3`, and `🟢 round 2's finding (🟡 4)` keys as **2** where
the cell names 4. So the rule takes away two wrong answers and no right one.
Accepting a prefix instead would make two rounds' findings legal in one table
and turn the `{number: …}` key that `close` threads through `unknown`,
`missing`, `already` and `depth_two` into a two-part key, for a shape no
record actually uses.

**The round is already in the file name**, `rounds/round-N.md`, which is what
the prefix was reaching for. A record read beside two others is a record whose
path says which round it is.

**Where the numbering is chosen is where the rule is stated**, not only at the
point of refusal. The reviewer picks the numbers in
`skills/code-review/SKILL.md` §*Findings format*; the fixer copies them into
the fix table from `skills/implement/SKILL.md` §5. Both say bare integer, and
so does `templates/sdd-round.md` where the column is defined — because the
refusal lands at the orchestrator, one hop from either agent that could have
avoided it.

## The fix range — `Fix range`

A row that states the commits a round's fixes were measured over, written by
the generator that already resolved them and read back here against the tree.
It is `Contract changes`'s neighbour in the field table and its model, and it
exists for a narrower reason: **a record is written once and the tree keeps
moving.** `evidence-check` does that job for the ledger, over content anchors,
and the records were left out of it (#344).

What the row closes is one measured class. A fix table states its range in
prose, and `HEAD` is not a commit — it resolves, so the sentence stays
readable while meaning a different set of commits every day. Three records of
one work item said such a range, which is the rate that makes it a rule rather
than a correction. There is no convention in that prose to enforce, which is
why the authoritative statement moves into the record instead of a parser
being pointed at the prose.

**The measurement, as a command rather than as a number.** A count over prose
depends entirely on what counts, and this paragraph first stated one with a
date and no method — three readers then produced three different answers from
it, which is the rule in
`seal/ledger/1789621028-nothing-reads-a-record-against-the-tree.md` R7 broken
in the document that states it. So the method is the claim:

```sh
for f in seal/specs/*/rounds/*-fixes.md; do
  head -8 "$f" | grep -oE '`[0-9a-f]{7,40}\.\.[A-Za-z0-9@_/.-]+`' | head -1
done
```

One backticked range from each file's first eight lines. At `56945007`, the
commit this work item was cut from, it prints **15** ranges over **39** files,
**5** of them ending `HEAD`, in **12** distinct sentence forms — the forms
counted by replacing the range with a placeholder and taking the first 40
characters of the line. At this work item's own tip it prints **4** ending
`HEAD` and the other three figures unchanged, because the work pinned one of
them.

**That the same command gives 5 and then 4 is the point, not a caveat.** A
figure here is reproducible against a named command AND a named tree state,
and against nothing less. A different reading of *stating a range in their
first eight lines* — one that counts unbackticked ranges, or ranges below the
eighth line — gives a different count and is not wrong; it is a different
question, and naming the command is what lets the next reader tell which one
was asked.

**Both halves are read, because either alone passes what the other catches.**
The ends say WHICH commits and `round_record.py`'s `parse_range` refuses a
moving one at either end, so a row written after this rule is pinned by
construction. The count says HOW MANY, and it is what catches a row written or
repaired by hand: a range whose ends still resolve while its count disagrees
with the tree is what a moving end leaves behind once it has stopped moving.

| The row | The check |
|---|---|
| `Fix range` absent, work item begun on or after the cutoff | **fails**, naming the row and what it buys |
| absent, work item begun before the cutoff (or with no timestamp prefix) | prints — the same grandfathering the rows above use, keyed to `chain_check.py`'s `RANGE_FROM`, whose value is the id of the work item that added the row |
| `none`, with or without a reason | passes. A round that commissioned no fixes has no range, and this is the value the row starts at |
| `none — the fixes are not yet written` — the template's own pending words — beside a `round-N` in `Fixes checked by`, work item begun on or after the cutoff | **fails**, naming both cells (#436). A later round opened these fixes, so they exist, and the cell contradicts its own file the way `no fixes to check` beside a `fixed` verdict does — the refusal `fix_surface` already makes on its own two rows, which took the same pending value from the same line of the generator. Beside `nobody — <why>` or `no fixes to check` the pair is untouched: nothing has opened the fixes, or there are none. Before the cutoff it prints, under the row's own grandfathering — no cutoff of its own, because the row has carried the pending value from birth since it shipped and zero committed records at or after `RANGE_FROM` hold the pair |
| an empty cell | **fails** on any record — a row that says nothing answers nothing |
| a value naming no readable `` `<a>..<b>`, N commits `` | **fails** on any record, quoting the cell. A present cell nobody can parse is always the author's to fix, where a row that did not exist when the record was written is not |
| both ends resolve and the count matches `git rev-list --count <a>..<b>` | passes |
| both ends resolve and the count differs | **fails**, naming both numbers and saying to read `git log --oneline <a>..<b>` — and that if the ends are what moved, the ends are what to correct |
| either end this repository cannot see | prints. A feature branch squashes into its release branch and the squash keeps none of the branch's own commits, so a merged record's fix commits are ordinarily invisible. `Target SHA` falls back to `carried_by_a_pull_head`; a range has no equivalent, because a pull head carries the commits and not the arithmetic between them |

**What the row cannot see, stated rather than left to be found.** A range whose
ends resolve and whose count is right can still be the wrong range — the fixes
may have landed elsewhere. Nothing compares the range against the fixes, and
nothing can here: `fix_surface` measures the surface from this same range, so
the two agree by construction rather than by checking each other. What is
closed is the narrower thing #344 measured, a range that stops meaning what it
said.

**The grandfathering is the checker's and not the generator's.** The table
above is what `chain_check` does at the pull request. `round_record.py close`
has no equivalent and should not grow one: it REPLACES this row rather than
inserting one, because a record's field order is the template's and a `close`
that inserted would put the row wherever it happened to look. So a record
written by a `new` from before the row existed is refused by `close` until the
row is added, and the refusal names the row and where it goes. The two
behaviours are different on purpose and a document that describes only the
first is describing half of it.

**`--range` refuses both ends, not only the second.** `HEAD` is the end that
was reported and a branch name at the start moves exactly as far. An end is
accepted when it is seven to forty hex characters AND resolves to a commit it
is a prefix of; the second half is what makes the first true, and it leaves one
coincidence standing — a branch whose name is hex and which happens to point at
a commit starting with that name. That is recorded rather than parsed away,
because refusing hex-shaped ref names would mean asking git which refs exist,
and the rule would then pass or fail on what somebody else had created.

## The fix surface — `Contract changes` and `New units`

<!-- specs/1788272986-the-fixes-are-what-open-the-next-round -->
Two more rows, read on every record the same way `Fixes checked by` is, and
for the same reason: every round has its own fixes. Issue #57 measured ten
regressions each traced to the fix that opened it, and the largest class —
four of ten — was a fix that changed a unit's contract while not every place
that contract reaches was revisited. The diff names the changed signature and
`grep` names the reach, which is why this can be a gate rather than a
question.

| The row | The check |
|---|---|
| `Contract changes` or `New units` absent, work item begun on or after the cutoff | **fails**, naming the row and what it buys |
| either row absent, work item begun before the cutoff (or with no timestamp prefix) | prints — the same grandfathering as above, keyed to `chain_check.py`'s `SURFACE_FROM`, whose value is the id of the work item that added the rows |
| `none`, with or without a reason after it | passes — `none — the fixes are not yet written` is the honest value while a round runs |
| `none — the fixes are not yet written`, on a record whose `Fixes checked by` names a `round-N`, work item begun on or after `chain_check.py`'s `ORDER_FROM` | **fails**, naming the row and the checker two rows above it. A later round opened these fixes, so they exist, and the cell contradicts its own file — the shape `no fixes to check` beside a `fixed` verdict already takes. Before that cutoff it prints |
| the same cell while `Fixes checked by` still reads `nobody — <why>` | passes. That is the state the ordering rule REQUIRES, and refusing it would refuse every correctly written record at the moment it lands |
| the same cell while `Fixes checked by` reads `no fixes to check` | passes — the arm reads a `round-N` and nothing else. This is the value the TERMINAL record of every run carries, and it is the one place the pair is not merely unrefused but wrong: a round that commissioned no fixes will never have any, so *not yet written* is false the moment it is written and nothing here says so. Whether the arm should refuse it too is open — the refusal would land on merged records whose repair is honest, unlike the `nobody` case |
| `none` with a reason the checker does not recognise | passes — see the limit below |
| an empty cell | **fails** on any record — a row that says nothing answers nothing, and an empty cell is always the author's to fill |
| a `Contract changes` entry (`;`-separated) carrying `unit → call sites` (`→` or `->`) | passes |
| an entry with no arrow, or an empty half | **fails** on any record, naming the entry — a unit without its reach restates the diff and leaves the measured failure's unchecked half unchecked |

**Five values can stand in the reach half, and only the first is a unit
name.** `round_record.py`'s `call_sites` writes the enclosing top-level unit
of every call it finds; the file's basename where the call sits at module
level or outside Python; `pytest`, appended after the named sites when any
caller is under `tests/`; `pytest only` when those callers are the whole
reach; and `no call site found` when there is nothing, because the row above
refuses a unit listed without a reach and an empty half would be the tolerant
read that row refuses. The last three live in `round_record.py` as `PYTEST`,
`PYTEST_ONLY` and `NO_SITE`.

**`pytest only` is also what a unit pytest itself reaches gets, and that is
not the same condition.** The clause above is about a unit's CALLERS all
sitting under `tests/`. A collected test function has no callers at all: the
runner calls it, so the only `test_thing(` in the tree is its own `def` line
and the reach came back empty. The row then read `no call site found` — *this
unit is dead* — about a case that runs on every CI leg (#211). Three shapes
are members, each by a rule of pytest's own collection rather than by a
convention of any repository:

| The unit | How pytest reaches it |
|---|---|
| a `test_*` def in a file `python_files` collects | collected by name pattern, the file and the function both |
| a fixture under `tests/`, or in a `conftest.py` pytest loads | injected by parameter name, so `name(` never occurs |
| a `pytest_*` def in a `conftest.py` pytest loads | dispatched by the plugin manager |

**Two of those three rows say where the file sits, and they say different
things.** Collection is two rules: `python_files = test_*.py *_test.py`
decides which FILE becomes a test module, and `python_functions = test_*`
decides which def inside it is a case. A `test_*` def in `tests/helpers.py`
satisfies the second and not the first, so pytest never runs it — reading the
def name and the directory alone said *the runner covers this* about it. A
`conftest.py` is the opposite case: pytest loads it by name and documents the
repository root placement first, so a fixture or a hook there is reached from
outside `tests/` exactly as one inside it is. Both were round 1's findings on
the change that introduced this section.

The directory still decides whether a conftest is loaded at all, and that is
the second finding coming back inside the repair for the first. pytest imports
a `conftest.py` for the test files collected at or below its own directory, so
one with nothing collected under it — a vendored tree, a package directory, an
examples directory, `src/` in a segregated layout — is imported by nobody and
its fixtures are injected into nothing. Calling them the runner's is the same
false sentence one directory over, and it is true inside `tests/` as well as
outside it: `tests/vendor/conftest.py` with no test module under it is loaded
no more than `src/conftest.py` is. So the name gate is not *anywhere*, it is
*anywhere pytest would load it*, and it replaces the `tests/` gate for a
conftest rather than sitting beside it.

What that question is asked of is the tracked file list, not the runner's
configuration. A repository that narrows collection itself — `testpaths`, a
`confcutdir`, an `--ignore` — has conftests this reads as loaded that a
particular run does not load, and the error runs toward `pytest only`. The
trade is that reading the configuration means implementing pytest's own
rootdir discovery inside a review tool, and a repository whose tests are where
its tests are gets the right answer without one.

**It is those three and not everything under `tests/`,** which is the
boundary the rule needs to stay honest. A helper that is passed by name as a
value and never called reads `no call site found` for a different reason, and
saying *the runner covers this* about a unit nothing covers is #211's own
false sentence pointing the other way. Measured at the fix: 1892 of 1947
`test_*` defs and 8 of 42 fixtures were reading `no call site found`, against
one helper that was reading it correctly.

**One limit, recorded rather than closed: the hook arm reads `conftest.py`
alone, and pytest is wider than that.** It registers collected test modules as
plugins too, so a `pytest_generate_tests` in a test module really is
dispatched and really has no call site — and it still reads `no call site
found`. Widening the arm to every `pytest_*` def under `tests/` would catch it
and would also catch any helper somebody named `pytest_something`, which is
the row saying *the runner covers this* about a unit nothing covers. The
narrower rule with the limit written down is the trade; a hook that wants the
row moves to a `conftest.py`, where pytest looks for it first anyway.

**What `Contract changes` does not see, and this paragraph is the deliverable
rather than an apology for one.** The derivation compares a unit's
parameters, its return arities, and its **set of returnable constant
literals** — the last of the four `templates/sdd-round.md` promises. What
none of the three reaches is a changed **input→value mapping**: a unit that
keeps returning exactly the values it already returned, and changes which
inputs reach which one.

The measured instance is
`tests/test_release_hygiene.py#is_a_record_of_a_moment`, as finding 11 of
`seal/specs/1788735085-a-loaded-file-naming-a-real-version-is-a-timer/rounds/round-2.md`
confirmed. Its fix made it answer `False` where it had answered `True` —
narrowing the exemption from any file under a dated directory to a file whose
own name begins with the date. Signature unchanged, arity unchanged, return
type unchanged, and the returnable set is `{True, False}` at both ends. The
comparison is blind to it **by construction**, not by an oversight a later
edit could quietly repair, because asking which inputs reach which return is
asking what the function computes.

So the residual is the reviewer's, and it belongs in the round's own verdicts
rather than in this row. A `Contract changes` cell reading `none` means *no
unit's parameters, arities or returnable literals moved* — never *nothing a
caller depends on moved*.

**The check ships anyway, and the order of those two facts is the point.**
Stating the limit without the check was refused as an answer: it moves the
work to a person, which this repository's first goal treats as the more
expensive design. The literal-set comparison catches the sentinel case #194
opened for — `token_thirds` returning 0 for a mean it cannot compute — and
this paragraph says where it stops. A later session that widens the check to
try to cover the mapping is removing a stated hole rather than closing a gap;
what it would have to add is an answer to *which inputs reach which return*,
which the arrow's and the comma's limits already decline for the same reason.

**Leaving that vocabulary out is what made a correct cell read as a
mistake.** A review round of the work item that added this paragraph opened a
finding against `hide_from_git → build, ensure, pytest`, on the grounds that
this section defines the reach as call sites a `grep` can name and nothing is
called `pytest`. The cell was the generator's own output, re-derived at the
record's own SHA. Test callers collapse because they are a fix's pins rather
than its reach: naming twelve of them buries the one caller that matters.

**The pending arm is this branch's own damage repaired**, and it is worth
saying which way round that went. Before `ORDER_FROM` a record could be
written after its fixes and both rows filled from the start; the ordering rule
made *not yet written* the value every record now begins with, and nothing
required the second step. `says_none` accepts a reason, so an abandoned cell
read exactly like a finished one — a check reporting clean while something is
missing, which is the title of the work item that produced it.

**Its direction is `allow` for a reason the checker does not recognise, and
that is a deliberate exception to this document's `blocks more` default.** The
alternative is refusing an honest custom reason for its wording, and a rule
about which English sentences mean *not yet* is the enumeration over an
unbounded domain the arrow's and the comma's limits already decline. What is
caught instead is the measured failure: the template's own words, copied into
a record and left standing. The phrase lives in `chain_check.py` as `NOT_YET`
and `templates/sdd-round.md` prints that constant, so the two cannot drift.

**What escapes is wider than a rewording, and three spellings carry the
template's words UNCHANGED.** This paragraph declared the escape as a
rewording for a round, and it was measured over 23 cells and found narrower
than the behaviour (round 3's 🟡 5). `says_none` tests the first character
after `none` while `says_not_yet` strips `SEPARATORS` from both ends, so each
of these passes the cell as `none` and silences the arm:

| The cell | Why it escapes |
|---|---|
| `none ― the fixes are not yet written`, with U+2015 rather than the em dash | the leading space is what satisfies `says_none`, and the bar is outside `SEPARATORS`, so it survives the strip and stands in front of the constant |
| `none — the  fixes are not yet written`, with a doubled space | the extra space is INSIDE the constant rather than before it, so no widening of `SEPARATORS` reaches it |
| `none — nothing yet; the fixes are not yet written` | only a substring match reaches a clause before the phrase, and the substring match is exactly the mutation the prefix rule exists to refuse |

Only the first of the three is punctuation, so widening `SEPARATORS` would
close one and leave this section false about the other two — and it would
widen a constant four other readers in the same file share. The limit is
written down instead. What *this record passed* means is *its cell does not
carry the template's own pending words*, never *its fix surface is complete*,
and a session that spelled the cell any of these ways is not the session that
forgot it.

**The arm keys on `Fixes checked by`, so a session that leaves THAT cell
behind too is reached by nothing here** (round 3's 🟡 1). The value a
forgetful session leaves is `nobody — <why>`, which is the honest mid-run
state and the row above says why it cannot be refused — so the arm reaches
the session that filled the checker cell and stopped, and not the one that
filled nothing. What covers the second is `Fixes checked by`'s own check: it
prints a notice for `nobody` on every record, and refuses it on the LAST
record beside a checked `Pass`. A non-terminal record carrying `nobody` is
false by construction — a later record exists, and round N+1 reviews round
N's fixes — and nothing refuses that today. Keying the arm on the sibling
records instead would give it a second source of truth, which is the property
that makes the narrow key defensible in the first place.

Only the ABSENT row is grandfathered by `SURFACE_FROM`, and the pending arm
above has a grandfathering of its own that reaches a row which is PRESENT:
before `ORDER_FROM` the same cell prints instead of failing. A merged record
has no honest repair
for a missing row — writing reach rows for fixes nobody re-read fabricates a
review — where a malformed row's repair is formatting, which is always the
author's. One limit is recorded rather than parsed away: the arrow is found
by substring, so an ASCII `->` inside a backticked unit name reads as the
reach separator, and such a unit passes without its reach. `→` is the
spelling that avoids it — parsing code spans to close the gap would be an
enumeration over an unbounded domain, the closing the review skill's own
rules refuse. The rows are filled when the fixes land, by the session that has
the fix diff open, so their prompt budget is zero. What `New units` buys sits
with the verifying round: what it names is a finding surface — *is this
correct* — rather than a verification surface, because a unit the fixes
created has been reviewed by nobody.

## The depth in `New units`

`New units` carries a second thing beyond the names, and it has a cutoff of
its own — `chain_check.py`'s `DEPTH_FROM`, later than `SURFACE_FROM`. A work
item begun between the two owes the row and not the depth in it: its records
were written when the row named units alone, and deriving a depth now for
fixes nobody re-read fabricates the answer.

| The entry | The check |
|---|---|
| `unit (depth 1)`, entries separated by `;` | passes |
| `none`, with or without a reason | passes, unchanged — the depth did not take the value a round with no fixes yet has to be able to write |
| an entry with no depth, work item begun on or after `DEPTH_FROM` | **fails**, naming the entry and showing the shape |
| an entry at depth 2 or above | **fails**, naming the entry and where the unit goes instead: deferred with a named answerer, or an issue |
| an entry below depth 1 | **fails** — it names no level the rule defines, and read permissively it sits under the bound |
| an entry carrying more than one unit or more than one depth — a comma list under a single `(depth N)`, or two markers | **fails**, naming the entry. One declaration covering two names says nothing about the second, and the comma is the spelling this row used before the depth existed |
| any of those, work item begun before `DEPTH_FROM` (or with no timestamp prefix) | prints |

**The refusal names the exit because a refusal that does not is a wall.** The
rule and its exit shipped one phase before this check, in that order and on
purpose: a session meeting *this unit may not exist* with nowhere to put it
stops the chain, which costs more than the unreviewed unit did.

**The generator's refusal names the finding whose fix commit added the unit**,
not the file the unit landed in. It resolves that from the commits `close`
already holds — one per `fixed` row — rather than from the range's two ends,
because a range with two fixes in one file attributes every unit in that file
to whichever row the walk reaches first, and the reader is then sent to a row
that did not add the unit.

Where the range resolves the adder to a fix whose finding sits inside no unit
an earlier record names, **the unit is at depth 1 and the rule says nothing**.
Its adder is known and it is not a depth-2 unit, so refusing it would refuse
a unit the definition above does not reach. Resolving to several candidate
findings is not that state: it is a resolution that still cannot say which
fix added the unit, and it takes the fallback below.

Where the range cannot resolve one — a single commit answering two findings
resolves to nothing at any cost — **it still refuses, and the message says the
attribution is file-level and names every candidate finding** instead of
asserting one. It refuses because that is the direction every verdict the
checker cannot read takes, and the asymmetry is `CONTRIBUTING.md`'s: a wrong
deny costs a prompt, and a wrong allow here ships a unit read by nobody. It
stops asserting because the depth goes per entry, so a per-file answer is
structurally unable to state what the record is required to state.

What no check can see is a depth declared wrong — `(depth 1)` on a unit that
is really second-level. The rule is a declaration, and the verifying round
reading the `New units` surface is what looks at it. The declaration is per
finding as well as per entry: a finding whose coordinates sit at two depths
— one inside a unit an earlier round's fixes created, another not — is
written as two findings, so each verdict carries one depth and the fix of
one does not refuse the units the other's fix adds. `round_record.py close`
keys its refusal on the finding's `Location` and names the finding whose
fix added the unit, so a reviewer who did not split reads which finding to
split next round (#366).

One limit is recorded rather than parsed away, the mirror of the arrow's above:
the comma that marks a crowded entry is found by substring, so a comma anywhere
in the entry outside the depth marker is read as separating two units.
`` `get(a, b)` (depth 1) `` is refused, and so is
`` `helper` (depth 1) — adds a, b ``, where the comma sits in the reason rather
than in the name. An entry that needs a comma is written without one.

**The separator has the same limit, and it runs before both of the others.**
`;` splits `Contract changes` and `New units` before anything looks at code
spans, so a literal semicolon inside a code span splits the entry carrying it,
and the tail is refused for having no reach. The record that first hit this was
the one describing a change to how the separator is read — the entry recording
the limit is the entry that met it. Spell the character as a word. Because the
hygiene workflow runs this check on every pull request, a record written the
other way opens the pull request red.

Parsing code spans to tell any of the three apart is the same enumeration over
an unbounded domain the arrow's limit declines.

## What ran the round — `Ran by`

A record says what the round was asked, what it found, and which commit it
read. It said nothing about what executed it, and that fact survives nowhere
else: the model is a spawn-time argument, and once the session ends it exists
only in a transcript. Measured — every segment of two consecutive work items
was metered and posted to a measurement log, and not one of those readings can
be attributed to a runner afterwards.

The cell names **two** things joined by the word `on` — `agent on model`.
Either half alone answers neither question the numbers raise: an agent without
a model cannot be compared against another run of the same agent, and a model
without an agent cannot be told apart from the orchestrating session's own
turns. The joining word is a word rather than a punctuation mark, which is
what keeps this row out of the separator limit above.

Read on every record, like `Fixes checked by` and the fix surface above and
the floor in `docs/review-chain-spec.md`, and for the same reason: every
round was run by something, and a work item whose rounds ran under different
runners is the comparison the row exists to make. A check reading the last
record alone answers it for one round.

| The row | The check |
|---|---|
| `agent on model`, both halves non-empty | passes |
| `unknown — <why>` | passes at any age — a project may genuinely not know, since agent definitions pin no model and a session spawning through another harness has no name for one |
| absent, work item begun on or after the cutoff | **fails**, naming the row and what it buys |
| absent, work item begun before the cutoff | prints — the grandfathering above, keyed to `chain_check.py`'s `RUNNER_FROM`, whose value is the id of the work item that added the row |
| an empty cell | **fails** on any record — a row that says nothing answers nothing |
| a bare `unknown`, with nothing after it | **fails** on any record — the cell then records that something is missing and not what, which is the refusal `nobody` takes for the same reason |
| a cell naming one thing — no `on` with whitespace on both sides, or a half that is empty | **fails** on any record, naming what the two halves are for |
| the ABSENT row, work item with no timestamp prefix | prints — `item_began` has no second to compare, so the cutoff is below it and that row is excused permanently. **The three malformed states above are not**: they fail for a work item named any way at all |

Only the ABSENT row is grandfathered, and the reason is sharper here than for
the rows above: nobody can recover what ran a segment whose session is over,
and a value invented now is worse than the blank, because a reading nobody can
trust reads exactly like one nobody took. A malformed row is refused at any
age, because formatting is always the author's.

**The row is the spawning session's, and that is a rule about where the value
comes FROM rather than about whose keystrokes fill the cell.** An agent is
told what it is, so a value it writes about itself is the value it was told;
the orchestrator is the party that chose the model. For a round record the two
coincide, because the orchestrator runs `round_record.py new` for that file
and hands it the value as `--ran-by`. For a build phase's
record they do not — the segment writes it — so the value is handed over in
the spawn prompt and transcribed, or filled in afterwards. What is refused is
a segment sourcing the value from its own idea of what it is.

**What no check can see is which of those two happened.** `ran_by` reads the
shape of the cell and nothing about where the value came from, so a
transcribed `specseal:smith on Opus` and an invented one are the same eight
words. The rule is a declaration, like the depth's, and the reader who looks
at it is whoever holds the spawn prompt beside the record — the orchestrator
at the round that follows, or the person reading the pull request.

This branch's own four phase records are the worked case, and they are the
mixed one rather than the clean one: the agent half and the model came from
the spawn prompt, and the version detail after it did not. That is what the
declaration looks like when it is only partly sourced, and no check reports
it. A round record has the easier job — the orchestrator runs the generator
for that file and chose the model — which is why the rule's difficulty is
entirely on the phase side.

One limit is recorded rather than parsed away, the same shape the three above
take and outside their sequence — those three are `Contract changes` and
`New units` parsing, and this row is parsed by neither:
a cell beginning with the word `unknown` is read as the unknown answer whole,
so `unknown on Opus` is an unknown carrying a reason rather than a pair whose
agent is not known. Nothing is lost by it — the model is still written where a
reader sees it — and telling the two apart would mean a rule about whether an
English reason may begin with `on`.

## The record generator — what it writes, and what it refuses at the keyboard

`skills/code-review/scripts/round_record.py` is the one writer of
`rounds/round-N.md`, and `bin/round-record` is how it is typed. The sections
above say what each field means; this one says what the generator does about
them, and it is where fourteen work items' specifications came to rest.

<!-- specs/1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records -->
**A record is derived, not typed.** `new` writes the round record from the
warden's report and the spawn prompt's round paragraph — `Target SHA` from
git, `PR` from `gh`, both surface rows at *not yet written*, the verdict,
probe and deferred tables copied from the report — and `close` applies the
implementer's fix table and derives the fix surface from the fix range. The
orchestrator writes one thing by hand, the round paragraph, and no
orchestrator prose ever sits in a parsed cell. Both halves run
`chain_check --worktree` on the work item before they return, so the check
sees the cell that was just written rather than the one at `HEAD`.

<!-- specs/1788844127-the-reviewers-report-reaches-the-record-retyped -->
**The record and the report are different artifacts with different owners,
and neither is retyped into the other.** The reviewer writes its report to
`rounds/round-<n>-report.md` under the work item and returns that path;
`new` reads `--report` from that location when the flag is absent. A report
that reaches the record through a person's hands is a copy nobody can check
against its original.

<!-- specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed -->
**A script a shipped document tells an agent to run is reachable by a
command.** Every `skills/*/scripts/*.py` a shipped document names either has
a `bin/` wrapper pair or is classified, with its reason, in the case that
pins this rule. `chain_check.py` is the one classified: CI and the scripts
that run it carry its full path, and no shipped document shows it with a
flag to type. Every document naming a script also names a form that can be
typed — the wrapper, or the script's repository-relative path. A document
that names a script and no way to reach it is an instruction with no
executable spelling.

### What it refuses before anything is written

<!-- specs/1788789985-round-record-dies-on-python-3-9 -->
**An interpreter below the supported floor is refused at entry**, in a
sentence naming the floor, the version it found and the interpreter it found
it at — before argument parsing, before the sibling checker is loaded, and
before anything is read or written. Dying partway through on a construct the
old interpreter does not know tells the reader about the construct rather
than about the floor, and the floor is the fact they need. The repository's
supported floor is stated once, in `.github/scripts/run_tests.py`, and the
guard names that number rather than a second copy of it.

<!-- specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id -->
**A finding id is a bare integer, behind an optional severity marker, in both
the verdict table and the fix table**, and a refusal names the format and
quotes the offending row. A duplicate quotes both rows, because naming one of
a pair is the manual scan the rule was written to remove. The same work item
fixed what `Contract changes` compares: a unit's contract carries the set of
constant literals it returns, so gaining or losing one reads as a contract
change — and the document states the hole that leaves, a changed
input-to-value mapping, rather than implying there is none.

<!-- specs/1789356180-the-two-halves-of-one-generator-refuse-each-other -->
**A verdict row that commissions nothing takes no fix row.** `close` stops
demanding one for a row that is not an open finding, and stops writing a
verdict word over it; a row with no finding id and a row whose verdict is
`❓ out of verified scope` are both members. A refusal names **every**
offending row rather than the first, because a message naming one costs a
round trip per repair, and five were measured in one record.

<!-- specs/1789296200-the-record-before-the-fix-sequence-has-no-arm -->
**`new` says when the reviewer's target is no longer the branch's HEAD.** It
compares the resolved `--target` against HEAD, names the commits that landed
since the reviewer read it, and says what that can mean. There is one escape,
`--written-late "<why>"`, and the reason it carries reaches the record — so a
state that used to leave no trace leaves one, and `chain_check`'s
`written_late` arm prints for a record carrying that reason instead of
failing. A gate with no honest way past it is a gate people route around.

### What it copies, and what copying costs

<!-- specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row -->
**The record carries the reviewer's paste-ready fixes**, from a heading the
reviewer writes, by the mechanism the file already had for the probes table.
And a bare `|` inside a cell the record **copies** no longer truncates the
row: every column of the verdicts table, `## Executed probes`,
`## Inherited coordinates`, `## Deferred`, and `close`'s `Commit or grounds`.
The distinction is who wrote the pipe. A value the generator composes with a
pipe in it is a defect in the generator and stays refused; a copied cell is
the reviewer's own text, and truncating it silently loses the finding.

<!-- specs/1788873610-every-copy-out-of-raw-meets-the-hider-question -->
**Every record the generator writes is asked the hider question before the
bytes reach the disk**, in the one function that writes one — not at each
call site, which is where a copy gets missed. A comment that opens inside a
fenced block and closes outside it is refused by a message naming the
comment, on every text the question is asked of. A record that hides part of
itself from the next reader is the one failure the whole chain rests on not
happening.

<!-- specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading -->
**A fenced block that closes after a later heading is refused, naming the
heading it swallowed.** A fence opened under `## Executed probes` and closed
below `## Deferred` takes the Deferred section into the probes block, and the
record then reads as though the section were empty. The message names what
the fence ate, so the writer is told what to fix rather than that something
is wrong.

<!-- specs/1789347354-a-wrapped-terminal-line-is-not-one-value -->
**A wrapped terminal line is one value, and the join stops at a blank line.**
A terminal row a narrow window wrapped is still one value, so a continuation
is joined to it. A line that opens a new markdown block stops the join as
well: a heading marker followed by a space, a list, quote or table marker, a
fence, a thematic break or a setext underline. A continuation that opens with
an issue number such as `#120`, with `**bold**`, with an HTML tag or with an
indented run of prose is joined, because its first characters cannot tell it
from prose. The blank line is the only stop that covers every shape, and
that sentence is the one that keeps the next reader from widening the marker
list instead of trusting the blank line.

### What `close` derives, and the arithmetic it must not double

<!-- specs/1789621028-nothing-reads-a-record-against-the-tree -->
**A record is read against the tree, not only against itself.** The
`Fix range` row states a range and a commit count, and the check compares
both against what the repository actually holds — the job `evidence-check`
already does for the ledger over content anchors, and the records were left
out of. In the same class: `close` does not prefix a `Grounds` cell it has
already prefixed, for any of the three verdict words, because all three reach
the same line and all three join rather than overwrite.

<!-- specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places -->
**Where two rows share a coordinate, the forward map takes the first**, the
way the inherited table already did — two readers of one relation disagreeing
is how a record comes to state the same finding as open and as fixed. A
round's silence at zero filled rows is conditioned on whether the next
round's inherited table accounts for this round's coordinates, rather than
unconditional; and a row's severity is read from its `#` cell, with an
unrecognised verdict word getting a message of its own instead of falling
into the nearest branch.

<!-- specs/1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red -->
**A checker's own cases have to be able to fail, and several of these could
not.** Replacing a sweep's `failures.extend(errors)` with `pass` left it
green; a reader that said it read `HEAD` called `git ls-files`, which reads
the index; a rule testing the shape of `Fixes checked by` and not its
position accepted on the last record exactly what the pull-request check then
refused; and a depth walk attributing added units by **file** rather than by
enclosing unit named the wrong finding while refusing correctly. The standing
rule is the one `skills/agent-contract/SKILL.md` §15 states for new cases,
applied to the checkers themselves: a case nobody has seen fail is a case
nobody has seen.
