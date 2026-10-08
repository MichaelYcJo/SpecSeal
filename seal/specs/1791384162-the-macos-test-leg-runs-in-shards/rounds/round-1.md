# 1791384162-the-macos-test-leg-runs-in-shards — review round 1

| Field | Value |
|---|---|
| Target SHA | c5d1f1973a311d6fb67a1f567cd364eab331db48 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 876 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `ce72430e9ab18ab882c12c6f75a0f258ef9ea3b3..ef383561ecbede09f3241f8218f7766ad9fc6489`, 4 commits |
| Contract changes | none |
| New units | matrix_include_entries (depth 1); test_a_matrix_key_beside_include_is_refused_by_its_line (depth 1); test_an_include_that_is_not_the_matrixs_own_is_refused (depth 1) |
| Fix of a fix | no |
| Needs a fix | yes — 🟡 1, a matrix key beside `include:` is read silently and can collapse the shards while the shard case passes |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the build at c5d1f197, against origin/release/v0.21.0. The spawn named five things to attack. First, pytest_matrix: does it read every shape test.yml holds and refuse, rather than skip, one it does not read, and does any test still slice test.yml by text? Second, the S1 and S2 arithmetic and the 1.5-times budget rule against the run's own job logs, and whether 15 minutes leaves margin. Third, whether the shared .test_durations bounds the macOS balance by the Windows timings, and whether anything states that limit. Fourth, the ledger fragment's corrected, re-read and S1 to S5 rows, and the plan.md 152 to 153 rewording. Fifth, whether S5's line-anchor workaround for the fence cut is sound until #867 lands. Facts arrived labelled. Executed by the orchestrator: bin/test over four matrix modules (67 passed), ruff, and run 37700567455's job times. Read from the smith: shard counts summing to 12,827, the mutations, and evidence-check --strict.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A key beside `include:` under `matrix:` is read silently, and a base axis there makes GitHub merge include entries into fewer jobs while the shard case passes | `tests/test_ci_gives_the_checks_what_they_need.py:144` | **fixed** `e182401f` | fixed at e182401f — a key beside `include:` under the `pytest` job's `matrix:`, before or after it, is refused naming its line, and so is an `include:` that is not a key of `matrix:`. The five new cases were red against the reader at c5d1f197, and four breaks of the new branch were each red through `bin/mutation-check`; probe P2: a `python:` axis beside `include:` raised nothing; GitHub's documented include rules (read) |
| ⬜ 2 | `${{ … }}` in a value and an apostrophe in a plain scalar are refused, the first as "a nested collection" | `tests/test_ci_gives_the_checks_what_they_need.py:104` | answered | a note, left as it stands: both shapes are refused rather than misread, so the reader blocks more than YAML does and never less; no entry in `test.yml` has either shape; probe P3; blocks more, and no entry in the tree has either shape |
| ⬜ 3 | A `pytest_` prefix makes the helper a hook if it ever lives in a conftest, and pytest then stops with INTERNALERROR | `tests/test_ci_gives_the_checks_what_they_need.py:120` | **fixed** `4f58a081` | fixed at 4f58a081 — the reader is `matrix_include_entries`, and its docstring says why it has no `pytest_` prefix; probe P6: exit 3, `unknown hook 'pytest_matrix'`; `plan.md` Alternative G names conftest as the natural home |
| ⬜ 4 | The durable text does not say that a case Windows skips is priced near zero for macOS, or that a refresh means re-reading the macOS shard times | `CONTRIBUTING.md:209` | **fixed** `0d75dd00` | fixed at 0d75dd00 — `CONTRIBUTING.md`'s refresh paragraph says the file prices a case as Windows ran it, and that the macOS shard times are read again after a refresh; `test.yml:71` and `CONTRIBUTING.md:190` state only half of it; the pull request's run spreads the groups 1.9× |
| ⬜ 5 | `Corrected · S4` restates "the slowest shard is under 12 minutes" in the present tense | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:1` | answered | corrected at ef383561: `Corrected · S4` puts the 12-minute figure in the past, on the runs S4 recorded, and names the later Windows shards at 12 m 42 s and 12 m 15 s; `plan.md:50`–`51` record 12 m 42 s and 12 m 15 s; correction to the run's paperwork |
| ⬜ 6 | 0.20.0's S9 covers the rewritten paragraphs, its anchor hid the change, and no row records a re-read | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:7` | answered | corrected at ef383561: a hand-written `Re-read · S9` row cites S9 with its heading anchor and the two paragraph anchors that carry the reading; the fence cut stays #867's; the claim still holds (read); correction to the run's paperwork |
| ⬜ 7 | Ledger S4's "one way" headline goes past what the tree does | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md:6` | answered | corrected at ef383561 and 4f58a081: this item's ledger S4 and the reader's docstring say the job's entries are read in one place, and name `tests/test_release_hygiene.py`'s and `tests/test_arm_check.py`'s readings as the two that remain; `tests/test_release_hygiene.py:1034`, `tests/test_arm_check.py:309`; correction to the run's paperwork |
| ⬜ 8 | The changelog headline holds for a run alone, not under the five-job macOS cap | `seal/specs/1791384162-the-macos-test-leg-runs-in-shards/changelog.md:3` | answered | corrected at ef383561: the changelog's headline says a run alone no longer waits, and a paragraph names GitHub's five-job macOS cap on the Free, Pro and Team plans; `plan.md:115`–`121` and `plan.md:224`; correction to the run's paperwork |
| 🟢 | The shard and budget arithmetic, and the budget of 15 measured against two runs | `.github/workflows/test.yml:53` | confirmed | run 37700567455's and run 37703030097's job times recomputed; sums re-added |
| 🟢 | The five `Re-read ·` rows and `Corrected · S8` hold, and the ledger closes | `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md` | confirmed | `evidence-check --strict .` exit 0, executed; each cited claim read |
| 🟢 | S5's paragraph anchors do not depend on the fence cut | `skills/evidence-check/scripts/evidence_check.py:550` | confirmed | a quoted line that is not a heading owns its paragraph |
| 🟢 | The pull request's CI at c5d1f197 is green on every job, each macOS shard named with its `timeout` of 15 | run 37703030097 | confirmed | `gh pr checks 876`: 16 checks pass, executed; whether GitHub enforces the 15 is seen only when a shard runs past it |

## Paste-ready fixes

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

```
P2 no refusal, entries: 3
P3 - { os: example-os, split: ${{ inputs.split }} } -> a nested collection in a matrix entry: '- { os: example-os, split: ${{ inputs.split }} }'
P3 - { os: example-os, note: it's } -> an unclosed quote in a matrix entry: "- { os: example-os, note: it's }"
P6 exit 3 ["INTERNALERROR> pluggy._manager.PluginValidationError: unknown hook 'pytest_matrix' in plugin <module 'conftest' ...>", '', 'no tests ran in 0.00s']
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `tests/test_release_hygiene.py:1034` reads the floor from every `python:` in the raw file, comments included, which is a second reading of the matrix | `spec.md` Out, *The other reader of `python:`*; #835's registry | #835's implementer |
| `heading_level` cuts a markdown section at a `#` line inside a fence, so `CONTRIBUTING.md#"## Running the checks"` does not reach lines 166 onward | #867's frame, `spec.md` line 50 | #867's implementer |
| `.test_durations` is stale: 504 collected cases are missing and 727 entries are dead | #874 | the owner, who starts the refresh run |
