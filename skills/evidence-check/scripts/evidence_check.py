#!/usr/bin/env python3
"""evidence_check — does the evidence ledger still point at what it claims?

Scans evidence ledgers (default: docs/**/_evidence.md) for `file:line` /
`file:start-end` coordinates and classifies each:

  BROKEN   file missing, or the line range exceeds the file's length
  DRIFTED  the range was touched by commits since the ledger's baseline SHA
           (the coordinate may still be right — but nobody has re-verified it)
  OK       resolvable and untouched since the baseline
  EXTERNAL path not in this repo and no --map given — cannot judge here

Exit codes: 0 clean · 1 drift only · 2 broken coordinates (or drift with
--strict). Designed for CI: a spec-code link that stops resolving should fail
the build the same way a broken test does.

Usage:
  evidence_check.py [--ledger GLOB]... [--map NAME=PATH]... [--strict] [ROOT]

--map resolves cross-repo coordinates (e.g. a migration's original repo):
  a coordinate `legacy-api/src/service.py:120` with --map legacy-api=~/work/legacy-api
  is checked inside that checkout instead of ROOT.
"""

import argparse
import glob
import os
import re
import subprocess
import sys

# `path:12` or `path:12-34` where path looks like a file (has / or .ext).
COORD_RE = re.compile(
    r"(?P<path>[A-Za-z0-9_@][A-Za-z0-9_.@/-]*[/.][A-Za-z0-9_.@/-]*?):(?P<start>\d+)(?:-(?P<end>\d+))?\b"
)
SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")


def git(args, cwd):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout


def find_baseline(text, repo):
    """First plausible commit SHA in the ledger's header that exists in repo."""
    header = text[:2000]
    for m in SHA_RE.finditer(header):
        code, _ = git(["cat-file", "-e", f"{m.group(0)}^{{commit}}"], repo)
        if code == 0:
            return m.group(0)
    return None


def changed_ranges(repo, baseline, path):
    """Line ranges of `path` touched since baseline, in BASELINE numbering.

    Ledger coordinates were written against the baseline, so overlap must be
    judged on the diff's OLD side — a deletion shifts every later line, and
    new-side positions would miss the very lines the citation meant (caught
    by test_pure_deletion_still_drifts_neighbors).
    """
    code, out = git(["diff", "--unified=0", f"{baseline}..HEAD", "--", path], repo)
    if code != 0:
        return []
    ranges = []
    for m in re.finditer(r"^@@ -(\d+)(?:,(\d+))? \+\S+ @@", out, re.MULTILINE):
        start = int(m.group(1))
        count = int(m.group(2)) if m.group(2) is not None else 1
        # A pure insertion (count 0) still touches its neighbor: keep 1 line.
        ranges.append((start, start + max(count, 1) - 1))
    return ranges


def overlaps(a_start, a_end, ranges):
    return any(not (a_end < s or a_start > e) for s, e in ranges)


def file_lines(path):
    try:
        with open(path, "rb") as f:
            return sum(1 for _ in f)
    except OSError:
        return None


