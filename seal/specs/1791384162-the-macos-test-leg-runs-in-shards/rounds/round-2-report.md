# 1791384162-the-macos-test-leg-runs-in-shards — round 2 report

| Field | Value |
|---|---|
| Round | 2, verifying |
| Target SHA | 4cfbfc0089f99135b5bc927261539c7cbecd5da4 |
| Target | round 1's fixes, `ce72430e..ef383561` (4 commits), and the table and closing commits after them |
| Reviewer | warden on Opus 5.5 |
| Where | a `git clone --no-local` at the target SHA, under the session scratchpad's `1791384162-the-macos-test-leg-runs-in-shards/round-2/clone`; removed before hand-over |

## How the findings relate

Every finding round 1 recorded as fixed or answered is closed. The new
reader refuses a key beside `include:` before or after it, it still reads
the tree's `test.yml` as its eight entries, and each break of its new branch
that a case should catch is caught but one.

What this round found sits in the sentences around the reader, plus the one
break no case catches:

1. The docstring gives a reason for refusing `exclude:` that GitHub's own
   documentation contradicts. The refusal is still safe. Only the reason
   and the refusal message are wrong (⬜ 1).
2. The correction for round 1's note 7 fixed the headline but added a
   sentence that goes too far the other way. It says two other readings of
   `test.yml` remain, and at least five other test modules read the file.
   The sentence is in the docstring (⬜ 2) and in the ledger's S4 (⬜ 3).
3. The fixture swapped `exclude:` for `fail-fast: false`, but placed it
   before `matrix:`, where the loop never reads it. So the stop at
   `matrix:`'s own indentation is pinned by no case (⬜ 4).

None of the four would ship a defect. `Needs a fix` is `no`.

## Findings from reading, confirmed by probes

### ⬜ 1 · The docstring says an `exclude:` changes which jobs the entries are, and GitHub says it cannot

`tests/test_ci_gives_the_checks_what_they_need.py:149` says "an `exclude:`
takes combinations away, so the entries read here would no longer be the
jobs". The refusal message at `:187` says the same of every sibling key:
"changes which jobs the entries are".

GitHub's workflow syntax reference, in its section on a job's matrix strategy,
says "All `include` combinations are processed after `exclude`". It also says
"If you don't specify any matrix variables, all configurations under
`include` will run". I read both sentences in the fetched page and did not
run a workflow on GitHub. In a matrix whose only other key is `exclude:`,
the exclusion runs first against an empty base matrix, and every `include:`
entry is added after it. So an `exclude:` beside `include:` removes no entry
in this job's shape.

- **What stays right.** The refusal itself. A reader that refuses a shape
  it does not need is the safe direction, and round 1 asked for exactly
  that.
- **What is wrong.** The reason in the docstring, and the message an
  editor sees when they add an `exclude:`. The message tells them their key
  changes the jobs, which sends them looking for an effect that is not
  there.
- **What the fix is.** Keep the refusal, say it is refused because the
  reader reads no other key, and drop the claim about `exclude:`.

This sits in `matrix_include_entries`, a unit round 1's fixes created.

### ⬜ 2 · The docstring says two other readings of `test.yml` remain, and there are more

`tests/test_ci_gives_the_checks_what_they_need.py:127` says "Two other
readings of the file remain, each asking something else", naming
`tests/test_release_hygiene.py` and `tests/test_arm_check.py`. The file is
`.github/workflows/test.yml`, and other test modules read it as well:

- `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:446`
  reads the `ledger` job's warning line.
- `tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py:68`
  reads the `pytest` job's pytest line through `jobs`.
- `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:980` reads the
  `pytest` job's pip line through `jobs`.
- `tests/test_ci_gives_the_checks_what_they_need.py:325` reads every job's
  checkout depth.
- `tests/test_the_gate_names_every_step_ci_runs.py` and
  `tests/test_deferral_check.py` name the file too.

Each of those reads something other than the entries, so the sentence's
intent holds. What the two named modules share is narrower: each reads
Python versions out of the file without the reader. The sentence should say
that.

### ⬜ 3 · Correction: the ledger's S4 carries the same sentence

`seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:6` says "Two
other readings of `test.yml` stay, each asking something else". It is the
same overreach as ⬜ 2, in the run's paperwork. The headline round 1 asked
for, "the `pytest` job's entries are read in one place", is right. When ⬜ 2
is fixed the docstring's hash moves, so this row's anchor on
`matrix_include_entries` is re-stamped in the same pass.

