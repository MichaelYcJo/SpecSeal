"""A worktree creation is judged and recorded where git made it (#692,
phase 4: S7, S8).

Real git and a real shell, in fixture clones carrying the stubs
`hooks/hook-install.py` writes. The oracle for "a creation ran" is the
worktree on disk, and for "consent" the record under
`<git-common-dir>/specseal-worktree-consent/<session>`.
"""

import io
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import load_hook_module
from test_the_guard_asks_once_per_session import ask_entries, write_transcript

HOOKS = Path(__file__).resolve().parent.parent / "hooks"
sys.path.insert(0, str(HOOKS))
import creationgate  # noqa: E402

install_mod = load_hook_module("hook-install.py", "hook_install_for_creation")
consent_mod = load_hook_module("worktree_consent.py", "consent_beside_post_checkout")

BASH = shutil.which("bash")
pytestmark = pytest.mark.skipif(BASH is None, reason="no bash to run commands in")
SESSION = "s-create"


@pytest.fixture(autouse=True)
def _installer_writes(git_hooks_installed):
    """The stubs are the subject of every case here."""


def env(home, session=SESSION, **extra):
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update(
        HOME=str(home),
        XDG_CONFIG_HOME=str(home / ".config"),
        GIT_CONFIG_NOSYSTEM="1",
    )
    if session:
        e["CLAUDE_CODE_SESSION_ID"] = session
    e.update(extra)
    return e


class Clone:
    def __init__(self, tmp_path):
        self.tmp = tmp_path
        self.home = tmp_path / "home"
        self.home.mkdir()
        self.top = tmp_path / "repo"
        self.top.mkdir()
        for args in (
            ("init", "-q"),
            ("symbolic-ref", "HEAD", "refs/heads/main"),
            ("config", "user.name", "x"),
            ("config", "user.email", "x@example.com"),
            ("config", "commit.gpgsign", "false"),
        ):
            self.git(*args, session="")
        (self.top / "seal").mkdir()
        (self.top / "seal" / "README.md").write_text("root\n", encoding="utf-8")
        (self.top / "seal" / "config.md").write_text(
            "# Repository config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n",
            encoding="utf-8",
        )
        self.git("add", ".", session="")
        self.git("commit", "-q", "-m", "init", session="")
        self.git("branch", "existing", session="")
        assert install_mod.install(str(self.top), "installer")

    def git(self, *args, session=SESSION, cwd=None, **extra):
        return subprocess.run(
            ["git", "-C", str(cwd or self.top), *args],
            capture_output=True,
            text=True,
            env=env(self.home, session, **extra),
            stdin=subprocess.DEVNULL,
        )

    def sh(self, command, session=SESSION, cwd=None, **extra):
        return subprocess.run(
            [BASH, "-c", command],
            cwd=str(cwd or self.top),
            capture_output=True,
            text=True,
            env=env(self.home, session, **extra),
            stdin=subprocess.DEVNULL,
            timeout=60,
        )

    def record(self, session=SESSION):
        return self.top / ".git" / "specseal-worktree-consent" / session

    def press(self):
        write_transcript(
            self.home / ".claude" / "projects", SESSION, ask_entries(self.top)
        )


@pytest.fixture
def clone(tmp_path):
    return Clone(tmp_path)


def q(p):
    return shlex.quote(str(p))


# --- S7: a creation that ran is the record; one that did not, is not -------

RAN = {
    "plain": "git worktree add {wt} -b nb",
    "cd first": "cd {sub} && git worktree add {wt} -b nb",
    "a ; after a cd": "cd {sub} ; git worktree add {wt} -b nb",
    "behind a redirection": "2>/dev/null git worktree add {wt} -b nb",
    "git 2>&1 worktree": "git 2>&1 worktree add {wt} -b nb",
    "builtin cd": "builtin cd {sub} && git worktree add {wt} -b nb",
    "time cd": "time cd {sub} && git worktree add {wt} -b nb",
    "pushd": "pushd {sub} >/dev/null && git worktree add {wt} -b nb",
    "2>&1 cd": "2>&1 cd {sub} && git worktree add {wt} -b nb",
    "a loop variable": "for d in {top}; do git -C $d worktree add {wt} -b nb; done",
    "eval": "eval 'git worktree add {wt} -b nb'",
    "an existing branch": "git worktree add {wt} existing",
    # #686's comment: the `cd` fails, so the creation after `||` runs.
    "eval true, then a cd that fails": (
        "eval true; 2>/dev/null cd {missing} || git worktree add {wt} -b nb"
    ),
}

