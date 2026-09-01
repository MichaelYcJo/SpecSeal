# Every branch appends to the same two files — spec

Closes #46 and #52.

## What this changes

Two files in this repository are append-mostly registries that every branch
writes to, and both cost something at the merge.

| File | What every branch does to it | What it costs |
|---|---|---|
| `CHANGELOG.md` | appends an entry under `## Unreleased` | three parallel branches shared exactly one file, and it was this one. The conflict arrives after the broad gate has run, which forces the broad gate to run again |
| `.specseal/map.md` | appends rows stamped with a commit SHA | the same conflict shape, plus a second failure: a squash discards the commit a row was stamped at, and the row's drift baseline stops resolving |

Both are fixed the same way — **one fragment per work item** — and the ledger
half needs one more thing, because a fragment alone does not tell a row where
its drift baseline comes from.

## Scope

### A. A ledger row's baseline comes from `git blame`

A row carries a `Checked` **date** and no SHA. The commit its drift is
measured from is the commit `git blame` names for that row's own line in its
ledger file.

The property that closes #52: blame is computed on the tree as it stands, so
no rewrite can orphan it. After a squash it answers with the squash commit —
the value pull request #49 wrote into seven cells by hand.

Measured on this tree rather than argued: `9b5501d` — the commit seven rows
named before #49 repaired them — is not an ancestor of `origin/main`, so a
fresh clone and CI both see BROKEN. Blame of the same file attributes twenty
lines to `e7ff924`, #48's squash commit, which is exactly what #49 typed in.

- A row that DOES carry a resolvable SHA keeps using it. Rows written under
  the old rule go on working, and nothing has to be rewritten.
- Where blame cannot answer, the ledger header's baseline is still the
  fallback. Two cases: a ledger line not committed yet (blame calls that the
  all-zero SHA), and a coordinate that resolves in another checkout, where a
  commit of THIS repository is not a diff base at all.
- Blame is read in `--porcelain`, and the format is part of the design. The
  default and `-s` forms decorate a boundary commit as `^9829412`, which
  `git cat-file` rejects; porcelain spells it plainly. Every answer is checked
  against `git cat-file` before it is used, so a name that does not resolve
  falls back rather than reaching `git diff`, where it would report "nothing
  changed".

### B. The ledger is fragmented, and the fragments are never gathered

A new work item that records evidence writes `.specseal/map/<work-item-id>.md`.
The checker already reads that glob; what is missing is where a fragment's
baseline comes from and what a work item is told to write.

**A fragment carries no baseline header**, because A removes the need for one:
every row in it gets its baseline from blame of its own line. The header
baseline survives in `.specseal/map.md` alone, as the fallback for the two
cases blame cannot answer.

`.specseal/map.md` stays where it is. The migration is incremental — the
existing rows are not moved, and the file's header says what it now is.

### C. The changelog is fragmented, and the fragments ARE gathered

A change writes `specs/<work-item-id>/changelog.md` and does not touch
`CHANGELOG.md`. Release preparation concatenates the fragments into the
released `## X.Y.Z — <date>` section.

`## Unreleased` stops existing. The fragments are the unreleased state, and a
heading by that name in `CHANGELOG.md` means somebody went back to appending
to the shared file.

A gathered fragment is marked in `CHANGELOG.md` by an HTML comment naming the
work item it came from, so gathering is idempotent and checkable. That marker
is what a release pull request is checked against.

## Acceptance

| # | Scenario | Verified by |
|---|---|---|
| 1 | A ledger row with no SHA in its Checked column is measured from the commit blame names for its line | `tests/test_a_row_measures_from_its_own_history.py` |
| 2 | A row that carries a resolvable SHA still measures from it | the same file, and `tests/test_ledger_stamps_resolve.py` unchanged |
| 3 | A ledger line not committed yet falls back to the header baseline and says so | `tests/test_a_row_measures_from_its_own_history.py`, and `tests/test_evidence_check_hardening.py::test_missing_baseline_skips_drift_and_says_so` unchanged |
| 3b | A boundary line — the first line of every fragment — gets a name git resolves, not blame's `^`-decorated one | the same file |
| 4 | A fragment with no header baseline is checked row by row rather than skipped | `tests/test_a_row_measures_from_its_own_history.py` |
| 5 | The gather script concatenates every ungathered fragment into a dated section, in work-item order | `tests/test_the_changelog_is_gathered_at_release.py` |
| 6 | Gathering twice writes one copy | the same file |
| 7 | `--check` fails while a fragment is ungathered and passes once it is in | the same file |
| 8 | A release pull request runs that check | the same file, reading `.github/workflows/hygiene.yml` |
| 9 | No document still tells a change to stamp a branch commit or to edit `CHANGELOG.md` | the same file |

## Not in scope

- Moving the rows already in `.specseal/map.md` into fragments. Decision 2 is
  an incremental migration on purpose: a bulk move would re-date every claim
  in the file without re-reading one of them, which is the failure the per-row
  baseline exists to prevent.
- Shipping the changelog convention to plugin users. Fragmenting a changelog
  is this repository's own release convention; the plugin mandates no
  changelog at all. The ledger half DOES ship, because the checker ships.
- Re-anchoring shifted-only coordinates (issue #12 / #14). Blame moves the
  baseline; it does not renumber a coordinate.
