### Changed

- A released ledger file never changes, and a re-read is a row in your own
  fragment (#715). Where `seal/config.md` declares the new
  `Ledger frozen from` row, which this repository now does,
  `seal/ledger.md` and every `seal/releases/<X.Y.Z>.md` are not edited after
  their release. A branch that re-reads a released row writes a
  `Re-read ·` row into `seal/ledger/<work-item-id>.md`, citing the released
  row by content, and a claim it finds false takes a `Corrected ·` row
  there instead. Two branches that re-read one released row used to meet on
  its line at their squash, after the broad gate had run; now they write
  different files, and git merges them with no conflict. A repository
  without the row keeps re-stamping in place, as before.

- `evidence-check` reads a released row together with every row that
  re-reads it. A coordinate is OK when any of those readings recorded what
  the code holds now, and DRIFTED when none did, so two branches that edited
  the same unit still leave the row DRIFTED. A `Corrected ·` row supersedes
  the row it cites. A citation into a fragment, a citing row without its
  `Re-read <date>` or `Corrected <date>` note, and a citation whose row is
  gone are each named.

- `evidence-check --reverify --into seal/ledger/<work-item-id>.md --checked
  <YYYY-MM-DD>` writes those rows: one `Re-read ·` row per drifted released
  row, never one per coordinate, each naming the work item that read it.
  Under the freeze, plain `--reverify` re-stamps the fragments, writes no
  released file, and exits 1 naming each released row it left. The commit
  advisor's repair line says the same.

- `correction-check` refuses a pull request that changes `seal/ledger.md`,
  or a release file its base already had, when the range adds a work item at
  or above the cutoff or adds none. A branch cut before the rule is read
  under the old one and told so in one line, even after it merges the
  release branch in. A `Corrected ·` row a merge drops while the released
  row it cites still stands is reported as a lost correction.

- `fold_ledger.py --split` is gone. It had run once, at 0.15.1, and its only
  act left was writing `seal/ledger.md`. The fold now refuses a `--version`
  older than the newest release file and writes nothing; a second fold for
  the newest version still joins its file. A `settle` fold writes its
  readings into `seal/ledger/<unix-seconds>-fold.md`. Under the freeze,
  `settle` names a released row anchored into a retiring directory
  `released` and says to correct it, never remove it. Once a correction
  supersedes the row, the directory can go.

- Every kind of record has one home, indexed in the new
  `docs/the-record-layout.md`. The ledger rules live in
  `docs/the-evidence-ledger.md`, and which file a change writes lives in the
  layout document. `CLAUDE.md`, `CONTRIBUTING.md`, the skills and the
  scripts that restated them now link there. A case refuses a copy put back.
  Four further steps are decided there and land later: the commit-gate
  document's split (#727), one changelog file per release (#728), a work
  item's directory by lifetime (#729), and the other rules `CLAUDE.md`
  restates (#730).
