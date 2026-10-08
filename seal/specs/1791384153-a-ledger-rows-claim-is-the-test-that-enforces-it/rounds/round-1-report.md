# Round 1 report — 1791384153 (#836), draft PR #887

Target SHA `9fda7dbaad5a0e89972e3ae4cb5e430590a5f36b`, reviewed as the diff
`ad447367...9fda7dba` in a `git clone --no-local` of the worktree under the
round's scratch directory. No earlier rounds exist, so nothing was carried
from a round record. The smith's account (the spawn prompt's facts,
`overview.md`, the phase files) was read in full and checked claim by claim
against the code; where it held, the verdict table says so with my own
grounds.

## How the findings relate

The new row form promises one thing: an `OK` test row means the suite holds
the claim, and nobody has to re-read it. Three findings break that promise
from three sides, and two are paperwork.

1. 🔴 1 — a released test row whose test goes away can never be cleared. The
   documented repair does not reach the checker's test reader.
2. 🟡 2 — the checker calls `OK` a test the suite never runs, or one that
   cannot fail, so `OK` can stand for a claim nothing holds.
3. 🟡 3 — a ledger with no test row in it at all can now fail, because a
   hashed coordinate that quotes `::` is read as a test.
4. ⬜ 4, ⬜ 5 — a second spelling `fold-check` now accepts, and two of this
   item's own rows that claim more than the tests they name.

## 🔴 1 — a released test row whose test is gone stays BROKEN for good

`check_ledger` reads test tokens over the raw ledger text, every row,
superseded or not (`skills/evidence-check/scripts/evidence_check.py:1690`,
`held_by_tests(text, …)`). A hashed released row stops being checked once a
`Corrected ·` row supersedes its family, because `family_view` owns those
lines and `check_ledger` blanks them. Test tokens skip that path entirely.

So the repair `spec.md` §*What drifting means* names for a BROKEN test row,
"a `Corrected ·` row re-points", does not work. Under `Ledger frozen from`
the released file cannot be edited, and the superseding row changes nothing
the checker reads. `--strict` exits 2 on every later run, and so do the
broad gate, the CI `ledger` job and the commit advisor.

This bites at the first rename after 0.21.0 ships. This item's own rows T1
to T13 and its five `Corrected ·` rows become released rows at the fold, and
each names a test somebody will rename one day.

Executed, probe 2 in the round's scratch directory: a frozen repository with
one released test row naming `tests/test_svc.py::test_old`, the function
renamed to `test_new`, and a fragment `Corrected ·` row citing the released
row and naming `::test_new`. `--strict` printed `BROKEN tests/test_svc.py::test_old`
and exited 2. `--reverify --into` and in-place `--reverify` each exited 0
and printed nothing about it, so no tool even names the row.

The fix belongs at the family reader, not in a special case. A family's
member rows are read in `family_view`, and only for a family that is not
superseded; `check_ledger` then reads test tokens over `body`, where those
lines are already blanked. `reverify` needs the same skip for its `LEFT`
lines (`evidence_check.py:3779`).

## 🟡 2 — `OK` for a test the suite never runs or that cannot fail

`collected` (`evidence_check.py:2319`) checks names only. The new section of
`docs/the-evidence-ledger.md` and `spec.md` D2 both say a test row is `OK`
where its test is "one unit pytest collects by default". Executed, probe 1
part A: seven node ids all read `OK`, exit 0 under `--strict`, and pytest's
own `--co` over the same tree disagreed on three of them.

- **Not collected at all.** A `def test_x` in `tests/helpers.py` and one in
  `tests/conftest.py`: pytest's default file pattern is test_*.py or
  *_test.py, and it never collects tests from a conftest. A
  `class TestInit` with an `__init__`: pytest refuses it with a
  `PytestCollectionWarning`. The checker said `OK` for all three.
- **Collected, but can never fail.** A function under
  `@pytest.mark.skip`, one under `@pytest.mark.xfail`, and a module whose
  `pytestmark = pytest.mark.skip`. The suite stays green whatever the code
  does, so the row's claim, "the test passing", is held by nothing. A
  conditional `skipif` is legitimate (this repository has three modules
  with a module-level one), so only the unconditional marks are the defect.

The first group contradicts the checker's own stated rule. The second is a
limit the rule never states. Both let a test row stop every re-read of a
claim no test holds, which is the exact failure the row form exists to end.

## 🟡 3 — a ledger with no test row fails once a coordinate quotes `::`

`node_tokens` (`evidence_check.py:2251`) takes every code span holding `::`.
A hashed coordinate is normally written in a code span, and a quoted locator
may hold `::`: a heading like `## The Foo::bar form`, a minor anchor quoting
an `Enforced by:` line (which now carries `path::name` in this very
repository), or a C++, Rust, PHP or Ruby scope in a consuming repository.

