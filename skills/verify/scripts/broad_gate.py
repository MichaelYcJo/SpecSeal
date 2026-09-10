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
     itself. **No row is a refusal, not a default**: the command names the
     row to write and exits 2 with nothing run, because a seal taken over a
     command nobody chose is the counterfeit `verify` names
  2. `evidence-check --strict .`       the ledger's rows still anchor
  3. `unverified-check --baseline <base> seal/specs/`
  4. `chain_check.py --baseline <base>`   judged as a DRAFT pull request,
     because the cell this run is about to write still reads `not yet`
  5. `survivor-check --range <base>...HEAD`, with every
     `seal/specs/*/survivors.md` as `--exempt`

Every exit code is read directly off the subprocess (`agent-contract` §1),
and every check's output is kept in a file under `--keep-output` so the
report can quote a failing check's first lines and name where the rest is.
A check that fails does not stop the ones after it: the failure form names
every check that failed, which is what a reader acts on.

**On a failing test the comparison against the base is reactive and
mechanical** (`skills/verify/SKILL.md` §*The broad gate*). Only when the
repository's command fails AND its output names failing test files does the
gate add a scratch worktree at `<base>`, run the row's first command on those
files there, remove the worktree, and label each file `new` or `failing on
base too`. It decides nothing about either word: both go in the report and
the reader acts.

**Printed on success only.** The stamp — the disc and a panel carrying the
tree, the base, the suite's counts, the lint, the ledger's counts, the
chain's exit, and the round count when `--record` names a work item — is
`seal_stamp.stamp`'s. The failure form is `NOT SEALED <tree> against <base>`
and the failing checks with their first lines, no drawing.

`--record <item>` runs `round_record.py seal` on success, which sets the LAST
record's `Broad gate` cell and nothing else. With `--record`, success is the
checks green AND the cell written: a refusal from `seal` (the last record's
`Pass` is unchecked, so a finding is still open; or the SHA is premature) is
exit 2 and no stamp, because a seal over a record that says the run came too
early is a stamp over a contradiction.

Usage:
  broad-gate --base <ref> [--root DIR] [--record <item>] [--shape]
             [--scale 1.0] [--keep-output DIR]

Exit codes: 0 sealed · 1 not sealed · 2 refused — no row, no repository, a
base that does not resolve, a scale outside the band, a `seal` the record
refused; nothing ran on 2 except where the refusal names what ran.
"""

import argparse
import glob
import importlib.util
import json
import os
import re
import shlex
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
CHAIN = os.path.join(PLUGIN, "skills", "code-review", "scripts", "chain_check.py")
SURVIVOR = os.path.join(PLUGIN, "skills", "code-review", "scripts", "survivor_check.py")
RECORD = os.path.join(PLUGIN, "skills", "code-review", "scripts", "round_record.py")
CONFIG_READER = os.path.join(PLUGIN, "hooks", "config.py")

SEAL_DIR = "seal"
CONFIG = "config.md"
ROW = "Broad gate"
SPECS = "specs"
SURVIVORS = "survivors.md"
ROUND_RE = re.compile(r"^round-(\d+)\.md$")

# The five checks, by the name the report prints for each. The first is the
# repository's own command; the panel reads its `suite` and `lint` from that
# one run, because the row carries both.
SUITE, LEDGER, UNVERIFIED_NAME, CHAIN_NAME, SURVIVORS_NAME = (
    "suite",
    "ledger",
    "unverified",
    "chain",
    "survivors",
)

# How many lines of a failing check's output the report quotes before naming
# the file that holds the rest.
QUOTED = 8

NEW, ON_BASE = "new", "failing on base too"

# pytest's short-summary line for a failed test, `FAILED path::name - why`,
# printed under `-q` too. The file is what the base comparison re-runs.
FAILED_RE = re.compile(r"^FAILED\s+(\S+?)::", re.M)
# The counts on pytest's last line — `768 passed, 1 skipped in 12.3s` — with
# the `=` decoration and the timing left off. Searched from the last line
# backwards, because the row's command may print a linter's output after it.
COUNTS_RE = re.compile(
    r"(\d+ (?:passed|failed|skipped|errors?|xfailed|xpassed|deselected|warnings?)"
    r"(?:, \d+ [a-z]+)*)"
)
# `evidence-check`'s total line: `total: N ok · D drifted · B broken · …`.
LEDGER_RE = re.compile(r"total: (\d+) ok · \d+ drifted · (\d+) broken")


class Refused(Exception):
    """A reason nothing ran (exit 2)."""


def load(path, name):
    """Import a sibling script by path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None or not os.path.isfile(path):
        raise Refused(f"cannot load {path} — this copy of the plugin is missing it")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def broad_command(home):
    """The `Broad gate` row's value, or None for every way of not having one:
    no file, no row, an empty value, a file that will not read."""
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    try:
        with open(os.path.join(home, CONFIG), encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, ValueError):
        return None
    for item, value in config.config_rows(text):
        if item == ROW:
            return value or None
    return None


