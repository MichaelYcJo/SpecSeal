# 1791384162-the-macos-test-leg-runs-in-shards — round 1 report

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | c5d1f1973a311d6fb67a1f567cd364eab331db48 |
| Base | `origin/release/v0.21.0` at 5623d728, the merge-base |
| Reviewer | warden on Opus 5.5 |
| Where | a `git clone --no-local` at the target SHA, under the session scratchpad's `1791384162-the-macos-test-leg-runs-in-shards/round-1/clone`; removed before hand-over |

## How the findings relate

The change holds. The shards are right, the arithmetic is right and the
ledger closes. What this round found sits around the new reader and around
the one durations file:

1. The reader refuses every bad item under `include:`, but a key beside
   `include:` under `matrix:` passes silently. A key there changes which jobs
   the entries are, so the shard case can stay green while a leg runs one
   group (🟡 1).
2. Three smaller points about the reader: two shapes YAML accepts are
   refused, and its `pytest_` prefix fails pytest outright if it ever moves
   into a conftest (⬜ 2, ⬜ 3).
3. The durable text says the file is measured on Windows. It does not say
   what that costs macOS, or that a refresh moves the macOS groups away from
   the run the budget was set on (⬜ 4).
4. Four corrections to the run's paperwork (⬜ 5 to ⬜ 8).

## Findings from reading, confirmed by probes

### 🟡 1 · A matrix key beside `include:` goes unread, and it can collapse the shards into one job

`tests/test_ci_gives_the_checks_what_they_need.py:144` finds the one
`include:` and reads only the lines under it. Nothing checks what else sits
under `matrix:`. Probe P2 added `python: ["3.12", "3.13"]` beside
`include:` in the module's own fixture. `pytest_matrix` returned its three (NAME NOT IN TREE: renamed `matrix_include_entries` by round 1's fix)
entries and raised nothing.

This matters because GitHub only runs each `include:` entry as a job of its
own when the matrix has no other axis. With a base axis, an entry that
overwrites none of the axis values is merged into an existing combination
instead. A later entry may then overwrite a value an earlier one added. This
comes from GitHub's documented `include` rules. I read it and did not run it
on GitHub.

Here is the case. Someone adds `python: ["3.12"]` as an axis to try a second
interpreter later. All eight entries match `python: "3.12"`, so all eight
merge into one combination. Each one overwrites the `os`, `split` and
`timeout` the one before it added, and CI runs a single job: Windows group 4.
The shard case still reads eight entries, each group once, and passes. The
shard module's docstring claims the opposite: "What decides whether a leg's
union is the suite is the matrix itself … So the matrix is read here".

The spec asks only that items under `include:` be refused (Scope 3, S4), so
this is a quality finding and not a spec breach. It answers the round's
first question, though: the reader skips a shape instead of refusing it.

- **What the fix keeps:** every shape `test.yml` holds today. Probe P1 read
  the real matrix as its eight entries.
- **What it costs:** the fixture's `exclude:` sibling becomes a refused
  shape. The list still ends at the job's next key, so that test keeps its
  meaning.

### ⬜ 2 · Two shapes YAML reads are refused

Probe P3 confirmed both. `- { os: example-os, split: ${{ inputs.split }} }`
is refused as "a nested collection", because `{` inside a value counts as
nesting (`tests/test_ci_gives_the_checks_what_they_need.py:104`).
`note: it's` is refused as "an unclosed quote", because an apostrophe in a
plain scalar opens a quote. Both refusals block more and nothing in
`test.yml` has either shape. The first one is a usual way to write a matrix
value, though, and the refusal message points at nesting rather than at the
expression. I record it so the next editor does not take it for a YAML
error.

### ⬜ 3 · The name `pytest_matrix` breaks pytest if the helper ever moves into a conftest (NAME NOT IN TREE: renamed `matrix_include_entries` by round 1's fix)

