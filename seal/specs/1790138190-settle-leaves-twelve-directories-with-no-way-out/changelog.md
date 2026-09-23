### Changed

- A released work item that wrote no `spec.md` is retired by a rule now,
  not kept forever: `settle` prints it under its own heading, and
  `settle --retire` removes it with no marker in `docs/` when nothing in its
  `overview.md` `## Not verified` or its `evidence-todo.md` is still open. A
  directory whose record still holds an open row is kept, with every such
  row printed; closing the row (a re-homed row is closed too, ✅ naming
  where it went) in a pull request that merges before the one retiring the
  directory is what lets the next retirement take it. Before, these directories had no way out, and after
  two folds `settle` reported nothing left to fold while ten of them sat in
  `seal/specs/`. For every directory a retirement would take, the report also
  lists the open memo rows, the paths outside `seal/specs/` that cite into
  it, and the `tests/` files that read `seal/specs` — the three things a fold
  used to find by hand.
- The three pull-request checks read a rule retirement as one, through the
  same predicate `settle` asks: `unverified-check --baseline` names it apart
  from a fold, `chain_check --baseline` prints `retired: by the rule`, and
  `survivor-check` leaves a retired directory — folded or by the rule — out
  of its range, so a fold no longer owes a `survivors.md` row. Each still
  refuses a directory whose history held a `spec.md`, one with an open row
  at the merge base, and a file removed from a directory that stays.
- A fold is not a work item. `skills/settle/SKILL.md` says it opens no
  directory, is not asked the routing question, waives each commit with the
  no-review token in front, and is judged at its pull request; and that it
  changes `seal/ledger.md` only by removing a row the guard named and
  re-verifying a row its own prose edited.

### Fixed

- `settle --retire` no longer removes a directory a ledger row anchors
  into. It keeps that directory, removes the rest, exits 1, and names each
  row with its file, its line and its claim, saying whether the row is to be
  REMOVED or narrowed. Before, the row survived the removal and
  `evidence-check --strict` reported it broken only afterwards — twice on one
  branch. `settle` names such rows for every released directory before any
  prose is written, reading every ledger `evidence-check` reads and every
  line of each, including rows above the first section marker and rows
  inside a fence.
- A `seal/` root with no work item left is a green state. `settle` and
  `settle --retire` exit 0 and say the fold is complete when `seal/specs/`
  is empty or — as on a fresh checkout, since git keeps no empty
  directory — absent; `unverified-check` does the same for that path and
  still refuses any other missing one. Before, both exited 2, so every pull
  request after a complete fold would have failed, the shipped
  `templates/hygiene.yml` included.
  (`1790138190-settle-leaves-twelve-directories-with-no-way-out`, #517,
  #511)
