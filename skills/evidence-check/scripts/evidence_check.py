#!/usr/bin/env python3
"""evidence_check — does the evidence ledger still point at what it claims?

Scans the spec-to-code map (default: .specseal/map.md, .specseal/map/*.md,
and the pre-0.10 docs/**/_evidence.md) for coordinates of the form

    path#anchor@hash

and classifies each:

  BROKEN   the anchor is not in the file, or is in it more than once
  DRIFTED  the anchor is there and the content under it has changed
  OK       the anchor is there and the content is what the row recorded
  EXTERNAL path not in this repo and no --map given — cannot judge here

**A coordinate names a place by content, never by position.** A line number
moves for edits that have nothing to do with the claim, so a coordinate made of
one rots on contact: the row gets re-anchored, which resets whatever the row
was measured from, which needs a stamp, which a squash then orphans. Every one
of those mechanisms was compensation for the line number, and none of them is
here. There is no baseline, no stamp, no commit SHA, and the CHECK asks git
for nothing — the single exception is `--migrate`, a one-shot writer that may
consult the old stamp's commit before trusting a recorded line number, and
`content_at` says why that is a different act.

The anchor is a **symbol name** where the language offers one — `.py` is read
with the stdlib `ast`, so `Class.method` names a span exactly and no dependency
is added — and otherwise a **distinctive line of text**, quoted, which works in
any language. The hash covers the anchored region with trailing whitespace and
blank lines removed, so reformatting is not a change and reindenting is: in
Python indentation carries meaning, and a checker that shrugged at a dedent
would go quiet exactly where it should complain.

Exit codes: 0 clean · 1 drift only · 2 broken coordinates (or drift with
--strict). Designed for CI: a spec-code link that stops resolving should fail
the build the same way a broken test does.

Usage:
  evidence_check.py [--ledger GLOB]... [--map NAME=PATH]... [--strict] [ROOT]
  evidence_check.py --reverify [ROOT]     rewrite the hash of every resolvable
                                          row — an explicit "I have re-read
                                          these", never something a check does

--map resolves cross-repo coordinates (e.g. a migration's original repo):
  a coordinate `legacy-api/src/service.py#handler@a1b2c3d` with
  --map legacy-api=~/work/legacy-api is checked inside that checkout.
"""

import argparse
import ast
import glob
import hashlib
import os
import re
import subprocess
import sys
import tempfile

# `path#anchor@hash`. The anchor is either a dotted symbol name or a quoted
# line of text; `\|` inside the quotes is an escaped pipe, so a row anchored to
# a markdown table line does not split the table it lives in.
ANCHOR_RE = re.compile(
    r"(?P<path>[A-Za-z0-9_@.][A-Za-z0-9_.@/-]*[/.][A-Za-z0-9_.@/-]*?)"
    r"#(?P<locator>\"(?:[^\"\n]|\\\")+\"|[A-Za-z_][A-Za-z0-9_.]*)"
    r"(?:>(?P<claim>\"(?:[^\"\n]|\\\")+\"))?"
    r"@(?P<hash>[0-9a-f]{6,12})"
)
HASH_LEN = 8
# The old, pre-anchor coordinate shape — `path:line`, `path:start-end`. Nothing measures
# from these any more, and the one unacceptable outcome is silence: a ledger
# full of them once read `0 ok · 0 drifted · 0 broken`, exit 0, which stripped
# an updating user's whole coverage without one printed word.
OLD_COORD_RE = re.compile(
    r"(?P<path>[A-Za-z0-9_@.][A-Za-z0-9_.@/-]*[/.][A-Za-z0-9_.@/-]*?)"
    r":(?P<start>\d+)(?:-(?P<end>\d+))?\b"
)
OLD_STAMP_RE = re.compile(r"(\b\d{4}-\d{2}-\d{2})\s+`?[0-9a-f]{7,40}`?")
STAMP_SHA_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\s+`?(?P<sha>[0-9a-f]{7,40})`?")
# `example.com:8080` in a URL has the old coordinate shape exactly; the
# line-number checker learned this the same way, from ledgers citing links.
URL_HOST_RE = re.compile(r"(?://|\bhttps?:)[^\s)\]<>\"']*$")
# A claim region never runs longer than this. A claim needing more lines than
# this is a claim about the whole function, and the row should drop the claim
# anchor and locate alone rather than pretend to a narrower subject.
CLAIM_CAP = 12


def normalise(lines):
    """The region as the hash sees it.

    Trailing whitespace goes and blank lines go, so a reformat that only moves
    those is not a change. **Leading whitespace stays**: in Python indentation
    decides what a statement belongs to, and a hash that ignored it would call
    a dedent no change at all — a checker going quiet exactly where the edit
    matters most.
    """
    return "\n".join(line.rstrip() for line in lines if line.strip())


def content_hash(lines):
    return hashlib.sha256(normalise(lines).encode("utf-8")).hexdigest()[:HASH_LEN]


