# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `205ac78` |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Build `plan.md`'s row 1 and nothing past it: `skills/verify/scripts/seal_stamp.py`
— the 29×32 chart as module data, `build`, the colour row writer emitting at
transitions, the letter twin, `letter`, `beside`, `stamp(rows, scale=1.0,
shape=False)`, `not_sealed(tree, base, failures)`, `pick_shape(stream)`, and
the interpreter-floor guard; `bin/seal-stamp` with its `.cmd` twin; and part 1
of `tests/test_the_seal_is_taken_once_by_the_sealer.py`: the twin and block
forms have equal width and height, a coloured row's SGR sequences are fewer
than its cells, the panel renders its `(label, value)` rows and `None` blanks,
0.75 is accepted and 0.5 refused with a sentence, `not_sealed` contains no
disc character and names every failure, `pick_shape` on a non-UTF-8 or
non-TTY stream is letters. Every case seen red first; mutations after,
restored from the implementer's own copy.

Three facts came labelled `read`: the source outside the tree (the chart, the
computing script, the panel script — to be read once, with no file in the tree
naming that directory); `hooks/console.py#to_utf8` and the rule that blocks
and colour are for a UTF-8 terminal only; the floor guard the sibling scripts
carry, and the `bin/session-cost` pair as the wrapper to copy. One fact came
`unverified` with this phase as its answerer: whether the chart at 0.75 is
still legible as letters.

## What this phase found

**The computed disc was half a cell off centre, and the case that pins
symmetry is what found it.** The source's `build` sampled each cell at its
corner (`dx = x - ox` with `ox = w / 2`), so for `w = 43` the disc's centre sat
at 21.5 while the cells' centres run 0…42 with their middle at 21. Measured on
the twin before the fix: the top rope row was 18 letters wide and the bottom
one 12, with the first line blank. #30's *a circle that is calculated cannot be
off centre* holds only when the sample point is the cell's centre; `px` now
uses `x + 0.5 - ox`, `y + 0.5 - oy`, and the chart lookup uses `math.floor`
rather than `int` because `int` truncates toward zero and would read stitch 0
twice at the top-left edge. After the fix the top and bottom rope rows are both
`OooOOOooO`, and the disc is 43×22 at 1.0 and 33×17 at 0.75 — the two sizes
the issue measured. `test_the_disc_is_symmetric_because_it_is_computed` is a
case the plan's list did not name; it pins the issue's claim and it went red
against the source's geometry.

**`pick_shape` has to be asked before the streams are reconfigured, which is
the opposite of the plan's ordering.** `plan.md`'s Technical context says the
twin is picked *after that call*. Measured: `sys.stdout` and `sys.__stdout__`
are the same object, and `reconfigure(encoding="utf-8")` moves both — under
`PYTHONIOENCODING=cp949`, `sys.__stdout__.encoding` read `cp949` before the
call and `utf-8` after it. Asked afterwards, a cp949 console would be handed
the blocks it cannot draw. `__main__` asks first, then reconfigures, and passes
the answer into `main(console_wants_letters=…)`. Phase 2's `broad_gate.py`
must do the same.

**A pipe gets letters; the plan's sentence said blocks, and the spec won.**
The same Technical context bullet reads *a UTF-8 pipe gets blocks*. `spec.md`
§Scope 1 says the twin is *chosen when stdout is not a UTF-8 terminal*, S5
says the same, and §Out says *the sealer's returned text carries the ASCII
twin; the colour form is for a person's terminal* — and an agent's stdout is a
pipe. `pick_shape` returns letters for any stream that is not a UTF-8 tty, and
`test_the_command_piped_prints_the_twin` pins it: the wrapper piped prints the
same bytes as `--shape`. Simulated with `script` under `PYTHONIOENCODING=cp949`
(a tty on another codepage): letters.

**The handoff's `payload_meter.py` does not exist in the tree.** It was named
as one of two sibling scripts carrying the floor guard; only a
`__pycache__/payload_meter.cpython-312.pyc` is present, and `session_cost.py`
carries no guard (it is `deferred` in
`tests/test_a_script_says_which_interpreter_it_needs.py#CLASSIFIED`). The
guard was copied from `round_record.py#below_floor`, the block whose comment
says it is the spelling to copy, with `seal-stamp:` as its command name.

**0.75 is legible as letters — the floor holds.** Rendered with `--shape` at
both scales and read. At 1.0 the three petals, the `W` highlight down the
centre petal, the `yyyyyyyyy` band and the foot are all distinct. At 0.75 the
lily is still a fleur: crown of three, band, foot. What it loses: the two side
petals merge with the centre one into a single `GGGGGGGGGGGGG` bar on one
row, and the highlight thins to single `W` cells. As letters every cell is a
full character, so the letter form is if anything easier to read than the
half-block form at the same size.

**A scale above 1.0 is refused too — a decision the spec does not make.**
`shrink` returns the chart unchanged for any `f >= 1.0`, so `--scale 1.5`
would have printed the 1.0 drawing while saying nothing. `check_scale` refuses
above `SCALE_CEILING = 1.0` with a sentence saying the chart is one cell per
stitch and does not enlarge; pinned in the floor case and seen red with the
ceiling moved to 2.0.

**Sizes, measured on the module.** At 1.0 the stamp with the panel is 22 rows
by 84 columns; the colour form is 12,251 bytes carrying 564 SGR sequences
(the issue's *about 12 KB*). At 0.75 it is 17 rows and 8,223 bytes.

**For phase 2.** `stamp` raises `ValueError` carrying the refusal sentence;
the command turns it into exit 2 with nothing on stdout. `not_sealed(tree,
base, failures)` takes `failures` as `[(name, lines)]` — the check's name and
the first lines the gate kept — and renders `NOT SEALED   <tree> against
<base>` first. The panel's values are the gate's data and are not ASCII-checked
by the twin: a `·` in the `ledger` value on a cp949 console degrades to `?`
under `errors="replace"` rather than crashing; `SAMPLE_ROWS` spells it `.`
and the gate may want to when the twin is chosen.

**How the cases were seen red.** All twelve ran once with the module absent
(12 failed), then eleven mutation arms each broke one unit and ran its case:
the twin dropping bottom-half cells, corner sampling, a colour code per
cell, the panel skipping `None`, the floor at 0.5, the ceiling at 2.0,
`not_sealed` appending the twin, `pick_shape` ignoring the encoding, ignoring
the tty, always letters, and the command ignoring what the console wants.
Every arm red; the module restored from bytes held by the script and
sha256-compared after each arm; `__pycache__` cleared between arms.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
