#!/usr/bin/env python3
"""broad-gate — the one broad run, taken once after the rounds settle.

Issue #30. `CLAUDE.md` §*Verification Scope* says the full suite, the
repository-wide lint and the typecheck run once, after the review rounds
settle, and for three releases nobody was assigned that run: contract §2
forbade it to the smith and the warden, and the orchestrator that took it by
default kept hundreds of output lines in the one context a release cannot
replace. This command is the run, as a thing the sealer types.

What it does, in order, from the repository root:

  1. the repository's own broad command — the `Broad gate` row of
     `seal/config.md`, one shell command line the repository wrote for
     itself. **A row is refused four ways, and all four are exit 2 with
     nothing run**: no row at all, because a seal taken over a command nobody
     chose is the counterfeit `verify` names; a `Broad gate` line that is
     there and will not parse as a row of that table, which the refusal
     quotes back rather than reporting as absent (#415); a `Broad gate` line
     written inside a code fence, which no walk of that table reads because
     a fenced table is an example of the format rather than a repository's
     own answer (#429); or a row this gate would not run as the command it
     reads as — the whole command wrapped in backticks or in `$(…)`, or
     ending in a single `&`. No refusal names a command to write: the row is
     a person's, and the message says where they answer it
  2. `evidence-check --strict .`       the ledger's rows still anchor
  3. `unverified-check --baseline <base> seal/specs/`
  4. `chain_check.py --baseline <base>`   judged as a DRAFT pull request,
     because the cell this run is about to write still reads `not yet`
  5. `survivor-check --range <base>...HEAD`, with every
     `seal/specs/*/survivors.md` as `--exempt`
  6. `correction_check.py --range <base>...HEAD`   no merge on this branch
     dropped a correction the ledger had made
  7. `seal.py mode --check`            the `Mode` row and the folder agree

**Which arms exist is declared rather than remembered** (#468). `PARTITION`
below holds every step of `.github/workflows/hygiene.yml`'s `release` job
against the arm that mirrors it, or against the reason none does, and a case
holds that table against the workflow from both sides. The list above went
three releases at five while the workflow went to thirteen steps, and no case
went red for it.

**`<base>` above is a resolved commit, never the ref as typed.** `--base` is
resolved once before anything runs, to the ref CI will read: the given ref's
upstream where the checkout declares one, else `refs/remotes/origin/<base>`,
else the ref as given. Every consumer takes that commit, including the
scratch worktree and the `Broad gate` cell. A branch name in a local checkout
is a LOCAL ref and a runner has no local branches, so a checkout one commit
behind its remote sealed green over a question nobody asked while CI refused
the same commit on the same check (#423). Where resolving MOVES the answer
one line says so and the run continues; where it does not, nothing extra
prints. Nothing is fetched.

Every exit code is read directly off the subprocess (`agent-contract` §1),
and every check's output is kept in a file under `--keep-output` so the
report can quote a failing check's first lines and name where the rest is.
A check that fails does not stop the ones after it: the failure form names
every check that failed, which is what a reader acts on.

**On a failing test the comparison against the base is reactive and
mechanical** (`skills/verify/SKILL.md` §*The broad gate*). The row runs with
a pytest recorder of the gate's own loaded (`recording_env`), which writes
down, inside each pytest process the row starts, every test it ran and its
outcome. Only when the repository's command fails AND that record holds
failing test files does the gate add a scratch worktree at `<base>`, run the
row there once, unchanged, with the recorder loaded again, remove the
worktree, and label each file `new`, `failing on base too`, or
`new?` with the reason no run measured it, from the base's own record
(#825). No line pytest printed decides a word, and no file is appended to
any run. It decides nothing about any of the words: they go in the report
and the reader acts.

**Drawn on success only, and only where a person is looking** (#400). The
stamp — the disc and a panel carrying the tree and its branch, the base and
the ref it came from, the work item and its pull request, the suite's counts,
the ledger's three counts, the chain's exit, how many more steps CI runs
than this seal answers, and the round count when `--record` names a work
item — `capped` beside it and the deferred findings' homes beneath it where
the run ended at the cap (`rounds_rows`) — a list too long for its row
continuing on the row beneath it (`panel`) — is
`seal_stamp.stamp`'s, and it is drawn only over a written cell. On a
terminal a recorded seal draws it once, in the form `pick_shape` chooses.
Anywhere else a recorded seal draws nothing and prints one line beginning
`SEALED`, naming the values file the panel's rows were written to, under
`<git-common-dir>/specseal-stamp/<session>/`; `hooks/sealer-stamp.py` draws
it at the end of the turn of the session named by `CLAUDE_CODE_SESSION_ID`.
Without `--record` there is no cell, so on a terminal or off one the line
says nothing was recorded, and nothing is written or drawn. A sealer's
stdout is a pipe, so a sealer's run never draws. Both lines name what was
sealed as `<branch> @ <tree> against <ref> @ <base commit>`, the branch left
out on a detached HEAD and the ref left out where it is the commit itself
(#666). The failure form is `NOT SEALED` with the same names and the failing
checks with their first lines, no drawing and no file. A recorded seal adds
one line after the stamp or the `SEALED` line, where git still sees the
cell's file uncommitted: the cell is written and not committed, and CI reads
HEAD.

`--record <item>` runs `round_record.py seal` on success, which sets the LAST
record's `Broad gate` cell and nothing else. With `--record`, success is the
checks green AND the cell written. `seal` ends non-zero two ways and BOTH are
exit 2 here with no stamp: a refusal raised before the write — the last
record's `Pass` unchecked, its `Fixes checked by` still reading `nobody`, or
a premature SHA — and the chain check `seal` runs after the write, which
comes back as 1 for errors and 2 for a check that could not run. **The exit
code cannot tell the two apart and neither can the presence of a
`round-record:` line, which both endings print**; the word `sealed` is the
discriminator, and the gate's message says which of the two happened. A seal
over a record that says the run came too early, or over a tree the chain
check refuses, is a stamp over a contradiction.

**`--preflight` runs arms 2 to 7 alone, and seals nothing** (#638). It is the
orchestrator's step before it spawns the sealer: the same base resolved the
same way, every refusal of the row applied, and then every arm above except
the row, in the same order, with the same arguments, each output kept the
same way. The row is read and never run, so a refusal on a record arm — a
drifted ledger row, a chain refusal, a survivor — arrives in seconds rather
than after a whole suite. It writes no cell, no values file and no stamp,
adds no worktree, prints no coverage line, and prints no line beginning
`SEALED` or `NOT SEALED`: its stdout opens `PREFLIGHT PASSED` or `PREFLIGHT
FAILED`, the failing arms under the second in the failure form's own words.
`--record` beside it is refused, because a preflight writes no cell. It is
not the broad gate and replaces no part of the sealer's run.

**Then it asks `seal`'s own refusals, and writes nothing** (#702). Three
refusals are not record arms: `round_record.py seal` raises them when the
sealer writes the cell, after the suite — the last record's `Pass`
unchecked, its `Fixes checked by` reading anything but `no fixes to check`,
and a SHA the record's `Target SHA` descends from. After the arms, the
preflight runs `round_record.py seal --check` on the work item declared for
the checked-out branch, with the cell value the sealer's run would hand it.
The declaration is found by `hooks/routing.py#item_dir`, which reads the
declarations in the working tree, untracked ones included — what the commit
gate reads, and what `seal` reads when the sealer runs it. The chain arm keys
on the same branch but reads only the declarations committed at HEAD, so an
uncommitted second declaration naming the branch skips the ask here while
the chain arm still finds one.
`--check` asks every refusal `seal` raises and stops before the write, so
`seal` stays the one authority and nothing here restates its predicates. Its
output is kept as `seal.txt`, its exit code is read off the subprocess, and
a refusal joins the failing arms under `PREFLIGHT FAILED` as `seal`. It is
not an arm: it mirrors no CI step, so it is no `checks[...] = run(...)` and
takes no `PARTITION` row. Where no single declaration names the branch —
none, two, or a detached HEAD — nothing is asked and one stderr line says
so; the exit is the arms' own.

Usage:
  broad-gate --base <ref> [--root DIR] [--record <item>] [--shape]
             [--keep-output DIR]
  broad-gate --preflight --base <ref> [--root DIR] [--keep-output DIR]

Exit codes: 0 sealed · 1 not sealed · 2 refused — no row, no repository, a
base that does not resolve, a copy of the plugin whose sibling will not
load (a malformed `seal-mark.txt` among them), a `seal` the record
refused; nothing ran on 2 except where the refusal names what ran. Under
`--preflight`: 0 every record arm passed and `seal --check` refused nothing
or was not asked · 1 an arm failed or `seal --check` refused · 2 refused,
with nothing run, `--record` given among the refusals.
"""

import argparse
import functools
import glob
import importlib.util
import json
import ntpath
import os
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import tempfile

# --- the interpreter floor -----------------------------------------------
#
# Copied from `skills/code-review/scripts/round_record.py`, whose comment says
# this block is the spelling to copy. It sits after the imports, uses no syntax
# newer than the interpreter it means to catch, and precedes every other act
# at module level.
FLOOR = (3, 12)
FLOOR_TEXT = ".".join(str(part) for part in FLOOR)
BELOW_FLOOR = (
    "broad-gate: needs python {floor} or newer, and this is python {found} "
    "at {executable}.\n"
    "Nothing was read and nothing was written.\n"
    "`python3` is not always the newest interpreter installed -- macOS ships "
    "python 3.9 under that name -- so name one explicitly, `python{floor} "
    "<this script> ...`, or see CONTRIBUTING.md section 'Running the checks'."
)


def below_floor(version=None, executable=None):
    """The sentence for an interpreter under the floor, or None above it."""
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


# --- where the pieces are ------------------------------------------------
#
# Resolved relative to this file, never to the caller's cwd, so the command
# works from the plugin cache and from a clone alike. `hooks/config.py` is
# loaded by path the way `chain_check.py` loads `hooks/routing.py`: it is the
# one reader of `seal/config.md`'s table, and a second reader that parsed the
# table differently would answer a different question about the same file.
HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
STAMP = os.path.join(HERE, "seal_stamp.py")
UNVERIFIED = os.path.join(HERE, "unverified_check.py")
EVIDENCE = os.path.join(
    PLUGIN, "skills", "evidence-check", "scripts", "evidence_check.py"
)
CORRECTION = os.path.join(
    PLUGIN, "skills", "evidence-check", "scripts", "correction_check.py"
)
SEAL_SCRIPT = os.path.join(PLUGIN, "skills", "implement", "scripts", "seal.py")
CHAIN = os.path.join(PLUGIN, "skills", "code-review", "scripts", "chain_check.py")
SURVIVOR = os.path.join(PLUGIN, "skills", "code-review", "scripts", "survivor_check.py")
RECORD = os.path.join(PLUGIN, "skills", "code-review", "scripts", "round_record.py")
# The branch → work item key the preflight's ask reads (#702).
ROUTING = os.path.join(PLUGIN, "hooks", "routing.py")
CONFIG_READER = os.path.join(PLUGIN, "hooks", "config.py")

SEAL_DIR = "seal"
CONFIG = "config.md"
ROW = "Broad gate"
SPECS = "specs"
SURVIVORS = "survivors.md"
ROUND_RE = re.compile(r"^round-(\d+)\.md$")

# The checks, by the name the report prints for each. The first is the
# repository's own command; the panel reads its `suite` and `lint` from that
# one run, because the row carries both.
#
# There is no count in this comment on purpose. There were five of these for
# three releases and every document that said `five` had to be found again
# when the sixth landed — `PARTITION` below is where the list is declared, and
# a case holds it against the workflow rather than against a number typed here.
SUITE, LEDGER, UNVERIFIED_NAME, CHAIN_NAME, SURVIVORS_NAME = (
    "suite",
    "ledger",
    "unverified",
    "chain",
    "survivors",
)
# The two the workflow ran and the gate did not, until #468 (`PARTITION`).
CORRECTIONS_NAME, MODE_NAME = "corrections", "mode"

# How many lines of a failing check's output the report quotes before naming
# the file that holds the rest.
QUOTED = 8

NEW, ON_BASE = "new", "failing on base too"

# How many columns a panel value is given (#832, `spec.md` S5a of work item
# 1791270164): the widest that keeps the stamp's widest line inside an
# 80-column terminal, the floor a command line's output is held to. The open
# layout has no frame, so the terminal is the bound: 28 columns of disc, `GAP`
# (3) clear, a label of seven and a space, and the value — 28 + 3 + 8 + 41 =
# 80. Before #832 it was 23, what `seal_stamp.letter`'s 36-column frame left.
# A longer value runs past the terminal's edge or wraps into the disc's
# column, so the gate elides before it does (round 1, finding 5 of #666): a
# cut ref would read as a whole ref, and nothing prints beside the row on a
# run where the given and resolved bases agree (A4).
#
# Stated here and measured over there, and neither may move without the other
# going red: `test_the_panel_value_width_is_what_the_stamp_actually_gives`
# draws a value of this width and measures the stamp's widest line.
PANEL_VALUE_WIDTH = 41
ELISION = "..."
# The panel's own characters (#832 S5a, the owner's design of 2026-10-07):
# the separator inside a value, the arrow before a deferral's homes, the mark
# on a result row that passed and the mark on a row that is not a pass. They
# are the owner's and not ASCII; `seal_stamp`'s letter twin, which exists for
# a console that is not UTF-8, maps them where it writes them.
SEP, ARROW, TICK, DOT = " · ", "→", "✓ ", "· "


def fit(value, keep="head", width=None):
    """`value` as the panel can carry it: unchanged where it fits, else
    elided to `width` — `PANEL_VALUE_WIDTH` unless a caller names less —
    with `ELISION` on the side that was cut.

    `keep="head"` for a branch name, whose issue number leads and is what a
    reader matches to a ticket; `keep="tail"` for a ref, where the
    `origin/` a runner reads is the part a reader can infer. Every value
    `panel` returns passes through here, so no row is wider than the frame
    and none is cut by it without a marker (#666). `width` is the room a
    ref has beside its commit on the `base` row (#832)."""
    value = str(value)
    width = PANEL_VALUE_WIDTH if width is None else width
    if len(value) <= width:
        return value
    room = width - len(ELISION)
    return ELISION + value[-room:] if keep == "tail" else value[:room] + ELISION


def wrapped(label, pieces):
    """A list on as many panel rows as it needs: the first row under `label`,
    the rest as `""` rows beneath it (round 1's 🟡 1 of #666).

    The owner chose continuation rows over a wider panel (`questions.md`
    Q1), so a list of counts or homes continues rather than losing its tail
    to `...`; only a branch or a ref, which have no bound, are elided. Each
    piece but the first carries the separator that joins it to the one
    before (`", #664"`, or `" · 11 skipped"` since #832). A row is broken
    before a piece that would not fit, and keeps that separator's mark — the
    comma, or the ` ·` — at its end so the reader sees the list goes on; two
    columns are held back for it on every piece but the last, because ` ·`
    is two. One piece wider than the frame by itself is still elided by
    `fit`."""
    rows, line = [], ""
    for n, piece in enumerate(pieces):
        room = PANEL_VALUE_WIDTH - (0 if n == len(pieces) - 1 else 2)
        if line and len(line + piece) > room:
            lead = piece[: len(piece) - len(piece.lstrip(", ·"))]
            rows.append(line + lead.rstrip())
            line = piece.lstrip(", ·")
        else:
            line += piece
    rows.append(line)
    return [(label if n == 0 else "", fit(row)) for n, row in enumerate(rows)]


# pytest's short-summary line for a failed test, `FAILED path::name - why`,
# printed under `-q` too. Read only where the row's run at `HEAD` left no
# record (`failing_files`), to name the files that read `NO_RECORD_AT_HEAD`;
# the path may hold a space (#813).
FAILED_RE = re.compile(r"^FAILED\s+(.+?)::", re.M)
# `evidence-check`'s total line: `total: N ok · D drifted · B broken · …`.
LEDGER_RE = re.compile(r"total: (\d+) ok · (\d+) drifted · (\d+) broken")


class Refused(Exception):
    """A reason nothing ran (exit 2)."""


