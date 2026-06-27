"""evidence-check: verdicts, exit codes, cross-repo resolution."""
import os
import subprocess
import sys

import pytest

SCRIPT = os.path.join(os.path.dirname(__file__), "..",
                      "skills", "evidence-check", "scripts", "evidence_check.py")


def run(args, cwd):
    return subprocess.run([sys.executable, SCRIPT, *args],
                          cwd=cwd, capture_output=True, text=True)


@pytest.fixture
def ledger_repo(tmp_path):
    d = tmp_path / "proj"
    (d / "docs" / "policies" / "demo").mkdir(parents=True)
    (d / "src").mkdir()
    git = lambda *a: subprocess.run(["git", "-C", str(d), *a], check=True,
                                    capture_output=True, text=True)
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (d / "src" / "service.py").write_text("".join(f"line{i}\n" for i in range(1, 9)))
    git("add", "-A")
    git("commit", "-qm", "base")
    base = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    (d / "docs" / "policies" / "demo" / "_evidence.md").write_text(
        f"# demo ledger\n| Baseline commit | `{base}` |\n\n"
        "| POL-1 | `src/service.py:2-3` |\n"
        "| POL-2 | `src/service.py:7` |\n"
        "| POL-3 | `src/service.py:99` |\n"
        "| POL-4 | `src/missing.py:5` |\n"
        "| POL-5 | `legacy-api/src/old.py:10` |\n"
    )
    git("add", "-A")
    git("commit", "-qm", "ledger")
    # drift: touch lines 2-3's range after the baseline
    (d / "src" / "service.py").write_text(
        "line1\nCHANGED\n" + "".join(f"line{i}\n" for i in range(3, 9)))
    git("commit", "-qam", "drift")
    return d


def test_verdicts_and_exit_code(ledger_repo):
    r = run(["."], str(ledger_repo))
    assert r.returncode == 2  # broken present
    assert "DRIFTED  src/service.py:2-3" in r.stdout
    assert "BROKEN   src/service.py:99" in r.stdout
    assert "BROKEN   src/missing.py:5" in r.stdout
    assert "EXTERNAL legacy-api/src/old.py:10" in r.stdout


def test_map_resolves_external(ledger_repo, tmp_path):
    ext = tmp_path / "legacy-api" / "src"
    ext.mkdir(parents=True)
    (ext / "old.py").write_text("x\n" * 20)
    r = run(["--map", f"legacy-api={tmp_path / 'legacy-api'}", "."], str(ledger_repo))
    assert "EXTERNAL" not in r.stdout


def test_default_repo_resolves_unprefixed(ledger_repo, tmp_path):
    # a migration-style ledger citing the original repo without a prefix
    orig = tmp_path / "orig"
    (orig / "apps").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(orig)], check=True)
    (orig / "apps" / "svc.py").write_text("a\nb\nc\n")
    (ledger_repo / "docs" / "policies" / "demo" / "_evidence.md").write_text(
        "# ledger\n| POL-9 | `apps/svc.py:2` |\n")
    r = run(["--default-repo", str(orig), "."], str(ledger_repo))
    assert "1 ok" in r.stdout and r.returncode == 0


def test_clean_ledger_exits_zero(ledger_repo):
    (ledger_repo / "docs" / "policies" / "demo" / "_evidence.md").write_text(
        "# ledger\n| POL-1 | `src/service.py:1` |\n")
    assert run(["."], str(ledger_repo)).returncode == 0


def test_drift_only_exit_codes(ledger_repo):
    (ledger_repo / "docs" / "policies" / "demo" / "_evidence.md").write_text(
        "# ledger\n"
        + f"baseline `{first_commit(ledger_repo)}`\n"
        + "| POL-1 | `src/service.py:2` |\n")
    assert run(["."], str(ledger_repo)).returncode == 1
    assert run(["--strict", "."], str(ledger_repo)).returncode == 2


def first_commit(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-list", "--max-parents=0", "HEAD"],
        capture_output=True, text=True).stdout.strip()


def test_no_ledger_is_a_noop(tmp_path):
    assert run(["."], str(tmp_path)).returncode == 0
