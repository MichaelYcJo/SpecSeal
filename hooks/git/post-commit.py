#!/usr/bin/env python3
"""git `post-commit`: the implementer notice, after a commit that happened (#692).

`hooks/implementer-notice.py` holds what the notice says and why. It used to
learn that a commit happened by reading the Bash command for `git commit`;
git running this hook is that fact, in the worktree the commit landed in.
"""

import os
import sys

HOOKS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HOOKS)

import commitgate  # noqa: E402
import console  # noqa: E402


def main():
    return commitgate.post_commit(os.getcwd(), os.environ, sys.stdout)


if __name__ == "__main__":
    console.to_utf8()
    sys.exit(main())
