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

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck. The scope rule holds them until the review rounds settle, and the rounds are edits already scheduled | the review orchestrator |
| That `.github/workflows/hygiene.yml`'s new step fires on a release pull request. Read, not run — the branch condition is the same shape as the version-bump step above it, and the script's own two directions are executed | the review orchestrator, at the release pull request |
| Whether `git log -L` costs materially more on a ledger an order of magnitude larger. Measured at 36 rows, one clone, macOS | repository owner |

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
