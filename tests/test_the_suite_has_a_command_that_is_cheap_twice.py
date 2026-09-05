"""The repository ships a command for its own suite, and the second call is cheap.

Issue #156. The issue says nothing names a command; that half is wrong --
`CONTRIBUTING.md` §*Running the checks* named `uvx --with pytest python3 -m
pytest tests/ -q`. What it did not have is a command that is cheap the second
time it runs: that form resolves its environment on every call, 55-58 seconds
each, paid on all seventeen test calls of one measured segment (#133). Six
`bin/` pairs now exist and `test` is the sixth.

This file pins the four things that decide whether the command still works in
six months, none of which the diff shows on its own:

  - it is a sibling, not a special case -- both wrappers, the same path
    resolution as the five before it;
  - a warm call reuses the environment and never rebuilds it, which is the
    whole work item;
  - the virtualenv it writes is invisible to git, whichever of the two tools
    built it (`uv venv` writes the ignore, `python -m venv` does not);
  - every way of failing produces a sentence, not a traceback. The runner
    writes to the working tree, so a machine with neither `uv` nor a new
    enough Python has to be told what to install.

The sentences are pinned because a person reads them and acts on them, which
is the only reason they exist.
"""

import importlib.util
import os
import pathlib
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIN = os.path.join(ROOT, "bin")
SCRIPT = os.path.join(ROOT, ".github", "scripts", "run_tests.py")