NOT_RAN = {
    "after false &&": "false && git worktree add {wt} -b nb",
    "in an echo": "echo git worktree add {wt} -b nb",
    "in a heredoc body": "cat > /dev/null <<'EOF'\ngit worktree add {wt} -b nb\nEOF",
    "in a function never called": "f() {{ git worktree add {wt} -b nb; }}",
}


def fill(template, clone):
    sub = clone.top / "seal"
    return template.format(
        wt=q(clone.tmp / "wt"),
        sub=q(sub),
        top=q(clone.top),
        missing=q(clone.tmp / "missing"),
    )


@pytest.mark.parametrize("name", sorted(RAN))
def test_s7_a_creation_bash_ran_is_recorded_in_its_clone(clone, name):
    clone.press()
    got = clone.sh(fill(RAN[name], clone))
    assert (clone.tmp / "wt").is_dir(), (name, got.stderr)
    assert clone.record().exists(), name


@pytest.mark.parametrize("name", sorted(NOT_RAN))
def test_s7_a_creation_bash_never_ran_leaves_no_record(clone, name):
    clone.press()
    clone.sh(fill(NOT_RAN[name], clone))
    assert not (clone.tmp / "wt").exists()
    assert not clone.record().exists(), name


# --- S8: refuse, then the answer, then allowed -------------------------------


HEADLINE = "SpecSeal took this worktree back: {new} was created and removed again"


def test_s8_the_first_creation_of_an_attended_session_is_one_confirmation(clone):
    first = clone.git("worktree", "add", str(clone.tmp / "wt1"), "-b", "a1")
    assert first.returncode != 0
    assert not (clone.tmp / "wt1").exists()
    assert HEADLINE.format(new=os.path.realpath(clone.tmp / "wt1")) in first.stderr, (
        first.stderr
    )
    assert "Its branch `a1` stays; `git branch -D a1` removes it" in first.stderr
    assert "git -c specseal.answer=worktree-ok worktree add …" in first.stderr
    assert "`git worktree add …  # [worktree-ok]`, still works" in first.stderr
    assert not clone.record().exists()
    # The person's answer, typed back by the model.
    second = clone.git(
        "-c",
        "specseal.answer=worktree-ok",
        "worktree",
        "add",
        str(clone.tmp / "wt2"),
        "-b",
        "a2",
    )
    assert second.returncode == 0, second.stderr
    assert (clone.tmp / "wt2").is_dir()
    assert clone.record().exists()
    # And every creation after it in the session.
    for n in range(3, 7):
        got = clone.git("worktree", "add", str(clone.tmp / f"wt{n}"), "-b", f"a{n}")
        assert got.returncode == 0, (n, got.stderr)


def test_s8_an_automation_run_pays_no_confirmation(clone):
    clone.press()
    for n in range(1, 7):
        got = clone.git("worktree", "add", str(clone.tmp / f"wt{n}"), "-b", f"a{n}")
        assert got.returncode == 0, (n, got.stderr)


def test_s8_the_old_token_carries_the_answer_through_the_bash_call(clone):
    command = f"git worktree add {q(clone.tmp / 'wt')} -b nb  # [worktree-ok]"
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": str(clone.top),
        "session_id": SESSION,
    }
    for group in ("pre-bash",):
        subprocess.run(
            [sys.executable, str(HOOKS / "dispatch.py"), group],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            env=env(clone.home),
            check=True,
        )
    got = clone.sh(command)
    assert got.returncode == 0, got.stderr
    assert (clone.tmp / "wt").is_dir()


def test_a_refused_creation_from_a_linked_worktree_counts_the_tree_it_ran_from(clone):
    """`post-checkout`'s parent, `git worktree add`, stands at the toplevel
    the creation ran from; the record and the count are that clone's."""
    clone.press()
    clone.git("worktree", "add", str(clone.tmp / "first"), "-b", "f1")
    got = clone.git(
        "worktree",
        "add",
        str(clone.tmp / "second"),
        "-b",
        "f2",
        cwd=clone.tmp / "first",
    )
    assert got.returncode == 0, got.stderr
    assert clone.record().exists()


