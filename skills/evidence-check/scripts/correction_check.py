#!/usr/bin/env python3
"""Did a merge in this range drop a correction the ledger had already made?

Issue #424. Two branches each corrected rows of `seal/ledger.md` that the
other had not touched -- which the fragment rule of the day did not merely
permit but REQUIRED, because a branch that falsified what a row claimed had to
repair it in the shared file. Since #715 a released file is not edited at all
where the freeze is declared (`docs/the-evidence-ledger.md` §*A released row
is read again in the branch's fragment*), and the arms below say what that
changed here. So the file conflicted, and the two hunks
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
the parent it came from and the row that still stands; or a `Corrected ·` row
was dropped (below); or a released ledger file changed under the freeze
(below). Each kind is named in its own words. **2** unusable input, a freeze
row that is not a work-item id among it. Nothing is ever written; this reads
git and prints.

## Two arms #715 added

**A dropped `Corrected ·` row is a loss.** A released ledger file is not
edited after its release, so a correction of one of its rows is a citing row
in the branch's fragment: a first cell opening `Corrected · `, and a first
anchor naming the released row. A merge whose parent carried such a row and
whose result carries it at no ledger path, while the released file it cites
is still there, has brought the false claim back to life -- the same loss a
dropped marker is, and invisible to the marker arm because the whole row went.
The row is identified by its citation with the hash dropped, which no edit to
the row moves. A row a parent deleted relative to the base is honoured, as a
marker is.

**The freeze.** Where `seal/config.md` at the range's tip declares
`Ledger frozen from | <work-item id>`, a range that changes `seal/ledger.md`,
or a `seal/releases/*.md` the merge base already had, is refused -- when the
range adds a work item at or above the cutoff, or adds none. A range whose
added work items all sit below it is read under the rule it was cut under,
and one line says so. Adding a release file is allowed, and so is the file
named for the base's own version on a `release/vX.Y.Z` base, which is a
second fold joining its version before the tag (#540). Without the row the
arm is off. `frozen_changes` holds the rule and `freeze_report` the words.

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

A marker that vanishes **with its row** is `REMOVED` and correct:
`docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no
commit* -- a row whose anchor a change removes is REMOVED, not re-pointed -- is the
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

`seal/ledger.md`, every `seal/ledger/*.md` fragment and every
`seal/releases/*.md` release file, from the first commit rather than the
shared file alone. `.github/scripts/fold_ledger.py` moves every fragment into
`seal/releases/<X.Y.Z>.md` at the release (#547; into `seal/ledger.md` before
it), so a check watching one of them goes blind exactly when the rows become
shared. All three are read at each commit through `git cat-file --batch`,
because the ledger corpus here runs to thousands of lines and about a
megabyte, with single rows running to thousands of characters, and a process
spawn per file per commit is most of the run. No digit stands in that
sentence on purpose: the corpus grows at every release, so a measured size
written here is a figure nothing would ever re-take.

**A row that moves between two of those paths at a merge is not identified
on either.** The survival test identifies a row within one path, so a merge
that moves a row from `seal/ledger.md` to a release file — as the one-time
`fold_ledger.py --split` did at the release that shipped #547, before #715
retired it — is silent about that row's markers: the bias toward silence
above, stated rather than met as a surprise. The split ran at a
release-preparation commit with no merge in its range, which kept that
silence from hiding a loss.

Only the committed root is readable at all. A repository in local mode keeps
`seal/` under the git common directory and commits nothing, so it has no
history for this to read -- and no workflow to run it from.

**Which rows: the ones the checker reads, and no others** (#584). A row
inside a fenced block that closes is an example, and
`evidence_check.py#quoted_lines` skips it, so it is not a claim and has no
correction to lose. A row under a fence that never closes, and a row inside
an HTML comment, are read, because the checker reads both: a row the
checker watches is a row whose correction a merge can drop, and not reading
it is the silent direction for the one check that exists to see the drop.
The fence rule is `unverified_check.py#closed_fence_lines`, loaded by path
beside this script; a copy taken without it exits 2 with a sentence naming
the path, before anything is examined.

## Markers in prose are out of scope, by construction

The convention writes a marker into a row cell. Text outside a table row has
no row, so the survival test has nothing to decide there, and a loss it cannot
tell from a rewrite is not a loss this reports.
"""

import argparse
import importlib.util
import os
import re
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
# The fence rule the checker's ledger walks read by (#584). Loaded at import,
# so every invocation reaches the missing-file sentence before it reads
# anything.
READER = os.path.join(HERE, "..", "..", "verify", "scripts", "unverified_check.py")


