"""The commit gate decides inside the commit, in the worktree it lands in
(#692, phase 3: S1-S6, S9, S13).

Every case runs a real shell and real git in fixture repositories carrying the
stubs `hooks/hook-install.py` writes, pointing at this checkout's
`hooks/git/`. The oracle is what git did -- whether HEAD moved -- and never
what a reading of the command said it would do.

The world each case builds:

  * `main`, an opted-in clone on `release`, which no declaration names -- the
    session's directory, as the main checkout was in the recorded run;
  * `w`, a linked worktree of it on `feat`, which a routing declaration names;
  * `u`, a second opted-in clone, undeclared.
"""

import io
import json
import os
import shlex
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest
from conftest import load_hook_module, symlink_or_skip
from test_the_guard_asks_once_per_session import ask_entries, write_transcript

HOOKS = Path(__file__).resolve().parent.parent / "hooks"
sys.path.insert(0, str(HOOKS))
import gate  # noqa: E402  -- the plain name the hooks import
import tokens  # noqa: E402

install_mod = load_hook_module("hook-install.py", "hook_install_for_the_commit_gate")
crg = load_hook_module("commit-review-gate.py", "crg_beside_the_git_hooks")

BASH = shutil.which("bash")
pytestmark = pytest.mark.skipif(BASH is None, reason="no bash to run commands in")

SESSION = "s-commit"


@pytest.fixture(autouse=True)
def _installer_writes(git_hooks_installed):
    """The stubs are the subject of every case here."""


def env(home, session=SESSION, **extra):
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update(
        HOME=str(home),
        XDG_CONFIG_HOME=str(home / ".config"),
        GIT_CONFIG_NOSYSTEM="1",
        GIT_AUTHOR_NAME="x",
        GIT_AUTHOR_EMAIL="x@example.com",
        GIT_COMMITTER_NAME="x",
        GIT_COMMITTER_EMAIL="x@example.com",
    )
    if session:
        e["CLAUDE_CODE_SESSION_ID"] = session
    e.update(extra)
    return e


def g(d, *args, home, check=True, session=SESSION, **extra):
    return subprocess.run(
        ["git", "-C", str(d), *args],
        capture_output=True,
        text=True,
        check=check,
        env=env(home, session, **extra),
        stdin=subprocess.DEVNULL,
        timeout=60,
    )


def clone(path, home, branch):
    path.mkdir(parents=True)
    g(path, "init", "-q", home=home, session="")
    g(path, "symbolic-ref", "HEAD", f"refs/heads/{branch}", home=home, session="")
    for key, value in (
        ("commit.gpgsign", "false"),
        # In the repository, so `env -i git commit` still has an identity and
        # reaches its hooks rather than dying before them.
        ("user.name", "x"),
        ("user.email", "x@example.com"),
    ):
        g(path, "config", key, value, home=home, session="")
    (path / "seal").mkdir()
    (path / "seal" / "README.md").write_text("root\n", encoding="utf-8")
    # A recorded mode, so `mode-gate.py` has nothing to say in `pre-bash`.
    (path / "seal" / "config.md").write_text(
        "# Repository config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n",
        encoding="utf-8",
    )
    (path / "f.py").write_text("a = 1\n", encoding="utf-8")
    g(path, "add", ".", home=home, session="")
    g(path, "commit", "-q", "-m", "init", home=home, session="")
    return path


def declare(worktree, branch):
    d = worktree / "seal" / "specs" / "1790000000-x"
    d.mkdir(parents=True, exist_ok=True)
    (d / "routing.md").write_text(
        "| Axis | Answer |\n|---|---|\n| Review | through the review chain |\n"
        f"| Destination | open the pull request |\n| Branch | {branch} |\n",
        encoding="utf-8",
    )


class World:
    def __init__(self, tmp_path):
        self.tmp = tmp_path
        self.home = tmp_path / "home"
        self.home.mkdir()
        self.main = clone(tmp_path / "main", self.home, "release")
        self.w = tmp_path / "w"
        g(
            self.main,
            "worktree",
            "add",
            "-q",
            str(self.w),
            "-b",
            "feat",
            home=self.home,
            session="",
        )
        declare(self.w, "feat")
        self.u = clone(tmp_path / "u", self.home, "main")
        for r in (self.main, self.u):
            assert install_mod.install(str(r), "installer")

    def head(self, d):
        return g(d, "rev-parse", "HEAD", home=self.home, session="").stdout.strip()

    def change(self, d, name="f.py", text=None):
        p = Path(d) / name
        p.write_text(
            text or (p.read_text(encoding="utf-8") if p.exists() else "") + "b = 2\n",
            encoding="utf-8",
        )
        g(d, "add", name, home=self.home, session="")

    def sh(self, command, cwd=None, session=SESSION, **extra):
        return subprocess.run(
            [BASH, "-c", command],
            cwd=str(cwd or self.main),
            capture_output=True,
            text=True,
            env=env(self.home, session, **extra),
            stdin=subprocess.DEVNULL,
            timeout=60,
        )


@pytest.fixture
def world(tmp_path):
    return World(tmp_path)


def q(p):
    return shlex.quote(str(p))


def as_the_tool_spells_it(command):
    """The `-c` string the Bash tool hands its shell for COMMAND: the command
    inside `eval '…'`, with more after it (`pwd -P` into a file, in the
    harness).

    The more-after-it is what keeps the shell alive. bash 5.1 and later
    replace a `-c` shell with the last command of its list, so `bash -c
    "$COMMAND"` holds the command in no process by the time git's hook walks
    up to `claude`, and an answer `hooks/answers.py` can only give to the
    call whose argv carries it is given to nobody. macOS's bash 3.2 does not
    do that, so both cases that model a call that way passed there and
    failed on ubuntu's 5.2 (#692, after the chain: CI run 36965695916). The
    harness's own string cannot be replaced, because `eval` is not its last
    command; the argv `ps` shows for it is the one
    `tests/test_the_old_spellings_reach_the_hook.py#shell` records."""
    return f"eval {q(command)} < /dev/null && pwd -P >/dev/null"


# --- S1: the recorded run's four commands -----------------------------------