def _load_runner():
    spec = importlib.util.spec_from_file_location("specseal_run_tests", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rt = _load_runner()


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def posix_entries():
    """Every `bin/` wrapper that is not the Windows twin."""
    return sorted(n for n in os.listdir(BIN) if not n.endswith(".cmd"))


def fake_venv(root):
    """A directory that looks to `has_pytest` like a built environment."""
    venv = root / ".venv"
    python = rt.venv_python(venv)
    python.parent.mkdir(parents=True)
    python.write_text("")
    (python.parent / ("pytest.exe" if os.name == "nt" else "pytest")).write_text("")
    return venv


class Recorder:
    """Stands in for `subprocess.run`; records commands, never runs one."""

    def __init__(self, returncode=0):
        self.calls = []
        self.kwargs = []
        self.returncode = returncode

    def __call__(self, command, **kwargs):
        self.calls.append(list(command))
        self.kwargs.append(kwargs)
        return subprocess.CompletedProcess(command, self.returncode)


class FakeSys:
    """An interpreter below the floor, without touching the real `sys`.

    `stderr` is looked up when it is asked for, not when this class is
    defined: capsys replaces `sys.stderr` per test, and a captured-at-import
    handle would send the sentences past the capture — leaving the cases that
    read them unable to fail.
    """

    version_info = (3, 9, 6)
    version = "3.9.6 (main, Jan 1 2026)"
    executable = "/usr/bin/python3"

    @property
    def stderr(self):
        return sys.stderr


# --- it is a sibling, not a special case -----------------------------------


def test_both_wrappers_ship_and_point_at_the_runner():
    """`bin/` is on the Bash tool's PATH while the plugin is enabled, and
    cmd.exe resolves the `.cmd` twin through PATHEXT. A new command means both
    files or it means one platform."""
    posix = os.path.join(BIN, "test")
    windows = os.path.join(BIN, "test.cmd")
    assert os.path.isfile(posix), "bin/test missing"
    assert os.path.isfile(windows), "bin/test.cmd missing"
    assert ".github/scripts/run_tests.py" in read(posix)
    text = read(windows)
    assert ".github\\scripts\\run_tests.py" in text
    assert "py -3" in text and "python " in text, (
        "the .cmd twin prefers `py -3` and falls back to `python`"
    )


def test_every_bin_entry_has_a_windows_twin():
    """The rule the five earlier pairs follow, asked of all of them at once:
    the sixth entry is where a lone POSIX wrapper would have arrived."""
    missing = [n for n in posix_entries() if not os.path.isfile(f"{BIN}/{n}.cmd")]
    assert not missing, f"{missing} ship without a .cmd twin — Windows loses them"


@pytest.mark.parametrize("entry", posix_entries())
def test_every_posix_wrapper_resolves_its_own_directory(entry):
    """A wrapper that resolves against the caller's cwd works from the
    repository root and nowhere else, which is the failure a session hits
    from a subdirectory."""
    text = read(os.path.join(BIN, entry))
    assert 'here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)' in text, (
        f"bin/{entry} does not resolve its own directory the way its siblings do"
    )
    assert '"$@"' in text, f"bin/{entry} does not pass its arguments through"


def test_the_wrapper_points_at_the_contract_rather_than_inviting_a_full_run():
    """`bin/test` with no arguments runs a five-minute suite that
    `skills/agent-contract/SKILL.md` §2 forbids to smith and warden. The file
    a session reads before typing it says so, and names where the rule is."""
    text = read(os.path.join(BIN, "test"))
    assert "agent-contract" in text and "orchestrator" in text, (
        "bin/test no longer says the full suite is the orchestrator's, so a "
        "segment reading it has nothing telling it not to"
    )


@pytest.mark.skipif(os.name == "nt", reason="the POSIX wrapper needs a POSIX shell")
def test_a_copy_without_the_runner_beside_it_says_so(tmp_path):
    """`bin/` reaches a user's machine and `.github/` does not, so a plugin
    user's copy of this wrapper finds no runner. That has to be a sentence:
    `python3 <missing path>` is a traceback about a file the reader never
    named."""
    copy = tmp_path / "bin"
    copy.mkdir()
    (copy / "test").write_text(read(os.path.join(BIN, "test")), encoding="utf-8")
    (copy / "test").chmod(0o755)
    result = subprocess.run(
        [str(copy / "test")], capture_output=True, encoding="utf-8", errors="replace"
    )
    assert result.returncode == 2, result
    assert "no runner beside it" in result.stderr, result.stderr
    assert "Traceback" not in result.stderr


# --- the second call is the whole work item --------------------------------


def test_a_built_environment_is_reused_and_never_rebuilt(tmp_path, monkeypatch):
    """The measured cost was setup paid on every call. A warm call must not
    reach the builder at all — not even to ask a tool whether it is current."""
    venv = fake_venv(tmp_path)
    monkeypatch.setattr(
        rt, "build", lambda _: pytest.fail("a warm call rebuilt the environment")
    )
    assert rt.ensure(venv) == rt.venv_python(venv)


def test_a_missing_environment_is_built_once(tmp_path, monkeypatch):
    """And the cold call does reach it, once."""
    built = []

    def build(venv):
        built.append(venv)
        fake_venv(tmp_path)
        return None

    monkeypatch.setattr(rt, "build", build)
    venv = tmp_path / ".venv"
    assert rt.ensure(venv) == rt.venv_python(venv)
    assert built == [venv]


def test_a_build_that_leaves_no_pytest_is_a_sentence(tmp_path, monkeypatch, capsys):
    """A build that reports success and produces nothing usable is the
    half-built state, and the next call would loop through it forever."""
    monkeypatch.setattr(rt, "build", lambda _: None)
    assert rt.ensure(tmp_path / ".venv") is None
    assert "still not in it" in capsys.readouterr().err


# --- invisible to git ------------------------------------------------------


def test_the_environment_hides_itself_from_git(tmp_path):
    """`uv venv` writes this ignore and `python -m venv` does not (checked on
    3.12), so the runner writes it whichever built the directory — otherwise
    the fallback path leaves a virtualenv in every `git status`."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "pyvenv.cfg").write_text("home = /usr/bin\n")
    rt.hide_from_git(venv)
    assert (venv / ".gitignore").read_text().strip() == "*"
    status = subprocess.run(
        ["git", "-C", str(tmp_path), "status", "--porcelain"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout
    assert ".venv" not in status, f"the virtualenv is visible to git: {status!r}"


def test_an_existing_ignore_is_left_alone(tmp_path):
    """`uv venv` wrote one already; overwriting it would be this runner
    editing another tool's file for no gain."""
    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / ".gitignore").write_text("*\n# written by uv\n")
    rt.hide_from_git(venv)
    assert "written by uv" in (venv / ".gitignore").read_text()


# --- a sentence, not a traceback -------------------------------------------


def test_neither_tool_available_names_what_to_install(monkeypatch):
    """The failure to design against: the first call writes to the tree, and a
    machine with no `uv` and macOS's 3.9 under the name `python3` has to be
    told which of the two to fix."""
    monkeypatch.setattr(rt.shutil, "which", lambda _: None)
    monkeypatch.setattr(rt, "sys", FakeSys())
    sentence = rt.build("/nowhere/.venv")
    assert sentence, "no sentence at all — the caller sees a half-built directory"
    assert sentence.startswith("bin/test"), (
        "the sentence has to name the command it is about: the reader typed "
        "bin/test and the runner it reaches has a name they never saw"
    )
    assert "uv" in sentence
    assert "3.12" in sentence, "the floor is what makes the interpreter wrong"
    assert "3.9.6" in sentence, "a reader cannot check a floor without the version"


