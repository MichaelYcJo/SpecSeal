#!/usr/bin/env python3
"""Draw the release's seal as a PNG, attach it, and put it in the note (#718).

The 0.17.0 seal was drawn by hand, and from #718 to #832 this script drew it
the same way: the terminal stamp's cells painted one rectangle per half-cell.
That made every edge a staircase and the emblem a block mosaic, which is
what #832 opened on.

**The seal is the owner's SVG** (#832). `SVG`, `release-seal.svg` beside
this file, is the owner's 32 x 32 seal: radial-gradient wax, a rim, a pressed
groove, and the seal's mark with a shadow and a highlight. The owner drew a
Georgia Bold §; the mark is the terminal stamp's placeholder, Georgia Bold's
S, until #857 chooses it, and the release image follows the terminal's. Its
three layers were turned into `<path>` outlines once, on a machine that has
the face, because the runner has no Georgia and a fallback serif would draw
a different glyph. `rasterise` hands it to `rsvg-convert` at `SEAL_PX` times
`DENSITY` pixels square, and the note shows it `SEAL_PX` wide, so a
high-density screen draws it sharp.

**`rsvg-convert` is a release dependency, never a plugin one.** It comes from
`librsvg2-bin`, a system package the `seal` job installs with `apt-get`
(`.github/workflows/publish-release.yml`). Nothing under `hooks/` or
`skills/` imports this file or calls the binary, and this file imports no
third-party module: the gates are stdlib-only (`CONTRIBUTING.md` §*Running
the checks*). The suite reads the PNG it draws with Pillow, pinned in
`.github/scripts/run_tests.py#PILLOW`, in one case that skips where the
binary is absent.

**The rows are a fixed set, read from what the tag carries.** The suite's
counts come from the record the broad gate's recorder wrote for the run at
the tag, read by the broad gate's own reader and counter (`suite_counts`),
the pull requests and their `chain: capped` labels from the one `gh pr list`
call the note already makes, and the work items, rounds and deferred issues
from the round records at the tag, through the readers the review chain's
own gates use (`chain_counts`). A source that cannot be read says `not read`
in its row.

**Any failure leaves the note as it was published.** `.github/workflows/
publish-release.yml` runs this in its `seal` job, after `publish` created
the release in the same run. The note is already out by then, so a seal that
cannot be drawn costs the image and never the counts -- the rule
`publish_release_note.py`'s docstring states for its summary. Every failure
here is one log line and one `::warning::` with an exit of 0, and nothing is
edited unless the glance table is still in the note exactly as `glance`
wrote it: a note somebody edited after publication is left alone, and so is
its asset list. The upload comes before the edit, so an edit that fails
leaves an attached image the note does not show, which the warning names.

`DRY_RUN=1` draws the PNG at `SEAL_PNG` (by default `seal.png` in a
temporary directory), prints the rows and the note it would write, and
uploads and edits nothing, so the seal of a release whose job did not run can
be drawn by hand from a checkout at the tag, on a machine with
`rsvg-convert`, attached with `gh release upload` and shown with
`gh release edit --notes-file`.

Environment: `TAG`, `REPO`, `GH_TOKEN`, `SUITE_RECORDS` (the directory the
recorder wrote in) and `SUITE_KEY` (the key the run at the tag was handed),
`SUITE_OUTCOME` (the suite step's outcome), `DRY_RUN`, `SEAL_PNG`.

Exit code: 0, always.
"""

import functools
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
# Where this file's own repository is, which the modules below are loaded
# from; and the tree whose round records the chain rows read. They are the
# same checkout at the tag, and two names so a case can point the second at
# a fixture without moving the first.
CODE = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = CODE


# The tree's own modules are loaded when first asked for, not at import: a
# module that will not load is one more way for the seal to fail, and every
# way it fails has to end in today's note and an exit of 0 (`main`), which an
# import at the top of this file would end before `main` ran.
def module(name, *parts):
    """The repository's module at `CODE/<parts>`, loaded once under `name`."""
    return _module(name, os.path.join(CODE, *parts))


@functools.cache
def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def publisher():
    """`.github/scripts/publish_release_note.py`, which owns the note's
    glance block, the pull request list and how a release is counted."""
    return module(
        "specseal_publish_release_note", ".github", "scripts", "publish_release_note.py"
    )


