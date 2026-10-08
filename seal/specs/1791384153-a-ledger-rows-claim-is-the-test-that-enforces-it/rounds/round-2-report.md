# Round 2 report — 1791384153 (#836), draft PR #887

Target SHA `d5642a077aad2050501071399990aaf8dedbd6ed`. This is a verifying
round. Its target is the diff of round 1's fixes, `144aaf1a..ecf51398`
(c40b625e code, 0a4b68c9 pin, 6544ed58 docs, ecf51398 ledger), plus
ce3a762d and d5642a07, which are paperwork. I reviewed it in a
`git clone --no-local` of the worktree under this round's scratch
directory. The new units round 1's `New units` row names were judged as
code, not as fixes.

Carried, not re-derived: round 1's coordinates for the checker's family
reader and the test-row units. Everything below is re-derived at the
target SHA.

The smith's account was read and checked claim by claim. It holds where
it can be checked. 30 cases were red against the pre-fix checker (the
smith says 28; my count includes the extended resolver case and the
`fold-check` case), and all 120 cases of the two touched modules pass at
the head. The smith's full-suite count and `evidence-check --strict`
total were not re-run here; they belong to the broad gate.

## How the findings relate

Round 1's five findings are each closed. Two new defects sit inside units
round 1's fixes created, and both are about one question the spawn asked:
does the checker read an unconditional mark in every spelling, and never
mistake a conditional one for it?

1. 🟡 1. A conditional `xfail` written with a keyword is mistaken for an
   unconditional one. The row reads `MALFORMED` on a test that can fail,
   which the docs promise is left to the reader.
2. 🟡 2. An unconditional mark is missed where the test sits inside an
   `if` or a `try`, or where `pytestmark` is extended with `+=`. The test
   reads `OK` while pytest skips it.
3. ⬜ 3. One sentence of the docs promises a little more than the checker
   reads.

## 🟡 1 — an `xfail` given its condition by keyword reads as one that cannot fail

`unconditional` treats an `xfail` call as conditional only where it has a
positional argument (`skills/evidence-check/scripts/evidence_check.py:2387`,
`not (call and mark.args)`). pytest's signature is
`xfail(condition=None, *, reason=None, raises=None, run=True, strict=…)`,
so `@pytest.mark.xfail(condition=sys.platform == "win32", reason="…")` is
the same conditional mark spelled with a keyword. The checker calls it
`MALFORMED` and `--strict` exits 2.

`strict=True` goes the same way. A strict `xfail` fails the suite where
the test passes, so it does not leave the suite green whatever the code
does. This repository carries one at
`tests/test_the_recorder_writes_what_its_process_ran.py:1040`.

Executed, the marks probe: three spellings, each through `node_finding`
and through pytest itself.

- `@pytest.mark.xfail(condition=…)` reads `MALFORMED`. pytest ran it and
  it failed, exit 1.
- `pytestmark = pytest.mark.xfail(condition=…)` reads `MALFORMED`. pytest
  ran it and it failed, exit 1.
- `@pytest.mark.xfail(strict=True)` on a passing test reads `MALFORMED`.
  pytest failed it, exit 1.

`docs/the-evidence-ledger.md:251` says an `xfail` given a condition is
left to the reader. A repository that writes the condition as a keyword
cannot name that test in a row at all.

## 🟡 2 — a mark is missed where `unit_kinds` finds the test and `never_fails` does not

`never_fails` looks the test up among the direct children of the module
and class bodies (`evidence_check.py:2413`). `unit_kinds`, which
`collected` and `named_unit` read, also walks into `if`, `try` and `with`
bodies at the same qualified name. So a test defined under a module-level
`if` resolves, reads as a test, and has its own decorator skipped. The
`pytestmark` reader has the same blind spots: it reads only `=` and an
annotated `=` at the top of a body, so `pytestmark += [pytest.mark.skip]`
and a `pytestmark` under a class-level `if` are not read.

Executed, the marks probe: `@pytest.mark.skip` on a test under
`if sys:` reads `OK`, and pytest reported it skipped. A module whose
`pytestmark` is extended by `+=` reads `OK`, and pytest reported it
skipped.

`docs/the-evidence-ledger.md:249` promises that a test under an
unconditional mark "on itself, a class around it or its module" holds
nothing. These shapes are rare. They are inside that promise, though,
and each one is an `OK` for a claim nothing holds, which is round 1's
🟡 2 again in a spelling it did not name.

The fix belongs in the lookup and not in a list of shapes. `never_fails`
should find the node by the same walk `unit_kinds` uses, so the two
readers cannot disagree about where a test is.

