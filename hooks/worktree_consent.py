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

This module is also where the guard asks *what is consent*, and the record is
one of two answers. The other is the person's `automation` answer to the
routing question, read out of this session's own transcript
(`automation_answered`). An automation run creates its worktrees before any of
them has run, so the record cannot exist yet at the first one, and the answer
the person gave a minute earlier is the one fact on disk that the model did
not write: the harness wrote it from the click. `consent` reads both, record
first.

Failure is silent and one-directional. An unwritable `.git` leaves no record,
the next creation asks, and that is the direction a guard should fail in -- a
crash would be worse than the prompt it saves, because a hook that raises dies
with stdout empty, which is how a hook says "nothing to see here" (the guard's
own `_idle_min` says the same thing about a different crash).
"""

import glob
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

# Where the harness writes session transcripts. One constant, so a test points
# it at a temporary directory and no case can read a real transcript on the
# machine running it.
PROJECTS_ROOT = os.path.join(os.path.expanduser("~"), ".claude", "projects")

# Question 1 of the routing batch, `skills/implement/orchestration.md`
# §*Question 1 — single-select*, as leading phrases. A test pins these against
# that table, so relabelling the question turns a case red instead of quietly
# bringing the prompt back.
ROUTING_LABELS = ("automation", "per axis", "no work item")
PRESET = "automation"

# Where a label's decoration starts: `automation (Recommended)`,
# `automation — 안 멈추고 끝까지`, `automation - nothing stops`.
_DECORATION = (" (", " —", " -")


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


def leading_phrase(label) -> str:
    """A label casefolded and cut where its decoration starts, then stripped.

    The orchestrator may decorate a label it was told to use verbatim, and the
    ten routing answers on disk when this was written carried three
    decorations: `automation (권장)`, `automation (Recommended)` and
    `automation — 안 멈추고 끝까지`. What they share is the phrase before the
    first ` (`, ` —` or ` -`. A label that is not a string has no phrase.
    """
    if not isinstance(label, str):
        return ""
    text = label.casefold()
    cut = min((i for i in (text.find(d) for d in _DECORATION) if i >= 0), default=-1)
    return (text[:cut] if cut >= 0 else text).strip()


def transcript_for(session, transcript_path="") -> str:
    """This session's own MAIN transcript, or "" for every way of not having one.

    The payload's `transcript_path` when its basename is `<session>.jsonl`;
    otherwise the one file matching `<PROJECTS_ROOT>/*/<session>.jsonl`. A
    subagent's tool call carries its parent's `session_id`, so a subagent
    reaches its parent's answer through the second form, whatever path its own
    payload names. Nothing else is scanned: no other session's file, and no
    `subagents/` file, because a subagent has no `AskUserQuestion` to be
    answered in.

    More than one match is no match. Two files cannot both be this session's
    transcript, and choosing one is a guess about which of them the harness
    meant.
    """
    session = os.path.basename(str(session or ""))
    if not session or session in (".", ".."):
        return ""
    name = session + ".jsonl"
    if transcript_path and os.path.basename(str(transcript_path)) == name:
        return str(transcript_path)
    try:
        found = glob.glob(
            os.path.join(glob.escape(PROJECTS_ROOT), "*", glob.escape(name))
        )
    except (OSError, ValueError):
        return ""
    found = [p for p in found if os.path.isfile(p)]
    return found[0] if len(found) == 1 else ""


def _routing_preset(result) -> bool:
    """True when a structured `AskUserQuestion` result pressed the preset.

    One single-select question whose options' leading phrases are exactly the
    three of `ROUTING_LABELS`, answered with a label whose leading phrase is
    `PRESET`. `answers` maps a question's text to the chosen label. A
    multi-select answer is the chosen labels joined by `, `, and the routing
    question is not one, so `multiSelect` must be `False` rather than merely
    absent: an absent field is a shape nobody measured.
    """
    if not isinstance(result, dict):
        return False
    questions, answers = result.get("questions"), result.get("answers")
    if not isinstance(questions, list) or not isinstance(answers, dict):
        return False
    for q in questions:
        if not isinstance(q, dict) or q.get("multiSelect") is not False:
            continue
        options = q.get("options")
        if not isinstance(options, list):
            continue
        phrases = sorted(
            leading_phrase(o.get("label")) if isinstance(o, dict) else ""
            for o in options
        )
        if phrases != sorted(ROUTING_LABELS):
            continue
        text = q.get("question")
        if isinstance(text, str) and leading_phrase(answers.get(text)) == PRESET:
            return True
    return False


def _content(entry):
    message = entry.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    return content if isinstance(content, list) else []


def _clone_of(cwd) -> str:
    """The common git directory of the clone `cwd` sits in, real-pathed, or ""."""
    common = optin.git_common_dir(optin.repo_root(cwd)) if isinstance(cwd, str) else ""
    return os.path.realpath(common) if common else ""


def automation_answered(top: str, session: str, transcript_path: str = "") -> bool:
    """True when the person pressed `automation` on the routing question, in
    this session's own transcript, from this clone.

    The harness writes this answer from the person's click; the model writes
    the question and its options and never which one was pressed. That is the
    whole difference from `[worktree-ok]` and from a `routing.md` the model
    wrote itself, and it is why the answer stands beside the record as
    consent. `docs/worktree-guard-spec.md` §*Creation consent* holds the table.

    Four conditions, and every way of failing one is False, which is the
    guard's behaviour before this reader existed:

      1. the transcript is this session's own main one (`transcript_for`);
      2. the answer is a harness-written `AskUserQuestion` result: a `user`
         entry whose `tool_result` names, by `tool_use_id`, an EARLIER
         assistant `tool_use` called `AskUserQuestion`, read from the entry's
         structured `toolUseResult`. A Bash result echoing *The user answered:
         "automation"* has no such link and no `answers` object;
      3. the question is the routing question and the preset was pressed
         (`_routing_preset`);
      4. the result entry's own `cwd` is in the same clone as `top`.

    A line is parsed only when it could matter to one of the two roles, so a
    long transcript costs a substring test per line. Every read error, every
    malformed line and every missing field is skipped or answered False;
    nothing here raises, because a hook that raises dies with stdout empty,
    which reads as "nothing to see here".
    """
    path = transcript_for(session, transcript_path)
    if not path:
        return False
    want = _clone_of(top)
    if not want:
        return False
    asked = set()
    clones = {}
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if "AskUserQuestion" not in line and "toolUseResult" not in line:
                    continue
                try:
                    entry = json.loads(line)
                except (ValueError, RecursionError):
                    continue
                if not isinstance(entry, dict):
                    continue
                kind = entry.get("type")
                if kind == "assistant":
                    for item in _content(entry):
                        if (
                            isinstance(item, dict)
                            and item.get("type") == "tool_use"
                            and item.get("name") == "AskUserQuestion"
                            and isinstance(item.get("id"), str)
                        ):
                            asked.add(item["id"])
                    continue
                if kind != "user" or not asked:
                    continue
                linked = any(
                    isinstance(item, dict)
                    and item.get("type") == "tool_result"
                    and item.get("tool_use_id") in asked
                    for item in _content(entry)
                )
                if not linked or not _routing_preset(entry.get("toolUseResult")):
                    continue
                cwd = entry.get("cwd")
                key = cwd if isinstance(cwd, str) else ""
                if key not in clones:
                    clones[key] = _clone_of(key) if key else ""
                if clones[key] == want:
                    return True
    except OSError:
        return False
    return False


def consent(top: str, session: str, transcript_path: str = "") -> str:
    """Which consent this session holds for splitting this clone, or "".

    `"record"` when a creation already ran (`granted`), `"answer"` when the
    person pressed `automation` (`automation_answered`), and "" for neither.
    The record is read first because it is one `stat`; the transcript is
    scanned only when there is no record, and once the first creation runs the
    writer below records it, so the scan is paid at most until then.
    """
    if granted(top, session):
        return "record"
    if automation_answered(top, session, transcript_path):
        return "answer"
    return ""


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