def py_spans(text):
    """{qualified name: [(start, end)]} for defs, classes and constants — or
    None for a file that will not parse.

    Decorators are part of the span: a decorator carries behaviour, and a row
    anchored to the function it decorates should notice one being added or
    removed. A module- or class-level assignment is a unit too — this
    repository's own ledger cites three constants — and its span is the whole
    statement, multi-line value included. An assignment inside a function is a
    local, not a unit, and is not collected.

    None rather than `{}` for a SyntaxError, because the two callers diverge
    on exactly that: a file that cannot be parsed falls back to the generic
    text rule, while a file that parses and simply lacks the symbol is
    BROKEN. Conflating the two anchored rows to leftover call sites, and
    `--reverify` then made the wrong anchor permanent (round 4, 🔴 2).
    """
    out = {}
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None

    def walk(node, prefix, in_function):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = prefix + child.name
                start = min([child.lineno] + [d.lineno for d in child.decorator_list])
                out.setdefault(name, []).append((start, child.end_lineno))
                walk(child, name + ".", not isinstance(child, ast.ClassDef))
            elif isinstance(child, (ast.Assign, ast.AnnAssign)) and not in_function:
                targets = (
                    child.targets if isinstance(child, ast.Assign) else [child.target]
                )
                for t in targets:
                    elts = t.elts if isinstance(t, (ast.Tuple, ast.List)) else [t]
                    for n in elts:
                        if isinstance(n, ast.Name):
                            out.setdefault(prefix + n.id, []).append(
                                (child.lineno, child.end_lineno)
                            )
            else:
                walk(child, prefix, in_function)

    walk(tree, "", False)
    return out


def heading_level(line):
    m = re.match(r"^(#{1,6})\s", line)
    return len(m.group(1)) if m else None


def text_regions(lines, anchor, markdown=False):
    """Every region a text anchor matches, 1-based and inclusive.

    A markdown heading owns everything down to the next heading at its level or
    above, which is what a reader means by a section. Anything else owns the
    contiguous run of non-blank lines it sits in — a paragraph, a table, a
    block of code.

    **The heading rule is markdown-only.** `#` opens a comment in Python, shell
    and YAML, and reading one as a heading made a 23-line comment block resolve
    to its first line alone. Found by migrating this repository's own ledger,
    not by reasoning about it.
    """
    want = " ".join(anchor.split())
    out = []
    for i, line in enumerate(lines):
        if " ".join(line.split()) != want:
            continue
        level = heading_level(line) if markdown else None
        if level is not None:
            j = i + 1
            while j < len(lines):
                k = heading_level(lines[j])
                if k is not None and k <= level:
                    break
                j += 1
            out.append((i + 1, j))
        else:
            a = b = i
            while a > 0 and lines[a - 1].strip():
                a -= 1
            while b + 1 < len(lines) and lines[b + 1].strip():
                b += 1
            out.append((a + 1, b + 1))
    return out


def unescape(anchor):
    """The anchor as written in the file it points at."""
    return anchor.replace("\\|", "|").replace('\\"', '"')


HEADING_SEP = " / "


def heading_path(lines, parts):
    """[(start, end)] for a `## A / ### B` heading path in a markdown file.

    Each part narrows inside the section the previous one opened, so a heading
    that repeats across a document is disambiguated by its parent rather than
    by a line number. Zero matches or several is the caller's BROKEN.
    """
    regions = [(1, len(lines))]
    for part in parts:
        want = " ".join(part.split())
        found = []
        for lo, hi in regions:
            for i in range(lo - 1, hi):
                if " ".join(lines[i].split()) != want:
                    continue
                level = heading_level(lines[i])
                if level is None:
                    continue
                j = i + 1
                while j < hi:
                    k = heading_level(lines[j])
                    if k is not None and k <= level:
                        break
                    j += 1
                found.append((i + 1, j))
        regions = found
        if not regions:
            return []
    return regions


def resolve(path, locator, text):
    """[(start, end)] for the LOCATOR — empty for none, several for ambiguous.

    **A coordinate's job is to put a reader in the right logic, not to pin a
    line.** So the address is the enclosing unit: the function for code, the
    heading for a document. That unit is stable against every edit that does
    not change what the unit IS, which is the whole property being bought.

    **An anchor degrades to DRIFTED, never to BROKEN.** The two cost different
    things. BROKEN says *I cannot find it, go edit the ledger*, which is the
    bookkeeping this design exists to remove; DRIFTED says *it changed, go
    re-read the claim*, which is the work the ledger exists for. Every case
    below is decided by that, and so are the ones nobody has thought of yet.

    It is why a markdown locator is a heading path rather than a sentence. A
    sentence anchor breaks on any rewording — eleven rows here pointed at one
    — while a heading is the document's own structure and survives its prose
    being rewritten. The hash still reports the prose changing, so the row
    still says re-read this; it just stops saying go fix the ledger.
    """
    lines = text.splitlines()
    markdown = path.endswith(".md")
    if locator.startswith('"'):
        body = unescape(locator[1:-1])
        if markdown:
            parts = [p for p in body.split(HEADING_SEP) if p.strip()]
            if parts and heading_level(parts[0].strip()) is not None:
                return heading_path(lines, parts)
        return text_regions(lines, body, markdown)
    if path.endswith(".py"):
        spans = py_spans(text)
        if spans is not None:
            # The parse succeeded, so ast's answer is the whole answer: a
            # symbol it cannot find is GONE. Falling back to the text rule
            # here read a leftover call site as the unit — a moved function
            # reported DRIFTED instead of BROKEN-with-hint, and --reverify
            # anchored the row to the call permanently (round 4, 🔴 2). The
            # fallback survives only for the file ast cannot read at all.
            return spans.get(locator, [])
    return generic_units(lines, locator)


