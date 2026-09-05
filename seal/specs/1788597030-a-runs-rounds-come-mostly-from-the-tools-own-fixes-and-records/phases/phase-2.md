# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | d53021d |
| Ran by | specseal:smith on fable-5.1 |

The `Ran by` value is transcribed the way phase 1's was: the agent is the
definition this segment was spawned from, and the model is what the
harness's own system prompt states. Neither half is the segment's idea of
what it is.

## What this phase was asked

Build phase 2 of `plan.md` and only phase 2, on branch
`feat/161-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records`,
with routing answered and the question batch closed — ask nobody anything.

1. `round_record.py close --item <dir> --round N --fixes <file> --range
   <a>..<b> [--broad-gate "<text>"] [--root <repo>] [--baseline <ref>]`.
   The fix table is `| # | Verdict | Commit or grounds |` under `## Fixes`,
   one row per finding, the verdict `fixed` (a commit that resolves and lies
   inside the range), `answered` (the grounds), or `deferred <home>` (an
   issue or a file). Applied to the verdict cells as `**fixed** `<sha>`` with
   the Grounds prefixed `fixed at <sha>` and the smith's note after it,
   `answered` with the grounds, `deferred <home>` with the home. Four
   refusals, exit 2 and nothing written: a `#` not in the table, a verdict
   outside the three, a `fixed` with no resolving commit, a finding left
   with no row. `Contract changes` from an AST comparison over the range of
   every `.py` file it touches — parameters or return arity changed — as
   `unit → site, site` with sites the enclosing top-level unit of every
   `name(` in the tree at `<b>`, `pytest only` when every site is under
   `tests/`, the basename for a module-level call. `New units` from the same
   comparison — top-level definitions and module-level constants present at
   `<b>` and absent at `<a>` — as `unit (depth N)`, `;`-separated, no comma;
   for non-`.py` files, A1's diff-line heuristic, with a trailing HTML
   comment after the table naming the files read that way. Depth: a `fixed`
   finding whose `Location` names a unit that an earlier record's `New
   units` names makes every unit the range adds in that file depth 2, and a
   depth-2 unit is refused before any cell is written, naming the unit, the
   finding, the record, and the exit the rule gives. `--broad-gate` sets its
   cell; `Pass` ticked when nothing is open after the table applies; `Fixes
   checked by` left as it stands; `chain_check --worktree` run as `new` runs
   it. Reuse phase 1's units.
2. `agents/smith.md` (`:114` and `:170-185`) and `skills/implement/SKILL.md`
   §5: a fix pass hands over the `## Fixes` table and writes no
   `phases/phase-N.md` and no `plan.md` row — its record is the round
   record `close` writes; the build's phases keep theirs. `smith.md` says
   the depth is measured by `close` from the diff rather than declared in
   the hand-back, the rule's sentence kept.
3. Tests in a sibling of `tests/test_the_record_is_generated.py`: the table
   applied and each verdict shape read back; the four refusals; `Contract
   changes` against a real diff changing one signature with one in-tree and
   one test-only call site; `New units` against a diff adding a def and a
   constant at depth 1; the depth-2 refusal seen red first, on a fixture
   whose `round-1.md` names `helper`, whose `round-2.md` locates a finding at
   `mod.py#helper`, and whose range adds `helper_guard` in `mod.py`; the
   non-Python heuristic on one `.js` file; `Pass` ticked after all rows
   close; `--broad-gate` read back; the two agent sentences pinned, each
   seen red with the sentence stashed.

