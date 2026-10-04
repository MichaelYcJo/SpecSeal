# 1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | pending — the commit that adds this record, named in the next one |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`questions.md` Q1, as a measurement: what pytest 9.1.1 prints, and with what
exit code, when one appended test path does not exist — once plain and once
under `pytest-xdist` 3.8.0 with `-n 2` — invoked from a directory below a
scratch root, output and exit code recorded here verbatim. The result fixes
the line form the not-found reading matches and the text S5's measured-ending
row carries. No change to the tree beyond this record.

The spawn added a stop condition to Q1's options: **if the not-found phrase is
absent under `-n`, stop after phase 1 and hand back the measured output rather
than improvising.**

## What this phase found

**Q1 is answered (c): under `pytest-xdist` the not-found reply is not printed
at all, so the build stops here.** The frame's premise — that pytest's own
reply at the base says which appended file the base lacks — holds for plain
pytest and fails for the row this repository runs.

### The runs

The scratch root held one file, `sub/tests/test_one.py`, whose one test fails
(`def test_a(): assert False`). Every run was invoked from `<scratch>/sub`
with `python -m pytest`, from this worktree's `.venv` (pytest 9.1.1,
pytest-xdist 3.8.0, Python 3.14.3, darwin), through `subprocess.run` with an
argument list. stdout and stderr are given as Python reprs; `<scratch>` and
`<venv-python>` stand for the paths the runs printed. The scratch directory is
removed.

| # | Arguments after `python -m pytest` | Exit | stdout | stderr |
|---|---|---|---|---|
| 1 | `-q -p no:cacheprovider tests/test_one.py tests/test_two.py` | 4 | `'\nno tests ran in 0.00s\n'` | `'ERROR: file or directory not found: tests/test_two.py\n\n'` |
| 2 | `-q -p no:cacheprovider -n 2 tests/test_one.py tests/test_two.py` | 5 | `'bringing up nodes...\nbringing up nodes...\n\n\nno tests ran in 0.21s\n'` | `''` |
| 3 | `-q -p no:cacheprovider tests/test_two.py tests/test_one.py` | 4 | `'\nno tests ran in 0.00s\n'` | `'ERROR: file or directory not found: tests/test_two.py\n\n'` |
| 4 | `-q -p no:cacheprovider -n 2 tests/test_two.py tests/test_one.py` | 5 | `'bringing up nodes...\nbringing up nodes...\n\n\nno tests ran in 0.21s\n'` | `''` |
| 5 | `-q -p no:cacheprovider -n 2 tests/test_one.py tests/test_two.py tests/test_three.py` | 5 | `'bringing up nodes...\nbringing up nodes...\n\n\nno tests ran in 0.21s\n'` | `''` |
| 6 | `-q -p no:cacheprovider -n 2 tests/test_one.py` (control: nothing missing) | 1 | ends `'…short test summary info …\nFAILED tests/test_one.py::test_a - assert False\n1 failed in 0.22s\n'` | `''` |

A second pass looked for the text anywhere under other output settings, with
stdout and stderr joined (`'not found' in out`):

| # | Arguments after `python -m pytest` | Exit | Output | `not found` in it |
|---|---|---|---|---|
| 7 | `-p no:cacheprovider -n 2 tests/test_one.py tests/test_two.py` | 5 | `'===… test session starts ===…\nplatform darwin -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0\nrootdir: <scratch>/sub\nplugins: xdist-3.8.0\ncreated: 2/2 workers\n2 workers [0 items]\n\n\n===… no tests ran in 0.23s ===…\n'` | no |
| 8 | `-v -p no:cacheprovider -n 2 tests/test_one.py tests/test_two.py` | 5 | as 7, with `-- <venv-python>` on the platform line, `scheduling tests via LoadScheduling`, and `no tests ran in 0.22s` | no |
| 9 | `-q -rA -p no:cacheprovider -n 2 tests/test_one.py tests/test_two.py` | 5 | `'bringing up nodes...\nbringing up nodes...\n\n\nno tests ran in 0.22s\n'` | no |
| 10 | `-q -p no:cacheprovider -n auto tests/test_one.py tests/test_two.py` | 5 | `'bringing up nodes...\nbringing up nodes...\n\n\nno tests ran in 0.59s\n'` | no |
| 11 | `-q -p no:cacheprovider -n 0 tests/test_one.py tests/test_two.py` | 4 | `'\nno tests ran in 0.00s\nERROR: file or directory not found: tests/test_two.py\n\n'` | yes |

And the row this repository runs, from the worktree root:
`bin/test -q tests/test_one_word_one_meaning.py tests/test_B_does_not_exist.py`
exited 5 and printed, after the runner's own `bin/test: <venv-python>` line,
`bringing up nodes...` twice and `no tests ran in 0.64s`. Nothing else.

### What the runs settle

- **Plain pytest: Q1's option (a).** The reply is a line of its own on
  stderr, `ERROR: file or directory not found: <arg>`, exactly as appended,
  relative to the invocation directory, and it names the first missing
  argument whatever its position (runs 1 and 3). The exit is 4. `-n 0`
  behaves the same (run 11).
- **Under xdist: option (c).** With any appended path missing, the workers
  collect nothing (`2 workers [0 items]`), the run exits 5, and the text
  `not found` appears in no output setting tried (runs 2, 4, 5, 7–10).
  **The present file's failing test does not run either** (control run 6
  shows it would): one missing path costs the measurement for every file of
  that run, and nothing in the output says which path did it.
- **No counterfeit word comes out of it.** `no tests ran in 0.21s` carries no
  leading count, so `PYTEST_SUMMARY_RE` does not match it — the frame's
  technical context already records that for plain pytest, and the xdist line
  is the same text. Every prefix tried prints no summary, and every file of
  the run reads `NO_RUNNER` (`new?`).

### Why this stops the build rather than letting it go on to phase 2

Q1's option (c) lets the build continue where xdist output gives no measured
word, and that half holds. The spawn's stop condition is narrower and is the
one followed. It is also the one the measurement argues for, because of what
plan A would do to this repository's own row:

| | At 94d7b2e0 | After plan A, under xdist |
|---|---|---|
| A branch adds a failing `tests/test_new.py` and also fails `tests/test_old.py`, which the base fails too; the row ends in `bin/test -q` | the root split finds `tests/test_new.py` absent at the base and gives it `new` without a run; `tests/test_old.py` is run alone at the base and reads `failing on base too` | both are appended; the run prints `no tests ran`, no not-found reply and no summary; **both read `new?`** |

The middle column is read from `compare_at_base` at 94d7b2e0. The right
column applies the measured runs above to `plan.md`'s approach A as written;
no code for A exists, so it is read, not executed.

`bin/test` runs pytest from the repository root, so for this row the root
split asks the right directory and its `new` is not counterfeit. Plan A would
replace two measured words with two unmeasured ones on every failing broad
gate of a branch that adds a failing test module — which `compare_at_base`'s
own docstring calls "every branch that adds a test module". That is weaker,
never counterfeit, and it lands on the row this repository runs. Spec
Scope 2's sentence "pytest's own reply is the measurement of absence" is true
only where xdist is off.

What a re-frame has to choose between is `questions.md` Q4, opened by this
phase. Nothing was built toward any of its options.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
