#!/usr/bin/env python3
"""evidence_check — does the evidence ledger still point at what it claims?

Scans the spec-to-code map (default: .specseal/map.md, .specseal/map/*.md,
and the pre-0.10 docs/**/_evidence.md) for `file:line` /
`file:start-end` coordinates and classifies each:

  BROKEN   file missing, or the line range exceeds the file's length
  DRIFTED  the range was touched by commits since the row's baseline
           (the coordinate may still be right — but nobody has re-verified it)
  OK       resolvable and untouched since that baseline
  EXTERNAL path not in this repo and no --map given — cannot judge here

A row's baseline is the commit the row FIRST APPEARED in — the tree its
author read the code against. A stamp written in the row wins where there is
one, for rows written under the older rule, and the ledger header's baseline
is the fallback where neither can answer. Without a per-row form, one wide
refactor drifts every row at once and the cheapest way out is bumping the
header, which re-dates every claim without re-reading any of them.

Deriving it is what lets a ledger split into `.specseal/map/<work-item>.md`
fragments that carry no header of their own, and what survives a squash: the
answer is computed on the history in front of it, so no rewrite can orphan it.
First appearance rather than last touch, because a commit that rewrites rows
in bulk — a migration, a reformat, a merge resolution — would otherwise pull
every row it touched forward to itself and report the ledger green.

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
# The leading `.` is allowed: a coordinate in `.github/` or `.specseal/` was
# read as `github/...` and reported EXTERNAL — the plugin could not cite its
# own directory.
COORD_RE = re.compile(
    r"(?P<path>[A-Za-z0-9_@.][A-Za-z0-9_.@/-]*[/.][A-Za-z0-9_.@/-]*?):(?P<start>\d+)(?:-(?P<end>\d+))?\b"
)
# `example.com:8080` in a URL has the coordinate shape exactly; every ledger
# citing a link used to print it as EXTERNAL noise. Drop matches whose path is
# the authority part of a URL.
URL_HOST_RE = re.compile(r"(?://|\bhttps?:)[^\s)\]<>\"']*$")
SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
# A row's STAMP: the date and the SHA together, backticked or not. Rows write
# no SHA under the current rule, so a bare hex word in a row is prose — and
# prose that names a commit is exactly what a row about the ledger contains.
# `tests/test_ledger_stamps_resolve.py` reads the same shape.
STAMP_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\s+`?([0-9a-f]{7,40})`?")


def git(args, cwd):
    r = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, encoding="utf-8", errors="replace"
    )
    return r.returncode, r.stdout


def is_commit(sha, repo, cache):
    key = (repo, sha)
    if key not in cache:
        code, _ = git(["cat-file", "-e", f"{sha}^{{commit}}"], repo)
        cache[key] = code == 0
    return cache[key]


def header_of(text):
    """The ledger's header: everything above its first row that cites code.

    A row carrying a coordinate is a claim, not a declaration, so the header
    ends where the first one begins. Without that cut the scan below reaches
    into the rows themselves — and a row ABOUT a commit names it in prose,
    which then becomes the whole ledger's baseline. Measured on the first
    fragment written here: a commit resolvable in one clone and nowhere else
    was picked up out of a row and printed as the ledger's baseline.

    A Baseline declaration cites no code, so nothing that was found before is
    lost. The 2000-character cap stays as the outer bound.
    """
    header = text[:2000]
    at = 0
    for line in header.splitlines(keepends=True):
        if line.lstrip().startswith("|") and COORD_RE.search(line):
            return header[:at]
        at += len(line)
    return header


def find_baseline(text, repo, cache=None):
    """First plausible commit SHA in the ledger's header that exists in repo."""
    cache = {} if cache is None else cache
    for m in SHA_RE.finditer(header_of(text)):
        if is_commit(m.group(0), repo, cache):
            return m.group(0)
    return None


