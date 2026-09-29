# Feature Specification: arm-check reads every supported `ast`

<!-- seal/specs/1790690762-arm-check-reads-every-supported-ast/spec.md — WHAT
this work delivers and how we'll know. The policy documents in docs/ outrank
this file; cite them, don't restate. -->

Milestone 49 (0.16.0), item L: #684. Item K's broad gate (#683) found it when
`bin/test` built its `.venv` on Python 3.14. This branch is cut from
`release/v0.16.0` at `346b4af7`.

**The class.** `skills/verify/scripts/arm_check.py` holds a classification of
AST node types, `ARM_SHAPES` and `NOT_ARMS`, and says it is **total over the
grammar**. `_refuse_unknown` refuses any node type outside it. Two cases in
`tests/test_arm_check.py` hold the tables to `ast`'s own class tree. Both
compare against **the interpreter that happens to run them**. The repository
supports every interpreter from the floor (`.github/scripts/run_tests.py#FLOOR`,
3.12) upward (`README.md` §*Install*: "Python 3.12 or newer"). CI runs the
suite at 3.12 alone (`.github/workflows/test.yml`, job `pytest`). So a grammar
change in any newer Python is invisible to every unattended run. The docstring
promise that "a Python release that adds a node type turns that case red"
(`arm_check.py`'s module docstring, `tests/test_arm_check.py`'s module
docstring) holds only on a contributor's machine that happens to have that
Python.

Python 3.14 changed the grammar in both directions at once:

- it **added** `TemplateStr` and `Interpolation` (t-strings, PEP 750). The
  shipped script refuses any file that holds a t-string, on a user's 3.14
  `python3`. The tables are not total there.
- it **removed** `Bytes`, `Ellipsis`, `NameConstant`, `Num` and `Str`. They
  are classified, and 3.12 and 3.13 still have them as classes, so they
  cannot simply be deleted. The "names nothing the grammar does not have"
  case goes red on 3.14 for a table that is correct.

The class is **a table whose truth depends on the interpreter, checked on one
interpreter**. It closes when each name the supported interpreters do not all
have carries the versions that have it, every interpreter checks its own slice
exactly in both directions, and CI runs the check at every version where a
slice changes. Adding the two t-string names alone closes the instance and
leaves the class: the next Python repeats #684.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #684 (the ticket) | The two symptoms, their reproduction on 3.13 and 3.14, and the requirement that "the tables have to hold for every interpreter at or above the floor, not only the one running" |
| `CONTRIBUTING.md` §*Running the checks* ("Python 3.12 is the supported floor", held as `FLOOR`) and `README.md` §*Install* ("Python 3.12 or newer") | The range is the floor and everything newer. No ceiling is declared anywhere, so 3.14 is supported today |
| `.github/scripts/run_tests.py#FLOOR` comment and `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#test_ci_runs_the_suite_at_the_floor_the_runner_holds` | The `pytest` job runs the whole suite at the floor and only there. This item does not change that job (§*Scope*, out) |
| `tests/test_release_hygiene.py#test_the_python_floor_is_the_same_number_everywhere` | The lowest `python: "X.Y"` anywhere in `test.yml` must stay the floor. A newer leg is allowed |
| `tests/test_ci_gives_the_checks_what_they_need.py#test_every_job_that_runs_pytest_has_the_whole_history` | A new job that runs pytest checks out with `fetch-depth: 0` |
| `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR` and `ruff.toml` (`B` selected) | `arm_check.py` carries no `zip(` with `strict=` on its line and no `.UTC`, **in code or in a comment**, and no bare `zip` (B905) |
| `arm_check.py#_node_arms`, the comment at the first `zip` | The script claims more than the floor: it "runs under whatever `python3` `bin/arm-check` finds — measured on macOS's own, a 3.9". The build keeps that true (constraint C2) |
| `tests/test_release_hygiene.py#LOADED`, `#timers_in` and `#test_no_loaded_file_names_a_version_at_or_above_the_running_one` | `skills/` is swept for version-shaped tokens above the plugin's own version. A three-part Python version in `arm_check.py` is refused as a timer, so the script names minor versions only, as the tuple `(3, 14)` or the text `3.14` |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | §12: the class above, enumerated below. §14: `arm-check`'s output on a t-string file changes from a refusal to a list of arms, so a case pins it (S1, S2). §15: every new case is seen red, on a named interpreter |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `arm-check` is report-only and exits 0 either way (`skills/verify/SKILL.md` §*`arm-check` asks condition 2…*), so it is not a gate. The failure direction is stated anyway, below, because the change makes the walk accept input it refused |
| `CLAUDE.md` §*The goal a design is chosen against* | The version facts are checked by CI, not by whichever interpreter a contributor has. The prompt budget is zero |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | New rows go to `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md`. The row in `seal/releases/0.9.5.md` whose claim 3.14 made false is corrected where it stands (`plan.md` §*Ledger*) |

