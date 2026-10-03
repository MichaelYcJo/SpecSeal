#!/usr/bin/env python3
"""One interpreter per hook event instead of one per gate.

Every gate here decides in well under a millisecond of its own work; the cost
is the Python that has to start before it can decide. Measured on the author's
machine, a bare interpreter is ~92ms and each gate ~110-180ms — so four gates
firing on one Bash call spent most of half a second starting up to conclude
that three of them had nothing to do.

This runs a group of gates in ONE process, feeding each the same payload and
merging what they print. The gate modules are imported and their `main()`
called, unchanged — they stay runnable on their own (that is how the tests
drive them, and how anyone debugging one reaches it).

Usage: dispatch.py <group>, payload on stdin.

Merging: a PreToolUse group can produce more than one decision, and the
strictest wins — deny over ask over silence — with every reason kept, because
a gate that was overruled still has something the user needs to read.

Failure is isolated and open: a gate that raises is skipped, and the others
still decide. A crashing gate must not block a tool call, and must not take
its neighbours down with it.

And it is said (#28). A skipped gate used to read exactly like an allow, with
nobody told. Now the skip writes a record under the git common dir, once per
gate per session, and the `stop` group says every pending record at the end
of the main session's turn as a `systemMessage`, placed before the sealer's
stamp. Nothing the report adds decides anything, and a group whose gates all
ran prints what it printed before.
"""

import importlib.util
import io
import json
import os
import subprocess
import sys
import time
from contextlib import redirect_stderr, redirect_stdout

HOOKS = os.path.dirname(os.path.abspath(__file__))

# Where a gate that failed is written down: one file per gate per session
# under `<git-common-dir>/<FAILURES_DIR>/<session>/`, named for the gate. It
# waits as `<gate>.pending` until the `stop` group says it, and then stays as
# `<gate>.reported`, which is what keeps it from being written or said again
# in that session.
FAILURES_DIR = "specseal-gate-failure"
PENDING = ".pending"
REPORTED = ".reported"
# The longest first line of an exception's message a record keeps, in UTF-16
# units: the report joins the `Stop` message `seal_stamp.MESSAGE_RESERVE` is
# held for, and the harness counts that message in them, so a character
# outside the BMP is two.
MESSAGE_CAP = 200
# The longest exception TYPE name a record keeps, in the same units and for
# the same message (#722). The plugin's own longest is `NoMutationDefined`,
# 17 characters, but a gate's import can raise a class from anywhere, and a
# class names itself whatever it likes; a name with no bound is a report no
# fixed reserve can hold. 40 keeps every built-in name whole -- the longest,
# `PendingDeprecationWarning`, is 25 -- and the cut name still says which
# class it was, the way the cut message still says what it said.
NAME_CAP = 40

# What `run_gate` saw fail during this invocation, in order, as
# `(gate, phase, exception)` where phase is "load" or "run". Kept beside the
# return value rather than inside it: `run_gate` returns a gate's stdout, and
# a case replaces it with a function returning one
# (`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py#test_the_stop_group_reports_the_stop_event`).
# One invocation is one process, so the list starts empty for each.
FAILED = []

LABEL = "SpecSeal: {count} failed and {verb} skipped"
CLOSING = (
    "Nothing was blocked, and each gate is said once per session. "
    "Updating or reinstalling the plugin usually repairs it."
)