### ⬜ 4 · No case pins the stop at `matrix:`'s own indentation

The loop ends the matrix at `if indent(line) <= floor`
(`tests/test_ci_gives_the_checks_what_they_need.py:181`). Mutation M1
changed `<=` to `<` and ran the three modules that call the reader. All 26
cases passed, so the mutant survived.

Round 1's fix took `exclude:` out of the fixture and put `fail-fast: false`
at `:214`, before `matrix:`, which is where the tree's `test.yml` has it. The
loop starts below `matrix:`, so it never reads that line. The only line that
ends the matrix, in the fixture and in the tree, is `runs-on:` at indent 4,
which is below the floor either way.

- **What the mutant would do.** A `strategy:` key written after the matrix,
  such as `max-parallel: 2`, would be read as an `include:` item and
  refused. That is a refusal of a valid shape and never a silent misreading.
  This is why the finding is ⬜.
- **What pins it.** Probe Q4 adds `max-parallel: 2` after the entries. It
  reads the three entries at the target SHA and is red under M1. The
  paste-ready case below is Q4 written as a case.

So the answer to the question about the fixture: the swap keeps every case
able to fail that round 1's fix needed, and the `fail-fast: false` line
itself tests nothing.

## Round 1's findings, answered on this round's grounds

- **Finding 1 (fix or justify), fixed at e182401f: closed.** Probes Q2 and
  Q3 add a base axis before `include:` and an `exclude:` after the entries
  to the tree's own `test.yml`. Both are refused naming the line. Q6 refuses
  a sibling after entries written at `include:`'s own indentation, and Q7
  refuses a sibling with a flow value. Q5 and Q8 show that trailing comments
  and a comment line between `matrix:` and `include:` do not break the read.
  Mutations M2 to M5 each turn at least one new case red, and between them
  every one of the five new cases. Q1 reads the tree's eight entries. The
  reader compares indentation only against `matrix:` and `include:`, so the
  indentation width does not matter (read, not probed at another width).
- **Note 2, answered as a note: still holds.** The two refused shapes are
  unchanged by the fix, and the tree has neither (Q1 reads every entry).
- **Note 3, fixed at 4f58a081: closed.** The reader is
  `matrix_include_entries`, its docstring says why it has no `pytest_`
  prefix, and every caller imports the new name. The old name survives only
  in round files and `phases/phase-1.md`, inside fences, quoted call
  expressions or marked lines. `tests/test_a_record_states_what_the_tree_has.py`
  is green over them.
- **Note 4, fixed at 0d75dd00: closed.** `CONTRIBUTING.md:192`–`195` now say
  the file prices each case as Windows ran it, and that a refresh is
  followed by reading the macOS shard times again and resetting the
  `timeout`. Both halves of round 1's note are there.
- **Note 5, answered at ef383561: closed.** I recomputed the three figures
  from `gh run view --json jobs`. Run 37465328899's Windows group 3 took
  10 m 03 s. Run 37576998008's group 4 took 12 m 42 s. Run 37577753583's
  group 4 took 12 m 15 s. Each is under the budget of 20. One word is loose:
  "on the runs S4 recorded" is plural, and S4 recorded one run. The run is
  named right after it, so nothing is misread.
- **Note 6, answered at ef383561: closed.** The `Re-read · S9` row quotes
  0.20.0's S9 claim word for word (`seal/releases/0.20.0.md:208`), and the
  claim holds. `CONTRIBUTING.md:170`–`171` count both sharded legs, macOS at
  three and Windows at four, and the paragraph at `:189` says what a stale
  `.test_durations` asks for both legs.
- **Note 7, answered at ef383561 and 4f58a081: the headline is closed.** The
  sentence added next to it is ⬜ 2 and ⬜ 3.
- **Note 8, answered at ef383561: closed.** GitHub's limits page gives 5
  concurrent macOS jobs on the Free, Pro and Team plans and 50 on
  Enterprise (read, fetched this round). Two runs at three macOS jobs each
  make six, so the paragraph's "can wait" is right. The headline's "a run
  alone" holds on this round's own CI run: the slowest macOS shard took
  7 m 29 s against ubuntu's 9 m 01 s and the slowest Windows shard's
  9 m 33 s.

## Regression tests to plant

