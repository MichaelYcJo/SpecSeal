# 1790690762-arm-check-reads-every-supported-ast — round 2 report

| Field | Value |
|---|---|
| Round | 2, a verifying round |
| Target SHA | `806fad61` |
| Fix range checked | `deb6290f..54e31f21` (round 1's fix table), with `4a15bd7d` and `806fad61` read as paperwork |
| Base | `346b4af7`, the merge base with `origin/release/v0.16.0` (now at `20d1b289`) |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` at the target and a second at `deb6290f`, both in the session scratchpad. Nothing was written in the worktree except this file |

## What this round found

Nothing needs a fix. All six of round 1's verdicts are closed, and each one
held when I ran or read it. The S6 guard reads today's `test.yml` exactly as
intended. The module is green on 3.12, 3.13 and 3.14 with pytest alone. The
cross-module import holds under `-n auto`. The three checkers are clean.

The push on `selects_this_module` found four ⬜ items. None of them ships a
defect, because every one needs a future edit to `test.yml` before it
matters:

- **⬜ 1.** `selects_this_module` counts four more kinds of spelling under which
  pytest runs no case of this module and still exits 0.
- **⬜ 2.** `pythons_ci_runs_this_module_at` reads one physical line at a time.
  A folded or plain multi-line `run:` that puts `--ignore` or `-k` on its
  second line is therefore still counted.
- **⬜ 3.** Six of `_UNREADABLE`'s eight options are pinned by no case.
- **⬜ 4 (paperwork).** L3's Notes name the multi-line shape that does not
  count and leave out the two shapes that do.

⬜ 1 and ⬜ 2 belong to the class round 1's ⬜ 2 named. Round 1 named one
member of that class, and the fix closed that member and the neighbours it
listed. It did not close the whole class. One tested fix, below, covers
⬜ 1 to ⬜ 3.

## Round 1's verdicts, one by one

### ⬜ 1 (S6 holds the Python below each bound): closed

Read: `below` at `tests/test_arm_check.py:340` adds `(major, minor - 1)` for
each bound at or above `run_tests_floor()`. Today the one bound is `(3, 14)`,
so S6 requires 3.13 and 3.14.

Executed: I ran S6 on 3.12.11 and on 3.14.3 against the workflow mutants. S6
read each mutant through its `WORKFLOW` path, and the clone was never
edited.

- 3.13 leg deleted: red, naming `['3.13']`.
- 3.14 leg deleted: red, naming `['3.14']`.
- Control: green.

The docstring's `Red how` and L3's claim match these results. The two
restatements round 1 named are corrected at `f75d1b9b`: the `test.yml`
comment at line 119 and the module docstring.

### ⬜ 2 (an `--ignore` of this module was counted): closed as written, class open

Executed, same probe:

- The job's line rewritten to `pytest tests/ --ignore=tests/test_arm_check.py -q`: red, naming 3.13 and 3.14.
- The same with `--ignore` as a separate word: red, naming 3.13 and 3.14.
- Rewritten to `pytest tests/ -q`: green. This is right, because that job
  then runs the whole suite at 3.13 and 3.14.

With `_removes_this_module` answering False, the five removal lines of the
line case go red, as its docstring says.

The class is wider than the spellings pinned. See ⬜ 1 and ⬜ 2 below.

### ⬜ 3 (a second copy of the job splitter): closed

Read: `pythons_ci_runs_this_module_at` calls the `jobs` it imports from
`tests/test_ci_gives_the_checks_what_they_need.py#jobs` on
`"\n".join(code_lines(text))`.

Executed:

- With `jobs` replaced by a function returning `{}`, S6 is red, naming 3.13
  and 3.14.
- The import holds under the CI job's install, which is pytest alone. The
  module ran with `--with pytest` only on three Pythons.
- The import holds under `-n auto`. A 30-module run on 3.13.9 with
  pytest-xdist was green, and it included both modules.
- The imported module needs only `os`, `re` and `conftest`.

Other test modules in this suite already import from test modules (for
example `tests/test_a_finding_id_is_a_bare_integer.py`), so the pattern is
established here.

One behaviour changed, and in the safe direction. The inline splitter read a
workflow whose first code line is `jobs:`. The imported one raises an
assertion that there is no `jobs:` block, which turns S6 red rather than silently
green. Executed: that fragment raises. `test.yml` does not have that shape.

### ⬜ 4, ⬜ 5 (wording): closed

Read at `806fad61`:

- `test.yml:32-37` now says the module is the one *known* to depend on the
  interpreter, and that no other module was measured.
- `CONTRIBUTING.md:161-164` carries the reason in parentheses. The five jobs
  still count to five: lint, the suite, arm-check, the ledger, and hygiene.

### ⬜ 6 (L2's count): closed

Executed: `/usr/bin/python3` (3.9.6) loads `arm_check.py` at the head. It
has 124 classified names, and `ast` lacks 17 of them. That matches L2's
corrected Notes.

## New findings (this round)

### ⬜ 1 — `selects_this_module` counts spellings under which pytest runs no case of this module

This finding is at `tests/test_arm_check.py:266`, a unit created by round 1's
fixes.

Executed: each line below went to `selects_this_module` and, as the same
words, to a real pytest 9.1.1 on 3.13. The pytest run used a fixture
repository holding `tests/test_arm_check.py` (two cases) and
`tests/test_other.py`. For every line, `selects_this_module` answered True
and pytest ran no case of the module:

| Spelling | pytest exit |
|---|---|
| `pytest tests/ -qk 'not arm'` (argparse unbundles `-q -k`) | 0 |
| `pytest tests/ -vm slow` | 5 in the fixture, where no case carries the mark; read, not run: 0 wherever another case carries it |
| `pytest tests/ --setup-plan`, `--setup-only`, `--fixtures`, `--markers`, `--version`, `-h` | 0 each |
| `pytest tests/ --deselect tests/test_arm` (`--deselect` is a node-id **prefix**) | 0 |
| `pytest tests/ --ignore-glob=./tests/*` (pytest makes the glob absolute first) | 5 in the fixture, where it ignores every case; read, not run: 0 under a narrower glob such as `./tests/*arm*`, which leaves the rest running |

This matters because S6 exists to fail when no leg runs this module at a
bound. Wherever pytest exits 0, the arm-check job stays green, S6 stays
green, and the module runs at no Python. The workflow-level probe confirms
it: with the job's line rewritten to `pytest tests/ -qk 'not arm'`, S6 is
green on 3.12 and 3.14.

Why ⬜ and not 🟡: today's `test.yml` is read correctly, so the release ships
no defect. What is missing is the guard against a future edit, which is how
round 1 graded the same class.

Other spellings failed closed, which is the safe direction and not a
finding:

- `bin/test tests/test_arm_check.py`: S6 red, naming 3.13 and 3.14.
- `pytest tests/test_arm*.py`: not counted.
- A `::case` selection: not counted.
- `pytest … && python -m …`: not counted, because the `-m` after `&&` is read
  as pytest's.
- A quoted whole `run:` value: not counted.

The same probe showed an abbreviated option such as `--ign=` makes pytest
exit 4, so CI fails loudly on it. No false count comes from abbreviations.

### ⬜ 2 — a `run:` continued over several lines is read line by line, so a folded or plain scalar's second line is lost

This finding is at `tests/test_arm_check.py:299`, in
`pythons_ci_runs_this_module_at`. That unit predates round 1's fixes, which
is why this is a separate finding from ⬜ 1.

The unit calls `selects_this_module` on each physical line of a job. YAML
joins a folded (`run: >`) or plain multi-line scalar into one command. The
reader does not.

Executed on 3.13, with PyYAML used only to show what the shell receives:

| `run:` shape | The shell receives | S6 counts | pytest runs the module |
|---|---|---|---|
| `>` with `--ignore=tests/test_arm_check.py` on line 2 | `pytest tests/ --ignore=tests/test_arm_check.py` | 3.13, 3.14 | no |
| plain scalar, same second line | the same | 3.13, 3.14 | no |
| `>-` with `-k 'not arm'` on line 2 | `pytest tests/ -q -k 'not arm'` | 3.13, 3.14 | no |
| literal block with a backslash continuation that names the module | `pytest tests/test_arm_check.py -q` | nothing | yes (fails closed) |

With the arm-check job rewritten to the first shape, S6 is green on 3.12 and
3.14. A folded `run: >` is a common way to write a long pytest command, so
this is the most likely member of the class to arrive by accident. It is
still ⬜, for the same reason as ⬜ 1.

### ⬜ 3 — six of `_UNREADABLE`'s eight options are pinned by no case

This finding is at `tests/test_arm_check.py:244`, a unit created by round 1's
fixes.

Executed: with `_UNREADABLE` emptied to `()`, all 14 line cases stay green.
The two filter lines (`-k 'not arm'` and `-mslow`) are caught by the separate
`word[:2] in ("-k", "-m")` branch. `--lf`, `--last-failed`, `--sw`,
`--stepwise`, `--co` and `--collect-only` can each be deleted with no case
going red.

The docstring's `Red how` claims red "with the `_UNREADABLE` branch deleted",
and that holds, because the branch deletion takes the short-option arm with
it. The tuple's own entries are unpinned, which is §14's gap.

The comment above the tuple also says these options "select by an expression
or by an earlier run". `--co` does neither: it runs nothing. The fix below
widens the comment to the class it actually holds.

### ⬜ 4 — paperwork: L3's Notes state the multi-line shape that fails closed and omit the two that count

This finding is at `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md`,
L3, Notes: "A `run: \|` block whose pytest command is continued over several
lines is read line by line and would not count."

That sentence is true, and the probe in ⬜ 2 confirms it. But L3's clause
says a job counts only where "no `--ignore` … names the module". A folded or
plain scalar that does name the module in an `--ignore` is counted, which
the clause as written excludes.

If the ⬜ 1–3 fix is taken, the Notes sentence changes too, because a
backslash continuation then counts. The replacement is fenced below. Because
this is in a record, it is a correction and is not counted in `Needs a fix`.

## The account, checked

- Round 1's record claims ⬜ 1 is "red naming `['3.13']`" with the 3.13 leg
  removed. Confirmed on 3.12 and 3.14.
- It claims ⬜ 2 is red in both spellings with the control green, and "14
  parametrized cases pin it". The first half is confirmed. The 14 cases pin
  the removal and short-filter branches, but not six of `_UNREADABLE`'s
  entries (⬜ 3).
- It claims ⬜ 3's versions read are unchanged and S6 is red with `jobs`
  emptied. Confirmed: `{3.12, 3.13, 3.14}` before and after.
- L3's Verified behavior says the line case is red "with the `-k`/`-m`
  branch deleted (the two filter lines)". Consistent with ⬜ 3: deleting the
  branch is red, and emptying the tuple is not.
- L2's 17 of 124 on 3.9.6 is confirmed.

## Regression tests to plant

Only if the ⬜ 1–3 fix is taken. Both new cases go into
`tests/test_arm_check.py` beside
`test_a_job_counts_only_where_its_pytest_line_selects_this_module`. Seen red,
executed in this round:

- Against the head's `selects_this_module`, the seven false-count lines of
  the new line case each answer True. The two control lines, `--collect-only`
  and `--lf`, answer False, and the one True line answers True.
- Against the head's `pythons_ci_runs_this_module_at`, four of the six
  workflow cases are red: the three false counts and the backslash
  continuation that names the module. The one-line and two-command controls
  are green.

## Facts for the evidence ledger

- pytest 9.1.1: `--deselect` takes a node-id prefix, so
  `--deselect tests/test_arm` deselects every case in
  `tests/test_arm_check.py`. It exits 0 when the rest passes. Executed
  2026-09-30 on 3.13.9.
- pytest 9.1.1 refuses an abbreviated long option (`--ign=` exits 4).
  Executed the same day.
- A folded or plain multi-line `run:` reaches the shell as one line joined
  by spaces. Executed through PyYAML the same day. This is the ground for L3
  if ⬜ 2 is taken.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `selects_this_module` answers True for a filter bundled behind a flag (`-qk`, `-vm`), for an option that runs no case (`--setup-plan`, `--setup-only`, `--fixtures`, `--markers`, `--version`, `-h`), for a `--deselect` prefix shorter than the module path, and for an `--ignore-glob` spelled with `./`; pytest runs no case of the module under each, and exits 0 wherever other cases still run | `tests/test_arm_check.py:266` | deferred #687 | Executed on 3.13 against pytest 9.1.1 in a fixture repository; with the arm job's line rewritten to `pytest tests/ -qk 'not arm'`, S6 is green on 3.12 and 3.14. No defect ships: today's workflow is read right |
| ⬜ 2 | `pythons_ci_runs_this_module_at` reads each physical line, so a folded or plain multi-line `run:` whose second line holds `--ignore` of the module or `-k` is counted at 3.13 and 3.14 | `tests/test_arm_check.py:299` | deferred #687 | Executed: three shapes counted, and pytest ran the module under none of them; with the arm job rewritten to the folded shape, S6 is green on 3.12 and 3.14. A different unit from ⬜ 1, which predates round 1's fixes |
| ⬜ 3 | Six of `_UNREADABLE`'s eight options are pinned by no case, and its comment names a class that `--co` is not in | `tests/test_arm_check.py:244` | deferred #687 | Executed: `_UNREADABLE` emptied, all 14 line cases green |
| ⬜ 4 | L3's Notes name the literal-block continuation that fails closed and omit the folded and plain shapes that count, where the clause says an `--ignore` of the module is never counted | `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md` L3 | open | Read against ⬜ 2's probe. Paperwork, so not counted in `Needs a fix` |
| 🟢 | round 1's finding 1 is closed — S6 requires the Python just below each bound | `tests/test_arm_check.py:340` | confirmed | Executed on 3.12.11 and 3.14.3: 3.13 leg deleted is red naming 3.13, 3.14 leg deleted is red naming 3.14, control green; restatements read at `f75d1b9b` |
| 🟢 | round 1's finding 2 is closed as written — an `--ignore` of the module, in either spelling, is not counted | `tests/test_arm_check.py:256` | confirmed | Executed: both spellings red naming 3.13 and 3.14, `pytest tests/ -q` green; five removal lines red with `_removes_this_module` answering False. The class it belongs to is wider, which is this round's ⬜ 1 and ⬜ 2 |
| 🟢 | round 1's finding 3 is closed — S6 splits jobs with the suite's one splitter | `tests/test_arm_check.py:299` | confirmed | Executed: red with `jobs` returning `{}`; green with pytest alone on 3.12, 3.13, 3.14 and under `-n auto` on 3.13. A `jobs:` on the first line now raises rather than reads, which fails closed |
| 🟢 | round 1's findings 4 and 5 are closed — the matrix comment and the CONTRIBUTING job list | `.github/workflows/test.yml:32` | confirmed | Read at `806fad61`: `test.yml:32-37` and `CONTRIBUTING.md:161-164` |
| 🟢 | round 1's finding 6 is closed — L2 says 17 | `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md` L2 | confirmed | Executed on 3.9.6 at `806fad61`: 124 classified, 17 absent from `ast` |
| 🟢 | S6 reads today's `test.yml` as intended | `.github/workflows/test.yml:122` | confirmed | Executed: the reader gives `{3.12, 3.13, 3.14}` from the `pytest` and `arm-check-grammar` jobs, lint and ledger contribute nothing, and S6 requires `{3.13, 3.14}` |
| 🟢 | The module and every module that reads `test.yml` or `CONTRIBUTING.md` are green; the ledger and the two range checkers are clean | `tests/test_arm_check.py` | confirmed | Executed: 74 passed and 2 skipped on 3.12.11 and 3.13.9, 76 passed on 3.14.3; 30 modules on 3.13.9 with `-n auto` 1586 passed, 2 skipped; `evidence_check.py --strict` exit 0 with 0 drifted; `correction_check.py` and `survivor_check.py` exit 0 |
| ❓ | S7: the two legs of `arm-check-grammar` on GitHub's runners | `.github/workflows/test.yml:122` | ❓ out of verified scope | Not executable here. CI on pull request #685 answers it |
| ❓ | `questions.md` Q1: the whole suite on 3.14 | `seal/specs/1790690762-arm-check-reads-every-supported-ast/questions.md` Q1 | ❓ out of verified scope | A broad run is not a warden's. The sealer answers it, and has to choose 3.14 on purpose because the worktree's `.venv` is 3.13.9 |

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

Probe hygiene. Every probe read the clone and wrote only to temporary files
beside it. The workflow mutants were separate temp files, so no tracked file
changed, and `git status` in the clone was clean after each probe. My
3.9-count probe failed once on its own loader (the module was not registered
in `sys.modules` before its dataclass ran), was corrected, and ran again.
Every probe file, fixture and clone is deleted at handover.

## Paste-ready fixes

No 🔴 or 🟡 was opened. The ⬜ 1–3 fix below is offered because it is
tested. It closes the class, and does not only close the spellings listed.

### ⬜ 1, ⬜ 2, ⬜ 3 — read what pytest and the shell actually receive

This replaces `_REMOVES` through `pythons_ci_runs_this_module_at` in
`tests/test_arm_check.py`, lines 238–311. `_THIS_MODULE` and
`_PINNED_PYTHON` stay as they are. It adds no import, because `fnmatch`,
`posixpath`, `re` and `shlex` are already imported.

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

The two cases, placed after
`test_a_job_counts_only_where_its_pytest_line_selects_this_module`:

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

The new names in these two fences are proposals, so each prose line naming
one carries the marker.
NAME NOT IN TREE: `_run_commands` and `_short_options` are proposed units.
NAME NOT IN TREE: `_SHORT_WITH_VALUE` and `_RUN_KEY` are proposed constants.
The two case names are new as well. If this is taken, the L3 row's clause and Code grounds gain the new
unit and the two cases. Its Notes sentence becomes the one below (⬜ 4).

### ⬜ 4 — L3's Notes sentence

Taken together with the fix above:

```text
A job's `run:` is read as the commands the shell receives: a folded or plain scalar is one command however many lines it spans, and a literal block is one command per line with a backslash continuation joined, so an `--ignore` or `-k` on a continuation line removes what the first line named.
```

Without the fix, the sentence names both directions:

```text
A literal `run:` block whose pytest command is continued with a backslash is read line by line and does not count; a folded or plain multi-line `run:` is read the same way, so an `--ignore` or `-k` on its second line is not seen and the job is counted.
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round, at `806fad61` unless marked:

- `seal/specs/1790690762-arm-check-reads-every-supported-ast/rounds/round-1.md` and `round-1-report.md` (whole)
- `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md` (whole), and its diff over `deb6290f..806fad61`
- `seal/specs/1790690762-arm-check-reads-every-supported-ast/spec.md` (lines 180–195)
- `tests/test_arm_check.py` (lines 197–230, 233–380 through the diff), and the diff `deb6290f..54e31f21` over `tests/`, `.github/` and `CONTRIBUTING.md`
- `.github/workflows/test.yml` (whole)
- `tests/test_ci_gives_the_checks_what_they_need.py` (lines 1–95)
- `tests/conftest.py` (lines 60–175)
- `tests/test_a_workflow_is_read_the_one_way.py` (lines 1–60 and its case names)
- `skills/verify/scripts/arm_check.py` (lines 289–314)
- `skills/verify/scripts/broad_gate.py` (lines 1795–1815)
- `bin/test` (lines 1–40)
- `ruff.toml` (its selection lines)