## ⬜ 3 — one sentence promises a test that "can fail", and gives the suite a question it never answers

`docs/the-evidence-ledger.md:256-257` says a test row is `OK` where each
test "reads as a test and can fail". The checker reads only that the test
carries no unconditional `skip` or `xfail` mark. A test whose body is
`assert True` reads `OK`, so "can fail" is more than the checker reads.
The next sentence qualifies it, which is why this is ⬜.

Lines 262-264 and `skills/evidence-check/SKILL.md:291` say whether pytest
collects the test is "the suite's answer". A test pytest never collects
does not turn the suite red, so nothing answers that question. That is
the orchestrator's directed wording, and the caller may keep it. A wording
that states the consequence would be: "`OK` says what reading the file can
tell and no more. Nothing here notices a test pytest does not collect
under the repository's own configuration, and whether a collected test
passes is the suite's answer." Changing it means updating
`test_the_documents_state_the_test_row`, which pins the current sentence.

## Round 1's findings

- **🔴 1 is closed.** `check_ledger` now passes the family-owned lines as
  unread, and `family_view` reads a member's tests only for a family that
  is not superseded. `reverify` passes `left_alone`'s superseded members.
  Executed: the case for the round 1 reproduction was red against the
  pre-fix checker and is green now. The supersede probe also showed what
  the rule does not hide. A live row outside the family that names the
  same test is still read: `BROKEN`, exit 2, and named on a `LEFT` line by
  `--reverify` once that test is gone. A family that is only re-read, not
  corrected, still reads its released row's gone test `BROKEN`, exit 2.
- **🟡 2 is closed for every shape it named.** The three collection shapes
  and the unconditional marks are `MALFORMED`. Executed, the marks probe:
  `@pytest.mark.skip`, `@mark.skip` after `from pytest import mark`,
  `@pt.mark.skip` after `import pytest as pt`, `skip(reason=…)`,
  `skip("…")`, `pytestmark = [pytest.mark.skip]`, the annotated
  `pytestmark`, bare `xfail`, `xfail(reason=…)` and `unittest.skip` each
  read `MALFORMED`, and pytest skipped or xfailed each one. A positional
  `skipif`, a `skipif(condition=…)` and a positional `xfail` each read
  `OK`, and pytest ran each one and failed it. 🟡 1 and 🟡 2 above are the
  two shapes that still go wrong.
- **🟡 3 is closed.** `node_tokens` drops a span that `ANCHOR_RE` or
  `PACT_ANCHOR_RE` matches. Both new cases were red before the fix and are
  green now.
- **⬜ 4 is closed.** `named_unit` answers `()` for a dotted part. The
  `fold-check` case was red before the fix.
- **⬜ 5 is closed.** Read: line 18 of this item's ledger fragment now
  names the pact-anchor test, and T12 names twelve cases.

## The supersede rule, and a hole it inherits

The spawn asked whether the supersede rule can hide a live test row. It
hides what it should: the released row and its re-reads. Nothing outside
the family is hidden. One shape is worth naming, and it is older than this
branch. A `Corrected ·` row whose Code grounds cell holds only its
citation supersedes the released row and holds nothing itself, and
`--strict` reads it clean, exit 0. The supersede probe showed the same
result for a hashed released row, so this comes from #715's family reader
and not from #836. It is in the Deferred table below.

## Checked and outside the promise

A module-level call such as pytest.skip("…", allow_module_level=True) is
not a mark, and it still reads `OK` while pytest skips the module. The
docs promise marks, so this is outside the promise as written. The spawn's
direction lists "module" without saying whether a call counts, so this is
a ❓ for the caller. The ini option xfail\_strict makes a bare `xfail` one
that can fail too. That is configuration, which the direction leaves to
the suite.

## Regression tests to plant

- `tests/test_a_ledger_row_is_held_by_its_test.py`: an `xfail` given its
  condition by keyword, a module `pytestmark` with `condition=`, and a
  strict `xfail` each read clean (🟡 1); a skip on a test under a module
  `if`, a `pytestmark` extended by `+=`, and a class `pytestmark` under an
  `if` each read `MALFORMED` (🟡 2). Both are in the fenced fixes below.
  Executed: in the scratch clone, the six new cases were red against the
  head checker (6 failed, exit 1). With the fix below applied, all 126
  cases of the two touched modules passed, exit 0. The marks probe then
  read every keyword-conditional and strict `xfail` as `OK`, and the
  `if` shape and `+=` shape as `MALFORMED`. The clone was restored to the
  target SHA afterwards.

