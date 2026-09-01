#!/usr/bin/env python3
"""evidence_check — does the evidence ledger still point at what it claims?

Scans the spec-to-code map (default: .specseal/map.md, .specseal/map/*.md,
and the pre-0.10 docs/**/_evidence.md) for `file:line` /
`file:start-end` coordinates and classifies each:

  BROKEN     file missing, or the line range exceeds the file's length
  DRIFTED    the range was touched by commits since the row's baseline
             (the coordinate may still be right — but nobody re-verified it)
  UNMEASURED resolvable, but the row has no baseline at all, so nothing was
             compared. NOT the same as untouched, which is what `OK` used to
             say for it
  AMBIGUOUS  the row carries two distinct stamps. It is still measured, from
             the widest of them, and the disagreement is reported
  OK         resolvable, compared against a baseline, and untouched
  EXTERNAL   path not in this repo and no --map given — cannot judge here

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

Exit codes: 0 clean · 1 drift only · 2 broken coordinates, or — under
--strict — drift, UNMEASURED or AMBIGUOUS. Designed for CI: a spec-code link
that stops resolving should fail the build the same way a broken test does.

UNMEASURED and AMBIGUOUS print and pass without --strict, because a fragment
is uncommitted for most of its working life and a red light on every ordinary
run is one a session learns to click past.

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
    return full_sha(sha, repo, cache) is not None


def full_sha(sha, repo, cache):
    """The 40-character object a stamp names, or None.

    Resolving rather than merely testing is what tells two spellings of one
    commit apart from two commits. `23cbd2e` and `23cbd2e24` in the same row
    used to read as two stamps and switch that row's drift check off — and a
    ledger repaired by hand is exactly where mixed abbreviations occur, as
    pull request #49 did across seven rows.
    """
    key = (repo, sha)
    if key not in cache:
        code, out = git(["rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}"], repo)
        cache[key] = out.strip() if code == 0 and out.strip() else None
    return cache[key]


def commit_time(sha, repo, cache):
    """Committer timestamp, for ordering two stamps git cannot rank."""
    key = (repo, sha, "time")
    if key not in cache:
        code, out = git(["show", "-s", "--format=%ct", sha], repo)
        cache[key] = int(out.strip()) if code == 0 and out.strip() else 0
    return cache[key]


def widest_baseline(shas, repo, cache):
    """The candidate whose diff window to HEAD is widest.

    Ancestry decides it where git can: an ancestor's diff to HEAD contains the
    descendant's, so it can only report MORE drift, and more is the safe
    direction for a row nobody can disambiguate. Where neither reaches the
    other the committer date is the fallback — a proxy, and named as one.
    """
    best = shas[0]
    for sha in shas[1:]:
        if git(["merge-base", "--is-ancestor", sha, best], repo)[0] == 0:
            best = sha
        elif git(["merge-base", "--is-ancestor", best, sha], repo)[0] != 0:
            if commit_time(sha, repo, cache) < commit_time(best, repo, cache):
                best = sha
    return best


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

    **The first citing row is the bound, and the 2000-character cap is only a
    backstop for a ledger that has none.** The cap used to run first and the
    cut second, which made the cut dead on any ledger whose first citing row
    sits past 2000 — measured on two of the three files it was written for:
    `.specseal/map.md` capped at 2000 with its first citing row at char 3732,
    `templates/map.md` capped, and only the fragment actually cut. Reversing
    the order alone was not enough, because the cap then truncated the cut
    result and the declaration could still fall outside it: this change grew
    `.specseal/map.md`'s header by roughly 800 characters, and its `Baseline`
    row sits at char 753, so another 1250 above it would push the declaration
    out of the window and the fallback would vanish while the run printed the
    same line as a healthy file.

    So the cap applies only where no citing row was found. There is nothing to
    check in such a ledger anyway, and the cap here is a guard against reading
    a whole file that never declares a header at all.

    This function bounds where the header ENDS. What is read inside it is
    `find_baseline`'s business, and that is where the 2000-character bound on
    accidental prose now lives — a declaration is searched for across the
    whole header, a prose SHA only near the top.
    """
    at, found = 0, False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("|") and COORD_RE.search(line):
            found = True
            break
        at += len(line)
    return text[:at] if found else text[:2000]