- **⬜ 4:** in `tests/test_ci_gives_the_checks_what_they_need.py`, beside
  the sibling case, a case where a `strategy:` key after the matrix ends it.
  See the fenced fix. It is red under M1 (probe Q4, executed).

## Facts for the evidence ledger

- The pull request's run 37706881322 at 4cfbfc00 gives a third macOS
  measurement: groups 1, 2 and 3 took 5 m 23 s, 4 m 51 s and 7 m 29 s,
  ubuntu 9 m 01 s, and the Windows shards 7 m 26 s, 8 m 05 s, 9 m 33 s and
  8 m 12 s. The slowest macOS shard so far is 7 m 56 s (round 1's run
  37703030097), and 1.5 times that is 11 m 54 s, still under 15.

## The broad gate

The full suite has not run at 4cfbfc00. That is the sealer's run, after the
rounds settle. This round leaves nothing that needs a fix. The four notes
are the orchestrator's to answer or fix, and once they are answered the
sealer's spawn is what comes due.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The docstring and the refusal message say a key beside `include:` changes which jobs the entries are, and GitHub processes `include:` after `exclude:`, so an `exclude:` beside it removes no entry | `tests/test_ci_gives_the_checks_what_they_need.py:149` | open | GitHub's workflow syntax reference, "All `include` combinations are processed after `exclude`" (read); the refusal itself is safe; inside `matrix_include_entries`, a unit round 1's fixes created |
| ⬜ 2 | The docstring says two other readings of `test.yml` remain, and at least five other test modules read the file | `tests/test_ci_gives_the_checks_what_they_need.py:127` | open | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:446`, `tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py:68`, `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:980`, `tests/test_ci_gives_the_checks_what_they_need.py:325` (read); inside `matrix_include_entries` |
| ⬜ 3 | Ledger S4 says two other readings of `test.yml` stay, the same overreach as ⬜ 2 | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:6` | open | the same readers as ⬜ 2; correction to the run's paperwork |
| ⬜ 4 | No case pins the stop at `matrix:`'s own indentation: changing `<= floor` to `< floor` leaves every case green, and the fixture's `fail-fast: false` sits before `matrix:` where the loop never reads it | `tests/test_ci_gives_the_checks_what_they_need.py:181` | open | mutation M1 survived, 26 passed (executed); probe Q4 reads a `max-parallel:` after the matrix and is red under M1 (executed); the mutant refuses a valid shape rather than misreading one |
| 🟢 | round 1's finding 1 is closed — a key beside `include:`, before or after it, is refused naming its line, and so is an `include:` outside `matrix:` | `tests/test_ci_gives_the_checks_what_they_need.py:183` | confirmed | probes Q1 to Q3 and Q5 to Q8, executed; M2 to M5 each red, executed; the tree's `test.yml` reads as eight entries |
| 🟢 | round 1's note 2 stands as answered — both shapes are still refused, and the tree has neither | `tests/test_ci_gives_the_checks_what_they_need.py:104` | confirmed | unchanged by the fix; Q1 reads every entry of the tree, executed |
| 🟢 | round 1's note 3 is closed — the reader is `matrix_include_entries`, and its docstring says why it has no `pytest_` prefix | `tests/test_ci_gives_the_checks_what_they_need.py:120` | confirmed | every importer uses the new name (read); the four modules that call it, 124 passed, executed |
| 🟢 | round 1's note 4 is closed — the refresh paragraph says the file prices a case as Windows ran it and asks for the macOS shard times to be read again | `CONTRIBUTING.md:192` | confirmed | read against round 1's note; `tests/test_docs_line_wrap.py` green, executed |
| 🟢 | round 1's note 5 is closed — `Corrected · S4` puts 12 minutes in the past and names 12 m 42 s and 12 m 15 s | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:1` | confirmed | the three figures recomputed from `gh run view` for runs 37465328899, 37576998008 and 37577753583, executed; "the runs S4 recorded" is plural for one run, which misleads nobody |
| 🟢 | round 1's note 6 is closed — `Re-read · S9` quotes S9 word for word and the claim holds | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:13` | confirmed | `seal/releases/0.20.0.md:208` and `CONTRIBUTING.md:170` read |
| 🟢 | round 1's note 7 headline is closed — S4 now says the job's entries are read in one place | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:6` | confirmed | read; the sentence added beside it is this round's ⬜ 2 and ⬜ 3 |
| 🟢 | round 1's note 8 is closed — the changelog says a run alone, and names the five-job macOS cap on Free, Pro and Team | `seal/specs/1791384162-the-macos-test-leg-runs-in-shards/changelog.md:3` | confirmed | GitHub's limits page, 5 on Free, Pro and Team and 50 on Enterprise (read); run 37706881322's job times, executed |
| 🟢 | The pull request's CI at 4cfbfc00 is complete and green | run 37706881322 | confirmed | `gh pr checks 876` exit 0, 13 checks pass, none running; both runs' `headSha` is 4cfbfc00, executed |

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

Q1 to Q9 were one probe file (NAME NOT IN TREE: test_tmp_round2_864.py),
run once through the clone's `bin/test` with `-p no:xdist -s`: 10 passed,
exit 0, each probe asserting what it reports. M1 to M5 ran the three
modules that call the reader. The file, the clone and its `.venv` were
removed before hand-over.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `tests/test_release_hygiene.py:1034` reads the floor from every `python:` in the raw file, comments included | `spec.md` Out, *The other reader of `python:`*; #835's registry; already deferred in round 1 | #835's implementer |
| `heading_level` cuts a markdown section at a `#` line inside a fence | #867's frame; already deferred in round 1 | #867's implementer |
| `.test_durations` is stale | #874; already deferred in round 1 | the owner, who starts the refresh run |

