#!/usr/bin/env python3
"""settle — name the released work items a policy document has yet to absorb.

`seal/README.md` has said a work item's directory "waits until a later
`settle` folds it" since the root existed, and nothing was ever built. The
directory therefore never stops growing: 98 work items, 1,338 files, 15M on
the tree this shipped from, and no check reads any of it after the merge.

**This reads, groups and records. It never writes prose and it never judges.**
`docs/one-root-by-lifetime.md` §*What keeps `settle` light* says the step
"moves and does not verify", and folding *only what is still true* is exactly
a judgment about truth — so the standing statement each segment gets is
written by the session, following `skills/settle/SKILL.md`, and this command
supplies the corpus it is written from. A script that wrote the prose itself
would either splice 97 sentences up under their provenance comments, which is
a move and not a compaction, or assert that each moved sentence still holds,
which is the one thing the clause above forbids.

  settle                        what would fold, grouped by segment
  settle --retire               remove the directories whose fold is recorded,
                                and the released ones with no spec.md and
                                nothing open
  settle --released-at REF      what counts as released (default origin/main)
  settle --root DIR             a repository other than this one

**Released means present on the branch the release merges to**, which is why
`--released-at` names a ref rather than a date. The two alternatives were
measured on this repository and both are wrong: 11 work items carry no
`<!-- specs/<id> -->` marker in `CHANGELOG.md` although they plainly shipped,
and 15 carry none in `seal/ledger.md`.

**The fold record is the provenance comment, and there is no second file.**
A folded sentence carries `<!-- specs/<work-item-id> -->` in the `docs/`
document it landed in — the marker `.github/scripts/fold_ledger.py#marker`
and `.github/scripts/gather_changelog.py#marker` already write — so the
record is derived from the destination and cannot disagree with it. Reading
it is `skills/verify/scripts/unverified_check.py#folded_items`, loaded here
rather than re-spelled: that module is the fold record's one reader, and the
same arm of `unverified-check` is what would otherwise call a retirement this
branch's deletion.

**The guards.** A work item whose `evidence-todo.md` still has an open row is
skipped and named, never folded and never removed. A fact a reviewer verified
that never reached the ledger is exactly what the directory must not take
with it. And a directory a live ledger row anchors into is kept, with the row
named and what `CLAUDE.md` requires of it (#511): removing the directory
would leave the row BROKEN, and the checker would only say so afterwards.

**Two halves, and the retirement is the second.** The command lists what a
session has to write policy for; `--retire` removes the directories whose
policy was written, which the marker is the proof of. Nothing that states a
rule is removed without one, so the failure this arrangement can produce is a
thin policy document, which a reader can see, rather than a directory deleted
with nothing absorbing it, which nobody can.

**The rule arm, and why it needs no marker.** A released work item that wrote
no `spec.md` states no rule — a release entry, a renumbering, a CI repair —
so there is nothing for a document to absorb, and #517's owner decision D3
retires it by that rule rather than by a record. One condition narrows it:
nothing in its record may be open, because an open `## Not verified` or
`evidence-todo.md` row is a claim with an answerer, not a rule. Whether a
directory qualifies is `unverified_check.py#retired_by_rule`, the predicate
every CI reader asks of the merge-base, asked here of the working tree.

**Local mode is refused rather than reported on.** A root under the common
git directory is never committed, so no ref holds the work item directories,
nothing in them reads as released, and nothing removed from them could be
recovered. `seal mode shared` moves the root into the tree and this command
works from there. A repository that opted out with the scratch marker is
refused too, and told which of the two it is. The marker is an empty FILE
under the common git directory, read the way `hooks/optin.py#home_at` reads
it; a directory of that name is not one, and is refused as no root.

Exit codes: 0 the report was produced, or the retirement ran, or the root
holds no work item at all — an empty or absent `seal/specs/` under a present
`seal/` is the state a complete fold reaches · 1 a retirement was asked for
and something refused it · 2 the arguments or the tree were unusable, which
is five states: a `--released-at` ref that does not resolve,
a root at neither place, a root in local mode, a repository that opted out,
and an interpreter below the floor.
"""

import argparse
import collections
import glob
import importlib.util
import os
import re
import shutil
import subprocess
import sys

