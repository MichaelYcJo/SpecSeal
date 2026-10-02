"""The installer puts the git hooks where git runs them, owns only what it
wrote, and says what it did once (#692, phase 2: S12, P1, P2).

Every repository here is a fixture under `tmp_path`. The installer is driven
in-process and the stubs it writes run under real git, so what is pinned is
what git does with them -- not what a reading of the stub says it would do.
The stubs point at this checkout's `hooks/git/`, which is the installed
plugin's layout one directory over.
"""

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import load_hook_module

HOOKS_DIR = Path(__file__).resolve().parent.parent / "hooks"
sys.path.insert(0, str(HOOKS_DIR))
import githooks  # noqa: E402  -- the plain name the installer imports

install_mod = load_hook_module("hook-install.py", "hook_install_under_test")

GIT_ENV = {
    "GIT_AUTHOR_NAME": "x",
    "GIT_AUTHOR_EMAIL": "x@example.com",
    "GIT_COMMITTER_NAME": "x",
    "GIT_COMMITTER_EMAIL": "x@example.com",
    "GIT_CONFIG_NOSYSTEM": "1",
}


def env(**extra):
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update(GIT_ENV)
    e.update(extra)
    return e


def g(d, *args, check=True, **extra):
    return subprocess.run(
        ["git", "-C", str(d), *args],
        capture_output=True,
        text=True,
        check=check,
        env=env(**extra),
        stdin=subprocess.DEVNULL,
        timeout=60,
    )


@pytest.fixture(autouse=True)
def _installer_writes(git_hooks_installed):
    """Every case here is about the installer, so it is let write."""


@pytest.fixture
def home(tmp_path, monkeypatch):
    """A HOME of the case's own, so a person's global `core.hooksPath` never
    reaches a fixture."""
    h = tmp_path / "home"
    h.mkdir()
    monkeypatch.setenv("HOME", str(h))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(h / ".config"))
    return h


def repo(path, opted_in=True):
    path.mkdir(parents=True)
    g(path, "init", "-q")
    g(path, "symbolic-ref", "HEAD", "refs/heads/main")
    g(path, "config", "commit.gpgsign", "false")
    (path / "f").write_text("1\n", encoding="utf-8")
    if opted_in:
        # Committed, as a shared-mode root is, so every worktree carries it.
        (path / "seal").mkdir()
        (path / "seal" / "README.md").write_text("root\n", encoding="utf-8")
    g(path, "add", ".")
    g(path, "commit", "-q", "-m", "init")
    return path


def hooks_of(r):
    return Path(r) / ".git" / "hooks"


def stubs_in(directory):
    return sorted(
        h
        for h in githooks.HOOKS
        if (Path(directory) / h).exists()
        and githooks.read_stub(str(Path(directory) / h))[0]
    )


def test_the_stubs_land_in_the_common_hooks_directory_from_a_linked_worktree(
    tmp_path, home
):
    r = repo(tmp_path / "r")
    wt = tmp_path / "wt"
    g(r, "worktree", "add", "-q", str(wt), "-b", "side")
    said = install_mod.install(str(wt), "s1")
    directory = hooks_of(r)
    assert stubs_in(directory) == sorted(githooks.HOOKS)
    for hook in githooks.HOOKS:
        p = directory / hook
        # Asked as `decides` asks it. Windows keeps no execute bit, and git
        # there runs a hook without one, so the mode is POSIX's question (#692).
        assert os.access(p, os.X_OK)
        lines = p.read_text(encoding="utf-8").splitlines()
        assert lines[0] == "#!/bin/sh"
        assert lines[1] == f"{githooks.MARKER} {githooks.plugin_version()}"
        assert githooks.read_stub(str(p))[2] == str(HOOKS_DIR / "git" / f"{hook}.py")
    assert said == (
        f"SpecSeal installed its git hooks in {directory}: pre-commit, "
        "reference-transaction and post-commit. From here on git itself judges a "
        "commit in this clone, inside the commit, instead of a reading of the "
        "command before it runs. Each file carries the line `# specseal-git-hook`, "
        "and a hook file without it is never touched."
    )
    assert githooks.decides(str(wt))
    assert githooks.decides(str(r))