def test_s1_a_commit_lands_in_the_declared_worktree_with_no_stop(world):
    """Rows 1 and 2 of 1790644505's table: `cd <W> && …` then a commit after
    a heredoc or after `;`. 0.15.7 asked the person both times, naming the main
    checkout; the commit lands in the declared worktree, and git says so."""
    (world.w / "CHANGES.md").write_text("x\n", encoding="utf-8")
    before = (world.head(world.main), world.head(world.w))
    first = world.sh(
        f"cd {q(world.w)} && python3 - <<'EOF'\n"
        "p = 'CHANGES.md'; open(p, 'a').write('entry\\n')\n"
        "EOF\n"
        "git add CHANGES.md && git commit -q -m 'docs: entry'"
    )
    assert first.returncode == 0, first.stderr
    second = world.sh(
        f"cd {q(world.w)} && grep -c nothing CHANGES.md ; "
        "echo more >> CHANGES.md && git add CHANGES.md && git commit -q -m 'docs: pin'"
    )
    assert second.returncode == 0, second.stderr
    assert world.head(world.main) == before[0]
    assert world.head(world.w) != before[1]
    assert gate.HEADER not in first.stderr + second.stderr


def test_s1_a_heredoc_that_ends_early_commits_into_the_main_checkout_and_is_stopped(
    world,
):
    """Row 3: the body's own `EOF` line ended the heredoc, so the commit became
    a real command line in the session's directory. That is a real commit into
    an undeclared checkout, and it is the one stop kept."""
    world.change(world.main)
    before = world.head(world.main)
    got = world.sh(
        f"cat > {q(world.tmp / 'issue.md')} <<'EOF'\nquoted:\nEOF\n"
        "git add f.py && git commit -q -m 'stray'\nEOF"
    )
    assert world.head(world.main) == before
    assert gate.HEADER in got.stderr
    assert f"No review is recorded for this cycle in {world.main}," in got.stderr


def test_s1_a_patch_whose_body_mentions_a_commit_commits_nothing_and_is_not_stopped(
    world,
):
    """Row 4: 0.15.7 answered `UNREADABLE_CONSTRUCT`; nothing here commits."""
    before = (world.head(world.main), world.head(world.w))
    got = world.sh(
        f"cd {q(world.w)} && python3 - <<'EOF'\n"
        f"for c in ['git commit -m x', 'cd {world.main}; git commit -m y']:\n"
        "    print(c)\nEOF"
    )
    assert got.returncode == 0, got.stderr
    assert (world.head(world.main), world.head(world.w)) == before
    assert gate.HEADER not in got.stderr


# --- S2: every commit the base stopped is still stopped --------------------

import test_a_commit_behind_a_reserved_word_is_judged as rw  # noqa: E402
import test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged as wr  # noqa: E402
import test_no_shape_the_base_stops_reads_silent as ns  # noqa: E402


def corpus():
    rows = {}
    for name, cmd in ns.corpus("{W}", "{M}", "{U}"):
        rows["ns: " + name] = cmd
    for name, (cmd, _) in {**wr.WRAPPED, **rw.SHAPES}.items():
        rows["shape: " + name] = cmd
    for name, cmd in {
        **wr.HANDED,
        **wr.SUBSTITUTED,
        **wr.REDIRECTED,
        **rw.EVALS,
    }.items():
        rows["handed: " + name] = cmd
    for name, fn in wr.POSITIONS.items():
        rows["position: " + name] = fn(wr.C)
    for name, pre in {
        "builtin cd": "builtin cd {U}",
        "command cd": "command cd {U}",
        "time cd": "time cd {U}",
        "pushd": "pushd {U} >/dev/null",
        "cd $W unset": 'cd "$W"',
        "2>&1 cd": "2>&1 cd {U}",
    }.items():
        rows["#686: " + name] = f"{pre} && {wr.C}"
        rows["#686 ;: " + name] = f"{pre} ; {wr.C}"
    return rows


CORPUS = corpus()


def _sandbox(base, with_hooks, home):
    """main (undeclared), w (declared) and u (undeclared), each with a staged
    change, logging nothing -- HEAD is the oracle."""
    repos = {}
    for name in ("main", "w", "u"):
        d = clone(base / name, home, "release" if name != "w" else "feat")
        if name == "w":
            declare(d, "feat")
        (d / "f.py").write_text("a = 2\n", encoding="utf-8")
        g(d, "add", "f.py", home=home, session="")
        if with_hooks:
            assert install_mod.install(str(d), "installer")
        repos[name] = d
    return repos


def _as_a_session(base, repos):
    """The argv that runs `$CORPUS_COMMAND` the way the harness runs a Bash
    call: a process named `claude` holding a lease in every clone, and the
    command in a shell of its own below it.

    The shell of its own matters: a fork of a shell named `claude` is named
    `claude` too, so a subshell in the command would be the nearest `claude`
    and its pid would match no lease. The harness's own shell is a child of
    `claude` with another name, which is what this gives. The variable is
    exported as well -- `env -i` is what takes it away, and the lease is what
    is left then (S9)."""
    claude = base / "claude"
    symlink_or_skip(BASH, claude)
    writes = "".join(
        f"mkdir -p {q(Path(g(d, 'rev-parse', '--absolute-git-dir', home=base, session='').stdout.strip()) / 'specseal-leases')}"
        f" && printf '{{\"pid\": %s}}' $$ > "
        f"{q(Path(g(d, 'rev-parse', '--absolute-git-dir', home=base, session='').stdout.strip()) / 'specseal-leases' / SESSION)}\n"
        for d in repos.values()
    )
    return [str(claude), "-c", writes + f'{q(BASH)} -c "$CORPUS_COMMAND"\nexit $?']


ROW_BOUND = 20


def _run_bounded(argv, *, cwd, env, timeout):
    """Run ARGV to its end or to TIMEOUT; True when it ended on its own.

    Not `subprocess.run(..., capture_output=True, timeout=…)`, which bounds
    the direct child alone: a row's shell runs below the `claude` one, so a
    row that never ends -- the corpus's `until false` did not, before it got
    its `break` -- outlived the kill. On POSIX it ran on, an orphan
    committing forever; on Windows `run` reads the pipes to their end after
    the kill, the orphan held them, and the windows-latest leg hung with no
    case named (#692, after the chain: CI run 36965695916). So nothing here
    is a pipe, and on POSIX the whole session the row started is ended,
    whether it ended on its own or not. Windows has no group kill without a
    job object, so there the direct child is ended and a row that did not
    end is still a failure that names itself."""
    group = os.name != "nt"
    proc = subprocess.Popen(
        argv,
        cwd=cwd,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=group,
    )
    try:
        proc.wait(timeout=timeout)
        ended = True
    except subprocess.TimeoutExpired:
        ended = False
    finally:
        if group:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
        else:
            proc.kill()
        proc.wait()
    return ended


