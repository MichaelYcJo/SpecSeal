#!/usr/bin/env python3
"""Does wording this range removed still stand somewhere else in the tree?

A fix pass repairs the coordinate a finding named. The fact the finding was
about is usually stated in more than one place, so the other statements survive
and arrive as a later round -- `skills/agent-contract/SKILL.md` §12 is the rule
against it, it reaches every agent at startup, and it has been re-broken seven
times, once by a session that had read it and restated it as the cap.

**So this is a check and not an eighth sentence.** It takes the range a fix
pass wrote, works out which sentences the range REMOVED, and reports every
place at the range's tip that still carries one of them.

  survivor-check --range A..B                 the fix pass a smith just wrote
  survivor-check --range origin/main...HEAD   a whole branch, at the PR
  survivor-check --range A..B --exempt seal/specs/<id>/survivors.md

Exit codes: **0** nothing survived. **1** survivors, each named with its path,
the surviving text and the corrected sentence it matched. **2** unusable
input -- a range that does not resolve, an exemption file that will not parse.
Nothing is ever written; this reads git and prints.

## Why the input is the diff

A hand-written list of the sentences that appear twice would rot exactly the
way #210's list of guard arms did, and it would have to be extended by whoever
writes the next shared sentence -- the party that has just demonstrated seven
times that it will not. The diff is the one input nobody has to remember to
update. The shape was written down when #180 was scheduled: *grep the changed
sentences' distinguishing terms across the rest of the corpus and report the
survivors.*

## Why not a grep, and why not a phrase floor

Two real cases from this repository's own history rule out the two obvious
mechanics, one case each.

**A literal grep fails #269.** `7bcf36a` reworded `agents/warden.md` §6 and
left `GENERATOR_NAMED[WARDEN]` in `tests/test_the_rules_have_one_owner.py`
pinning the sentence it replaced. That pin is one sentence split across two
adjacent string literals -- `"... from this report once the "` then
`"orchestrator has verified its findings"` -- so no LINE holds the sentence and
nothing line-oriented finds it. The module was red from that commit through two
review rounds and two broad gates, because contract §2 leaves the broad gate
to whichever agent definition assigns it and no reviewer's does, so no round
could see it.

**A longest-common-phrase floor fails #267.** `ad6f81a` corrected a docstring
that called a join's receiver *an argument ... never a leaf*, and the same
claim stood in two ledger rows, one of them the shared file. Those rows
PARAPHRASE rather than copy -- *an argument to an operand, never a leaf*
against *an argument to element 4, never a leaf of the expression* -- and the
longest identical run is three words. No floor above three accepts it, and at
three every three-word run in the corpus is accepted with it.

So the metric is rarity-weighted n-gram overlap, counted over independent runs
of shared wording. Rarity is what lets *never a leaf* count while *of the
expression* does not, and a summed score rather than a ratio is what lets a
twelve-word test needle and a three-thousand-word ledger cell be judged on the
same scale. Its unit is **one phrase that occurs nowhere else**, so the number
means the same thing in a repository of twenty files and one of a thousand.

## What a sentence is in a Python file

**The prose of a `.py` file is its comments, its docstrings and its string
literals, and nothing else** (#543). A line of code normalises to the same
words in every file that walks a list the same way -- `for i in range(start,
len(lines))` is the same four-word run wherever it stands -- so under the
whole-file reading a branch that rewrote one loop was told that every other
loop of that shape still stood: four of one branch's five exemption rows,
and six of the twenty-one places the 0.15.0 release's four ranges reported,
were function bodies matched on loop, assignment and `if` shapes. None of
them was wording, and none could be corrected.

So the standard library's tokenizer reads every `.py` file first, on both
sides of the range and in the pool, and keeps COMMENT, STRING and
FSTRING_MIDDLE text where it stands. Every other token is blanked to spaces
with a sentence end where it stood, line numbers intact -- so a code token
between two literals ends the sentence (`"a", x, "b"` is two), and two
literals with only a line break between them are one, which is the shape
#269's pin has and the reason the file kind is not simply skipped: a
docstring is exactly where a removed rule survives, and the one real
survivor on the fourth of those four ranges is a `#` comment. A comment keeps
its `#`, so a comment block is still read one line per sentence and this
reading is subtractive: code gone, nothing joined that was not joined
before. A file the tokenizer refuses -- an unterminated string, a bad
dedent -- is read whole, as it always was.

Code in any other kind of file -- a workflow's `run:` block, a shell script,
a `bin/` wrapper -- is read as it always was. Not one measured instance is
in one, and no line-oriented reader exists for them the way the tokenizer
exists for Python.

## What is excluded, by construction rather than by list

**A record of a past round.** Everything under a work item's `rounds/` is out
of the **pool** that is searched and out of the **range** that is measured --
both sides of the range's path list, not its added side alone. A round record
and a reviewer's report carry the SHA they were written against and quote the
defective wording verbatim -- that is what they are for, and
`skills/implement/SKILL.md` says a round record never asserts a present state.

**Which of the two was the defect, and it was the range** (#365). The
exclusion shipped on the pool alone and read as complete, because this section
stated the intent and one of the two functions carried it. A report quoting
the removed sentence counted as wording the fix wrote, `wanted` subtracted the
survivor that quotation was about, and the check reported success having
measured nothing -- on exactly the branches that went through review, since
the review chain is what produces the disarming input. Measured at three tips
of one branch: with round 1's paragraph the range reported its survivor, and
the next commit, which added only round 1's record and report, turned the same
range green.

**What it is worth was measured, and it is not what it looks like.** On #267's
range the corrected clause does stand in `round-2.md` and `round-2-report.md`,
and with the exclusion switched off those two score **1.51** -- under the floor
by 0.09, so the floor would have refused them anyway. What the exclusion
actually buys is the other side of the same arithmetic: dropping two files that
carry the wording raises `idf` for every phrase they held, and row R3 goes from
**1.69 to 1.79**. So it is not the thing that keeps a record from being
reported on this range; it is the thing that stops records from diluting the
survivors into the floor. Both matter, and only the second was measurable
here.

**The work item's own exemption file.** `survivors.md` directly under
`seal/specs/<id>/` is out of the **pool** and out of the **range**, on both
sides of the range's path list, for a reason one step stronger than a round
record's: its rows QUOTE the surviving wording, because the quote is the
anchor. Left in the range, a row's quote counts as wording the fix wrote and
`wanted` subtracts the very survivor the row excuses (#507); left in the pool,
the file is one more carrier of exactly the phrases that produced the score,
and a survivor near the floor drops under it (#308). Either way the `exempt`
line never prints, and the check goes green because the survivor was not
found rather than because it was excused -- measured on three pull requests
of one release, 36 rows written and 7 consulted. The file is read by
`--exempt` alone, as a judgment on the search's result and never as an input
to it.

**A phase record.** Everything under a work item's `phases/` is out of the
**pool** and out of the **range**, on both sides of the range's path list,
because it is the same kind of file as a round record: what a phase was
asked, what building it found and what it removed -- a past state, quoted
for audit, instructing nobody (#460). In the pool it was reported beside the
real survivor, two of four places in one measured pass, and answering it
meant editing a record; in the range it subtracted what it quoted, the
exemption file's shape one directory over. That a phase record is corrected
in place while its work item is live does not keep it in: the exclusion is
about what the file is, never about when it was last written, and a round
record's `Deferred` and `Fixes checked by` cells are filled after the fact
too. What this gives up is the one shape the pool caught only because these
records were in it -- a correction inside an HTML comment while the false
claim rendered in bold -- and `seal/follow-up.md` names whose that loss is.

**A released changelog section, and a gathered fragment.** Every line under
a heading that names a version in the root `CHANGELOG.md` -- `## 0.15.0 —
2026-09-23`, up to the next heading that names a version or `Unreleased`,
so a `## ` line a gathered fragment carries does not end it (#564) -- is out
of the **pool** and out of the **range**, on both sides of the range's path
list; and so is a `<x>/specs/<id>/changelog.md` -- `seal/specs/<id>/` or the
pre-0.4.0 `specs/<id>/` -- whose `<!-- specs/<id> -->` marker stands in
`CHANGELOG.md` at the range's tip, because a gathered fragment is that
released entry one file over (#307). A released section records what a past
release did, in that release's words, and a released entry is not rewritten
(`CLAUDE.md` §*Repo rule — a change writes fragments, never the shared
file*): reported against one, the branch that changed the behaviour it
describes could correct nothing, and two of the four ranges the 0.15.0
release was measured on carried exactly that report. The region is read off
the heading rather than the file being left out by path, so an
`## Unreleased` section and an ungathered fragment stay in -- they are this
release's own prose, the thing the sweep is for. In the range, a release's
gathering commit writes each fragment's text under a heading that is
blanked. This repository's gatherer leaves the fragment in place; one that
deletes it, or a range that edits a gathered one, would without this count
the fragment's sentences as removed, and the work items' own `spec.md` and
`overview.md` would be reported at the release. The gathered text is held
at the release and not written as the range's own (#557): the fragment's
own branch wrote it, so it may not subtract a survivor the same commit's
correction left. Only its n-grams that also occur in a sentence
`CHANGELOG.md` itself lost count, and against that file's sentences alone,
so a gathered rewording of a lost entry still splits that entry into runs.

**Struck-through text.** A `~~...~~` span is this repository's own mark for a
claim it no longer makes; `seal/ledger.md`'s R3 carries three of them. Text
inside one is by definition not a standing sentence.

Both losses go one way: a survivor hidden inside an excluded region costs
whatever the unanswered finding was worth, and an invented survivor costs a red
build to somebody who did not write the line. The same asymmetry
`.github/scripts/rider_check.py` argues for, for the same reason.

## The escape, which is not turning it off

A survivor a person has opened and judged legitimate gets a row in
`seal/specs/<work-item-id>/survivors.md`:

    | Path | Quote | Grounds |
    |---|---|---|
    | `seal/ledger.md` | never a leaf | the row quotes its own corrected
      sentence in order to record that it was corrected |

The **quote is the anchor**, so the exemption stops applying the moment the
text changes, and what it degrades to is *reported again*. An exempted survivor
is still printed, under `exempt`, with its grounds -- a row that silences
something invisibly is a row nobody audits. There is no value meaning *check
nothing*.

## A deletion is one row, because otherwise it is 153

A branch that DELETES a shipped section is the case per-survivor rows cannot
serve. Every sentence of the section stands in the durable copies that are
supposed to survive a deletion -- the design records under `seal/specs/`,
`CHANGELOG.md` and the tickets themselves -- so #293's own range reported **153**
survivors at 1.60-1.62, every one correct as a report and none of them a
defect. Writing 153 rows is not an escape anybody takes; the branch turns the
check off instead, which is the outcome the escape exists to prevent.

So the same file takes a second row shape, with the range in the first cell:

    | Range | Grounds |
    |---|---|
    | `origin/release/vX.Y.Z...HEAD` | the deleted section's sentences stand
      in the durable copies by design |

**The row is anchored on two things, the range and the work item.** The spec is
RESOLVED rather than string-matched, because CI spells the range
`origin/<base>...HEAD` and a person spells it as two oids, and those are the
same range. Resolving is what makes the range alone insufficient: that spelling
is not a range, it is a RELATION, and it re-resolves to whatever range the
checkout it is read on is over. Every `seal/specs/*/survivors.md` in the tree
is handed to every run, and a `survivors.md` lives until the release that ships
it, so one merged row in that spelling matched every later branch cut from the
same base and excused its whole run. So the second anchor is the directory the
row lives in: a declaration holds only over a range that touches its own work
item, which a work item's own range always does. In local mode nothing under
the root is committed, so no range touches it, and the `Branch` row of the
work item's `routing.md` stands in: the declaration holds over a range whose
tip is on that branch and on no local branch that one was cut from (#554).

Both anchors degrade the way the quote above does -- loudly. A spec that no
longer resolves prints under `unresolved`; a declaration refused for belonging
to another work item prints under `not yours`, with that work item named.
Neither refuses the whole run: a `survivors.md` outlives the branch whose refs
its range names, and exit 2 there would turn every later range's check into a
refusal over a row that has nothing to do with it.

The grounds are not optional. What a reviewer reads is the written sentence,
and a row without one silences 153 places on the strength of nothing, so it is
not a row at all.

**The deliberate-duplication case is not what the escape is for.** `CLAUDE.md`
and `CONTRIBUTING.md` deliberately carry the same sentence about ledger
removals. A branch correcting it in one and not the other IS reported, and that
report is right: those two have already disagreed once, and the disagreement
left a branch with no reading that permits the only correct act. The escape is
for the third kind of carrier, text that quotes old wording in order to say it
was wrong.

## A retirement is out of the range, so a fold owes no row

A fold is the other deletion of shipped sentences, and the largest. The
directories `settle --retire` removes hold specs whose sentences stand in
`docs/` because that is what a fold IS, so every one of them was reported and
a fold branch owed the range row above. Under #517 a fold is not a work item
and has no directory to hold a `survivors.md`, so the row had nowhere to live.

So a directory the range retired is left out of it, the way a round record
is: gone at the right end, and either folded — its `<!-- specs/<id> -->`
marker in `docs/` — or retired by the rule, which is
`unverified_check.py#retired_by_rule` asked of the left end. It is the same
predicate `settle` and the other two readers ask, loaded rather than spelled
here. A sentence the same range removes from anywhere else is measured as
before.

**It leaves after the pairing across paths, not before it** (#591). A
sentence a fold carries verbatim from the retired `spec.md` into `docs/` is a
move, and the range is not its author. Dropped first, the retired side left
that arrival unpaired, so it paired with a correction the same range made
elsewhere and held it, and the correction's other copies went unreported. So
the retired side is read at the left end and takes part in the pairing, and
only its departures that paired with nothing are then dropped. It is gone at
the right end, so it adds nothing written.

## What it does not answer

It reads the tip of the range, so a survivor introduced AFTER the range is
invisible to it. It answers *did this range leave wording standing*, never *is
the tree consistent now*, which is why the report prints what it examined.
"""

