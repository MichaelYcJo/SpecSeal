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
update, and `docs/flow.md`'s 0.9.3 row names it: *grep the changed sentences'
distinguishing terms across the rest of the corpus and report the survivors.*

## Why not a grep, and why not a phrase floor

Two real cases from this repository's own history rule out the two obvious
mechanics, one case each.

**A literal grep fails #269.** `7bcf36a` reworded `agents/warden.md` §6 and
left `GENERATOR_NAMED[WARDEN]` in `tests/test_the_rules_have_one_owner.py`
pinning the sentence it replaced. That pin is one sentence split across two
adjacent string literals -- `"... from this report once the "` then
`"orchestrator has verified its findings"` -- so no LINE holds the sentence and
nothing line-oriented finds it. The module was red from that commit through two
review rounds and two broad gates, because contract §2 reserves the broad gate
for the orchestrator and no round could see it.

**A longest-common-phrase floor fails #267.** `ad6f81a` corrected a docstring
that called a join's receiver *an argument ... never a leaf*, and the same
claim stood in two ledger rows, one of them the shared file. Those rows
PARAPHRASE rather than copy -- *an argument to an operand, never a leaf*
against *an argument to element 4, never a leaf of the expression* -- and the
longest identical run is three words. No floor above three accepts it, and at
three every three-word run in the corpus is accepted with it.

So the metric is rarity-weighted n-gram overlap. Weighting is what lets *never
a leaf* count while *of the expression* does not, and a summed bit score rather
than a ratio is what lets a twelve-word test needle and a three-thousand-word
ledger cell be scored on the same scale.

## What is excluded, by construction rather than by list

**A record of a past round.** Everything under a work item's `rounds/` is out.
A round record and a reviewer's report carry the SHA they were written against
and quote the defective wording verbatim -- that is what they are for, and
`skills/implement/SKILL.md` says a round record never asserts a present state.
Measured on #267's range: the corrected clause stands in `round-2.md` and
`round-2-report.md`, and reporting either would be wrong.

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

**The deliberate-duplication case is not what the escape is for.** `CLAUDE.md`
and `CONTRIBUTING.md` deliberately carry the same sentence about ledger
removals. A branch correcting it in one and not the other IS reported, and that
report is right: those two have already disagreed once, and the disagreement
left a branch with no reading that permits the only correct act. The escape is
for the third kind of carrier, text that quotes old wording in order to say it
was wrong.

## What it does not answer

It reads the tip of the range, so a survivor introduced AFTER the range is
invisible to it. It answers *did this range leave wording standing*, never *is
the tree consistent now*, which is why the report prints what it examined.
"""

import argparse
import math
import os
import re
import subprocess
import sys
from collections import Counter

# Words per n-gram. Three is the smallest that carries word order, and order is
# what separates `an argument to an operand` from `an operand to an argument`.
# The rarity weighting below, not the length, is what does the discriminating.
N = 3

# The score a candidate must reach, in bits: a floor on the summed
# `log2(F / df)` of the INDEPENDENT phrases it shares with a corrected
# sentence, where `F` is the corpus file count. It reads as *the odds of this
# much rare wording co-occurring by accident are under one in two-to-the-BITS*.
#
# **Calibrated, not chosen.** Measured over 77 real ranges -- every commit of
# five unsquashed work-item branches that carried a review chain --
# `phases/phase-3.md` holds the curve. The two real survivors this work item
# exists for score 17.6 (#269's left-behind pin) and 16.6 (#267's row R3 in
# the shared ledger), and the number sits below the weaker of them with room
# rather than pressed against it: 15 costs 26 reports over the 77 ranges where
# 16 costs 24, and a floor set at the weakest survivor already measured is a
# floor that misses the next one.
BITS = 15.0

# A candidate needs more than one INDEPENDENT phrase in common -- see `runs`
# for why independence is the thing being counted. Without this, one six-word
# coincidence read as four overlapping n-grams cleared any threshold this side
# of 26 bits, which is what the first calibration run found.
#
# Two, because the defect is a restated FACT and a fact takes more than three
# words to state. Both real survivors share exactly two.
SHARED_FLOOR = 2

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
    as a file with no sentences in it, which is a different fact."""
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
        found[path] = body.decode("utf-8", "replace")
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
BLOCK = re.compile(r"^\s*(?:[-*+>#]|\d+[.)](?=\s)|[-*_=]{3,}\s*$)")

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
    """Every sentence in `text`, struck-through spans already gone."""
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