def _run_corpus_row(base, command, with_hooks, home):
    repos = _sandbox(base, with_hooks, home)
    text = (
        command.replace("{W}", str(repos["w"]))
        .replace("{U}", str(repos["u"]))
        .replace("{M}", str(base / "m"))
    )
    before = {
        k: g(d, "rev-parse", "HEAD", home=home, session="").stdout
        for k, d in repos.items()
    }
    flock_existed = os.path.exists("/tmp/l")
    try:
        ended = _run_bounded(
            _as_a_session(base, repos),
            cwd=str(repos["main"]),
            env=env(home, CORPUS_COMMAND=as_the_tool_spells_it(text)),
            timeout=ROW_BOUND,
        )
    finally:
        if not flock_existed and os.path.exists("/tmp/l"):
            os.remove("/tmp/l")
        for p in base.rglob("*"):
            if p.is_dir():
                try:
                    p.chmod(0o755)
                except OSError:
                    pass
    assert ended, (
        f"the row did not end within {ROW_BOUND} s, so what it committed is "
        f"not an answer: {command!r}"
    )
    landed = set()
    for k, d in repos.items():
        if not d.is_dir():
            d = base / "m"
        if g(d, "rev-parse", "HEAD", home=home, session="").stdout != before[k]:
            landed.add(k)
    return landed


def test_a_row_that_does_not_end_is_named_and_leaves_nothing_behind(tmp_path):
    """The bound S2's runner leans on, held without a corpus row: a shell
    that starts a loop of its own and outlives the bound is reported as not
    ended, within the bound and not after the loop, and on POSIX the loop
    goes with it. The loop is finite, so where nothing ends it -- Windows --
    it is gone ten seconds later rather than at the end of the job."""
    alive = tmp_path / "alive"
    loop = f"for i in $(seq 1 100); do touch {q(alive)}; sleep 0.1; done"
    started = time.monotonic()
    ended = _run_bounded(
        [BASH, "-c", f"{q(BASH)} -c {q(loop)}; exit $?"],
        cwd=str(tmp_path),
        env=dict(os.environ),
        timeout=1,
    )
    assert not ended
    assert time.monotonic() - started < 8, "the bound waited for the loop"
    if os.name != "nt":
        alive.unlink(missing_ok=True)
        time.sleep(0.5)
        assert not alive.exists(), "the row's loop outlived the bound"


@pytest.mark.parametrize("name", sorted(CORPUS))
def test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land(
    tmp_path, name
):
    """M6's oracle as a case: where bash commits into `main` or `u` with no
    hooks, the same command with the hooks lands nothing there. The base's
    verdict is not asked -- every stop it made on a real commit is in this
    set, and so is every commit it missed."""
    home = tmp_path / "home"
    home.mkdir()
    bare = _run_corpus_row(tmp_path / "bare", CORPUS[name], False, home)
    undeclared = bare & {"main", "u"}
    if not undeclared:
        pytest.skip("bash commits into no undeclared repository with this command")
    hooked = _run_corpus_row(tmp_path / "hooked", CORPUS[name], True, home)
    assert not (hooked & undeclared), (name, sorted(hooked))


# --- S3: --no-verify ----------------------------------------------------------


def status(world, d):
    return (
        world.head(d),
        g(d, "status", "--porcelain", home=world.home, session="").stdout,
        g(d, "write-tree", home=world.home, session="").stdout,
    )


def test_s3_no_verify_is_met_where_the_branch_moves_and_nothing_moves(world):
    world.change(world.main)
    before = status(world, world.main)
    got = g(
        world.main,
        "commit",
        "--no-verify",
        "-q",
        "-m",
        "x",
        home=world.home,
        check=False,
    )
    assert got.returncode != 0
    assert status(world, world.main) == before
    assert gate.BACKSTOP in got.stderr
    assert f"No review is recorded for this cycle in {world.main}," in got.stderr


def test_s3_no_verify_into_the_declared_worktree_goes_through(world):
    world.change(world.w)
    before = world.head(world.w)
    g(world.w, "commit", "--no-verify", "-q", "-m", "x", home=world.home)
    assert world.head(world.w) != before


def test_a_commit_pre_commit_let_through_leaves_no_mark_behind(world):
    world.change(world.w)
    g(world.w, "commit", "-q", "-m", "x", home=world.home)
    judged = (
        Path(
            g(
                world.w, "rev-parse", "--absolute-git-dir", home=world.home, session=""
            ).stdout.strip()
        )
        / "specseal-judged"
    )
    assert judged.is_dir() and not list(judged.iterdir())


@pytest.mark.parametrize(
    "args",
    [
        ("reset", "-q", "--hard", "HEAD~1"),
        ("cherry-pick", "side"),
        ("merge", "-q", "--ff-only", "side"),
        ("revert", "--no-edit", "HEAD"),
    ],
    ids=["reset", "cherry-pick", "merge", "revert"],
)
def test_a_branch_moved_by_anything_but_git_commit_is_not_judged(world, args):
    """M12: only `git commit` hands the backstop GIT_AUTHOR_DATE, so the
    undeclared checkout's branch moves for every other command as before."""
    g(world.main, "branch", "side", home=world.home, session="")
    g(world.main, "switch", "-q", "side", home=world.home, session="")
    world.change(world.main)
    g(world.main, "commit", "-q", "-m", "on side", home=world.home, session="")
    g(world.main, "switch", "-q", "release", home=world.home, session="")
    if args[0] in ("reset", "revert"):
        g(world.main, "merge", "-q", "--ff-only", "side", home=world.home, session="")
    got = g(world.main, *args, home=world.home, check=False)
    assert got.returncode == 0, got.stderr
    assert gate.HEADER not in got.stderr


def diverged(world):
    """`release` and `side` in the undeclared main checkout, each changing
    f.py its own way, `side` with a second commit on top. Made as a person's
    commits, so nothing judges the setup."""
    d = world.main
    g(d, "branch", "side", home=world.home, session="")
    world.change(d, text="a = 'release'\n")
    g(d, "commit", "-q", "-m", "release", home=world.home, session="")
    g(d, "switch", "-q", "side", home=world.home, session="")
    world.change(d, text="a = 'side'\n")
    g(d, "commit", "-q", "-m", "side", home=world.home, session="")
    world.change(d, name="g.py", text="g = 1\n")
    g(d, "commit", "-q", "-m", "side 2", home=world.home, session="")
    return d


def resolve(world, d):
    world.change(d, text="a = 'both'\n")


def busy(world, d):
    gitdir = Path(
        g(
            d, "rev-parse", "--absolute-git-dir", home=world.home, session=""
        ).stdout.strip()
    )
    return any(
        (gitdir / n).exists()
        for n in ("rebase-merge", "rebase-apply", "CHERRY_PICK_HEAD", "REVERT_HEAD")
    )


