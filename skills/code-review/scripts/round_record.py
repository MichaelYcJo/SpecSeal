#!/usr/bin/env python3
"""round-record — write `rounds/round-N.md` from what is not prose.

Issue #161 measured the last branch of this repository: fifteen review rounds
and 22 h 47 min, of which 12.8 h sat in front of record commits, and half of
the 65 findings were located in a record rather than in code. The record is
nine parsed fields and four tables. Every one of them is derivable from
something a person did not type into a cell — the target from git, the
terminal lines and the three tables from the reviewer's report, the reach-back
from the record that came before — and the orchestrator was deriving all of
it by hand, one cell at a time, with the reviewer's report open and a fix
pass waiting.

So this writes the record. `new` takes the reviewer's report and the round
paragraph of the spawn prompt, and derives the rest.

The report is read from `<item>/rounds/round-N-report.md` where `--report` is
absent — the path the reviewer wrote it to, derived from the same two
arguments the record's own path is. It used to be a required flag pointing at
a file that did not exist: the reviewer returns its report as a message, the
orchestrator is told not to open the transcript, so the orchestrator retyped
the report to have something to pass. That is #228, and a retyped verdict row
carries retyped coordinates.

  Report              `--report`, else `<item>/rounds/round-N-report.md`; the
                      absence of both refuses and names the path
  Target SHA          `--target`, which has to resolve
  Ran by              `--ran-by`
  PR                  `--pr`, else what `gh pr view` says, else `not yet opened`
  Broad gate          `--broad-gate`, else `not yet`
  Fixes checked by    `nobody — the fixes are not yet written` while a verdict
                      is open or closed on a fix; `no fixes to check` when
                      every verdict closed without one. The two values are
                      the landing states `templates/sdd-round.md` and
                      `chain_check.fix_surface` describe, and the second
                      exists because a record that commissions no fixes will
                      never have any — *not yet written* is false of it the
                      moment it is written
  Contract changes    `none — the fixes are not yet written`, or a bare `none`
  New units           in the same two states, for the same reason
  Needs a fix         what stands after the colon in the report's line
  Loses a record or   the same, for the second line; a report lacking either
  crashes             line is refused
  Pass                ticked when no verdict row is open
  the four sections   the round paragraph verbatim; the report's verdict,
                      probe and deferred tables row for row; every `Location`
                      cell of every earlier record, deduplicated

Then it sets the previous record's `Fixes checked by` to `round-N` — the one
reach-back the orchestrator forgot five times on the last branch — and runs
`chain_check.py --worktree` on the repository, so the record is judged before
it is committed rather than by CI afterwards.

`close` is the other end of the round. It takes the smith's fix table — one
row per finding under `## Fixes`, `| # | Verdict | Commit or grounds |`, the
verdict `fixed` with the commit, `answered` with the grounds, or `deferred
<home>` — and the range of fix commits, and derives the rest:

  the verdict cells    `**fixed** `<sha>`` with the grounds prefixed
                       `fixed at <sha>`, `answered` with the grounds, or
                       `deferred <home>` with the home; a commit has to
                       resolve and lie inside the range
  Contract changes     every top-level Python unit whose parameters, return
                       arities or set of returnable constant literals differ
                       between the two ends of the range, each with the
                       enclosing unit of every `name(` in the tree,
                       `unit → site, site`; callers under `tests/` read
                       `pytest`, or `pytest only` when they are the whole
                       reach — and so does a unit pytest itself reaches, which
                       has no call site in the tree by design
  New units            every top-level def, class and module-level constant
                       present at the end of the range and absent at its
                       start, `unit (depth 1)`; for a file the AST cannot read
                       the `+` diff lines are read for `def`, `class`,
                       `function`, `fn`, `func`, and a comment after the table
                       says which files were read that way
  Pass                 ticked when no verdict is open once the table applies
  Fixes checked by     `no fixes to check` when no verdict closed on a fix
                       word once the table applies — every row `deferred
                       <home>` or `answered`, the capped run's last record,
                       which has no next round to set it; otherwise left as
                       it stands for `new` of the next round to set. The
                       derivation is `new`'s, in one spelling
  Broad gate           `--broad-gate`, when given

A unit at depth 2 is refused before any of that is written: a `fixed`
finding whose `Location` sits inside a unit an earlier record's `New units`
names, in a file the range adds a unit to. The refusal names the unit, the
finding, the record, and the exit the rule gives. The check runs the way it
runs for `new`.

**Every cell writer takes a structured value and refuses one it cannot
write.** A `|` or a newline in any cell, or a comma in `New units` or
`Contract changes`, is refused before anything touches the disk: the last
branch's 🔴 1 of round 2 was a semicolon inside a code span splitting a cell,
and its 🔴 1 of round 4 was prose inside a `New units` entry. Neither can be
written here, and there is no `--grounds` or `--note` flag for a session to
hide prose in. The generator carries none of the template's explanatory
comments into the record either: those are documentation, and a record is
read by checkers.

Nothing here commits. The generator writes files and runs the check; the
commit is the orchestrator's, made from a record it has read.

The constants this file matches against are `chain_check.py`'s wherever that
file has one — the headings, the field labels, the verdict vocabulary, the
`not yet written` reason — loaded from it rather than spelled again, so the
writer and the checker cannot drift about a string. What is defined here is
only what the checker never reads: the headings and headers of the two tables
it does not parse, and the honest starting values of the cells it does.

Exit codes: 0 and 1 are `chain_check`'s own, after the record is written ·
2 the input was unusable, or the interpreter is below the floor — either way
nothing was read and nothing was written · a sibling script that will not
load is 1, before anything is read.

Those are all three exits, enumerated from this module's own AST rather than
remembered: `SystemExit(2)` at the guard, `SystemExit(<sentence>)` in `load`,
and `sys.exit(main())` at the bottom. `SystemExit` carrying a string exits 1
— only an int argument sets the code — so `load` is 1 either way, and this
paragraph said 2 until #226's review round asked what actually happens.
"""

import argparse
import ast
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# The interpreter, before this file does anything a reader could mistake for
# progress.
#
# Issue #226, reported from another repository. On a machine whose `python3`
# is 3.9 this died at the `zip(..., strict=True)` below with an interpreter
# traceback -- and it died there, which is to say after argument parsing, path
# resolution and the report read had all succeeded. So the failure read as a
# bug in the report, and the message named neither the version needed nor the
# flag. macOS still ships 3.9 as `/usr/bin/python3`, so that is the default
# interpreter on a common platform, and a repository pinning a newer one does
# not help: this script is invoked directly rather than through it.
#
# The four `strict=True` sites stay. `CONTRIBUTING.md` §Running the checks
# names 3.12 as the supported floor, so dropping them would buy nothing but a
# few more lines before the next 3.10+ construct, at the price of the
# invariant the comment above the first one states.
#
# **The floor is one number, and this is a sixth carrier of it** -- after
# `ruff.toml`, both READMEs, the CI matrix and CONTRIBUTING's sentence, all of
# which say 3.12 and are held together by tests. It deliberately does not
# import `FLOOR` from `.github/scripts/run_tests.py`: a read that can fail
# gives the guard a second way to die on the one machine that has no other
# way of being told what is wrong, and a fallback-safe read still has to name
# a floor in its `except` branch, so the second spelling survives the import
# anyway. `tests/test_a_script_says_which_interpreter_it_needs.py` pins this
# number to the runner's and to ruff.toml's instead.
#
# **This block is the spelling to copy**, for the other scripts of the class
# `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md` enumerates.
# Two things about its shape are load-bearing. It sits after the imports and
# not after `import sys`, because ruff's E402 is selected and every shipped
# script was measured to compile under 3.9, so no import above it can fail
# first. And it uses no syntax newer than the oldest interpreter it means to
# catch -- no walrus, no f-string -- since a guard that cannot parse is the
# traceback it exists to replace.
FLOOR = (3, 12)
FLOOR_TEXT = ".".join(str(part) for part in FLOOR)
BELOW_FLOOR = (
    "round-record: needs python {floor} or newer, and this is python {found} "
    "at {executable}.\n"
    "Nothing was read and nothing was written.\n"
    "`python3` is not always the newest interpreter installed -- macOS ships "
    "python 3.9 under that name -- so name one explicitly, `python{floor} "
    "<this script> ...`, or see CONTRIBUTING.md section 'Running the checks'."
)


def below_floor(version=None, executable=None):
    """The sentence for an interpreter under the floor, or None above it.

    Both numbers are in the sentence. A floor with no found version tells the
    reader what is wanted and not whether they have it -- and the reader
    whose `python3` is secretly 3.9 is exactly the one who does not know what
    they are running. The interpreter's path is there for the same reason: on
    macOS the surprise is not the version, it is which file `python3` was.
    """
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

HERE = os.path.dirname(os.path.abspath(__file__))
CHAIN = os.path.join(HERE, "chain_check.py")