import argparse
import importlib.util
import io
import math
import os
import re
import subprocess
import sys
import tokenize
from collections import Counter, deque

# Words per n-gram. Three is the smallest that carries word order, and order is
# what separates `an argument to an operand` from `an operand to an argument`.
# The rarity weighting below, not the length, is what does the discriminating.
N = 3

# The score a candidate must reach, and **its unit is one phrase that occurs
# nowhere else.** A run whose wording is unique in the corpus is worth exactly
# 1.0, whatever the corpus is; one that also appears in a few other files is
# worth a fraction of that. So `1.6` reads as *more than one and a half
# phrases that nothing else in this tree carries*.
#
# **Scaled by the corpus, and that was measured rather than foreseen.** The
# score began as raw `log2(F / df)` bits, calibrated to 15 against a corpus of
# 633 files. Then a probe repository of two files scored a survivor that was
# plainly there at 2 bits, because the most a phrase can be worth in a
# two-file corpus is `log2(2)` -- so the constant was not a property of the
# defect at all, it was a property of THIS repository's size, and every
# smaller repository running the plugin would have been silently exempt.
# Dividing by `log2(F)` is what makes the number mean the same thing in a
# twenty-file repository and a thousand-file one.
#
# **Calibrated over 77 real ranges** -- every commit of five unsquashed
# work-item branches that carried a review chain -- and `phases/phase-3.md`
# holds the curve. The two survivors this work item exists for score 1.89
# (#269's left-behind pin) and 1.79 (#267's row R3 in the shared ledger), and
# the floor sits below the weaker of them with room rather than pressed
# against it.
FLOOR = 1.6

# **A floor above 1.0 is what requires two independent phrases**, and there is
# no second constant saying so. One run is worth `log2(F / df) / log2(F)`,
# which is at most 1.0 and reaches it only when nothing else in the corpus
# carries the phrase -- so any floor past 1.0 cannot be cleared by one run
# however rare it is. That is the whole reason the unit is what it is.
#
# There WAS a second constant, `SHARED_FLOOR = 2`, and a mutation sweep found
# it could not change a single answer: the floor had already refused every
# one-run candidate. Removing it is not a simplification for its own sake --
# a constant that cannot change the answer tells a reader the independence
# requirement lives somewhere it does not, and it hid the fact that dropping
# the corpus scale would let a one-run coincidence through.

# A blob bigger than this is not prose anybody wrote by hand.
SIZE_CAP = 2 * 1024 * 1024


class Refused(Exception):
    """Unusable input. Exit 2, and nothing was examined."""


# --- git -------------------------------------------------------------------


def git(root, *args):
    """Text output, or None if the command failed.

    Returns None rather than "" on failure. #111 is what that distinction
    costs when it is missing: a git call that fails read as a repository with
    no remote, and the empty string switched off a refusal."""
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
    text = out.strip()
    return text or None