# The owner's seal (#832), beside this file because this file is its one
# reader. Its text is paths, so drawing it looks up no font.
SVG = os.path.join(HERE, "release-seal.svg")
# The seal's width and height on the release page, in CSS pixels, and how
# many PNG pixels it is drawn with per CSS pixel. The note's `<img>` carries
# `SEAL_PX`, and the PNG is `SEAL_PX * DENSITY` square, so a screen at twice
# the density draws it from pixels it has rather than by stretching them.
SEAL_PX = 160
DENSITY = 2


# --- the rows ------------------------------------------------------------
#
# A release's panel is a fixed set of rows, held here as one constant: the
# owner's 0.17.0 seal is the drawing, and a label the code composed from free
# text could grow past the eight-wide label column the panel was drawn in, and
# a dry run still prints the rows in. That column is `{label:<8}`, not the
# longest label: `deferred` is exactly eight, which is the only reason the
# column looked set by it. Since #832 the image carries no rows: they reach
# the note as its alt text (`alt_text`).
LABELS = ("SEALED", "tag", "PRs", "issues", "suite", "items", "capped", "deferred")
# The widest value a release's panel carries before the frame would cut it.
# It was `skills/verify/scripts/broad_gate.py#PANEL_VALUE_WIDTH` until #832
# widened the gate's to 41 for the open layout's 80 columns; a release's rows
# were out of that work item's scope, so this one stays 23, and the case that
# held the two to one number holds this one apart from the gate's.
PANEL_VALUE_WIDTH = 23
# What a row says when the source it is read from could not be read: the row
# stays, because a dropped row reads as none and a 0 reads as a count
# (`questions.md` Q8).
NOT_READ = "not read"
# The label the review chain puts on a pull request whose run ended at the
# round cap (`docs/review-chain-spec.md`).
CAPPED_LABEL = "chain: capped"


def plural(count, word):
    return f"{count} {word}{'' if count == 1 else 's'}"


def release_rows(version, sha, pulls_n, issues_n, suite, chain):
    """The panel's rows for a release, `(label, value)` with `""` for a
    continuation, in `LABELS`' order.

    `suite` is `(passed, skipped)`; `chain` is `chain_counts`' four, each a
    number or None for not read. A suite value wider than
    `PANEL_VALUE_WIDTH` moves `S skipped` to a continuation row under
    `P passed` (`questions.md` Q6): only the suite can overflow, a five-digit
    count and a three-digit skip being 25. The items row needs both its
    numbers and the capped row both of its own, so either missing says
    `not read`."""
    items, rounds, capped, deferred = chain
    passed, skipped = suite
    rows = [
        ("SEALED", f"v{version}"),
        ("tag", sha[:8]),
        ("", "main"),
        ("PRs", f"{pulls_n} merged"),
        ("issues", f"{issues_n} closed"),
    ]
    whole = f"{passed} passed, {skipped} skipped"
    if len(whole) <= PANEL_VALUE_WIDTH:
        rows.append(("suite", whole))
    else:
        rows += [("suite", f"{passed} passed"), ("", f"{skipped} skipped")]
    rows += [
        (
            "items",
            NOT_READ
            if items is None or rounds is None
            else f"{items} . {plural(rounds, 'round')}",
        ),
        (
            "capped",
            NOT_READ if capped is None or items is None else f"{capped} of {items}",
        ),
        ("deferred", NOT_READ if deferred is None else plural(deferred, "issue")),
    ]
    return rows


