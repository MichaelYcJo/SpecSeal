#!/usr/bin/env python3
"""unverified-check — read what an overview recorded as unverified, and fail
on a record that cannot be read.

`verify` condition 4 lets a claim go out unproven as long as the row names who
answers it. Nothing ever read those rows again. The measured failure: a row in
`specs/1787495842-verify-the-unverified/overview.md` said nobody had seen the
gates render in an interactive TUI and named the user as the answerer. Months
later the user hit exactly that, from the other side, and asked why every gate
renders as yes/no. The record was accurate and no procedure ever closed it.

So this reads every `## Not verified` section and reports what is still open.
It does **not** fail because items are open. Dozens were open the day it was
written, and a build that goes red for an honest `unverified` row teaches
people to write none, which voids the condition it is defending. Counting them
is what `unverified-check specs/` is for; no number is repeated in prose here,
because a number in a comment is right for one commit and nobody recounts it.

It fails for what the author can always fix:

  malformed   a section that cannot be read. A tolerant parser reports zero
              here, and zero reads as "everything has been closed" — the worst
              available failure, because it is indistinguishable from success
  fewer rows  a table that lost rows against the base revision, or an
              `overview.md` that was there and is not (`--baseline REF`)
  no baseline the ref itself does not resolve. That is exit 2, not a pass:
              a comparison against nothing is not a comparison

An item is closed by marking it, never by deleting it: prefix the Item cell
with the check mark and say in the second cell what closed it. Anything
unmarked counts open, so the silent direction is always "still open".

Deliberately a text scan of markdown, not a parser library: the gates here are
stdlib-only, and the format it accepts is one line long. That format is strict
on purpose — see `check_file`.

Exit codes: 0 the record is readable (open items are reported, not punished) ·
1 a section could not be read, or rows were deleted · 2 the path or arguments
were unusable, which includes a scan that found no overview at all.
"""

import argparse
import os
import re
import subprocess
import sys

OVERVIEW = "overview.md"
HEADING = "## Not verified"
HEADER = ("Item", "Who must answer")
CLOSED = "✅"
PLACEHOLDER = re.compile(r"^<[^>]*>$")
# Characters that occupy no width: the two variation selectors, the zero-width
# family, and the byte-order mark. None of them make a marker into a claim.
INVISIBLE = "\ufe0f\ufe0e\u200b\u200c\u200d\u2060\ufeff"
SEPARATOR = re.compile(r"^:?-+:?$")
SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}
# The heading matcher for a base revision. There is one reader; only how it
# finds the section is an argument, because a base commit may spell the
# heading the way this corpus did before it was normalized. Everything else —
# how a cell is read, where a fence ends, how a path resolves — is shared, and
# that sharing is what stopped one fix from opening the next gap.
LOOSE_HEADING = re.compile(r"^#{2,3}\s.*not verified", re.I)


def split_row(line):
    """Cells of one markdown table row, or None if the line is not a row.

    `\\|` inside a cell is an escaped pipe, not a column break."""
    s = line.strip()
    if not s.startswith("|"):
        return None
    s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def is_separator(cells):
    return bool(cells) and all(SEPARATOR.match(c) for c in cells)


def is_header(cells):
    return bool(cells) and cells[0].strip().lower() == "item"


def visible(s):
    """`s` without characters that take no space on screen.

    Many keyboards emit U+2705 followed by U+FE0F, and a zero-width space
    pastes in from anywhere. Either one makes `| \u2705 | done |` survive a
    plain `.strip()` while looking exactly like a bare check mark, which is
    the one row shape this refuses."""
    return s.translate({ord(c): None for c in INVISIBLE}).strip()


def strip_comments(lines):
    """The same lines with HTML comment content blanked out, indices intact.

    A template explains a section in a comment beside it, and an overview keeps
    that comment. The guidance is not rows, and it is not prose where a table
    belongs."""
    out, inside = [], False
    for line in lines:
        rest, kept = line, ""
        while rest:
            if inside:
                end = rest.find("-->")
                if end == -1:
                    rest = ""
                else:
                    rest, inside = rest[end + 3 :], False
            else:
                start = rest.find("<!--")
                if start == -1:
                    kept, rest = kept + rest, ""
                else:
                    kept, rest, inside = kept + rest[:start], rest[start + 4 :], True
        out.append(kept)
    return out


