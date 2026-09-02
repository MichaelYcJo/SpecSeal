"""The old roots move into `seal/` at session start, once per repository.

`.specseal/` and `specs/<id>/` became `seal/` in 0.4.0, and the opt-in became
the root's presence. Nothing reads the old names after that except the hook
under test, so a repository still holding them gets silence from every gate
until it runs — the fail direction the design record keeps on purpose. The
same grounds that let `hooks/ledger-migrate.py` write to a tree unasked
apply: the tree is the plugin's own, every step is a staged `git mv` or a
rewrite of a tracked file, and the diff is the review.

Every case here is about a boundary from the spec's table of what the session
prints and what it refuses (S5 to S9): never over uncommitted work, once per
repository, a stopped move resumed, rows that cite a moved file following it
with their hashes untouched, a throwaway repository left alone, and silence
when there is nothing to do.
"""

import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys

import pytest
from conftest import load_hook_module

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EC = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")

SERVICE = "def handler(x):\n    return x + 1\n\n\ndef other():\n    return 0\n"
ROUND = (
    "# round 1\n\n| Field | Value |\n|---|---|\n| Target SHA | abc |\n\n- [x] Pass\n"
)
ROUTING = "# routing\n\n| Axis | Answer |\n|---|---|\n| Review | straight to the PR |\n"
FOLLOW_UP = "# Follow-up\n\nnothing scheduled\n"
OLD_README = "# .specseal/ — the old text, describing a layout that is gone\n"
ITEM = "1788000000-a-work-item"


def load_checker():
    spec = importlib.util.spec_from_file_location("specseal_evidence_for_root", EC)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    return ec


def coordinate(repo, path, locator):
    """`path#locator@hash` at the content the file holds right now."""
    ec = load_checker()
    body = (repo / path).read_text(encoding="utf-8")
    places = ec.resolve(path, locator, body)
    assert len(places) == 1, f"fixture anchor is not unique: {places}"
    a, b = places[0]
    return f"{path}#{locator}@{ec.content_hash(body.splitlines()[a - 1 : b])}"


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


@pytest.fixture
def hook(tmp_path):
    mod = load_hook_module("root-migrate.py", "root_migrate")
    mod.STATE_DIR = str(tmp_path / "state")
    mod.MARKER = os.path.join(mod.STATE_DIR, "root-migrated")
    return mod


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def repo(tmp_path):
    """The old layout, committed: a ledger and a fragment under `.specseal/`,
    one work item and one foreign directory under `specs/`, and three ledger
    rows citing a file that moves."""
    d = tmp_path / "proj"
    d.mkdir()
    git(d, "init", "-q", "-b", "main")
    git(d, "config", "user.email", "t@example.com")
    git(d, "config", "user.name", "t")
    write(d, "src/service.py", SERVICE)
    write(d, ".specseal/README.md", OLD_README)
    write(d, ".specseal/follow-up.md", FOLLOW_UP)
    write(d, f"specs/{ITEM}/routing.md", ROUTING)
    write(d, f"specs/{ITEM}/rounds/round-1.md", ROUND)
    write(d, "specs/notes/todo.md", "# not SpecSeal's\n")
    rows = [
        coordinate(d, "src/service.py", "handler"),
        coordinate(d, f"specs/{ITEM}/rounds/round-1.md", '"# round 1"'),
        coordinate(d, ".specseal/follow-up.md", '"# Follow-up"'),
    ]
    write(
        d,
        ".specseal/map.md",
        "# map\n\n| Clause | Coordinate |\n|---|---|\n"
        + "".join(f"| {n} | `{c}` |\n" for n, c in zip("ABC", rows, strict=True)),
    )
    write(
        d,
        f".specseal/map/{ITEM}.md",
        f"# {ITEM}\n\n| Clause | Coordinate |\n|---|---|\n"
        f"| D | `{coordinate(d, f'specs/{ITEM}/routing.md', '"# routing"')}` |\n",
    )
    git(d, "add", "-A")
    git(d, "commit", "-qm", "the old layout, committed")
    return d