## Paste-ready fixes

### ⬜ 1

In `tests/test_ci_gives_the_checks_what_they_need.py`, the last paragraph of
the docstring of `matrix_include_entries`:

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

And the refusal, which the sibling case still matches by "beside
`include:`" and by the sibling's line:

```python
            raise ValueError(
                "a `matrix:` key beside `include:`, which this reader does "
                f"not read: {line.strip()!r}"
            )
```

### ⬜ 2

In the same docstring's first paragraph:

```python
    entry written another way was not an entry, and nothing said so. Two
    other cases read Python versions out of the file without it, each asking
    something else: `tests/test_release_hygiene.py` takes the floor from
    every `python:` in it, and `tests/test_arm_check.py` reads the Pythons
    of the jobs that run its own module.
```

### ⬜ 3

In `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md`, S4's
claim, then re-stamp the row's `matrix_include_entries` anchor after ⬜ 1 and
⬜ 2:

```
Two other cases read Python versions out of `test.yml` without it, each asking something else:
```

in place of

```
Two other readings of `test.yml` stay, each asking something else:
```

### ⬜ 4

In `tests/test_ci_gives_the_checks_what_they_need.py`, after
`test_an_include_that_is_not_the_matrixs_own_is_refused`:

```python
def test_a_strategy_key_after_the_matrix_ends_it():
    """A `strategy:` key written after the matrix sits at `matrix:`'s own
    indentation. It ends the matrix and is not a key beside `include:`."""
    old = "    runs-on: ${{ matrix.os }}\n"
    text = MATRIX.replace(old, "      max-parallel: 2\n" + old, 1)
    assert text != MATRIX
    assert matrix_include_entries(text) == matrix_include_entries(MATRIX)
```

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened this round, read in the worktree at 4cfbfc00 unless noted:

- `seal/specs/1791384162-the-macos-test-leg-runs-in-shards/rounds/round-1.md`, `round-1-fixes.md`, `round-1-report.md`
- the fix diff `ce72430e..ef383561`: `CONTRIBUTING.md`, the ledger fragment, `changelog.md`, `overview.md`, `phases/phase-1.md`, `phases/phase-2.md`, `questions.md`, and the four test modules
- `tests/test_ci_gives_the_checks_what_they_need.py` (lines 51–200, the fixture at 202–230, and the grep of its cases)
- `tests/conftest.py` (lines 51–120)
- `.github/workflows/test.yml` (lines 25–160)
- `CONTRIBUTING.md` (lines 170–215)
- `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` (lines 440–470), `tests/test_arm_check.py` (lines 280–330), `tests/test_release_hygiene.py` (lines 1025–1045)
- `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md`
- `seal/releases/0.20.0.md` rows S4 and S9
- this work item's `plan.md` (lines 44–56, 110–124, 218–228) and `changelog.md`
- `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/phases/phase-3.md` and `phase-5.md` (the 10 m 03 s lines)
- `bin/test` (header)
- GitHub's workflow syntax reference and its limits page, fetched and read
