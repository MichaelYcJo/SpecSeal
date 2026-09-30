# 1790690762-arm-check-reads-every-supported-ast — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 697d2b39 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md`'s one phase, as `spec.md` and `plan.md` state it, under routing
`automation`: classify `TemplateStr` and `Interpolation` in `NOT_ARMS`, add
the range table, rewrite S4 and add S1, S2, S5 and S6, add the CI job after
`ledger` and rewrite the `pytest` matrix comment, make the module docstrings,
the two table cases and `CONTRIBUTING.md`'s job sentence true, correct the
`seal/releases/0.9.5.md` row in place, write L1-L3 into this item's fragment,
and write the changelog fragment. Every S case written first and seen red on
the interpreter the spec names, and at least one mutant killed per changed
branch.

What the spawn added to the plan:

- Q2 and Q3 take their stated defaults and `questions.md` records it: the job
  is not a required check, and there are pinned legs only. Q4 and Q5 are the
  build's to answer. Q1 is the sealer's measurement, and the build may note
  what the narrow modules do on 3.14.
- The worktree's `.venv` is Python 3.13.9. It stays, and `bin/test` must not
  rebuild it on 3.14.
- `arm_check.py` must still run on 3.12, and on 3.9 while its comment claims
  it. No `zip(…strict=`, `pairwise` or `.UTC` anywhere in it, comments
  included, and no bare `zip` (B905).
- The plan's three traps: the job goes after `ledger`, the section states the
  floor once, and no three-part version string goes under `skills/`.
- Every drifted row `bin/evidence-check .` names is re-read before
  `--reverify --checked 2026-09-29`, and `--strict` ends with 0 drifted and
  0 refused. `bin/survivor-check` runs over `origin/release/v0.16.0...HEAD`.
- Narrow runs only, and nothing is pushed.

## What this phase found

**The frame's premise about the interpreter did not hold, and the build
measured 3.14 another way.** Spec M5 and the plan's step 1 expected this
worktree to have no `.venv`, so that the first `bin/test` would build one on
3.14 and show the base's reds there. The worktree already had a 3.13.9
`.venv` at the spawn, and the spawn said to keep it. So every run the spec
places on "3.14" was run through
`uv run --isolated --no-project --python 3.14 --with pytest`, on 3.14.3, and
the same form was used for 3.12.11 and 3.13.9. `bin/test`, on the 3.13
`.venv`, ran the neighbour modules. The same premise sits under `questions.md`
Q1, which expected the sealer's broad gate here to run on 3.14. It will run on
3.13 unless the sealer chooses otherwise, and Q1's row now says so.

**Each S case, what it was red against, and where. Every run was executed.**

| Case | Red against | Python |
|---|---|---|
| S1 `test_a_module_holding_a_t_string_is_read_rather_than_refused` | the base `346b4af7`: `UnknownNodeType` naming `TemplateStr`. Also with `TemplateStr` deleted from `NOT_ARMS` | 3.14.3 |
| S2 `test_an_interpolation_is_counted_exactly_as_an_f_string_field` | the base: refused. After the fix, with `Interpolation` moved into `ARM_SHAPES`: the dispatch's `UnknownNodeType`, "`Interpolation` is listed in ARM_SHAPES and this dispatch does not handle it" | 3.14.3 |
| S3 `test_every_ast_constructor_is_classified` (assertion unchanged) | the base: names `Interpolation` and `TemplateStr`. Also with `TemplateStr` deleted from `NOT_ARMS` | 3.14.3 |
| S4 `test_the_classification_names_nothing_the_grammar_does_not_have` | the base: the old case names the five aliases. Rewritten, with the five alias ranges deleted: it names the five | 3.14.3 |
| S4, the stale direction | `TemplateStr`'s range deleted: "classified here and absent" | 3.12.11 |
| S4, the kept-off direction | `Num` bounded at `(3, 13)`: "says this Python 3.13 lacks them, and its `ast` has them" | 3.13.9 |
| S5 `test_the_range_table_holds_classified_names_and_bounds_above_the_floor` | a range added for `Frobnicate`, which is unclassified. Separately, `Interpolation`'s bound set to `(3, 12)` | 3.13.9 |
| S6 `test_every_bound_of_the_range_table_is_a_python_ci_runs_this_module_at` | committed at `538755b4` before the job existed: names 3.14, with CI running the module at 3.12 alone. After the job, with the 3.14 leg commented out, and with the job's `run:` line naming another module | 3.13.9 |
| S7 | not executable here. CI on this item's pull request runs the two legs | — |

Each mutant was applied alone by a script in the scratchpad. The script
asserted that its pattern matched, restored the file from bytes it had kept,
checked the restore by sha256, and cleared `tests/__pycache__` and the
script's `__pycache__` between mutants. Every mutant was run after the
change it mutates had been committed.

**After the change, the module on three Pythons, executed:** 3.12.11 gives
60 passed and 2 skipped (S1 and S2 cannot parse there), 3.13.9 gives the
same, and 3.14.3 gives 62 passed.

**C1, C2 and the traps, executed:**

- `uvx ruff check` and `ruff format --check` pass on both `.py` files.
- A grep of `arm_check.py` for `zip\(.*strict=`, `\.UTC\b` and a three-part
  version finds nothing.
- `tests/test_a_script_says_which_interpreter_it_needs.py` and
  `tests/test_release_hygiene.py` pass. They include the version sweep and
  the floor case.
- `skills/verify/scripts/arm_check.py hooks/review-history-guard.py` exits 0
  and prints 32 arms under `/usr/bin/python3` (3.9.6), 3.12 and 3.14.
- The job is placed after `ledger`, and
  `test_ci_runs_the_suite_at_the_floor_the_runner_holds` passes.
- `CONTRIBUTING.md`'s new words name 3.13 and 3.14 only, and
  `test_the_section_states_the_floor_once` passes.

**Two choices the plan left to the build.**

- The table is named `ONLY_ON_SOME_PYTHONS`, in the spec's suggested shape
  (Q4).
- S2's fixture is two implicitly concatenated t-strings (Q5). On 3.14 they
  parse as one `TemplateStr`, and their f-string twin parses as one
  `JoinedStr`, so the comparison also covers the concatenation.

S6 counts a job when a `run:` line hands pytest the module or the whole
`tests/` directory. It then takes every `python:` or `python-version:` pin
quoted as `"X.Y"` in that job. So the `pytest` job's 3.12 legs count as runs
of the module, and the `lint` job's 3.12 does not.

**The 0.9.5 row was corrected, not removed.** None of its three anchors was
removed. One of them, `#test_every_ast_constructor_is_classified`, drifted
because its docstring and message changed. The claim was false only in what
it said about "the grammar", so the claim was narrowed in place, a
`Corrected 2026-09-29` note was added, and the row was re-read against the
edit. `bin/evidence-check .` named 12 drifted anchors. Eleven were this
fragment's placeholders and one was that row, and each was re-read before
`--reverify --checked 2026-09-29`. After that, `--strict` gave 3086 ok,
0 drifted and 0 refused.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `pytest` matrix comment's claim that 3.13 is run because a gate runs on whatever `python3` resolves to. No 3.13 leg ever existed (spec M7) | `.github/workflows/test.yml`'s `arm-check-grammar` job and its comment, which run the one interpreter-dependent module at 3.13 and 3.14 |
| The unconditional stale-name assertion `CLASSIFIED - grammar()` is empty | the same case, made exact per Python through `ONLY_ON_SOME_PYTHONS` |
