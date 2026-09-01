# Every branch appends to the same two files — closing memo

Two append-mostly registries every branch wrote to are now written one fragment
per work item, and a ledger row's drift baseline stopped being a value anybody
types — which is what let the ledger split at all. Closes #46 and #52.

## Where the design and the plan diverged

**The baseline reading changed mid-implementation, and the numbers are why.**
The work item was specified as *the baseline comes from `git blame`* — the
commit that last touched the row's line. That shipped, and then measurement
refuted it.

Against the 36 coordinates in `.specseal/map.md`: last touch is later than the
stamp the row wrote on **all 36**, equal on none, earlier on none. A later
baseline is a narrower diff window, so last touch catches strictly less drift
than the stamps it replaces, uniformly, with nothing re-read to earn it. The
cause is in the attribution — `cdb2434`, a release commit that rewrote stamps
in bulk, holds the baseline for **16 of 36** under last touch and **none**
under first appearance.

`git log -L`, oldest entry, is what ships. It costs one git call per row rather
than one per file — 455 ms for 36 rows against 17 ms — and rows carrying a
stamp never reach it, so the whole checker still runs in about half a second
here.

One thing corrected rather than carried, because the first draft of the
reasoning overstated it: **a bulk rewrite collapsing drift windows is not
something a derived baseline introduces.** The written stamp does it too, which
is exactly how `cdb2434` came to hold those 16 rows. What differs is the
trigger — the written scheme resets a row when somebody deliberately edits its
stamp, last touch resets it on any edit to the line. Deriving automates an
existing failure and widens what fires it; first appearance narrows it back.

**A defect found by running the checker on this work item's own fragment.**
The first `bin/evidence-check .` after writing the ledger fragment reported
drift against `9b5501d` — a commit resolvable in this clone and nowhere else.
Two separate readings were doing it: `row_baseline` took the first resolvable
hex word in the row, and rows about the ledger name commits in prose; and
`find_baseline` scans the first 2000 characters, which reaches into the rows of
any ledger shorter than that. Both are fixed — a row's baseline must be a date
and a SHA together, and the header ends above the first row that cites code —
and what is left is Q2 in `questions.md`.

That defect was latent before this work item and is worse after it. With every
row stamped, the stamp usually won; with rows writing no stamp, prose is all
there is.

**A gap the derivation opened, found the same way.** With the baseline derived
from first appearance, a row that drifts cannot be cleared by re-reading the
code: the walk goes past an edit to the row on purpose, so re-wording it leaves
the baseline where it was and the row reads DRIFTED for good. Four rows of this
work item's own fragment reached that state when the design changed under them.

The answer restores a role for the stamp, and a better one than it had. A
stamp is now what a re-verified row writes, it wins over the derivation, and it
may name a commit the branch made — the old rule against that existed because
an orphaned stamp fell back to the ledger header, a baseline from before the
work. The fallback is the row's own first appearance now, which after a squash
is the squash commit. An orphaned stamp costs nothing.

## What review round 1 changed

Ten findings, and the three groups the record names each had one cause.

**The design moved and half the documents did not follow.** `9a7ce62` changed
the reading from last touch to first appearance and brought along only the
three files that commit happened to touch. Four more went on stating the
rejected reading, two of them shipping to plugin users. The case written to
catch exactly that listed three documents of seven — so the check and the
defect were introduced together, and `README.ko.md` could never have been
caught by it at all, because the phrase it looks for is English.

**The derived baseline had three places it could not answer for, and all three
printed like a healthy row.** Renaming a ledger turned that file's drift check
off entirely: `git log -L` resolves a path inside the anchor commit, and the
anchor predates the rename. A row with no baseline was appended as `OK`, the
same word as a comparison that happened. And blanking a coordinate with a
space let a date and a hex word that were never adjacent read as a stamp.

Every one of those reports LESS than the scheme it replaces, which is the
shape that does not announce itself.

**The fragment convention reached half the documents.** The two a session
actually reads still told it to file the entry under `## Unreleased`, and a
case pinned that sentence in place — so a `smith` following its own contract
would either invent a heading this repository's checks refuse or append to the
shared region the fragments exist to empty. That is the collision this work
item was opened to remove, arriving from the document meant to prevent it.