## Facts for the evidence ledger

- `unconditional` reads an `xfail`'s condition only positionally, until
  🟡 1 is closed.
- `never_fails` and `unit_kinds` find a test by two different walks,
  until 🟡 2 is closed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | An `xfail` given its condition as `condition=`, or made `strict=True`, reads as one that cannot fail: `MALFORMED`, `--strict` exit 2, on a test pytest runs and fails | `skills/evidence-check/scripts/evidence_check.py:2387` | open | executed, marks probe: three spellings `MALFORMED`, each run and failed by pytest; docs line 251 leaves a conditional `xfail` to the reader |
| 🟡 2 | `never_fails` finds the test only among direct children, while `unit_kinds` walks into `if`/`try`/`with`; a skip on a test under a module `if`, and a `pytestmark` extended by `+=`, read `OK` | `skills/evidence-check/scripts/evidence_check.py:2413` | open | executed, marks probe: both `OK`, both skipped by pytest; inside the promise at docs line 249 |
| ⬜ 3 | The docs say an `OK` test "can fail" and that the suite answers whether pytest collects it; the checker reads neither, and nothing answers the second | `docs/the-evidence-ledger.md:256` | open | read; the behaviour is right and the sentence over-promises; the second half is the orchestrator's directed wording |
| 🟢 | round 1's blocking finding 1 is closed — a released test row re-pointed by a `Corrected ·` row reads clean, and in-place `--reverify` no longer names it | `skills/evidence-check/scripts/evidence_check.py:1692` | confirmed | executed: its two cases red before c40b625e and green at the head; supersede probe: a live row outside the family is still read, a re-read-only family still `BROKEN` |
| 🟢 | round 1's finding 2 is closed for every shape it named — non-test file, conftest, class with `__init__`, unconditional skip and xfail on the test, class or module | `skills/evidence-check/scripts/evidence_check.py:2343` | confirmed | executed: 22 parametrised cases red before c40b625e and green at the head; marks probe over ten spellings |
| 🟢 | round 1's finding 3 is closed — a code span holding a coordinate or a pact anchor is no test | `skills/evidence-check/scripts/evidence_check.py:2262` | confirmed | executed: both cases red before c40b625e and green at the head |
| 🟢 | round 1's finding 4 is closed — `fold-check` refuses a dotted `path::A.b` | `skills/evidence-check/scripts/evidence_check.py:2322` | confirmed | executed: the `fold-check` case and the resolver case red before c40b625e and green at the head |
| 🟢 | round 1's finding 5 is closed — the two ledger rows name what they claim | `seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md:18` | confirmed | read at ecf51398: the pact-anchor test named; T12 names twelve cases |
| ❓ | A module-level skip call (not a mark) still reads `OK`; whether the direction's "module" covers a call | `skills/evidence-check/scripts/evidence_check.py:2390` | ❓ out of verified scope | executed, marks probe: `OK`, pytest skipped the module; the docs promise marks only. The orchestrator answers whether it is in scope |
| ❓ | The full suite, `evidence-check --strict .` and `fold-check` over the whole tree at the head | the head | ❓ out of verified scope | the broad gate; the sealer answers it after the rounds settle |
| ❓ | The pytest legs of PR #887 (macOS, Ubuntu, Windows shards) | PR #887 | ❓ out of verified scope | pending when read; lint, ledger, release and both arm-check-grammar legs had passed. CI answers it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight guard modules the prompt named, in the clone at the head | 437 passed, exit 0 |
| The two touched modules (`tests/test_a_ledger_row_is_held_by_its_test.py`, `tests/test_a_folded_statement_names_what_enforces_it.py`) at the head, then with the checker of 9fda7dba | head 120 passed, exit 0; pre-fix 30 failed, 90 passed, exit 1 |
| Marks probe: twenty spellings, each through `node_finding` and through pytest | see the block below |
| Supersede probe: five ledgers, `--strict` and in-place `--reverify` | see the block below |
| The proposed fixes, in the clone: six new cases on the head checker, then the two modules and the marks probe with the fix applied; clone restored after | head checker 6 failed, exit 1; fixed 126 passed, exit 0 |
| `gh pr checks 887` | lint, ledger, release, arm-check-grammar 3.13 and 3.14 pass; every pytest leg pending |
| The full suite (the broad gate) | not yet run, by anyone in this round |

### Marks probe

