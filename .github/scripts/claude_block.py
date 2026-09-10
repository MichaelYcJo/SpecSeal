#!/usr/bin/env python3
"""Keep the repository's `CLAUDE.md` block identical to its one source.

The block between `<!-- specseal:start -->` and `<!-- specseal:end -->` is
what `install.sh` puts into a user's `CLAUDE.md`, and it used to be read out
of this repository's own `CLAUDE.md` -- a file that also carries the
repository's house rules, and that every session here loads. Issue #292
measured that copy against an installed one and found `## Git` 95 % identical:
one sentence had moved in one and not the other, and nothing read both.

So the block lives in `templates/claude-md-block.md`, markers included, and
this script keeps the repository's copy equal to it:

  claude_block.py --write    regenerate the region inside CLAUDE.md from it
  claude_block.py --check    exit 1 naming the first line that differs

`install.sh` reads the template directly, the `preset-setup` and `update`
skills name it, and the hygiene workflow runs `--check` on every pull
request. The repository's `CLAUDE.md` keeps the generated copy by the owner's
answer (`seal/specs/1788993115-*/questions.md` Q1): a contributor without the
plugin still has to read the rules.

Exit codes. 0: the two agree, or `--write` made them agree. 1: they differ
(`--check` only). 2: a file the script cannot read, a target with no markers
-- which is not a disagreement but a file the script cannot place a block in;
placing one is `install.sh`'s act, on a user's file, with a backup -- or an
interpreter below the floor, where nothing is read and nothing is written.

The region is cut the way `install.sh`'s `awk` cuts it: from the line holding
the start marker through the line holding the end marker, inclusive. Both
files go through the same cut, so a template that someday carries a comment
above its markers still names the same bytes the installer ships.

Line endings are the target's. A checkout with `autocrlf=true` holds
`CLAUDE.md` with CRLF endings; the two blocks are compared without their
endings, and `--write` gives the template's lines the ending the target
already has, so nothing outside the region moves -- reading and writing with
newline translation used to turn every line of the file into the platform's
ending, the block and the owner's rules below it alike (#292 round 1).
"""

import argparse
import os
import sys

# **The floor is one number, and this is another carrier of it.** The block
# below is `skills/code-review/scripts/round_record.py`'s, copied as that
# file says it should be: after the imports, no syntax newer than the oldest
# interpreter it means to catch, and before every other module-level act.
# `tests/test_a_script_says_which_interpreter_it_needs.py` pins the number to
# the runner's and to ruff.toml's.
FLOOR = (3, 12)
FLOOR_TEXT = ".".join(str(part) for part in FLOOR)
BELOW_FLOOR = (
    "claude-block: needs python {floor} or newer, and this is python {found} "
    "at {executable}.\n"
    "Nothing was read and nothing was written.\n"
    "`python3` is not always the newest interpreter installed -- macOS ships "
    "python 3.9 under that name -- so name one explicitly, `python{floor} "
    "<this script> ...`, or see CONTRIBUTING.md section 'Running the checks'."
)


def below_floor(version=None, executable=None):
    """The sentence for an interpreter under the floor, or None above it."""
    version = tuple(sys.version_info[:3]) if version is None else tuple(version)
    if version[:2] >= FLOOR:
        return None
    return BELOW_FLOOR.format(
        floor=FLOOR_TEXT,
        found=".".join(str(part) for part in version),
        executable=sys.executable if executable is None else executable,
    )


_refusal = below_floor()
if _refusal:
    sys.stderr.write(_refusal + "\n")
    raise SystemExit(2)


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEMPLATE = os.path.join(ROOT, "templates", "claude-md-block.md")
TARGET = os.path.join(ROOT, "CLAUDE.md")
START = "<!-- specseal:start -->"
END = "<!-- specseal:end -->"
NAME = "claude-block"


class NoBlock(Exception):
    """The file holds no marker region this script can name."""


