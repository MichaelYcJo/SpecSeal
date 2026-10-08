# 1791384162-the-macos-test-leg-runs-in-shards — review round 2

| Field | Value |
|---|---|
| Target SHA | 4cfbfc0089f99135b5bc927261539c7cbecd5da4 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 876 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `d4e2eb7e1374cb0e70a3ceb6dfa68cbfc444dc28..d4e2eb7e1374cb0e70a3ceb6dfa68cbfc444dc28`, 0 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Verifying round 2 of round 1's fixes: the range ce72430e..ef383561 plus the table and closing commits, at 4cfbfc00. The job was the answers to round 1's fixed and answered verdicts. The New units row (matrix_include_entries and its two new cases) was a finding surface. The spawn named four things to judge. First, whether the reader refuses every key beside include: at any position while still reading the tree's test.yml. Second, whether the fixture swap of exclude: for fail-fast is still a can-fail case. Third, whether the ledger corrections for ⬜ 5 to 7 are true. Fourth, whether the changelog's five-job-cap paragraph is true. It also ran the eight suite-wide guard modules once. Facts arrived labelled. Executed by the orchestrator: the close (3 fixed, 5 answered), the NOT-IN-TREE markers, and evidence-check --strict at exit 0. Read from the smith: the reds, the mutations and the 440 passed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The docstring and the refusal message say a key beside `include:` changes which jobs the entries are, and GitHub processes `include:` after `exclude:`, so an `exclude:` beside it removes no entry | `tests/test_ci_gives_the_checks_what_they_need.py:149` | answered | a note, left as it stands: refusing an `exclude:` beside `include:` is the safe direction, and only the stated reason (GitHub processes `include:` after `exclude:`) is wider than the docs; recorded here and in the pull request body; GitHub's workflow syntax reference, "All `include` combinations are processed after `exclude`" (read); the refusal itself is safe; inside `matrix_include_entries`, a unit round 1's fixes created |
| ⬜ 2 | The docstring says two other readings of `test.yml` remain, and at least five other test modules read the file | `tests/test_ci_gives_the_checks_what_they_need.py:127` | answered | a note, left as it stands: the docstring names the two readings that take Python versions out of `test.yml` without the reader; other modules read other parts of the file; `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:446`, `tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py:68`, `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:980`, `tests/test_ci_gives_the_checks_what_they_need.py:325` (read); inside `matrix_include_entries` |
| ⬜ 3 | Ledger S4 says two other readings of `test.yml` stay, the same overreach as ⬜ 2 | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:6` | answered | a note, left as it stands: the same wording as ⬜ 2, in ledger S4's claim; no check reads the count; the same readers as ⬜ 2; correction to the run's paperwork |
| ⬜ 4 | No case pins the stop at `matrix:`'s own indentation: changing `<= floor` to `< floor` leaves every case green, and the fixture's `fail-fast: false` sits before `matrix:` where the loop never reads it | `tests/test_ci_gives_the_checks_what_they_need.py:181` | answered | a note, left as it stands: the surviving mutant would refuse a valid shape and never misread one; the stop at `matrix:`'s own indentation is pinned only through the tree's `test.yml`; mutation M1 survived, 26 passed (executed); probe Q4 reads a `max-parallel:` after the matrix and is red under M1 (executed); the mutant refuses a valid shape rather than misreading one |
| 🟢 | round 1's finding 1 is closed — a key beside `include:`, before or after it, is refused naming its line, and so is an `include:` outside `matrix:` | `tests/test_ci_gives_the_checks_what_they_need.py:183` | confirmed | probes Q1 to Q3 and Q5 to Q8, executed; M2 to M5 each red, executed; the tree's `test.yml` reads as eight entries |
| 🟢 | round 1's note 2 stands as answered — both shapes are still refused, and the tree has neither | `tests/test_ci_gives_the_checks_what_they_need.py:104` | confirmed | unchanged by the fix; Q1 reads every entry of the tree, executed |
| 🟢 | round 1's note 3 is closed — the reader is `matrix_include_entries`, and its docstring says why it has no `pytest_` prefix | `tests/test_ci_gives_the_checks_what_they_need.py:120` | confirmed | every importer uses the new name (read); the four modules that call it, 124 passed, executed |
| 🟢 | round 1's note 4 is closed — the refresh paragraph says the file prices a case as Windows ran it and asks for the macOS shard times to be read again | `CONTRIBUTING.md:192` | confirmed | read against round 1's note; `tests/test_docs_line_wrap.py` green, executed |
| 🟢 | round 1's note 5 is closed — `Corrected · S4` puts 12 minutes in the past and names 12 m 42 s and 12 m 15 s | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:1` | confirmed | the three figures recomputed from `gh run view` for runs 37465328899, 37576998008 and 37577753583, executed; "the runs S4 recorded" is plural for one run, which misleads nobody |
| 🟢 | round 1's note 6 is closed — `Re-read · S9` quotes S9 word for word and the claim holds | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:13` | confirmed | `seal/releases/0.20.0.md:208` and `CONTRIBUTING.md:170` read |
| 🟢 | round 1's note 7 headline is closed — S4 now says the job's entries are read in one place | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:6` | confirmed | read; the sentence added beside it is this round's ⬜ 2 and ⬜ 3 |
| 🟢 | round 1's note 8 is closed — the changelog says a run alone, and names the five-job macOS cap on Free, Pro and Team | `seal/specs/1791384162-the-macos-test-leg-runs-in-shards/changelog.md:3` | confirmed | GitHub's limits page, 5 on Free, Pro and Team and 50 on Enterprise (read); run 37706881322's job times, executed |
| 🟢 | The pull request's CI at 4cfbfc00 is complete and green | run 37706881322 | confirmed | `gh pr checks 876` exit 0, 13 checks pass, none running; both runs' `headSha` is 4cfbfc00, executed |

## Paste-ready fixes

```python
    **`include:` has to be the matrix's only key.** GitHub runs each entry
    as a job of its own only where the matrix has no other key: beside a base
    axis an entry is merged into the axis' combinations, so the entries read
    here would no longer be the jobs. An `exclude:` removes no entry, because
    GitHub processes `include:` after it, but this reader reads no key except
    `include:` and refuses it too. A sibling key under `matrix:` is refused
    naming its line, and so is an `include:` that is not a key of the job's
    `matrix:`.
