#!/usr/bin/env python3
"""Does every signatory still agree with the pact? Run at the pact's repository.

Issue #647. A work item that commits in more than one repository, where those
repositories keep a contract together, keeps the one copy of that contract in
`seal/pact.md` in one of them -- the pact's repository -- and every repository
of the work item is a signatory (`docs/the-pact.md`). A signatory cites the
clauses it was built against as pact anchors,

  pact:<name>/"<heading path>"@<hash>

in its specs' Grounding and in its ledger rows. This command reads every
signatory from the pact's repository and grades each of those anchors against
the clause as the pact holds it now.

  pact-check            in the pact's repository
  pact-check ROOT       the pact's repository at ROOT

**Local only.** No CI runs it: a signatory's pull request can read one
repository, and this needs all of them (#647's decision 2). What a signatory's
CI does instead is print the relationship, `chain_check.py#pact_notices`.

## Where the signatories are

The pact's `| Signatory |` table lists them by origin remote URL, and a
checkout is found for each, in this order and with nothing guessed:

  1. `~/.claude/specseal/pact-paths.md`, a `| Remote | Path |` table kept per
     machine and never committed, keyed by remote URL compared normalised;
  2. every sibling directory of the pact's repository whose origin remote
     normalises to the signatory's -- exactly one of them.

A signatory neither finds is reported with the map line to add.

## What each anchor reads

  OK          the hash matches the clause in the pact's current checkout
  SUPERSEDED  it does not, and a commit in HEAD's own history of the pact
              gave the clause this hash: the signatory was built against a
              superseded clause. Re-read it there and re-anchor
  NOT TAKEN   it does not, and a commit reachable from another ref but not
              from HEAD gave it this hash, named: the pact has not taken the
              signatory's recorded change. Land that ref's change, or
              reconcile
  UNMATCHED   no commit here gave the clause this hash: squashed away, or
              never a version. Read both sides
  BROKEN      the heading path resolves to no clause, or to more than one:
              renamed or removed. Re-coordinate the signatory

Git is asked one thing: which way a mismatch points. It never decides `OK`,
which is the bound `evidence-check` keeps by asking git for nothing. A pact
under local mode has no history, so every mismatch there reads `UNMATCHED`,
and the summary says so.

## Exit codes

  0  every listed signatory was read, and every anchor is `OK`
  1  a `SUPERSEDED`, `NOT TAKEN` or `UNMATCHED` anchor, or a signatory not
     found on this machine
  2  unusable input: no pact here, a pact or file that cannot be read, a
     `BROKEN` anchor, an anchor naming this pact that does not parse, a
     `Pact` row or notify value that will not parse, a relationship
     recorded on one side only, or a pact's repository with no origin
     remote

These mirror `evidence-check`'s classes, where `BROKEN` is exit 2 and drift is
exit 1. Nothing is ever written.
"""

import argparse
import glob
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "..", "..", "hooks")
CHECKER = os.path.join(HERE, "evidence_check.py")
PACT_FILE = "pact.md"
CONFIG_FILE = "config.md"
MAP = os.path.join(".claude", "specseal", "pact-paths.md")
MAP_HEADER = re.compile(r"^\|\s*Remote\s*\|\s*Path\s*\|\s*$")

OK, SUPERSEDED, NOT_TAKEN, UNMATCHED, BROKEN = (
    "OK",
    "SUPERSEDED",
    "NOT TAKEN",
    "UNMATCHED",
    "BROKEN",
)
NOT_FOUND, ONE_SIDED, REFUSED, UNREADABLE = (
    "NOT FOUND",
    "ONE-SIDED",
    "REFUSED",
    "UNREADABLE",
)
# Anything that starts like a pact anchor naming a pact, so one that does
# not parse -- `#` for `/`, no quotes, no hash -- is named rather than passed
# over. A mistyped citation is otherwise read by nobody: not here, not by the
# signatory's own check, which passes pact anchors over by design, and not by
# chain-check (round 1 of #647, yellow 4).
PACT_MENTION_RE = re.compile(r"(?<![A-Za-z0-9_.@/-])pact:(?P<name>[A-Za-z0-9_.-]+)\S*")
# Which exit each finding is: the classes `evidence-check` keeps.
EXIT_ONE = frozenset({SUPERSEDED, NOT_TAKEN, UNMATCHED, NOT_FOUND})
EXIT_TWO = frozenset({BROKEN, ONE_SIDED, REFUSED, UNREADABLE})