def corpus(root, rev):
    """`{path: [Sentence]}` for the tree at `rev`, less what is excluded."""
    paths = [p for p in tracked(root, rev) if not records_a_past_round(p)]
    return {
        path: sentences(path, text)
        for path, text in read_blobs(root, rev, paths).items()
    }


# --- the check -------------------------------------------------------------


def corrected(root, a, b):
    """`[Sentence]` -- what the range removed -- and the n-grams it wrote.

    A sentence counts as corrected when the file holds it FEWER times at `b`
    than at `a`. Counted rather than tested for membership, so a sentence
    corrected in one place and left standing in another place of the SAME file
    is still corrected -- which is #267's shape, where the docstring was
    repaired and two ledger rows were not.

    The second return is the n-grams of the sentences the range ADDED. Those
    are the wording the fix wrote, and subtracting them is what makes the score
    mean *removed*: a phrase the fix kept is not a phrase the fix corrected.
    Only the added sentences, never the whole after-file, or a same-file
    survivor would cancel itself out."""
    names = git(root, "diff", "--name-only", "-z", a, b)
    if names is None:
        raise Refused(f"cannot diff {a[:7]}..{b[:7]} in {root}")
    paths = [path for path in names.split("\0") if path]
    before = read_blobs(root, a, paths)
    after = read_blobs(root, b, paths)
    gone, written = [], set()
    for path in paths:
        was = sentences(path, before[path]) if path in before else []
        now = sentences(path, after[path]) if path in after else []
        counted = Counter(s.key for s in now)
        seen = Counter()
        for sentence in was:
            seen[sentence.key] += 1
            if seen[sentence.key] > counted[sentence.key]:
                gone.append(sentence)
        old = Counter(s.key for s in was)
        fresh = Counter()
        for sentence in now:
            fresh[sentence.key] += 1
            if fresh[sentence.key] > old[sentence.key]:
                written.update(sentence.grams())
    return gone, written


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


def weigh(sequence, shared, bits):
    """`(score, [(phrase, bits)])` for one source-candidate pair.

    A run is scored by the bits of its RAREST n-gram, never by their sum. A
    run carrying a phrase that only two files have is at least as unlikely as
    that phrase, so the rarest one is a sound floor on the whole run's
    improbability -- and summing the overlaps would count the same evidence
    once per position it can be read from."""
    total, named = 0.0, []
    for run in runs(sequence, shared):
        best = max(run, key=lambda gram: bits.get(gram, 0.0))
        weight = bits.get(best, 0.0)
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


def score(gone, keep, where, bits, floor):
    """`[(score, candidate, source, shared)]`, worst first.

    `shared` is the phrases a candidate has in common with the sentence it
    matched, each with the bits it contributed, so the report can name the
    wording rather than print a number nobody can act on.

    One candidate is reported once, against its best-scoring source. A
    restated fact reaches several sentences of one paragraph, and reporting the
    same coordinate three times would spend a reader's attention on the
    scoring rather than on the survivor."""
    found = {}
    for source in gone:
        sequence = source.grams()
        mine = set(sequence) & keep
        reached = {}
        for gram in mine:
            if bits.get(gram, 0.0) <= 0:
                continue
            for candidate in where.get(gram, ()):
                # A sentence does not survive itself: the same words somewhere
                # else are a survivor, the same words at the same place are the
                # sentence the range left alone.
                if candidate.path == source.path and candidate.line == source.line:
                    continue
                reached.setdefault(id(candidate), [candidate, set()])[1].add(gram)
        for candidate, shared in reached.values():
            total, named = weigh(sequence, shared, bits)
            if len(named) < SHARED_FLOOR or total < floor:
                continue
            best = found.get(id(candidate))
            if best is None or total > best[0]:
                found[id(candidate)] = (total, candidate, source, named)
    return sorted(found.values(), key=lambda row: -row[0])