# **The interpreter floor, copied from
# `skills/code-review/scripts/round_record.py#below_floor`**, which is written
# to be copied and says so. Two things about its shape are load-bearing, and
# they are the reason it is copied rather than imported. It sits after the
# imports and not after `import sys`, because ruff's E402 is selected and
# every shipped script is measured to compile under 3.9, so no import above it
# can fail first. And it uses no syntax newer than the oldest interpreter it
# means to catch — no walrus, no f-string — since a guard that cannot parse is
# the traceback it exists to replace.
#
# A read that can fail gives the guard a second way to die on the one machine
# that has no other way of being told what is wrong, which is why the floor is
# spelled here instead of imported;
# `tests/test_a_script_says_which_interpreter_it_needs.py` pins this number to
# the runner's and to `ruff.toml`'s.
FLOOR = (3, 12)
FLOOR_TEXT = ".".join(str(part) for part in FLOOR)
BELOW_FLOOR = (
    "settle: needs python {floor} or newer, and this is python {found} "
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
READER = os.path.join(HERE, "..", "..", "verify", "scripts", "unverified_check.py")
CHECKER = os.path.join(
    HERE, "..", "..", "evidence-check", "scripts", "evidence_check.py"
)
OPTIN = os.path.join(HERE, "..", "..", "..", "hooks", "optin.py")

SPECS = "seal/specs"
LEDGER = "seal/ledger.md"
FRAGMENTS = "seal/ledger"
RELEASES = "seal/releases"
TESTS = "tests/"

# `path#anchor@hash`, narrowed to the one group this reads. The full shape is
# `skills/evidence-check/scripts/evidence_check.py#ANCHOR_RE`, which resolves
# the anchor and the hash as well; nothing here opens the code a row cites, so
# the path is the whole of what a segment is derived from.
COORDINATE_RE = re.compile(
    r"(?P<path>[A-Za-z0-9_@.][A-Za-z0-9_.@/-]*[/.][A-Za-z0-9_.@/-]*?)"
    r"#(?:\"(?:[^\"\n]|\\\")+\"|[A-Za-z_][A-Za-z0-9_.]*)"
    r"(?:>\"(?:[^\"\n]|\\\")+\")?"
    r"@[0-9a-f]{6,12}"
)
MARKER_LINE_RE = re.compile(r"^<!-- specs/(\S+) -->$", re.M)


def under(root, rel):
    """The disk path of a `/`-joined repository-relative path."""
    return os.path.join(root, *rel.split("/"))


def plural(count):
    """`s` unless there is one of them. Every count this prints is read by a
    person, and `1 work items` is the tell that nobody read the output."""
    return "" if count == 1 else "s"


def load(path, name):
    """Import a sibling script by path, or refuse with a sentence.

    Not a bare `exec_module`: `spec_from_file_location` hands back a spec for
    any path ending in `.py`, present or not, so a missing reader reaches the
    loader and raises `FileNotFoundError` — a traceback where this file's
    whole contract is that every failure is a sentence. That is the shape the
    rider on `round_record.py#load` is still waiting for somebody to fix; it
    arrives written here rather than copied broken.
    """
    if not os.path.isfile(path):
        raise SystemExit(
            f"settle: cannot read {path}, and it is where the fold record is "
            "read from. This command ships beside it under `skills/`; a copy "
            "of one script taken on its own is not a plugin."
        )
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"settle: cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- what the tree says ----------------------------------------------------


def work_items(root):
    """Every work item id with a directory under `seal/specs/`, in id order."""
    top = under(root, SPECS)
    if not os.path.isdir(top):
        return []
    return sorted(
        name for name in os.listdir(top) if os.path.isdir(os.path.join(top, name))
    )


def released(root, ref):
    """Work item ids whose directory is present at `ref`, or None if it is not.

    A work item is released when the branch the release merges to holds its
    directory, which is a question only git can answer. None is returned for
    a ref that does not resolve, and the caller refuses: a ref this cannot
    read would otherwise make every work item read as unreleased and the
    whole report as "nothing to fold", which is the quiet zero every checker
    in this plugin is written against.
    """
    r = subprocess.run(
        ["git", "-C", root, "ls-tree", "-r", "--name-only", ref],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        return None
    prefix = SPECS + "/"
    found = set()
    for line in r.stdout.splitlines():
        if line.startswith(prefix):
            rest = line[len(prefix) :]
            if "/" in rest:
                found.add(rest.split("/", 1)[0])
    return found


def open_rows(text):
    """Table body rows of an evidence-todo file that are still open.

    The rule is `unverified_check.py#todo_open_rows`, and its docstring says
    how a person applies it by hand. It moved there when the rule arm's
    predicate began reading `evidence-todo.md` too: the guard here and the
    predicate every CI reader asks are one rule, not two copies of it.

    **`.github/scripts/fold_ledger.py#open_rows` is the same function**,
    loaded by path from the shipped reader (#487). The direction that is
    closed is the other one: that script is this repository's own release
    automation, not on the list of what the plugin ships
    (`tests/test_the_release_check_watches_what_ships.py#SHIPS`), so a shipped
    command may not depend on IT — a user's repository has the ledger fold
    nowhere. The guard travels with the command that enforces it.
    """
    return load(READER, "specseal_unverified_reader").todo_open_rows(text)


def open_items(root):
    """{work item id: open row count} for every one the guard is holding."""
    out = {}
    for path in sorted(
        glob.glob(os.path.join(under(root, SPECS), "*", "evidence-todo.md"))
    ):
        with open(path, encoding="utf-8") as f:
            rows = open_rows(f.read())
        if rows:
            out[os.path.basename(os.path.dirname(path))] = len(rows)
    return out


# --- what groups -----------------------------------------------------------


def coordinates(root):
    """{work item id: [the path of each ledger coordinate it wrote]}.

    Three addresses hold the rows and all are read, which is what the checker
    does: `seal/ledger.md`, the rows from before the fragments existed and,
    until `fold_ledger.py --split` moves them, the sections a release folded
    there; `seal/releases/<X.Y.Z>.md`, one file per release, where the fold
    writes each work item's section under its own `<!-- specs/<id> -->`
    marker (#547); and `seal/ledger/<id>.md`, the fragment of a work item
    whose release has not folded it yet.

    A section runs from its marker to the next marker or the next `##`
    heading, which is exactly what `fold_ledger.py#section` writes, and a
    release file is that section byte for byte — one `## ` line, then the
    markers — so one loop reads the shared ledger and every release file.
    Rows above the first marker belong to no work item — they are the rows
    from before the fragments existed, and the ledger's own header says so.

    **A line has to be live, by the one rule the reader owns.** A line anchor
    is not a test that the line is live — round 1's finding 1, met here twice:
    a fenced example opens no section (round 2's finding 5) and neither does a
    marker inside a commented-out draft (round 3's finding 2). Either would
    attribute every coordinate after it to the id in the quotation, and the
    segment the report prints would be wrong for two work items at once.

    Both loops below read through `unverified_check.py#live_lines`, the same
    function `folded_items` reads through, rather than a copy of any part of
    the rule. A line is live there when it BEGINS outside a fence, outside a
    comment and outside a code span, answered by one scan carrying all three
    states; the line comes back unchanged, and the coordinate still sits
    inside its backticks.

    The comment state cannot be asked of the raw text, which is what makes
    the code-span state part of the same question: a ledger anchor quotes the
    text it points at, and measured 2026-09-22 four rows of `seal/ledger.md`
    held `<!--` inside backticks with no closer on the line — asking the
    comment state of the file as it stood lost three real section markers.
    The count is a reading of one day's file and grows at every release fold;
    what the rule rests on is that such rows exist, not that there are four.
    That reader answered this with three passes in sequence for four review
    rounds, and each formulation had a shape it got wrong; `live_lines`'s own
    docstring carries why a sequence could not answer it.

    **A THIRD quotation is out of scope, and it is named here so it is not
    met as a surprise:** markdown's indented code block. The fence delimiter
    rule the ledger readers share, `unverified_check.py#fence_opener`, knows the
    two fenced forms only, so a fragment that shows its example row indented
    four spaces has that example counted as its own coordinate. Teaching the
    shared rule an indented block would move `readable`, `check_text`,
    `round_record.py` and the review-history guard at once — measured
    2026-09-22, one such widening reddens
    `tests/test_the_record_is_generated.py#test_a_continuation_that_looks_like_an_opener_is_still_joined`,
    a record reader with no stake in this rule. `reader_blanking_passes` is
    NOT that refusal and does not fire here: it reads the calls `readable`
    makes by name, and a widened `blank_fences` leaves that set unchanged. It
    refuses a pass ADDED to `readable`, which is a different alternative.
    The ledger and every fragment here carry rows as tables and an example as
    a fence, so the shape is answered by convention rather than by the reader.
    `FOLD_MARKER` is line-anchored, so `folded_items` is not reachable this
    way at all — measured 2026-09-22, an indented marker returns the empty
    set. `tests/test_settle_reads_before_it_removes.py#test_an_indented_example_row_is_counted_and_the_reader_says_so`
    pins the decision, so a session that widens the reader is told what this
    one chose.
    """
    out = collections.defaultdict(list)
    live_lines = load(READER, "specseal_unverified_reader").live_lines
    ledgers = [
        under(root, LEDGER),
        *sorted(glob.glob(os.path.join(under(root, RELEASES), "*.md"))),
    ]
    for ledger in ledgers:
        if not os.path.isfile(ledger):
            continue
        with open(ledger, encoding="utf-8") as f:
            current = None
            for line, live in live_lines(f.read().split("\n")):
                if not live:
                    continue
                marker = MARKER_LINE_RE.match(line)
                if marker:
                    current = marker.group(1)
                    continue
                if line.startswith("## "):
                    current = None
                if current:
                    out[current] += [
                        m.group("path") for m in COORDINATE_RE.finditer(line)
                    ]
    for path in sorted(glob.glob(os.path.join(under(root, FRAGMENTS), "*.md"))):
        work_item_id = os.path.basename(path)[: -len(".md")]
        with open(path, encoding="utf-8") as f:
            for line, live in live_lines(f.read().split("\n")):
                if live:
                    out[work_item_id] += [
                        m.group("path") for m in COORDINATE_RE.finditer(line)
                    ]
    return out


# --- what a removal would break --------------------------------------------

AnchoredRow = collections.namedtuple("AnchoredRow", "file line clause dead live items")

# A cell boundary: a pipe no backslash escapes. A ledger anchor that quotes a
# table line escapes the pipes it holds, and splitting on those would hand the
# report a fragment of the anchor as the row's first cell.
CELL_RE = re.compile(r"(?<!\\)\|")

# What the guard prints for each verdict. Pinned by
# `tests/test_settle_reads_before_it_removes.py`, because a person acts on it.
REMOVED_SAYS = (
    "REMOVED — every anchor it cites lies inside a directory a retirement "
    "removes, and `CLAUDE.md` says a row whose anchor a change removes is "
    "REMOVED, not re-pointed; its claim is written anew where it still stands"
)
NARROW_SAYS = (
    "narrow — drop the anchor{s} inside a retiring directory and keep the "
    "{live} live one{live_s}; whether such a row is removed instead is the "
    "repository owner's question (`seal/ledger.md` §1788354065's S12 row)"
)


# What a settled root prints, for the report and the retirement alike.
SETTLED = (
    "settle: {specs}/ in {root} holds no work item — nothing to fold and "
    "nothing to retire. A complete fold ends here, and git keeps no empty "
    "directory, so a fresh checkout of this state has no {specs}/ at all.\n"
)

# The rule arm's headings, and the listings D1's table asks the command to
# print by itself. Pinned by `tests/test_settle_reads_before_it_removes.py`.
RULE_HEADING = (
    "retired by the rule — released, no `spec.md`, nothing open; "
    "`settle --retire`\nremoves these with no marker, because a moment "
    "states no rule to fold:"
)
RULE_KEPT_HEADING = (
    "kept by the rule — no `spec.md`, but the record still holds an open "
    "row, which\nleaves by being closed (✅ with what closed it) in a pull "
    "request merged before the\none that retires the directory, never with it:"
)
TAKES_HEADING = (
    "what a retirement here would take with it — read each before `settle --retire`:"
)
READERS_HEADING = (
    "checks that read `seal/specs` — each owes an answer by "
    "`skills/settle/SKILL.md` §3\nbefore the directories go:"
)


def write_rule_kept(kept, out):
    """Each spec-less directory the rule arm keeps, with every open row."""
    for work_item_id, rows in kept:
        out.write(f"    {work_item_id}\n")
        for name, item in rows:
            out.write(f"        open in {name}: {item}\n")
        if not rows:
            out.write(
                "        the rule's predicate refused it with nothing open read\n"
            )


def first_cell(line):
    """The first cell of a table row, which names the row's claim.

    A row commented out on its own line still carries an anchor the checker
    reads, so the guard names it; the comment opener in front of it is not
    the claim (round 2's finding 7)."""
    text = line.strip()
    if text.startswith("<!--"):
        text = text[len("<!--") :].strip()
    cells = CELL_RE.split(text)
    if len(cells) > 1 and not cells[0].strip():
        cells = cells[1:]
    return cells[0].strip() if cells else ""


def anchored_rows(root, work_item_ids):
    """Every live ledger row with an anchor inside one of these directories.

    #511. A retirement used to remove a directory a ledger row anchored into,
    and the checker then reported the row BROKEN — found twice on one branch,
    both times after the fact. This is the read that answers it before
    anything is removed.

    **It is not `coordinates`, and it cannot be.** That reader attributes a
    row to the work item whose `<!-- specs/<id> -->` section holds it, and
    skips every row above the first marker, which is exactly where this
    repository's one anchored row sat. What this asks is only whether an
    anchor's PATH lies under `seal/specs/<id>/`, whoever wrote the row, so it
    reads every ledger the checker reads, asked of the checker itself
    (`evidence_check.py#default_patterns` — `seal/ledger.md`, every
    `seal/ledger/*.md`, every `seal/releases/*.md`, and the pre-0.10
    `docs/**/_evidence.md`), with the one coordinate shape, `COORDINATE_RE`.

    **Every line, a fenced or commented one included.** The checker reads a
    commented row and a row inside a fence that never closes, so either is
    BROKEN after the removal like any other. This used to read through
    `unverified_check.py#live_lines`, whose ambiguous line is settled as *not
    live*: that bias keeps a directory for the marker reader and removed one
    here, which was #511 again one step narrower (round 1's finding 1). A
    guard that reads fewer lines or fewer files than the checker keeps fewer
    directories than the checker will report broken. Since #444 the checker
    skips a row inside a fence that closes, and this still reads one, which
    keeps a directory the checker would not break — the direction to be wrong
    in, since a kept directory is a sentence and a removed one is not.

    It reads and names; it never edits the ledger. Which row goes is a
    judgment about a claim, and `docs/one-root-by-lifetime.md` §*What keeps
    `settle` light* keeps that out of the command.
    """
    prefixes = {f"{SPECS}/{i}/": i for i in work_item_ids}
    if not prefixes:
        return []
    checker = load(CHECKER, "specseal_evidence_checker")
    sources = []
    for path in checker.resolve_patterns(checker.default_patterns(root)):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if rel not in sources:
            sources.append(rel)
    found = []
    for rel in sources:
        with open(under(root, rel), encoding="utf-8") as f:
            lines = f.read().split("\n")
        for number, line in enumerate(lines, start=1):
            paths = [m.group("path") for m in COORDINATE_RE.finditer(line)]
            dead, items = [], set()
            for path in paths:
                for prefix, work_item_id in prefixes.items():
                    if path.startswith(prefix):
                        dead.append(path)
                        items.add(work_item_id)
            if dead:
                found.append(
                    AnchoredRow(
                        rel,
                        number,
                        first_cell(line),
                        dead,
                        len(paths) - len(dead),
                        sorted(items),
                    )
                )
    return found


def verdict(row):
    """What `CLAUDE.md` requires of one anchored row, as a person reads it."""
    if not row.live:
        return REMOVED_SAYS
    return NARROW_SAYS.format(
        s=plural(len(row.dead)), live=row.live, live_s=plural(row.live)
    )


def write_anchored(rows, out):
    """One block per row: where it is, what it claims, where it points, and
    what `CLAUDE.md` says to do with it."""
    for row in rows:
        out.write(f"    {row.file}:{row.line}  {row.clause}\n")
        out.write(f"        into {', '.join(row.items)}\n")
        out.write(f"        {verdict(row)}\n")


def segment_of(paths):
    """`(segment, reason)` for one work item's coordinate paths.

    The segment is the enclosing file of the work item's ledger anchors,
    which is what `spec.md` §*What groups* fixes, and it is decided by
    majority rather than by the first row: a work item cites several
    coordinates and the one it cites most is the code it is about.

    **A `tests/` anchor rolls up to the segment of the code it pins**, and
    this is the rule that decides it — Q2, against the real corpus, where 852
    of 1,772 coordinates are under `tests/`. A case that pins
    `round_record.py`'s behaviour is evidence about `round_record.py`, so a
    work item's test anchors are dropped in favour of its code anchors, and
    they carry no segment of their own.

    What that leaves is named rather than guessed, which is the other half of
    Q2's default. A work item whose anchors are ALL under `tests/` pins code
    this file cannot name: the link from a case to the code it pins is
    nowhere a machine reads, and inventing it from a filename is the second
    mechanism `plan.md` rejected building before the first one exists. Such
    an item is returned ungrouped with `tests only` as its reason, and so is
    one with no ledger row at all.
    """
    if not paths:
        return None, "no ledger row"
    code = [p for p in paths if not p.startswith(TESTS)]
    if not code:
        return None, "tests only"
    counted = collections.Counter(code)
    best = max(counted.values())
    return sorted(p for p in counted if counted[p] == best)[0], None


# --- the report ------------------------------------------------------------


def survey(root, ref):
    """What the report is derived from, and where the retirement gets released.

    One walk for the listing, so no work item appears in two of its lists.

    **The retirement does not take its candidates from here.** `retire` reads
    the markers, the directories and the guard from the tree again, and its
    own docstring says why: a classification made for a printed list is not a
    guard on a destructive act. This sentence used to say the opposite — that
    the retirement was derived from this walk, and that a second traversal was
    the failure mode to avoid — which after round 1's finding 4 was the stale
    half of a contradiction, and the half a reader meets first. Left standing
    it invites the next editor to simplify `retire` back to `found["folded"]`,
    which is exactly the mutation that reopens that finding.

    What the retirement does take from here is `released`, which only git can
    answer and which this has already asked.
    """
    present = work_items(root)
    on_base = released(root, ref)
    if on_base is None:
        return None
    reader = load(READER, "specseal_unverified_reader")
    folded = reader.folded_items(root)
    held = open_items(root)
    rows = coordinates(root)

    survey = {
        "released": [i for i in present if i in on_base],
        "unreleased": [i for i in present if i not in on_base],
        "folded": [],
        "skipped": [],
        "grouped": collections.defaultdict(list),
        "ungrouped": [],
        "anchored": [],
        "rule": [],
        "rule_kept": [],
        "retiring": [],
        "takes": {},
        "citations": {},
        "readers": [],
    }
    # Every released directory, folded or not, because this list is for the
    # session writing the prose: a row it sees now is answered before the
    # retirement, rather than found by a red `evidence-check` after it.
    survey["anchored"] = anchored_rows(root, survey["released"])
    for work_item_id in survey["released"]:
        # The guard is asked first. `spec.md` G3 says an item with an open row
        # is skipped AND NAMED, never folded — and an item that was both
        # folded and held used to be named under "waiting to be retired",
        # which tells the reader to run the command that will refuse it, while
        # the summary counted it `0 skipped`. `retire()` reads `open_items`
        # again and keeps the directory either way; what this decides is what
        # the reader is told before running anything.
        if work_item_id in held:
            survey["skipped"].append((work_item_id, held[work_item_id]))
            continue
        if work_item_id in folded:
            survey["folded"].append(work_item_id)
            continue
        # D3: a released work item with no `spec.md` states no rule, so there
        # is nothing to place and it is not "ungrouped". Whether the rule arm
        # takes it is the predicate's answer, the one every CI reader asks of
        # the merge-base; this only asks it of the working tree.
        if not has_spec(root, work_item_id):
            directory = f"{SPECS}/{work_item_id}"
            if reader.retired_by_rule(root, None, directory):
                survey["rule"].append(work_item_id)
            else:
                survey["rule_kept"].append(
                    (work_item_id, reader.open_record_rows(root, None, directory))
                )
            continue
        segment, reason = segment_of(rows.get(work_item_id, []))
        if segment is None:
            survey["ungrouped"].append((work_item_id, reason))
        else:
            survey["grouped"][segment].append(work_item_id)

    # What a retirement here would take with it, by either arm: D1's table,
    # the three things #514's frame found by hand and the command should
    # report by itself. A directory the anchored guard holds is not retiring.
    holding = {i for row in survey["anchored"] for i in row.items}
    # Nor is it listed under the rule arm's heading, which says `settle
    # --retire` removes what it lists: the anchored heading already names it
    # as kept (round 1's finding 5).
    survey["rule"] = [i for i in survey["rule"] if i not in holding]
    survey["retiring"] = [
        i for i in survey["folded"] + survey["rule"] if i not in holding
    ]
    if survey["retiring"]:
        for work_item_id in survey["retiring"]:
            survey["takes"][work_item_id] = reader.open_record_rows(
                root, None, f"{SPECS}/{work_item_id}"
            )
        survey["citations"], survey["readers"] = citations(root, survey["retiring"])
    return survey


def has_spec(root, work_item_id):
    """Whether the work item's directory holds a `spec.md` on disk."""
    return os.path.isfile(under(root, f"{SPECS}/{work_item_id}/spec.md"))


# A path into a work item directory, however it is spelled before `specs/`
# (`seal/specs/`, the old `specs/`, a local-mode root). The name may be cut
# short with an ellipsis, which is how this repository's prose abbreviates a
# long id; a marker and a bare id carry no `/` after the name, so neither is
# read as a citation.
CITATION_RE = re.compile(r"specs/(\d{6,}[^\s/`'\"()\[\]|<>*]*)/")
ELLIPSES = ("…", "...")


def names(name, work_item_id):
    """Whether a cited directory name, possibly abbreviated, is this id."""
    for dots in ELLIPSES:
        if name.endswith(dots):
            stem = name[: -len(dots)]
            return bool(stem) and work_item_id.startswith(stem)
    return name == work_item_id


def tracked_text(root):
    """`(repo-relative path, text)` for every tracked text file outside
    `seal/specs/`. A file holding a NUL byte is binary and skipped."""
    r = subprocess.run(
        ["git", "-C", root, "ls-files", "-z"],
        capture_output=True,
    )
    if r.returncode != 0:
        return
    for rel in r.stdout.decode("utf-8", "replace").split("\0"):
        if not rel or rel.startswith(SPECS + "/"):
            continue
        try:
            with open(under(root, rel), "rb") as f:
                data = f.read()
        except OSError:
            continue
        if b"\0" in data:
            continue
        yield rel, data.decode("utf-8", "replace")


def citations(root, work_item_ids):
    """`({id: ["path:line", ...]}, [tests/ files naming seal/specs])`.

    The two listings a fold otherwise builds by hand. A path outside
    `seal/specs/` that cites into a retiring directory stops resolving when
    it goes, and each one is the fold's to rewrite or leave with a reason;
    and every `tests/` file that reads `seal/specs` is a check
    `skills/settle/SKILL.md` §3 says has to be answered before anything is
    removed. One scan of the tracked tree answers both.
    """
    cited = {i: [] for i in work_item_ids}
    readers = []
    for rel, text in tracked_text(root):
        if rel.startswith(TESTS) and SPECS in text:
            readers.append(rel)
        if "specs/" not in text:
            continue
        for number, line in enumerate(text.split("\n"), start=1):
            for m in CITATION_RE.finditer(line):
                for work_item_id in work_item_ids:
                    if names(m.group(1), work_item_id):
                        where = f"{rel}:{number}"
                        if where not in cited[work_item_id]:
                            cited[work_item_id].append(where)
    return cited, sorted(readers)


def report(found, ref, out=sys.stdout):
    """What a session reads before it writes one statement per segment."""
    write = out.write
    foldable = sum(len(v) for v in found["grouped"].values())
    write(
        f"released and unfolded: {foldable} work item{plural(foldable)} in "
        f"{len(found['grouped'])} segment{plural(len(found['grouped']))}, "
        f"{len(found['ungrouped'])} ungrouped, {len(found['skipped'])} skipped\n"
    )
    write(
        f"(released = present at {ref}; {len(found['unreleased'])} "
        "unreleased and untouched)\n"
    )
    write(
        f"no spec.md: {len(found['rule'])} to retire by the rule, "
        f"{len(found['rule_kept'])} kept by it\n"
    )

    for segment in sorted(found["grouped"]):
        items = found["grouped"][segment]
        write(f"\n{segment}  ({len(items)} work item{plural(len(items))})\n")
        for work_item_id in items:
            write(f"    {work_item_id}\n")

    if found["ungrouped"]:
        write("\nungrouped — no segment this can name, so a session names it:\n")
        for work_item_id, reason in found["ungrouped"]:
            write(f"    {work_item_id}  ({reason})\n")

    if found["skipped"]:
        write("\nskipped — an evidence-todo row is still open, and a fact that\n")
        write("never reached the ledger may not leave with the directory:\n")
        for work_item_id, count in found["skipped"]:
            write(
                f"    {work_item_id}  ({count} open row{plural(count)} in "
                f"{SPECS}/{work_item_id}/evidence-todo.md)\n"
            )

    if found["folded"]:
        write("\nfolded already, waiting to be retired — `settle --retire`:\n")
        for work_item_id in found["folded"]:
            write(f"    {work_item_id}\n")

    if found["anchored"]:
        write(
            "\nanchored — a ledger row cites a path inside a released work "
            "item's\ndirectory, and `settle --retire` keeps that directory "
            "until the row is answered:\n"
        )
        write_anchored(found["anchored"], out)

    if found["rule"]:
        write(f"\n{RULE_HEADING}\n")
        for work_item_id in found["rule"]:
            write(f"    {work_item_id}\n")

    if found["rule_kept"]:
        write(f"\n{RULE_KEPT_HEADING}\n")
        write_rule_kept(found["rule_kept"], out)

    if found["retiring"]:
        write(f"\n{TAKES_HEADING}\n")
        for work_item_id in found["retiring"]:
            write(f"    {work_item_id}\n")
            rows = found["takes"].get(work_item_id, [])
            cited = found["citations"].get(work_item_id, [])
            if not rows and not cited:
                write(
                    f"        nothing open, and nothing outside {SPECS}/ "
                    "cites into it\n"
                )
            for name, item in rows:
                write(f"        open in {name}: {item}\n")
            for where in cited:
                write(f"        cited from {where}\n")
        write(f"\n{READERS_HEADING}\n")
        for rel in found["readers"] or ["none under tests/"]:
            write(f"    {rel}\n")

    write(
        "\nNothing was written and nothing was removed. `skills/settle/SKILL.md`\n"
        "is the procedure: one standing statement per segment in `docs/`, each\n"
        "folded sentence carrying its `<!-- specs/<id> -->` comment, then\n"
        "`settle --retire` removes the directories that comment now covers.\n"
    )
    return 0


def retire(found, root, out=sys.stdout):
    """Remove the directories whose fold `docs/` records, and nothing else.

    The marker is the condition, so a directory is removed only where a
    policy document has absorbed the work item. An item the guard is holding
    is refused even with a marker: the fold was recorded and the fact the row
    names still has not reached the ledger. So is an item a live ledger row
    anchors into (#511), per directory rather than for the whole run — the
    evidence-todo guard's shape — so one held directory does not stop the
    others, and the run exits 1 naming every row.

    **The candidate set is read from the tree, not taken from `survey`.** It
    used to be `found["folded"]`, and round 1's finding 4 moved the guard
    ahead of the fold record in `survey` — correctly, because the REPORT must
    say *skipped and named* rather than *waiting to be retired*. That one move
    would have emptied `found["folded"]` of every held item and left the
    refusal below unreachable, so the only guard on a destructive act would
    have been a classification made for a printed list. Two readers of
    `open_items` is the point rather than the redundancy: this one decides
    what is removed, and it answers to the tree.

    `found` is still where *released* comes from, because only git can answer
    that and `survey` has already asked.

    **`present` stays in the intersection although it decides nothing today.**
    Round 2's finding 6 is right that it is inert: `found["released"]` is
    already a subset of the directories `survey` saw, so the only case the
    term can catch is a directory removed between the two calls in this same
    process. What it costs is one set operation; what it buys is that
    `shutil.rmtree` below cannot be handed a path that is gone. Leaving it out
    would make a destructive call depend on an invariant held by another
    function at another moment, which is the coupling the paragraph above is
    about. It also has a second reader now — `stranded` is `marked & present`,
    and that one is not inert at all.
    """
    reader = load(READER, "specseal_unverified_reader")
    marked = reader.folded_items(root)
    present = set(work_items(root))
    released_at_base = set(found["released"])
    held = open_items(root)
    # The rule arm (D3), read from the tree like the marker arm and for the
    # same reason: a released directory with no `spec.md` whose record holds
    # nothing open is a candidate with no marker, and one whose record does
    # is kept and named. The predicate is the one every CI reader asks.
    spec_less = sorted(
        i for i in (present & released_at_base) - marked if not has_spec(root, i)
    )
    by_rule = [
        i for i in spec_less if reader.retired_by_rule(root, None, f"{SPECS}/{i}")
    ]
    rule_kept = [
        (i, reader.open_record_rows(root, None, f"{SPECS}/{i}"))
        for i in spec_less
        if i not in by_rule
    ]
    candidates = sorted((marked & present & released_at_base) | set(by_rule))
    # #511's guard, asked of the candidates themselves and read from the
    # ledger now, for the reason the paragraph above gives for `open_items`:
    # the report's list is not a guard on a destructive act.
    anchored = anchored_rows(root, candidates)
    holding = {i for row in anchored for i in row.items}
    refused = [i for i in candidates if i in held or i in holding]
    removable = [i for i in candidates if i not in held and i not in holding]
    if not removable and not refused and not rule_kept:
        # THREE states, and they are told apart by what the sentence asserts
        # rather than by what happens to be empty. Round 1 split one of them
        # out of the other; round 2's finding 2 is that the split fired on
        # `if marked:`, which asks only whether `docs/` records any fold at
        # all, while the sentence it prints asserts that none of the marked
        # items still has a directory. Nothing had asked that, and a reader
        # who acts on *the fold is complete* stops looking.
        stranded = sorted(marked & present)
        if marked and not stranded:
            out.write(
                f"nothing left to retire: docs/ records the fold of "
                f"{len(marked)} work item{plural(len(marked))}, and none of "
                f"them still has a directory under {SPECS}/. "
                "The fold is complete.\n"
            )
            return 0
        if stranded:
            # Marked, still on disk, and not present at `--released-at`. It is
            # reachable two ways: a policy absorbing work that has not merged
            # to the release branch yet, and a run pointed at an older ref
            # than the one the items merged to.
            out.write(
                f"nothing to retire: docs/ records the fold of "
                f"{len(stranded)} work item{plural(len(stranded))} whose "
                f"directory is still under {SPECS}/, and none of them is "
                "present at the release ref, so nothing here reads as "
                "released:\n"
            )
            for work_item_id in stranded:
                out.write(f"    {work_item_id}\n")
            return 1
        out.write(
            "nothing to retire: no released work item carries a "
            "`<!-- specs/<id> -->` marker in docs/, so none of them has been "
            "folded yet, and none is a released directory with no `spec.md`. "
            "`settle` alone says which ones are waiting for one.\n"
        )
        return 1
    for work_item_id in removable:
        shutil.rmtree(under(root, f"{SPECS}/{work_item_id}"))
        why = (
            "  (no `spec.md` — retired by the rule, with no marker)"
            if work_item_id in by_rule
            else ""
        )
        out.write(f"removed {SPECS}/{work_item_id}/{why}\n")
    todo_kept = [i for i in refused if i in held]
    if todo_kept:
        out.write(
            "\nkept, although the fold is recorded — an evidence-todo row is "
            "still open:\n"
        )
        for work_item_id in todo_kept:
            count = held[work_item_id]
            out.write(f"    {work_item_id}  ({count} open row{plural(count)})\n")
    if anchored:
        out.write(
            "\nkept — a ledger row anchors inside the directory, and removing "
            "it would\nleave the row BROKEN. Answer each row, then run "
            "`settle --retire` again:\n"
        )
        write_anchored(anchored, out)
    if rule_kept:
        out.write(f"\n{RULE_KEPT_HEADING}\n")
        write_rule_kept(rule_kept, out)
    kept = len(refused) + len(rule_kept)
    out.write(
        f"\nretired {len(removable)} work item{plural(len(removable))}; {kept} kept\n"
    )
    return 1 if kept else 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="settle",
        description="Name the released work items a `docs/` policy has yet to "
        "absorb, grouped by the segment their ledger rows anchor in.",
    )
    ap.add_argument(
        "--root", default=None, help="repository root (default: the one this is run in)"
    )
    ap.add_argument(
        "--released-at",
        default="origin/main",
        metavar="REF",
        help="the branch a release merges to. A work item is released when "
        "its directory is present there (default: origin/main)",
    )
    ap.add_argument(
        "--retire",
        action="store_true",
        help="remove the directories whose fold `docs/` records, and the "
        "released ones with no spec.md and nothing open in their record. "
        "Writes no prose: what it removes is what a policy document has "
        "already absorbed, or a record of a moment that states no rule. A "
        "directory a ledger row anchors into is kept",
    )
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root or os.getcwd())
    # The root is resolved through the one resolver, `hooks/optin.py#home_at`,
    # the way `evidence_check.py#seal_home` reaches it from the same depth.
    # Before this, `under(root, SPECS)` was the only place looked at, so a
    # local-mode repository holding ninety-eight work items was told it had
    # none — and the sentence written for local mode, in the `--released-at`
    # refusal below, could never be printed, because this check fired first
    # and always.
    optin = load(OPTIN, "specseal_optin")
    # The common git directory is resolved once and handed down: `home_at`
    # takes it for exactly this caller, the one that needs the value for the
    # opt-out sentence below as well, and resolving it here and again inside
    # `home_at` was round 3's finding 5.
    common = optin.git_common_dir(root)
    home = optin.home_at(root, common)
    if not home:
        # `home_at` answers "" for two states, and round 2's finding 7 is that
        # they were given one sentence: no root at either place, and a
        # repository that opted out with the scratch marker. The second was
        # told it had no work items while holding them in the tree, which is
        # the defect one refusal up reached through another door.
        #
        # `isfile`, the accessor `home_at` uses and says why: `exists` also
        # accepts a DIRECTORY of that name, which no gate reads as an opt-out,
        # so this arm told such a repository to delete "that file" to turn the
        # gates back on — every clause false (round 3, finding 1).
        if common and os.path.isfile(os.path.join(common, optin.SCRATCH)):
            sys.stderr.write(
                f"settle: {root} has opted out — `{optin.SCRATCH}` is under "
                "its git directory, so every gate in this plugin reads it as "
                "a repository that never opted in and this command will "
                "remove nothing. Delete that file to turn them back on.\n"
            )
            return 2
        sys.stderr.write(
            f"settle: {root} has no {SPECS}/ at either place — nothing was "
            "read. This command folds work items, and a repository with none "
            "has nothing to settle.\n"
        )
        return 2
    # **Local mode refuses, and it is not the same refusal.** Resolving the
    # root is only half the finding: with the root found, a local-mode run
    # would go on to ask git which work items are released, git would answer
    # with none — an uncommitted root has no path in any tree — and the report
    # would say there is nothing to fold. That is the quiet zero this whole
    # module is written against, reached by the other door. So the state is
    # named here. It is the right answer as well as the honest one: nothing
    # removed from a root git never held can be recovered.
    #
    # The sentence written for local mode used to live inside the
    # `--released-at` refusal below and this comment claimed the fix made it
    # reachable at last. It did the opposite — that branch fires only for a
    # ref that does not resolve, and this one returns before `survey` is
    # called, so the clause was more unreachable than it had been (round 2,
    # finding 4). It is stated here and taken out of there.
    if os.path.realpath(home) != os.path.realpath(under(root, "seal")):
        sys.stderr.write(
            f"settle: the seal root of {root} is {home}, which is local mode "
            "— nothing was read. Local mode never commits the root, so no ref "
            "holds the work item directories, nothing in them can be called "
            "released, and nothing removed from them could be recovered. "
            "`seal mode shared` moves the root into the tree, and this "
            "command works from there.\n"
        )
        return 2
    # **A settled root is not an unusable one (#517, `spec.md` G7).** After
    # the last retirement the tree that ran `--retire` holds an empty
    # `seal/specs/`, and a fresh checkout of that commit holds none at all,
    # because git keeps no empty directory. Both are the state a complete
    # fold reaches, with the `seal/` root still there, and this used to
    # refuse the second at exit 2 — the command unable to run on its own
    # finished work. A repository with no root at either place is still
    # refused above.
    if not work_items(root):
        sys.stdout.write(SETTLED.format(root=root, specs=SPECS))
        return 0

    found = survey(root, args.released_at)
    if found is None:
        sys.stderr.write(
            f"settle: --released-at {args.released_at} does not resolve in {root} — nothing was "
            "read. Without it every work item reads as unreleased and this "
            "would report nothing to fold, which is the one answer it must "
            "not give by accident.\n"
        )
        return 2

    if args.retire:
        return retire(found, root)
    return report(found, args.released_at)


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
