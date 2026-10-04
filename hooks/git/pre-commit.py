#!/usr/bin/env python3
"""git `pre-commit`: the commit gate, inside the commit (#692).

Run by the stub `hooks/hook-install.py` writes, from the installed plugin, with
git's working directory at the root of the worktree the commit lands in. That
is the whole of where-it-lands: no command text is read, so no shell
construct -- a `cd` behind a redirection, a loop variable, an `eval` -- can
route the commit somewhere this did not judge.

What it judges is `hooks/gate.py#arms_missing`, the judgment the PreToolUse
fallback shares. What it reads to judge:

  * the session, from `hooks/hooksession.py` -- none is a person's own commit,
    which is theirs (P2, answer (a));
  * the waivers, from `git -c specseal.waive=<arm>` (`GIT_CONFIG_PARAMETERS`,
    phase 1's M11) and from the old bare words `hooks/answers.py` carried
    over from the Bash call (P3, answer (a));
  * the paths, from the index git is about to commit -- `GIT_INDEX_FILE`
    names it for `-a` and for a pathspec commit alike (M2);
  * the press, from the session's own transcript
    (`hooks/worktree_consent.py#automation_answered`), only once a refusal is
    decided.

A commit it lets through leaves a one-shot mark for `reference-transaction`,
keyed by the old HEAD, the tree and the commit's `GIT_AUTHOR_DATE` (M12), so
the backstop refuses only a commit that never came through here.

A refusal is the exit status and the text on stderr; git prints it into the
command's output and aborts the commit.
"""

import os
import sys

HOOKS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HOOKS)

import commitgate  # noqa: E402
import console  # noqa: E402


def main():
    return commitgate.pre_commit(os.getcwd(), os.environ, sys.stderr)


if __name__ == "__main__":
    console.to_utf8()
    sys.exit(main())