def alt_text(rows):
    """One sentence carrying every value of `rows`, in the shape of the alt
    text written by hand for 0.17.0's seal, for a reader whose browser does
    not draw the image. No `]`, `[` or line break is let through: the text
    was first written into a Markdown image, which any of them ends early.
    Since #832 it sits in an `<img>`'s `alt`, and `sealed_glance` escapes it
    for that attribute."""
    by = {}
    for label, value in rows:
        if label:
            by[label] = [value]
            last = label
        else:
            by[last].append(value)
    sealed, tag = by["SEALED"][0], by["tag"]
    first = f"The {sealed.removeprefix('v')} release seal: SEALED {sealed} at {tag[0]}"
    suite = [part.strip() for value in by["suite"] for part in value.split(",")]
    parts = [
        first + "".join(f" on {more}" for more in tag[1:]),
        plural(int(by["PRs"][0].split()[0]), "pull request") + " merged",
        plural(int(by["issues"][0].split()[0]), "issue") + " closed",
        "the suite at " + " and ".join(suite),
    ]
    items, capped, deferred = by["items"][0], by["capped"][0], by["deferred"][0]
    if items == NOT_READ:
        parts.append("work items not read")
    else:
        count, rounds = items.split(" . ")
        rounds = rounds.replace("round", "review round")
        parts.append(f"{plural(int(count), 'work item')} over {rounds}")
    if capped == NOT_READ:
        parts.append("capped not read")
    else:
        parts.append(f"{capped.split()[0]} of them capped")
    parts.append(
        "deferred not read" if deferred == NOT_READ else f"{deferred} deferred"
    )
    return re.sub(r"[\]\[\r\n]+", " ", ", ".join(parts))


# --- the sources ---------------------------------------------------------


def gate():
    """`skills/verify/scripts/broad_gate.py`, whose reader and counter the
    broad gate's panel reads the same record with (#869): one counter for the
    panel and the release, and no second reader of what pytest printed."""
    return module(
        "specseal_broad_gate_for_release_seal",
        "skills",
        "verify",
        "scripts",
        "broad_gate.py",
    )


def suite_counts(directory, key):
    """`(passed, skipped)` from the record the broad gate's recorder wrote
    under `directory` for the sessions carrying `key` (#869).

    The run at the tag loads the recorder as the broad gate loads it
    (`.github/workflows/publish-release.yml`), and `broad_gate.read_record`
    counts each report under the category pytest's own summary line counts
    it under. Raises `ValueError` where no directory or no key is named,
    where no session carries the key, where a line of a keyed record did not
    parse, where a session stopped part-way, where a test or a collection
    had no file of its own and so counts under no category (`unplaced`),
    or where the counts hold a failure or an error -- a `SEALED` above a red
    or a short suite would be false, and a record nobody can read is never a
    zero."""
    if not directory:
        raise ValueError("SUITE_RECORDS names no directory")
    if not key:
        raise ValueError("SUITE_KEY names no key")
    record = gate().read_record(directory, key, CODE)
    if not record.sessions:
        raise ValueError(f"no record under {directory} carries the key {key}")
    if record.unread:
        raise ValueError(
            f"{record.unread} of the lines under {directory} did not parse as "
            "the recorder's"
        )
    if record.unended:
        raise ValueError(
            f"{record.unended} of the suite's pytest sessions stopped part-way"
        )
    if record.unplaced:
        raise ValueError(
            f"{record.unplaced} of the suite's tests and collections had no "
            "file of their own and were counted under no category"
        )
    failed = record.counts.get("failed", 0)
    errors = record.counts.get("error", 0)
    if failed or errors:
        raise ValueError(
            f"the suite at the tag did not pass: {failed} failed and {errors} errors"
        )
    return record.counts.get("passed", 0), record.counts.get("skipped", 0)


def readers():
    """`(routing, chain_check, the markdown reader)`: the modules the review
    chain's own gates read round records with, so the counts here are the
    ones a gate would read and a change to where records live has to move
    these readers first."""
    return (
        module("specseal_routing", "hooks", "routing.py"),
        module(
            "specseal_chain_check", "skills", "code-review", "scripts", "chain_check.py"
        ),
        module(
            "specseal_unverified_reader",
            "skills",
            "verify",
            "scripts",
            "unverified_check.py",
        ),
    )


def labels_of(pull):
    return {
        (label.get("name") if isinstance(label, dict) else str(label)) or ""
        for label in pull.get("labels") or ()
    }


