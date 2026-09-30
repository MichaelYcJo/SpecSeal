# 1790690762-arm-check-reads-every-supported-ast — review round 2

| Field | Value |
|---|---|
| Target SHA | 806fad617bcd7ec2d5f886e2181022f66e3cc184 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #685 — https://github.com/MichaelYcJo/SpecSeal/pull/685 |
| Broad gate | e216193f against 20d1b289 |
| Fixes checked by | no fixes to check |
| Fix range | `806fad617bcd7ec2d5f886e2181022f66e3cc184..86d1bc9717b1773229fafabd878eb10be9bd06a9`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, verifying, over round 1's fix range `deb6290f..54e31f21` at HEAD `806fad61`. Asked whether each of round 1's six verdicts is closed. It pushed on `selects_this_module` across every realistic spelling of a pytest invocation in a workflow `run:`, and on the imported job splitter under `-n auto` and a pytest-only install. It re-ran the module on 3.12, 3.13 and 3.14 and the modules that read the workflow, and ran the three ledger checks.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `selects_this_module` answers True for a filter bundled behind a flag (`-qk`, `-vm`), for an option that runs no case (`--setup-plan`, `--setup-only`, `--fixtures`, `--markers`, `--version`, `-h`), for a `--deselect` prefix shorter than the module path, and for an `--ignore-glob` spelled with `./`; pytest runs no case of the module under each, and exits 0 wherever other cases still run | `tests/test_arm_check.py:266` | deferred #687 | Executed on 3.13 against pytest 9.1.1 in a fixture repository; with the arm job's line rewritten to `pytest tests/ -qk 'not arm'`, S6 is green on 3.12 and 3.14. No defect ships: today's workflow is read right |
| ⬜ 2 | `pythons_ci_runs_this_module_at` reads each physical line, so a folded or plain multi-line `run:` whose second line holds `--ignore` of the module or `-k` is counted at 3.13 and 3.14 | `tests/test_arm_check.py:299` | deferred #687 | Executed: three shapes counted, and pytest ran the module under none of them; with the arm job rewritten to the folded shape, S6 is green on 3.12 and 3.14. A different unit from ⬜ 1, which predates round 1's fixes |
| ⬜ 3 | Six of `_UNREADABLE`'s eight options are pinned by no case, and its comment names a class that `--co` is not in | `tests/test_arm_check.py:244` | deferred #687 | Executed: `_UNREADABLE` emptied, all 14 line cases green |
| ⬜ 4 | L3's Notes name the literal-block continuation that fails closed and omit the folded and plain shapes that count, where the clause says an `--ignore` of the module is never counted | `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md` L3 | answered | `86d1bc97` — L3's note says a literal block continued with a backslash does not count, and a folded or plain multi-line `run:` is counted with an `--ignore` or `-k` on its second line unseen; the counting half is #687; Read against ⬜ 2's probe. Paperwork, so not counted in `Needs a fix` |
| 🟢 | round 1's finding 1 is closed — S6 requires the Python just below each bound | `tests/test_arm_check.py:340` | confirmed | Executed on 3.12.11 and 3.14.3: 3.13 leg deleted is red naming 3.13, 3.14 leg deleted is red naming 3.14, control green; restatements read at `f75d1b9b` |
| 🟢 | round 1's finding 2 is closed as written — an `--ignore` of the module, in either spelling, is not counted | `tests/test_arm_check.py:256` | confirmed | Executed: both spellings red naming 3.13 and 3.14, `pytest tests/ -q` green; five removal lines red with `_removes_this_module` answering False. The class it belongs to is wider, which is this round's ⬜ 1 and ⬜ 2 |
| 🟢 | round 1's finding 3 is closed — S6 splits jobs with the suite's one splitter | `tests/test_arm_check.py:299` | confirmed | Executed: red with `jobs` returning `{}`; green with pytest alone on 3.12, 3.13, 3.14 and under `-n auto` on 3.13. A `jobs:` on the first line now raises rather than reads, which fails closed |
| 🟢 | round 1's findings 4 and 5 are closed — the matrix comment and the CONTRIBUTING job list | `.github/workflows/test.yml:32` | confirmed | Read at `806fad61`: `test.yml:32-37` and `CONTRIBUTING.md:161-164` |
| 🟢 | round 1's finding 6 is closed — L2 says 17 | `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md` L2 | confirmed | Executed on 3.9.6 at `806fad61`: 124 classified, 17 absent from `ast` |
| 🟢 | S6 reads today's `test.yml` as intended | `.github/workflows/test.yml:122` | confirmed | Executed: the reader gives `{3.12, 3.13, 3.14}` from the `pytest` and `arm-check-grammar` jobs, lint and ledger contribute nothing, and S6 requires `{3.13, 3.14}` |
| 🟢 | The module and every module that reads `test.yml` or `CONTRIBUTING.md` are green; the ledger and the two range checkers are clean | `tests/test_arm_check.py` | confirmed | Executed: 74 passed and 2 skipped on 3.12.11 and 3.13.9, 76 passed on 3.14.3; 30 modules on 3.13.9 with `-n auto` 1586 passed, 2 skipped; `evidence_check.py --strict` exit 0 with 0 drifted; `correction_check.py` and `survivor_check.py` exit 0 |
| ❓ | S7: the two legs of `arm-check-grammar` on GitHub's runners | `.github/workflows/test.yml:122` | ❓ out of verified scope | Not executable here. CI on pull request #685 answers it |
| ❓ | `questions.md` Q1: the whole suite on 3.14 | `seal/specs/1790690762-arm-check-reads-every-supported-ast/questions.md` Q1 | ❓ out of verified scope | A broad run is not a warden's. The sealer answers it, and has to choose 3.14 on purpose because the worktree's `.venv` is 3.13.9 |

