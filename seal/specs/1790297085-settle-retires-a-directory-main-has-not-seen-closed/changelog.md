- **A script copied without the sibling it loads exits 2 and says which file
  is missing (issue #590).** `fold-check`, `settle` and `round-record` each
  load another shipped script by path. Copied on their own, the first two
  exited 1, the code each uses for a problem found or a retirement refused,
  and `round-record` died with a Python traceback. All three now print one
  sentence naming the missing file and what it is for, and exit 2, the code
  for an input nothing could be read from. `settle` used to describe every
  missing file as the fold record's reader; each file now has its own
  description. `chain-check` already behaved this way.
- **`settle --retire` keeps a directory whose closure has not reached the
  branch the release merges to (issue #602).** A work item with no `spec.md`
  is retired once nothing in its record is open, and `settle` asked that of
  the working tree only. The checks on a pull request ask it where the
  branch forked from its base. So a row closed on a release branch let
  `settle --retire` remove the directory in the same release, and the release
  pull request into `main` then failed. `settle` now asks at the merge base
  of `--released-at` and `HEAD` as well. A directory closed here and still
  open there is listed under its own heading, naming the base and the rows
  open there, and `--retire` keeps it and exits 1. A `--released-at` that
  shares no commit with `HEAD` is refused at exit 2.
