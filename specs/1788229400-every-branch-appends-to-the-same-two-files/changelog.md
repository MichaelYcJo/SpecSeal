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
  request repaired those cells by hand. **The baseline comes from `git blame`
  of the row's own line now.** Blame is computed on the tree as it stands, so
  no rewrite can orphan it: against the same file it attributes twenty lines to
  `e7ff924`, the squash commit that discarded `9b5501d` — exactly what the
  repair typed in. The Checked column keeps the **date** somebody read the
  code, which is also the guard on what blame gives up: it answers for the
  row's line, so re-wording a Notes cell moves the baseline with nobody
  re-reading the code, and a row read in August that says August is how a
  reader sees the gap. Rows already stamped are unchanged and are not being
  rewritten — a SHA written into a row still wins.

  Blame is what makes the second registry splittable. **A work item's evidence
  rows go in `.specseal/map/<work-item-id>.md`**, which the checker's default
  globs already read, and such a fragment needs no baseline header at all:
  every row in it measures from its own line. `.specseal/map.md` is not moved —
  the migration is incremental, the rows in it stay where they are, and its
  header now says so. Ledger fragments are never gathered back, because a row
  is checked against the code it cites rather than concatenated.

  Read in `--porcelain`, and the format is load-bearing: blame's default and
  `-s` forms decorate a boundary commit as `^9829412`, which `git cat-file`
  rejects, and the first line of every fragment is a boundary line. Every
  answer is checked against `git cat-file` before it reaches `git diff`, where
  a name that resolves to nothing would report "nothing changed" — a pass
  produced by a failure. (#52)
