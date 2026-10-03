---
name: evidence-check
description: |
  Verify that the evidence ledger's content anchors still resolve — a missing
  or ambiguous unit fails the build, changed content demands re-verification.
  Use when: checking ledger health, before merging spec-driven work, wiring
  the check into CI, or after large refactors.
  NOT for: judging whether the code is CORRECT — this checks that the
  evidence still points somewhere, not that the claim is still true.
---

# evidence-check — does the ledger still point at what it claims?

Specs rot silently: code moves, the ledger's coordinates keep claiming grounds
that are no longer there, and the next reader trusts them. This skill makes
that rot mechanical to catch — the same way a broken test catches a
regression.

## A coordinate names content, never a position

```
path#major                     the enclosing unit
path#major>minor               ... narrowed to the place a claim is about
```

Both carry a hash: `path#major@3f9a2c1b`, `path#major>minor@a71b0e42`.

**A coordinate's job is to put a reader in the right logic, not to pin a
line.** So the address is the enclosing unit, which is stable against every
edit that does not change what the unit *is*.

| Level | What it is | Where it comes from |
|---|---|---|
| **Major** | a function or class for code, a heading path for a document | `ast` for `.py`; otherwise the declaration rule below; `## A / ### B` for markdown |
| **Minor**, optional | the statement the claim is actually about | the name it references (`ast` for `.py`), or a quoted line as a last resort |

```
| CLAUSE | `hooks/routing.py#parse@3f9a2c1b` | ... |
| CLAUSE | `agents/smith.md#"## Boundaries"@a71b0e42` | ... |
| CLAUSE | `hooks/gate.py#run>overlaps@5d1e7c04` | ... |
```

Escape a pipe inside a quoted anchor as `\|`, or the row splits the table it
lives in, and a double quote as `\"`, or the coordinate does not parse and
nothing checks it.

### The rule that decides everything else

**An anchor degrades to DRIFTED, never to BROKEN.**

The two cost different things. `BROKEN` says *I cannot find it, go edit the
ledger* — the bookkeeping this design exists to remove. `DRIFTED` says *it
changed, go re-read the claim* — the work the ledger exists for.

So the minor level narrows what is hashed and **never decides whether the row
resolves**. A minor anchor that stopped matching, or that now matches several
places, means that place changed: the row widens to its major unit and reports
`DRIFTED`. Only the major level can be `BROKEN`.

That is how *specific* and *not strict* stop fighting. Precision buys a
smaller hash and a row that says what it is about; it never buys a new way to
fail.

### The minor level is an escape hatch, not a habit

The default is that a row cites a symbol and the hash covers the whole symbol.
If a function changes, re-reading a claim about that function is a
conservative and honest signal rather than a false alarm — re-reading a row is
cheap, and being strict enough to MISS is not.

The cost, on the record: the most-cited symbols in this plugin's own ledger
carry four rows each, so an edit to one means re-reading four claims.

**Reach for a minor anchor only where a unit is large enough that whole-unit
hashing has been MEASURED to drift rows on unrelated edits** — never where it
merely looks as though it might. The instinct is to reach for precision, and
that instinct is what makes a ledger expensive.

### A document anchor is a heading path

`agents/smith.md#"## Boundaries"`, never a sentence. A sentence breaks on any
rewording, which is a `BROKEN` and a ledger edit; a heading is the document's
own structure and survives the prose beneath it being rewritten, while the
hash still reports that prose changing. Where one heading repeats, name its
parent: `"## Verify / ### Scope"`.

### Resolving a unit without a parser

`ast` is an exactness upgrade for `.py`, not the only road — most projects
adopting this are mostly code that is not Python.

The generic rule needs no parser and no dependency: **the name followed by
`(`, `{`, `=` or `:`, with only declaration keywords before it, then the block
to the next line at the same or lower indentation.** That closes a suite in an
indentation language and lands on the closing brace in a brace language,
because the brace sits at the declaration's own indent.

`=` is there because a module-level constant is a unit too, and a common one to
cite. The colon is stricter — it declares only when the name opens the line —
because `if v not in NAME:` also ends in one, and without that a row citing a
constant reads BROKEN for a use somewhere else in the file. A statement
keyword before the name — `return render(y);`, `await render(y)` — makes the
line a use for the same reason: it is the commonest shape in every brace
language, and reading it as a second declaration made an ordinary
one-declaration-one-call file BROKEN-ambiguous. A line with nothing at all
before the name whose statement ends — `render(1);` — is a call on structure
rather than on vocabulary, and is refused whatever the keyword list says.

Swift, Kotlin, Go, Ruby and Lua end no statement with a semicolon, so that
guard never reached them. **A line with nothing before the name, an opening
paren, and a span of ONE line is treated as uncertain in every language**, and
the span is what bounds it: `render() {` opens a block and stays a declaration
the rule is sure of, while `render(y)` alone does not.

