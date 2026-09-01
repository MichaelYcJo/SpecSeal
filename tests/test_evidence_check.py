"""evidence-check: ledger discovery, the CLI surface, and the exit codes.

The verdict machinery itself lives in `test_a_row_points_by_content.py`. What
is here is everything around it — which files are read, how several are
aggregated, and what a CI step sees.

**No fixture in this file runs git.** It used to need a repository with real
commits, because a row's baseline was a commit and drift was a diff. A
coordinate that names content needs only the file, which is the shortest
statement of what the redesign removed.
"""

import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")

SERVICE = "def handler(x):\n    return x + 1\n\n\ndef other():\n    return 0\n"
# `handler`'s body, hashed the way the checker hashes it.
GOOD = "9207ed06"


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def step(args, cwd):
    """The exit code of the CI step `evidence-ci` prints, guard included."""
    quoted = " ".join(f"'{a}'" for a in args)
    return subprocess.run(
        ["bash", "-e", "-c", f"python3 '{SCRIPT}' {quoted} || [ $? -eq 1 ]"],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
    ).returncode


@pytest.fixture
def proj(tmp_path):
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / "src" / "service.py").write_text(SERVICE)
    return d


def ledger(proj, body, at=".specseal/map.md"):
    path = proj / at
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# map\n\n" + body)
    return path