```
pytest_mark_skip                 checker=MALFORMED pytest_exit=0 1 skipped
from_pytest_import_mark          checker=MALFORMED pytest_exit=0 1 skipped
import_pytest_as_pt              checker=MALFORMED pytest_exit=0 1 skipped
skip_reason_kw                   checker=MALFORMED pytest_exit=0 1 skipped
skip_reason_positional           checker=MALFORMED pytest_exit=0 1 skipped
pytestmark_list                  checker=MALFORMED pytest_exit=0 1 skipped
pytestmark_tuple                 checker=MALFORMED pytest_exit=2 1 error
pytestmark_annotated             checker=MALFORMED pytest_exit=0 1 skipped
pytestmark_augmented             checker=OK        pytest_exit=0 1 skipped
xfail_bare                       checker=MALFORMED pytest_exit=0 1 xfailed
xfail_reason_kw                  checker=MALFORMED pytest_exit=0 1 xfailed
unittest_skip                    checker=MALFORMED pytest_exit=0 1 skipped
module_level_skip_call           checker=OK        pytest_exit=5 1 skipped
skip_under_module_if             checker=OK        pytest_exit=0 1 skipped
skipif_positional                checker=OK        pytest_exit=1 1 failed
skipif_condition_kw              checker=OK        pytest_exit=1 1 failed
xfail_positional                 checker=OK        pytest_exit=1 1 failed
xfail_condition_kw               checker=MALFORMED pytest_exit=1 1 failed
pytestmark_xfail_condition_kw    checker=MALFORMED pytest_exit=1 1 failed
xfail_strict                     checker=MALFORMED pytest_exit=1 1 failed
```

### Supersede probe

```
A  Re-read only, released test gone: exit 2, BROKEN tests/test_held.py::test_holds
B  Corrected row holding only its citation (test row): exit 0, total 1 ok
B2 Corrected row holding only its citation (hashed row): exit 0, total 1 ok
C  unrelated live row naming the superseded row's test: exit 0, total 3 ok
C2 same, that test gone: exit 2, BROKEN tests/test_held.py::test_holds
C2' in-place --reverify: exit 1, LEFT tests/test_held.py::test_holds BROKEN
D  family of two rows naming one gone test: exit 2, two BROKEN lines
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `Corrected ·` row whose Code grounds cell holds only its citation supersedes its released row and holds nothing itself, and `--strict` reads it clean, for hashed and test rows alike; from #715's family reader, not this branch | a candidate for a new issue against the family reader, for the orchestrator to place | the repository owner |

## Paste-ready fixes

### 🟡 1 and 🟡 2 — one condition rule, one walk

```python
# skills/evidence-check/scripts/evidence_check.py — `unconditional`, in place
# of its last two statements:
    if name == "skip":
        return True
    if name != "xfail":
        return False
    # A condition, positional or `condition=`, runs the test where it is
    # false; a `strict=` xfail fails where the test passes; `**options` may
    # carry either. Each is left to the reader (round 2, 🟡 1).
    return not call or not (
        mark.args
        or any(k.arg in (None, "condition", "strict") for k in mark.keywords)
    )


# What one level of a module or class body defines, as `unit_kinds` reads it:
# the statements an `if`, `try`, `with` or loop holds sit at the same level.
LEVEL_NODES = (
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Assign,
    ast.AnnAssign,
    ast.AugAssign,
)