# RIDER: this function's refusal is the shape #226 fixed one file over, and
# it is still the old shape here. A missing `chain_check.py` reaches
# `exec_module` and raises `FileNotFoundError` -- a bare traceback, exit 1 --
# because `spec_from_file_location` hands back a spec for any path ending in
# `.py`, present or not, so the `SystemExit` sentence below is unreachable
# from this call site. Whoever next opens this function: make the missing
# case a sentence naming `path` and what to do, the way `below_floor` does,
# and give it the same exit code the docstring promises. Measured, not read:
# the real script with `chain_check.py` deleted exits 1 with a traceback.
# Verified 2026-09-08 against load@643ea575.
def load(path, name):
    """Import a sibling script by path, or die — either way exit 1.

    This said `exit 2`, and 2 is the one code this module documents as meaning
    nothing was read and nothing was written. Both ways out are 1: a
    `SystemExit` carrying a string prints it and exits 1, since only an int
    argument sets the code.

    Which way out a missing checker takes is not the one the sentence below
    suggests, and it was measured rather than read. `spec_from_file_location`
    returns a spec for a path ending in `.py` whether or not the file is
    there, so `CHAIN` missing reaches `exec_module` and raises
    `FileNotFoundError` — an uncaught traceback, exit 1. The `SystemExit`
    branch fires only for a path with no loader at all, a directory or an
    unrecognised suffix, which a literal `chain_check.py` cannot be. So a
    missing sibling still arrives as the bare traceback #226 is about, one
    file over. The rider above says what that would take."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"round-record: cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


chain = load(CHAIN, "specseal_chain_check")

# The one heading and the one column the checker reads, by the checker's name.
VERDICTS = chain.VERDICTS
VERDICT_HEADER = ("#", "Finding", "Location", chain.VERDICT_COLUMN, "Grounds")
# The two tables the checker never parses, so their names live here. Their
# headers are what `agents/warden.md` §Report tells the reviewer to write,
# and `tests/test_the_record_is_generated.py` reads them from here and looks
# for them there — one constant, two carriers.
PROBES = "## Executed probes"
PROBE_HEADER = ("What was run", "Result")
DEFERRED = "## Deferred"
DEFERRED_HEADER = ("Finding", "Where it went", "Who answers it")
REPORT_TABLES = (
    (VERDICTS, VERDICT_HEADER),
    (PROBES, PROBE_HEADER),
    (DEFERRED, DEFERRED_HEADER),
)
# The section that is fenced blocks and no table. `skills/code-review/SKILL.md`
# §Findings format requires a paste-ready fix for every 🔴/🟡 and spends four
# paragraphs on what makes one paste-ready; until this heading existed, `new`
# copied the tables and dropped every one of those blocks (#187), so the file
# the fix pass is told to open instead of the report carried none of the
# artefact the report's four paragraphs are about.
PASTE_READY = "## Paste-ready fixes"
# What the section says when the report carried no fence under that heading.
# It states what the generator OBSERVED, not that none was needed: a round
# that opened a 🔴 and wrote no block is a gap, and this sentence beside that
# row in the verdict table is what makes the gap visible in the record itself.
NO_PASTE_READY = "no paste-ready fix in the report"
# Every heading the generator looks up in the report. A section added later is
# read, and guarded, by being added here, and no second list goes stale.
READ_HEADINGS = (*(h for h, _ in REPORT_TABLES), PASTE_READY)
# The subset `swallowed` may refuse a report over, and `PASTE_READY` is the
# first member of `READ_HEADINGS` that is NOT in it. The guard's premise is
# that a heading hidden by a fence and absent outside it was SWALLOWED, and
# that holds only where the report must carry the section. `agents/warden.md`
# §Report tells a round that opened nothing needing a fix to leave this
# heading out, so absence is a legitimate state here and the refusal would
# report a loss that did not happen (round 1's 🟡 3).
#
# It is also the shape that stops this tool during its own review rounds: a
# reviewer of the record generator pastes record-shaped blocks, headings and
# all, and the round that quotes the empty section's own sentence is exactly
# the round that wrote no fixes. `seal/ledger.md` F3 names that scenario as
# what the guard must never do.
#
# What it gives up, stated rather than left to be found: a report that DOES
# carry paste-ready fixes and whose heading a closed fence swallows now writes
# a record saying the report carried none. Nothing can tell that apart from a
# round that wrote none — the two texts are identical outside the fence — and
# the record shows the gap where a reader meets it, beside the open rows in
# the verdict table above. A refusal here would stop an unattended run over
# the legitimate case to catch the unlikely one, which is the trade
# `CLAUDE.md`'s first goal decides.
REQUIRED_HEADINGS = tuple(h for h, _ in REPORT_TABLES)
# Where the reviewer leaves the report, beside the record it becomes. The
# record is `round-N.md` and the report is `round-N-report.md`, so both names
# come out of `--item` and `--round` and neither can be spelled differently
# from the other (#228).
#
# `--report` used to be required, and the reviewer's report was not a file:
# the warden returns it as its final message and the orchestrator is told not
# to open the agent transcript, so the orchestrator RETYPED it into a file to
# pass here. Four rounds of one work item, four retypings, and 0.9.0's own
# #190 · #207 run retyped rounds 2 and 3. A retyped verdict row carries
# retyped coordinates, re-review inheritance carries the paraphrase into the
# next round, and `Fixes checked by` then points at a round whose report is
# not the report the reviewer wrote.
#
# The fixer side already had this shape -- `rounds/round-N-fixes.md`, which
# `close` takes as `--fixes` -- so this is the missing half of a convention
# rather than a new one. `agents/warden.md` §Report is the other half: it
# tells the reviewer to write the file and return the path.
REPORT_NAME = "round-{n}-report.md"
# The two sections the generator fills from somewhere other than the report.
ASKED = "## What this round was asked"
INHERITED = "## Inherited coordinates"
INHERITED_HEADER = ("From", "Coordinate", "Why it is still worth opening")
# Field labels the checker has no constant for, because it never reads them.
BROAD_GATE = "Broad gate"
# The honest values while nothing has happened yet. `not yet opened` is what
# `chain_check.declared_pull_head` documents as the pre-pull-request value;
# `nothing to drain` is `templates/sdd-round.md`'s required answer for a
# Deferred section with no rows.
PR_NOT_YET = "not yet opened"
GATE_NOT_YET = "not yet"
NOTHING_TO_DRAIN = "nothing to drain"
# Built by codepoint for the reason `chain_check.SEPARATORS` gives: an em dash
# in a string literal is what ruff's RUF001 reads as a mistyped hyphen.
DASH = chr(0x2014)
# The landing values `ORDER_FROM` requires of a record committed before its
# fixes exist, spelled from the checker's own words.
PENDING_CHECKER = f"{chain.NOBODY} {DASH} {chain.NOT_YET}"
PENDING_SURFACE = f"{chain.NONE_WORD} {DASH} {chain.NOT_YET}"
# The rows a comma splits. `depth_problems` reads a comma inside a `New
# units` entry as a second unit, and `fix_surface`'s reach list is
# comma-separated, so a comma in either is structure and not punctuation.
COMMA_SPLIT_ROWS = (chain.NEW_UNITS, chain.CONTRACT)
# The two terminal lines of a reviewer's report, by the field they land in.
TERMINAL_LINES = (chain.NEEDS, chain.FLOOR)
# Together with `REPORT_TABLES`' headings, everything the generator looks up
# in the report -- which is what `swallowed` guards, so a section added later
# is guarded by being added there and no second list goes stale.
SWALLOWED = (
    "a fenced block swallows `{name}` -- the report has no `{name}` outside "
    "a fence, so the record would lose it and say nothing. Close the fence "
    "above that line, or move the block below the section"
)
NEVER_CLOSED = (
    "a fenced block in the report is never closed -- copied as it stands it "
    "would swallow every heading after it, and every section below it would "
    "be gone from the record with nothing said"
)
# The same sentence for the OTHER text. `swallowed` reads the report with its
# comments stripped and `fenced_after` reads it verbatim, so a fence a comment
# hides is absent from the first check and present in the copy.
NEVER_CLOSED_VERBATIM = (
    "a fenced block under `{heading}` is never closed in the report as it "
    "stands, and the block is copied into the record verbatim -- the record "
    "would carry an open fence and every section below it would be gone with "
    "nothing said. An opener inside an HTML comment counts: the report-wide "
    "check reads the report with its comments stripped and this copy reads it "
    "as written. Close the fence, or take the opener out of the comment"
)
# The heading is only half of what a section is to the generator; the rows are
# the other half, and a fence can take those alone.
SWALLOWED_TABLE = (
    "a fenced block hides every table row of `{name}` -- the heading still "
    "stands, so nothing notices it went, and the generator copies only rows "
    "outside a fence. The section would arrive in the record empty and say "
    "nothing. Close the fence above the table, or move the block below the "
    "section"
)
# The round paragraph is spliced above every section a reader looks up, and
# the record is written before anything reads it.
ASKED_NEVER_CLOSED = (
    "a fenced block in the round paragraph is never closed -- the paragraph "
    f"is copied into the record above `{VERDICTS}`, so an open fence would "
    "blank the record from there down and the record is written before any "
    "reader gets to say so. Close the fence in the --asked file"
)
# The same never-closed question, asked of the OTHER hider. `readable` blanks
# with two passes and `strip_comments` runs first, so an HTML comment opened
# and never closed blanks every line below it exactly as an open fence does --
# and no fence question can see it, because by the time the fence pass runs
# those lines are already gone. Both are asked BEFORE their fence twin for
# that reason: an open comment blanks the closing fence of every block below
# it, so the fence question would answer first and name a fence that is closed
# in the text as written.
COMMENT_NEVER_CLOSED = (
    "an HTML comment in the report is never closed -- it blanks every line "
    "below it before anything is looked up, so the sections and the terminal "
    "lines under it are gone and the refusal you would otherwise get names a "
    "line you did in fact write. Close the comment with `-->`"
)
ASKED_COMMENT_NEVER_CLOSED = (
    "an HTML comment in the round paragraph is never closed -- the paragraph "
    f"is copied into the record above `{VERDICTS}` as it stands, so the "
    "record would carry the opener and every section below it would be blank "
    "to every reader, and the record is written before any reader gets to say "
    "so. Close the comment in the --asked file with `-->`"
)
# The third answer, and it is the one the two questions above used to read as
# the second. A comment that opens inside a fenced block and closes OUTSIDE it
# blanks that block's closing fence, because `strip_comments` runs first -- so
# the fence question, asked of the comment-stripped text, finds a block with no
# closer while every fence in the text as written closes. The refusal then
# named a fence that is closed and sent the reviewer to look for something
# that is not there, which is the defect §14 exists for and the one round 2 of
# #169's chain already paid for once.
#
# Asking the fence question of the RAW text as well is what tells the two
# apart: open in both texts is a fence nobody closed, open in the stripped
# text alone is a comment crossing a fence marker.
COMMENT_CROSSES_A_FENCE = (
    "an HTML comment in the report opens inside a fenced block and closes "
    "outside it. Every fence in the report as written closes; what reads as "
    "an unclosed fence is the comment blanking a closing one, because "
    "`readable` strips comments before it blanks fences. So the refusal you "
    "would otherwise get names a fence you did close. Close the comment "
    "inside the block, or move the whole comment out of it"
)
ASKED_COMMENT_CROSSES_A_FENCE = (
    "an HTML comment in the round paragraph opens inside a fenced block and "
    "closes outside it. Every fence in the paragraph as written closes; what "
    "reads as an unclosed fence is the comment blanking a closing one, "
    "because `readable` strips comments before it blanks fences. Close the "
    "comment inside the block in the --asked file, or move the whole comment "
    "out of it"
)
# The same three questions, asked of the RECORD rather than of an input, and
# this is the whole of what #182 is. Every copy the generator makes out of
# `raw` lands in one artefact, so the record's own text is the one place where
# every copy path is answerable at once -- the three the (copy x hider) grid
# named, the fourth it did not, and a fifth somebody adds later. A hider a
# SLICE of `raw` took half of is exactly a record no reader can read, which is
# why *balance across the slice* asked at the destination needs no knowledge
# of which slice took it.
#
# Measured at 8114937 before the guard: a report whose Grounds cell opens a
# comment and closes it on the line below is accepted, `new` exits 0, the
# record is written, and `## Executed probes`, `## Inherited coordinates` and
# `## Deferred` each resolve to 0 occurrences through the shared reader while
# standing in the bytes. Nothing in the run says a word.
RECORD_COMMENT_NEVER_CLOSED = (
    "the record this would write has an HTML comment that is never closed, so "
    "every line below it is blank to every reader of it -- `chain_check` at "
    "the pull request, the next round's inherited coordinates, "
    "`evidence-check` -- and the record is written before any of them gets to "
    "say so. A copied cell and a copied block are SLICES of the report, so a "
    "comment the report itself balances arrives here as half of one. Close it "
    "inside the cell it opens in, or move it out of the row"
)
RECORD_NEVER_CLOSED = (
    "the record this would write has a fenced block that is never closed, so "
    "every heading below it is gone to every reader of it and the record is "
    "written before any of them gets to say so. A copied block is a SLICE of "
    "the report, so a fence the report itself balances arrives here as half "
    "of one. Close the block inside the section it is copied from"
)
RECORD_COMMENT_CROSSES_A_FENCE = (
    "the record this would write has an HTML comment that opens inside a "
    "fenced block and closes outside it. Every fence in the record as written "
    "closes; what reads as an unclosed fence is the comment blanking a "
    "closing one, so every reader below that line reads the record as one "
    "open block. Close the comment inside the block, or move the whole "
    "comment out of it"
)
# A line no fence regex can match and no comment marker, appended to ask a
# reader pass whether its hider is still open at the end of the file: blanked
# means open, kept means closed. Both passes ask it, of their own hider.
SENTINEL = "x"
# Which hider is open, as `open_hider` answers it and as each text's message
# set is keyed. Three answers and not two: `STRADDLE` is a comment crossing a
# fence marker, which the fence question alone reports as `FENCE`.
COMMENT, FENCE, STRADDLE = "comment", "fence", "straddle"
# One message set per text the question is asked of. The set is what makes the
# question shareable: the ORDER of the two passes is a property of `readable`
# and not of any one text, so a text contributes its three sentences and
# nothing else. The five sentences that predate #182 keep their bytes, so
# every case and every ledger anchor naming one still stands.
REPORT_HIDERS = {
    COMMENT: COMMENT_NEVER_CLOSED,
    FENCE: NEVER_CLOSED,
    STRADDLE: COMMENT_CROSSES_A_FENCE,
}
ASKED_HIDERS = {
    COMMENT: ASKED_COMMENT_NEVER_CLOSED,
    FENCE: ASKED_NEVER_CLOSED,
    STRADDLE: ASKED_COMMENT_CROSSES_A_FENCE,
}
RECORD_HIDERS = {
    COMMENT: RECORD_COMMENT_NEVER_CLOSED,
    FENCE: RECORD_NEVER_CLOSED,
    STRADDLE: RECORD_COMMENT_CROSSES_A_FENCE,
}


class Refused(Exception):
    """An input this cannot turn into a record. Nothing is written."""


def open_hider(reader, text):
    """Which hider is still open at the end of `text`, or None.

    `readable` blanks with two passes and `strip_comments` runs first, so an
    HTML comment opened and never closed blanks every line below it exactly
    as an open fence does -- one pass earlier, where no fence question can
    see it. The comment is asked FIRST for that reason: an open comment
    blanks the closing fence of every block below it, so the other order
    answers first and names a fence that is closed in the text as written.

    **The order lives here and nowhere else.** It is a property of the pass
    order in `readable`, not of any one text, and it used to be written out
    once per text -- twice by the time round 2 of #169's chain was done, in
    `swallowed` and in `build`, each with its own pair of raises. A third
    text would have carried a third copy of it.

    `STRADDLE` is the third answer, and it is what those two pairs read as
    `FENCE`: a comment opening inside a fenced block and closing outside it
    blanks that block's own closing fence, so the fence question finds a
    block with no closer while every fence in the text as written closes.
    Asking the fence question of the raw text as well is what tells them
    apart, and one boolean is the whole difference between a message a
    reviewer can act on and a message that sends them looking for a fence
    they did close.
    """
    lines = text.splitlines()
    if not reader.strip_comments([*lines, SENTINEL])[-1]:
        return COMMENT
    stripped = reader.strip_comments(lines)
    if reader.blank_fences([*stripped, SENTINEL])[-1]:
        return None
    return FENCE if not reader.blank_fences([*lines, SENTINEL])[-1] else STRADDLE


def opens_at(reader, lines, blank):
    """The 1-based line the still-open hider opens on, or 0 for none.

    Asked of the reader's own pass over each prefix rather than by a second
    implementation of where a marker sits: the shortest prefix `blank`
    leaves open is the one whose last line opened it. A second reading of
    `<!--` and of a fence regex here is the check/copy asymmetry this module
    has now been bitten by three times, and a prefix walk cannot drift from
    the pass it calls.

    The record is a few hundred lines, so the quadratic walk is a few
    hundred thousand line visits on a path that already runs git.
    """
    for i in range(1, len(lines) + 1):
        if not blank([*lines[:i], SENTINEL])[-1]:
            return i
    return 0


def hiders_close(reader, text, messages):
    """Refuse `text` when a hider in it is still open, in `messages`' words.

    The coordinate is appended rather than written into each sentence, so
    the sentences stay one per (text, hider) and none of them can be the one
    that forgot to say where. A record is composed from three sources and
    `somewhere in the record` is not something a person can act on.
    """
    kind = open_hider(reader, text)
    if kind is None:
        return
    lines = text.splitlines()
    if kind == FENCE:
        line = opens_at(reader, reader.strip_comments(lines), reader.blank_fences)
    else:
        line = opens_at(reader, lines, reader.strip_comments)
    seen = lines[line - 1].strip()[:120] if 0 < line <= len(lines) else ""
    raise Refused(f"{messages[kind]} (line {line}: {seen!r})")


def write_record(reader, path, text):
    """Write a record, once the shared reader can read all of it.

    **This is the one function in this module that opens a file for writing,
    and that is the completeness argument #182 asks for.** The rule the
    (copy x hider) grid was reaching for is not about copies at all: every
    copy the generator makes out of `raw` lands in one artefact, so asking
    the question of the ARTEFACT answers for every copy path at once -- the
    three the grid named, the fourth it did not (`inherited_rows`), and a
    fifth somebody adds next year. The grid's row axis was a list of the
    sources somebody could see, which is the enumeration-by-reading this
    release is named for; the destination is one, and it is greppable:
    `grep -n 'open(' round_record.py` finds every writer, and
    `tests/test_the_record_is_generated.py` walks the AST for them.

    It closes the cell the `# RIDER:` in `swallowed` left open, too. A
    comment balanced in the report and half in the record is exactly a record
    the reader cannot read, and *balance across the slice* asked here needs
    no knowledge of which slice took the half. Measured at `8114937`: a
    report whose Grounds cell opens a comment and closes it on the line below
    is accepted, `new` exits 0, and the record's `## Executed probes`,
    `## Inherited coordinates` and `## Deferred` each resolve to 0
    occurrences while standing in the bytes.

    It also reaches what no question asked of an INPUT can: a flag. `cell`
    refuses a `|` and a newline because either breaks the row, and `<!--`
    breaks every reader below it -- so `--ran-by 'x <!-- y'` used to write a
    record whose whole tail was blank.

    **What this gives up, stated rather than left to be found.** A record
    that legitimately ends inside a hider is refused, and the only way out is
    to fix the text it was copied from. The bound is that a fenced block is
    copied WHOLE, so a balanced comment inside one stays balanced here; only
    a slice can take half, and a slice taking half is the defect. And it is
    measured rather than argued: all 163 records committed under
    `seal/specs/*/rounds/round-*.md` were read through both passes at
    `8114937` and none has an open hider.
    """
    hiders_close(reader, text, RECORD_HIDERS)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def escape(value):
    """A cell's text with its pipes escaped the way `split_row` unescapes."""
    return value.replace("|", "\\|")


def row(cells):
    """One markdown table row from already-checked cells."""
    return "| " + " | ".join(cells) + " |"


def separator(width):
    return "|" + "---|" * width


