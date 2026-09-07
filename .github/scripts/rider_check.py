#!/usr/bin/env python3
"""Does every rider still say what state it was verified against?

A rider is a `RIDER:` comment planted at the coordinate it is about, and
`seal/follow-up.md` explains why it lives there instead of in a list. Its cost
is that nothing forces it to be deleted, so a spent rider looks exactly like a
live one; the stamp on it is the mitigation.

**The stamp used to name a commit, and this repository's merge rule destroys
the commits it had to name.** A fix pass runs on a feature branch, a feature
branch squashes into its release branch, and the squash keeps none of the
branch's own commits. The check then failed on the RELEASE branch, so whoever
repaired it was never whoever caused it, and no mistake was required for any of
it (#239). `skills/evidence-check/SKILL.md` already cites that exact failure as
one of the four grounds for deriving a ledger anchor from content rather than
writing a marker into the source, and `CLAUDE.md` states the rule that came out
of it. The ledger got the repair; the mechanism that supplied the evidence did
not, until here.

So a stamp names content:

    Verified 2026-09-08 against repo_root@1a2b3c4d

`repo_root` is the ledger's own anchor vocabulary -- a dotted Python symbol
name, a markdown heading path, or a quoted distinctive line -- resolved by
`evidence_check.resolve_unit` against the rider's OWN file. The hash is
`evidence_check.content_hash` of the region that anchor names.

**The path the ledger writes is left off, and that is the only departure.** A
ledger row is not in the file it cites, so it needs one. A rider IS the
coordinate, so the path would restate what the comment's location already says,
and a rename would need two edits for one move.

## The residual: a rider is inside the file it is about

Its own text is part of that file's content, so a hash covering the rider would
be written into the region it hashes and no fixed point would exist. Measured
when this was designed: twelve of the nineteen riders in the tree sat inside the
AST span of the unit they were about, so this is the dominant case and not a
corner.

**Every rider block in the region is removed before the region is hashed** --
not merely the one being stamped. Three properties follow, and the second and
third are why the rule is `every`:

  the stamp sits inside a block, so it is excluded, so the fixed point exists;

  editing a rider's own prose does not drift it. A rider's wording is not what
  it verified, and reporting a clarification as a code change would be false;

  planting a second rider in a unit does not drift the first. Three files
  already carry more than one, and a design where riders perturb each other
  gets worse the more the convention is used.

What it gives up: a change consisting only of adding or removing a comment
inside the unit goes unnoticed. For rider blocks that is the intent. For an
ordinary comment butted against one with no blank line between, it is
over-exclusion, because a block is read as the run of comment lines starting at
the `RIDER:` line and absorbs whatever follows it. Both failures lose an alarm
rather than inventing one.

## The verdicts, and why drift is loud

  OK       the anchor resolves once and the hash is what the stamp recorded
  DRIFTED  it resolves and the content changed -- re-read the rider, re-stamp
  BROKEN   it resolves to nothing, to several places, or only by resurrection

DRIFTED is the ledger's degradation and it is right here for a sharper reason
than that it is right there: a drifted rider IS the rider firing. It says
somebody edited the unit and did not answer the comment sitting in it, which is
the arrival `seal/follow-up.md` moved riders to their coordinates to get.

Both fail. `evidence_check` exits 1 on drift, so a rider that only warned would
be the looser of two rules about one thing -- and answering a drifted rider is
re-reading a comment in the file you just edited plus one command, where
answering an orphaned commit was bookkeeping with no reading in it at all.

**Resurrection is refused here where the ledger tolerates it.** A resurrected
place survives only because the declaration rule put keyword-blocked candidates
back, and `evidence_check` carries that uncertainty out to its caller. The
ledger tolerates it because its rows were bulk-migrated off line numbers. A
rider is hand-written by somebody standing at the coordinate, who can pick a
better anchor.

Usage:
  rider_check.py                  check every rider; exit 1 on drift, 2 on broken
  rider_check.py --migrate        one-shot: rewrite `at <sha>` stamps as anchors
  rider_check.py --reverify       recompute every hash and set today's date
  rider_check.py --reverify --only PATH   the same, for one file

`--migrate` consults the old stamp's commit before it trusts anything, exactly
as `evidence_check.py --migrate` does and for the same reason: a date says when
a person read the claim and a hash says what they read, so the two are true
together or not at all. Where the region at the stamped commit still hashes to
what it hashes today, the original date is kept, because nothing has changed
since it was earned. Where it does not, the rider is REFUSED and named -- the
content moved after it was verified, and only a person re-reading it can say
the claim still holds.
"""

