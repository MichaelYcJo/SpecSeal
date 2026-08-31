"""evidence-check hardening: boundaries, dedup, missing baseline, deletions."""

import os
import shutil
import subprocess
import sys

import pytest
from conftest import NOT_A_SHELL, shell_probe

# Resolved once: the probe spawns a process, and `step` is called from several
# cases. Only the "never was a shell" half is actionable here -- a shell whose
# environment ate the probe still runs the step correctly, and the case that
# owns that distinction is `tests/test_the_waiver_can_be_typed.py`.
_BASH = shell_probe("bash") if shutil.which("bash") else f"not on PATH -- {NOT_A_SHELL}"
BASH_IS_NOT_A_SHELL = _BASH if _BASH and _BASH.endswith(NOT_A_SHELL) else None

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
        [sys.executable, SCRIPT, *args],
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def _build_proj_template(d):
    (d / "src").mkdir(parents=True)
    git = lambda *a: subprocess.run(
        ["git", "-C", str(d), *a],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (d / "src" / "service.py").write_text("".join(f"line{i}\n" for i in range(1, 9)))
    git("add", "-A")
    git("commit", "-qm", "base")


@pytest.fixture(scope="session")
def _proj_template(tmp_path_factory):
    d = tmp_path_factory.mktemp("proj-template") / "proj"
    _build_proj_template(d)
    return d


@pytest.fixture
def proj(tmp_path, _proj_template):
    d = tmp_path / "proj"
    shutil.copytree(_proj_template, d)
    (d / "docs" / "policies" / "demo").mkdir(parents=True)
    return d


def ledger(proj, body, baseline=True):
    head = subprocess.run(
        ["git", "-C", str(proj), "rev-parse", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
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


def step(args, cwd):
    """The workflow step `evidence-ci` prints, run the way GitHub runs one.

    The name `bash` is asked to prove itself first. On a `windows-latest`
    runner it resolves to the WSL launcher, which exits 1 whatever it is
    handed -- so `== 1` below passed for a reason that had nothing to do with
    the guard, and `== 0` failed for the same non-reason. Neither line
    measured the step.

    Skipping there loses no coverage: the `ledger` job this models is
    `runs-on: ubuntu-latest`, so on Windows there is no step to model.
    """
    if BASH_IS_NOT_A_SHELL:
        pytest.skip(f"`bash` is {BASH_IS_NOT_A_SHELL}, and the `ledger` job is ubuntu")
    return subprocess.run(
        [
            "bash",
            "-e",
            "-c",
            '"$@" || [ $? -eq 1 ]',
            "_",
            sys.executable,
            SCRIPT,
            *args,
        ],
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).returncode


def test_letting_drift_warn_takes_both_halves(proj):
    """`evidence-ci` twice described a softer mode that does not exist.

    First by calling plain mode softer, then by saying the guard alone is
    enough. Drift fails a `bash -e` step either way; the guard only lets it
    through once `--strict` is gone too, and a broken coordinate still fails
    through that same guard."""
    ledger(proj, "| POL-1 | `src/service.py:4-5` |\n")
    (proj / "src" / "service.py").write_text(
        "".join(f"changed{i}\n" for i in range(1, 9))
    )
    subprocess.run(
        ["git", "-C", str(proj), "commit", "-qam", "touch the cited range"],
        check=True,
        capture_output=True,
    )

    assert run(["."], str(proj)).returncode == 1, "drift already fails without --strict"
    assert run(["--strict", "."], str(proj)).returncode == 2

    assert step(["--strict", "."], str(proj)) == 1, (
        "keeping --strict and adding the guard still breaks the step"
    )
    assert step(["."], str(proj)) == 0, "both halves together let drift warn"

    ledger(proj, "| POL-1 | `src/service.py:1-40` |\n")  # the file has 8 lines
    assert step(["."], str(proj)) == 1, "the guard must not swallow a broken coordinate"


def test_the_ci_skill_prints_the_step_that_matches_that_behavior():
    """The executed fact above is worth what the sentence beside it says.

    The first attempt at this correction told readers to change the step and
    left `--strict` in the printed snippet, which is the same overclaim one
    layer down: follow it literally and the build still breaks."""
    with open(
        os.path.join(
            os.path.dirname(__file__), "..", "skills", "evidence-ci", "SKILL.md"
        ),
        encoding="utf-8",
    ) as f:
        text = f.read()
    snippet = text.split("```yaml")[1].split("```")[0]
    assert "|| [ $? -eq 1 ]" in snippet, "the step lost the guard"
    assert "--strict" not in snippet, (
        "the printed step keeps --strict, whose exit 2 the guard cannot swallow"
    )
    assert "drop `--strict`" in text, "the prose stopped naming the other half"


def test_custom_ledger_glob(proj):
    head = subprocess.run(
        ["git", "-C", str(proj), "rev-parse", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
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
    ledger(
        proj,
        "| POL-1 | see https://example.com:8080/docs |\n"
        "| POL-2 | `src/service.py:2` |\n",
    )
    r = run(["."], str(proj))
    assert r.returncode == 0, r.stdout
    assert "example.com" not in r.stdout
    assert "1 ok" in r.stdout


# --- per-row baselines: drift drains row by row ---------------------------


def write_ledger(proj, baseline, body):
    """A ledger whose header baseline is pinned, not refreshed to HEAD."""
    (proj / "docs" / "policies" / "demo" / "_evidence.md").write_text(
        f"# ledger\n| Baseline commit | `{baseline}` |\n" + body
    )


def test_a_row_checked_after_the_change_is_not_drifted(proj):
    """One baseline per ledger makes drift all-or-nothing.

    Any wide refactor drifts every row at once, and the cheapest way out is
    bumping the header — which re-dates every claim without re-reading one.
    A row that records the commit it was re-checked at is measured from
    there, so the header can stay where it is."""
    base = subprocess.run(
        ["git", "-C", str(proj), "rev-parse", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    write_ledger(proj, base, "| POL-1 | `src/service.py:2` | 2026-01-01 |\n")
    (proj / "src" / "service.py").write_text("CHANGED\n" * 8)
    subprocess.run(["git", "-C", str(proj), "commit", "-qam", "edit"], check=True)
    after = subprocess.run(
        ["git", "-C", str(proj), "rev-parse", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()

    r = run(["."], str(proj))
    assert r.returncode == 1 and "DRIFTED" in r.stdout

    # Same stale header; only the row says it was re-read at `after`.
    write_ledger(proj, base, f"| POL-1 | `src/service.py:2` | 2026-01-02 `{after}` |\n")
    r = run(["."], str(proj))
    assert r.returncode == 0 and "1 ok" in r.stdout, r.stdout


def test_a_row_checked_before_a_later_change_still_drifts(proj):
    """The row's own SHA is a claim about when it was read, not an exemption."""
    checked = subprocess.run(
        ["git", "-C", str(proj), "rev-parse", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    ledger(proj, f"| POL-1 | `src/service.py:2` | 2026-01-01 `{checked}` |\n")
    (proj / "src" / "service.py").write_text("CHANGED\n" * 8)
    subprocess.run(["git", "-C", str(proj), "commit", "-qam", "edit"], check=True)
    r = run(["."], str(proj))
    assert r.returncode == 1 and "DRIFTED" in r.stdout, r.stdout


def test_a_sha_shaped_directory_in_the_row_is_not_a_baseline(proj):
    """`decade1/x.py:2` sits in the row too — stripping coordinates first is
    what keeps it from being read as a commit."""
    (proj / "decade1").mkdir()
    (proj / "decade1" / "x.py").write_text("a\nb\n")
    subprocess.run(["git", "-C", str(proj), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(proj), "commit", "-qm", "add"], check=True)
    ledger(proj, "| POL-1 | `decade1/x.py:2` |\n")
    r = run(["."], str(proj))
    assert r.returncode == 0 and "1 ok" in r.stdout, r.stdout


def test_a_coordinate_in_a_dot_directory_resolves(proj):
    """`.github/workflows/x.yml:3` was read as `github/...` and reported
    EXTERNAL — the plugin could not cite its own directories."""
    (proj / ".github").mkdir()
    (proj / ".github" / "w.yml").write_text("a\nb\nc\n")
    subprocess.run(["git", "-C", str(proj), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(proj), "commit", "-qm", "ci"], check=True)
    ledger(proj, "| POL-1 | `.github/w.yml:3` |\n")
    r = run(["."], str(proj))
    assert r.returncode == 0 and "1 ok" in r.stdout, r.stdout
    assert "EXTERNAL" not in r.stdout
