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

- **A ledger coordinate names content, not a position.** A row cited
  `path/file.py:120-134`, and a line number moves for edits that have nothing
  to do with the claim — so inserting a line above a cited function left the
  row pointing at the wrong lines while still reporting OK. Everything built to
  manage that was compensation: the coordinate rotted, so the row was
  re-anchored, so whatever it was measured from reset, so a stamp was needed,
  so a squash orphaned the stamp.

  **A row now cites `path#unit@hash`**, and `path#unit>place@hash` where a
  claim rests on one statement inside a large unit. The unit is a function or
  class for code and a heading path for a document. `.py` is read with the
  stdlib `ast`; every other language falls to a rule that needs no parser and
  no dependency — the name followed by `(`, `{` or `:`, then the block to the
  next line at the same or lower indentation, which lands on a closing brace
  because that brace sits at the declaration's own indent.

  **An anchor degrades to DRIFTED, never to BROKEN.** The two cost different
  things: BROKEN says *go edit the ledger*, which is the bookkeeping this
  removes, and DRIFTED says *go re-read the claim*, which is the work the
  ledger is for. So only the unit can be BROKEN. A narrowing anchor whose
  place has changed widens back to its unit and reports DRIFTED — precision
  buys a smaller hash, never a new way to fail. Narrowing is an escape hatch
  rather than a habit: cite the unit, and reach past it only where whole-unit
  hashing has been measured to drift rows on unrelated edits.

  A document anchor is a heading rather than a sentence, because a sentence
  breaks on any rewording while a heading survives the prose beneath it being
  rewritten.

  **Already keeping a ledger from 0.1.0? One command converts it:**
  `bin/evidence-check --migrate .` rewrites every `path:line` row to the new
  form against your current tree, drops the commit stamps, keeps the dates,
  and names every row it cannot prove rather than guessing. Until you run it,
  an old-format row **fails the check loudly** (`OLD-FORMAT`, exit 2, with or
  without `--strict`) — the alternative was your whole ledger silently
  reading `0 ok` while nothing was checked, which is worse than a red build
  that names the one command to run.

  **Two behaviours arrive without being asked for.** After a `git commit` in
  an opted-in repository, a broken anchor prints one advisory line in the
  terminal — the row, where its content went if that is provable, and the
  `--reverify` remedy. It never blocks, and it is silent when the ledger is
  clean or absent. And where a BROKEN row's content provably moved — renamed
  in place, or moved to another file, judged by content identity across a
  bounded repo-wide scan — the check names the destination, and
  `bin/evidence-check --reverify .` re-anchors it mechanically; a whole-file
  rename heals the same way. The hash covers the region under the
  anchor with trailing whitespace and blank lines removed, so a reformat is not
  a change; indentation is kept, because in Python a dedent moves a statement
  out of the block it belonged to.

  The verdicts follow from that. **BROKEN** where the anchor is gone or appears
  more than once — an ambiguous anchor is refused loudly rather than measured,
  since with two places to look an OK would be a claim about whichever one the
  code reached first. **DRIFTED** where the content under it changed.
  **OK** prints the region's current line numbers, for a reader to open. There
  is no baseline, no stamp, no commit SHA in any row, and `evidence-check`
  calls git for nothing at all.

  **Re-verifying a row is recomputing its hash**, so it has a flag:
  `evidence-check --reverify` rewrites every resolvable row and names what it
  changed. It is deliberately separate from the check — one that refreshed what
  it was checking would report OK for ever — and it leaves a row whose anchor
  is gone alone, because that is the one row somebody has to look at.

  What this closes rather than manages: a stamp a squash can orphan, a row
  whose coordinate resolves while pointing at the wrong lines, a coordinate
  into a file newer than the baseline that could never drift, and a row that
  was stale the moment it landed because another branch changed the cited code
  and merged first. That last one had been recorded as unreachable; a content
  hash sees it on the first run, because there is no time window to look at.
  (#12, #14, #23, #31, #52, #56)