Coordinates handed over and opened: `round_record.py` whole;
`chain_check.py` `fix_surface`, `depth_problems`, `DEPTH_RE`, `DEPTH_MAX`,
`NOT_YET`, `CLOSED_WORDS`, `FIX_WORDS`, `verdict_of`, `SHA_RE`,
`is_ancestor`, `resolves_to`, `field`, `checked_by`;
`templates/sdd-round.md:64-119`; the last item's `rounds/round-4.md:8-9`;
`skills/code-review/SKILL.md:339-440`; `tests/conftest.py`
`declare_routing`, `rounds_dir`. The line numbers named for `chain_check.py`
sat 60 to 90 lines above the units they named (phase 1 added lines to that
file after the prompt's figures were taken); every name resolved to the unit
it was said to name, and the offset changed nothing built on them.

## What this phase found

**The reach grammar needs the comma phase 1's cell writer refuses.** `cell`
refuses a comma in `Contract changes` and `New units` because the checker
splits on it, and `fix_surface`'s own grammar is `unit → site, site`. Both
are right, about different commas: the one between sites is structure the
writer adds, and the one that arrives inside a name is the prose the
refusal exists for. So the surface rows go through `part` — every unit and
site name refused a pipe, a newline, a comma, or a semicolon — and
`contract_entry` / `units_entry` / `surface_cell` join what `part` passed.
`cell` keeps its refusal unchanged for a string that arrives whole, and
phase 1's comma case stays green.

**`close` on a record whose every finding closed on a fix exits 1, through
the check, by design.** `Pass` is ticked because nothing is open, `Fixes
checked by` still reads `nobody — the fixes are not yet written` because
the spec leaves it for `new` N+1, and `checked_by` refuses exactly that
pair on the last record — the state that makes the verifying round
mandatory. The exit is the check's, the message names the verifying round
as the way out, and `new` for round N+1 clears it: the case
`test_a_closed_record_reads_back_through_the_next_round` runs the whole
sequence to exit 0. An orchestrator reading `close`'s exit should read the
message beside it; a 1 there is *spawn the verifying round*, not *the
record is wrong*.

**`→ pytest only` after `(depth 1)` is tolerated by `depth_problems` and
not emitted.** The last item's `round-4.md` wrote it; the walk finds one
depth marker and no comma, so it passes. The plan's grammar for `New
units` is `unit (depth N)`, so `close` writes that alone, and the test-only
fact stays in `Contract changes`, whose grammar has a place for it.

**Every OPEN finding needs a row; a finding the reviewer closed in the
report does not.** The spec says one row per finding. A reviewer may close
a finding in the report itself (`withdrawn`, `not a defect`), and a fix
pass has nothing to say about it — a row for it would overwrite the
reviewer's verdict with the smith's. `overview.md` carries the divergence.

**What "Grounds prefixed `fixed at <sha>`" was read as.** The cell becomes
`fixed at <sha>`, then ` — <note>` when the smith wrote one beside the
commit, then `; <what stood there>` when the reviewer's evidence label
stood there — so `executed` and `read` survive the close rather than being
replaced by the commit.

**What the AST comparison measures, and what it over-reports.** A
function's contract is its parameter names with a has-default flag each,
its `*args`/`**kwargs` names, and the set of arities its own `return`
statements have (0 bare, n for a tuple of n, 1 otherwise); a class's is its
`__init__` parameters; a constant has none, so a changed value is not a
changed contract. Call sites are `git grep -F "name("` at `<b>` with a
word-boundary post-filter (`my_only_tested(` is not a call of
`only_tested`), so a docstring that mentions `name(` counts as a site — the
over-reporting direction, which is the safe one for a reach list, and
recorded here rather than parsed away. A renamed file is one path, the new
one, so its units read as new. A `.py` file that does not parse at either
end falls to the diff-line heuristic and is named in the comment with the
non-Python files.

**`deferred <home>` counts open until phase 3.** `close` writes the cell as
the spec says; `Pass` stays unticked beside it because `CLOSED_WORDS` does
not carry the word yet. The case reads the cell and not the box.

**The formatter hook removed `import ast` between two edits of one batch.**
The import landed in one `Edit`, the code using it in the next, and the
hook's unused-import fix ran between them. Re-added after the block existed.
An import and its first use go in one edit.

**Seen red, and how.** All twenty cases were red before `close` existed —
at the missing `FIXES` constant, which is a weak red — so the load-bearing
lines were shown red again by mutation after the code existed: 39 mutations
in the first pass, 33 dead; the six not dead were four cases that read the
right cell and not the right thing (`call_sites`' word boundary with no
fixture, the unknown-number assertion satisfied by an off-by-one,
`field_index`'s off-by-one hidden by `fields()` keeping the last duplicate
label, the `smith.md` depth pin satisfied by the neighbouring paragraph)
and two mis-targeted mutations (`-k` cannot carry `#`; the formatter had
reflowed one line). Sharpened in `d53021d`; the second pass killed all
eight that were re-run. One mutation stays alive on purpose: replacing
`round_record.py close` in the depth paragraph with *the orchestrator* is
not caught, because the pin on that paragraph is its own sentence
(*measured rather than declared*) and the script's name is pinned by the
paragraph that owns it. Every unit this phase added is depth 1.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
