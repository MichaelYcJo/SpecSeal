"""A ledger check narrowed to one fragment reported clean, and it was blind.

`evidence-check --ledger '<fragment>'` reads that fragment and nothing else —
never `seal/ledger.md`, where the rows with the longest reach live. Issue #153
measured what that costs: one work item's three review rounds and two fix
passes all ran the scoped form and all reported ok, and the unscoped read at
the pull request found fifteen drifted rows and one broken claim, every one in
a file the branch had touched.

The guidance half of the answer is pinned in
`tests/test_the_handoff_names_the_form_it_ran.py`. Guidance binds a session
that reads it, and the session this trap was sprung on narrowed the command on
its own initiative — so the tool announces its own narrowing as well, and what
is here is that: a fixture repository, the checker run on it, and the line it
prints read back.

Every case here was seen red at `23c7ccb`, before the line existed.
"""

import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")

SERVICE = "def handler(x):\n    return x + 1\n"
# `handler`'s body, hashed the way the checker hashes it. Pinned rather than
# computed, so a fixture cannot agree with a broken hasher.
GOOD = "9207ed06"


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
    return " ".join(read(*parts).split())


@pytest.fixture
def proj(tmp_path):
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    return d


def ledger(proj, body, at="seal/ledger.md"):
    path = proj / at
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# map\n\n" + body, encoding="utf-8")
    return path


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def test_the_hash_in_this_files_fixtures_is_the_real_one(proj):
    """Pinned rather than computed: a fixture that asks the checker for its
    own expected value agrees with a broken checker."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_a_narrowed_run_names_the_shared_ledger_it_did_not_read(proj):
    """The case #153 is about. The fragment is clean, the shared ledger is
    broken, and the scoped run exits 0 — so the only thing that can tell
    anyone is the run saying what it skipped."""
    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n")
    (proj / "SPEC.md").write_text(
        f"| POL-1 | `src/service.py#handler@{GOOD}` |\n", encoding="utf-8"
    )
    r = run(["--ledger", "SPEC.md", "."], proj)
    assert r.returncode == 0, r.stdout
    assert "--ledger narrowed this run" in r.stdout, r.stdout
    assert "not read" in r.stdout, r.stdout
    assert os.path.join("seal", "ledger.md") in r.stdout, (
        "the run reports a clean SPEC.md and never names the ledger it "
        "skipped — which reads exactly like a repository with one ledger"
    )
    assert "run without --ledger" in r.stdout, (
        "naming the skipped file without naming the way to read it leaves "
        "the reader where the narrowing put them"
    )
    assert "gone" not in r.stdout, (
        "the skipped ledger was actually READ — the notice is a report on "
        "what was skipped, not a second pass over it"
    )


def test_every_skipped_ledger_is_named_not_counted(proj):
    """A count is not a coordinate. The reader has to open the files, and
    `2 ledgers were not read` names none of them."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    ledger(
        proj,
        f"| POL-2 | `src/service.py#handler@{GOOD}` |\n",
        at="seal/ledger/1788486395-other.md",
    )
    (proj / "SPEC.md").write_text(
        f"| POL-3 | `src/service.py#handler@{GOOD}` |\n", encoding="utf-8"
    )
    r = run(["--ledger", "SPEC.md", "."], proj)
    assert "2 ledgers" in r.stdout, r.stdout
    assert os.path.join("seal", "ledger.md") in r.stdout, r.stdout
    assert os.path.join("seal", "ledger", "1788486395-other.md") in r.stdout, r.stdout


def test_the_notice_counts_one_ledger_in_the_singular(proj):
    """`1 ledgers` is the tell that nobody read the line they shipped."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    (proj / "SPEC.md").write_text(
        f"| POL-2 | `src/service.py#handler@{GOOD}` |\n", encoding="utf-8"
    )
    r = run(["--ledger", "SPEC.md", "."], proj)
    assert "1 ledger " in r.stdout and "1 ledgers" not in r.stdout, r.stdout
    assert "was not read" in r.stdout, r.stdout


def test_an_unnarrowed_run_says_nothing_about_skipping(proj):
    """The line is a report on a narrowing. A run that narrowed nothing has
    nothing to report, and printing it anyway trains people past it."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["."], proj)
    assert "were not read" not in r.stdout and "was not read" not in r.stdout, r.stdout


def test_a_narrowing_that_skips_nothing_says_nothing(proj):
    """`--ledger seal/ledger.md` on a repository holding only that file read
    everything there was. A notice there would be false."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["--ledger", "seal/ledger.md", "."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout
    assert "not read" not in r.stdout, r.stdout


def test_a_second_spelling_of_the_same_file_is_not_reported_as_skipped(proj):
    """`--ledger ./seal/ledger.md` names the file the resolver would have
    opened, spelled with a `./` in front — which is what a person types. Two
    paths compared as raw strings are two files, so the run would report the
    ledger it had just read as one it skipped: a false notice, on the one run
    that narrowed nothing."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["--ledger", os.path.join(".", "seal", "ledger.md"), "."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout
    assert "not read" not in r.stdout, r.stdout


def test_the_notice_survives_a_narrowing_that_matches_nothing(proj):
    """The worst silence of the set. `--ledger` with a typo in it matches no
    file, the run says `no evidence ledgers found` and exits 0, and the
    repository's real ledgers are sitting right there."""
    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n")
    r = run(["--ledger", "TYPO.md", "."], proj)
    assert r.returncode == 0, r.stdout
    assert "no evidence ledgers found" in r.stdout, r.stdout
    assert os.path.join("seal", "ledger.md") in r.stdout, (
        "a narrowing that matched nothing reported an empty repository, "
        "which is the same sentence a repository with no ledger gets"
    )


def test_the_notice_reaches_a_reverify_run(proj):
    """`--reverify` is the run the narrowing exists FOR, so it is the run
    most likely to be narrowed and the one whose skipped set matters most:
    every row it did not re-stamp stays whatever it was."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    (proj / "SPEC.md").write_text(
        f"| POL-2 | `src/service.py#handler@{GOOD}` |\n", encoding="utf-8"
    )
    r = run(["--ledger", "SPEC.md", "--reverify", "."], proj)
    assert r.returncode == 0, r.stdout
    assert os.path.join("seal", "ledger.md") in r.stdout, (
        "the write that the narrowing exists to bound does not say what it left alone"
    )


def test_the_skill_documents_the_line_the_tool_prints():
    """A message a person reads and acts on, documented where the flag is
    documented. Without it the line is a fact about one release."""
    skill = flat("skills", "evidence-check", "SKILL.md")
    assert "which ledgers it did not read" in skill, (
        "`--ledger` is documented and its announcement is not, so the next "
        "edit to the message has nothing to check itself against"
    )
