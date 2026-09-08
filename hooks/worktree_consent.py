#!/usr/bin/env python3
"""PostToolUse: a worktree creation that actually RAN is consent for the rest
of the session.

`hooks/worktree-guard.py` answered worktree creation with `ask` at every site
that reached it, so no path through it cost zero prompts and the cost grew with
the number of worktrees. Measured on the 0.9.1 release run (#237): six work
items on six branches needed six `git worktree add` calls, and the guard held
the run at all six. An unattended run reaches the first and stops there.

`[worktree-ok]` could not fix that, and `has_token`'s docstring says why -- the
token is written into the command by whoever issues it, so the model can write
it on the first attempt, and reading it as consent turns the guard off with
nobody asked. This record is the evidence the token is not. A tool call reaches
PostToolUse only after it ran, and a `git worktree add` runs only if the
guard's `deny` did not fire and its `ask` was answered yes -- so the record is
written AFTER the answer rather than before the question, which is the one
thing a command text cannot forge.

The record is an empty file at
`<git-common-dir>/specseal-worktree-consent/<session-id>`. Its existence is the
whole fact, the way `specseal-worktree-choice/`'s markers and `optin.py`'s
`specseal-scratch` are. Three things about it were decisions rather than
defaults:

  A THIRD directory, not a value in `specseal-worktree-choice/create/`. That
  marker is written by PreToolUse BEFORE the answer and means "the question was
  put", so sharing one file would let the guard read its own question back as
  consent -- the `has_token` failure one directory over. The two also fail in
  opposite directions: an unwritable choice marker counts as ALREADY ASKED,
  because one missed question beats a deny nothing gets past, while an
  unwritable consent record must count as NO CONSENT, because the alternative
  is a guard that switches itself off when a disk is read-only. One file cannot
  fail two ways.

  The COMMON git directory, not `--absolute-git-dir`. The record stands for
  "this session may split this clone into worktrees", and a linked worktree is
  the same clone. Reading it through `optin.git_common_dir` keeps one answer to
  that question in this tree rather than two.

  NO expiry, and no pruning either. A session id is already scoped to a
  session, so a time bound on top of it can only produce one new outcome: a
  session that outlives the bound is asked a second time, which is the failure
  this removes. The choice markers beside it are not pruned either.

This is its own file rather than a branch inside the guard because
`hooks/dispatch.py` hands every gate the same payload with no event name. One
file wired to both events would have to tell them apart by sniffing
`hook_event_name`, and `skills/agent-contract/SKILL.md` §13 refuses a defence
that rests on a platform guarantee: where the field were absent the writer
would silently never record, which reads as "nobody ever consented" and costs
back every prompt this removes. A gate wired only to PostToolUse needs no
guarantee. The filename carries an underscore rather than the hyphen every
other gate here uses, because the guard imports it for the READ and a hyphen is
not importable -- the same reason `cmdline.py` and `optin.py` are spelled that
way.

The exit status of the creation is never read. What the record is about is the
approval, and the approval happened whether or not git then refused the path;
the retry after a failure is the worst moment to put the question again.

Failure is silent and one-directional. An unwritable `.git` leaves no record,
the next creation asks, and that is the direction a guard should fail in -- a
crash would be worse than the prompt it saves, because a hook that raises dies
with stdout empty, which is how a hook says "nothing to see here" (the guard's
own `_idle_min` says the same thing about a different crash).
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Reading a command line is no gate's property; `hooks/cmdline.py` owns it, and
# `hooks/optin.py` owns resolving a repository's git directories. Plain
# filenames mean `sys.modules` deduplicates both when `dispatch.py` runs
# several gates in one process.
import cmdline
import console
import optin

# One empty file per session per clone. Its existence is the fact.
CONSENT_DIR = "specseal-worktree-consent"


def consent_path(top: str, session: str) -> str:
    """Where this session's record lives in this clone, or "" if nowhere.

    The id names a file, so a separator in a malformed one must not become a
    path escape: `../../escaped` put an empty file at a repository root once
    already, through the guard's other marker. `hooks/session-lease.py` and
    `already_asked` both reduce it the same way.

    "" is returned rather than a guess for every way of not having an answer --
    no repository, no session id, an id that is only separators, or a common
    git directory that could not be resolved. The read then says "no consent"
    and the write does nothing, which is the same direction both should fail
    in.
    """
    session = os.path.basename(str(session or ""))
    if not session or session in (".", ".."):
        return ""
    common = optin.git_common_dir(top)
    if not common:
        return ""
    return os.path.join(common, CONSENT_DIR, session)


def granted(top: str, session: str) -> bool:
    """True when this session already created a worktree in this clone.

    `isfile`, not `exists`: the record is a file, and a path that is a
    directory is not one. An unreadable path answers False, which is the
    direction a guard reads as "ask".
    """
    path = consent_path(top, session)
    return bool(path) and os.path.isfile(path)


def record(top: str, session: str) -> bool:
    """Write the record. Silent on every failure; the caller ignores the answer.

    The return value exists for the tests, which need to tell "wrote it" from
    "could not" without inspecting a filesystem the failure case has made
    hostile on purpose.
    """
    path = consent_path(top, session)
    if not path:
        return False
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()
    except OSError:
        return False
    return True


def creation_directory(command: str, cwd: str) -> str:
    """The directory a `git worktree add` in `command` acted on, or "".

    EVERY segment is read, not just the first. The guard's own PreToolUse walk
    stops at the first verdict because that is the one it has to decide, while
    a creation anywhere in a command that ran is a creation that was approved.

    Comments and heredoc bodies come out first, the pair the guard's
    `_judgment_text` uses, and for the same reason: this is a judgment read of
    what the shell EXECUTED, and neither is executed. There is no consent read
    here at all -- no token is involved on this side.

    A segment the reader could not place falls back to the session's own
    directory, which is where the shell started. Getting that wrong lands the
    record in the wrong clone, so the next creation asks -- one prompt, on the
    side a guard should fail.
    """
    text = cmdline.drop_heredoc_bodies(cmdline.drop_comments(command))
    items, _clean = cmdline.split_segments_with_separators(text)
    for tokens, wheres in cmdline.walk_directories(items, cwd):
        if not cmdline.adds_a_worktree(tokens):
            continue
        here = cwd
        for where in wheres:
            if not isinstance(where, cmdline.Unresolved):
                here = where
                break
        return cmdline.apply_chdir(here, cmdline.parse_git(tokens)[2])
    return ""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    # Wired to PostToolUse and nothing else, so the event is not inferred --
    # but a payload that NAMES the other event is refused rather than trusted.
    # Nothing sends one; a group edited by hand would.
    if data.get("hook_event_name", "PostToolUse") != "PostToolUse":
        return

    session = data.get("session_id", "")
    if not session:
        return
    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}
    cwd = data.get("cwd") or ""

    if tool in ("Agent", "Task"):
        # The same decision arriving through a different tool: the harness
        # creates the worktree at <repo>/.claude/worktrees/<name>, and this
        # call reaching PostToolUse means it was permitted.
        if str(tool_input.get("isolation", "")).lower() != "worktree":
            return
        where = cwd
    elif tool == "Bash":
        where = creation_directory(tool_input.get("command", "") or "", cwd)
    else:
        return

    top = optin.repo_root(where)
    if not top:
        return
    record(top, session)


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    console.to_utf8()
    main()
