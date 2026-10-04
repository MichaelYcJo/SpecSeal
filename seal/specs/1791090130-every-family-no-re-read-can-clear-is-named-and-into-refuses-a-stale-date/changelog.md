### Fixed

- `evidence-check --reverify --into` no longer writes a `Re-read ·` row that
  a newer reading outranks (#746). A `Re-read ·` row is a reading dated
  `--checked`. Where a coordinate it would carry already had a reading dated
  later, in a fragment `--ledger` left out or in a release file, the row
  cleared nothing. The run still wrote it and exited 0, and `--strict`
  straight after exited 2. Now that row is left whole. Nothing is written or
  recorded for it, a `LEFT` line names it with `--checked`, the later
  reading's date and place, and the repair, and the run exits 1. The other
  rows of the same run are still written. A `--checked` equal to the newest
  date ties with it and is written. Where the newest reading is dated after
  today, which no `--checked` can reach, the line names a `Corrected ·` row
  as the repair.

- `docs/the-evidence-ledger.md` names the five things `--reverify` leaves at
  exit 0 while `--strict` exits 2 (#746). They are a released row corrected
  twice, a BROKEN coordinate outside a released row under the freeze, a
  family rooted in a fragment whose anchored statement is gone, a citing row
  refused `MALFORMED`, and a citation whose released line changed. It used to
  name the first one only. A case holds each one in every mode, narrowed and
  not.