def chain_counts(root, pulls):
    """`(items, rounds, capped, deferred)` for the release's pull requests,
    each a number or None for not read, with the log saying why.

    `capped` counts the pull requests labelled `CAPPED_LABEL`. A pull request
    is a work item where exactly one `routing.md` under `root` names its head
    branch (`hooks/routing.py#item_dir`), and its rounds are
    `hooks/routing.py#rounds`. `deferred` is the number of distinct issues
    that are the home of a Verdicts cell whose verdict is `deferred`, read
    with `chain_check.verdict_table`, `#verdict_of`, `#deferred_home` and
    `#issue_of` (#866): a home names an issue only where it is exactly `#N`,
    so a file, the frame, or an issue mentioned in the note behind the home
    counts none. A round record whose verdict table cannot be read, or
    holds a row the table reader skipped, leaves `deferred` None -- an
    incomplete count is a wrong number -- a `rounds` that cannot be listed
    leaves `rounds` None as well, and a reader
    that will not load leaves all three tree counts None.

    A tree with no declaration at all, or a pull request labelled
    `CAPPED_LABEL` that resolves to no work item, is a count known to be
    incomplete -- records moved (#715) or retired before the tag -- so the
    three tree rows are not read rather than drawn as 0 (round 1's 🔴 1)."""
    capped = sum(1 for pull in pulls if CAPPED_LABEL in labels_of(pull))
    try:
        routing, chain, reader = readers()
    except Exception as problem:
        print(
            f"the chain rows are not read: the round-record readers did not load ({problem})"
        )
        return None, None, capped, None
    if not routing.declarations(root):
        print(
            "the chain rows are not read: no routing.md under "
            f"{root} declares a branch, so the round records are not where "
            "the readers look"
        )
        return None, None, capped, None
    items, rounds, deferred, unread, lost = 0, 0, set(), [], []
    rounds_unread = False
    for pull in pulls:
        item = routing.item_dir(root, pull.get("headRefName") or "")
        if not item:
            if CAPPED_LABEL in labels_of(pull):
                lost.append(f"#{pull.get('number')}")
            continue
        items += 1
        if routing.rounds_unreadable(item):
            # Its records exist and cannot be listed, so its rounds are not
            # zero; the rounds row is not read, and neither is deferred.
            rounds_unread = True
            unread.append(os.path.join(item, routing.ROUNDS_DIR))
            continue
        records = routing.rounds(item)
        rounds += len(records)
        for path in records:
            try:
                with open(path, encoding="utf-8") as handle:
                    text = handle.read()
            except (OSError, UnicodeDecodeError):
                unread.append(path)
                continue
            rows, col, _header, errors = chain.verdict_table(
                reader, reader.readable(text), path
            )
            # A row `verdict_table` skipped is a verdict nobody counted.
            if col < 0 or errors:
                unread.append(path)
                continue
            for _line, seen in rows:
                issue = chain.issue_of(chain.deferred_home(seen[col]))
                if issue is not None:
                    deferred.add(issue)
    if lost:
        print(
            f"the chain rows are not read: {', '.join(lost)} carry "
            f"{CAPPED_LABEL!r} and resolve to no work item under {root}"
        )
        return None, None, capped, None
    if unread:
        print(
            (
                "the rounds and deferred rows are"
                if rounds_unread
                else "the deferred row is"
            )
            + " not read: no verdict table could be read in "
            + ", ".join(os.path.relpath(p, root) for p in unread)
        )
        return items, None if rounds_unread else rounds, capped, None
    return items, rounds, capped, len(deferred)


# --- publishing ----------------------------------------------------------

# The asset's name on the release, and so the last part of its URL.
ASSET = "seal.png"


class Refused(Exception):
    """A reason the seal is not attached; `main` says it and exits 0."""


def gh(*args):
    """`gh <args>`'s stdout, or `Refused` naming the call and what it said."""
    out = subprocess.run(["gh", *args], capture_output=True, encoding="utf-8")
    if out.returncode:
        raise Refused(f"gh {' '.join(args[:2])} failed: {out.stderr.strip()}")
    return out.stdout


def tagged(tag):
    """The commit `tag` names, which the panel's `tag` row shows."""
    out = subprocess.run(
        ["git", "rev-parse", f"{tag}^{{commit}}"], capture_output=True, encoding="utf-8"
    )
    if out.returncode:
        raise Refused(f"git rev-parse {tag} failed: {out.stderr.strip()}")
    return out.stdout.strip()