## What was measured before the frame, and by whom

| # | Fact | Label |
|---|---|---|
| M1 | `ast`'s constructor set, taken the way `tests/test_arm_check.py#grammar` takes it, compared with `CLASSIFIED` at `346b4af7`: 3.12.11 and 3.13.9 have 122 names, and both directions are empty. 3.14.3 has 119: missing `Interpolation`, `TemplateStr`; extra `Bytes`, `Ellipsis`, `NameConstant`, `Num`, `Str`. `AugLoad`, `AugStore`, `ExtSlice`, `Index`, `Param` and `Suite` are still classes on 3.14. No new abstract sum type appears on 3.14 (the same 13 names `ABSTRACT` lists) | executed by the framer: a probe run outside the tree under `uv run --isolated --python 3.12/3.13/3.14` and under `/usr/bin/python3` |
| M2 | On 3.9.6 the script loads, and its tables name 15 constructors 3.9 lacks (`Match*`, `match_case`, `TryStar`, `TypeAlias`, `TypeVar`, `ParamSpec`, `TypeVarTuple`). A superset is harmless at run time, because `_refuse_unknown` only looks up the names a parse produced | executed by the framer, same probe |
| M3 | On 3.14.3, `t"{x if a else b!r:>{b}} and {a or b}"` parses to `TemplateStr(values=[Interpolation(value=IfExp(…), str='x if a else b', conversion=114, format_spec=JoinedStr([Constant, FormattedValue])), Constant, Interpolation(value=BoolOp(Or…), …)])`. With the two names added to `CLASSIFIED` at run time, `arms()` finds the `IfExp` inside the interpolation as one arm, exactly as it does for the same text as an f-string, and does not count the `a or b`. `mutate()` under both operators gives a module that parses | executed by the framer, same probe |
| M4 | `bin/test tests/test_arm_check.py` with a 3.14 `.venv`: 2 failed. With a 3.13 `.venv`: 58 passed. `arm-check` on a t-string file on 3.14: `UnknownNodeType` | executed by #684's author; not re-run by the framer |
| M5 | `uv python list --only-installed` on this machine: 3.12, 3.13, 3.14 and the system 3.9. This worktree has no `.venv`, so the first `bin/test` here builds one with `uv venv --python ">=3.12"`, which takes the newest: 3.14 (`run_tests.py#build`) | executed (the listing) and read (`#build`) by the framer |
| M6 | The class, enumerated by construction: `git grep` over every tracked `.py` for `__subclasses__`, `dir(ast)` and a comparison of `sys.version_info` against 3.13 or later finds one site, `tests/test_arm_check.py#grammar`. The one other interpreter-derived set in the suite, `DROPPED_BY_THE_STRIP` in `tests/test_the_hooks_hide_what_a_renderer_hides.py`, is already asserted as what 3.12, 3.13 and 3.14 all give (`#test_the_strips_set_is_the_one_measured`) | executed (the grep) and read by the framer |
| M7 | `.github/workflows/test.yml`'s `pytest` matrix comment says "3.13 is what a current install resolves `python3` to, and a gate runs on whatever that name happens to be", and the matrix below it has no 3.13 leg. `git log -S'"3.13"'` on the file finds no commit that ever had one | executed (the log) and read by the framer |

## Scope

**In.**

1. `TemplateStr` and `Interpolation` classified in `NOT_ARMS`, in the group
   "an expression that computes a value and forks on nothing", beside
   `JoinedStr` and `FormattedValue`. The grounds: an interpolation, like a
   `FormattedValue`, tests nothing. Its `value` and `format_spec` are nodes
   the walk already enters through `ast.iter_child_nodes`, so any arm inside
   them is counted where it stands (M3). `str` is a plain string and
   `conversion` an integer.
2. A table in `arm_check.py`, beside the classification, of every classified
   name the supported interpreters do not all have, with the first Python that
   has it and the first that no longer does (either end open). Today that is
   the two t-string names (from 3.14) and the five constant aliases (until
   3.14).
3. The "names nothing the grammar does not have" case made exact per
   interpreter, in both directions. A name the table says the running Python
   has must be in `ast`. A name the table says it lacks must not be. The case
   also refuses a range for an unclassified name, and a range bound at or
   below the floor.