def missing_row(home):
    return (
        f"broad-gate: {os.path.join(home, CONFIG)} has no `{ROW}` row, so there "
        "is no command to seal over. Write the repository's own broad command "
        "into it as one shell command line —\n"
        f"    | {ROW} | <the full suite, the repository-wide lint, the typecheck> |\n"
        "— and run this again. There is no default: a seal taken over a "
        "command nobody chose seals nothing (`skills/verify/SKILL.md` §*The "
        "Seal Test*). Nothing ran."
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


def run(name, command, root, keep, shell=False, env=None):
    """Run one check from the repository root, keep its output under
    `keep/<name>.txt`, and return it with the exit code read directly."""
    r = subprocess.run(
        command,
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
        handle.write(f"exit {r.returncode}\n\n")
        handle.write(text)
    return Check(name, r.returncode, text, path)


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


def failing_files(text):
    """The test files pytest's `FAILED` lines name, in first-seen order."""
    return list(dict.fromkeys(FAILED_RE.findall(text)))


def first_command(command):
    """The row's first `&&`-joined command — the suite runner, by the shape
    every row this plugin has seen takes (`bin/test -q && uvx ruff …`)."""
    return command.split("&&", 1)[0].strip()


def compare_at_base(root, base, command, files, keep):
    """{file: `new` | `failing on base too`}, measured — never inferred.

    A scratch worktree at `base`, the row's first command run there on the
    failing files alone, the worktree removed whatever happened. A file the
    base does not carry cannot fail there, so it reads `new`, which is the
    truth: the test arrived with this branch.
    """
    scratch = tempfile.mkdtemp(prefix="broad-gate-base-")
    added = git(root, "worktree", "add", "--detach", scratch, base)
    if added is None:
        return {
            f: f"{NEW}? the base could not be checked out for comparison" for f in files
        }
    try:
        runner = f"{first_command(command)} {' '.join(shlex.quote(f) for f in files)}"
        check = run("suite-at-base", runner, scratch, keep, shell=True)
    finally:
        subprocess.run(
            ["git", "-C", root, "worktree", "remove", "--force", scratch],
            capture_output=True,
        )
    at_base = set(failing_files(check.text))
    return {f: (ON_BASE if f in at_base else NEW) for f in files}


# --- what the panel reads --------------------------------------------------


def suite_counts(text):
    for line in reversed(text.splitlines()):
        m = COUNTS_RE.search(line)
        if m:
            return m.group(1)
    return None


def ledger_counts(text):
    m = LEDGER_RE.search(text)
    return f"{m.group(1)} ok . {m.group(2)} broken" if m else None


def round_count(item):
    try:
        names = os.listdir(os.path.join(item, "rounds"))
    except OSError:
        return 0
    return sum(1 for n in names if ROUND_RE.match(n))


def panel(tree, base, checks, item):
    rows = [
        ("SEALED", ""),
        None,
        ("tree", tree),
        ("base", base),
        None,
        (SUITE, suite_counts(checks[SUITE].text) or "exit 0"),
        # NOT `("lint", "clean")`. The row is one shell command line and
        # nothing in it says which part is a linter (`templates/config.md`
        # §*Broad gate*), so `clean` over a row with no linter in it is the
        # seal asserting a check that never ran — the counterfeit `verify`
        # names, printed on the artifact a reader trusts BECAUSE it is drawn
        # on success alone. What the gate actually measured is the row's
        # exit code.
        ("row", f"exit {checks[SUITE].code}"),
        (LEDGER, ledger_counts(checks[LEDGER].text) or "exit 0"),
        (CHAIN_NAME, f"exit {checks[CHAIN_NAME].code}"),
    ]
    if item is not None:
        rows += [None, ("rounds", str(round_count(item)))]
    return rows


def failure_lines(check, verdicts=None):
    """What the failure form quotes for one check: its first lines, the
    FAILED lines with their base verdict where there are any, the exit code,
    and the file holding the rest."""
    lines = [f"exit {check.code}", *check.first_lines()]
    if verdicts:
        lines.append("failing test files, compared at the base:")
        lines.extend(f"  {f}  {word}" for f, word in verdicts.items())
    counts = suite_counts(check.text) if check.name == SUITE else None
    if counts:
        lines.append(counts)
    lines.append(f"full output: {check.path}")
    return lines


# --- the command -------------------------------------------------------------


def seal_record(item, tree, base_ref, root, base, keep):
    """`round_record.py seal` on the item; returns (exit code, output)."""
    check = run(
        "seal",
        [
            sys.executable,
            RECORD,
            "seal",
            "--item",
            item,
            "--broad-gate",
            f"{tree} against {base_ref}",
            "--root",
            root,
            "--baseline",
            base,
        ],
        root,
        keep,
    )
    return check.code, check.text


def gate(args, console_wants_letters):
    stamp = load(STAMP, "specseal_seal_stamp_for_broad_gate")
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
    head = git(root, "rev-parse", "--short", "HEAD")
    if head is None:
        raise Refused(f"broad-gate: {root} has no HEAD to seal — nothing ran")
    base = git(root, "rev-parse", "--short", f"{args.base}^{{commit}}")
    if base is None:
        raise Refused(
            f"broad-gate: --base {args.base} does not resolve in {root} — nothing "
            "ran. A base that cannot be checked out is a base nothing can be "
            "compared against"
        )
    tree, base = head.strip(), base.strip()
    item = None
    if args.record:
        item = os.path.abspath(args.record)
        if not os.path.isdir(item):
            raise Refused(f"broad-gate: --record {args.record} is not a directory")
    # `stamp` refuses a scale outside the band with a sentence; asked before
    # anything runs, so a refused scale is exit 2 with nothing spent.
    refused = stamp.check_scale(args.scale)
    if refused:
        raise Refused(f"broad-gate: {refused}")

    keep = args.keep_output or tempfile.mkdtemp(prefix="broad-gate-")
    os.makedirs(keep, exist_ok=True)
    py = sys.executable
    specs = os.path.join(home, SPECS)
    checks = {}
    checks[SUITE] = run(SUITE, command, root, keep, shell=True)
    checks[LEDGER] = run(LEDGER, [py, EVIDENCE, "--strict", root], root, keep)
    checks[UNVERIFIED_NAME] = run(
        UNVERIFIED_NAME,
        [py, UNVERIFIED, "--baseline", args.base, specs],
        root,
        keep,
    )
    checks[CHAIN_NAME] = run(
        CHAIN_NAME,
        [py, CHAIN, "--baseline", args.base, "--root", root],
        root,
        keep,
        env=draft_env(keep),
    )
    survivor_args = [py, SURVIVOR, "--range", f"{args.base}...HEAD", "--root", root]
    for path in exemptions(home):
        survivor_args += ["--exempt", path]
    checks[SURVIVORS_NAME] = run(SURVIVORS_NAME, survivor_args, root, keep)

    failures = []
    for name, check in checks.items():
        if not check.failed:
            continue
        verdicts = None
        if name == SUITE:
            files = failing_files(check.text)
            if files:
                verdicts = compare_at_base(root, args.base, command, files, keep)
        failures.append((name, failure_lines(check, verdicts)))
    sys.stderr.write(f"broad-gate: outputs kept under {keep}\n")
    if failures:
        sys.stdout.write("\n".join(stamp.not_sealed(tree, base, failures)) + "\n")
        return 1

    if item is not None:
        code, text = seal_record(item, tree, args.base, root, args.base, keep)
        sys.stdout.write(text)
        if code != 0:
            # `seal` exits 2 on a refusal raised BEFORE the write, and it
            # returns whatever `chain_check` returned — 1 for errors — from
            # AFTER it. Only the first of those means no cell was written,
            # and neither of them is a seal. Reading `== 2` let the second
            # fall through to the drawing and to `return 0`.
            sys.stderr.write(
                f"broad-gate: every check passed and `round_record.py seal` "
                f"exited {code}, so nothing is sealed. A `round-record:` line "
                "above is a refusal and no cell was written; anything else is "
                "the chain check `seal` runs after the write, and the cell may "
                "be written over a record that check still fails\n"
            )
            return 2
    shape = args.shape or console_wants_letters
    rows = panel(tree, base, checks, item)
    sys.stdout.write("\n" + "\n".join(stamp.stamp(rows, args.scale, shape)) + "\n\n")
    return 0


def main(argv=None, console_wants_letters=None):
    """`console_wants_letters` is `pick_shape` asked of stdout as the process
    found it — `__main__` asks before it reconfigures the streams."""
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
    parser.add_argument("--scale", type=float, default=1.0, help="the chart's scale")
    parser.add_argument(
        "--keep-output",
        default=None,
        metavar="DIR",
        help="where each check's output is kept (default: a temp dir)",
    )
    args = parser.parse_args(argv)
    if console_wants_letters is None:
        stamp = load(STAMP, "specseal_seal_stamp_for_broad_gate")
        console_wants_letters = stamp.pick_shape(sys.stdout)
    try:
        return gate(args, console_wants_letters)
    except Refused as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2


if __name__ == "__main__":
    # Which form, asked of stdout as the process found it — before the loop
    # below moves every stream to UTF-8 (`seal_stamp.py` measured why).
    try:
        _letters = load(STAMP, "specseal_seal_stamp_for_broad_gate").pick_shape(
            sys.stdout
        )
    except Refused as _exc:
        sys.stderr.write(str(_exc) + "\n")
        sys.exit(2)
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main(console_wants_letters=_letters))
