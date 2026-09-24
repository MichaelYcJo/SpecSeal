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
  Target SHA          the commit `--target` resolves to, never the revision
                      as typed; a flag that does not resolve is refused
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
# The label of the row this script WRITES and `chain_check.py` now READS, and
# the value meaning the run has not happened. Both used to be defined here,
# under a comment reading *"Field labels the checker has no constant for,
# because it never reads them"* -- true until #295, when the checker started
# reading this one. They moved to the reader, and this is the import, because
# the failure of two copies is silent in the direction that matters: rename
# the row here alone and this script keeps writing a row the checker no
# longer finds, which the checker reads as `no run was named`.
BROAD_GATE = chain.BROAD_GATE
GATE_NOT_YET = chain.GATE_NOT_YET
# What `seal` writes between the entries of a `Broad gate` cell that already
# held a run (#174): the new entry first, then this, then what was there. The
# cell used to hold one entry that every `seal` REPLACED, so a run taken
# again — after a pre-existing failure, or after the last fixes landed — erased
# the record of the first and the run-level table was filled from memory.
# Three constraints, all the readers': no `|` (a cell), no SHA-shaped word
# (`chain_check.broad_gate` takes the first one as the run) and no `<!--` (the
# hider question every record is asked). `earlier run` is none of those, and
# the newest entry stays first so the reader's `named[0]` is unchanged.
EARLIER_RUN = "; earlier run: "


def kept_broad_gate(reader, rows, value):
    """`value` in front of the run `rows`' `Broad gate` cell already holds,
    or `value` alone where it holds none (#174).

    ONE ENTRY PER RUN, NEWEST FIRST, for every writer of the cell. `seal` and
    `close --broad-gate` used to disagree — the first kept a held run and the
    second replaced it, while the template described them as writing the
    same cell (round 1's 🟡 1) — so both call this and neither builds the
    cell from the flag alone. `not yet` holds no run and is replaced, so a
    first seal is byte-identical to what it always was; the new entry goes in
    front so that `chain_check.broad_gate`, which takes the first SHA-shaped
    word as the run, reads what it read before.

    **A run the newest entry already records — the same commit against the
    same base — replaces that entry rather than standing beside it** (round
    1's ⬜ 8, narrowed by round 2's 🟡 1). It is the same claim about the
    same comparison — the sealer re-run over an unchanged checkout — and
    two entries for one claim would make the count of entries stop being
    the count of distinct comparisons — commit and base — which is what
    the run-level table reads off the cell. A run at that commit against
    ANOTHER base is another comparison and is kept behind the new entry
    like any earlier run, which is what `agents/sealer.md` and the
    `broad-gate.md` comment promise: a second run never erases the first.
    Keyed on the SHA alone, the replace
    erased the first base. The comparison is `same_run`'s, by prefix per
    SHA-shaped word, so an abbreviated entry and a full-length flag name one
    commit; nothing here asks git: `seal` has already refused a flag that
    does not resolve, and `close --broad-gate` never resolves its flag, so a
    value with no SHA-shaped word is written as typed and left for
    `chain_check.broad_gate` to report at the pull request.
    """
    held = reader.visible(chain.field(rows, BROAD_GATE) or "").strip()
    if not held or chain.says_gate_not_yet(held):
        return value
    entries = held.split(EARLIER_RUN)
    if same_run(entries[0], value):
        entries = entries[1:]
    if not any(chain.SHA_RE.search(e) for e in entries):
        return value
    return EARLIER_RUN.join([value, *entries])


def same_run(entry, value):
    """Whether `entry` and `value` record one run: the same commit AND the
    same base. A SHA-shaped word is compared by prefix, so an abbreviated
    entry and a full-length flag agree; every other word exactly. Two runs
    at one commit against different bases are two comparisons —
    `agents/sealer.md` binds a seal to both halves — and both are kept.
    """
    a, b = entry.split(), value.split()
    if len(a) != len(b):
        return False
    for x, y in zip(a, b, strict=True):
        if chain.SHA_RE.fullmatch(x) and chain.SHA_RE.fullmatch(y):
            if not (x.startswith(y) or y.startswith(x)):
                return False
        elif x != y:
            return False
    return True


# The row this script writes and `chain_check.written_late` reads, imported
# from the reader for the same reason `BROAD_GATE` is: rename it in one file
# alone and this one keeps writing a row the checker no longer finds, which
# the checker reads as a record that said nothing.
WRITTEN_LATE = chain.WRITTEN_LATE
# The honest value while nothing has happened yet. `not yet opened` is what
# `chain_check.declared_pull_head` documents as the pre-pull-request value;
# `nothing to drain` is `templates/sdd-round.md`'s required answer for a
# Deferred section with no rows.
PR_NOT_YET = "not yet opened"
NOTHING_TO_DRAIN = "nothing to drain"
# Built by codepoint for the reason `chain_check.SEPARATORS` gives: an em dash
# in a string literal is what ruff's RUF001 reads as a mistyped hyphen.
DASH = chr(0x2014)
# The landing values `ORDER_FROM` requires of a record committed before its
# fixes exist, spelled from the checker's own words.
PENDING_CHECKER = f"{chain.NOBODY} {DASH} {chain.NOT_YET}"
PENDING_SURFACE = f"{chain.NONE_WORD} {DASH} {chain.NOT_YET}"
# What the checker row says once `close` has applied a fix table that closed
# something on a fix word. `nobody` is still the truth -- the ordering rule
# requires a checker to be a LATER round, and none exists at this moment --
# and the REASON is not: the fixes are named in this record's own verdict
# cells, two rows below, so *not yet written* is false beside the commits that
# wrote them (#273 part 1).
#
# `nobody -- <why>` is the shape, so `checked_by` reads it exactly as it read
# the landing value: that arm splits the word from its reason and requires
# only that a reason exist. Measured before this was written -- neither arm of
# `chain_check` reads the reason text. `fix_surface`'s pending arm keys on
# `CHECKER_RE`, which matches `round-N` and neither spelling of this, and the
# `says_not_yet` it then applies reads the SURFACE row, which `close` fills
# from the diff.
WRITTEN_CHECKER = (
    f"{chain.NOBODY} {DASH} the fixes are written and no round has opened them"
)
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


def section_end(lines, start):
    """The index of the line that ends the section opened at `start`, or
    `len(lines)` where nothing does — `chain.section_end`, the one
    definition of a section both scripts read by.

    A section ends at the first heading of its own level or shallower, and a
    deeper heading is INSIDE it (#505). It used to end at any line starting
    with `#`, so a `## Paste-ready fixes` organised under one `###` per
    finding — the readable way to write six of them — had an empty body
    before any fence was looked for, and the record read `no paste-ready fix
    in the report` over six. The better-written report was the one that lost
    its fixes, and nothing raised.

    One definition of *a section* for the module, and for the checker:
    `section_body` reads by it and `swallowed`'s section-end scan reads by
    it, so a table a `###` labels is inside the section to both — copied by
    one and, when it stands only inside a fence, refused by the other — and
    `chain_check.verdict_table` reads a record's `## Verdicts` by the same
    rule, which is why the definition lives there. A reviewer's `##` inside
    a section is still an end, as it always was; the one shape that changes
    is the deeper heading, and a `####` under a `###` under the section is
    carried for the same reason, because the rule is *same level or
    shallower ends it* and not *one level deeper is allowed*.
    """
    return chain.section_end(lines, start)


