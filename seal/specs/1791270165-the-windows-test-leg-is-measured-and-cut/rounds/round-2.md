# 1791270165-the-windows-test-leg-is-measured-and-cut — review round 2

| Field | Value |
|---|---|
| Target SHA | 068f9fc5bdc750184648e97a8aae5af835f925ac |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #845 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `458ae587c8ddf72b979ddaa1daaa1656831dbcc7..ae88b6265aad24aaa561bda43b02591c6eaaad31`, 2 commits |
| Contract changes | none |
| New units | ceiling_from (depth 1); test_an_empty_variable_is_unset_and_a_decimal_is_seconds (depth 1); test_a_ceiling_of_zero_or_less_is_refused_naming_the_variable (depth 1) |
| Fix of a fix | first — 🟡 2 at tests/conftest.py#CASE_CEILING_S, a unit round-1's fixes changed |
| Needs a fix | yes — 🟡 1 (the refresh recipe's orphaned commits and missing timeout); 🟡 2 is fix or justify |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round for round 1's fixes at `c84ac48e..254130b0`. The reviewer was asked to open each fix, inheriting round 1's verdicts, judge the rest of `a9d7b0e5..068f9fc5` without running the full suite, and read every workflow's checks on the pull request for the pushed HEAD. Before the round the orchestrator ran `uvx ruff check` and `ruff format --check` on the four changed test files, `bin/survivor-check --range a9d7b0e5...HEAD --exempt <item>/survivors.md` (exit 0) and five touched and neighbouring modules (706 passed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The refresh recipe names commits 43326715 and 340dc6fa, which the squash into the release branch orphans, and omits the `timeout` the one unsharded Windows job needs, where the only value to copy is a shard's 20 against a measured 33 m 36 s | `CONTRIBUTING.md:194` | **fixed** `15cbd596` | fixed at 15cbd596; read; `docs/the-evidence-ledger.md` records the orphaned-commit failure; `phases/phase-3.md:32` holds the 33 m 36 s; `test.yml:78` reads the matrix's timeout |
| 🟡 2 | `SPECSEAL_CASE_CEILING_S` is parsed with `int()` at conftest import: an empty or decimal value stops the whole suite at collection, and zero or less fails every case | `tests/conftest.py:851` | **fixed** `15cbd596` | fixed at 15cbd596; executed: fresh imports with five values, and a module run under the empty value ending in ImportError while loading conftest |
| ⬜ 3 | `_stopped_untouched`, `_stopped_touched` and `_named_and_fixed_once` still say built once, which is per worker under xdist; round 1's correction took one instance of the class | `tests/test_a_fix_of_a_fix_is_counted.py:500` | **fixed** `15cbd596` | fixed at 15cbd596; executed: local `--durations`, five stopped cases at 15.5 to 16.2 s of setup each and two location cases at about 7 s |
| ⬜ 4 | The ledger's S7 row claims the variable without the anchor or evidence for it, and nothing pins that CI never sets it | `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md:19` | **fixed** `ae88b626` | fixed at ae88b626; read; a correction to the run's paperwork |
| 🟢 | round 1's blocking finding is closed — the survivor is excused with true grounds and `hygiene` is green | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/survivors.md` | confirmed | executed: the check exits 1 without the file and 0 with it over both ranges; hygiene run 37477813381 succeeded at `068f9fc5` |
| 🟢 | round 1's finding 2 is closed — the variable raises the ceiling for one run and CI sets nothing | `tests/conftest.py:851` | confirmed | executed: the module run passed, the new case among it; the new defect in the same line is finding 2 of this round |
| 🟢 | round 1's finding 3 is closed — the stopped templates build in setup | `tests/test_a_fix_of_a_fix_is_counted.py#a_stopped_run` | confirmed | executed: local `--durations`, every stopped case's build in its setup row |
| 🟢 | round 1's findings 4, 5, 6, 9 and 10 are closed — each sentence corrected | `tests/test_a_slow_case_names_itself.py:45`, `.github/workflows/test.yml:105`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:970`, `phases/phase-5.md:52`, `overview.md:24` | confirmed | read |
| 🟢 | round 1's finding 7 is closed — the recipe names the switch and the hidden-file flag | `CONTRIBUTING.md:193` | confirmed | read; the new defect in the same paragraph is finding 1 of this round |
| 🟢 | round 1's finding 8 stays answered — the call-only limit is named in three places | `CONTRIBUTING.md:182` | confirmed | read |
| carried | round 1's four confirmations: the budget is Q6 (a), the shards make the whole, the 4a sample and 4b cuts keep their claims, the ceiling under xdist | `tests/conftest.py`, `.github/workflows/test.yml` | confirmed | carried from round 1; the fixes touched none of the code they rest on except docstrings |

## Paste-ready fixes

```markdown
`.test_durations` goes stale as cases are added, which unbalances the
Windows shards and drops no case. To refresh it, push a branch on which
`test.yml` runs the Windows leg as one job again for a single run: one
Windows entry with `store: "--store-durations"` in place of the four shard
entries, with a `timeout` for the whole leg rather than a shard's 20 (it
ran 34 minutes unsharded when the file was first made, so 55 by the rule
beside the values); `${{ matrix.store }}` on the pytest line; and an
`actions/upload-artifact@v4` step with `path: .test_durations` and
`include-hidden-files: true` (the name starts with a dot, which the action
skips by default). Download the artifact with
`gh run download <run> -n <artifact>`, make its line ends LF, commit it,
and restore the shards.
```
```python
# tests/conftest.py — replaces the CASE_CEILING_S line; the two constants
# above it stay.


def ceiling_from(environ):
    """The ceiling for this run: Q6's 90 unless `CEILING_VARIABLE` holds a
    positive number of seconds. An empty value is unset; anything else
    stops the run with a sentence naming the variable, rather than with
    `int()`'s traceback."""
    raw = environ.get(CEILING_VARIABLE, "").strip()
    if not raw:
        return CASE_CEILING_DEFAULT_S
    try:
        seconds = float(raw)
    except ValueError:
        seconds = 0.0
    if not seconds > 0:
        raise ValueError(
            f"{CEILING_VARIABLE}={raw!r} is not a positive number of seconds; "
            f"unset it for the {CASE_CEILING_DEFAULT_S} s ceiling"
        )
    return int(seconds) if seconds.is_integer() else seconds


CASE_CEILING_S = ceiling_from(os.environ)
```
```python
# tests/test_a_slow_case_names_itself.py — add `import pytest` at the top,
# then:


def test_an_empty_variable_is_unset_and_a_decimal_is_seconds():
    assert ceiling_read_by_a_fresh_import(SPECSEAL_CASE_CEILING_S="") == "90"
    assert ceiling_read_by_a_fresh_import(SPECSEAL_CASE_CEILING_S="120.5") == "120.5"


def test_a_ceiling_of_zero_or_less_is_refused_naming_the_variable():
    for bad in ("0", "-5", "abc"):
        with pytest.raises(ValueError, match="SPECSEAL_CASE_CEILING_S="):
            conftest.ceiling_from({"SPECSEAL_CASE_CEILING_S": bad})
```

## Executed probes

| What was run | Result |
|---|---|
| `survivor_check.py --range a9d7b0e5...HEAD` in a `--no-local` clone at `068f9fc5`, without and with `--exempt` on `survivors.md` | exit 1 with the two comment lines at `:2799-2800`; exit 0, both excused |
| the same over `--range c84ac48e..HEAD` | without the file, `spec.md:31` and `spec.md:164`; exit 0 with it |
| `gh run view` on hygiene runs 37475198770 (`c84ac48e`) and 37477813381 (`068f9fc5`) | `failure` on the survivor step; `success` |
| `bin/test tests/test_a_fix_of_a_fix_is_counted.py tests/test_a_slow_case_names_itself.py -q --durations=20` in the clone | `64 passed`, exit 0; the five stopped cases at 15.51 to 16.17 s setup, none in the call rows |
| `bin/evidence-check --strict .` in the clone | exit 0 |
| a fresh import of `tests/conftest.py` under `SPECSEAL_CASE_CEILING_S` unset, `""`, `120.5`, `0`, `-5` | `90`; `ValueError`; `ValueError`; `0`; `-5` |
| `pytest tests/test_a_slow_case_names_itself.py` with the variable set empty | ImportError while loading conftest, nothing collected |
| `gh run view` on the `tests` run 37477813592 at `068f9fc5`: job results, pytest summary lines, Windows `--durations` rows for the stopped cases | every job `success`; the shards total 13,052, which is ubuntu's; group 1 builds both templates in setup and reuses one |
| the full suite (the broad gate) | not yet run, by anyone; it is the sealer's, once, after the rounds |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:2797` | round 1's 🔴 1 — fixed |
| round-1 | `tests/conftest.py:842` | round 1's 🟡 2 — fixed |
| round-1 | `tests/test_a_fix_of_a_fix_is_counted.py:511` | round 1's 🟡 3 — fixed |
| round-1 | `tests/test_a_slow_case_names_itself.py:40` | round 1's ⬜ 4 — fixed |
| round-1 | `.github/workflows/test.yml:105` | round 1's ⬜ 5 — fixed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:970` | round 1's ⬜ 6 — fixed |
| round-1 | `CONTRIBUTING.md:184` | round 1's ⬜ 7 — fixed |
| round-1 | `tests/conftest.py:860` | round 1's ⬜ 8 — answered |
| round-1 | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/phases/phase-5.md:51` | round 1's ⬜ 9 — fixed |
| round-1 | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/overview.md:24` | round 1's ⬜ 10 — fixed |
| round-1 | `tests/conftest.py:842`, `.github/workflows/test.yml:61` | round 1's 🟢 — confirmed |
| round-1 | `.github/workflows/test.yml:75` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_guard_resolves_the_tree_it_judges.py#_sample`, `tests/test_the_seal_is_taken_once_by_the_sealer.py#a_sealed_run` | round 1's 🟢 — confirmed |
| round-1 | `tests/conftest.py:854` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The 4b cuts' yield, now with two figures: locally under `-n auto` the five stopped cases each built their own template, and on Windows group 1 of run 37477813592 one case reused a build | `overview.md` Not verified; already deferred in round 1 | the repository owner, if the figure is wanted |
