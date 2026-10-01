### Changed

- The sealer's stamp names what it sealed (#666). Its panel carries the
  branch on the row under `tree`, the ref the base came from on the row under
  `base`, and an `item` row with the pull request and the work item's id
  (`#659 . 1790635412`). The panel keeps its width: a branch or ref name too
  long for its row is elided with `...`, the branch keeping its head and the
  ref its tail; a list too long for one row — the suite's counts, the
  deferred findings' homes — continues on the rows beneath, and no value is
  cut at the frame. The `from` row is gone, and so is `row`: the exit code
  the repository's row came back with now sits under the suite's counts. The
  `ledger` row shows `drifted` beside `broken` on the row beneath its `ok`.
  The `gate` row prints only where the copy of the gate that ran is not byte
  for byte the copy that was invoked, or where nothing told it which copy was
  invoked — the tree's copy run directly, or redirected by an installed copy
  older than this change — so a stamp from a seal whose branch did not change
  the gate, run through a current copy, no longer carries it; every run still
  names its copy on stderr. `rounds` says `capped` where the run ended at the
  cap, with the deferred findings and their homes on the row beneath
  (`2 deferred -> #664`), a home being the issue or the file the verdict
  names wherever it stands in the cell. `seal-stamp`'s sample shows every row the gate can
  print, and no longer says `lint clean`.

- The `SEALED` and `NOT SEALED` lines, and the label above a drawn stamp,
  read `<branch> @ <tree> against <ref> @ <base commit>`, leaving the branch
  out on a detached HEAD and the ref out where it is the commit itself. The
  label adds the pull request where the record names one. A values file
  written by an older gate still draws the label it always drew. After a
  recorded seal one more line says the `Broad gate` cell is written and not
  committed, and that CI reads the record at HEAD, so commit it before the
  pull request is marked ready. A failing `ledger` in the `NOT SEALED` form
  now ends with `evidence-check`'s own `total:` line.

- The `workflow` count, and the line beside the command that names the
  steps, cover only the steps CI runs for the base. Four steps of SpecSeal's
  `release` job run only on a pull request into `main` and two are skipped
  there, so a feature seal of SpecSeal reads `4 of 9 not answered` where it
  read `8 of 13`, a release seal reads `8 of 11`, and the line says how many
  steps it left out and why. Which steps those are is declared beside the
  partition and held against the workflow's guards, so a guard added to a
  fifth step fails the suite.

  The record's `Broad gate` cell, every exit code and every check are
  unchanged.
