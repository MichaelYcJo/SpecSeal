#!/usr/bin/env python3
"""git `reference-transaction`: the commit gate's backstop for `--no-verify` (#692).

`--no-verify` skips `pre-commit` and `commit-msg` and nothing else, so a
commit that bypassed the gate still has to move its branch, and this runs with
that update locked on disk. The stub starts Python only at `prepared` and only
where `GIT_AUTHOR_DATE` is exported, which every `git commit` and no other
branch-moving command does on the four gits measured (phase 1's M12). A
refusal here aborts the update: HEAD, the index and the working tree stay as
they were, with one unreachable commit object left (M2).

An update `pre-commit` already judged carries its one-shot mark, and passes.
"""

import os
import sys

HOOKS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HOOKS)

import commitgate  # noqa: E402
import console  # noqa: E402


def main():
    state = sys.argv[1] if len(sys.argv) > 1 else ""
    lines = sys.stdin.read().splitlines()
    return commitgate.reference_transaction(
        os.getcwd(), os.environ, state, lines, sys.stderr
    )


if __name__ == "__main__":
    console.to_utf8()
    sys.exit(main())
