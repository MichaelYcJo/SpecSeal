# Round 2 report — the Windows test leg is measured and cut (#841)

Reviewer: warden on Opus 5.5. This is the verifying round. Target
`068f9fc5` (the round 1 close commit); the fixes it judges are
`c84ac48e..254130b0`, three commits. The branch's own range is still
`a9d7b0e5..HEAD`: `origin/release/v0.20.0` moved to `275a7ce0` (#831) and
is not merged in. Round 1's coordinates were carried from `rounds/round-1.md`
and opened again; none of its verdicts was carried without opening the code
it rests on.

## Summary

Every round 1 fix closes its finding. The survivor check passes over the
branch's range with `survivors.md` and fails without it, as it should, and
the `hygiene` workflow is green at this HEAD. The stopped-run templates now
build in setup: a local `--durations` table shows each of the five stopped
cases with 15.5 to 16.2 s of setup and none of them in the call rows.

Two of the fixes opened something new.

- The rewritten refresh recipe in `CONTRIBUTING.md` names two commits that
  exist only on this feature branch, which squashes into its release
  branch. It also leaves out the `timeout` the one unsharded Windows job
  needs: the only Windows value in the tree is a shard's 20 minutes, and
  the leg ran 33 m 36 s unsharded.
- The new `SPECSEAL_CASE_CEILING_S` is parsed with `int()` at conftest
  import. An empty value or a decimal number stops the whole suite at
  collection with a `ValueError` traceback, and `0` makes every case fail.

## Findings

### 🟡 1 — the refresh recipe names two commits a squash orphans, and omits the unsharded job's timeout

*Read*, with one fact executed (the matrix and the phase 3 figure).
`CONTRIBUTING.md:194` reads *Commit 43326715 is that change, and 340dc6fa
took it back out.* Both commits are on
`perf/841-the-windows-test-leg-tripled-in-two-weeks` only. A pull request
into `release/vX.Y.Z` is squashed (`CLAUDE.md`, the merge-method rule), so
after the merge neither SHA is an ancestor of `release/v0.20.0` or of
`main`, and `git show 43326715` in a fresh clone answers *unknown
revision*. `docs/the-evidence-ledger.md` §*A row is a content anchor, and
it names no commit* records the same failure, measured: a commit seven
ledger rows named stopped being an ancestor of the default branch. The
paragraph is durable contributor documentation, so it ships the dangling
pointer in the release.

The same paragraph tells a person to put one Windows entry with
`store: "--store-durations"` in place of the four shard entries. It says
nothing about `timeout`. The job reads `timeout-minutes: ${{ matrix.timeout }}`
(`.github/workflows/test.yml:78`), and the only Windows value a person can
copy is a shard's `timeout: 20`. The unsharded Windows leg with
`--store-durations` took 33 m 36 s in run 37458654434
(`phases/phase-3.md:32`). Copied from a shard line, the job is cancelled at
20 minutes, before `pytest-split` writes `.test_durations` at the end of the
session, so the refresh produces no file. With no `timeout` key the
expression is empty, and what GitHub does with an empty `timeout-minutes`
I did not run; it is likely either a workflow error or the 360-minute
default.

Why it matters: round 1's ⬜ 7 was that the old recipe could not be
followed. The fix made it followable for the steps it names and left out
the one value that decides whether the run produces a file.

### 🟡 2 — the ceiling variable stops the whole suite on an empty or decimal value

*Executed* in a `--no-local` clone at `068f9fc5`. `tests/conftest.py:851`
is `CASE_CEILING_S = int(os.environ.get(CEILING_VARIABLE, …))`, run when
pytest imports the conftest. Importing it with each value:

| `SPECSEAL_CASE_CEILING_S` | Result |
|---|---|
| unset | `90` |
| `""` | `ValueError: invalid literal for int() with base 10: ''` |
| `120.5` | `ValueError: invalid literal for int() with base 10: '120.5'` |
| `0` | `0`, so every passing call is failed by the hook |
| `-5` | `-5`, the same |

`SPECSEAL_CASE_CEILING_S= .venv/bin/python -m pytest
tests/test_a_slow_case_names_itself.py` ends in *ImportError while loading
conftest* at that line, and nothing runs. Setting a variable to empty is a
common way to clear it for one command. The documented form is
`<seconds>`, and a number of seconds with a decimal point is a value a
person can reasonably type. Both stop every module rather than the one
case the knob exists for, and the traceback names `int()` rather than the
variable. The unit is the one round 1's fix rewrote, so this is a finding
inside a fix.

Fix or justify. The paste-ready fix below treats an empty value as unset,
accepts a decimal, and refuses zero or less with a sentence that names the
variable.

### ⬜ 3 — two more session templates still say "built once", which is per worker under xdist

*Executed* (local `--durations`) and read. Round 1's ⬜ 6 corrected
`a_sealed_run`'s docstring: under xdist a session or module fixture is
built once per worker that draws one of its cases. The same holds for the
templates in `tests/test_a_fix_of_a_fix_is_counted.py`, and their
docstrings were not corrected. `_stopped_untouched` (`:500`) says *built
once*, `_stopped_touched` (`:516`) says *The same*, and
`_named_and_fixed_once` (`:278`) says *built once*. In the local module run
(`bin/test`, `-n auto`), all five stopped cases show 15.5 to 16.2 s of
setup, which means each built its template on its own worker, and two
location cases show about 7 s of setup each. This is the class §12 asks to
enumerate, and the fix took one instance of three. No assertion depends on
it, so it is a sentence and not a defect.

The measurement also bears on the deferral round 1 recorded. On this
machine the five stopped cases saved nothing over building their own stop.
On CI's Windows group 1 one case did reuse a build (§*CI at this HEAD*).
The question stays where round 1 sent it (§*Deferred* below).

### ⬜ 4 — the ledger's S7 row widened its claim without an anchor or evidence for the new half

*Read.* `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md:19`
now claims the sentence names `SPECSEAL_CASE_CEILING_S`, *which raises the
ceiling for one run and which CI never sets*. Its anchors are still the
constant, the sentence, the hook and the inner-run case. The case that pins
the variable, `test_the_variable_raises_the_ceiling_for_one_run_and_unset_is_ninety`,
is not among them, and the Executed column still describes phase 5's probe
only. *CI never sets it* is pinned by nothing: no case reads `test.yml` for
the variable's absence. This is a correction to the run's paperwork.

## What round 1 found, answered

- 🔴 1, the survivor. *Executed.* `survivor_check.py --range
  a9d7b0e5...HEAD` exits 1 with the two comment lines at
  `tests/test_the_seal_is_taken_once_by_the_sealer.py:2799-2800`, and exits
  0 with `--exempt` on `survivors.md`. The grounds are true: the no-session
  case still moves its fixture under a spaced directory with `shutil.move`
  right below the comment. The two `spec.md` rows excuse what the fix range
  itself removed: `--range c84ac48e..HEAD` reports `spec.md:31` and
  `spec.md:164` without the file and exits 0 with it. `hygiene` run
  37477813381 at `068f9fc5` concluded `success`; 37475198770 at `c84ac48e`
  had failed on the same two lines.
- 🟡 2, the ceiling on a busy machine. *Executed.* The variable raises it,
  CI's `test.yml` sets nothing, and the failure sentence names it. Closed,
  with 🟡 2 above opened in the same line.
- 🟡 3, the stopped template charged to a call. *Executed.* The five cases
  show their build in setup and none appears among the call rows.
  `request.getfixturevalue` is called from the function fixture during
  setup, and `callspec.params` carries the direct `touched` parameter, so
  the `[True]` case gets the touched copy. Its own assertion on
  `return 1000` holds that.
- ⬜ 4, 5, 6, 9 and 10. *Read.* Each sentence is corrected where the finding
  pointed.
- ⬜ 7, the recipe. *Read.* It now names the switch and the hidden-file
  flag, which closes round 1's finding. 🟡 1 above is new.
- ⬜ 8, the call-only limit. *Read.* `CONTRIBUTING.md`, the changelog
  fragment and `overview.md` each name it, as the answer said.
- Round 1's four confirmations rest on code the fixes did not change
  (`test.yml`'s timeouts and shards, `_sample`, `a_sealed_run`'s
  assertions, the hook) and are carried, not re-derived.

## CI at this HEAD

`hygiene` run 37477813381 at `068f9fc5`: `success`. The `tests` run
37477813592 at the same SHA: every job `success` (lint, both
`arm-check-grammar` jobs, `ledger`, and all six `pytest` jobs). The pytest
summaries read: ubuntu 12,972 passed and 80 skipped in 8 m 30 s; macOS
12,964 passed and 88 skipped in 15 m 23 s; the four Windows shards 2,800,
6,925, 918 and 2,203 passed with 17, 32, 104 and 53 skipped, between
502 s and 624 s each. The shards make 12,846 + 206 = 13,052, ubuntu's
total at the same SHA. This is CI's run, read from its logs; it is not the
broad gate, which is the sealer's.

On Windows group 1 the stopped templates built in setup (13.36 s for the
touched one, 13.14 s for the untouched one), and
`test_the_depth_restarts_at_a_stop` then ran on the copy with a 7.31 s call
and no setup row in the top 50. So on CI the cut did save one build where
two cases shared a worker, which the local run did not show.

## Regression tests to plant

- `tests/test_a_slow_case_names_itself.py`: an empty variable reads 90, a
  decimal is accepted, and zero is refused naming the variable (in the
  🟡 2 fix below).
- Nothing pins that the stopped templates build in setup. A timing
  property belongs to the `--durations` table rather than to a case, so
  none is proposed.

## Facts for the evidence ledger

- S7's row: add the anchor
  `tests/test_a_slow_case_names_itself.py#test_the_variable_raises_the_ceiling_for_one_run_and_unset_is_ninety`
  and say in the Executed column how the variable's half was shown (⬜ 4).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The refresh recipe names commits 43326715 and 340dc6fa, which the squash into the release branch orphans, and omits the `timeout` the one unsharded Windows job needs, where the only value to copy is a shard's 20 against a measured 33 m 36 s | `CONTRIBUTING.md:194` | open | read; `docs/the-evidence-ledger.md` records the orphaned-commit failure; `phases/phase-3.md:32` holds the 33 m 36 s; `test.yml:78` reads the matrix's timeout |
| 🟡 2 | `SPECSEAL_CASE_CEILING_S` is parsed with `int()` at conftest import: an empty or decimal value stops the whole suite at collection, and zero or less fails every case | `tests/conftest.py:851` | open | executed: fresh imports with five values, and a module run under the empty value ending in ImportError while loading conftest |
| ⬜ 3 | `_stopped_untouched`, `_stopped_touched` and `_named_and_fixed_once` still say built once, which is per worker under xdist; round 1's correction took one instance of the class | `tests/test_a_fix_of_a_fix_is_counted.py:500` | open | executed: local `--durations`, five stopped cases at 15.5 to 16.2 s of setup each and two location cases at about 7 s |
| ⬜ 4 | The ledger's S7 row claims the variable without the anchor or evidence for it, and nothing pins that CI never sets it | `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md:19` | open | read; a correction to the run's paperwork |
| 🟢 | round 1's blocking finding is closed — the survivor is excused with true grounds and `hygiene` is green | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/survivors.md` | confirmed | executed: the check exits 1 without the file and 0 with it over both ranges; hygiene run 37477813381 succeeded at `068f9fc5` |
| 🟢 | round 1's finding 2 is closed — the variable raises the ceiling for one run and CI sets nothing | `tests/conftest.py:851` | confirmed | executed: the module run passed, the new case among it; the new defect in the same line is finding 2 of this round |
| 🟢 | round 1's finding 3 is closed — the stopped templates build in setup | `tests/test_a_fix_of_a_fix_is_counted.py#a_stopped_run` | confirmed | executed: local `--durations`, every stopped case's build in its setup row |
| 🟢 | round 1's findings 4, 5, 6, 9 and 10 are closed — each sentence corrected | `tests/test_a_slow_case_names_itself.py:45`, `.github/workflows/test.yml:105`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:970`, `phases/phase-5.md:52`, `overview.md:24` | confirmed | read |
| 🟢 | round 1's finding 7 is closed — the recipe names the switch and the hidden-file flag | `CONTRIBUTING.md:193` | confirmed | read; the new defect in the same paragraph is finding 1 of this round |
| 🟢 | round 1's finding 8 stays answered — the call-only limit is named in three places | `CONTRIBUTING.md:182` | confirmed | read |
| carried | round 1's four confirmations: the budget is Q6 (a), the shards make the whole, the 4a sample and 4b cuts keep their claims, the ceiling under xdist | `tests/conftest.py`, `.github/workflows/test.yml` | confirmed | carried from round 1; the fixes touched none of the code they rest on except docstrings |

## Paste-ready fixes

### 🟡 1

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

### 🟡 2

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The 4b cuts' yield, now with two figures: locally under `-n auto` the five stopped cases each built their own template, and on Windows group 1 of run 37477813592 one case reused a build | `overview.md` Not verified; already deferred in round 1 | the repository owner, if the figure is wanted |

Needs a fix: yes — 🟡 1 (the refresh recipe's orphaned commits and missing
timeout); 🟡 2 is fix or justify
Loses a record or crashes: no

## Proof

Files opened: `rounds/round-1.md`, `rounds/round-1-report.md` (head),
`survivors.md`, `spec.md:26-36` and `:160-172`, `phases/phase-3.md` (grep),
the fix diff `c84ac48e..254130b0` in full, `tests/conftest.py:800-880`,
`tests/test_a_slow_case_names_itself.py`,
`tests/test_a_fix_of_a_fix_is_counted.py:270-300` and `:440-660`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py:2785-2805`,
`.github/workflows/test.yml:40-80`, `.github/workflows/hygiene.yml:1-30`
and `:225-265`, `CONTRIBUTING.md:186-197`, `docs/the-evidence-ledger.md:16-30`,
`git show 43326715 -- .github/workflows/test.yml`.