def test_a_rebase_git_continues_is_not_judged(world):
    """Round 1's 🟡 7, c13: the sequencer's own `git commit -n` hands the
    backstop the author date and skips `pre-commit`. It is git's commit,
    made by a git process while a rebase is in progress, and is not judged."""
    d = diverged(world)
    g(d, "rebase", "-q", "release", home=world.home, check=False)
    resolve(world, d)
    got = g(d, "rebase", "--continue", home=world.home, check=False, GIT_EDITOR="true")
    assert gate.HEADER not in got.stderr, got.stderr
    assert got.returncode == 0, got.stderr
    assert not busy(world, d)


def test_an_interactive_rebases_reword_is_not_judged(world):
    """Round 1's 🟡 7, c09: a reword runs `pre-commit` from the sequencer."""
    d = diverged(world)
    got = g(
        d,
        "rebase",
        "-q",
        "-i",
        "HEAD~2",
        home=world.home,
        check=False,
        GIT_EDITOR="true",
        GIT_SEQUENCE_EDITOR="sed -i.bak 1s/^pick/reword/",
    )
    assert gate.HEADER not in got.stderr, got.stderr
    assert got.returncode == 0, got.stderr
    assert not busy(world, d)


@pytest.mark.parametrize("verb", ["cherry-pick", "revert"])
def test_a_pick_git_continues_is_not_judged(world, verb):
    """The same sequencer path, executed on four gits by round 1's fix pass:
    `cherry-pick --continue` and `revert --continue` run `pre-commit`."""
    d = diverged(world)
    g(d, "switch", "-q", "release", home=world.home, session="")
    if verb == "revert":
        g(
            d,
            "merge",
            "-q",
            "--ff-only",
            "--no-edit",
            "side",
            home=world.home,
            session="",
            check=False,
        )
        g(d, "reset", "-q", "--hard", "release", home=world.home, session="")
        world.change(d, text="a = 'later'\n")
        g(d, "commit", "-q", "-m", "later", home=world.home, session="")
        g(d, verb, "--no-edit", "HEAD~1", home=world.home, check=False)
    else:
        g(d, verb, "side~1", home=world.home, check=False)
    assert busy(world, d)
    resolve(world, d)
    got = g(d, verb, "--continue", home=world.home, check=False, GIT_EDITOR="true")
    assert gate.HEADER not in got.stderr, got.stderr
    assert got.returncode == 0, got.stderr
    assert not busy(world, d)


def test_a_commit_typed_while_a_rebase_is_paused_is_still_met(world):
    """What the criterion keeps: a `git commit --no-verify` a shell starts
    during a paused rebase is a commit, and its branch move is refused."""
    d = diverged(world)
    g(d, "rebase", "-q", "release", home=world.home, check=False)
    resolve(world, d)
    before = world.head(d)
    got = g(
        d, "commit", "--no-verify", "-q", "-m", "typed", home=world.home, check=False
    )
    assert got.returncode != 0
    assert gate.BACKSTOP in got.stderr
    assert world.head(d) == before


def test_a_commit_an_alias_starts_is_still_judged(world):
    """An alias runs `git commit` as a child of `git` too; with no sequencer
    state on disk it is a person's command, and is judged."""
    world.change(world.main)
    before = world.head(world.main)
    got = g(
        world.main,
        "-c",
        "alias.ci=commit",
        "ci",
        "-q",
        "-m",
        "x",
        home=world.home,
        check=False,
    )
    assert got.returncode != 0
    assert gate.HEADER in got.stderr
    assert world.head(world.main) == before


def test_concluding_a_conflicted_merge_is_judged(world):
    """Round 3's ⬜ 4, n07: `MERGE_HEAD` is no sequencer state, so `git merge
    --continue` in the undeclared main checkout is a commit the shell started,
    and it is refused with HEAD where it was."""
    d = diverged(world)
    g(d, "switch", "-q", "release", home=world.home, session="")
    g(d, "merge", "-q", "side", home=world.home, session="", check=False)
    resolve(world, d)
    before = world.head(d)
    got = g(d, "merge", "--continue", home=world.home, check=False, GIT_EDITOR="true")
    assert got.returncode != 0, got.stderr
    assert gate.HEADER in got.stderr
    assert world.head(d) == before


def test_a_mark_an_aborted_commit_left_passes_no_later_commit(world):
    """Round 1's 🟡 10, c16: the same HEAD, tree and author date, and another
    `git commit` process, which `pre-commit` never saw."""
    world.change(world.main)
    date = {"GIT_AUTHOR_DATE": "@1790000000 +0000"}
    aborted = g(
        world.main,
        "-c",
        "specseal.waive=review",
        "commit",
        "-q",
        "-m",
        "",
        home=world.home,
        check=False,
        **date,
    )
    assert aborted.returncode != 0
    before = world.head(world.main)
    got = g(
        world.main,
        "commit",
        "--no-verify",
        "-q",
        "-m",
        "x",
        home=world.home,
        check=False,
        **date,
    )
    assert got.returncode != 0, "a stale mark let a later commit through"
    assert gate.BACKSTOP in got.stderr
    assert world.head(world.main) == before


# --- S4, S5: who the refusal is put to --------------------------------------


def press(world):
    projects = world.home / ".claude" / "projects"
    write_transcript(projects, SESSION, ask_entries(world.main))


AUTOMATION_TEXT = (
    "This session's person pressed `automation` on the routing question, so "
    "no question is put to them, and none is to be put to them in its place: "
    "the run was promised that nothing would stop to ask.\n\n"
    "The ways on, none of which needs a person:\n"
    "  1. Only for a commit that belongs to no work item: re-issue it as "
    "`git -c specseal.waive=review commit …`. The older spelling, "
    "`: '[no-review]'; git commit …`, still works.\n"
    "  2. Otherwise, do not retry it: write the commit down and hand it back "
    "at the end of the run."
)


def test_s4_under_the_press_the_refusal_names_no_question_tool(world):
    press(world)
    world.change(world.main)
    got = g(world.main, "commit", "-q", "-m", "x", home=world.home, check=False)
    assert got.returncode != 0
    assert got.stderr.startswith(
        "SpecSeal stopped this commit; nothing was committed.\n"
    )
    assert AUTOMATION_TEXT in got.stderr
    assert "AskUserQuestion" not in got.stderr
    assert got.stderr.rstrip().endswith(
        "Re-issuing this commit unchanged meets this same refusal."
    )
    assert (
        got.stderr == gate.refusal(["review"], str(world.main), "release", True) + "\n"
    )


