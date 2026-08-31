#!/usr/bin/env python3
"""deferral-check — resolve the answerer named in an `unverified` row.

Condition 4 lets a claim go out unproven as long as it says *who or what
answers it*. Nothing checked that the answerer existed. The measured failure:
a session narrowed its run to one domain and deferred the rest to CI. That
repository's workflows assigned reviewers, deployed on push to the default
branch, and checked a migration graph. None ran the test suite, the default
branch had no protection, and the pre-commit hooks were lint and typecheck
only. The deferral named something that was not there, which reads exactly
like a deferral that was honoured.

So this resolves the common answerer. Given a repo and a kind of check, it
reports what would actually run it without being asked, and separates three
outcomes that a reader otherwise collapses into one:

  resolves        something runs it on pull requests
  wrong trigger   something runs it, but only after the point being deferred
  local only      a pre-commit hook runs it on the committer's machine
  nothing         no one runs it

Deliberately a text scan, not a YAML parse: the gates here are stdlib-only,
and a dependency for this would cost more than the precision it buys. The
cost is stated rather than hidden — see `read_events` and `KNOWN_LIMITS`.

Exit codes: 0 every requested kind resolves · 1 at least one does not ·
2 the path or arguments were unusable.
"""

import argparse
import os
import re
import sys

# A runner token is matched against the text of a command line. Word-boundary
# anchored so `pytest-cov` in a dependency list is not read as a test run.
RUNNERS = {
    "tests": [
        r"\bpytest\b",
        r"\bgo test\b",
        r"\bcargo test\b",
        r"\bnpm (?:run )?test\b",
        r"\b(?:pnpm|yarn) (?:run )?test\b",
        r"\bjest\b",
        r"\bvitest\b",
        r"\brspec\b",
        r"\bmvn (?:\S+ )*test\b",
        r"\bgradle (?:\S+ )*test\b",
        r"\bdotnet test\b",
        r"\bphpunit\b",
        r"\btox\b",
        r"\bmake test\b",
        r"\bpython3? -m unittest\b",
        r"\brails test\b",
        r"\bbin/test\b",
    ],
    "lint": [
        r"\bruff\b",
        r"\beslint\b",
        r"\bflake8\b",
        r"\bpylint\b",
        r"\bgolangci-lint\b",
        r"\bcargo clippy\b",
        r"\brubocop\b",
        r"\bmake lint\b",
        r"\bbiome\b",
    ],
    "typecheck": [
        r"\bmypy\b",
        r"\bpyright\b",
        r"\btsc\b",
        r"\bmake typecheck\b",
        r"\bgo vet\b",
    ],
}
KINDS = tuple(RUNNERS)

# Events that run before a change lands. A deferral is made at that point, so
# only these can answer it; anything else is named and not counted.
PRE_MERGE_EVENTS = {"pull_request", "pull_request_target", "merge_group"}

KNOWN_LIMITS = (
    "reads command text, not a YAML graph: a runner reached through a "
    "composite action, a reusable workflow, or a script this cannot see "
    "reads as absent"
)


def read_events(text):
    """Event names from a GitHub workflow's `on:` block.

    Three forms in the wild: `on: push`, `on: [push, pull_request]`, and a
    block of indented `event:` keys. Anything else lands as an empty set,
    which is reported as unknown rather than as absent.
    """
    events = set()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^on\s*:\s*(.*)$", line)
        if not m:
            continue
        rest = m.group(1).strip()
        if rest.startswith("["):
            events |= {e.strip() for e in rest.strip("[]").split(",") if e.strip()}
        elif rest and not rest.startswith("#"):
            events.add(rest)
        else:
            for follow in lines[i + 1 :]:
                if not follow.strip() or follow.lstrip().startswith("#"):
                    continue
                indent = len(follow) - len(follow.lstrip())
                if indent == 0:
                    break
                key = re.match(r"^\s*-?\s*([A-Za-z_][\w-]*)\s*:?\s*$", follow)
                if key and indent <= 2:
                    events.add(key.group(1))
        break
    return events


