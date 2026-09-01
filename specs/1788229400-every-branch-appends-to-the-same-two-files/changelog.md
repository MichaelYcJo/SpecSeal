- **Every branch appended to the same two files, and one of them broke at the
  merge.** Three branches ran in parallel on 2026-09-01, touched 34 files, and
  shared exactly one — `CHANGELOG.md`, in all three pairs. Nothing else
  overlapped at all, so parallel work was never what conflicted: appending to
  one three-line region was. The cost is when the conflict arrives, after the
  broad gate has run and before the pull request opens, where nothing may be
  edited — so resolving it buys a second run of the whole broad gate. Both
  registries are now written one fragment per work item, and no two work items
  share an id. **A changelog entry goes in `specs/<work-item-id>/changelog.md`**
  and `.github/scripts/gather_changelog.py --version X.Y.Z` concatenates the
  ungathered ones into a dated section at the release; `--check` reports any
  that never arrived, and the hygiene workflow runs it on every pull request
  into `main`, so a release cannot ship a change with no entry. Each gathered
  entry sits under an HTML comment naming its work item — invisible to a
  reader, and the only link from a released entry back to the work that
  produced it. Matching the text instead would have worked once: any later
  copy-edit to a released entry would make its fragment read as ungathered
  forever. `## Unreleased` is gone with the region it named. (#46)

- **A ledger row no longer names a commit, because there was no commit it
  could name.** A row's drift baseline was a SHA typed into its Checked column,
  and a feature branch had no good value to type: name the base and the row
  reads DRIFTED at birth, name the branch and the squash leaves it pointing at
  nothing. Measured — seven rows named `9b5501d`, which
  `git merge-base --is-ancestor 9b5501d origin/main` answers no to, and a pull
  request repaired those cells by hand. **The baseline is now the commit the
  row first appeared in**, derived from its own line's history and computed on
  whatever history is in front of it, so no rewrite can orphan it: after a
  squash it is the squash commit, which is what that repair typed in. The
  Checked column keeps the **date** somebody read the code — the one thing in
  the row a person still asserts.

  **First appearance, not last touch**, and the difference was measured rather
  than argued. Last touch is what a single `git blame` answers for free, and
  against the 36 coordinates in this repository's ledger it is later than the
  written stamp on all 36, equal on none, earlier on none — a strictly
  narrower drift window than the stamps it replaces, with nothing re-read to
  earn it. One release commit that rewrote stamps in bulk holds the baseline
  for 16 of those 36 that way, and for none of them by first appearance. A
  bulk rewrite collapsing drift windows is not new — the written stamp does it
  too, which is how that release commit got there — but last touch widens the
  trigger from *somebody edited a stamp* to *somebody edited the line*, a typo
  included. It costs one git call per row instead of one per file, about 13 ms
  a row, and rows carrying a stamp never reach it.

  Deriving the baseline is what makes the second registry splittable. **A work
  item's evidence rows go in `.specseal/map/<work-item-id>.md`**, which the
  checker's default globs already read, and such a fragment needs no baseline
  header at all: every row in it measures from its own line. `.specseal/map.md`
  is not moved — the migration is incremental, the rows in it stay where they
  are, and its header now says so. Ledger fragments are never gathered back,
  because a row is checked against the code it cites rather than concatenated.

  Rows already stamped are unchanged and are not being rewritten: **a stamp
  written into a row still wins**, and it has to be a date and a SHA together,
  because a bare hex word in a row is prose. That distinction is load-bearing
  now that rows write no stamp — a row explaining why the stamp went names
  commits, and the first such word used to become the row's baseline, and the
  ledger's. Wherever rows ARE moved into a fragment later, their stamps move
  with them verbatim: `git log -L` does not follow a row out of a file that
  stays, so a stripped stamp would make the move itself the baseline.

  **Two verdicts join `ok`, `drifted`, `broken` and `external`.** A row with no
  baseline at all now reads `UNMEASURED` instead of `ok` — the old word said a
  comparison had happened and found the range untouched, which is not what an
  uncommitted ledger line has been through, and a fragment is uncommitted for
  most of its working life. A row carrying two stamps that name **different
  commits** reads `AMBIGUOUS`, because the scan reads the physical row and
  `Verified behavior` sits before `Checked`, so the winner would otherwise be
  whichever cell came first. Such a row is still measured, from the wider of
  the two candidates, so a genuinely drifted row still reports drift; skipping
  the comparison had made a second stamp a way to silence a real finding. Two
  spellings of ONE commit are not two stamps. Both verdicts print and pass and
  fail only under `--strict`, because a red light on every ordinary run is one
  a session learns to click past. The run also names where a header baseline
  came from — `from a Baseline row` or `from header prose` — and a SHA that a
  rationale paragraph merely mentions, deep in a header, is not read as one at
  all, while a declaration is read wherever it sits.

  **A row whose coordinate a change invalidates is moved, not re-stamped.**
  Remove it from `.specseal/map.md` and write it into the work item's own
  fragment, in a commit after the one that removed it. The derivation walks
  past edits to a line on purpose, so an edited row keeps the baseline it was
  born with and re-anchoring it in place leaves a tripwire that can never fire
  again; a new line's first appearance is the commit that added it. That is
  what empties the shared ledger into fragments as work items touch the code
  its rows cite. **A migration ledger declares a second baseline** for the
  original repository, because a cross-repo row is never measured from this
  repository's history and committing its line changes nothing.

  Blame is read in `--porcelain`, and the format is load-bearing twice over.
  It spells a boundary commit plainly where the default and `-s` forms
  decorate it as `^9829412`, which `git cat-file` rejects — and the first line
  of every fragment is a boundary line. It also reports each line's number in
  the commit that touched it and the PATH git knew that line by. Without the
  path, renaming a ledger file turned its drift check off entirely — `git
  log -L` resolves a path inside the anchor commit, and the anchor predates
  the rename — and the line number is what lets the walk start in the right
  place when the file has uncommitted edits above the row. That block is
  printed only for the first line of each commit, so the path is remembered
  per commit rather than read from beside every line. Every
  answer is checked against `git cat-file` before it reaches `git diff`, where
  a name resolving to nothing would report "nothing changed" — a pass produced
  by a failure. (#52)