def start(hook, repo):
    """One session start; returns what the hook printed."""
    out = io.StringIO()
    stdin, stdout = sys.stdin, sys.stdout
    sys.stdin = io.StringIO(json.dumps({"cwd": str(repo)}))
    sys.stdout = out
    try:
        hook.main()
    finally:
        sys.stdin, sys.stdout = stdin, stdout
    return out.getvalue()


def message(out):
    return json.loads(out)["systemMessage"] if out.strip() else ""


def check(repo, *ledgers):
    """The checker's `total:` line, on the given ledgers or its defaults."""
    args = [a for led in ledgers for a in ("--ledger", led)]
    r = subprocess.run(
        [sys.executable, EC, *args, "."],
        cwd=str(repo),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    totals = [line for line in r.stdout.splitlines() if line.startswith("total:")]
    assert totals, r.stdout + r.stderr
    return totals[0]


def stamped(hook, repo):
    try:
        with open(hook.MARKER, encoding="utf-8") as f:
            return str(repo) in f.read().splitlines()
    except OSError:
        return False


# --- S5: the first session start moves, once ---------------------------------


def test_the_first_session_start_moves_the_tree_and_says_so_in_one_line(hook, repo):
    out = message(start(hook, repo))
    assert "moved .specseal/ and 1 work item into seal/" in out, out
    assert "review the diff and commit" in out, out
    for rel in (
        "seal/README.md",
        "seal/ledger.md",
        f"seal/ledger/{ITEM}.md",
        "seal/follow-up.md",
        f"seal/specs/{ITEM}/routing.md",
        f"seal/specs/{ITEM}/rounds/round-1.md",
    ):
        assert (repo / rel).is_file(), rel
    assert not (repo / ".specseal").exists(), "the old root was left behind"
    assert stamped(hook, repo)


def test_every_move_is_staged_and_history_follows_the_file(hook, repo):
    """`git mv`, not a rename on disk: `git diff --cached` shows the whole
    move, nothing is left unstaged for a person to find, and after the commit
    the notice asks for, `--follow` reaches the file's old name."""
    start(hook, repo)
    unstaged = git(repo, "diff", "--name-only").stdout.strip()
    assert unstaged == "", f"left unstaged:\n{unstaged}"
    staged = git(repo, "diff", "--cached", "--name-status", "-M").stdout
    assert (
        f"R100\tspecs/{ITEM}/rounds/round-1.md\tseal/specs/{ITEM}/rounds/round-1.md"
        in staged
    ), staged
    git(repo, "commit", "-qm", "the move, reviewed")
    # The round record, not the ledger: the ledger's rows were re-pointed in
    # the same commit, and on a four-row fixture that is more than half the
    # file, so git's rename detection cannot pair it. On a real ledger one
    # row in a hundred changes and `--follow` reaches it too; the fixture
    # pins the property on the file whose content did not move.
    log = git(
        repo,
        "log",
        "--follow",
        "--oneline",
        "--",
        f"seal/specs/{ITEM}/rounds/round-1.md",
    ).stdout
    assert "the old layout, committed" in log, log


def test_the_readme_is_rewritten_from_the_new_template(hook, repo):
    """Q5: the file is plugin-owned and its old text described a layout that
    no longer exists. The rewrite is staged with the move."""
    start(hook, repo)
    text = (repo / "seal" / "README.md").read_text(encoding="utf-8")
    assert text.startswith("# seal/"), text[:80]
    assert "the old text" not in text
    assert "seal/README.md" not in git(repo, "diff", "--name-only").stdout


def test_a_foreign_entry_under_specs_stays_and_is_named(hook, repo):
    """`specs/` stops being SpecSeal's directory, and a project may have had
    one before the plugin arrived. Only `<seconds>-<slug>` directories move."""
    out = message(start(hook, repo))
    assert (repo / "specs" / "notes" / "todo.md").is_file()
    assert not (repo / "seal" / "specs" / "notes").exists()
    assert "left specs/notes where it is" in out, out


def test_specs_goes_away_when_git_left_it_empty(hook, repo):
    git(repo, "rm", "-rq", "specs/notes")
    git(repo, "commit", "-qm", "only SpecSeal's work items under specs/")
    out = message(start(hook, repo))
    assert "left specs/" not in out, out
    assert not (repo / "specs").exists()


def test_the_second_session_start_is_silent(hook, repo):
    start(hook, repo)
    assert start(hook, repo) == "", "the second session start spoke"


def test_the_hook_does_not_wait_for_the_new_opt_in(hook, repo):
    """The old layout is exactly what does not opt in any more, so a hook
    gated on `optin.opted_in` would never meet what it moves."""
    optin = load_hook_module("optin.py", "optin_for_root")
    assert not optin.opted_in(str(repo)), "the fixture already opted in"
    assert "moved" in message(start(hook, repo))
    assert optin.opted_in(str(repo)), "the move did not produce the opt-in"


# --- S6: a dirty tree is refused ---------------------------------------------


def test_uncommitted_changes_under_the_old_roots_refuse_the_move(hook, repo):
    """Work in progress outranks the move. The refusal says why, stamps
    nothing — so the next clean session start moves — and touches nothing."""
    ledger = repo / ".specseal" / "map.md"
    ledger.write_text(ledger.read_text() + "| E | half a row |\n", encoding="utf-8")
    out = message(start(hook, repo))
    assert "uncommitted changes" in out and "Commit, then" in out, out
    assert (repo / ".specseal" / "map.md").is_file()
    assert not (repo / "seal").exists()
    assert not stamped(hook, repo)
    git(repo, "commit", "-qam", "the wip lands")
    assert "moved" in message(start(hook, repo))


def test_a_staged_edit_under_the_old_roots_is_work_in_progress_too(hook, repo):
    """`dirty()` looks past a staged rename or deletion with a clean worktree,
    because that is what its own stopped run leaves. A staged MODIFICATION is
    somebody's edit, and it still refuses."""
    ledger = repo / ".specseal" / "map.md"
    ledger.write_text(ledger.read_text() + "| E | half a row |\n", encoding="utf-8")
    git(repo, "add", "-A")
    assert "uncommitted changes" in message(start(hook, repo))
    assert not (repo / "seal").exists()


def test_an_untracked_file_under_a_work_item_is_work_in_progress(hook, repo):
    write(repo, f"specs/{ITEM}/overview.md", "# not yet added\n")
    assert "uncommitted changes" in message(start(hook, repo))
    assert not (repo / "seal").exists()


def test_a_git_that_cannot_answer_reads_as_dirty(hook, repo, monkeypatch):
    monkeypatch.setattr(
        hook.subprocess,
        "run",
        lambda *a, **k: (_ for _ in ()).throw(OSError("no git")),
    )
    assert hook.dirty(str(repo))


# --- S7: a stopped move resumes ----------------------------------------------


def test_a_move_by_hand_that_stopped_halfway_is_finished(hook, repo):
    """The state a person leaves after moving the ledger by hand and no
    more: `seal/` and `.specseal/` both exist. What remains moves, and the
    marker is stamped only then."""
    (repo / "seal").mkdir()
    git(repo, "mv", ".specseal/map.md", "seal/ledger.md")
    git(repo, "commit", "-qm", "half a move, by hand")
    out = message(start(hook, repo))
    assert "moved .specseal/ and 1 work item into seal/" in out, out
    assert (repo / "seal" / "ledger.md").is_file()
    assert (repo / "seal" / "ledger" / f"{ITEM}.md").is_file()
    assert not (repo / ".specseal").exists()
    assert stamped(hook, repo)


def test_a_step_that_fails_stops_the_run_and_stamps_nothing(hook, repo, monkeypatch):
    """The next session start continues from where it stopped, and stamps
    when nothing old is left."""
    real = hook.git_mv
    calls = []

    def flaky(root, src, dst):
        calls.append(src)
        if len(calls) == 3:
            raise hook.MoveError(src, "disk full")
        real(root, src, dst)

    monkeypatch.setattr(hook, "git_mv", flaky)
    out = message(start(hook, repo))
    assert "moved 2 of 5 into seal/ and stopped at" in out, out
    assert "disk full" in out and "The next session start continues" in out, out
    assert (repo / "seal" / "ledger.md").is_file()
    assert (repo / ".specseal").is_dir(), "the old root is still there to resume from"
    assert not stamped(hook, repo)

    monkeypatch.setattr(hook, "git_mv", real)
    out = message(start(hook, repo))
    assert "moved .specseal/ and 1 work item into seal/" in out, out
    assert not (repo / ".specseal").exists()
    assert stamped(hook, repo)


def test_a_directory_already_at_the_destination_is_merged_file_by_file(hook, repo):
    """`git mv dir existing-dir` puts the source INSIDE the destination. A
    resumed run meets exactly that state, so a directory is moved per file."""
    write(repo, "seal/ledger/another.md", "# another fragment\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "a fragment already at the new address")
    start(hook, repo)
    assert (repo / "seal" / "ledger" / f"{ITEM}.md").is_file()
    assert (repo / "seal" / "ledger" / "another.md").is_file()
    assert not (repo / "seal" / "ledger" / "map").exists(), "moved INTO the destination"


# --- S8: rows that cite a moved file follow it --------------------------------


def test_rows_citing_a_moved_file_are_re_pointed_with_their_hashes_untouched(
    hook, repo
):
    before = (repo / ".specseal" / "map.md").read_text(encoding="utf-8")
    totals_before = check(repo, ".specseal/map.md", ".specseal/map/*.md")
    out = message(start(hook, repo))
    assert "3 ledger rows re-pointed" in out, out
    after = (repo / "seal" / "ledger.md").read_text(encoding="utf-8")
    fragment = (repo / "seal" / "ledger" / f"{ITEM}.md").read_text(encoding="utf-8")
    assert f"`seal/specs/{ITEM}/rounds/round-1.md#" in after, after
    assert "`seal/follow-up.md#" in after, after
    assert f"`seal/specs/{ITEM}/routing.md#" in fragment, fragment
    assert "`src/service.py#handler@" in after, "a row under no moved prefix changed"
    hashes = lambda t: sorted(re.findall(r"@([0-9a-f]{6,12})`", t))
    assert hashes(before) == hashes(after) and len(hashes(after)) == 3
    totals_after = check(repo)
    assert totals_before == totals_after, f"{totals_before}\n{totals_after}"
    assert "0 broken" in totals_after and "0 drifted" in totals_after, totals_after


def test_the_re_pointed_ledgers_are_staged_with_the_move(hook, repo):
    start(hook, repo)
    assert git(repo, "diff", "--name-only").stdout.strip() == ""


# --- S9: a throwaway repository is not migrated ------------------------------


def test_a_repository_declaring_itself_throwaway_is_left_alone(hook, repo):
    write(repo, ".specseal/scratch", "")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "throwaway")
    out = message(start(hook, repo))
    assert "throwaway" in out and "Delete the file if it is not" in out, out
    assert (repo / ".specseal" / "map.md").is_file()
    assert not (repo / "seal").exists()
    assert not stamped(hook, repo)


# --- silence ------------------------------------------------------------------


def test_a_repository_with_nothing_old_says_nothing(hook, tmp_path):
    d = tmp_path / "fresh"
    d.mkdir()
    git(d, "init", "-q")
    assert start(hook, d) == ""
    assert not stamped(hook, d)


def test_a_moved_repository_is_stamped_so_an_old_branch_is_not_moved_again(hook, repo):
    """A branch cut before the move still carries the old layout. Once the
    root has been seen moved, the once-per-repository rule is already
    answered for it, and checking such a branch out later stages nothing."""
    start(hook, repo)
    git(repo, "commit", "-qm", "the move")
    git(repo, "switch", "-qc", "old", "HEAD~1")
    assert (repo / ".specseal").is_dir(), "the old branch carries the old layout"
    assert start(hook, repo) == ""
    assert (repo / ".specseal").is_dir()


def test_a_marker_already_carrying_the_root_keeps_the_hook_silent(hook, repo):
    """Q8 (a): the ledger hook's rule. A refused-then-never-committed
    repository is not re-nagged every morning; the silent gates are the
    backstop, and the CHANGELOG entry carries the by-hand sequence."""
    hook.stamp(str(repo))
    assert start(hook, repo) == ""
    assert (repo / ".specseal").is_dir()


def test_the_hook_is_wired_into_session_start_before_the_ledger_migration(hook):
    """The dispatch group is the only thing that runs hooks in production, and
    the ledger-format migration reads the ledgers at the addresses this one
    creates, so the order is part of the contract."""
    dispatch = load_hook_module("dispatch.py", "dispatch_for_root")
    group = dispatch.GROUPS["session-start"]
    assert "root-migrate.py" in group
    assert group.index("root-migrate.py") < group.index("ledger-migrate.py")


def test_the_hook_reads_the_old_names_and_nothing_else_does(hook):
    """S15's exception, pinned from the other side: this file is the one
    reader of `.specseal/` left in `hooks/`, and it carries a rider saying it
    can go once no repository is left to migrate."""
    src = open(os.path.join(ROOT, "hooks", "root-migrate.py"), encoding="utf-8").read()
    assert "# RIDER:" in src and ".specseal" in src
    for name in sorted(os.listdir(os.path.join(ROOT, "hooks"))):
        if name.endswith(".py") and name != "root-migrate.py":
            text = open(os.path.join(ROOT, "hooks", name), encoding="utf-8").read()
            assert ".specseal/map" not in text, f"{name} still reads the old ledger"


# --- round 1: what git does not track is not the hook's to move --------------


def test_an_ignored_file_directly_under_the_old_root_does_not_stop_the_move(hook, repo):
    """Round 1's 🔴 1. `.DS_Store` is macOS's default and it is usually
    ignored, so `dirty()` never saw it — and `git mv` refused it, so every
    session start stopped at the same unit and the tree stayed half-moved for
    good. The units are what git tracks; an ignored file is left where it is,
    and `.specseal/` may stay on disk holding nothing else."""
    write(repo, ".gitignore", ".DS_Store\n")
    git(repo, "add", ".gitignore")
    git(repo, "commit", "-qm", "ignore the finder's file")
    write(repo, ".specseal/.DS_Store", "\0")
    out = message(start(hook, repo))
    assert "moved .specseal/ and 1 work item into seal/" in out, out
    assert (repo / "seal" / "specs" / ITEM / "routing.md").is_file()
    assert stamped(hook, repo)
    assert git(repo, "ls-files", "--", ".specseal", f"specs/{ITEM}").stdout == ""
    assert os.listdir(repo / ".specseal") == [".DS_Store"]
    assert start(hook, repo) == "", "nothing tracked is left, so nothing to say"


def test_a_file_named_seal_stops_with_a_line_not_an_exception(hook, repo):
    """Round 1's 🟡 2. `os.makedirs` sat outside `git_mv`'s try, so a
    committed file named `seal` raised out of `main()`; under the dispatcher
    that is silence at every session start."""
    write(repo, "seal", "not a directory\n")
    git(repo, "add", "seal")
    git(repo, "commit", "-qm", "a file in the way")
    out = message(start(hook, repo))
    assert "stopped at .specseal/map.md" in out and "seal" in out, out
    assert "by hand" in out, out
    assert (repo / ".specseal" / "map.md").is_file()
    assert not stamped(hook, repo)


def test_a_destination_already_holding_the_file_is_named_and_left_to_the_person(
    hook, repo
):
    """Round 1's 🟡 3. A branch bootstrapped on the new layout merged into
    one still on the old leaves `seal/ledger.md` beside `.specseal/map.md`.
    `git mv` failed with `destination exists` and the line promised a
    continuation that never came; the person has to keep one."""
    write(repo, "seal/ledger.md", "# the newer ledger\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "both ledgers")
    out = message(start(hook, repo))
    assert "seal/ledger.md already exists" in out, out
    assert "keep one by hand" in out and "git rm .specseal/map.md" in out, out
    assert not out.endswith("The next session start continues."), out
    assert not stamped(hook, repo)
    assert (repo / ".specseal" / "map.md").is_file()


def test_a_row_citing_a_foreign_specs_entry_is_left_where_it_is(hook, repo):
    """Round 1's 🟡 4. `specs/notes/` is not a work item and stays; a row
    citing it has to stay with it, or S8's equal totals break."""
    ledger = repo / ".specseal" / "map.md"
    row = coordinate(repo, "specs/notes/todo.md", '"# not SpecSeal\'s"')
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + f"| D | `{row}` |\n", encoding="utf-8"
    )
    git(repo, "commit", "-qam", "a row citing a foreign entry")
    before = check(repo, ".specseal/map.md", ".specseal/map/*.md")
    out = message(start(hook, repo))
    assert "3 ledger rows re-pointed" in out, out
    after = (repo / "seal" / "ledger.md").read_text(encoding="utf-8")
    assert "`specs/notes/todo.md#" in after and "seal/specs/notes" not in after, after
    assert check(repo) == before


def test_a_repoint_that_fails_after_the_moves_says_so_and_stamps_nothing(
    hook, repo, monkeypatch
):
    """Round 1's 🟡 2, second half. An `OSError` out of `repoint()` used to
    escape `main()` after every unit had moved, and the next start stamped
    over rows still pointing at the old paths."""

    def failing(root):
        raise OSError("read-only ledger")

    monkeypatch.setattr(hook, "repoint", failing)
    out = message(start(hook, repo))
    assert "could not re-point the ledger" in out and "read-only ledger" in out, out
    assert "evidence-check --reverify ." in out, out
    assert (repo / "seal" / "ledger.md").is_file()
    assert not (repo / ".specseal").exists()
    assert not stamped(hook, repo)


HEADINGS = {"README.md": "### Coming up from 0.3.x", "README.ko.md": "### 0.3.x"}


def by_hand_block(readme):
    """The `bash` block under the README's coming-up section, comments off."""
    text = open(os.path.join(ROOT, readme), encoding="utf-8").read()
    section = text.split(HEADINGS[readme], 1)[1]
    block = section.split("```bash\n", 1)[1].split("```", 1)[0]
    return [ln.split("#", 1)[0].strip() for ln in block.splitlines() if ln.strip()]


@pytest.mark.parametrize("readme", ["README.md", "README.ko.md"])
def test_the_readmes_by_hand_sequence_yields_the_hooks_tracked_set(
    hook, repo, tmp_path, readme
):
    """Round 1's P6, pinned to the document: the block a person copies is
    read out of the README and run line by line on a copy of the fixture, and
    `git ls-files` has to agree with the hook's. `--reverify` is what closes
    the rows the hand sequence leaves broken."""
    hand = tmp_path / "hand"
    shutil.copytree(repo, hand)
    start(hook, repo)
    for line in by_hand_block(readme):
        line = line.replace("<id>", ITEM)
        line = line.replace("evidence-check ", f"{sys.executable} {EC} ")
        subprocess.run(line, shell=True, cwd=str(hand), capture_output=True)
    tracked = lambda d: git(d, "ls-files").stdout.split()
    assert tracked(hand) == tracked(repo), tracked(hand)
    totals = check(hand)
    assert "0 broken" in totals, totals
