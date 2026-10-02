"""The old consent spellings, carried from a Bash command to the git hook that
judges it (#692, `questions.md` P3 answer (a), W6).

`[no-review]` and `[no-parity]` are bare words a shell drops before git runs,
so a git hook cannot see them. (`[worktree-ok]` is not carried: a creation is
judged before git runs, by the guard, which reads it from the command itself --
`questions.md` P6.) `hooks/answer-write.py` reads them out of the command in
`pre-bash` (`hooks/tokens.py`) and writes them here with the command that
carried them; the hook asks `given`; `hooks/answer-clear.py` removes that
call's answers in `post-bash`. So an answer lives for one Bash call: the
command that carried the token, and every action in it (W6), which is what
`[no-review]` always meant by waiving "one command".

**Whose call.** The parent and every subagent share one session id, so an
answer keyed by the session alone waived any agent's commit while the call
that carried it ran, and the next agent's call cleared it (round 1 of #692,
🟡 9). Each call's answers sit in a directory of their own, named by the
payload's `tool_use_id`, beside the command they came with. The hook reads
the argv of its own ancestors up to the `claude` process
(`hooks/hooksession.py#call_args`) -- the Bash tool's shell carries the
command it runs there -- and an answer is given only when its command is in
that argv. The shell spells the command its own way (`'` as `'"'"'`, a
newline as `\\012` in `ps`), so both sides are compared as their ASCII
letters and digits alone, octal escapes dropped first. Where no ancestor
carries it -- no `claude` above the hook, or no `ps` -- the answer is not
given, and the refusal names `git -c specseal.waive=…`, which belongs to its
own command and has neither problem.

**Where.** `~/.claude/specseal/answers/<session>/<call>/`, beside the
version-check state this plugin already keeps in its own directory, and
nowhere a person's repository or git configuration holds (P1). Keyed by
session and call and not by clone, because a command can act on a clone its
text does not name, and working out which one is the reading this redesign
removes.

**How long, when post-bash never runs.** A call another gate denies never
reaches PostToolUse, so the writer prunes the session's calls older than
`FRESH` seconds -- the Bash tool's longest timeout, ten minutes, with room --
and `given` refuses an answer that old. A token is consent, so the stale
direction is the one to bound.
"""

import hashlib
import os
import re
import shutil
import time

# `SPECSEAL_ANSWERS` moves it, and only the suite sets it (`tests/conftest.py`),
# so that no case writes into the home of whoever runs it. Read at each call,
# because a module is imported before a case's environment is set.
OVERRIDE = "SPECSEAL_ANSWERS"


def root_dir():
    return os.environ.get(OVERRIDE) or os.path.join(
        os.path.expanduser("~"), ".claude", "specseal", "answers"
    )


# The tokens a hook asks about, each as the file name it is kept under.
NAMES = {
    "[no-review]": "no-review",
    "[no-parity]": "no-parity",
}

# The file beside them holding the command that carried them.
COMMAND = "command"

FRESH = 15 * 60

# How far ahead of `time.time()` an answer's own file may be stamped and still
# be read as written now. On `windows-latest` under Python 3.12, 401 of 3,000
# files read their stamp ahead of a `time.time()` taken right after the write,
# each by under a microsecond (#692's Windows pass, CI run 37013783175): the
# write and the read fall in one tick of a coarse clock, and the two floats
# round apart. An exact lower bound of 0 refused those answers, a different
# one in each run. A file stamped further ahead than this is still refused: a
# token is consent, and a stamp set into the future would keep one alive.
SKEW = 2


def _part(value):
    part = os.path.basename(str(value or "").strip())
    return "" if part in ("", ".", "..") else part


def call_id(tool_use_id, command):
    """The name one Bash call's answers are kept under: the payload's
    `tool_use_id`, or the command's own hash where a harness sends none, which
    `pre-bash` and `post-bash` derive alike."""
    return _part(tool_use_id) or (
        "cmd-" + hashlib.sha1(str(command or "").encode("utf-8")).hexdigest()[:16]
    )


def directory(session, root=None):
    session = _part(session)
    return os.path.join(root or root_dir(), session) if session else ""


def _call_dir(session, call, root):
    d, call = directory(session, root), _part(call)
    return os.path.join(d, call) if d and call else ""


def clear(session, call, root=None):
    """Remove the answers one call holds. Silent on failure."""
    d = _call_dir(session, call, root)
    if d:
        shutil.rmtree(d, ignore_errors=True)


def _prune(session, root, now):
    d = directory(session, root)
    try:
        names = os.listdir(d) if d else []
    except OSError:
        return
    for name in names:
        path = os.path.join(d, name)
        try:
            if now - os.stat(path).st_mtime > FRESH:
                shutil.rmtree(path, ignore_errors=True)
        except OSError:
            continue


def write(session, call, command, tokens, root=None, now=None):
    """Keep `tokens` for this one call, beside `command`; the names written.
    Calls left behind by a denied command are pruned first."""
    _prune(session, root, time.time() if now is None else now)
    d = _call_dir(session, call, root)
    names = [NAMES[t] for t in tokens if t in NAMES]
    if not d or not names:
        return []
    try:
        os.makedirs(d, mode=0o700, exist_ok=True)
        with open(os.path.join(d, COMMAND), "w", encoding="utf-8") as f:
            f.write(command or "")
    except OSError:
        return []
    written = []
    for name in names:
        try:
            open(os.path.join(d, name), "w").close()
            written.append(name)
        except OSError:
            continue
    return written


_ESCAPE = re.compile(r"\\[0-7]{3}")
_OTHER = re.compile(r"[^A-Za-z0-9]")


def _squash(text):
    return _OTHER.sub("", _ESCAPE.sub("", text or ""))


def given(session, token, args, root=None, now=None):
    """True when a Bash call that carried `token` is the one this hook runs
    under: a fresh answer whose command is in one of `args`, the argv strings
    of the hook's ancestors. `args` may be a callable, asked only when an
    answer is there to match."""
    d = directory(session, root)
    name = NAMES.get(token)
    if not d or not name:
        return False
    now = time.time() if now is None else now
    try:
        calls = sorted(os.listdir(d))
    except OSError:
        return False
    for call in calls:
        try:
            age = now - os.stat(os.path.join(d, call, name)).st_mtime
            if not -SKEW <= age <= FRESH:
                continue
            with open(os.path.join(d, call, COMMAND), encoding="utf-8") as f:
                carried = _squash(f.read())
        except OSError:
            continue
        if callable(args):
            args = args()
        if any(carried in _squash(a) for a in args):
            return True
    return False