def load(path, name):
    """Import a sibling script by path, or raise `Refused`: where the file is
    not there, and where executing it raises (#869) — `seal_stamp.py` reads
    its disc's mark chart at import and raises `CHART_MALFORMED`'s sentence
    for one that is not in shape, which then ends the gate at exit 2 with
    that sentence and nothing run, rather than in a traceback. The
    exception's own sentence is what the person reads; one with none is
    named by its type. A `SystemExit` — a sibling's interpreter floor — is
    no `Exception` and keeps its own exit."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None or not os.path.isfile(path):
        raise Refused(f"cannot load {path} — this copy of the plugin is missing it")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:
        said = str(exc) or type(exc).__name__
        raise Refused(
            f"broad-gate: {path} will not load, so nothing ran: {said}"
        ) from exc
    return mod


@functools.lru_cache(maxsize=1)
def stamp_module():
    """`seal_stamp.py`, loaded once per process: `panel` asks it the one
    question both of them answer (`ref_is_commit`), and a case drives
    `panel` without a gate around it to have loaded it."""
    return load(STAMP, "specseal_seal_stamp_for_broad_gate")


def git(root, *args):
    """stdout of a git call in `root`, or None on a non-zero exit."""
    r = subprocess.run(
        ["git", "-C", root, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.stdout if r.returncode == 0 else None


def repo_root(start):
    out = git(start, "rev-parse", "--show-toplevel")
    return os.path.normpath(out.strip()) if out and out.strip() else None


def branch_name(root):
    """The branch checked out at `root`, or None on a detached HEAD.

    What the `SEALED` and `NOT SEALED` lines name beside the tree (#666): a
    head naming two commits told a reader which hash was sealed and never
    which branch, so a stamp was matched to its work by hand. `symbolic-ref
    -q` exits non-zero on a detached HEAD and prints nothing, which is the
    None the lines read as *leave the branch out*."""
    out = git(root, "symbolic-ref", "--short", "-q", "HEAD")
    return out.strip() if out and out.strip() else None


# --- which copy of the gate runs, and the stamp says which ------------------
#
# `bin/broad-gate` on the Bash tool's PATH is the installed plugin's, and this
# script resolves every arm relative to itself (`PLUGIN`, above). So a branch
# that changes the gate was measured by the copy that predates the change,
# and the stamp could not say which copy drew it — #475, measured twice: seven
# arms in the tree against five installed, and a chain refusal from the
# released copy over a state the branch had repaired. CI runs the checkout's
# scripts (`.github/workflows/hygiene.yml`), and the gate exists to say what CI
# will say (`docs/the-broad-gate.md`), so the checkout's copy is the one that
# asks the question the merge is judged by. Where the gated tree ships one,
# `main` runs it in place of this file, with the same argument vector, and
# says so; every run's stderr names which copy ran, `tree` or `plugin`, with
# its version, and the panel's `gate` row says `tree <version>` where that
# copy's bytes differ from the one the caller invoked, or where no invoked
# copy was handed over to compare — the tree's copy run directly, or
# redirected by an installed copy older than #666 (`gate_copy`). A
# tree that breaks an arm seals itself — that is the stated cost, named on
# the stamp by `tree` and caught at the pull request by the same scripts.

GATE_REL = os.path.join("skills", "verify", "scripts", "broad_gate.py")
PLUGIN_JSON = os.path.join(".claude-plugin", "plugin.json")


def shipped_gate(root):
    """The gate the tree at `root` ships, or None.

    None where the tree has no `skills/verify/scripts/broad_gate.py`, which is
    every repository that installs the plugin rather than developing it — for
    them nothing about the run changes. None too where that file IS this one
    by `os.path.realpath`, which is what keeps the tree's own copy from
    re-running itself: the redirected-to copy finds itself under the root and
    goes on to `gate()`.
    """
    candidate = os.path.join(root, GATE_REL)
    if not os.path.isfile(candidate):
        return None
    if os.path.realpath(candidate) == os.path.realpath(__file__):
        return None
    return candidate


def plugin_version(plugin):
    """`version` from `<plugin>/.claude-plugin/plugin.json`, or `?` where the
    file cannot be read or does not say -- a run never stops on a label."""
    try:
        with open(os.path.join(plugin, PLUGIN_JSON), encoding="utf-8") as handle:
            version = json.load(handle).get("version")
    except (OSError, ValueError, AttributeError):
        return "?"
    return str(version) if version else "?"


def under(path, root):
    """Whether `path` lies under `root`, both taken by realpath."""
    if root is None:
        return False
    path, root = os.path.realpath(path), os.path.realpath(root)
    try:
        return os.path.commonpath([path, root]) == root
    except ValueError:  # different drives on Windows
        return False


def copy_origin(root, plugin=PLUGIN, running=None):
    """`tree <version>` where the running copy lies under the gated root,
    `plugin <version>` otherwise, the version read from the running copy's
    own `plugin.json` — which copy ran, as the stderr line says it on every
    run (`running_line`) and the panel's `gate` row says it where it differs.

    A path does not fit `PANEL_VALUE_WIDTH`; a version alone does not tell a
    branch cut from the tag apart from the tag. The pair says where the copy
    came from and which release it belongs to, and the line `main` writes to
    stderr carries the path in full, the way `moved_line` and `coverage_line`
    carry what the panel cannot. Elided at the frame (`fit`), so a long
    version is a shorter label and never a wider row. `running` is this
    file unless a case names another.
    """
    origin = (
        "tree" if under(__file__ if running is None else running, root) else "plugin"
    )
    return fit(f"{origin} {plugin_version(plugin)}")


def gate_copy(root, plugin=PLUGIN, running=None, installed=None):
    """The panel's `gate` row, or None where it would say nothing (#666).

    The row printed on every stamp from 0.15.1 (#475), and in this repository
    every seal is redirected to the tree's copy, so it read `tree <version>`
    every time and told nobody anything. It prints now only where the copy
    that measured the tree is NOT the copy the caller invoked:

      - the running copy lies under the gated root, AND
      - its bytes differ from `installed`, the copy the caller invoked, whose
        path the redirect hands the child in `INVOKED_AS_VAR` and `main`
        passes here; or `installed` is None — the tree's copy invoked
        directly, or redirected by an installed copy older than #666, either
        way with no path handed over — which is the direction that says more
        when it cannot tell.

    A repository that ships no gate runs the invoked copy, which is not under
    its root, so it gets no row, which is the *carries no information* case
    the owner named.

    **Two bounds, named rather than claimed.** It compares one file, so a
    tree that changed a sibling arm (`chain_check.py`, say) and not
    `broad_gate.py` prints no row although the arms it runs are the tree's;
    and an installed copy that cannot be read counts as different, so the row
    prints. Versions are not compared: within a release cycle the tree's
    `plugin.json` equals the installed one until the release bumps it, so a
    branch that changed the gate — #475 itself — would print nothing exactly
    when it matters (`plan.md` §*Alternatives considered*).
    """
    running = __file__ if running is None else running
    if not under(running, root):
        return None
    if installed:
        try:
            with open(running, "rb") as mine, open(installed, "rb") as theirs:
                if mine.read() == theirs.read():
                    return None
        except OSError:
            pass
    return copy_origin(root, plugin, running)


def running_line(root):
    """The one stderr line every run carries once the root has resolved:
    the running copy's absolute path and which copy it is."""
    return f"broad-gate: gate {os.path.realpath(__file__)} ({copy_origin(root)})"


def redirect_line(root, shipped):
    """What `main` writes before handing the run to the tree's own copy."""
    return (
        f"broad-gate: {root} ships its own gate; running {shipped} "
        f"(tree {plugin_version(root)}) in place of "
        f"{os.path.realpath(__file__)} (plugin {plugin_version(PLUGIN)})"
    )


# --- which base, and it is the one CI will read ----------------------------
#
# `.github/workflows/hygiene.yml` spells every base it takes
# `origin/${{ github.base_ref }}`, at its four base-taking steps. That is not
# a choice the workflow made: a runner's checkout has no local branch, so the
# remote-tracking ref is the only thing that resolves there. This gate was
# handed the ref AS TYPED and so resolved the LOCAL one, and the two part as
# soon as the local ref falls behind — #423, where the gate sealed a branch
# green over two excused survivors and CI refused the same commit with seven.
#
# `tests/test_the_gate_asks_the_range_ci_will_ask.py` holds this spelling
# against the workflow's, so the two readers cannot drift apart again in
# silence.
REMOTE_BASE = "refs/remotes/origin/{ref}"
REMOTE_LABEL = "origin/{ref}"
UPSTREAM_BASE = "{ref}@{{upstream}}"


class Base:
    """Which commit the gate compares against, and where that spelling came
    from: the caller's `--base`, the ref the resolution landed on, and both
    refs' commits.

    `commit` is what every check is handed, because #423's own comment asks
    for the property that anything recorded as evidence names a commit rather
    than a ref — a ref re-resolves and a commit does not. `ref` is what a
    person reads, in the panel and in the line below.

    `commit` is None for a base that resolves nowhere. That is not this
    unit's refusal to raise: `gate()` owns the message, and the message has
    to quote the spelling the caller typed rather than a resolution of it.
    """

    __slots__ = ("commit", "given", "given_commit", "ref")

    def __init__(self, given, given_commit, ref, commit):
        self.given, self.given_commit = given, given_commit
        self.ref, self.commit = ref, commit

    @property
    def moved(self):
        """True where resolving changed the answer — including the case where
        the given spelling names no commit in this checkout at all, which is
        an ordinary clone that never made a local branch for its base."""
        return self.commit != self.given_commit


def moved_line(root, base):
    """The one line printed where resolving the base MOVED the answer, or
    None where the given spelling and the resolved one are the same commit.

    Printed and then the run continues. A refusal was the ticket's second
    direction and `plan.md` §*Alternatives considered* rejected it: its only
    repair is a `git fetch` and a second nine-minute gate, performed by a
    person the sealer has no way to ask, and it fires on the ordinary release
    case where a sibling merges while this branch is open.

    **Nothing prints where the two agree.** A line on every run is a line
    people learn to skip, which is the reasoning
    `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` already
    applies to the lenient ledger notice.

    Two fillings, because a given spelling can name no commit at all. A clone
    that never made a local branch for its base is an ordinary checkout, and
    resolving it in silence would be the very defect this repairs — so
    `Base.moved` compares commits, and `None` is not a hash.

    **It never says CI reads a ref CI does not read.** Step 1 of the rule is
    `<base>@{upstream}`, which a clone tracking a second remote — a fork with
    an upstream — answers with something that is not `origin/<base>`, and the
    workflow spells `origin/<base>` literally. Where the two part, the line
    says what THIS checkout declares and names the ref a runner would read
    beside it. `agents/sealer.md` has the sealer quote this line in its
    report, so a sentence that can be wrong here is wrong in a report
    (round 1, finding 2).

    **And it names a runner's ref only where a runner could hold one.** The
    clause above was over-claimed by one spelling: `--base @{-1}` passes
    `names_a_branch`, because `check-ref-format --branch` expands `@{-N}`
    before it checks, and the runner label built out of it is `origin/@{-1}`
    — a name no ref can have. The line used to offer it as *the ref a runner
    reads*. `a_runner_could_hold` asks git about the constructed label, and
    where git refuses it the line says the runner has no counterpart for that
    spelling instead of naming one (round 2, finding 10, and #461).

    **The counts name what they are measured against.** `1 ahead, 0 behind`
    has no subject and both refs are in the sentence, so the reading that
    makes it true is the nearer noun rather than anything stated (round 1,
    finding 7).
    """
    if not base.moved:
        return None
    runner = REMOTE_LABEL.format(ref=base.given)
    if base.ref == runner:
        reads = f"CI reads {base.ref}, which is {base.commit}"
    elif a_runner_could_hold(root, runner):
        reads = (
            f"this checkout says {base.given} tracks {base.ref}, which is "
            f"{base.commit} — not the {runner} a runner reads"
        )
    else:
        reads = (
            f"this checkout says {base.given} tracks {base.ref}, which is "
            f"{base.commit}; a runner's checkout has no counterpart for "
            f"{base.given}"
        )
    if base.given_commit is None:
        return (
            f"broad-gate: --base {base.given} names no commit in this "
            f"checkout; {reads}. Every check below was asked about {base.ref}."
        )
    # `--left-right` counts each side of the symmetric difference: what the
    # given spelling holds that the resolved one does not, then the reverse.
    counts = git(
        root, "rev-list", "--count", "--left-right", f"{base.given}...{base.ref}"
    )
    apart = ""
    if counts and len(counts.split()) == 2:
        behind, ahead = counts.split()
        apart = f" — {base.ref} is {ahead} ahead and {behind} behind {base.given}"
    return (
        f"broad-gate: --base {base.given} is {base.given_commit} in this "
        f"checkout; {reads}{apart}. Every check below was asked about "
        f"{base.ref}."
    )


def short_commit(root, rev):
    """`rev`'s short commit hash, or None where it names no commit."""
    out = git(root, "rev-parse", "--short", f"{rev}^{{commit}}")
    return out.strip() if out and out.strip() else None


def names_a_branch(root, given):
    """True where `given` is a spelling a branch could have.

    Asked of git rather than of a pattern written here, because the rule this
    guards — which remote-tracking ref a BRANCH corresponds to — is meaningful
    only for a branch name, and git already owns what one is.

    **`--branch` EXPANDS `@{-N}` and then checks what it expanded to.** That
    is the property, and it is not the same as refusing everything carrying
    `@{…}`, which is what this docstring claimed until round 2 of #423
    measured it. On git 2.54.0, `@{-1}` is accepted and the command prints
    the branch it expanded to (`base`); `HEAD`, `HEAD~1`, `base@{u}` and
    `topic@{1}` are each refused with *is not a valid branch name*. `base`,
    `release/vX.Y.Z` and a short SHA are accepted. The SHA being accepted is
    right: it is a legal branch name, and no ref exists for it, so it reaches
    the fallback either way.

    `@{-1}` being accepted is right too — it does name a branch, so taking
    that branch's upstream is coherent. What it is NOT is a spelling a
    runner's checkout can build a remote-tracking ref out of, and that is a
    different question, asked of git separately in `a_runner_could_hold`
    (#461).
    """
    return git(root, "check-ref-format", "--branch", given) is not None


def a_runner_could_hold(root, ref):
    """True where `ref` is a name a ref in a runner's checkout could have.

    A different question from `names_a_branch`, and it has to be, because
    `--branch` expands `@{-N}` before it checks: `@{-1}` passes that call and
    the `origin/@{-1}` built out of it is not a name any ref can have. Git
    refuses the whole name here, so `origin/@{-1}` comes back False while
    `origin/base` comes back True.

    Asked of git rather than of a pattern written here, for the reason round
    1's finding 6 established: a hand-written guard closed the spelling in
    front of it and moved the defect one step down to `origin/HEAD` instead
    of closing the class. #461's *Not this* says the same thing.
    """
    return git(root, "check-ref-format", ref) is not None


def resolve_base(root, given):
    """`--base` as CI will read it, as a `Base`.

    Three steps, in order:

      1. `<given>@{upstream}` — what THIS checkout says the base tracks. It
         comes first because a clone whose base branch tracks a second remote
         (a fork with an upstream) is the defect class being repaired, and
         reaching for `origin/` there would compare against the fork's stale
         copy.
      2. `refs/remotes/origin/<given>` — the spelling the workflow uses
         literally, and what a runner always has.
      3. the ref as given. A base with no remote-tracking counterpart — never
         pushed, a bare SHA, a repository with no remote at all — resolves to
         itself, and every gate fixture in the suite is that repository.
         **What does NOT stay the same there is what the consumers are
         handed.** The resolution turns the ref into its commit for them too,
         so that repository's `Broad gate` cell, its `NOT SEALED` line and the
         baselines the child checks quote back all name a hash where they
         named a branch. One assertion in
         `tests/test_the_seal_is_taken_once_by_the_sealer.py` moved for it,
         and this paragraph said *nothing about that run changes* until round
         1 measured it (finding 3).

    Nothing is fetched. A remote-tracking ref is only as fresh as the last
    fetch, and #423 §*Not this* refuses a check that moves refs to make
    itself pass — an unattended run may have no credentials. What this buys
    is that the gate asks the question the merge is judged by; what it cannot
    buy is that the answer is current, which is why the ref is named in what
    a person reads.
    """
    given_commit = short_commit(root, given)
    # Both steps are asked only of a spelling a BRANCH could have, and that is
    # the whole of round 1's finding 6. `@{upstream}` is a suffix on any
    # revision expression, so `HEAD@{upstream}` answers for the branch the
    # checkout is sitting on rather than for the one `--base` named; and a
    # clone creates `refs/remotes/origin/HEAD`, so guarding step 1 alone moved
    # the same defect one step down and `--base HEAD` resolved to
    # `origin/HEAD`. A short SHA is a legal branch name and needs no guard:
    # neither ref exists for it, so it reaches the fallback the way A9 asks.
    if names_a_branch(root, given):
        tracked = git(
            root, "rev-parse", "--abbrev-ref", UPSTREAM_BASE.format(ref=given)
        )
        if tracked and tracked.strip():
            name = tracked.strip()
            commit = short_commit(root, name)
            if commit is not None:
                return Base(given, given_commit, name, commit)
        commit = short_commit(root, REMOTE_BASE.format(ref=given))
        if commit is not None:
            return Base(given, given_commit, REMOTE_LABEL.format(ref=given), commit)
    return Base(given, given_commit, given, given_commit)


def seal_home(root):
    """`<root>/seal/` where it exists, else `<git-common-dir>/seal/`, else
    None — the two places every `seal/…` path in this plugin resolves to
    (`agent-contract` §16), read in that order."""
    shared = os.path.join(root, SEAL_DIR)
    if os.path.isdir(shared):
        return shared
    common = git(root, "rev-parse", "--git-common-dir")
    if common and common.strip():
        local = os.path.join(root, common.strip(), SEAL_DIR)
        if os.path.isdir(local):
            return os.path.normpath(local)
    return None


def config_text(home):
    """The root's `config.md` as text, or None where there is none or it
    will not read: the text half of `hooks/config.py#config_text`, the one
    place the file is opened (#867). Every caller of this one runs after
    `broad_command`, which has already refused a file that will not read,
    so None here is a file that is not there."""
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    return config.config_text(home)[0]


def broad_command(home):
    """The `Broad gate` row's value, or None for every way of not having one:
    no file, no row, an empty value.

    **Two states are refused, not read as no row** (#867): a `config.md`
    that is there and will not read, and a `Broad gate` row written twice.
    Either raises `Refused` naming the path, so the sealer's gate exits 2
    with nothing run. Read as no row, an unreadable file was reported as a
    missing row, which sent a person to add a row the file already held,
    and a doubled row ran its first command."""
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text, refused = config.config_text(home)
    if refused is not None:
        raise Refused(f"broad-gate: {refused}. Nothing ran")
    if text is None:
        return None
    value, refused = config.value_of(config.config_rows(text), ROW)
    if refused is not None:
        raise Refused(
            f"broad-gate: {os.path.join(home, CONFIG)}: {refused}. Nothing ran"
        )
    return value or None


# A refused line's first cell, read the way a cell was read before the escape
# existed -- up to the first pipe. The line does not parse, so this is a
# reading of what the person meant by it and not a row of the table.
FIRST_CELL = re.compile(r"^\|([^|]*)\|")


def refusal(home):
    """(refused, below, stopper) for the root's config — the one reader's
    answer about every line it will not take as a row, passed through.

    Every way of not having one lands on `([], [], None)`: no file, a file
    that will not read, a table with no refused line at all.
    """
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return [], [], None
    return config.refusal(text)


def rows_read(home):
    """Every row the table reader actually returned for the root's config.

    **One arm of `missing_row` cannot use `below`, and this is what it uses
    instead.** `hooks/config.py#refusal` fills `below` with the rows written
    under the STOPPING line; the arm for a quoted line that nothing stopped
    the reader at has no stopping line, so `below` is empty there whatever
    the file holds — measured 2026-09-18 over a file where the quoted line is
    the only row and over the same file with a row under it, `[]` both times.

    In that arm alone, every row this returns is written BELOW the quoted
    line, which is what makes it the right question there and the wrong one
    anywhere else: a row that had parsed ABOVE the quoted line would have
    made that line the stopping one, which is a different arm.

    It calls the one reader rather than walking the file again. A second walk
    written here would answer a different question about the same file, which
    is the split `hooks/config.py` exists to prevent.
    """
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return []
    return config.config_rows(text)


def names_this_row(line):
    """Whether a refused line's first cell is this gate's row."""
    first = FIRST_CELL.match(line.strip())
    return bool(first and first.group(1).strip() == ROW)


def hides_this_row(below):
    """Whether this gate's row is one of the rows the STOPPING line took.

    The row is in the person's file and the reader never reached it, so
    saying it is ABSENT is a true sentence about a cause that is not the real
    one — the same shape #415 was opened about, one item over. Asked of the
    rows rather than of the refused line, because a file that has no such row
    anywhere is a file the absent-row refusal is right about, malformed line
    or not (#415 round 1 🟡 3).

    `below` is read from the line that actually stopped the reader, which is
    what makes this answer the table's. Read from the FIRST refused line it
    held rows that had arrived perfectly well, and the branch was gated on a
    flag describing that line rather than on the rows — so a row under a
    SECOND refused line was handed to this function and reported absent
    anyway (#415 round 2 🟡 1).
    """
    return any(item == ROW for item, _value in below)


def refused_broad_row(home):
    """The `Broad gate` row a person wrote that the table reader will not
    take as a row — as written, with its own indentation — or None.

    **Asked of every refused line, not of the first one.** A file with two
    lines the reader will not take can have this gate's row under the
    second, and answering about the first reported that row as ABSENT —
    which is the message this whole work item exists to end, arriving one
    line further down (#415 round 2 🟡 1).

    None covers every other shape: no such line, refused lines naming other
    items only, and a file that will not read. Only the row this gate is
    about gets the second sentence, because only this row's absence is what
    the gate is refusing over.
    """
    refused, _below, _stopper = refusal(home)
    return next((line for line, _reached in refused if names_this_row(line)), None)


def fenced_row_at(home):
    """(index, line) for this gate's row written inside a code fence, or
    (None, None). `fenced_row` below is that answer's line alone, and its
    docstring is where this one's reasoning lives.

    The INDEX is what lets the refusal say *a fence above it*: an opener left
    unclosed lower down the file is not this row's cause, and the person whose
    row is in a block that closes correctly still has to move it (#429,
    round 2).

    **Fenced, and not merely hidden.** The reader hides a line inside an HTML
    comment that closes too (#667), and "written inside a code fence" is false
    of that line; `commented_row_at` below is the question about it. So this
    asks the reader WHICH kind hid the line rather than taking the complement
    of what it shows.
    """
    return hidden_row_at(home, "fence")


def commented_row_at(home):
    """(index, line) for this gate's row written inside an HTML comment that
    closes, or (None, None) -- `fenced_row_at`'s question about the other
    kind of block the reader hides (#667). A row somebody parked in a comment
    is not an answer they gave, so no walk of the table reads it; and then the
    absent-row refusal would send them to write a row they can see, and the
    fence refusal would name a fence that is not there, which is the
    wrong-cause shape #415 and #429 were opened about."""
    return hidden_row_at(home, "comment")


def hidden_row_at(home, kind):
    """(index, line) for the first line naming this gate's row that the one
    reader hides as KIND, or (None, None). The kind is the reader's answer,
    `hooks/config.py#hidden_lines`, never a walk of this file's own."""
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return None, None
    lines = text.splitlines()
    hidden, _opened_at = config.hidden_lines(lines, text)
    return next(
        (
            (index, line)
            for index, line in enumerate(lines)
            if hidden.get(index) == kind and names_this_row(line)
        ),
        (None, None),
    )


def fenced_row(home):
    """This gate's row written INSIDE a code fence — as written, with its own
    indentation — or None.

    **The one question about a fenced line anybody asks, and this gate is the
    only one that may ask it.** `hooks/config.py#unfenced` makes a fenced line
    invisible to all three walks of that table, which is what stops an example
    from being the command this gate seals over (#429). It also makes a
    `Broad gate` line written only inside a fence look exactly like no row at
    all — and then the absent-row refusal below is a true sentence about a
    cause that is not the real one, which is the failure #415 was opened
    about, arriving one shape over. So the line is found again here, on the
    refusal path alone.

    Asked by THIS command and by nothing else. `hooks/config.py` and
    `hooks/mode-gate.py` say nothing about a fence: a `PreToolUse` hook that
    prints is noise on every Bash call, where this command speaks once and
    only when it refuses.

    It reads the fence rule from the one reader and asks it which lines it
    hid inside a fence — `hooks/config.py#hidden_lines`, which also hides a
    line in an HTML comment and says which it was (#667) — rather than
    walking the file by a rule of its own. A second fence rule written here
    would answer a different question about the same file, which is the split
    `hooks/config.py` exists to prevent.

    **The line alone**, which is what a message quotes. `fenced_row_at` above
    is the same answer with the index beside it, for the one caller that has
    to say where the line is relative to a fence.
    """
    return fenced_row_at(home)[1]


def fence_left_open(home, above=None):
    """Whether a fenced code block ABOVE the line at index ABOVE is never
    closed — or anywhere in the file, where ABOVE is None.

    Read off the one fence rule, not a second one. It is the difference
    between a row somebody pasted into an example block and a row that is in
    the live table with a fence opened above it — and the two need different
    sentences, because the second person has nothing to move. Told to move a
    row that is already where it belongs, they follow the instruction exactly
    and nothing changes, which is the wrong-cause shape #415, #429 and #430
    were each opened about.

    False for every way of not having an answer: no file, a file that will not
    read, a file with no fence in it at all.

    **Above, because that is what the sentence says.** A file whose row sits
    in an example block that closes and which opens a second block further
    down answered True here, and the person was told to close a fence that has
    nothing to do with their row while the act they needed — move it — was the
    sentence they did not get (#429, round 2).
    """
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return False
    opened_at = config.fence_map(text.splitlines(), text)[1]
    if opened_at is None:
        return False
    return above is None or opened_at < above


def missing_row(home):
    """The refusal for a row the gate could not read — and there are three,
    because there are three causes and what a person does about each one is
    different.

    Where the row IS in the file and the line will not parse, saying it is
    absent is a true sentence about a cause that is not the real one: the
    person goes looking for a row that is sitting in front of them. So that
    line is quoted back and the escape is named (#415). The whole line is
    quoted rather than its first cell, because a refusal that does not show
    the line sends the reader back to the file to guess which one it meant
    (`questions.md` W1).

    **What that line cost is a condition, and the sentence says which way it
    fell.** The reader breaks on a line it cannot parse only once it has
    found a row, so a refused line written as the table's FIRST row loses
    only itself and every row under it still arrives. Telling that person
    their rows were lost sends them to reformat rows that were read
    correctly, which is this work item's own defect one file over — so the
    cost sentence is read off the file, never stated flat (#415 round 1
    🟡 1).

    **It is read off the line that actually stopped the reader, which is
    not always the line being quoted.** A file with two lines the reader
    will not take has four shapes, and each gets its own sentence: nothing
    stopped the reader at all; this line stopped it; this line was read and
    something LOWER DOWN stopped it, so the rows under that line are the
    lost ones; or the reader had already stopped ABOVE this line and never
    met it. Chosen from a flat `ended` these collapsed into two, and both of
    the two were false about the two-line file — the rows below were lost
    while the refusal said they were read (#415 round 2 🟡 1).

    **Three of those four then ask what was actually written below, because
    a sentence about rows below a line is false where no row is below it**
    (#430). A `Broad gate` line written LAST in its table — the shape this
    repository's own `seal/config.md` has, and the shape the table
    `templates/config.md` ships has — lost nothing with it, and being told
    that every row below it is gone sends that person looking for rows they
    never wrote. So each of those three sentences has a subject in every
    state, and the fourth needs none: its clause *this one included* names
    the quoted line itself. The signal differs by arm and the difference is
    not cosmetic — the two arms with a stopping line read `below`, and the
    arm without one reads `rows_read`, whose docstring says why `below` is
    empty there either way.

    **And a sentence about what was WRITTEN cannot be answered from rows
    alone.** `below` holds what parsed; a further line the reader will not
    take as a row is written under that line too, and `refused` is where it
    is. So each of those sentences says *no ROW was written*, which is what
    the value supports, and the two arms that go on to predict that one edit
    finishes the file — *this one line is the whole of what changes* — say
    instead that fixing it moves the stopping place down, because that is
    what a further refused line below makes true. Measured at all four sites
    with a second malformed line below (#430, round 1); `spec.md`
    §*Data & interfaces* fixed the old wording, and `overview.md` §*Where spec
    and implementation diverged* records the correction with both sides
    quoted.

    **The fifth arm is the one where following this message makes the file
    worse**, and it was the one arm with nothing to say about what lies below.
    Where the rows below the quoted line were read, repairing that line is
    what lets the stop rule stop — and it then stops at the next line this
    reader will not take, so rows that arrive today go with the repair.
    Measured: `config_rows` returns the `Mode` row before the instructed edit
    and the `Broad gate` row after it (#430, round 2). That arm now says there
    is more than one line to write here.

    **The third cause is a row written where no walk of that table reads
    it.** A `| Broad gate |` line inside a code fence is an example of the
    format rather than this repository's own answer, and `hooks/config.py#
    unfenced` is what stops every walk from reading one (#429). That leaves
    the line looking exactly like no row at all, so the absent-row refusal
    below would send a person to write a row they can already see — the
    wrong-cause message this whole work item exists to end. `fenced_row`
    above finds it and the refusal says where it has to move to.

    Where there is no such line, the message is the absent-row refusal
    unchanged. It used to say *write the repository's own broad command into
    it* and print the row to type. The only reader standing here is a
    session, so what that sentence asked for is the one thing the row may not
    be: #401 is a session that met this message after its review rounds had
    settled, ran four candidate commands, chose one, wrote the row, and told
    the owner afterwards. The message now says whose the row is and where
    they answer it.
    """
    refused, below, stopper = refusal(home)
    # Two tails, because two of these sentences are about the line this gate
    # QUOTES and two are about the line that STOPPED the reader. Each is the
    # lines below its own subject that this reader will not take as rows —
    # which `below` cannot answer, holding only what parsed (#430, round 1).
    mine, reached, after_mine, after_stopper = None, False, [], []
    for position, (line, got) in enumerate(refused):
        if mine is None and names_this_row(line):
            mine, reached = line, got
            after_mine = [text for text, _got in refused[position + 1 :]]
            break
    if stopper is not None:
        # **The stopper's POSITION, not its identity.** `refused` holds line
        # text, and CPython hands back one shared object for every
        # one-character string — so two refused lines that are both `|` are
        # the same object, `line is stopper` matched both, and the tail came
        # from the last of them with the clause about the lines below silently
        # dropped. Every entry appended before the stopper carries `got` True
        # and the stopper's is the last of those, which is a fact about how
        # `refusal` fills the list rather than about the text (#430, round 2).
        last_reached = max(
            position for position, (_line, got) in enumerate(refused) if got
        )
        after_stopper = [text for text, _got in refused[last_reached + 1 :]]
    moves_the_stop = (
        ". There are more lines below it this reader will not take as rows "
        "either, so fixing this one moves the stopping place down rather "
        "than clearing the table"
    )
    if mine is not None:
        if stopper is None:
            if rows_read(home):
                # **The one arm where doing what this message asks makes the
                # file worse**, and it was the one arm with nothing to say
                # about what lies below. Measured over a file whose quoted
                # line, a second malformed line and a `Mode` row stand in that
                # order: the reader returns the `Mode` row today and loses it
                # once the quoted line parses, because the stop rule the
                # repair switches on then stops at the second malformed line
                # (#430, round 2).
                cost = (
                    ". The rows below it were read: nothing had parsed above "
                    "this line, so the table had not begun and the stop rule "
                    "needs a row before it can stop"
                ) + (
                    ""
                    if not after_mine
                    else ". Fixing this line is what lets the stop rule stop, "
                    "and the next line below it this reader will not take as "
                    "a row is where it will — so the rows under THAT line, "
                    "which arrive today, go with the repair. There is more "
                    "than one line to write here"
                )
            else:
                cost = (
                    ". Nothing else was lost with it, because no row was "
                    "written below it: nothing had parsed above this line "
                    "either, so the table had not begun and the stop rule "
                    "needs a row before it can stop"
                ) + (moves_the_stop if after_mine else "")
        elif mine is stopper:
            if below:
                cost = (
                    " — and every row written BELOW that line is lost with "
                    "it, each falling back to its default with nothing said "
                    "anywhere"
                )
            else:
                cost = (
                    " — and no row was written below it, so nothing else was "
                    "lost with it"
                ) + (
                    ": this one line is the whole of what changes"
                    if not after_mine
                    else moves_the_stop
                )
        elif reached:
            if below:
                under = (
                    "so every row under that line is lost, each falling back "
                    "to its default with nothing said anywhere"
                )
            else:
                under = (
                    "and no row was written under that line, so nothing else "
                    "was lost with it"
                ) + (
                    ": that one line is the whole of what changes"
                    if not after_stopper
                    else ". There are more lines below THAT one this reader "
                    "will not take as rows either, so fixing it moves the "
                    "stopping place down rather than clearing the table"
                )
            cost = (
                ". The rows directly below it were read — nothing had parsed "
                "above this line, and the stop rule needs a row before it can "
                "stop. The reader stopped LOWER DOWN, at\n"
                f"    {stopper.strip()}\n" + under
            )
        else:
            cost = (
                ". The reader never even reached it: it had already stopped "
                "ABOVE it, at\n"
                f"    {stopper.strip()}\n"
                "so every row from there down is lost — this one included — "
                "each falling back to its default with nothing said anywhere"
            )
        return (
            f"broad-gate: {os.path.join(home, CONFIG)} has a `{ROW}` line "
            "and this is it, written so that it does not parse as a row of "
            "that table:\n"
            f"    {mine.strip()}\n"
            f"Nothing read it, so there is no command to seal over{cost}.\n"
            "A cell of that table ends at a `|`. A value that needs one is "
            "written with markdown's own escape, `\\|`, which the reader "
            "reduces to a plain pipe before any shell sees it — so "
            f"`| {ROW} | bin/test -q \\| tee out.txt |` is the row that runs "
            "that command. `templates/config.md` §*What is refused, and what "
            "stays allowed* is where the row says so, and `/specseal:config` "
            "is the door to it. Nothing ran."
        )
    if stopper is not None and hides_this_row(below):
        # The same condition as the three arms above, asked of the one row
        # this branch already knows about: `hides_this_row` is true only
        # when `below` holds this gate's row, so a one-element `below` is
        # this row and nothing else, and *every OTHER row* then names rows
        # nobody wrote (#430, site 4).
        if len(below) > 1:
            others = (
                "Every other row under that line is gone the same way, each "
                "falling back to its default."
            )
        else:
            # `below` holds rows, so *nothing else was written* is a claim
            # about the file this value cannot support: a further line the
            # reader will not take as a row is written under that line too,
            # and `refused` is where it is (#430, round 1).
            others = (
                "No other row was written under that line, so nothing else "
                "was lost with it."
            ) + (
                ""
                if not after_stopper
                else " There are more lines below it this reader will not "
                "take as rows either."
            )
        return (
            f"broad-gate: {os.path.join(home, CONFIG)} has a `{ROW}` row and "
            "the reader never reached it. This line above it does not parse "
            "as a row of that table, and the reader stops reading there:\n"
            f"    {stopper.strip()}\n"
            f"So the `{ROW}` row written BELOW it is invisible, and there is "
            f"no command to seal over. {others}\n"
            "A cell of that table ends at a `|`. A value that needs one is "
            "written with markdown's own escape, `\\|`, which the reader "
            "reduces to a plain pipe before any shell sees it. "
            "`templates/config.md` §*What is refused, and what stays allowed* "
            "is where the row says so, and `/specseal:config` is the door to "
            "the file. Nothing ran."
        )
    at, fenced = fenced_row_at(home)
    if fenced is not None:
        # Two causes, two acts, and the person in the second case has nothing
        # to move: their row is in the live table and a fence opened ABOVE it
        # was never closed, so it runs to the end of the file and takes the
        # whole table with it. Told to move the row they would follow the
        # instruction exactly and change nothing (#429, round 1). The fence
        # has to be above the row: one opened below it leaves the row inside a
        # block that closes, where moving it is still the act (#429, round 2).
        where = (
            "A fenced code block above it is never closed, so it runs to the "
            "end of the file and takes the whole table with it. Close that "
            "fence — the row itself may already be where it belongs."
            if fence_left_open(home, at)
            else "Move the row into the `| Item | Value |` table that stands "
            "outside every fence, or add that table if the file has none."
        )
        return (
            f"broad-gate: {os.path.join(home, CONFIG)} has a `{ROW}` line and "
            "this is it, written inside a code fence:\n"
            f"    {fenced.strip()}\n"
            "A table inside a code fence is an example of the format and not "
            "this repository's own answer, so no walk of that table reads it "
            "— not this gate's reader, not the mode gate's, and not "
            "`seal mode`'s writer. The row is not absent: it is written where "
            f"nothing reads it, and there is no command to seal over.\n{where}\n"
            "`templates/config.md` §*What is refused, and what stays allowed* "
            "is where the rule says so, and `/specseal:config` is the door to "
            "the file. Nothing ran."
        )
    _at, commented = commented_row_at(home)
    if commented is not None:
        # The fourth cause (#667). A row parked in an HTML comment that closes
        # is one somebody took out of the table, so no walk reads it, and
        # neither the absent-row sentence nor the fence sentence is true of
        # it. The one act is the person's: take it out of the comment if it
        # is the command to seal over.
        return (
            f"broad-gate: {os.path.join(home, CONFIG)} has a `{ROW}` line and "
            "this is it, written inside an HTML comment:\n"
            f"    {commented.strip()}\n"
            "A row inside a comment that closes is parked, not this "
            "repository's answer, so no walk of that table reads it — not this "
            "gate's reader, not the mode gate's, and not `seal mode`'s writer. "
            "The row is not absent and it is not in a code fence: it is "
            "commented out, and there is no command to seal over.\n"
            "If it is the command to seal over, take the row out of the "
            "comment and into the `| Item | Value |` table.\n"
            "`templates/config.md` §*What is refused, and what stays allowed* "
            "is where the rule says so, and `/specseal:config` is the door to "
            "the file. Nothing ran."
        )
    return (
        f"broad-gate: {os.path.join(home, CONFIG)} has no `{ROW}` row, so "
        "there is no command to seal over — and choosing one is not this "
        "session's to do. There is no default because a row is a thing a "
        "person wrote, and what the sealer's seal covers is exactly that "
        "(`skills/verify/SKILL.md` §*The Seal Test*): a session that picks a "
        "command here seals its own choice.\n"
        "Take it to whoever owns the repository. `/specseal:config` is where "
        f"they answer it — it shows every row and adds this one with its "
        "section — and `templates/config.md` §*Choosing a value — the "
        "criterion* is what they choose against. Nothing ran."
    )


# --- looking at the value before a shell gets it -------------------------


def wholly_substituted(value):
    """The opening delimiter of a command substitution wrapping the WHOLE
    value — `` ` `` or `$(` — or None where nothing wraps it.

    A pair that closes early wraps a part rather than the whole, and a part
    is the repository's own composition: `pytest -n $(nproc)` still runs as
    the command it reads as. So `$(a) && b` reads as None here, and so does
    `` `a` && `b` `` — a row nothing in this module claims to catch. Both
    fall out of one reading, which is the point: what is refused is a form,
    not the characters in it.
    """
    if len(value) > 1 and value[0] == "`" == value[-1]:
        return "`" if "`" not in value[1:-1] else None
    if not value.startswith("$(") or not value.endswith(")"):
        return None
    depth = 0
    for i, char in enumerate(value[1:], 1):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return "$(" if i == len(value) - 1 else None
    return None


def not_as_written(home, command):
    """The refusal for a `Broad gate` value the gate would not run as the
    command it reads as — or None for every value it would.

    **The criterion has two halves: the value must run as the command it
    reads as, and the exit code the gate reads must be that command's.**
    `templates/config.md` §*Broad gate* owns it, owns the list of refused
    forms and owns the list of what stays allowed, each with its reason.
    This function is the half that acts; a form belongs here only by failing
    one of those halves there.

    Three forms fail one. The whole value wrapped in backticks, or in the
    `$(…)` spelling of the same thing, runs the checks first, DISCARDS their
    exit status, and executes their output as a command — measured on #402:
    the same content exits 1 bare and 0 wrapped, with the failure still on
    the screen. A trailing `&` backgrounds the line, so the shell answers 0
    before any check has finished.

    Everything else stays legal, a pipe included, because the row is an
    arbitrary shell command line by design and telling a status-discarding
    `;` from one inside a quoted argument needs a shell parser — whose own
    failure modes would make legitimate rows unwritable.

    Nothing is stripped or rewritten. A value silently repaired here leaves
    the file still wrong and teaches the next person that it was right.
    """
    value = command.strip()
    opener = wholly_substituted(value)
    if opener == "`":
        form = "is the whole command wrapped in backticks"
        does = (
            "so a shell reads it as command substitution: the checks run "
            "first, their exit status is DISCARDED, and their output is then "
            "executed as a command. What this gate would read is that "
            "command's exit code and not the checks'"
        )
    elif opener == "$(":
        form = "is the whole command wrapped in `$(…)`"
        does = (
            "which is command substitution in its other spelling and does "
            "the same thing: the checks' exit status is DISCARDED and their "
            "output is executed as a command in its place"
        )
    elif value.endswith("&") and not value.endswith("&&"):
        form = "ends in a single `&`"
        does = (
            "so `/bin/sh` backgrounds the whole line and answers 0 before any "
            "check has finished. A seal drawn from that 0 covers nothing that "
            "ran. Under `cmd.exe` the same character separates two commands "
            "instead, which is a different wrong answer refused for the same "
            "reason: the exit code read is not the checks'"
        )
    else:
        return None
    rewritten = (value[len(opener) : -1] if opener else value[:-1]).strip()
    return (
        f"broad-gate: the `{ROW}` row in {os.path.join(home, CONFIG)} {form}, "
        f"{does}.\n"
        f"    as written: | {ROW} | {value} |\n"
        f"    as meant:   | {ROW} | {rewritten} |\n"
        "Nothing ran, and nothing was repaired: the row is a person's to "
        "write, and a value quietly fixed here would leave the file still "
        "wrong. `templates/config.md` §*Broad gate* lists what is refused "
        "and what stays allowed, with the reason for each, and "
        "`/specseal:config` is the door to the row."
    )


# --- running one check ---------------------------------------------------


class Check:
    """One check's name, exit code, output text and where the output is."""

    def __init__(self, name, code, text, path):
        self.name, self.code, self.text, self.path = name, code, text, path

    @property
    def failed(self):
        return self.code != 0

    def first_lines(self, n=QUOTED):
        lines = [ln.rstrip() for ln in self.text.splitlines() if ln.strip()]
        return lines[:n]


def run(name, command, root, keep, shell=False, env=None, windows=None, comspec=None):
    """Run one check from the repository root, keep its output under
    `keep/<name>.txt`, and return it with the exit code read directly.

    **A shell string is handed over through `handed_to_shell`**, which is the
    one place this module's shell sites meet: `gate`'s `SUITE` and
    `compare_at_base`'s `suite-at-base` both arrive here, so neither needed a
    change of its own (#448). Where what the shell is handed differs from what
    the row says, one stderr line says so before the run, and the kept file
    carries both lines above the exit code — the row as written first, because
    that is the line a reader retypes. `windows` and `comspec` are the
    platform, passed through, so a case can drive the `cmd.exe` branch from
    any machine the way `quote` is driven. `root` is passed through too,
    because it is where the row runs, and so where a command name's first
    part is asked whether it is a directory (#596).
    """
    handed = handed_to_shell(command, windows, comspec, root) if shell else command
    rewritten = shell and handed != command
    if rewritten:
        sys.stderr.write(handed_line(name, handed) + "\n")
    r = subprocess.run(
        handed,
        cwd=root,
        shell=shell,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    text = r.stdout + ("\n" if r.stdout and r.stderr else "") + r.stderr
    path = os.path.join(keep, f"{name}.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(f"$ {command if shell else shlex.join(command)}\n")
        if rewritten:
            handle.write(f"{HANDED} {handed}\n")
        handle.write(f"exit {r.returncode}\n\n")
        handle.write(text)
    return Check(name, r.returncode, text, path)


# --- what `cmd.exe` is handed ------------------------------------------------
#
# `subprocess.run(..., shell=True)` on Windows runs `%COMSPEC% /c "<string>"`,
# and `COMSPEC` is `cmd.exe` unless somebody changed it. `cmd.exe` reads a `/`
# in a command NAME as the start of a switch, so the row `bin/test -q && …`
# runs a command called `bin` with the argument `/test`, prints "not
# recognized" in the machine's own language, and exits 1 — which the failure
# form then reports as the suite failing (#448). `bin/test.cmd` exists so that
# `cmd.exe` can call the runner, and it is reached as `bin\test`.

CMD_EXE = "cmd.exe"
# The kept file's second line where the shell was handed something else.
HANDED = "cmd.exe was handed:"


def handed_line(name, handed):
    """The one stderr line a rewritten check prints before it runs."""
    return (
        f"broad-gate: {name} — cmd.exe reads a `/` in a command name as the "
        f"start of a switch, so a command name that starts in a directory has "
        f"its `/` handed to it as `\\`: {handed}"
    )


CMD_VARIABLE = re.compile(r"%([^%]+)%")


def as_cmd_expands(part, here):
    """`part` with each plain `%NAME%` replaced as `cmd /c` replaces it
    before it reads a command name (#596). What of `cmd.exe`'s expansion is
    modelled is the list below, and nothing past it.

    A name defined in this process's environment takes its value, which is
    the environment `run` hands the shell. Where the environment defines
    neither `CD` nor `__CD__`, `cmd.exe` computes them, and both name the
    directory the row runs in, which is `here`. A defined one wins, as it
    does in `cmd.exe` (`set /?`), so the environment is asked first (#616).
    Any other name is left as written, as `cmd /c` leaves an undefined one,
    and so is `%%`. A substring or substitution (`%NAME:~0,2%`,
    `%NAME:a=b%`) is not modelled and is left as written too, so a name that
    starts with one keeps its `/`. Nor is where `cmd.exe` resumes scanning
    after an undefined name: this resumes after the name's closing `%`, and
    whether `cmd.exe` does is unverified, since only a Windows run answers
    it. Nothing else is expanded: `$NAME` and `'…'` mean nothing to
    `cmd.exe`, which is why this is not `ntpath.expandvars`.
    """

    def value(match):
        name = match.group(1)
        if name in os.environ:
            return os.environ[name]
        if name.upper() == "CD":
            return os.path.abspath(here)
        if name.upper() == "__CD__":
            return os.path.join(os.path.abspath(here), "")
        return match.group(0)

    return CMD_VARIABLE.sub(value, part)


def cmd_exe_reads(windows=None, comspec=None):
    """Whether `subprocess.run(..., shell=True)` hands its string to
    `cmd.exe`: Windows, where `COMSPEC` names `cmd.exe` or is unset, which
    Python answers with `cmd.exe` too.

    `handed_to_shell` rewrites a command name only for `cmd.exe`, and this
    is where it asks (#747). `windows` and `comspec` default to this
    machine's, for the reason `handed_to_shell`'s docstring gives.
    """
    if windows is None:
        windows = os.name == "nt"
    if not windows:
        return False
    if comspec is None:
        comspec = os.environ.get("COMSPEC")
    # `ntpath` whatever this machine is: `C:\Windows\System32\cmd.exe` has no
    # `/` in it for `posixpath.basename` to split at.
    return not comspec or ntpath.basename(comspec.strip().strip('"')).lower() == CMD_EXE


def handed_to_shell(command, windows=None, comspec=None, root=None):
    """The string `subprocess.run(command, shell=True)` should be given.

    `command` unchanged everywhere but one place: Windows, where the shell
    `COMSPEC` names is `cmd.exe` — or `COMSPEC` is unset, which Python
    answers with `cmd.exe` too. There a COMMAND NAME that starts in a
    directory has its `/` written `\\`, and nothing else changes
    (`command_names_backslashed`).

    **The directory is asked here, and the scan stays pure.** `root` is
    where the row runs — `run`'s own `root`, which is the repository for
    `gate` and the scratch worktree for `compare_at_base` — and a name's
    first part is a directory where `os.path.isdir(os.path.join(root,
    part))` says so, once any `%VAR%` in it is expanded, because `cmd.exe`
    expands it before it reads the name — as far as `as_cmd_expands` models
    that expansion, which its docstring states; a variable that names
    nothing stays as written and names no directory.
    `None` is the current directory, which is where
    `subprocess.run` with `cwd=None` would run the row. The read happens
    here because this function already reads `COMSPEC` from the
    environment; the scan takes the answer as an argument (#596).

    Keyed on the shell and not on `os.name` alone, because a Windows machine
    can name a POSIX shell in `COMSPEC` (`tests/conftest.py#
    posix_row_shell_or_skip` exists for that machine), and a POSIX shell
    runs `bin/test` as written. `windows` and `comspec` default to this
    machine's, and are arguments so that both branches can be driven from
    either platform — `quote`'s docstring says what reading `os.name` in the
    body cost the last time.
    """
    if not cmd_exe_reads(windows, comspec):
        return command
    here = os.curdir if root is None else root
    # `cmd.exe` expands `%VAR%` before it reads the name, so the part is
    # expanded before it is asked, as far as `as_cmd_expands` models it.
    return command_names_backslashed(
        command,
        lambda part: os.path.isdir(os.path.join(here, as_cmd_expands(part, here))),
    )


# `cmd.exe`'s own commands. Written straight against one of them, a `/` is
# that command's switch -- `rd/s/q`, `dir/b`, `cd/d` -- and `cmd.exe` runs the
# row as written. Turned into `\` it stops being a switch, so it is left.
CMD_BUILTINS = frozenset(
    {
        "assoc",
        "break",
        "call",
        "cd",
        "chdir",
        "cls",
        "color",
        "copy",
        "date",
        "del",
        "dir",
        "echo",
        "endlocal",
        "erase",
        "exit",
        "for",
        "ftype",
        "goto",
        "if",
        "md",
        "mkdir",
        "mklink",
        "move",
        "path",
        "pause",
        "popd",
        "prompt",
        "pushd",
        "rd",
        "rem",
        "ren",
        "rename",
        "rmdir",
        "set",
        "setlocal",
        "shift",
        "start",
        "time",
        "title",
        "type",
        "ver",
        "verify",
        "vol",
    }
)


def command_names_backslashed(command, is_directory):
    """`command` with `/` written `\\` inside each word `cmd.exe` reads as a
    command name and that starts in a directory, and every other character
    exactly where it was.

    **Which names start in a directory is asked, not read.** `is_directory`
    is called with the part of a name before its first `/`, with its `"`
    and `^` removed and every leading `@` dropped, as the built-in check
    drops them, and answers whether that
    part names a directory. The scan does no I/O of its own:
    `handed_to_shell` asks the filesystem where the row runs, and a case
    can answer from any machine. An empty part is a name that begins with
    `/`, which starts at the drive's root; that always exists, so it is
    answered here without asking.

    **A position scan over the string, never a tokenise-and-re-render**,
    because re-rendering is how quoting gets lost. The part of `cmd.exe`'s
    lexer it models:

      - a word is in COMMAND POSITION at the start of the line and after
        `&&`, `||`, `&` or `|`; blanks and a `(` that opens a block are
        passed over there, and the word begins at the next character;
      - the command name runs from there to the first unquoted blank, tab,
        `<`, `>`, `&`, `|` or `(`. At its first `/` one decision is made for
        the whole name: where the part before it names a directory, that
        `/` and every later one in the name become `\\` — inside a quoted
        stretch too, since a quoted Windows path takes `\\`; where it does
        not, every `/` in the name is handed over as written, because
        `bin/test` is a path and `xcopy/e` is a program and its switch;
      - `"` is the only quote; outside one, `^` escapes the next character,
        and that character is copied as written, so `^&` is never a
        separator and `^/` is never rewritten — in command position it is
        the name's first character, so `^a b/c` keeps `b/c` an argument;
      - a `<` or `>` ends command position until the next separator;
      - a `/` written straight after one of `cmd.exe`'s own commands
        (`CMD_BUILTINS`, a leading `@` aside) is that command's switch, so
        `rd/s/q` and `dir/b` stay as written and the name ends there. This
        is asked first, before any directory, so a `dir/` directory in the
        tree does not turn `dir/b` into a path.

    Three things `cmd.exe` does are left unmodelled because modelling them
    changes no output, and a branch that changes no output is one nothing
    can hold: a leading `@` is read as the first character of the name,
    which has no `/` in it, and is dropped only where the name is asked
    about — the built-in check and the directory part; a `)` does not end
    a name, which only matters for a `/` written straight after one; and
    the `&` of `2>&1` is read as a separator, which makes the handle digit
    after it a "name" with no `/` in it. The `2>&1` case in `tests/test_the_gate_hands_cmd_a_path_it_can_
    run.py` holds that last one to what it hands over.

    **Not rewritten, and named rather than claimed:** a path after `call`,
    `start`, `if`, `else`, `for … do` or `cmd /c`, which `cmd.exe` reads as
    an argument of those words and then splits exactly as it did before this
    existed; and a command name after a redirection at the start of a
    command (`>out bin/test`), where this scan stops treating the rest as
    command position. None is worse than the row handed as written, and
    `templates/config.md` §*Broad gate* states the rule and these examples.

    **Judged where the row starts, and bounded there, named rather than
    claimed:** a directory an earlier command in the same row makes, or
    one a `cd` earlier in the row enters, is not seen, so that name is
    handed over as written — which is what `cmd.exe` got before #448, and
    no worse than the row itself. And a directory at the root named like a
    program the row calls with a glued switch (an `xcopy/` directory)
    makes `xcopy/e` read as a path; `cmd.exe` itself is ambiguous in that
    tree, and a blank before the switch (`xcopy /e`) is never rewritten.
    `templates/config.md` §*Broad gate* states both.
    """
    out = []
    at_command = True  # the next word read is a command name
    in_name = False  # inside that command name now
    quoted = False
    start = 0  # where the current command name began
    turned = None  # the name's one decision, taken at its first `/`

    def opens_name(at):
        nonlocal at_command, in_name, start, turned
        at_command, in_name, start, turned = False, True, at, None

    def turn(at):
        """Whether the name's `/` at `at` is written `\\`."""
        nonlocal turned
        if turned is None:
            part = command[start:at]
            part = part.lstrip("@").replace('"', "").replace("^", "")
            turned = part == "" or bool(is_directory(part))
        return turned

    i, n = 0, len(command)
    while i < n:
        c = command[i]
        if quoted:
            if c == '"':
                quoted = False
            elif c == "/" and in_name and turn(i):
                c = "\\"
            out.append(c)
            i += 1
            continue
        if c == '"':
            quoted = True
            if at_command:
                opens_name(i)
            out.append(c)
            i += 1
            continue
        if c == "^":
            # The escaped character is the name's first one where it stands
            # in command position, so the next blank ends that name.
            if at_command:
                opens_name(i)
            out.append(command[i : i + 2])
            i += 2
            continue
        if c in "&|":
            # `&&` and `||` are two of these in a row, which is the same state.
            at_command, in_name = True, False
        elif c in "<>":
            at_command, in_name = False, False
        elif c in " \t(":
            # A `(` opens a block in command position, which stays command
            # position; anywhere else it ends the name, so `echo(a/b)` keeps
            # its argument as written.
            in_name = False
        else:
            if at_command:
                opens_name(i)
            if c == "/" and in_name:
                if command[start:i].lstrip("@").lower() in CMD_BUILTINS:
                    # A built-in's switch, written against it: as written.
                    in_name = False
                elif turn(i):
                    c = "\\"
        out.append(c)
        i += 1
    return "".join(out)


def draft_env(keep):
    """The environment `chain_check.py` runs under: a draft pull-request
    payload, unless the caller's environment already carries one.

    The gate runs BEFORE `seal` writes the cell, so at this moment the last
    record honestly reads `not yet` — and `chain_check.py` judged as READY
    fails that cell as the run that never happened. Judged as a draft it
    excuses exactly that and nothing else, the way `round_record.run_check`
    already does for a record being generated. Inside a workflow the payload
    GitHub wrote is the authority and is left alone.
    """
    env = dict(os.environ)
    if env.get("GITHUB_EVENT_PATH"):
        return env
    payload = os.path.join(keep, "draft-event.json")
    with open(payload, "w", encoding="utf-8") as handle:
        json.dump({"pull_request": {"draft": True}}, handle)
    env["GITHUB_EVENT_PATH"] = payload
    return env


def exemptions(home):
    return sorted(glob.glob(os.path.join(home, SPECS, "*", SURVIVORS)))


# --- the reactive base comparison ------------------------------------------
#
# #825. Four designs in a row inferred which pytest process printed a line,
# from the row's text and from what pytest printed, and each fix moved the
# guess one level up. The gate now loads a recorder of its own into every run
# it measures, and the pytest process that collected a test is the process
# that writes that test's outcome down. No line pytest printed is read for a
# word, and no file is appended to any run.

# The recorder's directory, which holds the recorder and nothing else, so the
# row's interpreter is shown nothing else of this plugin's through
# `PYTHONPATH`. Beside this file, so a tree that ships its own gate ships its
# own recorder with it (`gate_copy`).
RECORDER_DIR = os.path.join(HERE, "pytest_record")
RECORDER = "specseal_pytest_record"
# The four variables a measured run is handed, and the directory under the
# kept output the records go in. The two the recorder reads are its own
# module's names, written again here rather than imported, because the
# recorder runs in the row's interpreter and this file is never loaded there.
RECORD_KEY_VARIABLE = "SPECSEAL_RECORD_KEY"
RECORD_DIR_VARIABLE = "SPECSEAL_RECORD_DIR"
RECORDS = "records"
# The kept name of the row's one run at the base.
BASE_RUN = "suite-at-base"


def record_key(kind):
    """A key made fresh for one run: `head-<16 hex>` or `base-<16 hex>`.

    Fresh per run is what makes a record left in the directory by anything
    else — an earlier gate run into the same `--keep-output`, a test that
    writes there — carry another key, so the reader passes over it."""
    return f"{kind}-{secrets.token_hex(8)}"


def records_dir(keep):
    """The absolute directory every record of this gate run goes in. Absolute,
    because the row may `cd` before it starts pytest."""
    return os.path.join(os.path.abspath(keep), RECORDS)


def recording_env(keep, key):
    """The environment a run the gate measures is handed (`#825`): this
    process's own, with the recorder's directory first on `PYTHONPATH`,
    ` -p specseal_pytest_record` appended to whatever `PYTEST_ADDOPTS` holds,
    and the recorder's two variables set — the records directory, made here,
    and `key`.

    Every pytest the row starts inherits all four. The first session in a
    process that finds the key claims it and takes it out of that process's
    environment, so a pytest it starts in turn — one a test spawns, an xdist
    worker — records nothing. A row that replaces either variable rather than
    adding to it takes the recorder away from its runs; `templates/config.md`
    rule 3 says what that costs."""
    env = dict(os.environ)
    directory = records_dir(keep)
    os.makedirs(directory, exist_ok=True)
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in (RECORDER_DIR, env.get("PYTHONPATH")) if part
    )
    env["PYTEST_ADDOPTS"] = f"{env.get('PYTEST_ADDOPTS', '')} -p {RECORDER}".lstrip()
    env[RECORD_DIR_VARIABLE] = directory
    env[RECORD_KEY_VARIABLE] = key
    return env


class RunRecord:
    """What the records carrying one key say about the run they came from.

    `sessions` is how many pytest sessions claimed the key. `failing` holds
    every file with a failing test, in any phase, or a failed collection, in
    the order the records first name it; `collected` every file any line
    names. A file is its path made relative to the run's worktree and
    spelled with `/`, or its absolute path where it lies outside the
    worktree. `unread` counts the lines of the keyed files that did not
    parse as an object, which the recorder never writes (#869); another
    run's file is not counted. `counts` is how many reports pytest's own
    summary line counts under each category, over the keyed sessions, in
    the order each category was first written: a `test` line under its
    `category`, a failed collection under `error` and a skipped one under
    `skipped`, as pytest's terminal reporter counts them. `unplaced` sums the
    `end` lines' counts of the tests and collections the recorder wrote as
    no line, for want of a file of their own (#825's reframe after round 3);
    `unplaced_red` sums only those of sessions whose `end` line shows a
    non-zero exit, because a session that exited 0 failed nothing, counted
    or not (#825 round 5). `unended` counts the sessions that stopped
    part-way: those whose record holds no `end` line, because the process
    died or the recorder stopped writing (#849); those whose `end` line says
    pytest stopped the session -- an interrupt, `pytest.exit()`, `-x` or
    `--maxfail`, a plugin's stop (#852); and those whose `end` line shows an
    exit `RAN_TO_ITS_END` does not hold, the net for a stop no hook showed
    (#849 round 1).

    Named apart from `Record`, which is a round record's home (#666)."""

    __slots__ = (
        "collected",
        "counts",
        "failing",
        "sessions",
        "unended",
        "unplaced",
        "unplaced_red",
        "unread",
    )

    def __init__(self):
        self.sessions, self.unread, self.unplaced = 0, 0, 0
        self.unplaced_red, self.unended = 0, 0
        self.failing, self.collected, self.counts = {}, set(), {}


def record_path(path, worktree):
    """`path` as the comparison names a file: its `realpath` made relative to
    the `realpath` of `worktree`, with `/`, or its `realpath` where it is not
    under the worktree.

    `realpath` on both sides is not optional: pytest reports its rootdir
    resolved, and on macOS a `mkdtemp` directory and that rootdir spell one
    place `/var/…` and `/private/var/…` (`phases/phase-1.md` of 1791270161).
    """
    real = os.path.realpath(path)
    try:
        rel = os.path.relpath(real, os.path.realpath(worktree))
    except ValueError:
        # Another drive on Windows: not under the worktree.
        return real
    if rel.split(os.sep)[0] == os.pardir:
        return real
    return rel.replace(os.sep, "/")


# The `end` exits of a pytest session that ran to its end (#849 round 1). A
# stop is read off the `end` line's `stopped` first (#852): what pytest
# handed `pytest_keyboard_interrupt` and the session's `shouldfail` and
# `shouldstop`, which the recorder writes. The exit is the net for a stop no
# hook shows. pytest defines six, and its `wrap_session` gives each one this
# way:
#
#   0 OK, 1 TESTS_FAILED, 5 NO_TESTS_COLLECTED -- the run loop ran every test
#     it collected, or there were none. Held here. A stopped session gives
#     them too, and `stopped` is what tells it apart: `pytest.exit` with a
#     `returncode` of 0, 1 or 5 chooses one (an `exit` entry), and a run
#     without xdist that `-x` or `--maxfail` stops exits 1 (a `failures`
#     entry). A failed collection under `-x` exits 1 where another collector
#     starts after it, and 2 where it was the last one collected.
#   2 INTERRUPTED -- a `KeyboardInterrupt`, `pytest.exit()` with no code, the
#     run loop's `Interrupted`: a failed collection without `-x` or
#     `--continue-on-collection-errors` (no test runs), xdist under `-x` or
#     `--maxfail`, and `--stepwise` or another plugin that sets `shouldstop`.
#     Each also puts an entry in `stopped`.
#   3 INTERNAL_ERROR -- the run loop raised, a hook among the causes; and a
#     `pytest.exit()` in an xdist worker, which reaches the controller as an
#     internal error with no hook called.
#   4 USAGE_ERROR -- pytest refused an argument after the session started,
#     a `-k` expression it cannot parse among them; no test runs.
#
# Any other value is a return code `pytest.exit` or a plugin chose, and is no
# exit of a session that ran to its end. Every exit above was measured with
# the recorder loaded on pytest 6.1, 7.0 and 9.1 (#849 round 2), and again
# with every stop `stopped` carries on the same three builds and on 9.1 with
# pytest-xdist 3.8 under `-n 2` (`phases/phase-1.md` of 1791384158). One stop
# shows in neither: a `pytest.exit()` raised by a `pytest_sessionfinish`
# hook that runs after the recorder's is raised after the `end` line was
# written, and that session reads as one that ran to its end. One
# over-strictness is named rather than closed: pytest sets `shouldfail` after
# the test that reaches `-x` or `--maxfail`, last test or not, so a session
# whose limit fell on its last test ran every test and still reads unended
# (#869 round 1's ⬜ 4).
RAN_TO_ITS_END = (0, 1, 5)

# The category pytest's terminal reporter counts a collect report under
# (`TerminalReporter.pytest_collectreport`): a failed collection is an
# `error` on its summary line and a skipped one a `skipped` (#869).
COLLECT_CATEGORY = {"failed": "error", "skipped": "skipped"}


def read_record(directory, key, worktree):
    """The `RunRecord` of every `*.jsonl` under `directory` whose first line
    — the recorder's `session` line — carries `key`, with paths named against
    `worktree`.

    Pure, apart from reading the files. A file whose first line does not
    carry this key is another run's and is passed over whole, whatever its
    name says, and none of its lines is counted; a line of a keyed file that
    does not parse as an object is counted in `unread` and passed over, and
    a blank line is passed over uncounted. Every line naming a path is a
    test or a failed or skipped collection, and its `outcome` says whether
    it failed. A file's lines are read as a set for the lists — xdist's
    controller is handed one failed collection once per worker
    (`phases/phase-1.md` of 1791270161) — so a collection is counted once
    per session however often its line was written, and a `test` line once
    per line, as pytest counts each report. A `test` line whose `category`
    is not a word, or is `""`, counts under none. Files are
    read in the order they were last written, so where a row runs pytest
    twice the first runner's files come first. A directory that cannot be
    listed, or a file that cannot be read, holds no record. An `end` line's
    `unplaced`, where it is an integer, is added to the record's, and to its
    `unplaced_red` too where that line's `exitstatus` is not 0. A keyed file
    with no `end` line, with an `end` line whose `stopped` is not an empty
    list — a stop pytest showed, or a value the recorder never writes — or
    with an `end` line whose `exitstatus` is not in `RAN_TO_ITS_END`, adds
    one to `unended`."""
    record = RunRecord()
    try:
        names = os.listdir(directory)
    except OSError:
        return record
    found = []
    for name in names:
        if not name.endswith(".jsonl"):
            continue
        path = os.path.join(directory, name)
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                found.append((os.stat(path).st_mtime_ns, name, handle.read()))
        except OSError:
            continue
    for _, _, text in sorted(found):
        parsed, unread = [], 0
        for line in text.splitlines():
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except ValueError:
                unread += 1
                continue
            if isinstance(value, dict):
                parsed.append(value)
            else:
                unread += 1
        if not parsed or parsed[0].get("key") != key:
            continue
        record.sessions += 1
        record.unread += unread
        # A session stopped part-way where it wrote no `end` line -- its
        # process died, or its recorder stopped writing (#849, #825 round 6)
        # -- where its `end` line says pytest stopped it (#852), or where
        # that line shows an exit no session that ran to its end gives (#849
        # round 1).
        ends = [value for value in parsed[1:] if value.get("kind") == "end"]
        if not ends or any(
            end.get("stopped") != [] or end.get("exitstatus") not in RAN_TO_ITS_END
            for end in ends
        ):
            record.unended += 1
        collections = set()
        for value in parsed[1:]:
            unplaced = value.get("unplaced")
            if value.get("kind") == "end" and type(unplaced) is int:
                record.unplaced += unplaced
                # A session that exited 0 failed nothing, counted or not.
                if value.get("exitstatus") != 0:
                    record.unplaced_red += unplaced
            path_of = value.get("path")
            if not isinstance(path_of, str):
                continue
            named = record_path(path_of, worktree)
            record.collected.add(named)
            if value.get("outcome") == "failed":
                record.failing.setdefault(named, None)
            category = None
            if value.get("kind") == "test":
                category = value.get("category")
            elif value.get("kind") == "collect":
                seen = (value.get("nodeid"), value.get("outcome"))
                if seen not in collections:
                    collections.add(seen)
                    category = COLLECT_CATEGORY.get(value.get("outcome"))
            if isinstance(category, str) and category:
                record.counts[category] = record.counts.get(category, 0) + 1
    return record


def failing_files(text):
    """The test files pytest's `FAILED` lines name, in first-seen order —
    read only where the row's run at `HEAD` left no record carrying its key,
    and each of them then reads `NO_RECORD_AT_HEAD`."""
    return list(dict.fromkeys(FAILED_RE.findall(text)))


def quote(path, windows=None):
    """One path, quoted for the shell `run(..., shell=True)` hands it to.

    `windows` is the platform, defaulting to this one, so BOTH branches can
    be driven from a case on either machine. Reading `os.name` inside the
    body left the branch that exists for Windows undrivable from the machine
    this was written on, and the whole unit could be replaced by `return
    path` with every case still green -- #103's class, made out of the fix
    for it. The platform is not what was missing; CI runs
    `windows-latest` on every push. An assertion was.

    On Windows `run(..., shell=True)` goes through `cmd.exe`, and
    `subprocess.list2cmdline` builds the argv quoting `CreateProcess` reads,
    which Python's own documentation says is NOT `cmd.exe` quoting: it wraps
    a path holding a space and leaves `& | ^ < > ( )` for the shell to act
    on. Double quotes carry both -- inside them `cmd.exe` treats none of
    those as syntax -- and a `"` cannot appear in a Windows path at all.

    What double quotes do NOT stop is `%VAR%` expansion, which `cmd.exe`
    performs inside them. A test path holding percent signs would still be
    mangled; it is named here rather than claimed closed, because the fix for
    it is not quoting and this unit should not pretend otherwise.
    """
    if windows is None:
        windows = os.name == "nt"
    return f'"{path}"' if windows else shlex.quote(path)


# What a file reads where no run measured it (#747). Each starts `new?`, so it
# is never read as `new`, and says the comparison was not measured.
NOT_MEASURED = f"{NEW}? not measured"
# How a row earns the measured word, said by both reasons that are about a
# row whose pytest did not load the recorder.
EARNS_THE_WORD = (
    "A row earns the measured word by letting every pytest it runs load the "
    "gate's recorder: it adds to the PYTHONPATH and PYTEST_ADDOPTS the gate "
    "hands it rather than replacing them, and runs pytest in that "
    "environment rather than one it builds, through any wrapper"
)
# What a missing record means, said by both reasons: every cause, never one
# of them as the only one (#825 round 3's 🟡 3 and round 4's 🟡 3). The
# records alone cannot tell the three apart, so the sentence names each and
# where it shows: a row that started no pytest -- a part before its runner
# failed, the module's case A5, or a row with no runner at all -- prints no
# pytest output; a pytest that loaded no recorder prints its own; and the
# recorder's warning is `specseal_pytest_record: no record written: <error>`.
NO_RECORD_CAUSES = (
    "the row started no pytest, because a part before its runner failed or "
    "it has none; none it started loaded the recorder; or the one that did "
    "could not write its record and warned 'specseal_pytest_record: no record "
    "written' in {kept}"
)
# Where the row's run at `HEAD` left no record carrying its key: the files
# come from the `FAILED` lines of `suite.txt`, and the base is not run.
NO_RECORD_AT_HEAD = (
    f"{NOT_MEASURED}: no pytest the row ran here left a record of the gate's "
    f"recorder ({NO_RECORD_CAUSES.format(kept='suite.txt')}), so this file is "
    "named only by a FAILED line of suite.txt and the base was not run. "
    f"{EARNS_THE_WORD}"
)
# Where the row's run at the base left no record carrying the base's key.
NO_RECORD = (
    f"{NOT_MEASURED}: the row ran once at the base, and no pytest it ran there "
    "left a record of the gate's recorder "
    f"({NO_RECORD_CAUSES.format(kept='suite-at-base.txt')}; records/ is beside "
    f"it). {EARNS_THE_WORD}"
)
# Formatted with the exit of the row's run at the base, where no session of
# that run collected the file and the run did not exit 0 (`questions.md` Q1
# of 1791270161 holds the trade).
NOT_REACHED = (
    f"{NOT_MEASURED}: the row ran once at the base and exited {{code}}, and no "
    "pytest it ran there collected this file, so the run may have ended before "
    "reaching it and whether the base fails it was not measured (kept as "
    "suite-at-base.txt, with records/ beside it). A file the branch added "
    "reads this way wherever the base's own row already fails"
)


# Formatted with the base record's `unplaced_red` count, where a file would
# read `new` from a base record one of whose sessions ended non-zero and left
# tests or collections out of every list: one of them may be this file's
# failure, so `new` is not measured (#825 round 4's 🟡 2, the worker that
# dies in a test's setup before any report of it reaches the xdist
# controller). A session that exited 0 failed nothing, so what it left out
# cannot be (#825 round 5). A red session whose left-out reports all passed
# still turns `new` into this: the limit rule 3 names.
UNPLACED_AT_BASE = (
    f"{NOT_MEASURED}: the row ran once at the base, and its sessions that "
    "ended non-zero left {count} of the tests and collections their pytest "
    "reported in no list, "
    "such as a test whose xdist worker died before any report of it arrived, "
    "so one of them may be this file's failure and whether the base fails it "
    "was not measured (kept as suite-at-base.txt, with records/ beside it)"
)


# Formatted with how many of the base's sessions stopped part-way, where a
# file would read `new`, so what such a session held passing may not have
# finished. It wrote no `end` line: its process died, as plain pytest does on
# a test that calls `os._exit` or segfaults, or its recorder stopped writing
# (#849, #825 round 6's 🟡 1: round 4's 🟡 2 without xdist). Or its `end` line
# says pytest stopped the session (#852), or shows an exit `RAN_TO_ITS_END`
# does not hold: pytest ended the session itself (#849 round 1). Checked
# after `UNPLACED_AT_BASE`, whose count is the one a red session can give.
UNENDED_AT_BASE = (
    f"{NOT_MEASURED}: the row ran once at the base, and {{count}} of its pytest "
    "sessions stopped part-way, because the process died or the recorder "
    "stopped writing before the session's end line, or pytest stopped the "
    "session (an interrupt, pytest.exit(), -x or --maxfail, a plugin's stop) "
    "or ended it on an error of its own, so this file's tests there may not "
    "have finished and whether the base fails it was not measured (kept as "
    "suite-at-base.txt, with records/ beside it)"
)


# Formatted with how many lines of the base's keyed records did not parse as
# the recorder's, where a file would read `new` (#869). The recorder writes
# one JSON object per line, so such a line was written by something else or
# cut short, and it may have held this file's failing test. Checked after
# `UNENDED_AT_BASE`: a session that died part-way can leave a cut last line,
# and its reason is the one that names the cause. A file the record holds
# failing still reads `failing on base too`: what the record does hold is
# kept.
UNREAD_AT_BASE = (
    f"{NOT_MEASURED}: the row ran once at the base, and {{count}} of the lines "
    "in the records its pytest wrote there did not parse as the recorder's and "
    "each was passed over, so one may have held this file's failure and "
    "whether the base fails it was not measured (kept as suite-at-base.txt, "
    "with records/ beside it)"
)


# Where the scratch worktree at the base could not be added.
NOT_CHECKED_OUT = f"{NEW}? the base could not be checked out for comparison"


def base_word(record, code, path):
    """The word `path` reads from the base's `RunRecord` and the exit of the
    run that wrote it — the five rows of `compare_at_base`'s table, and
    `new` given only where the record left nothing out."""
    if not record.sessions:
        return NO_RECORD
    if path in record.failing:
        return ON_BASE
    if path in record.collected or code == 0:
        if record.unplaced_red:
            return UNPLACED_AT_BASE.format(count=record.unplaced_red)
        if record.unended:
            return UNENDED_AT_BASE.format(count=record.unended)
        if record.unread:
            return UNREAD_AT_BASE.format(count=record.unread)
        return NEW
    return NOT_REACHED.format(code=code)


def compare_at_base(root, base, command, files, keep):
    """{file: `new` | `failing on base too` | `new? …`}, read off a record
    the base's own pytest wrote — never inferred.

    `files` are the failing files of the row's run at `HEAD`, as
    `read_record` names them against `root`. A scratch worktree is added at
    `base`, the row runs there **once, unchanged** — nothing appended, no
    prefix cut — handed `recording_env` with a key of its own, its output
    kept as `suite-at-base.txt` and its record under `records/`, and the
    worktree is removed whatever happened. Each file is named against the
    scratch worktree the way it was named against `root`, and reads one row
    of this table (#825):

      - no session carries the base's key: `NO_RECORD`;
      - a failing test or a failed collection of the file: `failing on base
        too`;
      - the file collected, and nothing of it failed: `new`;
      - the file in no session, and the row exited 0: `new` — the row ran to
        its end at the base and never collected the file, so the base cannot
        fail a test it did not run;
      - the file in no session, and the row exited non-zero: `NOT_REACHED`
        with the exit — a part that failed before a later runner, `-x`, an
        interrupt, a crash, or simply a file the branch added on a base whose
        row is already red.

    Either `new` reads `UNPLACED_AT_BASE` with the count instead where a
    session of the base that ended non-zero left any test or collection out
    of every list: one of them may be the file's failure — an xdist worker
    that died in a test's setup, before any report of it reached the
    controller, is one — so the record cannot say the file passed. A session
    that exited 0 failed nothing, so what it left out cannot be. Where no
    such count is given, either `new` reads `UNENDED_AT_BASE` instead where a
    session of the base stopped part-way: it wrote no `end` line, as plain
    pytest a test kills with `os._exit` writes none (#849), or its `end`
    line shows an exit `RAN_TO_ITS_END` does not hold, as a
    `KeyboardInterrupt` in a test and xdist under `-x` give (#849 round 1).
    `failing on base too` is not affected.

    The process that collected a test is the process that wrote its line,
    so there is no `whose` to decide: a test that runs pytest itself starts
    a pytest with no key, which records nothing, and a second runner in the
    row writes its own session with its own paths. Each line names its file
    by the path pytest holds for the test or the collector, carried on the
    report from the process that held it, and never by a name pytest made
    from that path, so no rootdir and no argument enters it (#825's reframe
    after round 3). What `templates/config.md` rule 3 names as left open is
    a test written against this gate's key or its file.

    The `run` call stays in this function's own body, one call for the one
    run: the shell sites are `gate` and this function, and a case holds
    that.
    """
    scratch = tempfile.mkdtemp(prefix="broad-gate-base-")
    added = git(root, "worktree", "add", "--detach", scratch, base)
    if added is None:
        # The worktree that was not added still leaves the directory
        # `mkdtemp` made, and nothing below runs to remove it.
        shutil.rmtree(scratch, ignore_errors=True)
        return {f: NOT_CHECKED_OUT for f in files}
    try:
        key = record_key("base")
        ran = run(
            BASE_RUN,
            command,
            scratch,
            keep,
            shell=True,
            env=recording_env(keep, key),
        )
        record = read_record(records_dir(keep), key, scratch)
        return {f: base_word(record, ran.code, f) for f in files}
    finally:
        subprocess.run(
            ["git", "-C", root, "worktree", "remove", "--force", scratch],
            capture_output=True,
        )


# --- the workflow this gate is a local reading of ---------------------------
#
# The gate exists so the sealer's one run says what CI will say. It said a
# SHORTER list than CI for one release: `.github/workflows/hygiene.yml`'s
# `release` job gained a step in #424, nobody extended the gate, and no case
# in the suite went red for it — a coverage probe over the eight structural
# modules that read those files reported 243 passed and 8 skipped with the arm
# absent (#468).
#
# So the list is declared here rather than remembered. **Every step of that
# job is mirrored by a named arm or excluded with a reason a person wrote**,
# there is no third state, and
# `tests/test_the_gate_names_every_step_ci_runs.py` holds the partition
# against the workflow from both sides: a step added to the workflow and left
# unclassified goes red there, and so does a row naming a step that was
# renamed away.
#
# **A reason is prose, never a category.** `EXCLUDED` tells the next reader
# nothing, and the reason is the whole value of the row — it is what a person
# checks when they wonder whether this gate's seal covers them.
#
# What this does NOT close, stated rather than left to be found: an exclusion
# can be written to make the case green rather than to state a truth, and the
# partition would then be total and this gate's stamp still short of what the
# merge is judged by. That hole is real and open; what the declaration buys is
# that the omission is now a sentence somebody wrote and signed rather than a
# silence.

WORKFLOW = os.path.join(".github", "workflows", "hygiene.yml")
RELEASE_JOB = "release"

# A job's key under `jobs:`, at two spaces. Anything deeper is inside a job.
JOB_RE = re.compile(r"^  ([A-Za-z0-9_-]+):\s*$")
# A step's name. Any indentation: the dash is what makes it a step of the
# list, where a `name:` with no dash is a key inside one (`with:`, `env:`).
STEP_RE = re.compile(r"^\s*-\s+name:\s*(\S.*?)\s*$")


def unquote(value):
    """A YAML scalar with its matching quotes off, if it wore any."""
    for mark in ('"', "'"):
        if len(value) >= 2 and value.startswith(mark) and value.endswith(mark):
            return value[1:-1]
    return value


def job_steps(text, job):
    """Every named step of one job of a workflow, in file order.

    **Text in, list out.** The reader is driven over shapes this repository's
    workflow does not happen to have, because a reader nothing drives is a
    reader nobody can tell is partial — #424's finding 4, whose repair was the
    same move.

    **No YAML parser.** This script runs with no third-party dependency, and
    CI installs a test runner and nothing else. A step name is a `- name:`
    line, read as text, the way
    `tests/test_ci_gives_the_checks_what_they_need.py#jobs` already reads the
    same file. A step that exists only in a comment is not a step, and that
    falls out of both patterns rather than out of a line dropping comments:
    each requires the first non-blank character to be the list's dash or the
    job key's own letter. The line that dropped them was written, mutated,
    and found to change nothing — dead code that looks like a defence is
    worse than none.

    **Known gap: a TRAILING comment joins the step name.** YAML ends an
    unquoted scalar at ` #`, and this reader does not, so
    `- name: a step  # why` reads as `a step  # why`. Not live — no `- name:`
    line in `hygiene.yml` carries one — and it fails LOUDLY if one ever does,
    because A1 goes red with the comment visible in the name it could not
    classify. `strip_comments` in
    `tests/test_ci_gives_the_checks_what_they_need.py`, the reader this one
    follows, has the same gap, so it is a class rather than something this
    reader opened (round 1, recorded as a correction rather than fixed).

    A file this cannot read as a workflow comes back empty rather than
    raising. The gate calls it on whatever sits at that path in the repository
    it was pointed at, and the plugin ships to repositories that have no such
    workflow at all — for them nothing about the run may change. What keeps an
    empty answer from reading as a pass is the caller: the case that grades
    this repository refuses an empty list rather than counting zero
    unclassified steps.
    """
    lines = text.splitlines()
    try:
        # Found by walking rather than by splitting on `"\njobs:\n"`: that
        # spelling cannot see a `jobs:` on the FIRST line of the file, and
        # driving this reader over a fragment that had one is what said so.
        start = lines.index("jobs:") + 1
    except ValueError:
        return []
    steps, current = [], None
    for line in lines[start:]:
        job_line = JOB_RE.match(line)
        if job_line:
            current = job_line.group(1)
            continue
        if current != job:
            continue
        step = STEP_RE.match(line)
        if step:
            steps.append(unquote(step.group(1)))
    return steps


# Each row is a step of the `release` job, spelled as `hygiene.yml` spells it,
# and then either the arm that mirrors it or the reason none does.
#
# **Four of the eight exclusions could not run here at all; four could.** The
# measurement `questions.md` M1 asked for, taken by construction over all
# thirteen: three steps have no local answer (the pull request's body, the
# remote's pull-request namespace, the tracker), one raises a warning and can
# refuse nothing, one is shell written inline in the workflow with no script
# to share, and three run a script that belongs to this repository rather
# than to the plugin. The last four are the ones with a local answer, and
# `seal/config.md`'s `Broad gate` row is where a repository names checks of
# its own — not the arm list of a script that ships to every repository that
# installs the plugin.
#
# **Which of the thirteen CI runs depends on the base** (#666). Four run only
# on a pull request into `main` (`ONLY_AT_MAIN`) and two are skipped there
# (`SKIPPED_AT_MAIN`'s arms), so the `workflow` count is taken over
# `steps_for(workflow, base)` rather than over this table: a step CI does not
# ask of a pull request is neither answered nor unanswered by the sealer's run.
PARTITION = (
    (
        "every issue this pull request claims, and every one it only names",
        None,
        "reads the body of the pull request, and a gate run on a branch has "
        "no pull request to read. The step never fails either — it reports a "
        "split and exits 0 — so there is no verdict for an arm to carry",
    ),
    (
        "a change to what ships must move the version",
        None,
        "the check is shell written inline in the workflow, with no script "
        "both sides can run. An arm would be a second reading of one "
        "question, which is the drift this partition exists to stop",
    ),
    (
        "every changelog fragment reached the released file",
        None,
        "runs `.github/scripts/gather_changelog.py`, which belongs to this "
        "repository and not to the plugin this gate ships in. A repository's "
        "own checks belong in the `Broad gate` row of `seal/config.md`",
    ),
    (
        "every ledger fragment folded into the gathered ledger",
        None,
        "runs `.github/scripts/fold_ledger.py`, this repository's own script "
        "rather than one the plugin ships, and the `Broad gate` row is where "
        "a repository names a check of its own",
    ),
    (
        "the unverified record is readable, and rows leave it closed",
        UNVERIFIED_NAME,
        None,
    ),
    (
        "the pull request heads a round record may name",
        None,
        "fetches the remote's pull-request namespace. The gate seals the tree "
        "that is already here and fetches nothing, so a ref only a fetch "
        "would bring is a ref it cannot reach",
    ),
    (
        "a declared review chain has the round record it claimed",
        CHAIN_NAME,
        None,
    ),
    (
        "wording this branch removed is not still standing elsewhere",
        SURVIVORS_NAME,
        None,
    ),
    (
        "no merge on this branch dropped a correction the ledger had made",
        CORRECTIONS_NAME,
        None,
    ),
    (
        "the milestone this release claims is the work it carries",
        None,
        "asks the tracker through `gh` which issues the milestone holds. The "
        "gate reads no network and carries no token",
    ),
    (
        "the mode the row declares is the mode the folder is in",
        MODE_NAME,
        None,
    ),
    (
        "the CLAUDE.md block is the template's, line for line",
        None,
        "runs `.github/scripts/claude_block.py` over this repository's own "
        "CLAUDE.md. The plugin does not ship that script, and a repository "
        "that wants it sealed names it in the `Broad gate` row",
    ),
    (
        "both READMEs move together",
        None,
        "raises a warning and never fails, so there is nothing for an arm to "
        "refuse. Every arm here is an exit code",
    ),
)


# The branch a pull request into which is a release, spelled once.
MAIN = "main"

# The mirrored arms whose steps skip a pull request into `main`. In
# `hygiene.yml` each of the two steps opens its `run:` with `if [ "${{
# github.base_ref }}" = "main" ]; then … exit 0`, because a release branch
# carries squashed commits and every work item was already read at its own
# pull request. An arm that asks where its step does not ask is a second
# reading of one question, which is what `PARTITION` exists to stop (#473).
#
# Held against the workflow by
# `tests/test_the_gate_names_every_step_ci_runs.py`: for each mirrored arm,
# its step skips at `main` exactly where this names it, so a guard added to a
# third step, or dropped from one of these, fails the suite.
SKIPPED_AT_MAIN = (SURVIVORS_NAME, CORRECTIONS_NAME)

# The steps that run ONLY on a pull request into `main`, by step name (#666).
# In `hygiene.yml` each of the four opens its `run:` with `if [ "${{
# github.base_ref }}" != "main" ]; then … exit 0`: a release pull request is
# where the version moves, the fragments are gathered and folded, and the
# milestone is judged. On any other base CI never asks them, so a seal that
# counted them as *not answered* counted questions nobody asks — the owner
# read `8 of 13 not answered` on a feature seal whose honest count was `4 of
# 9`. None of the four is mirrored, so no arm changes; what changes is the
# denominator of the `workflow` count and the names beside it.
#
# Held against the workflow by `tests/test_the_gate_names_every_step_ci_runs.py`
# from both sides, the way `SKIPPED_AT_MAIN` is: a `!= "main"` guard added to
# a fifth step, or dropped from one of these, fails the suite.
ONLY_AT_MAIN = (
    "a change to what ships must move the version",
    "every changelog fragment reached the released file",
    "every ledger fragment folded into the gathered ledger",
    "the milestone this release claims is the work it carries",
)


def mirrored():
    """The arm each classified step is mirrored by, by step name."""
    return {name: arm for name, arm, _ in PARTITION if arm}


def base_is_main(given):
    """Whether the base the caller gave is `main`: `given`, with one leading
    `origin/` removed. This gate's one reading of the workflow's
    `github.base_ref == "main"`, asked by `skipped_at_main` for the arms and
    by `steps_for` for the count, so the two cannot disagree about which
    pull request is a release (#666). None — no base known — is not `main`.

    **The bound, named rather than claimed:** it is keyed on the spelling,
    so `refs/heads/main` or `upstream/main` reads as not-`main`. For the arms
    that runs both, and for the count it counts the four only-at-`main`
    steps as running; both are the direction that over-asks."""
    if given is None:
        return False
    if given.startswith("origin/"):
        given = given[len("origin/") :]
    return given == MAIN


def steps_for(workflow, given):
    """The `release` job's steps CI runs for a pull request into `given`, in
    file order (#666).

    Every step of the job, less `ONLY_AT_MAIN` where the base is not `main`,
    and less the steps `SKIPPED_AT_MAIN`'s arms mirror where it is. A step
    left out here is neither answered nor unanswered: CI does not ask it of
    this pull request, so the sealer's run neither covers it nor misses it. `given`
    None — no base known — leaves out what a base that is not `main` would,
    which is what every caller that knows no base has been asked about."""
    steps = job_steps(workflow, RELEASE_JOB) if workflow else []
    if base_is_main(given):
        skipped = {name for name, arm, _ in PARTITION if arm in SKIPPED_AT_MAIN}
        return [step for step in steps if step not in skipped]
    return [step for step in steps if step not in ONLY_AT_MAIN]


def left_out_clause(workflow, given):
    """The clause the coverage line adds for the steps `steps_for` left out,
    or "" where it left none: how many, and why (#666)."""
    every = job_steps(workflow, RELEASE_JOB) if workflow else []
    left = len(every) - len(steps_for(workflow, given))
    if not left:
        return ""
    why = (
        f"{'are steps' if left > 1 else 'is a step'} CI skips on a pull request "
        f"into `{MAIN}`"
        if base_is_main(given)
        else f"{'run' if left > 1 else 'runs'} only on a pull request into `{MAIN}`"
    )
    return (
        f" {left} more {why}, so this count leaves {'them' if left > 1 else 'it'} out."
    )


def skipped_at_main(given, workflow):
    """The arms this run leaves out because CI skips their steps, in
    `PARTITION` order. Empty unless BOTH hold:

      - the base the caller gave names `main`: `given`, with one leading
        `origin/` removed, is `main`. That is this gate's reading of the
        workflow's `github.base_ref == "main"`, keyed on what the caller
        said the pull request merges into, as `agents/sealer.md` tells the
        sealer to pass it; and
      - the gated repository's workflow carries that arm's step in its
        `release` job.

    The second half is what keeps a repository with no such workflow exactly
    as it was (`workflow_text`'s docstring): many of them merge feature
    branches straight into `main`, and skipping there would drop two arms
    from every run, which is the unsafe direction.

    **The bound, named rather than claimed:** the skip is keyed on the
    spelling `main` or `origin/main` and on the step being present in the
    workflow, not on the guard the step carries, so `refs/heads/main` or
    `upstream/main` runs both arms, the direction that over-asks. The
    spelling is read by `base_is_main`, which the `workflow` count asks too.
    """
    if not workflow or not base_is_main(given):
        return []
    steps = set(job_steps(workflow, RELEASE_JOB))
    return [
        arm for name, arm, _ in PARTITION if arm in SKIPPED_AT_MAIN and name in steps
    ]


def skipped_line(arms):
    """The one stderr line a run that leaves arms out prints before the
    checks run."""
    named = " and ".join(f"`{arm}`" for arm in arms)
    return (
        f"broad-gate: the base is `{MAIN}`, and {WORKFLOW} skips the steps the "
        f"{named} {'arms mirror' if len(arms) > 1 else 'arm mirrors'} on a pull "
        f"request into `{MAIN}`, so this run does not run "
        f"{'them' if len(arms) > 1 else 'it'} either"
    )


def workflow_text(root):
    """The hygiene workflow of the repository being gated, or None.

    None is the ordinary case away from this repository: the plugin ships to
    repositories that have no such workflow, and for them nothing about the
    run changes (`spec.md` A7). **A file that is there and is not UTF-8 is the
    same case**, and it has to be: `UnicodeDecodeError` is a `ValueError`
    rather than an `OSError`, and `main` catches only `Refused`, so a decode
    error raised here ended the whole run on a traceback instead of a verdict
    — the largest possible change to the run of a repository this partition
    is not about (round 1, finding 5).
    """
    try:
        with open(os.path.join(root, WORKFLOW), encoding="utf-8") as handle:
            return handle.read()
    except (OSError, ValueError):
        return None


def unanswered(text, given):
    """The steps CI runs for this base (`steps_for`) that this run answers
    nothing for, in file order. `given` is required, here and in
    `coverage_line` (round 1's 🟡 3 of #666): a default answered every caller
    that dropped it with the feature-base count, in silence.

    A step no row classifies counts here too, and that is the honest answer
    rather than an oversight: in another repository whose workflow happens to
    carry this name, every step is one this gate runs nothing for.
    """
    arms = mirrored()
    return [step for step in steps_for(text, given) if step not in arms]


def coverage_line(text, given):
    """One line naming the steps this seal did not answer, or None.

    **Over the steps CI runs for this base** (#666, `steps_for`), and one
    clause saying how many it left out and why (`left_out_clause`): a step CI
    does not ask of this pull request is not a step the sealer's run failed
    to answer, and naming it among the unanswered sent a reader to four steps
    no run of this pull request would ever ask.

    **Names here, a count on the panel** (`questions.md` W1).
    The panel gives a value `PANEL_VALUE_WIDTH` columns (23 when this was
    written, 41 since #832), which thirteen step
    names do not fit and a count does — and a reader who is told only a number
    has to reconstruct WHICH from two files, which is the reconstruction this
    work item exists to remove. So the panel carries the number and this
    carries the names, on the stream the gate already uses to say which
    command the row asked for.

    **A step no row classifies is named apart from one a row excludes.**
    `PARTITION` describes SpecSeal's own `release` job; in another repository
    whose workflow happens to carry that job name, every step is unclassified
    and none of them has a reason written anywhere. Pointing that reader at
    `PARTITION` sends them to thirteen rows about a workflow they do not run,
    which is the reconstruction from two files this work item exists to
    remove, arriving one level further out (round 1, finding 3).
    """
    if not job_steps(text, RELEASE_JOB):
        return None
    steps = steps_for(text, given)
    short = unanswered(text, given)
    left = left_out_clause(text, given)
    if not short:
        return (
            f"broad-gate: this seal answers every one of the {len(steps)} "
            f"`{RELEASE_JOB}` steps {WORKFLOW} runs for this base." + left
        )
    classified = {name for name, _, _ in PARTITION}
    excluded = [step for step in short if step in classified]
    unknown = [step for step in short if step not in classified]
    said = (
        f"broad-gate: {WORKFLOW}'s `{RELEASE_JOB}` job runs {len(steps)} "
        f"steps for this base and this seal answers {len(steps) - len(short)}." + left
    )
    if excluded:
        said += (
            " Not answered, each with the reason no arm mirrors it in "
            "`broad_gate.py#PARTITION`: " + "; ".join(excluded) + "."
        )
    if unknown:
        said += (
            " In no row of `broad_gate.py#PARTITION` at all, so this gate has "
            "no reading of them and answers nothing for them: "
            + "; ".join(unknown)
            + "."
        )
    return said


# --- what the panel reads --------------------------------------------------


# The order pytest's summary line prints the categories in, from its
# `KNOWN_TYPES` with the two no report carries left out (`deselected`,
# `warnings`); a category outside it follows, in the order it was first
# written, as pytest prints one (#869).
SUMMARY_ORDER = ("failed", "passed", "skipped", "xfailed", "xpassed", "error")
# The one category pytest's line pluralises among those a report carries.
PLURALS = {"error": "errors"}


def suite_counts(record):
    """The suite's counts as pytest's summary line prints them, without its
    clock — `1 failed, 767 passed, 1 error` — read off the `RunRecord` of
    the row's run, or None.

    Every number is a count of lines the row's own pytest wrote, under the
    category pytest's own line counts each report under (`read_record`), so
    nothing the row PRINTS can reach it (#869). None where no session
    carries the key, where a keyed file holds a line that did not parse —
    a count that passed a line over is not one anybody can vouch for —
    where a report was counted under no category because it had no file of
    its own (`unplaced`, which pytest's own line counted; #869 round 1's
    🟡 2), or where no report was counted at all."""
    if not record.sessions or record.unread or record.unplaced or not record.counts:
        return None
    known = [name for name in SUMMARY_ORDER if name in record.counts]
    other = [name for name in record.counts if name not in SUMMARY_ORDER]
    said = []
    for name in known + other:
        count = record.counts[name]
        word = PLURALS.get(name, name) if count != 1 else name
        said.append(f"{count} {word}")
    return ", ".join(said)


def ledger_counts(text):
    """`(ok, drifted, broken)` off `evidence-check`'s `total:` line, or None.

    On a drawn panel `drifted` and `broken` are both 0 by construction: the
    gate passes `--strict`, which exits 2 on either. #666 carried them on the
    row beneath `ok` because the owner asked for it; #717's owner took that
    row off, and #832's owner put the three back on the one `ledger` row
    (`spec.md` decision 6 of work item 1791270164), so `panel` prints all
    three. The count that varies is where it varies, at the end of the
    failure form's `ledger` entry (`failure_lines`)."""
    m = LEDGER_RE.search(text)
    return m.groups() if m else None


def ledger_total(text):
    """`evidence-check`'s own `total:` line, or None where its output has
    none. The failure form quotes a check's FIRST lines and this line is its
    LAST, so a refused ledger used to be reported without its counts."""
    for line in reversed(text.splitlines()):
        if line.startswith("total:"):
            return line.rstrip()
    return None


def round_count(item):
    try:
        names = os.listdir(os.path.join(item, "rounds"))
    except OSError:
        return 0
    return sum(1 for n in names if ROUND_RE.match(n))


class Record:
    """The record a recorded seal just wrote its cell into, as the plugin's
    own readers read it (#666).

    `path` is the home `round_record.seal_home` picks — the last round record,
    or `broad-gate.md` for a work item that ran no rounds — and `rows` its
    `| field | value |` rows, None where the home is not a round record or
    cannot be read. `chain` and `reader` are the modules that read it, kept so
    a later question of the same record asks the same reader.

    **No second reader of a round record.** `chain_check.py` owns the record's
    vocabulary and `round_record.py` owns which file the cell lands in, and a
    reader written here would be a third answer to both, which is the split
    `hooks/config.py`'s loading comment above refuses."""

    __slots__ = ("chain", "lines", "path", "reader", "rows")

    def __init__(self, path, rows=None, lines=None, chain=None, reader=None):
        self.path, self.rows, self.lines = path, rows, lines
        self.chain, self.reader = chain, reader


def sealed_record(item, root):
    """The `Record` the cell went into, or None where nothing can say.

    Under a preflight, the record the cell WOULD go into: the preflight asks
    it to name the record `seal --check` read, and only after that exited 0.

    Asked only after `seal` exited 0, so the files it reads were just read by
    the same scripts in a subprocess. Every failure is None and never a
    refusal: what this feeds is a label and a line, and a run that sealed
    does not stop on a label."""
    # `SystemExit` too: `round_record.py`'s own `load` raises it for a sibling
    # it cannot find, which is how it ends its own run, and must not end this
    # one.
    try:
        generator = load(RECORD, "specseal_round_record_for_broad_gate")
        reader, routing, _root, item, rounds = generator.where(
            argparse.Namespace(item=item, root=root)
        )
        n, path = generator.seal_home(routing, item, rounds)
    except (Exception, SystemExit):  # a label never stops a sealed run
        return None
    if n is None:
        return Record(path, chain=generator.chain, reader=reader)
    try:
        with open(path, encoding="utf-8") as handle:
            lines = reader.readable(handle.read())
        rows = generator.chain.table_rows(reader, lines)
    except (Exception, SystemExit):
        return Record(path, chain=generator.chain, reader=reader)
    return Record(path, rows, lines, generator.chain, reader)


def rounds_rows(item, record):
    """The `rounds` row and, where it has one, the row beneath it (#666).

    `<R>` is the count of round records, as before. ` · capped` is appended
    where the last record's `Needs a fix` says the run reopened as
    `chain_check.says_reopened` reads it (#866): `seal` has already refused
    an unchecked `Pass`, so that is a record whose every finding closed while
    the reviewer's own answer still says the round needed a fix — the shape
    `skills/verify/SKILL.md` §*The broad gate* defines a run that ended at
    the cap by. The panel is that cell's third reader and has no reading of
    its own: a cell `says_reopened` answers None for — `yes` alone, a word
    outside the vocabulary, an empty cell — is a record that cannot answer,
    and prints `<R>` alone like the shapes below. The row beneath counts the verdict rows
    `chain_check.verdict_of` calls `deferred` or `deferred (no home)` and
    lists the distinct homes after `→`, in table order, a homeless deferral
    counted and naming none. The two were ` . ` and `->` until #832 (`SEP`,
    `ARROW`). A home is `chain_check.deferred_home`'s answer (#866): what
    stands after the word up to the first ` — `, as `close` writes it, so a
    home written as prose prints as that prose. It reaches the panel as
    ASCII, anything outside it reading `?`, because the letter twin maps only
    the owner's characters and a home is somebody's text.

    Read off the table regardless of `capped`, because the two come apart in
    this tree: measured 2026-10-01 over every work item whose last record has
    `Pass` checked (`phases/phase-3.md`), every one reading `yes` holds a
    deferral, and ten reading `no` hold one too — a deferral by choice, or a
    capped round's findings carried into a verifying round.

    **`<R>` alone wherever the record cannot answer both questions** — a
    record that cannot be read, a `broad-gate.md` home, a record with no
    `Needs a fix` row or one `says_reopened` cannot read, and one with no
    readable `## Verdicts` table. Half an
    answer there would be a `capped` with no count beside it, or a count
    with nothing saying whether the run was capped, and neither is a shape
    `seal` leaves on a record it accepted (`spec.md` S4)."""
    head = str(round_count(item))
    if record is None or record.rows is None:
        return [("rounds", head)]
    chain, reader = record.chain, record.reader
    needs = chain.field(record.rows, chain.NEEDS)
    found, col, _header, _errors = chain.verdict_table(
        reader, record.lines, os.path.basename(record.path)
    )
    reopened = chain.says_reopened(needs) if needs is not None else None
    if reopened is None or col < 0:
        return [("rounds", head)]
    if reopened:
        head += f"{SEP}capped"
    count, homes = 0, []
    for _line, seen in found:
        word = chain.verdict_of(seen, col)
        if word == chain.DEFERRED:
            home = chain.deferred_home(seen[col])
            home = home.encode("ascii", "replace").decode("ascii") if home else None
            if home and home not in homes:
                homes.append(home)
        elif word != f"{chain.DEFERRED} {chain.NO_HOME}":
            continue
        count += 1
    rows = [("rounds", head)]
    if count:
        if homes:
            pieces = [f"{count} deferred {ARROW}", f" {homes[0]}"]
            rows += wrapped("", pieces + [f", {home}" for home in homes[1:]])
        else:
            rows.append(("", f"{count} deferred"))
    return rows


def pull_request(record):
    """`#<N>` from the record's `| PR |` row, or None.

    Read with `chain_check.PR_RE` over `PR_FIELD`, the way
    `chain_check.declared_pull_head` reads it. `not yet opened` — the honest
    value while the review runs — names no number, and neither does a
    `broad-gate.md` home, which has no such row. Nothing is looked up: the
    gate reads no network (`PARTITION`'s reason for the milestone step)."""
    if record is None or record.rows is None:
        return None
    found = record.chain.PR_RE.search(
        record.chain.field(record.rows, record.chain.PR_FIELD) or ""
    )
    return f"#{found.group(1)}" if found else None


def item_value(item, pr=None):
    """The `item` row: `#<pr> · <id>`, or `<id>` alone where the record names
    no pull request. `<id>` is the digits before the first `-` of the work
    item directory's name — the part every reference to a work item carries —
    and the whole name where it has no `-`. The separator was ` . ` until
    #832 (`SEP`)."""
    name = os.path.basename(os.path.normpath(item))
    ident = name.split("-", 1)[0] or name
    return f"{pr}{SEP}{ident}" if pr else ident


def panel(
    tree,
    base,
    checks,
    item,
    workflow=None,
    copy=None,
    branch=None,
    pr=None,
    record=None,
    run=None,
):
    """The stamp's rows, as `(label, value)`, with `""` as the label of a row
    that continues the one above it (#666) and `None` for the blank line
    between the identity rows and the result rows (#832).

    `base` is a `Base`. `copy` is `gate_copy`'s value and None leaves the
    `gate` row out; `branch` is `branch_name`'s, None on a detached HEAD;
    `pr` is `pull_request`'s, None where the record names none; `record` is
    `sealed_record`'s, which `rounds_rows` reads; `run` is the `RunRecord`
    of the row's run here, whose `suite_counts` the `suite` row prints
    (#869) — never the row's printed output, which a test can print into.

      SEALED
      tree      <tree>
                <branch>                   absent on a detached HEAD
      base      <commit>  <Base.ref>       the commit alone where the ref IS it
      item      #<pr> · <id>               absent without --record
      gate      tree <version>             only where `gate_copy` says so
      (blank)                              `None`
      suite     ✓ <recorded counts>        joined by ` · `, wrapped onto `""`
                                           rows; `exit N` where there are none
      ledger    ✓ <ok> ok · <d> drifted · <b> broken   `exit N` with no total
      chain     ✓ exit <code>              read off the chain's own check
      CI also   · <n> more steps           absent without a hygiene workflow
      rounds    <R>[ · capped]             absent without --record
                <k> deferred → <homes>     only where k > 0 (`rounds_rows`)

    **The result rows carry a `✓`, and the blank before them is a row**
    (#832, `spec.md` decision 6 of work item 1791270164, the owner's design
    of 2026-10-07). #717's owner had taken `chain exit 0`, the suite's
    `exit 0` and the ledger's `0 drifted . 0 broken` off the panel, because
    a panel drawn on success alone says again what `SEALED` says, and the
    sheet drew no blank line. The owner's newer design shows them, so they
    are back in one shape: a `✓` where the arm's count or exit was read, the
    ledger's three counts on its one row, `chain ✓ exit <code>`, and a dim
    `·` before `CI also`'s value, the mark of a row that is not a pass.
    `exit N` stays where a row has no count to print, because then it is the
    only statement of what that arm did. The failure form keeps every arm's
    exit code (`failure_lines`). The drawing does not know which label
    starts the result rows, so the blank before them is `None` here rather
    than a rule there; an older values file without one draws without it.

    **The values are the owner's characters** — ` · ` (`SEP`), `→`
    (`ARROW`), `✓ ` (`TICK`) and `· ` (`DOT`). They were ASCII, ` . ` and
    `->`, until #832, for the letter twin's console that is not UTF-8
    (`seal_stamp.pick_shape`), where `·` and `→` print as `?`. That console
    is served where it is drawn for: the twin maps the four to ASCII as it
    writes them, and the values stay what the owner chose.

    **The panel keeps its width, and nothing on it is cut by the frame.**
    A value is given `PANEL_VALUE_WIDTH` columns, the widest that keeps the
    stamp inside 80, and the owner chose continuation rows over a wider
    stamp (`questions.md` Q1 of #666). So the branch goes on the row under
    its label, where it has the whole width; a list — the suite's counts,
    the deferred homes — continues on further rows (`wrapped`, round 1's
    🟡 1); and every value passes through `fit` on the way out, which elides
    only a name: a branch keeps its HEAD, whose issue number is what a
    reader matches to a ticket, and a ref keeps its TAIL, because for the
    `origin/<base>` a runner reads the prefix is the part a reader can infer.
    The ref shares the `base` row with its commit since #832, two spaces
    after it, so it is elided to the room the commit leaves. Where step 1
    lands on a second remote the prefix is NOT inferable, and the line the
    gate prints is what names that ref in full — it fires whenever the given
    and resolved commits differ (`questions.md` W1, round 1 finding 5); the
    `SEALED` line names it in full as well.

    **Where the moved-base line does not fire, the ref on the `base` row is
    the only statement a reader gets.** A4 keeps the line silent where the
    two bases agree, so a fork whose base and `origin`'s name one commit
    renders a long `other/…` ref as its tail with the remote hidden — the
    stated cost of keeping the tail (`phases/phase-3.md`, round 2 finding
    13).

    Two rows left with #666, and why: `from` became the row under `base`,
    which #832 folded into the `base` row, and `row` — the exit code the
    repository's row came back with — continued under `suite` until #717
    took it off. NOT `("lint", "clean")` either: the row is
    one shell command line and nothing in it says which part is a linter
    (`templates/config.md` §*Broad gate*), so `clean` over a row with no
    linter in it is the sealer's stamp asserting a check that never ran.
    """
    stamp = stamp_module()
    rows = [("SEALED", ""), ("tree", tree)]
    if branch:
        rows.append(("", fit(branch)))
    if stamp.ref_is_commit(base.ref, base.commit):
        rows.append(("base", base.commit))
    else:
        room = PANEL_VALUE_WIDTH - len(f"{base.commit}  ")
        ref = fit(base.ref, keep="tail", width=room)
        rows.append(("base", f"{base.commit}  {ref}"))
    if item is not None:
        rows.append(("item", item_value(item, pr)))
    if copy:
        rows.append(("gate", copy))
    rows.append(None)
    counts = suite_counts(run) if run is not None else None
    if counts:
        first, *more = counts.split(", ")
        rows += wrapped(SUITE, [TICK + first, *(SEP + part for part in more)])
    else:
        rows.append((SUITE, f"exit {checks[SUITE].code}"))
    ledger = ledger_counts(checks[LEDGER].text)
    if ledger:
        ok, drifted, broken = ledger
        said = f"{ok} ok{SEP}{drifted} drifted{SEP}{broken} broken"
        rows.append((LEDGER, TICK + said))
    else:
        rows.append((LEDGER, f"exit {checks[LEDGER].code}"))
    rows.append((CHAIN_NAME, f"{TICK}exit {checks[CHAIN_NAME].code}"))
    # What this seal did NOT answer, which a reader otherwise reconstructs
    # from two files (#468). A COUNT, because a panel value is
    # `PANEL_VALUE_WIDTH` columns and a step name is a sentence — the names
    # go to stderr beside the command line, where `coverage_line` puts them
    # (`questions.md` W1).
    #
    # Absent where the repository has no such workflow, which is the ordinary
    # case away from this one: the partition describes SpecSeal's own CI, the
    # plugin ships to repositories that have none, and for them nothing about
    # the run changes (`spec.md` A7).
    #
    # Over the steps CI runs for THIS base (#666): `unanswered` leaves out the
    # four that run only into `main` on any other base, and the two CI skips
    # at `main` on a release one, so the number is one CI will ask.
    #
    # `CI also  <n> more steps` is the owner's wording (#717). The total it
    # was `<n> of` left the panel for the stderr line, which says it beside
    # the names; the row still prints at 0, because a row that goes quiet
    # reads as a gate that stopped looking. The dim `·` before the count is
    # the owner's mark for a row that is not a pass (#832); the label stays
    # `CI also`, seven columns already (`questions.md` Q15 of 1791270164).
    if job_steps(workflow, RELEASE_JOB) if workflow else []:
        short = len(unanswered(workflow, base.given))
        rows.append(("CI also", f"{DOT}{short} more steps"))
    if item is not None:
        rows += rounds_rows(item, record)
    return [None if row is None else (row[0], fit(row[1])) for row in rows]


def failure_lines(check, verdicts=None, record=None):
    """What the failure form quotes for one check: its first lines, the
    FAILED lines with their base verdict where there are any, the exit code,
    and the file holding the rest. `record` is the `RunRecord` of the row's
    run at `HEAD`, for the suite; None for every other check.

    **Where the record at `HEAD` left tests or collections out, it says how
    many** (#825's reframe after round 3). `record.unplaced` is the count of
    them — a test with no file of its own, a report a plugin built without
    its path — and each is in no list above, so a person reading the list
    alone would not know they ran.

    **Where a session at `HEAD` stopped part-way, it says how many did**
    (#849 round 1). `record.unended` is the count of them. The test a
    session stopped in may have written no failing line — one that kills
    plain pytest writes only its passing setup, and a `KeyboardInterrupt`
    writes no call — and the tests it never reached wrote none, so its file
    can be in no list above.

    **Where a line of the record at `HEAD` did not parse, it says how many**
    (#869). `record.unread` is the count of them; the gate passed each over,
    so a failing test it named is in no list above.

    **A failing `suite` ends with the counts its pytest recorded** (#869),
    `suite_counts` of `record`, in pytest's own words and never read off
    what the row printed. **Where no pytest the row ran left a record, it
    says so** (#448): the exit code alone reads as tests failing, and it is
    equally what a shell prints when the row never reached the suite —
    `cmd.exe` exits 1 with a "not recognized" line in the machine's own
    language — so the line names every cause of a missing record and says
    the exit is not a count. Where a record holds lines that did not parse,
    `UNREAD_HERE` has already said why no count follows.

    **A failing `ledger` ends with `evidence-check`'s `total:` line** (#666),
    the way a failing `suite` ends with its counts. The check prints that
    line LAST and this quotes its first lines, so a refusal for one drifted
    row reached the reader with no count of how many; it is added only where
    the quoted lines do not already hold it.
    """
    lines = [f"exit {check.code}", *check.first_lines()]
    if verdicts:
        # Where no pytest at `HEAD` left a record the base is not run, and
        # every row says so; nor is it where the base could not be checked
        # out. The heading does not claim otherwise (#825 rounds 1 and 2).
        words = set(verdicts.values())
        if words == {NO_RECORD_AT_HEAD}:
            lines.append(NAMED_BY_FAILED_LINES)
        elif words == {NOT_CHECKED_OUT}:
            lines.append(BASE_NOT_CHECKED_OUT)
        else:
            lines.append(COMPARED_AT_BASE)
        lines.extend(f"  {f}  {word}" for f, word in verdicts.items())
    if record is not None and record.unplaced:
        lines.append(UNPLACED.format(count=record.unplaced))
    if record is not None and record.unended:
        lines.append(UNENDED_HERE.format(count=record.unended))
    if record is not None and record.unread:
        lines.append(UNREAD_HERE.format(count=record.unread))
    if check.name == SUITE:
        counts = suite_counts(record) if record is not None else None
        if counts:
            lines.append(counts)
        elif record is None or not record.sessions:
            lines.append(NO_RECORD_HERE)
    if check.name == LEDGER:
        total = ledger_total(check.text)
        if total and total not in lines:
            lines.append(total)
    lines.append(f"full output: {check.path}")
    return lines


# The heading over a failing suite's files: compared at the base, named by
# `FAILED` lines alone where no pytest at `HEAD` left a record, or not
# compared because the base could not be checked out.
COMPARED_AT_BASE = "failing test files, compared at the base:"
NAMED_BY_FAILED_LINES = (
    "failing test files, named by FAILED lines; the base was not run:"
)
BASE_NOT_CHECKED_OUT = (
    "failing test files, not compared: the base could not be checked out:"
)

# The line under the listing where the record at `HEAD` counted tests or
# collections it wrote as no line, formatted with the count.
UNPLACED = (
    "{count} of the tests and collections the row's pytest reported had no "
    "file of their own and are in no list: a test a conftest or a plugin "
    "parents to the session or to a directory, a failed collection of the "
    "whole session, or a report a plugin built without its path (counted as "
    "unplaced on the end line of each record under records/)"
)

# The line under the listing where a session of the row's pytest at `HEAD`
# stopped part-way, formatted with how many did: the test it stopped in may
# have written no failing line, and the tests it never reached wrote none, so
# their file can be in no list above (#849 round 1).
UNENDED_HERE = (
    "{count} of the row's pytest sessions here stopped part-way, because the "
    "process died or the recorder stopped writing before the session's end "
    "line, or pytest stopped the session (an interrupt, pytest.exit(), -x or "
    "--maxfail, a plugin's stop) or ended it on an error of its own, so a test "
    "it stopped in may be in no list and the tests it never reached are in "
    "none (each session's record is under records/)"
)

# The line under the listing where a line of the records the row's pytest
# wrote at `HEAD` did not parse as the recorder's, formatted with how many
# (#869): the gate passed each over, so a failing test it named may be in no
# list, and no count of the suite is printed.
UNREAD_HERE = (
    "{count} of the lines in the records the row's pytest wrote here did not "
    "parse as the recorder's and each was passed over, so a failing test may "
    "be in no list and the suite's counts are not given (each session's "
    "record is under records/)"
)

# The line a failing `suite` gets where no pytest the row ran left a record,
# in place of the counts (#448, #869). Every cause of a missing record, never
# one of them as the only one (`NO_RECORD_CAUSES`); a pytest that died
# part-way is not among them, because it left a record and `UNENDED_HERE`
# counts it.
NO_RECORD_HERE = (
    "no pytest the row ran here left a record of the gate's recorder "
    f"({NO_RECORD_CAUSES.format(kept='suite.txt')}), so this exit code is not "
    "a count of failing tests"
)


# --- the command -------------------------------------------------------------


def seal_record(item, tree, root, base, keep, check=False):
    """`round_record.py seal` on the item; returns (exit code, output). The
    output is kept as `<keep>/seal.txt`, by `run`'s rule for a check named
    `seal`.

    `check` adds `--check` (#702): every refusal `seal` raises, asked with
    the same value the sealer's run would hand it, and nothing written. The
    preflight is its one caller with `check`.

    One `base`, not two. It took `base_ref` and `base` and its one caller
    passed `args.base` to both, which is a signature inviting whoever writes
    the second caller to give the two different values."""
    check = run(
        "seal",
        [
            sys.executable,
            RECORD,
            "seal",
            "--item",
            item,
            "--broad-gate",
            f"{tree} against {base}",
            "--root",
            root,
            "--baseline",
            base,
            *(["--check"] if check else []),
        ],
        root,
        keep,
    )
    return check.code, check.text


# --- the preflight (#638) -----------------------------------------------------
#
# The record arms, then `seal`'s own refusals (#702), typed by the orchestrator
# before it spawns the sealer. Neither head begins `SEALED` or `NOT SEALED`: a
# preflight is read by the same eyes and the same tests that read a seal, and
# either word on it would be taken for one.
PREFLIGHT_PASSED = "PREFLIGHT PASSED   {tree} against {base}"
PREFLIGHT_FAILED = "PREFLIGHT FAILED   {tree} against {base}"
PREFLIGHT_TAIL = (
    " · the record arms, and `seal`'s refusals where a work item is declared "
    "for the branch: the `Broad gate` row was not run and nothing is sealed"
)
# Appended to the stderr line that quotes the row, so a reader sees the row
# was read — every refusal about it still applies — and not handed to a shell.
ROW_NOT_RUN = " — read, and not run: this is a preflight"
PREFLIGHT_RECORD = (
    "broad-gate: --preflight and --record were both given, and a preflight "
    "writes no cell — nothing ran. The cell is the sealer's, written by a full "
    "run: `broad-gate --base <base> --record <item>`. Drop `--record`: the "
    "preflight asks `seal`'s refusals of the branch's declared work item on "
    "its own"
)
# The one stderr line the ask prints (#702): what `seal --check` was asked
# about and what it answered, or why nothing was asked. `{home}` is the
# record it read where that file is on disk, and the work item's directory
# otherwise — where it refused, and for a `straight to the PR` item whose
# `broad-gate.md` the sealer has not written yet (round 1's ⬜ 4), so the
# line never names a file the reader cannot open.
PREFLIGHT_ASKED = (
    "broad-gate: asked `round_record.py seal --check` of {home}, found through "
    "the one declaration naming {branch}: {outcome}"
)
ASKED_PASSED = "no refusal, and nothing was written"
ASKED_REFUSED = "it refused, and nothing was written — `seal` is in the verdict"
PREFLIGHT_NOT_ASKED = (
    "broad-gate: `seal`'s refusals were not asked — no single work item "
    "declares {branch}: either none does or more than one does, so there is "
    "no one work item to ask them of"
)
PREFLIGHT_DETACHED = (
    "broad-gate: `seal`'s refusals were not asked — HEAD is detached, so no "
    "declaration names this checkout and there is no record to ask them of"
)


def preflight_line(head, tree, base):
    """The first line of a preflight's stdout: which verdict, the tree, the
    resolved base, and what the run did not do."""
    return head.format(tree=tree, base=base) + PREFLIGHT_TAIL


def preflight_asked_line(where, root, branch, outcome, flavour=os.path):
    """`PREFLIGHT_ASKED` for the home `where` under `root`, which it names
    repository-relative and with `/` on every platform, the way a path is
    written everywhere else in this repository.

    `flavour` is the path module whose separator applies, `os.path` for the
    running platform. A case passes `ntpath` to exercise the Windows
    separator from a POSIX machine: the line used to print `relpath` as it
    came, and the Windows leg alone saw `seal\\specs\\…` (`agent-contract`
    §13). Callers pass four arguments."""
    return PREFLIGHT_ASKED.format(
        home=flavour.relpath(where, root).replace(flavour.sep, "/"),
        branch=f"`{branch}`",
        outcome=outcome,
    )


def gate(args, console_wants_letters, terminal=False):
    """The run. `terminal` is whether stdout has a person in front of it:
    only then, and only over a written cell, is the stamp drawn here, and
    every other sealed run signals instead (#400). Its default is the pipe, which is what every caller that
    is not `__main__` — a case driving this in process — is writing to."""
    stamp = stamp_module()
    root = repo_root(os.path.abspath(args.root or os.getcwd()))
    if root is None:
        raise Refused(
            f"broad-gate: {args.root or os.getcwd()} is not in a git repository — "
            "nothing ran"
        )
    home = seal_home(root)
    if home is None:
        raise Refused(
            f"broad-gate: {root} has no seal/ at either place a root lives "
            "(`<repo>/seal/`, `<git-common-dir>/seal/`) — this repository is "
            "not opted in, and there is no config to read a command from. "
            "Nothing ran"
        )
    command = broad_command(home)
    if command is None:
        raise Refused(missing_row(home))
    # The one place the value is looked at before a shell is handed it, and
    # the only one there needs to be: the other surface that runs the row
    # (`compare_at_base`, which runs it once, unchanged, at the base) is
    # reached only after the run below, so this refusal closes it by
    # reachability rather than by a second guard in a second place (`spec.md`
    # §*The class, enumerated by construction*). It runs the very row this
    # refusal passed (#825).
    unrunnable = not_as_written(home, command)
    if unrunnable:
        raise Refused(unrunnable)
    head = git(root, "rev-parse", "--short", "HEAD")
    if head is None:
        raise Refused(f"broad-gate: {root} has no HEAD to seal — nothing ran")
    # The one read of `args.base` in this file, and the count is held by a
    # case: a seventh consumer written later cannot take the unresolved value
    # without that case going red (`spec.md` §*The class, enumerated by
    # construction*). Every check below asks `base.commit`, which is the
    # commit CI will compare against. The readers of `base.given`, the
    # caller's spelling, are none of them a check: `moved_line`, which exists
    # to say how that spelling differs from what it resolved to; and, through
    # `base_is_main`, `skipped_at_main` (#473) and the `workflow` count —
    # `coverage_line` and `panel`, through `steps_for` (#666) — because the
    # workflow's guard compares a branch NAME (`github.base_ref`) and a
    # resolved commit carries no name.
    base = resolve_base(root, args.base)
    if base.commit is None:
        raise Refused(
            f"broad-gate: --base {base.given} does not resolve in {root} — nothing "
            "ran. A base that cannot be checked out is a base nothing can be "
            "compared against"
        )
    tree = head.strip()
    branch = branch_name(root)
    item = None
    if args.record:
        if args.preflight:
            raise Refused(PREFLIGHT_RECORD)
        item = os.path.abspath(args.record)
        if not os.path.isdir(item):
            raise Refused(f"broad-gate: --record {args.record} is not a directory")
    # The work item the preflight asks `seal`'s refusals of (#702): the ONE
    # declaration naming the checked-out branch, or "" for none, two, or a
    # detached HEAD. It is read from the working tree, as the commit gate
    # reads it and as `seal` reads the records, and not from HEAD as the
    # chain arm reads it (round 1's ⬜ 3): an uncommitted declaration counts
    # here and not there. Resolved
    # here, before anything runs, so a copy of the plugin missing the reader
    # is a refusal with nothing spent rather than one after the arms.
    asked = ""
    if args.preflight:
        asked = load(ROUTING, "specseal_routing_for_broad_gate").item_dir(root, branch)

    keep = args.keep_output or tempfile.mkdtemp(prefix="broad-gate-")
    os.makedirs(keep, exist_ok=True)
    py = sys.executable
    specs = os.path.join(home, SPECS)
    checks = {}
    # The first of `verify`'s four conditions is to name the command before
    # running it, and the row is the only part of this run the gate did not
    # choose. `agents/sealer.md` asks the sealer to quote it and let the
    # reader judge it — and the sealer opens no repository file, by its own
    # rule, so it has to arrive here (round 1's 🟡 9). `run` wrote it to the
    # kept output file and nothing reached the report.
    said = moved_line(root, base)
    if said:
        sys.stderr.write(said + "\n")
    sys.stderr.write(
        f"broad-gate: `{ROW}` says: {command}"
        + (ROW_NOT_RUN if args.preflight else "")
        + "\n"
    )
    # Before the checks rather than after them, so a run that comes back NOT
    # SEALED carries it too: what this run's seal would not have covered is as
    # much a fact about a failed run as about a sealed one. A preflight prints
    # none: the line says what THIS SEAL answers, and a preflight seals nothing.
    workflow = workflow_text(root)
    coverage = (
        coverage_line(workflow, base.given) if workflow and not args.preflight else None
    )
    if coverage:
        sys.stderr.write(coverage + "\n")
    # The arms CI's own steps skip at this base, where this repository's
    # workflow carries those steps (#473). Neither has a panel row, and a step
    # both sides skip is agreed rather than unanswered, so the line is the
    # whole of what a reader sees change.
    skipped = skipped_at_main(base.given, workflow)
    if skipped:
        sys.stderr.write(skipped_line(skipped) + "\n")
    # A preflight skips the row by CONDITION and keeps this assignment where it
    # stands: `PARTITION`'s cases read every `checks[...] = run(...)` in this
    # function, so a second list of arms for the preflight would be the drift
    # that table was declared to end (#468). Every arm below runs either way.
    # The row's run records what each pytest it starts ran (#825), under a key
    # made for this run alone. The record is read once, here, for every
    # outcome (#869): the failure loop below takes its failing files and its
    # counts from it, and the panel its counts.
    head_key = record_key("head")
    head = None
    if not args.preflight:
        checks[SUITE] = run(
            SUITE, command, root, keep, shell=True, env=recording_env(keep, head_key)
        )
        head = read_record(records_dir(keep), head_key, root)
    checks[LEDGER] = run(LEDGER, [py, EVIDENCE, "--strict", root], root, keep)
    checks[UNVERIFIED_NAME] = run(
        UNVERIFIED_NAME,
        [py, UNVERIFIED, "--baseline", base.commit, specs],
        root,
        keep,
    )
    checks[CHAIN_NAME] = run(
        CHAIN_NAME,
        [py, CHAIN, "--baseline", base.commit, "--root", root],
        root,
        keep,
        env=draft_env(keep),
    )
    if SURVIVORS_NAME not in skipped:
        survivor_args = [
            py,
            SURVIVOR,
            "--range",
            f"{base.commit}...HEAD",
            "--root",
            root,
        ]
        for path in exemptions(home):
            survivor_args += ["--exempt", path]
        checks[SURVIVORS_NAME] = run(SURVIVORS_NAME, survivor_args, root, keep)
    # The two arms #468 added, and `PARTITION` is where each says which step
    # of the workflow it stands for. The range is the survivor arm's, spelled
    # the same way for the same reason: both walk what this branch did
    # relative to the commit CI will compare against.
    if CORRECTIONS_NAME not in skipped:
        checks[CORRECTIONS_NAME] = run(
            CORRECTIONS_NAME,
            [py, CORRECTION, "--range", f"{base.commit}...HEAD", "--root", root],
            root,
            keep,
        )
    # No `--root`: `seal.py mode` resolves the repository from the working
    # directory, which `run` already sets to the tree being gated.
    checks[MODE_NAME] = run(MODE_NAME, [py, SEAL_SCRIPT, "mode", "--check"], root, keep)

    failures = []
    for name, check in checks.items():
        if not check.failed:
            continue
        verdicts, record = None, None
        if name == SUITE:
            # The failing files come from the record the row's pytest wrote
            # here. Where no pytest left a record there is nothing to
            # compare, so the `FAILED` lines only name the files, and the base
            # is not run (#825). A session that stopped part-way here is
            # counted under the list (#849 round 1), and so is a line of the
            # record that did not parse (#869).
            record = head
            if head.sessions:
                files = list(head.failing)
                if files:
                    verdicts = compare_at_base(root, base.commit, command, files, keep)
            else:
                verdicts = {f: NO_RECORD_AT_HEAD for f in failing_files(check.text)}
        failures.append((name, failure_lines(check, verdicts, record)))
    # The preflight's ask (#702), after the arms and whatever they found, so
    # a chain refusal and a `seal` refusal are both named in one run. It is
    # NOT an arm: it mirrors no CI step, so it is no `checks[...] = run(...)`
    # (`PARTITION`'s cases read every one) and the loop above stays the one
    # loop. `seal --check` stops before the write, and a refusal joins the
    # failures in the failure form's own words.
    if args.preflight and asked:
        code, text = seal_record(asked, tree, root, base.commit, keep, check=True)
        if code != 0:
            kept = os.path.join(keep, "seal.txt")
            failures.append(("seal", failure_lines(Check("seal", code, text, kept))))
            where, outcome = asked, ASKED_REFUSED
        else:
            record = sealed_record(asked, root)
            on_disk = record is not None and os.path.isfile(record.path)
            where, outcome = (record.path if on_disk else asked), ASKED_PASSED
        sys.stderr.write(preflight_asked_line(where, root, branch, outcome) + "\n")
    elif args.preflight:
        sys.stderr.write(
            (
                PREFLIGHT_NOT_ASKED.format(branch=f"`{branch}`")
                if branch
                else PREFLIGHT_DETACHED
            )
            + "\n"
        )
    sys.stderr.write(f"broad-gate: outputs kept under {keep}\n")
    if failures:
        form = stamp.not_sealed(tree, base.commit, failures, branch, base.ref)
        if args.preflight:
            # The same per-check lines under a first line that is not a
            # verdict on a seal. The form is `seal_stamp`'s, kept in one
            # place, and only its head is the preflight's (`phases/phase-1.md`
            # of 1790815611 says why the head is replaced here rather than
            # passed in).
            form[0] = preflight_line(PREFLIGHT_FAILED, tree, base.commit)
        sys.stdout.write("\n".join(form) + "\n")
        return 1
    if args.preflight:
        sys.stdout.write(preflight_line(PREFLIGHT_PASSED, tree, base.commit) + "\n")
        return 0

    if item is not None:
        code, text = seal_record(item, tree, root, base.commit, keep)
        sys.stdout.write(text)
        if code != 0:
            # `seal` exits 2 on a refusal raised BEFORE the write, and it
            # returns whatever `chain_check` returned from AFTER it — 1 for
            # errors, 2 for a check that could not run. Only the first means
            # no cell was written, and neither of them is a seal. Reading
            # `== 2` let the second fall through to the drawing.
            #
            # The exit code cannot tell the two apart, because both sides
            # can be 2 — and NEITHER can the presence of a `round-record:`
            # line, which is what this message used to point at: a refusal
            # prints `round-record: <why>` and a write prints
            # `round-record: sealed <path> — …`, and `run` merges both of
            # the child's streams into the text above. The word is `sealed`.
            wrote = any(
                line.startswith("round-record: sealed") for line in text.splitlines()
            )
            sys.stderr.write(
                f"broad-gate: every check passed and `round_record.py seal` "
                f"exited {code}, so nothing is sealed. "
                + (
                    "The `round-record: sealed` line above says the cell WAS "
                    "written, and what stands under it is the chain check "
                    "`seal` runs after the write — the cell is now on a "
                    "record that check still fails"
                    if wrote
                    else "The `round-record:` line above is a refusal raised "
                    "before the write, and no cell was written"
                )
                + "\n"
            )
            return 2
    record = sealed_record(item, root) if item is not None else None
    rows = panel(
        tree,
        base,
        checks,
        item,
        workflow,
        gate_copy(root, installed=getattr(args, "invoked_as", None)),
        branch=branch,
        pr=pull_request(record),
        record=record,
        run=head,
    )
    # The cell is in the working tree and CI reads HEAD (#666): said after
    # the stamp or the `SEALED` line, on the same stream, and only where a
    # cell was written and git still sees it uncommitted.
    uncommitted = uncommitted_line(root, record)
    if terminal and item is not None:
        # A person is in front of this stream, and it is the one place the
        # gate draws. Once, and no values file is left for anyone else to
        # draw a second time (#400). Only over a written cell: #400's
        # Done-when says no other path draws a stamp, so a run without
        # `--record` signals on a terminal too.
        shape = args.shape or console_wants_letters
        sys.stdout.write("\n" + "\n".join(stamp.stamp(rows, shape)) + "\n\n")
        if uncommitted:
            sys.stdout.write(uncommitted + "\n")
        return 0
    sys.stdout.write(
        signal(
            stamp,
            root,
            tree,
            base,
            item,
            rows,
            branch=branch,
            pr=pull_request(record),
        )
        + "\n"
    )
    if uncommitted:
        sys.stdout.write(uncommitted + "\n")
    return 0


# The variable Claude Code sets in every Bash call, a subagent's included, to
# the id of the MAIN session — the id a `Stop` payload carries as `session_id`
# (`questions.md` Q2 of 1790562543, measured 2026-09-28). It is not
# documented, and where it is absent the values land under `none/`, which no
# hook reads, and the signal line says so.
SESSION_VAR = "CLAUDE_CODE_SESSION_ID"

# The second variable the gate reads, and the one it sets itself: `main`
# hands the tree's copy, on the redirect, the realpath of the copy the caller
# invoked, and nobody else sets or reads it. `gate_copy` compares the two
# files' bytes to decide whether the panel's `gate` row says anything (#666).
# Absent, the running copy was invoked directly, or redirected by an installed
# copy older than #666, which sets no such variable.
INVOKED_AS_VAR = "SPECSEAL_BROAD_GATE_INVOKED_AS"

NOTHING_RECORDED = (
    " · nothing was recorded (no --record), so no stamp is written or drawn"
)
VALUES_UNWRITTEN = " · nothing will be drawn: the stamp's values could not be written"
NO_SESSION_FOUND = (
    " · no Claude Code session was found, so no hook draws the stamp; "
    "`seal-stamp --from {command}` draws it"
)
# The recovery is named on this line too (round 1's 🟡 1). The hook draws
# nothing, and says nothing, where it cannot: a `python3` under
# `seal_stamp.py`'s 3.12 floor, a main session whose working directory is
# outside this clone, or a plugin older than the hook. The gate cannot see any
# of those, so it names the way to draw the stamp by hand on every line that
# names a values file. `NOTHING_RECORDED` and `VALUES_UNWRITTEN` name none,
# because neither run left a drawing to recover.
DRAWN_AT_TURN_END = (
    " · the stamp is drawn at the end of the turn of session {session}, from "
    "{path}; where none appears, `seal-stamp --from {command}` draws it"
)

# The `scale` every values file still carries, and what it was before #853
# retired the scale. Read by nothing in this tree. Written for one release
# cycle, 0.21's, because the gate a session runs is the tree's copy (`main`
# hands over to it) while the `Stop` hook that draws the file, and the
# `seal-stamp` a person types, are the installed plugin's: one older than
# #853 refuses a values file without a numeric `scale` and leaves the
# sealer's stamp undrawn (#869 round 1's 🟡 3). Remove it, and its pin in
# `tests/test_the_seal_is_taken_once_by_the_sealer.py`, in the first release
# after 0.21, once no installed plugin older than #853 is left to draw.
SCALE_FOR_OLDER_HOOKS = 0.9

# The line after the `SEALED` line on a recorded seal (#666). `seal` writes
# the cell into the working tree and commits nothing, CI reads the record at
# HEAD, and a pull request marked ready over an uncommitted cell fails on a
# cell reading `not yet` — after the one broad run it was meant to record. It
# names the act and the reason, and nothing it says is a question.
CELL_UNCOMMITTED = (
    "broad-gate: the `Broad gate` cell is written to {path} and not committed. "
    "CI reads the record at HEAD, so commit it before the pull request is "
    "marked ready"
)


def uncommitted_line(root, record):
    """`CELL_UNCOMMITTED` for the file the cell went into, or None.

    None without a record, and None where git says the file does not differ
    from HEAD: a re-seal at the commit and base the newest entry already
    records rewrites the same bytes (#174), and a line saying *not committed*
    over a committed file would be false on its face. Asked of git rather
    than assumed, so the line is true wherever it prints."""
    if record is None:
        return None
    # Both by realpath: `--record` arrives as typed, and the root as git
    # resolved it, so on a checkout under a symlinked directory the two
    # spellings of one file relate by `../..` and git reads the path as
    # outside the repository.
    rel = os.path.relpath(os.path.realpath(record.path), os.path.realpath(root))
    status = git(root, "status", "--porcelain", "--", rel)
    if not (status and status.strip()):
        return None
    return CELL_UNCOMMITTED.format(path=rel)


def common_dir(root):
    """The git common dir of `root`, absolute, or None."""
    common = git(root, "rev-parse", "--git-common-dir")
    if not (common and common.strip()):
        return None
    return os.path.normpath(os.path.join(root, common.strip()))


def signal(stamp, root, tree, base, item, rows, branch=None, pr=None):
    """The one line a sealed run prints where nobody can see a drawing.

    It starts with `SEALED` and carries `<branch> @ <tree> against <ref> @
    <base commit>` (`seal_stamp.sealed_names`), the way the failure form
    starts `NOT SEALED`. On a recorded seal it writes the panel's `rows` to a
    values file first and names it: the drawing is then the hook's, in the
    session that spawned the run, and this line is what reaches the report. A
    values file that cannot be written leaves the run sealed — every check
    passed and the cell was written — and says on stderr why nothing will be
    drawn.

    The values file carries `branch` and `pr` beside the keys it always had,
    which `seal_stamp.label` reads for the line above the drawing; a hook
    older than this gate ignores both and draws the rows under its own
    label. Its `scale` is read by nothing since #853 — the disc has one size
    — and is still written, as the constant `SCALE_FOR_OLDER_HOOKS`, for
    the one release cycle a hook older than #853 can meet the file
    (`docs/the-broad-gate.md` §*Where the stamp is drawn*)."""
    head = f"SEALED   {stamp.sealed_names(tree, base.commit, branch, base.ref)}"
    if item is None:
        return head + NOTHING_RECORDED
    session = os.environ.get(SESSION_VAR)
    values = {
        "tree": tree,
        "base": base.commit,
        "from": base.ref,
        "branch": branch,
        "pr": pr,
        "item": item,
        "session": session or None,
        "scale": SCALE_FOR_OLDER_HOOKS,
        "rows": rows,
    }
    common = common_dir(root)
    try:
        if common is None:
            raise OSError(f"{root} has no git common directory")
        path = stamp.write_values(common, session, values)
    except OSError as exc:
        sys.stderr.write(
            f"broad-gate: the stamp's values could not be written ({exc}), so "
            "nothing will be drawn. The run is still sealed: every check passed "
            "and the cell was written\n"
        )
        return head + VALUES_UNWRITTEN
    # Quoted for the shell the person types it into, so a checkout whose path
    # holds a space prints a command that runs as printed (round 1's ⬜ 5).
    command = quote(path)
    if stamp.session_key(session) == stamp.NO_SESSION:
        return head + NO_SESSION_FOUND.format(command=command)
    return head + DRAWN_AT_TURN_END.format(session=session, path=path, command=command)


def main(argv=None, console_wants_letters=None, console_is_terminal=None):
    """`console_wants_letters` is `pick_shape` asked of stdout as the process
    found it, and `console_is_terminal` is `is_terminal` asked of it —
    `__main__` asks both before it reconfigures the streams."""
    try:
        stamp = load(STAMP, "specseal_seal_stamp_for_broad_gate")
    except Refused as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2
    parser = argparse.ArgumentParser(
        prog="broad-gate",
        description="The one broad run, after the rounds settle: the "
        "repository's command and the plugin's checks, then the stamp.",
    )
    parser.add_argument("--base", required=True, help="the branch this merges into")
    parser.add_argument("--root", default=None, help="the repository (default: cwd)")
    parser.add_argument(
        "--record",
        default=None,
        metavar="ITEM",
        help="the work item whose last record takes the `Broad gate` cell",
    )
    parser.add_argument(
        "--shape", action="store_true", help="the letter twin, whatever the console"
    )
    parser.add_argument(
        "--keep-output",
        default=None,
        metavar="DIR",
        help="where each check's output is kept (default: a temp dir)",
    )
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="the record arms, then `seal --check` of the branch's declared work "
        "item, before the sealer is spawned: the row is read and not run, and "
        "nothing is sealed or written (#638, #702)",
    )
    # The redirect is decided from `parse_known_args`, before this copy's
    # parser can refuse an argument only the tree's copy knows: a flag added
    # to the gate is a change to the gate, and the copy that predates it must
    # not be the one that answers (#475; round 1's 🟡 1). `--base` is still
    # required here, so a call with no base is refused by the same parser as
    # before. The gated tree's own copy runs in place of this one with the
    # same argument vector, under the same interpreter, with inherited
    # streams; its exit code is this run's. Before `gate()` and before
    # anything runs, so `gate` is not entered by the copy that hands over.
    # `args.base` is not read here: the one read stays in `gate`, and the
    # child resolves it for itself. A root that is not a repository takes
    # `gate`'s own refusal below, unchanged.
    known, _unknown = parser.parse_known_args(argv)
    root = repo_root(os.path.abspath(known.root or os.getcwd()))
    if root is not None:
        shipped = shipped_gate(root)
        if shipped is not None:
            sys.stderr.write(redirect_line(root, shipped) + "\n")
            handed = sys.argv[1:] if argv is None else list(argv)
            env = {**os.environ, INVOKED_AS_VAR: os.path.realpath(__file__)}
            return subprocess.run(
                [sys.executable, shipped, *handed], env=env
            ).returncode
    args = parser.parse_args(argv)
    # Taken OUT of the environment rather than read from it: every check
    # below inherits this process's environment, and a suite that loads this
    # module in process would otherwise answer `gate_copy` for a redirect it
    # never made (#666).
    args.invoked_as = os.environ.pop(INVOKED_AS_VAR, None) or None
    if root is not None:
        sys.stderr.write(running_line(root) + "\n")
    if console_wants_letters is None:
        console_wants_letters = stamp.pick_shape(sys.stdout)
    if console_is_terminal is None:
        console_is_terminal = stamp.is_terminal(sys.stdout)
    try:
        return gate(args, console_wants_letters, terminal=console_is_terminal)
    except Refused as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2


if __name__ == "__main__":
    # Which form, and whether a person is looking at all, asked of stdout as
    # the process found it — before the loop below moves every stream to
    # UTF-8 (`seal_stamp.py` measured why).
    try:
        _stamp = load(STAMP, "specseal_seal_stamp_for_broad_gate")
    except Refused as _exc:
        sys.stderr.write(str(_exc) + "\n")
        sys.exit(2)
    _letters = _stamp.pick_shape(sys.stdout)
    _terminal = _stamp.is_terminal(sys.stdout)
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main(console_wants_letters=_letters, console_is_terminal=_terminal))
