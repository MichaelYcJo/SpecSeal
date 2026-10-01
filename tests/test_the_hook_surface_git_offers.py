"""What git's own hooks can and cannot decide, measured against real git.

#692 proposes moving the commit gate, the worktree guard and the consent
record out of a reader of the command's text and into git's hooks. Whether
that works depends on facts the manual does not state, and phase 1 of the
work item measured them on git 2.34.1, 2.39.5, 2.43.0 and 2.50.1
(`seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/phases/phase-1.md`).
This file pins those facts against whatever git runs the suite, so a git
release that changes one of them turns a case red instead of silently
changing what the design rests on.

The one that decides the design is the first case. A switch rewrites the
working tree and the index BEFORE it updates `HEAD`, so `reference-transaction`
never sees a switch it can refuse cleanly: on 2.34-2.43 no `HEAD` line arrives
at all, and on 2.50.1 it arrives with the tree already moved. Refusing there
leaves `HEAD` on the old branch and the new branch's files checked out. If a
future git refuses a switch before the tree moves, that case goes red, and
that is the moment the design's switch arm becomes buildable as framed.

Every repository here sets `core.hooksPath` to its own absolute hooks
directory, so a person's global hooks never run in these cases.
"""

import os
import re
import stat
import subprocess
from pathlib import Path

import pytest

ZERO = "0" * 40


def _git_version():
    out = subprocess.run(
        ["git", "--version"], capture_output=True, text=True, check=True
    ).stdout
    m = re.search(r"(\d+)\.(\d+)", out)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


# reference-transaction exists from git 2.28. Below that every case here is
# about a hook that never runs, so the module says so rather than passing.
pytestmark = pytest.mark.skipif(
    _git_version() < (2, 28),
    reason="git below 2.28 has no reference-transaction hook; "
    "the surface this file pins does not exist there",
)


def g(d, *args, check=True, env=None):
    e = dict(os.environ)
    # The cases read what the hooks wrote, and nothing about the calling
    # session may reach them.
    for k in list(e):
        if k.startswith("GIT_") and k not in ("GIT_EXEC_PATH",):
            del e[k]
    if env:
        e.update(env)
    return subprocess.run(
        ["git", "-C", str(d), *args],
        capture_output=True,
        text=True,
        check=check,
        env=e,
    )


