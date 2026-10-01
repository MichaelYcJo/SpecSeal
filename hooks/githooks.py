"""The git hooks this plugin installs: their stub, where git runs them, and
whether git decides in a clone (#692).

The commit gate, the worktree guard's creation arm and the consent record used
to learn where an action happens by reading the Bash command's text before the
shell ran it. Milestone 49 showed that prediction never converges: every
reading found one more shell shape that moved a commit somewhere the reader did
not follow. Git's own hooks run inside the action instead -- `pre-commit` in
the process making the commit, in the worktree whose index becomes it;
`post-checkout` in the worktree a creation just made -- so no command text is
an input to them, and no shell construct can route an action around them.

This module is what every party that needs that fact shares:

  * `hooks/hook-install.py` writes the stubs and rewrites them when the
    installed plugin moves;
  * the stubs themselves `exec` the installed plugin's `hooks/git/<hook>.py`;
  * the PreToolUse text paths that stay -- 0.16.0's reading, kept for a clone
    whose hooks slot is foreign (`questions.md` P1, answer (a)) -- ask
    `decides()` before they judge, and stand aside where git decides.

**A stub is a file this plugin wrote, and only that.** Its second line is the
marker below; the installer reads it to tell its own stub from a hook a person
or a hook manager put there, and never writes over a file without it (P1).

**The stub embeds the installed plugin's absolute path.** A git hook runs from
git, not from the harness, so `CLAUDE_PLUGIN_ROOT` is not in its environment
(measured, spec §*What the tree answered* 9). The path goes stale when the
plugin moves to a new version directory, so the stub tests it and exits 0 when
it is gone -- an uninstalled plugin leaves a stub that does nothing -- and the
installer rewrites it at the next session start or Bash call in the clone.

**What the stub decides before Python starts** (phase 1's M10: a Python start
per hook per commit cost 209-921 ms on this machine, against the plan's ~200 ms
row). A commit by a person at their own terminal is not judged (P2, answer
(a)), and that is known without Python when neither a session variable nor a
lease directory exists. `reference-transaction` judges only `prepared` with
`GIT_AUTHOR_DATE` exported, which phase 1's M12 measured as the one thing every
`git commit` hands the hook and no merge, reset, cherry-pick, rebase or pull
does, on git 2.34.1, 2.39.5, 2.43.0 and 2.50.1. `post-checkout` acts only on a
creation, whose previous HEAD git passes as the null object id (M3).
"""

import json
import os
import subprocess

# The hooks this plugin installs, in the order the installer names them.
HOOKS = ("pre-commit", "reference-transaction", "post-checkout", "post-commit")

# The stub's second line, followed by the plugin version that wrote it. A hook
# file without it is not this plugin's, whatever else it says.
MARKER = "# specseal-git-hook"

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.dirname(HERE)


def plugin_version(root=PLUGIN_ROOT):
    """The version in `<root>/.claude-plugin/plugin.json`, or "" unreadable."""
    try:
        with open(
            os.path.join(root, ".claude-plugin", "plugin.json"), encoding="utf-8"
        ) as f:
            value = json.load(f).get("version", "")
    except (OSError, ValueError, AttributeError):
        return ""
    return value if isinstance(value, str) else ""


def entry_point(hook, root=PLUGIN_ROOT):
    """The Python file a stub for `hook` runs."""
    return os.path.join(root, "hooks", "git", hook + ".py")


def _sh_quote(text):
    """`text` as one single-quoted sh word."""
    return "'" + text.replace("'", "'\\''") + "'"


# What each stub decides in sh, before an interpreter starts. Every line exits
# 0, so a stub's own refusal is always Python's and always has its text.
_NARROW = {
    "pre-commit": "",
    "reference-transaction": (
        # Only `prepared` can refuse, and only a commit hands the hook
        # GIT_AUTHOR_DATE (M12). stdin is drained so git never writes into a
        # closed pipe.
        '[ "$1" = prepared ] || { cat >/dev/null; exit 0; }\n'
        '[ -n "$GIT_AUTHOR_DATE" ] || { cat >/dev/null; exit 0; }\n'
    ),
    "post-checkout": (
        # A creation passes the null object id as the previous HEAD, in SHA-1
        # and SHA-256 repositories alike: a digit other than 0 is a switch.
        'case "$1" in *[!0]*) exit 0 ;; esac\n'
    ),
    "post-commit": "",
}

