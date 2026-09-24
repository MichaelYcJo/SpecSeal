#!/usr/bin/env python3
"""Did a merge in this range drop a correction the ledger had already made?

Issue #424. Two branches each corrected rows of `seal/ledger.md` that the
other had not touched -- which `CLAUDE.md`'s fragment rule does not merely
permit but REQUIRES, because a branch that falsifies what a row claims must
repair it in the shared file. So the file conflicted, and the two hunks
resolved in opposite directions because each side was the superset in one.
Taking a side wholesale reverted three corrections, each of which had turned a
false claim true.

**Nothing could see it, and that is the property this check is about.** A row
reverted to a superseded state is byte-identical to a row nobody has touched:
there is no marker on it, `evidence-check` reads anchors and hashes rather
than prose, and the hash is *correct* for the restored text. Run afterwards --
the obvious next step once a merge drifts anchors -- `--reverify` re-stamps the
restored rows, writing *somebody read this* over three claims that had been
read, found false and repaired. The only reason the incident was caught is
that a reviewer grepped for the marker the corrections carried and found **0**
occurrences of `Corrected 2026-09-15` in a file that had had three.

  correction-check --range A..B
  correction-check --range origin/release/vX.Y.Z...HEAD    at the pull request

Exit codes: **0** no merge in the range dropped a marker -- including the
common case of a range with no merge in it at all, which the report says in
those words. **1** a marker was lost, each one named with its file, the merge,
the parent it came from and the row that still stands. **2** unusable input.
Nothing is ever written; this reads git and prints.

## What it does NOT do, and why that is the design

It does not prevent the loss. Reading both sides of a hunk is irreducibly a
person's act -- `CLAUDE.md` §*The goal a design is chosen against* weighs a
design on whether it stops asking a person, and this is the case where the
asking cannot be removed, only made loud. A merge driver for the file was
rejected by the ticket for the same reason: a driver would have to understand
what a row CLAIMS, which is the judgment the whole ledger is built around a
person making.

## The marker is the verb and the date, never the sentence

`Corrected <date>` and `Re-read <date>`, and the two tokens are the whole of
the identity.

**Both verbs, and `Re-read` is the common one by a wide margin.** The census
beside `MARKER` below is the only place in this module that states a figure
about the corpus, and it says which corpus, which instrument and which date
each one is true of. Nothing here restates a digit, and that is the repair
#470 asked for: six sites stating one number is the defect it reported, and
correcting six copies would have left six copies to drift.

What those figures support is this. Row counts and occurrence counts differ,
because a row can carry a marker in more than one cell and a marker can carry
a qualifier between the verb and the date. A check watching `Corrected` alone
would watch a small fraction of the marked rows and ignore the rest, and the
work item that merged immediately before this one re-read and widened four
rows of the shared file, writing `Re-read` on every one of them. Losing one of
those to a merge is the loss the ticket is about.

**Nothing after the date is read**, because at least three spellings of the
`Corrected` sentence already exist -- `…by issue #98.`, `…by review round 3,
finding 3`, `…(#205):` -- and the fourth is somebody rewording one. A check
pinned to the prose goes red on a rewording and stays quiet on a revert, which
is both failure directions at once.

**And a short qualifier before it is read as part of the marker.** `Re-read
again <date>`, `Re-read a third time <date>`, `Corrected and widened <date>`:
a minority of this repository's markers, in a handful of spellings, and one
row carries no other. The marker's identity is the verb and the date, so a
qualifier changes neither -- which is what keeps a reworded marker from
reading as a lost one. `MARKER` below has the census, the bound and every
figure either of them rests on.

**This half was measured late, and the sentence above it is why.** The frame
counted the spellings of the sentence AFTER the date, found three, and stated
that with a count -- which made *the variation lives after the date* look
measured when only one side of the date had been looked at. Round 1's finding
1 measured the other side. The same false fact was standing in nine places by
then, including a ledger row, on a branch whose whole subject is ledger truth.

**What this cannot see, stated rather than discovered later:** a correction
that carries neither word. The check is exactly as good as the convention, and
the convention is prose. The census below is in this module so a later reader
can see what its reach actually was rather than assuming it covered
corrections as a class. What closes that gap is a structured column, which is
the ledger format changing -- a different work item.

## Row survival is the whole distinction

A marker that vanishes **with its row** is `REMOVED` and correct: `CLAUDE.md`
§*A row whose anchor a change removes is REMOVED, not re-pointed* is the
repository's own rule, and a branch that removes the code a row cites is
obeying it. A marker that vanishes **while its row stands** is the defect.

So a loss is reported only where the row can be shown to still stand, and the
bias where identity cannot be established is silence. That direction is
deliberate: a check that refuses correct work is one people learn to skip,
which is why this is acceptance row A3 of the spec and not a note.

A row is identified two ways, and the second exists because the first can be
what the correction edited:

  - **its first cell**, whitespace-collapsed. Cheap, and stable for the
    ordinary case where the correction landed in a later cell -- which is
    where all three of the incident's did.
  - **its content anchors**, `path#unit` with the hash dropped. A row is never
    re-pointed at whatever now sits nearest to where it used to look, so the
    anchors outlive any correction to the row's prose, including a correction
    to the claim itself.

The anchor route answers only where it answers **unambiguously**: where two
rows of the parent cite the same anchor set, it decides nothing. Otherwise
removing one of two rows that cite one unit would report a loss because its
neighbour still stands, which is A3 broken by the fallback that exists to
widen A1.

## The merge base is the third input, and a measurement is why

A merge is correct to drop a marker when a PARENT deleted it relative to the
merge base. It is wrong to drop one no parent asked to lose.

| | base | the parent that has it | the other parent | result | |
|---|---|---|---|---|---|
| a correction discarded | absent | present — it added it | absent, unchanged | absent | **report** |
| a deletion honoured | present | present, unchanged | absent — it deleted it | absent | silent |

Those two are indistinguishable without the base: in both the result equals
one parent and the other parent's marker is gone. The rule this check shipped
with read either parent alone, and measured over this repository's whole
reachable history -- 37 merge commits, 24 of them with a parent carrying a
ledger with markers -- it reported exactly one merge and five markers, all on
one row, and opening it showed correct work: `release/v0.9.3` re-anchored a
row whose section had moved file and rewrote the cell that carried four
historical `Re-read` sentences. The merge took that rewrite. With the base
read as well the count over the same history is zero.

Where two parents share no history there is no base to read. Such a merge is
not judged, and the report says so rather than reporting everything: a check
that answers where it cannot see is the failure `skills/verify/SKILL.md`
§*The Seal Test* is about.

## Markers are counted per row, not tested for presence

A row that carried `Re-read 2026-09-05` in two cells and carries it in one has
lost a correction exactly as much as a row that carried it in one cell and
carries it in none.

## What it reads

`seal/ledger.md` and every `seal/ledger/*.md` fragment, from the first commit
rather than the shared file alone. `.github/scripts/fold_ledger.py` moves
every fragment into the shared file at the release, so a check watching one of
them goes blind exactly when the rows become shared. Both are read at each
commit through `git cat-file --batch`, because `seal/ledger.md` here runs to
thousands of lines and about a megabyte, with single rows running to thousands
of characters, and a process spawn per file per commit is most of the run. No
digit stands in that sentence on purpose: the file grows at every release, so
a measured size written here is a figure nothing would ever re-take.

Only the committed root is readable at all. A repository in local mode keeps
`seal/` under the git common directory and commits nothing, so it has no
history for this to read -- and no workflow to run it from.

## Markers in prose are out of scope, by construction

The convention writes a marker into a row cell. Text outside a table row has
no row, so the survival test has nothing to decide there, and a loss it cannot
tell from a rewrite is not a loss this reports.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import Counter

# The two addresses a ledger lives at. The fragment glob is watched from the
# first commit rather than added later, because `fold_ledger.py` moves every
# fragment into the shared file at the release and a check watching one of
# them goes blind exactly when the rows become shared.
LEDGER = "seal/ledger.md"
FRAGMENTS = "seal/ledger"

# A blob bigger than this is not a ledger anybody wrote by hand. The shared
# file in this repository is around a megabyte, so the cap has room and is not
# a limit anything here is near. No measured size stands here: the file grows
# at every release, and the census note below is the one site in this module
# that states a figure about the corpus.
SIZE_CAP = 8 * 1024 * 1024

# The two verbs, and the date shape. Nothing AFTER the date is read, and a
# short run of lowercase words BEFORE it is read as part of the same marker
# rather than as a different one.
#
# **How the census below was taken, because that is the whole of what went
# wrong twice.** The frame counted the spellings AFTER the date, found three,
# and concluded the variation lives there — it had looked at one side only.
# Round 1 corrected that and then re-measured with the widened pattern ITSELF,
# so a spelling the pattern could not see was invisible to the census
# justifying it, and the bound came out one short. Both are the same error:
# an instrument that cannot see what it is being calibrated against.
#
# So the numbers below are taken by something that is NOT this pattern and has
# no bound at all. For every `\b(Corrected|Re-read)\b` in the file, find the
# next date on the same line and count the words between; a run made only of
# lowercase words is a candidate marker site. Nothing about it can be limited
# by the bound under test, and it is reproducible in a dozen lines. The walk
# goes verb by verb rather than as one expression over the file, because a
# single `verb ... date` pattern consumes any second verb standing before the
# date and silently drops its site --
# `test_the_bound_covers_every_candidate_marker_site_the_corpus_carries` is
# that walk as a case, and it is what holds the bound now.
#
# **Every figure here is three things or it is nothing: a corpus, an
# instrument and a moment.** Two earlier versions of this comment were false
# for want of one of them (#470).
#
#   corpus       `seal/ledger.md` alone. Not because a branch cannot move it
#                -- a branch CAN, and the one that wrote this comment moved it
#                twice, correcting rows C1 and C2 -- but because it is the
#                file a release folds the fragments INTO, so it is the part of
#                the corpus that survives a release instead of vanishing at
#                one. A figure spanning `seal/ledger/*.md` is invalidated by
#                any work item recording a correction in its own fragment, and
#                by the fold itself.
#   instrument   the unbounded walk above, never `MARKER`.
#   moment       2026-09-22, at the tip of the branch for #469, #470 and #471,
#                taken after both of that branch's own ledger edits. THESE
#                DIGITS GO STALE, by construction, at the next release that
#                folds a fragment in and at the next branch that corrects a
#                row. Nothing is wrong when they do. The case named above is
#                what holds the property; this is a snapshot of what the
#                property looked like on one day.
#
# Measured that way: **429 marker occurrences in `seal/ledger.md`** -- 426
# standing on the 204 rows that carry one, and 3 in the file's prose. The
# survival test acts on the 426 and never on the 3, because text outside a
# table row has no row for it to decide (see *Markers in prose are out of
# scope, by construction* above); a reader told *429 on 204 rows* would
# believe it watches three markers it cannot see, which is exactly what six
# tracked files said before #470. A pattern demanding the date immediately
# after the verb sees **385**. The other 44 put a qualifier in between, in ten
# spellings: `again` 23 times, `a third time` and `and re-executed` 5 each, `a
# fourth time` 3, `a fifth time` and `and re-stamped` 2 each, and one each of
# `and re-stamped again`, `and re-stamped a third time`, `and widened` and
# `and re-measured`. One row (`R4 · the printed bound reads BOTH of the gate's
# walks …`) carries a qualifier on every marker it has and no bare spelling at
# all, so losing one at a merge reported nothing. And the qualifier is not a
# one-off somebody can be asked to stop writing: nine commits in this
# repository's history have introduced `Re-read again` into that file -- a
# figure taken with `git log -S'Re-read again' -- seal/ledger.md` rather than
# with the walk above, which counts sites in a file and not commits. Naming
# the second instrument is not pedantry, and *counts commits against the
# first parent* is not yet a name: read as *the count rose* and read as *the
# count differs* it is two instruments, each perfectly stable and each
# answering higher than `git log -S` does. Review round 1 of work item
# 1789996780 and the fix pass answering it reported different totals for what
# both called one variant, and round 2 settled it by running both readings at
# three tips -- the gap was the predicate, not the history and not the days
# between the two readings. The conclusion holds on every reading, which is
# why the figure stays; `git log -S` is named because its question has one
# reading.
#
# **Both failure directions at once, which is what this design was chosen to
# avoid.** Silent when a qualified marker is reverted, and red when a
# resolution rewords `Re-read <date>` into `Re-read again <date>` — nothing
# lost, the verb and the date both standing. The second is A7 broken.
#
# Five words is the bound and lowercase is the gate. A qualifier is a phrase
# inside the sentence, so a capital letter is the next sentence and a digit is
# the date itself. The longest run the tree carries is five, and it is spelled
# `Re-read and re-stamped a third time <date>` -- the spelling is the address,
# because a line number moves for edits that have nothing to do with the
# claim, and this one was cited as `seal/ledger.md:1172` in four places until
# #470. The distribution has a hole where the old bound sat: runs of 0, 1, 2,
# 3 and 5 words occur and **no run of 4 does**, so a bound of four matches
# exactly what a bound of three matches (428 of the 429, against 429 at five)
# and buys nothing at all. Six and eight also reach 429, so five is the last
# bound that changes an answer; going past it would turn
# `test_a_run_long_enough_to_be_a_sentence_is_not_a_qualifier` green for
# nothing.
#
# **What the bound is justified by, stated because the split had never been
# taken.** That five-word run stands in the file's PROSE, not on a table row,
# and so do the two next-longest; no table row carries a qualifier longer than
# three words. So the survival test, which acts per row, would return the same
# verdicts today at a bound of three. The bound is not narrowed on that
# ground, and the reason is the sentence above: the same hands that wrote a
# five-word qualifier into this file's prose will write one into a row, and
# `markers()` is applied to whole-file text as well as to rows. What the bound
# is answerable to is the tree's longest spelling WHEREVER it stands -- which
# is a property, and which the census case holds.
#
# The bound is what keeps the verb from reaching across a clause to a date
# nobody wrote it against, which would manufacture a marker and then report
# its loss. The identity stays `(verb, date)`, so the spellings of one reading
# compare equal and a reword is not a loss.
VERBS = ("Corrected", "Re-read")
MARKER = re.compile(
    r"\b(" + "|".join(VERBS) + r")"
    r"(?:[ \t]+[a-z][a-z-]*){0,5}"
    r"[ \t]+(\d{4}-\d{2}-\d{2})(?!\d)"
)

# A content anchor with its hash dropped: `path#unit` out of `path#unit@hash`.
# The hash is what a correction changes and the anchor is what it does not, so
# only the left half is an identity. Both the plain and the double-backtick
# spellings the ledger uses reach this the same way -- the pattern is anchored
# on the `#` and the `@`, not on the quoting around them.
ANCHOR = re.compile(r"([^\s`|]+\.[A-Za-z0-9]+#[^`@|]*?)@[0-9a-f]{6,}")

# A markdown table separator, which is not a row anything can lose.
SEPARATOR = re.compile(r"^\|[\s:|-]*\|$")


def markers(text):
    """`{(verb, date): count}` for every marker in `text`."""
    return dict(Counter(MARKER.findall(text)))


class Row:
    """One table row of a ledger file, with the three things it is judged by.

    `key` is the first cell whitespace-collapsed, `anchors` the content
    anchors it cites with their hashes dropped, and `markers` the multiset of
    correction markers it carries.
    """

    def __init__(self, raw):
        self.raw = raw
        cells = raw.strip().strip("|").split("|")
        self.key = " ".join(cells[0].split()) if cells else ""
        self.anchors = frozenset(a.strip() for a in ANCHOR.findall(raw))
        self.markers = markers(raw)

    def __repr__(self):
        return f"Row({self.key[:40]!r})"


def rows(text):
    """Every table row of `text`, separators and blank lines dropped."""
    found = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or SEPARATOR.match(stripped):
            continue
        found.append(Row(line))
    return found


def _index(parsed):
    """`(by_key, by_anchor)` for a file's rows.

    `by_anchor` holds only anchor sets that ONE row of this file cites. A set
    two rows share decides nothing, for the reason the docstring gives.
    """
    by_key, by_anchor = {}, {}
    shared_keys, shared = set(), set()
    for row in parsed:
        if row.key in by_key or row.key in shared_keys:
            shared_keys.add(row.key)
            by_key.pop(row.key, None)
        else:
            by_key[row.key] = row
        if not row.anchors:
            continue
        if row.anchors in by_anchor or row.anchors in shared:
            shared.add(row.anchors)
            by_anchor.pop(row.anchors, None)
            continue
        by_anchor[row.anchors] = row
    return by_key, by_anchor


def standing(row, ambiguous, ambiguous_keys, by_key, by_anchor):
    """The row in the result that IS `row`, or None if it did not survive.

    `ambiguous` and `ambiguous_keys` are the anchor sets and the first cells
    more than one row of the PARENT carries. A row whose identity is ambiguous
    on one side falls through to the other, and a row ambiguous on both is not
    identified at all -- silence, which is the direction A3 argues for.

    The guard used to be the anchor route's alone, and that was the fallback
    carrying an argument the cheap identity needed just as much: removing one
    of two rows that share a first cell would report a loss because its twin
    still stands, which is A3 broken by the identity that runs first. Latent
    when round 1 measured it -- no marked row shared a key -- and not
    unreachable: `seal/ledger.md` repeats its section table headers, so well
    over a hundred of its rows carry one of two first cells.
    """
    if row.key not in ambiguous_keys:
        found = by_key.get(row.key)
        if found is not None:
            return found
    if row.anchors and row.anchors not in ambiguous:
        return by_anchor.get(row.anchors)
    return None


class Loss:
    """One marker a merge dropped from a row that is still there.

    `row` is the row as the parent carried it, `standing` as the result
    carries it, and `marker` the `(verb, date)` pair that went missing.
    """

    def __init__(self, row, standing, marker):
        self.row = row
        self.standing = standing
        self.marker = marker

    def __repr__(self):
        verb, date = self.marker
        return f"Loss({verb} {date} from {self.row.key[:40]!r})"


def losses(parent_text, result_text):
    """Every marker `parent_text` carries that `result_text` does not, whose
    row survived into `result_text`."""
    parsed = rows(parent_text)
    marked = [row for row in parsed if row.markers]
    if not marked:
        return []
    seen, keys = Counter(), Counter()
    for row in parsed:
        keys[row.key] += 1
        if row.anchors:
            seen[row.anchors] += 1
    ambiguous = {anchors for anchors, count in seen.items() if count > 1}
    ambiguous_keys = {key for key, count in keys.items() if count > 1}
    by_key, by_anchor = _index(rows(result_text))
    found = []
    for row in marked:
        survivor = standing(row, ambiguous, ambiguous_keys, by_key, by_anchor)
        if survivor is None:
            continue
        for marker, count in sorted(row.markers.items()):
            gone = count - survivor.markers.get(marker, 0)
            for _ in range(max(gone, 0)):
                found.append(Loss(row, survivor, marker))
    return found


def marker_counts(text):
    """`{(row key, marker): count}` for a whole file.

    The key alone, not the anchor route: this is read to ask what a PARENT
    decided relative to the base, and a row whose key moved between the two
    is a row the parent rewrote -- which the base test should read as an
    addition rather than as a deletion the merge may honour. Reading the
    anchors here would quietly turn a rewrite into permission to drop the
    marker with it.
    """
    counts = {}
    for row in rows(text):
        for marker, n in row.markers.items():
            ident = (row.key, marker)
            counts[ident] = max(counts.get(ident, 0), n)
    return counts


def honoured(loss, in_base, held):
    """Did one of the parents DELETE this marker relative to the base?

    `in_base` is the base's count for the loss's identity and `held` the same
    count for each parent. A parent holding fewer than the base did deleted
    it, and a merge that drops what a parent deleted is doing its job.
    """
    ident = (loss.row.key, loss.marker)
    return any(counts.get(ident, 0) < in_base.get(ident, 0) for counts in held)


# --- git -------------------------------------------------------------------


class Refused(Exception):
    """Unusable input. Exit 2, and nothing was examined."""


def git(root, *args):
    """Text output, or None if the command failed.

    None rather than `""` on failure, because the two are different facts: a
    file this commit does not carry and a git call that did not run read the
    same way once both are the empty string, and the second one silently
    switches a comparison off.
    """
    out = subprocess.run(
        ["git", "-C", root, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if out.returncode != 0:
        return None
    return out.stdout


def resolves(root, rev):
    """The full oid `rev` names, or None."""
    out = git(root, "rev-parse", "--verify", "-q", rev + "^{commit}")
    if out is None:
        return None
    return out.strip() or None


def parse_range(root, spec):
    """`A..B` or `A...B` into two resolved commits.

    `A...B` is what a pull request's own comparison is spelled with and what
    the CI leg passes, so it is resolved to its merge base here rather than
    sending whoever runs this at a pull request to work that out by hand.
    """
    for sep in ("...", ".."):
        if sep in spec:
            left, _, right = spec.partition(sep)
            break
    else:
        raise Refused(
            f"--range {spec} is not a range. Write `A..B`, the two commits "
            "the merges to read lie between"
        )
    a = resolves(root, left.strip() or "HEAD")
    b = resolves(root, right.strip() or "HEAD")
    if a is None:
        raise Refused(f"--range {spec}: `{left.strip()}` does not resolve in {root}")
    if b is None:
        raise Refused(f"--range {spec}: `{right.strip()}` does not resolve in {root}")
    if sep == "...":
        base = git(root, "merge-base", a, b)
        if base and base.strip():
            a = base.strip()
    return a, b


def merges(root, a, b):
    """Every merge commit in `a..b`, oldest last as git lists them."""
    out = git(root, "rev-list", "--merges", f"{a}..{b}")
    if out is None:
        raise Refused(f"cannot walk {a[:7]}..{b[:7]} in {root}")
    return out.split()


def parents(root, rev):
    out = git(root, "rev-parse", f"{rev}^@")
    return out.split() if out else []


def ledger_listing(root, revs):
    """`{rev: {the ledger paths it carries}}`.

    Per rev rather than a union, because the union alone cannot tell a path a
    rev does not carry from a path whose blob could not be read. Those are
    different facts and only one of them is a pass: a blob this cannot read
    is a blob it cannot judge, and saying nothing about it is a pass it did
    not earn.
    """
    listing = {}
    for rev in revs:
        out = git(root, "ls-tree", "-r", "--name-only", rev, "--", LEDGER, FRAGMENTS)
        listing[rev] = {p for p in (out or "").split("\n") if p.endswith(".md")}
    return listing


def read_blobs(root, pairs):
    """`{(rev, path): text}` for the pairs that exist and decode as text.

    One `git cat-file --batch` for every blob the walk needs rather than one
    `git show` per file per commit. The shared ledger here runs to about a
    megabyte and a range can hold dozens of merges; the difference is the run.
    No measured size stands here: the file grows at every release, and the
    census note beside `MARKER` is the one site in this module that states a
    figure about the corpus.

    A path a rev does not carry comes back absent rather than empty, because
    an empty string reads as a ledger with no rows in it, which is a
    different fact and one that would report every marker as lost.
    """
    if not pairs:
        return {}
    request = "".join(f"{rev}:{path}\n" for rev, path in pairs).encode("utf-8")
    out = subprocess.run(
        ["git", "-C", root, "cat-file", "--batch"],
        input=request,
        capture_output=True,
    )
    if out.returncode != 0:
        raise Refused(f"cannot read blobs in {root}")
    found = {}
    data, at = out.stdout, 0
    for pair in pairs:
        end = data.find(b"\n", at)
        if end < 0:
            break
        header = data[at:end].decode("utf-8", "replace").split()
        at = end + 1
        # `<oid> missing` for a pair this rev does not carry, `<oid> blob
        # <size>` otherwise. Anything else is a shape this parser does not
        # know, and stopping is safer than guessing an offset.
        if len(header) < 3 or header[1] != "blob":
            continue
        try:
            size = int(header[2])
        except ValueError:
            break
        body, at = data[at : at + size], at + size + 1
        if size > SIZE_CAP or b"\0" in body:
            continue
        found[pair] = body.decode("utf-8", "replace")
    return found


class Report:
    """One marker a merge dropped, with everything a reader needs to open it."""

    def __init__(self, path, merge, parent, loss):
        self.path = path
        self.merge = merge
        self.parent = parent
        self.loss = loss


def examine(root, a, b):
    """`(reports, merges examined, the things not judged)` over the range.

    The third value is a list of `(what, why)` lines. Two things reach it: a
    merge whose parents share no history, so there is no base to read, and a
    ledger blob this could not decode -- over the size cap, or holding a NUL
    byte. Both are printed rather than swallowed and neither refuses the run,
    because refusing everything over one unreadable blob turns a check about
    corrections into a check about file sizes.
    """
    walk = merges(root, a, b)
    reports, unjudged = [], []
    for merge in walk:
        kin = parents(root, merge)
        base = git(root, "merge-base", *kin) if len(kin) > 1 else None
        base = base.strip().split("\n")[0] if base and base.strip() else None
        if base is None:
            unjudged.append(
                (merge[:7], "its parents share no history, so there is no merge base")
            )
            continue
        revs = (merge, base, *kin)
        listing = ledger_listing(root, revs)
        paths = sorted(set().union(*listing.values()))
        if not paths:
            continue
        pairs = [(rev, path) for path in paths for rev in revs]
        blobs = read_blobs(root, pairs)
        for path in paths:
            gone = [
                rev for rev in revs if path in listing[rev] and (rev, path) not in blobs
            ]
            if gone:
                unjudged.append(
                    (
                        f"{merge[:7]} {path}",
                        "the blob is over the size cap or is not text at "
                        + ", ".join(rev[:7] for rev in gone),
                    )
                )
                continue
            result = blobs.get((merge, path), "")
            in_base = marker_counts(blobs.get((base, path), ""))
            held = [marker_counts(blobs.get((p, path), "")) for p in kin]
            # One marker gone from one row is ONE loss, whichever parents
            # carried it -- and every marker older than the fork is carried by
            # both, so appending per parent made the closing line read `2
            # correction marker(s)` for one row and one marker. That sends a
            # reader to open two hunks when there is one, and it inflates the
            # only number the report ends on.
            #
            # The parent named is the one that lost the most occurrences of
            # it, because that is the side whose text most needs reading. Ties
            # fall to the first parent, which is the side the person resolving
            # the conflict had checked out.
            #
            # Grouped by `(row key, marker)` rather than deduplicated: a row
            # that carried one marker in two cells and carries it in none has
            # lost it twice, and that pair is still two entries.
            carried = {}
            for parent in kin:
                text = blobs.get((parent, path))
                if text is None:
                    continue
                for loss in losses(text, result):
                    if honoured(loss, in_base, held):
                        continue
                    # The SURVIVING row, not the parent's. The parent's first
                    # cell is exactly what a correction changes -- which is
                    # why the anchor route exists at all (ledger row C4) -- so
                    # keying on it gives two parents that spell that cell
                    # differently two tags for one lost marker, and the
                    # closing line says two. That is finding 2 verbatim, one
                    # shape over. Every parent's loss converges on the same
                    # result row, so that row's text is the one identity that
                    # cannot move between the sides being compared.
                    tag = (loss.standing.raw, loss.marker)
                    carried.setdefault(tag, {}).setdefault(parent, []).append(loss)
            for by_parent in carried.values():
                parent, group = max(by_parent.items(), key=lambda kv: len(kv[1]))
                for loss in group:
                    reports.append(Report(path, merge, parent, loss))
    return reports, len(walk), unjudged


# --- the report ------------------------------------------------------------


def trim(text, width=150):
    """One line, short enough to read, with what was cut made visible."""
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 1] + "…"


def report(reports, examined, unjudged, a, b, out=sys.stdout):
    """Print what was found and answer with the exit code."""
    span = f"{a[:7]}..{b[:7]}"
    if not examined:
        # A5. The common case is a range with no merge in it, and it has to
        # SAY it looked at none -- a check that prints nothing cannot be told
        # from one that did nothing, and the second is what a green build
        # would then be resting on.
        print(
            f"correction-check: no merge commit in {span}, so no correction "
            "can have been dropped at one",
            file=out,
        )
        return 0
    print(
        f"correction-check: examined {examined} merge commit(s) in {span}",
        file=out,
    )
    for what, why in unjudged:
        print(f"  not judged  {what} — {why}", file=out)
    if not reports:
        print("  no correction marker was dropped at a merge", file=out)
        return 0
    print("", file=out)
    for entry in reports:
        verb, date = entry.loss.marker
        print(f"{entry.path}", file=out)
        print(f"  lost        {verb} {date}", file=out)
        print(f"  at merge    {entry.merge[:7]}", file=out)
        print(f"  from parent {entry.parent[:7]}, which carried it", file=out)
        print(f"  row         {trim(entry.loss.row.key, 110)}", file=out)
        print(f"  standing    {trim(entry.loss.standing.raw)}", file=out)
        print("", file=out)
    print(
        f"{len(reports)} correction marker(s) a parent carried are gone from the "
        "merge result, on rows that still stand. Open each hunk and read BOTH "
        "sides: a row reverted to a superseded state is byte-identical to a row "
        "nobody touched, so nothing downstream can see it",
        file=out,
    )
    return 1


def main(argv=None, out=sys.stdout):
    ap = argparse.ArgumentParser(
        prog="correction-check",
        description=(
            "Report every correction marker a merge in this range dropped "
            "from a row that still stands."
        ),
    )
    ap.add_argument(
        "--range", required=True, metavar="A..B", help="the commits to walk"
    )
    ap.add_argument("--root", default=".", help="the repository (default: .)")
    args = ap.parse_args(argv)
    try:
        root = os.path.abspath(args.root)
        a, b = parse_range(root, args.range)
        reports, examined, unjudged = examine(root, a, b)
        return report(reports, examined, unjudged, a, b, out=out)
    except Refused as exc:
        print(f"correction-check: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main())