def test_a_failing_build_step_is_a_sentence(tmp_path, monkeypatch, capsys):
    """A tool that is present and fails — no network, a broken uv — must not
    leave the caller reading exit codes. And the note that a build is starting
    names the tool, so a first call that pauses for a minute is legible."""
    monkeypatch.setattr(rt.shutil, "which", lambda _: "/usr/bin/uv")
    monkeypatch.setattr(rt.subprocess, "run", Recorder(returncode=1))
    sentence = rt.build(tmp_path / ".venv")
    assert sentence and "could not build" in sentence
    assert "run bin/test again" in sentence
    assert "building" in capsys.readouterr().err


def test_nothing_announces_a_build_that_cannot_happen(monkeypatch, capsys):
    """The note printed before the strategy was chosen, so the machine with
    neither tool was told a build was starting and then told it was
    impossible. Measured on 3.9.6 with no uv, before the note moved."""
    monkeypatch.setattr(rt.shutil, "which", lambda _: None)
    monkeypatch.setattr(rt, "sys", FakeSys())
    assert rt.ensure(pathlib.Path("/nowhere/.venv")) is None
    err = capsys.readouterr().err
    assert "building" not in err, "a build was announced that could not happen"
    assert "Install uv" in err


def test_a_tree_without_a_suite_is_a_sentence(tmp_path, monkeypatch, capsys):
    """The shipped-copy case again, one level in: a runner that reaches a tree
    with no `tests/` says so rather than handing pytest an empty argument."""
    monkeypatch.setattr(rt, "repo_root", lambda: tmp_path)
    assert rt.main([]) == 2
    assert "no tests directory" in capsys.readouterr().err


# --- what it actually runs -------------------------------------------------


def test_arguments_pass_through(tmp_path, monkeypatch):
    (tmp_path / "tests").mkdir()
    venv = fake_venv(tmp_path)
    recorder = Recorder()
    monkeypatch.setattr(rt, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(rt.subprocess, "run", recorder)
    assert rt.main(["tests/test_session_cost.py", "-q"]) == 0
    assert recorder.calls == [
        [str(rt.venv_python(venv)), "-m", "pytest", "tests/test_session_cost.py", "-q"]
    ]


def test_no_arguments_runs_the_whole_suite(tmp_path, monkeypatch):
    (tmp_path / "tests").mkdir()
    fake_venv(tmp_path)
    recorder = Recorder()
    monkeypatch.setattr(rt, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(rt.subprocess, "run", recorder)
    rt.main([])
    assert recorder.calls[0][-1] == "tests"


def test_it_does_not_pass_n_auto(tmp_path, monkeypatch):
    """pytest-xdist is installed by `.github/workflows/test.yml`, not by this
    virtualenv. `-n auto` would fail on every freshly built one, and the fix
    for a caller who wants it is to install xdist and pass it."""
    (tmp_path / "tests").mkdir()
    fake_venv(tmp_path)
    recorder = Recorder()
    monkeypatch.setattr(rt, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(rt.subprocess, "run", recorder)
    rt.main([])
    assert "-n" not in recorder.calls[0], (
        "the built environment has no xdist, so -n auto fails on the first run"
    )


def test_pytest_runs_from_the_repository_root(tmp_path, monkeypatch):
    """So `bin/test tests/x.py` means the same thing from any directory, which
    is the scenario a session hits: it is rarely at the root."""
    (tmp_path / "tests").mkdir()
    fake_venv(tmp_path)
    recorder = Recorder()
    monkeypatch.setattr(rt, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(rt.subprocess, "run", recorder)
    rt.main([])
    assert recorder.kwargs[0]["cwd"] == str(tmp_path)


def test_it_names_the_interpreter_it_used(tmp_path, monkeypatch, capsys):
    """Two virtualenvs on one machine is the ordinary case — a worktree has
    its own — so which one ran the suite is not something to infer."""
    (tmp_path / "tests").mkdir()
    venv = fake_venv(tmp_path)
    monkeypatch.setattr(rt, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(rt.subprocess, "run", Recorder())
    rt.main([])
    assert str(rt.venv_python(venv)) in capsys.readouterr().err


def test_the_exit_code_is_pytests(tmp_path, monkeypatch):
    """A runner that swallows the suite's verdict is a green gate over a red
    suite."""
    (tmp_path / "tests").mkdir()
    fake_venv(tmp_path)
    monkeypatch.setattr(rt, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(rt.subprocess, "run", Recorder(returncode=1))
    assert rt.main([]) == 1


def test_the_root_is_the_repository_not_the_scripts_directory():
    """`.github/scripts/` up two. One level off and the virtualenv lands in
    `.github/`, where nothing looks for it."""
    assert rt.repo_root() == pathlib.Path(ROOT).resolve()