def region(lines):
    """`(first, last)` indexes of the marker lines, inclusive.

    A start marker with no end marker after it is a damaged block, refused
    the way `install.sh` refuses it: editing would silently take everything
    after the start marker with it.
    """
    first = next((i for i, line in enumerate(lines) if START in line), None)
    if first is None:
        raise NoBlock(f"no `{START}` marker")
    last = next((i for i, line in enumerate(lines[first:], first) if END in line), None)
    if last is None:
        raise NoBlock(f"a `{START}` marker with no `{END}` after it")
    return first, last


def read_lines(path, what):
    """The file's lines with the endings they have on disk: `newline=""`
    turns nothing into `\\n`, so a CRLF target is read as CRLF."""
    try:
        with open(path, encoding="utf-8", newline="") as f:
            return f.read().splitlines(keepends=True)
    except OSError as exc:
        raise NoBlock(f"cannot read the {what} at {shown(path)}: {exc}") from exc


def bare(line):
    """The line without its ending, which is what two copies are compared
    on: a CRLF checkout carries the same block as an LF one."""
    return line.rstrip("\r\n")


def ending_of(lines):
    """The ending a file uses -- CRLF when any line has one, else LF."""
    return "\r\n" if any(line.endswith("\r\n") for line in lines) else "\n"


def block(lines):
    first, last = region(lines)
    return lines[first : last + 1]


def first_difference(wanted, found):
    """`(index, wanted line, found line)` of the first line that differs, or
    None when the two blocks are identical.

    No branch for one block being a prefix of the other: `block()` cuts both
    at the line holding the end marker, so a block with a line more or fewer
    differs at some line before the shorter one runs out -- the marker line
    itself, at the latest. A `<end of block>` branch was written for that
    shape, and a mutation sweep found it dead.
    """
    for i in range(min(len(wanted), len(found))):
        if bare(wanted[i]) != bare(found[i]):
            return i, wanted[i], found[i]
    return None


def shown(path):
    """The path as the reader will look for it: relative to the working
    directory when it is under it, which in CI is the repository root."""
    rel = os.path.relpath(path)
    return path if rel.startswith("..") else rel


def quote(line):
    return bare(line)


def check(template_path, target_path, out):
    wanted = block(read_lines(template_path, "template"))
    target = read_lines(target_path, "target")
    first, _ = region(target)
    found = block(target)
    diff = first_difference(wanted, found)
    template, copy = shown(template_path), shown(target_path)
    if diff is None:
        out.write(f"{NAME}: {copy} carries the block {template} holds\n")
        return 0
    i, a, b = diff
    out.write(
        f"{NAME}: the block in {copy} differs from {template} "
        f"at block line {i + 1} ({copy}:{first + i + 1})\n"
        f"  template: {quote(a)}\n"
        f"  copy:     {quote(b)}\n"
        f"Edit the template, then `python3 {shown(__file__)} --write` "
        "regenerates the copy.\n"
    )
    return 1


def write(template_path, target_path, out):
    wanted = block(read_lines(template_path, "template"))
    target = read_lines(target_path, "target")
    first, last = region(target)
    template, copy = shown(template_path), shown(target_path)
    wanted = [bare(line) + ending_of(target) for line in wanted]
    if target[first : last + 1] == wanted:
        out.write(f"{NAME}: {copy} already carries the block; nothing written\n")
        return 0
    with open(target_path, "w", encoding="utf-8", newline="") as f:
        f.write("".join(target[:first] + wanted + target[last + 1 :]))
    out.write(f"{NAME}: wrote the block from {template} into {copy}\n")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog=NAME,
        description="keep the CLAUDE.md marker block identical to templates/claude-md-block.md",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="exit 1 when the two differ")
    mode.add_argument(
        "--write", action="store_true", help="regenerate the copy from the template"
    )
    parser.add_argument(
        "--template", default=TEMPLATE, help="the block, markers included"
    )
    parser.add_argument(
        "--target", default=TARGET, help="the file holding the generated copy"
    )
    args = parser.parse_args(argv)
    try:
        if args.check:
            return check(args.template, args.target, sys.stdout)
        return write(args.template, args.target, sys.stdout)
    except NoBlock as exc:
        sys.stderr.write(f"{NAME}: {exc}\nNothing was written.\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