def test_s5_an_attended_session_is_told_to_ask_and_the_second_attempt_is_the_same(
    world,
):
    world.change(world.main)
    first = g(world.main, "commit", "-q", "-m", "x", home=world.home, check=False)
    second = g(world.main, "commit", "-q", "-m", "x", home=world.home, check=False)
    assert first.returncode != 0 and second.returncode != 0
    assert first.stderr == second.stderr
    text = first.stderr
    assert (
        "Do not choose for the user. Ask with the AskUserQuestion tool, offering "
        "exactly these three options:" in text
    )
    assert '    1. "Declare the routing" — ' in text
    assert '    2. "Review it first" — ' in text
    assert (
        '    3. "Commit without a review" — re-issue it as '
        "`git -c specseal.waive=review commit …`. The older spelling, "
        "`: '[no-review]'; git commit …`, still works." in text
    )
    assert "Then do what they picked." in text


def test_s5_both_spellings_the_refusal_names_actually_commit(world):
    world.change(world.main)
    before = world.head(world.main)
    g(
        world.main,
        "-c",
        "specseal.waive=review",
        "commit",
        "-q",
        "-m",
        "x",
        home=world.home,
    )
    assert world.head(world.main) != before
    # The old spelling, through the PreToolUse writer that carries it.
    world.change(world.main)
    before = world.head(world.main)
    command = ": '[no-review]'; git commit -q -m y"
    group(world, "pre-bash", command, "toolu_a")
    got = as_a_call(world, command)
    assert got.returncode == 0, got.stderr
    assert world.head(world.main) != before
    group(world, "post-bash", command, "toolu_a")
    world.change(world.main)
    again = as_a_call(world, "git commit -q -m z")
    assert again.returncode != 0, "the answer outlived the call that carried it"


def group(world, name, command, call):
    """One dispatcher group for one Bash call, as the harness runs it."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": str(world.main),
        "session_id": SESSION,
        "tool_use_id": call,
    }
    subprocess.run(
        [sys.executable, str(HOOKS / "dispatch.py"), name],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env(world.home),
        check=True,
        timeout=60,
    )


def as_a_call(world, command):
    """COMMAND as the Bash tool runs it: a shell of its own, carrying the
    command in its argv for as long as the command runs, below a process
    named `claude`."""
    claude = world.tmp / "bin" / "claude"
    if not claude.exists():
        fake_claude(world)
    return subprocess.run(
        [str(claude), "-c", f'{q(BASH)} -c "$CALL_COMMAND"; exit $?'],
        cwd=str(world.main),
        capture_output=True,
        text=True,
        env=env(world.home, CALL_COMMAND=as_the_tool_spells_it(command)),
        stdin=subprocess.DEVNULL,
        timeout=60,
    )


def test_an_old_spelling_waives_no_other_agents_commit(world):
    """Round 1's 🟡 9, c25: while agent A's call carrying `[no-review]` runs,
    agent B's commit under the same session id is its own command, and is
    judged; and B's call starting does not take A's answer away."""
    a = ": '[no-review]'; git commit -q -m a"
    group(world, "pre-bash", a, "toolu_a")
    group(world, "pre-bash", "git commit -q -m b", "toolu_b")
    world.change(world.main)
    before = world.head(world.main)
    b = as_a_call(world, "git commit -q -m b")
    assert b.returncode != 0, "A's token waived B's commit"
    assert world.head(world.main) == before
    group(world, "post-bash", "git commit -q -m b", "toolu_b")
    got = as_a_call(world, a)
    assert got.returncode == 0, got.stderr
    assert world.head(world.main) != before


def test_s6_inside_a_message_the_waiver_is_prose(world):
    world.change(world.main)
    before = world.head(world.main)
    got = g(
        world.main,
        "commit",
        "-q",
        "-m",
        "specseal.waive=review later",
        home=world.home,
        check=False,
    )
    assert got.returncode != 0
    assert world.head(world.main) == before


# --- S9: the session without the environment variable -----------------------


def fake_claude(world):
    """A shell named `claude`, so the hook's ancestry has one.

    A symlink to bash, executed through its own name: `ps` then names the
    process `claude` (its path, on macOS). Not `sh`, because macOS's `/bin/sh`
    is a launcher that re-executes another shell under another name; and not a
    copy, because macOS kills a copied system binary on launch (measured:
    exit 137)."""
    d = world.tmp / "bin"
    d.mkdir()
    symlink_or_skip(BASH, d / "claude")
    return d / "claude"


def lease_then(world, body):
    """A `claude` process that writes its own lease, then runs BODY."""
    gitdir = g(
        world.main, "rev-parse", "--absolute-git-dir", home=world.home, session=""
    ).stdout.strip()
    leases = Path(gitdir) / "specseal-leases"
    # `; exit $?` keeps the shell from exec-ing the last command in its own
    # place, which would take the `claude` process out of the ancestry.
    return (
        f"mkdir -p {q(leases)} && printf '{{\"pid\": %s}}' $$ > {q(leases / SESSION)}"
        f" && {body}; exit $?"
    )


def test_s9_the_lease_names_the_session_when_no_variable_is_exported(world):
    claude = fake_claude(world)
    press(world)
    world.change(world.main)
    before = world.head(world.main)
    got = subprocess.run(
        [str(claude), "-c", lease_then(world, "git commit -q -m x")],
        cwd=str(world.main),
        capture_output=True,
        text=True,
        env=env(world.home, session=""),
        stdin=subprocess.DEVNULL,
        timeout=60,
    )
    assert got.returncode != 0
    assert world.head(world.main) == before
    assert AUTOMATION_TEXT in got.stderr


def test_s9_an_emptied_environment_is_still_judged_through_the_lease(world):
    """M6's two rows a probe could not see: `env -i git commit …`."""
    claude = fake_claude(world)
    world.change(world.main)
    before = world.head(world.main)
    path = os.environ.get("PATH", "")
    got = subprocess.run(
        [
            str(claude),
            "-c",
            lease_then(
                world, f"env -i PATH={q(path)} HOME={q(world.home)} git commit -q -m x"
            ),
        ],
        cwd=str(world.main),
        capture_output=True,
        text=True,
        env=env(world.home, session=""),
        stdin=subprocess.DEVNULL,
        timeout=60,
    )
    assert got.returncode != 0, got.stderr
    assert world.head(world.main) == before


def test_s9_no_variable_and_no_lease_is_a_persons_own_commit(world):
    """P2, answer (a)."""
    world.change(world.main)
    before = world.head(world.main)
    g(world.main, "commit", "-q", "-m", "mine", home=world.home, session="")
    assert world.head(world.main) != before