def level(node):
    """The definitions and assignments one level of NODE holds, through the
    compound statements `unit_kinds` walks into without a new name."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, LEVEL_NODES):
            yield child
        elif not isinstance(child, ast.expr):
            yield from level(child)


def never_fails(text, names):
    """Whether the test NAMES name in the Python TEXT, a class around it, or
    its module carries an unconditional skip or xfail mark (round 1, 🟡 2):
    as a decorator, or in a `pytestmark` assigned or extended in the module
    or the class. The test is found where `unit_kinds` finds it (round 2,
    🟡 2)."""

    def marked(node):
        for child in level(node):
            if isinstance(child, ast.Assign):
                targets = child.targets
            elif isinstance(child, (ast.AnnAssign, ast.AugAssign)):
                targets = [child.target]
            else:
                continue
            if any(isinstance(t, ast.Name) and t.id == "pytestmark" for t in targets):
                if child.value is not None and unconditional(child.value):
                    return True
        return False

    node = ast.parse(text)
    if marked(node):
        return True
    for name in names:
        node = next(
            (n for n in level(node) if getattr(n, "name", None) == name), None
        )
        if node is None:
            return False
        if any(unconditional(d) for d in node.decorator_list):
            return True
        if isinstance(node, ast.ClassDef) and marked(node):
            return True
    return False
```

```python
# tests/test_a_ledger_row_is_held_by_its_test.py, after
# test_a_conditional_mark_is_left_to_the_reader:
@pytest.mark.parametrize(
    "text",
    [
        "import sys\nimport pytest\n\n@pytest.mark.xfail(condition=sys.platform "
        "== 'x', reason='x')\ndef test_x():\n    assert True\n",
        "import sys\nimport pytest\npytestmark = pytest.mark.xfail(condition="
        "sys.platform == 'x', reason='x')\n\ndef test_x():\n    assert True\n",
        "import pytest\n\n@pytest.mark.xfail(strict=True)\ndef test_x():\n"
        "    assert True\n",
    ],
    ids=["xfail with condition=", "module pytestmark with condition=", "strict xfail"],
)
def test_an_xfail_that_can_fail_is_left_to_the_reader(repo, text):
    """Round 2, 🟡 1: an `xfail` given its condition by keyword runs where
    the condition is false, and a strict one fails where the test passes.
    Red before the fix: MALFORMED, exit 2."""
    (repo / "tests" / "test_maybe.py").write_text(text, encoding="utf-8")
    fragment(repo, [held("`tests/test_maybe.py::test_x`")])
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert findings(out.stdout) == [], out.stdout


@pytest.mark.parametrize(
    "text, node",
    [
        (
            "import sys\nimport pytest\n\nif sys:\n    @pytest.mark.skip\n"
            "    def test_x():\n        assert False\n",
            "test_x",
        ),
        (
            "import pytest\npytestmark = []\npytestmark += [pytest.mark.skip]\n\n"
            "def test_x():\n    assert False\n",
            "test_x",
        ),
        (
            "import sys\nimport pytest\n\nclass TestS:\n    if sys:\n"
            "        pytestmark = pytest.mark.skip\n\n"
            "    def test_x(self):\n        assert False\n",
            "TestS::test_x",
        ),
    ],
    ids=["under a module if", "pytestmark extended", "class pytestmark under an if"],
)
def test_a_mark_is_read_where_the_test_is_found(repo, text, node):
    """Round 2, 🟡 2: `unit_kinds` finds a test inside an `if`, so the mark
    on it is read there too. Red before the fix: OK, exit 0."""
    (repo / "tests" / "test_never.py").write_text(text, encoding="utf-8")
    fragment(repo, [held(f"`tests/test_never.py::{node}`")])
    out = run(["--strict", "."], repo)
    assert out.returncode == 2, out.stdout + out.stderr
    ((status, coord, detail),) = findings(out.stdout)
    assert (status, coord) == ("MALFORMED", f"tests/test_never.py::{node}")
    assert detail.startswith(NEVER), detail
```

Needs a fix: yes — 🟡 1 (a keyword-conditional or strict `xfail` reads
as one that cannot fail) and 🟡 2 (a mark on a test under an `if`, or a
`pytestmark` extended by `+=`, is not read), both inside units round 1's
fixes created
Loses a record or crashes: no

The broad gate has not come due: this round leaves 🟡 1 and 🟡 2 open, so
the sealer's spawn waits for their fix and the round that checks it.

## Proof block

Files opened in this round, in the clone at `d5642a07` unless named:
`seal/specs/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it/rounds/`
`round-1.md`, `round-1-fixes.md`, `round-1-report.md`; the diff
`144aaf1a..ecf51398` of `skills/evidence-check/scripts/evidence_check.py`,
`docs/the-evidence-ledger.md`, `skills/evidence-check/SKILL.md`,
`templates/ledger.md`, `tests/test_a_ledger_row_is_held_by_its_test.py`,
`tests/test_a_folded_statement_names_what_enforces_it.py` and
`seal/ledger/` (grep only); in `evidence_check.py`: `ANCHOR_RE`,
`PACT_ANCHOR_RE`, `OLD_COORD_RE`, `check_ledger`, `ledger_table_rows`,
`grounds_cells`, `malformed_rows`, `node_tokens`, `unit_kinds`,
`named_unit`, `collected`, `unconditional`, `never_fails`, `node_finding`,
`held_by_tests`, `cell_index`, `family_view`, `left_alone`, the
`reverify` loop, `place`; `tests/test_a_ledger_row_is_held_by_its_test.py`
lines 1-140; `bin/test`; `.github/scripts/run_tests.py` (its venv lines);
`tests/test_the_recorder_writes_what_its_process_ran.py:1040` (grep).