def test_a_second_call_writes_nothing_and_says_nothing(tmp_path, home):
    r = repo(tmp_path / "r")
    install_mod.install(str(r), "s1")
    before = {h: (hooks_of(r) / h).stat().st_mtime_ns for h in githooks.HOOKS}
    assert install_mod.install(str(r), "s1") == ""
    assert install_mod.install(str(r), "s2") == ""
    assert before == {h: (hooks_of(r) / h).stat().st_mtime_ns for h in githooks.HOOKS}


def test_a_stub_an_older_plugin_wrote_is_rewritten_and_said_as_updated(tmp_path, home):
    r = repo(tmp_path / "r")
    for hook in githooks.HOOKS:
        p = hooks_of(r) / hook
        p.write_text(githooks.stub_text(hook, version="0.0.1"), encoding="utf-8")
        p.chmod(0o755)
    said = install_mod.install(str(r), "s1")
    assert said.startswith(f"SpecSeal updated its git hooks in {hooks_of(r)}:")
    for hook in githooks.HOOKS:
        assert (
            githooks.read_stub(str(hooks_of(r) / hook))[1] == githooks.plugin_version()
        )


def test_a_stub_whose_plugin_path_is_gone_is_rewritten(tmp_path, home):
    r = repo(tmp_path / "r")
    gone = tmp_path / "old-plugin"
    for hook in githooks.HOOKS:
        p = hooks_of(r) / hook
        p.write_text(githooks.stub_text(hook, root=str(gone)), encoding="utf-8")
        p.chmod(0o755)
    assert not githooks.decides(str(r))
    install_mod.install(str(r), "s1")
    assert githooks.decides(str(r))


FOREIGN_TAIL = (
    ", and a hooks slot somebody else holds is never written over. Commits in "
    "this clone are judged as SpecSeal 0.16.0 judged them, by reading each "
    "command before it runs. This is said once per session."
)


def test_core_hooks_path_makes_the_clone_foreign(tmp_path, home):
    r = repo(tmp_path / "r")
    g(r, "config", "core.hooksPath", ".husky")
    said = install_mod.install(str(r), "s1")
    assert stubs_in(hooks_of(r)) == []
    assert said == (
        f"SpecSeal installed no git hooks in {r}: core.hooksPath is set to .husky"
        + FOREIGN_TAIL
    )
    assert install_mod.install(str(r), "s1") == ""
    assert install_mod.install(str(r), "s2") == said
    assert not githooks.decides(str(r))


def test_a_hooks_path_set_after_the_stubs_turns_git_off(tmp_path, home):
    """The stubs are still on disk, and git no longer runs them."""
    r = repo(tmp_path / "r")
    install_mod.install(str(r), "s1")
    assert githooks.decides(str(r))
    g(r, "config", "core.hooksPath", ".husky")
    assert not githooks.decides(str(r))


def test_a_stub_put_back_alone_leaves_its_neighbours_untouched(tmp_path, home):
    r = repo(tmp_path / "r")
    install_mod.install(str(r), "s1")
    (hooks_of(r) / "post-commit").unlink()
    others = {
        h: (hooks_of(r) / h).stat().st_mtime_ns
        for h in githooks.HOOKS
        if h != "post-commit"
    }
    install_mod.install(str(r), "s2")
    assert (hooks_of(r) / "post-commit").exists()
    assert others == {h: (hooks_of(r) / h).stat().st_mtime_ns for h in others}


def test_a_global_hooks_path_is_foreign_too(tmp_path, home):
    r = repo(tmp_path / "r")
    subprocess.run(
        ["git", "config", "--global", "core.hooksPath", str(tmp_path / "mine")],
        check=True,
        env=env(),
        timeout=60,
    )
    assert "core.hooksPath is set to" in install_mod.install(str(r), "s1")
    assert stubs_in(hooks_of(r)) == []