def hook(hooks, name, body):
    p = hooks / name
    p.write_text("#!/bin/sh\n" + body, encoding="utf-8")
    p.chmod(p.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def repo(tmp_path):
    """`main` with marker.txt saying `main`, and `other` saying `other`."""
    d = tmp_path / "r"
    d.mkdir()
    g(d, "init", "-q")
    g(d, "symbolic-ref", "HEAD", "refs/heads/main")
    for k, v in (
        ("user.email", "x@example.com"),
        ("user.name", "x"),
        ("commit.gpgsign", "false"),
        ("core.autocrlf", "false"),
    ):
        g(d, "config", k, v)
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    g(d, "config", "core.hooksPath", str(hooks))
    (d / "marker.txt").write_text("main\n", encoding="utf-8")
    (d / "f.py").write_text("a = 1\n", encoding="utf-8")
    g(d, "add", ".")
    g(d, "commit", "-q", "-m", "init")
    g(d, "branch", "other")
    g(d, "switch", "-q", "other")
    (d / "marker.txt").write_text("other\n", encoding="utf-8")
    g(d, "commit", "-q", "-am", "other")
    g(d, "switch", "-q", "main")
    return d, hooks


# Refuses at `prepared` when a line of stdin ends with $REFUSE_SUFFIX, and
# logs, for every state, the marker file as the hook's own directory sees it.
REFUSING_RT = r"""input=$(cat)
printf '%s %s\n' "$1" "$(cat marker.txt 2>/dev/null)" >>"$RT_LOG"
printf '%s\n' "$input" | sed 's/^/  /' >>"$RT_LOG"
if [ "$1" = prepared ] && [ -n "$REFUSE_SUFFIX" ]; then
  if printf '%s\n' "$input" | grep -q -- "$REFUSE_SUFFIX\$"; then
    exit 1
  fi
fi
exit 0
"""


def head(d):
    r = g(d, "symbolic-ref", "-q", "HEAD", check=False)
    return r.stdout.strip() or g(d, "rev-parse", "HEAD").stdout.strip()


@pytest.mark.parametrize("verb", ["switch", "checkout"])
def test_no_git_refuses_a_switch_before_the_tree_moves(tmp_path, verb):
    d, hooks = repo(tmp_path)
    log = tmp_path / "rt.log"
    hook(hooks, "reference-transaction", REFUSING_RT)
    r = g(
        d,
        verb,
        "other",
        check=False,
        env={"RT_LOG": str(log), "REFUSE_SUFFIX": " HEAD"},
    )
    text = log.read_text(encoding="utf-8") if log.exists() else ""
    head_lines = re.findall(r"^  \S+ \S+ HEAD$", text, re.M)

    # Whatever git did with the hook, the working tree is on `other`.
    assert (d / "marker.txt").read_text(encoding="utf-8") == "other\n", (
        f"git {verb} left the tree on `main` after reference-transaction "
        "refused it: this git refuses a switch before the tree moves, which "
        "phase 1 of #692 found no git doing. The design's switch arm may now "
        f"be buildable as framed.\nhook log:\n{text}"
    )
    if head_lines:
        # 2.50.1: the HEAD symref line arrives, after the tree moved.
        assert r.returncode != 0
        assert head(d) == "refs/heads/main"
        assert "prepared other" in text
        # The refusal left the index on `other` too: a broken state, not a
        # prevented switch.
        assert g(d, "status", "--porcelain").stdout.strip() != ""
    else:
        # 2.34-2.43: a switch reaches reference-transaction with no line at
        # all, so a hook cannot even see it.
        assert r.returncode == 0, r.stderr
        assert head(d) == "refs/heads/other"


def test_a_commit_past_no_verify_is_refused_at_the_ref_and_leaves_the_tree(tmp_path):
    d, hooks = repo(tmp_path)
    hook(hooks, "pre-commit", "exit 1\n")
    hook(hooks, "reference-transaction", REFUSING_RT)
    with open(d / "f.py", "a", encoding="utf-8") as f:
        f.write("b = 2\n")
    g(d, "add", "f.py")
    before = (
        g(d, "rev-parse", "HEAD").stdout,
        g(d, "status", "--porcelain").stdout,
        g(d, "write-tree").stdout,
    )
    r = g(
        d,
        "commit",
        "--no-verify",
        "-m",
        "x",
        check=False,
        env={"RT_LOG": str(tmp_path / "rt.log"), "REFUSE_SUFFIX": " refs/heads/main"},
    )
    assert r.returncode != 0
    after = (
        g(d, "rev-parse", "HEAD").stdout,
        g(d, "status", "--porcelain").stdout,
        g(d, "write-tree").stdout,
    )
    assert after == before


def test_a_refused_creation_leaves_no_worktree_and_keeps_its_branch(tmp_path):
    d, hooks = repo(tmp_path)
    hook(hooks, "reference-transaction", REFUSING_RT)
    wt = tmp_path / "wt"
    r = g(
        d,
        "worktree",
        "add",
        str(wt),
        "-b",
        "nb",
        check=False,
        env={"RT_LOG": str(tmp_path / "rt.log"), "REFUSE_SUFFIX": " HEAD"},
    )
    assert r.returncode != 0
    assert not wt.exists()
    listed = g(d, "worktree", "list", "--porcelain").stdout
    assert listed.count("worktree ") == 1, listed
    # The branch `-b` asked for is created in its own transaction first, and
    # the refusal does not take it back.
    assert (
        g(d, "rev-parse", "--verify", "-q", "refs/heads/nb", check=False).returncode
        == 0
    )


POST_CHECKOUT_LOG = r"""printf '%s %s %s\n' "$1" "$3" "$(pwd -P)" >>"$PC_LOG"
exit 0
"""


def test_post_checkout_tells_a_creation_from_a_switch_and_runs_in_the_tree(tmp_path):
    d, hooks = repo(tmp_path)
    hook(hooks, "post-checkout", POST_CHECKOUT_LOG)
    log = tmp_path / "pc.log"
    env = {"PC_LOG": str(log)}
    wt = tmp_path / "wt"
    g(d, "worktree", "add", str(wt), "-b", "nb", env=env)
    g(d, "switch", "-q", "other", env=env)
    lines = log.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2, lines
    created, switched = (line.split(" ", 2) for line in lines)
    assert created[0] == ZERO
    assert created[1] == "1"
    assert Path(created[2]) == wt.resolve()
    assert switched[0] != ZERO
    assert switched[1] == "1"
    assert Path(switched[2]) == d.resolve()


WAIVE_LOG = r"""if [ "$1" = "" ] || [ "$1" = prepared ]; then
  printf '%s=%s\n' "${1:-pre-commit}" "$(git config --get specseal.waive)" >>"$W_LOG"
fi
[ -n "$1" ] && cat >/dev/null
exit 0
"""


def test_a_dash_c_waiver_reaches_both_hooks_and_a_message_does_not(tmp_path):
    d, hooks = repo(tmp_path)
    hook(hooks, "pre-commit", WAIVE_LOG)
    hook(hooks, "reference-transaction", WAIVE_LOG)
    log = tmp_path / "w.log"
    env = {"W_LOG": str(log)}
    with open(d / "f.py", "a", encoding="utf-8") as f:
        f.write("b = 2\n")
    g(d, "-c", "specseal.waive=review", "commit", "-q", "-am", "x", env=env)
    first = log.read_text(encoding="utf-8").splitlines()
    assert "pre-commit=review" in first
    assert "prepared=review" in first
    log.unlink()
    with open(d / "f.py", "a", encoding="utf-8") as f:
        f.write("c = 3\n")
    g(d, "commit", "-q", "-am", "specseal.waive=review later", env=env)
    second = log.read_text(encoding="utf-8").splitlines()
    assert "pre-commit=" in second
    assert not any(line.endswith("=review") for line in second), second


CACHED_LOG = r"""git diff --cached --name-only | tr '\n' ' ' >>"$C_LOG"
echo >>"$C_LOG"
exit 0
"""


def test_pre_commit_sees_the_paths_a_dash_a_and_a_pathspec_commit_record(tmp_path):
    d, hooks = repo(tmp_path)
    hook(hooks, "pre-commit", CACHED_LOG)
    log = tmp_path / "c.log"
    env = {"C_LOG": str(log)}
    with open(d / "f.py", "a", encoding="utf-8") as f:
        f.write("b = 2\n")
    (d / "g.py").write_text("e = 5\n", encoding="utf-8")
    g(d, "add", "g.py")
    g(d, "commit", "-q", "-a", "-m", "dash-a", env=env)
    with open(d / "f.py", "a", encoding="utf-8") as f:
        f.write("c = 3\n")
    with open(d / "g.py", "a", encoding="utf-8") as f:
        f.write("i = 7\n")
    g(d, "add", "g.py")
    g(d, "commit", "-q", "-m", "pathspec", "f.py", env=env)
    lines = [line.split() for line in log.read_text(encoding="utf-8").splitlines()]
    assert lines == [["f.py", "g.py"], ["f.py"]]


# M12: which command hands reference-transaction GIT_AUTHOR_DATE. It is the
# criterion the `--no-verify` backstop keys on (owner's answer of 2026-10-01 in
# `questions.md` P4): a commit pre-commit did not judge is refused, and nothing
# else that moves a branch is.
AUTHOR_DATE_LOG = r"""if [ "$1" = prepared ]; then
  grep ' refs/heads/' >/dev/null && printf '%s %s\n' "$LABEL" "${GIT_AUTHOR_DATE:+dated}" >>"$A_LOG"
else
  cat >/dev/null
fi
exit 0
"""


def test_only_git_commit_hands_reference_transaction_an_author_date(tmp_path):
    d, hooks = repo(tmp_path)
    hook(hooks, "reference-transaction", AUTHOR_DATE_LOG)
    log = tmp_path / "a.log"

    def step(label, *args):
        g(d, *args, env={"A_LOG": str(log), "LABEL": label})

    with open(d / "f.py", "a", encoding="utf-8") as f:
        f.write("b = 2\n")
    step("commit", "commit", "-q", "-am", "b")
    with open(d / "f.py", "a", encoding="utf-8") as f:
        f.write("c = 3\n")
    step("no-verify", "commit", "-q", "--no-verify", "-am", "c")
    step("amend", "commit", "-q", "--amend", "-m", "c2")
    step("cherry-pick", "cherry-pick", "other")
    step("revert", "revert", "--no-edit", "HEAD")
    step("reset", "reset", "-q", "--hard", "HEAD~1")
    g(d, "branch", "ff", "main~1")
    g(d, "switch", "-q", "ff")
    step("merge-ff", "merge", "-q", "--ff-only", "main")
    step("merge-no-ff", "merge", "-q", "--no-ff", "--no-edit", "other")
    step("branch-f", "branch", "-f", "other", "main")
    step("update-ref", "update-ref", "refs/heads/other", "main~1")
    got = dict(line.split(" ", 1) for line in log.read_text().splitlines())
    dated = {label for label, value in got.items() if value.strip() == "dated"}
    assert dated == {"commit", "no-verify", "amend"}, got
    assert set(got) == {
        "commit",
        "no-verify",
        "amend",
        "cherry-pick",
        "revert",
        "reset",
        "merge-ff",
        "merge-no-ff",
        "branch-f",
        "update-ref",
    }


# M14: post-checkout runs after a creation, cannot stop it, and can take it
# back -- which is where the creation ladder decides (phase 4).
UNDO = r"""case "$1" in *[!0]*) exit 0 ;; esac
new=$(pwd -P)
common=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
cd "$common" || exit 1
git worktree remove --force "$new" >/dev/null 2>&1
exit 1
"""


def test_post_checkout_can_take_back_a_fresh_worktree(tmp_path):
    d, hooks = repo(tmp_path)
    hook(hooks, "post-checkout", UNDO)
    for name, args in (("wt1", ["-b", "nb"]), ("wt2", ["other"])):
        r = g(d, "worktree", "add", str(tmp_path / name), *args, check=False)
        assert r.returncode != 0
        assert not (tmp_path / name).exists()
    listed = g(d, "worktree", "list", "--porcelain").stdout
    assert listed.count("worktree ") == 1, listed
    # The branch `-b` made stays; the existing one is free to check out again.
    assert (
        g(d, "rev-parse", "--verify", "-q", "refs/heads/nb", check=False).returncode
        == 0
    )
    (hooks / "post-checkout").unlink()
    g(d, "worktree", "add", "-q", str(tmp_path / "again"), "other")
