# 1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 6e85e1d2 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

S8: the module docstring, `owner`'s docstring and the comment over
`NOT_A_FILE_OPENER` name exactly the receivers the code excuses, with ⬜ 3's
sentence (a `zipfile.Path` reached by `/`, `.joinpath` or a name is judged as
`Path.open`) and D4's shape in *What no row can hold*. This work item's
`changelog.md` under `### Fixed`. The ledger fragment: E1's `Re-read ·` row
written by `evidence-check --reverify --into` with `--checked 2026-10-04`,
naming E1 and nothing else, and one new row for C1–C3. Then
`bin/evidence-check .` at 0 drifted and 0 broken,
`tests/test_no_real_identifiers.py` and ruff on the module.

## What this phase found

**The docstrings, read against the code, and the new claims executed once.**
S8 is a reading check and no case pins docstring prose in this module. The
two behavioural sentences this phase added were cheap to run, so they were
run once as a probe and not planted: `(zipfile.Path(z) / "a").open("r",
"utf-8")`, `.joinpath("a").open()` and a `zipfile.Path` bound to a name each
came back as `<expr>.open()`, and the `/` form with `encoding=` as a keyword
came back with no site; `import wave` then `def f(wave): return wave.open()`
came back with no site, the under-report the docstring now names; and
`zipfile.ZipFile.open(zf, n)` and `tarfile.TarFile(p).open()` came back with
no site, so *called on the class or built in the receiver* is what the code
does for both.

**The comment over `NOT_A_FILE_OPENER` widened as the plan said it would.**
*Receivers that open no text file* is false for `tokenize`, which opens text
in the encoding the file declares. The comment now says *whose `open` takes
no locale encoding* and names where the module list came from.

**The re-read named E1 and nothing else.** `--reverify --into` wrote one
citing row, for `seal/releases/0.18.1.md`'s E1, whose `judge` coordinate this
work moved. E1's claim, read against the new `judge`, holds: the walk is
over every tracked `.py`, the K1 calls and K2 shapes are what it reports, and
the module is resolved from the file's imports. No other released row cites a
unit this work changed. J1's hashes were stamped by `--reverify` narrowed to
the fragment with `--ledger`, which left every released file untouched.

**The records arm reads this work item once the fragment exists.** Before
it, `bin/evidence-check .` counted this work item among the unread. After
it, the arm read it with 0 refused. Phase 2's record had named stdlib
identifiers with underscores in backticks that nothing in the tree carries;
they were taken out of backticks before the fragment landed.

`bin/evidence-check .` at this phase's commit: exit 0, 0 drifted, 0 broken.
`bin/test` on the module: 137 passed. Ruff check and format check clean on
the module.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The module docstring's *and on a bare name no import binds* and `owner`'s *a bare name no import binds, read as itself* | none: phase 2 removed the behaviour; the docstrings now say the opposite |
| The comment over `NOT_A_FILE_OPENER`, *receivers that open no text file* | the same comment, reworded to *whose `open` takes no locale encoding* |
