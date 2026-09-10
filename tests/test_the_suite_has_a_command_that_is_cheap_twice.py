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
import re
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIN = os.path.join(ROOT, "bin")
SCRIPT = os.path.join(ROOT, ".github", "scripts", "run_tests.py")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "test.yml")

# Held before any test can replace `subprocess.run` on the module the runner
# imports: `rt.subprocess` IS this module, so a case that fakes the builder's
# calls fakes the git calls that check what the builder left behind.
REAL_RUN = subprocess.run


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


def test_the_runner_behind_the_wrapper_says_the_same_thing():
    """Round 1's 🟡 7. `bin/test` is five lines and one `exec` into
    `.github/scripts/run_tests.py`.

    #30 re-pointed the wrapper's comment from `orchestrator` to `sealer` and
    left the module it runs saying the other thing — one command, two files,
    two owners, which is the §12 class this branch already knows
    `survivor-check` cannot reach. The changelog claimed *the runner's own
    comment … all of them now say the sealer's*, true of the wrapper and
    false of the runner.

    Nothing pinned this docstring: the case above reads `bin/test`, and the
    negative pin in `tests/test_the_seal_is_taken_once_by_the_sealer.py` is
    applied to the two agent definitions only."""
    runner = read(os.path.join(ROOT, ".github", "scripts", "run_tests.py"))
    assert "is the sealer's, run once after" in runner, (
        "the file `bin/test` execs no longer says whose the full suite is"
    )
    assert "is the orchestrator's" not in runner, (
        "the wrapper and the module it runs name two different owners for one command"
    )


def test_the_wrapper_points_at_the_contract_rather_than_inviting_a_full_run():
    """`bin/test` with no arguments runs a five-minute suite that
    `skills/agent-contract/SKILL.md` §2 forbids to smith and warden. The file
    a session reads before typing it says so, and names where the rule is.

    Re-pointed by #30 from `orchestrator` to `sealer`. The rule forbade the
    run to two agents and assigned it to none, so the comment named the
    participant that happened to take it; naming the agent is what makes the
    sentence readable without knowing who is driving."""
    text = read(os.path.join(BIN, "test"))
    assert "agent-contract" in text and "sealer" in text, (
        "bin/test no longer says the full suite is the sealer's, so a "
        "segment reading it has nothing telling it not to"
    )


@pytest.mark.skipif(os.name == "nt", reason="the POSIX wrapper needs a POSIX shell")
def test_a_copy_without_the_runner_beside_it_says_so(tmp_path):
    """A copy of `bin/` taken on its own — vendored wrappers, a partial
    copy — has no runner beside it. That has to be a sentence: `python3
    <missing path>` is a traceback about a file the reader never named."""
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


def test_both_wrappers_say_the_same_thing_when_the_runner_is_missing():
    """The case above EXECUTES the POSIX wrapper and is skipped on `nt`, so on
    the one platform the `.cmd` twin runs, nothing reads its sentence. It
    shipped with half of one: the reader was told the copy has no runner and
    never told where to get it. This case reads both files, so it runs
    everywhere."""
    posix = read(os.path.join(BIN, "test"))
    windows = read(os.path.join(BIN, "test.cmd"))
    for fragment in (
        "has no runner beside it",
        "Run it from a clone of the SpecSeal repository",
    ):
        assert fragment in posix, f"bin/test no longer says: {fragment}"
        assert fragment in windows, (
            f"bin/test.cmd drops what its POSIX twin tells the reader: {fragment}"
        )


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


def test_an_environment_below_the_floor_is_refused(tmp_path, capsys):
    """`FLOOR` was enforced where the runner BUILDS and nowhere else. A `.venv`
    the runner ADOPTS was accepted on the strength of an interpreter file and a
    `pytest*` script, so a directory left by an older Python -- a contributor's,
    or this repository's own from before the floor moved -- ran the suite on a
    version nothing here supports, and said nothing."""
    venv = fake_venv(tmp_path)
    (venv / "pyvenv.cfg").write_text("version = 3.9.6\n")
    assert rt.ensure(venv) is None
    err = capsys.readouterr().err
    assert "3.9.6" in err, (
        "the sentence does not name the version found, so the reader cannot "
        "check the floor against anything"
    )
    assert f"below the {rt.FLOOR_TEXT} floor" in err
    assert "Remove that directory" in err, (
        "the reader is told the environment is wrong and not what to do about it"
    )
    assert "Traceback" not in err


