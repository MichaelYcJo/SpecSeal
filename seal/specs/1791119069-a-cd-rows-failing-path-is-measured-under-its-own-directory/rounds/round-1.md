# 1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory — review round 1

| Field | Value |
|---|---|
| Target SHA | c553bd92c93c7c1332f7f54d5b6c18693d6954d1 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #787 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `7e61b5963ed410fabe27a2971efd72bb06d20f13..2bd38cec06d92409430f845f16944ce9ee3a9292`, 4 commits |
| Contract changes | none |
| New units | measured_summary (depth 1); test_a_run_of_several_that_counted_only_warnings_is_not_measured (depth 1); SUMMARIES (depth 1); test_a_run_that_collected_nothing_is_never_read_as_a_summary (depth 1) |
| Needs a fix | yes — 🟡 1 (a warnings-only nothing-collected line read as a summary gives `new` for a file the base fails) and 🟡 2 (two runners in two directories, unnamed in rule 3). |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of #761 (PR #787), at c553bd92 against `release/v0.18.2` (94d7b2e0): spec compliance first against the re-framed spec and plan (approach H), then quality, in `broad_gate.py#compare_at_base`. Judge the candidate rule and the solo-run verdicts under plain pytest and xdist, for root rows and rows that `cd` first, and whether a solo run's output can be misread; the direction left as `new?`; the smith's six recorded divergences; rule 3's three sentences and pins; and the `Corrected ·` rows over 0.18.1's B3 and S5.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A run of several that collected nothing but counted a warning ends `1 warning in <t>s`, which `PYTEST_SUMMARY_RE` reads as a summary, so a file the base fails reads `new` in the un-nominated direction; rule 3's pinned third sentence, the docstring and the spec say `new?` | `skills/verify/scripts/broad_gate.py:2126` | **fixed** `1133a101` | fixed at 1133a101 — `NOTHING_COLLECTED_RE` also reads a count of warnings alone, and the new `measured_summary` never reads a line it matches as pytest's summary, whatever the exit code. A warning count beside any other count stays a summary (`1 warning, 1 error in …`, `1 passed, 1 warning in …`). The shapes come from pytest 9.1.1's `_pytest/terminal.py`. `_build_normal_summary_stats_line` writes one `<count> <type>` per counted type in `KNOWN_TYPES` order, or `no tests ran` where none was counted. A run that collected nothing counts no test outcome, so it can end only with `no tests ran` or a warning count. A deselected count means tests were collected, so `3 deselected in …` stays a summary. `summary_stats` writes the line between `=` rules, bare under `-q`, and not at all under `-qq`. xdist's own lines (`bringing up nodes...`, `created:`, `N workers [0 items]`) are not summary lines. Cases added: the reviewer's case (plain and xdist), five `NOTHING_COLLECTED` rows, and eleven `SUMMARIES` rows. All were red at c553bd92: both e2e runs gave `new` for the file the base fails. Four mutations through `mutation-check` were each red: the warnings alternative, the singular, `measured_summary`'s guard, and the loop back on the bare regex. D1 and `Corrected · B3` follow in `fabf0329`; executed, probes p2: `new` for a file the base fails, plain and `-n 2`, at the target and at `94d7b2e0`; with the fix all four read `new?`, and the proposed case and rows are red against the target's gate |
| 🟡 2 | A row with two pytest runners in two directories is measured in the first runner's directory: `new` for a file the base fails, and `failing on base too` for a file the base never ran; rule 3 names neither and `spec.md:57` claims the right directory is always asked | `templates/config.md:333` | **fixed** `1133a101` | fixed at 1133a101 — This takes the orchestrator's fallback, because the fail-closed verdict needs new mechanism. Deciding "more than one runner prefix" means a new reading: count the summary lines in the branch's suite output, or run the whole row at the base. It also means a new argument to `compare_at_base`. That is a rule, which `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it* refuses a fix pass. Rule 3 gains the two-runner sentence and its advice, pinned (red at c553bd92 and red when deleted). `spec.md`'s directory claim is scoped to a row with one runner, §*Out* gains the row, and the docstring names the shape; executed, probes p1 and p1b at the target and at `94d7b2e0` |
| ⬜ 3 | `compare_at_base`'s second docstring paragraph says "every present file reads `new?`, never `new`", which names the removed split and is false for a candidate | `skills/verify/scripts/broad_gate.py:2049` | **fixed** `1133a101` | fixed at 1133a101 — `compare_at_base`'s second paragraph now names `measured_summary` and drops `present` and the false "never `new`". survivor-check then found rule 3's own "never `new`" sentence, which the solo run had made false; it was corrected in `2bd38ce1`; read |
| ⬜ 4 | The pytest 9.1.1 exemption's reason names the comments over `ERROR_RE` and `STOPPED_EARLY_RE`, and not the one over `NOTHING_COLLECTED_RE` | `tests/test_release_hygiene.py:159` | **fixed** `1133a101` | fixed at 1133a101 — The 9.1.1 row's reason names the comment over `NOTHING_COLLECTED_RE` beside `ERROR_RE` and `STOPPED_EARLY_RE`; read |
| ⬜ 5 | `overview.md`'s divergence table omits the added limit case and the `VERSIONS_OF_ANOTHER_PRODUCT` row, which are recorded only in phase files | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/overview.md:9` | answered | corrected at `834b1243`. `overview.md`'s divergence table holds all six: the call count, the `SKILL.md` glob, the added limit case, the `VERSIONS_OF_ANOTHER_PRODUCT` row, the `NAME NOT IN TREE` marks, and the return order; read; a paperwork correction |
| ⬜ 6 | `plan.md` counts two `ruff` runs per candidate on this repository's row; the row's three prefixes cost five | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/plan.md:89` | answered | `plan.md:89` stays as the frame wrote it. The correct count for this repository's row (`uvx ruff check . && uvx ruff format --check . && bin/test -q`) is three prefix runs per candidate: `ruff check` three times, `ruff format --check` twice, and `bin/test` once. Rule 3's "one more run of each prefix up to and including the runner per such file" states it correctly; read; a paperwork correction |
| ⬜ 7 | A runner that remaps pytest's exit code turns a truly new module from `new` (unrun) into `new?`; honest, but it contradicts the plan's "fewer unmeasured words" and rule 3 does not name it | `skills/verify/scripts/broad_gate.py:1935` | answered | A wrapper that remaps pytest's exit code makes the solo run print no line read with exit 4 or 5, so the file reads `new?`. That word is honest: it costs a reader one run by hand and never lets a failure through. `plan.md` §*Operational impact*'s "fewer unmeasured words" is about measured words, and the run behind the old `new` was not one: at 94d7b2e0 that `new` came from the root's tree without any run. Rule 3's "with exit 4 or 5" tells the row's author what the reading needs; executed, probe p3 |
| ⬜ 8 | The `skills/verify/SKILL.md` glob edit is unpinned (contract §14) | `skills/verify/SKILL.md:509` | **fixed** `1133a101` | fixed at 1133a101 — `test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written` pins "open the kept `suite-at-base-*.txt` files" in `skills/verify/SKILL.md`. The pin is green at c553bd92, where the text already stood, and was seen red with the glob put back to `suite-at-base-<k>.txt` through `mutation-check`; read; ledger D2 says so |
| 🟢 | Scope 1–6: the candidate rule, the solo runs, the others' group unchanged, the order, the kept names, `NO_RUNNER`'s parenthesis | `skills/verify/scripts/broad_gate.py:2034` | confirmed | executed: 25 selected cases passed with none skipped; probes p1–p3 kept the files the spec names |
| 🟢 | Divergences: one `run` call, the `SKILL.md` glob, the added limit case, the return order, the `NAME NOT IN TREE` marks, the 3.8.0 exemption | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/overview.md:9` | confirmed | the limit case and the return order executed by mutation; the rest read |
| 🟢 | `Corrected · B3` and `Corrected · S5` state the code at the target and cite the rows they supersede | `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md:16` | confirmed | read against the code |