**The rule reports how sure it is rather than being asked to be right.** Where
the certain candidates would leave the set empty, the uncertain ones come back —
a C# `public new void Render(int x)` and a Swift `case loading(String)` are
declarations whose modifiers are statement keywords elsewhere — and the
answer is marked as having survived only that way. What the marking buys is
that nothing downstream has to tell the two apart. The check accepts such a
place only where its content reconstructs the row's recorded hash, and
otherwise treats the unit as GONE: `BROKEN` with the repo-wide scan naming the
destination, which is the answer `ast` already gives `.py`. `--reverify`
refuses to write onto such a place at all, because it is the command that
MAKES the hash and has none to compare against. `--migrate` answers the same
way, with one exception it can prove: where the old stamp's commit holds the
cited lines unchanged, the person's own line numbers vouch for that place and
the row migrates.

**A row citing such a unit is still written by hand.** The check names the
place and the hash it holds — `1-2@a1b2c3d4` — so recording it is a copy
rather than a computation somebody has to do themselves.

Where it cannot resolve a unit, that is `BROKEN` and a person looks. Loud and
honest beats a per-language parser nobody maintains.

### Marker comments in the source are not the mechanism

An adopting project will ask whether to tag cited places with a marker comment
so the checker can find them. **No**, on four grounds:

- **ownership** — the ledger is this plugin's artifact and the code is the
  project's. An anchor scheme requiring writes into the observed source
  inverts that.
- **decay** — a teammate deletes or duplicates a marker they do not
  recognise, silently.
- **coverage** — markers only cover marked places, while the ledger's value is
  citing arbitrary ones, including pre-adoption and vendored code. The derived
  anchor is needed anyway, so a marker can only ever be an optimisation.
- **measured cost** — this repository's rider comments (the `RIDER` marker)
  carried commit SHAs, a squash orphaned them, and a patch release exists
  because of it.

**The one permitted use** is a place with no structure at all — a magic
constant in a config, one line inside a large literal — where neither a symbol
nor a heading exists to derive from. There a bare identifier comment is the
last resort. It carries a name and nothing else: no SHA, no date, no
verification state. Verified-ness lives in the ledger only.

## Run

```bash
evidence-check [ROOT]          # on PATH while the plugin is enabled
evidence-check --strict .
evidence-check --reverify .    # after re-reading: rewrite each row's hash
evidence-check --reverify --checked 2026-09-29 .   # and date every row it moved
```

| Flag | Meaning |
|---|---|
| `--ledger GLOB` | ledgers to scan (default `seal/ledger.md`, `seal/ledger/*.md` and `seal/releases/*.md`). A run given this prints which ledgers it did not read, and how to read them |
| `--default-repo PATH` | migration ledgers cite the ORIGINAL repo with unprefixed paths — resolve them against this checkout |
| `--map NAME=PATH` | resolve `NAME/...` prefixed coordinates against another checkout |
| `--strict` | drift, a malformed coordinate and an overflowing row exit 2, the broken-coordinate code, instead of 1. This is the form `broad-gate` runs |
| `--reverify` | rewrite every resolvable row's hash to what its anchor holds now — and re-anchor every BROKEN row that exactly one unit reconstructs, path and locator both |
| `--checked YYYY-MM-DD` | with `--reverify` only: the date you re-read the rows on, written into the date cell of every row whose hash moves. It says every such row was re-read, so read each row citing a drifted coordinate first, or narrow the write with `--ledger`. A value that is not a calendar date in that form, a date later than today, and the flag without `--reverify` or beside `--migrate` exit 2 before any ledger is read |
| `--migrate` | rewrite old `path:line` rows to `path#unit@hash`; what it cannot prove is left and named |

### Which reader graded your tree

Four readers run this checker over one tree. **Three of them read its exit
code** and grade drift, a malformed coordinate and an overflowing row
differently, and the command above is the most lenient of those three; the
fourth never reaches the exit code at all.

| Reader | Drift is | MALFORMED is | OVERFLOW is |
|---|---|---|---|
| `evidence-check .`, the command this page documents | exit 1, the lenient reading | exit 1, the lenient reading | exit 1, the lenient reading |
| CI's `ledger` job, which runs the same script and adds no flag of its own | exit 1, rendered as a `::warning::` — the job still passes | exit 1, rendered as the same `::warning::` — the job still passes | exit 1, rendered as the same `::warning::` — the job still passes |
| `broad-gate` | exit 2. It runs this same check with `--strict`, and the branch comes back `NOT SEALED` | exit 2, for the same reason | exit 2, for the same reason |
| `hooks/evidence-advisor.py` | not reported at all. It imports this module in process rather than running the script, so it never reaches the exit code — and a line that prints on every commit is a line people learn to skip | printed as a block on the commit, never an exit code: the advisor keeps `MALFORMED` among the rows it names and drops drift | printed as a block on the commit, never an exit code: each row named with its ledger and line, because the commit that wrote the stray `\|` is the one to hear it |

All four are right about the tree they are looking at. A branch mid-flight
legitimately drifts, and the gate runs once at the end over a tree nobody is
still editing — so the disagreement is the design and not a defect. What was
the defect is that nobody said so: a session that ran the documented command
and read exit 1 had no way to learn that the run which decides reads the same
tree as a refusal.