4. A case that every range bound is a Python version CI runs
   `tests/test_arm_check.py` at, read from `.github/workflows/test.yml`.
5. A CI job in `test.yml`, after `ledger`, on `ubuntu-latest`, that runs
   `tests/test_arm_check.py` at 3.13 and 3.14. The `pytest` job's 3.12 legs
   cover the floor. The job checks out at `fetch-depth: 0`.
6. Every touched sentence made true: `arm_check.py`'s module docstring on how
   totality is checked, `tests/test_arm_check.py`'s module docstring and the
   two table cases' docstrings and messages, `test.yml`'s matrix comment (M7),
   and `CONTRIBUTING.md` §*Running the checks*' "CI runs four jobs".
7. The ledger: the `seal/releases/0.9.5.md` row whose claim 3.14 made false
   corrected in place, and this item's rows in its own fragment.
8. The changelog fragment, `seal/specs/1790690762-arm-check-reads-every-supported-ast/changelog.md`.

**Out, each with its grounds.**

- **`run_tests.py` choosing the newest interpreter.** It is not the defect. Its
  docstrings, `CONTRIBUTING.md` §*Running the checks* and `build`'s
  `uv venv --python ">=3.12"` all state the intent as the floor **or newer**.
  A plugin user's `python3` may be 3.14 (`README.md` §*Install*), and the
  newest-interpreter build is the only run anywhere that met this defect.
  Pinning it to the floor would make the local suite as blind as CI.
- **The whole suite on 3.13 or 3.14 in CI.** The `pytest` job is stated to run
  at the floor (`run_tests.py#FLOOR` comment), and a case holds it there. The
  whole suite on 3.14 has not been measured green by anyone in the tree (#684
  reports one module). The sealer's broad gate in this worktree will run on a
  3.14 `.venv` (M5), which measures it (`questions.md` Q1). A red there
  outside `tests/test_arm_check.py` is a new issue, not this item.
- **macOS and Windows legs for the new job.** `ast`'s class tree does not vary
  by platform.
- **The broad gate mirroring the new job.** The gate's partition covers
  `hygiene.yml`'s `release` job (`docs/the-broad-gate.md` §*What the gate runs,
  and how the list is kept true*), and it already runs the suite on whatever
  interpreter the `.venv` holds rather than on CI's.
- **Python 3.15.** No interpreter on this machine has it, and `setup-python`
  legs are pinned by this item. Adding it is one leg plus any ranges it needs,
  and item 4's case makes a missing leg red. Whether a floating leg should
  catch it unattended is `questions.md` Q3.
- **Tightening 3.9 into a guarantee.** The floor is 3.12. The 3.9 comment in
  `_node_arms` is kept true by the build (C2), not promoted.
- **`skills/verify/SKILL.md`.** Its sentence "refuses an AST node type it does
  not recognise" stays true, and it says nothing about interpreter versions.
- **#226's five scripts below the floor** (`seal/follow-up.md`). Unrelated.

## User scenarios & acceptance *(mandatory)*