## Paste-ready fixes

```python
# The line that says pytest collected nothing: `no tests ran in 0.21s`, alone
# on a line, bare under `-q` or between `=` rules as the summary is (#761).
# Measured against pytest 9.1.1 and pytest-xdist 3.8.0 in that work item's
# `phases/phase-1.md`: given a path that does not exist, plain pytest prints
# it beside `ERROR: file or directory not found: <path>` and exits 4, and
# under xdist it is the only trace and the exit is 5. It carries no leading
# count, so `PYTEST_SUMMARY_RE` never reads it as a summary. Where the run
# counted warnings, pytest prints their count in its place, `1 warning in
# 0.00s` plain and `3 warnings in 0.49s` under xdist (#761 round 1, an ini
# key pytest does not know). That line DOES match `PYTEST_SUMMARY_RE`, so
# `compare_at_base` asks this reading first. A count of warnings beside any
# other count (`1 warning, 1 error in …`) is a summary and is not read here.
NOTHING_COLLECTED_RE = re.compile(
    r"^=*\s*(?:no tests ran|\d+ warnings?) in \d+(?:\.\d+)?s"
    r"(?: \(\d+:\d\d:\d\d\))?\s*=*$",
    re.M,
)
```
```python
                # A run that collected nothing is never read as a summary,
                # even where warnings give its last line a count. Only for a
                # file run alone does it settle anything: a group of several
                # that collects nothing does not say which of them the base
                # lacks.
                empty = collected_nothing(tried.text, tried.code)
                if empty and alone:
                    nothing = True
                    break
                if not empty and PYTEST_SUMMARY_RE.search(tried.text):
                    measured = tried.text
                    break
