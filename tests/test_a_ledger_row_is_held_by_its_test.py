"""A ledger row may name the test that holds its claim, instead of a hash (#836).

A hashed row records what a unit held when somebody read it, so every edit to
the unit owes a re-read, and most rows written since 0.18.0 were that
bookkeeping. A row whose Code grounds cell names a test in pytest's own
spelling -- `tests/test_x.py::test_y`, or `tests/test_x.py::TestA::test_b`
for a method -- has no hash and never drifts: `evidence-check` reads that the
test is there, and the suite reads that it passes.

  S1   a test row resolves, and counts among `ok`
  S2   a renamed test breaks the row, naming the file and the name
  S3   a method is spelled pytest's way, and the bare spelling is named
  S4   a unit pytest does not collect is no test
  S5   a row is one form or the other; a citing row's citation is not code
  S6   a node id outside the Code grounds cell is prose
  S8   `--reverify` writes nothing on a test row, and names a broken one
  S11  a ledger with no node id reads as it always did
  S12  the copy `evidence-ci` vendors alone reads S1-S5 the same way

`docs/the-evidence-ledger.md` §*A claim held by a test* is the rule, and
`seal/specs/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it/
spec.md` holds the decisions. No fixture here runs git.
"""

import importlib.util
import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")


def load():
    spec = importlib.util.spec_from_file_location("specseal_evidence_held", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ec = load()

SERVICE = "def handler(x):\n    return x + 1\n"
# The tests a fixture row may name, and the units that are not tests.
HELD = (
    "def test_holds():\n    assert True\n\n\n"
    "class TestA:\n    def test_b(self):\n        assert True\n\n\n"
    "class TestOuter:\n    class TestInner:\n        def test_c(self):\n"
    "            assert True\n\n\n"
    "def helper():\n    return 1\n\n\n"
    "class Holder:\n    def test_d(self):\n        assert True\n\n\n"
    "CONSTANT = 1\n"
)
FRAGMENT = "seal/ledger/2000000001-a-later-item.md"
TESTS = "tests/test_held.py"


def vendored(tmp_path):
    """The checker as `evidence-ci` vendors it: alone in `tools/`, with no
    `hooks/` and no `SKILL.md` beside it (S12)."""
    tools = tmp_path / "elsewhere" / "tools"
    tools.mkdir(parents=True)
    dst = tools / "evidence_check.py"
    dst.write_bytes(open(SCRIPT, "rb").read())
    return str(dst)


@pytest.fixture(params=["plugin", "vendored"])
def script(request, tmp_path):
    return SCRIPT if request.param == "plugin" else vendored(tmp_path)


@pytest.fixture
def repo(tmp_path):
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    (d / "tests").mkdir()
    (d / "tests" / "test_held.py").write_text(HELD, encoding="utf-8")
    return d


def fragment(repo, rows):
    path = repo / FRAGMENT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(row + "\n" for row in rows), encoding="utf-8")
    return path


def held(grounds, claim="R1 · the claim holds"):
    return f"| {claim} | {grounds} | seen red, then green | 2026-10-08 | |"