def parse_range(root, spec):
    """`A..B` or `A...B` into two resolved commits.

    Both spellings are accepted and mean the same thing here, because what is
    read is the two endpoints and never the walk between them. `A...B` is what
    a pull request's own comparison is spelled with, and refusing it would send
    whoever runs this at a pull request to work out the merge base by hand."""
    for sep in ("...", ".."):
        if sep in spec:
            left, _, right = spec.partition(sep)
            break
    else:
        raise Refused(
            f"--range {spec} is not a range. Write `A..B`, the two commits a "
            "fix pass lies between"
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


def tracked(root, rev):
    """Every path in the tree at `rev`."""
    out = git(root, "ls-tree", "-r", "--name-only", "-z", rev)
    if out is None:
        raise Refused(f"cannot list the tree at {rev[:7]} in {root}")
    return [path for path in out.split("\0") if path]


def read_blobs(root, rev, paths):
    """`{path: text}` for the paths that exist at `rev` and decode as text.

    One `git cat-file --batch` for the whole corpus rather than one `git show`
    per file. A tree here is two hundred files and the difference is two
    hundred process spawns, which is most of the run.

    A path missing at `rev`, a blob over the size cap, and a blob holding a NUL
    byte all come back absent rather than empty -- an empty string would read
    as a file with no sentences in it, which is a different fact.

    **`\\r\\n` comes back as `\\n`, here and nowhere else** (#564). Every
    committed text reaches every reader through this function, and a `$`
    under `re.M` stands before `\\n` and never before `\\r\\n`: a changelog
    committed with CRLF had no gathered ids at all. One boundary rather than
    one pattern, so the next `$`-anchored reader inherits it. Line counts are
    unchanged; a lone `\\r` is left alone."""
    if not paths:
        return {}
    request = "".join(f"{rev}:{path}\n" for path in paths).encode("utf-8")
    out = subprocess.run(
        ["git", "-C", root, "cat-file", "--batch"],
        input=request,
        capture_output=True,
    )
    if out.returncode != 0:
        raise Refused(f"cannot read the tree at {rev[:7]} in {root}")
    found = {}
    data, at = out.stdout, 0
    for path in paths:
        end = data.find(b"\n", at)
        if end < 0:
            break
        header = data[at:end].decode("utf-8", "replace").split()
        at = end + 1
        # `<oid> missing` for a path this rev does not carry, and `<oid> blob
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
        found[path] = body.decode("utf-8", "replace").replace("\r\n", "\n")
    return found


# --- reading text ----------------------------------------------------------

# A claim this repository no longer makes is struck through rather than
# deleted, so text inside a `~~...~~` span is not a standing sentence.
#
# **Bounded to one line, and that is not a simplification.** Written with
# DOTALL it read `seal/ledger.md` -- 17 `~~` markers, an ODD number, so one is
# unpaired -- and every pairing after the stray one was offset by one marker.
# The span that followed ran across lines and swallowed row R3, which is the
# primary survivor of this work item's own second acceptance case: the check
# reported the fragment row and stayed silent about the shared file, which is
# the one carrier the ticket says a reader meets first.
#
# A single stray marker can now corrupt only its own line, and GFM
# strikethrough does not cross a blank line anyway. Every strike in this tree
# is within one line, long as some of those lines are.
STRUCK = re.compile(r"~~[^\n]+?~~")

# What a word is, after lowercasing. Everything else -- quotes, backticks,
# underscores, dots, hyphens, newlines -- is a separator, which is what joins
# a sentence split across two adjacent string literals into one sentence.
WORD = re.compile(r"[a-z0-9]+")

# A line that starts a new markdown block, so the sentence before it ended
# whether or not it carried a full stop. Also a thematic break or a setext
# underline, which is a whole line of one punctuation character.
#
# Every marker CommonMark requires a space after asks for one here. The class
# used to be a bare `[-*+>#]`, which reads `#120` at the head of a line as a
# heading — and in this corpus, where a round record or a ledger row names an
# issue in every other sentence, `#120` at the head of a line is a wrapped
# sentence rather than a block. Splitting there costs a survivor: no n-gram
# crosses the false boundary, so evidence straddling the wrap is unreachable
# however high the score would have been. `>` keeps no space requirement
# because the markdown needs none.
#
# `.github/scripts/issue_claims_check.py#BLOCK_START` and
# `skills/code-review/scripts/round_record.py#BLOCK_START` are the other two
# carriers of this pattern, kept spelled alike on purpose and not shared
# through an import — the two script roots ship on different paths. This one
# needs no fence opener: `blank_struck` has already run, and a fence line
# inside a segment is prose that scores nothing.
BLOCK = re.compile(
    r"^\s*(?:[-*+](?=\s)|\#{1,6}(?=\s|$)|>|\d+[.)](?=\s)|[-*_=]{3,}\s*$)"
)

# Where a sentence ends inside a segment: sentence punctuation before
# whitespace or the end, or a table cell boundary. The `|` is what keeps a
# ledger row from being one three-thousand-word sentence whose token set
# contains everything in the corpus.
END = re.compile(r"[.!?;](?=\s|$)|\|")


def blank_struck(text):
    """`text` with every struck-through span blanked, line numbers intact.

    Blanked rather than removed: the replacement keeps the newlines, so every
    line after a multi-line strike still reports its own number."""

    def blank(match):
        return "".join("\n" if ch == "\n" else " " for ch in match.group(0))

    return STRUCK.sub(blank, text)


# The changelog the gatherer writes, at the repository root and under this
# name. A changelog kept elsewhere or under another name keeps the reading
# every other document has (#307's *Out*).
CHANGELOG = "CHANGELOG.md"

# A heading that opens a RELEASED section: `## 0.15.0 — 2026-09-23`, and the
# `## [1.2.3]` and `## v1.2.3` spellings other changelogs use. `## Unreleased`
# matches nothing here, and that is the whole reason the region is read off
# the heading rather than the file being left out by path: a repository
# following `agents/smith.md`'s *let the entry accumulate unreleased* keeps
# live prose in this file, above the first version, and that prose is this
# release's own.
VERSION_HEADING = re.compile(r"^##\s+\[?v?\d+\.\d+(?:\.\d+)?")
# The one other heading that ends a released section: `## Unreleased`, and the
# `## [Unreleased]` Keep a Changelog spells. No other `## ` line does (#564): a
# gathered fragment carrying `## Notes` is still the released entry, and read
# as live after its heading it was written as the release's own wording.
UNRELEASED_HEADING = re.compile(r"^##\s+\[?unreleased\b", re.I)


def released_lines(text):
    """`[(line, released)]` for every line of a changelog -- the one region
    rule `blank_released` and `only_released` both read, so the two stay
    exact complements.

    A version heading opens a released region, and after it only another
    version heading or an `Unreleased` heading changes it. The rule reads
    headings and never the gather's marker, so a misspelled marker cannot
    reopen the region; and `## Unreleased` directly after a gathered body,
    where a gatherer inserting above the first `## ` leaves it, stays live."""
    out, released = [], False
    for line in text.split("\n"):
        if VERSION_HEADING.match(line):
            released = True
        elif UNRELEASED_HEADING.match(line):
            released = False
        out.append((line, released))
    return out


def blank_released(text):
    """`text` with every released section of a changelog blanked, line
    numbers intact -- the heading naming a version and every line under it,
    up to the next version or `Unreleased` heading (`released_lines`).

    A released section records what a past release did, in that release's
    words, and a released entry is not rewritten. Reported against one, a
    branch that changed the behaviour the entry describes could correct
    nothing, and two of the four ranges the 0.15.0 release was measured on
    carried exactly that report (#307)."""
    return "\n".join(
        "" if released else line for line, released in released_lines(text)
    )


def only_released(text):
    """The complement of `blank_released`: every line of a released section
    kept, line numbers intact, every other line blanked.

    Read by `newly_released` at both ends of the range, so a sentence a
    release moved from `## Unreleased` under a version heading is counted
    as still held rather than as removed (round 1's 🟡 1). What is held,
    and when its wording is written, is `corrected`'s to decide."""
    return "\n".join(
        line if released else "" for line, released in released_lines(text)
    )


def newly_released(path, before, after):
    """`[Sentence]` standing under a version heading at `after` beyond what
    stood under one at `before` -- what the range itself moved or wrote into
    a released section, counted per sentence."""

    def released(text):
        # A gather's marker line is blanked, so it ends a block here. The
        # gatherer writes a fragment's body directly under its marker, and a
        # marker line starts no block, so a fragment opening with prose had
        # its first sentence joined to the marker's words: a key nothing in
        # the fragment has, which `corrected` then wrote instead of holding.
        # Blanked on both ends of the range, and never by widening `BLOCK`,
        # which two other scripts spell alike on purpose.
        text = MARKER.sub("", only_released(text))
        return [
            Sentence(path, line, raw)
            for line, raw in segments(blank_struck(text))
            if raw
        ]

    prior = Counter(s.key for s in released(before))
    out = []
    for sentence in released(after):
        if prior[sentence.key] > 0:
            prior[sentence.key] -= 1
        else:
            out.append(sentence)
    return out


# What a Python file SAYS, as opposed to what it does. Its prose is its
# comments, its docstrings and its string literals; every other token -- a
# name, an operator, a number, a keyword -- is code, and a line of code
# normalises to the same words in every file that walks a list the same way.
# #543: `for i in range(start, len(lines))` scored 2.77 against another
# module's copy of the same loop, four of one branch's five exemption rows
# were that shape, and the six instances on the 0.15.0 release's four ranges
# were function bodies matched on loop, assignment and `if` shapes.
#
# The kinds are read off the tokenizer by name. On 3.12 an f-string is
# FSTRING_START, FSTRING_MIDDLE and FSTRING_END with its expressions as
# ordinary tokens, and the middle is the prose; below 3.12 the whole f-string
# is one STRING, which the set already holds. A kind the interpreter does not
# know is left out rather than named, so the set is right on every version.
PROSE_TOKENS = {tokenize.COMMENT, tokenize.STRING} | {
    getattr(tokenize, name)
    for name in ("FSTRING_MIDDLE", "TSTRING_MIDDLE")
    if hasattr(tokenize, name)
}
# Tokens that stand for no text and are blanked WITHOUT a sentence end. The
# delimiters of an f-string are its quotes, and a plain string's quotes end
# nothing, so `f"a {x} b" "c"` reads `b c` as one sentence the way `"b" "c"`
# does; INDENT is the run of spaces at the head of a block, where a `|`
# would be a wordless sentence per indented block -- noise, never a claim.
#
# **Line structure is not listed, and that was measured rather than
# assumed.** NL and NEWLINE stand at the end of a line, past its text, and
# DEDENT and ENDMARKER stand on the next token's own column or past the last
# line; the position guard in `python_prose` writes nothing for any of them,
# so naming them here changed no output under mutation. A member that cannot
# change the answer tells a reader the joining of two literals across a line
# break lives here, and it lives in the guard.
STRUCTURE_TOKENS = {
    getattr(tokenize, name)
    for name in (
        "INDENT",
        "FSTRING_START",
        "FSTRING_END",
        "TSTRING_START",
        "TSTRING_END",
    )
    if hasattr(tokenize, name)
}
# What a blanked code token leaves behind: a cell boundary, which `END`
# already splits on. So `segments` needs no second rule to read
# `"first half", name, "second half"` as two sentences -- the code between
# the literals is where each one ends.
CODE_STOOD_HERE = "|"


def python_prose(text):
    """`text` with every code token of a Python file blanked, line numbers
    intact the way `blank_struck` keeps them.

    A comment, a docstring or a string literal stays where it stands. Every
    other token becomes spaces with a `|` at its first character, so a
    sentence ends where the code stood: `"a", x, "b"` is two sentences, and
    two adjacent literals across a line break are one, because nothing but
    line structure stands between them.

    **A file the tokenizer refuses is returned as it is** -- an unterminated
    string, a bad dedent, a byte the reader cannot place -- which is the
    whole-file reading every `.py` file had before this function existed.
    That fallback reports MORE rather than less, and more is the direction a
    checker of claims may fail in: a survivor missed inside a file nobody
    can parse costs what the unanswered finding was worth."""
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, SyntaxError, ValueError):
        return text
    lines = text.split("\n")
    out = [[" "] * len(line) for line in lines]
    for token in tokens:
        (row, col), _end = token.start, token.end
        if row < 1 or row > len(out):
            continue
        if token.type in PROSE_TOKENS:
            for offset, part in enumerate(token.string.split("\n")):
                at = col if offset == 0 else 0
                out[row - 1 + offset][at : at + len(part)] = part
        elif token.type not in STRUCTURE_TOKENS and col < len(out[row - 1]):
            out[row - 1][col] = CODE_STOOD_HERE
    return "\n".join("".join(row) for row in out)


