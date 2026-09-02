#!/usr/bin/env python3
"""PostToolUse advisory: a commit that leaves ledger anchors broken is told so.

The rename that breaks a ledger row is caught at the commit that made it, in
the terminal where the rename just happened — not in CI minutes later, and not
by somebody remembering to run a command. The checker costs about 114 ms with
no git calls, which is what makes running it at every commit affordable.

**Advisory, never a gate.** A pre-commit block would fire on every
work-in-progress ledger state and fight the commit-early rule; PostToolUse
cannot block, and this would not want to. What a broken anchor costs is one
line here, naming the row and — where exactly one unit reconstructs the
recorded content — that unit, plus the one command that repairs everything
provable:

    evidence-check: this commit leaves 2 anchors broken
      BROKEN  src/app.py#total  locator not found — identical content at #total_price (renamed?)
      BROKEN  src/app.py#greet  locator not found
    `bin/evidence-check --reverify .` re-anchors what it can prove.

**Silent when clean, silent when the repository has no ledger, silent outside
opted-in repositories.** A line that prints on every commit is a line people
learn to skip; drift is not reported here for the same reason — a branch
mid-flight legitimately drifts. Two verdicts name something a person must
touch either way and both are printed: BROKEN, and OLD-FORMAT, whose block
carries the migration command instead of the re-anchor one.

No success check on the commit: no hook here reads exit codes, and the trade
is safe in both directions — after a failed commit the tree is unchanged, so
a clean ledger stays silent and a broken one prints a line that is true
anyway.

This arm runs under `hooks/dispatch.py`'s crash isolation, where a raising
gate is skipped silently (the rider at `run_gate` records what that silence
costs a GATE). For this arm the cost does not bite: it never blocks, so a
crash loses one reminder and defends nothing less — the same line prints
again at the next commit, and CI still says it at the pull request.

What a change to a gate must carry (`CONTRIBUTING.md`), answered for an
advisory: failure direction — wrong-silent misses one reminder that CI
repeats, wrong-print is a true line early, both cheap and the first cheaper;
prompt budget — zero, it asks nothing ever; platform — pure Python and one
in-process import, no process inspection.
"""

import importlib.util
import json
import os
import shlex
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console  # noqa: F401  (reconfigures the streams on import)
import optin

CHECKER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "skills",
    "evidence-check",
    "scripts",
    "evidence_check.py",
)
WRAPPERS = {"command", "env", "nohup", "time", "sudo"}


def commits_in(command):
    """True when some segment's command word is git with a commit subcommand.

    Word-level like the other post hooks, so `echo "git commit"` in prose does
    not fire. Over-matching is cheap here anyway: the advisory prints only
    when the ledger is actually broken, and then the line is true whatever
    command surfaced it.
    """
    import re

    for seg in re.split(r"&&|\|\||[;\n|]", command):
        try:
            toks = shlex.split(seg)
        except ValueError:
            continue
        i = 0
        while i < len(toks) and (
            ("=" in toks[i] and not toks[i].startswith("-"))
            or os.path.basename(toks[i]) in WRAPPERS
        ):
            i += 1
        if i < len(toks) and os.path.basename(toks[i]) == "git":
            if any(t == "commit" for t in toks[i + 1 :]):
                return True
    return False


def failing_rows(root, home=None):
    """[(status, coord, detail)] for every BROKEN and OLD-FORMAT row.

    Imported rather than spawned: dispatch already paid for this interpreter,
    and a second one would double the cost of the commit path for a check
    that usually says nothing.

    OLD-FORMAT is in the filter because the commit that needs the migration
    line most — one made in a repository whose ledger predates anchors — got
    silence from this hook when only BROKEN was read (round 4, 🟡 6).

    `ledger.md` and `ledger/*.md` are under `home` — the `seal/` that
    `optin.home_at(root)` resolves, which in local mode is under the git
    directory (#80) — and `docs/**/_evidence.md` stays under the repository
    root, because it is a committed file at an old address and not part of
    the root that moved. Spelling `seal/` under `root` here is what left a
    local-mode ledger unread at every commit.
    """
    spec = importlib.util.spec_from_file_location("specseal_evidence", CHECKER)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    import glob

    home = home or optin.home_at(root)
    patterns = [os.path.join(root, "docs", "**", "_evidence.md")]
    if home:
        patterns = [
            os.path.join(home, "ledger.md"),
            os.path.join(home, "ledger", "*.md"),
            *patterns,
        ]
    out = []
    for pat in patterns:
        for ledger in sorted(glob.glob(pat, recursive=True)):
            for status, coord, detail in ec.check_ledger(ledger, root, {}):
                if status in ("BROKEN", "OLD-FORMAT"):
                    out.append((status, coord, detail))
    return out


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return
    if payload.get("tool_name") != "Bash":
        return
    command = (payload.get("tool_input") or {}).get("command") or ""
    if not commits_in(command):
        return
    cwd = payload.get("cwd") or os.getcwd()
    root = optin.repo_root(cwd)
    home = optin.home_at(root)
    if not root or not home:
        return
    rows = failing_rows(root, home)
    if not rows:
        return
    broken = [(c, d) for s, c, d in rows if s == "BROKEN"]
    old = [(c, d) for s, c, d in rows if s == "OLD-FORMAT"]
    lines = []
    if broken:
        n = len(broken)
        lines.append(
            f"evidence-check: this commit leaves {n} anchor{'s'[: n != 1]} broken"
        )
        lines += [f"  BROKEN  {coord}  {detail}" for coord, detail in broken]
        lines.append("`bin/evidence-check --reverify .` re-anchors what it can prove.")
    if old:
        n = len(old)
        lines.append(
            f"evidence-check: {n} pre-anchor ledger row{'s'[: n != 1]} — "
            "nothing is checked until they migrate"
        )
        lines += [f"  OLD-FORMAT  {coord}" for coord, _ in old]
        lines.append("`bin/evidence-check --migrate .` rewrites what it can prove.")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
