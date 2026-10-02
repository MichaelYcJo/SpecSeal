"""A worktree creation is judged before git runs, in a clone carrying this
plugin's git hooks too (#692, `questions.md` P6, answer (a)).

Round 1 found that taking a creation back after git made it cannot undo what
the creation did on the way: `-B` resets an existing branch before any hook
runs, `--no-checkout` and `--orphan` run no `post-checkout` at all, `--lock`
leaves a tree one `--force` cannot remove, and a Bash creation naming
`.claude/worktrees/` bought the session's consent. The owner's answer is the
switch arm's: 0.16.0's reading decides before the command runs, wherever the
clone's hooks are.

Each case is what the harness does with one Bash call -- `pre-bash`, the
command only if nothing denied or asked, then `post-bash` -- in a real clone
the installer has written its stubs into. The oracle is the world afterwards:
a branch's tip, a directory on disk, the consent record. Never what a reading
said.
"""

import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import load_hook_module, symlink_or_skip
from test_the_guard_asks_once_per_session import ask_entries, write_transcript

HOOKS = Path(__file__).resolve().parent.parent / "hooks"
install_mod = load_hook_module("hook-install.py", "hook_install_for_creation")

BASH = shutil.which("bash")
pytestmark = pytest.mark.skipif(BASH is None, reason="no bash to run commands in")
SESSION = "s-create"


@pytest.fixture(autouse=True)
def _installer_writes(git_hooks_installed):
    """The stubs are the subject of every case here."""


def env(home, session=SESSION):
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update(
        HOME=str(home),
        XDG_CONFIG_HOME=str(home / ".config"),
        GIT_CONFIG_NOSYSTEM="1",
    )
    if session:
        e["CLAUDE_CODE_SESSION_ID"] = session
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
            self.git(*args)
        (self.top / "seal").mkdir()
        (self.top / "seal" / "README.md").write_text("root\n", encoding="utf-8")
        (self.top / "seal" / "config.md").write_text(
            "# Repository config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n",
            encoding="utf-8",
        )
        self.git("add", ".")
        self.git("commit", "-q", "-m", "init")
        # A branch with a commit of its own, which `main` does not have.
        self.git("switch", "-q", "-c", "existing")
        (self.top / "f.txt").write_text("own\n", encoding="utf-8")
        self.git("add", "f.txt")
        self.git("commit", "-q", "-m", "existing's own")
        self.git("switch", "-q", "main")
        assert install_mod.install(str(self.top), "installer")
        assert (self.top / ".git" / "hooks" / "pre-commit").is_file()

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.top), *args],
            capture_output=True,
            text=True,
            env=env(self.home, session=""),
            stdin=subprocess.DEVNULL,
        )

    def tip(self, branch):
        return self.git("rev-parse", "--verify", "--quiet", branch).stdout.strip()

    def record(self):
        return self.top / ".git" / "specseal-worktree-consent" / SESSION

    def press(self):
        write_transcript(
            self.home / ".claude" / "projects", SESSION, ask_entries(self.top)
        )

    def claude(self):
        """A shell named `claude`, for the hooks to run below.

        The harness runs every hook below its own `claude` process, and the
        guard's count of other sessions starts by finding that process among
        its ancestors (`hooks/worktree-guard.py#sessions_in_tree`). A case
        that ran the dispatcher straight from pytest borrowed the ancestor of
        whoever ran the suite: inside a session the count was taken and a
        second creation met the single-stream refusal, while in CI, with no
        `claude` anywhere, the count was unusable and the same creation met
        the confirmation prompt instead (#692, after the chain: CI run
        36965695916). A symlink to bash, so `ps` names it `claude`, for the
        reasons `tests/test_the_commit_gate_decides_at_the_commit.py#fake_claude`
        gives."""
        link = self.tmp / "bin" / "claude"
        if not link.exists():
            link.parent.mkdir(exist_ok=True)
            symlink_or_skip(BASH, link)
        return link

    def call(self, command):
        """One Bash call as the harness makes it: the decision, and the
        command's result when it ran (None when it did not)."""
        payload = {
            "tool_name": "Bash",
            "tool_input": {"command": command},
            "cwd": str(self.top),
            "session_id": SESSION,
        }
        hook = f"{q(sys.executable)} {q(HOOKS / 'dispatch.py')}"

        def group(name):
            # `; exit $?` keeps bash from exec-ing the hook in its own place,
            # which would take the `claude` process out of the ancestry.
            return subprocess.run(
                [str(self.claude()), "-c", f"{hook} {name}; exit $?"],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                env=env(self.home),
            ).stdout

        out = group("pre-bash")
        decision = "silent"
        if out.strip():
            decision = (json.loads(out).get("hookSpecificOutput") or {}).get(
                "permissionDecision", "silent"
            )
        if decision in ("deny", "ask"):
            return decision, None
        ran = subprocess.run(
            [BASH, "-c", command],
            cwd=str(self.top),
            capture_output=True,
            text=True,
            env=env(self.home),
            stdin=subprocess.DEVNULL,
            timeout=60,
        )
        group("post-bash")
        return decision, ran


