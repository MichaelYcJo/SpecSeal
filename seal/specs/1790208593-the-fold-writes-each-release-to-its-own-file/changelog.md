- **The fold writes each release's ledger rows to a file of its own
  (issue #547).** `fold_ledger.py --version X.Y.Z` writes
  `seal/releases/X.Y.Z.md` instead of appending to `seal/ledger.md`, and a
  second fold for one release joins that file and keeps its date. Every
  reader of the ledger reads the new glob: `evidence-check` (and its
  `--reverify`, `--migrate` and narrowing notice), the commit-time advisor,
  the session-start migration, `correction-check` and `settle`. A row is a
  content anchor, so where it sits changes nothing a check reports.
  `fold_ledger.py --split` moves the sections already folded into
  `seal/ledger.md` into their own files once, byte for byte, and rewrites the
  one row anchored into a moved section. It runs at the release that ships
  this change, after its `--dry-run` is read, and `fold_ledger.py --check`
  refuses a `seal/ledger.md` that still heads a release, naming `--split`.
  What this buys: `seal/ledger.md` shrinks to about 100 lines and stops
  growing, a release adds a file, and a re-stamp's diff or a conflict's hunks
  land in the 10–307-line file of the release the row belongs to. **What it
  does not buy:** the ticket expected it to remove the ledger's merge
  conflicts, and it does not. Every conflict in the merge that prompted it
  was two branches re-stamping the same row, and that row still conflicts
  wherever it stands. Removing that conflict means changing where a
  re-verification is recorded, which is a 0.16.0 question.
- **A ledger fragment's own marker line is folded once (issue #553).** Twenty
  work items' fragments began with their own `<!-- specs/<id> -->` line, and
  the fold wrote its marker in front of each, so `seal/ledger.md` marked
  twenty work items twice and `fold_ledger.py --check` counted 118 over 98
  folded sections. The fold drops a fragment's own leading marker. `--check`
  refuses a work item marked more than once anywhere in the ledger, naming
  each file and line, and so does `tests/test_release_hygiene.py` on every
  pull request. The twenty doubled lines are removed, every row
  byte-identical.