import argparse
import datetime
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CHECKER = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")

# Where a rider may live. Every root that holds something this repository
# executes or ships, and none that holds prose ABOUT riders -- `docs/`,
# `CLAUDE.md` and `seal/` describe the convention and quote the marker, and a
# description is not a rider.
#
# `.github` and `tests` were missing until #239. Three riders sat outside the
# scan and were held to nothing at all: one in `.github/scripts/fold_ledger.py`
# and two under `tests/`, one of which had never been given a stamp in any form.
# That is the same shape as `templates` having been missing before it, which is
# the second time this list was the defect rather than the corpus.
RIDER_ROOTS = (".github", "agents", "hooks", "skills", "templates", "tests")

# Directories no walk here descends. `__pycache__` carries a compiled copy of a
# module that holds a rider, and a walk that reads one answers for the file.
SKIP_DIRS = frozenset({".git", "__pycache__", ".venv", "venv", "node_modules"})

READABLE = (".py", ".md", ".yml", ".yaml", ".sh", ".toml", ".cfg", ".txt")

MARKER = "RIDER:"

# `Verified <date> at <sha>` -- what a stamp said before #239. Kept so the
# checker can name it and say what it costs, never so it can pass.
OLD_STAMP = re.compile(
    r"Verified (?P<date>\d{4}-\d{2}-\d{2}) at (?P<sha>[0-9a-f]{7,40})\b"
)

# `Verified <date> against <anchor>@<hash>`. The locator alternatives and the
# hash width are `evidence_check.ANCHOR_RE`'s, minus the path.
NEW_STAMP = re.compile(
    r"Verified (?P<date>\d{4}-\d{2}-\d{2}) against "
    r"(?P<locator>\"(?:[^\"\n]|\\\")+\"|[A-Za-z_][A-Za-z0-9_.]*)"
    r"@(?P<hash>[0-9a-f]{6,12})"
)