def runners_in(text, kind):
    """Command lines in `text` that run `kind`, deduped, in file order."""
    found = []
    for line in text.splitlines():
        stripped = line.strip().lstrip("-").strip()
        if not stripped or stripped.startswith("#"):
            continue
        for pattern in RUNNERS[kind]:
            if re.search(pattern, stripped):
                cmd = re.sub(r"^(?:run|entry|script)\s*:\s*", "", stripped)
                if cmd not in found:
                    found.append(cmd)
                break
    return found


def workflow_files(root):
    d = os.path.join(root, ".github", "workflows")
    if not os.path.isdir(d):
        return []
    return [
        os.path.join(d, n)
        for n in sorted(os.listdir(d))
        if n.endswith((".yml", ".yaml"))
    ]


def other_ci_files(root):
    """CI systems whose config is a single known path."""
    out = []
    for rel in (
        ".gitlab-ci.yml",
        ".circleci/config.yml",
        "Jenkinsfile",
        "azure-pipelines.yml",
        ".drone.yml",
        ".travis.yml",
    ):
        p = os.path.join(root, rel)
        if os.path.isfile(p):
            out.append(p)
    d = os.path.join(root, ".buildkite")
    if os.path.isdir(d):
        out += [
            os.path.join(d, n)
            for n in sorted(os.listdir(d))
            if n.endswith((".yml", ".yaml"))
        ]
    return out


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def inspect(root, kind):
    """(verdict, lines) for one kind. Verdict is the exit-code decision."""
    resolving, wrong_trigger, local_only = [], [], []

    for path in workflow_files(root):
        text = read(path)
        cmds = runners_in(text, kind)
        if not cmds:
            continue
        name = os.path.relpath(path, root)
        events = read_events(text)
        if not events or events & PRE_MERGE_EVENTS:
            when = "on " + ", ".join(sorted(events)) if events else "trigger unread"
            resolving.append((name, cmds, when))
        else:
            wrong_trigger.append((name, cmds, "on " + ", ".join(sorted(events))))

    for path in other_ci_files(root):
        cmds = runners_in(read(path), kind)
        if cmds:
            # These systems run every pipeline on push by default; treating
            # them as pre-merge is the reading that does not invent a failure.
            resolving.append((os.path.relpath(path, root), cmds, "pipeline"))

    pc = os.path.join(root, ".pre-commit-config.yaml")
    if os.path.isfile(pc):
        cmds = runners_in(read(pc), kind)
        if cmds:
            local_only.append((".pre-commit-config.yaml", cmds, "local hook"))

    lines = []
    for name, cmds, when in resolving:
        lines.append(f"  answers   {name} ({when}) — {'; '.join(cmds)}")
    for name, cmds, when in wrong_trigger:
        lines.append(
            f"  too late  {name} ({when}, not pull_request) — {'; '.join(cmds)}"
        )
    for name, cmds, when in local_only:
        lines.append(
            f"  local     {name} ({when}, the committer's machine "
            f"only) — {'; '.join(cmds)}"
        )

    if resolving:
        return True, lines
    if not lines:
        lines.append("  nothing runs it")
    return False, lines


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="deferral-check",
        description="Resolve the answerer named in an `unverified` row.",
    )
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument(
        "--kind",
        default="tests",
        choices=(*KINDS, "all"),
        help="which check is being deferred (default: tests)",
    )
    args = ap.parse_args(argv)

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"deferral-check: no such path: {args.path}", file=sys.stderr)
        return 2

    kinds = KINDS if args.kind == "all" else (args.kind,)
    unresolved = []
    for kind in kinds:
        ok, lines = inspect(root, kind)
        print(f"{kind}: {'resolves' if ok else 'DOES NOT RESOLVE'}")
        for line in lines:
            print(line)
        if not ok:
            unresolved.append(kind)

    print(f"\nlimit: {KNOWN_LIMITS}")
    if unresolved:
        print(
            f"\nDeferring {', '.join(unresolved)} to CI names an answerer "
            f"that is not there. Run it, or say it is unanswered."
        )
        return 1
    return 0


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main())