def words(text):
    """`text` as a list of normalised words."""
    return WORD.findall(text.lower())


def segments(text):
    """`[(line, raw)]` -- the text broken at block boundaries and sentence ends.

    Two passes, and they answer different questions. The first is about
    markdown structure: a blank line or the start of a new block ends whatever
    was being said, whether or not a full stop arrived. The second is about
    sentences inside one block."""
    blocks, buffer, start = [], [], 0
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or BLOCK.match(line):
            if buffer:
                blocks.append((start, "\n".join(buffer)))
                buffer = []
            if not line.strip():
                continue
            start = number
            buffer = [line]
            continue
        if not buffer:
            start = number
        buffer.append(line)
    if buffer:
        blocks.append((start, "\n".join(buffer)))

    out = []
    for start, block in blocks:
        at = 0
        for match in END.finditer(block):
            piece = block[at : match.end()]
            if piece.strip():
                out.append((start + block.count("\n", 0, at), piece))
            at = match.end()
        rest = block[at:]
        if rest.strip():
            out.append((start + block.count("\n", 0, at), rest))
    return out


class Sentence:
    """One segment, with where it was read and what it normalises to."""

    __slots__ = ("key", "line", "path", "raw", "words")

    def __init__(self, path, line, raw):
        self.path = path
        self.line = line
        self.raw = " ".join(raw.split())
        self.words = words(raw)
        self.key = " ".join(self.words)

    def grams(self):
        return ngrams(self.words)

    def where(self):
        return f"{self.path}:{self.line}"


def sentences(path, text):
    """Every sentence in `text`, struck-through spans already gone -- and in
    a Python file, every code token gone too (`python_prose`).

    Both `corrected` and `corpus` build every sentence through this
    function, so a reader placed here holds on both sides of the range and
    in the pool by construction."""
    if path.endswith(".py"):
        text = python_prose(text)
    elif path == CHANGELOG:
        text = blank_released(text)
    return [
        Sentence(path, line, raw) for line, raw in segments(blank_struck(text)) if raw
    ]


def ngrams(seq, n=N):
    """The n-grams of a word list, as joined strings."""
    if len(seq) < n:
        return []
    return [" ".join(seq[i : i + n]) for i in range(len(seq) - n + 1)]


# --- the corpus ------------------------------------------------------------


def records_a_past_round(path):
    """True for a work item's round records and reviewer reports.

    Matched on the path's own shape rather than on a root read from config,
    because the `seal/` root sits in one of two places and a linked worktree
    spells the second one differently. What identifies these files is that they
    sit in a `rounds/` directory inside a `specs/` directory, which is true at
    either root."""
    parts = path.replace("\\", "/").split("/")
    return "rounds" in parts and "specs" in parts[: parts.index("rounds")]


def records_a_past_state(path):
    """True for a file under a work item directory that records or judges a
    past state and instructs nobody -- the class `records_a_past_round` is
    one member of.

    The members: a round record or reviewer's report (`records_a_past_round`,
    unchanged); the work item's own `survivors.md`, directly under its
    `specs/<id>/` directory; and everything under its `phases/`, a record of
    what a phase was asked, found and removed (#460). One predicate rather than one per member,
    applied on both sides -- `corpus` and `corrected` -- because the defect
    this closes was one member excluded on one side (#365) and the next
    member excluded on neither (#507, #308): the exemption file's rows QUOTE
    the surviving wording, so in the range it subtracts the survivor it
    excuses before `--exempt` is read, and in the pool it is one more carrier
    of exactly the phrases that produced the score.

    Matched on the path's own shape, at either `seal/` root, the way
    `records_a_past_round` is. `survivors.md` has to sit directly under the
    work item directory: one level deeper it is somebody's prose until the
    layout says otherwise, and `OWNER_DIR` is where a deeper file is a
    question at all."""
    if records_a_past_round(path):
        return True
    parts = path.replace("\\", "/").split("/")
    if "specs" not in parts:
        return False
    inside = parts[parts.index("specs") + 2 :]
    return inside == ["survivors.md"] or (len(inside) > 1 and inside[0] == "phases")


# The marker a gathered changelog fragment leaves in `CHANGELOG.md`, in the
# shape `unverified_check.py#FOLD_MARKER` already spells for the fold's
# marker in `docs/`. Spelled here rather than imported from the gatherer:
# `.github/scripts/gather_changelog.py` is this repository's release
# automation, and a shipped script does not depend on it.
MARKER = re.compile(r"^<!-- specs/(\S+) -->$", re.M)


def gathered_fragments(root, rev):
    """The work item ids whose changelog fragment the tip's `CHANGELOG.md`
    has gathered -- read off the marker each gather writes, at `rev`.

    One `read_blobs` call and no path list: the question is what one file
    says, never which files exist.

    **A marker counts only on a live line**, read through
    `unverified_check.py#live_lines` as `folded_items` reads `docs/`. A
    gathered fragment is EXCUSED from the sweep, so a marker quoted in a fence,
    an HTML comment or a code span must not excuse one — that is the silent
    direction, a removal nobody is told about. A marker the reader parks by
    mistake keeps a fragment in the sweep, which a person sees."""
    text = read_blobs(root, rev, [CHANGELOG]).get(CHANGELOG, "")
    return {
        marker
        for line, live in reader().live_lines(text.splitlines())
        if live
        for marker in MARKER.findall(line)
    }


def a_gathered_fragment(path, gathered):
    """True for `<x>/specs/<id>/changelog.md` whose `<id>` is in `gathered` --
    `seal/specs/<id>/changelog.md`, and the pre-0.4.0 `specs/<id>/changelog.md`
    as well; `corrected` reads the held text at exactly the paths this accepts.

    A gathered fragment is the released entry one file over: its text stands
    verbatim under a version heading of `CHANGELOG.md`, whether the release
    that gathered it leaves the file standing, as this repository's gatherer
    does until `settle` retires the work item, or deletes it. So it is out
    of the pool and out of the range on both sides, the way a released
    section is -- and an ungathered fragment is in, because it is this
    release's own prose.

    A sibling of `records_a_past_state` rather than a parameter on it,
    because that predicate is a pure function of the path and this one is
    not: it needs the tip's `CHANGELOG.md`, so it carries its own argument
    and is applied beside the other in `corrected` and `corpus`."""
    parts = path.replace("\\", "/").split("/")
    if "specs" not in parts:
        return False
    inside = parts[parts.index("specs") + 1 :]
    return len(inside) == 2 and inside[1] == "changelog.md" and inside[0] in gathered


# The fold record's one reader, loaded by path the way `chain_check.py#load`
# loads it from this same directory. It answers both arms of what a
# retirement is: the marker (`folded_items`) and the rule (`retired_by_rule`).
HERE = os.path.dirname(os.path.abspath(__file__))
READER = os.path.join(HERE, "..", "..", "verify", "scripts", "unverified_check.py")
# A work item's directory, read off a path: the `seal/` root's `specs/`, or
# the top-level `specs/` a repository from before 0.4.0 still carries. Local
# mode is never committed, so it never reaches a range. Anchored at the start,
# so `docs/specs/<name>/` is a directory of prose like any other and stays in
# the range (round 1's finding 4).
WORK_ITEM_DIR = re.compile(r"^((?:seal/)?specs/[^/]+)/")


