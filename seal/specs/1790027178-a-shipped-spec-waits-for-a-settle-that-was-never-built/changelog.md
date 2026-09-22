- **`settle` — the fold a shipped spec has been waiting for.** `seal/README.md`
  has told every reader since the root existed that a work item's directory
  "waits until a later `settle` folds it", and nothing was ever built: 98 work
  items, 1,347 files and 15M of records that no check reads after the merge.
  The step exists now. `settle` names the released work items whose `spec.md`
  no `docs/` policy has absorbed yet, grouped by the file their ledger rows
  anchor in, with the ones it cannot group named and any held by an open
  `evidence-todo.md` row skipped and named. It writes no policy prose — that
  half is a judgment about what is still true, which
  `docs/one-root-by-lifetime.md` says the step may not make — and
  `skills/settle/SKILL.md` is the procedure a session follows to write it.
  `settle --retire` then removes the directories that prose already covers,
  and nothing else.

- **A folded work item is no longer read as a deletion, and a folded corpus is
  no longer read as everything gathered.** `unverified-check --baseline`
  called a removed released work item this branch's deletion — 97 of them in
  one commit, which is what made the fold impossible rather than merely noisy.
  It now reads the fold record and names such a directory as folded; a removal
  with nothing recorded still fails. `gather_changelog.py --check` went the
  other way and passed having examined nothing once the fragment glob went
  empty, so it now counts the markers `CHANGELOG.md` carries and refuses a
  corpus with neither.

- **A fold's prerequisites are not the two checks the design record names.**
  `docs/one-root-by-lifetime.md` §*The dependency rule* was written when this
  repository had thirteen work items; at ninety-eight, fourteen test modules
  read the record corpus and at least six carry a population floor that a fold
  turns red. `skills/settle/SKILL.md` carries that as a general rule with the
  three answers a floor takes, because any repository running this methodology
  accumulates checks over its own records.

- **Nothing was removed.** The mechanism ships and the fold of this
  repository's own ninety-seven released work items is its own work item. The
  dry run over them reports 81 grouped into 37 segments, 16 named and none
  skipped.