def section_body(reader, lines, heading):
    """(start, [(index, line)]) for the one section under `heading`, or None.

    `lines` are already `readable`, so a heading inside a comment or a fence
    is not a section, and indices are the raw file's. The section runs to
    `section_end`: a heading of the section's own level or shallower ends
    it, and a deeper one is part of it (#505).
    """
    starts = reader.sections(lines, heading)
    if not starts:
        return None
    if len(starts) > 1:
        raise Refused(f"the report has {len(starts)} `{heading}` sections")
    end = section_end(lines, starts[0])
    return starts[0], [(i, lines[i]) for i in range(starts[0] + 1, end)]


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
    # A row that repeats the header is a second table's header under a
    # `###` inside the section (round 1's 🟡 3 — reachable since #505 made
    # the section reach past the `###`): it names the columns and is not a
    # row, and copied through it carried a `#` cell reading `#` that
    # `finding_number` admits as a row commissioning nothing. Skipped the
    # way the separator is; the rows under it are the section's.
    return [
        (i, cells)
        for i, cells in rows[1:]
        if not reader.is_separator([reader.visible(c) for c in cells])
        and tuple(reader.visible(c) for c in cells) != header
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
        # The same end `section_body` reads by (#505): a table under a `###`
        # inside this section is this section's, so rows hidden there are
        # rows this section lost. Ending at any `#` put them outside the
        # span, and the record then arrived with the template's empty table
        # and nothing said so.
        end = section_end(lines, start)
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


# A line that opens a new markdown block, so the terminal value stops before
# it. The blank line is the ordinary end and markdown needs one anyway; these
# are the shapes a report puts next to a terminal line without one.
#
# Every marker CommonMark requires a space after asks for one here, which is
# what the previous spelling got wrong in both directions at once. A bare `#`
# reads `#120` at the head of a line as a heading, and a continuation
# beginning `#120` is this module's own subject hard-wrapped — in a repository
# that writes issue numbers that way in every record it keeps. The space
# requirement then takes the run-of-three markers out of the class, so a
# thematic break and a setext underline come back as whole-line alternatives
# of their own; `\r*$` on each is what makes a CRLF checkout read like an LF
# one. A `-` underline shorter than three characters is not among them and is
# joined: it rides on the thematic-break alternative, where the `=` side has
# one of its own at any length. That is the model module's trade, stated in
# its own comment as `a --- b`, `--` and `= x` are prose, and the blank line
# is what covers it. `\d+[.)]` is there because `1)` is an ordered list item
# and `\d+\.` alone let one through.
#
# **What it does not cover, and cannot.** A continuation that opens with an
# HTML tag, with `**bold**`, or with an indented run of prose is
# indistinguishable from a block opener by its first characters, and this
# pattern joins all three rather than guessing. Widening it to catch them is
# how the truncation got here: every marker added is one more shape a genuine
# continuation may not begin with, and a truncated cell reads as a finished
# sentence, so nobody looks. **The blank line under the terminal pair is the
# only stop that covers every shape**, which is why `agents/warden.md` asks
# the reviewer for one rather than relying on this.
#
# `.github/scripts/issue_claims_check.py#BLOCK_START` segments hand-wrapped
# prose for the same reason and pays the same price. The alternatives below
# are its, plus the two fence openers this module needs, and the two are kept
# spelled alike on purpose — `skills/code-review/scripts/survivor_check.py`
# is the third carrier of the same shape. They are not shared through an
# import: the two script roots ship on different paths and neither can reach
# the other.
BLOCK_START = re.compile(
    r"^[ \t]*(?:"
    r"[-*+](?=\s)"
    r"|\#{1,6}(?=\s|$)"
    r"|\d+[.)](?=\s)"
    r"|[>|]"
    r"|```|~~~"
    r"|(?:-[ \t]*){3,}\r*$"
    r"|(?:\*[ \t]*){3,}\r*$"
    r"|(?:_[ \t]*){3,}\r*$"
    r"|=+[ \t]*\r*$"
    r")"
)


def terminal_value(reader, lines, label):
    """What stands after the colon in the report's `<label>: …` line.

    **A wrapped line is one value.** `agents/warden.md` shows the two terminal
    lines in a fence and says nothing about wrapping, the prose around them is
    hand-wrapped, and a `yes — <what>` worth writing is long enough to reach
    the margin. Matching the physical line alone kept its remainder and
    dropped everything after the wrap with no refusal: `rounds/round-1.md` of
    #120 shipped ending mid-clause at *the one that reopens the*, where the
    report it was generated from carried *defect this work item was filed
    against* on the next line.

    Truncation is the dangerous direction of the two. A value cut at a wrap
    still reads as a finished sentence, so nobody looks; a value that swallowed
    a following line reads as wrong at a glance. So the value is joined across
    the wrap, and the run stops at a blank line, at the other terminal label,
    or at a line opening a new markdown block. That last guard is not
    decoration: ` ` is in `chain.SEPARATORS`, so a swallowed prose line parses
    as a `no` with a reason and lands in the cell looking deliberate.

    **The third stop is a narrowing and it does not cover every shape.**
    `BLOCK_START` above says which shapes it catches and which it deliberately
    joins instead of guessing at, and it is the one place in this module that
    lists them. Only the blank line covers all of them, so
    a report that leaves one under the terminal pair is the shape nothing can
    get wrong. `docs/review-handoff-protocol.md` §*The Needs a fix field — the
    answer a run ends on* states that rule for a second implementation, and
    `agents/warden.md` §*Report* asks the reviewer for the blank line.
    """
    pattern = re.compile(r"^\s*" + re.escape(label) + r"\s*:\s*(.*?)\s*$")
    others = tuple(
        re.compile(r"^\s*" + re.escape(other) + r"\s*:")
        for other in TERMINAL_LINES
        if other != label
    )
    found = []
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if match is None:
            continue
        parts = [match.group(1)]
        for following in lines[index + 1 :]:
            if not following.strip():
                break
            if BLOCK_START.match(following):
                break
            if any(other.match(following) for other in others):
                break
            parts.append(following.strip())
        found.append(" ".join(part for part in parts if part))
    if len(found) != 1:
        raise Refused(
            f"the report has {len(found)} `{label}:` lines and the record "
            "needs exactly one — the row is copied from what stands after "
            "the colon"
        )
    value = reader.visible(found[0])
    word, reason = chain.yes_or_no(value)
    if word is None:
        raise Refused(
            f"`{label}: {value}` is not `{chain.FLOOR_NO}` or "
            f"`{chain.FLOOR_YES} {DASH} <what>`, which is the vocabulary the "
            "checker reads the row in"
        )
    if word == chain.FLOOR_YES and not reason:
        # Refused here, at the writer, for the reason `written_late_cell`
        # refuses an empty `--written-late`: `chain_check.py` refuses a bare
        # `yes` in BOTH rows, so a record written with one fails one command
        # later than the reviewer is at the keyboard (#138). The class is
        # the two terminal lines, whichever the ticket named.
        raise Refused(
            f"`{label}: {value}` carries no reason. The whole of what makes "
            "the line readable is what was found, and the next round "
            "inherits it. `chain_check.py` refuses a bare `yes` in both "
            f"rows — `{chain.NEEDS}` because it is the cell the floor's "
            "count of later records restarts at, so three characters must "
            f"not buy a round; `{chain.FLOOR}` because the cell would record "
            "that something was found and not what. The shape is "
            f"`{chain.FLOOR_YES} {DASH} <what>`, copied from the reviewer's "
            "line of the same name, and refusing it here is one command "
            "earlier than the pull request"
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
    the first after the fix table applies and writes BOTH of its answers.
    One spelling, called from both subcommands, so the two cannot disagree
    about which words commission a fix.

    **`close` used to write only `no fixes to check`**, for the record whose
    every verdict closed on `deferred <home>` or `answered` — a capped run's
    last record has no next round to set the cell, and the check refuses
    `Pass` beside `nobody` there (`questions.md` A6 of the work item that
    added this). The other answer was left standing on the grounds that a fix
    was written and a later round owes it a reading, which is true of WHO and
    false of WHAT: the landing value says the fixes are not yet WRITTEN, and
    at this point they are written and named in the record's own verdict
    cells two rows below. `close` corrects the reason and keeps `nobody`
    (#273 part 1). It corrects only the landing value it recognises — a cell
    naming a `round-N` is a later round's reading and is not this pass's to
    touch.
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


def reach_forward(reader, rounds, n, rows):
    """Round N+1's inherited rows for round N, at the words round N's verdict
    cells now carry. Returns `(path, text, filled)` or None.

    `rows` is `{Location cell: (`#` cell, verdict word)}` for round N as the
    fix table has just left it — the caller has those in hand, and taking
    them rather than re-reading the record is what keeps this a pure read of
    the file it writes.

    **Two records committed together stated the same findings as open and as
    fixed** (#342). `new --round N+1` writes `## Inherited coordinates` from
    every earlier record's verdict cells, and at that moment round N's cells
    read `open`, because a record is committed BEFORE the fixes it commissions
    (`docs/review-chain-spec.md`'s ordering rule). `close --round N` then
    writes the words into round N and nothing carried them forward, so the
    `Why` cell froze at the reviewer's word while the record one file over
    said `**fixed**`.

    The reach is symmetric with `reach_back` above, which already goes the
    other way — into round N-1's `Fixes checked by` — and refuses rather than
    guesses when it cannot act. **Ordering `close --round N` before
    `new --round N+1` would cost no code and is not the repair**: it makes
    correctness depend on a spawn order nothing enforces, and the ordering
    rule requires the record committed before its fixes exist, so both orders
    are reachable by design.

    Silent where round N+1 does not exist, which is every ordinary run: the
    fix pass comes first and the verifying round is spawned after it. Silent
    too where its table names no row from round N **and accounts for round
    N's coordinates anyway**, because `inherited_rows` is first-seen-wins
    ACROSS rounds — a round whose every coordinate an earlier round already
    claimed is written into that section under the earlier round and under no
    other, which is the ordinary shape of a re-review round rather than a
    malformed record (round 1's 🔴 2).

    **Filling nothing has a second cause and the silence covered it too**
    (#405): the section EDITED OR TRUNCATED after `new` wrote it, which the
    other two refusals both miss — a table with no rows at all is readable
    and inherits no coordinate for the verdict table to lack. The accounting
    separates them. Every coordinate of round N appears in a table `new`
    wrote, so a table naming none of round N's rows and missing some of round
    N's coordinates is one that lost rows, and it is refused naming them.
    """
    path = os.path.join(rounds, f"round-{n + 1}.md")
    if not os.path.exists(path):
        return None
    text = read_text(path, f"later record round-{n + 1}.md")
    raw, lines = text.splitlines(), reader.readable(text)
    body = table_body(reader, lines, INHERITED, INHERITED_HEADER, False)
    if body is None:
        raise Refused(
            f"round-{n + 1}.md exists and has no readable `{INHERITED}` table, "
            f"so the rows this round's verdicts belong in cannot be found. "
            "Its `Why` cells will go on saying what round "
            f"{n} said before its fixes; write the section, or remove the "
            "record if the round has not run; no cell was written"
        )
    mine = f"round-{n}"
    filled = 0
    # Every coordinate the table carries, WHATEVER round it is attributed to.
    # `inherited_rows` is first-seen-wins across rounds, so round N's own
    # coordinates sit under round N or under an earlier round that claimed
    # them first -- which is why the accounting below reads the whole column
    # and not the `round-N` rows alone.
    accounted = set()
    for i, cells in body:
        seen = [reader.visible(c) for c in cells]
        if len(seen) < len(INHERITED_HEADER):
            continue
        accounted.add(seen[1])
        if seen[0].strip() != mine:
            continue
        coordinate = seen[1]
        if coordinate not in rows:
            raise Refused(
                f"round-{n + 1}.md inherits `{coordinate}` from {mine}, and "
                f"round-{n}'s verdict table holds no row with that `Location`. "
                "The reach-forward sets a `Why` cell from the row it names and "
                "does not guess which row that is; correct the coordinate; no "
                "cell was written"
            )
        cell_number, word = rows[coordinate]
        raw[i] = row(
            (
                mine,
                escape(coordinate),
                escape(f"round {n}'s {cell_number} {DASH} {word}"),
            )
        )
        filled += 1
    if not filled:
        # Filling nothing has TWO causes and only one of them is ordinary
        # (#405). The accounting is what tells them apart, and it runs only
        # here -- narrowed by measurement rather than by preference. Applied
        # to every run instead, it refuses a section whose rows are correct
        # as far as they go: 2 of the 139 committed round-N/round-N+1 pairs
        # fill a row from round N and still leave coordinates of round N
        # unaccounted, both of them sections written BY HAND rather than by
        # `new` (2026-09-15, `1788272986` round 2 and `1788433011` round 2).
        # A hand-written section is a shape this repository has; refusing it
        # for filling only what it knew about is the reader sent to correct a
        # table that is not wrong.
        unaccounted = [c for c in rows if c not in accounted]
        if unaccounted:
            named = ", ".join(sorted(unaccounted))
            many = "s" if len(unaccounted) > 1 else ""
            raise Refused(
                f"round-{n + 1}.md's `{INHERITED}` table names no row from "
                f"{mine} and does not account for {len(unaccounted)} of round "
                f"{n}'s coordinate{many} either: {named}. `new` writes one row "
                "per `Location` cell of every earlier record, so a table it "
                "wrote holds all of them — under this round or under an "
                "earlier one that claimed the coordinate first. A table "
                "holding neither was edited or truncated after `new` wrote "
                f"it, and the `Why` cells round {n}'s verdicts belong in are "
                "gone with the rows: regenerate the section, or put the rows "
                "back. A round whose every coordinate an earlier round "
                "already claimed is NOT this state — its table accounts for "
                "all of them and nothing is said; no cell was written"
            )
        # NOT a refusal (round 1's 🔴 2). `inherited_rows` is first-seen-wins
        # ACROSS rounds, so a round whose every coordinate an earlier round
        # already claimed is written into this section under that earlier
        # round and under no other. A re-review round looking again where the
        # round before it looked is the ordinary shape, and refusing it stops
        # the run this reach exists to keep truthful. The refusal's grounds
        # stated a rule about `new` without that qualifier, so the reader was
        # sent to correct a table that was already right.
        return None
    ending = "\n" if text.endswith("\n") else ""
    return path, "\n".join(raw) + ending, filled


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


# --- whether the commit the round read is still the branch's HEAD -----------

# `new` is the last command the orchestrator runs before it dispatches a fix
# pass. It is handed the commit the reviewer read and it can ask git for the
# branch's HEAD, and until this it compared the two for nothing -- so a record
# being written after its own fixes was first said out loud at the pull
# request, by `chain_check.written_late`, on a line no later commit can clear.
#
# It PRINTS and refuses nothing, and that is a measurement rather than a
# preference. A refusal was the shape this work item carried in, and phase 1
# measured what it would have cost: over this repository's own pre-squash
# branches -- the only place the moment survives, since a feature branch
# squashes into its release branch and takes the reviewed commit with it -- 40
# records of 152 have a `Target SHA` that is not their adding commit's first
# parent. Both of the two opened by hand differ because the round's OWN
# paperwork landed between the review and the record, one of them a commit
# reading `docs: round 1's paragraph is recorded before the round runs`.
#
# So the difference is evidence and not a verdict. `new` cannot tell a fix
# commit from a round paragraph, the numbers say it would be wrong about one
# correct run in four, and the orchestrator reading the subjects can tell them
# apart at a glance. What `new` owes the orchestrator is the list.
HEAD_MOVED = "the commit this round read is not the branch's HEAD"


def written_late_cell(given):
    """The `Written late` cell: `no`, or `yes {DASH} <why>` from the flag.

    `--written-late` carries the REASON and not the cell, so the vocabulary
    belongs here and a caller cannot half-write it. The value is stripped of
    the separators `yes` would be joined by, so a reason typed with the dash
    already in front of it does not land with two.

    An empty reason is refused, in the shape `nobody {DASH} <why>` and
    `unknown {DASH} <why>` are already refused in: a bare `yes` says a record
    was written late and says nothing a reader can act on, and this row's whole
    purpose is that the pull request stops refusing the record on the strength
    of it. A relaxation bought with an empty cell is a waiver with no author.
    """
    if given is None:
        return chain.FLOOR_NO
    reason = given.strip().strip(chain.SEPARATORS).strip()
    if not reason:
        raise Refused(
            f"--written-late {given!r} carries no reason. The cell is what "
            f"makes the pull request print `{WRITTEN_LATE}` instead of "
            "refusing this record, so a reader has to be told WHY it was "
            "committed after the fixes it commissions — the fix pass was "
            "spawned before the record was committed, HEAD moved mid-review, "
            f"whatever happened. The shape is `{chain.FLOOR_YES} {DASH} <why>` "
            f"and the flag carries the `<why>`, the way `{chain.NOBODY} "
            f"{DASH} <why>` already asks for one"
        )
    return f"{chain.FLOOR_YES} {DASH} {reason}"


def head_moved(root, target):
    """(reviewed, head, [`<abbrev> <subject>`]) when HEAD is not `target`.

    None when they are the same commit. `reviewed` is the RESOLVED target and
    not the string `--target` carried: the flag legitimately takes a branch
    name or a `HEAD~1`, and a line reading *the round read HEAD~1* names
    nothing anybody can open a week later.

    `<target>..HEAD` rather than a count, because the orchestrator's whole
    judgment here is which KIND of commit landed: a fix pass and a round
    paragraph are one line apart in this listing and indistinguishable in a
    number. A target that is not an ancestor of HEAD still answers -- the
    listing is what HEAD reaches and the target does not -- and that is the
    honest answer for a branch somebody reset sideways.

    It is NOT the honest answer for a tree that is simply BEHIND the target.
    The listing is empty there while the two commits still differ, so this
    returns an empty third element rather than None, and `head_moved_line`
    answers that state on a branch of its own. Printing the ordinary line
    would offer a count of nothing and two readings that are both false.

    None where git will not answer. `build` has already refused a `--target`
    that does not resolve, so the only way here is a repository `rev-parse
    HEAD` fails on, and a line about a tree this cannot read would name a
    cause that is not the cause.
    """
    head = git(root, "rev-parse", "HEAD")
    reviewed = git(root, "rev-parse", f"{target}^{{commit}}")
    if head is None or reviewed is None:
        return None
    head, reviewed = head.strip(), reviewed.strip()
    if not head or not reviewed or head == reviewed:
        return None
    listed = git(root, "log", "--format=%h %s", f"{reviewed}..{head}") or ""
    return reviewed, head, [ln.strip() for ln in listed.splitlines() if ln.strip()]


def head_moved_line(reviewed, head, between):
    """The line `new` prints when the two differ. Read by a person, so
    `agent-contract` §14 pins every sentence of it in a case."""
    if not between:
        # HEAD reaches nothing the reviewed commit does not, and the two are
        # still different commits: HEAD is BEHIND the record's own target, or
        # sits on another branch entirely. Neither reading below describes
        # that, and printing them would send the reader to a repair for a
        # state they are not in -- `--written-late` above all, which writes a
        # reason into a record nothing is late about.
        return (
            f"round-record: {HEAD_MOVED} {DASH} the round read {reviewed[:7]}, "
            f"HEAD is {head[:7]}, and HEAD reaches no commit the round did "
            "not.\n"
            "  So nothing landed after the review on THIS tree: HEAD is "
            "behind the commit this record names, or on another branch. "
            "Neither of the usual two readings applies.\n"
            "  Check that `--target` names the commit this tree's HEAD stood "
            "at when the round ran, and that you are in the tree the round "
            "reviewed. Nothing is refused here, and the record is written."
        )
    count = len(between)
    listing = "".join(f"\n    {line}" for line in between)
    return (
        f"round-record: {HEAD_MOVED} {DASH} the round read {reviewed[:7]}, HEAD "
        f"is {head[:7]}, and {count} commit{'' if count == 1 else 's'} "
        f"{'stands' if count == 1 else 'stand'} between them.{listing}\n"
        "  There are two readings and only you can tell them apart. Either "
        "the fix pass for this round has already run, in which case this "
        "record is being written after the work it commissions, and the pull "
        "request refuses it on a line no later commit can clear. Or HEAD "
        "moved during the review, which `templates/sdd-round.md` already asks "
        f"`{chain.TARGET}` to hold {DASH} both commits in that one cell.\n"
        "  Nothing is refused here. Measured over this repository's own "
        "pre-squash branches, 40 records of 152 differ this way, and the "
        "commonest cause by far is the round's own paperwork committed "
        "between the review and the record. Read the subjects above and "
        "decide.\n"
        f'  Where the first reading is the true one, `--written-late "<why>"` '
        f"writes the reason into the record's `{WRITTEN_LATE}` row, and the "
        "pull request prints it instead of refusing the record on a line no "
        "later commit can clear."
    )


# --- the bound the next round is under, said as the record is written -------

ENDS_THE_RUN = "this record ends the run"
ONE_REOPENING = "one reopening remains"


def floor_and_fixes(reader, earlier):
    """(the floor record, the later ones that closed on a fix, how many
    records the FIRING count walk has spent, whether that walk is still
    running, the record it started from).

    The last three are one answer in three cells and never disagree: with no
    walk firing the count is 0 and the record is None, because a count
    reported from a walk would be a number about a record the caller is not
    told. A walk FIRES two ways. Still running with one record spent, it
    counts the record being written as the gate's second; stopped with two
    or more spent, it is an error the gate already returns at the record it
    started from (#218) — and a walk that stopped at one bounds nothing.

    **`chain_check.stopping_floor` runs TWO walks over the records after the
    floor, and this used to carry one of them.** The reopening walk counts
    fix-closing records wherever they sit and refuses a second; the count walk
    counts every later record up to and including the first that reopened
    (`Needs a fix: yes — <what>`) or closed on a fix, and refuses a second counted
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
        # Through the gate's own reader of the reopening question rather
        # than a `== FLOOR_YES` of this line's own (#138): a bare `yes` is
        # no reopening there, so it is none here, and the printed bound and
        # the gate cannot be made to disagree by one cell — #218's class.
        reopened = needs is not None and (
            chain.says_reopened(reader.visible(needs).strip()) is True
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
    #
    # A RUNNING walk counts this record next, so one record already reaches
    # the gate's two. A STOPPED walk bounds nothing further — unless it
    # already reached two, which is an error `stopping_floor` returns at
    # `path` right now, before this record exists (#218). Reading only the
    # running walks printed `one reopening remains` at round 4 over a floor
    # record the gate was refusing, one round after it had printed `ends the
    # run` at round 3: the most permissive of the three sentences, after the
    # strictest, on a branch that could not pass its own gate. `running` is
    # what tells the two apart for `bound_line`, and the inner `break` is
    # what makes a stopped walk's count the gate's — without it every record
    # after the stop would be counted too (the ticket's ninth mutation
    # survivor, which this reading closes).
    counted, counted_at, running = 0, None, False
    for i, (path, met, _r, _w) in enumerate(seen):
        if not met:
            continue
        spent, stopped = 0, False
        for _p, _m, reopened, wrote in seen[i + 1 :]:
            spent += 1
            if reopened or wrote:
                stopped = True
                break
        fires = spent > 1 if stopped else spent >= 1
        if fires and spent > counted:
            counted, counted_at, running = spent, path, not stopped
    return seen[floor_i][0], fixes, counted, running, counted_at


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
    if counted_at is not None:
        if count_excused:
            return None
        # The record the FIRING walk started from, which is not always the
        # earliest floor record `met` names (round 2, 🟡 1). Naming `met`
        # here sent the reader to a walk that had already stopped, and the
        # count beside it then belonged to a record the sentence did not
        # mention — the one thing in this line a reader can check.
        started = os.path.basename(counted_at)
        if not running or counted > 1:
            # A walk that already reached two — STOPPED there, or still
            # running past it: the gate returns an error at `started` right
            # now, whatever this record says, and the line reports the
            # gate's own refusal rather than the most permissive sentence it
            # has (#218). Falling through to the reopening walk printed `one
            # reopening remains` for the stopped walk, and the running walk
            # of two printed `reaches 3 here`, a count the gate never says
            # (round 1's ⬜ 5 of the work item that fixed #218).
            return (
                f"round-record: {ENDS_THE_RUN} — the gate already returns an "
                f"error at {started}, whose count of round records after the "
                f"floor reached {counted} before this record exists. "
                f"{chain.CAPPED_EXIT}"
            )
        # One record after some floor record was quiet, so that walk is
        # still running and this record is the one it counts next — the
        # gate's SECOND counted record, which it refuses.
        return (
            f"round-record: {ENDS_THE_RUN} — {started} met the floor and the "
            "record after it neither reopened the run nor closed on a fix, "
            "so the gate's count of round records after the floor reaches 2 "
            f"here. {chain.CAPPED_EXIT}"
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
    # The commit the flag names, not the flag: `HEAD~1` and a branch name are
    # legitimate spellings at the keyboard and name nothing in a record —
    # `chain_check.target_shas` reads the cell for SHA-shaped words and
    # reported *no row naming a commit* over a cell that held the revision
    # as typed (#382). `head_moved` resolves the same flag for its printed
    # line, so the line and the cell now agree.
    target = reader.commit_of(root, args.target)
    if target is None:
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

    # The report's own verdict table, keyed the way `close` will key it. Two
    # things come out of reading it here rather than reading the copy:
    #
    # 1. A malformed id is refused where the AUTHOR is. `copied_row` validated
    #    nothing, so a numbering the reviewer chose surfaced two commands
    #    later, at `close`, one hop from either agent that could have avoided
    #    it (#321's answer 1).
    # 2. A row that commissions nothing is left out of `Pass` and out of
    #    `landing_values`, which is what keeps the two subcommands agreeing.
    #    Counted as a verdict, `✅ | … | verified |` reads OPEN — `verified`
    #    is in no vocabulary — so `new` would tick no box for a round that
    #    opened nothing, and `close` would tick one. The two halves refusing
    #    each other is the defect, not a spelling of it.
    keyed = verdict_rows(reader, lines)
    words = [
        chain.verdict_of([reader.visible(c) for c in cells], VERDICT_COL)
        for _i, cells in keyed.values()
    ]
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
        cell(chain.TARGET, target),
        cell(WRITTEN_LATE, written_late_cell(args.written_late)),
        cell(chain.RAN_BY, args.ran_by),
        cell(chain.PR_FIELD, pull_request_cell(root, args.pr)),
        cell(BROAD_GATE, args.broad_gate if args.broad_gate else GATE_NOT_YET),
        cell(chain.CHECKED_BY, checker),
        # The same pending value the two surface rows take, for the same
        # reason: a record is committed before its fixes exist, so the range
        # they were measured over does not exist either when `new` runs.
        # `close` replaces it with the resolved ends and their count.
        cell(chain.FIX_RANGE, surface),
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
    # `seal` names no round — it finds the last one — so it has no `--round`.
    if getattr(args, "round", 1) < 1:
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
    # Beside the `wrote` line, because it is a fact about the record just
    # written and about the `--target` it was written from. The reach-back and
    # the bound below are about OTHER records.
    moved = head_moved(root, args.target)
    if moved is not None:
        print(head_moved_line(*moved))
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
# One spelling, held in the checker because the checker reads it too (#427):
# this generator writes the prefix and `chain_check` names a cell carrying two.
FIXED_AT = chain.CLOSE_PREFIX
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
# What tells a row that names NO finding apart from a row that names one
# badly. A cell carrying a digit was reaching for an id and missed -- `R2-1`,
# `1-1`, `1b` -- and is refused. A cell carrying none is admitted unless it is
# empty or its severity owes an answer (`OWED_MARKERS` below).
#
# The corpus split is 199 carrying digits to 51 carrying none, and the 51 are
# NOT one population -- which is the opposite of what this comment said for a
# release. Re-derived through the module's own `table_body` over the same 207
# records: 44 of the 51 are a severity marker and a single LETTER, `🔴 A`
# through `🟢 O`, which is an id written in the wrong alphabet; and every one
# of the 44 predates `round_record.py` (2026-09-02/03 against the generator's
# 2026-09-05), so they are hand-written records from before a generator read
# the column at all. Seven are the shape this rule is for: `carried` twice,
# `🟢 fix-surface` twice, `🟢 fragment`, `🟢 grep`, `🟢 overview`. Neither `✅`
# nor a bare em dash occurs in a committed record -- the 21 bare em dashes are
# in reviewers' REPORTS, a different corpus. Zero cells are empty.
#
# So the evidence for admitting a no-digit cell is 7 rows, not 51, and the
# dominant no-digit shape is a finding id. That is why the rule reads the
# severity as well: it is 44 rows of a mistake this admission would otherwise
# make silent.
DIGIT_RE = re.compile(r"\d")
# The two severities that mean somebody owes this row an answer, per
# `skills/code-review/SKILL.md`'s scheme: 🔴 blocks merge, 🟡 needs grounds.
# 🟢, ❓ and ⬜ commission nothing by definition, which is why they are absent.
#
# A no-digit cell carrying one of these two was an id in the wrong alphabet
# rather than a row that commissions nothing, and the corpus says so without a
# margin: all 26 such rows are genuine findings -- 11 later closed `fixed`, 4
# `answered`, 11 still `open` -- and none of the 25 carrying 🟢, ❓ or no marker
# is. A VOCABULARY test of the verdict cannot do this job: a confirmation
# reads `verified`, which is in no vocabulary and therefore OPEN, so reading
# the verdict as OPEN/CLOSED would trade one refusal for another. Reading the
# one word `open` is the narrower thing `OPEN_WORD` below does.
OWED_MARKERS = ("\N{LARGE RED CIRCLE}", "\N{LARGE YELLOW CIRCLE}")
# The one verdict word that says the row is open in as many letters. Read only
# on a row whose `#` cell has already admitted it, where the two cells then
# contradict each other -- and one WORD rather than a vocabulary test, which
# is the distinction the grounds for NOT reading the verdict missed.
# `verified` is in no vocabulary and therefore OPEN, so reading the verdict as
# OPEN/CLOSED would refuse every confirmation; reading this one word refuses
# none of them. `says_open` below is where the word ends (round 2's 🟡 7).
OPEN_WORD = "open"
# The boundary `verdict_of` ends its own vocabulary on -- `fixed d3fe44d` and
# `fixed, d3fe44d` are both `fixed`. Spelled here rather than reached for in
# `chain.SEPARATORS`, which is six characters wide and has five other readers:
# borrowing it made `open-ended question` and `open: see 5` read as the open
# verdict, and tied what counts as open to a constant the `deferred` home
# reader is free to widen.
OPEN_BOUNDARY = (" ", ",")


def says_open(word):
    """`word` is the open verdict, however the reviewer ended it.

    The grounds for not running a VOCABULARY test hold and are untouched:
    `verified` is in no vocabulary and would be refused, which costs every
    confirmation row the `#` cell admits. What never followed from those
    grounds is EQUALITY. `verdict_of` ends a vocabulary word on a space or a
    comma — that is what makes `fixed d3fe44d` read as `fixed` — and the same
    boundary here reaches `open — deferred` and `open, comment only`
    (round 3's 🟡 2).

    **Measured 2026-09-15 over the committed `round-N.md` records that parse**
    — 211 of the 212 this repository carries, 2,044 verdict rows, none of them
    short — read through this module's own `table_body` and through
    `chain.verdict_of`: **123 verdict cells begin `open` and 9 of them
    continue**, so equality reached 114 of 123. Every one of the 9 continues
    with a space or a comma, so `says_open` reaches all 123; none of them is in
    `CLOSED_WORDS`. Of the 25 no-digit cells the `#` rule admits, 15 carry a
    verdict outside `CLOSED_WORDS` — the grounds against a vocabulary test,
    re-derived in the same pass — and **0** are newly refused by this arm.

    The population, the date and the reader are stated because the figure that
    stood here before was none of those things and did not reproduce under any
    of the six populations round 4 tried.

    The boundary is spelled out in `OPEN_BOUNDARY` rather than borrowed from
    `chain.SEPARATORS`. The wider set reaches `open-ended question` and
    `open: see 5`, and the refusal a reviewer then reads names a word the
    cell does not carry — the over-reach `verdict_of` names one function
    above, where dropping the boundary would let `not a defect` swallow `not
    a defective reading` (round 4's 🟡 2).
    """
    if not word.startswith(OPEN_WORD):
        return False
    rest = word[len(OPEN_WORD) :]
    return not rest or rest[0] in OPEN_BOUNDARY


BARE_ID = "a bare integer"
# Which of the two tables a refusal is about. The reviewer writes one and the
# fixer copies the numbering into the other, so a message naming the format
# and not the file sends the reader to the table that is already correct.
RECORD_LABEL = "verdict table"
FIX_TABLE_LABEL = "fix table"
DEPTH_EXIT = "deferred with a named answerer, or becomes an issue"


def finding_number(label, seen, line, taken, bad, idless, owed):
    """The finding one `#` cell names, `None` for a row that names none, or
    `Refused` for a duplicate.

    Four readings of the cell, and the third is #321's:

      digits behind an optional marker   the finding, keyed
      no digit, and the cell says the    `None` where `idless` is on — a row
      row commissions nothing            that commissions nothing, admitted
                                         and left exactly as it was written
      no digit, and the cell is empty    appended to `owed`: the caller
      or its severity owes an answer     refuses
      anything else                      appended to `bad`, and so is a
                                         no-digit cell where `idless` is off

    **A row that commissions nothing is a shape reviewers reach for**, and the
    evidence for it is seven rows rather than the fifty-one this said for a
    release. Measured 2026-09-14 over the 207 committed records that parse, 51
    of 1,989 verdict rows carry a `#` cell with no digit — and 44 of those are
    a severity marker and a single LETTER, which is a finding id in the wrong
    alphabet. Seven are the shape this admits: `carried`, `🟢 fix-surface`,
    `🟢 fragment`, `🟢 grep`, `🟢 overview`. Three tickets are that shape: a
    confirmation the round verified and did not open (#321), an earlier
    round's closure carried into this round's table (#341), and a `❓ out of
    verified scope` marker (#353). None can be referenced by a fix table,
    because there is nothing to commission.

    **Which is why the severity is read as well.** A `#` cell alone cannot say
    whether anything is owed, and admitting a row on its strength ticked
    `Pass` over an open finding — the record asserting that a review passed
    while its own table said otherwise, which is the defect this whole work
    item is named for, reproduced inside its own fix (round 1's 🔴 1). The
    marker already carries that meaning: 🔴 blocks merge, 🟡 needs grounds, and
    all 26 no-digit cells carrying one are genuine findings. An empty cell is
    refused for the neighbouring reason — it says nothing at all, which is
    what a reviewer who forgot the id writes, and no committed record has one.

    A vocabulary test of the verdict cannot serve here: a confirmation reads
    `verified`, which is in no vocabulary and therefore OPEN, so reading the
    verdict as OPEN/CLOSED would trade one refusal for another. Reading the one
    word `open` does not, and `says_open` above is that arm.

    `idless` is off for the fix table, where the row IS the commission: a fix
    row naming no finding has nothing to apply itself to.

    **`bad` is a list rather than a raise.** #303, merged into #321, measured
    five offending rows against a message naming one, at two round trips per
    repair. The caller refuses once, with all of them. `owed` is a second list
    for the same reason and refuses separately, because the two say different
    things to the reviewer. The duplicate refusal stays immediate because it
    already quotes both of its rows, and `taken` is {number: the row that
    already claimed it} so that it can.

    **The `#` cell is not the only cell that says a row owes an answer**, which
    is why `verdict_rows` reads the Verdict cell beside it. Reading the marker
    alone admitted six shapes whose Verdict cell said `open` — three of them
    carrying no marker at all, so the residual stated here for a round did not
    describe them (round 2's 🟡 7). It matches the WORD — `says_open` ends it
    on a space or a comma, the boundary `verdict_of` uses for its own
    vocabulary — rather than a vocabulary, and that is what makes it free:
    `verified` is in no vocabulary and therefore OPEN, so refusing everything
    outside `CLOSED_WORDS` would refuse every confirmation row.

    What this still gives up, stated rather than left to be found: a row takes
    TWO mistakes in two cells to slip through now — 🟢, ❓ or ⬜ on a row that
    IS an open finding, AND a verdict worded as something other than `open`.
    Such a row writes a finding no fix table will be asked to close, and
    `close` exits 0 over it. The cheaper mistake is the other one, where
    numbering a confirmation row costs an inflated count in one record.
    """
    text = chain.EMPHASIS.sub("", seen).strip()
    m = FINDING_ID_RE.match(text)
    if not m:
        if idless and not DIGIT_RE.search(text):
            # Admitted only where the cell SAYS the row commissions nothing.
            # An empty cell says nothing at all, and a severity that owes an
            # answer says the opposite; either way the caller refuses, because
            # a row admitted here is never keyed, never asked for a closure
            # and never counted toward `Pass` — so `Pass` would be ticked
            # over an open finding, which is a record asserting that a review
            # passed while its own table says otherwise.
            if not text or any(marker in text for marker in OWED_MARKERS):
                owed.append((text, line))
            return None
        bad.append((text, line))
        return None
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


def id_refusal(label, bad):
    """`Refused` naming the format and quoting every offending row, or None.

    One message for the whole table. The explanation is written once and the
    rows are listed under it, so a reviewer repairing five of them reads the
    rule once and opens the table once.
    """
    if not bad:
        return None
    many = "s" if len(bad) > 1 else ""
    rows = "\n".join(f"    {text!r}: {line.strip()}" for text, line in bad)
    return Refused(
        f"the {label} has {len(bad)} row{many} whose `#` cell is not {BARE_ID} "
        "— an optional severity marker, then digits and nothing else (`1`, "
        "`\N{LARGE RED CIRCLE} 2`, `\N{WHITE LARGE SQUARE} 13`). A "
        "round-prefixed id collapses toward one key: `R2-1` and `R2-2` are the "
        "same digits to a reader that takes the first run, which is how eight "
        "findings became one. Number this round's findings 1..N and let the "
        "record's own file name carry the round. A verdict row that commissions "
        "nothing — a confirmation, an earlier round's closure, a scope marker — "
        "carries no id at all and is left as written; what is refused here is a "
        f"cell that names something else.\nThe row{many}:\n{rows}"
    )


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


# A range end has to be a COMMIT somebody can open, which is narrower than a
# ref that resolves (#344). `HEAD`, `@`, a branch and a tag all resolve, and
# all four name something different tomorrow -- so a record stating one is a
# sentence that stays readable while meaning a different set of commits every
# day. Three instances in one work item is what made it a ticket.
#
# Hex, seven to forty characters, AND resolving to a commit it is a prefix of.
# The second half is what makes the first one true: a branch named `abcdefg`
# is hex-shaped, and it passes this only if it happens to point at a commit
# whose sha starts with its own name. That coincidence is recorded rather than
# parsed away -- refusing hex-shaped ref NAMES would mean asking git which
# refs exist, and the check would then pass or fail on what somebody else had
# created.
PINNED_RE = re.compile(r"^[0-9a-fA-F]{7,40}$")


def parse_range(root, value):
    """(a, b) as full commits from `<a>..<b>`, or `Refused`.

    BOTH ends, not only the second. `HEAD` is the end #344 measured and a
    branch name at the start moves exactly as far; a rule aimed at the word
    that happened to be reported closes the instance and not the class (§12).
    """
    a, dots, b = value.partition("..")
    a, b = a.strip(), b.strip()
    if not dots or not a or not b or b.startswith("."):
        raise Refused(f"--range {value!r} is not `<a>..<b>`")
    out = []
    for ref in (a, b):
        full = chain.resolves_to(root, ref)
        if full is None:
            raise Refused(f"--range names `{ref}`, which does not resolve in {root}")
        if not PINNED_RE.match(ref) or not full.startswith(ref.lower()):
            raise Refused(
                f"--range names `{ref}`, which resolves today and is not a "
                f"commit anybody can open tomorrow. A record states its fix "
                f"range as commits, and `{ref}` is a name that moves: this "
                f"same record would mean a different set of commits every "
                f"time the branch does. Write the commit instead — "
                f"`git -C {root} rev-parse {ref}` gives `{full[:8]}`, so "
                f"`--range "
                + (f"{full[:8]}..{b}" if ref == a else f"{a}..{full[:8]}")
                + "`. No cell was written"
            )
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
    # The rider that stood here is spent: it asked for the empty-span repair
    # and the `note` line below now cuts the commit's own code span, where it
    # used to cut the hex alone. It was right that the repair belongs here and
    # not in `chain.SEPARATORS` -- that constant is read by the `deferred`
    # home below and by `chain_check`'s own readers -- and its stated REASON
    # did not hold at this site: `chain.EMPHASIS` is ``[*_`]+`` and runs over
    # the verdict cell one line before `SEPARATORS` is reached, so a home
    # written as a code span already arrives with its backticks gone
    # (measured 2026-09-14). The other two callers are still a real cost and
    # nothing has measured them, so the constant is left alone.
    text = read_text(path, "fix table")
    raw, lines = text.splitlines(), reader.readable(text)
    out, taken, bad, keyed = {}, {}, [], []
    # Two passes, so the id refusal names every offending row before a verdict
    # word on some other row can refuse first. `idless` is off here: in this
    # table the row IS the commission, and one naming no finding has nothing
    # to apply itself to.
    for i, cells in table_body(reader, lines, FIXES, FIXES_HEADER, True):
        seen = [reader.visible(c) for c in cells]
        if len(seen) < len(FIXES_HEADER):
            raise Refused(f"a fix row has {len(seen)} cells: {raw[i].strip()!r}")
        number = finding_number(FIX_TABLE_LABEL, seen[0], raw[i], taken, bad, False, [])
        if number is not None:
            keyed.append((number, seen))
    refusal = id_refusal(FIX_TABLE_LABEL, bad)
    if refusal is not None:
        raise refusal
    for number, seen in keyed:
        verdict = chain.EMPHASIS.sub("", seen[1]).strip().rstrip(".").strip()
        word, third = verdict.lower(), seen[2].strip()
        if word == FIXED:
            sha = chain.SHA_RE.search(third)
            if not sha:
                raise Refused(
                    f"finding {number} is `{FIXED}` and its third cell names no "
                    f"commit: {third!r}. A fix is a commit somebody can open"
                )
            # Cut the commit's own code span, not just the commit. Cutting
            # the hex alone left both backticks standing with nothing between
            # them, so `` `e7d3447` — widened `` landed as `fixed at e7d3447
            # — `` — widened`: an empty code span beside the commit, on 210
            # of this repository's committed verdict rows (#391 part 2,
            # measured 2026-09-14). Widened HERE and not in
            # `chain.SEPARATORS`, which the `deferred` home reader below and
            # `chain_check`'s own readers share.
            # `chain.SEPARATORS` is six characters wide and holds no period, so a cell
            # opening `` `6233b769`. `` left the stop behind and the row
            # rendered `fixed at 6233b769 — . <note>` (#414). Nine such cells
            # were repaired BY HAND once and the next record the generator
            # wrote carried the rendering again, which is §12's rule as a
            # measurement: the fix is owed to the cause, not to the cells.
            # The period is added HERE for the reason the paragraph above
            # gives -- five readers share the constant, and a trailing period
            # in a `deferred` home or in a `nobody — <why>` reason is part of
            # a sentence rather than decoration.
            start, end = sha.start(), sha.end()
            if start and third[start - 1] == "`" and third[end : end + 1] == "`":
                start, end = start - 1, end + 1
            note = (third[:start] + third[end:]).strip(chain.SEPARATORS + ".")
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
            # The third cell is the fix pass's reasoning — why the finding
            # could not be closed on the branch, what it measured, what a
            # reader should open — and it was discarded whenever the verdict
            # cell carried the home. A deferred finding is the one verdict
            # whose reasoning is the whole of its value, because nothing else
            # in the tree will explain why it left (#391 part 1). Empty when
            # the home came out of this cell, so a `| N | deferred | #12 |`
            # row does not say `#12` twice.
            # The home comes off the FRONT of the note rather than being
            # compared with the whole of it. An equality test caught
            # `| N | deferred #12 | #12 |` and missed the shape immediately
            # beside it -- #391's own worked example,
            # `| N | deferred #309 | #309 -- the parity arm is out of scope |`,
            # which printed `#309 -- #309 -- the parity arm ...`: a smaller
            # version of the same noise in the cell #391 exists to make
            # readable (round 1's finding 4).
            # The SECOND member of #414's class, and the one its own report
            # did not name. This cut is the same shape as the commit span's
            # above -- a span chosen by the generator taken off the front of a
            # cell somebody wrote -- so a third cell reading `#309. the parity
            # arm is out of scope` left the stop behind and the row rendered
            # `#309 — . the parity arm is out of scope`. Executed 2026-09-15
            # through this function before the widening. Enumerated rather
            # than assumed: the module's three other `chain.SEPARATORS` strips
            # read a whole cell, or a remainder whose first character the arm
            # above it already tested to be a separator, so none of them can
            # leave a stop behind.
            rest = third[len(home) :] if third.startswith(home) else third
            out[number] = (DEFERRED_WORD, home, rest.strip(chain.SEPARATORS + "."))
        elif any(
            word.startswith(w) and word[len(w)] in chain.SEPARATORS
            for w in (FIXED, ANSWERED)
        ):
            # The cell BEGINS with a word this table admits and carries a
            # suffix, which is one cell doing two cells' work.
            # `docs/review-chain-spec.md` prescribed exactly that for a
            # correction — `answered — corrected at <sha>` — for as long as
            # `agents/smith.md` prescribed the two-cell shape beside it, so a
            # reader who followed the spec met a message listing three words
            # and had to work out that their cell had begun with one of them
            # (#341's comment). `deferred <home>` is the one word that
            # legitimately carries a suffix and is handled above.
            # `head` is the word the arm matched on, taken from the arm's
            # own test rather than by splitting the cell. `SEPARATORS`
            # begins with a space, so splitting on the first of its
            # characters found ANYWHERE in the cell gave `answered,` for
            # `answered, corrected at <sha>` -- and the paste-ready row the
            # message then printed carried `answered,` as its verdict,
            # which this table refuses on the next run. Every separator
            # that touches the word was wrong this way, not the comma
            # alone; the em-dash spelling the documents name worked only
            # because a space follows the word there (round 1's finding 3).
            head = next(
                w
                for w in (FIXED, ANSWERED)
                if word.startswith(w) and word[len(w)] in chain.SEPARATORS
            )
            raise Refused(
                f"finding {number}'s verdict `{seen[1]}` begins with `{head}` "
                f"and then carries more. The Verdict cell holds the word alone "
                f"and everything after it goes in `{FIXES_HEADER[2]}`: write "
                f"`| {number} | {head} | {verdict[len(head) :].strip(chain.SEPARATORS)} |`. "
                f"Only `{DEFERRED_WORD} <home>` carries its own suffix, because "
                "the home is what makes a deferral readable"
            )
        else:
            raise Refused(
                f"finding {number}'s verdict `{seen[1]}` is none of `{FIXED}`, "
                f"`{ANSWERED}`, `{DEFERRED_WORD} <home>` — the three a fix pass "
                "may hand over. A reviewer's words (`withdrawn`, `not a "
                "defect`) are the reviewer's to write"
            )
    return out


def verdict_rows(reader, lines):
    """{finding number: (index, cells)} for the verdict table in `lines`.

    A row whose `#` cell names no finding is absent from the mapping, which
    is the whole of what a row that commissions nothing costs downstream:
    `close` never asks a fix table for it, never writes a verdict word over
    it, and never counts it toward `Pass`.

    Read from the RECORD on the `close` path and from the REPORT on the `new`
    path. The two tables carry the same heading under the same header — that
    is what lets `table_of` copy one into the other — so the ids a reviewer
    chose are refused where the reviewer is rather than two commands later at
    the orchestrator (#321's answer 1, which composes with answer 2 above
    rather than replacing it).
    """
    out, taken, bad, owed = {}, {}, [], []
    for i, cells in table_body(reader, lines, VERDICTS, VERDICT_HEADER, True):
        seen = [reader.visible(c) for c in cells]
        if len(seen) <= VERDICT_COL:
            # A digit in the `#` cell KEYS the row, so a row with no Verdict
            # cell passed here and reached every caller that indexes
            # `VERDICT_COL` by position -- `build`'s `words`, `close`'s
            # `open_now`, its `already` message and its write pass -- as an
            # IndexError rather than a refusal naming the row. A REGRESSION:
            # before the verdict arm landed, `new` computed `Pass` through
            # `verdict_words`, which raised `a verdict row has N cells`
            # (round 3's 🔴 1).
            #
            # The bound is `VERDICT_COL` and not the header width, which is
            # what round 3's paste-ready code proposed. The wider test refuses
            # a row that is merely missing `Grounds` — four cells, a verdict
            # present, nothing that crashes — and that shape is deliberately
            # ADMITTED and written short rather than padded, so the record
            # shows the column the reviewer left out instead of inventing one
            # (`test_a_short_row_with_a_comment_pipe_is_not_padded_into_a_full_one`,
            # which the wider test turns red). Refusing exactly what crashes
            # leaves that decision standing. Free either way against the
            # corpus: zero of the 2,044 committed verdict rows are short at
            # all (2026-09-15, through `table_body`).
            #
            # This raises on the FIRST offending row where `bad` and `owed`
            # below collect every one and refuse once -- #303's shape, two
            # round trips per repair. It is left an immediate raise
            # deliberately (round 4's ⬜ 5): the guard was already immediate
            # before the verdict arm and only its condition widened, and with
            # zero committed rows short the cost falls on a reviewer's first
            # draft and nowhere else. Making it a list is the repair if
            # anybody opens this function again for another reason.
            raise Refused(
                f"a verdict row has {len(seen)} cells, so it has no "
                f"`{chain.VERDICT_COLUMN}` cell at column {VERDICT_COL + 1}: "
                f"{lines[i].strip()!r}. Every reader downstream indexes that "
                "column by position, so a short row carrying a digit is keyed "
                "here and reaches them as a crash rather than as a refusal "
                "naming the row"
            )
        flagged = len(bad) + len(owed)
        number = finding_number(
            RECORD_LABEL, seen[NUMBER_COL], lines[i], taken, bad, True, owed
        )
        if number is not None:
            out[number] = (i, cells)
        elif len(bad) + len(owed) == flagged and says_open(
            chain.verdict_of(seen, VERDICT_COL)
        ):
            # The `#` cell says this row commissions nothing and the Verdict
            # cell says it is open, in as many letters. The marker arm catches
            # the reviewer who wrote the severity and forgot the id; this
            # catches the one who wrote a severity that owes nothing and then
            # said `open` anyway -- three of the six shapes it reaches carry
            # no marker at all, so the marker arm cannot see them. §12: round
            # 1's 🔴 1 named the class, and this is its third member.
            #
            # `flagged` is what keeps a row failing BOTH arms from being
            # quoted twice, which counted two rows where the table holds one.
            owed.append((seen[NUMBER_COL].strip(), lines[i]))
    refusal = id_refusal(RECORD_LABEL, bad)
    if refusal is not None:
        raise refusal
    if owed:
        many = "s" if len(owed) > 1 else ""
        rows = "\n".join(f"    {text!r}: {line.strip()}" for text, line in owed)
        raise Refused(
            f"the {RECORD_LABEL} has {len(owed)} row{many} that commissions "
            "nothing by its `#` cell and owes an answer by another cell: the "
            "`#` cell is empty, or carries a severity that owes an answer, or "
            f"the `{chain.VERDICT_COLUMN}` cell reads `{OPEN_WORD}`. "
            "\N{LARGE RED CIRCLE} blocks merge and \N{LARGE YELLOW CIRCLE} "
            "needs grounds, so both commission a fix-table row; an empty cell "
            "says nothing at all; and a row the record itself calls "
            f"`{OPEN_WORD}` is open whatever its `#` cell says — while a row "
            "with no id is never keyed, never asked for a closure and never "
            "counted toward `Pass`, so `Pass` would be ticked over an open "
            "finding. Number it, or write the severity and the verdict the "
            "row actually has (\N{LARGE GREEN CIRCLE}, "
            "\N{BLACK QUESTION MARK ORNAMENT}, "
            f"\N{WHITE LARGE SQUARE}).\nThe row{many}:\n{rows}"
        )
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
            # RIDER: `chain.EMPHASIS` is `[*_`]+` and it is applied to the
            # whole entry, so every underscore INSIDE a unit name is stripped
            # with the backticks around it -- `only_tested` is read back as
            # `onlytested`, and `added` names come from the AST unstripped, so
            # `unit not in named` is true for every snake_case parent. The
            # depth-2 walk below therefore reaches no Python unit whose name
            # carries an underscore, which is most of them. Measured
            # 2026-09-15 while building #333's cases: committed records write
            # entries like `` `test_a_cell_of_only_separators_is_not_an_answer` ``,
            # and this reads them as one long word. #30's own refusal fired
            # through `quote`, which has no underscore, and named `quote` as
            # the parent for units added by a fix inside a unit that does.
            # NOT REPAIRED HERE: it is outside work item 1789425391's six
            # tickets and it widens what the rule refuses, which is a change
            # to a gate. The repair is to strip the emphasis characters from
            # the ENDS of the entry rather than everywhere in it, and it needs
            # the corpus measured for records this newly reaches. The answerer
            # is the repository owner.
            # Verified 2026-09-15 against units_named_earlier@9165d624.
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


def unit_adders(reader, root, fixes):
    """{(path, unit): {finding number}} — which fix commit added each unit.

    A second `measure`, one per `fixed` commit, over that commit alone.
    `close` already resolves every `fixed` commit and places it inside the
    range; what it does not hold is WHICH of them introduced a given unit,
    because `measure` compares the range's TWO ENDS and nothing between
    them (`questions.md` Q5). That is what `depth_two` below needs to name a
    finding rather than a file.

    Bounded by the fix range, which is the reason the cost is affordable: a
    fix range is two or three commits, and each pass parses only the files
    that ONE commit touched rather than the range's whole surface.

    A commit with no parent contributes nothing — every unit in it is `added`
    against an empty tree, which is true and useless — and the walk falls
    back to the file-level answer for anything it cannot attribute.
    """
    adders = {}
    for number, (word, value, _note) in fixes.items():
        if word != FIXED:
            continue
        full = chain.resolves_to(root, value)
        parent = chain.resolves_to(root, f"{full}^") if full else None
        if parent is None:
            continue
        _c, added, _h, _at_a, _at_b = measure(
            reader, root, parent, full, touched(root, parent, full)
        )
        for rel, unit in added:
            adders.setdefault((rel, unit), set()).add(number)
    return adders


def depth_two(reader, root, a, rows, fixes, added, at_a, earlier, adders=None):
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

    **The finding is named from `adders`, not from the file** (#333). The
    walk used to compare the FILE — `inside = [n for r, n in added if r == f]`
    — so every unit added to a file was attributed to whichever candidate
    row the loop reached first. It fired correctly on #30 and named the wrong
    finding and the wrong enclosing unit, which is worse than firing wrongly:
    the reader is sent to a row that did not add the unit.

    **A unit whose adder resolves to no candidate row is at depth 1**, and
    this rule has nothing to say about it (round 1's 🟡 3). `unit_adders`
    resolves every `fixed` commit's units, including those added by findings
    that sit inside no unit an earlier record names; the walk took the
    file-level fallback on those and printed a non-resolution that had not
    happened. Resolving to SEVERAL candidate rows is a different state and
    still takes the fallback: it is a resolution that cannot say which fix
    added the unit.

    **Where the range cannot resolve one, it still refuses and says so.**
    A single commit answering two findings resolves to nothing at any cost,
    and the direction every verdict the checker cannot read takes is the one
    that blocks: `docs/review-chain-spec.md`'s own depth table fails an entry
    below depth 1 for the neighbouring reason, and the asymmetry is
    `CONTRIBUTING.md`'s — a wrong deny costs a prompt, and a wrong allow here
    ships a unit that is read by nobody. What changes on the fallback is the
    MESSAGE: it says the attribution is file-level and names every candidate
    finding rather than asserting one, because a per-file answer is
    structurally unable to state what `templates/sdd-round.md` requires per
    entry.
    """
    named = units_named_earlier(reader, earlier)
    if not named or not added:
        return
    # A PASS rather than its result, so the guard above runs first (round 1's
    # ⬜ 5). `unit_adders` is a second `measure`, one per `fixed` commit;
    # evaluated at the call site it was paid on every round-1 `close`, where
    # there are no earlier records at all and this returns at once --
    # `phases/phase-5.md` measured that pass at 127.8 ms.
    adders = adders() if callable(adders) else (adders or {})
    # {(file, unit added): {finding number: (parent unit, the record naming it)}}
    candidates = {}
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
                for name in [n for r, n in added if r == f]:
                    candidates.setdefault((f, name), {})[number] = (
                        unit,
                        named[unit],
                        reader.visible(cells[NUMBER_COL]),
                        reader.visible(location),
                    )
    if not candidates:
        return

    lines = []
    for (f, name), rows_for in candidates.items():
        resolved = set(adders.get((f, name), ()))
        owners = sorted(resolved & set(rows_for))
        if len(owners) == 1:
            unit, record_n, cell_text, location = rows_for[owners[0]]
            lines.append(
                f"`{name}` in {f} would be at depth 2: added by the fix of "
                f"{cell_text}, whose Location `{location}` is inside `{unit}`, "
                f"a unit round-{record_n}.md's `{chain.NEW_UNITS}` names."
            )
            continue
        if resolved and not owners:
            # The range DID resolve the adder, and to NO candidate row: the
            # fix that added this unit sits inside no unit an earlier record
            # names, so the unit is at depth 1 and this rule has nothing to
            # say about it -- #333's quiet direction, which the file-level
            # walk answered by refusing and the repair then answered by
            # printing a non-resolution that had not happened (round 1's
            # 🟡 3).
            #
            # `not owners` is what keeps this narrow, and the round's
            # paste-ready `if resolved` was not: one commit answering two
            # findings resolves to BOTH candidate rows, which is a resolution
            # that still cannot say which fix added the unit. That shape
            # takes the file-level sentence below, and skipping it turned
            # `test_a_depth_two_refusal_it_cannot_attribute_says_so_and_names_every_candidate`
            # red -- S12's own case.
            continue
        every = "; ".join(
            f"{cell_text} (inside `{unit}`, round-{record_n}.md)"
            for _n, (unit, record_n, cell_text, _loc) in sorted(rows_for.items())
        )
        lines.append(
            f"`{name}` in {f} would be at depth 2, and the attribution is "
            f"FILE-LEVEL: the range does not resolve which fix added it, so "
            f"every fix inside an earlier unit in {f} is a candidate — {every}."
        )
    if not lines:
        return
    raise Refused(
        "\n".join(lines) + " A fix pass may add a unit; that unit's fix may "
        "not, because the fix is read by the round that follows and the unit "
        f"it added is read by nobody. The unit is {DEPTH_EXIT}; no cell was "
        "written"
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
        # The parenthetical names the ids the verdict table DOES hold, so
        # an empty mapping rendered as `(which has )` and the reader learned
        # less than the sentence promised. Pre-existing; the admission rule
        # is what makes an empty mapping reachable from a well-formed report
        # (round 1's finding 5).
        held = ", ".join(map(str, sorted(rows))) or "no numbered rows at all"
        raise Refused(
            f"the fix table names finding{'s' if len(unknown) > 1 else ''} "
            f"{', '.join(map(str, unknown))}, not in round {args.round}'s verdict "
            f"table (which has {held})"
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
    depth_two(
        reader,
        root,
        a,
        rows,
        fixes,
        added,
        at_a,
        earlier,
        lambda: unit_adders(reader, root, fixes),
    )

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
    # Through the same path as `seal` (round 1's 🟡 1): a run the cell
    # already holds is kept behind the new entry by either writer.
    gate = (
        cell(
            BROAD_GATE,
            kept_broad_gate(reader, chain.table_rows(reader, lines), args.broad_gate),
        )
        if args.broad_gate
        else None
    )
    # The range this pass was measured over, as commits and as a count (#344).
    # `parse_range` has already refused an end that is not a commit somebody
    # can open, so both halves here are pinned by construction -- and the
    # count is derived from them rather than typed, which is the half a reader
    # can check against the tree without opening anything.
    counted = git(root, "rev-list", "--count", f"{a}..{b}")
    # `isdigit()` as well as `is None`, because `chain_check.fix_range` reads
    # the same command forty lines away and checks both, and two readings of
    # one command that disagree are the split this file spends its docstrings
    # closing (round 1's 8). Defensive either way: git answers a digit or
    # fails.
    if counted is None or not counted.strip().isdigit():
        raise Refused(
            f"git rev-list --count {a[:7]}..{b[:7]} failed in {root}, so the "
            f"`{chain.FIX_RANGE}` row cannot be derived. No cell was written"
        )
    spanned = int(counted.strip())
    fix_range = cell(
        chain.FIX_RANGE,
        f"`{a}..{b}`, {spanned} commit{'' if spanned == 1 else 's'}",
    )

    # Nothing above touched `raw`; everything below does, indices first and
    # the one insertion last.
    for number, (word, value, note) in fixes.items():
        i, _cells = rows[number]
        cells = row_cells(reader, raw[i], len(VERDICT_HEADER))
        while len(cells) <= GROUNDS_COL:
            cells.append("")
        # `old` is the REVIEWER's grounds — the reason the finding was opened.
        # A fix pass is not asked to change it; it is asked what it did about
        # the finding, and the two are different sentences by different
        # authors. All three words join rather than overwrite (§12: #391 names
        # the `deferred` row and the class is three wide). `fixed` was already
        # the only one of the three that preserved what stood.
        old = cells[GROUNDS_COL].strip()
        if word == FIXED:
            cells[VERDICT_COL] = f"**{FIXED}** `{value}`"
            grounds = f"{FIXED_AT} {value}" + (f" {DASH} {note}" if note else "")
        elif word == ANSWERED:
            cells[VERDICT_COL], grounds = ANSWERED, value
        else:
            cells[VERDICT_COL] = f"{DEFERRED_WORD} {value}"
            grounds = value + (f" {DASH} {note}" if note else "")
        # #427: `close` joined a cell it had already written, so re-closing a
        # corrected record carried the fix grounds twice and nothing said so.
        # The path is not a misuse a person can be told out of -- correcting a
        # record and re-closing it is the documented way out of a record
        # written wrong, and the repair that reached it restored the `Verdict`
        # cells from the reviewer's report and left `Grounds` alone, because
        # its author did not know this line prefixes.
        #
        # TWO arms, because one of them alone closes the instance and not the
        # class (§12). The first is the re-close with the SAME fix table, which
        # is what a corrected record produces and what #427 reproduced
        # byte-identically; it covers all three verdict words, because all
        # three reach this line and all three join. The second is the cell that
        # already carries a close-prefix naming a DIFFERENT commit -- a fix
        # pass that amended its commit between two closes, or a row reopened
        # and re-closed under another word -- which the first arm cannot see
        # because the text it would compare has changed.
        #
        # It REFUSES rather than overwriting, which is `questions.md` Q4
        # (#427 allows either). Overwriting discards the reviewer's sentence
        # silently, and not discarding it is what this whole join was written
        # for. Refusing costs the author one restore and tells them which half
        # of the record is still half-repaired.
        #
        # Nothing has reached disk when this raises: `write_record` runs after
        # this loop, so `raw`'s earlier rows are in memory only.
        if old and (old.startswith(grounds) or chain.CLOSE_PREFIX_RE.match(old)):
            raise Refused(
                f"finding {number}'s `Grounds` cell already carries a close "
                f"prefix -- {old[:60]!r} -- so this row was closed once "
                f"already and only its `{chain.VERDICT_COLUMN}` cell was "
                f"reopened. Writing it again would carry the fix grounds "
                f"twice, and a record that says a thing twice still parses, "
                f"so nobody would see it. Restore the `Grounds` cell to what "
                f"the reviewer wrote as well -- the round's report is where it "
                f"stands -- and run `close` again, or leave the row as it is. "
                f"No cell was written"
            )
        cells[GROUNDS_COL] = grounds + (f"; {old}" if old else "")
        raw[i] = row([escape(c) for c in cells])
    words = [
        chain.verdict_of(
            [reader.visible(c) for c in row_cells(reader, raw[i], len(VERDICT_HEADER))],
            VERDICT_COL,
        )
        for i, _ in rows.values()
    ]
    # The map the forward reach reads, built here for the same two reasons
    # `words` is: `raw` already carries the fix table, and no line has been
    # inserted into it yet, so the indices the record was parsed at are still
    # its own.
    #
    # EVERY verdict row, not only the numbered ones (round 1's 🔴 1).
    # `inherited_rows` writes one row per `Location` cell of every row -- a
    # confirmation, an earlier round's closure carried forward, an
    # `❓ out of verified scope` -- while `rows` holds only what
    # `finding_number` keyed. Keying this map from `rows` refused a pair of
    # records this generator itself wrote, at exit 2, and sent the reader to
    # correct a coordinate that was already right.
    #
    # FIRST row at a coordinate wins, which is how `inherited_rows` resolves
    # the same repeat -- it skips a `Location` it has already emitted. A plain
    # assignment here ended holding the LAST, so the two sides named different
    # rows of one record and the `Why` cell round N+1 carried came from a row
    # the section had attributed nothing to (#404). The two now agree BY
    # CONSTRUCTION rather than by both being right: whichever row a repeat
    # resolves to, both sides resolve to the same one, so there is no row left
    # for them to disagree about. Refusing the repeat instead was measured and
    # is foreclosed -- 71 of the 247 committed records that parse repeat a
    # `Location`, over 105 coordinates (2026-09-15), so a refusal would refuse
    # records this repository has already written.
    location = VERDICT_HEADER.index("Location")
    number = VERDICT_HEADER.index("#")
    now = {}
    for i, _cells in table_body(reader, lines, VERDICTS, VERDICT_HEADER, True):
        seen = [
            reader.visible(c) for c in row_cells(reader, raw[i], len(VERDICT_HEADER))
        ]
        if len(seen) > VERDICT_COL and seen[location]:
            now.setdefault(
                seen[location], (seen[number], chain.verdict_of(seen, VERDICT_COL))
            )
    still_open = [w for w in words if w not in chain.CLOSED_WORDS]
    # The same derivation `new` makes from the report's verdicts, over the
    # verdicts as the table left them. Both of its answers are written here,
    # and the second one used to be left alone:
    #
    #   `no fixes to check`   nothing closed on a fix word, so no fixes will
    #                         ever exist and *not yet written* would be false
    #                         the moment it was written
    #   `nobody -- <why>`     a fix word closed something, so the fixes exist
    #                         and no round has opened them. The landing value
    #                         says they are not yet WRITTEN, which was true
    #                         while the round ran and is false now: the
    #                         commits are in this record's own verdict cells,
    #                         two rows below (#273 part 1). A capped run's
    #                         last record keeps whatever stands here forever,
    #                         because there is no next `new` to correct it.
    #
    # Only the landing value is corrected. A cell naming a `round-N` is a
    # later round's reading and is not this pass's to touch.
    checker, _surface = landing_values(words)
    boxes = [i for i, ln in enumerate(lines) if chain.PASS_RE.match(ln)]
    if len(boxes) != 1:
        raise Refused(f"the record has {len(boxes)} `Pass` boxes and needs one")
    raw[boxes[0]] = f"- [{' ' if still_open else 'x'}] Pass"
    at = field_index(reader, lines, chain.CHECKED_BY)
    standing = row_cells(reader, raw[at], 2)
    standing = reader.visible(standing[1]).strip() if len(standing) > 1 else ""
    if checker != chain.NO_FIXES and standing == PENDING_CHECKER:
        checker = WRITTEN_CHECKER
    if checker in (chain.NO_FIXES, WRITTEN_CHECKER):
        raw[at] = cell(chain.CHECKED_BY, checker)
    # Round 1's 🟡 2. `field_index` refuses a record with no such row, and
    # its message names a count and no repair -- which is right for a label
    # every `new` has always written and wrong for the one label `new` began
    # writing this release. `chain_check` grandfathers those records behind
    # `RANGE_FROM`; the generator has no equivalent and should not grow one,
    # because `close` REPLACES a row rather than inserting one: a record's
    # field order is the template's, and a `close` that inserted would put the
    # row wherever it happened to look. So the refusal stands and says what to
    # add and where.
    try:
        at_range = field_index(reader, lines, chain.FIX_RANGE)
    except Refused:
        raise Refused(
            f"the record has no `| {chain.FIX_RANGE} | … |` row, so there is "
            f"nowhere to write the range this pass was measured over. It was "
            f"written by a `new` from before that row existed. `close` "
            f"replaces the row rather than inserting one, because a record's "
            f"field order is the template's — so add `| {chain.FIX_RANGE} | "
            f"{chain.NONE_WORD} |` under `| {chain.CHECKED_BY} | … |` and run "
            f"`close` again. No cell was written"
        ) from None
    raw[at_range] = fix_range
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

    # The forward reach is built BEFORE either write, so its refusals land
    # where every other refusal in this subcommand does — with nothing on
    # disk changed. Round N's own write goes first, because round N+1's rows
    # are only true once it has landed.
    forward = reach_forward(reader, rounds, args.round, now)

    ending = "\n" if text.endswith("\n") else ""
    write_record(reader, target, "\n".join(raw) + ending)
    if forward is not None:
        write_record(reader, forward[0], forward[1])
    counts = {
        w: sum(1 for word, _, _ in fixes.values() if word == w)
        for w in (FIXED, ANSWERED, DEFERRED_WORD)
    }
    print(
        f"round-record: closed {os.path.relpath(target, root)} {DASH} "
        + ", ".join(f"{n} {w}" for w, n in counts.items())
        + f"; {fix_range.strip('| ')}; {contract.strip('| ')}; {units.strip('| ')}"
        + (
            f"; {chain.CHECKED_BY} | {checker}"
            if checker in (chain.NO_FIXES, WRITTEN_CHECKER)
            else ""
        )
        + (
            f"; {INHERITED} of round-{args.round + 1}.md | {forward[2]} row"
            f"{'s' if forward[2] > 1 else ''} filled"
            if forward is not None
            else ""
        )
    )
    return run_check(root, args.baseline or default_baseline(root))


# --- seal: the one cell the broad gate writes ---------------------------------


def last_record(routing, rounds):
    """(N, path) of the highest-numbered `round-N.md` on disk, or `Refused`."""
    found = earlier_records(routing, rounds, sys.maxsize)
    if not found:
        raise Refused(
            f"{rounds} holds no round-N.md — there is no last record to seal. "
            "The broad gate runs after the rounds settle, and no round has run"
        )
    return found[-1]


def seal_home(routing, item, rounds):
    """(N, path) — the record the cell lands on, or (None, the file it lands in).

    **The home is picked from the DECLARATION, never from what happens to be on
    disk.** `chain_check` reads `broad-gate.md` on its direct arm alone and the
    last round record on its chain arm — one home per `Review` answer, chosen
    there by the same row. A home chosen here by the disk therefore disagrees
    with the reader twice, in opposite directions:

      a CHAIN work item whose `rounds/` is still empty — the ordinary state
          while round 1 runs — took the no-rounds branch and was sealed into
          `broad-gate.md`, which no reader of that work item ever opens, and
          `seal` printed `sealed` over it

      a DIRECT work item that does have round records was sealed onto the last
          one, which the direct arm never reads

    Both come from the same missing read, so both are closed by one. Round 1
    reproduced the first in a throwaway clone: exit 0, `sealed …
    broad-gate.md`, and the post-write `chain_check` still reporting the round
    record missing. What it costs is the sealer's answer — success reported for
    a seal that does not count, and the next party re-taking the run without
    knowing why. It fails closed either way, which is why nothing merged unrun.

    `last_record` used to RAISE on the empty-`rounds/` path, and that refusal
    was half of why a `straight to the PR` work item could not be sealed at
    all — the other half being a reader that returned before it looked. The
    refusal comes back here for the ONE state it was always right about: a
    chain declaration whose first record is not written yet.

    An unreadable or absent declaration falls back to the disk, which is this
    module's standing direction — a file nobody can read is not an answer
    somebody gave, and no arm of `chain_check` walks a work item that declared
    nothing, so neither home is read for it.
    """
    declared = None
    try:
        with open(os.path.join(item, routing.FILENAME), encoding="utf-8") as f:
            declared = routing.parse(f.read())
    except (OSError, UnicodeDecodeError):
        pass

    if declared is not None and declared["review"] == routing.DIRECT:
        return None, os.path.join(item, chain.BROAD_GATE_FILE)

    found = earlier_records(routing, rounds, sys.maxsize)
    if found:
        return found[-1]

    if declared is not None:
        raise Refused(
            f"{os.path.join(item, routing.FILENAME)} declares "
            f"`{declared['review']}` and {rounds} holds no `round-N.md`. For "
            "that answer the cell belongs on the last round record, and "
            f"`{chain.BROAD_GATE_FILE}` is read only for a work item "
            f"declaring `{routing.DIRECT}` — written there it would be a seal "
            "nothing reads. Write the round record first; no cell was written"
        )
    return None, os.path.join(item, chain.BROAD_GATE_FILE)


def new_broad_gate_file(item, value):
    """The whole text of a `broad-gate.md` holding that cell alone."""
    return (
        f"# {os.path.basename(os.path.abspath(item))} {DASH} broad gate\n"
        "\n"
        f"<!-- The `{BROAD_GATE}` cell, for a work item that ran no review\n"
        "rounds. Where rounds ran the same cell lives on the last\n"
        "`rounds/round-N.md`; this file is the other home, and it holds that\n"
        "row and nothing else.\n"
        "\n"
        "Written by `round-record seal`, which picks the home from what\n"
        "exists, and read by `chain_check.py` at the pull request. The cell\n"
        "records the commit the run happened at and the base it was compared\n"
        "against, so an edit after the run spends it — which is the whole of\n"
        "what a broad-gate cell asserts, and none of it depends on a round\n"
        "having run. One entry per run, newest first: a run at a new commit,\n"
        "or at this one against another base, is written in front and the\n"
        "earlier one stays behind it as `earlier run`; a run the newest entry\n"
        "already records — the same commit against the same base — replaces\n"
        "it. The reader takes the first SHA as the run. -->\n"
        "\n"
        "| Field | Value |\n"
        "|---|---|\n"
        f"{cell(BROAD_GATE, value)}\n"
    )


def seal(args):
    """Set the LAST record's `Broad gate` cell, and touch nothing else.

    This is the sealer's one write (issue #30, `questions.md` Q3), and it is a
    subcommand of its own because `close` cannot make it. `close` applies a
    fix table, and it refuses a row for a finding the reviewer already closed
    -- correctly, since that row would overwrite the reviewer's verdict. So
    once a record's fix table has been applied, every finding in it is
    closed, and `close --broad-gate` on that record is refused for the table
    it needs to be handed. Measured on the other work item of this release:
    CI found three Windows failures after the gate had run, the gate had to
    be re-taken at a later commit, and `close --round 3 --fixes <the same
    table> --broad-gate '<new sha> against <base>'` refused with *the fix
    table has a row for finding 17 (`answered`), which the reviewer already
    closed … no cell was written*. The only way through was a fix table with
    a header and no rows -- which wrote the cell and nothing else, exit 0,
    and which nobody would think to write. This subcommand is that path with
    a name: it takes neither `--fixes` nor `--range`, reads no verdict row,
    and writes one cell.

    Six refusals, each before the write. Counted rather than described --
    the number is the `raise Refused` sites in this function, and both times
    a document put a smaller number on them it was wrong inside one round.

      the record has no `Pass` box, or more than one   nothing here can be
          read, so nothing is written
      `Pass` is unchecked          a finding is still OPEN in the verdict
          table, so the round has not ended and the run this cell records
          would be a run over findings still open
      `Fixes checked by` reads anything but `no fixes to check`
          the fixes that closed those findings were read by nobody, and the
          verifying round is still owed. `Pass` says the TABLE is closed,
          and `close` ticks it the moment a fix table applies, which is one
          row earlier than the run ending -- so the broad seal lands in the
          window `skills/code-review/orchestration.md` §*Orchestrator: the
          pull request opens before round 1* calls red, on a record the
          verifying round is about to stop being the last one of. A capped
          run's LAST record reads `no fixes to check`, so this costs it
          nothing -- but a capped record that WROTE fixes reads `round-N`
          and is not the last record, so the refusal is what sends that run
          to spawn its verifying round first. `docs/review-chain-spec.md`
          §*The cap bounds rounds, and not the fixes of the round it
          stopped* owns that.
          Everything outside that ONE value is refused -- not `nobody`
          alone, and not everything-but-a-`round-N` either. The chain check
          this subcommand runs AFTER the write refuses on that same row, and
          a cell written there is a cell standing on a record its own check
          will not accept. `round-N` is part of what is refused because
          `CHECKER_RE` tests the cell's SHAPE and cannot test its POSITION,
          and a named checker has to be a LATER round than the record
          carrying it -- which the LAST record has none of (#335)
      `--broad-gate` carries no SHA-shaped word   the cell records a commit
      the SHA it carries does not resolve in this repository
      a `--broad-gate` SHA the record's `Target SHA` descends from   the
          run was spent before the round it seals -- the same test
          `chain_check.broad_gate` applies at the pull request, asked here
          so the cell is never written in a state the check would fail

    The first two are not one refusal said twice, and phase 5 plus round 1
    of #30 are the two halves of one question answered wrongly twice before
    it settled. `Needs a fix` is the reviewer's prose and refuses a run that
    ended at the cap; `Pass` is the verdict table and says nothing about
    whether a fix was read; `Fixes checked by` is the row that answers *has
    this run ended*, and its starting value is exactly the state that must
    refuse. All three were tried in that order.

    A fourth refusal stood first and was removed in phase 5: `Needs a fix`
    reading `yes` refused before either of the above, and it made a CAPPED
    run unsealable. `docs/review-chain-spec.md` bounds a run at three
    rounds, five while a red finding is open, and a run that ends at the cap
    ends with findings closed `deferred <home>` rather than fixed. `Needs a
    fix` is the REVIEWER's answer, written while the round ran, and nothing
    rewrites it afterwards -- so it still read `yes` over a verdict table
    with nothing open in it. Measured on a fixture in phase 4 of #30:
    `close` applied a fix table closing the one finding `deferred #999`, the
    `Pass` box came out checked because `deferred <home>` is a closing word,
    `Needs a fix` stayed `yes`, this refusal fired, and `chain_check` then
    failed the ready pull request on a `Broad gate` cell nothing could
    write. Two rules of the repository contradicted each other, and the cap
    exists for exactly the case that hit it.

    What the refusal was reaching for is *a finding is still open*, and
    `Pass` answers that one row down, from the verdict table rather than
    from prose. A record whose every verdict is closed -- on a fix, on
    grounds, or `deferred <home>` -- has ended its run whatever the reviewer
    concluded while it was running.

    Then `chain_check --worktree` runs, as `new` and `close` do. Commits
    nothing.
    """
    reader, routing, root, item, rounds = where(args)
    n, path = seal_home(routing, item, rounds)

    # NO ROUNDS: the three record refusals below have nothing to read and
    # nothing to say. `Pass`, `Fixes checked by` and `Target SHA` are each a
    # question about a round that ran — has its verdict table closed, has a
    # later round read its fixes, was the run spent before the commit it
    # sealed — and a work item that ran none answers all three by having no
    # round. What is NOT skipped is the pair below them: the cell still has to
    # carry a SHA-shaped word and that SHA still has to resolve here, because
    # those are about the RUN rather than about the review.
    if n is None:
        rows = []
        raw = lines = []
        # A `broad-gate.md` already there is read for ONE thing: the run it
        # holds, which the write below keeps behind the new entry (#174).
        # Nothing else of it is asked, because the three record refusals
        # are about a round, and this home has none.
        if os.path.isfile(path):
            held_text = read_text(path, chain.BROAD_GATE_FILE)
            rows = chain.table_rows(reader, reader.readable(held_text))
    else:
        text = read_text(path, f"last record round-{n}.md")
        raw, lines = text.splitlines(), reader.readable(text)
        rows = chain.table_rows(reader, lines)

    boxes = [m for ln in lines for m in [chain.PASS_RE.match(ln)] if m]
    if n is not None and len(boxes) != 1:
        raise Refused(
            f"round-{n}.md has {len(boxes)} `Pass` boxes and needs one; no cell "
            "was written"
        )
    if n is not None and boxes[0].group(1) == " ":
        raise Refused(
            f"round-{n}.md's `Pass` is unchecked — a finding in its verdict "
            "table is still open, and the broad gate seals a review that has "
            f"ended. `{chain.NEEDS}` is not read here: it is the reviewer's "
            "answer from while the round ran, and a capped run leaves it "
            "`yes` over a table with nothing open in it; no cell was written"
        )

    # `Pass` says nothing in the verdict table is open. It does NOT say the
    # run ended: `close` ticks the box the moment a fix table applies, and
    # the verifying round that reads those fixes has not run yet.
    # `skills/code-review/orchestration.md` §*Orchestrator: the pull request
    # opens before round 1* calls that window red, and it is the window a
    # seal is spent in — the verifying round's record becomes the last one,
    # its cell reads `not yet`, and the run has to be taken again.
    # A capped run's LAST record reads `no fixes to check`, so this costs it
    # nothing — but a capped record that WROTE fixes reads `round-N` and is
    # not the last record, so the refusal is what sends that run to spawn its
    # verifying round first. `docs/review-chain-spec.md` §*The cap bounds
    # rounds, and not the fixes of the round it stopped* owns that.
    #
    # Every value that is NOT a later round and NOT `no fixes to check` is
    # refused, rather than `nobody` alone (round 2's 🟡 12). The row has a
    # three-word vocabulary, and reading only `nobody` let the other two
    # thirds of what it can hold -- a name, a word outside the vocabulary, an
    # empty cell -- reach the write: the cell was written, `round-record:
    # sealed …` was printed, and the chain check this subcommand runs AFTER
    # the write then refused on that very row. `reach_back` two hundred lines
    # up already refuses an unreadable cell rather than acting on it, and
    # says why -- this is the same cell, one subcommand over.
    checker = reader.visible(chain.field(rows, chain.CHECKED_BY) or "").strip()
    plain = checker.strip("`").rstrip(".").lower()
    if n is not None and plain != chain.NO_FIXES:
        # A `round-N` is refused HERE rather than left to the check after the
        # write (#335). `CHECKER_RE` tests the SHAPE of the cell and cannot
        # test its POSITION, and the position is what decides this one: a
        # named checker has to be a LATER round, and `last_record` two
        # hundred lines up chose this file by being the highest-numbered one
        # on disk. So the value is unreachable on the record this subcommand
        # is holding, and admitting it wrote the cell and then had the chain
        # check refuse the same row one step later.
        #
        # The lastness is not derived here. It is the SELECTION CRITERION of
        # the line that chose the file, which is why reading it costs nothing
        # -- `docs/review-handoff-protocol.md` §*The `Fixes checked by` field*
        # states the rule about the last record in ratified policy, and
        # `docs/review-chain-spec.md` §*What the record carries* says it
        # twice more.
        why = (
            "a `round-N` names a LATER round, and this is the last record on "
            "disk — `last_record` chose this file by being the "
            "highest-numbered one, so there is no later round for the cell "
            "to name. `chain_check.checked_by` refuses the same row at the "
            "pull request"
            if chain.CHECKER_RE.match(plain)
            else "the fixes that closed its findings have been read by no "
            "LATER round. `Pass` was ticked by `close` when the fix table "
            "applied, which is one row earlier than the run ending"
        )
        raise Refused(
            f"round-{n}.md's `{chain.CHECKED_BY}` reads `{checker}`, and this "
            f"is the LAST record, where `{chain.NO_FIXES}` is the only value "
            f"`seal` accepts. {why}. `{chain.NOBODY} {DASH} <why>` is "
            "allowed on a last record by the protocol and refused here for "
            "its own reason: `seal` runs with `Pass` ticked, and "
            "`skills/code-review/orchestration.md` fails a pull request whose "
            f"last record reads `{chain.NOBODY}` beside a checked `Pass`. "
            "Spawn the verifying round first, before the sealer runs; its "
            "record is the one this cell "
            f"belongs on, and its own row then reads `{chain.NO_FIXES}`; no "
            "cell was written"
        )

    named = chain.SHA_RE.findall(args.broad_gate)
    if not named:
        raise Refused(
            f"--broad-gate {args.broad_gate!r} carries no SHA-shaped word. The "
            "cell records the commit the run happened at and the base it was "
            "compared against, `<sha> against <base>`; no cell was written"
        )
    ran_at = chain.resolves_to(root, named[0])
    if ran_at is None:
        raise Refused(
            f"--broad-gate names `{named[0]}`, which {root} cannot see. The "
            "sealer's mark names a commit this repository holds — the tree "
            "the run was taken over; no cell was written"
        )
    for sha in chain.SHA_RE.findall(chain.field(rows, chain.TARGET) or ""):
        reviewed = chain.resolves_to(root, sha)
        if reviewed is None or reviewed == ran_at:
            continue
        if chain.is_ancestor(root, ran_at, reviewed):
            raise Refused(
                f"--broad-gate names `{named[0]}`, and round-{n}.md's "
                f"`{chain.TARGET}` names `{sha}`, which descends from it. The "
                "run was spent BEFORE the round it is meant to seal — "
                "everything that round reviewed after that commit went "
                "through no broad gate (`CLAUDE.md` §*Verification Scope*). "
                "Run it again at the tree as it stands; no cell was written"
            )

    # ONE ENTRY PER RUN, NEWEST FIRST (#174). A run the cell already holds is
    # kept behind the new one as `earlier run`, because a second broad run --
    # after a pre-existing failure, or after the last fixes landed -- used to
    # REPLACE the first and the run-level table was then filled from memory.
    # `kept_broad_gate` is the one path, shared with `close --broad-gate`.
    value = kept_broad_gate(reader, rows, args.broad_gate)
    if n is None:
        write_record(reader, path, new_broad_gate_file(item, value))
    else:
        i = field_index(reader, lines, BROAD_GATE)
        raw[i] = cell(BROAD_GATE, value)
        ending = "\n" if text.endswith("\n") else ""
        write_record(reader, path, "\n".join(raw) + ending)
    print(
        f"round-record: sealed {os.path.relpath(path, root)} {DASH} `{BROAD_GATE}` | {value}"
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
    p.add_argument(
        "--written-late",
        default=None,
        help=f"WHY this record is being committed after the fixes it "
        f"commissions. Writes `{WRITTEN_LATE} | yes {DASH} <why>`, which "
        "`chain_check` prints instead of failing on. Absent, the row reads "
        "`no` and a late record is refused exactly as before",
    )
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
    s = sub.add_parser("seal", help="set the LAST record's Broad gate cell alone")
    s.add_argument("--item", required=True, help="the work item directory")
    s.add_argument(
        "--broad-gate",
        required=True,
        help="the cell: `<sha> against <base>` — the commit the one broad run "
        "happened at, and the base it was compared against",
    )
    s.add_argument("--root", default=None, help="the repository (default: the item's)")
    s.add_argument(
        "--baseline",
        default=None,
        help="the base for chain_check (default: the upstream, else origin/main)",
    )
    args = ap.parse_args(argv)
    try:
        commands = {"new": new, "close": close, "seal": seal}
        return commands[args.command](args)
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