Two decisions were the repository owner's, taken during the round: the
no-baseline verdict fails under `--strict` only, and Q2 closes by reading the
header SHA and printing where it came from. Both are recorded where they
apply — `questions.md` for Q2, the verdict table for the first.

## What review round 2 changed

Ten findings, and the record groups them by what round 1's fixes cost.

**Round 1's re-anchoring was the wrong act, and the paragraph written to
license it was wrong about the code.** A row re-anchored in place and stamped
did two bad things at once: the stamp named a commit this branch made, which
the squash discards — reproduced, `test_ledger_stamps_resolve.py` red on the
squashed branch — and the row's derived baseline became the repository's FIRST
commit, where the cited file was 299 lines against a coordinate in the 600s.
Its drift tripwire could never fire again.

The repository owner's decision: such a row is **removed from `.specseal/map.md`
and written afresh into the branch's own fragment**, because the derivation
distinguishes an edited line from a new one and the fix is to make the row new.
No stamp is written anywhere, so the failure has nothing to occur on.

One thing that came out of executing it, and it is not obvious: **rewriting a
row in place does not make it new.** Rewriting all nine rows cell by cell left
every one of them still deriving the commit that first created its line. What
works is removing them in one commit and writing them in the next. Both facts
are now in the four documents that state the rule.

**A second stamp in a row was a way to silence a real finding.** The ambiguity
branch skipped the drift comparison entirely, so a genuinely drifted row went
from exit 1 to exit 0 — and CI runs the checker without `--strict`. It is
measured from the widest candidate now and still says the row is ambiguous.
Beside it, two spellings of one commit were read as two disagreeing stamps,
which is the ordinary shape of a hand-repaired ledger.

**Removing the header cap in round 1 left a fragment's prose unbounded**, so a
commit named 2500 characters into a rationale paragraph became the file's
baseline — and that baseline is what every row the derivation cannot anchor
falls back to. A declaration is deliberate and is now searched for across the
whole header; prose is accidental and is read only near the top. Nothing had
guarded the round 1 fix at all: reverting it left 55 cases green.

## What review round 3 changed

No 🔴, and two of the three findings were the same shape: **a fix from round 2
whose guard could not fail.** That is the third round running in which this
repository has called that a finding, and both instances were mine.

`widest_baseline` decides which of two disagreeing stamps a row is measured
from, and replacing its whole body with `return shas[0]` left all 62 ledger
cases green — `shas[0]` being whichever cell came first, the exact choice
round 2's 🔴 4 exists not to trust. The guard needed the drift to fall
*between* the two stamps with the descendant in the earlier cell, which no
existing fixture had.

The dedup guard failed for a subtler reason, and it is a consequence of 🔴 4
rather than an oversight. Since an ambiguous row is now measured anyway, a
drifted one reports `DRIFTED` — so the case asserting `AMBIGUOUS not in
stdout` on a drifted row passed whether the two spellings read as one stamp or
two. The direction where the readings differ is an **untouched** row, and both
sides of that fixture exit 0, so the verdict has to be asserted rather than the
exit code.

The third was a sentence in the shipped skill that `--help` had already been
corrected away from: `--strict` turns `UNMEASURED` and `AMBIGUOUS` into exit 2
as well, and neither of those fails the run without it.

## Then the rule changed rather than being reconciled

Three review rounds went on one chain, and the branch's own shape is the
argument: 23 commits, 12 of them touching `.specseal/`. Half the work was
bookkeeping about the ledger rather than evidence in it.

**The cause was that a coordinate was a line number.** A line moves for edits
unrelated to the claim, so the coordinate rotted, so the row was re-anchored,
so its derived baseline reset, so a stamp was needed to clear the drift, so a
squash orphaned the stamp. Blame, first appearance, the two extra verdicts and
the two rules that ended up forbidding each other were all compensation for
that one fact.

A row now names **content**: `path#anchor@hash`, where the anchor is a symbol
read with the stdlib `ast` or a distinctive line of text, and the hash covers
the region under it. `evidence_check.py` goes from 747 lines to 372 and no
longer imports `subprocess` — the shortest statement of what was removed is
that the checker asks git for nothing.