Each case is written and seen red **before** the change that turns it green,
on the interpreter named. The base is `346b4af7`. "3.14" is the `.venv` that
`bin/test` builds in this worktree (M5). "3.12" and "3.13" mean
`uv run --isolated --no-project --python 3.1X --with pytest python -m pytest …`
from the worktree root.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · a t-string file is read, not refused | Given a module with `if a:` around `return t"{x if a else b}"`, when `arms()` reads it on 3.14, then it returns the `If` arm and the `IfExp` arm and raises nothing | executed: a new case in `tests/test_arm_check.py`, skipped below 3.14 because the source does not parse there. The t-string lives inside a string literal, so the test file itself parses on 3.12. **Red on 3.14 at the base**: `UnknownNodeType` naming `TemplateStr` |
| S2 · an interpolation counts exactly as an f-string's replacement field | Given a module whose t-string interpolations hold an `IfExp`, a `BoolOp` value, a comprehension with an `if` guard, a `!r` conversion and a format spec with a nested field, when `arms()` reads it and the same text with each `t` prefix replaced by `f`, then the two arm lists agree on shape, note, source and line, and `mutate()` under each operator gives a module that parses | executed: a new case, skipped below 3.14. **Red on 3.14 at the base** (refused). After the fix, **red on 3.14** with `Interpolation` moved into `ARM_SHAPES`, which the dispatch in `_node_arms` refuses |
| S3 · the tables are total on the running Python | `tests/test_arm_check.py#test_every_ast_constructor_is_classified`, unchanged in its assertion | executed on 3.12, 3.13 and 3.14. **Red on 3.14 at the base**, naming `Interpolation` and `TemplateStr` (M4) |
| S4 · the tables name nothing the running Python lacks, and a range is exact | Given the range table, when the second table case runs, then every classified name the table places on the running Python is in `ast`, and every classified name it excludes is not | executed on 3.12, 3.13 and 3.14. **Red on 3.14 at the base**, naming the five aliases. After the fix: **red on 3.12** with `TemplateStr`'s entry deleted (declared present, absent), and **red on 3.13** with `Num` given an upper bound of 3.13 (declared absent, present) |
| S5 · the range table holds only classified names and only bounds above the floor | Given the range table, then each name in it is in `CLASSIFIED`, and each bound is above `run_tests.py#FLOOR` | executed on any interpreter. **Red** with a range added for an unclassified name, and with a bound of `(3, 12)` |
| S6 · every version where a slice changes is one CI runs the module at | Given `test.yml`, then every range bound is a Python version at which some job runs `tests/test_arm_check.py` (the `pytest` job over `tests/`, or the new job) | executed on any interpreter, reading the workflow as text through `tests/conftest.py#code_lines`, no YAML parser. **Red before the new job exists**, naming 3.14. Write it before the job |
| S7 · CI runs the module at 3.13 and 3.14 | Given a pull request, when CI runs, then the new job's two legs run `tests/test_arm_check.py` and pass | executed by CI on this item's pull request. `test_every_job_that_runs_pytest_has_the_whole_history`, `test_the_python_floor_is_the_same_number_everywhere` and `test_ci_runs_the_suite_at_the_floor_the_runner_holds` stay green |

**Constraints the build meets, verified rather than cased.**

| # | Constraint | Verified how |
|---|---|---|
| C1 | `arm_check.py` carries no `zip(` with `strict=`, no `.UTC`, no bare `zip`, no three-part Python version | executed: `tests/test_a_script_says_which_interpreter_it_needs.py`, `uvx ruff check` on the file, and `tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one` |
| C2 | The shipped script still enumerates on the interpreters it claims | executed: `/usr/bin/python3 skills/verify/scripts/arm_check.py hooks/review-history-guard.py` (3.9) and the same under 3.12 and 3.14 exit 0 and print the same total |
| C3 | Every existing case in `tests/test_arm_check.py` stays green on 3.12, 3.13 and 3.14 | executed, the three runs above |

## Data & interfaces

- `arm_check.py`: `NOT_ARMS` gains two names in an existing group. One new
  module-level constant, the range table. Suggested shape:
  `{name: (first_version_having_it or None, first_version_without_it or None)}`,
  with versions as `(major, minor)` tuples. `CLASSIFIED`, `NOT_ARM_NAMES`,
  `_refuse_unknown` and the `UnknownNodeType` message are unchanged. The
  command line is unchanged.
- `tests/test_arm_check.py`: the second table case rewritten, S1, S2, S5 and S6
  added. `grammar()` and `ABSTRACT` unchanged.
- `.github/workflows/test.yml`: one new job after `ledger`. The `pytest` and
  `ledger` jobs unchanged apart from the matrix comment (M7).
- Ledger coordinates: `plan.md` §*Ledger*.

## Failure direction and prompt budget

The walk now **accepts** a file it used to refuse. A wrong accept is the
failure `_refuse_unknown` exists to prevent: an arm inside a node the walk
misjudged goes uncounted, and the total still reads like a total. The grounds
against it are M3: an interpolation's arms are counted where they stand, and
S2 holds that equal to the f-string reading, which the 0.9.5 ledger rows
already cover.

The table check becomes **permissive** for a declared name on a Python the
declaration excludes. A wrong declaration could hide a stale name. S4 checks
every declaration from both sides, and S6 makes CI run both sides of every
bound.

No person is asked anything, by the build or by the change. Prompt budget:
zero.

## What the changelog fragment says

Under `### Fixed`, one bullet, written for a plugin user:

- **`arm-check` reads a module holding a t-string on Python 3.14.** It used to
  refuse the file, naming `TemplateStr`. An interpolation's arms are now
  counted exactly as an f-string's are. Its node-type tables are checked on
  every Python from 3.12 to 3.14, so a table that is right for one interpreter
  and wrong for another no longer passes unnoticed (#684).

## Open questions → questions.md

Nothing here waits on a person. `questions.md` lists the judgments the ticket
left open and how the tree answered each, then the rows still open.

Framed 2026-09-29 by framer, before the build.
