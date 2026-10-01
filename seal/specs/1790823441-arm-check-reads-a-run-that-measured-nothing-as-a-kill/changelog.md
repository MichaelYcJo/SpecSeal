### Fixed

- `arm-check` no longer reports a run that measured nothing as a perfectly
  watched module (#703). A `killed` was read from a non-zero exit under a
  mutation, and nothing ran the command without one first. So a `-k` that
  selected no case (exit 5), a module path that did not exist (exit 4) and a
  case that already failed (exit 1) each printed `killed` beside every arm,
  `0 watched by no case`, exit 0.

  With `--tests`, the command now runs once against the module as it is,
  before anything is written, under the same `--timeout`. Anything but a pass
  prints `no baseline:` with the cause (`exit 5`, the bound it did not return
  within, or the error that stopped it starting), then *Nothing was written
  and no arm was measured.*, then the command's own output, and exits 2. That
  is the code a negative `--timeout` already gets. A run that measured its
  arms still exits 0 whether or not one survived. Measured on
  `hooks/review-history-guard.py` against `tests/test_chain_hooks.py`, the
  extra run took the whole command from 107.9 s to 110.5 s on one machine.

- `arm-check` clears the cached bytecode the cases would actually load when
  `PYTHONPYCACHEPREFIX` is a relative path and `--cwd` is not the shell's
  directory (#703). CPython reads a relative prefix against the directory of
  the process that imports, which is the cases' `--cwd`. The clear read it
  against `arm-check`'s own directory, so a stale `.pyc` stayed exactly where
  the cases read it. `clear_bytecode_cache` takes that directory as `cwd`;
  a caller passing none reads the prefix as before.