# Words that BEGIN a statement and can be followed directly by a call —
# `return render(y);`, `await render(y)`, `if render(x):`. Any of them in the
# text before the name makes the line a use rather than a declaration.
STATEMENT_WORDS = frozenset(
    [
        "return",
        "raise",
        "throw",
        "yield",
        "await",
        "assert",
        "case",
        "match",
        "if",
        "elif",
        "while",
        "with",
        "switch",
        "do",
        "else",
        "new",
        "not",
        "and",
        "or",
        "in",
        "of",
        "until",
        "unless",
        "when",
    ]
)


def generic_units(lines, name):
    """[(start, end)] for `name`'s declaration block, without any parser.

    The `ast` path exists for `.py` only, and a project adopting this skill is
    mostly code that is not Python. Falling back to text anchors there would
    hand those projects the brittle version of this design, so the major level
    has a rule that needs no parser and no dependency.

    A declaration is the name followed by `(`, `{`, `:` or `=`. The block runs
    to the next line at the same or lower indentation, which closes a suite in
    an indentation language and lands on the closing brace in a brace
    language, because that brace sits at the declaration's own indent.

    `=` is in that list because a module-level constant is a unit too, and a
    common one to cite — this plugin's own ledger cites three. Without it every
    constant in every adopting project falls to a literal text anchor, which is
    the brittle form this rule exists to avoid. A multi-line value comes along,
    since its continuation lines are indented past the name.

    It is coarser than a parser and that is the trade. Where it cannot resolve
    a unit the answer is BROKEN and a person looks — loud and honest beats a
    per-language parser nobody maintains.
    """
    out = []
    # What may sit before the name on a declaration line: keywords and
    # modifiers, nothing else. `x = f(` is already blocked because `=` cannot
    # appear in `pre`; `if v not in NAME:` is why the colon is stricter still.
    # Statement keywords are blocked by name: `return render(y);` is the
    # commonest shape in every brace language, and reading it as a second
    # declaration made a one-declaration-one-call file BROKEN-ambiguous
    # (round 4, 🔴 1). The list names the USES because declaration modifiers
    # (`export`, `static`, `async`, `def`, ...) are unbounded across
    # languages, and a wrong entry here fails loud — a declaration whose
    # modifier matched would report BROKEN — never silent.
    esc = re.escape(name)
    opener = re.compile(r"^(?P<pre>[\w\s*&]*?)\b" + esc + r"\s*(?P<delim>[({=]|:)")
    for i, line in enumerate(lines):
        m = opener.match(line)
        if not m:
            continue
        pre_words = m.group("pre").replace("*", " ").replace("&", " ").split()
        if STATEMENT_WORDS.intersection(pre_words):
            continue  # `return render(y);` is a use, not a declaration
        if m.group("delim") == ":" and m.group("pre").strip():
            continue  # `if v not in NAME:` is a use, not a declaration
        indent = len(line) - len(line.lstrip())
        j = i + 1
        while j < len(lines):
            nxt = lines[j]
            if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= indent:
                break
            j += 1
        while j > i + 1 and not lines[j - 1].strip():
            j -= 1
        out.append((i + 1, j))
    return out


def name_statements(text, region, name):
    """[(start, end)] for the innermost statements in `region` referencing `name`.

    The minor level is resolved by what a statement REFERENCES — the call it
    makes, the name it assigns, the exception it handles — rather than by the
    characters of its line. Renaming a local on that line then changes nothing;
    renaming the thing it calls does, and widening to the unit with a DRIFTED
    is the right answer there too.
    """
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    lo, hi = region
    hits = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.stmt):
            continue
        if not (lo <= node.lineno and (node.end_lineno or node.lineno) <= hi):
            continue
        if any(
            (isinstance(x, ast.Name) and x.id == name)
            or (isinstance(x, ast.Attribute) and x.attr == name)
            or (
                isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and x.name == name
            )
            for x in ast.walk(node)
        ):
            hits.append(node)
    inner = [
        n
        for n in hits
        if not any(
            m is not n
            and n.lineno <= m.lineno
            and (m.end_lineno or m.lineno) <= (n.end_lineno or n.lineno)
            for m in hits
        )
    ]
    return sorted({(n.lineno, n.end_lineno or n.lineno) for n in inner})