def reader():
    """`unverified_check.py`, or a sentence saying why it cannot be read."""
    if not os.path.isfile(READER):
        raise Refused(
            f"cannot read {READER}, which says what a retirement is. This "
            "script ships beside it under `skills/`."
        )
    spec = importlib.util.spec_from_file_location("specseal_unverified_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def retired_directories(root, a, b, paths):
    """The work item directories this range retired, by either arm.

    A directory is retired when it is gone at `b` and was either folded — its
    `<!-- specs/<id> -->` marker is in `docs/` — or retired by the rule: at
    `a` it held no `spec.md` and nothing open, which is
    `unverified_check.py#retired_by_rule`, the predicate `settle` and the other
    two CI readers ask. Never re-derived here.
    """
    candidates = sorted(
        {m.group(1) for m in map(WORK_ITEM_DIR.match, paths) if m is not None}
    )
    if not candidates:
        return set()
    loaded = reader()
    folded = loaded.folded_items(root)
    out = set()
    for directory in candidates:
        if loaded.tree_at(root, b, directory):
            continue
        if os.path.basename(directory) in folded or loaded.retired_by_rule(
            root, a, directory
        ):
            out.add(directory)
    return out


def corpus(root, rev):
    """`{path: [Sentence]}` for the tree at `rev`, less what is excluded --
    what `records_a_past_state` names, and the changelog fragments the tip's
    `CHANGELOG.md` has gathered."""
    gathered = gathered_fragments(root, rev)
    paths = [
        p
        for p in tracked(root, rev)
        if not records_a_past_state(p) and not a_gathered_fragment(p, gathered)
    ]
    return {
        path: sentences(path, text)
        for path, text in read_blobs(root, rev, paths).items()
    }


# --- the check -------------------------------------------------------------


def corrected(root, a, b):
    """`[Sentence]` -- what the range removed -- the n-grams it wrote, and
    the gathered n-grams that split `CHANGELOG.md`'s removed sentences alone.

    A sentence counts as corrected when the file holds it FEWER times at `b`
    than at `a`. Counted rather than tested for membership, so a sentence
    corrected in one place and left standing in another place of the SAME file
    is still corrected -- which is #267's shape, where the docstring was
    repaired and two ledger rows were not.

    The second return is the n-grams of the sentences the range ADDED. Those
    are the wording the fix wrote, and subtracting them is what makes the score
    mean *removed*: a phrase the fix kept is not a phrase the fix corrected.
    Only the added sentences, never the whole after-file, or a same-file
    survivor would cancel itself out.

    **A work item's round records are out of this list, as they are out of the
    pool** (#365). The pool refuses them because a record quoting a defective
    sentence is not a place that still instructs anybody; the range refuses
    them for the mirror reason. A reviewer's report quotes that sentence
    verbatim, so a record left in the range counts as wording the fix wrote
    and `wanted` subtracts the very survivor the quotation is about -- which
    made every branch that went through review report success having measured
    nothing. The work item's own `survivors.md` is out for the same reason
    one step stronger (#507): its rows quote the surviving wording by design,
    so committed inside the range it subtracted the survivors it was written
    to excuse, and the `exempt` lines that would have shown the grounds never
    printed. `records_a_past_state` is the one predicate for the class, and
    `corpus` applies the same one.

    **The filter goes on `paths`, so it holds on both sides of the range.** A
    sentence REMOVED from a record is not corrected wording either, and
    filtering the added side alone would leave this function naming a
    coordinate inside a record of a past state as the place a claim was
    corrected.

    **A rename is read as a deletion plus an addition** (`--no-renames`,
    #551), **and a sentence that arrives verbatim at another path is held,
    not written** (#563, `paired_across_paths`). With git's rename
    detection on, a move with one sentence reworded -- a rename to git too,
    `R096` when measured on a forty-paragraph file -- never listed the old
    path, so the reworded sentence never became a source and its copy in
    another file was never reported. Read as a deletion plus an addition,
    that sentence is removed and looked for. The rest of the moved text was
    then written back as the range's own, and it subtracted every n-gram it
    shared with a correction made elsewhere in the same range, so a quote
    the move carried along hid itself and every other copy of the claim.
    Paired across paths it is neither removed nor written, and a pure move
    removes nothing, which is why it is silent.

    **The release commit is held, not removed** (round 1's 🟡 1, round 2's
    🟡 1 and 🟡 2). In a repository that lets the entry accumulate under
    `## Unreleased`, the release moves that section under a version heading.
    The section is live at `a` and blanked at `b`, so counted as any other
    file it reads as every sentence removed, and a document restating an
    entry is reported at the release with nothing anybody may correct. So
    for `CHANGELOG.md` the sentences this range put under a version heading
    -- the released sentences at `b` beyond those at `a` -- are added to the
    held count before the difference is taken; a sentence standing in an
    older release holds nothing. And where the file lost a sentence, their
    fresh wording is written, as any file's is: an entry reworded as it is
    released splits the removed sentence into the runs it no longer shares,
    and withholding it would merge them into one that never clears the
    floor. A gathered fragment's text is held and not written as the
    range's own, because the fragment's own branch wrote it, not this
    range: a release that renames `## Unreleased` or rewords an entry loses
    a sentence, and the gathered wording would then subtract the survivor a
    correction in the same commit left standing in another file (round 3's
    🟡 1, #557). Of a gathered sentence, only the n-grams that also occur in a
    sentence THIS file lost count, and they are the third return rather than
    part of `written`: `score` subtracts them from `CHANGELOG.md`'s removed
    sentences alone, so a live entry the release replaced with a gathered
    fragment rewording it is still split into the runs it no longer shares,
    as a reworded release is, while no gathered text subtracts another
    file's sentence. A release that removes no live sentence writes nothing
    at all."""
    names = git(root, "diff", "--name-only", "--no-renames", "-z", a, b)
    if names is None:
        raise Refused(f"cannot diff {a[:7]}..{b[:7]} in {root}")
    # A fragment gathered at the tip is out on both sides too (#307): the
    # range that gathers it writes its text under a version heading, which
    # is blanked. This repository's gatherer leaves the fragment where it
    # is, and one that deletes it, or a range that edits a gathered one,
    # would otherwise put the fragment's sentences in the list as removed,
    # and their live copies -- the work item's own `spec.md` and
    # `overview.md` -- would be reported at the release.
    gathered = gathered_fragments(root, b)
    paths = [
        path
        for path in names.split("\0")
        if path
        and not records_a_past_state(path)
        and not a_gathered_fragment(path, gathered)
    ]
    # A retired directory is out of the range too (#517), for the reason the
    # round records are: its sentences stand in `docs/` by design, because
    # that is what a fold is, and the removed spec is not a place that still
    # instructs anybody. It leaves AFTER the pairing below and not here
    # (#591): a sentence a fold carries verbatim into `docs/` is a move, and
    # dropped before the pairing its arrival paired with a correction the
    # same range made elsewhere, and held it.
    retired = retired_directories(root, a, b, paths)
    before = read_blobs(root, a, paths)
    after = read_blobs(root, b, paths)
    # A gathered fragment's text stands under a version heading at `b`, and
    # this range did not write it -- the fragment's own branch did. Read at
    # `a`, where it stands whether the release leaves the fragment or deletes
    # it, so `moved` below can hold that text without writing it as this
    # range's. The paths are the ones `a_gathered_fragment` accepts, never a
    # second spelling of them (#564): a fragment that predicate kept out of
    # the range and this reader did not find was written all the same.
    fragments = (
        [path for path in tracked(root, a) if a_gathered_fragment(path, gathered)]
        if gathered
        else []
    )
    shipped = {
        sentence.key
        for path, text in read_blobs(root, a, fragments).items()
        for sentence in sentences(path, text)
    }
    gone, fresh, split = [], [], set()
    for path in paths:
        was = sentences(path, before[path]) if path in before else []
        now = sentences(path, after[path]) if path in after else []
        moved = []
        if path == CHANGELOG and path in after:
            # A release moves `## Unreleased` under a version heading. What
            # THIS range put under one is held, never a heading the file
            # already had: a sentence standing in an older release is not
            # what a correction to the live section kept.
            moved = newly_released(path, before.get(path, ""), after[path])
        counted = Counter(s.key for s in now + moved)
        seen, lost = Counter(), len(gone)
        for sentence in was:
            seen[sentence.key] += 1
            if seen[sentence.key] > counted[sentence.key]:
                gone.append(sentence)
        if len(gone) == lost:
            # Nothing of this file was removed, so there is nothing the moved
            # section's wording could split; a gathered release writes none.
            moved = []
        # Held above like any released sentence, never written whole: a
        # release that renames `## Unreleased` or rewords an entry loses a
        # sentence, and the gathered text would then subtract the survivor a
        # correction in the same commit left standing in another file.
        held = [sentence for sentence in moved if sentence.key in shipped]
        moved = [sentence for sentence in moved if sentence.key not in shipped]
        # ...except against what THIS file lost: a live entry the release
        # replaced with a gathered fragment rewording it is still split by
        # that rewording, as a reworded release is (step A's round 2 🟡 1).
        # Those n-grams are kept apart from `written`, which every file's
        # removed sentences are scored against, and `score` subtracts them
        # from this file's alone: written for every file, a fragment quoting
        # wording the same commit corrected elsewhere would subtract that
        # survivor again (round 2's 🟡 1).
        lost_here = {gram for sentence in gone[lost:] for gram in sentence.grams()}
        for sentence in held:
            split.update(gram for gram in sentence.grams() if gram in lost_here)
        old, new = Counter(s.key for s in was), Counter()
        for sentence in now + moved:
            new[sentence.key] += 1
            if new[sentence.key] > old[sentence.key]:
                fresh.append(sentence)
    # Only after every path is counted: a sentence that left one path and
    # arrived at another is a move, and neither side of it is this range's.
    gone, fresh = paired_across_paths(gone, fresh, set(after))
    # A retired directory is gone at `b`, so it added nothing to `fresh`.
    gone = [
        sentence
        for sentence in gone
        if not any(sentence.path.startswith(d + "/") for d in retired)
    ]
    written = {gram for sentence in fresh for gram in sentence.grams()}
    return gone, written, split


def paired_across_paths(gone, fresh, present=frozenset()):
    """`(gone, fresh)` less every sentence the range moved between paths.

    A sentence removed at one path and added verbatim at another -- the same
    key, paired one for one -- is neither removed nor written (#563). It is
    the counting rule `corrected` already applies inside one file, where a
    reordered sentence is neither, applied across files: a move changes no
    sentence's author, so the moved text is held the way a gathered
    fragment's is. A file moved whole, a rename and a document split into
    two that both remain are all this shape; no whole-file rule sees the
    split.

    **Which departure an arrival pairs with is the move's own origin**
    (#592). A key removed at two paths and added at one -- a correction at
    one, a move at the other -- used to pair with the first in path order,
    and the report's `corrected` line then named the path that only moved.
    So the pairs are taken by the departure path's affinity to the arrival
    path -- the distinct keys that left the one and arrived at the other --
    then by the departure's path being gone at `b` (not in `present`), then
    by path order. A file moved whole or a section split off shares every
    key it carried with its destination, and a correction shares the one.
    The verdict is the same whichever departure pairs, because the key and
    so its n-grams are; only the source's coordinate moves.

    The two lists can only meet across paths: within one path, a key is
    either counted down or counted up, never both. A pair leaves `gone`
    only when every n-gram it has is in `written` anyway, so `wanted` can
    only grow -- and a larger `wanted` can join two runs into one, which
    `weigh` scores by its rarest n-gram. That is the score the same text
    gets had it not moved."""
    departures, arrivals = {}, {}
    for at, sentence in enumerate(gone):
        departures.setdefault(sentence.key, {}).setdefault(sentence.path, [])
        departures[sentence.key][sentence.path].append(at)
    for at, sentence in enumerate(fresh):
        if sentence.key in departures:
            arrivals.setdefault(sentence.key, {}).setdefault(sentence.path, [])
            arrivals[sentence.key][sentence.path].append(at)
    # Counted per path rather than per sentence, so a fold moving three
    # hundred rows that share a date cell is three hundred pairs, not
    # ninety thousand candidates.
    affinity = Counter(
        (origin, destination)
        for key, found in arrivals.items()
        for origin in departures[key]
        for destination in found
    )
    held, moved = set(), set()
    for key, found in arrivals.items():
        origins = {path: deque(at) for path, at in departures[key].items()}
        destinations = {path: deque(at) for path, at in found.items()}
        order = sorted(
            (
                -affinity[(origin, destination)],
                origin in present,
                departures[key][origin][0],
                found[destination][0],
                origin,
                destination,
            )
            for origin in origins
            for destination in destinations
        )
        for *_rank, origin, destination in order:
            while origins[origin] and destinations[destination]:
                held.add(origins[origin].popleft())
                moved.add(destinations[destination].popleft())
    return (
        [sentence for at, sentence in enumerate(gone) if at not in held],
        [sentence for at, sentence in enumerate(fresh) if at not in moved],
    )


def wanted(gone, written):
    """The n-grams worth looking for: removed, and not written back."""
    keep = set()
    for sentence in gone:
        keep.update(sentence.grams())
    return keep - written


def carriers(pool, keep):
    """`{ngram: [Sentence]}` and `{ngram: files}` over the corpus."""
    where, files = {}, {}
    for found in pool.values():
        here = set()
        for sentence in found:
            for gram in sentence.grams():
                if gram in keep:
                    where.setdefault(gram, []).append(sentence)
                    here.add(gram)
        for gram in here:
            files[gram] = files.get(gram, 0) + 1
    return where, files


def runs(sequence, shared):
    """The maximal stretches of `sequence` whose n-grams are all shared.

    **This is what makes the score count evidence rather than n-grams**, and it
    was measured rather than reasoned. The one clear false positive in the
    first calibration run shared *be a second reader of the* -- a single
    six-word run, which at `n = 3` is four overlapping n-grams, each scored on
    its own for about 6 bits, totalling 26. The two real survivors of #267 and
    #269 each shared TWO stretches that do not touch: *the join's ... argument*
    together with *never a leaf*, and *from this report once* together with
    *has verified its findings*.

    So the discriminator is not how much wording is shared, it is **how many
    independent places it is shared in**. Overlapping n-grams are one piece of
    evidence written four ways."""
    out, current = [], []
    for gram in sequence:
        if gram in shared:
            current.append(gram)
            continue
        if current:
            out.append(current)
            current = []
    if current:
        out.append(current)
    return out


def weights(pool_size, files):
    """`{ngram: weight}`, where 1.0 is *this phrase occurs nowhere else*.

    `log2(F / df)` over `log2(F)`. A one-file corpus has no elsewhere, so
    every weight is zero and nothing can be reported -- which is the honest
    answer rather than a division by zero."""
    scale = math.log2(pool_size) if pool_size > 1 else 0.0
    if scale <= 0:
        return {}
    return {
        gram: math.log2(pool_size / count) / scale
        for gram, count in files.items()
        if count > 0
    }


def weigh(sequence, shared, weight_of):
    """`(score, [(phrase, weight)])` for one source-candidate pair.

    A run is scored by its RAREST n-gram, never by the sum of them. A run
    carrying a phrase that only two files have is at least as unlikely as that
    phrase, so the rarest one is a sound floor on the whole run's
    improbability -- and summing the overlaps would count the same evidence
    once per position it can be read from."""
    total, named = 0.0, []
    for run in runs(sequence, shared):
        best = max(run, key=lambda gram: weight_of.get(gram, 0.0))
        weight = weight_of.get(best, 0.0)
        if weight <= 0:
            continue
        total += weight
        # The whole run, not its rarest n-gram: a reader looking for the
        # survivor searches for words, and three of them are harder to find
        # than the phrase they sit in.
        # Consecutive n-grams overlap by `N - 1` words, so the run's own text
        # is the first one plus the last word of each that follows it.
        phrase = " ".join([run[0]] + [gram.split()[-1] for gram in run[1:]])
        named.append((phrase, weight))
    return total, named


def score(gone, keep, where, weight_of, floor, split=frozenset()):
    """`[(score, candidate, source, shared)]`, worst first.

    `shared` is the phrases a candidate has in common with the sentence it
    matched, each with what it contributed, so the report can name the wording
    rather than print a number nobody can act on.

    One candidate is reported once, against its best-scoring source. A
    restated fact reaches several sentences of one paragraph, and reporting the
    same coordinate three times would spend a reader's attention on the
    scoring rather than on the survivor."""
    found = {}
    for source in gone:
        sequence = source.grams()
        mine = set(sequence) & keep
        if source.path == CHANGELOG:
            # What a gathered rewording shares with the entry it replaced
            # splits that entry, and no other file's sentence (`corrected`).
            mine -= split
        reached = {}
        for gram in mine:
            if weight_of.get(gram, 0.0) <= 0:
                continue
            for candidate in where.get(gram, ()):
                # **No self-match guard, and it took a probe to see why one
                # was wrong.** The obvious guard skips a candidate at the
                # source's own path and line -- but the source is read at `a`
                # and the candidate at `b`, so equal line numbers are two
                # different revisions of one file and not one sentence. A
                # probe where a claim was corrected in the first of two
                # copies in one file put both at line 5, and the guard threw
                # away the survivor it exists to find.
                #
                # None is needed, because `corrected` counts. A sentence is a
                # source only where the file holds it FEWER times at `b`, so
                # an occurrence still there is by construction a different
                # one, and a sentence that merely moved never becomes a
                # source at all.
                reached.setdefault(id(candidate), [candidate, set()])[1].add(gram)
        for candidate, shared in reached.values():
            total, named = weigh(sequence, shared, weight_of)
            if total < floor:
                continue
            best = found.get(id(candidate))
            if best is None or total > best[0]:
                found[id(candidate)] = (total, candidate, source, named)
    return sorted(found.values(), key=lambda row: -row[0])


def examine(root, a, b, floor=FLOOR):
    """The whole run: `(rows, files examined, sentences corrected)`.

    Every caller goes through this. It returns the two counts as well as the
    rows because the report line names what was examined -- a check that says
    only what it found cannot be told apart from one that looked at nothing."""
    gone, written, split = corrected(root, a, b)
    keep = wanted(gone, written)
    pool = corpus(root, b)
    where, files = carriers(pool, keep)
    return (
        score(gone, keep, where, weights(len(pool), files), floor, split),
        len(pool),
        len(gone),
    )


def survivors(root, a, b, floor=FLOOR):
    """`examine`'s rows alone, for a caller that wants only the survivors."""
    return examine(root, a, b, floor)[0]


# --- the exemptions --------------------------------------------------------


# A first cell naming a range rather than a path, which is what tells the two
# row shapes apart. A path cannot match it: the dots need a non-space word on
# BOTH sides, so `../notes.md` is a path and `A..B` is a range.
RANGE_CELL = re.compile(r"^[^\s|]+\.\.\.?[^\s|]+$")

# The work item a `survivors.md` belongs to, read off the file's own path. It
# is the declaration's SECOND anchor, and without it the row has effectively
# one that does not hold: `hygiene.yml` hands every `seal/specs/*/survivors.md`
# in the tree to every run, and the spelling this module recommends --
# `origin/<base>...HEAD` -- re-resolves on each checkout, so one merged row
# matched every later branch cut from the same base and excused its whole run.
#
# The owner is the `seal/specs/<id>` prefix wherever the file sits beneath it
# (#304). The tail used to be `[^/]+$`, one segment, so a `survivors.md` one
# directory deeper had no owner -- and an ownerless declaration is not asked
# the ownership question, so it kept the unbounded reach the question exists
# to refuse, in silence. Not anchored at the start, because `--exempt` paths
# may be absolute; a file outside any `seal/specs/<id>/` keeps the hand-run
# reach `whole_range` documents, and the pre-0.4.0 top-level `specs/` root is
# left out on purpose (`spec.md` §*Out* of work item 1790174139).
#
# A local-mode file matches too, `<git-common-dir>/seal/specs/<id>/`, and its
# owner is never in a range's diff because nothing there is committed; so
# `whole_range` asks that work item's `routing.md` instead (#554).
OWNER_DIR = re.compile(r"(?:^|.*/)(seal/specs/[^/]+)/.+$")

# The routing declaration's one reader, loaded by path the way
# `chain_check.py` loads it. Its `Branch` row is who owns a local-mode
# declaration.
ROUTING = os.path.join(HERE, "..", "..", "..", "hooks", "routing.py")
# Where the common git directory is, and so local mode's root: the one reader
# `hooks/optin.py` keeps for every gate, never a second copy of it here.
OPTIN = os.path.join(HERE, "..", "..", "..", "hooks", "optin.py")


def hook(path, name, what):
    """A module under `hooks/`, loaded by path, or `Refused` saying which.

    The hooks ship beside this script in the plugin; a copy without one
    cannot place a local-mode declaration, and that is unusable input
    rather than a judgment. `what` is what the missing file answers."""
    if not os.path.isfile(path):
        raise Refused(
            f"cannot read {path}, which {what}. "
            "This script ships beside it in the plugin."
        )
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def local_specs(root):
    """The real path of local mode's `specs/` directory, or "".

    `<git-common-dir>/seal/specs`, where `agent-contract` §16 puts the local
    root, the common directory read by `hooks/optin.py#git_common_dir`.
    Real paths and `normcase`, because a temporary directory on macOS sits
    behind a symlink, and Windows spells one drive two ways."""
    common = hook(
        OPTIN, "specseal_optin", "says where local mode's seal/ root is"
    ).git_common_dir(root)
    if not common:
        return ""
    return os.path.normcase(os.path.realpath(os.path.join(common, "seal", "specs")))


def local_item(source, local):
    """The local-mode work item directory `source` sits in, or None."""
    if not local:
        return None
    where = os.path.normcase(os.path.realpath(source))
    if not where.startswith(local + os.sep):
        return None
    return os.path.join(local, os.path.relpath(where, local).split(os.sep)[0])


def on_its_branch(root, item, b):
    """None when the range's tip `b` is on the branch `item`'s `routing.md`
    names -- `refs/heads/<Branch>` or an ancestor of it -- and on no local
    branch that one was cut from; otherwise the reason it is not, as the
    `not yours` line prints it.

    Asked of the range's tip rather than of the checkout, because ownership
    is a question about the range: a detached HEAD at the branch's tip is
    the same range. A branch cut from another carries that branch's history,
    so a tip on it may be the other branch's tip, and that range is the
    other branch's run: a stacked child's row would otherwise excuse its
    parent's whole range. A `routing.md` that is missing, will not parse or
    names no branch, and a branch that does not resolve, each answer with
    their own reason -- the declaration then prints under `not yours`,
    which is the loud direction."""
    routing = hook(
        ROUTING, "specseal_routing", "says whose a local-mode declaration is"
    )
    try:
        with open(os.path.join(item, "routing.md"), encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return "it has no routing.md this run can read"
    declared = routing.parse(text)
    if not declared:
        return "its routing.md is not a declaration naming a branch"
    ref = f"refs/heads/{declared['branch']}"
    tip = resolves(root, ref)
    if tip is None:
        return f"the branch its routing.md names, {declared['branch']}, is not here"
    if git(root, "merge-base", "--is-ancestor", b, ref) is None:
        return "this range's tip is not on the branch its routing.md names"
    # A branch cut from another carries that branch's history, so a tip on
    # it can be the tip of a branch it was cut from -- that branch's run, and
    # a stacked child's row would otherwise excuse its parent's whole range.
    heads = git(
        root, "for-each-ref", "--contains", b, "--format=%(objectname)", "refs/heads"
    )
    for head in set((heads or "").split()) - {tip}:
        if git(root, "merge-base", "--is-ancestor", head, ref) is not None:
            return (
                "this range's tip is on a branch the one its routing.md names "
                "was cut from"
            )
    return None


def read_exemptions(paths):
    """`([(path, quote_words, grounds)], [(range_spec, grounds, source_file)])`.

    TWO row shapes, told apart by the first cell, and both live in the same
    `survivors.md`:

      `| Path | Quote | Grounds |`    one judged survivor. The quote is the
          anchor and it is matched on normalised words, so a backtick or a
          line break in either the row or the surviving text does not decide
          whether an exemption holds.

      `| Range | Grounds |`          a whole range, for #297. A branch that
          DELETES a shipped section leaves every sentence of it standing in
          the durable copies that are supposed to survive a deletion, and
          #293's own range reported 153 of them at 1.60-1.62 -- every one
          correct as a report and none of them a defect. 153 written
          sentences is not an escape anybody takes; a branch turns the check
          off instead, which is the outcome the escape exists to prevent.

    **A range row is anchored on TWO things**, and the range alone was not
    enough. Run the check over a different range and the row does not hold --
    but `origin/<base>...HEAD`, the spelling CI passes and this module
    recommends, is not a range, it is a RELATION, and it re-resolves to
    whatever range the checkout it is read on is over. So the second anchor is
    the work item the file lives in, which is why the path is carried in the
    tuple. Between them a declaration cannot outlive the deletion it was
    written for, and it cannot be a standing *check nothing* -- which this
    design still has no value for.

    A range row with no grounds is NOT a row. The grounds are the whole
    content of the escape: what a reviewer reads is the written sentence, and
    a row without one silences 153 places on the strength of nothing.
    """
    rows, ranges = [], []
    for path in paths:
        if not os.path.isfile(path):
            raise Refused(f"--exempt {path} does not exist")
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        # Counted per FILE, not per run. Checking the accumulated total would
        # let a second `--exempt` naming an empty file pass on the strength of
        # the first one's rows, which is the direction a checker of claims must
        # not fail in.
        before = len(rows) + len(ranges)
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) < 2:
                continue
            if set("".join(cells)) <= set("-: "):
                continue
            first = cells[0].strip("`").strip()
            # The range shape is tested FIRST, because it is the narrower
            # pattern: a path never matches `RANGE_CELL`, so nothing that is
            # a per-survivor row can be captured here.
            if RANGE_CELL.match(first):
                if cells[1]:
                    # The file is carried so `whole_range` can ask whose
                    # declaration this is. A row with no work item directory
                    # above it -- an `--exempt` file passed from anywhere --
                    # keeps the old reach, because there is nothing to scope it
                    # to and refusing it would break running the check by hand.
                    ranges.append((first, cells[1], path))
                continue
            if len(cells) < 3:
                continue
            quote = words(cells[1])
            if not first or first.lower() == "path" or not quote:
                continue
            rows.append((first, quote, cells[2]))
        if len(rows) + len(ranges) == before:
            raise Refused(
                f"--exempt {path} holds no `| Path | Quote | Grounds |` or "
                "`| Range | Grounds |` row. An exemption file with nothing in "
                "it silences nothing, and reading it as empty would hide the "
                "fact that it was not written"
            )
    return rows, ranges


def whole_range(root, ranges, a, b):
    """`(match, unresolved, foreign)` for the declarations handed to this run.

    Resolved rather than string-matched, because the two spellings of one
    range are both real: CI runs `origin/<base>...HEAD`, which is what a
    session copies into the declaration, and a person running it by hand
    types two oids. Comparing the text would refuse the same range for being
    spelled the other way.

    **Resolving is also why the range alone was not an anchor.**
    `origin/<base>...HEAD` is not a range, it is a RELATION, and it resolves to
    whatever range the checkout it is read on is over. `hygiene.yml` hands
    every `seal/specs/*/survivors.md` in the tree to every run, and a
    `survivors.md` lives until the release that ships it -- so one merged
    declaration in that spelling matched every later branch cut from the same
    base, excused every one of its survivors and turned the step off for the
    rest of the release. That is the outcome the escape exists to prevent,
    arriving through the escape.

    So a declaration is also its work item's. It holds only over a range that
    touches the directory the file sits in, and a work item's own range always
    does -- its routing declaration is committed there before its first edit.
    A `survivors.md` outside any work item directory keeps the old reach:
    there is nothing to scope it to, and refusing it would break running the
    check by hand.

    **In local mode the directory is never in a range** (#554): the root is
    `<git-common-dir>/seal/` and nothing under it is committed, so the test
    above refused every work item its own range row. There a declaration is
    its work item's when the range's tip is on the branch that work item's
    `routing.md` names and on no local branch that one was cut from
    (`on_its_branch`), which also says why when it is not. Local files are
    shared by every
    worktree of the clone, so the branch is what keeps a relation-spelled
    row off another branch's range. Shared mode keeps the diff test: a pull
    request's CI checkout is a detached merge commit with no branch ref.

    **Ownership is asked only of a declaration that WOULD have matched**, and
    a refused one is returned in `foreign` so the report prints it. A row that
    quietly stopped applying is the one failure a rotting anchor must not
    have, and that rule binds in this direction too -- a declaration a work
    item wrote for its own range and cannot use is a line somebody has to
    read, not a silence. Testing the range first is also what keeps the
    `git diff` out of every run that has no matching declaration.

    **A spec that will not resolve is REPORTED, never exit 2**, and that is a
    landmine avoided rather than leniency. A `survivors.md` lives in the tree
    from the work item's first row until the release that ships it, and the
    refs its range names -- a release branch -- get deleted. Refusing the run
    then would turn every later range's check into exit 2 over a row that has
    nothing to do with it.

    **And it is reported to the run it addresses, which the second anchor
    decides** (#439). A declaration that resolves nowhere and belongs to a
    work item this range touches nothing of is the *not this run's range*
    case one step over: it could not have excused this run whether or not
    it resolved, so the line would be addressed to nobody -- and it was, on
    every pull request into a release branch and every seal, three times per
    run for one release, because every shipped `survivors.md` in the tree
    names a release branch that is deleted at the release. So ownership is
    asked of an unresolved declaration before it is printed, by the same
    test a resolved one gets -- the lazily computed `changed` list in shared
    mode, `on_its_branch` in local mode: one with no owner -- an `--exempt`
    file passed from anywhere -- or owned by a work item this range touches
    (in local mode, one `on_its_branch` accepts) is a declaration this run
    could have used, and prints under `unresolved` as before. The wrong
    allow is empty, because an unresolved row excuses nothing whether
    printed or not.
    """
    match, unresolved, foreign = None, [], []
    changed = local = None
    for spec, grounds, source in ranges:
        try:
            left, right = parse_range(root, spec)
        except Refused:
            left = right = None
        if left is not None and (left, right) != (a, b):
            # Not this run's range at all, which needs no line: the row is
            # honest and says so itself. Only a row that resolved ONTO this
            # range and is then refused has something a reader must be told.
            continue
        owner = OWNER_DIR.match(source.replace("\\", "/"))
        mine, item, why = True, None, "this range touches nothing in it"
        if owner is not None:
            if local is None:
                local = local_specs(root)
            item = local_item(source, local)
        if owner is not None and item is not None:
            # Local mode: nothing under the root is committed, so the owner
            # is never in `changed`, and the work item's branch answers --
            # with the reason it refused, when it does.
            why = on_its_branch(root, item, b)
            mine = why is None
        elif owner is not None:
            if changed is None:
                # `--no-renames` for the reason `corrected` gives: a file
                # moved out of a work item's directory is a change to that
                # directory, and rename detection would list only where it
                # went.
                names = git(root, "diff", "--name-only", "--no-renames", "-z", a, b)
                changed = [path for path in (names or "").split("\0") if path]
            mine = any(path.startswith(owner.group(1) + "/") for path in changed)
        if left is None:
            # Unresolved: printed to a run that could have used it, and to
            # no other. Nothing is silenced either way.
            if mine:
                unresolved.append((spec, grounds))
            continue
        if not mine:
            # The reason is the test that refused it, so a person reading
            # the line knows which file to open.
            foreign.append((spec, grounds, owner.group(1), why))
            continue
        if match is None:
            match = (spec, grounds)
    return match, unresolved, foreign


def exempted(candidate, rows):
    """The grounds that exempt this candidate, or None.

    The path matches when the row names the candidate's path or a suffix of it,
    so a row written in a repository read from another directory still holds.
    The quote matches when its words appear as a contiguous run in the
    candidate's own -- which is what makes the exemption rot loudly: edit the
    surviving text and the run is gone and the survivor is reported again."""
    for where, quote, grounds in rows:
        target = candidate.path.replace("\\", "/")
        if target != where and not target.endswith("/" + where.lstrip("/")):
            continue
        span = candidate.words
        for at in range(len(span) - len(quote) + 1):
            if span[at : at + len(quote)] == quote:
                return grounds
    return None


# --- the report ------------------------------------------------------------


def trim(text, width=150):
    """One line, short enough to read, with what was cut made visible."""
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 1] + "…"


