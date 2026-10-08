# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — review round 1

| Field | Value |
|---|---|
| Target SHA | 9fda7dbaad5a0e89972e3ae4cb5e430590a5f36b |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 887 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `144aaf1a5aef0b7708542fc111ade47cfdc7c8d7..ecf51398379e1399cdd2867157e82b5e0c85f946`, 4 commits |
| Contract changes | named_unit → phase-1.md, node_finding, target_problem, pytest; collected → spec.md, phase-1.md, round-1-report.md, round-1.md, collected, conftest_is_loaded, runner_reached, node_finding; held_by_tests → round-1-report.md, round-1.md, check_ledger, reverify |
| New units | TEST_FILE_RE (depth 1); NEVER_FAILS (depth 1); NEVER_RUNS (depth 1); unconditional (depth 1); never_fails (depth 1); test_a_method_spelled_with_a_dot_is_named (depth 1); released_test_row (depth 1); test_a_released_test_row_re_pointed_by_a_correction_reads_clean (depth 1); test_reverify_leaves_a_superseded_test_row_unnamed (depth 1); test_a_corrections_own_gone_test_is_still_broken (depth 1); test_a_test_the_suite_does_not_collect_holds_nothing (depth 1); NEVER (depth 1); test_a_test_that_cannot_fail_holds_nothing (depth 1); test_a_conditional_mark_is_left_to_the_reader (depth 1); test_a_coordinate_quoting_a_scope_is_no_test (depth 1); test_a_pact_anchor_quoting_a_scope_is_no_test (depth 1) |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (a released test row cannot be re-pointed once its test is gone), 🟡 2 (`OK` for a test the suite never runs or that cannot fail), 🟡 3 (a no-node-id ledger fails on a coordinate quoting `::`) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the build at 9fda7dba, after the branch merged the release branch at ad447367, against origin/release/v0.21.0. The spawn named six things to attack. First, what 'pytest collects it by default' means without running pytest. Second, whether a test row can stop re-reading a claim no test pins. Third, the five Corrected test rows. Fourth, the integration re-stamps of the release branch's 33 drifted rows. Fifth, the fold-check resolver change against every Enforced by target in docs. Sixth, the vendored checker copy. Probes were to run in a scratch repository. It also ran the eight guard modules once. Facts arrived labelled. Read from the smith: the test-row grades, the resolver, the 38 released rows read, the 17 mutations and the integration. Executed by the orchestrator: 33 drifted at the release head ad447367.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A released test row whose test is renamed or removed stays BROKEN for good: `held_by_tests` reads superseded rows too, so the `Corrected ·` re-point the spec names does not clear it, and `--strict`, the broad gate, CI and the advisor stay red | `skills/evidence-check/scripts/evidence_check.py:1690` | **fixed** `c40b625e` | fixed at c40b625e; executed, probe 2: `--strict` exit 2 with the `Corrected ·` row in place; both `--reverify` forms exit 0 and name nothing |
| 🟡 2 | `collected` reads `OK` for a test pytest never collects (non-test file, conftest, class with `__init__`) or that can never fail (unconditional skip, xfail, module `pytestmark` skip) | `skills/evidence-check/scripts/evidence_check.py:2319` | **fixed** `c40b625e` | fixed at c40b625e; executed, probe 1 part A: seven node ids `OK`, exit 0; pytest's own collection skipped three of them |
| 🟡 3 | A hashed coordinate in a code span whose quoted locator holds `::` is read as a test: two `MALFORMED` findings on a ledger with no node id, `--strict` exit 2 | `skills/evidence-check/scripts/evidence_check.py:2251` | **fixed** `c40b625e` | fixed at c40b625e; executed, probe 1 part B: base `OK`, head two `MALFORMED`; breaks S11 |
| ⬜ 4 | `fold-check` accepts `path::A.b`, a dotted spelling of a method beside the documented `path::A::b` | `skills/settle/scripts/fold_check.py:308` | **fixed** `c40b625e` | fixed at c40b625e; executed, probe 1 part C: `named_unit` answers `('def',)` for `A.b`; no target uses it today |
| ⬜ 5 | Ledger lines 14 and 12 claim more than their named tests hold: the pact-anchor half of line 14 has no named test, and T12 names two of the cases it claims | `seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md:14` | answered | corrected at ecf51398; read; a correction to the run's paperwork, outside `Needs a fix` |
| 🟢 | The `fold-check` resolver change answers every `Enforced by:` target in `docs/` as before | `skills/settle/scripts/fold_check.py:308` | confirmed | executed, probe 1 part C: 451 of 451 targets alike |
| 🟢 | The `Corrected ·` test rows at ledger lines 15 to 18 each hold their claim as written | `seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md:15` | confirmed | read, each case body against its claim |
| 🟢 | The integration re-stamps hold against the merged text | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md` | confirmed | read: S8, K21, W9, G9, two warden rows; G14 by its guard; four warden rows carried from the overview |
| ❓ | The full suite, `evidence-check --strict .` and `fold-check` over the whole tree at the head | the head | ❓ out of verified scope | the broad gate; the sealer answers it after the rounds settle |
| ❓ | The pytest legs of PR #887 (macOS, Ubuntu, Windows shards) | PR #887 | ❓ out of verified scope | pending when read; lint, ledger, release and arm-check-grammar had passed. CI answers it |

## Paste-ready fixes

```python
# skills/evidence-check/scripts/evidence_check.py, in family_view, inside
#     for top, members in families.items():
#         if top in superseded:
#             continue
# and before the ANCHOR_RE loop over the members:
        for key in sorted(members, key=lambda k: (str(k[0]), k[1])):
            _, _, header, cells = row(key)
            if header is None:
                column = LEDGER_COLUMNS.index(CODE_GROUNDS)
            else:
                column = header.index(CODE_GROUNDS) if CODE_GROUNDS in header else -1
            if 0 <= column < len(cells):
                for token in node_tokens(cells[column]):
                    emit(key, node_finding(token, root, maps, default_repo))