A malformed coordinate is not a branch mid-flight, and it is graded like drift
for a different reason: the repository owner's answer of 2026-09-26, which
keeps a release from starting to refuse rows in a repository's lenient run.
The readers that decide — `broad-gate` and the vendored CI template, which
both pass `--strict` — still refuse it at exit 2. `OLD-FORMAT`, the other
coordinate nothing can parse, stays exit 2 under both readings. A row with
more cells than its table's header, `OVERFLOW`, takes the malformed
coordinate's grading for the same reason, which was about a lenient run and
not about which release changed it (#585).

**So a lenient run says it.** Where a *check* run's answer is exit 1 and only
there, the check prints which reading you took and what `broad-gate` would say
instead. Exit 0 and exit 2 print nothing extra, because every reader grades
those alike. `--migrate` and `--reverify` are writers, not readings of drift:
each returns 1 for the rows or ledgers it could not rewrite, names them, and
carries no notice (#354).

### A narrowed run says what it did not read

`--ledger` is right for one of this tool's two jobs and blinding for the
other. Narrowing is what keeps `--reverify` off a row whose claim is false and
belongs to somebody else; carried into reading, it hides every row the branch
broke in a ledger it does not own. So a `--ledger` run opens with the files it
skipped, named one per line:

```
--ledger narrowed this run — 1 ledger this repository carries was not read:
  seal/ledger.md
run without --ledger to read them; a branch falsifies rows in ledgers it does
not own, and those are the rows with the longest reach
```

It prints before anything is read, so it is above the totals rather than
behind them, and it prints even when the pattern matched nothing at all —
otherwise a typo in the glob reports `no evidence ledgers found`, which is the
sentence a repository with no ledger gets. A run that narrowed to exactly what
the defaults would have opened skips nothing and says nothing.

The line is a report, not a second pass: nothing in a skipped ledger is
opened, hashed or re-stamped.

**Two names for one file are one ledger.** What was read and what the defaults
would have opened are matched by inode (`st_dev`/`st_ino`), so a case variant
on a case-insensitive filesystem, a hard link and a symlink all count as read.
Comparing spellings of the path instead put a platform inside the answer:
`--ledger SEAL/ledger.md` read the ledger and then listed it as unread, which
is a notice naming a file it had just opened.

**Two ways out of the fold, not one**, and the second was missing here until
a review round asked. `os.stat` raising is the obvious one — a file that
vanishes between the glob and the check, or a path that cannot be traversed.
The other is an inode of **zero**, which raises nothing: Python's contract is
*"if non-zero, uniquely identifies the file"*, and CPython's Windows `stat`
leaves both fields 0 when it cannot open a file. Taken at face value every
such file has one identity, so a ledger that WAS read swallows every ledger
that was not and the run says nothing. Both ways out fall back to the
normalized absolute path, which over-reports rather than under-reports:
a ledger is named as skipped rather than passed over in silence.

Measured (#153): one work item's three review rounds and two fix passes all
ran the scoped form and all reported ok. The unscoped read at the pull request
found fifteen drifted rows and one broken claim, every one in a file the
branch had touched.

## Verdicts and what to do

| Verdict | Meaning | Action |
|---|---|---|
| `BROKEN` (exit 2) | the MAJOR unit — or its whole file — is not there, or the unit is there more than once | fix the coordinate now. Where the content still exists the line names the destination, graded by proof: `identical content at <where> (renamed?/moved?)` is content identity across a repo-wide scan and `--reverify` acts on it; `same name at <path> (content differs)` is a labelled fact only; several matches are counted, never named |
| `OLD-FORMAT` (exit 2, `--strict` or not) | an old `path:line` row from before content anchoring, which nothing measures any more | run `evidence-check --migrate .` — a red build naming the migrator beats a green build checking nothing |
| `MALFORMED` (exit 1; 2 under `--strict`, which is what `broad-gate` passes) | a row's `Code grounds` cell holds a coordinate that does not parse — a placeholder or short hash, no path, a bare `"` inside a quoted locator, a minor anchor that is not quoted — or cites no coordinate at all while the row claims something. Before this verdict such a row entered no count and the totals read clean | write it as `path#anchor@hash`: a `"` inside a quoted locator as `\"`, the hash as `@00000000` until `--reverify` fills it. `--reverify` names the row and leaves it, because which reading of an unparseable coordinate was meant is not the checker's call. Exit 1 here means *fix the coordinate*, not *re-read*: the verdict word on the row says which of the two exit 1 is |
| `OVERFLOW` (exit 1; 2 under `--strict`, which is what `broad-gate` passes) | a table row in a ledger file splits into more cells than its table's header, so the text past the last column is in no column and no reader sees it — usually an unescaped `\|` inside a cell. A row under no header, which is every fragment row, is counted against the five columns `templates/ledger.md` declares for a ledger row. The line is named with both counts | write a `\|` inside a cell as `\\|`; a table that is not ledger rows takes a header of its own. `--reverify` names the row and leaves it, and still rewrites the row's hashes where their anchors resolve, because the hash is not what is wrong. Exit 1 here means *escape the pipe*, not *re-read* |
| `DRIFTED` (exit 1; 2 under `--strict`, which is what `broad-gate` passes) | the content changed, or a minor anchor's place is gone | re-open it, re-read the claim, then `--reverify`. This is one of the three verdicts the readers grade differently, `MALFORMED` and `OVERFLOW` being the others — see *Which reader graded your tree* |
| `EXTERNAL` (exit 0) | the path resolves in no known checkout, in a repository that has DECLARED cross-repo intent — a parity config, `--map`, or `--default-repo` | pass `--map`/`--default-repo`, or accept as out of scope. Without such a declaration a missing path is `BROKEN` instead: a deleted or renamed directory must fail the build, not read as somebody else's repo |
| `NOT-IN-TREE` (exit 2, records arm) | a record of a work item that has not shipped, or a row of `seal/follow-up.md`, names a compound backticked identifier that nothing carries outside `seal/specs/`, `seal/ledger/` and `seal/follow-up.md`, or writes a `path#name` whose path resolves to a file that does not carry the name | correct the record, or append ` · NAME NOT IN TREE` on the line where the record means a name the tree does not have (placed before any trailing colon introducing a block). The marker exempts the LINE, not the name |
| `UNREADABLE` (exit 2, records arm) | a record under a live work item, or a `seal/follow-up.md` that is there, that could not be opened, or a directory the walk could not LIST — a work item's own folder, or `seal/ledger/` itself | a record nobody can read is indistinguishable from a record with nothing in it, which is the green build this refuses. The same holds a directory up, where it is worse: an unlistable `seal/ledger/` used to read as a repository with no live work item and take the whole arm quiet at exit 0. A directory that is ABSENT is still an empty answer — a repository that has not started is not a broken one |
| `OK` | the content is what the row recorded — the current line numbers are printed for you to open |

**An ambiguous MAJOR unit is BROKEN, loudly, and never a measurement.** With
two places to look, an `OK` would be a claim about whichever one the code
happened to reach first. An ambiguous minor anchor widens instead — see the
rule above.

## Re-verifying is recomputing the hash

```
evidence-check --reverify .
```

It rewrites the hash of every row whose anchor resolves, and names each one it
changed. That is a person saying they have re-read the code, which is why it
is a separate command: a check that refreshed what it was checking would
report `OK` for ever. A row whose anchor is gone is left alone — silently
renaming its hash would hide the one row somebody has to look at. A
`MALFORMED` row is left too, with a `LEFT` line naming it and the remedy, and
the run exits 1. An `OVERFLOW` row gets the same `LEFT` line, naming the
ledger and the line because this command prints no heading per ledger, and
the run exits 1.

**A new hash says somebody re-read the row, and the date cell says when**
(#387). `--reverify` alone leaves every date as it stands and, after the
count line, names each row whose hash it moved — its ledger and line, its
first cell, and its date cell as it is — so the reading that nothing dated is
in front of whoever ran it. `--checked YYYY-MM-DD` writes the date instead:
` · YYYY-MM-DD` after the dates a cell holds, the date alone in an empty
cell, and nothing where the cell already ends in it. A row is dated once
however many of its coordinates moved. A rename healed by identical content
moves the hash, so it is dated too; a file moved whole reconstructs with the
recorded hash, so its row is re-pointed and neither dated nor named; and a
row whose anchor still resolves at its recorded path and hash is never
touched.

The date cell is the column headed `Checked`, else the column headed `Date`,
else — under no header — the fourth cell of a row exactly five cells wide.
Under `--checked` a row whose hash moved and that has no date cell is **left
whole**, hash included, with a `LEFT` line, and the run exits 1: writing the
hash alone would make a row whose two halves disagree, which is what the flag
exists to end.

**The flag asserts every row whose hash it moves was re-read.** One drifted
unit can be cited by several rows, and the check names the coordinate once.
Read every row that cites a drifted coordinate before typing the date, or
narrow the write with `--ledger` to the files you did read.

**In a signatory, the re-read also records a pact change** (#647,
`docs/the-pact.md`). Where `seal/config.md` names a pact in a `Pact` row and a
row whose hash this moves — in place, or into a `Re-read ·` row under
`--into` — cites one of its clauses as a pact anchor, or a coordinate of such
a row is BROKEN, one row per ledger row is appended to
`seal/pact-changes/<work-item-id>.md` and a `recorded` line names it. `Pact
notify | always` records every row whose code moved, with `—` for its clause,
and `never` records nothing. The work item is the `--into` fragment's, else
the one a `routing.md` declares for the branch; with neither, the row is
named on a `LEFT` line and the run exits 1. A copy of this script with no
`hooks/` beside it cannot read the `Pact` row: it names each row citing a
pact on a `LEFT` line, records nothing, and exits 1. The ledger is written
exactly as before in every case.

## A row inside a fence is an example, not a claim

A ledger that explains its own row format shows an example row in a fenced
code block, and nobody wrote that row as a claim. So the check, `--reverify`
and `--migrate` all skip every line of a fenced block that **closes**: the
example is not reported, and neither writer changes a byte of it (#444).

Three things are still read, each because skipping it would be silent:

- **A fence that never closes.** It runs to the end of the file, and reading
  nothing from there on would pass a broken row on a file whose author made
  a mistake. Its rows are checked as rows.
- **An HTML comment.** A commented-out row is a claim somebody parked, and
  dropping it is the silent direction.
- **An indented code block.** Only a fence is a quotation here.

What counts as a fence is CommonMark's rule, and the one the ledger and record
readers share: at most three spaces of indentation, three or more backticks or
tildes, a backtick opener whose info string holds no backtick, and a closer of
the same character, at least as long, with nothing after it. The release
scripts, the correction check and the payload meter ask it too (#584). The
readers that keep a rule of their own, or none, are named in
`skills/verify/scripts/unverified_check.py#fence_opener`'s docstring, each
with its reason.

**A ledger row you mean as a claim does not belong inside a fence.** Before
this rule, one there was checked. Now it is not, and nothing says so.

## What the region is

| Anchor | Region |
|---|---|
| a symbol in `.py` | the whole `def`/`class` span, **decorators included** — a decorator carries behaviour |
| a symbol elsewhere | the declaration line to the next line at its indent or lower, so a closing brace ends it |
| a markdown heading path | down to the next heading at its level or above, which is what a reader means by a section |
| a minor anchor | the statement it names, capped so a claim cannot quietly grow to a whole unit |
| any other line | the contiguous run of non-blank lines it sits in — a paragraph, a table, a block of code |

**The heading rule is markdown-only.** `#` opens a comment in Python, shell and
YAML, and reading one as a heading made a 23-line comment block resolve to its
first line alone.

**Indentation is content.** Trailing whitespace and blank lines are normalised
away, so a reformat is not a change; leading whitespace is not, because in
Python a dedent moves a statement out of the block it belonged to, and a
checker that shrugged at that would go quiet exactly where the edit matters.

## One fragment per work item

A work item's rows go in `seal/ledger/<work-item-id>.md`, which the default
globs already read. Two branches never queue at one file, because no two work
items share an id. The release that ships the work item folds its fragment
into the ledger and removes the file — this plugin's own repository folds
into one file per release, `seal/releases/<X.Y.Z>.md`, which the default
globs read too. A row is checked against the code it cites wherever it
sits, so the fold changes no row's status. The `ok` total counts a
`(coordinate, hash)` pair once per file, so a fold can change the count.

Where `seal/config.md` declares `Ledger frozen from`, a released ledger file
never changes, and a re-read of one of its rows is written into your own
fragment: `evidence-check --reverify --into seal/ledger/<work-item-id>.md
--checked <YYYY-MM-DD> .` writes one `Re-read ·` row per drifted released
row, and plain `--reverify` writes no released file and names each row it
left. What a citing row is, and how the checker reads a released row with
the rows that cite it, is `docs/the-evidence-ledger.md` §*A released row is
read again in the branch's fragment*.

A row citing a range that spans several definitions becomes several
coordinates, one per definition. That is not a loss: it is the row saying which
pieces of code it is actually about.

## `correction-check` — a correction a merge dropped

Without the freeze, the fragment rule has one exception and the exception is
the whole of this problem: a branch that removes or edits the code an
existing ledger row cites, or makes what the row claims false, keeps that
claim true in the file the row is in. So two branches in one release correct
rows of one file, the file conflicts, and resolving it by taking a side
reverts whatever the other side had corrected. Where `seal/config.md`
declares `Ledger frozen from`, a released row is read again and corrected by
a citing row in the branch's own fragment instead, and a released file takes
no edit to conflict on — `docs/the-evidence-ledger.md` §*A released row is
read again in the branch's fragment* is the rule.

**This check cannot see that, and neither can anything else here.** A row
reverted to a superseded state is byte-identical to a row nobody touched:
there is no marker on it, the anchors resolve, and the hash is correct for the
restored text. Run afterwards, `--reverify` re-stamps it — writing *somebody
read this* over a claim that had been read, found false and repaired.

So a second command reads what the corrections carry in their prose:

```bash
correction-check --range origin/<base>...HEAD
```

It walks every merge commit in the range, reads `seal/ledger.md`, every
`seal/ledger/*.md` fragment and every `seal/releases/*.md` file at the merge,
at both parents and at the merge base, and names every `Corrected <date>` or
`Re-read <date>` marker a parent carried that the result does not — while the
row carrying it still stands. A marker that went **with** its row is `REMOVED`
and correct, and a marker a parent deleted relative to the base is that
parent's decision rather than the merge's. A `Corrected ·` row a merge
dropped while the released row it cites stands is a loss too, and under the
freeze a range that changes a released file is refused, with the exemptions
that section names. Exit 0 when nothing was dropped or refused, 1 with each
loss and each refused file named, 2 for a range or a freeze row that will not
read.

**Its moment is the pull request, and it has no other.** A feature branch
squashes into its release branch, so the merges it reads stop existing the
moment the branch lands. The hygiene workflow runs it on every pull request
into a release branch for that reason, and a repository with no merges in the
range gets one line saying so and exit 0.

It reports the loss; it does not prevent it. Reading both sides of a hunk is a
person's act, and a merge driver for the file would have to understand what a
row claims — which is the judgment this whole ledger is built around a person
making.

## `pact-check` — the signatories against the pact

Some work items commit in more than one repository, and where those
repositories keep a contract together, the one copy of it is the pact,
`seal/pact.md` in one of them (`docs/the-pact.md`). Every repository of such
a work item is a signatory. A signatory other than the pact's repository
names it in a `Pact` row of its `seal/config.md`, and cites the clauses it
was built against as pact anchors:

```
pact:orders-api/"## Order response shape / ### Fields"@1a2b3c4d
```

The name is the last path segment of the pact's repository's normalised
origin URL, the locator is a heading path in `seal/pact.md`, and the hash is
this checker's content hash of that clause, the value a local coordinate to
the heading would carry. **This checker passes a pact anchor over.**
`ANCHOR_RE` cannot match inside one, and the readers that blank coordinates
before reading a line another way blank pact anchors first, so a clause
heading holding a version is never an old-format coordinate here.

What grades them is a second command, run at the pact's repository:

```bash
pact-check
```

It reads the pact's `| Signatory |` table, finds each signatory's checkout
through `~/.claude/specseal/pact-paths.md` (a `| Remote | Path |` table kept
per machine) or a sibling directory with that origin, guessing nothing, and
refuses a signatory whose config does not name this pact. Then it grades every
anchor naming this pact in the signatory's ledger files and specs: `OK`;
`SUPERSEDED`, built against a clause HEAD's own history replaced; `NOT TAKEN`,
citing a version only another ref holds, which it names; `UNMATCHED`, a hash
no commit gave the clause; `BROKEN`, a heading path naming no single clause.
Git is asked which way a mismatch points and never whether an anchor is `OK`.
Exit 0 when every signatory was read and every anchor is `OK`, 1 for the three
mismatches or a checkout not found, 2 for `BROKEN`, a refused row or file, an
anchor naming the pact that does not parse, a relationship recorded on one
side only, or no origin remote. A token that begins an anchor — `pact:<name>`
followed by `/` or `#`, or by the rest of an anchor with its `/` missing —
and does not parse is that last kind; the refusal names both ways out, a
quoted heading path with a hash, or a fenced code block for an example.
Every path it prints is in POSIX form on every platform: relative to its
repository inside one, and beginning `~/` where it lies under `~`.

**It reads every signatory's pact changes too** — the
`seal/pact-changes/<work-item-id>.md` records a signatory's `--reverify`
writes (§*Re-verifying is recomputing the hash*), following that signatory's
`Pact notify` as read now. A row citing a clause of this pact is `NOT TAKEN`,
exit 1, until a pact review here takes it: the line names the record and
line, the clause, the work item and the record's content hash, which is the
value the review writes. A `—` row from a signatory whose notify is `always`
is `NOTED` and moves no exit. A pact review is a work item at the pact's
repository whose record, `seal/pact-reviews/<work-item-id>.md`
(`templates/pact-review.md`), has one row per record it takes: the signatory,
`<work-item-id>@<content hash>`, and `holds` or `amended`. A record is taken
at that hash alone, so one that grows after its review reads `NOT TAKEN`
again, naming both hashes. A review row naming a signatory the pact does not
list, a record that signatory does not hold, another verdict, or `amended`
for a clause that still has the recorded hash is refused at exit 2, as is a
record that will not read or parse. The `READ` line and the summary count the
pact changes read and taken.

**It is local only.** A signatory's pull request can read one repository, so
its CI prints the relationship and verifies nothing (`chain-check`'s pact
notices), and this command is where the reconciliation runs. A `SUPERSEDED`
or `UNMATCHED` line names the clause's current hash, so a new citation can be
written with `@00000000` and corrected from its first report.

## The records arm — what a work item's records say about the tree

A ledger row is a claim about the tree that something reads. A **record** —
`spec.md`, `plan.md`, `overview.md`, `rounds/round-N.md`, `phases/phase-N.md`
— states the same kind of thing and nothing read it (#190). It names a unit,
or stamps one, and the next commit moves what it named.

Every run reads them, under its own heading and with its own counts, and no
flag turns it on:

```
records — what unreleased work items and seal/follow-up.md state about the tree
  NOT-IN-TREE  seal/specs/1780000000-x/plan.md:14  `gone_helper` — nothing outside …
  1 work item read · 38 unread · 206 names read · 0 stamps read · 1 refused · 0 drifted · 0 external · seal/follow-up.md read
```

**Whose records are read is decided by the ledger fragment.** A work item
with `seal/ledger/<id>.md` still on disk has not shipped; the release folds
that file away, so the boundary is a file the fold already removes and there
is nothing else to keep true. A shipped work item's records are records of a
moment — a plan from two releases ago proposing a helper that was built under
another name is correct as history — and refusing those would be refusing the
past.

**`seal/follow-up.md` is read on every run, whatever is live** (#508). It
is permanent and a row leaves it when its item is done, so every row in it is
live, and its rows are unit names read by a person months later — a row once
named a case in no file and was caught by grepping. It is read by the same
claim rules as a record and it is **out of the corpus**, because a file both
read and counted as the tree answers its own question. The summary line ends
by saying which it was: `seal/follow-up.md read`, `no seal/follow-up.md`, or
`seal/follow-up.md unreadable`, which is also `UNREADABLE` and exit 2.

**`N unread` is the other half of that boundary**, because *has a fragment*
answers *is live* and its converse does not: a work item that has not written
its rows yet is skipped, and used to be skipped in silence. `0 names read`
and exit 0 says the same thing for *every record is clean* and *no record was
opened*, so the count is on the line either way.

**What counts as a claim.** A backticked identifier carrying an underscore,
and an anchor stamp `path#unit@hash` resolved exactly as a ledger row's is. A
single word in backticks is prose far more often than it is a unit. A FENCED
line is a quotation — a paste-ready fix is code the tree does not have yet —
and an HTML comment that begins a line is an aside; neither is read.

**A name written the way a coordinate is written is a claim too** (#508):
a backticked `path#name`, `path#name()` or `path#Class.method` with no hash.
Where the path resolves to a readable file, the way a ledger row's path does,
every segment of the name has to be a token of **that** file, so a case
named under the wrong test file is refused though another file has it, and a
one-word name is read, because the path is what makes it a claim. The
refusal names the path. Where the path does not resolve — a bare file name,
a missing file, a path out of the root — each segment is read the way the
same name written bare is: an underscore, and the whole corpus. Three
fragments are not refused: after a `.md` path, a GitHub heading anchor
(`README.md#install`, `README.md#dont` for `## Don't`), read against the
file's words lower-cased and the anchors GitHub builds from its rendered
headings, setext and quoted ones included; a line
anchor, `#L120`, which names no unit; and a path the stamp half calls
`EXTERNAL`, which is not read at all. What it gives up: a name that survives
only in a comment of the named file passes, and a bare file name paired with
a name another file carries passes.

**A comment is an aside only where it begins a line**, or begins what is left
of a line after a `-->`. One that opens part-way along text is read with the
text, so a name inside it is read and can be refused. Put the marker on that
line, or start the comment on a line of its own. Treating a mid-line comment
as an aside would need a scanner that knows code spans, because records quote
`<!--` inside backticks all the time, and each such quotation would otherwise
hide every claim up to the next `-->` without a word (#220).

**Both of those are REGIONS, and each runs to its own end.** A comment is an
aside to its `-->`, so a template's two-line comment is an aside on both
lines. **The `-->` ends the aside where it stands, not at the end of its
line**: a name written after it is read, and a `<!--` right after it opens
an aside again. A fence runs to a close of the same character that is at
least as long as the opener and carries nothing after it, the rule the
ledger and record readers share. So a `~~~` quoted inside a ```-block does not
end the quotation, and neither does a ```` ``` ```` quoted inside a
```` ```` ```` block. And a fence the record
never closes reads as a malformed record rather than as a quotation of
everything left: its lines are read as claims, because an author's missing
backticks must not be the thing that makes the rest of a record pass in
silence. A comment the record never closes takes the same answer — its lines
are read, because a missing `-->` is the same mistake one region over, and
until #217 it silenced every claim under it while the arm said nothing. The
`NAME NOT IN TREE` marker still exempts any line it sits on, held or not.

**What counts as the tree.** Every identifier-shaped token in every file the
walk reaches, prose and file names included, outside `seal/specs/`,
`seal/ledger/` and `seal/follow-up.md`. `seal/ledger.md` and `seal/releases/` are inside it: a shipped
row's names are the tree's. Caches, build output and `.git` are skipped,
because a `__pycache__` carries the identifiers of a module the tree has since
lost.

**An untracked or `.gitignore`d file still counts**, and that is a known
hole: a scratch note holding a name silences a refusal with no committed
byte. Closing it means asking git what it carries, and this checker calls git
for nothing outside `--migrate` — see *A row carries no line number and no
commit* in `README.md`. What the hole costs is bounded in the safe direction:
CI reads a clean checkout, where the untracked file does not exist, so CI is
the stricter reader and the local run is the lenient one.

**Grading follows the ledger's**, with one difference. `EXTERNAL` is exit 0
and `DRIFTED` in a record does not fail the run: a live work item's branch is
editing the very units its records stamp, so failing on drift would be red by
construction. A name the tree does not carry has no such excuse — it is
absent, or the record is wrong, and the marker is one comment away.

## Known limits

- A missing file is `BROKEN` with the same graded scan hints as a missing
  symbol — a renamed file or directory is findable by content. `EXTERNAL`
  needs declared cross-repo intent, and where intent is declared but a row's
  file is in none of the named checkouts, the scan stays OFF: searching this
  repository for a row that may cite the other one manufactures evidence.
  Intent is read per ROW where it can be: a row whose prefix is not among the
  `--map` names is a local row and keeps its scan. What cannot be read per row
  is an UNPREFIXED row in a repository declaring `seal/parity.md` or
  `--default-repo` — it may be citing the original, and nothing in the
  coordinate says which. Such a row loses the scan for any move, not just for
  a renamed directory: no `(moved?)` hint and no `--reverify` heal, so it is
  fixed by `--map` or by hand.
- `DRIFTED` means "someone must re-read this", not "the claim is wrong".
- A place the rule is unsure of — a C# `new`, a Swift `case`, a one-line
  bare-name declaration — is never re-anchored by `--reverify`, and is
  migrated only where the old stamp vouches for the cited lines. Where its
  content changed in place and no destination is provable, both commands leave
  the row and print the hash to record by hand. Accepting it instead is how a
  call site left behind by a move becomes the row's permanent anchor.
- Every row the check calls `BROKEN`, `DRIFTED`, `MALFORMED` or `OVERFLOW`
  gets a line back from `--reverify`, whether or not it could heal it.
  Silence there reads as a heal that happened.
- `OVERFLOW` reads every table in a ledger file, not only a table with a
  `Code grounds` column, because a split is a defect of the row whichever
  table it stands in. So a table under no header that is not ledger rows, six
  cells wide or wider, is named: give it a header. A table whose own header is
  wider than five columns is measured against that header, and a row with
  fewer cells than its header is not named, because every cell of a short row
  is rendered and nothing in it is hidden.
- `MALFORMED` reads one cell of a row: the column headed `Code grounds`, or
  the second cell of a row under no header, which is every fragment row. A
  table whose header names no such column is not read, so a ledger that
  renamed the column takes that table out of the verdict, and a coordinate
  that does not parse in a Notes or Verified-behavior cell is not named.
  Scanning every cell was measured on this plugin's own ledgers and refused
  seven correct things in eight — the template's notation row, `#unit@hash`
  shorthand, a quoted example of the bug — which is why the arm keys on the
  template's column name. A claim row whose `Code grounds` cell is empty is
  not read either: a row citing nothing is named only when the cell holds
  text.
- A nested `def` is anchored by its qualified name — `outer.inner` — and the
  short name alone resolves to nothing. Such a row reads `BROKEN` with the
  qualified unit named on the same line, and `--reverify` re-anchors it.
- Reconstruction proves identity of content, not history. Deleting a unit
  that has a boilerplate twin — an `__init__`, a trivial getter, a thin
  wrapper, and most readily of all a one-line constant, where the name
  substitution leaves nothing but the value — reads as `renamed?` pointing at
  the twin, and `--reverify` would re-anchor to it. Deleting `TIMEOUT = 10`
  beside an unrelated `RETRIES = 10` is the cheapest way to see it. The line says *identical content*, which is the whole of
  what was proven; the deletion is yours to spot in the diff.
- Renaming a symbol reads as `BROKEN` — but where exactly one unit
  reconstructs the recorded content, the line names it and `--reverify` fixes
  the row. The proof substitutes the candidate's name with the row's locator
  and compares against the RECORDED hash, so content that changed AND moved
  matches nothing and stays a plain BROKEN.
- The rename scan is bounded so the clean path stays fast: same-extension
  files only, files over 256 KB skipped, and past 200 candidate files it
  degrades to the row's own file and says so on the line. Measured
  2026-09-23, CLI wall time, median of five, Python 3.12 on macOS, on
  one-line candidate files: one BROKEN row against 200 files ~72 ms, past
  the cap ~70 ms, against ~67 ms for an empty ledger. The interpreter and the
  import are nearly all of it.
- A name match with different content never fixes anything — `main`,
  `resolve` and `check` collide across files as a matter of course.
- The generic unit rule stops AT a closing brace rather than including it. The
  brace carries no claim, and a language-aware rule for what closes a block is
  the per-language parser this deliberately does not have.
- A `path#name` whose name holds a hyphen or starts with a digit is not read at
  all, so a multi-word heading anchor such as `README.md#known-limits` is
  checked by nobody. And a `#` line GitHub does not render as a heading — in
  an unclosed fence, an HTML comment, front matter or `<pre>` — still gives the
  file an anchor, so a record naming it passes.

## Migrating a pre-anchor ledger

**The default is that nobody runs anything**: at the first session start after
updating, an opted-in repository's ledger migrates itself and prints one line
ending *review the diff and commit*. Once per repository; never over an
uncommitted ledger file — the dirty check covers exactly the files the
migration would rewrite, and a dirty one is skipped with one line and retried
at the next clean session start. The write is licensed by ownership (the
ledger is the plugin's artifact) and bounded by visibility: deterministic,
idempotent, all-or-nothing per row, old text in git history.

A recorded line number is trusted only as far as it can be vouched for. Where
git can produce the file at a row's old stamp, a cited range whose content
changed since that commit is LEFT rather than rewritten onto whatever sits at
those lines now. Where the proof is unavailable — no git, no stamp, a commit
a squash orphaned — the row migrates against the current tree alone and the
summary says how many did, so those rows are reviewed in the diff rather than
assumed.

For CI, for a skipped tree, or by hand:

```
evidence-check --migrate .
```

One command, once. Each `path:line` row is resolved against
the current tree to its enclosing unit and rewritten as `path#unit@hash`; the
commit stamp drops and the date stays. The run prints the same faithfulness
report this repository's own 51-coordinate migration was held to: how many
converted, and every row left named with why — a line past the end of its
file, a file that is gone, a range no single unit contains. A left row keeps
failing the plain check as `OLD-FORMAT`, so nothing is silently dropped, and
running the command twice is a no-op.

## CI

`/specseal:evidence-ci` does the wiring: it vendors `scripts/evidence_check.py`
to `tools/` and writes `.github/workflows/evidence-check.yml`, resolving the
plugin's own path so nobody has to know where it is installed. Re-running it
diffs the vendored copy against the current one.

Vendoring over fetch-at-run keeps CI deterministic and offline-safe, and puts
the checker in the diff where a reviewer can see it change.
