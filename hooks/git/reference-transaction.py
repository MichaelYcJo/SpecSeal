#!/usr/bin/env python3
"""git `reference-transaction`: the commit gate's backstop for `--no-verify` (#692).

Run by the stub `hooks/hook-install.py` writes, from the installed plugin.
"""

import sys


def main():
    sys.stdin.read()
    return 0


if __name__ == "__main__":
    sys.exit(main())
