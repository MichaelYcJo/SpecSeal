# 1790690762-arm-check-reads-every-supported-ast — review round 1

| Field | Value |
|---|---|
| Target SHA | 0b153e9578a8838beffa6af309b2b81c775ba536 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #685 — https://github.com/MichaelYcJo/SpecSeal/pull/685 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 over the build range `40c11190..0b153e95` at HEAD `0b153e95`, against `346b4af7`. Spec compliance first, then quality. The pushes:
- an interpolation's arms counted exactly as an f-string's, by an f-against-t differential on 3.14;
- `ONLY_ON_SOME_PYTHONS` checked against each supported interpreter's `ast`, both directions, and 3.9 still running the script;
- the CI job's placement and reach, and every module that parses `test.yml` or `CONTRIBUTING.md`;
- the floor constructs;
- the ledger correction and L1–L3.

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

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