@pytest.fixture
def clone(tmp_path):
    return Clone(tmp_path)


def q(p):
    return shlex.quote(str(p))


# --- round 1's four: refused before git runs, so nothing moved ---------------


def test_a_refused_dash_capital_b_leaves_the_branch_where_it_was(clone):
    """🔴 1: `-B` resets an existing branch before any hook can run."""
    before = clone.tip("existing")
    wt = clone.tmp / "wt"
    decision, _ran = clone.call(f"git worktree add -B existing {q(wt)} main")
    assert clone.tip("existing") == before
    assert not wt.exists()
    assert decision == "deny"


@pytest.mark.parametrize(
    "flags",
    [("--no-checkout",), ("--orphan",), ("--lock",)],
    ids=["no checkout", "orphan", "lock"],
)
def test_a_creation_git_runs_no_undo_for_is_refused_before_it(clone, flags):
    """🟡 4 and 🟡 6: `--no-checkout` and `--orphan` run no `post-checkout`,
    and `--lock` leaves a tree one `--force` cannot remove."""
    wt = clone.tmp / "wt"
    joined = " ".join(flags)
    decision, _ran = clone.call(f"git worktree add {joined} -b nb {q(wt)}")
    assert not wt.exists()
    assert not clone.tip("nb")
    assert decision == "deny"


def test_a_bash_creation_under_the_harness_path_buys_no_consent(clone):
    """🟡 5: the path the Agent tool's isolation uses is not that spawn's
    answer when a Bash command names it."""
    wt = clone.top / ".claude" / "worktrees" / "x"
    decision, _ran = clone.call(f"git worktree add {q(wt)} -b n21")
    assert not clone.record().exists()
    assert not wt.exists()
    assert decision == "deny"
    second = clone.tmp / "second"
    decision, _ran = clone.call(f"git worktree add {q(second)} -b n21b")
    assert not second.exists()
    assert decision == "deny"


# --- and what an answer lets through is recorded as 0.16.0 recorded it -----


def test_an_answered_creation_runs_and_the_record_follows_it(clone):
    clone.press()
    wt = clone.tmp / "wt"
    decision, ran = clone.call(f"git worktree add {q(wt)} -b nb")
    assert decision != "deny"
    assert ran is not None and ran.returncode == 0, ran and ran.stderr
    assert wt.is_dir()
    assert clone.record().exists()


def test_the_old_token_puts_the_creation_to_the_person_before_it_runs(clone):
    """0.16.0's `[worktree-ok]` row: the token is not a choice, it turns the
    refusal into the harness's own confirmation."""
    wt = clone.tmp / "wt"
    decision, _ran = clone.call(f"git worktree add {q(wt)} -b nb  # [worktree-ok]")
    assert decision == "ask"
    assert not wt.exists()


def test_no_git_hook_judges_a_creation(clone):
    """Nothing in the clone's hooks directory runs for a checkout, so a
    creation git makes is the guard's alone, before it."""
    assert not (clone.top / ".git" / "hooks" / "post-checkout").exists()