# check_ledger: a family's rows are blanked in BODY and read above, so a
# superseded released row's tests are not read again, as its hashes are not.
    findings.extend(held_by_tests(body, root, maps, default_repo))

# reverify, in the per-ledger loop, in place of held_by_tests(text, ...):
        ident = file_identity(ledger)
        live = "".join(
            BLANK_RE.sub(" ", line) if (ident, n) in superseded else line
            for n, line in enumerate(gfm_lines(text, keepends=True), 1)
        )
        untested.extend(
            (coord, f"{status} — {why}")
            for status, coord, why in held_by_tests(live, root, maps, default_repo)
            if status != "OK"
        )
```
```python
# tests/test_a_ledger_row_is_held_by_its_test.py
def test_a_released_test_row_re_pointed_by_a_correction_reads_clean(repo):
    """A released row naming a test that was renamed is repaired by one
    `Corrected ·` row naming the new test; the released row is superseded,
    so its gone test is not read again. Red before the fix: BROKEN, exit 2."""
    (repo / "seal" / "releases").mkdir(parents=True)
    (repo / "seal" / "config.md").write_text(
        "# Repository config\n\n| Item | Value |\n|---|---|\n"
        "| Ledger frozen from | 1 |\n",
        encoding="utf-8",
    )
    section = "### 1000000001-the-first-item"
    row = f"| R1 · held | `{TESTS}::test_holds` | seen red | 2026-01-01 | |"
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.write_text(
        f"## 0.1.0 — 2026-01-01\n\n{section}\n\n{row}\n", encoding="utf-8"
    )
    tests = repo / TESTS
    tests.write_text(
        tests.read_text(encoding="utf-8").replace("def test_holds", "def test_renamed"),
        encoding="utf-8",
    )
    cite = (
        f'seal/releases/0.1.0.md#"{section}">"R1 · held"@{ec.content_hash([row])}'
    )
    fragment(
        repo,
        [
            f"| Corrected · held | `{cite}`, `{TESTS}::test_renamed` | seen red, "
            "then green | 2026-02-01 | Corrected 2026-02-01 by work item "
            "2000000001: re-pointed |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert findings(out.stdout) == [], out.stdout
```
```python
# skills/evidence-check/scripts/evidence_check.py
# pytest's default file pattern; a conftest is never collected from.
TEST_FILE_RE = re.compile(r"(?:test_[^/]*|[^/]*_test)\.py")
# Marks that leave the suite green whatever the code does. `skipif` is a
# condition and is left to the reader.
NEVER_FAILS = ("skip", "xfail")


def collected(names, kinds, path=""):
    """Whether pytest collects what NAMES name by default, from PATH: a file
    named test_*.py or *_test.py, a function named `test...` or a class named
    `Test...` with no `__init__`, at the top level or inside such classes."""
    if path and not TEST_FILE_RE.fullmatch(path.rsplit("/", 1)[-1]):
        return False
    for depth in range(1, len(names) + 1):
        outer = ".".join(names[:depth])
        if kinds.get(outer) == ("class",) and outer + ".__init__" in kinds:
            return False
    for depth in range(1, len(names)):
        if not names[depth - 1].startswith("Test") or kinds.get(
            ".".join(names[:depth])
        ) != ("class",):
            return False
    own, last = kinds.get(".".join(names), ()), names[-1]
    return (own == ("def",) and last.startswith("test")) or (
        own == ("class",) and last.startswith("Test")
    )


def never_fails(text, names):
    """Whether the module, or the unit or a class around it, carries an
    unconditional `pytest.mark.skip` or `pytest.mark.xfail`."""

    def marked(node):
        for dec in getattr(node, "decorator_list", []):
            target = dec.func if isinstance(dec, ast.Call) else dec
            if isinstance(target, ast.Attribute) and target.attr in NEVER_FAILS:
                return True
        return False

    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets
        ):
            value = node.value.func if isinstance(node.value, ast.Call) else node.value
            if isinstance(value, ast.Attribute) and value.attr in NEVER_FAILS:
                return True
    scope = tree.body
    for name in names:
        node = next(
            (n for n in scope if getattr(n, "name", None) == name), None
        )
        if node is None:
            return False
        if marked(node):
            return True
        scope = getattr(node, "body", [])
    return False


# node_finding, in place of the `collected` test at its end:
    if not collected(names, kinds, path):
        return ("MALFORMED", token, f"a {own[0]} {NOT_A_TEST}")
    if never_fails(body, names):
        return (
            "MALFORMED",
            token,
            "is marked to skip or to fail, so the suite stays green whatever "
            f"the code does — {TEST_FORM}; or write `path#anchor@hash`",
        )
    return ("OK", token, f"a {own[0]} pytest collects")
```
```python
# tests/test_a_ledger_row_is_held_by_its_test.py
@pytest.mark.parametrize(
    "rel, text, node",
    [
        ("tests/helpers.py", "def test_x():\n    assert True\n", "test_x"),
        ("tests/conftest.py", "def test_x():\n    assert True\n", "test_x"),
        (
            "tests/test_init.py",
            "class TestI:\n    def __init__(self):\n        pass\n\n"
            "    def test_x(self):\n        assert True\n",
            "TestI::test_x",
        ),
        (
            "tests/test_skip.py",
            "import pytest\n\n@pytest.mark.skip\ndef test_x():\n    assert False\n",
            "test_x",
        ),
        (
            "tests/test_xfail.py",
            "import pytest\n\n@pytest.mark.xfail\ndef test_x():\n    assert False\n",
            "test_x",
        ),
        (
            "tests/test_module.py",
            "import pytest\npytestmark = pytest.mark.skip\n\n"
            "def test_x():\n    assert False\n",
            "test_x",
        ),
    ],
)
def test_a_test_the_suite_never_runs_or_cannot_fail_holds_nothing(
    repo, script, rel, text, node
):
    (repo / rel).write_text(text, encoding="utf-8")
    fragment(repo, [held(f"`{rel}::{node}`")])
    out = run(["--strict", "."], repo, script)
    assert out.returncode == 2, out.stdout + out.stderr
    assert [f[0] for f in findings(out.stdout)] == ["MALFORMED"], out.stdout
```
```python
# skills/evidence-check/scripts/evidence_check.py
def node_tokens(cell):
    """Every code span of CELL that holds `::` and no coordinate: what a Code
    grounds cell names as a test, parsed or not, in cell order. A span
    holding a coordinate or a pact anchor is that coordinate, whatever its
    quoted locator says (a heading `## A::b`, a C++ scope)."""
    return [
        m.group(2).strip()
        for m in CODE_SPAN_RE.finditer(cell)
        if NODE_SEP in m.group(2)
        and not ANCHOR_RE.search(m.group(2))
        and not PACT_ANCHOR_RE.search(m.group(2))
    ]
```
```python
# tests/test_a_ledger_row_is_held_by_its_test.py
def test_a_coordinate_quoting_a_scope_is_no_test(repo, script):
    """S11 and D3: a coordinate is unambiguous by its shape, so `::` inside
    its quoted locator is no node id. Red before the fix: two MALFORMED."""
    doc = repo / "docs" / "guide.md"
    doc.parent.mkdir()
    doc.write_text("# Guide\n\n## The Foo::bar form\n\nText.\n", encoding="utf-8")
    fragment(repo, [held('`docs/guide.md#"## The Foo::bar form"@00000000`')])
    run(["--reverify", "."], repo, script)
    out = run(["--strict", "."], repo, script)
    assert out.returncode == 0, out.stdout + out.stderr
    assert findings(out.stdout) == [], out.stdout
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight guard modules the prompt named, in the clone | 437 passed, exit 0 |
| Probe 1 part A: seven node ids for units pytest does not collect or that cannot fail, `--strict` | all seven `OK`, exit 0; pytest `--co` collected four of the seven |
| Probe 1 part B: a ledger of hashed rows only, one quoting a heading with `::`, base checker then head checker | base `OK`; head two `MALFORMED`, exit 2 |
| Probe 1 part C: old `ast.walk` resolver against `named_unit` over every `Enforced by:` target in `docs/` | 451 of 451 alike; `A.b` resolves to `('def',)` |
| Probe 2: a released test row re-pointed by a `Corrected ·` row after its test was renamed | `--strict` BROKEN, exit 2; `--reverify --into` and in-place `--reverify` exit 0, silent |
| `gh pr checks 887` | lint, ledger, release, arm-check-grammar 3.13 and 3.14 pass; every pytest leg pending |
| This report, staged in the clone, under `evidence-check .` (lenient) and four guard modules (identifiers, line wrap, one word one meaning, records) | records arm 0 refused; ledger total 7813 ok, 0 drifted; 166 passed, exit 0 |
| The full suite (the broad gate) | not yet run, by anyone in this round |

```
1. released test row, test present: exit 0
total: 1 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed · 0 overflow
2. renamed, Corrected row re-points it: exit 2
  BROKEN   tests/test_svc.py::test_old  no def or class named test_old in tests/test_svc.py
total: 2 ok · 0 drifted · 1 broken · 0 external · 0 old-format · 0 malformed · 0 overflow
3. --reverify --into after that: exit 0
0 citing rows written · 0 released rows left
4. --reverify in place: exit 0
0 citing rows written · 0 released rows left
```
```
base --strict exit 2 | BROKEN src/widget.cpp#"Widget::render" locator not found / total: 1 ok · ... · 0 malformed
head --strict exit 2
  BROKEN   src/widget.cpp#"Widget::render"  locator not found
  MALFORMED src/widget.cpp#"Widget::render"@00000000  does not parse as a test — ...
  MALFORMED docs/guide.md#"## The Foo::bar form"@24db4556  does not parse as a test — ...
  MALFORMED `src/widget.cpp#"Widget::render"@00000000`  holds a test and a code coordinate, ...
  MALFORMED `docs/guide.md#"## The Foo::bar form"@24db4556`  holds a test and a code coordinate, ...
total: 1 ok · 0 drifted · 1 broken · 0 external · 0 old-format · 4 malformed · 0 overflow
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