**What the migration found, rather than what it assumed.** All 51 coordinates
migrated faithfully, but only after three corrections the data forced:

- a cited range usually runs to the line before the next definition, so it ends
  on a blank separator that belongs to no content. Trimming blank padding took
  symbol anchors from 20 to 28.
- five rows cite a span across several definitions. Those become several
  coordinates, one per definition, which is the row saying what it is actually
  about. Treating it as one anchor was what produced the first 14 "partial"
  results.
- `#` opens a comment in Python and a heading in markdown. Reading one as the
  other made a 23-line comment block resolve to its first line. The heading
  rule is markdown-only, and that was found by migrating rather than by
  reasoning.

**Rows whose subject the change removed were removed, not re-anchored.** Twelve
of them documented the baseline machinery; their claims went with the code.

**Then the anchor gained a second level, and one rule joining them.** A single
value cannot both locate and notice: locating wants something coarse that
survives edits, noticing wants the few lines a claim rests on. So a coordinate
carries a **major** unit — a function or class for code, a heading path for a
document — and an optional **minor** anchor inside it.

The joining rule is what makes the pair work: **the minor level narrows what is
hashed and never decides whether the row resolves.** A stale minor anchor
widens to its unit and reports DRIFTED. Only the major level can be BROKEN.
That follows from the principle the design now states out loud — an anchor
degrades to DRIFTED, never to BROKEN — because BROKEN means *go edit the
ledger*, which is the bookkeeping being removed.

Three things measurement decided rather than argument:

- **Markdown sentence anchors had to go.** Thirteen rows pointed at a sentence,
  and rewording any of them broke the row. They are heading paths now.
- **Whole-unit hashing is the default, and the minor level is an escape
  hatch.** The instinct is to reach for precision, and that instinct is what
  makes a ledger expensive. The cost of the default is on the record: the
  most-cited symbols here carry four rows each.
- **The generic declaration rule exists because `ast` does not.** A project
  adopting this is mostly code that is not Python, and text anchors there would
  be the brittle version of the design. Executed on a TypeScript fixture:
  `handler` resolves to its block, `Box.open` to its own, an absent name to
  nothing.

Marker comments in the source were considered and refused, with the reasoning
written into the skill rather than left to be re-litigated.

## The last pieces: the destination on BROKEN, and the 0.1.0 blocker

**A raw hash comparison can never see a rename**, and finding that decided the
feature's shape. A unit's name is the first line of its own hashed region, so
the ordered comparison — recorded hash against the other units' hashes — fired
on nothing; the tests written red first stayed red against the implementation
of the instruction's letter. The shipped comparison reconstructs: substitute
the candidate's name with the row's locator throughout its region, then hash.
A pure rename, recursion included, reconstructs the old region exactly; a
rename plus an edit reconstructs nothing and stays a plain BROKEN. The same
proof licenses `--reverify`'s rewrite, and the hash follows the locator for
the same reason it could not stay.

The scan grades evidence rather than trusting names: hash identity, unique
across a bounded repo-wide scan, names the destination and fixes; a name with
different content is printed as the labelled fact it is and never acted on;
two matches are counted and never chosen. A whole-file rename heals
mechanically — every row on the old path finds its unit in the new file —
which replaced the known limit that said a file rename was a by-hand edit.

**The release blocker was pinned verbatim before it was fixed**: an existing
0.1.0 ledger read `0 ok · 0 drifted · 0 broken`, exit 0 — every row silently
ignored on update, the quiet-where-it-used-to-complain shape aimed at every
adopting repository at once. An old-format row now fails the run with or
without `--strict`, naming `--migrate`, which ships the same enclosing-unit
migration this branch ran on its own 51 coordinates: faithfulness report,
left-and-named over guessed, idempotent, all-or-nothing per row.

The post-commit advisory arm prints whatever the checker prints, so it
inherited the graded hints with no code of its own — confirmed by a dispatch
case, not assumed. No pointer was added to the update skill or the README:
the update skill already relays the changelog entry that carries the command,
and the OLD-FORMAT line itself names it, so the loop closes twice without a
third copy.

## Then the migration stopped being a command

