"""The commit gate as git runs it: `pre-commit`, its `reference-transaction`
backstop, and `post-commit`'s notice (#692).

`hooks/git/*.py` are thin entry points into this module, so that a case can
drive one hook in-process and the stubs run the same code from a shell. What
each hook reads, and why each reading is the right one, is in those files'
docstrings; what is judged is `hooks/gate.py`'s.

Nothing here reads `GIT_DIR`. git does not export it to `pre-commit`,
`post-commit` or `post-checkout` (phase 1's M4, on 2.50.1), so every reading
asks `git rev-parse` in the working directory git gave the hook.
"""

import hashlib
import importlib.util
import os
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
    bare word carried over from the Bash call (P3)."""
    out = set()
    for value in gate.git(["config", "--get-all", "specseal.waive"], cwd).splitlines():
        for word in value.replace(",", " ").split():
            if word in (gate.REVIEW, gate.PARITY):
                out.add(word)
    for arm, token in gate.TOKENS.items():
        if answers.given(session, token):
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


def _key(old, tree, date):
    old = "" if not old or set(old) <= ZERO else old
    return hashlib.sha1(f"{old}\n{tree}\n{date}".encode()).hexdigest()


def _judged_dir(cwd):
    git_dir = gate.git(["rev-parse", "--absolute-git-dir"], cwd)
    return os.path.join(git_dir, JUDGED) if git_dir else ""


def _leave_mark(cwd, head, date):
    d = _judged_dir(cwd)
    tree = gate.git(["write-tree"], cwd)
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
        open(os.path.join(d, _key(head, tree, date)), "w").close()
    except OSError:
        pass


def _take_mark(cwd, old, new, date):
    """True when `pre-commit` judged this update; the mark is used up."""
    d = _judged_dir(cwd)
    tree = gate.git(["rev-parse", "--verify", "--quiet", f"{new}^{{tree}}"], cwd)
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
    head = gate.git(["rev-parse", "--verify", "--quiet", "HEAD"], cwd)
    arms = gate.arms_missing(
        cwd,
        top,
        waived(cwd, session),
        lambda: gate.git(["diff", "--cached", "--name-only"], cwd).splitlines(),
        head=head,
    )
    if arms:
        return _refuse(stream, arms, top, cwd, session)
    _leave_mark(cwd, head, environ.get("GIT_AUTHOR_DATE", ""))
    return 0


def _commit_lines(lines, cwd):
    """The (old, new) pairs of this transaction that move a branch or a
    detached HEAD, once each."""
    detached = not gate.git(["symbolic-ref", "-q", "HEAD"], cwd)
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
    over nothing, for a root commit."""
    if base:
        args = ["diff", "--name-only", base, new]
    else:
        args = ["diff-tree", "--root", "-r", "--name-only", "--no-commit-id", new]
    return lambda: gate.git(args, cwd).splitlines()


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
        if arms:
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
