#!/usr/bin/env python3
"""chain-check — at the pull request, does the review state hold up?

The commit gate used to be the only place the review chain was enforced, and
it had nothing to read: a work item routed to the chain and a work item nobody
had decided anything about were byte-identical to it, so it asked at every
commit. Recording the answer in `seal/specs/<id>/routing.md` lets the gate stay
quiet — but only if the check moves somewhere rather than disappearing. This
is the somewhere. It runs on the pull request, where nobody has to be sitting.

What it reads, for every routing declaration this pull request adds or changes:

  through the review chain   at least one `seal/specs/<id>/rounds/round-*.md` that
                             git carries, every commit its Target SHA names being
                             REACHABLE (below), whose last round has `Pass`
                             CHECKED, whose Pass claim does not sit beside
                             a blocking finding it left open, and whose
                             `Fixes checked by` names a checker this repository
                             can confirm (below). A draft pull request is
                             excused the checked `Pass`, and nothing else
  straight to the PR         nothing required — the declaration is printed,
                             because a decision nobody sees is not a record
  an unreadable declaration  FAIL. A tolerant read reports "no declaration",
                             which is indistinguishable from a branch that
                             never declared
  no declaration at all      pass, with a notice
  a record still sitting at  FAIL, naming the file and `rounds/`. The records
  `specs/<id>/round-N.md`    moved one level down and no fallback ships, so a
                             repository that updated the plugin and moved
                             nothing would otherwise fail with `holds no
                             round-N.md` — true, and indistinguishable from a
                             work item that skipped its review

REACHABLE, and why it is not "an ancestor of HEAD". It was, and the branching
model destroys that property on purpose: `CONTRIBUTING.md` has feature branches
squash into the release branch, and the commits a round reviewed are exactly
what a squash discards. Measured on the release branch one commit after the
first work item merged, this check failed on its own release — naming two
commits of a review that had actually happened.

Narrowing it to records the pull request CHANGED does not fix that, and the
measurement says so: a new work item's round records are added relative to
`main`, so they are in every release pull request's diff. Both halves are
needed, and they answer different questions.

  is anything required of this record at all?   only if the pull request adds
      or changes it. A record that arrived in an earlier merge is history, and
      a check has no business asserting a property of it now

  which commits count as reachable?             an ancestor of HEAD, of the
      branch `routing.md` names, or of a pull request head. The first two need
      no new field. The third is what makes the answer survive: a branch is a
      mutable name and the paragraph that used to sit here asked people not to
      delete one, which is not a mechanism. Five were deleted anyway, by hand
      — `delete_branch_on_merge` is false in this repository, so nothing
      automatic did it and nothing stopped it either — and a release pull
      request went red naming six commits across five work items, every one
      of them still sitting on its `refs/pull/<N>/head`.

  Why that namespace and not "any ref that resolves": GitHub writes it, a
  squash does not touch it, deleting the branch does not touch it, and nothing
  else writes into it. Accepting any ref would re-open what `target_refs`
  records below — a tag carrying a commit nobody reviewed satisfying the check.

  A record's own `| PR |` row is read first when it names a number, which
  makes the failure name one ref instead of a namespace. It stays optional: a
  review that finishes before its pull request opens writes `not yet opened`,
  and the scan covers that with nothing written at all.

  What it costs: `refs/pull/*/head` is not in a default clone.
  `.github/workflows/hygiene.yml` fetches it, and where nobody has, the
  failure says which fetch is missing rather than sending anyone to restore a
  branch.

  (The paragraph above says a new work item's records ARE in every release
  pull request's diff. Both are true and they are about different merges:
  added by the release, already present after it.)

That "no declaration at all" row is the one that matters most, and it follows
this repository's own precedent. `unverified_check.py` refuses to fail for an
honest open item
because a build that goes red for one teaches people to write none, which
voids the condition it defends. A check that failed for a MISSING declaration
would teach sessions not to declare, and the same reasoning applies one level
up. It fails only for what the author can always fix.

The cost of that row is real and is stated rather than left to be found:
declaring nothing becomes a way past this check, and a quieter one than
already exists. `[no-review]` at least stays in the command. Declaring nothing
leaves no file, no token, and no line anywhere except the notice below.

FIXES CHECKED BY, and why a second field beside `Pass`. `Pass` is a claim
about the FINDINGS: none of them is still open. It says nothing about the
ANSWERS -- a finding is closed by a fix, the fix is written after the round
ends, and the round that follows is what opens it. Every round has one except
the last, whose fixes are written by the session that then ticks its box.
Measured on two consecutive work items in this repository (#33): the one round
that did look at the previous round's fixes found seven defects in them, and
its own fixes then went in unread.

So every record carries `| Fixes checked by | … |`, with three values and no
others. Only a LATER round may be named, so the LAST record of a finished run
can only read `no fixes to check` or `nobody`, and the earlier ones name the
round that opened them:

  round-N              that round opened these fixes. N above this record's
                       own number, and `rounds/round-N.md` committed
  no fixes to check    nothing here closed with a fix. Refused beside a
                       verdict cell reading one, which is the same
                       contradiction-inside-one-file the `Pass` rule refuses
  nobody -- <why>      the gap, written down. Prints on every run, and FAILS
                       beside a checked `Pass` on the last record -- see the
                       cutoff below

`nobody` is a disclosure rather than a claim, and a check that failed for an
honest disclosure would teach people to write none, which is the reasoning
`unverified_check.py` already runs on and the same one the "no declaration at
all" row below follows. So the cell prints wherever it appears, and on any
record but the last it is refused nothing at all.

What it may not do is stand beside `- [x] Pass` on the LAST record, because
that combination is the review saying it passed. A run whose final fixes
nobody opened has not passed: #33 measured the one set of fixes anybody ever
did open and found seven defects inside it.

That refusal reaches work items begun on or after `STRICT_FROM` and no
others, and the cutoff is what makes it shippable rather than theatre. A
record written before the rule existed is usually merged and has no honest
repair -- writing a `round-4.md` for a review nobody ran fabricates one, and
unticking `Pass` fails the ready-pull-request rule instead. A check whose
first production act is red on history nobody can fix is a check people learn
to skip, and skipping loses the records it could have caught in exchange for
the ones it never could.

Nothing after the cutoff is stuck, and the message says so. One verifying
round at the diff of those fixes closes it, and a round that opens nothing
needing a fix does not consume the cap.

The draft excuse does NOT reach this row. `Pass` is excused in a draft because
a review still running has not reached its verdict; a record naming a checker
it does not have is wrong at every stage.

THE FIX SURFACE, two rows read the same way. Issue #57 traced ten regressions
on one work item to the fixes that opened them, and the largest class -- four
of ten -- was a fix that changed a unit's contract while not every place that
contract reaches was revisited. The diff names the changed signature; `grep`
names the reach; a person reading the diff missed all four. So the record
carries the reach as a row, and a second row for the units the fixes CREATED,
which are the one surface the verifying round's own rule (*answers, not new
findings*) would otherwise skip:

  Contract changes     every unit whose signature, return arity, return type,
                       or set of returnable values changed in this round's
                       fixes, each with the call sites it reaches --
                       `unit → site, site`, units separated by `;`. A unit
                       listed without its reach is refused: the diff already
                       names the signature, and the reach is the half it does
                       not show
  New units            the top-level definitions and constants the fixes
                       added. The verifying round treats what this row names
                       as a finding surface -- *is this correct* -- rather
                       than a verification surface

Both accept `none`, with or without a reason after it, because the honest
mid-run value is `none — the fixes are not yet written` and the honest
terminal value of many rounds is plain `none`. A record whose work item began
before `SURFACE_FROM` prints instead of failing when a row is absent -- the
grandfathering shape `Fixes checked by` already uses, for the same reason: a
merged record has no honest repair, and writing reach rows for fixes nobody
re-read would fabricate a review. A row that is PRESENT and malformed fails
on any record, because formatting is always the author's to fix.

Read on EVERY record, where `Pass` is read on the last one alone. The two
scopes differ for a reason rather than by oversight: `Pass` is a verdict on
the whole review and the last round's is the one that speaks for it, while
this is a fact about one round's own fixes and every round has one. Reading
only the last record was the first shape, and it made `round-N` unreachable --
a checker has to be later, and the last record has no later round -- which is
a vocabulary value nothing could ever use.

What it costs is a repository that updates the plugin: every record in a work
item whose declaration the pull request touches needs the row, not just the
newest. The failure names the row and the three values, which is the same
trade `docs/review-handoff-protocol.md` records for the `rounds/` move.

WHAT IT CANNOT SEE, stated here rather than discovered later:

  whether the review was any good   the same limit the commit gate carries.
                                    A round record naming three findings and
                                    one naming none look alike to it, and a
                                    checked `Pass` is a claim by whoever
                                    wrote the record. What is refused is the
                                    claim that contradicts its own table
  a review nobody wrote down        `<git-dir>/specseal-reviewed` cannot reach
                                    CI. The round record stops being only an
                                    inheritance aid and becomes the pull
                                    request's evidence
  whether the TIP was reviewed      it requires a round record whose target is
                                    reachable, not that HEAD itself was
                                    reviewed. Requiring the tip would put
                                    the every-commit problem back, one fix
                                    commit later
  a record already merged           no claim is made about WHERE the commits
                                    of a round record this pull request does
                                    not touch are. Everything else about it is
                                    still read — the `Target SHA` row has to be
                                    there, the `Pass` box has to be there and
                                    consistent. Its commits are expected to be
                                    gone, and the review it records was
                                    enforced at the pull request that added it
  whether the target CONTRIBUTED    reachability from the declared branch is
                                    not evidence that the reviewed commit is in
                                    what merges. Measured: a commit pushed to
                                    the branch AFTER the squash, merged
                                    nowhere, satisfies `Target SHA`. That is
                                    the price of not asserting a property the
                                    squash destroys, and it is paid knowingly
  a repository with no CI           then nothing checks at the pull request at
                                    all, and enforcement is a convention

ONE SOURCE, NOT TWO. Everything read here comes out of git at HEAD -- the
declarations, the round records, their content. Two readers of one directory
is how an untracked file became a pull request's evidence, and moving only the
NAMES to git left the same defect one line further in: a record committed with
a blocking finding open and edited on disk to read `fixed` exited 0. A working
tree that differs from HEAD is what CI never sees, so reading one makes the
local run the more permissive of the two.

ONE READER, NOT TWO. The section and table reading comes from
`unverified_check.py` rather than being written again. Two readers of the same
markdown drifted apart in four places across three review rounds in this
repository — which section is counted, how a cell is normalized, what counts
as a separator — and each pair that was closed opened another. A comment or a
fenced code block that mentions a blocking finding must not count here for
exactly the reason it must not count there.

Exit codes: 0 the review state holds (or nothing was declared) · 1 a
declaration or a round record fails · 2 the arguments or the repository were
unusable, which includes the shared reader failing to load — with no reader
there is no check, and reporting success for a check that never ran is the
one outcome worse than failing.
"""

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
READER = os.path.join(HERE, "..", "..", "verify", "scripts", "unverified_check.py")
ROUTING = os.path.join(HERE, "..", "..", "..", "hooks", "routing.py")

