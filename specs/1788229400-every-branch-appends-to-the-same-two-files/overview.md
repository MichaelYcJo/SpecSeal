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