def test_the_hash_in_this_files_fixtures_is_the_real_one(proj):
    """Pinned rather than computed, so a fixture cannot agree with a broken
    hash function by using it to build its own expectation."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("ec", SCRIPT)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    assert ec.content_hash(SERVICE.splitlines()[0:2]) == GOOD


def test_a_matching_row_is_ok_and_exits_zero(proj):
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_drift_exits_one_and_strict_exits_two(proj):
    ledger(proj, "| POL-1 | `src/service.py#handler@00000000` |\n")
    assert run(["."], proj).returncode == 1
    assert run(["--strict", "."], proj).returncode == 2


def test_a_broken_coordinate_exits_two(proj):
    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n")
    r = run(["."], proj)
    assert "BROKEN" in r.stdout and r.returncode == 2, r.stdout


def test_a_deleted_root_level_file_is_broken_not_external(proj):
    """`main.py#f` with the file deleted used to classify as EXTERNAL — first
    path element missing meant "other repo" — and EXTERNAL never fails the
    build. A root-level coordinate has no cross-repo prefix, so a missing file
    there is a broken citation."""
    ledger(proj, "| POL-1 | `src/service.py#handler@00000000` |\n")
    (proj / "src" / "service.py").unlink()
    r = run(["."], proj)
    assert r.returncode == 2 and "BROKEN" in r.stdout and "EXTERNAL" not in r.stdout


def test_duplicate_coordinates_are_counted_once(proj):
    ledger(
        proj,
        f"| POL-1 | `src/service.py#handler@{GOOD}` |\n"
        f"| POL-2 | `src/service.py#handler@{GOOD}` |\n",
    )
    assert "1 ok" in run(["."], proj).stdout


def test_map_resolves_a_prefixed_cross_repo_path(proj, tmp_path):
    other = tmp_path / "legacy"
    (other / "src").mkdir(parents=True)
    (other / "src" / "service.py").write_text(SERVICE)
    ledger(proj, f"| POL-1 | `legacy/src/service.py#handler@{GOOD}` |\n")
    # EXTERNAL needs declared cross-repo intent since round 4's 🔴 3; a
    # parity config is one of the three declarations.
    (proj / ".specseal" / "parity.md").write_text("# parity\n")
    assert "1 external" in run(["."], proj).stdout
    r = run(["--map", f"legacy={other}", "."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_a_missing_prefix_without_cross_repo_intent_is_broken(proj):
    """EXTERNAL is a claim about ANOTHER repository, and only a declaration —
    `.specseal/parity.md`, `--map`, `--default-repo` — says this project has
    one. Without intent, a deleted or renamed directory turned its rows
    EXTERNAL and the build stayed green (round 4, 🔴 3)."""
    ledger(proj, "| POL-1 | `legacy/src/old.py#handler@00000000` |\n")
    r = run(["."], proj)
    assert "EXTERNAL" not in r.stdout and "BROKEN" in r.stdout, r.stdout
    assert r.returncode == 2, r.stdout


def test_migrate_reads_map_and_default_repo(proj, tmp_path):
    """`--migrate` ignored both, so a legacy-parity ledger could never
    migrate and the OLD-FORMAT prescription line was circular for exactly
    those repositories (round 4, 🟡 9)."""
    other = tmp_path / "legacy"
    (other / "src").mkdir(parents=True)
    (other / "src" / "old.py").write_text(SERVICE)
    orig = tmp_path / "orig"
    (orig / "apps").mkdir(parents=True)
    (orig / "apps" / "svc.py").write_text(SERVICE)
    ledger(
        proj,
        "| POL-1 | `legacy/src/old.py:1-2` | 2026-08-31 |\n"
        "| POL-2 | `apps/svc.py:1-2` | 2026-08-31 |\n",
    )
    r = run(
        ["--migrate", "--map", f"legacy={other}", "--default-repo", str(orig), "."],
        proj,
    )
    assert "2 rows migrated" in r.stdout, r.stdout
    text = (proj / ".specseal" / "map.md").read_text()
    assert f"legacy/src/old.py#handler@{GOOD}" in text, text
    assert f"apps/svc.py#handler@{GOOD}" in text, text


def test_default_repo_resolves_an_unprefixed_cross_repo_path(proj, tmp_path):
    """A migration ledger states coordinates against the ORIGINAL repo with no
    prefix. The property is resolution: found in the other checkout rather than
    reported EXTERNAL or BROKEN."""
    orig = tmp_path / "orig"
    (orig / "apps").mkdir(parents=True)
    (orig / "apps" / "svc.py").write_text(SERVICE)
    ledger(proj, f"| POL-9 | `apps/svc.py#handler@{GOOD}` |\n")
    r = run(["--default-repo", str(orig), "."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_no_ledger_at_all_is_a_no_op(proj):
    r = run(["."], proj)
    assert "no evidence ledgers found" in r.stdout and r.returncode == 0


@pytest.mark.parametrize(
    "at",
    [".specseal/map.md", ".specseal/map/core.md", "docs/policies/demo/_evidence.md"],
)
def test_the_checker_finds_the_ledger_with_no_arguments(proj, at):
    """The current home, the per-work-item fragment, and the pre-0.10 address."""
    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n", at=at)
    r = run(["."], proj)
    assert "no evidence ledgers found" not in r.stdout, r.stdout
    assert "src/service.py#gone" in r.stdout, r.stdout
    assert r.returncode == 2


def test_a_custom_ledger_glob_is_read_instead(proj):
    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n")
    (proj / "SPEC.md").write_text(f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["--ledger", "SPEC.md", "."], proj)
    assert "SPEC.md" in r.stdout and "1 ok" in r.stdout and r.returncode == 0


def test_several_ledgers_aggregate_and_the_worst_one_decides(proj):
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    ledger(
        proj, "| POL-9 | `src/service.py#gone@00000000` |\n", at=".specseal/map/b.md"
    )
    r = run(["."], proj)
    assert "1 ok" in r.stdout and "1 broken" in r.stdout
    assert r.returncode == 2, "a broken coordinate in the second ledger must fail"


def test_a_coordinate_in_a_dot_directory_resolves(proj):
    """A leading dot is allowed: `.github/...` was read as `github/...` and
    reported EXTERNAL, so the plugin could not cite its own directory."""
    (proj / ".github").mkdir()
    (proj / ".github" / "svc.py").write_text(SERVICE)
    ledger(proj, f"| POL-1 | `.github/svc.py#handler@{GOOD}` |\n")
    r = run(["."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_letting_drift_warn_takes_both_halves(proj):
    """`evidence-ci` twice described a softer mode that does not exist.

    Drift fails a `bash -e` step either way; the guard only lets it through
    once `--strict` is gone too, and a broken coordinate still fails through
    that same guard."""
    ledger(proj, "| POL-1 | `src/service.py#handler@00000000` |\n")
    assert run(["."], proj).returncode == 1, "drift already fails without --strict"
    assert run(["--strict", "."], proj).returncode == 2
    assert step(["--strict", "."], proj) == 1, "the guard cannot swallow exit 2"
    assert step(["."], proj) == 0, "both halves together let drift warn"

    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n")
    assert step(["."], proj) == 1, "the guard must not swallow a broken coordinate"


def test_the_ci_skill_prints_the_step_that_matches_that_behavior():
    """The executed fact above is worth what the sentence beside it says."""
    with open(
        os.path.join(ROOT, "skills", "evidence-ci", "SKILL.md"), encoding="utf-8"
    ) as f:
        text = f.read()
    snippet = text.split("```yaml")[1].split("```")[0]
    assert "|| [ $? -eq 1 ]" in snippet, "the step lost the guard"
    assert "--strict" not in snippet, (
        "the printed step keeps --strict, whose exit 2 the guard cannot swallow"
    )
    assert "drop `--strict`" in text, "the prose stopped naming the other half"