def check_ledger(ledger, root, maps, cache, default_repo=None):
    text = open(ledger, encoding="utf-8", errors="replace").read()
    baseline = find_baseline(text, root)
    default_baseline = find_baseline(text, default_repo) if default_repo else None
    findings = []  # (status, coord, detail)
    seen = set()
    for m in COORD_RE.finditer(text):
        raw_path, start = m.group("path"), int(m.group("start"))
        end = int(m.group("end") or start)
        coord = f"{raw_path}:{start}" + (f"-{end}" if end != start else "")
        if coord in seen:
            continue
        seen.add(coord)

        # Resolve: mapped prefix wins, then repo root, then --default-repo
        # (ledgers for migrations state coordinates against the ORIGINAL repo
        # with no prefix — the default repo is where those resolve).
        repo, rel = root, raw_path
        for name, mapped in maps.items():
            if raw_path == name or raw_path.startswith(name + "/"):
                repo = mapped
                rel = raw_path[len(name) :].lstrip("/") or "."
                break
        else:
            if (
                not os.path.isfile(os.path.join(root, raw_path))
                and default_repo
                and os.path.isfile(os.path.join(default_repo, raw_path))
            ):
                repo = default_repo
        full = os.path.join(repo, rel)

        if not os.path.isfile(full):
            # Cross-repo coordinates always carry a prefix directory
            # (legacy-api/src/...). A bare root-level path whose file is gone
            # is a broken citation, not an external one — EXTERNAL is exempt
            # from --strict, and a deleted file must fail the build.
            if (
                repo == root
                and "/" in rel
                and not os.path.exists(os.path.join(root, rel.split("/")[0]))
            ):
                findings.append(
                    ("EXTERNAL", coord, "not in this repo; pass --map/--default-repo")
                )
            else:
                findings.append(("BROKEN", coord, "file not found"))
            continue
        n = file_lines(full)
        if n is not None and end > n:
            findings.append(("BROKEN", coord, f"file has {n} lines"))
            continue
        base = (
            baseline
            if repo == root
            else (default_baseline if repo == default_repo else None)
        )
        if base:
            key = (repo, base, rel)
            if key not in cache:
                cache[key] = changed_ranges(repo, base, rel)
            if overlaps(start, end, cache[key]):
                findings.append(
                    ("DRIFTED", coord, f"touched since {base[:9]} — re-verify")
                )
                continue
        findings.append(("OK", coord, ""))
    return baseline, findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--ledger", action="append", default=[])
    ap.add_argument("--map", action="append", default=[], metavar="NAME=PATH")
    ap.add_argument(
        "--default-repo",
        metavar="PATH",
        help="repo that unprefixed coordinates resolve against when "
        "absent from ROOT (migration ledgers cite the original repo)",
    )
    ap.add_argument("--strict", action="store_true", help="drift also fails")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    default_repo = (
        os.path.abspath(os.path.expanduser(args.default_repo))
        if args.default_repo
        else None
    )
    maps = {}
    for spec in args.map:
        name, _, path = spec.partition("=")
        maps[name] = os.path.abspath(os.path.expanduser(path))

    patterns = args.ledger or ["docs/**/_evidence.md"]
    ledgers = sorted(
        {
            p
            for pat in patterns
            for p in glob.glob(os.path.join(root, pat), recursive=True)
        }
    )
    if not ledgers:
        print("no evidence ledgers found — nothing to check")
        return 0

    totals = {"OK": 0, "DRIFTED": 0, "BROKEN": 0, "EXTERNAL": 0}
    cache = {}
    for ledger in ledgers:
        baseline, findings = check_ledger(ledger, root, maps, cache, default_repo)
        rel_ledger = os.path.relpath(ledger, root)
        base_note = baseline[:9] if baseline else "none — drift check skipped"
        print(f"\n{rel_ledger}  (baseline: {base_note})")
        for status, coord, detail in findings:
            totals[status] += 1
            if status != "OK":
                print(f"  {status:8} {coord}  {detail}")
        print(
            f"  {sum(1 for s, _, _ in findings if s == 'OK')} ok · "
            f"{sum(1 for s, _, _ in findings if s == 'DRIFTED')} drifted · "
            f"{sum(1 for s, _, _ in findings if s == 'BROKEN')} broken · "
            f"{sum(1 for s, _, _ in findings if s == 'EXTERNAL')} external"
        )

    print(
        f"\ntotal: {totals['OK']} ok · {totals['DRIFTED']} drifted · "
        f"{totals['BROKEN']} broken · {totals['EXTERNAL']} external"
    )
    if totals["BROKEN"]:
        return 2
    if totals["DRIFTED"] and args.strict:
        return 2
    if totals["DRIFTED"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