GROUPS = {
    # The installer goes first: a stub that went missing or stale is back
    # before the command runs, and the gates after it ask whether git decides
    # in the clone they are about to judge (`hooks/githooks.py#decides`).
    #
    # `answer-write.py` hands the old consent tokens to those hooks (P3), and
    # `answer-clear.py` in `post-bash` takes them back when the call is over.
    "pre-bash": (
        "hook-install.py",
        "answer-write.py",
        "commit-review-gate.py",
        "worktree-guard.py",
        "mode-gate.py",
    ),
    "pre-agent": ("worktree-guard.py", "implementer-mark.py"),
    "pre-skill": ("review-skill-gate.py",),
    "post-bash": (
        "review-history-guard.py",
        "implementer-notice.py",
        "session-lease.py",
        "evidence-advisor.py",
        "worktree_consent.py",
        "answer-clear.py",
    ),
    # The AFTER half of the worktree guard, and the only group that exists for
    # one gate. It cannot join `pre-agent`: what it records is that the call
    # RAN, which is the whole of why the record is evidence a command text
    # cannot forge.
    "post-agent": ("worktree_consent.py",),
    "post-edit": ("lint-python.py", "session-lease.py"),
    # The root move precedes the ledger-format migration, because the second
    # reads the ledgers at the addresses the first creates.
    # The git hooks are installed last, into the root the two migrations above
    # may just have moved.
    "session-start": (
        "version-check.py",
        "root-migrate.py",
        "ledger-migrate.py",
        "hook-install.py",
    ),
    # The end of a main-session turn, where a sealed run's stamp is drawn
    # after the text it belongs under (#400). One gate, like `post-agent`,
    # because nothing else here has anything to say when a turn ends.
    "stop": ("sealer-stamp.py",),
}

# The event a group answers where its prefix does not say it. Read only on
# the decision path, which a `Stop` hook never takes, but the group added for
# one event must not report another.
EVENTS = {"stop": "Stop"}

RANK = {"deny": 3, "ask": 2, "allow": 1}


def run_gate(filename, payload):
    """A gate's stdout, or "" when it printed nothing or failed.

    stdin, stdout and argv are swapped for the call: the gates read the
    payload from stdin, and lint-python reads a path from argv[1] — left
    alone it would read the group name as a filename.
    """
    path = os.path.join(HOOKS, filename)
    out = io.StringIO()
    argv, stdin = sys.argv, sys.stdin
    phase = "load"
    try:
        spec = importlib.util.spec_from_file_location(
            f"specseal_gate_{filename.replace('-', '_')[:-3]}", path
        )
        module = importlib.util.module_from_spec(spec)
        sys.argv = [path]
        sys.stdin = io.StringIO(payload)
        with redirect_stdout(out), redirect_stderr(io.StringIO()):
            spec.loader.exec_module(module)
            phase = "run"
            # Import must not consume stdin; main() gets its own copy.
            sys.stdin = io.StringIO(payload)
            try:
                module.main()
            except SystemExit:
                pass
    except (Exception, SystemExit) as exc:
        # A `SystemExit` reaching here was raised at LOAD: `main()`'s own is
        # caught above, because `worktree-guard.py` ends with `sys.exit(0)`.
        # Left uncaught, one module body calling `sys.exit` ended the whole
        # group, and the gates after it never decided.
        FAILED.append((filename, phase, exc))
        # Deliberate, and still open: a crashing gate must not block a tool
        # call or take its neighbours down, so the call goes ahead exactly as
        # if the gate had printed nothing. What changed with #28 is that the
        # failure no longer reads like an allow to NOBODY: `main()` writes it
        # down and the `stop` group says it once per session. The isolation
        # property `tests/test_dispatch.py` and
        # `tests/test_the_implementer_is_recorded.py` assert is unchanged, and
        # both cases pass unedited.
        return ""
    finally:
        sys.argv, sys.stdin = argv, stdin
    return out.getvalue()


def readable(parsed):
    """Whether `merge` can read this JSON, asked of the fields the path it
    takes actually reads. Each other type raised there -- after every gate
    had run and outside `run_gate`'s isolation, so one gate's odd output
    ended the group and a neighbour's `deny` with it (#661).

    An object is required, and its `hookSpecificOutput` is an object where
    it is truthy; a falsy one (`null`, `false`, `0`, `""`, `[]`) was read as
    absent before #661 and still is. Where it holds a truthy decision, the
    decision path reads that decision and its reason, so those are text (the
    reason may be null) and the `systemMessage` is not asked: a `deny` beside
    a message that is not text is still a `deny` (round 2's 🟡 3). Otherwise
    the message path reads the `systemMessage`, which is text or null."""
    if not isinstance(parsed, dict):
        return False
    hook_out = parsed.get("hookSpecificOutput") or {}
    if not isinstance(hook_out, dict):
        return False
    decision = hook_out.get("permissionDecision")
    if decision:
        reason = hook_out.get("permissionDecisionReason")
        return isinstance(decision, str) and (reason is None or isinstance(reason, str))
    message = parsed.get("systemMessage")
    return message is None or isinstance(message, str)