def blame_lines(repo, rel, cache):
    """{line in the working tree: (commit that last touched it, its line there)}.

    One `git blame` per ledger, cached, rather than one per row: a ledger has
    as many rows as the work has accumulated and blame reads the whole file
    either way. This is not the baseline — `first_appearance` walks back from
    here to find that — it is the anchor that makes the walk possible, because
    the file is read from the WORKING TREE and `git log -L` counts lines in a
    commit. An uncommitted insertion above a row shifts every number below it,
    and blame is what maps one numbering to the other.

    **`--porcelain`, and the format is load-bearing.** Blame's default and
    `-s` forms mark a boundary commit by prefixing its SHA with `^` —
    `^9829412` for every line of this repository's own ledger that reaches the
    walk's first commit — and a reader that takes the first field verbatim
    hands `git cat-file` a name it rejects. Porcelain spells the same SHA
    plainly and puts `boundary` on a metadata line of its own, so there is
    nothing to strip.

    Lines nobody has committed yet blame as the all-zero SHA — reachable in
    ordinary use, since a ledger is edited before it is committed. They are
    dropped here rather than returned: handing `git diff` a name that resolves
    to nothing answers "nothing changed", which is a pass produced by a
    failure.
    """
    key = (repo, rel)
    if key not in cache:
        code, out = git(["blame", "--porcelain", "--", rel], repo)
        found = {}
        if code == 0:
            # A porcelain header is `<40-hex> <orig line> <final line>` at the
            # start of a line; every content line is TAB-prefixed and every
            # other metadata line starts with a word.
            for m in re.finditer(r"^([0-9a-f]{40}) (\d+) (\d+)", out, re.MULTILINE):
                if m.group(1) != "0" * 40:
                    found[int(m.group(3))] = (m.group(1), int(m.group(2)))
        cache[key] = found
    return cache[key]


def first_appearance(repo, rel, sha, lineno, cache):
    """The commit a ledger row was WRITTEN in, or None.

    `git log -L <n>,<n>:<file>` walks one line's history and lists every commit
    that changed it, newest first. The oldest entry is where the row came into
    existence, which is the tree its author read the code against — the
    as-of date a claim actually has.

    **Why not the last commit that touched the line**, which one `git blame`
    would have answered for free. Measured on this repository's own ledger, at
    36 coordinates: blame's answer is LATER than the stamp the row wrote on 36
    of them, equal on none, earlier on none. A later baseline is a narrower
    diff window, so last-touch catches strictly less drift than the stamps it
    replaces — uniformly, and with nothing re-read to earn it.

    The cause is in the same measurement. Under last touch, `cdb2434` — a
    release-preparation commit that rewrote stamps in bulk — is the baseline
    for 16 of the 36 rows, because any commit rewriting rows en masse pulls
    every one of them forward to itself. Under first appearance `cdb2434` is
    the baseline for none of them, and the 36 spread over four commits
    reaching back to the ledger's first.

    Stated precisely, because the loose version is wrong: a bulk rewrite
    collapsing drift windows is not something a computed baseline introduces.
    The written stamp does it too — `cdb2434` holds those 16 rows precisely
    because it rewrote their stamps by hand. What differs is the trigger. The
    written scheme resets a row only when somebody deliberately edits its
    stamp; last touch resets it on any edit to the line, a typo included.
    Deriving the baseline automates an existing failure and widens what fires
    it, and first appearance is what narrows it back.

    **A row moved between ledger files loses this**, and that is the rule the
    migration turns on. `git log -L` does not follow a row out of a file that
    STAYS — executed: a ledger keeps one row and gives another to a new file,
    and in that file the row's history begins at the move. Renaming a whole
    ledger is a different case, which git detects and follows; a migration is
    not that shape. So rows carried into a fragment keep their written stamps
    verbatim, the stamp wins over anything derived, and the move resets
    nobody's window. A derived baseline is for rows born where they live.

    What it costs: one git call per row instead of one per file. Measured here
    at 455 ms for 36 rows against 17 ms for the single blame, about 13 ms a
    row. Rows carrying a stamp never reach this, so the bill is proportional
    to rows with no stamp of their own.

    What neither reading fixes: a row written on one branch citing lines that
    another branch changed, where the second branch merges first. The row's
    first appearance is its own squash commit, which already contains the
    other change, so it reads clean while its coordinate was stale on arrival.
    Catching that needs the coordinate checked against the code it cites,
    which is issue #31 — recorded in this work item's `questions.md`.
    """
    key = (repo, rel, sha, lineno)
    if key not in cache:
        code, out = git(
            ["log", "-L", f"{lineno},{lineno}:{rel}", "--format=%H", "-s", sha], repo
        )
        oldest = None
        if code == 0:
            for line in out.splitlines():
                word = line.strip()
                if SHA_RE.fullmatch(word) and len(word) == 40:
                    oldest = word
        cache[key] = oldest
    return cache[key]