def find_baseline(text, repo, cache=None, source=None):
    """First plausible commit SHA in the ledger's header that exists in repo.

    A fragment declares no baseline, so a commit its PROSE names becomes the
    whole file's — which happened twice on the first fragment written here,
    the second time in the paragraph explaining the first. The answer is to
    read it and say so rather than to refuse it: `source` comes back with
    `a Baseline row` or `header prose`, and the run prints which. Refusing a
    header SHA outside a labelled row would break a ledger whose header writes
    a bare one, and its failure direction is the quiet one — such a ledger
    loses its fallback while printing the same line as a healthy file.

    **Two passes, and only the second is bounded.** A DECLARED baseline is
    deliberate, so it is looked for across the whole header however long that
    header has grown — the earlier single pass cut the search at 2000
    characters and a declaration pushed past it vanished silently. Prose is
    accidental, so the fallback pass keeps the 2000-character bound: a
    rationale paragraph 2500 characters into a fragment header had otherwise
    become that file's baseline, and the header baseline is what every row the
    derivation cannot anchor falls back to. An honest UNMEASURED turning into
    a measurement against whatever commit an argument mentioned is the quiet
    direction, and the bound is what keeps it out.
    """
    cache = {} if cache is None else cache
    header = header_of(text)

    def declared(line):
        return line.lstrip().startswith("|") and "aseline" in line

    for line in header.splitlines():
        if not declared(line):
            continue
        for m in SHA_RE.finditer(line):
            if is_commit(m.group(0), repo, cache):
                if source is not None:
                    source.append("a Baseline row")
                return m.group(0)
    for m in SHA_RE.finditer(header[:2000]):
        if is_commit(m.group(0), repo, cache):
            if source is not None:
                source.append("header prose")
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
            #
            # `filename` is NOT emitted for every line. Git suppresses the
            # whole metadata block for a commit it has already printed, so in
            # a ledger of forty lines written by five commits only five blocks
            # carry one — measured on this repository's own fragment, where
            # line 1 has a block and line 2 has a bare header. A reader that
            # expects `filename` beside each header therefore finds it for the
            # first line of each commit and nothing else, so the path is
            # remembered per commit and only the working-tree path is assumed
            # when git named none.
            names, sha, orig, final = {}, None, None, None
            for line in out.splitlines():
                head = re.match(r"^([0-9a-f]{40}) (\d+) (\d+)", line)
                if head:
                    sha, orig = head.group(1), int(head.group(2))
                    final = int(head.group(3))
                    if sha != "0" * 40:
                        found[final] = (sha, orig, names.get(sha, rel))
                    continue
                if sha and line.startswith("filename "):
                    # The block belongs to the header just read, so the entry
                    # to correct is that one. `orig` is 1-based, so the guard
                    # this used to carry was never false, and walking every
                    # recorded row to find the one just added was O(rows) for
                    # a lookup already in hand.
                    names[sha] = line[len("filename ") :]
                    if sha != "0" * 40 and final in found:
                        found[final] = (sha, orig, names[sha])
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