def test_a_hook_file_without_the_marker_is_never_touched(tmp_path, home):
    r = repo(tmp_path / "r")
    install_mod.install(str(r), "s1")
    theirs = hooks_of(r) / "pre-commit"
    theirs.write_text("#!/bin/sh\necho mine\n", encoding="utf-8")
    said = install_mod.install(str(r), "s2")
    assert theirs.read_text(encoding="utf-8") == "#!/bin/sh\necho mine\n"
    # Ours are taken out, so git and the text fallback never both judge.
    assert stubs_in(hooks_of(r)) == []
    assert said == f"SpecSeal installed no git hooks in {r}: {theirs}" + FOREIGN_TAIL
    assert not githooks.decides(str(r))


def test_a_sample_hook_is_not_a_foreign_slot(tmp_path, home):
    r = repo(tmp_path / "r")
    assert (hooks_of(r) / "pre-commit.sample").exists()
    install_mod.install(str(r), "s1")
    assert stubs_in(hooks_of(r)) == sorted(githooks.HOOKS)


@pytest.mark.parametrize("why", ["no seal root", "scratch marker"])
def test_a_clone_that_does_not_opt_in_gets_nothing_and_loses_ours(tmp_path, home, why):
    r = repo(tmp_path / "r")
    install_mod.install(str(r), "s1")
    assert stubs_in(hooks_of(r)) == sorted(githooks.HOOKS)
    if why == "no seal root":
        (r / "seal" / "README.md").unlink()
        (r / "seal").rmdir()
    else:
        (r / ".git" / "specseal-scratch").write_text("", encoding="utf-8")
    assert install_mod.install(str(r), "s2") == ""
    assert stubs_in(hooks_of(r)) == []
    never = repo(tmp_path / "never", opted_in=False)
    assert install_mod.install(str(never), "s1") == ""
    assert stubs_in(hooks_of(never)) == []


def test_an_empty_cwd_writes_nowhere(tmp_path, home, monkeypatch):
    r = repo(tmp_path / "r")
    monkeypatch.chdir(r)
    assert install_mod.install("", "s1") == ""
    assert stubs_in(hooks_of(r)) == []


def test_the_suites_switch_writes_nothing(tmp_path, home, monkeypatch):
    """The seam `tests/conftest.py` sets for every other case."""
    r = repo(tmp_path / "r")
    monkeypatch.setenv(install_mod.SWITCH, "off")
    assert install_mod.install(str(r), "s1") == ""
    assert stubs_in(hooks_of(r)) == []


def test_main_says_it_as_a_system_message(tmp_path, home, monkeypatch, capsys):
    import io

    r = repo(tmp_path / "r")
    payload = {"tool_name": "Bash", "cwd": str(r), "session_id": "s1"}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    install_mod.main()
    out = json.loads(capsys.readouterr().out)
    assert out["systemMessage"].startswith("SpecSeal installed its git hooks in")


# --- what the stub itself decides, under real git ---------------------------


def fake_plugin(tmp_path, body):
    """A plugin root whose entry points print `ran <hook>` and do BODY."""
    root = tmp_path / "plugin"
    (root / "hooks" / "git").mkdir(parents=True)
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text(
        '{"version": "9.9.9"}', encoding="utf-8"
    )
    for hook in githooks.HOOKS:
        (root / "hooks" / "git" / f"{hook}.py").write_text(
            "import sys\n"
            f"sys.stderr.write('ran {hook}\\n')\n"
            "sys.stdin.read() if not sys.stdin.isatty() else None\n" + body,
            encoding="utf-8",
        )
    return root


def put_stubs(r, root):
    for hook in githooks.HOOKS:
        p = hooks_of(r) / hook
        p.write_text(githooks.stub_text(hook, root=str(root)), encoding="utf-8")
        p.chmod(0o755)


def commit(r, **extra):
    (Path(r) / "f").write_text(os.urandom(4).hex(), encoding="utf-8")
    g(r, "add", "f")
    return g(r, "commit", "-q", "-m", "x", check=False, **extra)


def test_a_session_commit_runs_the_entry_point(tmp_path, home):
    r = repo(tmp_path / "r")
    put_stubs(r, fake_plugin(tmp_path, "sys.exit(1)\n"))
    got = commit(r, CLAUDE_CODE_SESSION_ID="s1")
    assert got.returncode != 0
    assert "ran pre-commit" in got.stderr