Executed, probe 1 part B: a ledger whose only rows were hashed coordinates,
one of them `docs/guide.md#"## The Foo::bar form"@<hash>`, stamped by the
base checker at `ad447367`. The base read it `OK`. The head read the same
row as two `MALFORMED` findings, "does not parse as a test" and "holds a test
and a code coordinate", and `--strict` exited 2.

That is S11's promise broken: "a ledger with no node id is unchanged".
It is also the reason D3 gives for reading code spans only, turned around: a
coordinate is unambiguous by its shape, so a span that holds one is a
coordinate and not a test. This repository's ledgers carry no such row today
(the spec's count), so the cost lands first on a consuming repository that
updates its vendored copy, and here at the first row quoting an
`Enforced by:` line by minor anchor.

## ⬜ 4 — `fold-check` now accepts a dotted target pytest never writes

`target_problem` hands the name to `named_unit` split on `::`, and
`named_unit` joins the parts with `.` (`skills/settle/scripts/fold_check.py:308`).
So `path::A.b` resolves to the method `b` of `A`, a second spelling beside
the documented `path::A::b`. Executed, probe 1 part C: `named_unit` answered
`('def',)` for `A.b`. No target in `docs/` uses it today, so nothing ships
wrong; the grammar is wider than the sentence that states it. The ledger side
does not have this, because `NODE_ID_RE` admits identifiers only.

## ⬜ 5 — two of this item's test rows claim more than the tests they name

Both sit in `seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md`,
so each is a correction and outside `Needs a fix`.

- **Line 14, `Corrected ·` on the `MALFORMED` claim.** The claim includes
  "a coordinate none of `ANCHOR_RE`, `OLD_COORD_RE` and `PACT_ANCHOR_RE`
  parses". None of the eight node ids exercises a pact anchor; the test that
  does is
  `tests/test_a_pact_anchor_is_no_coordinate_of_the_signer.py::test_a_pact_anchor_beside_the_local_coordinate_is_not_malformed`.
  Q3's own rule says a row whose tests hold only part of the claim takes the
  `Re-read ·` row. Adding that node id makes the row whole.
- **Line 12, T12.** The claim is that the vendored copy reads T1 to T5 as
  the plugin's does, and the row names only the T1 and T5 cases. Every case
  from T1 to T5 takes the `script` fixture, so the claim is true today, but
  removing the fixture from a T2 to T4 case leaves this row `OK`. Naming
  those cases, or narrowing the claim to the two named, closes it.

## What was checked and holds

- **The resolver change, against every `Enforced by:` target.** Executed,
  probe 1 part C: 473 targets in `docs/` at the head, 451 with `::name`;
  the old `ast.walk` resolver and `named_unit` answered alike on all 451.
- **The other three `Corrected ·` test rows (lines 15 to 18 less line 14).**
  Read: line 15's case asserts the `LEFT` line, the unchanged ledger and exit
  1, which is the narrowed claim; line 16's case reads both `SKILL.md`
  places against `exit_code` and the `DRIFTED` row; line 17's three cases
  hold the one view, `--into` in the advisor's line and the correction's
  coordinates in `FROZEN_REPAIR`; line 18's case pins the four places. Each
  holds its claim as written.
- **The integration re-stamps.** Read against the merged text: S8 (one
  `| Item | Value |` table in `templates/config.md`, first row the commit and
  pull request language), K21 (`mode_refusal` named with the same reason as
  `with_row`), W9 (`read_record` named as a tool's output), G9
  (`heading_starts` splits with `gfm_lines`, ends kept, levels from
  `heading_level`), and two of the six `agents/warden.md` rows (the blank
  line under the terminal pair, and the three tables with the two lines).
  G14 is held by its guard, which passed in the run below. The remaining
  four warden rows were carried from the overview's reading, not re-derived.
- **The vendored copy.** Read: there is no tracked vendored copy; S12 is the
  `script` fixture copying the file alone into a `tools/` directory, and every
  S1 to S5 case runs over both.
- **The eight guard modules.** Executed once: 437 passed, exit 0.

## Regression tests to plant

- `tests/test_a_ledger_row_is_held_by_its_test.py`: a released test row
  whose test is renamed, re-pointed by a `Corrected ·` row, reads clean
  under `--strict` (🔴 1); a node id in a non-test file, in a conftest, on a
  class with `__init__`, and on an unconditional skip or xfail is
  `MALFORMED` (🟡 2); a hashed coordinate quoting `::` in a code span reads
  as it did before this work (🟡 3). Each is in the fenced fixes below.

## Facts for the evidence ledger

- `held_by_tests` is called over raw text in `check_ledger` and `reverify`,
  so superseding does not reach a test row (🔴 1), until fixed.
- pytest's default collection also depends on the file name and on a class
  having no `__init__`; the checker's `collected` reads neither (🟡 2).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A released test row whose test is renamed or removed stays BROKEN for good: `held_by_tests` reads superseded rows too, so the `Corrected ·` re-point the spec names does not clear it, and `--strict`, the broad gate, CI and the advisor stay red | `skills/evidence-check/scripts/evidence_check.py:1690` | open | executed, probe 2: `--strict` exit 2 with the `Corrected ·` row in place; both `--reverify` forms exit 0 and name nothing |
| 🟡 2 | `collected` reads `OK` for a test pytest never collects (non-test file, conftest, class with `__init__`) or that can never fail (unconditional skip, xfail, module `pytestmark` skip) | `skills/evidence-check/scripts/evidence_check.py:2319` | open | executed, probe 1 part A: seven node ids `OK`, exit 0; pytest's own collection skipped three of them |
| 🟡 3 | A hashed coordinate in a code span whose quoted locator holds `::` is read as a test: two `MALFORMED` findings on a ledger with no node id, `--strict` exit 2 | `skills/evidence-check/scripts/evidence_check.py:2251` | open | executed, probe 1 part B: base `OK`, head two `MALFORMED`; breaks S11 |
| ⬜ 4 | `fold-check` accepts `path::A.b`, a dotted spelling of a method beside the documented `path::A::b` | `skills/settle/scripts/fold_check.py:308` | open | executed, probe 1 part C: `named_unit` answers `('def',)` for `A.b`; no target uses it today |
| ⬜ 5 | Ledger lines 14 and 12 claim more than their named tests hold: the pact-anchor half of line 14 has no named test, and T12 names two of the cases it claims | `seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md:14` | open | read; a correction to the run's paperwork, outside `Needs a fix` |
| 🟢 | The `fold-check` resolver change answers every `Enforced by:` target in `docs/` as before | `skills/settle/scripts/fold_check.py:308` | confirmed | executed, probe 1 part C: 451 of 451 targets alike |
| 🟢 | The `Corrected ·` test rows at ledger lines 15 to 18 each hold their claim as written | `seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md:15` | confirmed | read, each case body against its claim |
| 🟢 | The integration re-stamps hold against the merged text | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md` | confirmed | read: S8, K21, W9, G9, two warden rows; G14 by its guard; four warden rows carried from the overview |
| ❓ | The full suite, `evidence-check --strict .` and `fold-check` over the whole tree at the head | the head | ❓ out of verified scope | the broad gate; the sealer answers it after the rounds settle |
| ❓ | The pytest legs of PR #887 (macOS, Ubuntu, Windows shards) | PR #887 | ❓ out of verified scope | pending when read; lint, ledger, release and arm-check-grammar had passed. CI answers it |

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

### Probe 2

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

### Probe 1 part B

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

The C++ row was BROKEN under both checkers because the probe's quoted locator
did not match its text; the Markdown row is the clean comparison.

## Paste-ready fixes

### 🔴 1 — read a family's test tokens where its superseding is known

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

### 🟡 2 — a test is collected by its file and its class too, and can fail

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

### 🟡 3 — a span that holds a coordinate is a coordinate, not a test

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

Needs a fix: yes — 🔴 1 (a released test row cannot be re-pointed once its
test is gone), 🟡 2 (`OK` for a test the suite never runs or that cannot
fail), 🟡 3 (a no-node-id ledger fails on a coordinate quoting `::`)
Loses a record or crashes: no

The broad gate has not come due: this round leaves 🔴 1, 🟡 2 and 🟡 3
open, so the sealer's spawn waits for the fix round and the verifying round
after it.

## Proof block

Files opened in this round, at `9fda7dba` in the clone unless named:
`seal/specs/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it/`
`spec.md`, `overview.md`, `questions.md`, `survivors.md`, `changelog.md`;
`seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md`;
the diff of `seal/ledger/1791384154-…`, `1791384156-…`, `1791384158-…` and
`1791384160-…`; `skills/evidence-check/scripts/evidence_check.py` (the diff,
`ANCHOR_RE`, `resolve_unit`, `grounds_cells`, `malformed_rows`,
`citing_verb`, `check_ledger`, `family_view`, `ledger_families`,
`left_alone`, the `reverify` loop); `skills/settle/scripts/fold_check.py`
(the diff, `target_problem`); `hooks/evidence-advisor.py` (the diff);
`docs/the-evidence-ledger.md`, `templates/ledger.md`,
`skills/evidence-check/SKILL.md`, `skills/evidence-ci/SKILL.md` (the diffs);
`tests/test_a_ledger_row_is_held_by_its_test.py` (head and the test list);
the named cases in `tests/test_a_row_points_by_content.py`,
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`,
`tests/test_a_released_row_is_read_again_in_a_fragment.py` and
`tests/test_a_pact_anchor_is_no_coordinate_of_the_signer.py`;
`seal/releases/0.5.0.md` (S8), `0.15.4.md`, `0.15.5.md`, `0.16.0.md` (G14,
G9), `0.18.0.md`, `0.18.3.md`, `0.20.0.md` (W9);
`templates/config.md` (headings and tables);
`skills/verify/scripts/payload_meter.py` (`heading_starts`);
`tests/test_every_reader_ends_a_line_where_gfm_does.py` (`OUT_OF_CLASS`
entries); `bin/test`; `.github/scripts/run_tests.py` (its venv lines).