def blank_fences(lines):
    """The same lines with fenced blocks blanked out, indices intact.

    A skill or an overview quoting this very format must not read as rows or
    as a second section. Blanking rather than truncating matters: the working
    tree and the base revision have to agree about where the table is, or
    adding an example reads as a deletion and rows after an example read as
    absent."""
    out, marker = [], None
    for line in lines:
        opener = re.match(r"^\s*(`{3,}|~{3,})", line)
        if opener and marker is None:
            marker = opener.group(1)
            out.append("")
            continue
        if opener and marker and opener.group(1)[0] == marker[0]:
            if len(opener.group(1)) >= len(marker):
                marker = None
            out.append("")
            continue
        out.append("" if marker else line)
    return out


def readable(text):
    """The lines a reader should judge: no comment text, no fenced blocks.

    Every read starts here — the working tree and the base revision alike —
    which is what keeps the two sides of the comparison counting the same
    table."""
    return blank_fences(strip_comments(text.splitlines()))


def headings(lines):
    """(index, text) for every heading in already-`readable` lines."""
    return [(i, line.rstrip()) for i, line in enumerate(lines) if line.startswith("#")]


def parse_section(body, offset, strict_header=True):
    """(open, closed, errors) for the body lines of one section.

    `offset` is the file line number of body[0], so every error carries a
    coordinate the author can open."""
    errors, open_rows, closed_rows = [], [], []
    content = [(offset + i, ln) for i, ln in enumerate(body) if ln.strip()]

    if not content:
        errors.append(
            (offset, "the section is empty — write the table, or `none — <why>`")
        )
        return open_rows, closed_rows, errors

    first_no, first = content[0]
    if first.strip().lower().startswith("none"):
        for line_no, line in content[1:]:
            if line.strip().startswith("|"):
                errors.append((line_no, "`none` and a table in the same section"))
                break
        return open_rows, closed_rows, errors

    cells = split_row(first)
    if cells is None:
        errors.append(
            (
                first_no,
                "expected `| Item | Who must answer |`, found prose. Prose "
                "belongs under `## Not done`; this section is read by a machine",
            )
        )
        return open_rows, closed_rows, errors
    if (tuple(cells) != HEADER) if strict_header else not is_header(cells):
        errors.append(
            (
                first_no,
                f"header is |{'|'.join(cells)}|, and the one this reads is "
                f"|{'|'.join(HEADER)}|",
            )
        )
        return open_rows, closed_rows, errors
    if len(content) < 2 or not is_separator(split_row(content[1][1]) or []):
        errors.append((first_no, "the header row is not followed by a separator row"))
        return open_rows, closed_rows, errors

    rows = content[2:]
    if not rows:
        errors.append(
            (first_no, "a table with no rows says nothing — write `none — <why>`")
        )
    for line_no, line in rows:
        cells = split_row(line)
        if cells is None:
            errors.append((line_no, "a line inside the table that is not a table row"))
            continue
        if len(cells) != 2:
            errors.append((line_no, f"{len(cells)} cells, expected 2"))
            continue
        item, who = cells
        # One normalization for every judgment below. Reading the raw cell in
        # one place and the normalized cell in another is how a zero-width
        # space turned a separator into an unverified item and a blank row
        # into an open one.
        seen = [visible(c) for c in cells]
        if is_separator(seen) or is_header(seen):
            errors.append(
                (
                    line_no,
                    "a second header or separator row inside the section — it "
                    "holds one table, and a repeated one counts `|---|---|` "
                    "as an unverified item",
                )
            )
            continue
        if not seen[0] or not seen[1]:
            errors.append(
                (line_no, "an empty cell — every row names an item and its answerer")
            )
            continue
        if PLACEHOLDER.match(seen[0]) or PLACEHOLDER.match(seen[1]):
            errors.append((line_no, "the template's placeholder is still in the row"))
            continue
        if seen[0].startswith(CLOSED):
            rest = visible(seen[0][len(CLOSED) :])
            if not rest:
                errors.append(
                    (
                        line_no,
                        f"a bare {CLOSED} — the row keeps the item's text, and "
                        "the second cell says what closed it",
                    )
                )
                continue
            closed_rows.append((line_no, rest, who))
        else:
            open_rows.append((line_no, item, who))
    return open_rows, closed_rows, errors


