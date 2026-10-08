# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — review round 2

| Field | Value |
|---|---|
| Target SHA | d5642a077aad2050501071399990aaf8dedbd6ed |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 887 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | first — 🟡 1 at skills/evidence-check/scripts/evidence_check.py#unconditional, a unit round-1's fixes added; 🟡 2 at skills/evidence-check/scripts/evidence_check.py#never_fails, a unit round-1's fixes added |
| Needs a fix | yes — 🟡 1 (a keyword-conditional or strict `xfail` reads as one that cannot fail) and 🟡 2 (a mark on a test under an `if`, or a `pytestmark` extended by `+=`, is not read), both inside units round 1's fixes created |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Verifying round 2 of round 1's fixes: 144aaf1a..ecf51398 plus the table and the close at d5642a07. The job was the answers to round 1's five verdicts. The changed units named_unit, collected and held_by_tests and their callers were a finding surface. The spawn asked three things: whether an unconditional skip is detected in every spelling and a conditional one never mistaken for it; whether the supersede rule can hide a live test row; and whether the docs promise only what the checker reads. It also ran the eight guard modules once. Facts arrived labelled. Read: the orchestrator's direction for round 1's 🟡 2. Read from the smith: the supersede rule, the coordinate exclusion, 28 reds, 15 mutations and 1,304 passed. The round was stopped once by the orchestrator in error and resumed.

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

## Paste-ready fixes

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
```
A  Re-read only, released test gone: exit 2, BROKEN tests/test_held.py::test_holds
B  Corrected row holding only its citation (test row): exit 0, total 1 ok
B2 Corrected row holding only its citation (hashed row): exit 0, total 1 ok
C  unrelated live row naming the superseded row's test: exit 0, total 3 ok
C2 same, that test gone: exit 2, BROKEN tests/test_held.py::test_holds
C2' in-place --reverify: exit 1, LEFT tests/test_held.py::test_holds BROKEN
D  family of two rows naming one gone test: exit 2, two BROKEN lines
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1690` | round 1's 🔴 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2319` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2251` | round 1's 🟡 3 — fixed |
| round-1 | `skills/settle/scripts/fold_check.py:308` | round 1's ⬜ 4 — fixed |
| round-1 | `seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md:14` | round 1's ⬜ 5 — answered |
| round-1 | `seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md:15` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md` | round 1's 🟢 — confirmed |
| round-1 | the head | round 1's ❓ — out of verified scope |
| round-1 | PR #887 | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `Corrected ·` row whose Code grounds cell holds only its citation supersedes its released row and holds nothing itself, and `--strict` reads it clean, for hashed and test rows alike; from #715's family reader, not this branch | a candidate for a new issue against the family reader, for the orchestrator to place | the repository owner |
