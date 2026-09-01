"""The pre-anchor ledger migrates itself at session start, once per repo.

`claude plugin update` is the whole of what a user does. The philosophy is the
repository's own, stated in CLAUDE.md: between two designs that catch the same
thing, the one that stops to ask a person is the more expensive — and
`--migrate` as a command a person must remember to run is that more expensive
design. The command survives for CI and for anyone who wants it by hand; this
hook removes the remembering.

What licenses a hook writing to a tree unasked: the ledger is the plugin's own
artifact — the same ownership that lets `preset-setup` replace the CLAUDE.md
marker block — and the operation is deterministic, idempotent, all-or-nothing
per row, fully visible in `git diff`, with the old text safe in git history.

Every case here is about the boundaries: never over uncommitted work, never
twice, never at check time, silent when there is nothing to do.
"""

import io
import json
import os
import subprocess
import sys

import pytest
from conftest import load_hook_module

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

OLD_SERVICE = "def handler(x):\n    return x + 1\n\n\ndef other():\n    return 0\n"


@pytest.fixture
def hook(tmp_path):
    mod = load_hook_module("ledger-migrate.py", "ledger_migrate")
    mod.STATE_DIR = str(tmp_path / "state")
    mod.MARKER = os.path.join(mod.STATE_DIR, "ledger-migrated")
    return mod


@pytest.fixture
def repo(tmp_path):
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / ".specseal" / "map").mkdir(parents=True)
    git = lambda *a: subprocess.run(
        ["git", "-C", str(d), *a], check=True, capture_output=True, encoding="utf-8"
    )
    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    (d / "src" / "service.py").write_text(OLD_SERVICE)
    (d / ".specseal" / "map" / "f.md").write_text(
        "# map\n\n"
        "| A | `src/service.py:1-2` | 2026-08-31 `9829412` |\n"
        "| B | `src/service.py:999` | 2026-08-31 |\n"
    )
    git("add", "-A")
    git("commit", "-qm", "an old-format ledger, committed")
    return d


def start(hook, repo):
    """One session start; returns what the hook printed."""
    out = io.StringIO()
    stdin, stdout = sys.stdin, sys.stdout
    sys.stdin = io.StringIO(json.dumps({"cwd": str(repo)}))
    sys.stdout = out
    try:
        hook.main()
    finally:
        sys.stdin, sys.stdout = stdin, stdout
    return out.getvalue()


def test_the_first_session_start_migrates_and_says_so_in_one_line(hook, repo):
    out = start(hook, repo)
    assert "ledger migrated to anchor format" in out, out
    assert "1 row" in out and "1 left" in out, out
    assert "review the diff and commit" in out, out
    ledger = (repo / ".specseal" / "map" / "f.md").read_text()
    assert "src/service.py#handler@" in ledger, ledger
    assert "src/service.py:1-2" not in ledger, ledger
    assert "src/service.py:999" in ledger, "the unprovable row was guessed at"
    assert "`9829412`" not in ledger, "the stamp survived on the migrated row"


def test_the_second_session_start_is_silent(hook, repo):
    """Once per repo. The attempt stamps a marker, so a repository whose left
    rows persist is not re-nagged every morning — the ordinary check's
    OLD-FORMAT failure is the loud backstop that remains."""
    start(hook, repo)
    assert start(hook, repo) == "", "the second session start spoke"


def test_uncommitted_ledger_changes_are_never_overwritten(hook, repo):
    """Work in progress outranks the migration. The skip says why, the marker
    is NOT stamped — so the next session with a clean tree migrates — and the
    OLD-FORMAT failure stays loud in between."""
    ledger = repo / ".specseal" / "map" / "f.md"
    ledger.write_text(ledger.read_text() + "| C | someone's half-written row |\n")
    before = ledger.read_text()
    out = start(hook, repo)
    assert "uncommitted" in out, out
    assert ledger.read_text() == before, "the hook overwrote work in progress"

    subprocess.run(
        ["git", "-C", str(repo), "commit", "-qam", "the wip lands"],
        check=True,
        capture_output=True,
    )
    out = start(hook, repo)
    assert "ledger migrated to anchor format" in out, (
        f"the skip stamped the marker, so a clean tree never migrated:\n{out}"
    )


def test_a_clean_ledger_says_nothing(hook, repo):
    ledger = repo / ".specseal" / "map" / "f.md"
    ledger.write_text("# map\n\n| A | `src/service.py#handler@00000000` |\n")
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-qam", "already anchored"],
        check=True,
        capture_output=True,
    )
    assert start(hook, repo) == ""


def test_a_scratch_repo_is_left_alone_even_with_an_old_ledger(hook, repo):
    """`.specseal/scratch` takes the opt-in back, and it is the only way a
    repository can HOLD a ledger while not being opted in — `.specseal/`
    existing is the opt-in itself. Found by mutation: a fixture with no
    ledger at all passed whether or not the opt-in was consulted."""
    (repo / ".specseal" / "scratch").write_text("")
    before = (repo / ".specseal" / "map" / "f.md").read_text()
    assert start(hook, repo) == ""
    assert (repo / ".specseal" / "map" / "f.md").read_text() == before


def test_a_git_that_cannot_answer_reads_as_dirty(hook, repo, monkeypatch):
    """Overwriting on a guess is the one direction this hook must never fail
    in, so an unanswerable `git status` is treated as work in progress."""
    monkeypatch.setattr(
        hook.subprocess,
        "run",
        lambda *a, **k: (_ for _ in ()).throw(OSError("no git")),
    )
    assert hook.dirty(str(repo), [str(repo / ".specseal" / "map" / "f.md")])


def test_the_plain_checker_still_never_rewrites(repo):
    """Reading never rewrites — session start is the write moment, and the
    checker stays pure. Held here beside the hook so the pair is one read."""
    EC = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")
    before = (repo / ".specseal" / "map" / "f.md").read_text()
    subprocess.run(
        [sys.executable, EC, "."], cwd=str(repo), capture_output=True, encoding="utf-8"
    )
    assert (repo / ".specseal" / "map" / "f.md").read_text() == before


def test_the_hook_is_wired_into_session_start(hook):
    """The dispatch group is the only thing that runs hooks in production; a
    hook not named there is dead code with passing tests."""
    dispatch = load_hook_module("dispatch.py", "dispatch_for_migrate")
    assert "ledger-migrate.py" in dispatch.GROUPS["session-start"]