def report(
    rows,
    exemptions,
    a,
    b,
    examined,
    corrected_count,
    out=sys.stdout,
    whole=None,
    unresolved=(),
    foreign=(),
):
    """Print the survivors and answer with the exit code.

    `whole` is the `(range_spec, grounds)` declaration covering this exact
    range, and it excuses every candidate. `unresolved` is the declarations
    whose range does not resolve here and that this run could have used --
    which `whole_range` decides by the second anchor, so one owned by a work
    item the range touches nothing of (in local mode, one `on_its_branch`
    refuses) never arrives (#439); they silence
    nothing and are printed, because a declaration that quietly stopped
    applying is the one failure a rotting anchor must not have. `foreign` is
    the same failure one step
    over: a declaration that resolved onto this exact range and belongs to a
    work item the range does not touch -- in local mode, one `on_its_branch`
    refused -- printed with the work item it came from and the reason that
    refused it.
    """
    standing, excused = [], []
    for score, candidate, source, shared in rows:
        grounds = whole[1] if whole else exempted(candidate, exemptions)
        (excused if grounds else standing).append(
            (score, candidate, source, shared, grounds)
        )

    print(
        f"survivor-check: examined {examined} files at {b[:7]}, against "
        f"{corrected_count} sentence(s) the range {a[:7]}..{b[:7]} removed",
        file=out,
    )
    for spec, grounds in unresolved:
        print(
            f"  unresolved  {spec} does not resolve here, so it silences "
            f"nothing -- {trim(grounds, 80)}",
            file=out,
        )
    for spec, grounds, owner, why in foreign:
        print(
            f"  not yours   {spec} was written by {owner} and {why}, so it "
            f"silences nothing -- {trim(grounds, 80)}",
            file=out,
        )
    if whole:
        print(
            f"  declared    the whole range {whole[0]} -- {trim(whole[1], 100)}",
            file=out,
        )
    for _score, candidate, _source, _shared, grounds in excused:
        print(f"  exempt   {candidate.where()} -- {trim(grounds, 100)}", file=out)
    if not standing:
        # Two different facts, and the second one used to print the first's
        # sentence. `no removed wording is still standing` is false when a
        # survivor was found and excused, and a person reading it would take
        # the exemption rows above for something other than what silenced the
        # run.
        print(
            f"  every survivor is excused by a row above ({len(excused)})"
            if excused
            else "  no removed wording is still standing",
            file=out,
        )
        return 0

    print("", file=out)
    for score, candidate, source, shared, _ in standing:
        phrases = ", ".join(
            f"“{gram}”" for gram, _w in sorted(shared, key=lambda p: -p[1])[:4]
        )
        print(f"{candidate.where()}", file=out)
        print(f"  standing    {trim(candidate.raw)}", file=out)
        print(f"  corrected   {source.where()} -- {trim(source.raw)}", file=out)
        print(
            f"  shared      {len(shared)} phrase(s), {score:.2f}: {phrases}",
            file=out,
        )
        print("", file=out)
    print(
        f"{len(standing)} place(s) still carry wording this range removed. Correct "
        "each, or record it in seal/specs/<work-item-id>/survivors.md with the "
        "grounds and a quote from the surviving text",
        file=out,
    )
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="survivor-check",
        description="Report every place still carrying wording a range removed.",
    )
    ap.add_argument(
        "--range",
        required=True,
        metavar="A..B",
        help="the fix commits. A work item directory the range retired, "
        "folded or by the rule, is left out of it on both sides",
    )
    ap.add_argument("--root", default=".", help="the repository (default: .)")
    ap.add_argument(
        "--exempt",
        action="append",
        default=[],
        metavar="FILE",
        help="a `| Path | Quote | Grounds |` table of judged survivors",
    )
    ap.add_argument(
        "--floor",
        type=float,
        default=FLOOR,
        help=(
            "the score a survivor must reach, in units of one phrase that "
            f"occurs nowhere else (default: {FLOOR})"
        ),
    )
    args = ap.parse_args(argv)
    try:
        root = os.path.abspath(args.root)
        a, b = parse_range(root, args.range)
        # Before the run rather than after it: an exemption file that will not
        # parse is exit 2, and finding that out after several seconds of
        # indexing prints a refusal underneath a report.
        exemptions, ranges = read_exemptions(args.exempt)
        # After the endpoints resolve and before the indexing, for the reason
        # the line above gives: a declaration is judged against the range this
        # run is actually over, and nothing here costs several seconds.
        whole, unresolved, foreign = whole_range(root, ranges, a, b)
        rows, examined, gone = examine(root, a, b, args.floor)
        return report(
            rows,
            exemptions,
            a,
            b,
            examined,
            gone,
            whole=whole,
            unresolved=unresolved,
            foreign=foreign,
        )
    except Refused as exc:
        print(f"survivor-check: {exc}", file=sys.stderr)
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