# P2: a commit with no Claude session behind it is a person's own, and stays
# theirs. No session variable and no lease anywhere in the clone means there is
# nobody to look for, so Python is not started. A lease alone does start it,
# because S9's second route -- the `claude` ancestor matched against a lease --
# is the one that survives a harness that exports no variable. Leases sit under
# each worktree's own git directory (`hooks/session-lease.py`), so the whole
# clone is looked at.
_P2 = (
    'if [ -z "$CLAUDE_CODE_SESSION_ID$CLAUDECODE" ]; then\n'
    "  c=$(git rev-parse --git-common-dir 2>/dev/null)\n"
    "  l=\n"
    '  for d in "$c/specseal-leases" "$c"/worktrees/*/specseal-leases; do\n'
    '    [ -d "$d" ] && l=1\n'
    "  done\n"
    '  [ -n "$l" ] || {{ {drain}exit 0; }}\n'
    "fi\n"
)


def stub_text(hook, root=PLUGIN_ROOT, version=None):
    """The whole stub file for `hook`, pointing at `root`'s entry point."""
    if version is None:
        version = plugin_version(root)
    target = _sh_quote(entry_point(hook, root))
    # Only reference-transaction is handed anything on stdin.
    p2 = _P2.format(drain="cat >/dev/null; " if hook == "reference-transaction" else "")
    return (
        "#!/bin/sh\n"
        f"{MARKER} {version}\n"
        "# Written by the SpecSeal plugin (hooks/hook-install.py), which rewrites\n"
        "# it when the installed plugin moves and never touches a hook file\n"
        "# without the line above. Removing the plugin leaves this a no-op.\n"
        f"h={target}\n"
        '[ -f "$h" ] || exit 0\n'
        + _NARROW[hook]
        + p2
        + 'if command -v python3 >/dev/null 2>&1; then exec python3 "$h" "$@"; fi\n'
        'if command -v py >/dev/null 2>&1; then exec py -3 "$h" "$@"; fi\n'
        "exit 0\n"
    )


def read_stub(path):
    """(ours, version, target) for the hook file at `path`, or None if absent.

    `ours` is whether the marker line is there; `target` is the entry point the
    stub runs, "" when it cannot be read back.
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(4096)
    except FileNotFoundError:
        return None
    except OSError:
        return (False, "", "")
    lines = head.splitlines()
    if len(lines) < 2 or not lines[1].startswith(MARKER):
        return (False, "", "")
    version = lines[1][len(MARKER) :].strip()
    target = ""
    for line in lines:
        if line.startswith("h='") and line.endswith("'"):
            target = line[3:-1].replace("'\\''", "'")
            break
    return (True, version, target)


def _git(top, *args):
    try:
        out = subprocess.run(
            ["git", "-C", top, *args],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else ""


def hooks_path_setting(top):
    """`core.hooksPath` as git reads it for `top`, or "" when it is unset.

    Set at any level -- the repository, the person's global config, the
    system's -- it moves every hook git runs there, so a stub under the common
    git directory would never run.
    """
    return _git(top, "config", "--get", "core.hooksPath") or ""


def hooks_dir(common):
    """Where git runs hooks for a clone whose common git directory is `common`,
    when `core.hooksPath` is unset: one directory for every worktree of it."""
    return os.path.join(common, "hooks") if common else ""


def slot(top, common):
    """("ours" | "free" | "foreign", detail) for the clone at `top`.

    `foreign` carries what took the slot: `core.hooksPath` and its value, or
    the hook file that is not this plugin's. `ours` means every hook this
    plugin writes is there with its marker; `free` means none is foreign and
    at least one is missing or stale -- the installer's to write.
    """
    setting = hooks_path_setting(top)
    if setting:
        return "foreign", f"core.hooksPath is set to {setting}"
    directory = hooks_dir(common)
    if not directory:
        return "foreign", "the clone's git directory could not be read"
    current = True
    for hook in HOOKS:
        found = read_stub(os.path.join(directory, hook))
        if found is None:
            current = False
            continue
        ours, version, target = found
        if not ours:
            return "foreign", os.path.join(directory, hook)
        if (
            version != plugin_version()
            or target != entry_point(hook)
            or not os.path.isfile(target)
        ):
            current = False
    return ("ours" if current else "free"), directory


def decides(top, common=None):
    """True when git runs this plugin's judgment for actions in `top`'s clone.

    Every stub present with its marker and pointing at an entry point that
    exists, and nothing moving git's hooks elsewhere. The stub's version is
    not asked: a stub an older plugin wrote still runs a judgment, and the one
    it runs is the path it names. A text path that stands aside on this
    answer is never standing aside for a hook that will not run.
    """
    if not top:
        return False
    if common is None:
        import optin

        common = optin.git_common_dir(top)
    if not common or hooks_path_setting(top):
        return False
    directory = hooks_dir(common)
    for hook in HOOKS:
        found = read_stub(os.path.join(directory, hook))
        if not found or not found[0] or not found[2] or not os.path.isfile(found[2]):
            return False
    return True