def test_a_persons_commit_starts_no_python(tmp_path, home):
    """P2, answer (a): no session variable and no lease anywhere in the clone
    is a person's own commit, and the stub leaves before an interpreter."""
    r = repo(tmp_path / "r")
    put_stubs(r, fake_plugin(tmp_path, "sys.exit(1)\n"))
    got = commit(r)
    assert got.returncode == 0, got.stderr
    assert "ran" not in got.stderr


def test_a_lease_in_any_worktree_of_the_clone_starts_python(tmp_path, home):
    """S9's second route needs Python even with no variable exported."""
    r = repo(tmp_path / "r")
    wt = tmp_path / "wt"
    g(r, "worktree", "add", "-q", str(wt), "-b", "side")
    put_stubs(r, fake_plugin(tmp_path, "sys.exit(1)\n"))
    leases = r / ".git" / "worktrees" / "wt" / "specseal-leases"
    leases.mkdir()
    (leases / "s1").write_text('{"pid": 1}', encoding="utf-8")
    got = commit(r)
    assert got.returncode != 0
    assert "ran pre-commit" in got.stderr


def test_an_emptied_lease_directory_starts_no_python(tmp_path, home):
    """Round 1's 🟡 11: `hooks/session-lease.py` prunes lease files and never
    the directory, so a person's commit in every clone a session once used
    paid the interpreter starts P2 meant to spare it (396 ms against 125)."""
    r = repo(tmp_path / "r")
    put_stubs(r, fake_plugin(tmp_path, "sys.exit(1)\n"))
    (r / ".git" / "specseal-leases").mkdir()
    got = commit(r)
    assert got.returncode == 0, got.stderr
    assert "ran" not in got.stderr


@pytest.mark.skipif(os.name == "nt", reason="no execute bit to take away")
def test_a_stub_git_cannot_run_is_written_again_and_decides_nothing_till_then(
    tmp_path, home
):
    """Round 1's 🟡 3: git skips a hook it cannot execute, so a stub with the
    right bytes and the wrong mode is no stub."""
    r = repo(tmp_path / "r")
    install_mod.install(str(r), "s1")
    stub = hooks_of(r) / "reference-transaction"
    stub.chmod(0o644)
    assert not githooks.decides(str(r))
    install_mod.install(str(r), "s1")
    assert stub.stat().st_mode & stat.S_IXUSR
    assert githooks.decides(str(r))


def test_a_stub_whose_entry_point_is_gone_does_nothing(tmp_path, home):
    r = repo(tmp_path / "r")
    put_stubs(r, tmp_path / "uninstalled")
    assert commit(r, CLAUDE_CODE_SESSION_ID="s1").returncode == 0


def test_reference_transaction_starts_python_only_for_a_commit(tmp_path, home):
    """M12: only `git commit` hands the hook GIT_AUTHOR_DATE."""
    r = repo(tmp_path / "r")
    root = fake_plugin(tmp_path, "sys.exit(1)\n")
    put_stubs(r, root)
    (root / "hooks" / "git" / "pre-commit.py").write_text("", encoding="utf-8")
    s = {"CLAUDE_CODE_SESSION_ID": "s1"}
    assert g(r, "branch", "b1", check=False, **s).returncode == 0
    assert g(r, "update-ref", "refs/heads/b2", "HEAD", check=False, **s).returncode == 0
    got = commit(r, **s)
    assert got.returncode != 0
    assert "ran reference-transaction" in got.stderr


def test_the_installed_hooks_let_a_commit_through_where_nothing_is_missing(
    tmp_path, home
):
    """The stubs end to end, through the installed entry points: a reviewed
    HEAD is a commit with nothing missing. What they refuse is
    `tests/test_the_commit_gate_decides_at_the_commit.py`'s."""
    r = repo(tmp_path / "r")
    install_mod.install(str(r), "s1")
    head = g(r, "rev-parse", "HEAD").stdout.strip()
    (r / ".git" / "specseal-reviewed").write_text(head, encoding="utf-8")
    assert commit(r, CLAUDE_CODE_SESSION_ID="s1").returncode == 0