def literal_statements(lines, region, literal):
    """[(start, end)] for lines in `region` containing `literal` — last resort.

    For a claim about a bare `return`, a constant or a literal, where there is
    no referenced name to identify the place by.
    """
    want = " ".join(literal.split())
    lo, hi = region
    hits = [
        n for n in range(lo, hi + 1) if want and want in " ".join(lines[n - 1].split())
    ]
    if len(hits) != 1:
        return [(n, n) for n in hits]
    at = hits[0]
    indent = len(lines[at - 1]) - len(lines[at - 1].lstrip())
    last = at
    while last < hi and last - at + 1 < CLAIM_CAP:
        nxt = lines[last]
        if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= indent:
            break
        last += 1
    while last > at and not lines[last - 1].strip():
        last -= 1
    return [(at, last)]


def minor_region(path, text, region, minor):
    """[(start, end)] inside `region`, or [] when the minor anchor is stale.

    **An empty answer is not BROKEN.** The minor level narrows what is hashed;
    it never decides whether the row resolves. A minor anchor that stopped
    matching means that place changed, and *it changed, go re-read* is the
    honest report — so the caller widens to the major unit and says DRIFTED.
    Reporting BROKEN here would send somebody to edit the ledger, which is the
    bookkeeping this design exists to remove.

    Ambiguity widens for the same reason: several matches is not a place.
    """
    lines = text.splitlines()
    if minor.startswith('"'):
        found = literal_statements(lines, region, unescape(minor[1:-1]))
    elif path.endswith(".py"):
        found = name_statements(text, region, minor)
    else:
        found = literal_statements(lines, region, minor)
    return found if len(found) == 1 else []


SCAN_FILE_CAP = 200
SCAN_SIZE_CAP = 256 * 1024


def file_units(rel, body):
    """[(spelling, (start, end))] — every unit in one file, resolvable ones only."""
    lines = body.splitlines()
    units = []
    if rel.endswith(".py"):
        for name, places in (py_spans(body) or {}).items():
            if len(places) == 1:
                units.append((name, places[0]))
    elif rel.endswith(".md"):
        seen = {}
        for i, line in enumerate(lines):
            level = heading_level(line)
            if level is None:
                continue
            j = i + 1
            while j < len(lines):
                k = heading_level(lines[j])
                if k is not None and k <= level:
                    break
                j += 1
            name = '"' + line.strip().replace("|", "\\|").replace('"', '\\"') + '"'
            seen.setdefault(name, []).append((i + 1, j))
        units = [(n, p[0]) for n, p in seen.items() if len(p) == 1]
    else:
        opener = re.compile(r"^([\w\s*&]*?)\b(\w+)\s*([({=]|:)")
        names = set()
        for line in lines:
            m = opener.match(line)
            if m and not (m.group(3) == ":" and m.group(1).strip()):
                names.add(m.group(2))
        for name in sorted(names):
            found = generic_units(lines, name)
            if len(found) == 1:
                units.append((name, found[0]))
    return units


def scan_candidates(repo, rel, cache):
    """(other files worth scanning, capped?) for a broken row in `rel`.

    Built lazily — only a BROKEN row pays for this — and bounded twice, so the
    clean path stays the ~114 ms tool it just became: files over
    SCAN_SIZE_CAP are skipped, and past SCAN_FILE_CAP the scan degrades to
    the row's own file and the caller says so out loud. A silently narrowed
    search reads as a search that found nothing.

    Same extension only: a unit that moved kept its language.
    """
    ext = os.path.splitext(rel)[1]
    key = (repo, ext)
    if key not in cache:
        found, capped = [], False
        for dirpath, dirnames, filenames in os.walk(repo):
            dirnames[:] = sorted(d for d in dirnames if d != ".git")
            for fn in sorted(filenames):
                if os.path.splitext(fn)[1] != ext:
                    continue
                full = os.path.join(dirpath, fn)
                try:
                    if os.path.getsize(full) > SCAN_SIZE_CAP:
                        continue
                except OSError:
                    continue
                found.append(os.path.relpath(full, repo).replace(os.sep, "/"))
                if len(found) > SCAN_FILE_CAP:
                    capped = True
                    break
            if capped:
                break
        cache[key] = (found, capped)
    files, capped = cache[key]
    return [f for f in files if f != rel], capped