def rasterise(svg, png):
    """Draw `svg` as a `SEAL_PX * DENSITY` pixel square PNG at `png` with
    `rsvg-convert`, or raise `Refused` saying why: the SVG is not there, the
    binary is not on `PATH` -- the `seal` job installs it, and an install
    that failed lands here -- or it exited non-zero, with what it printed."""
    if not os.path.isfile(svg):
        raise Refused(f"the seal's SVG is not there: {svg}")
    side = str(SEAL_PX * DENSITY)
    try:
        out = subprocess.run(
            ["rsvg-convert", "-w", side, "-h", side, svg, "-o", png],
            capture_output=True,
            encoding="utf-8",
        )
    except FileNotFoundError as problem:
        raise Refused(
            "rsvg-convert is not installed (librsvg2-bin); the seal cannot be drawn"
        ) from problem
    if out.returncode:
        raise Refused(f"rsvg-convert failed: {out.stderr.strip()}")


def seal_release(tag, repo, dry):
    """Draw, attach and show the seal for `tag`, or raise `Refused` at the
    first thing that stops it -- before any write, apart from the edit."""
    note = publisher()
    version = note.version_of(tag)
    if version is None:
        raise Refused(f"{tag!r} is not a vX.Y.Z tag")
    outcome = os.environ.get("SUITE_OUTCOME", "").strip()
    if outcome and outcome != "success":
        raise Refused(f"the suite at {tag} ended {outcome}, and a seal says it passed")
    try:
        suite = suite_counts(
            os.environ.get("SUITE_RECORDS", "").strip(),
            os.environ.get("SUITE_KEY", "").strip(),
        )
    except (OSError, ValueError) as problem:
        raise Refused(f"the suite's counts cannot be read: {problem}") from problem
    pulls = note.merged_pulls(repo, version)
    if pulls is None:
        raise Refused("gh pr list could not list the release's pull requests")
    work, closed, people = note.tally(pulls, repo.split("/")[0])
    chain = chain_counts(ROOT, work)
    rows = release_rows(version, tagged(tag), len(work), len(closed), suite, chain)
    for label, value in rows:
        print(f"{label:<8} {value}")
    # The upload names the asset after the file, so a run that uploads
    # writes `ASSET` in a directory of its own; `SEAL_PNG` is a dry run's.
    path = os.environ.get("SEAL_PNG") if dry else ""
    path = path or os.path.join(tempfile.mkdtemp(prefix="release-seal-"), ASSET)
    rasterise(SVG, path)
    print(f"drew {path} from {os.path.basename(SVG)} with rsvg-convert")
    try:
        body = json.loads(gh("release", "view", tag, "--repo", repo, "--json", "body"))[
            "body"
        ]
    except (ValueError, KeyError, TypeError) as problem:
        raise Refused(f"gh release view printed no note: {problem}") from problem
    table = note.glance(work, closed, people)
    if body.count(table) != 1:
        raise Refused(
            "the glance table is not in the note exactly once as `glance` "
            "writes it for this release -- the note was edited after "
            "publication, went out without one, or the pull requests moved "
            "between the two lists; nothing was uploaded"
        )
    image = f"https://github.com/{repo}/releases/download/{tag}/{ASSET}"
    sealed = body.replace(
        table, note.sealed_glance(image, alt_text(rows), SEAL_PX, work, closed, people)
    )
    if dry:
        print("DRY_RUN -- nothing uploaded and nothing edited; the note would read:")
        print(sealed)
        return
    gh("release", "upload", tag, path, "--repo", repo)
    try:
        gh("release", "edit", tag, "--repo", repo, "--notes", sealed)
    except Refused as problem:
        raise Refused(
            f"{problem}; {ASSET} was uploaded and the note does not show it"
        ) from problem
    print(f"attached {ASSET} to {tag} and put it in the note")


def main():
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    tag = os.environ.get("TAG", "").strip()
    repo = os.environ.get("REPO", "").strip()
    dry = os.environ.get("DRY_RUN", "").strip() not in ("", "0", "false", "no")
    if dry:
        print("DRY_RUN -- nothing will be uploaded or edited")
    try:
        seal_release(tag, repo, dry)
    except (Exception, SystemExit) as problem:
        reason = (
            str(problem)
            if isinstance(problem, Refused)
            else (f"{type(problem).__name__}: {problem}")
        )
        reason = " ".join(reason.split())
        print(f"no seal: {reason} -- the note stays as it was published")
        print(f"::warning::release seal skipped: {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