def test_s9_a_lease_for_another_pid_names_no_session(world):
    gitdir = g(
        world.main, "rev-parse", "--absolute-git-dir", home=world.home, session=""
    ).stdout.strip()
    leases = Path(gitdir) / "specseal-leases"
    leases.mkdir()
    (leases / "someone").write_text('{"pid": 1}', encoding="utf-8")
    world.change(world.main)
    before = world.head(world.main)
    g(world.main, "commit", "-q", "-m", "mine", home=world.home, session="")
    assert world.head(world.main) != before


# --- S13: a clone that opted out ----------------------------------------------


@pytest.mark.parametrize("how", ["scratch", "no root"])
def test_s13_a_stub_in_a_clone_that_opted_out_is_silent(world, how):
    if how == "scratch":
        (world.main / ".git" / "specseal-scratch").write_text("", encoding="utf-8")
    else:
        shutil.rmtree(world.main / "seal")
    world.change(world.main)
    before = world.head(world.main)
    got = g(world.main, "commit", "-q", "-m", "x", home=world.home)
    assert world.head(world.main) != before
    assert got.stderr == ""


# --- the arms ----------------------------------------------------------------


def test_a_review_mark_naming_head_lets_the_commit_through(world):
    (world.main / ".git" / "specseal-reviewed").write_text(
        world.head(world.main), encoding="utf-8"
    )
    world.change(world.main)
    before = world.head(world.main)
    g(world.main, "commit", "-q", "-m", "x", home=world.home)
    assert world.head(world.main) != before


def test_the_parity_arm_reads_the_paths_git_is_committing(world):
    (world.w / "seal" / "parity.md").write_text("# parity\n", encoding="utf-8")
    (world.w / "docs").mkdir()
    (world.w / "docs" / "a.md").write_text("x\n", encoding="utf-8")
    g(world.w, "add", "docs/a.md", home=world.home, session="")
    before = world.head(world.w)
    g(world.w, "commit", "-q", "-m", "docs only", home=world.home)
    assert world.head(world.w) != before
    (world.w / "f.py").write_text("a = 3\n", encoding="utf-8")
    got = g(world.w, "commit", "-q", "-am", "code", home=world.home, check=False)
    assert got.returncode != 0
    assert gate.STATES["parity"].format(top=world.w) in got.stderr
    g(
        world.w,
        "-c",
        "specseal.waive=parity",
        "commit",
        "-q",
        "-am",
        "code",
        home=world.home,
    )
    # A comparison recorded at HEAD lets the next code commit through.
    gitdir = Path(
        g(
            world.w, "rev-parse", "--absolute-git-dir", home=world.home, session=""
        ).stdout.strip()
    )
    (gitdir / "specseal-parity").write_text(world.head(world.w), encoding="utf-8")
    (world.w / "f.py").write_text("a = 4\n", encoding="utf-8")
    before = world.head(world.w)
    g(world.w, "commit", "-q", "-am", "compared", home=world.home)
    assert world.head(world.w) != before


def test_no_session_is_judged_by_nothing_in_python_either(world):
    """The stub leaves before Python for P2; the entry point says the same
    thing on its own, for a stub an older plugin wrote."""
    world.change(world.main)
    environ = env(world.home, session="")
    assert commitgate.pre_commit(str(world.main), environ, io.StringIO()) == 0


# --- the fallback stands aside where git decides ------------------------------