def classify(text):
    """('decision'|'json'|'text'|'unreadable', value) for one gate's output.

    `unreadable` is JSON `merge` cannot read (`readable`), carried as the
    stripped text. `merge` drops it, and `main()` records the gate as one that
    failed while running, so it is said at the end of the turn rather than
    ending the group."""
    stripped = text.strip()
    if not stripped:
        return None, None
    try:
        parsed = json.loads(stripped)
    except ValueError:
        return "text", text.rstrip("\n")
    if not readable(parsed):
        return "unreadable", stripped
    if (parsed.get("hookSpecificOutput") or {}).get("permissionDecision"):
        return "decision", parsed
    return "json", parsed


def merge(outputs, event_name):
    """One stdout for the whole group."""
    decisions, jsons, texts = [], [], []
    for text in outputs:
        kind, value = classify(text)
        if kind == "decision":
            decisions.append(value)
        elif kind == "json":
            jsons.append(value)
        elif kind == "text":
            texts.append(value)

    if decisions:
        winner = max(
            decisions,
            key=lambda d: RANK.get(
                d["hookSpecificOutput"]["permissionDecision"].lower(), 0
            ),
        )
        reasons = [
            d["hookSpecificOutput"].get("permissionDecisionReason", "")
            for d in decisions
        ]
        out = {
            "hookSpecificOutput": {
                "hookEventName": event_name,
                "permissionDecision": winner["hookSpecificOutput"][
                    "permissionDecision"
                ],
                "permissionDecisionReason": "\n\n".join(
                    r for r in reasons + texts if r
                ),
            }
        }
        # A gate that only says something -- `hook-install.py`'s once-per-session
        # line -- is kept beside a neighbour's decision rather than dropped by
        # it: the line is said once, so dropping it once loses it.
        said = [
            j["systemMessage"]
            for j in jsons
            if isinstance(j.get("systemMessage"), str) and j["systemMessage"]
        ]
        if said:
            out["systemMessage"] = "\n\n".join(said)
        return json.dumps(out)
    if jsons:
        merged = dict(jsons[0])
        extra = [j.get("systemMessage") for j in jsons[1:] if j.get("systemMessage")]
        if extra and merged.get("systemMessage"):
            merged["systemMessage"] = "\n\n".join([merged["systemMessage"], *extra])
        return json.dumps(merged)
    return "\n".join(texts)


# --- a gate that failed is said (#28) ----------------------------------------
#
# Nothing below imports a module under `hooks/` except `optin.py`, and that
# one inside a guard: a report must not depend on the module whose failure it
# reports, and a broken `console.py` or `optin.py` is exactly the failure
# that silences the most gates at once.


def path_part(value):
    """`value` as one path component, or "" where it cannot be one. An id
    that names a directory must not escape it -- the measured `../../escaped`
    of `hooks/worktree-guard.py#already_asked`."""
    part = os.path.basename(str(value or ""))
    return "" if part in (".", "..") else part