VERDICTS = "## Verdicts"
TARGET = "Target SHA"
PASS_RE = re.compile(r"^\s*-\s*\[( |x|X)\]\s*Pass\b")
BLOCKING = "🔴"
# What a verdict cell may say for the finding to count as dealt with. Anything
# else counts OPEN — including a word this does not recognise. The direction is
# deliberate: an unreadable verdict that counted as closed would be the
# tolerant read this whole file exists to refuse.
CLOSED_WORDS = {"fixed", "answered", "withdrawn", "not a defect", "agreed, fixed"}
# The subset of `CLOSED_WORDS` that closed a finding by WRITING something. Those
# are the fixes `Fixes checked by` is about; `answered`, `withdrawn` and
# `not a defect` produced no code for a later round to open. Spelled as a
# subset of the set above rather than as its own vocabulary, so a verdict word
# added there is impossible to add here by accident -- the assertion below
# fails the module at import if the two ever come apart.
FIX_WORDS = {"fixed", "agreed, fixed"}
assert FIX_WORDS <= CLOSED_WORDS, "a fix word that is not a closing word"
# Markdown emphasis around the verdict word, and the code fence a cell puts
# round the commit after it. Both sets above are spelled bare, and a
# normalizer that read only the bare word matched NOTHING this repository ever
# wrote: every closed verdict in `seal/specs/*/rounds/round-*.md` reads `**fixed**`,
# and most cite a commit after it. Neither refusal that reads a verdict cell
# had ever fired on a real record.
EMPHASIS = re.compile(r"[*_`]+")
# The vocabulary as a match ORDER, longest spelling first, so the `fixed`
# inside `agreed, fixed` never takes the row from it. Derived from
# `CLOSED_WORDS` rather than written out again: the assertion above
# `FIX_WORDS` exists because two hand-kept lists drift, and a third list is
# that same bet taken a second time.
#
# This replaces a regex that located where the commit citation began and cut
# the cell there. Cutting was the wrong shape for the question. The pattern
# required a digit inside the hex run — `defaced` and `acceded` are seven
# characters of [0-9a-f] and ordinary English — and a real seven-character
# abbreviation carries no digit about one time in 959. At that point the
# pattern did not cut LATE; it did not cut at all, so `**fixed** `deadbee``
# normalized to `fixed deadbee`, which is in neither set, and a 🔴 that was
# properly closed read as still open. Round 2 opened that at the same site
# round 1 was closing, which `docs/review-chain-spec.md` calls the structure
# signal whatever the count.
#
# Matching the vocabulary as a PREFIX of the cell asks the question directly
# and never has to recognise a commit at all, so the digit question disappears
# rather than moving one spelling further out. It keeps the direction the cut
# was protecting: only the head of the cell is ever consulted, so
# `answered, and **sharpened** in `96a1ae3`` is `answered` and not a fix.
VOCAB = sorted(CLOSED_WORDS, key=len, reverse=True)
# `Pass` says the findings are closed. This says who opened the work that
# closed them, and it is the last record's answer to the question `Pass`
# cannot reach. See the module docstring for what each value means.
CHECKED_BY = "Fixes checked by"
NO_FIXES = "no fixes to check"
NOBODY = "nobody"
# Where the refusal for `Pass` beside `nobody` starts, as the unix second in a
# work item's own directory name. This is the id of the work item that added
# the rule, so the first item held to it is the one that wrote it.
#
# It is one constant for every repository, and that is the decision rather
# than an accident of this one. A work item begun before the rule existed was
# written when nothing asked, and its records are usually merged: a check
# whose first production act is red on history nobody can honestly repair is a
# check people learn to skip, which voids it for the records it COULD have
# caught. A repository installing the plugin fresh creates every work item
# after this second, so the whole of its history is held to the rule; one
# updating the plugin has exactly its pre-existing items excused. Neither
# needs to configure anything.
#
# What it costs: an old work item reopened years from now still writes its
# records under its original id, and stays excused. That is the same trade the
# grandfathering makes everywhere else, taken knowingly rather than closed
# with a second rule about how old is too old.
STRICT_FROM = 1788212517
# `round-N`, optionally with the `.md` a person copying a filename leaves on.
# The number is handed to `routing.round_number` rather than read here: that
# function is the one place the `round-N.md` ordering rule lives, and this
# would be the third reader of the pattern.
CHECKER_RE = re.compile(r"^round-\d+(?:\.md)?$")
# What may stand between `nobody` and its reason. An em dash is what the
# documents and the template use; the rest are what a person types instead,
# and refusing those would fail a record for its punctuation. The SPACE is in
# the set because the dash never touches the word -- `nobody — why` puts a
# space first, and leaving it out refused the one spelling every document
# shows.
# The two dashes are built by codepoint rather than typed. An en dash sitting
# in a string literal is what ruff's RUF001 reads as a hyphen somebody
# mistyped, and that rule earns its keep everywhere else in this file; the em
# dash goes the same way so the pair reads as a pair. 0x2014 is EM DASH and
# 0x2013 is EN DASH.
SEPARATORS = " " + chr(0x2014) + chr(0x2013) + "-:,"
# The fix surface (issue #57): what this round's fixes changed, with the call
# sites each change reaches, and what they created. See the module docstring.
CONTRACT = "Contract changes"
NEW_UNITS = "New units"
# `none` in either row, with or without a reason after a separator -- matched
# as a prefix the way `verdict_of` matches its vocabulary, so `none — the
# fixes are not yet written` is an answer and `nonempty` is not.
NONE_WORD = "none"
# A unit is separated from its reach by an arrow, either the typographic one
# every document shows or the ASCII one somebody types when it is not on the
# keyboard. `;` separates units, because a reach list needs its commas.
ARROWS = (chr(0x2192), "->")
# Where the two rows above become required, as the unix second in a work
# item's directory name -- the id of the work item that added them, so the
# first item held to the rule is the one that wrote it. The same shape and
# the same reasoning as `STRICT_FROM` above: a record written before the rule
# is usually merged and has no honest repair -- writing reach rows for fixes
# nobody re-read fabricates a review -- so those print instead of failing,
# and a check whose first production act is red on history nobody can fix is
# a check people learn to skip. What it costs is the same trade taken there:
# an old work item reopened later still writes records under its original id
# and stays excused.
SURFACE_FROM = 1788272986
# `templates/sdd-round.md:12` and `docs/review-handoff-protocol.md:84` both say
# the Target SHA cell may name BOTH commits when HEAD moved mid-review. The
# whole cell used to be handed to `merge-base` as one ref, so the documented
# form could not resolve and no round record has ever been able to use it —
# which is how `round-2.md` came to name a tree that did not hold the fixes it
# recorded as made. Every SHA-shaped word in the cell is checked, so a second
# one is not somewhere to hide a commit.
SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
# Where a reviewed commit still lives once the branch that carried it is gone.
# GitHub writes the head of every pull request under `refs/pull/<N>/head` and
# keeps it for as long as the pull request exists: a squash does not touch it,
# and neither does deleting the branch. `.github/workflows/hygiene.yml` fetches
# the namespace into `refs/remotes/pull/`, because a default clone has none of
# it.
PULL_HEADS = "refs/remotes/pull/"
# The number in a round record's own `| PR |` row. `not yet opened` is the
# honest value while the review runs and names no number, which is why nothing
# here requires one.
PR_FIELD = "PR"
PR_RE = re.compile(r"#?(\d+)")