The owner's call, on the repository's own stated philosophy: between two
designs that catch the same thing, the one that stops to ask a person is the
more expensive, and `--migrate` as a command a person must remember was that
design. It now runs itself at the first session start after updating — one
line printed, ending *review the diff and commit* — and `claude plugin
update` is the whole of what a user does.

The boundaries carry the design. It writes to a tree unasked, licensed by
ownership (the ledger is the plugin's artifact, the same grounds as
`preset-setup`'s marker block) and bounded by visibility — deterministic,
idempotent, all-or-nothing per row, old text in git history. It never touches
an uncommitted ledger file — the dirty check covers exactly the files it
would rewrite (round 4's 🟡 13 fixed the documents that claimed
`.specseal/`-wide): a dirty one is skipped with one line, the once-per-repo
marker is NOT stamped, and the next clean session start migrates. An unanswerable `git status` reads as dirty, because overwriting on
a guess is the one direction the hook must never fail in. Reading never
rewrites — the plain checker stays pure, held by a case that sits beside the
hook's own.

Two of the nine mutations found fixture blind spots rather than code defects:
a repository can only hold a ledger while not opted in through the
`.specseal/scratch` opt-out, and the git-cannot-answer path needed a raising
`subprocess.run` to be reachable at all.

## What review round 4 changed

The redesign span's first review, and the findings clustered on one habit:
the resolver answering where it should refuse. The generic rule read
`return render(y);` as a second declaration (🔴 1, fixed by naming the
statement keywords — the uses are a bounded list where declaration modifiers
are not, and a wrong entry fails loud); a parsing `.py` fell back to that
rule when a symbol was simply gone, so a moved function read DRIFTED off a
leftover call and `--reverify` made the wrong anchor permanent (🔴 2, fixed
by trusting a successful parse as the whole answer — which forced `ast` to
carry module- and class-level assignments, or the fix would have broken the
three constants this repository's own ledger cites).

The other cluster was scans searching repositories a row may not cite.
EXTERNAL now demands DECLARED cross-repo intent — a parity config, `--map`
or `--default-repo` — because without one there is no other repo to claim,
and a deleted directory was a green build (🔴 3). Where intent is declared
and a row's file is in none of the named checkouts, both the check and
`--reverify` refuse to scan at all: searching this repo for that row is how
a cross-repo coordinate got re-anchored onto a local look-alike (🔴 4, plus
the dead `default_repo` parameter now read). The trade is stated in Known
limits: a renamed local directory in a parity repository heals by `--map` or
by hand, never by a guessing scan.

`--migrate` grew the same discipline in its own direction (🟡 10, the
reviewer's stronger option taken as ordered): with git present, a cited
range is checked against the old stamp's commit and a row whose content
changed since is LEFT — the numbers no longer mean anything — while
unprovable rows migrate and are counted out loud. That put git INSIDE
`evidence_check.py`, so the no-git property was re-drawn rather than
dropped: `test_the_checker_asks_git_for_nothing` now proves by AST that
`subprocess` lives in `content_at` alone and only `migrate` calls it, and by
execution that a plain check answers with no git on PATH.

Smaller, each measured: the dedup key gained the hash (🟡 5); OLD-FORMAT
reached both totals lines and the commit advisory (🟡 6); heading-path
locators heal — reconstruction substitutes the path's LAST part (🟡 8);
`--migrate` reads `--map`/`--default-repo` through the same `place()` both
other commands use (🟡 9); ledger writes go write-then-rename and an
unreadable ledger reports instead of crashing (🟡 14); "moved intact" became
"identical content" everywhere, with the boilerplate-twin limit written down
(🟡 7); and six documents were corrected (🟡 11-13), including the
`.specseal/`-wide dirty-guard claim this memo itself carried.

## What review round 5 changed

Round 5 verified round 4's fourteen fixes — all closed — and reported eight
findings that closing them opened. A ninth arrived from the orchestrator's
security pass while these were being fixed.

Four of them are one shape: the checker answered for something it had not
actually read. `--migrate`'s since-the-stamp proof resolved its path against
the repository TOP LEVEL rather than against the root it was handed, so a run
from a subdirectory read a same-named file elsewhere and either refused an
untouched row forever or stamped a look-alike as proved (🔴 A). An unreadable
ledger was answered as an empty one, all zeros and exit 0 (🔴 B) — the
fail-open direction `tests/test_gates_do_not_fail_open.py` exists for, one
mechanism further out than the decode it was written about, which is why the
new case went into that file rather than beside the other checker pins.
`write_atomic` replaced the NAME it was given, so a symlinked ledger was
replaced by a regular file while the real one behind it stayed stale (🔴 D).
And a coordinate could climb out of the tree — `../elsewhere/file.py#name`
was read from wherever it landed and `--reverify` wrote back a hash of it
(🔴 I, reported by the orchestrator, present since 0.1.0 in the `path:line`
form and so a new guard rather than a repair).

**Where the answer diverged from the one that was given.** `questions.md` §Q3
settles the declaration rule by letting the recorded hash break a tie and says
that where no place matches, the row "stays the honest DRIFTED". It is BROKEN
here instead, and the grounds are what the two verdicts cost: `--reverify`
refuses a row that resolves to more than one place, so a DRIFTED it cannot
heal is exit 1 forever with no remedy a person can run. BROKEN says *go look*,
which is exactly the act that case needs. The rest of Q3 is implemented as
written — the keyword list may narrow a candidate set and never empty it, so
`public new void Render(int x)` and `case loading(String)` resolve, and Swift's
`case` needed no ruling.

The narrow structural guard Q3 left to judgement is IN: a line with nothing
before the name whose statement ends is a call, not a declaration. It is kept
alongside the hash rule rather than replaced by it, because `--reverify` has
no hash to compare against — it is the command that writes one — so it needs
the row to resolve to one place on its own.

**Two findings closed as an answer rather than a fix.** 🟡 F's `--map` half is
decidable per row and was fixed; its other half is not — an unprefixed row in
a repository declaring `.specseal/parity.md` or `--default-repo` may be citing
the original repository, and nothing in the coordinate says which. Those rows
keep the scan off and SKILL.md's Known limits was corrected to say the loss is
any move rather than a renamed directory, and that it costs the `--reverify`
heal as well as the `(moved?)` hint. 🟡 G — a one-line constant colliding with
an unrelated one-liner during a rename scan — closed as a Known-limits line
rather than by excluding one-line assignments from the scan. Grounds: the
design already accepts identity-of-content as its proof standard and already
records the boilerplate twin, a constant is that same class rather than a new
one, and excluding one-line units would take the `(moved?)` hint and the heal
away from every constant a project cites, which is more BROKEN-go-edit-the-
ledger than the limit it removes.

Three of round 5's 🟢 entries were closed while in these files: the `ast` row
in the ledger fragment described the behaviour round 4 replaced, the plan's
phase 12 still said the dirty guard covers `.specseal/`-wide, and one row of
the ledger fragment was cut from its table by a blank line. Finding 7's
wording — `(identical content)`, not `moved intact` — gained the pin it never
had. The multi-line constant span is closed as answered: `ast` spans the whole
assignment statement where the generic rule stops before the closing paren,
which is deliberate and pinned in `test_a_constant_is_a_unit_too`.

## What review round 6 changed

Round 6 confirmed all nine of round 5's fixes and reopened two of them.

**The 3+ Fix Rule fired, and the way out was one level up.** Round 4's 🔴 1,
round 5's 🔴 C and round 6's 🔴 J are three attempts at the same text rule for
what a declaration is. The two failure modes are one ambiguity: drop the
resurrection of keyword-blocked candidates and a C# `public new void
Render(int x)` reads BROKEN, keep it and a `return render(y);` left behind by a
move reads as the unit — round 4's 🔴 2 returning for every file that is not
`.py`, which SKILL.md says is most of what adopts this skill. No keyword list
separates them, so the fourth patch was not written. The repository owner chose
to carry the uncertainty out of the classifier instead: `generic_units` answers
`(places, resurrected)`, `resolve_unit` carries it up, the check treats a
resurrected place that reconstructs nothing as a unit that is GONE, and
`--reverify` refuses to write onto one.

**Where the shape was implemented differently from the sketch.** The brief
suggested changing `resolve`'s return type. `resolve` has two module callers
and about thirty case sites, and `file_units` is one of the callers that does
not care — so `resolve` keeps returning a plain list and a sibling
`resolve_unit` carries the pair. What makes the split safe rather than a place
for the fact to go quiet is a case, not a convention:
`test_the_two_commands_that_must_know_ask_for_the_flag` walks the module's AST
and fails if `check_ledger` or `reverify` reaches for the shorter name.

**What was NOT changed, deliberately.** The scan that proposes a destination —
`file_units` feeding `content_matches` — still offers resurrected candidates.
Filtering them there was considered and rejected: reconstruction against the
row's recorded hash is the same evidence standard that decides the tie in the
check, so refusing a candidate that reconstructs would contradict the rule this
round is implementing. The refusal belongs where there is no hash to lean on,
which is `--reverify` acting on the row's OWN place.

The narrow semicolon widening the reviewer offered — dropping the empty-`pre`
condition from the call-statement guard — was not taken. It closes the C
family and leaves Go, Ruby, Kotlin and Lua, and it would have been the fourth
patch at the site the rule change exists to stop patching.

**🟡 K and the three 🟢 entries.** The `--default-repo` branch of `place`
skipped the containment test the other two branches run, so a source file
symlinked out of the checkout was read and reported `1 ok`; `place`'s docstring
claimed all three branches ran it, which is now true rather than narrowed.
`cross_repo_intent`'s prefix term could never fire — a row carrying a declared
prefix is resolved into the mapped checkout before either call site asks — so
it is gone and the docstring says what actually fixed 🟡 F. `--reverify` now
prints a line for every row it leaves alone. The no-git document pin covers
`.specseal/map.md` as well, where the corrected sentence had nothing guarding
it.

**`contained`'s two prices are now written into its docstring** rather than
left in a round record: a source file symlinked OUT of the repository is
refused, which is the price all three branches pay; and where the filesystem
cannot resolve links, `os.path.realpath` degrades to a lexical normalisation
that still catches `..` and stops catching symlinks. Neither direction fails
toward reading the file.

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck. The scope rule holds them until the review rounds settle, and the rounds are edits already scheduled | the review orchestrator |
| `dirty()`'s pathspecs on Windows. The defensive `.replace(os.sep, "/")` is in; whether git accepts what the hook sends on Windows at all is the round-4 ❓ | the broad gate's windows leg |
| That `.github/workflows/hygiene.yml`'s new step fires on a release pull request. Read, not run — the branch condition is the same shape as the version-bump step above it, and the script's own two directions are executed | the review orchestrator, at the release pull request |
| ✅ Whether `git log -L` costs materially more on a ledger an order of magnitude larger | closed by removal: no row measures from a commit any more, and the check makes no git call at all — the cost question has no mechanism left to ask about |
| `--migrate`'s `git show <sha>:./<rel>` form on Windows. Executed on macOS only; the `./` is what makes git resolve against `-C` rather than the top level | the broad gate's windows leg |
| `write_atomic`'s symlink half on Windows. The case skips where symlinks cannot be created, so the windows leg proves the mode half alone | the broad gate's windows leg |
| `contained`'s symlink half on a filesystem where `realpath` cannot resolve links. Read, not run — it degrades to a lexical normalisation rather than raising, and the `..` half still holds | the broad gate's windows leg |

## Fed back into the spec

- **Q1, recorded not fixed** — a row can be stale the moment it lands, and no
  derived baseline sees it: branch A writes a row citing lines branch B
  changed, B merges first, and A's first appearance already contains B's
  change. The written stamp caught it noisily and by accident rather than by
  design. Closing it means checking the coordinate against the code it cites,
  which is issue #31.
- **Q2, recorded not fixed** — nothing forbids a commit SHA in a fragment's
  prose header, where the header scan reads it as the ledger's baseline. The
  options both have a failure direction that reports LESS drift, which is why
  it was not decided here.
- **The migration rule**, inferred during implementation and now in three
  documents: rows moved between ledger files carry their stamps verbatim,
  because `git log -L` does not follow a row out of a file that stays.
  Executed — and the first fixture written for it modelled a whole-file rename
  by accident, which git DOES follow, so the case now models a partial move.
