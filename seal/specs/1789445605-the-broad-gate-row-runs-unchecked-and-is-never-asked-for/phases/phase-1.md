# 1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 9c665caa |
| Ran by | specseal:smith on claude-opus-5[1m] |

Phases 1 and 2 ride this one commit, because `agent-contract` §14 puts a
change a person reads and the document that describes it together.

## What this phase was asked

The gate refuses a value it would not run as the command it reads as. One
function in `skills/verify/scripts/broad_gate.py` returning a reason or
`None`, called in `gate()` between the row being read and the first `run`,
raising `Refused` — exit 2, nothing run. Three forms refused: the whole value
wrapped in backticks, the whole value wrapped in `$(…)`, and a trailing `&`
that is not part of `&&`. The message names the form, quotes the value, and
shows the row rewritten. Nothing stripped. Red first by reverting the call in
`gate()`.

## What this phase found

**The frame held at every coordinate.** `broad_command:218`, `missing_row:233`,
`gate:516` reading the row at `:532` and running it at `:569`,
`first_command:346` with its one caller at `:389` — all exactly as `spec.md`
§*Data & interfaces* stated them. Nothing had to be re-cut.

**#402's measured shape reproduced, and it is worse than the ticket's
headline.** With the call in `gate()` reverted, the fixture whose row is
`` `echo true; echo "a check failed" >&2; false` `` came back **exit 0, with
`SEALED` drawn and `row exit 0` in the panel**, over a check that had failed.
The same content unwrapped exits 1 and prints `NOT SEALED`. The stamp was
earnable over a red suite, and it is that pair that is now a case.

**One entry of `spec.md`'s allowed list does not hold, and building it is what
found it.** The spec says a pipe stays legal, citing #402's own steer, and
that is true of the refusal: `not_as_written` returns `None` for it. But a
pipe **cannot reach the row at all**. `hooks/config.py#CONFIG_ROW` matches a
table cell as `[^|]*?`, so a value containing `|` ends the cell there and the
line stops being a row of that table. Executed against `config_rows`:
`bin/test -q | tee out.txt` → `[]`, the backslash-escaped spelling → `[]`,
`bin/test -q && ruff check .` → the row. End to end, the gate then reports
the row as **absent** — a true message about the wrong cause.

That is a defect in the tree rather than in this phase, and it is not repaired
here: `spec.md` lists `config_rows` Unchanged, it is the shared reader for
three callers and one of them is a `PreToolUse` hook, and its shell semantics
are not one row's business. What this phase does instead is refuse to let the
document promise a form nobody can write — the allowed list carries the
measurement beside the promise, and a case pins what the tree actually does so
that the day the reader learns to carry a pipe, it says so.

**Q1, measured.** No existing fixture row takes a refused form: the module's
only `Broad gate` row is `config()`'s bare `pytest` call, and the whole module
is 88 passed with the refusal in place. Nothing went red for the wrong reason.

**Where the refusal is raised is the whole of why there is only one.** Between
`:532` and the first `run`, so `compare_at_base` → `first_command` — #402's
second surface — is closed by reachability. It is reached only after the run
the refusal precedes, so a second guard there could not fire, and a guard that
cannot fire is the counterfeit one file over.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase adds a function, a call and six cases, and takes nothing out | none |
