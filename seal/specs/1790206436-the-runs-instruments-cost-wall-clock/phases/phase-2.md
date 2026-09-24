# 1790206436-the-runs-instruments-cost-wall-clock — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 5d51b319 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

The gate runs the copy the tree ships and says so (#475): `shipped_gate(root)`
in `skills/verify/scripts/broad_gate.py`, the redirect in `main` before
`gate()` with the same argument vector, one stderr line, the `gate` row
(`tree <version>` / `plugin <version>`) in `panel`, `HISTORICAL_ROWS` grows
by one with its docstring reason; the stub case, the self case and the
row/width cases red first; `agents/sealer.md` §*The command* gains the
paragraph the spec pins. `#gate` itself untouched — five ledger rows anchor
it. Verified by the three gate modules, `ruff`, and the four prose pins over
the definition.

## What this phase found

**Red first, at `2e5a4729`** (a scratch clone with the two edited test
modules copied in, run with the main checkout's interpreter, then deleted):
`9 failed` — the stub redirect with its argument vector (A7), both self
cases (A8), the `gate` row and line on a sealed run and the line on a
refusal (A9/A10), the row's value and its width, the sealer's sentence (A11),
and `test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before`
against the grown `HISTORICAL_ROWS`. Green here: `bin/test` over
`test_the_seal_is_taken_once_by_the_sealer.py`,
`test_the_gate_names_every_step_ci_runs.py` and
`test_the_gate_asks_the_range_ci_will_ask.py`, `191 passed in 27.04s`, exit 0.

**Mutation, one unit at a time, restored from kept bytes** — nine mutations
over the eight new cases, each run through `bin/test -k`:

| Mutation | Red |
|---|---|
| `shipped_gate` always `None` | the stub case |
| the realpath self check removed | both self cases |
| `gate_copy` always `plugin` | the value case |
| no elision on a long version | the width case |
| the running line dropped | the sealed-run case and the refusal case |
| the redirect line dropped | the stub case |
| the argument vector not handed over | the stub case |
| the panel's `gate` row dropped | the sealed-run case, the width case, the historical panel |
| an unreadable version reads as blank rather than `?` | the value case |

**W2, this phase's part — where the row sits and what the lines say.** The
`gate` row sits between `from` and the first blank: it is the same kind of
fact as `base` and `from` — what this run was measured against, and by what
— so `HISTORICAL_ROWS` is `("SEALED", "tree", "base", "from", "gate",
"suite", "row", "ledger", "chain")`. The running line is `broad-gate: gate
<realpath of the running script> (<tree|plugin> <version>)`; the redirect
line is `broad-gate: <root> ships its own gate; running <shipped> (tree
<root's plugin.json version>) in place of <realpath of this file> (plugin
<running copy's version>)`. In a redirect the invoking copy prints the
redirect line and the tree's copy then prints its own running line, so a
reader of stderr sees both copies once each.

**The version is elided at the frame rather than refused.** `plugin ` is
seven columns, `PANEL_VALUE_WIDTH` is 23, so sixteen columns of version fit;
a longer one is cut with `...` the way `panel` cuts the `from` row, keeping
the head because a version's head is the discriminating part. A nine-
character version fits with room, and the case pins both.

**`under()` is a separate helper on purpose.** `os.path.commonpath` raises
`ValueError` across drives on Windows, and a label must never end a run, so
the helper answers `False` there; `plugin_version` likewise answers `?` on
`OSError`, `ValueError` (bad JSON) and `AttributeError` (a JSON that is not
an object).

**`main` reads `args.root` and never `args.base`.** The root is resolved a
second time (`gate` resolves it again for itself) rather than passed in, and
`test_the_gate_asks_the_range_ci_will_ask.py`'s structural count of
`args.base` reads stayed at one.

**Where the frame does not hold: `gate` is touched by one argument, and the
five rows anchored on it drift.** `spec.md` §*Data & interfaces* and
`plan.md` §*Technical context* say `#gate` is untouched because the redirect
sits before it. The redirect does; the `gate` row does not, because `panel`
has no way to learn the gated root — `Base` carries the ref and the commit
and nothing else, and the root is a local of `gate`. So `gate`'s one call to
`panel` gained a sixth argument, `gate_copy(root)`, and `evidence-check
--strict` after this phase reports `skills/verify/scripts/broad_gate.py#gate`
DRIFTED beside `#panel`. The alternative that keeps the hash — a module
global `main` sets and `panel` reads — was refused: a caller that drives
`gate()` in process, which the fixture section of the sealer test says
exists, would then print `plugin` for a tree's own copy, and a label decided
by a side channel is the kind of fact the row exists to make readable. The
five rows (S7 and S12 of `1789002694`, the `not_as_written` row of
`1789445605`, R2 of `1789956662`, G3 of `1789985781`) are re-read in phase 4
and re-stamped where their claims hold; none is about the panel call.

**What the fixture measured about the child.** `run_gate` runs this tree's
script with `--root <fixture>`; the stub prints `sys.argv[1:]` and the case
reads `'--base', 'base'` and the fixture's absolute root back out of it, so
the argument vector reaches the child as given. The child inherits stdout,
so `console_wants_letters` is answered by the same stream in both copies.

**The remaining readers of `agents/sealer.md` stayed green**: the seven
modules the plan's `Verified by` column does not name were run as a batch
after the commit, `395 passed in 44.56s`, exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — `main` gained a branch and `panel` a row; no unit, sentence or row left the tree | none |