pytest reads every `pytest_`-prefixed function in a conftest as a hook. In
probe P6 a conftest that defined `pytest_matrix` stopped the run with (NAME NOT IN TREE: renamed `matrix_include_entries` by round 1's fix)
`INTERNALERROR … PluginValidationError: unknown hook 'pytest_matrix'`, exit
3. Today the helper lives in a test module, where pytest does not register
hooks, so nothing breaks. But `plan.md` Alternative G names `conftest.py` as
the natural home, and the consolidation that rejection defers to #835 or #867
would move it there. A rename is cheapest now: the helper is anchored only by
this branch's unreleased fragment, and after 0.21.0 ships a rename moves
released anchors.

### ⬜ 4 · Nothing durable says what a Windows-measured file costs macOS, or what a refresh asks of macOS

The round's third question was whether a macOS shard's balance depends on
Windows timings, and whether anything states that limit. It does depend on
them. The limit is stated only in part.

- **What is stated.** `test.yml:71` says "Only each case's price differs by
  system, and that is read off each leg's own jobs, never off the file", and
  `CONTRIBUTING.md:190` says the file is the Windows leg's and divides macOS
  too.
- **What is not stated.** A case that Windows skips enters the file at
  almost nothing. The shell oracle is 1.00 s in the file and 113 s of calls
  on macOS (`plan.md:85`–`92`), so it lands whole in whichever group the
  contiguous cut gives it. Neither file says this.
- **What the refresh misses.** The recipe ends "restore the shards"
  (`CONTRIBUTING.md:209`). It does not ask anyone to read the macOS shard
  times after a refresh. The 15-minute budget was set from groups cut by the
  old file, and a refreshed file moves where the cuts fall.

The budget's margin covers this today (⬜ rather than 🟡). On the pull
request's own run, group 3 took 7 m 56 s against 4 m 10 s for group 2, so
the groups already differ by a factor of 1.9.

### ⬜ 5 · Correction: `Corrected · S4` states a figure that this work item's own plan contradicts

`seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:1` repeats S4's
"the slowest shard is under 12 minutes" in the present tense. `plan.md:50`
and `plan.md:51` record Windows shards at 12 m 42 s (run 37576998008) and
12 m 15 s (run 37577753583). The row's evidence names run 37465328899, so the
figure is true of that run only. The row should say so in its claim, not
only in its evidence cell.

### ⬜ 6 · Correction: 0.20.0's S9 covers the paragraphs this branch rewrote, and no row records a re-read

0.20.0's S9 claims that `CONTRIBUTING.md` "counts the shards and says what
… a stale `.test_durations` ask of a contributor". It anchors
`CONTRIBUTING.md#"## Running the checks"`. Both paragraphs this branch
rewrote are what that claim is about. The anchor did not drift because of
the fence cut that `phases/phase-2.md` names, so `--reverify --into` wrote no
row for it.

I read the rewritten paragraphs against S9's claim, and the claim still
holds. Nothing in the fragment records that, so a reader of the ledger
cannot tell S9 was looked at. A hand-written `Re-read · S9` row, or one
sentence in S5's notes, closes that gap.

### ⬜ 7 · Correction: ledger S4 says the matrix is read "one way", and two other readers remain

`seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:6` opens with
"the suite reads the `pytest` job's matrix one way". Two other readers
remain:

- `tests/test_release_hygiene.py:1034` reads every `python: "…"` out of the
  raw file, comments included.
- `tests/test_arm_check.py:309` reads pinned Pythons out of the job's lines.

The spec leaves the first one out on purpose, and the second reads through
`jobs`. The rest of the claim is accurate. Only the "one way" headline goes
past it. Suggested wording: "the suite reads the `pytest` job's include
entries one way".

### ⬜ 8 · Correction: the changelog headline holds for one run at a time

`changelog.md:3` says "a pull request no longer waits on it". That was
measured on a run alone. `plan.md:115`–`121` records a cap of five
concurrent macOS jobs on this plan and runs that overlapped two and three at
a time. A run now starts three macOS jobs, so two runs at once queue one of
them, as `plan.md:224` itself says ("two runs at once share the cap").
Suggested wording: "a run alone no longer waits on it".

## What this round checked and found sound

- **Reader shape (question 1).** `pytest_matrix` reads every entry (NAME NOT IN TREE: renamed `matrix_include_entries` by round 1's fix)
  `test.yml` holds (P1). The four private slices are gone:
  `grep -rn 'index("  pytest:")' tests/` and a search for
  `"  ledger:"` slices found none. The remaining readers of `test.yml` read
  other things, as listed in ⬜ 7.
- **Arithmetic (question 2).** I recomputed every job time in
  `phases/phase-2.md` from run 37700567455's `startedAt` and `completedAt`
  values. I also re-added every sum: 12,739 + 88 = 12,827 for macOS,
  12,747 + 80 for ubuntu, and 12,608 + 219 for Windows. Each `plan.md`
  row checks out: 629 s, 921 s, 483 s and 396 s, which agrees with the
  1.123 ratio of the three shards' pytest times. The rule gives 6 m 56 s ×
  1.5 = 10 m 24 s, so 15. On the pull request's run at the target SHA the
  shards took 5 m 03 s, 4 m 10 s and 7 m 56 s. Applied to both runs, the
  rule still gives 15 (7 m 56 s × 1.5 = 11 m 54 s). The unsharded leg's
  largest spread across the six runs `plan.md` cites is 1.35. Applied to
  7 m 56 s that is 10 m 43 s, so 15 leaves a margin.
- **Ledger (question 4).** `evidence-check --strict .` exits 0 with 0
  drifted and 0 broken. I read the five `Re-read ·` rows' cited claims (0.8.2
  R3, 0.16.0 P1-1, 0.18.0 R3, 0.20.0 S1 and S2) against the code and each
  holds. `Corrected · S8`'s three budgets match `test.yml`. The `plan.md`
  152–153 rewording changes only the coordinate form. The diff of af700273
  shows two lines, and the framer's sentence is otherwise the same.
- **The S5 workaround (question 5).** It is sound in the meantime. A quoted
  line that is not a heading owns its whole paragraph
  (`skills/evidence-check/scripts/evidence_check.py:550`–`555`), so each S5
  anchor hashes a full rewritten paragraph and does not depend on the
  section cut. `heading_level` has no fence check, and `CONTRIBUTING.md:166`
  is a `# or:` line inside a fence, so the reading in `phases/phase-2.md` is
  right. If the anchored line itself is reworded, the row reads BROKEN
  rather than DRIFTED, which is the louder of the two failures.
- **Mutations.** The timeout case is red with one macOS `timeout` removed
  (P4). The shard case is red with a macOS group named twice, with a macOS
  count that disagrees, and with a ubuntu entry carrying a split (P5). These
  re-run three of the smith's claimed reds. I did not re-run the other
  seventeen.
- **Required checks.** Neither ruleset requires a `pytest` check by name.
  The required checks are `lint`, `release` and `ledger`, so the new job
  names do not orphan a requirement.

## Regression tests to plant

- **🟡 1:** in `tests/test_ci_gives_the_checks_what_they_need.py`, two more
  parametrized cases are refused: a base axis beside `include:`, and an
  `exclude:` beside it. See the fenced fix.

## Facts for the evidence ledger

- The pull request's run 37703030097 at c5d1f197 gives a second macOS
  measurement: groups 1, 2 and 3 took 5 m 03 s, 4 m 10 s and 7 m 56 s, and
  ubuntu took 8 m 07 s. S2 and S3 rest on one run, and this is the second.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A key beside `include:` under `matrix:` is read silently, and a base axis there makes GitHub merge include entries into fewer jobs while the shard case passes | `tests/test_ci_gives_the_checks_what_they_need.py:144` | open | probe P2: a `python:` axis beside `include:` raised nothing; GitHub's documented include rules (read) |
| ⬜ 2 | `${{ … }}` in a value and an apostrophe in a plain scalar are refused, the first as "a nested collection" | `tests/test_ci_gives_the_checks_what_they_need.py:104` | open | probe P3; blocks more, and no entry in the tree has either shape |
| ⬜ 3 | A `pytest_` prefix makes the helper a hook if it ever lives in a conftest, and pytest then stops with INTERNALERROR | `tests/test_ci_gives_the_checks_what_they_need.py:120` | open | probe P6: exit 3, `unknown hook 'pytest_matrix'`; `plan.md` Alternative G names conftest as the natural home |
| ⬜ 4 | The durable text does not say that a case Windows skips is priced near zero for macOS, or that a refresh means re-reading the macOS shard times | `CONTRIBUTING.md:209` | open | `test.yml:71` and `CONTRIBUTING.md:190` state only half of it; the pull request's run spreads the groups 1.9× |
| ⬜ 5 | `Corrected · S4` restates "the slowest shard is under 12 minutes" in the present tense | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:1` | open | `plan.md:50`–`51` record 12 m 42 s and 12 m 15 s; correction to the run's paperwork |
| ⬜ 6 | 0.20.0's S9 covers the rewritten paragraphs, its anchor hid the change, and no row records a re-read | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:7` | open | the claim still holds (read); correction to the run's paperwork |
| ⬜ 7 | Ledger S4's "one way" headline goes past what the tree does | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:6` | open | `tests/test_release_hygiene.py:1034`, `tests/test_arm_check.py:309`; correction to the run's paperwork |
| ⬜ 8 | The changelog headline holds for a run alone, not under the five-job macOS cap | `seal/specs/1791384162-the-macos-test-leg-runs-in-shards/changelog.md:3` | open | `plan.md:115`–`121` and `plan.md:224`; correction to the run's paperwork |
| 🟢 | The shard and budget arithmetic, and the budget of 15 measured against two runs | `.github/workflows/test.yml:53` | confirmed | run 37700567455's and run 37703030097's job times recomputed; sums re-added |
| 🟢 | The five `Re-read ·` rows and `Corrected · S8` hold, and the ledger closes | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md` | confirmed | `evidence-check --strict .` exit 0, executed; each cited claim read |
| 🟢 | S5's paragraph anchors do not depend on the fence cut | `skills/evidence-check/scripts/evidence_check.py:550` | confirmed | a quoted line that is not a heading owns its paragraph |
| 🟢 | The pull request's CI at c5d1f197 is green on every job, each macOS shard named with its `timeout` of 15 | run 37703030097 | confirmed | `gh pr checks 876`: 16 checks pass, executed; whether GitHub enforces the 15 is seen only when a shard runs past it |

## Executed probes

| What was run | Result |
|---|---|
| P1 `pytest_matrix(read("test.yml"))` | 8 entries: ubuntu 15, three macOS shards at 15, four Windows shards at 20 |
| P2 the module's fixture with `python: ["3.12", "3.13"]` beside `include:` | no refusal, 3 entries returned |
| P3 `${{ inputs.split }}` as a value; `note: it's` | both refused: "a nested collection", "an unclosed quote" |
| P4 the timeout case with group 2's `timeout: 15` removed | red: "a leg with no timeout" |
| P5 the shard case with macOS group 3 as group 2, as `--splits 4`, and with a split on ubuntu | red in all three |
| P6 a conftest that defines `pytest_matrix`, run by pytest 9.1.1 | exit 3, INTERNALERROR, PluginValidationError: unknown hook 'pytest_matrix' (NAME NOT IN TREE: renamed `matrix_include_entries` by round 1's fix) |
| `evidence-check --strict .` in the clone | exit 0; 6,844 ok, 0 drifted, 0 broken |
| `gh api` for the repository's two rulesets | required checks are `lint`, `release` and `ledger`; no `pytest` job by name |
| `gh run view 37700567455 --json jobs` | head 3a946dd0, success; every time in `phases/phase-2.md` agrees |
| `gh run view 37703030097 --json jobs` and `gh pr checks 876` at c5d1f197 | completed, success, 16 checks pass; macOS 5 m 03 s, 4 m 10 s and 7 m 56 s; ubuntu 8 m 07 s; Windows 10 m 30 s, 8 m 52 s, 8 m 22 s and 10 m 15 s |
| the full suite at the target SHA (broad gate) | not yet — not run by this round; the sealer's, after the rounds settle |

P1 to P6 were one probe file (NAME NOT IN TREE: test_tmp_probe_864.py),
run once through the clone's `bin/test` with `-p no:xdist`: 9 passed, exit 0,
each probe asserting what it reports. The file, the clone and its `.venv`
were removed before hand-over.

```
P2 no refusal, entries: 3
P3 - { os: example-os, split: ${{ inputs.split }} } -> a nested collection in a matrix entry: '- { os: example-os, split: ${{ inputs.split }} }'
P3 - { os: example-os, note: it's } -> an unclosed quote in a matrix entry: "- { os: example-os, note: it's }"
P6 exit 3 ["INTERNALERROR> pluggy._manager.PluginValidationError: unknown hook 'pytest_matrix' in plugin <module 'conftest' ...>", '', 'no tests ran in 0.00s']
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `tests/test_release_hygiene.py:1034` reads the floor from every `python:` in the raw file, comments included, which is a second reading of the matrix | `spec.md` Out, *The other reader of `python:`*; #835's registry | #835's implementer |
| `heading_level` cuts a markdown section at a `#` line inside a fence, so `CONTRIBUTING.md#"## Running the checks"` does not reach lines 166 onward | #867's frame, `spec.md` line 50 | #867's implementer |
| `.test_durations` is stale: 504 collected cases are missing and 727 entries are dead | #874 | the owner, who starts the refresh run |

## Paste-ready fixes

### 🟡 1

In `tests/test_ci_gives_the_checks_what_they_need.py`, `pytest_matrix`, (NAME NOT IN TREE: renamed `matrix_include_entries` by round 1's fix)
after `head = …`:

```python
    head = len(lines[heads[0]]) - len(lines[heads[0]].lstrip(" "))
    parent = next(
        (
            i
            for i in range(heads[0] - 1, -1, -1)
            if lines[i].strip()
            and len(lines[i]) - len(lines[i].lstrip(" ")) < head
        ),
        None,
    )
    if parent is None or lines[parent].strip() != "matrix:":
        raise ValueError("the `pytest` job's `include:` is not a key of its `matrix:`")
    floor = len(lines[parent]) - len(lines[parent].lstrip(" "))
    for line in lines[parent + 1 :]:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent <= floor:
            break
        if indent == head and not line.lstrip().startswith("-") and line.strip() != "include:":
            # GitHub runs each include entry as its own job only when the
            # matrix has no other key: beside a base axis, an entry is merged
            # into a combination and a later one overwrites what it added.
            raise ValueError(
                "a `matrix:` key beside `include:` changes which jobs the "
                f"entries are, and this reader does not read it: {line.strip()!r}"
            )
```

The fixture drops its `exclude:` sibling, so the list ends at `runs-on:`, and
two refusals join the parametrized case. Both are inserted before the
matrix's `include:`, which `LAST_ENTRY` cannot reach, so they take their own
case:

```python
MATRIX = """\
name: tests

jobs:
  lint:
    runs-on: ubuntu-latest
  pytest:
    strategy:
      matrix:
        include:
          - { os: ubuntu-latest, python: "3.12", timeout: 15 }
          # - { os: macos-latest, python: "3.12", timeout: 35 }
          - { os: macos-latest, python: "3.12", split: "--splits 2 --group 1", timeout: 5 }  # one
          - { os: example-os, python: '3.12', note: "a # b" }
    runs-on: ${{ matrix.os }}
    steps:
      - run: pytest tests/ ${{ matrix.split }}
  other:
    strategy:
      matrix:
        include:
          - { os: not-this-job }
"""


@pytest.mark.parametrize(
    "sibling",
    ['python: ["3.12", "3.13"]', "exclude:\n          - { os: example-os }"],
    ids=["base-axis", "exclude"],
)
def test_a_matrix_key_beside_include_is_refused_by_its_line(sibling):
    text = MATRIX.replace(
        "      matrix:\n        include:",
        f"      matrix:\n        {sibling}\n        include:",
        1,
    )
    assert text != MATRIX
    with pytest.raises(ValueError, match="beside `include:`") as caught:
        pytest_matrix(text)
    assert sibling.splitlines()[0] in str(caught.value), caught.value
```

The docstring's refusal list gains "a key beside `include:` under
`matrix:`", and the comment above `MATRIX` loses "a sibling key that ends
`include:`".

Needs a fix: yes — 🟡 1, a matrix key beside `include:` is read silently and can collapse the shards while the shard case passes

Loses a record or crashes: no

## Proof block

Files opened this round, read in the worktree at c5d1f197 unless noted:

- `.github/workflows/test.yml` (the `pytest` job, lines 30–150)
- `.github/scripts/run_tests.py` (diff)
- `CONTRIBUTING.md` (diff; headings and fences, lines 104–209)
- `tests/test_ci_gives_the_checks_what_they_need.py` (lines 1–260)
- `tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py`, `tests/test_a_slow_case_names_itself.py`, `tests/test_the_release_check_watches_what_ships.py` (diff)
- `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` (diff; lines 975–995)
- `tests/conftest.py` (lines 40–138)
- `tests/test_arm_check.py` (lines 230–345), `tests/test_release_hygiene.py` (lines 1025–1045), `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` (lines 440–470)
- `skills/evidence-check/scripts/evidence_check.py` (lines 517–620)
- `seal/releases/0.20.0.md` rows S1, S2, S4, S8, S9; `seal/releases/0.8.2.md` R3; `seal/releases/0.16.0.md` P1-1; `seal/releases/0.18.0.md` R3
- `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md`
- this work item's `spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`, `handoff.md`, `phases/phase-1.md`, `phases/phase-2.md`
