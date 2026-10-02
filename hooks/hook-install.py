#!/usr/bin/env python3
"""SessionStart and PreToolUse(Bash): put this plugin's git hooks where git runs
them, in every opted-in clone a session reaches (#692).

`hooks/githooks.py` holds why the judgment moved into git's own hooks and
what a stub is. This file is the one writer of the stubs, and it runs in two
groups for two reasons:

  * `session-start`, for the clone the session opens in;
  * `pre-bash`, for the clone the Bash call's `cwd` is in -- first in that
    group, so a stub that went missing or stale is back before the command
    runs. A session that walks into a second clone meets the stubs there at
    its first Bash call in it.

What it writes, and where, is one rule each:

  * **Only into an opted-in clone** (`hooks/optin.py`), and only into the
    common git directory's `hooks/`, which every worktree of the clone shares.
    A clone that is not opted in gets nothing, and stubs this plugin wrote
    there before -- a clone that opted out later -- are removed: a stub reads
    the opt-in at run time as well, so the removal is tidiness, not safety.
  * **Never over a slot somebody else holds** (`questions.md` P1, answer (a)).
    `core.hooksPath` set at any level, or a hook file without the stub's
    marker line, makes the whole clone foreign: nothing is written, any stub of
    this plugin's that is already there is taken out so git and the fallback
    never both judge, and the session is told once. The PreToolUse text paths
    then judge that clone as 0.16.0 did (`githooks.decides` is what they ask).
  * **Rewritten when the installed plugin moved.** A stub carries the version
    and the absolute path of the plugin that wrote it; either differing from
    the running plugin's, or the path being gone, is a stub to rewrite.

What it says is two messages, each once per session per clone, and both
pinned by `tests/test_the_hooks_are_installed_where_git_runs_them.py`: the
files it wrote, and the slot it would not write. A call that changes nothing
says nothing.

Failure is silent and open, the dispatcher's rule for every gate: a stub that
cannot be written leaves the clone without it, and the text paths then judge
it, which is 0.16.0's behaviour rather than none.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console
import githooks
import optin

# One empty file per session per clone per message, under the common git
# directory. Its existence is the fact, as for every once-per-session record
# beside it.
SAID_DIR = "specseal-git-hooks"

INSTALLED = (
    "SpecSeal {verb} its git hooks in {directory}: pre-commit, "
    "reference-transaction and post-commit. From here on git itself judges a "
    "commit in this clone, inside the commit, instead of a reading of the "
    "command before it runs. Each file carries the line `{marker}`, and a hook "
    "file without it is never touched."
)

FOREIGN = (
    "SpecSeal installed no git hooks in {top}: {detail}, and a hooks slot "
    "somebody else holds is never written over. Commits in this clone are "
    "judged as SpecSeal 0.16.0 judged them, by reading each command before it "
    "runs. This is said once per session."
)


def say_once(common, session, kind):
    """True the first time this session reaches `kind` in this clone.

    No session id, or a record that cannot be written, says nothing: a message
    repeated on every Bash call is worse than one missed.
    """
    session = os.path.basename(str(session or ""))
    if not common or not session or session in (".", ".."):
        return False
    path = os.path.join(common, SAID_DIR, f"{session}.{kind}")
    if os.path.exists(path):
        return False
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()
    except OSError:
        return False
    return True


def remove_ours(directory):
    """Take out every stub this plugin wrote under `directory`; the names."""
    removed = []
    for hook in githooks.HOOKS:
        path = os.path.join(directory, hook)
        found = githooks.read_stub(path)
        if found and found[0]:
            try:
                os.remove(path)
                removed.append(hook)
            except OSError:
                pass
    return removed


def write_stubs(directory):
    """Write every missing or stale stub under `directory`; True if any was."""
    version = githooks.plugin_version()
    wrote = False
    for hook in githooks.HOOKS:
        path = os.path.join(directory, hook)
        text = githooks.stub_text(hook, version=version)
        found = githooks.read_stub(path)
        # The right bytes are not enough: git skips a hook it cannot execute,
        # so a stub that lost its execute bit is written again (round 1 of
        # #692, 🟡 3).
        if found and found[0] and os.access(path, os.X_OK):
            try:
                with open(path, encoding="utf-8") as f:
                    if f.read() == text:
                        continue
            except OSError:
                pass
        try:
            os.makedirs(directory, exist_ok=True)
            tmp = path + ".specseal-tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            os.chmod(tmp, 0o755)
            os.replace(tmp, path)
            wrote = True
        except OSError:
            continue
    return wrote


# Set to `off`, the installer writes nothing anywhere. It is the suite's seam:
# `tests/conftest.py` sets it for every case, so no fixture repository a case
# builds for another gate grows stubs it did not ask for -- and a case that
# names a real clone by mistake cannot write into one. A clone with no stubs is
# judged by the text paths, 0.16.0's behaviour, so the seam fails toward the
# judgment that was there before.
SWITCH = "SPECSEAL_HOOK_INSTALL"


def install(cwd, session=""):
    """Bring the clone at `cwd` to the state the rules above name; the message
    to say, or ""."""
    if os.environ.get(SWITCH) == "off":
        return ""
    # An empty `cwd` is no repository (`optin.repo_root`), never the process's
    # own directory: a payload that names nowhere writes nowhere.
    top = optin.repo_root(cwd)
    if not top:
        return ""
    common = optin.git_common_dir(top)
    if not common:
        return ""
    directory = githooks.hooks_dir(common)
    if not optin.home_at(top, common):
        remove_ours(directory)
        return ""
    detail = githooks.foreign(top, common)
    if detail:
        if not detail.startswith("core.hooksPath"):
            remove_ours(directory)
        if say_once(common, session, "foreign"):
            return FOREIGN.format(top=top, detail=detail)
        return ""
    had = any(
        (found := githooks.read_stub(os.path.join(directory, hook))) and found[0]
        for hook in githooks.HOOKS
    )
    if not write_stubs(directory):
        return ""
    if say_once(common, session, "installed"):
        return INSTALLED.format(
            verb="updated" if had else "installed",
            directory=directory,
            marker=githooks.MARKER,
        )
    return ""


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(payload, dict):
        return
    if payload.get("tool_name") not in (None, "Bash"):
        return
    message = install(payload.get("cwd") or "", payload.get("session_id") or "")
    if message:
        print(json.dumps({"systemMessage": message}))


if __name__ == "__main__":
    console.to_utf8()
    main()