def content_matches(repo, rel, locator, want, cache):
    """(hash matches, name matches, capped) for a row whose locator is gone.

    Graded evidence, because the parts of an anchor discriminate with
    different strength. **A unit's name is part of its own hashed region** —
    `def handler(x):` is the first line of `handler`'s content — so the hash
    comparison RECONSTRUCTS: substitute a candidate's name with the row's
    locator throughout its region, hash that, compare with what the row
    RECORDED. A pure rename or a clean move then reconstructs the old region
    exactly; content that also changed reconstructs nothing.

    A name match with different content is a weaker fact and is returned
    separately: `main`, `resolve` and `check` collide across files as a
    matter of course, so a name alone must never fix anything.
    """
    markdown = rel.endswith(".md")
    old_name = unescape(locator[1:-1]) if locator.startswith('"') else locator
    old_last = old_name.rsplit(".", 1)[-1]
    if markdown:
        # A heading-PATH locator's recorded region starts at its LAST part's
        # heading line, not at the whole path string — substituting the whole
        # path made the parent-qualified form the one form that could never
        # be healed (round 4, 🟡 8).
        parts = [p for p in old_name.split(HEADING_SEP) if p.strip()]
        if len(parts) > 1 and heading_level(parts[0].strip()) is not None:
            old_name = parts[-1].strip()

    others, capped = scan_candidates(repo, rel, cache)
    hash_matches, name_matches = [], []
    for path in [rel, *([] if capped else others)]:
        body = read(os.path.join(repo, path))
        if body is None:
            continue
        lines = body.splitlines()
        for name, (a, b) in file_units(path, body):
            region = lines[a - 1 : b]
            if markdown:
                region = [old_name, *region[1:]]
            else:
                new_last = name.rsplit(".", 1)[-1]
                sub = re.compile(r"\b" + re.escape(new_last) + r"\b")
                region = [sub.sub(old_last, line) for line in region]
            if content_hash(region) == want:
                hash_matches.append((path, name, (a, b)))
            elif name == locator and path != rel:
                name_matches.append((path, name, (a, b)))
    return hash_matches, name_matches, capped


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def write_atomic(path, text):
    """Write-then-rename, never truncate-then-write.

    A crash mid-write used to leave a torn ledger whose only recovery was the
    session-start hook's committed baseline (round 4, 🟡 14). The temp file
    lands in the ledger's own directory so the rename never crosses a
    filesystem.
    """
    fd, tmp = tempfile.mkstemp(
        dir=os.path.dirname(path) or ".", prefix=os.path.basename(path) + "."
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def place(root, maps, default_repo, raw_path):
    """(repo, rel) — the checkout a coordinate is read from.

    A prefix named by --map wins; an unprefixed path missing from ROOT falls
    to --default-repo when the file exists there, which is how a migration
    ledger cites the original repository without a prefix. One function,
    because check, --reverify and --migrate answered this differently and two
    of the three were wrong (round 4, 🔴 4 and 🟡 9).
    """
    for name, mapped in maps.items():
        if raw_path == name or raw_path.startswith(name + "/"):
            return mapped, raw_path[len(name) :].lstrip("/") or "."
    if (
        default_repo
        and not os.path.isfile(os.path.join(root, raw_path))
        and os.path.isfile(os.path.join(default_repo, raw_path))
    ):
        return default_repo, raw_path
    return root, raw_path


def cross_repo_intent(root, maps, default_repo):
    """True when this project has DECLARED that its ledger may cite another
    repository: a parity config in the tree, or --map/--default-repo on the
    command line.

    EXTERNAL is a claim about another repo, and without one of these three
    declarations there is no other repo to claim — a missing top-level
    directory is then a broken citation, not an external one. Deleting or
    renaming a directory used to turn its rows EXTERNAL at exit 0, a green
    build over a false message (round 4, 🔴 3).
    """
    return (
        bool(maps)
        or bool(default_repo)
        or os.path.isfile(os.path.join(root, ".specseal", "parity.md"))
    )


def check_ledger(ledger, root, maps, default_repo=None):
    text = read(ledger)
    if text is None:
        # An unreadable ledger used to be a TypeError — swallowed under
        # dispatch, a traceback in CI (round 4, 🟡 14).
        return []
    findings = []
    seen = set()
    scan_cache = {}
    for m in ANCHOR_RE.finditer(text):
        raw_path, want = m.group("path"), m.group("hash")
        locator, claim = m.group("locator"), m.group("claim")
        coord = f"{raw_path}#{locator}" + (f">{claim}" if claim else "")
        # The hash is part of the key: two rows citing one unit at different
        # times disagree, and one of them is necessarily stale — deduping on
        # the coordinate alone skipped the stale one silently (round 4, 🟡 5).
        if (coord, want) in seen:
            continue
        seen.add((coord, want))

        repo, rel = place(root, maps, default_repo, raw_path)
        full = os.path.join(repo, rel)

        body = read(full)
        if body is None:
            if repo == root and cross_repo_intent(root, maps, default_repo):
                # The row cannot be placed in any repository this run knows,
                # and the declaration says another one exists. The scan stays
                # OFF: searching THIS repo for a row that may cite the other
                # one manufactures evidence, and did — a cross-repo row was
                # re-anchored onto a local look-alike (round 4, 🔴 4).
                if "/" in rel and not os.path.exists(
                    os.path.join(root, rel.split("/")[0])
                ):
                    findings.append(
                        (
                            "EXTERNAL",
                            coord,
                            "not in this repo; pass --map/--default-repo",
                        )
                    )
                else:
                    findings.append(("BROKEN", coord, "file not found"))
                continue
            # No cross-repo intent anywhere, or the row is mapped into a repo
            # we can honestly search: a missing file is a broken citation
            # whatever directory it sat in, and the same graded scan that
            # heals a renamed file heals a renamed DIRECTORY (round 4, 🔴 3).
            detail = "file not found"
            scan = scan_cache.setdefault(repo, {})
            hashes, names, capped = content_matches(repo, rel, locator, want, scan)
            if len(hashes) == 1:
                path, name, _ = hashes[0]
                tag = "moved?" if name == locator else "renamed?"
                detail += f" — identical content at {path}#{name} ({tag})"
            elif hashes:
                detail += f" — identical content at {len(hashes)} units"
            elif len(names) == 1:
                detail += f" — same name at {names[0][0]} (content differs)"
            if capped:
                detail += f" (repo-wide scan skipped: over {SCAN_FILE_CAP} files)"
            findings.append(("BROKEN", coord, detail))
            continue

        places = resolve(rel, locator, body)
        if not places:
            detail = "locator not found"
            scan = scan_cache.setdefault(repo, {})
            hashes, names, capped = content_matches(repo, rel, locator, want, scan)
            if len(hashes) == 1:
                path, name, _ = hashes[0]
                if path == rel:
                    detail += f" — identical content at #{name} (renamed?)"
                elif name == locator:
                    detail += f" — identical content at {path}#{name} (moved?)"
                else:
                    detail += f" — identical content at {path}#{name} (renamed?)"
            elif hashes:
                detail += f" — identical content at {len(hashes)} units"
            elif len(names) == 1:
                # A labelled fact, never the word "renamed": the content
                # differs, so the checker does not know that.
                detail += f" — same name at {names[0][0]} (content differs)"
            if capped:
                detail += f" (repo-wide scan skipped: over {SCAN_FILE_CAP} files)"
            findings.append(("BROKEN", coord, detail))
            continue
        if len(places) > 1:
            # Loudly, and never a measurement: with two places to look, an OK
            # would be a claim about whichever one the code happened to pick.
            at = ", ".join(f"{a}-{b}" for a, b in places)
            findings.append(
                ("BROKEN", coord, f"locator is ambiguous — {len(places)} places: {at}")
            )
            continue

        unit = places[0]
        if claim:
            inside = minor_region(rel, body, unit, claim)
            if not inside:
                # WIDEN, never break. The minor anchor's place changed, which
                # is something to re-read rather than a ledger to edit.
                findings.append(
                    (
                        "DRIFTED",
                        coord,
                        f"the anchored statement is gone from {locator} "
                        f"({unit[0]}-{unit[1]}) — re-verify",
                    )
                )
                continue
            unit = inside[0]

        start, end = unit
        got = content_hash(body.splitlines()[start - 1 : end])
        if got != want:
            findings.append(
                ("DRIFTED", coord, f"content changed at {start}-{end} — re-verify")
            )
            continue
        findings.append(("OK", coord, f"{start}-{end}"))
    findings.extend(old_format_rows(text))
    return findings


def old_format_rows(text):
    """("OLD-FORMAT", coord, remedy) for every pre-anchor coordinate in a row.

    Its own verdict, not folded into BROKEN, because the remedy differs — and
    it fails the run with or without `--strict`: a red build saying "run the
    migrator" beats a green build checking nothing. Only table rows are read,
    and new-format anchors are blanked first so a quoted locator that happens
    to mention an old coordinate cannot trip this forever.
    """
    findings, seen = [], set()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        for m in OLD_COORD_RE.finditer(ANCHOR_RE.sub(" ", line)):
            if URL_HOST_RE.search(line[: line.find(m.group(0))]):
                continue
            if m.group(0) in seen:
                continue
            seen.add(m.group(0))
            findings.append(
                (
                    "OLD-FORMAT",
                    m.group(0),
                    "old `path:line` coordinate — run `evidence-check --migrate .`",
                )
            )
    return findings


def content_at(root, sha, rel):
    """The file as the stamped commit held it — or None where git cannot say.

    The one git call in this file, and it belongs to the one-shot WRITER, not
    to the checker: `check_ledger`, `resolve` and `--reverify` never reach for
    git, which is what `test_the_checker_asks_git_for_nothing` pins. A
    migration is a different act — it rewrites rows on the strength of line
    numbers recorded long ago, and the old stamp's commit is the only
    evidence that can say whether those numbers still mean anything
    (round 4, 🟡 10).
    """
    try:
        r = subprocess.run(
            ["git", "-C", root, "show", f"{sha}:{rel}"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def migrate(ledgers, root, maps=None, default_repo=None):
    """Rewrite every old `path:line` row to `path#anchor@hash` — the shipped form of the
    migration this repository ran on its own 51 coordinates.

    Per coordinate: trim blank padding off the cited range, find the smallest
    resolvable unit that CONTAINS it, and write that unit's anchor with the
    hash computed the normal way. The stamp drops and the date stays: nothing
    measures from a commit any more.

    Before trusting a line number, the one evidence that can vouch for it is
    consulted: where git can produce the file at the row's old stamp, a cited
    range whose content CHANGED since that commit is LEFT — the numbers no
    longer mean what they meant, and rewriting on them anchored a row to
    whatever sits there now (round 4, 🟡 10). Where the proof is unavailable
    — no git, no stamp, a commit a squash orphaned, a cross-repo row — the
    row migrates on the current tree alone and the count of such rows is
    returned, so the caller can say so.

    What cannot be proven is LEFT and reported, never guessed — a line past
    the end of the file, a file that is gone, a range no single unit contains,
    a range that moved since the stamp. A left row keeps failing the plain
    check as OLD-FORMAT, so the loop closes on a person rather than on
    silence. Running this twice is a no-op: the second pass finds no old
    coordinates.

    Returns (rows migrated, [(coordinate, why) left], rows migrated without
    the stamp proof); printing belongs to the callers, because the
    session-start hook says it in one line where the CLI itemises.
    """
    maps = maps or {}
    migrated, left, unproven = 0, [], 0
    for ledger in ledgers:
        text = read(ledger)
        if text is None:
            continue
        out_lines = []
        for line in text.splitlines(keepends=True):
            if not line.lstrip().startswith("|"):
                out_lines.append(line)
                continue
            blanked = ANCHOR_RE.sub(lambda m: " " * len(m.group(0)), line)
            hits = [
                m
                for m in OLD_COORD_RE.finditer(blanked)
                if not URL_HOST_RE.search(blanked[: m.start()])
            ]
            if not hits:
                out_lines.append(line)
                continue
            sha_m = STAMP_SHA_RE.search(blanked)
            row_sha = sha_m.group("sha") if sha_m else None
            spliced, at, failed, row_n, row_unproven = [], 0, False, 0, 0
            for m in hits:
                raw, s = m.group("path"), int(m.group("start"))
                e = int(m.group("end") or s)
                repo, rel = place(root, maps, default_repo, raw)
                body = read(os.path.join(repo, rel))
                if body is None:
                    left.append((m.group(0), "file not found"))
                    failed = True
                    continue
                lines = body.splitlines()
                if e > len(lines):
                    left.append((m.group(0), f"line past EOF ({len(lines)} lines)"))
                    failed = True
                    continue
                proved = False
                if repo == root and row_sha:
                    old_body = content_at(root, row_sha, rel)
                    if old_body is not None:
                        old_lines = old_body.splitlines()
                        if e > len(old_lines) or normalise(
                            old_lines[s - 1 : e]
                        ) != normalise(lines[s - 1 : e]):
                            left.append(
                                (
                                    m.group(0),
                                    "content changed since the stamp "
                                    f"`{row_sha[:7]}` — the cited lines no "
                                    "longer mean what they meant",
                                )
                            )
                            failed = True
                            continue
                        proved = True
                while s < e and not lines[s - 1].strip():
                    s += 1
                while e > s and not lines[e - 1].strip():
                    e -= 1
                best = None
                for name, (a, b) in file_units(rel, body):
                    if (
                        a <= s
                        and e <= b
                        and (best is None or b - a < best[2] - best[1])
                    ):
                        best = (name, a, b)
                if best is None:
                    left.append((m.group(0), f"no single unit contains {s}-{e}"))
                    failed = True
                    continue
                name, a, b = best
                spliced.append(line[at : m.start()])
                spliced.append(f"{raw}#{name}@{content_hash(lines[a - 1 : b])}")
                at = m.end()
                row_n += 1
                if not proved:
                    row_unproven += 1
            if failed or not spliced:
                # All-or-nothing per row, so a partial rewrite never strands
                # half a cell and the report stays per-row readable.
                out_lines.append(line)
                continue
            migrated += row_n
            unproven += row_unproven
            spliced.append(line[at:])
            out_lines.append(OLD_STAMP_RE.sub(r"\1", "".join(spliced)))
        new_text = "".join(out_lines)
        if new_text != text:
            write_atomic(ledger, new_text)
    return migrated, left, unproven


def reverify(ledgers, root, maps, default_repo=None):
    """Rewrite the hash of every row whose anchor resolves. Explicit, by hand.

    Re-verifying is recomputing the hash, which is a person saying they have
    re-read the code. It is deliberately a separate command: a check that
    silently refreshed what it was checking would report OK forever.
    """
    changed = 0
    scan_cache = {}
    for ledger in ledgers:
        text = read(ledger)
        if text is None:
            continue
        out, at = [], 0
        for m in ANCHOR_RE.finditer(text):
            raw_path = m.group("path")
            locator, claim = m.group("locator"), m.group("claim")
            repo, rel = place(root, maps, default_repo, raw_path)
            body = read(os.path.join(repo, rel))
            places = resolve(rel, locator, body) if body is not None else []
            if not places and claim is None:
                if (
                    body is None
                    and repo == root
                    and cross_repo_intent(root, maps, default_repo)
                ):
                    # The row cannot be placed in any repository this run
                    # knows, and the declaration says another one exists.
                    # Scanning THIS repo re-anchored a cross-repo row onto a
                    # local look-alike (round 4, 🔴 4) — the check reports
                    # such a row EXTERNAL or file-not-found, and reverify
                    # must agree with the check rather than out-heal it.
                    continue
                # One unit reconstructing the RECORDED hash is what licenses
                # the rewrite — never a name-alone match, which is a fact to
                # print rather than evidence to act on. Path and locator both
                # follow the unit, and the hash follows the locator. It
                # cannot stay: the name is part of the unit's own hashed
                # region, so the recorded hash is of the OLD spelling and
                # keeping it would leave the re-anchored row DRIFTED with
                # nothing to re-read. Measured, in the case that pins this.
                scan = scan_cache.setdefault(repo, {})
                hashes, _, _ = content_matches(
                    repo, rel, locator, m.group("hash"), scan
                )
                if len(hashes) == 1:
                    path, name, (a, b) = hashes[0]
                    target = body if path == rel else read(os.path.join(repo, path))
                    new_raw = (
                        raw_path
                        if path == rel
                        else (raw_path[: len(raw_path) - len(rel)] + path)
                    )
                    out.append(text[at : m.start("path")])
                    out.append(new_raw)
                    out.append(text[m.end("path") : m.start("locator")])
                    out.append(name)
                    out.append(text[m.end("locator") : m.start("hash")])
                    out.append(content_hash(target.splitlines()[a - 1 : b]))
                    at = m.end("hash")
                    changed += 1
                    shown = f"#{name}" if path == rel else f"{path}#{name}"
                    # "identical content", not "moved intact": identity is
                    # the whole of what reconstruction proved. A deletion
                    # beside a boilerplate twin reconstructs too, and that
                    # history is the reader's to judge from the diff
                    # (round 4, 🟡 7).
                    print(f"  {raw_path}#{locator} -> {shown}  (identical content)")
                continue
            if body is None:
                continue
            if len(places) != 1:
                continue
            if claim:
                inside = minor_region(rel, body, places[0], claim)
                if not inside:
                    continue
                places = inside
            start, end = places[0]
            got = content_hash(body.splitlines()[start - 1 : end])
            if got == m.group("hash"):
                continue
            out.append(text[at : m.start("hash")])
            out.append(got)
            at = m.end("hash")
            changed += 1
            shown = f"{raw_path}#{locator}" + (f">{claim}" if claim else "")
            print(f"  {shown}  {m.group('hash')} -> {got}")
        if out:
            out.append(text[at:])
            write_atomic(ledger, "".join(out))
    print(f"{changed} row{'' if changed == 1 else 's'} re-verified")
    return 0


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
    ap.add_argument(
        "--migrate",
        action="store_true",
        help="rewrite old `path:line` rows to `path#anchor@hash`; rows it "
        "cannot prove are left and named",
    )
    ap.add_argument(
        "--reverify",
        action="store_true",
        help="rewrite each row's hash to what its anchor holds now",
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
    # `.specseal/map.md` is where it lives now; `map/*.md` is one fragment per
    # work item; `docs/**/_evidence.md` is the pre-0.10 address.
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

    if args.migrate:
        migrated, left, unproven = migrate(ledgers, root, maps, default_repo)
        print(
            f"{migrated} row{'' if migrated == 1 else 's'} migrated · {len(left)} left"
        )
        if unproven:
            print(
                f"  {unproven} rewritten without the since-the-stamp proof "
                "(git, the stamp, or the stamped commit unavailable) — "
                "those rows rest on the current tree alone; review them in "
                "the diff"
            )
        for coord, why in left:
            print(f"  LEFT  {coord}  {why}")
        return 1 if left else 0
    if args.reverify:
        return reverify(ledgers, root, maps, default_repo)

    totals = {"OK": 0, "DRIFTED": 0, "BROKEN": 0, "EXTERNAL": 0, "OLD-FORMAT": 0}
    for ledger in ledgers:
        findings = check_ledger(ledger, root, maps, default_repo)
        print(f"\n{os.path.relpath(ledger, root)}")
        for status, coord, detail in findings:
            totals[status] += 1
            if status != "OK":
                print(f"  {status:8} {coord}  {detail}")
        counts = {k: sum(1 for s, _, _ in findings if s == k) for k in totals}
        # old-format is on the line even at zero: a red build whose summary
        # read all zeros is what round 4's 🟡 6 measured.
        print(
            f"  {counts['OK']} ok · {counts['DRIFTED']} drifted · "
            f"{counts['BROKEN']} broken · {counts['EXTERNAL']} external · "
            f"{counts['OLD-FORMAT']} old-format"
        )

    print(
        f"\ntotal: {totals['OK']} ok · {totals['DRIFTED']} drifted · "
        f"{totals['BROKEN']} broken · {totals['EXTERNAL']} external · "
        f"{totals['OLD-FORMAT']} old-format"
    )
    if totals["OLD-FORMAT"]:
        return 2
    if totals["BROKEN"]:
        return 2
    if totals["DRIFTED"]:
        return 2 if args.strict else 1
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
