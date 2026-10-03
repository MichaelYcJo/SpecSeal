"""Box 3 of #715: two branches re-reading one released row do not conflict.

Each branch edits a unit a released row cites and re-reads that row into its
OWN fragment with `evidence-check --reverify --into`. No file is written by
both, so git merges them with no conflict, and the merged tree reads the row
as one family (S6). Where both edited the same unit, neither reading holds
the merged content and the row is DRIFTED: the halves rule of
`docs/the-evidence-ledger.md`, computed (S7). The control is the rule this
replaces: the same two re-reads written in place into the released file
conflict on the row's line.

Driven from Python, per `skills/agent-contract/SKILL.md` §8.
"""

import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")

A = "def f(x):\n    a = x + 1\n    b = a * 2\n    c = b - 3\n    return c\n"
B = "def g(x):\n    return x\n"


def git(root, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=check,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def checker(root, *args):
    return subprocess.run(
        [sys.executable, SCRIPT, *args, "."],
        cwd=str(root),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def commit(root, message):
    git(root, "add", "-A")
    git(root, "commit", "-qm", message)


def unit_hash(root, rel, name):
    import importlib.util

    spec = importlib.util.spec_from_file_location("ec", SCRIPT)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    text = (root / rel).read_text()
    ((a, b),), _ = ec.resolve_unit(rel, name, text)
    return ec.content_hash(ec.gfm_lines(text)[a - 1 : b])


def released_repo(tmp_path, frozen=True):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "t@example.com")
    git(root, "config", "user.name", "t")
    write(root, "a.py", A)
    write(root, "b.py", B)
    f, g = unit_hash(root, "a.py", "f"), unit_hash(root, "b.py", "g")
    write(
        root,
        "seal/releases/0.1.0.md",
        "## 0.1.0 — 2026-01-01\n\n### 1000000001-the-first\n\n"
        f"| R1 · f and g agree | `a.py#f@{f}`, `b.py#g@{g}` | read | 2026-01-01 | |\n",
    )
    if frozen:
        write(
            root,
            "seal/config.md",
            "| Item | Value |\n|---|---|\n| Ledger frozen from | 1 |\n",
        )
    commit(root, "release 0.1.0")
    return root


def branch(root, name, rel, old, new, fragment=None):
    git(root, "checkout", "-q", "-b", name, "main")
    write(root, rel, (root / rel).read_text().replace(old, new))
    if fragment is None:
        out = checker(root, "--reverify", "--checked", "2026-02-01")
    else:
        out = checker(root, "--reverify", "--into", fragment, "--checked", "2026-02-01")
    assert out.returncode == 0, out.stdout + out.stderr
    commit(root, f"{name} edits {rel} and re-reads the row")
    git(root, "checkout", "-q", "main")


def test_s6_two_branches_re_reading_one_released_row_merge_cleanly(tmp_path):
    """S6. A edits `f`, B edits `g`, each re-reads R1 into its own fragment:
    both merge with no conflict, and the merged tree checks clean."""
    root = released_repo(tmp_path)
    branch(root, "a", "a.py", "x + 1", "x + 10", "seal/ledger/2000000001-a.md")
    branch(root, "b", "b.py", "return x", "return -x", "seal/ledger/2000000002-b.md")
    assert (
        git(root, "merge", "-q", "--no-ff", "-m", "a", "a", check=False).returncode == 0
    )
    merge = git(root, "merge", "-q", "--no-ff", "-m", "b", "b", check=False)
    assert merge.returncode == 0, merge.stdout + merge.stderr
    out = checker(root, "--strict")
    assert out.returncode == 0, out.stdout


def test_the_control_in_place_re_reads_of_one_row_conflict(tmp_path):
    """The rule this replaces: without the freeze, `--reverify` re-stamps R1
    in place on both branches, and the second merge conflicts on its line."""
    root = released_repo(tmp_path, frozen=False)
    branch(root, "a", "a.py", "x + 1", "x + 10")
    branch(root, "b", "b.py", "return x", "return -x")
    git(root, "merge", "-q", "--no-ff", "-m", "a", "a")
    merge = git(root, "merge", "-q", "--no-ff", "-m", "b", "b", check=False)
    assert merge.returncode != 0, merge.stdout
    assert "seal/releases/0.1.0.md" in merge.stdout + merge.stderr


def test_s7_both_branches_editing_one_unit_leave_the_row_drifted(tmp_path):
    """S7. A and B edit different lines of `f`; git merges them cleanly, and
    neither reading holds the merged `f`, so R1 is DRIFTED on `a.py#f`."""
    root = released_repo(tmp_path)
    branch(root, "a", "a.py", "x + 1", "x + 10", "seal/ledger/2000000001-a.md")
    branch(root, "b", "a.py", "b - 3", "b - 30", "seal/ledger/2000000002-b.md")
    git(root, "merge", "-q", "--no-ff", "-m", "a", "a")
    merge = git(root, "merge", "-q", "--no-ff", "-m", "b", "b", check=False)
    assert merge.returncode == 0, merge.stdout + merge.stderr
    out = checker(root, "--strict")
    assert out.returncode == 2, out.stdout
    drifted = [
        line.split()[1]
        for line in out.stdout.splitlines()
        if line.strip().startswith("DRIFTED")
    ]
    assert drifted and set(drifted) == {"a.py#f"}, out.stdout