def load(path, name):
    """Import a sibling script by path, or die — a missing reader is exit 2."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"chain-check: cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(root, *args):
    r = subprocess.run(
        ["git", "-C", root, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    return r.stdout if r.returncode == 0 else None


def changed(root, base):
    """Every path this pull request adds or changes, or None.

    One diff, read twice below -- for the declarations and for the round
    records. Two `git diff` calls against the same base would be two values
    built by the same rule today and by two rules after the first edit to
    either, which is the split this file keeps closing in other places.

    `-z` for the same reason `tracked_files` uses it two functions down. Without
    it `core.quotePath` (on by default) wraps and octal-escapes any path holding
    non-ASCII, a quote or a backslash, and `round_records` builds its paths from
    `ls-tree`, which never quotes. Round 1 caught the consequence by execution:
    a work-item id containing `é` made the membership test at the per-record
    decision fail, `refs` became None, and the reachability requirement
    disappeared for a record the pull request had just added -- exit 1 on the
    previous revision of this file, exit 0 on the one that introduced the test.
    The line printed `already merged`, which is why it was invisible.

    Returns `(paths, renamed)`: every path the diff names under its NEW name,
    and the subset that arrived as an exact rename (`R100`). `--name-status`
    with `-M` rather than `--name-only`, because a rename has two names and
    `--name-only` printed the new one indistinguishably from an added file.
    The root move to `seal/` renames every declaration in a repository at once,
    and `changed_routing` needs to know which of the paths it sees are those.
    """
    out = git(root, "diff", "--name-status", "-z", "-M", f"{base}...HEAD")
    if out is None:
        return None
    fields = out.split("\0")
    paths, renamed = [], set()
    i = 0
    while i < len(fields):
        status = fields[i]
        if not status:
            i += 1
            continue
        if status[0] in "RC":
            # A rename or a copy carries two names; the second is the one
            # the tree holds now, and the one every reader below opens.
            if i + 2 >= len(fields):
                break
            new = fields[i + 2]
            paths.append(new)
            if status == "R100":
                renamed.add(new)
            i += 3
            continue
        if i + 1 >= len(fields):
            break
        paths.append(fields[i + 1])
        i += 2
    return paths, renamed


def changed_routing(paths, renamed, work_items):
    """Routing declarations this pull request adds or changes.

    Never one it only renamed. The root move to `seal/` (`specs/<id>/` into
    `seal/specs/<id>/`) renames every declaration in the repository, and each
    shows up in the diff under its new path exactly as an added one would.
    Judging them would put every released work item under review on the
    pull request that moved it, each needing its round records' Target SHA
    to resolve — a declaration the pull request only moved is not one it
    made. A rename that also EDITED the file (`R` below 100) is judged: the
    edit is the pull request's own.

    `work_items` is `routing.WORK_ITEMS`, passed in rather than spelled here,
    so the prefix has one spelling.
    """
    return sorted(
        p
        for p in paths
        if p.startswith(f"{work_items}/")
        and os.path.basename(p) == "routing.md"
        and p not in renamed
    )


# What git calls a plain file. An allow-list rather than a deny-list, so a
# mode nobody anticipated is excluded rather than admitted -- `120000` is a
# symbolic link and `160000` a submodule, and neither is a record.
REGULAR = ("100644", "100755")


def tracked_files(root, item):
    """Filenames git carries directly in `item` as regular files.

    `os.listdir` was the rule here, and it answered a question git had not
    been asked. Everything else in this check comes from git -- the
    declarations from `git diff`, the ancestry from `merge-base` -- so two
    values built by two rules were being compared. Both halves of that were
    reachable, and both were reproduced against a scratch repository:

      an untracked `round-1.md` counted as this pull request's evidence,
      exit 0, when CI would never have seen the file at all

      a tracked symbolic link `round-3.md` pointing at a clean `round-1.md`
      turned exit 1 into exit 0, with the failing `round-2.md` committed and
      sitting between them, unread

    The second one is the sharper of the two, because the LAST round is the
    one whose verdict speaks: anything that can add a name at the end of the
    sort decides which file gets read.
    """
    out = git(root, "ls-tree", "-z", "HEAD", "--", f"{item}/")
    if out is None:
        return []
    names = []
    for entry in out.split("\0"):
        if not entry:
            continue
        meta, _, path = entry.partition("\t")
        parts = meta.split()
        if len(parts) < 3 or parts[0] not in REGULAR:
            continue
        names.append(os.path.basename(path))
    return names


def read_record(root, rel):
    """The file as git carries it at HEAD, or None.

    The name comes from `ls-tree`, so the content has to come from the same
    place. It did not: round 2 moved the NAMES to git and left `open()` where
    it was, so the check still built two values by two rules -- one line
    later. Both halves were reproduced:

      a record committed with a blocking finding open, edited on disk to read
      `fixed` and never committed, exited 0

      a working tree holding a clean copy where git carries a failing
      `round-2.md` folded the failing record out of the list entirely

    A working tree that differs from HEAD is exactly what CI never sees and a
    local run always can, which makes the local run the more permissive of
    the two -- the wrong direction for the only enforcement left.
    """
    return git(root, "show", f"HEAD:{rel}")


def round_records(routing, root, item):
    """`seal/specs/<id>/rounds/round-*.md` git actually carries, highest round last.

    `rounds/` rather than the work item's own directory: `round-N` is the one
    member of the SDD set that is plural and unbounded, and the structure
    should say which member grows. `tracked_files` is asked for the
    subdirectory rather than filtered afterwards, because `ls-tree` without
    `-r` reports `rounds` itself as a tree and the mode filter drops it --
    which is exactly the silent nothing `stray_records` below exists to stop
    being the only answer.

    Ordered by `routing.round_number`, which is where that rule lives: this
    file and `hooks/routing.py` used to sort by two rules, and the docstring
    here called the other one a defect instead of removing it.

    Nothing is folded by realpath any more. That fold was `unverified_check.py`'s
    `unique_by_target`, and it resolved WORKING-TREE paths -- which stopped
    being what this counts once the content came from git. It was not merely
    redundant beside the mode filter: a worktree holding a clean copy where
    git carries a failing record folded the failing one away, which is the
    same exit-0 the link case produced, reached from the other side.
    """
    found = []
    where = f"{item}/{routing.ROUNDS_DIR}"
    for n in tracked_files(root, where):
        number = routing.round_number(n)
        if number is not None:
            # `/`, not `os.path.join`. Every consumer of this path is git or
            # something built from git: `read_record` spends it as
            # `git show HEAD:<rel>`, and the membership test in `main`
            # compares it against `git diff --name-only`. On Windows the
            # join spelled the separator \ for both, and git accepts and
            # prints only `/` -- so the record git carries could not be read,
            # and, one line further on, the record this pull request had just
            # ADDED tested as one it did not touch, which drops the
            # reachability requirement entirely. Same shape as the
            # `core.quotePath` defect `changed` describes: two spellings of
            # one path, and the quiet half is the dangerous one.
            found.append((number, f"{where}/{n}"))
    return [rel for _, rel in sorted(found)]


def rounds_unreadable(routing, root, item):
    """True when git carries `rounds` as a BLOB rather than a tree.

    The filesystem twin is `hooks/routing.py:rounds_unreadable`, and round 2
    found it shipped without this one: the hook named the state and the pull
    request check did not, so one repository was told two different things
    about one tree.

    What it costs when missing is the message this file's own header calls
    *true, and indistinguishable from a work item that skipped its review* --
    and worse here than in the hook, because the `mkdir` that message then
    prescribes fails with `File exists`, leaving no next step at all.

    Git is asked for the entry's TYPE rather than run through
    `tracked_files`, whose mode allow-list is `100644`/`100755`. A symbolic
    link is `120000` and fell straight through that, which put this reader
    and the hook back on opposite answers for one tree -- the state this
    function was added for, reappearing inside the fix for it.
    """
    out = git(root, "ls-tree", "-z", "HEAD", "--", f"{item}/{routing.ROUNDS_DIR}")
    if not out:
        return False
    for entry in out.split("\0"):
        if not entry:
            continue
        meta, _, path = entry.partition("\t")
        fields = meta.split()
        if len(fields) >= 2 and os.path.basename(path) == routing.ROUNDS_DIR:
            return fields[1] != "tree"
    return False


def stray_records(routing, root, item):
    """`round-N.md` git carries at the work item's TOP level, lowest first.

    Records nothing reads. The flat location is where every record in every
    repository sat before `rounds/`, and no fallback ships: a permanent dual
    read would put two places to look in the reader four gates import, and an
    expiry nothing enforces is a comment.

    So the cost of refusing the fallback is paid here instead. Without this,
    a repository that updated the plugin and moved nothing would fail its
    pull request with `holds no round-N.md` -- true, useless, and
    indistinguishable from a work item that skipped its review. The caller
    turns this list into a message naming the file and the destination, which
    is the entire migration path this release ships.
    """
    found = []
    for n in tracked_files(root, item):
        number = routing.round_number(n)
        if number is not None:
            found.append((number, f"{item}/{n}"))
    return [rel for _, rel in sorted(found)]


def pull_request_state():
    """(`draft` | `ready` | `unknown`, where that was read from).

    Read out of the event payload GitHub writes to disk, not out of
    `gh pr view --json isDraft`. The payload is already this workflow's
    authority for `github.base_ref` two steps above this one, and it needs no
    network, no token, and no `gh` on PATH -- three things a check that must
    not fail open should not depend on.

    `unknown` is every run outside a pull-request event, and it is judged as
    a READY pull request. That direction is the whole decision:

      judged as draft   `no pull-request context` becomes the quietest way
                        past this check that exists, quieter than
                        `[no-review]`, which at least stays in the command
      judged as ready   a local mid-round run exits 1, which is the true
                        answer -- the rounds have not finished

    A `--draft` flag was considered for the local case and rejected for the
    first reason: an override anyone can type is the same hole with a name.
    What the unknown state must not do is pass in SILENCE, so the verdict
    below prints which state was assumed and why.
    """
    path = os.environ.get("GITHUB_EVENT_PATH")
    if not path or not os.path.exists(path):
        return "unknown", "no pull-request event payload"
    try:
        with open(path, encoding="utf-8") as f:
            event = json.load(f)
    except (OSError, ValueError) as exc:
        return "unknown", f"the event payload would not read ({exc})"
    pr = event.get("pull_request")
    if not isinstance(pr, dict) or "draft" not in pr:
        return "unknown", "the event payload names no pull request"
    if not isinstance(pr["draft"], bool):
        # Every non-empty string is truthy, so `"draft": "false"` read as a
        # draft -- and a draft is excused the checked `Pass`. Anything that is
        # not the boolean the schema promises drops to `unknown`, which is
        # judged as READY, so a malformed payload cannot be quieter than a
        # well-formed one.
        return "unknown", (
            f"the event payload's `draft` is {type(pr['draft']).__name__}, "
            "not a boolean"
        )
    return ("draft" if pr["draft"] else "ready"), path


def field(rows, label):
    """The value of a `| label | value |` row, or None."""
    for cells in rows:
        if len(cells) >= 2 and cells[0].strip() == label:
            return cells[1].strip()
    return None


def table_rows(reader, lines):
    """Every table row in already-`readable` lines, as lists of cells."""
    out = []
    for line in lines:
        cells = reader.split_row(line)
        if cells is not None:
            out.append(cells)
    return out


def tracked_declarations(root, routing):
    """(path, parsed) for every `seal/specs/<id>/routing.md` git carries at HEAD.

    `routing.declarations` walks the working tree, which is right where it is
    called from -- a hook fires before the commit, and an uncommitted
    declaration is what the author just wrote. It is wrong here for the same
    reason `os.listdir` was wrong for the round records: CI has no working
    tree that differs from HEAD, so a check that reads one is more permissive
    locally than in the place it actually runs.

    The vocabulary still comes from `routing.parse` rather than being written
    again -- what changed is where the bytes come from, not who reads them.
    """
    out = git(root, "ls-tree", "-r", "-z", "HEAD", "--", f"{routing.WORK_ITEMS}/")
    if out is None:
        return []
    found = []
    for entry in out.split("\0"):
        if not entry:
            continue
        meta, _, path = entry.partition("\t")
        parts = meta.split()
        if len(parts) < 3 or parts[0] not in REGULAR:
            continue
        if os.path.basename(path) != routing.FILENAME:
            continue
        text = read_record(root, path)
        if text is None:
            continue
        parsed = routing.parse(text)
        if parsed:
            found.append((path, parsed))
    return found


def declared_for_this_branch(root, routing):
    """(declarations, why there are none) for the branch this run is on.

    `changed_routing` reads what this pull request CHANGED, so a pull request
    that adds only round records to a work item declared in an earlier one
    found nothing and printed *this pull request declared neither way* — a
    sentence about a tree that is holding the declaration right there.

    The key is the branch, which is what `routing.for_branch` already uses at
    the commit: one key read at two sites rather than a second rule that
    drifts from the first. In a workflow the branch is `GITHUB_HEAD_REF`,
    because a pull-request checkout is a detached merge commit and has no
    branch of its own to read.

    The reason is returned rather than left to the caller to guess, because
    the empty answers mean different things and one of them was being
    reported as another: a detached HEAD with no `GITHUB_HEAD_REF` printed
    *declared neither way* about a pull request that had declared, in a commit
    further back. Widening the workflow's `types:` is what put that state
    within reach, so it is answered in the same change.
    """
    branch = os.environ.get("GITHUB_HEAD_REF") or routing.current_branch(root)
    if not branch:
        return [], (
            "the branch could not be read — a detached HEAD with no "
            "GITHUB_HEAD_REF — so no declaration could be matched to one. "
            "This is not a pull request that declared nothing; it is a run "
            "that had no key to look one up by"
        )
    matching = [
        p for p, d in tracked_declarations(root, routing) if d["branch"] == branch
    ]
    if len(matching) > 1:
        return [], (
            f"{len(matching)} committed declarations name `{branch}`, which is "
            "not an answer — the same reading `routing.for_branch` takes at "
            f"the commit: {', '.join(sorted(matching))}"
        )
    if not matching:
        return [], (
            "this pull request declared neither way, so the review-chain "
            "check examined nothing. Add seal/specs/<work-item>/routing.md to "
            "declare."
        )
    return [matching[0]], ""


def is_ancestor(root, sha, ref):
    r = subprocess.run(
        ["git", "-C", root, "merge-base", "--is-ancestor", sha, ref],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.returncode == 0


def target_refs(reader, root, declared):
    """Refs a round's Target SHA is allowed to be an ancestor of.

    HEAD, and the branch the declaration names -- BOTH forms of it, remote and
    local, each kept only if it resolves. Round 1 measured why neither shortcut
    survives:

      taking the first that resolves and stopping hid a local branch carrying
      the reviewed commit behind a stale `origin/<branch>` that did not, and
      the failure advised restoring a branch that was sitting right there

      resolving the bare name let git's disambiguation order decide, and
      `refs/tags/` beats `refs/heads/`. A tag and a branch both named `dup`
      resolved to the TAG, and `merge-base --is-ancestor` followed it -- so a
      tag carrying a commit nobody reviewed satisfied the check while the
      branch's own commits were invisible. The bare name also accepts anything
      git parses as a revision, and a `| Branch | main |` cell admitted every
      commit on `main`.

    Fully qualified closes both. Nothing here reads the branch git happens to be
    on: the declaration's `| Branch |` row is the work item's own statement of
    where its rounds ran, and it is the same row `hooks/routing.py` matches a
    commit against.
    """
    refs = ["HEAD"]
    branch = declared.get("branch")
    if branch:
        for candidate in (f"refs/remotes/origin/{branch}", f"refs/heads/{branch}"):
            if reader.resolves(root, candidate):
                refs.append(candidate)
    return refs


def declared_pull_head(reader, root, rows):
    """`[refs/remotes/pull/<N>/head]` for the number a record's `PR` row names.

    The row is already in `templates/sdd-round.md`, and this gives it a second
    job rather than asking anyone to write something new: where it names a
    number, the reviewed commit has one exact place to be, and the failure
    below can name it. It stays OPTIONAL -- a review that finishes before its
    pull request opens writes `not yet opened`, which is the truth, and the
    namespace scan in `reachable` covers that case without a number.
    """
    cell = field(rows, PR_FIELD) or ""
    found = PR_RE.search(cell)
    if not found:
        return []
    ref = f"{PULL_HEADS}{found.group(1)}/head"
    return [ref] if reader.resolves(root, ref) else []


def carried_by_a_pull_head(root, sha):
    """The `refs/pull/<N>/head` carrying `sha`, or None.

    The fallback that needs nothing written. One `for-each-ref`, so the cost
    does not grow with a ref per call, and it is narrower than "any ref that
    resolves": nothing but a pull request writes this namespace, so a tag
    cannot satisfy the check through it -- which is the exact failure
    `target_refs` records for resolving a bare name.

    Returns None when the namespace was never fetched, and the caller's
    message says so, because "not fetched" and "not there" are different
    repairs and a check that confuses them sends people to restore a branch
    that would not have helped.
    """
    r = subprocess.run(
        [
            "git",
            "-C",
            root,
            "for-each-ref",
            "--contains",
            sha,
            "--format=%(refname)",
            PULL_HEADS,
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        return None
    first = r.stdout.split("\n")[0].strip()
    return first or None


def reachable(root, sha, refs):
    """(True, ref) for the first ref `sha` is an ancestor of, else (False, None)."""
    for ref in refs:
        if is_ancestor(root, sha, ref):
            return True, ref
    carrier = carried_by_a_pull_head(root, sha)
    if carrier:
        return True, carrier
    return False, None


def verdict_table(reader, lines, rel):
    """(rows, the Verdict column's index, errors) for `## Verdicts`.

    Rows are `(line number, cells already run through `reader.visible`)`, with
    the header and the separator dropped.

    ONE parse, two questions. Which blocking findings are still open was the
    only one asked of this table until `Fixes checked by` arrived and needed a
    second — whether anything here closed by writing a fix. A second walk of
    the same markdown is exactly the split this file spends its docstrings
    closing everywhere else, so the walk happens here and the questions are
    asked of what it returns.

    The verdict table is located by its own heading and read with the shared
    reader, so a 🔴 inside a comment or a fenced block is not a finding.
    """
    starts = reader.sections(lines, VERDICTS)
    if not starts:
        return (
            [],
            -1,
            [
                (
                    rel,
                    0,
                    f"no `{VERDICTS}` section — a round record without "
                    "one says nothing about what it found",
                )
            ],
        )
    if len(starts) > 1:
        return [], -1, [(rel, starts[1] + 1, f"more than one `{VERDICTS}` section")]

    start = starts[0]
    body = []
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("#"):
            break
        body.append((i + 1, lines[i]))

    rows = [(n, reader.split_row(ln)) for n, ln in body if ln.strip()]
    rows = [(n, c) for n, c in rows if c is not None]
    if not rows:
        return (
            [],
            -1,
            [
                (
                    rel,
                    start + 1,
                    f"`{VERDICTS}` holds no table — write the "
                    "rows, or `none` with a header row and no findings",
                )
            ],
        )

    header = [reader.visible(c).lower() for c in rows[0][1]]
    if "verdict" not in header:
        return (
            [],
            -1,
            [
                (
                    rel,
                    rows[0][0],
                    "the verdict table has no `Verdict` "
                    f"column; its header is |{'|'.join(rows[0][1])}|",
                )
            ],
        )
    col = header.index("verdict")

    seen_rows, errors = [], []
    for line_no, cells in rows[1:]:
        seen = [reader.visible(c) for c in cells]
        if reader.is_separator(seen):
            continue
        if len(cells) <= col:
            errors.append(
                (
                    rel,
                    line_no,
                    f"{len(cells)} cells, and the `Verdict` column is number {col + 1}",
                )
            )
            continue
        seen_rows.append((line_no, seen))
    return seen_rows, col, errors


def verdict_of(seen, col):
    """One row's verdict cell, normalized the way `CLOSED_WORDS` is spelled.

    The sets are spelled bare and the records are not. Every closed verdict
    this repository has ever written reads `**fixed**`, usually with the
    commit that closed it beside the word, so a normalizer that lowercased and
    stripped a full stop recognised none of them. What that cost is both
    directions of the same gap: `closed_with_a_fix` answered False on every
    record in the repository, so the one refusal separating an honest `nobody`
    from a silent pass never ran, and `open_blocking` read a 🔴 legitimately
    closed as `**fixed** `sha`` as still open.

    Two layers come off and then the vocabulary is matched as a PREFIX:

      emphasis   `**fixed**`, `` `fixed` `` — `EMPHASIS`
      the stop   a trailing full stop
      the head   the first word of `VOCAB` the cell BEGINS with, ended by a
                 space or a comma, so `fixed d3fe44d` and `fixed deadbee` are
                 both `fixed` and neither has to be recognised as a commit

    Reading only the head of the cell is what keeps the other direction safe.
    `answered, and **sharpened** in `96a1ae3` — …` begins with `answered,` and
    stops there, so a long `answered` cell that mentions a fix does not read
    as one — where a reader scanning the whole cell for a fix word would have
    found one.

    The boundary is what makes it a word rather than a prefix of one. Without
    it `not a defect` would swallow `not a defective reading`, and the two are
    opposite verdicts. Anything the vocabulary does not begin the cell with
    comes back as the normalized cell itself, which is in neither set and
    therefore counts OPEN — `not fixed` included, which is the direction this
    whole file takes for a cell it cannot read.
    """
    s = EMPHASIS.sub("", seen[col]).lower().strip().rstrip(".").strip()
    for word in VOCAB:
        if s == word or s.startswith(word + " ") or s.startswith(word + ","):
            return word
    return s


def open_blocking(reader, lines, rel):
    """(rows, errors) — blocking findings the last round left open."""
    rows, col, errors = verdict_table(reader, lines, rel)
    if col < 0:
        return [], errors
    still_open = [
        (line_no, seen[0] or f"row at line {line_no}", verdict_of(seen, col))
        for line_no, seen in rows
        if BLOCKING in "".join(seen) and verdict_of(seen, col) not in CLOSED_WORDS
    ]
    return still_open, errors


def closed_with_a_fix(reader, lines, rel):
    """True when a verdict here closed its finding by WRITING something.

    `answered`, `withdrawn` and `not a defect` close a finding and produce no
    code, so a record holding only those has nothing for a later round to
    open and `no fixes to check` is the truth. A record holding one `fixed`
    does not, and that is the only combination this exists to refuse.

    A table this cannot read answers False. The unreadable table is already an
    error from `open_blocking`, and raising a second one about a cell nobody
    could locate would name a cause that is not the cause.
    """
    rows, col, _errors = verdict_table(reader, lines, rel)
    if col < 0:
        return False
    return any(verdict_of(seen, col) in FIX_WORDS for _line, seen in rows)


def resolves_to(root, sha):
    """The full commit `sha` names in this repository, or None.

    None is *this repository cannot see it*, which after a squash is the
    ordinary state of a reviewed commit rather than a fault. Everything built
    on this treats None as "no claim", the way `check_round` already does for
    a record the pull request does not touch.
    """
    r = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.stdout.strip() or None


def target_shas(reader, root, rel):
    """Every SHA in one record's `Target SHA` row, in the order written.

    The row may name two — `templates/sdd-round.md` says so for a HEAD that
    moved mid-review — and the order is what makes them usable: the first is
    what the round opened, the last is the newest tree it saw.
    """
    text = read_record(root, rel)
    if text is None:
        return []
    rows = table_rows(reader, reader.readable(text))
    return SHA_RE.findall(field(rows, TARGET) or "")


def reviewed_later(reader, root, rel, rows, value, checker_rel):
    """(errors,) — the named checker looked at something after this round did.

    The round NUMBER being higher is not that fact. Two records can carry the
    same `Target SHA`, and then round 2 reviewed the tree round 1 reviewed:
    the fixes that closed round 1 were written after both, so round 2 cannot
    have opened them however its file is numbered. Rounds are also cheap to
    number and expensive to run.

    Both sides are read at their NEWEST tree, which is `mine[-1]` and
    `theirs[-1]`. `templates/sdd-round.md` lets the row name two SHAs — *both,
    if HEAD moved mid-review* — and comparing the checker's newest against
    this record's FIRST was a hole rather than a nicety: round 1 writing
    `A and B` and round 2 writing `B` passed, where two records at one shared
    SHA correctly failed. A round that read exactly what this round read has
    seen nothing new, and how many SHAs each row happens to list does not
    change that.

    Only positively established inversions are refused, never an absence:

      the same commit          both records' newest trees are one commit,
                               compared as resolved commits where the
                               repository still carries them and as the whole
                               written sets where it does not
      strictly earlier         the checker's newest tree is an ANCESTOR of
                               this record's newest

    Anything else passes, the unrelated-commit case included. A squash
    discards the commits a round reviewed, so *cannot be compared* is the
    ordinary state of a merged record and failing there would fail history
    for being history.
    """
    mine = SHA_RE.findall(field(rows, TARGET) or "")
    theirs = target_shas(reader, root, checker_rel)
    if not mine or not theirs:
        return []

    same = f"`{CHECKED_BY}` names `{value}`, and that record reviewed the "
    same += "same commit this one did. A round that looked at the same tree "
    same += "cannot have opened the fixes that closed this round — those "
    same += "were written after it ended. The number is later; the review "
    same += "is not"

    mine_head, theirs_head = resolves_to(root, mine[-1]), resolves_to(root, theirs[-1])
    if mine_head is None or theirs_head is None:
        return [(rel, 0, same)] if set(mine) == set(theirs) else []
    if mine_head == theirs_head:
        return [(rel, 0, same)]
    if is_ancestor(root, theirs_head, mine_head):
        return [
            (
                rel,
                0,
                f"`{CHECKED_BY}` names `{value}`, and that record's "
                f"`{TARGET}` is an ancestor of this one's — it reviewed an "
                "EARLIER tree. A round numbered later that looked at an "
                "earlier commit read none of the fixes this round's findings "
                "were closed by",
            )
        ]
    return []


def item_began(rel):
    """The unix second in `seal/specs/<seconds>-<slug>/rounds/round-N.md`, or None.

    None is the grandfathered answer, and deliberately so. A repository that
    names its work items some other way has no date to compare, and failing
    its records would be failing them for a naming convention rather than for
    a state anybody chose.
    """
    parts = rel.replace("\\", "/").split("/")
    if len(parts) < 3:
        return None
    began = parts[-3].split("-", 1)[0]
    return int(began) if began.isdigit() else None


def pass_checked(lines):
    """True, False, or None when the record carries no `Pass` checkbox.

    One reader, not two. `check_round` asks whether the box is checked and so
    does the refusal for `Pass` beside `nobody`; a second scan of the same
    lines is how two readers of one record start disagreeing about it.
    """
    for line in lines:
        m = PASS_RE.match(line)
        if m:
            return m.group(1).lower() == "x"
    return None


def nobody_reason(value):
    """The reason after `nobody`, `""` when none was given, or None.

    None means the cell is not a `nobody` at all — `nobodys` is a word this
    does not recognise, and recognising it would be the tolerant read the
    vocabulary exists to refuse.
    """
    if not value.startswith(NOBODY):
        return None
    rest = value[len(NOBODY) :]
    if rest and rest[0] not in SEPARATORS:
        return None
    return rest.strip(SEPARATORS)


def checked_by(reader, routing, root, rel, siblings, last=False):
    """(errors, notices) for one record's `Fixes checked by` row.

    `siblings` maps every `round-N.md` git carries in this work item to its
    path, so a named checker is confirmed against the repository rather than
    taken on the record's word — that it exists, and that it looked at
    something later than this record did.

    `last` is true for the record that carries the review's `Pass` verdict,
    and it is what makes the refusal for `Pass` beside `nobody` reachable. On
    an earlier record `Pass` says nothing about the whole review, so a checked
    box there is not the claim this refuses.

    EVERY record, where `Pass` is read on the last one alone, and the two
    scopes are different for a reason that is not symmetry. `Pass` is a
    verdict on the whole review, and the last round's is the one that speaks.
    This is a fact about ONE round's fixes, and every round has its own.

    Reading only the last record made the `round-N` value unreachable, which
    is worth recording because a vocabulary value nothing can use is a
    vocabulary value nobody will notice is dead: a checker has to be a LATER
    round, the last record has none by construction, so the only values it can
    ever hold are `no fixes to check` and `nobody`. Found by mutating the
    sibling lookup and watching the case that was supposed to cover it stay
    green.
    """
    text = read_record(root, rel)
    if text is None:
        return [(rel, 0, "git does not carry this file at HEAD")], []
    lines = reader.readable(text)
    rows = table_rows(reader, lines)
    cell = field(rows, CHECKED_BY)
    if cell is None:
        return [
            (
                rel,
                0,
                f"no `| {CHECKED_BY} | … |` row. `Pass` says this round's "
                "findings are closed; it cannot say who opened the work that "
                f"closed them, and the last round's fixes are the one set no "
                f"later round reads. Write `round-N` (a LATER round), "
                f"`{NO_FIXES}`, or `{NOBODY} — <why>`",
            )
        ], []
    value = reader.visible(cell).strip().strip("`").strip().rstrip(".").lower()
    mine = routing.round_number(os.path.basename(rel))

    if CHECKER_RE.match(value):
        name = value if value.endswith(".md") else f"{value}.md"
        number = routing.round_number(name)
        if number is not None and mine is not None and number <= mine:
            return [
                (
                    rel,
                    0,
                    f"`{CHECKED_BY}` names `{value}`, which is this round or "
                    "one that ran before these fixes existed. A round cannot "
                    "check its own fixes — that is the fixer certifying its "
                    "own work, and it is the state this field was added to "
                    "make visible. Only a LATER round can have opened them",
                )
            ], []
        if name not in siblings:
            return [
                (
                    rel,
                    0,
                    f"`{CHECKED_BY}` names `{value}`, and git carries no "
                    f"such record in this work item (it carries "
                    f"{', '.join(sorted(siblings)) or 'none'}). A checker "
                    "nobody can open is not a checker",
                )
            ], []
        return reviewed_later(reader, root, rel, rows, value, siblings[name]), []

    if value == NO_FIXES:
        if closed_with_a_fix(reader, lines, rel):
            return [
                (
                    rel,
                    0,
                    f"`{CHECKED_BY}` says `{NO_FIXES}` while a verdict in "
                    "this round's own table closed on a fix. Both cannot be "
                    "true, and this is the same contradiction-inside-one-file "
                    "that a checked `Pass` beside an open "
                    f"{BLOCKING} is",
                )
            ], []
        return [], []

    reason = nobody_reason(value)
    if reason == "":
        return [
            (
                rel,
                0,
                f"`{CHECKED_BY}` says `{NOBODY}` and does not say why. The "
                "reason is the whole of what makes this readable — without "
                "it the cell records that something is missing and not what",
            )
        ], []
    if reason is None:
        # Every other word. Strict, the way `hooks/routing.py` is strict about
        # the Review and Destination axes: a value outside the vocabulary is
        # not a value. Read loosely, `the session that wrote them` would pass
        # as an answer, and that is precisely the state this field exists to
        # refuse. The direction is the one `CLOSED_WORDS` takes for a verdict
        # cell — a word this cannot read is never the reassuring reading.
        return [
            (
                rel,
                0,
                f"`{CHECKED_BY}` is `{cell.strip()}`, which is none of the "
                f"three values. Write `round-N` naming a LATER round, "
                f"`{NO_FIXES}`, or `{NOBODY} — <why>`. A session, an agent or "
                "a name is not one of them: the fixes were opened by a round "
                "that reported on them, or they were opened by nobody",
            )
        ], []
    began = item_began(rel)
    if last and pass_checked(lines) and began is not None and began >= STRICT_FROM:
        return [
            (
                rel,
                0,
                f"`Pass` is checked beside `{CHECKED_BY}: {cell.strip()}`. A "
                "run cannot claim to have passed while the fixes that closed "
                "its findings were opened by nobody — that is the state #33 "
                "measured, at a 100% hit rate on the one set of fixes anybody "
                "ever looked at. The way out costs no round: spawn one "
                "verifying round at the diff of those fixes, and a round that "
                "opens nothing needing a fix does not consume the cap. This "
                f"record's cell then names it and the new record reads "
                f"`{NO_FIXES}`. Work items begun before {STRICT_FROM} are "
                "excused this and print instead",
            )
        ], []
    return [], [
        (
            rel,
            0,
            f"`{CHECKED_BY}` is `{cell.strip()}` — the fixes that closed this "
            "round were opened by nobody. This does not fail the pull "
            "request, and it is printed on every run so that the state lives "
            "in the diff rather than in a session that has ended",
        )
    ]


def says_none(value):
    """True when a fix-surface cell answers `none`, reason or no reason.

    The reason is allowed for the same cause a tail is allowed after a
    verdict word: `none — the fixes are not yet written` is the honest
    mid-run value, and refusing it would refuse the truth. The boundary is a
    separator, so `nonempty` is not a `none` — the tolerant read this file
    refuses everywhere else.
    """
    s = EMPHASIS.sub("", value).lower().strip().rstrip(".").strip()
    if s == NONE_WORD:
        return True
    if not s.startswith(NONE_WORD):
        return False
    rest = s[len(NONE_WORD) :]
    return bool(rest) and rest[0] in SEPARATORS


def fix_surface(reader, root, rel):
    """(errors, notices) for one record's `Contract changes` and `New units`.

    Read on EVERY record, like `checked_by` and for the same reason: every
    round has its own fixes. The grandfathering is `item_began` against
    `SURFACE_FROM`, and it reaches only the ABSENT row — a row that is
    present and malformed fails on any record, because an empty cell or a
    unit with no reach is always the author's to fix, where a review nobody
    ran is not.

    An unreadable record returns nothing: `checked_by` already reports that
    state, and a second error naming a different cause would name a cause
    that is not the cause.

    Known limit, recorded rather than parsed away: the arrow is found by
    substring, so an ASCII `->` inside a backticked unit name reads as the
    reach separator and a unit named `operator->` passes without its reach.
    `→` is the spelling that avoids it. Parsing code spans to close the gap
    would be an enumeration over an unbounded domain — the closing the
    review skill's own rules refuse.
    """
    text = read_record(root, rel)
    if text is None:
        return [], []
    rows = table_rows(reader, reader.readable(text))
    began = item_began(rel)
    excused = began is None or began < SURFACE_FROM
    errors, notices = [], []
    for label, bought in (
        (
            CONTRACT,
            "the largest regression class measured in #57 — a fix changed "
            "a unit's contract, and not every place that contract reaches "
            "was revisited. The diff names the changed signature; this row "
            "is where the reach is named. Write each changed unit with the "
            "call sites it reaches (`unit → site, site`, units separated "
            "by `;`), or `none`",
        ),
        (
            NEW_UNITS,
            "a unit the fixes created has been reviewed by nobody, and the "
            "verifying round treats what this row names as a finding "
            "surface — is this correct — rather than a verification "
            "surface. Write the top-level definitions and constants this "
            "round's fixes added, or `none`",
        ),
    ):
        cell = field(rows, label)
        if cell is None:
            message = f"no `| {label} | … |` row: {bought}"
            if excused:
                notices.append(
                    (
                        rel,
                        0,
                        message + ". This work item began before the rule "
                        "landed, so this prints instead of failing — the "
                        "grandfathering `Fixes checked by` already uses",
                    )
                )
            else:
                errors.append((rel, 0, message))
            continue
        value = reader.visible(cell).strip()
        if not value:
            errors.append(
                (
                    rel,
                    0,
                    f"`{label}` is empty — a row that says nothing answers "
                    "nothing. Write the units, or `none`",
                )
            )
            continue
        if says_none(value):
            continue
        if not EMPHASIS.sub("", value).strip(SEPARATORS + ";"):
            # `;` alone survived both refusals above: not `none`, not empty,
            # and the entry walk below skips every empty entry it yields.
            # Separators with nothing between them say exactly as much as an
            # empty cell, and take the same answer (round 1's 🟡 1).
            errors.append(
                (
                    rel,
                    0,
                    f"`{label}` is `{value}` — separators with nothing "
                    "between them, which says exactly what an empty cell "
                    "says. Write the units, or `none`",
                )
            )
            continue
        if label != CONTRACT:
            continue
        for entry in value.split(";"):
            entry = entry.strip()
            if not entry:
                continue
            arrow = next((a for a in ARROWS if a in entry), None)
            unit, _, reach = entry.partition(arrow) if arrow else (entry, "", "")
            if not arrow or not unit.strip() or not reach.strip():
                errors.append(
                    (
                        rel,
                        0,
                        f"`{CONTRACT}` lists `{entry}` without the call "
                        "sites it reaches. The diff already names the "
                        "changed signature; the reach is the half it does "
                        "not show, and a unit listed without it is the "
                        "unchecked half of the measured failure. Write "
                        "`unit → call site, call site`",
                    )
                )
    return errors, notices


def check_round(reader, root, rel, strict=True, refs=None):
    """(errors,) for one round record — the reachability and the Pass claim.

    Who opened the fixes is NOT read here. `checked_by` is asked of every
    record, this one included, and a function called on the last record alone
    is the wrong place for a question every round has its own answer to.

    `strict` is false only for a draft pull request, where an unchecked
    `Pass` is the honest state of a review still running. It does not reach
    `Fixes checked by`: a record naming a checker it does not have is wrong at
    every stage of a run, where an unchecked box is merely early.

    `refs` is None for a record this pull request does not touch, and then no
    claim is made about where its commits are. Everything else is still read:
    a `Target SHA` row has to be THERE either way, because "which commit did
    this round review" is answerable after a squash even when the commit is
    not, and a record missing the row says nothing about what it looked at
    whatever its age.
    """
    errors = []
    text = read_record(root, rel)
    if text is None:
        return [(rel, 0, "git does not carry this file at HEAD")]

    lines = reader.readable(text)
    rows = table_rows(reader, lines)

    cell = field(rows, TARGET)
    named = SHA_RE.findall(cell or "")
    if not cell or not named:
        errors.append(
            (
                rel,
                0,
                f"no `| {TARGET} | … |` row naming a commit — without it "
                "nobody can tell which commit this round actually looked at",
            )
        )
    looked = list(refs) + declared_pull_head(reader, root, rows) if refs else []
    for sha in named if refs else []:
        found, _carrier = reachable(root, sha, looked)
        if not found:
            errors.append(
                (
                    rel,
                    0,
                    f"`{TARGET}` names {sha}, which is not an ancestor of "
                    f"{' or '.join(looked)} and is on no "
                    f"`{PULL_HEADS}<N>/head` — this round reviewed something "
                    "this repository cannot see. A squash discards the "
                    "reviewed commits and a branch is a name anything can "
                    "delete; the pull request head that carried them is not. "
                    "If this is a checkout that never fetched them, "
                    f"`git fetch origin '+refs/pull/*/head:{PULL_HEADS}*/head'` "
                    "is the missing step and not a lost commit",
                )
            )

    checked = pass_checked(lines)
    if checked is None:
        errors.append(
            (
                rel,
                0,
                "no `- [ ] Pass` checkbox — `was it reviewed` "
                "and `did it pass` are different questions, and without "
                "this one only the first is answerable",
            )
        )
        return errors

    if strict and not checked:
        errors.append(
            (
                rel,
                0,
                "the last round's `Pass` is not checked. In this design "
                "the review chain runs BEFORE the pull request, so an "
                "unchecked `Pass` here means the chain was skipped or has "
                "not finished — neither is a state to open a ready pull "
                "request in. Open it as a draft while the rounds run",
            )
        )

    still_open, table_errors = open_blocking(reader, lines, rel)
    errors.extend(table_errors)
    if checked and still_open:
        for line_no, what, verdict in still_open:
            errors.append(
                (
                    rel,
                    line_no,
                    f"`Pass` is checked, and this "
                    f"{BLOCKING} row reads `{verdict or 'empty'}` — a "
                    "blocking finding that is not fixed, answered or "
                    f"withdrawn: {what}",
                )
            )
    return errors


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="chain-check",
        description="At the pull request: every routing declaration it "
        "touches has the review evidence it claimed.",
    )
    ap.add_argument(
        "--baseline",
        metavar="REF",
        required=True,
        help="the branch this pull request merges into",
    )
    ap.add_argument("--root", default=".", help="the repository to read")
    args = ap.parse_args(argv)

    try:
        reader = load(READER, "specseal_unverified_reader")
        routing = load(ROUTING, "specseal_routing")
    except (OSError, SyntaxError, ImportError, SystemExit) as exc:
        print(
            f"chain-check: the shared reader would not load ({exc}) — nothing "
            "was checked, and reporting a pass for a check that never ran is "
            "worse than failing",
            file=sys.stderr,
        )
        return 2

    root = reader.repo_root(os.path.abspath(args.root))
    if root is None:
        print(
            f"chain-check: {args.root} is not in a git repository — nothing "
            "was compared",
            file=sys.stderr,
        )
        return 2
    if not reader.resolves(root, args.baseline):
        print(
            f"chain-check: --baseline {args.baseline} does not resolve in "
            f"{root} — nothing was compared. A shallow checkout lands here, "
            "and passing it would report a check that never ran",
            file=sys.stderr,
        )
        return 2

    diff = changed(root, args.baseline)
    if diff is None:
        print(f"chain-check: cannot diff against {args.baseline}", file=sys.stderr)
        return 2
    paths, renamed = diff
    touched = set(paths)
    # What the pull request added or edited, plus the one for this branch:
    # the second used to be a fallback for when the first was empty, and the
    # union is what the spec says — a pull request that adds only round
    # records to an item declared in an earlier one is judged on that item,
    # and one that moves every declaration (S10) is judged on its own alone.
    own, why = declared_for_this_branch(root, routing)
    declarations = sorted(
        set(changed_routing(touched, renamed, routing.WORK_ITEMS)) | set(own)
    )

    state, where = pull_request_state()
    strict = state != "draft"
    print(
        f"chain-check: judged as a {'draft' if state == 'draft' else 'ready'} "
        f"pull request ({where})"
    )

    if not declarations:
        # What was NOT checked, not what was not found. "No declaration found"
        # describes this script's own state and reads as routine; this
        # describes the pull request's state, and it is the sentence the next
        # person tightening the check will quote. Which sentence depends on
        # WHY there is none — an author who declared nothing and a run with no
        # key to look one up by are different states.
        print(reader.annotate("notice", "", 0, why))
        return 0

    errors, notices = [], []
    for rel in declarations:
        item = os.path.dirname(rel)
        text = read_record(root, rel)
        if text is None:
            errors.append(
                (
                    rel,
                    0,
                    "git does not carry this file at HEAD. A declaration CI "
                    "cannot open is not a declaration, whatever the working "
                    "tree holds",
                )
            )
            continue
        declared = routing.parse(text)
        if declared is None:
            errors.append(
                (
                    rel,
                    0,
                    "not a readable declaration. It needs `| Review | through the "
                    "review chain |` or `| Review | straight to the PR |`, a "
                    "`| Destination | … |` row, and a `| Branch | … |` row. Read "
                    "loosely this would report `no declaration`, which is what a "
                    "branch that never declared looks like",
                )
            )
            continue

        if declared["review"] == routing.DIRECT:
            print(f"{item}: straight to the PR — declared, nothing required")
            continue

        # Before the count, and reported even when `rounds/` also holds
        # records: a file at the old location is evidence nothing reads, and
        # the count alone cannot say so. Without this the whole migration
        # arrives as `holds no round-N.md`, which names neither the file nor
        # where it goes.
        strays = stray_records(routing, root, item)
        if strays:
            errors.append(
                (
                    rel,
                    0,
                    f"{', '.join(strays)} — a round record git carries at the "
                    f"work item's top level, where nothing reads it. Round "
                    f"records live in {item}/{routing.ROUNDS_DIR}/ now: "
                    f"`mkdir {item}/{routing.ROUNDS_DIR} && git mv` them "
                    f"there — `git mv` does not create its destination. "
                    f"Left where they are, this pull "
                    f"request's only evidence that a review happened is "
                    f"invisible to every reader of it",
                )
            )

        # AFTER the strays, and it keeps its `continue`. Round 3 found the
        # early exit swallowing the stray report: a partial migration — the
        # directory made, one record moved, two left behind — showed only the
        # `rounds` state and named neither straggler, so the person fixed one
        # thing, pushed, and waited for CI to learn about the rest. Where the
        # message is the entire migration path, a round trip per finding is
        # the cost this release exists to remove. The exit still has to
        # happen: past it lies `holds no round-N.md`, the sentence this whole
        # check was added to stop being the only answer.
        if rounds_unreadable(routing, root, item):
            errors.append(
                (
                    rel,
                    0,
                    f"{item}/{routing.ROUNDS_DIR} is not a directory, so "
                    f"nothing can read a round record out of it — and a "
                    f"review that happened reads exactly like one that did "
                    f"not. `git mv … {routing.ROUNDS_DIR}` without the "
                    f"trailing slash does this to a single record. Open it: "
                    f"if it is your round record, `mkdir` the directory and "
                    f"move it inside",
                )
            )
            continue

        records = round_records(routing, root, item)
        if not records:
            if strays:
                continue
            errors.append(
                (
                    rel,
                    0,
                    f"declares `{routing.CHAIN}` and {item}/{routing.ROUNDS_DIR}/ "
                    "holds no `round-N.md`. The round record is this pull "
                    "request's only evidence that a review happened — the local "
                    "`specseal-reviewed` mark cannot travel here",
                )
            )
            continue
        last = records[-1]
        refs = target_refs(reader, root, declared) if last in touched else None
        print(
            f"{item}: through the review chain — {len(records)} round "
            f"record(s), last is {os.path.basename(last)}, "
            + (
                f"its target must be reachable from {' or '.join(refs)}, "
                f"or from the `{PULL_HEADS}<N>/head` that carried it"
                if refs
                # What this established, not what it concluded. `already merged`
                # was the claim here, and it is one the code cannot make -- it
                # knows the path was not in the diff and nothing more. Saying it
                # the wrong way is what made a quoted path read as routine
                # instead of as the dropped check it was.
                else "not changed by this pull request — no claim made about "
                "where its commits are"
            )
        )
        errors.extend(check_round(reader, root, last, strict, refs))

        # EVERY record, where the block above reads the last one alone. Who
        # opened a round's fixes is a fact about that round, and each has its
        # own; the `Pass` verdict is a claim about the whole review, and the
        # last round's is the one that speaks for it.
        #
        # Keyed by basename, because `checked_by` is confirming a name a
        # person wrote in a cell (`round-4`) and the directory it sits in is
        # already fixed by `round_records`. The path is the value, so the
        # named record can be opened and its `Target SHA` compared.
        siblings = {os.path.basename(p): p for p in records}
        for record in records:
            who_errors, who_notices = checked_by(
                reader, routing, root, record, siblings, last=record == last
            )
            errors.extend(who_errors)
            notices.extend(who_notices)
            surface_errors, surface_notices = fix_surface(reader, root, record)
            errors.extend(surface_errors)
            notices.extend(surface_notices)

    for rel, line, message in notices:
        print(reader.annotate("notice", rel, line, message))
    for rel, line, message in errors:
        print(reader.annotate("error", rel, line, message))
    return 1 if errors else 0


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
