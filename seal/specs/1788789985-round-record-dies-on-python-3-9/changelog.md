- **`round_record.py` says which interpreter it needs, at entry, instead of
  dying partway through with an interpreter traceback (issue #226).** On a
  machine whose `python3` is 3.9 it died at `zip(..., strict=True)` with
  `TypeError: zip() takes no keyword arguments` — and it died there, which is
  to say after argument parsing, path resolution and the report read had all
  succeeded. So the failure read as a bug in the report, and the message named
  neither the version needed nor the flag. macOS still ships 3.9 as
  `/usr/bin/python3`, so that is the default interpreter on a common platform,
  and a repository pinning a newer one does not help because the script is
  invoked directly rather than through it. Reported from another repository on
  0.8.3.

  Fifteen lines after the imports now refuse an interpreter below the floor
  with a sentence naming the floor, the version found and the interpreter it
  was found at, and saying that nothing was read and nothing was written.
  Exit 2, which already meant *nothing was written*, and the docstring's
  exit-code line says so now rather than being quietly widened.

  **The four `strict=True` sites stay, and that is the ticket's other
  suggestion refused on grounds rather than on taste.** `CONTRIBUTING.md`
  names 3.12 as the supported floor, so dropping them would buy a few more
  lines before the next 3.10+ construct, at the price of the invariant the
  comment above the first one states: both of the reader's passes keep indices
  intact, so the two reads are the same file line for line, and a length that
  differed would truncate the hidden set — which is that check reporting clean
  because it read less.

  **The guard runs before `chain = load(CHAIN, ...)`, and the placement is
  load-bearing.** That assignment reads and executes a second file at import,
  before `main()` is ever called, and it succeeds on 3.9 — so a guard written
  in `main()`, which is where one naturally goes, would still let the operator
  watch exactly the progress the ticket is about. A mutation that moved it
  there left every end-to-end case green and was caught by one case reading
  the module's own AST.

  **The floor is not imported from `.github/scripts/run_tests.py`, and the
  reason is the argument rather than the convenience.** A read that can fail
  gives the guard a second way to die on the one machine that has no other way
  of being told what is wrong; and a fallback-safe read still has to name a
  floor in its `except` branch, so the second spelling survives the import
  anyway. The number is pinned by a test instead, which is the mechanism this
  repository already uses for the same number in five other places. That pin
  ties the repository's two floor authorities together for the first time:
  `test_release_hygiene.py` reads `ruff.toml`, the runner's own suite reads
  `run_tests.py`, and nothing read both.

  **The class was enumerated by construction and five members were deferred,
  each with an answerer.** Twenty-five entry points ship; six carry a
  construct newer than the floor. `.github/scripts/gather_changelog.py`,
  `.github/scripts/fold_ledger.py`, `skills/implement/scripts/seal.py` and
  `skills/verify/scripts/session_cost.py` use `datetime.UTC` (3.11) and
  `hooks/root-migrate.py` uses `zip(strict=)` — three of them named after a
  literal `python3 ` in the release checklist, one invoked by the harness, and
  one that ends a run report. A new case re-runs that enumeration on every
  suite run, so a seventh cannot arrive as a traceback on a stranger's
  machine.

  The scan's own spelling was wrong twice and the record says so, because it
  is the same failure both times — an instance the pattern could not reach.
  `zip\([^)]*strict=` hid the site in `round_record.py#inherited_rows`, where
  an inner call closes a parenthesis before the keyword is reached; and
  `datetime\.UTC` hid `session_cost.py`, which spells the module
  `import datetime as dt`. Review round 1 found the second by re-deriving the
  class from the AST rather than from the table, which is what an enumeration
  is for.
