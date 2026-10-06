# Round 3 report — the Windows test leg is measured and cut (#841)

Reviewer: warden on Opus 5.5. This is the verifying round and the last
round of the run: `round-record` said the reopening is spent. Target
`3468d368` (the round 2 close commit). The fixes it judges are
`458ae587..ae88b626`, two commits. The branch's range is still
`a9d7b0e5..HEAD`; `origin/release/v0.20.0` moved to `275a7ce0` (#831) and
is not merged in. Round 1's and round 2's coordinates were carried from
`rounds/round-1.md` and `rounds/round-2.md` and opened again. No verdict was
carried without opening the code it rests on, except where the table says
`carried`.

## Summary

Round 2's 🟡 2 is closed with its class. `ceiling_from` treats an empty
value as unset, takes a decimal, and refuses zero, a negative value, a word
and `nan` with a sentence that names the variable. The new empty-value case
goes red when the old `int()` line is put back. Round 2's two ⬜ are closed
as well.

Round 2's 🟡 1 is closed at both of its instances, but not as a class. The
recipe no longer names a commit, and it now gives the unsharded job a
`timeout` of 55. The values that only commit 43326715 held were the
`timeout`'s neighbours too, and one of them is load-bearing today: the
upload step's `if: always() && matrix.store != ''`. Following the recipe as
written, the refresh run uploads nothing (🟡 1 below).

CI is green at this HEAD on every workflow, and the four Windows shards
add up to the whole suite again.

When 🟡 1 is fixed or answered, nothing this round found stays open, and
what comes due is the sealer's spawn for the broad gate.

## Findings

### 🟡 1 — the refresh recipe's upload step has no condition, so the run it describes uploads no file

*Executed* in a `--no-local` clone at `3468d368`, with one step *read*.
`CONTRIBUTING.md:194` tells a person to add *an
`actions/upload-artifact@v4` step with `path: .test_durations` and
`include-hidden-files: true`*. It does not say the step needs
`if: always() && matrix.store != ''`. Commit 43326715 carried that
condition and the name `test-durations-${{ matrix.os }}`; round 2's fix took
the commit's name out of the paragraph, which was right, and with it the
only place a person could find either value.

The condition is load-bearing now in a way it was not when 43326715 ran.
Since 340dc6fa the suite holds
`tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py`, which
asserts that every Windows entry is a shard. I applied the recipe to the
clone's `test.yml` exactly as worded: one Windows entry with
`store: "--store-durations", timeout: 55`, `${{ matrix.store }}` on the
pytest line, and the upload step with the two keys it names. Then:

- `test_every_group_of_the_windows_split_runs_exactly_once` fails with
  *a Windows leg that is not a shard*.
- `test_the_pytest_line_hands_the_split_to_pytest` fails, because the
  line no longer ends in `${{ matrix.split }}`.

So the refresh branch's `pytest` step exits non-zero on every leg, by
construction. A step after it runs only under `always()`, so the upload the
recipe describes is skipped and the run produces no artifact. The file
itself is written: a separate probe ran `pytest-split` 0.11.0 under xdist
with one failing case and `--store-durations`, pytest exited 1, and the
durations file held both cases.

The other half of the condition matters as soon as a person adds
`always()` alone. Without `matrix.store != ''`, ubuntu and macOS also run
the step. Their checkout holds the committed `.test_durations`, so they
upload the stale file, and ubuntu finishes about 25 minutes before the
unsharded Windows job. `upload-artifact@v4` refuses a second artifact of
the same name in one run, so Windows' upload fails, and the artifact a
person downloads is the file they meant to replace. That last part is
*read* from the action's documented behaviour and was not run.

Why it matters: this is the class round 2's 🟡 1 named. That finding was
*what the unsharded job needs that the recipe omits*, and the fix supplied
one of the omitted values. The recipe is durable contributor documentation
and ships with the release. Its only purpose is to produce a new
`.test_durations`, and as worded it cannot. The paragraph is a unit round
2's fix rewrote, so this is a finding inside a fix; its `Location` is a
`.md`, which the fix-of-a-fix count does not read.

## What round 2 found, answered

- 🟡 1, the refresh recipe. *Read.* The paragraph names no commit, and the
  unsharded entry now carries a `timeout`. 55 is Q6's rule applied to
  33 m 36 s (`phases/phase-3.md:32`): 1.5 times is 50.4, rounded up to 5.
  Both instances are closed; the class is not, which is 🟡 1 above.
- 🟡 2, the ceiling variable. *Executed.* A fresh import with each value:
  unset or `""` reads 90, `" 120 "` 120, `120.5` 120.5, `1e3` 1000; `0`,
  `-5`, `abc` and `nan` each stop with `ValueError:
  SPECSEAL_CASE_CEILING_S='…' is not a positive number of seconds; unset it
  for the 90 s ceiling`. Run under pytest with `abc`, the run stops with
  *ImportError while loading conftest* and that sentence on the `E` line.
  With the old `int()` line put back in the clone,
  `test_an_empty_variable_is_unset_and_a_decimal_is_seconds` goes red, so
  the case was seen red. `inf` is accepted and switches the ceiling off;
  that is a value a person types on purpose, and I do not count it.
- ⬜ 3, *built once*. *Read.* `_named_and_fixed_once`, `_stopped_untouched`
  and `_stopped_touched` now say once per session and once per xdist worker.
  Every session or module fixture this branch adds is one of those three or
  `a_sealed_run`, which round 1 corrected, and `test.yml:106` says *in its
  own worker*. The class is closed.
- ⬜ 4, the ledger's S7 row. *Executed.* The claim is split into two rows:
  the hook row no longer claims the variable, and the new row anchors
  `ceiling_from` and the three variable cases and says that *CI sets no such
  variable* is read and checked by no case. `bin/evidence-check --strict .`
  exits 0 in the clone.

## What round 1 found, answered

Carried from round 2, which opened each one against the code at
`068f9fc5`. The fix range `458ae587..ae88b626` touched none of the code
those verdicts rest on except the three docstrings of ⬜ 3, the `ceiling_from`
lines and the recipe paragraph, each answered above.
`bin/survivor-check --range 458ae587..HEAD` reports that no removed wording
is still standing.

## CI at this HEAD

*Executed* (logs read). `gh pr checks 845` shows every check passing at
`3468d368`, the pull request's head. The `tests` run is 37482442997 and the
`hygiene` run is 37482443016; both concluded `success`.

- ubuntu: `12975 passed, 79 skipped in 306.31s`, a 5 m 22 s job.
- macOS: `12967 passed, 87 skipped in 735.11s`, a 12 m 36 s job.
- Windows, four shards: 2,801, 6,926, 918 and 2,203 passed, with 17, 32,
  104 and 53 skipped. That is 12,848 and 206, which makes 13,054, the same
  total as ubuntu and macOS. The slowest shard job, group 3, took
  10 m 27 s against its 20.
- lint, ledger, both `arm-check-grammar` legs and hygiene's `release`
  job passed.

The suite on CI is not the broad gate. It is the sealer's run, once, and it
has not happened.

## Regression tests to plant

None for 🟡 1. A case could read the recipe for the condition, but a
sentence pinned by a regex is weaker than the paste-ready paragraph. If
the owner wants one, it belongs in
`tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py`: assert
that `CONTRIBUTING.md` names `always()` and `matrix.store != ''` in the
paragraph that names `--store-durations`.

## Facts for the evidence ledger

None new. The S9 row, `CONTRIBUTING.md#"## Running the checks"`, will drift
when the recipe changes, and the fix should read it again.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The refresh recipe's upload step carries no `if: always() && matrix.store != ''`: the shard cases fail on the refresh branch by construction, so the step is skipped and no file is uploaded, and with `always()` alone ubuntu uploads the stale committed file first | `CONTRIBUTING.md:194` | open | executed: the recipe applied in a clone, two shard cases red; a probe showed `pytest-split` writes the file on a red session; the name conflict is read from the action's documented behaviour |
| 🟢 | round 2's finding 1 is closed at both instances — no commit named, and the unsharded entry's timeout of 55 | `CONTRIBUTING.md:191` | confirmed | read; 1.5 times 33 m 36 s is 50.4, rounded up to 55; the class is open as 🟡 1 |
| 🟢 | round 2's finding 2 is closed with its class — the variable's empty, decimal, zero, negative, word and nan values | `tests/conftest.py#ceiling_from` | confirmed | executed: fresh imports with eight values beside the cases' own, a pytest run under `abc`, and the empty-value case red with the old line put back |
| 🟢 | round 2's ⬜ 3 is closed — the three templates say per worker | `tests/test_a_fix_of_a_fix_is_counted.py#_stopped_untouched` | confirmed | read; every session or module fixture the branch adds was checked |
| 🟢 | round 2's ⬜ 4 is closed — the ledger's S7 claim is split and anchored | `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md:19` | confirmed | executed: `bin/evidence-check --strict .` exit 0 |
| carried | round 1's verdicts and round 2's carried confirmations | `tests/conftest.py`, `.github/workflows/test.yml`, `tests/test_a_fix_of_a_fix_is_counted.py` | confirmed | carried from round 2; the fix range touched none of their code but what this table answers above |

## Paste-ready fixes

```markdown
`.test_durations` goes stale as cases are added, which unbalances the
Windows shards and drops no case. To refresh it, push a branch on which
`test.yml` runs the Windows leg as one job again for a single run: one
Windows entry with `store: "--store-durations"` in place of the four shard
entries, with a `timeout` for the whole leg rather than a shard's 20 (it
ran 34 minutes unsharded when the file was first made, so 55 by the rule
beside the values); `${{ matrix.store }}` on the pytest line; and an
`actions/upload-artifact@v4` step with `if: always() && matrix.store != ''`,
`path: .test_durations` and `include-hidden-files: true` (the name starts
with a dot, which the action skips by default). Both halves of the
condition are needed. On that branch the shard cases in
`tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py` fail,
because the matrix has no shards, so without `always()` the upload is
skipped although the file was written. Without `matrix.store != ''`,
ubuntu and macOS upload the committed file under the same name first.
Download the artifact with `gh run download <run> -n <artifact>`, make its
line ends LF, commit it, and restore the shards.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_slow_case_names_itself.py tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py -q` in a `--no-local` clone at `3468d368` | `11 passed`, exit 0 |
| `bin/evidence-check --strict .` in the clone | exit 0 |
| `bin/survivor-check --range 458ae587..HEAD` in the clone | exit 0, no removed wording standing |
| a fresh import of `tests/conftest.py` under `SPECSEAL_CASE_CEILING_S` set to `inf`, `nan`, `1e3`, `" 120 "`, a thousand written with an underscore, three Arabic-Indic digits, `0.0001`, `abc` | `inf`; ValueError; `1000`; `120`; `1000`; `300`; `0.0001`; ValueError, each naming the variable |
| `pytest tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py` with the variable set to `abc` | exit 4, ImportError while loading conftest, the `E` line is the sentence naming the variable |
| the clone's `test.yml` edited as the recipe words it, and the conftest line put back to `int()`; the shard module, the timeout case and the two new variable cases run; both files restored | 3 failed, 3 passed: the two shard cases and the empty-value case red; the timeout case and the zero-or-less case green |
| `pytest-split` 0.11.0 under `-n 2` with `--store-durations` over one passing and one failing case, in a scratch directory, deleted | exit 1, and the durations file held both cases |
| `gh run view 37458654434` and its artifacts | every job `success`; artifact `test-durations-windows-latest`, which the shard module did not yet exist to fail |
| `gh pr checks 845` and `gh run view` on runs 37482442997 and 37482443016 at `3468d368` | every check `pass`; the Windows shards total 12,848 passed and 206 skipped, 13,054 as on ubuntu and macOS; slowest shard 10 m 27 s |
| the full suite (the broad gate) | not yet run, by anyone; it is the sealer's, once, after the rounds |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The 4b cuts' yield, with the two figures round 2 recorded | `overview.md` Not verified; already deferred in round 1 and carried by round 2 | the repository owner, if the figure is wanted |

Needs a fix: yes — 🟡 1 (the refresh recipe's upload step needs `if: always() && matrix.store != ''`)
Loses a record or crashes: no

## Proof block

Files opened this round: `.github/workflows/test.yml`, `CONTRIBUTING.md`
(the *Running the checks* section), `tests/conftest.py` (the ceiling
section), `tests/test_a_slow_case_names_itself.py` (case list and the fix
diff), `tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py`,
`tests/test_a_fix_of_a_fix_is_counted.py` (the fix diff's docstrings),
`seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md` (the
fix diff's rows), `rounds/round-1.md` (its header and verdicts),
`rounds/round-2.md`, `rounds/round-2-report.md` (to the round 1 answers),
`phases/phase-3.md` (the lines naming run 37458654434), and commit
43326715's `test.yml` diff.
