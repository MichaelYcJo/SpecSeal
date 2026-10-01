#!/usr/bin/env python3
"""git `post-checkout`: a worktree creation, judged and recorded where it ran (#692).

Run by the stub `hooks/hook-install.py` writes, from the installed plugin. The
stub starts Python only when the previous HEAD is the null object id, which is
a creation and only a creation (phase 1's M3, M14). `hooks/creationgate.py`
holds what is decided and why.
"""

import os
import sys

HOOKS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HOOKS)

import creationgate  # noqa: E402


def main():
    return creationgate.post_checkout(os.getcwd(), os.environ, sys.argv[1:], sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