def split_cells(line, spans=False, limit=None, comments=False):
    """Cells of one markdown row, or None when the line is not one.

    Three knobs over what `reader.split_row` does, and with all three off
    this is that function: leading `|` dropped, one closing `|` dropped, a
    break at every `|` no single backslash precedes, each cell stripped and
    its `\\|` unescaped. Nothing here may drift from it — the record is read
    back through it, so a cell this composes and that one reads differently
    is a cell the pull-request check reads differently from the record.

    `spans` reads a `|` inside a backtick code span as text. That is the
    reviewer's own markup saying the character is not a column break — a
    shell pipeline in a probes row, an augmented assignment in a Grounds
    cell — and it is the one reading that recovers the column it belongs
    to. Runs close the way CommonMark closes a code span: a run of N closes
    a run of N. An unbalanced run swallows every break after it, which is
    why the reading is taken only when it lands on the width its caller
    expects.

    `comments` reads a `|` between `<!--` and `-->` as text, for the same
    reason `spans` does inside a backtick run, and for one more that is not
    about markup at all: `table_body` measured this row's width on
    `strip_comments(report)`, where that character is NOT a break, and
    `copied_row` rebuilds the row from `raw`, where it is. Two texts
    disagreeing about one character is the asymmetry `NEVER_CLOSED_VERBATIM`
    already documents for fences; here it cost a column, at exactly header
    width, so nothing downstream complained and the Location stood in the
    Verdict cell `chain_check` reads (round 1's 🔴 1).

    `limit` caps how many breaks are taken; every `|` after that stays in
    the last cell as the text it stood in, spacing and all. Rejoining
    already-split cells cannot do that — `split_row` strips each one, so
    `a |= b` comes back as `a | = b`.
    """
    s = line.strip()
    if not s.startswith("|"):
        return None
    body = s[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    out, buf, i, marker, hidden = [], [], 0, None, False
    while i < len(body):
        ch = body[i]
        if comments and not hidden and body.startswith("<!--", i):
            hidden = True
            buf.append(body[i : i + 4])
            i += 4
            continue
        if hidden:
            if body.startswith("-->", i):
                hidden = False
                buf.append(body[i : i + 3])
                i += 3
                continue
            buf.append(ch)
            i += 1
            continue
        if spans and ch == "`":
            j = i
            while j < len(body) and body[j] == "`":
                j += 1
            if marker is None:
                marker = j - i
            elif j - i == marker:
                marker = None
            buf.append(body[i:j])
            i = j
            continue
        broken = len(out)
        if (
            ch == "|"
            and marker is None
            and (i == 0 or body[i - 1] != "\\")
            and (limit is None or broken < limit)
        ):
            out.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    out.append("".join(buf))
    return [c.strip().replace("\\|", "|") for c in out]


def raw_cells(line, spans=False, limit=None):
    """`split_cells` as a line of the RAW report has to be read.

    One place rather than a flag at each call site, and the difference is
    whether the rule can be observed. `table_body` counts a row's columns on
    `strip_comments(report)` and `copied_row` is handed `raw`, so a `|`
    inside an HTML comment is never a break here — not as a preference but
    because the two texts have to agree about every character. Measured
    while closing round 1's 🔴 1: with the flag written at each of
    `row_cells`' four readings, removing any ONE of them left every case
    green, because a later reading recovers what an earlier one splits
    wrongly. Removing it here turns them red.

    `split_cells` keeps the knob and keeps defaulting it off, because with
    all three knobs off that function has to be `reader.split_row` and
    `test_the_plain_reading_is_the_readers_own` holds it there.
    """
    return split_cells(line, spans=spans, limit=limit, comments=True)


def row_cells(reader, line, width):
    """`line`'s cells, `width` of them wherever the line can give that many.

    Three readings, in the order that keeps the reviewer's own placement
    most often. #189 measured the loss this repairs: a `|` inside a cell
    makes the row carry more cells than the header declares, every renderer
    drops the surplus, and the text from that character on is invisible in
    the rendered record while surviving in the raw file.

    1. The plain reading, wherever it already fits. This is what every
       downstream check does, so the ordinary row is read by the function
       that will read it back rather than by a second spelling of it.
    2. Otherwise the code-span reading, capped at `width` breaks, wherever
       that lands on the width. A `|` inside a backtick code span is the
       reviewer's own markup saying the character is not a break: all eight
       over-wide rows in this repository's committed records have their
       pipe inside one, and one of the eight has it in a column that is not
       the last. The cap has to be ON here — a row carrying both a span
       pipe and a bare one past it is over-wide under either reading alone,
       and the uncapped span reading then missed it and let the plain cap
       re-split the code span, landing the Location in the Verdict cell
       (round 1's 🟡 2).
    3. Otherwise the plain cap, so a `|` past the last column stays in the
       last cell as text. An unbalanced backtick run lands here, because it
       swallows every break and comes in UNDER the width at reading 2.

    Every reading goes through `raw_cells`, so a `|` inside an HTML comment
    is never a break. That is not a preference: `table_body` counted this
    row's columns on the comment-stripped text and this function is handed
    `raw` (round 1's 🔴 1).

    **An uncapped span reading used to stand before reading 1** — the shape
    round 1's fix arrived in. It is gone because it is subsumed: a reading
    that lands exactly on `width` is unchanged by a cap of `width - 1`, and
    it is reached only where the plain reading is over the width, which is
    reading 2. Measured before removing it, over all 4128 body rows of this
    repository's committed records and 432 generated rows covering every
    combination of a bare pipe, a span pipe, a comment pipe and an
    unbalanced backtick run in three columns: zero disagreements. What it
    cost while it stood was a branch no case could observe — dropping its
    `spans=True` left the whole module green, because reading 2 returns the
    same cells.

    The cap is a guess and it is the only one available: nothing in a
    flattened row says which column a bare `|` came from. It is never worse
    than what the record did before — the leading cells land at the same
    indices either way — and it makes the text visible instead of dropped.
    The stated limit is that a bare `|` in a column that is not the last
    lands the rest of the row in the last column.

    Returns None for a line that is not a row, and fewer than `width` cells
    for a row that has fewer. Neither is refused here: `table_body` and
    `fix_table` own what a short row means, and a refusal would stop an
    unattended run over something no person can decide.
    """
    if reader.split_row(line) is None:
        return None
    plain = raw_cells(line)
    if len(plain) <= width:
        return plain
    spanned = raw_cells(line, spans=True, limit=max(width - 1, 0))
    if len(spanned) == width:
        return spanned
    return raw_cells(line, limit=max(width - 1, 0))


def copied_row(reader, line, width):
    """One report row re-serialised into the record, its pipes escaped."""
    cells = row_cells(reader, line, width)
    if cells is None:
        return line.strip()
    return row([escape(c) for c in cells])


def cell(label, value):
    """`| label | value |`, or `Refused`.

    A `|` would split the row and a newline would end it, so neither can be
    written whatever the row. A comma is refused in the two rows the checker
    splits on it, and nowhere else — `Needs a fix` is prose and keeps its
    commas.
    """
    if not isinstance(value, str) or not value.strip():
        raise Refused(f"`{label}` needs a value and got {value!r}")
    for what, char in (("a pipe", "|"), ("a newline", "\n"), ("a newline", "\r")):
        if char in value:
            raise Refused(
                f"`{label}` cannot carry {what}: {value!r}. A row is one line "
                "and its cells are what stands between the pipes"
            )
    if label in COMMA_SPLIT_ROWS and "," in value:
        raise Refused(
            f"`{label}` cannot carry a comma: {value!r}. The checker splits "
            "that row on it, so a comma is a second entry and never punctuation"
        )
    return row((label, value))


def git(root, *args):
    r = subprocess.run(
        ["git", "-C", root, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    return r.stdout if r.returncode == 0 else None


def pull_request_cell(root, given, which=shutil.which, run=subprocess.run):
    """The `PR` cell: the flag, else `gh`'s answer, else `not yet opened`.

    `gh pr view --json number,url` on the current branch. The number goes
    first so `chain_check.PR_RE` finds it before the digits in the URL.
    `which` and `run` are parameters so a case can stand in for a `gh` that
    answers without a remote to ask.
    """
    if given is not None:
        return given
    if which("gh") is None:
        return PR_NOT_YET
    try:
        r = run(
            ["gh", "pr", "view", "--json", "number,url"],
            cwd=root,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return PR_NOT_YET
    if r.returncode != 0:
        return PR_NOT_YET
    try:
        answer = json.loads(r.stdout)
        number, url = int(answer["number"]), str(answer["url"])
    except (ValueError, KeyError, TypeError):
        return PR_NOT_YET
    return f"#{number} {DASH} {url}"


def pull_request_is_ready(root, which=shutil.which, run=subprocess.run):
    """True only when `gh` says the branch's pull request is not a draft.

    `chain_check` judges an unchecked `Pass` as a failure on a READY pull
    request and as the honest state of a running review on a draft. A record
    being generated is a review still running, so the check is told `draft`
    unless the platform says otherwise — and the platform is asked, not the
    session.
    """
    if which("gh") is None:
        return False
    try:
        r = run(
            ["gh", "pr", "view", "--json", "isDraft"],
            cwd=root,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        return r.returncode == 0 and json.loads(r.stdout).get("isDraft") is False
    except (OSError, subprocess.SubprocessError, ValueError, AttributeError):
        return False


def default_baseline(root):
    """The upstream of the current branch, else `origin/main`."""
    upstream = git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    return upstream.strip() if upstream and upstream.strip() else "origin/main"


def read_text(path, what):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as exc:
        raise Refused(f"cannot read the {what} at {path}: {exc}") from exc


def report_path(rounds, n, given):
    """The report to read: `--report` where it was passed, else the convention.

    The default is derived from `--item` and `--round` -- the same pair
    `round-N.md` itself is built from, one function away -- so the reviewer
    and the generator cannot spell the path differently from each other.

    The flag stays, and it wins. Two callers still need it: a round whose
    report was written before `agents/warden.md` told the reviewer where to
    leave one, and a round that ran more than one reviewer, where the
    orchestrator hands each its own path rather than letting the second
    overwrite the first.

    The absence of the default names the path AND the convention. `read_text`
    would name the path alone, and a path with no sentence beside it reads as
    a mistyped argument -- which is the one thing it cannot be here, because
    nobody typed it.
    """
    if given is not None:
        return given
    path = os.path.join(rounds, REPORT_NAME.format(n=n))
    if not os.path.isfile(path):
        # `isfile` is False for two different states and the message named
        # one. A reviewer that made the directory instead of the file read
        # `no report at <path>` about a path with something at it, which is
        # the one reading the guard has to rule out -- it exists to be
        # readable by somebody who typed no path (#228, round 1 ⬜ 6).
        lead = (
            f"{path} is a directory, and the report is a file"
            if os.path.isdir(path)
            else f"no report at {path}"
        )
        raise Refused(
            f"{lead}, and no --report. The reviewer writes its "
            f"report there and returns the path (`agents/warden.md` §Report), "
            "and this reads it from where the reviewer left it rather than "
            "from a copy somebody retyped (#228). `--report <path>` names one "
            "written somewhere else"
        )
    return path


def section_body(reader, lines, heading):
    """(start, [(index, line)]) for the one section under `heading`, or None.

    `lines` are already `readable`, so a heading inside a comment or a fence
    is not a section, and indices are the raw file's.
    """
    starts = reader.sections(lines, heading)
    if not starts:
        return None
    if len(starts) > 1:
        raise Refused(f"the report has {len(starts)} `{heading}` sections")
    body = []
    for i in range(starts[0] + 1, len(lines)):
        if lines[i].startswith("#"):
            break
        body.append((i, lines[i]))
    return starts[0], body


def table_body(reader, lines, heading, header, required):
    """[(index, cells)] for the body rows under `heading`, or None.

    The header has to be the record's own, cell for cell: a table whose
    columns differ is one the checker's column lookup reads differently, and
    copying it would put the difference in the record. Returns None when the
    section is absent and not required. Indices are the raw file's, so a
    caller can copy the raw line or replace it.
    """
    found = section_body(reader, lines, heading)
    if found is None:
        if required:
            raise Refused(
                f"the report has no `{heading}` section — the generator copies "
                "that table into the record, and a report without it says "
                "nothing about what the round found"
            )
        return None
    _start, body = found
    # `row_cells` rather than `split_row`: a `|` the reviewer wrote inside a
    # cell used to make the row carry more cells than the header declares,
    # and every reader downstream of this one — `fix_table`'s third cell,
    # `verdict_rows`' verdict column — then read the wrong index (#189).
    rows = [(i, row_cells(reader, ln, len(header))) for i, ln in body if ln.strip()]
    rows = [(i, cells) for i, cells in rows if cells is not None]
    if not rows:
        if required:
            raise Refused(f"`{heading}` holds no table")
        return None
    seen = tuple(reader.visible(c) for c in rows[0][1])
    if seen != header:
        raise Refused(
            f"`{heading}` has the header {row(seen)!r}; the record's is "
            f"{row(header)!r}, and the generator copies only a table in the "
            "record's own columns"
        )
    return [
        (i, cells)
        for i, cells in rows[1:]
        if not reader.is_separator([reader.visible(c) for c in cells])
    ]


def table_of(reader, raw, lines, heading, header, required):
    """The rows under `heading`, header and separator first, pipes escaped.

    Each row is re-serialised from `raw` rather than copied from it, so a
    `|` the reviewer wrote inside a cell reaches the record as text instead
    of splitting the row (#189). `raw` and not `lines`, because `lines` has
    the HTML comments stripped and a comment a reviewer wrote inside a cell
    is theirs to keep.
    """
    body = table_body(reader, lines, heading, header, required)
    if body is None:
        return None
    return [row(header), separator(len(header))] + [
        copied_row(reader, raw[i], len(header)) for i, _ in body
    ]


def swallowed(reader, report, lines):
    """Refuse a fence that has taken something the generator reads with it.

    Two halves of one rule, both read over the whole report: **a hider must
    close, and its span must not cross a line the generator reads the report
    by.** The first half used to live in `fenced_after`, where it saw one
    section; both belong here, because a fence can open in one section and
    close in another and the section it destroys is not the one it opened in.

    **A hider, not a fence.** `readable` blanks with two passes and
    `strip_comments` runs first, so an unterminated HTML comment blanks every
    line below it exactly as an open fence does -- and it does it one pass
    earlier, where no fence question can see it. The never-closed half of the
    rule is `hiders_close(reader, report, REPORT_HIDERS)` below, which is
    where the pair of raises that used to stand here went: the ORDER of the
    two questions is a property of `readable` and not of this text, and it
    had already been written out twice by the time #182 needed a third text
    asked. What stays here is the positional half -- the span -- which is
    about `REPORT_TABLES` and `TERMINAL_LINES` and so is about the report
    alone.

    `readable` blanks a fence, so a heading inside one is not a heading to
    any walk downstream: `section_body` runs straight past it, the fence
    reads as closed, and the section is simply gone from the record. #169
    reported one shape of that -- a fence under the probes table closing
    below `## Deferred`, exit 0, the Deferred table inside the fence and the
    record's own Deferred section reading `nothing to drain`.

    The rule is about the SPAN and not about the name it crossed, which is
    what makes it cover the shapes #169 did not name -- a fence opened under
    the verdict table that closes below `## Executed probes` takes the whole
    probes section with it, and `fenced_after` is never even called for that
    section, so no guard living inside it could see the shape.

    What may not be lost is `REQUIRED_HEADINGS`, the table rows that stand
    under `REPORT_TABLES`' members, and `TERMINAL_LINES`. A list of section
    constants typed out here would go stale the day a section is added;
    these are the constants the generator reads BY, so a section it cannot
    read is a section it does not have.

    `REQUIRED_HEADINGS` and not `READ_HEADINGS`, and the difference is a
    rule rather than an omission: the premise here is that a heading hidden
    by a fence and absent outside it was SWALLOWED, and that inference holds
    only for a section the report must carry. `PASTE_READY` is optional, so
    its absence is a legitimate state and the refusal would report a loss
    that did not happen — round 1's 🟡 3, whose grounds are F3's own Notes.
    That constant carries the trade this gives up.

    The rows are the third loop and they are the half round 1 of this work
    item's own chain found missing (🟡 2): a heading is only half of what a
    section is to the generator, and a fence can take the rows and leave the
    heading standing -- `## Deferred` then reads `nothing to drain` in the
    record beside a row the reviewer wrote. The condition is F3's, one level
    down: the section has rows only inside a fence. A fence quoting rows
    beside a table that still stands is left alone, for the same reason a
    fence quoting a heading is.

    What this does NOT read is the report as written. `fenced_after` does,
    and the difference is exactly the HTML comments: `strip_comments` runs
    here first, so a fence opener a comment hides is not a fence to anything
    below. That is why the never-closed raise in `fenced_after` is a second
    check and not a duplicate of the first (🔴 1 of the same round).

    A fence quoting one of those names is left alone while the real one
    still stands outside it. That matters more than it looks: a reviewer of
    this generator pastes record-shaped blocks, headings and all, and a rule
    that refused the mention rather than the loss would stop the tool on its
    own review rounds.

    The lines a fence hid are read off the reader's own two passes rather
    than by tracking fences a third time here: `lines` is
    `blank_fences(strip_comments(...))`, so what a fence hid is exactly what
    survives comment stripping and is blank afterwards. A `#` at column 0 is
    a Markdown heading and a Python comment both, and only the fence tells
    them apart -- which is why nothing here reads the `#` character.
    """
    # The comment STRADDLE used to be the one shape of this rule left open,
    # and the rider that carried it here is gone because #182 closed it: a
    # comment whole in the report and half in the record, because a copied row
    # and a copied block are SLICES of `raw`, is exactly a record no reader can
    # read -- and `write_record` asks that of the record. *Balance across the
    # slice*, which is the limit argument this function could not make, needs
    # no knowledge of which slice took the half once it is asked at the
    # destination.
    hiders_close(reader, report, REPORT_HIDERS)
    stripped = reader.strip_comments(report.splitlines())
    # `strict=True` states the invariant the pair rests on: both of the
    # reader's passes keep indices intact, so the two reads are the same file
    # line for line. A length that differed would truncate the hidden set,
    # which is this guard reporting clean because it read less. The index is
    # kept because the table half of the rule below is positional: a row is
    # lost from the section it stood in, and from no other.
    pairs = enumerate(zip(stripped, lines, strict=True))
    hidden = [(i, s.strip()) for i, (s, ln) in pairs if s.strip() and not ln]
    text = [t for _i, t in hidden]
    for heading in REQUIRED_HEADINGS:
        if heading in text and not reader.sections(lines, heading):
            raise Refused(SWALLOWED.format(name=heading))
    for label in TERMINAL_LINES:
        pattern = re.compile(r"^\s*" + re.escape(label) + r"\s*:")
        if any(pattern.match(h) for h in text) and not any(
            pattern.match(ln) for ln in lines
        ):
            raise Refused(SWALLOWED.format(name=f"{label}:"))
    for heading, _header in REPORT_TABLES:
        starts = reader.sections(lines, heading)
        if len(starts) != 1:
            continue  # absent is the loop above; twice is `section_body`'s
        start = starts[0]
        end = next(
            (i for i in range(start + 1, len(lines)) if lines[i].startswith("#")),
            len(lines),
        )
        if any(reader.split_row(ln) for ln in lines[start + 1 : end]):
            continue
        if any(start < i < end and reader.split_row(t) for i, t in hidden):
            raise Refused(SWALLOWED_TABLE.format(name=heading))


def fenced_after(reader, raw, lines, heading):
    """The raw lines of every fenced block under `heading`, in order.

    `templates/sdd-round.md` says a probes row whose subject was a proposed
    replacement owes the replacement itself, in a fenced block under the
    table, and `new` copied the table alone — so round 1 of #161's own chain
    read *Fix below (A)* in seven Grounds cells and carried none of them,
    and the fix pass rebuilt every one from a description. A fence is copied
    whole and nothing else of the section is, so no prose enters the record
    (`questions.md` A5 of that work item). `lines` are `readable`, which
    blanks fences, so the fence is read from `raw` at the section's indices.
    """
    found = section_body(reader, lines, heading)
    if found is None:
        return []
    out, marker = [], None
    for i, _ in found[1]:
        line = raw[i].rstrip()
        opener = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker is None:
            if opener:
                marker = opener.group(1)
                out.append(line)
            continue
        out.append(line)
        if (
            opener
            and opener.group(1)[0] == marker[0]
            and len(opener.group(1)) >= len(marker)
        ):
            marker = None
    # This is NOT the refusal `swallowed` already made, and it is not dead.
    # The two walks read two different texts: `swallowed` reads
    # `strip_comments(report)` and this one reads `raw`, so a fence opener
    # inside an HTML comment is absent from the first and an opener to this.
    # Phase 1 removed this raise as unreachable on the assumption that the
    # two texts agree about where a fence is; round 1 of this work item's own
    # chain executed the disagreement -- an opener inside a comment under the
    # probes table, the record written at exit 0, and its `## Inherited
    # coordinates` and `## Deferred` unreadable to every downstream reader.
    #
    # `swallowed` is still the report-wide half and still necessary: a fence
    # opened under the verdict table takes `## Executed probes` with it, this
    # function is then never called for a section the report no longer has,
    # and the record gets the empty template. Necessary is not sufficient,
    # which is what the removal read as.
    if marker is not None:
        raise Refused(NEVER_CLOSED_VERBATIM.format(heading=heading))
    return out


def terminal_value(reader, lines, label):
    """What stands after the colon in the report's `<label>: …` line."""
    pattern = re.compile(r"^\s*" + re.escape(label) + r"\s*:\s*(.*?)\s*$")
    found = [m.group(1) for ln in lines for m in [pattern.match(ln)] if m]
    if len(found) != 1:
        raise Refused(
            f"the report has {len(found)} `{label}:` lines and the record "
            "needs exactly one — the row is copied from what stands after "
            "the colon"
        )
    value = reader.visible(found[0])
    word, _ = chain.yes_or_no(value)
    if word is None:
        raise Refused(
            f"`{label}: {value}` is not `{chain.FLOOR_NO}` or "
            f"`{chain.FLOOR_YES} {DASH} <what>`, which is the vocabulary the "
            "checker reads the row in"
        )
    return value


def verdict_words(reader, rows):
    """The normalized verdict of each body row of a copied verdict table."""
    col = VERDICT_HEADER.index(chain.VERDICT_COLUMN)
    words = []
    for line in rows[2:]:
        cells = reader.split_row(line)
        seen = [reader.visible(c) for c in cells]
        if len(seen) <= col:
            raise Refused(f"a verdict row has {len(seen)} cells: {line!r}")
        words.append(chain.verdict_of(seen, col))
    return words


def landing_values(words):
    """(`Fixes checked by`, surface) a record lands on, from its verdict words.

    A verdict still open, or closed on a fix word, means fixes exist or will,
    and nobody has opened them yet: `nobody — the fixes are not yet written`
    and the pending surface. Every verdict closed without one means nothing
    here commissioned a fix, so *not yet written* would be false the moment
    it is written: `no fixes to check` and a bare `none`. The two are the
    landing states `templates/sdd-round.md` and `chain_check.fix_surface`
    describe.

    `new` derives both cells from the report's verdicts. `close` re-derives
    the first after the fix table applies, for the record whose every verdict
    closed on `deferred <home>` or `answered` — a capped run's last record has
    no next round to set the cell, and the check refuses `Pass` beside
    `nobody` there (`questions.md` A6 of the work item that added this). One
    spelling, called from both, so the two subcommands cannot disagree about
    which words commission a fix.
    """
    open_rows = [w for w in words if w not in chain.CLOSED_WORDS]
    fixed_rows = [w for w in words if w in chain.FIX_WORDS]
    if open_rows or fixed_rows:
        return PENDING_CHECKER, PENDING_SURFACE
    return chain.NO_FIXES, chain.NONE_WORD


def earlier_records(routing, rounds, n):
    """[(K, path)] for every `round-K.md` on disk with K < n, lowest first."""
    try:
        names = os.listdir(rounds)
    except OSError:
        return []
    found = []
    for name in names:
        k = routing.round_number(name)
        path = os.path.join(rounds, name)
        if k is not None and k < n and os.path.isfile(path):
            found.append((k, path))
    return sorted(found)


def inherited_rows(reader, earlier):
    """One row per `Location` cell of every earlier record, first seen wins.

    `Why` names the round, the finding and its verdict word, so the next
    round knows what it is reopening; coordinates carry, conclusions do not.
    """
    # RIDER: this is the fourth copy out of `raw`, and #182's COPY half is
    # closed at the destination -- `write_record` reads the record back, so a
    # hider a cell copied here cannot reach a written record. What is still
    # open is the READ-LESS half of the same class, and it has three members,
    # all in this module: a hider in an earlier record can blank a verdict row
    # so this function does not inherit its coordinate; it can blank a `New
    # units` row so `units_named_earlier` does not see an entry and
    # `depth_two`'s refusal is not made; and it can blank a `## Fixes` row so
    # `close` reports the smith as never having written one.
    #
    # None of the three writes a hider into a record and all three are LOUD
    # today, which is why they are here rather than in the guard. Measured
    # 2026-09-08 at 8114937: a `round-1.md` corrected in place with an opener
    # in a `Location` cell is refused at `a verdict row has 3 cells`, because
    # the opener swallows the row's remaining pipes. The message is cell
    # arithmetic rather than a comment, which is §14's defect one step short
    # of a loss.
    #
    # What closing it takes, and why a fix pass may not: a whole-text question
    # on an input read for named sections refuses a file this repository
    # already has -- the `` `<!--` `` inside a code span at
    # `seal/specs/1788826000-a-stamp-names-content-not-a-commit/rounds/round-1-fixes.md`
    # blanks that file's tail and hides nothing `fix_table` reads. Narrowed to
    # the section it is `swallowed` parameterised over its three constants,
    # which is a design call. If you open this function, take the whole class
    # or none of it. Verified 2026-09-08 against inherited_rows@8cef4835
    location = VERDICT_HEADER.index("Location")
    number = VERDICT_HEADER.index("#")
    seen, out = set(), []
    for k, path in earlier:
        text = read_text(path, f"earlier record round-{k}.md")
        lines = reader.readable(text)
        rows = table_of(
            reader, text.splitlines(), lines, VERDICTS, VERDICT_HEADER, True
        )
        for word, line in zip(verdict_words(reader, rows), rows[2:], strict=True):
            cells = [reader.visible(c) for c in reader.split_row(line)]
            coordinate = cells[location]
            if not coordinate or coordinate in seen:
                continue
            seen.add(coordinate)
            out.append(
                row(
                    (
                        f"round-{k}",
                        escape(coordinate),
                        escape(f"round {k}'s {cells[number]} {DASH} {word}"),
                    )
                )
            )
    return out


def reach_back(reader, path, n):
    """Set round N-1's `Fixes checked by` to `round-N`, touching nothing else.

    Refused when the cell is absent or outside the checker's vocabulary — a
    cell nobody can read is not one to overwrite silently — and when it
    already names a different later round, because that is a true fact about
    which round read those fixes and this would be replacing it with a guess.
    A cell reading `no fixes to check` is kept and said so: that round
    commissioned no fixes, and `round-N` would claim this one read some
    (round 1 of #161's own chain, 🟡 6). Returns the line to print.
    """
    text = read_text(path, f"earlier record round-{n - 1}.md")
    raw = text.splitlines()
    lines = reader.readable(text)
    hits = [
        i
        for i, ln in enumerate(lines)
        for cells in [reader.split_row(ln)]
        if cells and len(cells) >= 2 and cells[0].strip() == chain.CHECKED_BY
    ]
    if len(hits) != 1:
        raise Refused(
            f"{path} has {len(hits)} `| {chain.CHECKED_BY} | … |` rows, and the "
            "reach-back needs exactly one to set"
        )
    i = hits[0]
    value = reader.visible(reader.split_row(lines[i])[1]).strip("`").rstrip(".")
    mine = f"round-{n}"
    if chain.CHECKER_RE.match(value.lower()):
        named = value.lower().removesuffix(".md")
        if named != mine:
            raise Refused(
                f"{path}'s `{chain.CHECKED_BY}` already names `{value}`, and "
                f"this is {mine}. A record that says which round read its "
                "fixes is not overwritten with a different one"
            )
    elif value.lower() == chain.NO_FIXES:
        return (
            f"round-record: left `{chain.CHECKED_BY}` of {os.path.basename(path)} "
            f"at `{chain.NO_FIXES}` {DASH} that round commissioned no fixes, so "
            f"{mine} has none of its to read"
        )
    elif chain.nobody_reason(value.lower()) is None:
        raise Refused(
            f"{path}'s `{chain.CHECKED_BY}` reads `{value}`, which is outside "
            f"the vocabulary — `round-N`, `{chain.NO_FIXES}`, or "
            f"`{chain.NOBODY} {DASH} <why>`. Correct it before the reach-back "
            "overwrites it"
        )
    raw[i] = cell(chain.CHECKED_BY, mine)
    ending = "\n" if text.endswith("\n") else ""
    write_record(reader, path, "\n".join(raw) + ending)
    return (
        f"round-record: set `{chain.CHECKED_BY}` of {os.path.basename(path)} to {mine}"
    )


# --- the bound the next round is under, said as the record is written -------

ENDS_THE_RUN = "this record ends the run"
ONE_REOPENING = "one reopening remains"


def floor_and_fixes(reader, earlier):
    """(the floor record, the later ones that closed on a fix, how many
    records the FIRING count walk has spent, whether a count walk is still
    running, the record that walk started from).

    The last three are one answer in three cells and never disagree: with no
    walk running the count is 0 and the record is None, because a walk that
    has stopped bounds nothing and a count reported from one would be a
    number about a record the caller is not told.

    **`chain_check.stopping_floor` runs TWO walks over the records after the
    floor, and this used to carry one of them.** The reopening walk counts
    fix-closing records wherever they sit and refuses a second; the count walk
    counts every later record up to and including the first that reopened
    (`Needs a fix: yes`) or closed on a fix, and refuses a second counted
    record. A run whose floor was met and whose next rounds are simply QUIET
    is bounded by the second walk alone — so reading only the first printed
    `one reopening remains` at round 2 and the gate then refused round 3, the
    invitation into a round the gate does not allow (round 1, 🔴 2). That is
    #207's own defect, reproduced by the fix for it.

    **And the gate runs each walk from EVERY record whose floor row reads
    `no`, not from the earliest alone.** `stopping_floor` is called on every
    record — its own docstring says so, for the same reason `checked_by` is —
    so a second floor record starts its walks over the records after IT. The
    two walks answer that differently, and the answer is a property of the
    walk rather than a case anybody noticed:

      | Walk          | Stops? | Start point                              |
      | the reopening | never  | a suffix filter, so a later start's hits |
      |               |        | are all in an earlier start's. The       |
      |               |        | earliest DOMINATES: ≤ 1 there is ≤ 1     |
      |               |        | everywhere, and ≥ 2 there already fires  |
      | the count     | yes    | stopping breaks that. An earlier walk    |
      |               |        | that stopped says nothing about a later  |
      |               |        | floor record's own walk, which starts    |
      |               |        | fresh — so every floor record is walked  |

    That is the enumeration, taken by construction over `stopping_floor`'s
    body — the two loops under `word == FLOOR_NO`, which is the whole of what
    it does with `later` — and then a monotonicity question asked of each,
    rather than by reading for more instances of the shape. Reading the
    earliest floor record's count walk alone printed `one reopening remains`
    at round 4 of this work item while the gate returned an error at
    `round-2.md` (round 2, 🟡 1): round 1's 🔴 2 one floor record over, and
    the third instance of one class on this branch.

    The floor record is the EARLIEST earlier record whose `Loses a record or
    crashes` reads `no`, and taking the LATEST instead is the failure
    `chain_check.stopping_floor` records in its own docstring: every record
    the count stops at is itself a record that met the floor, so a count keyed
    to the latest restarts there and is unbounded by construction. That is
    about which record the RETURNED floor is, and the count walk above is
    about which records are walked — a walk from every floor record is not a
    count keyed to the latest, because each walk is bounded by its own start.

    **Whether the walk is still RUNNING is the fourth value, because the count
    the record being written inherits depends on it.** A record that reopened
    the run without writing fixes stops the walk at the gate, so this record
    is not counted at all and the gate allows it — counting it anyway would
    print `ends the run` over a round the gate is about to permit, which is
    the same false sentence one direction over.

    Read from disk rather than from `HEAD`. `chain_check.read_record` asks git
    because it is enforcing at a pull request, where the working tree is
    exactly what CI cannot see; this is a line printed to whoever just ran the
    command, and the records in front of them are the ones on disk. A record
    whose row is outside the vocabulary is simply not the floor record —
    `stopping_floor` already reports that at the gate, and a second reader
    inventing a sentence about it here would be the thing #207 is about.

    **An unreadable record answers nothing at all**, and that is the whole
    return rather than a record dropped from `fixes`. Skipping one leaves a
    run that HAS closed on a fix reading as a run that still has its reopening
    — the permissive direction, and against what this docstring says it does
    (round 1, 🟡 12). `checked_by` already names the unreadable record.
    """
    seen = []
    for _k, path in earlier:
        try:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
        except OSError:
            return None, [], 0, False, None
        lines = reader.readable(text)
        rows = chain.table_rows(reader, lines)
        floor = chain.field(rows, chain.FLOOR)
        met = floor is not None and (
            chain.yes_or_no(reader.visible(floor).strip())[0] == chain.FLOOR_NO
        )
        needs = chain.field(rows, chain.NEEDS)
        reopened = needs is not None and (
            chain.yes_or_no(reader.visible(needs).strip())[0] == chain.FLOOR_YES
        )
        seen.append((path, met, reopened, chain.closed_with_a_fix(reader, lines, path)))

    floor_i = next((i for i, row in enumerate(seen) if row[1]), None)
    if floor_i is None:
        return None, [], 0, False, None
    # The reopening walk, from the EARLIEST floor record — the only start it
    # needs, by the monotonicity argument above.
    fixes = [p for p, _m, _r, wrote in seen[floor_i + 1 :] if wrote]

    # The count walk, from EVERY floor record. Among the walks still running,
    # the earliest has the largest count — a later walk's records are all in
    # the earlier one, which would have to have stopped for the later one to
    # start fresh — so the maximum is the walk the gate refuses first, and
    # `counted_at` is the record it started from.
    counted, counted_at = 0, None
    for i, (path, met, _r, _w) in enumerate(seen):
        if not met:
            continue
        spent, stopped = 0, False
        for _p, _m, reopened, wrote in seen[i + 1 :]:
            spent += 1
            if reopened or wrote:
                stopped = True
                break
        if not stopped and spent > counted:
            counted, counted_at = spent, path
    return seen[floor_i][0], fixes, counted, counted_at is not None, counted_at


def bound_line(reader, routing, rounds, n):
    """What bound the next round is under, or None where there is none.

    **`docs/review-chain-spec.md` bounds a run one step earlier than the cap**:
    after a record whose floor row reads `no`, at most one later record may
    close on a fix, and the record that reads its fixes ends the run whatever
    it finds. `chain_check.py` enforces that at the broad gate — after every
    round of the run has already been spawned — and nothing says it at the
    moment a session decides whether to spawn again. Measured (#207): one work
    item ran rounds 3, 4 and 5 past the bound, wrote *"round N of a cap of
    five"* into every spawn prompt, and reverted 37.9 minutes of agent time.

    The cap is a number a prompt can carry and is wrong; the bound is a
    condition that has to be recomputed from the previous record's floor row
    every time a round ends. `new` already has that record in hand for the
    reach-back, so the answer costs a read it is already paying for.

    **A first round, and a run whose floor has not been met, print nothing.**
    A sentence invented for a state that has none is worse than silence: the
    cap still governs there, and the cap is not this line's subject.

    **A work item the gate grandfathers prints nothing either, and the two
    walks are grandfathered against DIFFERENT constants.** `stopping_floor`
    excuses the count walk's refusal below `FLOOR_FROM` and the reopening
    walk's below `REOPEN_FROM`, and for an item between the two the gate
    refuses one and merely notices the other. One guard for both would have
    silenced a bound that is really enforced at `1788500000-an-item`, and no
    guard at all declares a run capped where the gate only prints (round 1,
    🟡 8). Silence is the answer rather than a hedged sentence: this line
    exists to bound the decision to spawn again, and for a record the gate
    will not refuse there is no bound to state.
    """
    floor_at, fixes, counted, running, counted_at = floor_and_fixes(
        reader, earlier_records(routing, rounds, n)
    )
    if floor_at is None:
        return None
    # Every record here is one work item's, so `item_began` answers the same
    # whichever floor record is named — `floor_at` and `counted_at` alike.
    began = chain.item_began(floor_at.replace(os.sep, "/"))
    reopen_excused = began is None or began < chain.REOPEN_FROM
    count_excused = began is None or began < chain.FLOOR_FROM
    met = os.path.basename(floor_at)
    if fixes:
        if reopen_excused:
            return None
        reopened = os.path.basename(fixes[0])
        return (
            f"round-record: {ENDS_THE_RUN} — {met} met the floor and "
            f"{reopened} closed on a fix. At most one later record may close "
            "on a fix, and the record that reads its fixes ends the run "
            f"whatever it finds. {chain.CAPPED_EXIT}"
        )
    if counted and running:
        # Every record after some floor record was quiet, so that walk is
        # still running and this record is the one it counts next — the
        # gate's SECOND counted record, which it refuses.
        if count_excused:
            return None
        quiet = "record" if counted == 1 else "records"
        # The record the FIRING walk started from, which is not always the
        # earliest floor record `met` names (round 2, 🟡 1). Naming `met`
        # here sent the reader to a walk that had already stopped, and the
        # count beside it then belonged to a record the sentence did not
        # mention — the one thing in this line a reader can check.
        started = os.path.basename(counted_at)
        return (
            f"round-record: {ENDS_THE_RUN} — {started} met the floor and the "
            f"{counted} {quiet} after it neither reopened the run nor closed "
            "on a fix, so the gate's count of round records after the floor "
            f"reaches {counted + 1} here. {chain.CAPPED_EXIT}"
        )
    if reopen_excused:
        return None
    return (
        f"round-record: {ONE_REOPENING} — {met} met the floor and no later "
        "record has closed on a fix. If this round's own verdicts close on "
        "one, the record after it ends the run whatever it finds"
    )


def build(reader, routing, args, root, item, rounds):
    """The record's text, and the reach-back to make once it is written."""
    if not reader.resolves(root, args.target):
        raise Refused(
            f"--target {args.target} does not resolve in {root} — a record "
            "naming a commit nobody can open names nothing"
        )
    report = read_text(report_path(rounds, args.round, args.report), "report")
    raw = report.splitlines()
    lines = reader.readable(report)
    # Before anything is looked up: a section a fence has taken is absent by
    # every later reading, and each of those readings has its own, wrong
    # answer for absence -- an empty template, or a count of terminal lines.
    swallowed(reader, report, lines)
    asked = read_text(args.asked, "round paragraph").strip()
    if not asked:
        raise Refused(
            f"the round paragraph at {args.asked} is empty — `{ASKED}` is the "
            "durable home of what this round was told to attack (#119)"
        )
    # The report is not the only text spliced into the record. The round
    # paragraph is a copy of a spawn prompt, spawn prompts carry fenced blocks
    # and HTML comments routinely, and this one lands ABOVE every section a
    # reader looks up -- so it is asked the same questions the report is, in
    # the text a reader sees it in. All of them, because the check reads
    # `strip_comments(asked)` and the splice below copies `asked` verbatim:
    # asking only the fence question leaves the comment hider free to ride the
    # gap between the two texts, which is 🔴 1's asymmetry inside the guard
    # written to close 🟡 3 (round 2's 🔴 7, executed at `aed3ca0`: the record
    # written and four of its five sections unreadable).
    #
    # The pair of raises that used to stand here is now one call. `open_hider`
    # holds the order and the reason for it, because the order is a property
    # of `readable`'s passes rather than of this text -- and written out per
    # text it was already written twice, with a third text due.
    hiders_close(reader, asked, ASKED_HIDERS)

    verdicts = table_of(reader, raw, lines, VERDICTS, VERDICT_HEADER, True)
    probes = table_of(reader, raw, lines, PROBES, PROBE_HEADER, False) or [
        row(PROBE_HEADER),
        separator(len(PROBE_HEADER)),
    ]
    fenced = fenced_after(reader, raw, lines, PROBES)
    if fenced:
        probes = [*probes, "", *fenced]
    # #187: the paste-ready fix the findings format requires used to reach no
    # file at all. It is extracted by the mechanism the probes table has used
    # since #161 -- a fence is copied whole and nothing else of the section
    # is, so no prose enters a file `chain_check.py` reads.
    #
    # The empty arm is a scenario rather than an edge case: a verifying round
    # that opens nothing writes no fix, and the record still has to be
    # written. The sentence says what was OBSERVED -- that the report carried
    # no fence under the heading -- because a round that opened a 🔴 and wrote
    # no block is a gap, and only the reader can tell the two apart. Beside an
    # open row in the verdict table above, this line IS the gap made visible,
    # which is what `plan.md` says mitigates a reviewer omitting the heading.
    sketches = fenced_after(reader, raw, lines, PASTE_READY) or [NO_PASTE_READY]
    deferred = table_of(reader, raw, lines, DEFERRED, DEFERRED_HEADER, False)
    if deferred is None:
        deferred = [row(DEFERRED_HEADER), separator(len(DEFERRED_HEADER)), ""]
        deferred.append(NOTHING_TO_DRAIN)
    needs = terminal_value(reader, lines, chain.NEEDS)
    floor = terminal_value(reader, lines, chain.FLOOR)

    words = verdict_words(reader, verdicts)
    open_rows = [w for w in words if w not in chain.CLOSED_WORDS]
    checker, surface = landing_values(words)

    earlier = earlier_records(routing, rounds, args.round)
    if args.round > 1 and not any(k == args.round - 1 for k, _ in earlier):
        raise Refused(
            f"round {args.round} needs round-{args.round - 1}.md beside it in "
            f"{rounds}, and it is not there — the reach-back has nothing to set"
        )

    fields = [
        row(("Field", "Value")),
        separator(2),
        cell(chain.TARGET, args.target),
        cell(chain.RAN_BY, args.ran_by),
        cell(chain.PR_FIELD, pull_request_cell(root, args.pr)),
        cell(BROAD_GATE, args.broad_gate if args.broad_gate else GATE_NOT_YET),
        cell(chain.CHECKED_BY, checker),
        cell(chain.CONTRACT, surface),
        cell(chain.NEW_UNITS, surface),
        cell(chain.NEEDS, needs),
        cell(chain.FLOOR, floor),
    ]
    box = "x" if not open_rows else " "
    inherited = [row(INHERITED_HEADER), separator(len(INHERITED_HEADER))]
    inherited += inherited_rows(reader, earlier)

    parts = [
        f"# {os.path.basename(item)} {DASH} review round {args.round}",
        "",
        *fields,
        "",
        f"- [{box}] Pass",
        "",
        ASKED,
        "",
        asked,
        "",
        VERDICTS,
        "",
        *verdicts,
        "",
        PASTE_READY,
        "",
        *sketches,
        "",
        PROBES,
        "",
        *probes,
        "",
        INHERITED,
        "",
        *inherited,
        "",
        DEFERRED,
        "",
        *deferred,
    ]
    previous = next((p for k, p in earlier if k == args.round - 1), None)
    return "\n".join(parts) + "\n", previous


def run_check(root, baseline):
    """`chain_check --worktree` on the repository, printed, its code returned.

    The check reads the pull request's state from the event payload GitHub
    writes, and outside a workflow it has none and judges as READY — where an
    unchecked `Pass` fails. A record being generated is a review still
    running, so the check is told `draft` unless `gh` says the pull request
    is already ready, in which case it is judged as CI will judge it. On a
    machine without `gh` the check is told `draft` for every local run, and
    CI re-judges from the real payload at the pull request.
    """
    env_was = os.environ.get("GITHUB_EVENT_PATH")
    payload = None
    if not pull_request_is_ready(root):
        fd, payload = tempfile.mkstemp(suffix=".json", prefix="round-record-")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"pull_request": {"draft": True}}, f)
        os.environ["GITHUB_EVENT_PATH"] = payload
    try:
        return chain.main(["--worktree", "--baseline", baseline, "--root", root])
    finally:
        if payload is not None:
            if env_was is None:
                os.environ.pop("GITHUB_EVENT_PATH", None)
            else:
                os.environ["GITHUB_EVENT_PATH"] = env_was
            try:
                os.unlink(payload)
            except OSError:
                pass


def worktrees_of(item):
    """Every work tree of the clone `item` belongs to, main tree first, or [].

    Asked of git rather than derived from the path, because the path is where
    the derivation goes wrong. A local-mode work item sits under the common
    git directory (`skills/agent-contract/SKILL.md` §16), and
    `rev-parse --show-toplevel` REFUSES that -- measured 2026-09-08 against a
    scratch repository: exit 128, `fatal: this operation must be run in a work
    tree`. That is not a path git failed to recognise; it is git declining a
    work-tree question asked from inside the git directory, so no amount of
    normalising the argument gets an answer out of it.

    `git worktree list --porcelain` does answer from there (measured in the
    same run, from a main tree and from a linked worktree), and its first
    entry is the main worktree.

    Nothing here spells `.git`, and nothing takes `dirname` of the common
    directory. A repository created with `--separate-git-dir` keeps its git
    directory anywhere at all, and the tree above it is the repository root
    only by accident -- the kind of accident that holds on the author's
    machine and not on the one that reports the bug.
    """
    try:
        out = git(item, "worktree", "list", "--porcelain")
    except (OSError, subprocess.SubprocessError):
        # `git` missing from PATH or killed by the timeout. This sits on the
        # path to a REFUSAL, so a traceback here would replace a sentence
        # naming the item with a stack nobody can act on.
        return []
    if not out:
        return []
    return [
        line[len("worktree ") :].strip()
        for line in out.splitlines()
        if line.startswith("worktree ")
    ]


def repo_of(item, reader):
    """The repository root a work item belongs to, or None.

    Shared mode is asked first and is unchanged: the item is in the work tree,
    `reader.repo_root` answers in one `rev-parse`, and nothing new runs.

    Local mode is the case that used to be refused, and the answer is not the
    item's -- it is the CALLER's. One local root is shared by every worktree
    of the clone (`hooks/optin.py#home_at`), so the item cannot say which tree
    a run is about, and a round record is a record of the tree whose HEAD and
    branch it names. A caller sitting outside the clone entirely gets the main
    worktree, which is the only tree the item itself points at.
    """
    root = reader.repo_root(item)
    if root:
        return root
    trees = worktrees_of(item)
    if not trees:
        return None
    here = reader.repo_root(os.getcwd())
    if here and (
        os.path.realpath(here) in {os.path.realpath(t) for t in trees}
        or shares_the_clone(here, item)
    ):
        return here
    # `git worktree list` prints the GIT DIRECTORY rather than a work tree for
    # a bare clone and for one made with `--separate-git-dir` -- measured
    # 2026-09-08, both, and the second carries no `bare` line to tell it by.
    # `pr-notes.md` claimed this case was the one asking git avoids relying
    # on; executed, it is the one asking git gets wrong. A root every later
    # `git -C <root>` refuses is not a root, so this refuses instead of naming
    # one, and the caller's own sentence says both places were tried.
    first = trees[0]
    return first if reader.repo_root(first) else None


def common_dir_of(where):
    """`where`'s common git directory, absolute and resolved, or ""."""
    try:
        out = git(where, "rev-parse", "--git-common-dir")
    except (OSError, subprocess.SubprocessError):
        return ""
    out = (out or "").strip()
    return os.path.realpath(os.path.join(where, out)) if out else ""


def shares_the_clone(root, item):
    """True when `root` is a work tree of the clone `item` sits in.

    Compared by common git directory, never by the paths `git worktree list`
    prints. With `--separate-git-dir` those paths ARE the git directory, so
    the caller's own tree is not in the list it belongs to -- and the set
    comparison above then discards a caller who is standing in exactly the
    tree the record is about.
    """
    ours, theirs = common_dir_of(root), common_dir_of(item)
    return bool(ours) and ours == theirs


def where(args):
    """(reader, routing, root, item, rounds) for `--item`, or `Refused`."""
    reader = load(chain.READER, "specseal_unverified_reader")
    routing = load(chain.ROUTING, "specseal_routing")
    item = os.path.abspath(args.item)
    if not os.path.isdir(item):
        raise Refused(f"--item {args.item} is not a directory")
    root = args.root or repo_of(item, reader)
    if root is None:
        # Split from the test above, and both halves say which one failed.
        # One sentence covered them jointly -- `is not a directory inside a
        # git repository` -- and it was TRUE of a local-mode item, which is
        # how a correctly placed work item read as a mistyped path for three
        # releases.
        raise Refused(
            f"--item {args.item} is not inside a git repository. Both places "
            "a root lives were tried: the work tree, and the common git "
            "directory a local-mode root sits under. `--root` names the "
            "repository directly."
        )
    root = os.path.abspath(root)
    if args.round < 1:
        raise Refused(f"--round {args.round} — rounds are numbered from 1")
    rounds = os.path.join(item, routing.ROUNDS_DIR)
    return reader, routing, root, item, rounds


def new(args):
    reader, routing, root, item, rounds = where(args)
    target = os.path.join(rounds, f"round-{args.round}.md")
    if os.path.lexists(target):
        raise Refused(
            f"{target} already exists. A record is written once and corrected "
            "in place — this does not overwrite one"
        )

    text, previous = build(reader, routing, args, root, item, rounds)
    reached = None
    if previous is not None:
        reached = reach_back(reader, previous, args.round)
    os.makedirs(rounds, exist_ok=True)
    write_record(reader, target, text)
    print(f"round-record: wrote {os.path.relpath(target, root)}")
    if reached is not None:
        print(reached)
    # After the record is written and before the check runs — the moment the
    # orchestrator decides whether to spawn again, which is the moment the
    # enforcement at the broad gate does not reach (#207).
    bound = bound_line(reader, routing, rounds, args.round)
    if bound is not None:
        print(bound)
    return run_check(root, args.baseline or default_baseline(root))


# --- close: the fix table applied, the fix surface measured ------------------

# The smith's fix-pass handover: one row per OPEN finding of the round it
# answers, under this heading, in these columns. `agents/smith.md` and
# `skills/implement/SKILL.md` §5 tell the smith to write it, and
# `tests/test_the_fixes_close_the_record.py` reads both from here — one
# constant, three carriers.
FIXES = "## Fixes"
FIXES_HEADER = ("#", "Verdict", "Commit or grounds")
# The three verdicts a fix pass may hand over, all the checker's own closing
# words. `deferred <home>` closes on the home after it and a bare `deferred`
# stays OPEN (`questions.md` A4) -- `close` writes the word with the home, so
# a `Pass` ticked over a table of deferrals is the capped run's legal end.
FIXED, ANSWERED, DEFERRED_WORD = "fixed", "answered", chain.DEFERRED
assert {FIXED, ANSWERED, DEFERRED_WORD} <= chain.CLOSED_WORDS, (
    "a fix verdict the checker cannot close"
)
FIXED_AT = "fixed at"
# The reach grammar `fix_surface` reads, `unit → site, site`, in the checker's
# first spelling of the arrow. The comma between sites is the writer's own and
# never an input's, which is what lets `cell` keep refusing one in this row.
ARROW = chain.ARROWS[0]
PYTEST_ONLY = "pytest only"
PYTEST = "pytest"
NO_SITE = "no call site found"
TESTS_DIR = "tests"
# The three shapes pytest reaches without a call site anywhere in the tree
# (#211): a collected test function, a fixture it injects by parameter name,
# and a `conftest` hook it dispatches through its plugin manager. None of the
# three is ever written as `name(`, so the reach walk came back empty and the
# row said `no call site found` about units that run on every CI leg.
#
# Measured over this repository at ba22b28 rather than reasoned about: 1892 of
# 1947 `test_*` defs under `tests/` read `no call site found`, and so did 8 of
# 42 fixtures. The ticket named the first set and left the second in its own
# `Not verified` section.
#
# The rule is these three and NOT everything under `tests/`. One helper there
# reads `no call site found` for an unrelated reason — it is passed by name as
# a value and never called — and a wider rule would say the runner covers a
# unit nothing covers, which is #211's own false sentence pointing the other
# way.
#
# Round 1 of this work item is that the code drew the boundary one step short
# of the prose twice, in opposite directions. `test_*` alone is the FUNCTION
# half of pytest's collection and `python_files` is the other half, so a
# `test_*` def in `tests/helpers.py` was reading `pytest only` about a unit
# nothing collects — the false sentence above, pointing the way the rule
# exists to refuse. And the `tests/` gate stood in front of every arm, so a
# `conftest.py` at the repository ROOT — the placement pytest documents
# first — read `no call site found` for its fixtures and its hooks, which is
# #211's own defect left standing at the commonest placement of all.
TEST_PREFIX = "test_"
TEST_SUFFIX = "_test.py"
HOOK_PREFIX = "pytest_"
CONFTEST = "conftest.py"
FIXTURE = "fixture"
# The columns of the verdict table, by the record's header.
NUMBER_COL = VERDICT_HEADER.index("#")
LOCATION_COL = VERDICT_HEADER.index("Location")
VERDICT_COL = VERDICT_HEADER.index(chain.VERDICT_COLUMN)
GROUNDS_COL = VERDICT_HEADER.index("Grounds")
# `questions.md` A1: a file the AST cannot read — not Python, or Python that
# does not parse at one end of the range — gives up its added definitions by
# a `+` diff line starting with one of five keywords and a name. The record
# says which files were read that way, in a comment the checkers blank.
HEURISTIC_RE = re.compile(r"^\+\s*(?:def|class|function|fn|func)\s+([A-Za-z_]\w*)")
HEURISTIC_NOTE = "read by the diff-line heuristic and not by the AST"
# Prose is neither: a sentence beginning `class of` or `def` is not a
# definition, and every record and document a range touches would otherwise
# be named as read for them (round 1 of #161's own chain, 🟡 5).
PROSE_SUFFIXES = (".md", ".markdown", ".txt", ".rst")
# The shapes a `Location` cell names a unit in: `path#unit` or `path::unit`,
# either with `@hash` after, `path:line`, a backticked identifier with or
# without `()`, and a cell that is a bare identifier. A path is resolved
# against the tree at the range's start — exact, `./`-stripped, or the one
# tracked path ending in `/<path>`, because records name
# `chain_check.py#fix_surface` for a file three directories down (round 1
# of #161's own chain, 🟡 4: the five forms after the first escaped).
LOCATION_UNIT_RE = re.compile(r"([\w./-]+\.py)(?:#|::)([A-Za-z_]\w*)")
LOCATION_LINE_RE = re.compile(r"([\w./-]+\.py):(\d+)")
# A second unit named by its fragment alone after a path — `path#a` and
# `#b` — the form round 1 of #161's own chain located its 🟡 4 in. The
# fragment names a unit in the last path the cell resolved, or no file.
FRAGMENT_RE = re.compile(r'(?<![\w./\-"#])#([A-Za-z_]\w*)')
IDENTIFIER_RE = re.compile(r"`([A-Za-z_]\w*)(?:\(\))?`")
BARE_IDENTIFIER_RE = re.compile(r"^([A-Za-z_]\w*)(?:\(\))?$")
# A finding id is a bare integer, optionally behind a severity marker. #227:
# the id used to be the FIRST digit run anywhere in the cell, so `R2-1` and
# `R2-2` both read as `2` and eight round-prefixed findings collapsed toward
# one key. The refusal that followed reported a duplicate the table did not
# visibly have. The marker is what the group skips and the digits are the id;
# `[^\w\s]` reaches every marker the records carry — 🔴 🟡 🟢 ⬜ ❓ ✅ — and
# reaches no letter, so `r3 🟡 2`, `1-1`, `1b` and `A2` are refused rather
# than silently keyed to whichever digits came first.
#
# The repetition takes ONE marker character, not a run of them, and that is
# round 1's finding 3 rather than a style choice. `[^\w\s]+` inside the `*`
# group let a run of punctuation be split into groups in exponentially many
# ways, and a cell ending in a non-digit made the engine try all of them
# before refusing: 0.18 s at 22 characters, 2.9 s at 26, 11.4 s at 28, and
# each further character doubles it — so `close` and `new` produced nothing
# and never returned. The language is unchanged, because every repetition of
# the group already consumes exactly one marker and the outer `*` supplies
# the run; measured identical over 16 id shapes, and a 4000-character run
# now refuses in 0.00014 s.
FINDING_ID_RE = re.compile(r"^(?:[^\w\s]\s*)*(\d+)$")
BARE_ID = "a bare integer"
# Which of the two tables a refusal is about. The reviewer writes one and the
# fixer copies the numbering into the other, so a message naming the format
# and not the file sends the reader to the table that is already correct.
RECORD_LABEL = "verdict table"
FIX_TABLE_LABEL = "fix table"
DEPTH_EXIT = "deferred with a named answerer, or becomes an issue"


def finding_number(label, seen, line, taken):
    """The finding one `#` cell names, or `Refused` naming format and row.

    Two refusals, and #227 is that the old code could produce only the
    second, out of a table that held no duplicate. Both name the table they
    read, quote the offending cell, and quote the whole row — with eight rows
    and no coordinate, finding the pair was a manual scan.

    `taken` is {number: the row that already claimed it}, so the duplicate
    refusal can quote both rows rather than assert that two exist.
    """
    text = chain.EMPHASIS.sub("", seen).strip()
    m = FINDING_ID_RE.match(text)
    if not m:
        raise Refused(
            f"the {label} has a row whose `#` reads {seen!r}, and a finding id "
            f"is {BARE_ID} — an optional severity marker, then digits and "
            "nothing else (`1`, `\N{LARGE RED CIRCLE} 2`, "
            "`\N{WHITE LARGE SQUARE} 13`). A round-prefixed id collapses "
            "toward one key: `R2-1` and `R2-2` are the same digits to a reader "
            "that takes the first run, which is how eight findings became one. "
            "Number this round's findings 1..N and let the record's own file "
            f"name carry the round. The row: {line.strip()}"
        )
    number = int(m.group(1))
    if number in taken:
        raise Refused(
            f"the {label} has two rows numbered {number}:\n"
            f"    {taken[number].strip()}\n"
            f"    {line.strip()}\n"
            "A finding id names one row, so one of these has to change"
        )
    taken[number] = line
    return number


def part(label, text):
    """One name inside a surface entry — a unit or a site — or `Refused`.

    The writer joins names into `unit → site, site` and `unit (depth N)`, so
    the separators are its own: a name carrying one would read as two names,
    and `cell`'s refusal of a comma in these rows is what this keeps true.
    """
    text = text.strip()
    if not text:
        raise Refused(f"`{label}` needs a name and got {text!r}")
    for what, char in (
        ("a pipe", "|"),
        ("a newline", "\n"),
        ("a newline", "\r"),
        ("a comma", ","),
        ("a semicolon", ";"),
    ):
        if char in text:
            raise Refused(
                f"`{label}` cannot carry {what} inside a name: {text!r}. The "
                "separators of that row are the writer's, never a name's"
            )
    return text


def contract_entry(unit, sites):
    """`unit → site, site`, every name checked."""
    label = chain.CONTRACT
    return f"{part(label, unit)} {ARROW} " + ", ".join(part(label, s) for s in sites)


def units_entry(unit, depth):
    """`unit (depth N)`, the name checked."""
    return f"{part(chain.NEW_UNITS, unit)} ({chain.DEPTH_WORD} {depth})"


def surface_cell(label, entries):
    """The row for one surface list: `none` when empty, else `;`-joined.

    `row` rather than `cell`, because the joined value carries the writer's
    own commas and `cell` refuses one in these rows on purpose — every name
    in `entries` has been through `part`, which is the check `cell` would
    have made on the whole.
    """
    if not entries:
        return cell(label, chain.NONE_WORD)
    return row((label, "; ".join(entries)))


def parse_range(root, value):
    """(a, b) as full commits from `<a>..<b>`, or `Refused`."""
    a, dots, b = value.partition("..")
    a, b = a.strip(), b.strip()
    if not dots or not a or not b or b.startswith("."):
        raise Refused(f"--range {value!r} is not `<a>..<b>`")
    out = []
    for ref in (a, b):
        full = chain.resolves_to(root, ref)
        if full is None:
            raise Refused(f"--range names `{ref}`, which does not resolve in {root}")
        out.append(full)
    return out[0], out[1]


def touched(root, a, b):
    """The paths the range changes, as they stand at `b`; deletions left out.

    A rename is one path — the new one — so a renamed file's units read as
    new when nothing at `a` carries that path, which is the honest reading
    of a comparison that opens both ends by path.
    """
    out = git(root, "diff", "--name-status", "-M", a, b)
    if out is None:
        raise Refused(f"git diff {a[:7]}..{b[:7]} failed in {root}")
    paths = []
    for line in out.splitlines():
        cells = line.split("\t")
        if len(cells) < 2 or not cells[0] or cells[0][0] == "D":
            continue
        paths.append(cells[-1])
    return paths


def parse_module(text):
    """`ast.Module`, or None for text that is not Python."""
    if text is None:
        return None
    try:
        return ast.parse(text)
    except (SyntaxError, ValueError):
        return None


def signature(args):
    """A unit's parameters: names in order, whether each has a default, and
    the `*args` / `**kwargs` names — what a call site can be wrong about."""
    positional = args.posonlyargs + args.args
    padding = [False] * (len(positional) - len(args.defaults))
    defaults = padding + [True] * len(args.defaults)
    return (
        tuple((arg.arg, has) for arg, has in zip(positional, defaults, strict=True)),
        args.vararg.arg if args.vararg else None,
        tuple(
            (arg.arg, default is not None)
            for arg, default in zip(args.kwonlyargs, args.kw_defaults, strict=True)
        ),
        args.kwarg.arg if args.kwarg else None,
    )


def return_arities(node):
    """The set of arities the unit's own `return` statements have — 0 for a
    bare `return`, n for a tuple of n elements, 1 for anything else. A
    nested def, class or lambda is somebody else's returns."""
    found, stack = set(), list(node.body)
    while stack:
        n = stack.pop()
        if isinstance(
            n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
        ):
            continue
        if isinstance(n, ast.Return):
            if n.value is None:
                found.add(0)
            elif isinstance(n.value, ast.Tuple):
                found.add(len(n.value.elts))
            else:
                found.add(1)
        stack.extend(ast.iter_child_nodes(n))
    return frozenset(found)


def return_literals(node):
    """The set of constant values the unit's own `return` statements can
    produce, as `(type name, repr)` pairs — the value taken whole when the
    return is a constant, and its constant elements when it is a tuple. A
    nested def, class or lambda is somebody else's returns, the same boundary
    `return_arities` draws.

    #194: the contract compared parameters and return ARITIES, so a unit that
    began returning a value it could not return before — the same shape with
    a new meaning — changed neither and the row read `none`. The measured
    instance is `token_thirds`, which began returning 0 for a mean it cannot
    compute; the one call site interpreting that 0 was not revisited, and it
    reports growth on a run whose input collapsed. `templates/sdd-round.md`
    had already promised this half — *signature, return arity, return type,
    or set of returnable values*.

    **Keyed by type as well as value on purpose.** Python hashes `0` and
    `False` into one key, and `1` and `True` likewise, so a plain set of
    values reads a unit that swapped a count for a flag as unchanged. Those
    are two different things to return and two different things for a caller
    to test.

    What this does NOT catch is a changed input→value mapping, and that hole
    is stated in `docs/review-chain-spec.md` rather than closed. Widening it
    to reach that is not a small step: it is asking which inputs reach which
    return, which is the function.
    """
    found, stack = set(), list(node.body)
    while stack:
        n = stack.pop()
        if isinstance(
            n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
        ):
            continue
        if isinstance(n, ast.Return) and n.value is not None:
            parts = n.value.elts if isinstance(n.value, ast.Tuple) else [n.value]
            for part in parts:
                if isinstance(part, ast.Constant):
                    found.add((type(part.value).__name__, repr(part.value)))
        stack.extend(ast.iter_child_nodes(n))
    return frozenset(found)


def top_units(module):
    """{name: (contract, first line, last line)} for every top-level def,
    class and constant, in source order.

    The contract is what `Contract changes` compares: a function's
    parameters, return arities and set of returnable constant literals; a
    class's `__init__` parameters; and nothing for a constant — a changed
    value is not a changed contract. A constant is an assignment to a bare
    name at module level.

    The third element is #194's, and it is the last of the four things
    `templates/sdd-round.md` promises this row reads. `return_literals` says
    what it is and what it deliberately does not reach.
    """
    out = {}
    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            contract = (
                signature(node.args),
                return_arities(node),
                return_literals(node),
            )
            out[node.name] = (contract, node.lineno, node.end_lineno)
        elif isinstance(node, ast.ClassDef):
            init = next(
                (
                    n
                    for n in node.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and n.name == "__init__"
                ),
                None,
            )
            contract = (signature(init.args) if init else None, None, None)
            out[node.name] = (contract, node.lineno, node.end_lineno)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    out[target.id] = (None, node.lineno, node.end_lineno)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.value is not None:
                out[node.target.id] = (None, node.lineno, node.end_lineno)
    return out


def enclosing_unit(units, line):
    """The top-level unit whose lines hold `line`, or None at module level."""
    for name, (_, first, last) in units.items():
        if first <= line <= (last or first):
            return name
    return None


def measure(reader, root, a, b, paths):
    """(changed, added, heuristic, at_a, at_b) over the range.

    `changed` and `added` are `[(path, unit)]` — a contract that differs
    between the two ends, and a unit present at `b` and absent at `a`, in
    file order. `heuristic` names the files whose units came from the diff
    lines rather than the AST; a prose file (`PROSE_SUFFIXES`) is neither
    and is skipped whole. `at_a` and `at_b` are the parsed units per path,
    for the depth walk and the call-site walk.
    """
    changed, added, heuristic, at_a, at_b = [], [], [], {}, {}
    for rel in paths:
        if rel.endswith(PROSE_SUFFIXES):
            continue
        before_text = reader.show(root, a, rel)
        after_text = reader.show(root, b, rel)
        before = parse_module(before_text) if rel.endswith(".py") else None
        after = parse_module(after_text) if rel.endswith(".py") else None
        by_ast = after is not None and (before_text is None or before is not None)
        if by_ast:
            old = top_units(before) if before is not None else {}
            new_units = top_units(after)
            at_a[rel], at_b[rel] = old, new_units
            for name, (contract, _, _) in new_units.items():
                if name not in old:
                    added.append((rel, name))
                elif contract is not None and contract != old[name][0]:
                    changed.append((rel, name))
            continue
        heuristic.append(rel)
        for line in (git(root, "diff", a, b, "--", rel) or "").splitlines():
            m = HEURISTIC_RE.match(line)
            if m:
                added.append((rel, m.group(1)))
    return changed, added, heuristic, at_a, at_b


def under_tests(path):
    return TESTS_DIR in path.split("/")[:-1]


def decorated_as(node, name):
    """True when a decorator on `node` is `name` or ends in `.name`.

    Covers the four spellings a fixture arrives in — `@fixture`,
    `@fixture(...)`, `@pytest.fixture`, `@pytest.fixture(...)` — by reading
    the callee of a decorator that is a call and the decorator itself
    otherwise. The import alias is deliberately not resolved: what a module
    calls `pytest` is its own business, and the tail is the part that names
    the decorator.
    """
    for dec in getattr(node, "decorator_list", []):
        target = dec.func if isinstance(dec, ast.Call) else dec
        if isinstance(target, ast.Attribute) and target.attr == name:
            return True
        if isinstance(target, ast.Name) and target.id == name:
            return True
    return False


def collected(base):
    """True when pytest's default `python_files` patterns import this file.

    Collection is two rules and the arm below used to ask only one of them:
    `python_files = test_*.py *_test.py` decides which FILE becomes a test
    module, and `python_functions = test_*` decides which def inside it is a
    case. A `test_*` def in `tests/helpers.py` satisfies the second and not
    the first, so pytest never runs it — and `pytest only` would then say the
    runner covers a unit nothing covers.
    """
    return base.startswith(TEST_PREFIX) or base.endswith(TEST_SUFFIX)


def conftest_is_loaded(root, b, rel):
    """True when pytest imports this `conftest.py` at all.

    A conftest is loaded for the test files collected at or below its OWN
    directory — rootdir down to each collected file, `confcutdir` defaulting
    to rootdir — so one in a directory nothing is collected under is never
    imported, and its fixtures and hooks are injected into nothing. Round 2's
    finding 1 is that accepting the name alone said `pytest only` about all
    of them: `src/`, `a/b/`, a vendored tree, an examples directory, and
    `tests/vendor/` one gate over. That is round 1's finding 1 pointing the
    other way, which is the sentence `plan.md`'s alternatives table rejected
    the wider rule to avoid.

    The question is asked of the tracked file list rather than of the
    filesystem, so it answers for the tree at `b` the way every other walk
    here does. The repository root passes it in any tree that has tests at
    all, which is the placement round 1's finding 2 was raised for;
    `src/conftest.py` passes it in a colocated layout and fails it in a
    segregated one, which is what pytest does.
    """
    here = os.path.dirname(rel)
    prefix = f"{here}/" if here else ""
    return any(
        p.startswith(prefix) and collected(os.path.basename(p))
        for p in tracked_at(root, b)
        if p.endswith(".py")
    )


def runner_reached(reader, root, b, rel, name):
    """True when pytest reaches `rel`'s `name` with no call site in the tree.

    The three members are the constants above, and each is a rule of pytest's
    own collection rather than a convention of this repository: a def that
    `python_files` collects and `python_functions` names is a case, a fixture
    is injected by parameter name, and a `pytest_*` def in a `conftest.py` is
    dispatched as a hook.

    Where the file sits decides two different things, and they are not the
    same gate. A conftest is loaded by NAME rather than by directory, so it
    is a member from anywhere pytest would load it — and the directory is
    what says whether pytest loads it at all, which is `conftest_is_loaded`.
    That one rule replaces the `tests/` gate for a conftest at every
    placement, inside `tests/` and outside it alike, because a conftest with
    nothing collected under it is imported by nobody wherever it sits.
    Nothing else outside `tests/` is a member however it is named.
    """
    base = os.path.basename(rel)
    if not rel.endswith(".py"):
        return False
    if base == CONFTEST:
        if not conftest_is_loaded(root, b, rel):
            return False
    elif not under_tests(rel):
        return False
    module = parse_module(reader.show(root, b, rel))
    if module is None:
        return False
    for node in module.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name != name:
            continue
        if name.startswith(TEST_PREFIX) and collected(base):
            return True
        if name.startswith(HOOK_PREFIX) and base == CONFTEST:
            return True
        return decorated_as(node, FIXTURE)
    return False


def call_sites(reader, root, b, rel, name, at_b):
    """The reach of one changed unit at `b`: the enclosing top-level unit of
    every `name(` in the tracked files, the unit's own def line excluded,
    the file's basename for a call at module level or outside Python.

    Callers under `tests/` collapse to `pytest`, and to `pytest only` when
    they are the whole reach — or when the unit is one pytest itself reaches
    (`runner_reached`), which has no call site in the tree by design. A unit
    nobody calls and nothing collects reads `no call site found`, because
    `fix_surface` refuses a unit listed without a reach and an empty reach
    would be the tolerant read it refuses.
    """
    out = git(root, "grep", "-n", "-F", "-e", f"{name}(", b) or ""
    word = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"\(")
    named, tested = [], False
    for line in out.splitlines():
        try:
            _ref, path, number, text = line.split(":", 3)
            number = int(number)
        except ValueError:
            continue
        if not word.search(text):
            continue
        if path.endswith(".py"):
            if path not in at_b:
                module = parse_module(reader.show(root, b, path))
                at_b[path] = top_units(module) if module is not None else {}
            units = at_b[path]
            site = enclosing_unit(units, number)
            if path == rel and site == name and number == units[name][1]:
                continue
            site = site or os.path.basename(path)
        else:
            site = os.path.basename(path)
        if under_tests(path):
            tested = True
        elif site not in named:
            named.append(site)
    if not named:
        if tested or runner_reached(reader, root, b, rel, name):
            return [PYTEST_ONLY]
        return [NO_SITE]
    return named + ([PYTEST] if tested else [])


def fix_table(reader, path):
    """{finding number: (word, value, note)} from the smith's `## Fixes`.

    `value` is the commit for `fixed`, the grounds for `answered`, the home
    for `deferred`; `note` is what stood beside the commit, if anything.
    Refused: a row whose `#` names no number or names one twice, a verdict
    outside the three, a `fixed` whose third cell names no commit, an
    `answered` with no grounds, a `deferred` with no home.
    """
    # RIDER: `note` below cuts the sha out of the middle of its own code span
    # and leaves both backticks standing, because `chain.SEPARATORS` carries a
    # space, two dashes, a hyphen, a colon and a comma -- and no backtick. A
    # `fixed` cell reading ``fixed at `e7d3447` `` therefore lands in the
    # record as `fixed at e7d3447 -- `` --`, an empty code span beside the
    # commit. Read 2026-09-06 at aed3ca0 against `chain_check.py#SEPARATORS`
    # and visible in this work item's own `rounds/round-1.md`, rows 1 to 3.
    # It predates this branch. The repair is at the `note` line and NOT in
    # `chain.SEPARATORS`, which is shared with the `deferred` home and with
    # `chain_check`'s own readers: widening it there would strip a backtick
    # off a home that is deliberately a code span. Round 2's finding 9;
    # `seal/follow-up.md`'s header sends a coordinate-tied item here rather
    # than to that file. Verified 2026-09-08 against fix_table@884956f3.
    text = read_text(path, "fix table")
    raw, lines = text.splitlines(), reader.readable(text)
    out, taken = {}, {}
    for i, cells in table_body(reader, lines, FIXES, FIXES_HEADER, True):
        seen = [reader.visible(c) for c in cells]
        if len(seen) < len(FIXES_HEADER):
            raise Refused(f"a fix row has {len(seen)} cells: {raw[i].strip()!r}")
        number = finding_number(FIX_TABLE_LABEL, seen[0], raw[i], taken)
        verdict = chain.EMPHASIS.sub("", seen[1]).strip().rstrip(".").strip()
        word, third = verdict.lower(), seen[2].strip()
        if word == FIXED:
            sha = chain.SHA_RE.search(third)
            if not sha:
                raise Refused(
                    f"finding {number} is `{FIXED}` and its third cell names no "
                    f"commit: {third!r}. A fix is a commit somebody can open"
                )
            note = (third[: sha.start()] + third[sha.end() :]).strip(chain.SEPARATORS)
            out[number] = (FIXED, sha.group(), note)
        elif word == ANSWERED:
            if not third:
                raise Refused(
                    f"finding {number} is `{ANSWERED}` with no grounds in its "
                    "third cell. An answer nobody can argue with is not one"
                )
            out[number] = (ANSWERED, third, "")
        elif word == DEFERRED_WORD or (
            word.startswith(DEFERRED_WORD)
            and word[len(DEFERRED_WORD)] in chain.SEPARATORS
        ):
            home = verdict[len(DEFERRED_WORD) :].strip(chain.SEPARATORS) or third
            if not home:
                raise Refused(
                    f"finding {number} is `{DEFERRED_WORD}` with no home. Write "
                    f"`{DEFERRED_WORD} #N` or `{DEFERRED_WORD} <path>` — a "
                    "deferral to nowhere is how *someone will look at it* "
                    "becomes nobody did"
                )
            out[number] = (DEFERRED_WORD, home, "")
        else:
            raise Refused(
                f"finding {number}'s verdict `{seen[1]}` is none of `{FIXED}`, "
                f"`{ANSWERED}`, `{DEFERRED_WORD} <home>` — the three a fix pass "
                "may hand over. A reviewer's words (`withdrawn`, `not a "
                "defect`) are the reviewer's to write"
            )
    return out


def verdict_rows(reader, lines):
    """{finding number: (index, cells)} for round N's verdict table."""
    out, taken = {}, {}
    for i, cells in table_body(reader, lines, VERDICTS, VERDICT_HEADER, True):
        seen = [reader.visible(c) for c in cells]
        if len(seen) <= NUMBER_COL:
            raise Refused(f"a verdict row has no `#` cell: {lines[i].strip()!r}")
        number = finding_number(RECORD_LABEL, seen[NUMBER_COL], lines[i], taken)
        out[number] = (i, cells)
    return out


def units_named_earlier(reader, earlier):
    """{unit: K} for every entry of every earlier record's `New units` row,
    the lowest round first, in the entry grammar the checker reads."""
    named = {}
    for k, path in earlier:
        text = read_text(path, f"earlier record round-{k}.md")
        value = chain.field(
            chain.table_rows(reader, reader.readable(text)), chain.NEW_UNITS
        )
        if value is None or chain.says_none(reader.visible(value)):
            continue
        for entry in reader.visible(value).split(";"):
            entry = chain.DEPTH_RE.sub("", entry)
            for arrow in chain.ARROWS:
                entry = entry.split(arrow)[0]
            name = chain.EMPHASIS.sub("", entry).strip()
            if name and name not in named:
                named[name] = k
    return named


def tracked_at(root, a):
    """The paths the tree at `a` carries, for resolving a Location's path."""
    return set((git(root, "ls-tree", "-r", "--name-only", a) or "").splitlines())


def resolve_path(rel, tracked):
    """The tracked path a Location's path names, or None.

    Exact first, then `./`-stripped, then the one tracked path ending in
    `/<rel>` — a basename or a nested tail. Two candidates resolve to
    neither, because guessing a file is how a unit in the wrong file gets
    refused.
    """
    rel = rel[2:] if rel.startswith("./") else rel
    if rel in tracked:
        return rel
    ends = [t for t in tracked if t.endswith("/" + rel)]
    return ends[0] if len(ends) == 1 else None


def location_units(reader, root, a, text, tracked):
    """[(path or None, unit)] the `Location` cell of a finding names.

    Every path is resolved against `tracked`, the tree at `a` where the fix
    started (`resolve_path`); one that resolves to nothing names no unit
    here. A `path:line` is resolved to the top-level unit holding that line
    at `a`. A backticked identifier, with or without `()`, or a cell that
    is one bare identifier, names a unit and no file, and the caller finds
    the file among the ones the range touched.
    """
    visible = reader.visible(text)
    out, last = [], None
    for m in LOCATION_UNIT_RE.finditer(visible):
        last = resolve_path(m.group(1), tracked)
        if last is not None:
            out.append((last, m.group(2)))
    for m in FRAGMENT_RE.finditer(visible):
        out.append((last, m.group(1)))
    for m in LOCATION_LINE_RE.finditer(visible):
        rel = resolve_path(m.group(1), tracked)
        module = parse_module(reader.show(root, a, rel)) if rel is not None else None
        unit = enclosing_unit(top_units(module), int(m.group(2))) if module else None
        if unit:
            out.append((rel, unit))
    for m in IDENTIFIER_RE.finditer(visible):
        out.append((None, m.group(1)))
    m = BARE_IDENTIFIER_RE.match(visible)
    if m:
        out.append((None, m.group(1)))
    return out


def depth_two(reader, root, a, rows, fixes, added, at_a, earlier):
    """`Refused` when a `fixed` finding sits inside a unit an earlier record's
    `New units` names and the range adds a unit in that finding's file.

    That is depth 2 — a unit added by the fix of a finding inside a unit an
    earlier fix pass created — and the rule refuses it at the keyboard,
    naming the unit, the finding, the record whose row names the parent,
    and the exit. Nothing has been written when this raises.

    A Location that names a file is inside the unit only if that file
    holds a top-level unit of that name at `a` — `at_a` is the range's
    files parsed there, and a file the range did not touch has nothing
    added to refuse. A Location that names no file is resolved against
    every file the range touched that holds the unit at `a`, which is the
    widest honest reading of a name with no path beside it.
    """
    named = units_named_earlier(reader, earlier)
    if not named or not added:
        return
    tracked = tracked_at(root, a)
    for number, (word, _, _) in fixes.items():
        if word != FIXED:
            continue
        _i, cells = rows[number]
        location = cells[LOCATION_COL] if len(cells) > LOCATION_COL else ""
        for rel, unit in location_units(reader, root, a, location, tracked):
            if unit not in named:
                continue
            if rel is not None:
                files = [rel] if unit in at_a.get(rel, {}) else []
            else:
                files = [f for f, units in at_a.items() if unit in units]
            for f in files:
                inside = [n for r, n in added if r == f]
                if not inside:
                    continue
                raise Refused(
                    f"{', '.join(f'`{n}`' for n in inside)} in {f} would be at "
                    f"depth 2: added by the fix of {reader.visible(cells[NUMBER_COL])}, "
                    f"whose Location `{reader.visible(location)}` is inside "
                    f"`{unit}`, a unit round-{named[unit]}.md's `{chain.NEW_UNITS}` "
                    "names. A fix pass may add a unit; that unit's fix may not, "
                    "because the fix is read by the round that follows and the "
                    "unit it added is read by nobody. The unit is "
                    f"{DEPTH_EXIT}; no cell was written"
                )


def field_index(reader, lines, label):
    """The index of the one `| label | … |` row, or `Refused`."""
    hits = [
        i
        for i, ln in enumerate(lines)
        for cells in [reader.split_row(ln)]
        if cells and len(cells) >= 2 and cells[0].strip() == label
    ]
    if len(hits) != 1:
        raise Refused(
            f"the record has {len(hits)} `| {label} | … |` rows and needs one"
        )
    return hits[0]


def close(args):
    """Apply the fix table, measure the surface, tick `Pass`, run the check.

    Every refusal comes before the write: the table is parsed, every `fixed`
    commit resolved and placed inside the range, the range measured and the
    depth walked, and only then is the record rewritten in one pass.
    """
    reader, routing, root, _item, rounds = where(args)
    target = os.path.join(rounds, f"round-{args.round}.md")
    if not os.path.isfile(target):
        # The second member of ⬜ 6's class, same cause: `isfile` is False for
        # a directory too, and `does not exist` about a path that has one is
        # the reading the message has to rule out.
        raise Refused(
            f"{target} is a directory, not a record — `close` fills a record "
            "`new` wrote"
            if os.path.isdir(target)
            else f"{target} does not exist — `close` fills a record `new` wrote"
        )
    a, b = parse_range(root, args.range)
    fixes = fix_table(reader, args.fixes)

    text = read_text(target, f"record round-{args.round}.md")
    raw, lines = text.splitlines(), reader.readable(text)
    rows = verdict_rows(reader, lines)
    unknown = sorted(n for n in fixes if n not in rows)
    if unknown:
        raise Refused(
            f"the fix table names finding{'s' if len(unknown) > 1 else ''} "
            f"{', '.join(map(str, unknown))}, not in round {args.round}'s verdict "
            f"table (which has {', '.join(map(str, sorted(rows)))})"
        )
    open_now = [
        n
        for n, (_i, cells) in rows.items()
        if chain.verdict_of([reader.visible(c) for c in cells], VERDICT_COL)
        not in chain.CLOSED_WORDS
    ]
    missing = [n for n in open_now if n not in fixes]
    if missing:
        raise Refused(
            f"finding{'s' if len(missing) > 1 else ''} {', '.join(map(str, missing))} "
            f"of round {args.round} left with no row in the fix table. Every open "
            f"finding takes a row — `{FIXED}`, `{ANSWERED}`, or "
            f"`{DEFERRED_WORD} <home>` — or the record stays open"
        )
    # A row for a finding the reviewer closed in the report (`withdrawn`,
    # `not a defect`) would overwrite the reviewer's verdict with the smith's
    # (round 1 of #161's own chain, 🟡 3). One row per OPEN finding.
    already = sorted(n for n in fixes if n not in open_now)
    if already:
        named = ", ".join(
            f"finding {n} (`{chain.verdict_of([reader.visible(c) for c in rows[n][1]], VERDICT_COL)}`)"
            for n in already
        )
        raise Refused(
            f"the fix table has a row for {named}, which the reviewer already "
            f"closed in round {args.round}'s verdict table. A fix pass answers "
            "the OPEN findings and no other — a row here would overwrite the "
            "reviewer's verdict with the smith's; no cell was written"
        )
    for number, (word, value, _note) in fixes.items():
        if word != FIXED:
            continue
        full = chain.resolves_to(root, value)
        if full is None:
            raise Refused(
                f"finding {number}'s commit `{value}` does not resolve in {root}"
            )
        if not chain.is_ancestor(root, full, b) or chain.is_ancestor(root, full, a):
            raise Refused(
                f"finding {number}'s commit `{value}` lies outside --range "
                f"{a[:7]}..{b[:7]}. A fix the range does not hold is a fix the "
                "surface below was not measured on"
            )

    paths = touched(root, a, b)
    changed, added, heuristic, at_a, at_b = measure(reader, root, a, b, paths)
    earlier = earlier_records(routing, rounds, args.round)
    depth_two(reader, root, a, rows, fixes, added, at_a, earlier)

    contract = surface_cell(
        chain.CONTRACT,
        [
            contract_entry(n, call_sites(reader, root, b, r, n, at_b))
            for r, n in changed
        ],
    )
    # One entry per name, first seen first: two files adding the same name
    # read as one unit here, because the row carries no path (⬜ 7).
    units = surface_cell(
        chain.NEW_UNITS,
        [units_entry(n, 1) for n in dict.fromkeys(n for _r, n in added)],
    )
    gate = cell(BROAD_GATE, args.broad_gate) if args.broad_gate else None

    # Nothing above touched `raw`; everything below does, indices first and
    # the one insertion last.
    for number, (word, value, note) in fixes.items():
        i, _cells = rows[number]
        cells = row_cells(reader, raw[i], len(VERDICT_HEADER))
        while len(cells) <= GROUNDS_COL:
            cells.append("")
        old = cells[GROUNDS_COL].strip()
        if word == FIXED:
            cells[VERDICT_COL] = f"**{FIXED}** `{value}`"
            grounds = f"{FIXED_AT} {value}" + (f" {DASH} {note}" if note else "")
            cells[GROUNDS_COL] = grounds + (f"; {old}" if old else "")
        elif word == ANSWERED:
            cells[VERDICT_COL], cells[GROUNDS_COL] = ANSWERED, value
        else:
            cells[VERDICT_COL], cells[GROUNDS_COL] = f"{DEFERRED_WORD} {value}", value
        raw[i] = row([escape(c) for c in cells])
    words = [
        chain.verdict_of(
            [reader.visible(c) for c in row_cells(reader, raw[i], len(VERDICT_HEADER))],
            VERDICT_COL,
        )
        for i, _ in rows.values()
    ]
    still_open = [w for w in words if w not in chain.CLOSED_WORDS]
    # The same derivation `new` makes from the report's verdicts, over the
    # verdicts as the table left them. `no fixes to check` is written only
    # when it is the answer; otherwise the cell stays at the landing value
    # for `new` of the next round to set, because a fix was written and a
    # later round owes it a reading.
    checker, _surface = landing_values(words)
    boxes = [i for i, ln in enumerate(lines) if chain.PASS_RE.match(ln)]
    if len(boxes) != 1:
        raise Refused(f"the record has {len(boxes)} `Pass` boxes and needs one")
    raw[boxes[0]] = f"- [{' ' if still_open else 'x'}] Pass"
    if checker == chain.NO_FIXES:
        raw[field_index(reader, lines, chain.CHECKED_BY)] = cell(
            chain.CHECKED_BY, checker
        )
    raw[field_index(reader, lines, chain.CONTRACT)] = contract
    last = field_index(reader, lines, chain.NEW_UNITS)
    raw[last] = units
    if gate is not None:
        raw[field_index(reader, lines, BROAD_GATE)] = gate
    if heuristic:
        while last + 1 < len(raw) and reader.split_row(raw[last + 1]) is not None:
            last += 1
        raw.insert(
            last + 1,
            f"<!-- {chain.NEW_UNITS}: {', '.join(heuristic)} {HEURISTIC_NOTE} -->",
        )

    ending = "\n" if text.endswith("\n") else ""
    write_record(reader, target, "\n".join(raw) + ending)
    counts = {
        w: sum(1 for word, _, _ in fixes.values() if word == w)
        for w in (FIXED, ANSWERED, DEFERRED_WORD)
    }
    print(
        f"round-record: closed {os.path.relpath(target, root)} {DASH} "
        + ", ".join(f"{n} {w}" for w, n in counts.items())
        + f"; {contract.strip('| ')}; {units.strip('| ')}"
        + (f"; {chain.CHECKED_BY} | {checker}" if checker == chain.NO_FIXES else "")
    )
    return run_check(root, args.baseline or default_baseline(root))


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="round-record",
        description="Write a review round's record from the reviewer's report.",
    )
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("new", help="write rounds/round-N.md")
    p.add_argument("--item", required=True, help="the work item directory")
    p.add_argument("--round", required=True, type=int, metavar="N")
    p.add_argument("--target", required=True, help="the commit this round reviewed")
    p.add_argument(
        "--report",
        default=None,
        help="the reviewer's report, a file "
        "(default: <item>/rounds/round-<N>-report.md, where the reviewer "
        "leaves it)",
    )
    p.add_argument("--asked", required=True, help="the round paragraph, a file")
    p.add_argument("--ran-by", required=True, help="`<agent> on <model>`")
    p.add_argument("--broad-gate", default=None, help="the Broad gate cell")
    p.add_argument("--pr", default=None, help="the PR cell")
    p.add_argument("--root", default=None, help="the repository (default: the item's)")
    p.add_argument(
        "--baseline",
        default=None,
        help="the base for chain_check (default: the upstream, else origin/main)",
    )
    c = sub.add_parser("close", help="apply the fix table to rounds/round-N.md")
    c.add_argument("--item", required=True, help="the work item directory")
    c.add_argument("--round", required=True, type=int, metavar="N")
    c.add_argument(
        "--fixes", required=True, help=f"the smith's `{FIXES}` table, a file"
    )
    c.add_argument("--range", required=True, metavar="A..B", help="the fix commits")
    c.add_argument("--broad-gate", default=None, help="the Broad gate cell")
    c.add_argument("--root", default=None, help="the repository (default: the item's)")
    c.add_argument(
        "--baseline",
        default=None,
        help="the base for chain_check (default: the upstream, else origin/main)",
    )
    args = ap.parse_args(argv)
    try:
        return close(args) if args.command == "close" else new(args)
    except Refused as exc:
        print(f"round-record: {exc}", file=sys.stderr)
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
