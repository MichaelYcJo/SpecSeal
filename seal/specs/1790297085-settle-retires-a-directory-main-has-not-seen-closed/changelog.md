- **A script copied without the sibling it loads exits 2 and says which file
  is missing (issue #590).** `fold-check`, `settle` and `round-record` each
  load another shipped script by path. Copied on their own, the first two
  exited 1, the code each uses for a problem found or a retirement refused,
  and `round-record` died with a Python traceback. All three now print one
  sentence naming the missing file and what it is for, and exit 2, the code
  for an input nothing could be read from. `settle` used to describe every
  missing file as the fold record's reader; each file now has its own
  description. `chain-check` already behaved this way.