def load_checker(path=CHECKER):
    """`evidence_check` as a module, or a sentence and exit 2.

    A missing file is a sentence naming the path rather than the
    `FileNotFoundError` `spec_from_file_location` hands back for any name
    ending in `.py`, present or not. That shape is `round_record.py`'s own
    open rider, and copying the defect into a new file to keep the two
    matching would be the wrong half to be consistent with.
    """
    if not os.path.isfile(path):
        sys.stderr.write(
            f"rider_check: cannot find the anchor resolver at {path}. It is the "
            "shipped `evidence_check.py`; restore it or pass the checker a "
            "different root\n"
        )
        raise SystemExit(2)
    spec = importlib.util.spec_from_file_location("evidence_check", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def comment_blocks(lines):
    """[(start, end)] 1-based inclusive for every rider block in `lines`.

    A block opens at a line that both carries the marker and IS a comment: a
    `#` comment in Python, YAML and shell, or an HTML comment in markdown. That
    condition is what keeps the marker's own name out of the corpus -- this
    file, `tests/test_a_rider_reaches_its_file.py` and `seal/follow-up.md` all
    contain the string while describing it, always inside a string literal, a
    table cell or running prose, and never at the head of a comment.

    A `#` block runs while the following lines are comment lines, so a bare `#`
    continuation line inside a rider carries it on. An HTML block runs to its
    closing marker.
    """
    out = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if MARKER not in line:
            i += 1
            continue
        stripped = line.lstrip()
        if "<!--" in line:
            j = i
            while j < n and "-->" not in lines[j]:
                j += 1
            end = min(j, n - 1)
        elif stripped.startswith("#"):
            j = i
            while j + 1 < n and lines[j + 1].lstrip().startswith("#"):
                j += 1
            end = j
        else:
            i += 1
            continue
        out.append((i + 1, end + 1))
        i = end + 1
    return out


class Rider:
    """One rider block, and whatever its stamp says."""

    def __init__(self, rel, start, end, text):
        self.rel = rel
        self.start = start
        self.end = end
        self.body = "\n".join(text.splitlines()[start - 1 : end])
        self.old = OLD_STAMP.search(self.body)
        self.new = NEW_STAMP.search(self.body)

    def where(self):
        return f"{self.rel}:{self.start}"


def riders_in(rel, text):
    return [Rider(rel, a, b, text) for a, b in comment_blocks(text.splitlines())]


def tree_files(root, roots=RIDER_ROOTS):
    """Every readable file under the rider roots, sorted."""
    found = []
    for top in roots:
        base = os.path.join(root, top)
        if not os.path.isdir(base):
            continue
        for here, dirs, names in os.walk(base):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for name in sorted(names):
                if name.endswith(READABLE):
                    found.append(os.path.relpath(os.path.join(here, name), root))
    return sorted(found)


def all_riders(root, roots=RIDER_ROOTS):
    out = []
    for rel in tree_files(root, roots):
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                text = f.read()
        except (OSError, UnicodeDecodeError):
            continue
        if MARKER not in text:
            continue
        out.extend(riders_in(rel, text))
    return out


def region_lines(checker, rel, locator, text):
    """(lines the hash covers, None) or (None, why not).

    The anchored region with every rider block taken out of it. The blocks are
    removed by LINE NUMBER rather than by content, so two riders carrying the
    same sentence do not remove each other's lines.
    """
    places, resurrected = checker.resolve_unit(rel, locator, text)
    if not places:
        return None, "the anchor resolves to nothing in this file"
    if len(places) > 1:
        return None, f"the anchor resolves to {len(places)} places, so it names none"
    if resurrected:
        return None, (
            "the anchor survives only because the declaration rule put a "
            "keyword-blocked candidate back, so it may be a call site rather "
            "than the unit. Pick a more distinctive anchor"
        )
    start, end = places[0]
    lines = text.splitlines()
    blocks = comment_blocks(lines)
    kept = [
        line
        for number, line in enumerate(lines[start - 1 : end], start)
        if not any(a <= number <= b for a, b in blocks)
    ]
    if not kept:
        return None, (
            "the anchor names a region that is entirely rider comment, so "
            "there is no content under it to hash"
        )
    return kept, None


def region_hash(checker, rel, locator, text):
    kept, why = region_lines(checker, rel, locator, text)
    if kept is None:
        return None, why
    return checker.content_hash(kept), None


def check(root, roots=RIDER_ROOTS, checker=None):
    """(ok, drifted, problems) — `problems` is [(where, severity, sentence)]."""
    checker = checker or load_checker()
    ok, drifted, problems = 0, 0, []
    for rider in all_riders(root, roots):
        with open(os.path.join(root, rider.rel), encoding="utf-8") as f:
            text = f.read()
        if rider.old and not rider.new:
            problems.append(
                (
                    rider.where(),
                    "BROKEN",
                    "the stamp names a commit ({}). A feature branch squashes "
                    "into its release branch and the squash keeps none of its "
                    "commits, so this resolves to nothing for whoever reads it "
                    "next. Run `rider_check.py --migrate`".format(
                        rider.old.group("sha")
                    ),
                )
            )
            continue
        if not rider.new:
            problems.append(
                (
                    rider.where(),
                    "BROKEN",
                    "no verification stamp. A rider with none cannot be told "
                    "from a spent one, which is the whole cost "
                    "`seal/follow-up.md` accepts the convention against. Add "
                    "`Verified <date> against <anchor>@<hash>`",
                )
            )
            continue
        want = rider.new.group("hash")
        got, why = region_hash(checker, rider.rel, rider.new.group("locator"), text)
        if got is None:
            problems.append((rider.where(), "BROKEN", why))
        elif got != want:
            drifted += 1
            problems.append(
                (
                    rider.where(),
                    "DRIFTED",
                    "`{}` changed since this was verified on {} ({} -> {}). "
                    "Read the rider — that is what it is for — then either do "
                    "what it asks and delete it, or "
                    "`rider_check.py --reverify --only {}`".format(
                        rider.new.group("locator"),
                        rider.new.group("date"),
                        want,
                        got,
                        rider.rel,
                    ),
                )
            )
        else:
            ok += 1
    return ok, drifted, problems


def content_at(root, sha, rel):
    """The file as the stamped commit held it, or None where git cannot say."""
    try:
        run = subprocess.run(
            ["git", "-C", root, "show", f"{sha}:./{rel}"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return run.stdout if run.returncode == 0 else None


def restamp(body, date, locator, digest):
    """`body` with its stamp replaced by the new form, once."""
    new = f"Verified {date} against {locator}@{digest}"
    if NEW_STAMP.search(body):
        return NEW_STAMP.sub(lambda m: new, body, count=1)
    return OLD_STAMP.sub(lambda m: new, body, count=1)


def write_block(root, rider, body):
    path = os.path.join(root, rider.rel)
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines(True)
    ending = "\n" if lines and lines[-1].endswith("\n") else ""
    tail = lines[rider.end :]
    replacement = [line + "\n" for line in body.splitlines()]
    if not tail and ending == "":
        replacement[-1] = replacement[-1].rstrip("\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(lines[: rider.start - 1] + replacement + tail))


def reverify(root, only=None, roots=RIDER_ROOTS, today=None, checker=None):
    """Recompute every resolvable hash and set the date to today.

    Explicitly "I have re-read these", never something the check does — the
    same act and the same reason as `evidence_check.py --reverify`. The date
    moves BECAUSE the hash does: a date says when a person read the claim and a
    hash says what they read, so writing one without the other leaves a stamp
    asserting a reading that never happened.
    """
    checker = checker or load_checker()
    today = today or datetime.date.today().isoformat()
    written, refused = [], []
    for rider in all_riders(root, roots):
        if only and rider.rel != only:
            continue
        if not rider.new:
            refused.append(
                (rider.where(), "no anchor to recompute — `--migrate` first")
            )
            continue
        with open(os.path.join(root, rider.rel), encoding="utf-8") as f:
            text = f.read()
        digest, why = region_hash(checker, rider.rel, rider.new.group("locator"), text)
        if digest is None:
            refused.append((rider.where(), why))
            continue
        if digest == rider.new.group("hash") and today == rider.new.group("date"):
            continue
        write_block(
            root, rider, restamp(rider.body, today, rider.new.group("locator"), digest)
        )
        written.append((rider.where(), digest))
    return written, refused


def inferred_anchor(checker, rel, text, rider):
    """The unit a rider is about, where the file's own structure names one.

    The innermost Python unit whose span holds the rider, and otherwise the
    unit the block sits immediately above — which is where a rider about a
    whole definition goes. Anything else is returned as None and written by
    hand: choosing what a rider is ABOUT is a judgment, and a migration that
    guessed it would put a hash behind a claim nobody made.
    """
    if not rel.endswith(".py"):
        return None
    spans = checker.py_spans(text)
    if not spans:
        return None
    holding = []
    for name, places in spans.items():
        for start, end in places:
            if start <= rider.start and rider.end <= end:
                holding.append((end - start, name))
    if holding:
        return sorted(holding)[0][1]
    below = []
    for name, places in spans.items():
        for start, _end in places:
            if start > rider.end:
                below.append((start, name))
    if not below:
        return None
    first = sorted(below)[0]
    lines = text.splitlines()
    between = lines[rider.end : first[0] - 1]
    return first[1] if not any(line.strip() for line in between) else None


def migrate(root, roots=RIDER_ROOTS, checker=None):
    """One shot: `at <sha>` becomes `against <anchor>@<hash>`.

    The old stamp's commit is consulted before anything is written, the way
    `evidence_check.py --migrate` consults it before trusting a line number. A
    region that hashes at that commit to what it hashes today has not moved
    since the rider was earned, so the ORIGINAL date is kept — the reading it
    records really did happen against this content.

    Where they differ, or where git can no longer answer, the rider is REFUSED
    and named. The content moved after somebody verified it, and only a person
    re-reading the claim can say whether it still holds; writing today's date
    over it would manufacture a reading.
    """
    checker = checker or load_checker()
    written, refused = [], []
    for rider in all_riders(root, roots):
        if rider.new or not rider.old:
            continue
        path = os.path.join(root, rider.rel)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        anchor = inferred_anchor(checker, rider.rel, text, rider)
        if not anchor:
            refused.append(
                (
                    rider.where(),
                    "no unit encloses this rider and none sits directly under "
                    "it, so what it is ABOUT is a judgment. Write the anchor "
                    "by hand, then `--reverify`",
                )
            )
            continue
        digest, why = region_hash(checker, rider.rel, anchor, text)
        if digest is None:
            refused.append((rider.where(), f"{anchor}: {why}"))
            continue
        was = content_at(root, rider.old.group("sha"), rider.rel)
        if was is None:
            refused.append(
                (
                    rider.where(),
                    "git cannot resolve {} any more, which is the defect this "
                    "migration removes and also what stops it proving the "
                    "date. Re-read the rider and `--reverify`".format(
                        rider.old.group("sha")
                    ),
                )
            )
            continue
        then, _ = region_hash(checker, rider.rel, anchor, was)
        if then != digest:
            refused.append(
                (
                    rider.where(),
                    "`{}` has changed since {}, so that date records a reading "
                    "of different content. Re-read the rider, then "
                    "`--reverify`".format(anchor, rider.old.group("date")),
                )
            )
            continue
        write_block(
            root, rider, restamp(rider.body, rider.old.group("date"), anchor, digest)
        )
        written.append((rider.where(), f"{anchor}@{digest}"))
    return written, refused


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--migrate", action="store_true")
    parser.add_argument("--reverify", action="store_true")
    parser.add_argument("--only", default=None, help="one path, for --reverify")
    args = parser.parse_args(argv)
    checker = load_checker()

    if args.migrate:
        written, refused = migrate(args.root, checker=checker)
        for where, what in written:
            print(f"migrated {where} -> {what}")
        for where, why in refused:
            print(f"REFUSED  {where}: {why}")
        print(f"{len(written)} migrated · {len(refused)} refused")
        return 1 if refused else 0

    if args.reverify:
        written, refused = reverify(args.root, only=args.only, checker=checker)
        for where, digest in written:
            print(f"restamped {where} -> {digest}")
        for where, why in refused:
            print(f"REFUSED   {where}: {why}")
        print(f"{len(written)} restamped · {len(refused)} refused")
        return 1 if refused else 0

    ok, drifted, problems = check(args.root, checker=checker)
    for where, severity, sentence in problems:
        print(f"{severity:<8} {where}: {sentence}")
    broken = len(problems) - drifted
    print(f"{ok} ok · {drifted} drifted · {broken} broken")
    if broken:
        return 2
    return 1 if drifted else 0


if __name__ == "__main__":
    raise SystemExit(main())
