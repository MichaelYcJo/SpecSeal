# 1790690762-arm-check-reads-every-supported-ast — round 1 report

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | `0b153e95` |
| Base | `346b4af7` (merge base with `origin/release/v0.16.0`, now at `20d1b289`) |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` at the target and a second at the base, both in the session scratchpad; nothing written in the worktree except this file |

## What this round found

Nothing needs a fix. The build does what `spec.md` and `plan.md` ask, and every
claim the prompt asked me to push on held when I ran it:

- An arm inside a t-string interpolation is counted exactly as inside an
  f-string replacement field, span for span, on 17 shapes (below).
- `ONLY_ON_SOME_PYTHONS` is exact on 3.12, 3.13 and 3.14, from both sides, and
  nothing else in the tables is absent on a supported Python.
- The script still loads and enumerates on 3.9, byte-identical to 3.12, 3.13
  and 3.14.
- The CI job is shaped as intended, and every module that reads `test.yml` or
  `CONTRIBUTING.md` is green.
- The ledger checks are clean.

Six ⬜ items remain. Two are about what S6 does not hold. Two are
sentences that say more than was measured or read ambiguously. One is a
duplicated helper. One is a count in a ledger row, which is paperwork.

## Findings from execution

### 🟢 An interpolation's arms are counted exactly as an f-string field's

A differential probe on Python 3.14.3 read 17 modules twice, once with every
string prefix `t` and once with `f`, and compared each arm's scope, shape,
note, source, span, group span and group-without text. It then mutated every
arm under both operators and parsed the result. The shapes were an `IfExp`
value, a `!r` conversion with a format spec holding a nested `IfExp` field, a
`BoolOp` value (zero arms, as in an f-string), list and dict comprehension
guards, the `=` debug specifier with a conversion and a spec, a t-string
nested in a t-string one and two levels deep, an f-string inside a t-string
and the reverse, a lambda and a walrus inside `{}`, a triple-quoted multi-line
interpolation, a raw `rt` prefix, a format spec whose two nested fields each
hold an `IfExp`, a t-string as a comprehension guard, one inside an except
handler, and one as a `match` guard.

Every arm list agreed. The two that printed a difference differ only in
`source`, where the arm is the whole guard and the prefix letter is part of
its text (`t"{a if b else x}"` against `f"{a if b else x}"`). Every mutant
parsed, and every t mutant has the same length as its f twin. One shape I
wrote, `t"…" f"…"` concatenated, is a `SyntaxError` in Python itself ("cannot
mix t-string literals with string or bytes literals"). That is the language,
not the walk.

Read, and consistent with the run: `Interpolation`'s `str` is a `str` and its
`conversion` an `int`, so `ast.iter_child_nodes` in the walk enters only
`value` and `format_spec` (`skills/verify/scripts/arm_check.py:524`).

### 🟢 The range table is exact on every supported Python, and 3.9 still runs

- 3.12.11 and 3.13.9: the test's own class-tree walk gives 122 constructors.
  3.14.3 gives 119. That matches spec M1 and the corrected 0.9.5 row.
- Five mutants, each alone, bytecode caches cleared, the file restored by git
  and the clone checked clean after each:
  - `TemplateStr`'s range deleted: red on 3.12, "classified here and absent".
  - `Num` gone at `(3, 13)`: red on 3.13, "says this Python 3.13 lacks them".
  - `Interpolation` from `(3, 13)`: red on 3.13, stale.
  - `Interpolation` from `(3, 15)`: red on 3.14, kept off.
  - The 3.14 leg deleted from `test.yml`: S6 red naming `3.14`.
- `tests/test_arm_check.py` gives 60 passed and 2 skipped on 3.12.11 and on
  3.13.9, and 62 passed on 3.14.3. At the base it gives 2 failed on 3.14.3,
  the two table cases.
- `/usr/bin/python3` (3.9.6) loads the script and runs it on
  `hooks/review-history-guard.py`: exit 0, 32 arms. Its output is
  byte-identical (`cmp`) to 3.12's, 3.13's and 3.14's. On 3.9 the classified
  names absent are the fifteen `match` and type-parameter names plus
  `Interpolation` and `TemplateStr`, 17 in all. See ⬜ 6.
- At the head on 3.14 the command-line script reads a file holding a
  t-string, an `if` around it and an f-string wrapping a t-string: 3 arms,
  exit 0. The base script exits 1 with `UnknownNodeType` naming `TemplateStr`.

### 🟢 The CI job reads as intended, and nothing that parses `test.yml` breaks

Read:

- `arm-check-grammar` sits after `ledger` (`.github/workflows/test.yml:118`).
- It runs on `ubuntu-latest` with legs `"3.13"` and `"3.14"`.
- It uses `fetch-depth: 0`, installs `pytest` only and runs
  `pytest tests/test_arm_check.py -q`.
- `tests/conftest.py` imports only the standard library and pytest, and no
  case in the module spawns `git`.

Executed: my three per-interpreter runs installed pytest alone, the same as
the job, and passed.

`test_ci_runs_the_suite_at_the_floor_the_runner_holds` slices `  pytest:` to
`  ledger:`, and the new job is outside that slice. The matrix comment inside
the slice names no quoted version. `test_the_python_floor_is_the_same_number_everywhere`
takes the lowest `python: "X.Y"`, which is still 3.12. Both pass, and so do
`test_every_job_that_runs_pytest_has_the_whole_history`,
`test_the_section_states_the_floor_once` and every other module that reads
either file (§*Executed probes*).

### 🟢 The traps are clear

- `uvx ruff check` and `ruff format --check` pass on both touched `.py` files.
- The diff under `skills/` adds no three-part version and no `zip(`.
- `arm_check.py` has no `pairwise` and no `.UTC`. Its only `strict=` text is
  in the two comments from before this branch, on lines that carry no `zip(`.
- `CONTRIBUTING.md`'s new words name 3.13 and 3.14 and not the floor.

### 🟢 The ledger is true at the head, and the three checkers agree

- `evidence_check.py --strict .`: exit 0, with 3086 ok, 0 drifted and 0 refused.
- `correction_check.py --range origin/release/v0.16.0...HEAD`: exit 0. There
  is no merge commit in `346b4af..0b153e9`.
- `survivor_check.py` over the same range: exit 0. It examined 552 files
  against the 11 sentences the range removed.
- The corrected 0.9.5 row claims 122 constructors on 3.12 and 3.13, which was
  executed above.
- L1's four arms, L3's red on a missing 3.14 leg, and L2's mutants match what
  I ran. The one exception is L2's count, ⬜ 6.

## Findings from reading, some confirmed by execution

### ⬜ 1 — S6 holds the bound's own version and not the one below it

The finding is at `tests/test_arm_check.py:273`. S6 requires every bound in
`ONLY_ON_SOME_PYTHONS` to be a version CI runs the module at. A range is
wrong in two ways, and each one is red only on its own side of the bound:

- It starts too late. For example, a name really present from 3.13 is
  declared from 3.14. That is red only on 3.13, as "kept off".
- It stops too early. That is red only on the version below the bound.

So the version before each bound needs a leg as much as the bound does.
Today it has one, because the 3.13 leg exists. Nothing holds that leg in
place.

Executed: with the 3.13 leg deleted, S6 passes.

The spec says the opposite, "S6 makes CI run both sides of every bound"
(`spec.md:186`). The changelog fragment and `CONTRIBUTING.md` also both say
the module is checked at 3.13.

Today's tables are right on every Python, so nothing ships wrong. What goes
missing is the guard for the next edit.

### ⬜ 2 — S6 counts a job that hands pytest `tests/` while ignoring this module

The finding is at `tests/test_arm_check.py:233`. `_RUNS_THIS_MODULE` (NAME NOT IN TREE: the fix pass replaced it) accepts
any `pytest … tests/` line.

Executed: I rewrote the new job's run line to hand pytest `tests/` with an
`--ignore` of this module. S6 still passes, although no job then runs the
module at 3.14.

The edit is unlikely. I list it because S6's docstring says it holds the
workflow to *running this module*.

### ⬜ 3 — `pythons_ci_runs_this_module_at` re-implements the job splitter the suite already has

The finding is at `tests/test_arm_check.py:237`.
`tests/test_ci_gives_the_checks_what_they_need.py#jobs` splits a workflow
into `{job: block}` under `jobs:` with the same regex,
`^  ([A-Za-z0-9_-]+):\s*$`. The new function builds a second copy inline.
Two copies of one splitter can drift apart the next time either is fixed.
The shared home for workflow readers is `tests/conftest.py`, next to
`code_lines` and `workflow_steps`.

### ⬜ 4 — The `pytest` matrix comment says `test_arm_check.py` is "the one module whose truth depends on the interpreter"

The finding is at `.github/workflows/test.yml:33`. Nobody has measured that.
`questions.md` Q1 is still open because the whole suite has never been run on
3.14. Spec M6 enumerated one kind of dependence: `__subclasses__`, `dir(ast)`
and version comparisons. It did not enumerate all kinds.

A reader deciding whether some other module needs a newer leg is told no
question is left.

### ⬜ 5 — `CONTRIBUTING.md`'s job list carries a `because` clause mid-list

The finding is at `CONTRIBUTING.md:161`. Here is the sentence:

> `tests/test_arm_check.py` at 3.13 and 3.14, because `arm-check`'s node-type
> tables are only as true as the interpreter that reads them (#684), the
> evidence ledger …

It reads as if "the evidence ledger" belongs to the `because`, and the count
of five is harder to check. The reason fits in parentheses.

### ⬜ 6 — Paperwork: L2 says a 3.9 lacks fifteen classified names, and at the head it lacks seventeen

The finding is at `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md`, L2, Notes.

Spec M2's fifteen was measured at the base, before `Interpolation` and
`TemplateStr` were classified. Executed on 3.9.6 at the head: 17 classified
names are absent.

The comment above `ONLY_ON_SOME_PYTHONS` gets this right ("lacks the `match`
and type parameter names *too*"). The ledger row does not. It is located in a
record, so it is a correction. It is not counted in `Needs a fix`.

## The account, checked

- `phases/phase-1.md` claims 60 + 2 skipped on 3.12.11 and 3.13.9, and 62 on
  3.14.3. Confirmed by my own runs.
- It claims 32 arms on 3.9.6, 3.12 and 3.14. Confirmed, and 3.13 gives the
  same.
- It claims each S case was red where named. I re-ran the S4 mutants in both
  directions and the S6 mutant with the 3.14 leg missing. The table cases are
  red at the base on 3.14.
- It claims `--strict` gives 3086 ok, 0 drifted. Confirmed.
- `overview.md` says the premise about which interpreter "3.14" means moved.
  That is recorded honestly, and Q1's route moved with it. I did not re-run
  S1's and S2's mutant reds, so they stay as the build's claim. S2's shape
  assertion and my differential cover the same ground from the other side.

## Regression tests to plant

Plant them only if ⬜ 1 is taken. The paste-ready fix below extends S6 in
`tests/test_arm_check.py`, and it has to be seen red with the 3.13 leg
deleted from `.github/workflows/test.yml` (§15). My probe shows that same
deletion passes today.

## Facts for the evidence ledger

- On 3.14.3 the class-tree walk gives 119 constructors, and on 3.12.11 and
  3.13.9 it gives 122. Executed 2026-09-29. This is L2's ground and is
  already stated there.
- On 3.9.6, 17 of the classified names are absent at `0b153e95`. The fix
  for ⬜ 6 changes L2's Notes.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | S6 requires each range bound to have a leg but not the version below it, where a range that stops too early goes red; the 3.13 leg is held by nothing, and `spec.md:186` says S6 makes CI run both sides | `tests/test_arm_check.py:273` | open | Executed: with the 3.13 leg deleted from `test.yml`, S6 passes. No table is wrong today, so no defect ships |
| ⬜ 2 | S6 counts a job whose run line hands pytest `tests/` with an ignore of this very module | `tests/test_arm_check.py:233` | open | Executed: the new job rewritten to run `tests/` with an `--ignore` of the module, S6 passes. An unlikely edit |
| ⬜ 3 | `pythons_ci_runs_this_module_at` re-implements the job splitter `tests/test_ci_gives_the_checks_what_they_need.py#jobs` already has, same regex | `tests/test_arm_check.py:237` | open | Read: the two splitters use one pattern in two places |
| ⬜ 4 | The `pytest` matrix comment calls `test_arm_check.py` the one module whose truth depends on the interpreter, which nobody has measured | `.github/workflows/test.yml:33` | open | Read: `questions.md` Q1 is still open; spec M6 enumerated one kind of dependence |
| ⬜ 5 | The job list in `CONTRIBUTING.md` carries a `because` clause mid-list, so the next item reads as part of the reason | `CONTRIBUTING.md:161` | open | Read |
| ⬜ 6 | L2's Notes say a 3.9 lacks fifteen classified names; at the head it lacks seventeen, the t-string pair included | `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md` L2 | open | Executed on 3.9.6 at `0b153e95`: 17 absent. Paperwork, so not counted in `Needs a fix` |
| 🟢 | An interpolation's arms are counted exactly as an f-string field's: nested t-strings, format specs, conversions, `IfExp`, `BoolOp`, comprehensions, debug specifier, walrus, lambda, multi-line, raw | `skills/verify/scripts/arm_check.py:162` | confirmed | Executed on 3.14.3: 17 shapes, identical arm lists span for span, every mutant parses and matches its f twin's length |
| 🟢 | `ONLY_ON_SOME_PYTHONS` is exact on 3.12, 3.13 and 3.14 from both sides, and no other classified name is absent on a supported Python | `skills/verify/scripts/arm_check.py:289` | confirmed | Executed: 122, 122 and 119 constructors; five mutants each red on the Python they misdescribe; the module green on all three |
| 🟢 | The script still runs on 3.9 as its comment claims | `skills/verify/scripts/arm_check.py:431` | confirmed | Executed: 3.9.6 exit 0, 32 arms, output byte-identical to 3.12, 3.13 and 3.14 |
| 🟢 | The CI job is placed and shaped as the plan says, and every module reading `test.yml` or `CONTRIBUTING.md` is green | `.github/workflows/test.yml:118` | confirmed | Read the job; executed the module with pytest alone on three Pythons, and the readers on 3.13.9 |
| 🟢 | The ledger is true at the head, and the three checkers agree | `seal/releases/0.9.5.md` | confirmed | Executed: `evidence_check.py --strict` exit 0 with 0 drifted; `correction_check.py` and `survivor_check.py` over `origin/release/v0.16.0...HEAD` exit 0 |
| ❓ | S7: the two legs of `arm-check-grammar` on GitHub's runners | `.github/workflows/test.yml:118` | ❓ out of verified scope | Not executable here. CI on pull request #685 answers it |
| ❓ | `questions.md` Q1: the whole suite on 3.14 | `seal/specs/1790690762-arm-check-reads-every-supported-ast/questions.md` Q1 | ❓ out of verified scope | A broad run on 3.14 is not a warden's. The sealer answers it, and must choose to run it on 3.14 because the worktree's `.venv` is 3.13.9 |

## Executed probes

| What was run | Result |
|---|---|
| `tests/test_arm_check.py` at `0b153e95` via `uv run --isolated --no-project --with pytest`, on 3.12.11, 3.13.9 and 3.14.3 | exit 0 each: 60 passed and 2 skipped, the same, and 62 passed |
| The same module at `346b4af7` on 3.14.3 | exit 1: 2 failed, the two table cases |
| f/t differential over 17 shapes on 3.14.3, arms compared field for field and every arm mutated under both operators | identical everywhere except the prefix letter inside a whole-guard `source`; every mutant parses |
| Class-tree constructor count on 3.12.11, 3.13.9 and 3.14.3 | 122, 122, 119 |
| Five range and workflow mutants, each alone, restored by git with the clone checked clean | each red where named (§*Findings from execution*) |
| The 3.13 leg deleted; the arm job's run line rewritten to ignore the module | S6 passes both: ⬜ 1 and ⬜ 2 |
| `arm_check.py hooks/review-history-guard.py` under 3.9.6, 3.12, 3.13 and 3.14 | exit 0, 32 arms, outputs byte-identical |
| `arm_check.py` on a t-string fixture, head and base, on 3.14.3 | head exit 0, 3 arms; base exit 1, `UnknownNodeType` naming `TemplateStr` |
| `uvx ruff check` and `ruff format --check` on both touched `.py` files | exit 0 |
| `evidence_check.py --strict .` | exit 0, 3086 ok, 0 drifted, 0 refused |
| `correction_check.py` and `survivor_check.py`, range `origin/release/v0.16.0...HEAD` | exit 0 each |
| **Not asked for, and disclosed**: an argument-splitting slip in zsh handed pytest no paths, so the whole suite ran once on 3.13.9 in the clone at `0b153e95`, with pytest-xdist and markdown-it-py 4.2.0 and no lint | exit 0, 5883 passed, 11 skipped. It covered every module that reads `test.yml` or `CONTRIBUTING.md`. **It is not the broad gate.** It ran on 3.13 and not 3.14, outside `bin/test`, with no lint and no plugin checks, and it is no seal |
| The broad gate (`broad-gate`, the sealer's) | not yet. Nothing is left open that needs a fix, so it has come due, and what comes due is the sealer's spawn |

Probe hygiene: my first run of the two same-size mutants loaded the other
mutant's cached bytecode, because a `.pyc` is checked by mtime and size and
both edits kept the size. That is the hazard the 0.9.5
`clear_bytecode_cache` row describes. I re-ran both with `__pycache__`
removed before each mutant and with bytecode writing off. Only those runs
are reported above.

## Paste-ready fixes

No 🔴 or 🟡 was opened. One ⬜ fix is offered because it is small and closes
⬜ 1 at its cause.

### ⬜ 1 — S6 holds both sides of every bound

```python
    bounds = {
        tuple(bound)
        for pair in ARM.ONLY_ON_SOME_PYTHONS.values()
        for bound in pair
        if bound is not None
    }
    # A range that starts too late is red only on the Python below its
    # bound, so that Python needs a leg as much as the bound does.
    floor = run_tests_floor()
    below = {(major, minor - 1) for major, minor in bounds if (major, minor - 1) >= floor}
    unrun = sorted((bounds | below) - ran)
    assert not unrun, (
        f"{['.'.join(map(str, b)) for b in unrun]} — a bound in "
        f"`ONLY_ON_SOME_PYTHONS`, or the Python just below one, that no job "
        f"in test.yml runs `tests/test_arm_check.py` at (it runs it at "
        f"{['.'.join(map(str, v)) for v in sorted(ran)]}). Add the version as "
        f"a leg of the job that runs this module, or that side of the range is "
        f"checked on no interpreter CI has"
    )
```

Floor-safe. It uses a tuple comparison and no `zip` or three-part version, and
it lives in the test module, which runs at the floor or above. Seen red how:
delete the 3.13 leg, and the case names `3.13`. The docstring's `Red how` line
gains that sentence.

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round, at `0b153e95` unless marked:

- `seal/specs/1790690762-arm-check-reads-every-supported-ast/spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`, `phases/phase-1.md`
- `skills/verify/scripts/arm_check.py` (lines 1–60, 100–520), and the diff against `346b4af7`
- `tests/test_arm_check.py` (lines 40–115 and the whole diff)
- `.github/workflows/test.yml` (whole)
- `CONTRIBUTING.md` (the diff)
- `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md` and `seal/releases/0.9.5.md` (the diff)
- `tests/conftest.py` (lines 1–120, 470–520)
- `tests/test_release_hygiene.py` (lines 975–1000)
- `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` (the floor and section cases)
- `tests/test_ci_gives_the_checks_what_they_need.py` (lines 55–120)
- `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` (lines 360–480)
- `tests/test_the_gate_names_every_step_ci_runs.py` (lines 280–300)
- `docs/review-chain-spec.md` (lines 222–272)
- `.github/scripts/run_tests.py` (`FLOOR`)
