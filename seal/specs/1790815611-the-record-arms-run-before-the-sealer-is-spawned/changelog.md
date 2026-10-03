### Added

- `broad-gate --preflight` runs the record arms before the sealer is spawned
  (#638). A refusal on one of the gate's own record arms used to arrive only
  after a whole suite, because the gate runs the repository's `Broad gate` row
  first. Six instances across five releases were read from the flow logs,
  among them a DRIFTED ledger row, a chain refusal over a `fixed at` verdict
  and a survivor, each found by the sealer after its suite. The preflight
  catches the record-arm refusals among them. A refusal that
  `round_record.py seal` raises, such as an unchecked `Pass` or `nobody` on
  the last record, still reaches the sealer. (Added 2026-10-01: #702, the
  entry after this one, closes that gap in the same release — the preflight
  now asks those refusals through `round_record.py seal --check`.)

  The preflight is the same command with the same resolved base. It applies
  every refusal of the row and then runs every other arm, in the gate's
  order and with the same arguments. It reads the row and never runs it. It
  writes no cell, no values file and no stamp, adds no worktree, and prints no
  `SEALED` or `NOT SEALED` line: its stdout opens `PREFLIGHT PASSED` or
  `PREFLIGHT FAILED`, the failing arms under the second in the failure form's
  words. It exits 0, 1 or 2 as the gate does, and `--record` beside it is
  refused. On the fixture it took 1.57 s. On this repository it took about
  11 s, most of it `evidence-check --strict`, which costs the same with the
  preflight around it as without.

  The orchestrator runs it before it spawns the sealer and spawns only on exit
  0 (`skills/code-review/orchestration.md`, `skills/implement/orchestration.md`).
  It is not the broad gate, and the sealer's run is unchanged.

### Changed

- `templates/config.md`'s example `Broad gate` row goes lint-first, `uvx ruff
  check . && uvx ruff format --check . && bin/test -q`, the order this
  repository's own row took in #634. A red suite no longer hides the two
  seconds-long linters in a repository that copies it. The prose above it
  stops naming four of the gate's six arms and points at `broad_gate.py`'s
  docstring, where they are listed in order.