def examine(root, a, b, floor=BITS):
    """The whole run: `(rows, files examined, sentences corrected)`.

    Every caller goes through this. It returns the two counts as well as the
    rows because the report line names what was examined -- a check that says
    only what it found cannot be told apart from one that looked at nothing."""
    gone, written = corrected(root, a, b)
    keep = wanted(gone, written)
    pool = corpus(root, b)
    where, files = carriers(pool, keep)
    total = len(pool) or 1
    bits = {
        gram: math.log2(total / count) for gram, count in files.items() if count > 0
    }
    return score(gone, keep, where, bits, floor), len(pool), len(gone)


def survivors(root, a, b, floor=BITS):
    """`examine`'s rows alone, for a caller that wants only the survivors."""
    return examine(root, a, b, floor)[0]


# --- the exemptions --------------------------------------------------------


def read_exemptions(paths):
    """`[(path, quote_words, grounds)]` from the markdown tables named.

    A row is `| Path | Quote | Grounds |`. The quote is the anchor and it is
    matched on normalised words, so a backtick or a line break in either the
    row or the surviving text does not decide whether an exemption holds."""
    rows = []
    for path in paths:
        if not os.path.isfile(path):
            raise Refused(f"--exempt {path} does not exist")
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) < 3:
                continue
            if set("".join(cells)) <= set("-: "):
                continue
            where = cells[0].strip("`").strip()
            quote = words(cells[1])
            if not where or where.lower() == "path" or not quote:
                continue
            rows.append((where, quote, cells[2]))
        if not rows:
            raise Refused(
                f"--exempt {path} holds no `| Path | Quote | Grounds |` row. An "
                "exemption file with nothing in it silences nothing, and reading "
                "it as empty would hide the fact that it was not written"
            )
    return rows


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


def report(rows, exemptions, a, b, examined, corrected_count, out=sys.stdout):
    """Print the survivors and answer with the exit code."""
    standing, excused = [], []
    for score, candidate, source, shared in rows:
        grounds = exempted(candidate, exemptions)
        (excused if grounds else standing).append(
            (score, candidate, source, shared, grounds)
        )

    print(
        f"survivor-check: examined {examined} files at {b[:7]}, against "
        f"{corrected_count} sentence(s) the range {a[:7]}..{b[:7]} removed",
        file=out,
    )
    for _score, candidate, _source, _shared, grounds in excused:
        print(f"  exempt   {candidate.where()} -- {trim(grounds, 100)}", file=out)
    if not standing:
        print("  no removed wording is still standing", file=out)
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
            f"  shared      {len(shared)} phrase(s), {score:.1f} bits: {phrases}",
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
    ap.add_argument("--range", required=True, metavar="A..B", help="the fix commits")
    ap.add_argument("--root", default=".", help="the repository (default: .)")
    ap.add_argument(
        "--exempt",
        action="append",
        default=[],
        metavar="FILE",
        help="a `| Path | Quote | Grounds |` table of judged survivors",
    )
    ap.add_argument(
        "--bits",
        type=float,
        default=BITS,
        help=f"the score a survivor must reach (default: {BITS})",
    )
    args = ap.parse_args(argv)
    try:
        root = os.path.abspath(args.root)
        a, b = parse_range(root, args.range)
        # Before the run rather than after it: an exemption file that will not
        # parse is exit 2, and finding that out after several seconds of
        # indexing prints a refusal underneath a report.
        exemptions = read_exemptions(args.exempt)
        rows, examined, gone = examine(root, a, b, args.bits)
        return report(rows, exemptions, a, b, examined, gone)
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