def pre_bash(world, command, cwd):
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": str(cwd),
        "session_id": SESSION,
    }
    out = subprocess.run(
        [sys.executable, str(HOOKS / "dispatch.py"), "pre-bash"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env(world.home),
        timeout=60,
    ).stdout
    if not out.strip():
        return "silent"
    return (json.loads(out).get("hookSpecificOutput") or {}).get(
        "permissionDecision", "silent"
    )


def test_the_text_reading_stands_aside_where_git_decides(world):
    """The recorded run's 13 asks: a reading that named the main checkout for
    a commit landing in the declared worktree. Git decides in that clone, so
    the reading says nothing, whatever it read. `eval "$C"` stood here until
    P7, and is judged now (`STEPS_AROUND`)."""
    for command in (
        f"cd {q(world.w)} && true; git commit -m x",
        "git commit -m x",
    ):
        assert pre_bash(world, command, world.main) == "silent", command


def test_a_foreign_clone_keeps_the_text_reading(world, monkeypatch):
    """P1 (a), P5 (a): a clone whose hooks slot is somebody else's is judged
    as 0.16.0 judged it."""
    g(world.u, "config", "core.hooksPath", ".husky", home=world.home, session="")
    assert pre_bash(world, f"git -C {q(world.u)} commit -m x", world.main) == "deny"


STEPS_AROUND = {
    "-c core.hooksPath": "git -c core.hooksPath=/dev/null commit -m x",
    "the key in another case": "git -c CORE.HOOKSPATH=/dev/null commit -m x",
    "--config-env": "git --config-env=core.hooksPath=H commit -m x",
    "GIT_CONFIG_COUNT": (
        "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath "
        "GIT_CONFIG_VALUE_0=/nonexistent git commit -m x"
    ),
    "GIT_CONFIG_PARAMETERS": (
        "GIT_CONFIG_PARAMETERS=\"'core.hookspath'='/x'\" git commit -m x"
    ),
    "an exported GIT_CONFIG": "export GIT_CONFIG_GLOBAL=/x/g; git commit -m x",
    "env -i": "env -i PATH=/usr/bin git commit -m x",
    "env --ignore-environment": "env --ignore-environment git commit -m x",
    "a path-qualified env -": "/usr/bin/env - git commit -m x",
    "env -i in a subshell": "(env -i git commit -m x)",
    "GIT_CONFIG in a subshell": "(GIT_CONFIG_GLOBAL=/x/g git commit -m x)",
    "an unreadable command": "git commit -m 'x",
    # Round 2's 🟡 1: the session variables the stub reads, removed another
    # way than `env -i`. A harness may export one of the two, so either alone
    # is enough to leave the stub no session, and each case names one.
    "an emptied session variable": "CLAUDECODE= git commit -m x",
    "a session variable in a subshell": "(CLAUDECODE= git commit -m x)",
    "env -u": "env -u CLAUDECODE git commit -m x",
    "env -u glued to its name": "env -uCLAUDE_CODE_SESSION_ID git commit -m x",
    "env --unset=": "env --unset=CLAUDECODE git commit -m x",
    "unset": "unset CLAUDE_CODE_SESSION_ID; git commit -m x",
    # Round 2's 🟡 2: a config file the command names, which can carry
    # core.hooksPath where no word does.
    "include.path": "git -c include.path=/x/cfg commit -m x",
    "includeIf": "git -c includeIf.onbranch:main.path=/x/cfg commit -m x",
    "include.path through --config-env": (
        "git --config-env=include.path=CFG commit -m x"
    ),
    "include.path through git config": (
        "git config include.path /x/cfg && git commit -m x"
    ),
    "HOME": "HOME=/x/h git commit -m x",
    "XDG_CONFIG_HOME": "XDG_CONFIG_HOME=/x/c git commit -m x",
    # Round 3's 🟡 1: a string a shell parses again. None of these is plain,
    # so the reading judges each (P7, the owner's answer of 2026-10-02).
    "sh -c unsetting a session variable": "sh -c 'unset CLAUDECODE; git commit -m x'",
    "include.path behind cd in bash -c": (
        "bash -c 'cd . && git -c include.path=/x/cfg commit -m x'"
    ),
    "GIT_CONFIG behind cd in sh -c": (
        "sh -c 'cd . && GIT_CONFIG_GLOBAL=/x/g git commit -m x'"
    ),
    "HOME in a quoted substitution": 'echo "$(cd . && HOME=/x/h git commit -m x)"',
    "eval of a literal string": "eval 'unset CLAUDECODE; git commit -m x'",
    # P7: an `eval` is not plain, so the reading's fail-closed answer for one
    # whose argument it cannot reduce comes back, as 0.16.0 gave it.
    "eval of a variable": 'eval "$C"',
    # Round 3's 🟡 2: the environment emptied with another option first.
    "env -v -i": "env -v -i git commit -m x",
    "env -u then -i": "env -u FOO -i git commit -m x",
    "env -u glued behind a flag": "env -vuCLAUDECODE git commit -m x",
    "env -S splitting a -u": "env -S'-u CLAUDECODE' git commit -m x",
    "exec -c": "(exec -c git commit -m x)",
    # The limit beside the removed stub: `rm` and `chmod` are not plain, so
    # a command that takes the stubs away first is judged (P7).
    "the stubs removed first": (
        "rm -f .git/hooks/pre-commit .git/hooks/reference-transaction"
        " && git commit -m x"
    ),
    "the stubs' execute bit taken first": (
        "chmod -x .git/hooks/pre-commit .git/hooks/reference-transaction"
        " && git commit -m x"
    ),
}


@pytest.mark.parametrize("name", sorted(STEPS_AROUND))
def test_a_command_that_can_step_around_the_hooks_keeps_the_text_reading(world, name):
    """Round 1's 🟡 2 and 🟡 8, and round 2's 🟡 1 and 🟡 2: a setting, a
    config file that can carry one, an emptied environment or a removed
    session variable that lives in the one command
    can keep git from running the stubs, or the stub from finding the session,
    so the reading that asked before the command does not stand aside for it.
    A misread costs one refusal."""
    assert pre_bash(world, STEPS_AROUND[name], world.main) == "deny", name


@pytest.mark.parametrize(
    "command",
    [
        "git commit -m x",
        "git -c specseal.waive=parity commit -m x",
        "env FOO=1 git commit -m x",
        "printenv GIT_DIR",
        "echo GIT_CONFIG_NOSYSTEM",
        # A session name is read whole: expanded, or inside a message, it
        # removes nothing (round 2 of #692, 🟡 1).
        "echo $CLAUDECODE",
        "git commit -m 'mentions CLAUDE_CODE_SESSION_ID'",
        # A config key or HOME is read whole too (round 2 of #692, 🟡 2).
        "cat $HOME/x",
        "printenv HOME",
        "git -c user.name=HOME commit -m x",
        "git commit -m 'read include.path'",
        "",
    ],
)
def test_only_those_words_make_the_reading_judge_a_git_decided_clone(command):
    """The word list alone does not over-read. Since P7 the reading also
    judges every shape `tokens.is_plain` does not recognise; the cases below
    pin which of these commands are plain."""
    assert not tokens.steps_around_hooks(command)


# P7 (2026-10-02): the reading stands aside only for a command whose shape is
# known plain. These are the negatives above, sorted by that rule.
STILL_PLAIN = [
    "git commit -m x",
    "git -c specseal.waive=parity commit -m x",
    "echo GIT_CONFIG_NOSYSTEM",
    "echo $CLAUDECODE",
    "git commit -m 'mentions CLAUDE_CODE_SESSION_ID'",
    "cat $HOME/x",
    "git -c user.name=HOME commit -m x",
    "git commit -m 'read include.path'",
]
# Not plain any more, so the 0.16.0 reading judges them: `env`, `printenv`
# and `cat` with an expansion are programs outside the allowlist, and an
# empty command is no shape at all.
NO_LONGER_PLAIN = [
    "env FOO=1 git commit -m x",
    "printenv GIT_DIR",
    "printenv HOME",
    "",
]


@pytest.mark.parametrize(
    "command",
    [
        "git",  # a git with no subcommand
        "git -C /x/m; echo y",  # the same, before a separator
        "git --git-dir=/x/m commit -m x",  # a global option outside the rule
        ': "${X:=y}"; git commit -m x',  # an assignment inside an expansion
        "echo x(y); git commit -m x",  # a parenthesis inside a word
        "echo {a,b}; git commit -m x",  # a brace outside quotes
        "cat <<EOF\n'\nEOF\necho '",  # splits whole, but not once the body goes
        # A word the list reads, in an otherwise plain shape (round 3's m07):
        # it costs one judgment, which is the list's direction (P6).
        "git commit -m CLAUDECODE",
        "git commit -m x >&f",  # output duplicated onto a file
        "git diff --output=/x/o; git commit -m x",  # an option that writes
        "/usr/bin/git commit -m x",  # a program that is not the bare word
    ],
)
def test_each_other_condition_of_the_rule_makes_a_command_not_plain(command):
    assert not tokens.is_plain(command)


@pytest.mark.parametrize("command", STILL_PLAIN)
def test_a_negative_that_is_plain_stays_plain(command):
    assert tokens.is_plain(command)


@pytest.mark.parametrize("command", NO_LONGER_PLAIN)
def test_a_negative_outside_the_allowlist_is_not_plain(command):
    assert not tokens.is_plain(command)


# The shapes this repository's own agents type, and the same shape with one
# thing outside the rule. Each pair differs in one place.
PLAIN_AND_NOT = {
    "-m": ('git -C {d} commit -q -m "x"', 'git -C {d} commit -q -m "x"; ls'),
    "-F a file": ("git -C {d} commit -F {f}", "git -C {d} commit -F {f}; printenv"),
    "a quoted heredoc": (
        "git -C {d} commit -q -F - <<'EOF'\nfix `x` and $(y)\nEOF",
        "git -C {d} commit -q -F - <<EOF\nfix $(y)\nEOF",
    ),
    "cd first": ("cd {d} && git commit -q -m x", "cd {d} && X=1 git commit -q -m x"),
    "piped to tail": (
        "git -C {d} commit -q -m x 2>&1 | tail -3",
        "git -C {d} commit -q -m x 2>&1 | xargs echo",
    ),
    "to /dev/null": (
        "git -C {d} commit -q -m x >/dev/null",
        "git -C {d} commit -q -m x >{f}.out",
    ),
    "a -c the plugin reads": (
        "git -C {d} -c commit.gpgsign=false commit -q -m x",
        "git -C {d} -c core.editor=true commit -q -m x",
    ),
    "a subcommand outside the list": (
        "git -C {d} add f.py && git -C {d} commit -q -m x",
        "git -C {d} stash && git -C {d} commit -q -m x",
    ),
    "printf with no option": (
        "printf '%s\\n' x; git -C {d} commit -q -m x",
        "printf -v y x; git -C {d} commit -q -m x",
    ),
    "a substitution": (
        "git -C {d} commit -q -m 'it is $(x)'",
        'git -C {d} commit -q -m "it is $(echo x)"',
    ),
    "a subshell": ("git -C {d} commit -q -m x", "(git -C {d} commit -q -m x)"),
    "a second line": (
        "git -C {d} commit -q -m x\ngit -C {d} log -1",
        "git -C {d} commit -q -m x\nsh -c true",
    ),
}


@pytest.mark.parametrize("name", sorted(PLAIN_AND_NOT))
def test_a_plain_agent_commit_stands_aside_and_one_word_more_is_judged(world, name):
    """The allowlist's boundary in both directions (P7): the plain form is
    left to git, which refuses it itself, and the form with one thing outside
    the rule meets the 0.16.0 reading, which denies a commit into the
    undeclared main checkout."""
    msg = world.tmp / "msg.txt"
    msg.write_text("x\n", encoding="utf-8")
    plain, other = (s.format(d=q(world.main), f=q(msg)) for s in PLAIN_AND_NOT[name])
    assert tokens.is_plain(plain), plain
    assert not tokens.is_plain(other), other
    assert pre_bash(world, plain, world.main) == "silent", plain
    assert pre_bash(world, other, world.main) == "deny", other


# --- post-commit: the implementer notice --------------------------------------


def test_the_notice_follows_a_commit_git_made(world):
    routing_md = world.w / "seal" / "specs" / "1790000000-x" / "routing.md"
    routing_md.write_text(
        routing_md.read_text(encoding="utf-8") + "| Implementation | smith |\n",
        encoding="utf-8",
    )
    world.change(world.w)
    first = g(world.w, "commit", "-q", "-m", "x", home=world.home)
    assert "answers `Implementation` with `smith`" in first.stdout + first.stderr
    world.change(world.w)
    second = g(world.w, "commit", "-q", "-m", "y", home=world.home)
    assert "answers `Implementation`" not in second.stdout + second.stderr


def test_the_post_tool_use_notice_stands_aside_where_git_says_it(world, monkeypatch):
    notice = load_hook_module("implementer-notice.py", "notice_beside_post_commit")
    routing_md = world.w / "seal" / "specs" / "1790000000-x" / "routing.md"
    routing_md.write_text(
        routing_md.read_text(encoding="utf-8") + "| Implementation | smith |\n",
        encoding="utf-8",
    )
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": "git commit -m x"},
        "cwd": str(world.w),
        "session_id": "s-other",
    }
    out = io.StringIO()
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    monkeypatch.setattr(sys, "stdout", out)
    notice.main()
    assert out.getvalue() == ""


