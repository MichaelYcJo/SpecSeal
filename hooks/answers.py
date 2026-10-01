"""The old consent spellings, carried from a Bash command to the git hook that
judges it (#692, `questions.md` P3 answer (a), W6).

`[no-review]` and `[no-parity]` are bare words a shell drops before git runs,
so a git hook cannot see them. (`[worktree-ok]` is not carried: a creation is
judged before git runs, by the guard, which reads it from the command itself --
`questions.md` P6.) `hooks/answer-write.py` reads
them out of the command in `pre-bash` (`hooks/tokens.py`) and writes one empty
file per token here; the hook asks `given`; `hooks/answer-clear.py` removes the
session's files in `post-bash`. So an answer lives for one Bash call: the
command that carried the token, and every action in it (W6), which is what
`[no-review]` always meant by waiving "one command".

**Where.** `~/.claude/specseal/answers/<session>/`, beside the version-check
state this plugin already keeps in its own directory, and nowhere a person's
repository or git configuration holds (P1). Keyed by session and not by
clone, because a command can act on a clone its text does not name, and
working out which one is the reading this redesign removes.

**How long, when post-bash never runs.** A call another gate denies never
reaches PostToolUse, so the writer clears the session's files before it writes
the next call's, and `given` refuses a file older than `FRESH` seconds -- the
Bash tool's longest timeout, ten minutes, with room. A token is consent, so
the stale direction is the one to bound.
"""

import os
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

FRESH = 15 * 60


def _part(value):
    part = os.path.basename(str(value or "").strip())
    return "" if part in ("", ".", "..") else part


def directory(session, root=None):
    session = _part(session)
    return os.path.join(root or root_dir(), session) if session else ""


def clear(session, root=None):
    """Remove every answer this session holds. Silent on failure."""
    d = directory(session, root)
    if not d:
        return
    try:
        names = os.listdir(d)
    except OSError:
        return
    for name in names:
        try:
            os.remove(os.path.join(d, name))
        except OSError:
            pass


def write(session, tokens, root=None):
    """Replace this session's answers with `tokens`; the names written."""
    clear(session, root)
    d = directory(session, root)
    names = [NAMES[t] for t in tokens if t in NAMES]
    if not d or not names:
        return []
    written = []
    try:
        os.makedirs(d, mode=0o700, exist_ok=True)
    except OSError:
        return []
    for name in names:
        try:
            open(os.path.join(d, name), "w").close()
            written.append(name)
        except OSError:
            continue
    return written


def given(session, token, root=None, now=None):
    """True when this session's current Bash call carried `token`."""
    d = directory(session, root)
    name = NAMES.get(token)
    if not d or not name:
        return False
    try:
        age = (time.time() if now is None else now) - os.stat(
            os.path.join(d, name)
        ).st_mtime
    except OSError:
        return False
    return 0 <= age <= FRESH
