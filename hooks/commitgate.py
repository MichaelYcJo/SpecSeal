"""The commit gate as git runs it: `pre-commit`, its `reference-transaction`
backstop, and `post-commit`'s notice (#692).

`hooks/git/*.py` are thin entry points into this module, so that a case can
drive one hook in-process and the stubs run the same code from a shell. What
each hook reads, and why each reading is the right one, is in those files'
docstrings; what is judged is `hooks/gate.py`'s.

Nothing here reads `GIT_DIR`. git does not export it to `pre-commit`,
`post-commit` or `post-checkout` (phase 1's M4, on 2.50.1), so every reading
asks `git rev-parse` in the working directory git gave the hook.

**A commit git makes for its own sequencer is not judged** (round 1 of #692,
🟡 7). `rebase --continue`, a reword, `cherry-pick --continue` and `revert
--continue` each commit through a child `git commit`, which hands both hooks
the author date and, for the first, skips `pre-commit`. Measured on 2.34.1,
2.39.5, 2.43.0 and 2.50.1, that child is the one commit whose starter is
another `git` process while a sequencer state is on disk. A commit a shell
starts during a paused rebase -- `--amend` at an `edit` stop, `--no-verify`
before `--continue` -- has a shell for its starter, and is judged. An alias
(`git -c alias.ci=commit ci`) is started by git too, so the state has to be
there as well. `GIT_REFLOG_ACTION` is no criterion for this either: the
rebase's children set it, and cherry-pick's and revert's do not.
"""

import hashlib
import importlib.util
import os
import subprocess
import time

import answers
import gate
import hooksession
import optin
import routing

# One empty file per commit `pre-commit` let through, under the worktree's own
# git directory, named for the commit it judged. `reference-transaction`
# removes it when the branch moves; one left behind by a commit that aborted
# after `pre-commit` (an empty message, a failing `commit-msg`) names a tree
# and a date nothing will commit again, and is pruned after a day.
JUDGED = "specseal-judged"
PRUNE_AFTER = 24 * 60 * 60

ZERO = set("0")


def _context(cwd, environ):
    """(top, common, session) for a hook running in `cwd`, or None when the
    hook has nothing to judge: no repository, a repository that does not opt
    in (S13), or no Claude session behind the command (P2)."""
    top = optin.repo_root(cwd)
    if not top:
        return None
    common = optin.git_common_dir(top)
    if not optin.home_at(top, common):
        return None
    session, _route = hooksession.session(common, environ)
    if not session:
        return None
    return top, common, session


def waived(cwd, session):
    """The arms this command waived: `-c specseal.waive=<arm>`, and the old
    bare word carried over from the Bash call this commit runs under (P3,
    round 1's 🟡 9). The ancestry is walked once, and only if an answer is
    there to match it."""
    out = set()
    # `config --get-all` exits 1 where no such key is set: no waiver, git's
    # ordinary no, not a failure.
    configured = gate.git(["config", "--get-all", "specseal.waive"], cwd) or ""
    for value in configured.splitlines():
        for word in value.replace(",", " ").split():
            if word in (gate.REVIEW, gate.PARITY):
                out.add(word)
    walked = []

    def args():
        if not walked:
            walked.append(hooksession.call_args())
        return walked[0]

    for arm, token in gate.TOKENS.items():
        if answers.given(session, token, args):
            out.add(arm)
    return out


def pressed(top, session):
    """True when the session's person pressed `automation`. Every way of not
    reading it is False, the answer from before it was read."""
    try:
        import worktree_consent

        return worktree_consent.automation_answered(top, session, "") is True
    except Exception:
        return False


def _git_process():
    """The `git commit` process this hook runs under, as a string; "" where it
    cannot be named the same way from both hooks.

    The stub `exec`s the interpreter, so on a POSIX system its parent is the
    `git commit` that ran the hook, and both hooks of one commit share it
    (measured on four gits by round 1's fix pass). Git for Windows runs each
    hook through its own `sh.exe`, whose pid differs per hook, so there the
    mark is keyed without it.
    """
    return "" if os.name == "nt" else str(os.getppid())


def _key(old, tree, date, process=None):
    # The process is round 1's 🟡 10: a commit that aborted after
    # `pre-commit` (an empty message, a failing `commit-msg`) left a mark for
    # the same HEAD, tree and date, and a later `--no-verify` commit with that
    # date took it. The later commit is another `git` process.
    old = "" if not old or set(old) <= ZERO else old
    process = _git_process() if process is None else process
    return hashlib.sha1(f"{old}\n{tree}\n{date}\n{process}".encode()).hexdigest()


# What git leaves under a worktree's git directory while a rebase, a
# cherry-pick or a revert is in progress there.
SEQUENCER = (
    "rebase-merge",
    "rebase-apply",
    "sequencer",
    "CHERRY_PICK_HEAD",
    "REVERT_HEAD",
)