# --- the units underneath ----------------------------------------------------

import commitgate  # noqa: E402
import hooksession  # noqa: E402


def test_the_mark_names_one_commit():
    """The old HEAD, the tree and the commit's own author date: a mark left
    by a commit that aborted after pre-commit does not pass a later one."""
    base = commitgate._key("a" * 40, "t", "@1 +0000")
    assert base != commitgate._key("a" * 40, "t", "@2 +0000")
    assert base != commitgate._key("b" * 40, "t", "@1 +0000")
    assert base != commitgate._key("a" * 40, "u", "@1 +0000")
    # A root commit's old value is the null id at the ref and nothing in
    # pre-commit; both name the same commit.
    assert commitgate._key("0" * 40, "t", "@1 +0000") == commitgate._key(
        "", "t", "@1 +0000"
    )
    # And the `git commit` process both hooks are children of (🟡 10).
    assert commitgate._key("a" * 40, "t", "@1 +0000", 7) != commitgate._key(
        "a" * 40, "t", "@1 +0000", 8
    )


def test_the_backstop_judges_only_prepared(world):
    world.change(world.main)
    lines = [f"{world.head(world.main)} {'f' * 40} refs/heads/release"]
    e = env(world.home, GIT_AUTHOR_DATE="@1 +0000")
    for state in ("committed", "aborted"):
        assert (
            commitgate.reference_transaction(
                str(world.main), e, state, lines, io.StringIO()
            )
            == 0
        )


def test_a_detached_head_commit_past_no_verify_is_met_too(world):
    g(world.main, "switch", "-q", "--detach", "HEAD", home=world.home, session="")
    world.change(world.main)
    before = world.head(world.main)
    got = g(
        world.main,
        "commit",
        "--no-verify",
        "-q",
        "-m",
        "x",
        home=world.home,
        check=False,
    )
    assert got.returncode != 0
    assert world.head(world.main) == before
    assert gate.BACKSTOP in got.stderr


def test_two_leases_naming_one_pid_name_no_session(tmp_path):
    """W3: nobody can tell from here which of the two the hook runs under."""
    common = tmp_path / "git"
    leases = common / "specseal-leases"
    leases.mkdir(parents=True)
    (leases / "a").write_text('{"pid": 4242}', encoding="utf-8")
    assert hooksession.from_lease(str(common), 4242) == "a"
    (leases / "b").write_text('{"pid": 4242}', encoding="utf-8")
    assert hooksession.from_lease(str(common), 4242) == ""


def test_a_lease_in_a_linked_worktree_is_read(tmp_path):
    common = tmp_path / "git"
    leases = common / "worktrees" / "wt" / "specseal-leases"
    leases.mkdir(parents=True)
    (leases / "s9").write_text('{"pid": 4242}', encoding="utf-8")
    assert hooksession.from_lease(str(common), 4242) == "s9"
    assert hooksession.from_lease(str(common), 4243) == ""