def toplevel(cwd):
    """The nearest directory at or above `cwd` holding a `.git` entry, or "".

    The twin of `hooks/sealer-stamp.py#toplevel`, and duplicated rather than
    imported: that module imports `console` and `optin` at load, so reaching
    it would make the report depend on the modules whose failure it reports.
    `tests/test_a_gate_that_fails_says_so.py` holds the two to one answer."""
    if not cwd:
        return ""
    here = os.path.abspath(cwd)
    while True:
        if os.path.exists(os.path.join(here, ".git")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            return ""
        here = parent


def common_dir(top):
    """The git common dir of the repository at `top`, or "". A `.git`
    directory IS it, with no process started; a `.git` file (a linked
    worktree) is asked of git, the way `hooks/optin.py#git_common_dir` asks."""
    if not top:
        return ""
    dotgit = os.path.join(top, ".git")
    if os.path.isdir(dotgit):
        return dotgit
    try:
        out = subprocess.run(
            ["git", "-C", top, "rev-parse", "--git-common-dir"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return ""
    out = (out or "").strip()
    return os.path.normpath(os.path.join(top, out)) if out else ""


def opted_in(top, common):
    """Whether the repository at `top` runs the workflow, asked of
    `optin.py` -- and True where `optin.py` cannot answer. A broken
    `optin.py` silences thirteen of the fifteen gates, so "cannot tell" is
    the one state that must not also silence the report of it."""
    try:
        spec = importlib.util.spec_from_file_location(
            "specseal_optin_for_the_failure_report", os.path.join(HOOKS, "optin.py")
        )
        optin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(optin)
        return bool(optin.home_at(top, common))
    except (Exception, SystemExit):
        return True


def capped(text, cap):
    """`text` cut to at most `cap` UTF-16 units. A character outside the BMP
    is two, and one that would pass the cap is left out whole rather than
    split into half a pair. No marker is added: a cut is a shorter text, the
    way it always was for a message."""
    kept, units = [], 0
    for char in text:
        units += 2 if ord(char) > 0xFFFF else 1
        if units > cap:
            break
        kept.append(char)
    return "".join(kept)


def first_line(exc):
    """The first non-blank line of `exc`'s message, capped at `MESSAGE_CAP`
    UTF-16 units by `capped`."""
    lines = str(exc).strip().splitlines()
    return capped(lines[0].strip() if lines else "", MESSAGE_CAP)


def record(group, failures, body):
    """Write one pending record per gate in `failures` not yet recorded or
    said in this session. Writes nothing without a session id, a common dir,
    or an opted-in repository. Created exclusively, so two hook processes
    racing for one gate write it once."""
    session = path_part(body.get("session_id"))
    top = toplevel(body.get("cwd"))
    common = common_dir(top)
    if not session or not common:
        return
    directory = os.path.join(common, FAILURES_DIR, session)
    fresh = []
    for gate, phase, exc in failures:
        name = path_part(gate)
        seen = [os.path.join(directory, name + end) for end in (PENDING, REPORTED)]
        if name and not any(os.path.exists(p) for p in seen):
            fresh.append((name, phase, exc))
    # Asked only for a gate not yet written down. In an opted-in main
    # checkout a gate that stays broken then costs one `stat` pair per call
    # after its first. A linked worktree also pays `common_dir`'s `git
    # rev-parse` on every call where a gate fails, and a repository not opted
    # in, where nothing is ever written, loads `optin.py` once more on every
    # such call (measured in round 1: its probe P7).
    if not fresh or not opted_in(top, common):
        return
    # `at` is when and in what order this call's failures happened: the clock
    # once, and each gate's place among them. `draw` orders by it, because a
    # file's time can be equal for records written in one call (Windows CI
    # gave two records one time), which would say them in name order.
    now = time.time_ns()
    for place, (name, phase, exc) in enumerate(fresh):
        try:
            os.makedirs(directory, exist_ok=True)
            with open(
                os.path.join(directory, name + PENDING), "x", encoding="utf-8"
            ) as handle:
                json.dump(
                    {
                        "group": group,
                        "phase": phase,
                        "error": capped(type(exc).__name__, NAME_CAP),
                        "message": first_line(exc),
                        "at": [now, place],
                    },
                    handle,
                )
        except OSError:
            continue


def read_record(path):
    """A record's body, or {} where it cannot be read -- an older or newer
    plugin may have written it. The gate's name is in the file's name, so an
    unreadable body still yields a line."""
    try:
        with open(path, encoding="utf-8") as handle:
            body = json.load(handle)
    except (OSError, ValueError):
        return {}
    return body if isinstance(body, dict) else {}


def flat(value):
    """A record's field as one line of text, or "" where it is not a string."""
    return " ".join(value.split()) if isinstance(value, str) else ""


def describe(gate, body):
    """The line said for one gate.

    A gate that failed to LOAD fails in every group that loads its file, and
    its record is written once, by the first -- so each of those groups is
    named: a broken `worktree-guard.py` is an unguarded `pre-agent` too, not
    only an unguarded `pre-bash`. A failure while running depends on the
    payload, so it names the group it was seen in. The closing clause names
    only the groups where other gates were there to decide.

    Every field read from the record that has no fixed vocabulary is cut to
    its cap again here, because `read_record`'s writer may be an older or a
    newer plugin (#722): `error` at `NAME_CAP`, `message` at `MESSAGE_CAP`,
    and `group`, which this plugin writes from `GROUPS` but cannot trust a
    record to, at `NAME_CAP`. `phase` is read through a fixed table. The
    gate's name is the record's FILE name, which another plugin version's
    gates name, so it is cut at `NAME_CAP` too; and a load failure's group
    is expanded only where today's `GROUPS` puts the gate in the group the
    record names (round 1's 🟡 3)."""
    group = capped(flat(body.get("group")), NAME_CAP)
    gate = capped(gate, NAME_CAP)
    phase = body.get("phase")
    how = {"load": "failed to load", "run": "failed while running"}.get(phase, "failed")
    error = capped(flat(body.get("error")), NAME_CAP)
    message = capped(flat(body.get("message")), MESSAGE_CAP)
    cause = f"{error}: {message}" if error and message else error or message
    groups = [group] if group else []
    # Expanded only where this plugin's `GROUPS` puts the gate in the group
    # the record names: a record whose pair this version would never write
    # (a gate that moved groups between versions) names its own group alone.
    if phase == "load" and gate in GROUPS.get(group, ()):
        groups += [g for g, gates in GROUPS.items() if gate in gates and g != group]
    decided = [g for g in groups if any(o != gate for o in GROUPS.get(g, ()))]
    return "".join(
        [
            gate,
            f" {how}",
            f" in {' and '.join(groups)}" if groups else "",
            f" ({cause})" if cause else "",
            "; calls went ahead without it",
            f", and the other gates in {' and '.join(decided)} still decided"
            if decided
            else "",
            ".",
        ]
    )


def draw(body):
    """The report of every pending record of this session, oldest first, or
    "". Oldest by the `at` pair `record` writes -- the clock and the gate's
    place in its call -- because records one call writes can share a file
    time. Each record is renamed to `.reported` before its line is returned,
    the shape of `skills/verify/scripts/seal_stamp.py#claim` -- two drawers
    racing for one record say it once, and a crash between the rename and
    the print loses a line rather than repeating one.

    Only the main session's `Stop`: `SubagentStop` carries the same
    `session_id` and differs by `agent_id` alone, the reading
    `hooks/sealer-stamp.py` acts on."""
    if body.get("hook_event_name") != "Stop" or body.get("agent_id"):
        return ""
    session = path_part(body.get("session_id"))
    top = toplevel(body.get("cwd"))
    if not session or not top:
        return ""
    common = common_dir(top)
    directory = os.path.join(common, FAILURES_DIR, session) if common else ""
    try:
        names = [n for n in os.listdir(directory) if n.endswith(PENDING)]
    except OSError:
        return ""
    if not names or not opted_in(top, common):
        return ""
    # Oldest first by the `at` pair a record carries, and by the file's time,
    # at place 0, for a record from a plugin that wrote none. Name order
    # breaks what is still equal.
    waiting = []
    for name in names:
        path = os.path.join(directory, name)
        body = read_record(path)
        at = body.get("at")
        try:
            if not (
                isinstance(at, list)
                and len(at) == 2
                and all(type(v) is int for v in at)
            ):
                at = [os.stat(path).st_mtime_ns, 0]
        except OSError:
            continue
        waiting.append((at, name, path, body))
    lines = []
    for _, name, path, body in sorted(waiting):
        gate = name[: -len(PENDING)]
        line = describe(gate, body)
        try:
            os.replace(path, os.path.join(directory, gate + REPORTED))
        except OSError:
            continue
        lines.append(line)
    if not lines:
        return ""
    one = len(lines) == 1
    label = LABEL.format(
        count=f"{len(lines)} gate{'' if one else 's'}", verb="was" if one else "were"
    )
    return "\n".join([label, *lines, CLOSING])


def beside(merged):
    """The object a report is joined into: {} where the group printed
    nothing, the group's own JSON object where it printed one, and None
    where it printed anything else -- plain text at `Stop` reaches a
    different reader than a `systemMessage`, so it is not converted into
    one, and the records wait for a turn end that can carry them. No gate in
    `stop` prints plain text today."""
    if not merged.strip():
        return {}
    try:
        out = json.loads(merged)
    except ValueError:
        return None
    return out if isinstance(out, dict) else None


def report(group, payload, merged):
    """`merged`, after this call's failures are recorded -- and at `stop`,
    with every pending record of the session said. Never raises: what cannot
    be written or said is left as the silence it was before.

    At `stop` the report goes BEFORE whatever `systemMessage` the group
    already carries, in the same message: `sealer-stamp.py`'s drawing stays
    the last thing on the screen, which #400 decided."""
    try:
        # A payload that is not a JSON object raises below, and is caught.
        body = json.loads(payload)
        if FAILED:
            record(group, list(FAILED), body)
        if group == "stop":
            out = beside(merged)
            said = draw(body) if out is not None else ""
            if said:
                own = out.get("systemMessage")
                out["systemMessage"] = (
                    f"{said}\n\n{own}" if isinstance(own, str) and own else said
                )
                return json.dumps(out)
    except Exception:
        pass
    return merged


def main():
    group = sys.argv[1] if len(sys.argv) > 1 else ""
    gates = GROUPS.get(group)
    if not gates:
        return
    payload = sys.stdin.read()
    event_name = EVENTS.get(group) or (
        "PreToolUse" if group.startswith("pre-") else "PostToolUse"
    )
    # A plain loop rather than pairing the two lists with a strict zip, which
    # needs 3.10: a hook runs under whatever `python3` the harness finds, 3.9
    # on a stock macOS.
    outputs = []
    for gate in gates:
        text = run_gate(gate, payload)
        outputs.append(text)
        kind, value = classify(text)
        if kind == "unreadable":
            FAILED.append(
                (
                    gate,
                    "run",
                    ValueError(f"printed JSON the dispatcher cannot read: {value}"),
                )
            )
    merged = merge(outputs, event_name)
    # A group whose gates all loaded and ran reads nothing more than it did
    # before, except `stop`, which draws.
    if FAILED or group == "stop":
        merged = report(group, payload, merged)
    if merged.strip():
        print(merged)


if __name__ == "__main__":
    # THE entry point, and the only one that matters in production: `hooks.json`
    # spawns this file and nothing else, and it loads each gate with
    # `exec_module` and calls `main()` in-process. Seven of the eleven
    # `__main__` blocks in this tree are therefore unreachable when Claude Code
    # runs them -- so this block is where the streams get fixed, not each
    # gate's.
    #
    # A console whose encoding is not UTF-8 cannot encode the em dash, arrow
    # and middle dot these gates print, and the UnicodeEncodeError leaves
    # stdout EMPTY -- which is exactly how a hook says "nothing to see here".
    # The command the gate existed to stop goes through, and nothing reports
    # that a gate crashed. Korean, Japanese and Chinese Windows default to
    # cp949/cp932/cp936 and hit this.
    #
    # `stdin` is in the loop because the payload is where the non-ASCII
    # actually is: it carries the user's own command text, and one Korean path
    # or an em dash in a commit subject is enough. This file reads it, so a
    # raise there takes every gate in the group down at once -- and `hooks.json`
    # runs `python3 … || py -3 …`, so the retry meets an already-consumed stdin
    # and passes silently a second time.
    #
    # Unconditional, because branching on `os.name` would leave the Windows
    # path proven by nothing while Linux CI runs the other one; where a stream
    # is already UTF-8 this is a no-op. `errors` is named because `reconfigure`
    # resets it to `strict` whenever `encoding` is given without it, and stderr
    # ships as `backslashreplace` -- a path holding a lone surrogate must
    # degrade, not take the gate down on its way to reporting something. The
    # `hasattr` guard covers a stream that is None, which is what a hook
    # invoked with a closed stdin would hand us.
    #
    # The names are held rather than the streams, because `hooks/console.py`
    # -- the module this loop duplicates -- says a stream can be ABSENT and
    # reaches for it with `getattr(sys, name, None)`. Building the tuple from
    # `sys.stdin` directly raises `AttributeError` in that state, at module
    # level, before `main()`, with stdout empty. That is the silent allow this
    # block exists to close, arriving through the block itself.
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    main()
