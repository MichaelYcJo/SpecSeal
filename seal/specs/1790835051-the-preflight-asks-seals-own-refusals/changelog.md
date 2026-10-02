### Added

- `broad-gate --preflight` asks `round_record.py seal`'s own refusals before
  the sealer is spawned (#702). Three refusals were not record arms, so the
  preflight passed them and the sealer refused them after its whole suite:
  the last record's `Pass` unchecked, its `Fixes checked by` reading anything
  but `no fixes to check` (#535's shape, exactly as `new` and `close` write
  it), and a run the record's own `Target SHA` descends from. After the
  record arms, the preflight now runs `seal --check` on the work item whose
  `routing.md` names the checked-out branch. A refusal is named `seal` under
  `PREFLIGHT FAILED` with `seal`'s own sentence, exit 1, and its output is
  kept as `seal.txt`. Where no single work item declares the branch, or HEAD
  is detached, nothing is asked and one stderr line says so. The orchestrator
  types the same command as before. The ask added about one second to a
  preflight on the test fixture.

- `round_record.py seal --check` raises every refusal `seal` raises before
  the write, in the same order and with the same sentences, then prints one
  line naming the record it asked and exits 0. It writes no cell and no
  `broad-gate.md`, and runs no chain check. `seal` without the flag and the
  sealer's `broad-gate --base <base> --record <item>` are unchanged.

### Changed

- The first line of a preflight's stdout says what it did: the record arms,
  and `seal`'s refusals where a work item is declared for the branch. The
  `PREFLIGHT PASSED` and `PREFLIGHT FAILED` heads are unchanged.
