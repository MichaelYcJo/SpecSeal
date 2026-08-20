"""evidence-check hardening: boundaries, dedup, missing baseline, deletions."""

import os
import subprocess
import sys

import pytest

SCRIPT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "skills",
    "evidence-check",
    "scripts",
    "evidence_check.py",
)


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args], cwd=cwd, capture_output=True, text=True
    )


@pytest.fixture
def proj(tmp_path):
    d = tmp_path / "proj"
    (d / "docs" / "policies" / "demo").mkdir(parents=True)
    (d / "src").mkdir()
    git = lambda *a: subprocess.run(
        ["git", "-C", str(d), *a], check=True, capture_output=True, text=True
    )
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (d / "src" / "service.py").write_text("".join(f"line{i}\n" for i in range(1, 9)))
    git("add", "-A")
    git("commit", "-qm", "base")
    return d


def ledger(proj, body, baseline=True):
    head = subprocess.run(
        ["git", "-C", str(proj), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    header = f"| Baseline commit | `{head}` |\n" if baseline else "no baseline here\n"
    (proj / "docs" / "policies" / "demo" / "_evidence.md").write_text(
        "# ledger\n" + header + body
    )
    return head


def test_range_end_at_exact_file_length_is_ok(proj):
    ledger(proj, "| POL-1 | `src/service.py:6-8` |\n")  # file has exactly 8 lines
    r = run(["."], str(proj))
    assert r.returncode == 0 and "1 ok" in r.stdout


def test_deleted_root_level_file_is_broken_not_external(proj):
    # `main.py:2` with main.py deleted used to classify as EXTERNAL (first
    # path element missing == "other repo"), and EXTERNAL never fails the
    # build. Root-level coordinates have no cross-repo prefix, so a missing
    # file there is a broken citation.
    (proj / "main.py").write_text("a\nb\n")
    subprocess.run(["git", "-C", str(proj), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(proj), "commit", "-qm", "add main"], check=True)
    ledger(proj, "| POL-1 | `main.py:2` |\n")
    subprocess.run(["git", "-C", str(proj), "rm", "-q", "main.py"], check=True)
    r = run(["."], str(proj))
    assert r.returncode == 2 and "BROKEN" in r.stdout and "EXTERNAL" not in r.stdout


def test_missing_baseline_skips_drift_and_says_so(proj):
    ledger(proj, "| POL-1 | `src/service.py:2` |\n", baseline=False)
    (proj / "src" / "service.py").write_text("CHANGED\n" * 8)
    r = run(["."], str(proj))
    assert r.returncode == 0
    assert "drift check skipped" in r.stdout


def test_duplicate_coordinates_counted_once(proj):
    ledger(proj, "| POL-1 | `src/service.py:2` |\n| POL-2 | `src/service.py:2` |\n")
    r = run(["."], str(proj))
    assert "1 ok" in r.stdout


def test_pure_deletion_still_drifts_neighbors(proj):
    ledger(proj, "| POL-1 | `src/service.py:4-5` |\n")
    lines = [f"line{i}\n" for i in range(1, 9)]
    del lines[3]  # delete line4 entirely — a 0-count hunk in unified diff
    (proj / "src" / "service.py").write_text("".join(lines))
    subprocess.run(
        ["git", "-C", str(proj), "commit", "-qam", "delete a line"],
        check=True,
        capture_output=True,
    )
    r = run(["."], str(proj))
    assert r.returncode == 1 and "DRIFTED" in r.stdout


def test_custom_ledger_glob(proj):
    head = subprocess.run(
        ["git", "-C", str(proj), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    (proj / "SPEC.md").write_text(f"`{head}`\n| POL-1 | `src/service.py:1` |\n")
    (proj / "docs" / "policies" / "demo" / "_evidence.md").write_text("# empty\n")
    r = run(["--ledger", "SPEC.md", "."], str(proj))
    assert "SPEC.md" in r.stdout and "1 ok" in r.stdout


def test_multiple_ledgers_aggregate(proj, tmp_path):
    ledger(proj, "| POL-1 | `src/service.py:1` |\n")
    (proj / "docs" / "policies" / "other").mkdir()
    (proj / "docs" / "policies" / "other" / "_evidence.md").write_text(
        "# other\n| POL-9 | `src/missing.py:1` |\n"
    )
    r = run(["."], str(proj))
    assert r.returncode == 2  # broken in the second ledger fails the whole run
    assert "1 ok" in r.stdout and "1 broken" in r.stdout


def test_url_ports_are_not_coordinates(proj):
    # `example.com:8080` has the coordinate shape exactly; ledgers that cite
    # a link used to print it as EXTERNAL noise.
    ledger(proj, "| POL-1 | see https://example.com:8080/docs |\n"
                 "| POL-2 | `src/service.py:2` |\n")
    r = run(["."], str(proj))
    assert r.returncode == 0, r.stdout
    assert "example.com" not in r.stdout
    assert "1 ok" in r.stdout