def row_baseline(text, pos, repo, cache, ledger=None, root=None, blame=None):
    """The commit a row's drift is measured from, or None.

    One baseline for a whole ledger makes drift an all-or-nothing event: any
    wide refactor drifts every row at once, and the cheapest way out is to
    bump the header — which re-dates every claim without re-reading any of
    them. A row measured from its own last change drains row by row instead.

    Two things can answer, in this order.

    **A stamp written in the row** — a date and a SHA together, `2026-08-24
    a1b2c3d`, which is how rows were stamped before this. A bare SHA-shaped
    word is NOT one, and requiring the date is what makes the difference
    between a stamp and prose readable. Measured on the first fragment written
    under the new rule: its rows discuss two commits by name, one of them
    resolvable in the clone that wrote it and nowhere else, and the earlier
    word won — so the row measured from a commit no other checkout has, and
    said so in a report nobody would question. Coordinates are stripped before
    the scan for the same reason: a directory named like a short SHA sits in
    the same row and must not be read as one.

    **The commit the row first appeared in**, for a row that carries none.
    A stamp typed by hand names a commit the branch made, and a squash
    discards it: seven rows of this repository's own ledger named `9b5501d`,
    which `git merge-base --is-ancestor 9b5501d origin/main` answers no to —
    it survives on one unmerged local branch and nowhere a fresh clone can
    see. Pull request #49 repaired those cells by hand. A row's first
    appearance is computed on the history in front of it, so nothing can
    orphan it: after the squash it is the squash commit, which is the value
    #49 typed in.

    `first_appearance` holds why this is the row's FIRST commit and not its
    last, which is the reading one `git blame` would have given for free.

    The baseline is only ever a diff base (see `changed_ranges`), never an
    identity, so a commit that merely CONTAINS the row is the right answer.

    Re-wording a row does not move its baseline: `git log -L` walks past the
    edit to where the line came into existence. The Checked column keeps the
    DATE all the same, because it is the one thing here a person asserts —
    everything else is derived from history, and a derived date says when the
    row was written rather than when somebody read the code.

    The walk is skipped where it cannot answer, and the ledger header's
    baseline is still the fallback there. `ledger`/`root` unset is one such
    caller — `tests/test_ledger_stamps_resolve.py` asks only what the row
    wrote. The other is a coordinate resolving in another checkout: this
    repository's commits are not a diff base in that one.
    """
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    line = text[start:] if end == -1 else text[start:end]
    line = COORD_RE.sub(" ", line)
    for m in STAMP_RE.finditer(line):
        if is_commit(m.group(1), repo, cache):
            return m.group(1)
    if ledger is not None and root is not None and repo == root:
        blame = {} if blame is None else blame
        rel = os.path.relpath(ledger, root)
        anchor = blame_lines(root, rel, blame).get(text.count("\n", 0, pos) + 1)
        if anchor:
            sha = first_appearance(root, rel, anchor[0], anchor[1], blame)
            # Checked before it is used, at the one place a derived answer
            # leaves this function. Whatever a future git spells differently —
            # a decorated boundary, a name from a graft — reaches
            # `changed_ranges` only if it resolves, and falls back to the
            # header if it does not.
            if sha and is_commit(sha, root, cache):
                return sha
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


def check_ledger(
    ledger, root, maps, cache, default_repo=None, sha_cache=None, blame=None
):
    sha_cache = {} if sha_cache is None else sha_cache
    blame = {} if blame is None else blame
    with open(ledger, encoding="utf-8", errors="replace") as f:
        text = f.read()
    baseline = find_baseline(text, root, sha_cache)
    default_baseline = (
        find_baseline(text, default_repo, sha_cache) if default_repo else None
    )
    findings = []  # (status, coord, detail)
    seen = set()
    for m in COORD_RE.finditer(text):
        if URL_HOST_RE.search(text[: m.start()]):
            continue  # `https://example.com:8080/x` — a URL, not a coordinate
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
        # A row is measured from its own last change — a SHA it wrote, else
        # what `git blame` says about its line. The header baseline is the
        # fallback for the rows neither can answer for.
        base = row_baseline(
            text, m.start(), repo, sha_cache, ledger=ledger, root=root, blame=blame
        ) or (
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

    # Three locations, because the map moved and old repos keep working.
    # `.specseal/map.md` is where it lives now; `map/*.md` is for a repo that
    # outgrew one file; `docs/**/_evidence.md` is the pre-0.10 address and
    # stops being searched at 1.0.0.
    patterns = args.ledger or [
        ".specseal/map.md",
        ".specseal/map/*.md",
        "docs/**/_evidence.md",
    ]
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
    cache, sha_cache, blame = {}, {}, {}
    for ledger in ledgers:
        baseline, findings = check_ledger(
            ledger, root, maps, cache, default_repo, sha_cache, blame
        )
        rel_ledger = os.path.relpath(ledger, root)
        # A fragment carries no header baseline on purpose — every row in it
        # measures from its own line's history. Saying "skipped" there would
        # report the working case as the broken one, and the two have to be
        # told apart: nothing measures from anything only when the history
        # walk is silent too, which is a ledger git has never seen.
        if baseline:
            base_note = baseline[:9]
        elif blame_lines(root, rel_ledger, blame):
            base_note = "none in the header — each row measures from its own history"
        else:
            base_note = "none — drift check skipped"
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