# --- what is never taken back ------------------------------------------------


def test_a_worktree_the_harness_makes_for_an_agent_is_recorded_not_taken_back(clone):
    """M5 is unmeasured: if the Agent tool's isolation runs `git worktree
    add`, the person already answered the guard's Agent arm for it."""
    path = clone.top / ".claude" / "worktrees" / "agent-1"
    got = clone.git("worktree", "add", str(path), "-b", "agent-1")
    assert got.returncode == 0, got.stderr
    assert path.is_dir()
    assert clone.record().exists()


def test_a_persons_own_creation_is_theirs(clone):
    """P2, answer (a)."""
    got = clone.git("worktree", "add", str(clone.tmp / "wt"), "-b", "nb", session="")
    assert got.returncode == 0, got.stderr
    assert not clone.record().exists()


def test_a_clone_that_opted_out_is_left_alone(clone):
    (clone.top / ".git" / "specseal-scratch").write_text("", encoding="utf-8")
    got = clone.git("worktree", "add", str(clone.tmp / "wt"), "-b", "nb")
    assert got.returncode == 0, got.stderr


def test_a_switch_is_never_a_creation(clone):
    got = clone.git("switch", "-q", "existing")
    assert got.returncode == 0, got.stderr
    assert not clone.record().exists()


# --- the text paths stand aside where git decides ----------------------------


def test_the_guard_and_the_consent_writer_stand_aside_where_git_decides(
    clone, monkeypatch
):
    command = f"git worktree add {q(clone.tmp / 'wt')} -b nb"
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": str(clone.top),
        "session_id": SESSION,
    }
    out = subprocess.run(
        [sys.executable, str(HOOKS / "dispatch.py"), "pre-bash"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env(clone.home),
    ).stdout
    assert out.strip() == "", out
    # The command "ran" -- and the hook took the creation back -- so a
    # record written from the command would be consent nobody gave.
    clone.sh(command)
    assert not (clone.tmp / "wt").exists()
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    consent_mod.main()
    assert not clone.record().exists()


# --- the ladder's texts ------------------------------------------------------


def ladder(monkeypatch, sessions):
    monkeypatch.setattr(
        creationgate.guard(), "sessions_in_tree", lambda top, s: sessions
    )
    monkeypatch.setattr(creationgate.guard(), "LANG", "en")


def test_single_stream_steers_to_a_switch(monkeypatch, tmp_path):
    ladder(monkeypatch, ([], [], True))
    text = creationgate.reason(str(tmp_path), "s", "/x/wt", "nb", str(tmp_path))
    assert (
        f"No other session is working in {tmp_path} (= single-stream). Rule: for "
        "single-stream work, don't create a worktree, switch branches in the "
        "shared tree instead:" in text
    )
    # `git -C <top>`, because the case's own directory is no repository.
    assert "switch <branch>                  # existing branch" in text
    assert f"  git -C {tmp_path} fetch origin" in text
    assert "AskUserQuestion" not in text


def test_cannot_tell_offers_both_ways(monkeypatch, tmp_path):
    ladder(monkeypatch, ([], [], False))
    text = creationgate.reason(str(tmp_path), "s", "/x/wt", "", str(tmp_path))
    assert "offering exactly these two options:" in text
    assert (
        '  1. "Create the worktree" — re-issue it as `git -c specseal.answer=worktree-ok'
        in text
    )
    assert '  2. "Switch in the shared tree" — run ' in text
    assert "Its branch" not in text


def test_another_active_session_asks_for_the_confirmation(monkeypatch, tmp_path):
    session = {"pid": 7, "cwd": str(tmp_path), "app": "", "tty": "", "idle": 0}
    monkeypatch.setattr(
        creationgate.guard(), "fmt_sessions", lambda entries: "  - pid 7"
    )
    ladder(monkeypatch, ([session], [], True))
    text = creationgate.reason(str(tmp_path), "s", "/x/wt", "", str(tmp_path))
    assert f"Another Claude session is actively working in {tmp_path}" in text
    assert "Ask with the AskUserQuestion tool whether to create it." in text
