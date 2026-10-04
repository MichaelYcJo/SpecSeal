### Added

- `settle --retire-process` removes a released work item's process record
  without waiting for the fold (#729). The process record is `rounds/`,
  `phases/`, `survivors.md`, `broad-gate.md`, `handoff.md`, `pr.*.md`,
  `tests-todo.md` and `evidence-todo.md`, and nothing reads it after the
  release that shipped the work item. `routing.md`, `spec.md`, `plan.md`,
  `questions.md`, `overview.md` and `changelog.md` stay until the fold
  retires the directory. The arm writes no prose and runs first in the
  release checklist's step 2b, on every release, including one that skips
  the fold. Like the fold, it takes every work item present at
  `--released-at` (default `origin/main`). An item whose todo file holds an
  open row, or whose process record a ledger row anchors into, is kept whole
  and named, and the run exits 1. A file on neither list is kept and named,
  never taken. A citation from outside `seal/specs/` into a removed file is
  listed. `settle` with no flag now ends with this arm's dry run. Local mode
  is refused, as for every arm.

### Changed

- `survivor-check` no longer reports wording from a `broad-gate.md`,
  `handoff.md`, `pr.*.md`, `tests-todo.md` or `evidence-todo.md` that the
  range removed whole from a work item directory (#729). Removing such a
  file corrects none of its wording. Measured on this repository, dropping
  the process record reported 34 places from two `handoff.md` files and one
  `broad-gate.md`, none of them a survivor. A file of that kind that still
  stands is read as before, and so is a line corrected inside one.