```
```python
            raise ValueError(
                "a `matrix:` key beside `include:`, which this reader does "
                f"not read: {line.strip()!r}"
            )
```
```python
    entry written another way was not an entry, and nothing said so. Two
    other cases read Python versions out of the file without it, each asking
    something else: `tests/test_release_hygiene.py` takes the floor from
    every `python:` in it, and `tests/test_arm_check.py` reads the Pythons
    of the jobs that run its own module.
```
```
Two other cases read Python versions out of `test.yml` without it, each asking something else:
```
```
Two other readings of `test.yml` stay, each asking something else:
```
```python
def test_a_strategy_key_after_the_matrix_ends_it():
    """A `strategy:` key written after the matrix sits at `matrix:`'s own
    indentation. It ends the matrix and is not a key beside `include:`."""
    old = "    runs-on: ${{ matrix.os }}\n"
    text = MATRIX.replace(old, "      max-parallel: 2\n" + old, 1)
    assert text != MATRIX
    assert matrix_include_entries(text) == matrix_include_entries(MATRIX)
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight guard modules the spawn named | exit 0, 435 passed |
| `bin/test` over the four modules that call the reader | exit 0, 124 passed |
| Q1 the reader over the tree's `test.yml` | 8 entries |
| Q2 and Q3 the tree's `test.yml` with a base axis before `include:`, and with an `exclude:` after the entries | both refused, each naming its line |
| Q4 the fixture with `max-parallel: 2` after the matrix | 3 entries read |
| Q5 trailing comments on `matrix:` and `include:` | 3 entries read |
| Q6 entries at `include:`'s own indentation, then a sibling | refused, naming the sibling |
| Q7 a sibling with a flow value, `exclude: [ { os: example-os } ]` | refused, naming it |
| Q8 a comment line at indent 4 between `matrix:` and `include:` | 3 entries read |
| Q9 `fail-fast: false` before the matrix, and after it | 3 entries read both ways |
| M1 `<= floor` to `< floor`, through `bin/mutation-check` | survived: 26 passed; red against Q4 and Q9's after case |
| M2 any parent of `include:` accepted | red: the outside-`matrix:` case |
| M3 the loop starts at `include:` rather than `matrix:` | red: both before cases |
| M4 the sibling refusal becomes a stop | red: four cases, both after cases among them |
| M5 the parent search takes `<= head` | red: both before cases |
| `gh run view --json jobs` for runs 37465328899, 37576998008 and 37577753583 | Windows groups 10 m 03 s, 12 m 42 s and 12 m 15 s as the ledger states |
| `gh pr checks 876` and `gh run view` for runs 37706881322 and 37706881341 | completed, success, `headSha` 4cfbfc00; 13 checks pass, none running |
| the full suite at the target SHA (broad gate) | not yet — not run by this round; the sealer's, after the rounds settle |

```
Q1 tree: READ 8 entries
Q2 tree + axis before include: REFUSED a `matrix:` key beside `include:` changes which jobs the entries are, and this reader does not read it: 'python: ["3.12"]'
Q3 tree + exclude after entries: REFUSED a `matrix:` key beside `include:` changes which jobs the entries are, and this reader does not read it: 'exclude:'
Q4 max-parallel after matrix: READ 3 entries
Q5 trailing comments: READ 3 entries
Q6 compact item + sibling after: REFUSED ... 'python: ["3.12"]'
Q7 exclude flow after: REFUSED ... 'exclude: [ { os: example-os } ]'
Q8 comment at indent 4 between: READ 3 entries
Q9 fail-fast before: READ 3 entries
Q9 fail-fast after: READ 3 entries
M1 survived: 26 passed; against Q4 and Q9: 2 failed, 1 passed
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_ci_gives_the_checks_what_they_need.py:144` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_ci_gives_the_checks_what_they_need.py:104` | round 1's ⬜ 2 — answered |
| round-1 | `tests/test_ci_gives_the_checks_what_they_need.py:120` | round 1's ⬜ 3 — fixed |
| round-1 | `CONTRIBUTING.md:209` | round 1's ⬜ 4 — fixed |
| round-1 | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:1` | round 1's ⬜ 5 — answered |
| round-1 | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:7` | round 1's ⬜ 6 — answered |
| round-1 | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:6` | round 1's ⬜ 7 — answered |
| round-1 | `seal/specs/1791384162-the-macos-test-leg-runs-in-shards/changelog.md:3` | round 1's ⬜ 8 — answered |
| round-1 | `.github/workflows/test.yml:53` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:550` | round 1's 🟢 — confirmed |
| round-1 | run 37703030097 | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `tests/test_release_hygiene.py:1034` reads the floor from every `python:` in the raw file, comments included | `spec.md` Out, *The other reader of `python:`*; #835's registry; already deferred in round 1 | #835's implementer |
| `heading_level` cuts a markdown section at a `#` line inside a fence | #867's frame; already deferred in round 1 | #867's implementer |
| `.test_durations` is stale | #874; already deferred in round 1 | the owner, who starts the refresh run |