def _process(pid):
    """(parent pid, command name) of process `pid`; (None, "") unreadable."""
    try:
        out = subprocess.run(
            ["ps", "-o", "ppid=,comm=", "-p", str(pid)],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None, ""
    parent, _, comm = out.partition(" ")
    try:
        return int(parent), os.path.basename(comm.strip())
    except ValueError:
        return None, ""


def _sequencer_commit(cwd, commit=None):
    """True when git is making this commit for its own rebase, cherry-pick or
    revert: a sequencer state on disk, and the `git commit` running the hook
    started by another `git` process. Every way of not reading it is False,
    so the commit is judged; on Windows, where no `ps` answers, it always is.
    """
    git_dir = gate.git(["rev-parse", "--absolute-git-dir"], cwd) or ""
    if not git_dir or not any(
        os.path.exists(os.path.join(git_dir, name)) for name in SEQUENCER
    ):
        return False
    if commit is None:
        if os.name == "nt":
            return False
        commit = os.getppid()
    starter, _name = _process(commit)
    _parent, name = _process(starter)
    return name == "git"


def _judged_dir(cwd):
    # Outside a repository `rev-parse` exits non-zero: no directory, and no
    # mark is left or taken.
    git_dir = gate.git(["rev-parse", "--absolute-git-dir"], cwd) or ""
    return os.path.join(git_dir, JUDGED) if git_dir else ""


def _leave_mark(cwd, head, date):
    d = _judged_dir(cwd)
    # A tree git could not write leaves no mark, so the backstop judges.
    tree = gate.git(["write-tree"], cwd) or ""
    if not d or not tree or not date:
        return
    try:
        os.makedirs(d, exist_ok=True)
        cutoff = time.time() - PRUNE_AFTER
        for name in os.listdir(d):
            p = os.path.join(d, name)
            try:
                if os.stat(p).st_mtime < cutoff:
                    os.remove(p)
            except OSError:
                pass
        open(os.path.join(d, _key(head, tree, date)), "w", encoding="utf-8").close()
    except OSError:
        pass


def _take_mark(cwd, old, new, date):
    """True when `pre-commit` judged this update; the mark is used up."""
    d = _judged_dir(cwd)
    # `--verify --quiet` exits 1 for a name with no tree: no mark to take.
    tree = gate.git(["rev-parse", "--verify", "--quiet", f"{new}^{{tree}}"], cwd) or ""
    if not d or not tree:
        return False
    path = os.path.join(d, _key(old, tree, date))
    try:
        os.remove(path)
    except OSError:
        return False
    return True


def _refuse(stream, arms, top, cwd, session, backstop=False):
    branch = routing.current_branch(cwd)
    stream.write(
        gate.refusal(arms, top, branch, pressed(top, session), backstop) + "\n"
    )
    return 1


def pre_commit(cwd, environ, stream):
    context = _context(cwd, environ)
    if context is None:
        return 0
    top, _common, session = context
    # An unborn branch exits non-zero: no HEAD is git's ordinary no.
    head = gate.git(["rev-parse", "--verify", "--quiet", "HEAD"], cwd) or ""
    arms = gate.arms_missing(
        cwd,
        top,
        waived(cwd, session),
        # None where `git diff` failed, which the parity arm asks about (#868).
        lambda: gate.lines(gate.git(["diff", "--cached", "--name-only"], cwd)),
        head=head,
    )
    if arms and not _sequencer_commit(cwd):
        return _refuse(stream, arms, top, cwd, session)
    _leave_mark(cwd, head, environ.get("GIT_AUTHOR_DATE", ""))
    return 0


def _commit_lines(lines, cwd):
    """The (old, new) pairs of this transaction that move a branch or a
    detached HEAD, once each."""
    # `symbolic-ref -q` exits 1 on a detached HEAD, which is the answer read.
    detached = not (gate.git(["symbolic-ref", "-q", "HEAD"], cwd) or "")
    seen, out = set(), []
    for line in lines:
        parts = line.split()
        if len(parts) != 3:
            continue
        old, new, ref = parts
        if set(new) <= ZERO:
            continue
        if not (ref.startswith("refs/heads/") or (ref == "HEAD" and detached)):
            continue
        if (old, new) in seen:
            continue
        seen.add((old, new))
        out.append((old, new))
    return out


def _paths_between(cwd, base, new):
    """A callable listing the paths the commit `new` carries over `base` --
    over nothing, for a root commit -- or answering None where git could not
    list them, which the parity arm asks about (#868)."""
    if base:
        args = ["diff", "--name-only", base, new]
    else:
        args = ["diff-tree", "--root", "-r", "--name-only", "--no-commit-id", new]
    return lambda: gate.lines(gate.git(args, cwd))


def reference_transaction(cwd, environ, state, lines, stream):
    date = environ.get("GIT_AUTHOR_DATE", "")
    if state != "prepared" or not date:
        return 0
    pairs = _commit_lines(lines, cwd)
    if not pairs:
        return 0
    context = _context(cwd, environ)
    if context is None:
        return 0
    top, _common, session = context
    for old, new in pairs:
        if _take_mark(cwd, old, new, date):
            continue
        base = "" if set(old) <= ZERO else old
        arms = gate.arms_missing(
            cwd, top, waived(cwd, session), _paths_between(cwd, base, new), head=base
        )
        if arms and not _sequencer_commit(cwd):
            return _refuse(stream, arms, top, cwd, session, backstop=True)
    return 0


def _notice_module():
    spec = importlib.util.spec_from_file_location(
        "specseal_implementer_notice",
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "implementer-notice.py"
        ),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def post_commit(cwd, environ, stream):
    context = _context(cwd, environ)
    if context is None:
        return 0
    _top, _common, session = context
    try:
        said = _notice_module().notify(cwd, session)
    except Exception:
        return 0
    if said:
        stream.write(said + "\n")
    return 0