def load(path, name):
    """A sibling module by path, or a sentence and exit 2."""
    if not os.path.isfile(path):
        sys.stderr.write(
            f"pact-check: cannot read {path}, which this command reads the pact "
            "through. It ships in the plugin beside this script; a copy of one "
            "script taken on its own is not a plugin. Nothing was read.\n"
        )
        raise SystemExit(2)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(root, *args):
    """Git's stdout in ROOT, or None where git refused."""
    try:
        done = subprocess.run(
            ["git", "-C", root, *args],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout if done.returncode == 0 else None


def read(path):
    """The file's text, or None for one that will not read."""
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except (OSError, ValueError):
        return None


def origin(root):
    """ROOT's origin remote URL as written, or ""."""
    return (git(root, "remote", "get-url", "origin") or "").strip()


def path_map(config, home_dir):
    """({normalised remote: path}, refusal or None) from the machine-local
    map under HOME_DIR. No map is an empty one; a map that is there and will
    not read is a refusal, because reading it as empty would report every
    signatory it names as not found."""
    where = os.path.join(home_dir, MAP)
    if not os.path.lexists(where):
        return {}, None
    text = read(where)
    if text is None:
        return {}, f"{where} is there and could not be read"
    found, seen_header = {}, False
    row = re.compile(
        rf"^\|\s*(?P<remote>{config.CELL}+?)\s*\|\s*(?P<path>{config.CELL}+?)\s*\|\s*$"
    )
    for _index, line in config.unfenced(text.splitlines(), text):
        if not seen_header:
            seen_header = bool(MAP_HEADER.match(line))
            continue
        if config.CONFIG_SEPARATOR.match(line.strip()) and not found:
            continue
        match = row.match(line)
        if not match:
            break
        remote = config.normalise_remote(config.unescaped(match.group("remote")))
        found[remote] = os.path.expanduser(config.unescaped(match.group("path")))
    return found, None


def checkout(config, signatory, root, mapped):
    """(path, None) for the signatory's checkout, or (None, why not)."""
    written, normalised, _name = signatory
    if normalised in mapped:
        path = mapped[normalised]
        if not os.path.isdir(path):
            return None, f"the map names {path}, which is not a directory here"
        theirs = config.normalise_remote(origin(path))
        if theirs != normalised:
            return None, (
                f"the map names {path}, whose origin is "
                f"{theirs or 'not set'} rather than {normalised}"
            )
        return path, None
    parent = os.path.dirname(os.path.abspath(root))
    try:
        names = sorted(os.listdir(parent))
    except OSError:
        names = []
    hits = []
    for entry in names:
        path = os.path.join(parent, entry)
        if os.path.realpath(path) == os.path.realpath(root) or not os.path.isdir(path):
            continue
        if not os.path.lexists(os.path.join(path, ".git")):
            continue
        if config.normalise_remote(origin(path)) == normalised:
            hits.append(path)
    if len(hits) == 1:
        return hits[0], None
    line = f"`| {written} | <the path of its checkout> |`"
    if hits:
        return None, (
            f"{len(hits)} sibling directories have its origin ({', '.join(hits)}), "
            f"and nothing here guesses which: add {line} to ~/{MAP}"
        )
    return None, f"no checkout of it was found on this machine: add {line} to ~/{MAP}"


def anchor_files(home):
    """Every file of a signatory's root its pact anchors are read from: its
    ledger files and every work item's `spec.md`."""
    files = [os.path.join(home, "ledger.md")]
    for pattern in ("ledger/*.md", "releases/*.md", "specs/*/spec.md"):
        files.extend(sorted(glob.glob(os.path.join(home, *pattern.split("/")))))
    return [f for f in files if os.path.lexists(f)]


class History:
    """The pact file's versions, asked for lazily and once: HEAD's own
    history of it, newest first, and the commits that touched it on any
    other branch, remote-tracking branch or tag that HEAD does not hold.

    A pact under local mode sits under the git directory, a path git never
    tracked, so both lists come back empty with nothing special-cased: that is
    what makes every mismatch there `UNMATCHED`. `grade` reads HEAD's list
    before the other, so leaving HEAD's commits out of the second changes no
    verdict; it says what the list is and saves reading them twice."""

    def __init__(self, root, rel):
        self.root, self.rel = root, rel
        self._head = self._other = None
        self._texts = {}

    def commits(self, *revs):
        # `--full-history`: by default git follows only the TREESAME parent
        # of a merge, so a clause version on the side a merge did not keep
        # vanished from HEAD's list (and `--not HEAD` kept it out of the
        # other one), and its hash read UNMATCHED where SUPERSEDED is true.
        # A merge listed this way carries one parent's text, so it changes
        # no verdict.
        out = git(self.root, "rev-list", "--full-history", *revs, "--", self.rel)
        return out.split() if out else []

    def head(self):
        if self._head is None:
            self._head = self.commits("HEAD")
        return self._head

    def other(self):
        if self._other is None:
            self._other = self.commits(
                "--branches", "--remotes", "--tags", "--not", "HEAD"
            )
        return self._other

    def text(self, sha):
        if sha not in self._texts:
            self._texts[sha] = git(self.root, "show", f"{sha}:{self.rel}")
        return self._texts[sha]

    def ref_holding(self, sha):
        out = git(
            self.root,
            "for-each-ref",
            "--contains",
            sha,
            "--format=%(refname:short)",
            "refs/heads",
            "refs/remotes",
            "refs/tags",
        )
        refs = sorted(r for r in (out or "").split() if r)
        return refs[0] if refs else sha[:8]


def clause_hash(checker, text, locator):
    """(hash, None) for the clause LOCATOR names in a pact's TEXT, or
    (None, why it names none)."""
    body = checker.unescape(locator[1:-1])
    parts = [p for p in body.split(checker.HEADING_SEP) if p.strip()]
    if not parts or checker.heading_level(parts[0].strip()) is None:
        return None, "names no heading path, and a pact clause is addressed by one"
    lines = checker.gfm_lines(text)
    regions = checker.heading_path(lines, parts)
    if len(regions) != 1:
        return None, (
            "resolves to no clause in the pact"
            if not regions
            else f"resolves to {len(regions)} clauses in the pact"
        )
    start, end = regions[0]
    return checker.content_hash(lines[start - 1 : end]), None


def grade(checker, pact_text, history, locator, want):
    """(status, what to do) for one anchor."""
    current, why = clause_hash(checker, pact_text, locator)
    if current is None:
        return BROKEN, (
            f"the heading path {why}: the clause was renamed or removed. "
            "Re-coordinate the signatory"
        )
    if current == want:
        return OK, ""
    for sha in history.head():
        text = history.text(sha)
        if text is not None and clause_hash(checker, text, locator)[0] == want:
            return SUPERSEDED, (
                f"the signatory was built against a superseded clause, the one "
                f"at {sha[:8]}; it reads @{current} now. Re-read it in the "
                "signatory and re-anchor"
            )
    for sha in history.other():
        text = history.text(sha)
        if text is not None and clause_hash(checker, text, locator)[0] == want:
            return NOT_TAKEN, (
                f"the pact has not taken the signatory's recorded change: this "
                f"hash is the clause on {history.ref_holding(sha)} (at "
                f"{sha[:8]}), which HEAD does not hold. Land that ref's pact "
                "change, or reconcile"
            )
    return UNMATCHED, (
        f"no commit in this repository gave the clause this hash, and it reads "
        f"@{current} now: the version was squashed away or never existed. "
        "Read both sides"
    )


def check(root, out=sys.stdout, home_dir=None):
    """Read the pact at ROOT and every signatory; print; return the exit."""
    config = load(os.path.join(HOOKS, "config.py"), "specseal_config_for_pact")
    optin = load(os.path.join(HOOKS, "optin.py"), "specseal_optin_for_pact")
    checker = load(CHECKER, "specseal_evidence_for_pact")
    home_dir = home_dir or os.path.expanduser("~")

    def say(line):
        out.write(line + "\n")

    repo = optin.repo_root(os.path.abspath(root))
    if not repo:
        say(f"pact-check: {root} is not in a git repository — nothing was read")
        return 2
    home = optin.home_at(repo)
    pact_path = os.path.join(home, PACT_FILE) if home else ""
    if not home or not os.path.lexists(pact_path):
        say(
            f"pact-check: {repo} holds no seal/{PACT_FILE}, so there is no pact "
            "to reconcile here — run it in the repository that holds the pact"
        )
        return 2
    pact_text = read(pact_path)
    if pact_text is None:
        say(f"{UNREADABLE} {pact_path} — the pact could not be read")
        return 2
    mine = origin(repo)
    name = config.pact_name(mine)
    if not name:
        say(
            f"pact-check: {repo} has no origin remote, so the name every pact "
            "anchor carries cannot be derived — set `origin` and run it again"
        )
        return 2
    shared = optin.home_paths(repo)[0]
    local = os.path.realpath(home) != os.path.realpath(shared)
    rel = os.path.relpath(pact_path, repo).replace(os.sep, "/")
    history = History(repo, rel)

    findings = []

    def found(status, signatory, where, detail):
        findings.append(status)
        say(
            f"{status} {signatory} {where} — {detail}"
            if where
            else f"{status} {signatory} — {detail}"
        )

    signatories, refusals = config.pact_signatories(pact_text)
    for refusal in refusals:
        found(REFUSED, f"seal/{PACT_FILE}", "", f"the pact {refusal}")
    mapped, map_refusal = path_map(config, home_dir)
    if map_refusal:
        found(REFUSED, f"~/{MAP}", "", map_refusal)

    counts = dict.fromkeys((OK, SUPERSEDED, NOT_TAKEN, UNMATCHED, BROKEN), 0)
    read_count = 0
    for signatory in signatories:
        written = signatory[0]
        path, why = checkout(config, signatory, repo, mapped)
        if path is None:
            found(NOT_FOUND, written, "", why)
            continue
        their_home = optin.home_at(optin.repo_root(path) or path)
        if not their_home:
            found(
                ONE_SIDED,
                written,
                path,
                "the pact lists it, and it has no seal/ root to name this pact "
                "in: the relationship is recorded on one side only",
            )
            continue
        declared = config.declared_pacts(their_home)
        if declared is None:
            found(
                UNREADABLE,
                written,
                f"{their_home}/{CONFIG_FILE}",
                "could not be read",
            )
            continue
        pacts, notify, row_refusals = declared
        for refusal in row_refusals:
            found(REFUSED, written, f"seal/{CONFIG_FILE}", refusal)
        if not any(n == config.normalise_remote(mine) for _w, n, _ in pacts):
            found(
                ONE_SIDED,
                written,
                f"seal/{CONFIG_FILE}",
                f"the pact lists it, and its config names no `{config.PACT_ROW}` "
                f"row for {mine}: the relationship is recorded on one side "
                f"only. Add `| {config.PACT_ROW} | {mine} |` there, or take it "
                "out of the pact's `Signatory` table",
            )
            continue
        read_count += 1
        anchors = 0
        for file_path in anchor_files(their_home):
            body = read(file_path)
            shown = os.path.relpath(file_path, path).replace(os.sep, "/")
            if body is None:
                found(UNREADABLE, written, shown, "could not be read")
                continue
            view = checker.unquoted(body)
            for match in checker.PACT_ANCHOR_RE.finditer(view):
                if match.group("name").lower() != name:
                    continue
                anchors += 1
                status, detail = grade(
                    checker,
                    pact_text,
                    history,
                    match.group("locator"),
                    match.group("hash"),
                )
                counts[status] += 1
                if status != OK:
                    line = view.count("\n", 0, match.start()) + 1
                    found(status, written, f"{shown}:{line} {match.group(0)}", detail)
            graded = {m.start() for m in checker.PACT_ANCHOR_RE.finditer(view)}
            for near in PACT_MENTION_RE.finditer(view):
                if near.group("name").lower() != name or near.start() in graded:
                    continue
                line = view.count("\n", 0, near.start()) + 1
                found(
                    REFUSED,
                    written,
                    f"{shown}:{line}",
                    f"`{near.group(0)}` does not parse as "
                    f'`pact:{name}/"<heading path>"@<hash>`, so nothing grades '
                    "it. Quote the heading path and give it a hash, `@00000000` "
                    "until the first report names the real one",
                )
        say(
            f"READ {written} {path} — `{config.PACT_NOTIFY_ROW}`: "
            f"{notify or 'will not parse'}; {anchors} pact anchor"
            f"{'' if anchors == 1 else 's'} naming `{name}`"
        )

    summary = (
        f"pact-check: the pact `{name}` — {read_count} of {len(signatories)} "
        f"signator{'y' if len(signatories) == 1 else 'ies'} read · "
        + " · ".join(f"{counts[s]} {s.lower()}" for s in counts)
    )
    if local:
        summary += (
            ". The pact sits under the git directory (local mode), so it has no "
            "history and every mismatch reads unmatched"
        )
    say(summary)
    if any(status in EXIT_TWO for status in findings):
        return 2
    if any(status in EXIT_ONE for status in findings):
        return 1
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="pact-check",
        description="At the pact's repository: does every signatory still "
        "agree with the pact?",
    )
    ap.add_argument(
        "root",
        nargs="?",
        default=".",
        help="the pact's repository (default: the current directory)",
    )
    args = ap.parse_args(argv)
    return check(args.root)


if __name__ == "__main__":
    for _name, _errors in (("stdout", "replace"), ("stderr", "backslashreplace")):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main())