def check_file(path):
    """(open, closed, errors) for one overview.

    Exactly one `## Not verified` section, spelled that way. Tolerating other
    spellings is what makes an unknown one report zero, and this corpus had
    more than one of them."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as exc:
        return [], [], [(0, f"cannot be read: {exc}")]
    return check_text(text)


def sections(lines, heading):
    """Where the section starts, under the matcher this read was given.

    The canonical heading always wins when the file has one. Without that, a
    base revision holding both `## Not verified` and a heading that merely
    mentions the phrase would be counted differently from the working tree,
    and the file would be reported as having lost rows nobody removed."""
    if isinstance(heading, str):
        return [i for i, text in headings(lines) if text.strip() == heading]
    exact = [i for i, text in headings(lines) if text.strip() == HEADING]
    return exact or [i for i, text in headings(lines) if heading.match(text)]


def check_text(text, heading=HEADING, strict_header=True):
    """The reader. One of it, for the working tree and for a base revision.

    There used to be two, and while both existed every property added to one
    had to be added to the other by hand. Four pairs drifted apart across
    three review rounds — which section is counted, how a cell is normalized,
    where a fence ends, how a path resolves — and each fix on one side opened
    a gap on the other.

    Three of those four are now shared outright. The fourth is these two
    arguments, and they say the same thing twice: a base revision may be
    written the way the corpus was before this normalization. Measured here,
    the files that changed did not only change the heading — they renamed the
    second column from `Who` to `Who must answer` — so relaxing the heading
    alone would still have stopped comparing them.

    Nothing else relaxes. A legacy header still has to be a two-cell row whose
    first column is `Item`, and every row below it is read exactly as the
    working tree's rows are. The relaxation ends when every base carries the
    canonical wording."""
    lines = readable(text)

    found = sections(lines, heading)
    if not found:
        near = [(i, text) for i, text in headings(lines) if LOOSE_HEADING.match(text)]
        hint = (
            f" (found `{near[0][1].strip()}` at line {near[0][0] + 1})" if near else ""
        )
        return [], [], [(1, f"no `{HEADING}` section{hint}")]
    if len(found) > 1:
        at = ", ".join(str(i + 1) for i in found)
        return (
            [],
            [],
            [(found[1] + 1, f"more than one `{HEADING}` section: lines {at}")],
        )

    start = found[0]
    end = len(lines)
    for i, _ in headings(lines):
        if i > start:
            end = i
            break
    return parse_section(lines[start + 1 : end], start + 2, strict_header)


def overviews(paths):
    """Every overview.md under the given paths, in a stable order."""
    found = []
    for p in paths:
        # The argument is resolved once, and nothing below it is. `ls-tree`
        # lists a tracked symbolic link under its own path, so resolving each
        # file made a link that is right there read as deleted.
        p = real(p)
        if os.path.isfile(p):
            found.append(p)
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            if OVERVIEW in files:
                found.append(os.path.join(root, OVERVIEW))
    return sorted(dict.fromkeys(found))


def real(path):
    """`path` with symbolic links resolved.

    Every path this compares has to come through here. `git rev-parse
    --show-toplevel` answers with links already resolved, so a caller who
    reaches the tree through one — `/tmp` on macOS is a link to `/private/tmp`,
    and a code directory linked from home is the same shape — produced a
    repo-relative path like `../link/specs`, which matches no line of
    `ls-tree`. Both comparisons then found nothing to do and the run passed:
    the state the ref check above exists to prevent, reached by another
    door."""
    return os.path.realpath(path)


def git_path(path):
    r"""`path` as git spells it: forward slashes, whatever `os.sep` is here.

    Every repo-relative path in this file is built by `os.path.relpath` and
    then handed to git — as a `show` argument, or compared against what
    `ls-tree` printed. git answers and accepts `/` on every platform, so on
    Windows the two sides were built by two rules: `specs\x\overview.md`
    against `specs/x/overview.md`. `show` returned None and the row check
    quietly compared nothing; the presence check matched no path and reported
    every tracked overview as deleted.

    A no-op where `os.sep` already is `/`, rather than branching on `os.name`:
    the substitution has to be on the path Linux CI runs, or the Windows half
    is proven by nothing. It also must not run there — a backslash is a legal
    character in a POSIX filename, and rewriting it would corrupt a real name.
    """
    return path if os.sep == "/" else path.replace(os.sep, "/")


def repo_relative(path, root):
    r"""`path` as a repo-relative git path, or None when it has no relative form.

    The composition `git_path(os.path.relpath(...))` is not safe on its own:
    `relpath` raises across drives, and the four sites that hand a path to git
    were left holding that raise while the two reporting sites got
    `display_path`. Measured: the run printed one row and then died mid-report
    with the very `ValueError` the helper beside this one exists to prevent.

    None rather than a fallback, because these four are asking git a question
    about a path INSIDE a repository. A path on another volume is not inside
    this one -- a working tree cannot span drives -- so there is no answer to
    degrade to, and inventing one is the quiet zero this tool refuses.
    `main` rejects that case up front; this is what makes the rejection
    total rather than a promise.
    """
    try:
        return git_path(os.path.relpath(path, root))
    except ValueError:
        return None


def display_path(path, start):
    r"""`path` relative to `start`, or absolute when there is no relative form.

    `os.path.relpath` raises `ValueError` on Windows when the two are on
    different drives, and this is the reporting footing for every line the
    tool prints. Running `unverified-check D:\repo\specs` from `C:\` is
    an ordinary thing to do, and it died with a traceback before printing a
    single row. The absolute path is a worse answer than a relative one and a
    far better one than no output at all.
    """
    try:
        return os.path.relpath(path, start)
    except ValueError:
        return os.path.abspath(path)


def nearest_existing(path):
    """`path`, or the closest ancestor of it that exists.

    A deleted directory still has to name the repository it was in."""
    p = os.path.abspath(path)
    while not os.path.exists(p) and os.path.dirname(p) != p:
        p = os.path.dirname(p)
    return p


def unique_by_target(paths):
    """One path per real file, first in sort order.

    A tracked symbolic link and the file it points at are one record and two
    paths. Counting both doubles its open items. Presence is a different
    question and keeps every path — `ls-tree` lists the link under its own
    name, so dropping it here would report a file that is right there as
    deleted."""
    seen, out = set(), []
    for p in paths:
        target = os.path.realpath(p)
        if target in seen:
            continue
        seen.add(target)
        out.append(p)
    return out


def repo_root(path):
    here = path if os.path.isdir(path) else (os.path.dirname(path) or ".")
    r = subprocess.run(
        ["git", "-C", here, "rev-parse", "--show-toplevel"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.stdout.strip() if r.returncode == 0 else None


def resolves(root, ref):
    """Whether `ref` names a commit in `root`.

    Asked before anything is compared. An unresolvable ref used to make every
    comparison return "no base version", which is the same silence as a file
    that is genuinely new — so a CI checkout too shallow to hold the base
    branch turned the deletion check off and reported success."""
    r = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.returncode == 0


def overviews_at(root, ref, prefixes):
    """Repo-relative `overview.md` paths present at `ref` under `prefixes`.

    The scan walks the tree as it is now, so a file deleted wholesale never
    enters it and its rows leave without a word. Deleting the file was
    therefore cheaper and quieter than deleting one row from it, which is the
    behaviour the row check exists to make expensive."""
    r = subprocess.run(
        ["git", "-C", root, "ls-tree", "-r", "--name-only", ref],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        return []
    out = []
    for rel in r.stdout.splitlines():
        if os.path.basename(rel) != OVERVIEW:
            continue
        # The same skip list the scan walks with. Built by a different rule,
        # a tracked overview.md under build/ or node_modules/ would be absent
        # from every scan and so reported as deleted on every run — a red
        # build the author can only clear by renaming the directory.
        if set(os.path.dirname(rel).split("/")) & SKIP_DIRS:
            continue
        if any(p == "." or rel == p or rel.startswith(p + "/") for p in prefixes):
            out.append(rel)
    return out


def show(root, ref, rel):
    r = subprocess.run(
        ["git", "-C", root, "show", f"{ref}:{rel}"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.stdout if r.returncode == 0 else None


def annotate(kind, path, line, message):
    """A GitHub annotation in CI, a plain line anywhere else."""
    if os.environ.get("GITHUB_ACTIONS"):
        # An annotation is matched against the diff by path, and GitHub spells
        # those the way git does. Every caller passes `display_path` output,
        # which is `os.sep`-spelled on purpose -- right for a line a person
        # reads, wrong for this. Unreachable while `hygiene.yml` pins
        # `ubuntu-latest`; live the moment these tools run on the Windows leg,
        # which is what the decision in `.specseal/map.md` points at.
        where = f" file={git_path(path)},line={line}" if path else ""
        return f"::{kind}{where}::{message}"
    return f"{path}:{line}  {message}" if path else message


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="unverified-check",
        description="Report open `## Not verified` items; fail on a record "
        "that cannot be read.",
    )
    ap.add_argument("path", nargs="*", default=["."])
    ap.add_argument(
        "--baseline",
        metavar="REF",
        help="also fail when a table holds fewer rows than it does at REF, or "
        "when an overview.md that exists at REF is gone — an item leaves by "
        "being marked closed, not by the row or the file being deleted",
    )
    args = ap.parse_args(argv)

    missing = [p for p in args.path if not os.path.exists(p)]
    if missing and not args.baseline:
        print(f"unverified-check: no such path: {missing[0]}", file=sys.stderr)
        return 2
    # With a baseline, a path that is gone may be the thing being asked about:
    # the workflow runs `--baseline origin/<base> specs/`, and a change that
    # deletes specs/ used to be told it had mistyped an argument. A path that
    # held nothing at the base either is still a typo, and saying so is what
    # keeps `specs/ spces/` from passing in silence. That check needs the
    # repository, so it waits until the baseline block below has resolved one.

    # Resolved before the scan, because deleting every overview.md is the one
    # case where the scan finds nothing AND something has to be reported. It
    # used to exit 2 saying "nothing was checked", which reads as a bad
    # argument — and in a repository with one work item, deleting a single
    # file is that case.
    root = None
    if args.baseline:
        root = repo_root(real(nearest_existing(args.path[0])))
        if root is None:
            print(
                f"unverified-check: --baseline {args.baseline} needs a git "
                f"repository, and {args.path[0]} is not in one — nothing was "
                "compared",
                file=sys.stderr,
            )
            return 2
        if not resolves(root, args.baseline):
            print(
                f"unverified-check: --baseline {args.baseline} does not resolve "
                f"in {root} — nothing was compared. A shallow checkout or a "
                "renamed base branch lands here, and passing it would report "
                "a deletion check that never ran",
                file=sys.stderr,
            )
            return 2
        # Every argument is compared against ONE repository, the one the FIRST
        # argument is in. That was always the rule and nothing stated it, so on
        # Windows a second argument on another drive reached `os.path.relpath`
        # and aborted the run mid-report. Said here instead: a path with no
        # relative form to `root` is not in `root`, because a working tree
        # cannot span volumes.
        outside = [
            p
            for p in args.path
            if repo_relative(real(nearest_existing(p)), root) is None
        ]
        if outside:
            print(
                f"unverified-check: {outside[0]} is not in {root} — nothing "
                "was compared. Every path is read against the repository the "
                "first one is in, and this one is on another volume",
                file=sys.stderr,
            )
            return 2

    if missing and args.baseline:
        typos = [
            p
            for p in missing
            if not overviews_at(
                root,
                args.baseline,
                [repo_relative(real(p), root)],
            )
        ]
        if typos:
            print(
                f"unverified-check: no such path: {typos[0]} — and nothing "
                f"under it at {args.baseline} either, so there is nothing to "
                "compare it against",
                file=sys.stderr,
            )
            return 2

    files = overviews(args.path)
    cwd = os.getcwd()
    total_open = total_closed = 0
    bad, deleted, uncompared = [], [], []
    for path in unique_by_target(files):
        rel = display_path(path, cwd)
        open_rows, closed_rows, errors = check_file(path)
        total_open += len(open_rows)
        total_closed += len(closed_rows)
        for line_no, message in errors:
            bad.append(annotate("error", rel, line_no, message))
        if not errors and (open_rows or closed_rows):
            print(f"  {rel}  {len(open_rows)} open · {len(closed_rows)} closed")
            for _, item, who in open_rows:
                print(f"      open  {item}  —  {who}")

        if args.baseline and not errors:
            # An unreadable section returns zero rows, and comparing that zero
            # told the author to restore rows that never left.
            base_text = show(root, args.baseline, repo_relative(path, root))
            if base_text is None:
                continue
            base_open, base_closed, base_errors = check_text(
                base_text, heading=LOOSE_HEADING, strict_header=False
            )
            if base_errors:
                # Never a silent zero: a base this cannot read is a file whose
                # count is unknown, and saying so is the whole point of the
                # tool. It is not an error either — the author cannot edit a
                # commit that already happened.
                uncompared.append(
                    annotate(
                        "notice",
                        rel,
                        1,
                        f"not compared: the section at {args.baseline} could "
                        f"not be read ({base_errors[0][1]})",
                    )
                )
                continue
            was = len(base_open) + len(base_closed)
            now = len(open_rows) + len(closed_rows)
            if now < was:
                deleted.append(
                    annotate(
                        "error",
                        rel,
                        1,
                        f"{was} rows at {args.baseline}, {now} here. An item leaves "
                        f"this table by being marked {CLOSED} with what closed it, "
                        "never by being deleted",
                    )
                )

    if args.baseline:
        prefixes = sorted({repo_relative(real(p), root) for p in args.path})
        here = {repo_relative(f, root) for f in files}
        for rel in overviews_at(root, args.baseline, prefixes):
            if rel not in here:
                # Relative to the caller's directory, like every other line
                # this prints. The two deletion reports used to answer on
                # different footings, which only agreed when the command ran
                # from the repository root.
                deleted.append(
                    annotate(
                        "error",
                        display_path(os.path.join(root, rel), cwd),
                        1,
                        f"present at {args.baseline} and not here. Whatever it "
                        "recorded as unverified left with it — a renamed "
                        "directory reads the same way, and says so out loud "
                        "rather than dropping the rows",
                    )
                )

    if not files and not deleted:
        print(
            f"unverified-check: no {OVERVIEW} found under "
            f"{', '.join(args.path)} — nothing was checked",
            file=sys.stderr,
        )
        return 2

    print(
        f"\n{len(unique_by_target(files))} overviews · {total_open} open"
        f" · {total_closed} closed"
        f" · {len(bad)} unreadable"
        + (f" · {len(uncompared)} not compared" if uncompared else "")
    )

    if uncompared:
        print(f"\nnot compared against {args.baseline}:")
        for line in uncompared:
            print(line)

    if bad:
        print("\nthe record could not be read as it stands:")
        for line in bad:
            print(line)
        print(
            "\nThis is not a report of zero open items. A section this cannot "
            "read is a section whose count is unknown."
        )
    if deleted:
        print("\nrows left the record without being closed:")
        for line in deleted:
            print(line)
        print(
            "\nRe-add the row with " + CLOSED + " and what closed it. Deleting "
            "and verifying have to look different, or they are the same edit."
        )
    if bad or deleted:
        return 1

    if total_open == 0:
        print(f"open: 0 — every recorded item carries {CLOSED} and what closed it.")
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