```
```python
    nominated: it runs with the others, that run collects nothing, which is
    never read as pytest's summary even where warnings give its last line a
    count, and each file of it reads `new?`, never a counterfeit.
```
```python
    # A run that collected nothing but counted warnings: pytest gives the
    # count in place of `no tests ran` (#761 round 1).
    ("1 warning in 0.00s\nERROR: file or directory not found: tests/x.py\n", 4, True),
    ("=== 3 warnings in 0.49s ===\n", 5, True),
    ("1 warning in 0.00s\n", 1, False),
    ("1 passed, 1 warning in 0.01s\n", 0, False),
    ("1 warning, 1 error in 0.01s\n", 2, False),
```
```python
@pytest.mark.parametrize("xdist", UNDER)
def test_a_run_of_several_that_counted_only_warnings_is_not_measured(
    tmp_path, xdist
):
    """#761 round 1. As the limit case, and the base's `sub/tests/test_one.py`
    fails while an ini key pytest does not know gives every run a warning.
    The run of the two files collects nothing, and its last line is
    `1 warning in <t>s` rather than `no tests ran`. That line is not a
    measurement: `tests/test_one.py`, which the base fails, reads `new?`,
    never `new`."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {suite_row(xdist)}",
        {
            "tests/test_one.py": PASSING_TEST,
            "tests/test_two.py": PASSING_TWO,
            "sub/tests/test_one.py": FAILING_TEST.replace("test_two", "test_one"),
            "sub/pytest.ini": "[pytest]\nan_unknown_key = 1\n",
        },
        {
            "sub/tests/test_one.py": FAILING_TWO.replace("test_two", "test_one"),
            "sub/tests/test_two.py": FAILING_TWO,
        },
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_one.py") == gate.NO_RUNNER, out.stdout
```
```
A row that runs pytest in more than one directory — `pytest -q && cd sub && pytest -q` — is asked about every failing file by the first runner a prefix reaches, in that runner's directory: a file a later runner named reads `new` where that directory has no such file, and `failing on base too` where a same-named file there fails at the base. Read either word as the row's claim rather than a measurement, or write the row so one runner runs every directory.
```
```python
        "A row that runs pytest in more than one directory — `pytest -q && "
        "cd sub && pytest -q` — is asked about every failing file by the first "
        "runner a prefix reaches, in that runner's directory: a file a later "
        "runner named reads `new` where that directory has no such file, and "
        "`failing on base too` where a same-named file there fails at the base.",
```
```
So a run at the base, of a row with one runner as written, with the file
appended, asks the right directory whatever moved it.
```
```
| A row with two pytest runners in two directories | A candidate's solo run settles at the first runner, in its directory (`new` for a file the base fails), and a group's run can measure the root's same-named file (`failing on base too`). Measured in round 1, probes p1 and p1b, and identical at 94d7b2e0. No run of the row distinguishes the two runners' files, so rule 3 names it | the repository owner, if it is ever met — a new issue |
```

## Executed probes

| What was run | Result |
|---|---|
| The selected cases of `tests/test_the_seal_is_taken_once_by_the_sealer.py` around the comparison (S1–S5, S7, the base-lacks case, the below-a-cd case, the limit case, the runner-first, semicolon and lint-first cases, the `NO_RUNNER` pin), `-n 4`, in the clone at `c553bd92` | 25 passed, 0 skipped |
| Mutation: the `alone and` guard dropped | `test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd` failed; the clone restored |
| Mutation: the return written as `verdicts` | `test_a_root_run_row_measures_the_module_the_branch_added[plain]` failed; the clone restored |
| p1: `compare_at_base` on a row with a root runner and a `cd sub` runner; the base fails `sub/tests/test_two.py`, plain and `-n 2`, the target's gate and `94d7b2e0`'s | `new` from all four; at the target from `suite-at-base-1-1.txt`, which ends `no tests ran` (exit 4, or exit 5 under `-n 2`) |
| p1b: the same row; the base fails a different root `tests/test_two.py`, and the branch adds a failing `sub/tests/test_two.py` | `failing on base too` at both gates |
| p2: `cd sub` row in the un-nominated direction, the base failing `sub/tests/test_one.py`, with and without an unknown ini key, plain and `-n 2`, at both gates | without the key: `new?` for both files; with it: `new` for both, kept outputs ending `1 warning in 0.00s` and `3 warnings in 0.49s` |
| p3: an exit-remapping wrapper row, the branch adding a failing root module | the target gives `new?`; `94d7b2e0` gives `new` |
| Finding 1's fix applied in the clone: the probes, then the selected comparison cases plus the new case and rows | p2 all `new?`; 63 passed |
| Finding 1's new case and rows against the target's gate | 4 failed (the two `True` warning rows, and the case plain and `-n 2`); the clone restored |
| The full suite, lint and typecheck (the broad gate) | not yet — the sealer's, after the rounds settle; not run in this round |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
