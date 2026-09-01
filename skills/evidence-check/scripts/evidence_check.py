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
here. There is no baseline, no stamp, no commit SHA and no call to git.

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
import sys

# `path#anchor@hash`. The anchor is either a dotted symbol name or a quoted
# line of text; `\|` inside the quotes is an escaped pipe, so a row anchored to
# a markdown table line does not split the table it lives in.
ANCHOR_RE = re.compile(
    r"(?P<path>[A-Za-z0-9_@.][A-Za-z0-9_.@/-]*[/.][A-Za-z0-9_.@/-]*?)"
    r"#(?P<anchor>\"(?:[^\"\n]|\\\")+\"|[A-Za-z_][A-Za-z0-9_.]*)"
    r"@(?P<hash>[0-9a-f]{6,12})"
)
HASH_LEN = 8


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
    """{qualified name: [(start, end)]} for every def and class in a module.

    Decorators are part of the span: a decorator carries behaviour, and a row
    anchored to the function it decorates should notice one being added or
    removed. A file that will not parse yields nothing, so its rows fall to
    text anchors rather than reporting a false OK.
    """
    out = {}
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return out

    def walk(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = prefix + child.name
                start = min([child.lineno] + [d.lineno for d in child.decorator_list])
                out.setdefault(name, []).append((start, child.end_lineno))
                walk(child, name + ".")
            else:
                walk(child, prefix)

    walk(tree, "")
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


def resolve(path, anchor, text):
    """[(start, end)] for the anchor — empty for none, several for ambiguous."""
    lines = text.splitlines()
    markdown = path.endswith(".md")
    if anchor.startswith('"'):
        return text_regions(lines, unescape(anchor[1:-1]), markdown)
    if path.endswith(".py"):
        return py_spans(text).get(anchor, [])
    return text_regions(lines, anchor, markdown)


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def check_ledger(ledger, root, maps, default_repo=None):
    text = read(ledger)
    findings = []
    seen = set()
    for m in ANCHOR_RE.finditer(text):
        raw_path, anchor, want = m.group("path"), m.group("anchor"), m.group("hash")
        coord = f"{raw_path}#{anchor}"
        if coord in seen:
            continue
        seen.add(coord)

        repo, rel = root, raw_path
        for name, mapped in maps.items():
            if raw_path == name or raw_path.startswith(name + "/"):
                repo, rel = mapped, raw_path[len(name) :].lstrip("/") or "."
                break
        else:
            if (
                not os.path.isfile(os.path.join(root, raw_path))
                and default_repo
                and os.path.isfile(os.path.join(default_repo, raw_path))
            ):
                repo = default_repo
        full = os.path.join(repo, rel)

        body = read(full)
        if body is None:
            # A cross-repo coordinate always carries a prefix directory. A bare
            # root-level path whose file is gone is a broken citation, not an
            # external one — EXTERNAL is exempt from --strict, and a deleted
            # file must fail the build.
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

        places = resolve(rel, anchor, body)
        if not places:
            findings.append(("BROKEN", coord, "anchor not found"))
            continue
        if len(places) > 1:
            # Loudly, and never a measurement: with two places to look, an OK
            # would be a claim about whichever one the code happened to pick.
            at = ", ".join(f"{a}-{b}" for a, b in places)
            findings.append(
                ("BROKEN", coord, f"anchor is ambiguous — {len(places)} places: {at}")
            )
            continue

        start, end = places[0]
        got = content_hash(body.splitlines()[start - 1 : end])
        if got != want:
            findings.append(
                ("DRIFTED", coord, f"content changed at {start}-{end} — re-verify")
            )
            continue
        findings.append(("OK", coord, f"{start}-{end}"))
    return findings


def reverify(ledgers, root, maps, default_repo=None):
    """Rewrite the hash of every row whose anchor resolves. Explicit, by hand.

    Re-verifying is recomputing the hash, which is a person saying they have
    re-read the code. It is deliberately a separate command: a check that
    silently refreshed what it was checking would report OK forever.
    """
    changed = 0
    for ledger in ledgers:
        text = read(ledger)
        out, at = [], 0
        for m in ANCHOR_RE.finditer(text):
            raw_path, anchor = m.group("path"), m.group("anchor")
            repo, rel = root, raw_path
            for name, mapped in maps.items():
                if raw_path == name or raw_path.startswith(name + "/"):
                    repo, rel = mapped, raw_path[len(name) :].lstrip("/") or "."
                    break
            body = read(os.path.join(repo, rel))
            if body is None:
                continue
            places = resolve(rel, anchor, body)
            if len(places) != 1:
                continue
            start, end = places[0]
            got = content_hash(body.splitlines()[start - 1 : end])
            if got == m.group("hash"):
                continue
            out.append(text[at : m.start("hash")])
            out.append(got)
            at = m.end("hash")
            changed += 1
            print(f"  {raw_path}#{anchor}  {m.group('hash')} -> {got}")
        if out:
            out.append(text[at:])
            with open(ledger, "w", encoding="utf-8") as f:
                f.write("".join(out))
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

    if args.reverify:
        return reverify(ledgers, root, maps, default_repo)

    totals = {"OK": 0, "DRIFTED": 0, "BROKEN": 0, "EXTERNAL": 0}
    for ledger in ledgers:
        findings = check_ledger(ledger, root, maps, default_repo)
        print(f"\n{os.path.relpath(ledger, root)}")
        for status, coord, detail in findings:
            totals[status] += 1
            if status != "OK":
                print(f"  {status:8} {coord}  {detail}")
        counts = {k: sum(1 for s, _, _ in findings if s == k) for k in totals}
        print(
            f"  {counts['OK']} ok · {counts['DRIFTED']} drifted · "
            f"{counts['BROKEN']} broken · {counts['EXTERNAL']} external"
        )

    print(
        f"\ntotal: {totals['OK']} ok · {totals['DRIFTED']} drifted · "
        f"{totals['BROKEN']} broken · {totals['EXTERNAL']} external"
    )
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
