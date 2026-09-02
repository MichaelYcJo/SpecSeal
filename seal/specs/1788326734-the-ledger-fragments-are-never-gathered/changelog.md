- **The ledger fragments fold into `map.md` at the release, and an open
  evidence-todo row refuses it.** A work item writes its evidence rows to
  `.specseal/map/<work-item-id>.md` so two branches never queue at one file,
  and nothing ever folded them back: the directory gained one file per work
  item forever and almost every pull request touched it. Release preparation
  now runs `.github/scripts/fold_ledger.py --version X.Y.Z` beside the
  changelog gather, in the same commit. It moves every fragment into
  `.specseal/map.md` under a `## X.Y.Z — <date>` heading, one `###` section
  per work item marked with `<!-- specs/<work-item-id> -->`, copies every row
  byte for byte, and removes the fragment. A row is a content anchor, so
  `evidence-check` reports the same thing before and after; measured on this
  repository's own ledger, 55 rows across six fragments all arrived. The same
  step refuses to run, naming the file, while any `specs/<id>/evidence-todo.md`
  in the tree has an open row: a row in a file with no `drained` line whose
  first cell does not begin with ✅. `--dry-run` prints and writes nothing;
  `--check` reports a fragment left behind or an open row, and the hygiene
  workflow runs it on every pull request into `main`. Both halves work on
  today's paths, so the root merge only re-points them. `CLAUDE.md`,
  `CONTRIBUTING.md`, both READMEs, `docs/branch-and-release.md`, the
  `implement` and `evidence-check` skills and the two templates no longer say
  a ledger fragment is never gathered.