def row_stamps(text, pos, repo, cache):
    """Every DISTINCT resolvable stamp written in the row at `pos`, in order.

    A coordinate is blanked before the scan, because a directory named like a
    short SHA sits in the same row and must not be read as one. The filler is
    NUL rather than a space: a space is what `STAMP_RE` accepts between a date
    and a hex word, so collapsing a row that reads `2026-01-01` then a
    coordinate under `x/deadbeef1.py` then `cafe1234` to one space
    manufactured a stamp out of a date and a hex word that were never beside
    each other. NUL is not whitespace, so nothing joins across it.

    The list is returned rather than the first hit because the first hit is
    not obviously the author's. The scan reads the physical row, so a stamp in
    any earlier cell wins over the one in `Checked` — and `Verified behavior`,
    free prose where this repository's fragments do name commits, sits before
    it. Rather than guess, `check_ledger` measures from the widest of them and
    says the row is ambiguous.

    **Distinct means a distinct COMMIT, not a distinct string.** Two
    abbreviations of one commit agree perfectly, and reading them as two
    disagreeing stamps switched that row's drift check off. A ledger repaired
    by hand is where mixed lengths occur — pull request #49 rewrote stamps
    across seven rows. The matched spelling is what comes back, so a caller
    comparing against what the author typed still sees it.
    """
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    line = text[start:] if end == -1 else text[start:end]
    line = COORD_RE.sub("\x00", line)
    out, seen = [], set()
    for m in STAMP_RE.finditer(line):
        oid = full_sha(m.group(1), repo, cache)
        if oid and oid not in seen:
            seen.add(oid)
            out.append(m.group(1))
    return out


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
    stamps = row_stamps(text, pos, repo, cache)
    if stamps:
        return stamps[0]
    if ledger is not None and root is not None and repo == root:
        blame = {} if blame is None else blame
        rel = os.path.relpath(ledger, root)
        anchor = blame_lines(root, rel, blame).get(text.count("\n", 0, pos) + 1)
        if anchor:
            # The path git knew this line by AT the anchor commit, not the one
            # the file has now. `git log -L <n>,<n>:<path> <sha>` resolves the
            # path inside `<sha>`, so handing it today's name after a rename
            # is `fatal: There is no path ... in the commit`, rc 128 — and the
            # row then measured from nothing and printed `ok`. Executed: a
            # ledger renamed after its row drifted went from `1 drifted`/exit 1
            # to `1 ok`/exit 0, which turned that file's drift check off.
            sha = first_appearance(root, anchor[2], anchor[0], anchor[1], blame)
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
    ledger,
    root,
    maps,
    cache,
    default_repo=None,
    sha_cache=None,
    blame=None,
    source=None,
):
    sha_cache = {} if sha_cache is None else sha_cache
    blame = {} if blame is None else blame
    with open(ledger, encoding="utf-8", errors="replace") as f:
        text = f.read()
    baseline = find_baseline(text, root, sha_cache, source)
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
        # Two distinct stamps in one row: the scan reads the physical row, so
        # the winner would be whichever cell came first rather than the
        # author's. Saying so is right; SKIPPING the comparison was not — it
        # turned a genuinely drifted row into a passing run, because adding a
        # second stamp anywhere in the row jumped straight past the drift
        # check. Measured: one stamp gave DRIFTED and exit 1, the same row
        # plus a stamp in an earlier cell gave AMBIGUOUS and exit 0.
        #
        # So the row is measured from the WIDEST candidate — the one that can
        # only report more drift — and the ambiguity is carried in the message
        # rather than in place of the verdict.
        written = row_stamps(text, m.start(), repo, sha_cache)
        ambiguous = written[
            1:
        ] and f" · row carries {len(written)} stamps: " + ", ".join(
            s[:9] for s in written
        )
        if ambiguous:
            base = widest_baseline(written, repo, sha_cache)
        else:
            # A row is measured from the commit it first appeared in — or a
            # stamp it wrote. The header baseline is the fallback for the rows
            # neither can answer for.
            base = row_baseline(
                text, m.start(), repo, sha_cache, ledger=ledger, root=root, blame=blame
            )
        base = base or (
            baseline
            if repo == root
            else (default_baseline if repo == default_repo else None)
        )
        if not base:
            # Nothing to measure from, which is NOT the same as measured and
            # found untouched. `OK` used to be appended here unconditionally,
            # so a row nobody had committed yet was indistinguishable from a
            # row that had been compared — and a fragment spends most of its
            # working life uncommitted.
            findings.append(("UNMEASURED", coord, "no baseline — nothing was compared"))
            continue
        key = (repo, base, rel)
        if key not in cache:
            cache[key] = changed_ranges(repo, base, rel)
        if overlaps(start, end, cache[key]):
            findings.append(
                (
                    "DRIFTED",
                    coord,
                    f"touched since {base[:9]} — re-verify" + (ambiguous or ""),
                )
            )
            continue
        if ambiguous:
            findings.append(
                ("AMBIGUOUS", coord, f"measured from {base[:9]}, untouched" + ambiguous)
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
    ap.add_argument(
        "--strict",
        action="store_true",
        help="drift, and rows nothing could be measured for, also fail",
    )
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

    totals = {
        "OK": 0,
        "DRIFTED": 0,
        "BROKEN": 0,
        "EXTERNAL": 0,
        "UNMEASURED": 0,
        "AMBIGUOUS": 0,
    }
    cache, sha_cache, blame = {}, {}, {}
    for ledger in ledgers:
        source = []
        baseline, findings = check_ledger(
            ledger, root, maps, cache, default_repo, sha_cache, blame, source
        )
        rel_ledger = os.path.relpath(ledger, root)
        # A fragment carries no header baseline on purpose — every row in it
        # measures from its own line's history. Saying "skipped" there would
        # report the working case as the broken one, and the two have to be
        # told apart: nothing measures from anything only when the history
        # walk is silent too, which is a ledger git has never seen.
        if baseline:
            # WHERE it came from, because a fragment declares none and a
            # commit its prose happens to name is read all the same.
            base_note = f"{baseline[:9]} from {source[0] if source else 'the header'}"
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
            f"{sum(1 for s, _, _ in findings if s == 'EXTERNAL')} external · "
            f"{sum(1 for s, _, _ in findings if s == 'UNMEASURED')} unmeasured · "
            f"{sum(1 for s, _, _ in findings if s == 'AMBIGUOUS')} ambiguous"
        )

    print(
        f"\ntotal: {totals['OK']} ok · {totals['DRIFTED']} drifted · "
        f"{totals['BROKEN']} broken · {totals['EXTERNAL']} external · "
        f"{totals['UNMEASURED']} unmeasured · {totals['AMBIGUOUS']} ambiguous"
    )
    if totals["BROKEN"]:
        return 2
    if totals["DRIFTED"] and args.strict:
        return 2
    if totals["DRIFTED"]:
        return 1
    # UNMEASURED and AMBIGUOUS print and pass. A fragment is uncommitted for
    # most of its working life, so failing on it would put a red light in
    # front of a session on every ordinary run — one it would learn to click
    # past, which is how a real finding gets missed. `--strict` is where a
    # release asks for the stricter reading.
    if (totals["UNMEASURED"] or totals["AMBIGUOUS"]) and args.strict:
        return 2
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