## Paste-ready fixes

```python
# pytest's options that take a module back out of the paths it was handed.
# These three name what they remove, so each is read for whether it names
# this module.
_REMOVES = ("--ignore", "--ignore-glob", "--deselect")
# These select by an expression or by an earlier run, or run no case at all,
# which no reading of the line can resolve, so a job carrying one is not
# counted as running it.
_UNREADABLE = (
    "-k",
    "-m",
    "--lf",
    "--last-failed",
    "--sw",
    "--stepwise",
    "--co",
    "--collect-only",
    "--setup-only",
    "--setup-plan",
    "--fixtures",
    "--funcargs",
    "--fixtures-per-test",
    "--markers",
    "-h",
    "--help",
    "-V",
    "--version",
)
# pytest's short options that take a value. argparse lets a word bundle
# short options that take none ahead of one of these, so `-qk expr` is
# `-q -k expr`, and the letters after one of these are its value.
_SHORT_WITH_VALUE = "kmprcoWn"


def _short_options(word):
    """The short options a single-dash `word` bundles, `-qk` giving `-q`
    and `-k`, up to and including the first that takes a value."""
    for letter in word[1:]:
        yield "-" + letter
        if letter in _SHORT_WITH_VALUE:
            return


def _removes_this_module(option, value):
    """Whether `option value` takes `_THIS_MODULE` out of what pytest runs."""
    if option == "--ignore-glob":
        # pytest makes the glob absolute before it matches, so `./` and a
        # trailing `/` mean nothing to it.
        glob = posixpath.normpath(value)
        return fnmatch.fnmatch(_THIS_MODULE, glob) or fnmatch.fnmatch("tests", glob)
    if option == "--deselect":
        # A node id PREFIX: `tests/test_arm` deselects every case here.
        return any(
            _THIS_MODULE.startswith(prefix) or prefix.startswith(_THIS_MODULE)
            for prefix in (value, posixpath.normpath(value))
        )
    path = posixpath.normpath(value.split("::", 1)[0])
    return path == _THIS_MODULE or _THIS_MODULE.startswith(path + "/")


def selects_this_module(line):
    """Whether the pytest invocation on `line` runs `tests/test_arm_check.py`:
    it hands pytest the module or `tests/`, and no option takes the module
    back out. The line is split with `shlex`, and only pytest's own
    selection options are read; a line `shlex` cannot split counts as not
    running it."""
    try:
        words = shlex.split(line)
    except ValueError:
        return False
    start = next(
        (i for i, w in enumerate(words) if posixpath.basename(w) == "pytest"), None
    )
    if start is None:
        return False
    args, named, i = words[start + 1 :], False, 0
    while i < len(args):
        word = args[i]
        option, has_value, value = word.partition("=")
        if option in _REMOVES:
            if not has_value and i + 1 < len(args):
                i += 1
                value = args[i]
            if _removes_this_module(option, value):
                return False
        elif option in _UNREADABLE or (
            word[:1] == "-"
            and word[:2] != "--"
            and any(short in _UNREADABLE for short in _short_options(word))
        ):
            return False
        elif posixpath.normpath(word) in ("tests", _THIS_MODULE):
            named = True
        i += 1
    return named


_RUN_KEY = re.compile(r"^(\s*(?:-\s+)?)run:\s*(.*)$")


def _run_commands(block):
    """The commands each `run:` key in `block` hands the shell. A folded
    (`>`) or plain scalar is one command however many lines it spans; a
    literal (`|`) block is one per line, a line ending in a backslash joined
    to the next."""
    lines, commands, i = block.splitlines(), [], 0
    while i < len(lines):
        key = _RUN_KEY.match(lines[i])
        i += 1
        if not key:
            continue
        column, value, body = len(key.group(1)), key.group(2).strip(), []
        while i < len(lines) and (
            not lines[i].strip() or len(lines[i]) - len(lines[i].lstrip(" ")) > column
        ):
            body.append(lines[i].strip())
            i += 1
        if value[:1] == "|":
            pending = ""
            for line in body:
                if line.endswith("\\"):
                    pending += line[:-1] + " "
                    continue
                commands.append(pending + line)
                pending = ""
            if pending:
                commands.append(pending)
        elif value[:1] == ">":
            commands.append(" ".join(body))
        else:
            commands.append(" ".join([value, *body]))
    return commands


def pythons_ci_runs_this_module_at(text):
    """Every `(major, minor)` a job in `text` pins while it runs pytest over
    this module, read through `conftest.code_lines` so a commented-out leg
    or step counts for nothing. The jobs are split by
    `tests/test_ci_gives_the_checks_what_they_need.py#jobs`, the suite's one
    reader of a workflow's `jobs:` block, and a job's commands are read by
    `_run_commands`, so a `run:` continued over several lines is read as the
    one command the shell receives."""
    found = set()
    for block in jobs("\n".join(code_lines(text))).values():
        if any(selects_this_module(command) for command in _run_commands(block)):
            for line in block.splitlines():
                found.update((int(a), int(b)) for a, b in _PINNED_PYTHON.findall(line))
    return found
```
```python
@pytest.mark.parametrize(
    "line, runs",
    [
        ("- run: pytest tests/ -qk 'not arm'", False),
        ("- run: pytest tests/ -vm slow", False),
        ("- run: pytest tests/ --setup-plan", False),
        ("- run: pytest tests/ --fixtures", False),
        ("- run: pytest tests/ --collect-only", False),
        ("- run: pytest tests/ --lf", False),
        ("- run: pytest tests/ -h", False),
        ("- run: pytest tests/ --deselect tests/test_arm", False),
        ("- run: pytest tests/ --ignore-glob=./tests/*", False),
        ("- run: pytest tests/ -rA -n auto -Werror::DeprecationWarning", True),
    ],
)
def test_a_bundled_flag_a_run_of_nothing_and_a_prefix_are_read(line, runs):
    """What pytest accepts beyond the spellings above, each measured against
    a real pytest in round 2: a filter bundled behind a flag, an option that
    runs no case, a `--deselect` prefix and a `./` glob all leave this module
    unrun, and exit 0 where the rest of the suite passes."""
    assert selects_this_module(line) is runs


@pytest.mark.parametrize(
    "run, counted",
    [
        ("      - run: pytest tests/test_arm_check.py -q", True),
        (
            "      - run: |\n          pip install pytest\n"
            "          pytest tests/test_arm_check.py -q",
            True,
        ),
        (
            "      - run: |\n          pytest \\\n            tests/test_arm_check.py -q",
            True,
        ),
        (
            "      - run: >\n          pytest tests/\n          --ignore=tests/test_arm_check.py",
            False,
        ),
        (
            "      - run: pytest tests/\n          --ignore=tests/test_arm_check.py",
            False,
        ),
        ("      - run: >-\n          pytest tests/ -q\n          -k 'not arm'", False),
    ],
)
def test_a_run_continued_over_lines_is_read_as_one_command(run, counted):
    """A folded or plain `run:` hands the shell its lines joined, so an
    `--ignore` on the second line removes what the first named."""
    text = (
        "name: t\njobs:\n  arm:\n    strategy:\n      matrix:\n        include:\n"
        '          - { python: "3.14" }\n    steps:\n' + run + "\n"
        "      - run: echo done\n"
    )
    assert (pythons_ci_runs_this_module_at(text) == {(3, 14)}) is counted
```
```text
A job's `run:` is read as the commands the shell receives: a folded or plain scalar is one command however many lines it spans, and a literal block is one command per line with a backslash continuation joined, so an `--ignore` or `-k` on a continuation line removes what the first line named.
```
```text
A literal `run:` block whose pytest command is continued with a backslash is read line by line and does not count; a folded or plain multi-line `run:` is read the same way, so an `--ignore` or `-k` on its second line is not seen and the job is counted.
```

## Executed probes

| What was run | Result |
|---|---|
| `tests/test_arm_check.py` at `806fad61`, `uv run --isolated --no-project --with pytest`, on 3.12.11, 3.13.9 and 3.14.3 | exit 0 each: 74 passed and 2 skipped, the same, 76 passed |
| **Disclosed**: my first run of that command had bytecode writing turned off in the environment | 2 failed on each Python, the two bytecode-cache cases, which need bytecode to be written. The environment caused this, not the code. Re-run with the default and reported above |
| 30 modules that read `test.yml`, `CONTRIBUTING.md` or a workflow's jobs, with `tests/test_arm_check.py`, `tests/test_ci_gives_the_checks_what_they_need.py`, `tests/test_a_workflow_is_read_the_one_way.py`, `tests/test_no_real_identifiers.py` and the floor module `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` among them; 3.13.9, pytest-xdist `-n auto`, markdown-it-py 4.2.0 | exit 0, 1586 passed, 2 skipped |
| S6 against ten workflow mutants written to a temp file, on 3.12.11 and 3.14.3 | as listed under round 1's findings 1 to 3 and this round's ⬜ 1 and ⬜ 2; identical on both Pythons |
| 27 run lines through `selects_this_module` and through a real pytest 9.1.1 in a fixture repository, on 3.13.9 | 15 false counts; one of them (`uvx --from pytest`) was my probe's artifact, and `--sw-skip` was confounded by `-p no:cacheprovider`, so both are excluded; `--ign=` exits 4, so it is loud. What remains is ⬜ 1 |
| pytest's exit code under each ⬜ 1 spelling | 0 for eight, 5 for two in the fixture (where the mark or glob left no case at all), 4 for the abbreviation |
| Six multi-line `run:` shapes through the head's reader, with PyYAML showing the shell's command | ⬜ 2's table |
| The line case with `_removes_this_module` answering False, and with `_UNREADABLE` emptied | five lines red; nothing red (⬜ 3) |
| `arm_check.py` loaded on `/usr/bin/python3` 3.9.6, `hasattr(ast, name)` over the classified names | 124 classified, 17 absent |
| The paste-ready fix, exec'd into the module's namespace, on 3.12.11 and 3.14.3 | the 14 existing cases green, the 10 and 6 new cases green, S6 green on today's `test.yml`, reading `{3.12, 3.13, 3.14}` |
| The paste-ready fix and cases under the repository's `ruff.toml` | only undefined-name errors from linting a fragment; `ruff format --check` clean |
| `uvx ruff check` and `ruff format --check` on `tests/test_arm_check.py` | exit 0 |
| `evidence_check.py --strict .` | exit 0, 0 drifted, 0 broken; this work item's fragment 14 ok |
| `correction_check.py --range origin/release/v0.16.0...HEAD` | exit 0; no merge commit in `346b4af..806fad6` |
| `survivor_check.py`, ranges `deb6290f..806fad61` and `origin/release/v0.16.0...HEAD` | exit 0 each; 14 and 11 removed sentences, none standing |
| The broad gate (`broad-gate`, the sealer's) | not yet. Nothing open needs a fix, so it has come due, and what comes due is the sealer's spawn, run on 3.14 for Q1 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_arm_check.py:273` | round 1's ⬜ 1 — fixed |
| round-1 | `tests/test_arm_check.py:233` | round 1's ⬜ 2 — fixed |
| round-1 | `tests/test_arm_check.py:237` | round 1's ⬜ 3 — fixed |
| round-1 | `.github/workflows/test.yml:33` | round 1's ⬜ 4 — answered |
| round-1 | `CONTRIBUTING.md:161` | round 1's ⬜ 5 — answered |
| round-1 | `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md` L2 | round 1's ⬜ 6 — answered |
| round-1 | `skills/verify/scripts/arm_check.py:162` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/arm_check.py:289` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/arm_check.py:431` | round 1's 🟢 — confirmed |
| round-1 | `.github/workflows/test.yml:118` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.9.5.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1790690762-arm-check-reads-every-supported-ast/questions.md` Q1 | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