def test_an_environment_that_says_nothing_about_its_version_is_kept(tmp_path):
    """`pyvenv.cfg` is where both builders record the version, and a directory
    without a readable one is not evidence of an old interpreter -- a venv
    built by something else, or one whose file has been edited. Refusing on
    silence turns one unknown into a suite nobody can run, so only a version
    that is BOTH readable and below the floor is refused."""
    venv = fake_venv(tmp_path)
    assert not (venv / "pyvenv.cfg").exists()
    assert rt.ensure(venv) == rt.venv_python(venv)
    (venv / "pyvenv.cfg").write_text("home = /usr/bin\nprompt = '.venv'\n")
    assert rt.ensure(venv) == rt.venv_python(venv)


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


def git_status(tmp_path):
    """`git status --porcelain`, run through the real `subprocess.run`.

    Saved at import: a test that fakes `rt.subprocess.run` is faking the
    module, so the git call below would be answered by the fake too.
    """
    return REAL_RUN(
        ["git", "-C", str(tmp_path), "status", "--porcelain"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout


def test_a_failed_build_still_leaves_no_trace_in_git(tmp_path, monkeypatch):
    """The ignore was written after the LAST step succeeded, so the one run
    that ends in a sentence was the run that left a virtualenv behind. The
    install step is what fails on a machine with no network, and it fails
    after `uv venv` has already made the directory."""
    REAL_RUN(["git", "init", "-q", str(tmp_path)], check=True)
    venv = tmp_path / ".venv"

    def run(command, **kwargs):
        venv.mkdir(exist_ok=True)  # `uv venv` made the directory
        return subprocess.CompletedProcess(command, 1)  # the install step failed

    monkeypatch.setattr(rt.shutil, "which", lambda _: "/usr/bin/uv")
    monkeypatch.setattr(rt.subprocess, "run", run)
    assert rt.build(venv), "a failing build step still has to return a sentence"
    monkeypatch.undo()
    assert (venv / ".gitignore").read_text().strip() == "*"
    status = git_status(tmp_path)
    assert ".venv" not in status, (
        f"the half-built virtualenv is visible to git: {status!r}"
    )


def test_an_adopted_environment_is_hidden_too(tmp_path):
    """`hide_from_git` ran only at the end of a build, so a `.venv` the runner
    ADOPTS never reached it. That directory is exactly the one with no ignore
    of its own -- `python -m venv` writes none -- and the runner that finds it
    is the one call in its life that could have written one."""
    REAL_RUN(["git", "init", "-q", str(tmp_path)], check=True)
    venv = fake_venv(tmp_path)
    (venv / "pyvenv.cfg").write_text(f"version = {rt.FLOOR_TEXT}.0\n")
    assert rt.ensure(venv) == rt.venv_python(venv)
    assert (venv / ".gitignore").read_text().strip() == "*"
    status = git_status(tmp_path)
    assert ".venv" not in status, (
        f"the adopted virtualenv is visible to git: {status!r}"
    )


def test_a_refused_environment_is_hidden_too(tmp_path):
    """The floor refusal returned one line ABOVE the ignore the fix for the
    case above had just added, so the one adopted `.venv` the runner refuses
    was the one it left in `git status` -- and it is the directory least
    likely to carry an ignore of its own, because every version that refusal
    rejects is older than the 3.13 where `python -m venv` began writing one.
    The reader is told to remove the directory; until they do, it is dirt in
    every `git status` they run."""
    REAL_RUN(["git", "init", "-q", str(tmp_path)], check=True)
    venv = fake_venv(tmp_path)
    (venv / "pyvenv.cfg").write_text("version = 3.11.9\n")
    assert rt.ensure(venv) is None, "a below-floor environment is still refused"
    assert (venv / ".gitignore").read_text().strip() == "*"
    status = git_status(tmp_path)
    assert ".venv" not in status, (
        f"the refused virtualenv is visible to git: {status!r}"
    )


def test_a_directory_no_builder_can_finish_is_hidden_too(tmp_path, monkeypatch):
    """`build` returns its no-tool sentence from the branch ABOVE its own
    `try`, so `build`'s `finally` never runs and a directory that was already
    there is never reached. Held by `ensure`'s `finally` instead, which is
    why the guarantee is stated over exits rather than over a list of paths:
    this one is not a path anybody would have thought to add.

    Reachable, and on the machines least able to notice: a half-built `.venv`
    from an earlier run, then `uv` gone from PATH and macOS's 3.9 answering
    to `python3`."""
    REAL_RUN(["git", "init", "-q", str(tmp_path)], check=True)
    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "pyvenv.cfg").write_text("home = /usr/bin\n")
    monkeypatch.setattr(rt.shutil, "which", lambda _: None)
    monkeypatch.setattr(rt, "sys", FakeSys())
    assert rt.ensure(venv) is None, "a machine with neither tool still refuses"
    monkeypatch.undo()
    assert (venv / ".gitignore").read_text().strip() == "*"
    status = git_status(tmp_path)
    assert ".venv" not in status, (
        f"the unfinishable virtualenv is visible to git: {status!r}"
    )


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


# A `chmod 555` directory stops a write only where the operating system says
# it does. Root is not stopped by a permission bit, and on Windows `os.chmod`
# sets the read-only flag and nothing else -- the flag is ignored when a file
# is created inside a directory. On either, the write below would SUCCEED, the
# sentence would never print, and a case asserting it would fail for a reason
# that has nothing to do with the guard. So the fixture case is skipped there
# and `test_the_unwritable_sentence_is_the_same_on_every_platform` carries the
# wording on all three, by making the write itself refuse.
CHMOD_STOPS_A_WRITE = os.name != "nt" and hasattr(os, "geteuid") and os.geteuid() != 0


@pytest.mark.skipif(
    not CHMOD_STOPS_A_WRITE,
    reason="chmod 555 does not stop a write as root, and on Windows chmod "
    "sets only the read-only flag, which does not stop a file being created "
    "inside the directory",
)
def test_an_unwritable_venv_leaves_the_refusal_a_sentence(
    tmp_path, monkeypatch, capsys
):
    """Round 2 of #156's chain moved `hide_from_git` into `ensure`'s
    `finally`, which is what makes the guarantee exit-level rather than a list
    of remembered paths. It also put an unguarded write on the two exits whose
    entire product is a sentence, so a `.venv` the operator has made read-only
    turned the floor refusal into a `PermissionError` traceback printed after
    it -- the module's opening docstring says every failure here is a sentence
    rather than a traceback, and that was the one that was not.

    The runner does not try to make the write succeed. A read-only `.venv` is
    the operator's, and what they are owed is being told what it costs them."""
    REAL_RUN(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "tests").mkdir()
    venv = fake_venv(tmp_path)
    (venv / "pyvenv.cfg").write_text("version = 3.11.9\n")
    monkeypatch.setattr(rt, "repo_root", lambda: tmp_path)
    venv.chmod(0o555)
    try:
        assert rt.main([]) == 2, "the refusal keeps its own exit code"
        err = capsys.readouterr().err
    finally:
        venv.chmod(0o755)  # or tmp_path cleanup cannot unlink what is inside

    assert "Traceback" not in err, err
    assert "below the" in err and "3.11.9" in err, (
        "the refusal the reader actually needs no longer prints"
    )
    assert "could not write the ignore" in err, (
        "the ignore failed and nothing said so, which is the silent half of "
        "the defect the ignore exists against"
    )
    assert str(venv / ".gitignore") in err, (
        "the sentence does not name the file it could not write, so the "
        "reader cannot go and look at it"
    )
    assert "git status" in err, (
        "the reader is told a write failed and not what it costs them"
    )
    assert not (venv / ".gitignore").exists()
    assert ".venv" in git_status(tmp_path), (
        "the sentence promises the directory shows up in git status; it has "
        "to be true when it prints"
    )


def test_the_unwritable_sentence_is_the_same_on_every_platform(
    tmp_path, monkeypatch, capsys
):
    """The case above is skipped as root and on Windows, and the suite runs on
    `ubuntu-latest`, `macos-latest` and `windows-latest`. A sentence a person
    reads is pinned by contract §14 wherever it can print, so the write is
    made to refuse here instead of the directory being made to refuse it --
    the guard catches `OSError` and every platform can raise one."""
    real_write_text = pathlib.Path.write_text

    def refuse(self, *args, **kwargs):
        if self.name == ".gitignore":
            raise PermissionError(13, "Permission denied", str(self))
        return real_write_text(self, *args, **kwargs)

    monkeypatch.setattr(pathlib.Path, "write_text", refuse)
    venv = fake_venv(tmp_path)
    (venv / "pyvenv.cfg").write_text("version = 3.11.9\n")
    assert rt.ensure(venv) is None, "the refusal is unchanged"
    err = capsys.readouterr().err
    assert "Traceback" not in err, err
    assert "could not write the ignore" in err
    assert str(venv / ".gitignore") in err
    assert "git status" in err
    assert "Permission denied" in err, (
        "the sentence does not say why the write failed, so a full disk and a "
        "read-only directory read identically"
    )
    assert "until that write can succeed" in err, (
        "the remedy clause names a cause. `except OSError` is four cases -- "
        "permissions, a read-only filesystem, a full disk, a path that is a "
        "directory -- and `make it writable` is wrong advice on two of them "
        "(round 1's finding 3). The reason is carried by strerror above; the "
        "remedy has to say what must become true, not what to change"
    )
    assert "make it writable" not in err, (
        "the superseded remedy is back beside the new one -- a reader acts on "
        "the first thing that names an action"
    )


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


# --- what the documents name -----------------------------------------------
#
# A command nobody is pointed at costs what the old one cost. Three documents
# carry the pointing, and each is a sentence somebody reads and acts on:
# `CONTRIBUTING.md` for a person in a clone, the handoff protocol for the
# orchestrator writing a spawn prompt, and `agents/smith.md` for the segment
# that was not told.


def flat(*parts):
    """The file as one line, so a pinned phrase survives re-wrapping."""
    return " ".join(read(os.path.join(ROOT, *parts)).split())


def running_the_checks():
    """`CONTRIBUTING.md` §*Running the checks*, to the next heading."""
    text = read(os.path.join(ROOT, "CONTRIBUTING.md"))
    start = text.index("## Running the checks")
    return text[start : text.index("\n## ", start + 1)]


def test_the_section_names_the_cheap_command_before_the_slow_one():
    """A reader copies the first command in the block. That is the whole of
    #156: the first one paid 55-58 seconds for its environment on every
    call, and a section that names the cheap one second still costs that."""
    section = running_the_checks()
    assert "bin/test" in section, (
        "CONTRIBUTING.md §Running the checks does not name the runner at all"
    )
    assert section.index("bin/test") < section.index("uvx --with pytest"), (
        "the slow form is still the first command in the section, so it is "
        "still what a reader copies"
    )


def test_the_slow_form_says_what_it_is_for_and_what_it_costs():
    """Kept rather than deleted, because `bin/test` writes a `.venv` into the
    tree and a reader who does not want that needs the other form named. Kept
    without its cost, it reads as an equal alternative."""
    section = running_the_checks()
    assert "fallback" in section, (
        "the uvx form sits in the section as an unlabelled second option"
    )
    assert "seconds each" in section and "every call" in section, (
        "the fallback is named without the cost that demoted it, so the next "
        "reader promotes it back"
    )


def test_the_section_and_the_runner_state_the_same_floor():
    """The document names a version and the code enforces one. Two places
    saying a number is two places to disagree, and the disagreement is
    invisible until somebody's 3.11 builds an environment the suite needs
    3.12 for."""
    section = running_the_checks()
    assert f"Python {rt.FLOOR_TEXT} is the supported floor" in section, (
        "the floor sentence no longer states the floor the runner enforces "
        f"({rt.FLOOR_TEXT} in .github/scripts/run_tests.py's FLOOR)"
    )
    assert "FLOOR" in section, (
        "the sentence names a number the reader cannot trace to the code that holds it"
    )


def test_the_section_states_the_floor_once():
    """The sentence above is worth nothing while a second copy of the number
    sits in the same section untraced. Whichever one a reader finds first is
    the one they edit when the floor moves, and the other stays behind saying
    the old number with nothing pointing at it."""
    section = running_the_checks()
    found = section.count(rt.FLOOR_TEXT)
    assert found == 1, (
        f"the section states {rt.FLOOR_TEXT} {found} times; only the sentence "
        "naming FLOOR carries the number, and the rest refer back to it"
    )


def test_ci_runs_the_suite_at_the_floor_the_runner_holds():
    """`FLOOR`'s comment says the number is also the version CI runs the suite
    at. Nothing read the workflow, so that half was a claim about another file
    which could go stale in silence -- and a floor CI does not run at is a
    floor nothing measures."""
    workflow = read(WORKFLOW)
    matrix = workflow[workflow.index("  pytest:") : workflow.index("  ledger:")]
    versions = re.findall(r'python:\s*"([^"]+)"', matrix)
    assert versions, "the pytest job names no python version to compare"
    assert set(versions) == {rt.FLOOR_TEXT}, (
        f"CI runs the suite at {sorted(set(versions))} and the runner's FLOOR "
        f"comment claims {rt.FLOOR_TEXT}"
    )


def test_the_section_keeps_the_broad_once_rule():
    """It predates this work item and a cheap runner is exactly what would
    tempt a session to drop it."""
    section = running_the_checks()
    assert "Run the broad ones once" in section


def test_the_section_says_the_full_run_is_the_sealers():
    """`bin/test` with no arguments runs a five-minute suite that
    §2 forbids to smith and warden. The section that makes it cheap is the
    section that has to say who it is for, and name the form a segment
    types.

    Re-pointed by #30: who it is for is the `sealer` now, and phase 3 left the
    case under its old name on purpose. `seal/ledger.md`'s R4 row cited it as
    a coordinate, and renaming a unit REMOVES an anchor where changing its
    body only drifts one — so the rename waited for the phase that touches
    the ledger. That phase removed the coordinate from R4 and wrote the new
    claim into this work item's own fragment, which is where a claim goes
    when the code it cited stops existing under that name."""
    section = running_the_checks()
    assert "agent-contract" in section and "sealer" in section, (
        "the section makes the full suite cheap and says nothing about the "
        "rule that forbids it to a segment"
    )
    assert "bin/test tests/" in section, (
        "no narrow form is shown, so the only command a segment can copy is "
        "the one it must not run"
    )


def test_the_protocol_says_a_shipped_runner_is_found_not_typed():
    """#156's cause: the orchestrator typed the runner into every spawn
    prompt, and the segments it forgot rediscovered one."""
    protocol = flat("docs", "review-handoff-protocol.md")
    assert "A runner the repository ships is found, not typed into every prompt" in (
        protocol
    ), "the handoff still requires the incantation in the prompt, always"
    assert "where the repository ships none, the prompt carries the incantation" in (
        protocol
    ), (
        "the requirement drops the case it replaced — a repository with no "
        "runner still needs the prompt to carry one"
    )


def test_the_protocol_hands_over_the_narrow_form():
    """The requirement points a segment at a command that runs a five-minute
    suite. Naming it without naming which form is how §2 gets widened by a
    document that never mentions it."""
    protocol = flat("docs", "review-handoff-protocol.md")
    assert "The form a segment is handed is the narrow one" in protocol
    assert "the full suite is the sealer's, run once after the rounds" in protocol


def test_the_protocol_carries_the_measurement_that_bought_it():
    """Every requirement beside it names the failure it was bought by. One
    without is a rule a reader can talk themselves out of."""
    protocol = flat("docs", "review-handoff-protocol.md")
    assert "17 s, 2 s, 0 s and 0 s" in protocol, (
        "the requirement arrives with no measurement, where the four beside "
        "it each name theirs"
    )


def test_smith_finds_the_runner_before_inventing_a_command():
    """The prompt is what went missing, so the fix cannot live in the prompt.
    `agents/smith.md` reaches every segment at startup with nobody typing
    anything."""
    smith = flat("agents", "smith.md")
    assert "Find the runner before you invent a command" in smith, (
        "a segment whose prompt omits the runner has nothing telling it one "
        "exists, which is what the repeats measured"
    )
    assert "Type the narrow form, one module" in smith, (
        "smith is pointed at a command that runs the full suite and not at "
        "the form §2 leaves it"
    )
    assert "`docs/review-handoff-protocol.md` §*The handoff before round 1*" in smith, (
        "the rule is restated rather than linked, so the two carriers can drift apart"
    )


def test_warden_finds_the_runner_before_building_its_own():
    """The class is every segment that runs a test, and the fix reached one of
    them. `agents/warden.md` told a reviewer to build a `uv` venv in its clone
    and named no runner, so a review round paid for an environment the
    repository already had built -- the same cost, on the segment that runs
    more cases than the smith does. Both definitions ship to user
    repositories, so neither may name a command that exists only here."""
    warden = flat("agents", "warden.md")
    assert "Find the runner before you build your own" in warden, (
        "the reviewing segment is still told to assemble its own environment "
        "with nothing telling it a shipped runner may exist"
    )
    assert "Type the narrow form, one module" in warden, (
        "warden is pointed at a command that runs the full suite and not at "
        "the form §2 leaves it"
    )
    assert (
        "`docs/review-handoff-protocol.md` §*The handoff before round 1*" in warden
    ), "the rule is restated rather than linked, so the two carriers can drift apart"
    assert "make a `uv` venv inside the clone" in warden, (
        "the fallback went with the addition — a repository that ships no "
        "runner leaves the reviewer with nothing at all"
    )


@pytest.mark.parametrize("definition", ["smith.md", "warden.md"])
def test_no_agent_definition_names_this_repositorys_own_command(definition):
    """`agents/` is copied into every install, so a definition naming
    `bin/test` sends a user's segment after a file their repository does not
    have. The shape both carry instead is the generic one: a wrapper in
    `bin/`, or whatever the contribution guide names first."""
    text = flat("agents", definition)
    assert "bin/test" not in text, (
        f"agents/{definition} names this repository's own runner, and it "
        "ships to repositories that have no such file"
    )


def test_the_cheat_sheet_does_not_offer_the_runner():
    """`bin/` is on a plugin user's PATH, but `test` is a shell builtin, so
    PATH never gets a say. A row in the table that names commands a reader
    types would name the one command there that cannot be typed."""
    readme = read(os.path.join(ROOT, "README.md"))
    sheet = readme[readme.index("## Cheat sheet") :]
    rows = [line for line in sheet.splitlines() if line.startswith("| `")]
    assert not [row for row in rows if "bin/test" in row or "`test" in row], (
        "the cheat sheet offers a command a plugin user cannot type, and "
        "whose runner is this repository's own five-minute suite"
    )


def test_the_placement_stands_on_what_it_actually_buys():
    """Phase 1 recorded `.github/` as absent from a plugin cache. It is not:
    the plugin ships from the repository root, and 0.5.0, 0.7.0, 0.8.0 and
    0.8.1 each hold `.github/scripts/`. The location is still right and the
    reason is not, so the file has to carry the true one — otherwise the next
    reader moves the runner to fix a problem that was never there."""
    doc = " ".join(read(SCRIPT).split())
    assert "`.github/` does not" not in doc, (
        "the runner still claims a location hides it from a plugin cache"
    )
    assert "shell builtin" in doc, (
        "the runner does not say what actually keeps a plugin user from "
        "running this suite, so its placement reads as the guard"
    )
