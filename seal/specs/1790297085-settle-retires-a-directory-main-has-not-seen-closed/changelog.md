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
  the working tree only. The checks on a pull request ask it at the base
  branch's tip. So a row closed on a release branch let `settle --retire`
  remove the directory in the same release, and the release pull request
  into `main` then failed. `settle` now asks where the branch forked from
  `--released-at` as well, which is the same commit as the base's tip unless
  the base has moved since. A directory closed here and still open there is
  listed under its own heading, naming the base and the rows open there, and
  `--retire` keeps it and exits 1. Where the base has moved, the heading says
  to merge it into this branch. A `--released-at` that shares no commit with
  `HEAD`, or a clone too shallow to reach the one they share, is refused at
  exit 2.
- **The changelog gather refuses a fragment that carries a line starting
  `## ` (issue #586).** Such a line ends the released section, for the
  gather and for the release note alike, so every entry after it shipped
  under no version and the note stopped short. `gather_changelog.py
  --version`, with or without `--dry-run`, now stops before it writes or
  prints a section and names each such fragment, the line number and the
  line. The remedy is to demote the line to `###` or lower in a pull request
  into the release branch, then gather again. A fragment already gathered is
  not read again.