def load_reader(path=READER):
    """`unverified_check.py` as a module, or a sentence and exit 2.

    The file is checked for first, because `spec_from_file_location` hands
    back a spec for a missing `.py` path and `exec_module` then dies with a
    `FileNotFoundError` traceback at exit 1 -- the shape
    `payload_meter.py#_session_cost` gives the same refusal."""
    if not os.path.isfile(path):
        sys.stderr.write(
            f"correction-check: cannot read {path}, and it is what says which "
            "ledger rows stand inside a fenced example. This command ships "
            "beside it under `skills/`; a copy of one script taken on its own "
            "is not a plugin. Nothing was examined.\n"
        )
        raise SystemExit(2)
    spec = importlib.util.spec_from_file_location("specseal_unverified_reader", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reader = load_reader()

# `seal/config.md`'s one reader, `hooks/config.py#config_rows`, for the freeze
# row (#715). Loaded by path beside the fence reader, and a copy without it is
# refused the same way: this command ships with the plugin's `hooks/`.
CONFIG_READER = os.path.join(HERE, "..", "..", "..", "hooks", "config.py")


def load_config(path=CONFIG_READER):
    """`hooks/config.py` as a module, or a sentence and exit 2."""
    if not os.path.isfile(path):
        sys.stderr.write(
            f"correction-check: cannot read {path}, and it is what reads the "
            "`Ledger frozen from` row of seal/config.md. This command ships "
            "beside it in the plugin; a copy of one script taken on its own is "
            "not a plugin. Nothing was examined.\n"
        )
        raise SystemExit(2)
    sys.path.insert(0, os.path.dirname(path))
    try:
        spec = importlib.util.spec_from_file_location("specseal_config", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


config = load_config()

# The three addresses a ledger lives at. The fragment glob is watched from the
# first commit rather than added later, because `fold_ledger.py` moves every
# fragment into a release file at the release and a check watching one of
# them goes blind exactly when the rows become shared. The release directory
# is the third (#547): one file per release, written by the fold.
LEDGER = "seal/ledger.md"
FRAGMENTS = "seal/ledger"
RELEASES = "seal/releases"

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
#                twice, correcting rows C1 and C2 -- but because it was, on
#                the day below, the file a release folded the fragments INTO,
#                so it was the part of the corpus that survives a release. A
#                release now folds into `seal/releases/<X.Y.Z>.md` (#547), so
#                a figure taken today spans those files too. A figure
#                spanning `seal/ledger/*.md` is invalidated by any work item
#                recording a correction in its own fragment, and by the fold
#                itself.
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
    """Every table row of `text`, separators and blank lines dropped, and the
    rows inside a fenced block that closes (`unverified_check.py#
    closed_fence_lines`, the rule `evidence_check.py#quoted_lines` applies).

    A row is a line as GFM ends one, through the shared reader's `gfm_lines`
    (#664): split with `str.splitlines`, a U+2028 in a row's notes cut it,
    and a `Corrected` note after the cut belonged to no row, so dropping it
    in a merge was silent."""
    lines = reader.gfm_lines(text)
    quoted = reader.closed_fence_lines(lines)
    found = []
    for n, line in enumerate(lines):
        if n in quoted:
            continue
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


# A citing row (#715): its first cell opens with the verb and ` · `, and its
# first anchor is the released row it reads. A `Corrected ·` row is identified
# by that citation with its hash dropped, which no later edit to the row moves.
CORRECTED_ROW = "Corrected · "
# A citation's locator is quoted, and a quoted segment may hold `\|` -- the
# closing-pipe literal `evidence_check.py#citation_for` writes, or a heading
# with a pipe in it. `ANCHOR` stops at any `|`, so it is tried second
# (round 1, 🟡 5).
CITATION = re.compile(
    r'([^\s`|]+\.[A-Za-z0-9]+#"(?:[^"\\]|\\.)*"(?:>"(?:[^"\\]|\\.)*")?)@[0-9a-f]{6,}'
)


def corrections(text):
    """`{citation: row}` for every `Corrected ·` row of `text`."""
    found = {}
    for row in rows(text):
        if not row.key.startswith(CORRECTED_ROW):
            continue
        cited = CITATION.search(row.raw) or ANCHOR.search(row.raw)
        if cited:
            found.setdefault(cited.group(1).strip(), row)
    return found


class Dropped:
    """A `Corrected ·` row a merge dropped while the row it cites stands.

    Shaped like `Loss` where `report` reads one -- `row` and `marker` -- so a
    report names it with the same fields; `standing` is the released row's
    citation, because the released row is what still stands.
    """

    def __init__(self, row, citation):
        self.row = row
        self.citation = citation
        dated = MARKER.search(row.raw)
        self.marker = (dated.group(1), dated.group(2)) if dated else ("Corrected", "?")


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
        out = git(
            root, "ls-tree", "-r", "--name-only", rev, "--", LEDGER, FRAGMENTS, RELEASES
        )
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
        reports.extend(dropped_corrections(merge, base, kin, paths, listing, blobs))
    return reports, len(walk), unjudged


def dropped_corrections(merge, base, kin, paths, listing, blobs):
    """A `Report` for every `Corrected ·` row a parent carried at a path and
    the merge result carries at none, whose cited released file the result
    still has, and which no parent deleted relative to the base (#715).

    The result is read across every ledger path, because a fold moves a
    fragment's rows into a release file and a row that moved was not
    dropped. The cited row always stands where its file does: a released
    file is not edited, so the file is the row's survival."""
    kept = set()
    for path in listing[merge]:
        kept.update(corrections(blobs.get((merge, path), "")))
    found = []
    for path in paths:
        in_base = corrections(blobs.get((base, path), ""))
        held_by = {p: corrections(blobs.get((p, path), "")) for p in kin}
        held = list(held_by.values())
        for parent, carried in held_by.items():
            for citation, row in carried.items():
                if citation in kept:
                    continue
                if citation in in_base and any(citation not in h for h in held):
                    continue
                cited = citation.partition("#")[0]
                if cited not in listing[merge]:
                    continue
                if any(r.citation == citation for r in (f.loss for f in found)):
                    continue
                found.append(Report(path, merge, parent, Dropped(row, citation)))
    return found


# --- the freeze (#715) -----------------------------------------------------
#
# `Ledger frozen from | <work-item id>` in `seal/config.md` declares that a
# released ledger file is not edited after its release. A range is held to it
# when it adds a work item at or above the cutoff, or adds none -- a fold, a
# release preparation, a change belonging to no work item. A range whose added
# work items all sit below the cutoff was cut under the rule before, and is
# read under that one; the key is the work item rather than the merge base,
# because a branch that merges its release branch in moves its base past the
# rule and keeps its id (spec D5).

FROZEN_ROW = "Ledger frozen from"
CONFIG = "seal/config.md"
ROUTING = re.compile(r"^seal/specs/(\d+)-[^/]*/routing\.md$")
RELEASE_FILE = re.compile(r"^seal/releases/(\d+\.\d+\.\d+)\.md$")
BASE_VERSION = re.compile(r"release/v(\d+\.\d+\.\d+)$")


def config_at(root, rev):
    """`(text, refusal)` for `seal/config.md` as REV holds it — the two
    states `hooks/config.py#config_text` tells apart on disk, told apart for
    a blob (#867).

      (None, None)     REV holds nothing at that path: nothing is declared
      (text, None)     a blob that decodes as UTF-8
      (None, refusal)  something is there and will not read as text — a
                       tree of that name, or bytes that do not decode — in
                       the reader's own sentence, naming the path and REV

    `git show` alone could not tell them apart: it prints a tree's listing
    at exit 0, and it decoded with `errors="replace"`, so neither was ever
    refused and a decode error read whatever rows survived it."""
    spec = f"{rev}:{CONFIG}"
    kind = git(root, "cat-file", "-t", spec)
    if kind is None:
        return None, None
    where = f"{CONFIG} at {rev[:12]}"
    if kind.strip() != "blob":
        return None, config.unreadable_config(
            where, OSError(0, f"a {kind.strip()} in git, not a file")
        )
    out = subprocess.run(
        ["git", "-C", root, "cat-file", "blob", spec], capture_output=True
    )
    if out.returncode != 0:
        return None, config.unreadable_config(
            where, OSError(0, out.stderr.decode("utf-8", "replace").strip())
        )
    try:
        return out.stdout.decode("utf-8"), None
    except UnicodeDecodeError as undecodable:
        return None, config.unreadable_config(where, undecodable)


def cutoff_at(root, rev):
    """The `Ledger frozen from` value at REV, or None where the row is absent
    or empty. A value that is not a whole number is `Refused`, and so is a
    `config.md` that is there and will not read, and a row written twice
    (#867): the freeze arm never turns off because the file could not be
    read, which is the one direction that passes a pull request editing a
    frozen file."""
    text, refusal = config_at(root, rev)
    if refusal is not None:
        raise Refused(refusal)
    if text is None:
        return None
    value, refusal = config.value_of(config.config_rows(text), FROZEN_ROW)
    if refusal is not None:
        raise Refused(f"{CONFIG} at {rev[:12]}: {refusal}")
    if value is None or not value.strip():
        return None
    value = value.strip()
    if not value.isdigit():
        raise Refused(
            f"the `{FROZEN_ROW}` row of {CONFIG} holds `{value}`, which is not a "
            "work-item id — write the epoch prefix of the first work item the "
            "freeze binds, or `0` for every one"
        )
    return int(value)


def frozen_changes(root, a, b, spec):
    """`(cutoff, exempt ids, refused paths)` for the range, or None where the
    arm is off: no row at B.

    The base's own version is read off the range's left side as written,
    `release/vX.Y.Z`, because a second fold for one version joins that
    version's file before the tag (#540) and a resolved commit has no name.
    """
    cutoff = cutoff_at(root, b)
    if cutoff is None:
        return None
    added = git(
        root, "diff", "--name-only", "--diff-filter=A", a, b, "--", "seal/specs"
    )
    ids = sorted(
        int(m.group(1))
        for m in (ROUTING.match(p) for p in (added or "").split("\n"))
        if m
    )
    if ids and all(i < cutoff for i in ids):
        return cutoff, ids, []
    left = spec.partition("...")[0] if "..." in spec else spec.partition("..")[0]
    own = BASE_VERSION.search(left.strip())
    changed = git(
        root, "diff", "--no-renames", "--name-status", a, b, "--", LEDGER, RELEASES
    )
    refused = []
    for line in (changed or "").split("\n"):
        status, _, path = line.partition("\t")
        if not path or status == "A":
            continue
        release = RELEASE_FILE.match(path)
        if release and own and release.group(1) == own.group(1):
            continue
        if path == LEDGER or release:
            refused.append(path)
    return cutoff, [], refused


def freeze_report(root, a, b, spec, out=sys.stdout, found=None):
    """Print the freeze arm's answer and return its exit code. FOUND is
    `frozen_changes`' answer where the caller already has it: `main` asks
    before anything is printed, so a refused row stops the run unjudged."""
    if found is None:
        found = frozen_changes(root, a, b, spec)
    if found is None:
        return 0
    cutoff, exempt, refused = found
    if exempt:
        print(
            f"ledger freeze: every work item this range adds "
            f"({', '.join(str(i) for i in exempt)}) is below `{FROZEN_ROW}` "
            f"{cutoff}, so it is read under the rule it was cut under",
            file=out,
        )
        return 0
    if not refused:
        print(
            f"ledger freeze: no released ledger file changed (`{FROZEN_ROW}` {cutoff})",
            file=out,
        )
        return 0
    for path in refused:
        print(f"  frozen      {path}", file=out)
    print(
        f"{len(refused)} released ledger file(s) changed in this range, and a "
        f"released file is not edited after its release (`{FROZEN_ROW}` "
        f"{cutoff}). Write each re-read or correction as a citing row in your "
        "own fragment instead: `evidence-check --reverify --into "
        "seal/ledger/<work-item-id>.md --checked YYYY-MM-DD` for a re-read, a "
        "`Corrected ·` row for a claim that is false",
        file=out,
    )
    return 1


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
    dropped = [e for e in reports if isinstance(e.loss, Dropped)]
    reports = [e for e in reports if not isinstance(e.loss, Dropped)]
    for entry in dropped:
        print(f"{entry.path}", file=out)
        print(f"  dropped     {trim(entry.loss.row.key, 110)}", file=out)
        print(f"  at merge    {entry.merge[:7]}", file=out)
        print(f"  from parent {entry.parent[:7]}, which carried it", file=out)
        print(f"  corrects    {trim(entry.loss.citation)}", file=out)
        print("", file=out)
    if dropped:
        print(
            f"{len(dropped)} `Corrected ·` row(s) a parent carried are gone from "
            "the merge result, and the released row each corrected still stands, "
            "so its false claim reads as true again. Put each row back",
            file=out,
        )
    if not reports:
        return 1
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
        frozen = frozen_changes(root, a, b, args.range)
        code = report(reports, examined, unjudged, a, b, out=out)
        return max(code, freeze_report(root, a, b, args.range, out=out, found=frozen))
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