def run(args, cwd, script=SCRIPT):
    return subprocess.run(
        [sys.executable, script, *args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def findings(out):
    """`[(status, coordinate, detail)]` for every finding line printed."""
    found = []
    for line in out.splitlines():
        status, _, rest = line.strip().partition(" ")
        if status in ("DRIFTED", "BROKEN", "MALFORMED", "EXTERNAL", "OVERFLOW"):
            coord, _, detail = rest.strip().partition("  ")
            found.append((status, coord, detail))
    return found


def total(out):
    return next(line for line in out.splitlines() if line.startswith("total: "))


# --- S1 ------------------------------------------------------------------------


def test_a_test_row_resolves_and_counts_among_ok(repo, script):
    """S1. Red against the unfixed checker, which read the cell as citing
    nothing: `MALFORMED`, *cites no coordinate*."""
    fragment(repo, [held(f"`{TESTS}::test_holds`")])
    out = run(["--strict", "."], repo, script)
    assert out.returncode == 0, out.stdout + out.stderr
    assert findings(out.stdout) == [], out.stdout
    assert total(out.stdout).startswith("total: 1 ok · 0 drifted"), out.stdout


def test_several_tests_and_a_class_resolve_on_one_row(repo, script):
    fragment(repo, [held(f"`{TESTS}::test_holds`, `{TESTS}::TestA`")])
    out = run(["--strict", "."], repo, script)
    assert out.returncode == 0, out.stdout + out.stderr
    assert total(out.stdout).startswith("total: 2 ok"), out.stdout


# --- S2 ------------------------------------------------------------------------


def test_a_renamed_test_breaks_the_row(repo, script):
    """S2. BROKEN is exit 2 on the lenient run too, as a gone unit is."""
    fragment(repo, [held(f"`{TESTS}::test_holds`")])
    (repo / TESTS).write_text(
        HELD.replace("def test_holds", "def test_still_holds"), encoding="utf-8"
    )
    out = run(["."], repo, script)
    assert out.returncode == 2, out.stdout
    assert findings(out.stdout) == [
        (
            "BROKEN",
            f"{TESTS}::test_holds",
            f"no def or class named test_holds in {TESTS}",
        )
    ], out.stdout


def test_a_test_whose_file_is_gone_is_broken(repo, script):
    fragment(repo, [held("`tests/test_gone.py::test_holds`")])
    out = run(["."], repo, script)
    assert out.returncode == 2, out.stdout
    assert findings(out.stdout) == [
        ("BROKEN", "tests/test_gone.py::test_holds", "file not found")
    ], out.stdout


# --- S3 ------------------------------------------------------------------------


def test_a_method_resolves_in_pytests_spelling(repo, script):
    """S3. The names after the path join with `.`, the key `py_spans` uses."""
    fragment(
        repo,
        [
            held(f"`{TESTS}::TestA::test_b`"),
            held(f"`{TESTS}::TestOuter::TestInner::test_c`", "R2 · nested"),
        ],
    )
    out = run(["--strict", "."], repo, script)
    assert out.returncode == 0, out.stdout + out.stderr
    assert total(out.stdout).startswith("total: 2 ok"), out.stdout


def test_a_method_spelled_bare_is_named_with_its_spelling(repo, script):
    """S3's other half: `path::test_b` for a method is not a top-level
    function, and the detail says how pytest spells it."""
    fragment(repo, [held(f"`{TESTS}::test_b`")])
    out = run(["."], repo, script)
    assert out.returncode == 2, out.stdout
    assert findings(out.stdout) == [
        (
            "BROKEN",
            f"{TESTS}::test_b",
            f"no def or class named test_b in {TESTS} — it is a method of TestA, "
            f"and a method is written `{TESTS}::TestA::test_b`",
        )
    ], out.stdout


# --- S4 ------------------------------------------------------------------------


@pytest.mark.parametrize(
    "name, kind",
    [
        ("helper", "def"),
        ("Holder", "class"),
        ("Holder::test_d", "def"),
        ("CONSTANT", "constant"),
    ],
)
def test_a_unit_pytest_does_not_collect_is_no_test(repo, script, name, kind):
    """S4. A unit that merely exists holds nothing, which is what *cites no
    coordinate* refuses: MALFORMED, exit 1 leniently and 2 under `--strict`."""
    fragment(repo, [held(f"`{TESTS}::{name}`")])
    out = run(["."], repo, script)
    assert out.returncode == 1, out.stdout
    assert findings(out.stdout) == [
        (
            "MALFORMED",
            f"{TESTS}::{name}",
            f"a {kind} pytest does not collect by default, so nothing holds the "
            "claim — name it in Code grounds as pytest spells it, "
            "`tests/test_x.py::test_y`, or `tests/test_x.py::TestA::test_b` for a "
            "method; or, where no test holds it, write `path#anchor@hash`",
        )
    ], out.stdout
    assert run(["--strict", "."], repo, script).returncode == 2


@pytest.mark.parametrize(
    "token", [f"{TESTS}::test_holds[one]", "tests/test_held.txt::test_holds"]
)
def test_a_token_that_is_no_node_id_is_malformed(repo, script, token):
    """A parametrised id names no `def`, and a node id names a `.py` file."""
    fragment(repo, [held(f"`{token}`")])
    out = run(["."], repo, script)
    assert out.returncode == 1, out.stdout
    ((status, coord, detail),) = findings(out.stdout)
    assert (status, coord) == ("MALFORMED", token), out.stdout
    assert detail.startswith("does not parse as a test — name it"), detail


def test_a_unit_defined_twice_is_named(repo, script):
    (repo / TESTS).write_text(
        HELD + "\n\ndef test_holds():\n    assert False\n", encoding="utf-8"
    )
    fragment(repo, [held(f"`{TESTS}::test_holds`")])
    out = run(["."], repo, script)
    assert out.returncode == 2, out.stdout
    assert findings(out.stdout) == [
        (
            "BROKEN",
            f"{TESTS}::test_holds",
            f"test_holds is defined 2 times in {TESTS}; a test is defined once",
        )
    ], out.stdout


# --- S5 ------------------------------------------------------------------------


def handler_hash(repo):
    text = (repo / "src" / "service.py").read_text(encoding="utf-8")
    (place,) = ec.resolve_unit("src/service.py", "handler", text)[0]
    return ec.content_hash(ec.gfm_lines(text)[place[0] - 1 : place[1]])


def test_a_row_mixing_the_two_forms_is_malformed(repo, script):
    """S5. A row that says *held by a test* while still owing a re-read on
    every edit is the half-form that keeps the bookkeeping."""
    grounds = f"`{TESTS}::test_holds`, `src/service.py#handler@{handler_hash(repo)}`"
    fragment(repo, [held(grounds)])
    out = run(["."], repo, script)
    assert out.returncode == 1, out.stdout
    assert (
        "MALFORMED",
        grounds,
        "holds a test and a code coordinate, and a row is one form or the other — "
        "keep the test where it holds the claim and move the coordinates out, or "
        "keep the coordinates and move the test to Verified behavior",
    ) in findings(out.stdout), out.stdout


def test_a_citing_rows_citation_is_not_the_other_form(repo, script):
    """S5's other half: a `Corrected ·` row opens its grounds with the ledger
    line it supersedes, which is not a code coordinate."""
    section = "### 1000000001-the-first-item"
    row = f"| R1 · handler adds one | `src/service.py#handler@{handler_hash(repo)}` | read | 2026-01-01 | |"
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        f"## 0.1.0 — 2026-01-01\n\n{section}\n\n{row}\n", encoding="utf-8"
    )
    cite = (
        f'seal/releases/0.1.0.md#"{section}">"R1 · handler adds one"'
        f"@{ec.content_hash([row])}"
    )
    fragment(
        repo,
        [
            f"| Corrected · handler adds one | `{cite}`, `{TESTS}::test_holds` | "
            "seen red, then green | 2026-10-08 | Corrected 2026-10-08 by work item "
            "2000000001: held by its test from here on |"
        ],
    )
    out = run(["--strict", "."], repo, script)
    assert out.returncode == 0, out.stdout + out.stderr
    assert findings(out.stdout) == [], out.stdout


# --- S6 ------------------------------------------------------------------------


def test_a_node_id_outside_the_grounds_cell_is_prose(repo):
    """S6, over the shape the ledgers already hold: `path::name` in Verified
    behavior and Notes beside a hashed grounds cell. Nothing reads it, even
    where it names nothing."""
    fragment(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{handler_hash(repo)}` "
            "| `tests/test_gone.py::test_gone` is red without it | 2026-10-08 | "
            "`fold_check.py::bound` and `std::vector` are prose |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert findings(out.stdout) == [], out.stdout
    assert total(out.stdout).startswith("total: 1 ok"), out.stdout


# --- S8 ------------------------------------------------------------------------


def test_reverify_writes_nothing_on_a_test_row(repo):
    """S8. No hash to re-stamp and no date to write: the bytes stand."""
    path = fragment(repo, [held(f"`{TESTS}::test_holds`")])
    before = path.read_bytes()
    out = run(["--reverify", "--checked", "2026-10-08", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert path.read_bytes() == before
    assert "LEFT" not in out.stdout, out.stdout


def test_reverify_names_a_test_that_is_gone(repo):
    """S8's other half. A re-read cannot clear a gone test, so it is left
    and named, and the run exits 1 as it does for a malformed row."""
    path = fragment(repo, [held(f"`{TESTS}::test_gone`")])
    before = path.read_bytes()
    out = run(["--reverify", "--checked", "2026-10-08", "."], repo)
    assert out.returncode == 1, out.stdout
    assert path.read_bytes() == before
    assert (
        f"  LEFT  {TESTS}::test_gone  BROKEN — no def or class named test_gone in "
        f"{TESTS}"
    ) in out.stdout.splitlines(), out.stdout


# --- S9 ------------------------------------------------------------------------

HELD_OPTION = (
    "  a claim a test holds can move onto it once instead: a `Corrected ·` row "
    "citing the released row and naming that test in Code grounds, "
    "`tests/test_x.py::test_y`, retires the row's hashes, and no later edit "
    "drifts it (docs/the-evidence-ledger.md)"
)


def drifted_release(repo):
    """A released row citing `handler`, the freeze declared, then `handler`
    edited: a run of `--into` owes the row a `Re-read ·` row."""
    (repo / "seal").mkdir(exist_ok=True)
    (repo / "seal" / "config.md").write_text(
        "# Repository config\n\n| Item | Value |\n|---|---|\n"
        "| Ledger frozen from | 1 |\n",
        encoding="utf-8",
    )
    row = f"| R1 · handler adds one | `src/service.py#handler@{handler_hash(repo)}` | read | 2026-01-01 | |"
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        f"## 0.1.0 — 2026-01-01\n\n### 1000000001-the-first-item\n\n{row}\n",
        encoding="utf-8",
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("x + 1", "x + 2"), encoding="utf-8"
    )


def test_into_names_the_test_row_once_where_it_wrote_a_re_read(repo):
    """S9. `--into` cannot tell which of a row's grounds holds its claim, so
    it names the other repair once, in its summary, and writes none of it."""
    drifted_release(repo)
    out = run(["--reverify", "--into", FRAGMENT, "--checked", "2026-10-08", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    lines = out.stdout.splitlines()
    assert lines.count(HELD_OPTION) == 1, out.stdout
    assert (
        lines.index(HELD_OPTION)
        == lines.index("1 citing row written · 0 released rows left") + 1
    ), out.stdout
    assert "Corrected" not in (repo / FRAGMENT).read_text(encoding="utf-8")
    again = run(
        ["--reverify", "--into", FRAGMENT, "--checked", "2026-10-08", "."], repo
    )
    assert again.returncode == 0, again.stdout
    assert HELD_OPTION not in again.stdout.splitlines(), again.stdout


def test_the_commit_advisor_names_the_test_row_as_a_repair():
    """Q4 of this work item: the post-commit advisor carries its own repair
    sentence for a broken row under the freeze, so it names the other form
    too, rather than only the coordinates a correction carries."""
    spec = importlib.util.spec_from_file_location(
        "specseal_evidence_advisor_held",
        os.path.join(ROOT, "hooks", "evidence-advisor.py"),
    )
    advisor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(advisor)
    assert (
        "— or, where a test holds the claim, names that test instead, "
        "`tests/test_x.py::test_y`, and no later edit drifts it;"
    ) in advisor.FROZEN_REPAIR, advisor.FROZEN_REPAIR


# --- S11 -----------------------------------------------------------------------


def test_a_ledger_with_no_test_row_reads_as_it_always_did(repo):
    """S11. Hashed rows, a row citing nothing, prose holding `::` in and out
    of the grounds cell, and a fenced example holding a node id: the output
    is the one 0.20.0's checker printed for this ledger, line for line."""
    good = handler_hash(repo)
    ledger = repo / "seal" / "ledger.md"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(
        "# Ledger\n\n"
        "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
        "|---|---|---|---|---|\n"
        f"| P1 | `src/service.py#handler@{good}` std::vector | read | 2026-01-01 | `a::b` |\n"
        "| P2 | `src/service.py#handler@00000000` | read | 2026-01-01 | |\n"
        "| P3 | handler, read by hand | read | 2026-01-01 | |\n"
        "\n```\n"
        f"| P4 | `{TESTS}::test_gone` | an example | 2026-01-01 | |\n"
        "```\n",
        encoding="utf-8",
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 2, out.stdout
    assert [line.replace(os.sep, "/") for line in out.stdout.splitlines()[:5]] == [
        "",
        "seal/ledger.md",
        "  DRIFTED  src/service.py#handler  content changed at 1-2 — re-verify",
        "  MALFORMED handler, read by hand  cites no coordinate, so nothing checks "
        "the claim — write `path#anchor@hash` in the Code grounds cell, the hash as "
        "`@00000000`, then run `evidence-check --reverify .`; or, where a test "
        "holds the claim, name it in Code grounds as pytest spells it, "
        "`tests/test_x.py::test_y`, or `tests/test_x.py::TestA::test_b` for a "
        "method",
        "  1 ok · 1 drifted · 0 broken · 0 external · 0 old-format · 1 malformed "
        "· 0 overflow",
    ], out.stdout


def test_the_resolver_hands_each_caller_its_own_answer():
    """`unit_kinds` is memoised on the text; a caller that changes the dict
    it was handed changes nothing for the next one."""
    first = ec.unit_kinds(HELD)
    first["test_holds"] = ("class",)
    assert ec.unit_kinds(HELD)["test_holds"] == ("def",)
    assert ec.named_unit(HELD, ["TestA", "test_b"]) == ("def",)
    assert ec.named_unit(HELD, ["test_b"]) == ()
    assert ec.named_unit("def (:\n", ["x"]) is None
    # Round 1, ⬜ 4: a name is one identifier; `A.b` is not `A::b`.
    assert ec.named_unit(HELD, ["TestA.test_b"]) == ()


# --- round 1 -------------------------------------------------------------------


def released_test_row(repo, freeze):
    """A released row naming `test_holds`, then the test renamed, then one
    `Corrected ·` row in a fragment re-pointing the claim at the new name."""
    if freeze:
        (repo / "seal").mkdir(exist_ok=True)
        (repo / "seal" / "config.md").write_text(
            "# Repository config\n\n| Item | Value |\n|---|---|\n"
            "| Ledger frozen from | 1 |\n",
            encoding="utf-8",
        )
    section = "### 1000000001-the-first-item"
    row = f"| R1 · held | `{TESTS}::test_holds` | seen red | 2026-01-01 | |"
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        f"## 0.1.0 — 2026-01-01\n\n{section}\n\n{row}\n", encoding="utf-8"
    )
    (repo / TESTS).write_text(
        HELD.replace("def test_holds", "def test_renamed"), encoding="utf-8"
    )
    cite = f'seal/releases/0.1.0.md#"{section}">"R1 · held"@{ec.content_hash([row])}'
    fragment(
        repo,
        [
            f"| Corrected · held | `{cite}`, `{TESTS}::test_renamed` | seen red, "
            "then green | 2026-02-01 | Corrected 2026-02-01 by work item "
            "2000000001: re-pointed |"
        ],
    )


def test_a_released_test_row_re_pointed_by_a_correction_reads_clean(repo, script):
    """Round 1, 🔴 1. A released row naming a test that was renamed is
    repaired by one `Corrected ·` row naming the new test: the released row
    is superseded, so its gone test is not read again, as a superseded row's
    hashes are not. Red before the fix: BROKEN, exit 2."""
    released_test_row(repo, freeze=True)
    out = run(["--strict", "."], repo, script)
    assert out.returncode == 0, out.stdout + out.stderr
    assert findings(out.stdout) == [], out.stdout
    assert total(out.stdout).startswith("total: 2 ok"), out.stdout


def test_reverify_leaves_a_superseded_test_row_unnamed(repo):
    """Round 1, 🔴 1, the in-place writer: without the freeze `--reverify`
    reads the released file too, and a superseded row's gone test is no
    longer named on a `LEFT` line. Red before the fix: `LEFT`, exit 1."""
    released_test_row(repo, freeze=False)
    out = run(["--reverify", "--checked", "2026-10-08", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "test_holds" not in out.stdout, out.stdout


def test_a_corrections_own_gone_test_is_still_broken(repo):
    """Round 1, 🔴 1's other half: the correcting row starts a family of its
    own, and its own test is read like any row's."""
    released_test_row(repo, freeze=True)
    (repo / TESTS).write_text(HELD, encoding="utf-8")
    out = run(["--strict", "."], repo)
    assert out.returncode == 2, out.stdout
    assert [(s, c) for s, c, _ in findings(out.stdout)] == [
        ("BROKEN", f"{TESTS}::test_renamed")
    ], out.stdout


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
    ],
    ids=["not a test file", "conftest", "class with __init__"],
)
def test_a_test_the_suite_does_not_collect_holds_nothing(repo, script, rel, text, node):
    """Round 1, 🟡 2 (a): a statically readable test is in a `test_*.py` or
    `*_test.py` file, and its class has no `__init__`."""
    (repo / rel).write_text(text, encoding="utf-8")
    fragment(repo, [held(f"`{rel}::{node}`")])
    out = run(["--strict", "."], repo, script)
    assert out.returncode == 2, out.stdout + out.stderr
    ((status, coord, detail),) = findings(out.stdout)
    assert (status, coord) == ("MALFORMED", f"{rel}::{node}"), out.stdout
    assert "pytest does not collect by default" in detail, detail


NEVER = (
    "is marked to be skipped or to fail unconditionally, so the suite stays "
    "green whatever the code does and nothing holds the claim"
)


@pytest.mark.parametrize(
    "text, node",
    [
        (
            "import pytest\n\n@pytest.mark.skip\ndef test_x():\n    assert False\n",
            "test_x",
        ),
        (
            "import pytest\n\n@pytest.mark.skip(reason='later')\n"
            "def test_x():\n    assert False\n",
            "test_x",
        ),
        (
            "import pytest\n\n@pytest.mark.xfail\ndef test_x():\n    assert False\n",
            "test_x",
        ),
        (
            "import pytest\n\n@pytest.mark.xfail(reason='known')\n"
            "def test_x():\n    assert False\n",
            "test_x",
        ),
        (
            "import pytest\npytestmark = pytest.mark.skip\n\n"
            "def test_x():\n    assert False\n",
            "test_x",
        ),
        (
            "import pytest\npytestmark = [pytest.mark.slow, pytest.mark.skip]\n\n"
            "def test_x():\n    assert False\n",
            "test_x",
        ),
        (
            "import pytest\n\n@pytest.mark.skip\nclass TestS:\n"
            "    def test_x(self):\n        assert False\n",
            "TestS::test_x",
        ),
        (
            "import pytest\n\nclass TestS:\n    pytestmark = pytest.mark.xfail\n\n"
            "    def test_x(self):\n        assert False\n",
            "TestS::test_x",
        ),
    ],
    ids=[
        "skip",
        "skip with a reason",
        "xfail",
        "xfail with a reason",
        "module pytestmark",
        "module pytestmark list",
        "class decorator",
        "class pytestmark",
    ],
)
def test_a_test_that_cannot_fail_holds_nothing(repo, script, text, node):
    """Round 1, 🟡 2 (b): a test carrying an unconditional `skip` or `xfail`
    mark, on itself, a class around it or its module, leaves the suite green
    whatever the code does."""
    (repo / "tests" / "test_never.py").write_text(text, encoding="utf-8")
    fragment(repo, [held(f"`tests/test_never.py::{node}`")])
    out = run(["--strict", "."], repo, script)
    assert out.returncode == 2, out.stdout + out.stderr
    ((status, coord, detail),) = findings(out.stdout)
    assert (status, coord) == ("MALFORMED", f"tests/test_never.py::{node}")
    assert detail.startswith(f"{NEVER} — name it in Code grounds"), detail


@pytest.mark.parametrize(
    "text",
    [
        "import sys\nimport pytest\n\n@pytest.mark.skipif(sys.platform == 'x', "
        "reason='x')\ndef test_x():\n    assert True\n",
        "import sys\nimport pytest\n\n@pytest.mark.xfail(sys.platform == 'x', "
        "reason='x')\ndef test_x():\n    assert True\n",
        "import pytest\n\n@pytest.mark.slow\ndef test_x():\n    assert True\n",
    ],
    ids=["skipif", "xfail with a condition", "another mark"],
)
def test_a_conditional_mark_is_left_to_the_reader(repo, text):
    """Round 1, 🟡 2: `skipif`, and an `xfail` given a condition, run where
    the condition is false; whether that is here is the suite's to say."""
    (repo / "tests" / "test_maybe.py").write_text(text, encoding="utf-8")
    fragment(repo, [held("`tests/test_maybe.py::test_x`")])
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert findings(out.stdout) == [], out.stdout


def test_a_coordinate_quoting_a_scope_is_no_test(repo, script):
    """Round 1, 🟡 3, S11 and D3: a coordinate is unambiguous by its shape,
    so `::` inside its quoted locator is no node id. Red before the fix: two
    MALFORMED on a ledger holding no test row."""
    doc = repo / "docs" / "guide.md"
    doc.parent.mkdir()
    doc.write_text("# Guide\n\n## The Foo::bar form\n\nText.\n", encoding="utf-8")
    fragment(repo, [held('`docs/guide.md#"## The Foo::bar form"@00000000`')])
    run(["--reverify", "."], repo, script)
    out = run(["--strict", "."], repo, script)
    assert out.returncode == 0, out.stdout + out.stderr
    assert findings(out.stdout) == [], out.stdout


def test_a_pact_anchor_quoting_a_scope_is_no_test(repo):
    """Round 1, 🟡 3's other coordinate: a pact anchor's quoted heading path
    may hold `::` too, and it is a clause of a pact, not a test."""
    grounds = (
        f"`src/service.py#handler@{handler_hash(repo)}`, "
        '`pact:shared/"## The A::b clause"@abcdef12`'
    )
    fragment(repo, [held(grounds)])
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert findings(out.stdout) == [], out.stdout


# --- S13 -----------------------------------------------------------------------


def prose(rel):
    """REL's text with every run of whitespace one space, so a pin holds a
    sentence however the paragraph is wrapped."""
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return " ".join(handle.read().split())


@pytest.mark.parametrize(
    "rel, sentence",
    [
        (
            "docs/the-evidence-ledger.md",
            "**A row may name the test that holds its claim instead of a hash over "
            "the code.**",
        ),
        (
            "docs/the-evidence-ledger.md",
            "**The checker reads that the test is there, and the suite reads that "
            "it passes.**",
        ),
        ("docs/the-evidence-ledger.md", "**A row is one form or the other.**"),
        (
            "docs/the-evidence-ledger.md",
            "**A released row moves onto its test by one `Corrected ·` row, written "
            "when an edit reaches it, and never in bulk by a feature branch.**",
        ),
        ("docs/the-evidence-ledger.md", "**`path::name` has one resolver.**"),
        (
            "templates/ledger.md",
            "| <claim> | `tests/test_x.py::test_y`, … | how the test was seen red | "
            "<date seen red, then green> | |",
        ),
        (
            "templates/ledger.md",
            "| <claim> | `path#anchor@hash`, … | what reading the code showed | "
            "<date read> | |",
        ),
        (
            "skills/evidence-check/SKILL.md",
            "**A row held by a test takes three of these, and never `DRIFTED`** "
            "(#836).",
        ),
        (
            "skills/evidence-check/SKILL.md",
            "A row held by a test has no hash to rewrite: the run writes nothing on "
            "it and dates nothing",
        ),
        (
            "skills/evidence-ci/SKILL.md",
            "**Update the copy before the ledger holds a row held by a test.**",
        ),
        (
            "skills/evidence-ci/SKILL.md",
            "an older vendored copy reads it as `MALFORMED`, *cites no coordinate*",
        ),
    ],
)
def test_the_documents_state_the_test_row(rel, sentence):
    """S13. Each sentence a person reads to write or update a test row, pinned
    where it stands (`agent-contract` §14)."""
    assert sentence in prose(rel), f"{rel} no longer says: {sentence!r}"
