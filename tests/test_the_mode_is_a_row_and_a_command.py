"""`seal mode`: a declared row, a folder that decides, and a switch between
them that does what a `mv` cannot.

Issue #104. Switching between shared and local mode worked only as two shell
lines in `README.md`'s *Shared or local* section, and a repository arriving
from the 0.3.x layout landed in shared without ever being asked. The work
item is `seal/specs/1788411058-the-mode-is-two-shell-lines-in-a-readme/`, and
the scenario ids in the case names are its `spec.md`'s.

Three properties shape the cases, because each fails quietly if it fails:

**The row is declared state and the folder is observed state.** Nothing at
runtime reads the row — every hook resolves the root through
`hooks/optin.py#home_at` — so the cases assert what the FOLDER is after a
switch and never take the row's word for it.

**A refusal that refuses and moves something anyway passes a test that reads
only the exit code.** Every refusal case compares a snapshot of both root
paths and `git status --porcelain` from before the run.

**The workflow file is the half a `mv` leaves behind, and leaving it is not
tidiness.** Measured 2026-09-03 in a repository with no `seal/`:
`unverified_check.py` exits 2 for a path that is nowhere and `chain_check.py`
exits 0 having examined nothing — a build that is red forever beside a check
reporting a pass it never earned. So the carrying cases are here rather than
left to a reader's confidence.
"""

import importlib.util
import json
import os
import shutil
import subprocess

import pytest
from conftest import local_home, symlink_or_skip

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "implement", "scripts", "seal.py")
WORKFLOW = os.path.join(".github", "workflows", "hygiene.yml")


@pytest.fixture
def seal():
    spec = importlib.util.spec_from_file_location("specseal_seal_mode", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(repo, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def porcelain(repo):
    return sorted(git(repo, "status", "--porcelain").stdout.splitlines())


def files_under(path):
    if not os.path.isdir(path):
        return None
    out = []
    for dirpath, _dirnames, filenames in os.walk(path):
        for name in filenames:
            full = os.path.join(dirpath, name)
            out.append(os.path.relpath(full, path).replace(os.sep, "/"))
    return sorted(out)


def places(seal, repo):
    """(shared path, local path) for this repository, asked the way the
    command asks — never spelled here, or the tests would hold a second
    answer to the question `hooks/optin.py` exists to have one of."""
    _repo, _home, shared, local, _mode = seal.resolve(str(repo))
    return shared, local


def state(seal, repo):
    """Everything a refusal must leave exactly as it was."""
    shared, local = places(seal, repo)
    return {
        "shared": files_under(shared),
        "local": files_under(local),
        "porcelain": porcelain(repo),
        "workflow": os.path.exists(os.path.join(str(repo), WORKFLOW)),
    }


def records(home):
    """A root holding a ledger and one work item."""
    home = str(home)
    os.makedirs(os.path.join(home, "specs", "1788000000-a-work-item"), exist_ok=True)
    os.makedirs(os.path.join(home, "ledger"), exist_ok=True)
    with open(os.path.join(home, "ledger.md"), "w", encoding="utf-8") as handle:
        handle.write("# the ledger\n")
    with open(
        os.path.join(home, "specs", "1788000000-a-work-item", "routing.md"),
        "w",
        encoding="utf-8",
    ) as handle:
        handle.write("# routing\n")
    return home


@pytest.fixture
def shared_repo(repo):
    """A shared-mode repository whose root is committed."""
    records(os.path.join(str(repo), "seal"))
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "the root")
    return repo


@pytest.fixture
def local_repo(repo):
    """A local-mode repository: the root under the common git directory."""
    records(local_home(repo))
    return repo


def run(seal, argv, cwd, capsys):
    code = seal.main(argv, cwd=str(cwd))
    return code, capsys.readouterr().out


def config_of(seal, repo):
    """The `Mode` row as the command reads it: (kind, value)."""
    _repo, home, _shared, _local, _mode = seal.resolve(str(repo))
    return seal.declared(home)


def write_config(seal, repo, body):
    _repo, home, _shared, _local, _mode = seal.resolve(str(repo))
    with open(os.path.join(home, "config.md"), "w", encoding="utf-8") as handle:
        handle.write(body)


def row(value):
    return f"| Item | Value |\n|---|---|\n| Mode | {value} |\n"


# --- S1, S2: the report, and the row it fills in ---------------------------


@pytest.mark.parametrize("mode", ["shared", "local"])
def test_the_report_names_the_folder_the_row_and_whether_they_agree(
    mode, request, seal, capsys
):
    """S1. Three facts, and the command exists because none of them was
    visible anywhere."""
    repo = request.getfixturevalue(f"{mode}_repo")
    write_config(seal, repo, row(mode))
    before = state(seal, repo)

    code, out = run(seal, ["mode"], repo, capsys)

    assert code == 0, out
    assert "folder:" in out and "row:" in out
    assert out.count(mode) >= 2, out
    assert "They agree." in out
    assert state(seal, repo) == before, "a report moved something"


# The four ways of not declaring a mode. The same four the pull-request
# language row has for not naming a language, and they are one state.
UNDECLARED = [
    ("no file at all", None),
    ("a file with no such row", "| Item | Value |\n|---|---|\n| Other | x |\n"),
    ("an empty value", "| Item | Value |\n|---|---|\n| Mode |  |\n"),
    ("a file that is not that table", "# notes\n\nnothing here.\n"),
]


@pytest.mark.parametrize("what, body", UNDECLARED, ids=[w for w, _ in UNDECLARED])
@pytest.mark.parametrize("mode", ["shared", "local"])
def test_an_absent_row_is_written_from_where_the_folder_is(
    mode, what, body, request, seal, capsys
):
    """S2, and the half that matters: the value written is the FOLDER's.

    Every repository that has a `config.md` today has one row in it, the
    pull-request language, so "the row is absent" is the state of every
    existing repository on the day this ships. A fixed default of `shared`
    would write a lie into every undeclared local-mode repository — which is
    the exact document the check exists to catch, produced by the command
    that reports it. Running this in both modes is what tells the two apart;
    one mode alone passes for either implementation.
    """
    repo = request.getfixturevalue(f"{mode}_repo")
    if body is not None:
        write_config(seal, repo, body)

    code, out = run(seal, ["mode"], repo, capsys)

    assert code == 0, out
    assert "was written from where the folder is" in out, what
    assert config_of(seal, repo) == ("mode", mode), what
    assert "They agree." in out


def test_a_second_report_writes_nothing_more(local_repo, seal, capsys):
    """S2b. The write happens once, because after it the row is declared."""
    run(seal, ["mode"], local_repo, capsys)
    _repo, home, _s, _l, _m = seal.resolve(str(local_repo))
    path = os.path.join(home, "config.md")
    with open(path, "rb") as handle:
        first = handle.read()

    code, out = run(seal, ["mode"], local_repo, capsys)

    assert code == 0
    with open(path, "rb") as handle:
        assert handle.read() == first, "the second run rewrote the file"
    assert "was written from where the folder is" not in out


def test_an_existing_row_keeps_the_rest_of_the_file(local_repo, seal, capsys):
    """The row is one line of a person's file. `seal mode shared` in a
    local-mode repository is refused elsewhere; here the row is corrected by
    the report path, so the surrounding prose has to survive it."""
    write_config(
        seal,
        local_repo,
        "# Repository config\n\nSome prose nobody may lose.\n\n"
        "| Item | Value |\n|---|---|\n"
        "| Pull request language | Korean |\n| Mode | shared |\n\n"
        "## Trailing section\n\nMore prose.\n",
    )
    _repo, home, _s, _l, _m = seal.resolve(str(local_repo))
    path = os.path.join(home, "config.md")

    code, out = run(seal, ["mode", "local"], local_repo, capsys)

    assert code == 0, out
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    assert "Some prose nobody may lose." in text
    assert "| Pull request language | Korean |" in text
    assert "## Trailing section" in text
    assert "| Mode | local |" in text
    assert "| Mode | shared |" not in text


@pytest.mark.parametrize("shape", ["a directory", "a symbolic link"])
def test_a_row_that_cannot_be_written_still_reports(shape, local_repo, seal, capsys):
    """S2c. A person asked where things stand, and that answer does not need
    the write. Failing the report would make an unwritable config a reason
    not to answer a question."""
    _repo, home, _s, _l, _m = seal.resolve(str(local_repo))
    path = os.path.join(home, "config.md")
    if shape == "a directory":
        os.mkdir(path)
    else:
        symlink_or_skip(os.path.join(home, "nowhere.md"), path)

    code, out = run(seal, ["mode"], local_repo, capsys)

    assert code == 0, out
    assert "could not be written" in out, out
    assert "folder:" in out and "local" in out


def test_check_writes_nothing_even_when_the_row_is_absent(local_repo, seal, capsys):
    """S2d. `--check` runs in CI, and a check that mutates the tree it checks
    is not a check."""
    _repo, home, _s, _l, _m = seal.resolve(str(local_repo))
    path = os.path.join(home, "config.md")
    assert not os.path.exists(path)

    code, out = run(seal, ["mode", "--check"], local_repo, capsys)

    assert code == 0, out
    assert not os.path.exists(path), "--check wrote the row"
    assert "not declared" in out


# --- S3, S4, S5: what the check answers ------------------------------------


@pytest.mark.parametrize("mode", ["shared", "local"])
def test_check_passes_when_the_row_names_the_folders_mode(mode, request, seal, capsys):
    """S3."""
    repo = request.getfixturevalue(f"{mode}_repo")
    write_config(seal, repo, row(mode))
    assert run(seal, ["mode", "--check"], repo, capsys)[0] == 0


@pytest.mark.parametrize("mode, other", [("shared", "local"), ("local", "shared")])
def test_check_fails_and_names_both_ways_out(mode, other, request, seal, capsys):
    """S4. A disagreement is always the author's and always one command from
    fixed, which is what puts it on the failing side of this repository's own
    rule for a red build. So the message has to carry BOTH commands: moving
    the folder and correcting the row are different intentions."""
    repo = request.getfixturevalue(f"{mode}_repo")
    write_config(seal, repo, row(other))

    code, out = run(seal, ["mode", "--check"], repo, capsys)

    assert code == 1, out
    assert "disagree" in out
    assert "seal mode --apply" in out, "the way to move the folder is missing"
    assert f"seal mode {mode}" in out, "the way to correct the row is missing"


def test_a_value_that_is_not_a_mode_is_a_claim_nobody_can_act_on(
    shared_repo, seal, capsys
):
    """S5. Three ways of not declaring pass; a row that declares something
    unusable does not. It is not the same state, and treating it as "absent"
    would silently overwrite whatever the person meant."""
    write_config(seal, shared_repo, row("remote"))
    before = state(seal, shared_repo)

    assert run(seal, ["mode", "--check"], shared_repo, capsys)[0] == 1
    code, out = run(seal, ["mode", "--apply"], shared_repo, capsys)
    assert code == 1
    assert "remote" in out and "not a mode" in out
    assert state(seal, shared_repo) == before

    _code, out = run(seal, ["mode"], shared_repo, capsys)
    assert "not a mode" in out
    assert config_of(seal, shared_repo) == ("unknown", "remote"), (
        "the report overwrote a row it could not read"
    )


# --- S6, S7: no root at either place ---------------------------------------


def test_check_passes_where_there_is_no_root(repo, seal, capsys):
    """S6. A check that fails where there is nothing to check teaches people
    to delete the check. A workflow that outlived its root already goes red
    on `unverified_check.py`, which exits 2 for a path that is nowhere."""
    code, out = run(seal, ["mode", "--check"], repo, capsys)
    assert code == 0, out
    assert "nothing is declared" in out


@pytest.mark.parametrize(
    "argv", [["mode"], ["mode", "local"], ["mode", "shared"], ["mode", "--apply"]]
)
def test_everything_else_refuses_where_there_is_no_root(argv, repo, seal, capsys):
    """S7. Both places are named, because a person who sees this has to know
    which two."""
    code, out = run(seal, argv, repo, capsys)
    assert code == 1, out
    assert "shared mode" in out and "local mode" in out


# --- S8 to S11: the switch --------------------------------------------------


def test_shared_to_local_moves_stages_and_writes_the_row(shared_repo, seal, capsys):
    """S8. The three acts of the direction, asserted separately: a switch
    that moves the folder and forgets the index leaves the records committed,
    which is the state local mode exists to avoid."""
    shared, local = places(seal, shared_repo)

    code, out = run(seal, ["mode", "local"], shared_repo, capsys)

    assert code == 0, out
    assert not os.path.exists(shared), "the tree still holds the root"
    assert os.path.isfile(os.path.join(local, "ledger.md"))
    assert all(line.startswith("D ") for line in porcelain(shared_repo)), porcelain(
        shared_repo
    )
    assert config_of(seal, shared_repo) == ("mode", "local")


def test_local_to_shared_moves_stages_and_writes_the_row(local_repo, seal, capsys):
    """S9."""
    shared, local = places(seal, local_repo)

    code, out = run(seal, ["mode", "shared"], local_repo, capsys)

    assert code == 0, out
    assert not os.path.exists(local), "the local root was copied, not moved"
    assert os.path.isfile(os.path.join(shared, "ledger.md"))
    assert any("seal/ledger.md" in line for line in porcelain(local_repo))
    assert config_of(seal, local_repo) == ("mode", "shared")


def test_a_stopped_run_is_finished_by_a_second(shared_repo, seal, capsys):
    """S10. The rename runs first and every step after it is idempotent, so a
    run that stopped — or a person who ran the README's `mv` by hand — is
    finished rather than refused. The half state this reproduces is exactly
    what the by-hand `mv` leaves: the folder moved, the index untouched."""
    shared, local = places(seal, shared_repo)
    os.rename(shared, local)
    assert any("seal/ledger.md" in line for line in porcelain(shared_repo))

    code, out = run(seal, ["mode", "local"], shared_repo, capsys)

    assert code == 0, out
    assert "already the root" in out
    assert all(line.startswith("D ") for line in porcelain(shared_repo))
    assert config_of(seal, shared_repo) == ("mode", "local")


@pytest.mark.parametrize("mode, other", [("shared", "local"), ("local", "shared")])
def test_apply_moves_the_folder_to_what_the_row_says(
    mode, other, request, seal, capsys
):
    """S11. The flow the issue describes: edit the row, run the command."""
    repo = request.getfixturevalue(f"{mode}_repo")
    write_config(seal, repo, row(other))
    shared, local = places(seal, repo)

    code, out = run(seal, ["mode", "--apply"], repo, capsys)

    assert code == 0, out
    landed = local if other == "local" else shared
    left = shared if other == "local" else local
    assert os.path.isfile(os.path.join(landed, "ledger.md"))
    assert not os.path.exists(left)


def test_apply_with_no_row_says_what_to_write(local_repo, seal, capsys):
    """`--apply` is a person acting on a row they wrote. With none there is
    nothing to act on, and guessing would move a folder on no instruction."""
    before = state(seal, local_repo)
    code, out = run(seal, ["mode", "--apply"], local_repo, capsys)
    assert code == 1
    assert "not declared" in out and "| Mode |" in out
    assert state(seal, local_repo) == before


def test_two_spellings_of_the_answer_are_refused_together(local_repo, seal):
    """A mode, `--check` and `--apply` are three spellings of one answer.
    Any two is a question with two answers, and this command moves
    directories — so it is refused rather than resolved by precedence."""
    with pytest.raises(SystemExit) as exit_code:
        seal.main(["mode", "local", "--apply"], cwd=str(local_repo))
    assert exit_code.value.code == 2


# --- S12, S13: what a person is told before it acts -------------------------


def test_going_to_shared_says_the_commit_is_the_door(local_repo, seal, capsys):
    """S12. local → shared is the one direction that cannot be walked back,
    and the direction local mode exists to prevent. The point of no return is
    the COMMIT, not the move — the command stages precisely so that moment
    stays the person's — so the line has to say that, and say it above the
    line that tells them to commit."""
    code, out = run(seal, ["mode", "shared"], local_repo, capsys)

    assert code == 0
    assert "history" in out
    assert out.index("history") < out.index("Now commit"), (
        "the consequence arrives after the instruction to commit"
    )
    assert "seal mode local" in out, "the way back before the commit is not named"


def test_going_to_local_names_the_pair_that_carries_a_copy(shared_repo, seal, capsys):
    """S13. Every other clone loses the records at the next pull, and a
    person reading only this section will not connect that to `seal export`
    unless it is named here."""
    _code, out = run(seal, ["mode", "local"], shared_repo, capsys)
    assert "seal export" in out and "seal import" in out


# --- S14 to S20: refusing ---------------------------------------------------


@pytest.mark.parametrize("argv", [["mode", "local"], ["mode", "shared"]])
def test_both_roots_existing_refuses(argv, shared_repo, seal, capsys):
    """S14. A clone holding two roots is one whose owner has not said which
    is real, and a switch is not the moment to decide it. The same refusal
    `destination_root` makes for `seal import`."""
    _shared, local = places(seal, shared_repo)
    records(local)
    before = state(seal, shared_repo)

    code, out = run(seal, argv, shared_repo, capsys)

    assert code == 1, out
    assert "both roots exist" in out
    assert state(seal, shared_repo) == before


INDEXED = [
    ("a worktree modification", "modify"),
    ("a staged edit", "stage"),
    ("a staged deletion", "delete"),
]


@pytest.mark.parametrize("what, how", INDEXED, ids=[w for w, _ in INDEXED])
def test_a_change_the_index_carries_refuses(what, how, shared_repo, seal, capsys):
    """S15. `git rm -r --cached` takes a staged edit out of the index and
    prints nothing about it (measured 2026-09-03, all four tree states), so a
    half-staged move is worse than none."""
    ledger = os.path.join(str(shared_repo), "seal", "ledger.md")
    if how == "delete":
        git(shared_repo, "rm", "--quiet", "--", "seal/ledger.md")
    else:
        with open(ledger, "w", encoding="utf-8") as handle:
            handle.write("# changed\n")
        if how == "stage":
            git(shared_repo, "add", "--", "seal/ledger.md")
    before = state(seal, shared_repo)

    code, out = run(seal, ["mode", "local"], shared_repo, capsys)

    assert code == 1, out
    assert "not clean" in out
    assert state(seal, shared_repo) == before, "a refusal moved something"


@pytest.mark.parametrize("mode", ["shared", "local"])
def test_an_untracked_file_travels_with_the_folder(mode, request, seal, capsys):
    """S15b. The index cannot lose what it never had, and the file moves with
    the folder either way.

    Refusing over one was not a stricter version of the guard above, it was a
    different guard with no grounds — and it made the ordinary first run
    refuse, because the bare command writes an absent row and the switch a
    person runs next met the file it had just written. Found by running it.
    """
    repo = request.getfixturevalue(f"{mode}_repo")
    _repo, home, shared, local = seal.resolve(str(repo))[:4]
    with open(os.path.join(home, "untracked.md"), "w", encoding="utf-8") as handle:
        handle.write("# a draft\n")
    other = local if mode == "shared" else shared

    code, out = run(
        seal, ["mode", "local" if mode == "shared" else "shared"], repo, capsys
    )

    assert code == 0, out
    assert os.path.isfile(os.path.join(other, "untracked.md"))
    if mode == "shared":
        # Only the shared side has an index to report against: in local mode
        # the root is not in the working tree at all, so `git status` has
        # nothing to say about a file under it and the note has nothing to
        # name. The travel is what both directions share.
        assert "untracked" in out, "the file travelled without being named"


DESTINATIONS = ["a file", "a symbolic link", "a broken symbolic link"]


@pytest.mark.parametrize("shape", DESTINATIONS)
def test_a_destination_that_already_exists_refuses(shape, shared_repo, seal, capsys):
    """S16. `lexists`, not `exists`: a link to nothing reads as absent to the
    second, and `os.rename` onto one replaces the link — which is the defect
    `write_zip` and `place` were both fixed for."""
    _shared, local = places(seal, shared_repo)
    if shape == "a file":
        with open(local, "w", encoding="utf-8") as handle:
            handle.write("not a root\n")
    else:
        target = os.path.join(str(shared_repo), "elsewhere")
        if shape == "a symbolic link":
            os.mkdir(target)
        symlink_or_skip(target, local)
    before = state(seal, shared_repo)

    code, out = run(seal, ["mode", "local"], shared_repo, capsys)

    assert code == 1, out
    assert "already exists" in out or "both roots" in out
    assert state(seal, shared_repo) == before
    assert os.path.lexists(local), "the refusal removed what was there"


def test_a_source_that_is_a_symbolic_link_refuses(local_repo, seal, capsys):
    """S17. `hooks/root-migrate.py` refuses a linked `.specseal/` rather than
    half-moving it, for the same reason: moving the link moves one entry and
    leaves every record where it was."""
    _repo, home, shared, local, _mode = seal.resolve(str(local_repo))
    real = os.path.join(str(local_repo), "elsewhere")
    shutil.move(local, real)
    symlink_or_skip(real, local)
    before = state(seal, local_repo)

    code, out = run(seal, ["mode", "shared"], local_repo, capsys)

    assert code == 1, out
    assert "symbolic link" in out
    assert state(seal, local_repo) == before
    assert not os.path.exists(shared)


def test_a_dirty_workflow_path_refuses(shared_repo, seal, capsys):
    """S18, and the enumeration this command is built on: the switch stages
    the workflow file too, so a guard watching only the root would leave that
    path's uncommitted work to be taken by `git rm`. #81 closed "a path this
    command writes through" three times, one name apart each time."""
    path = os.path.join(str(shared_repo), WORKFLOW)
    os.makedirs(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("name: hygiene\n")
    git(shared_repo, "add", "-A")
    git(shared_repo, "commit", "-qm", "a workflow")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("name: hygiene\n# edited\n")
    before = state(seal, shared_repo)

    code, out = run(seal, ["mode", "local"], shared_repo, capsys)

    assert code == 1, out
    assert "not clean" in out and "hygiene.yml" in out
    assert state(seal, shared_repo) == before


def test_a_rename_that_cannot_be_performed_refuses_and_names_the_mv(
    local_repo, seal, capsys
):
    """S19. The one platform-dependent step, and the guarantee is REMOVED
    rather than assumed: the destination's parent is made unwritable, so the
    failure is produced. `os.rename` also refuses across filesystems, which
    is why the message names `mv` — that one copies."""
    shared, _local = places(seal, local_repo)
    parent = os.path.dirname(shared)
    mode_bits = os.stat(parent).st_mode
    os.chmod(parent, 0o500)
    try:
        probe = os.path.join(parent, "probe-whether-chmod-took")
        try:
            with open(probe, "w", encoding="utf-8"):
                pass
            os.remove(probe)
            pytest.skip("the working tree is writable despite chmod (root?)")
        except OSError:
            pass
        before = state(seal, local_repo)

        code, out = run(seal, ["mode", "shared"], local_repo, capsys)

        assert code == 1, out
        assert "could not be moved" in out
        assert "mv " in out, "the move that does work across filesystems is not named"
        assert "Nothing else has run" in out
        assert state(seal, local_repo) == before
    finally:
        os.chmod(parent, mode_bits)


@pytest.mark.parametrize("shape", ["a directory", "a symbolic link"])
def test_a_config_that_cannot_be_written_refuses_before_the_move(
    shape, shared_repo, seal, capsys
):
    """S20. The row is one of the five paths the switch touches, and a switch
    that moves the root and then cannot write the row leaves the two
    disagreeing — which is the state this whole work item exists to end."""
    _repo, home, _shared, local, _mode = seal.resolve(str(shared_repo))
    path = os.path.join(home, "config.md")
    if shape == "a directory":
        os.mkdir(path)
    else:
        symlink_or_skip(os.path.join(home, "nowhere.md"), path)
    before = state(seal, shared_repo)

    code, out = run(seal, ["mode", "local"], shared_repo, capsys)

    assert code == 1, out
    assert "config.md" in out
    assert state(seal, shared_repo) == before
    assert not os.path.exists(local)


# --- S21 to S25: the workflow file ------------------------------------------


def template_text():
    with open(os.path.join(ROOT, "templates", "hygiene.yml"), encoding="utf-8") as f:
        return f.read()


def install_by_hand(repo, text=None):
    path = os.path.join(str(repo), WORKFLOW)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(template_text() if text is None else text)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "the workflow")
    return path


def test_the_template_carries_the_marker_and_the_placeholder(seal):
    """The marker and the placeholder are literals in `seal.py`, and a
    template that stopped carrying either would silently change what the
    command does: a file nobody recognises as this plugin's is never removed,
    and a version that cannot be pinned is never written. Pinned here so the
    two cannot drift apart."""
    text = template_text()
    assert seal.PLUGIN_CLONE in text, (
        "the workflow no longer names the plugin's clone URL, so "
        "`remove_workflow` cannot recognise its own file"
    )
    assert seal.PLACEHOLDER in text, (
        "the workflow no longer carries the version placeholder"
    )


def test_shared_to_local_removes_the_workflow_this_plugin_wrote(
    shared_repo, seal, capsys
):
    """S21. Measured: left behind, `unverified_check.py` exits 2 forever and
    `chain_check.py` exits 0 having read nothing. Removing it is the
    difference between "CI does not run these checks" and "CI says these
    checks passed"."""
    path = install_by_hand(shared_repo)

    code, out = run(seal, ["mode", "local"], shared_repo, capsys)

    assert code == 0, out
    assert not os.path.exists(path), "the workflow outlived the root it reads"
    assert any(
        ".github/workflows/hygiene.yml" in line for line in porcelain(shared_repo)
    )
    assert "removed" in out


def test_a_workflow_this_plugin_did_not_write_is_left_alone(shared_repo, seal, capsys):
    """S22. Deleting somebody's workflow because it shares a name is the
    destructive direction, so the file stays and the report says what that
    means. The switch still completes: the file is not the switch."""
    path = install_by_hand(shared_repo, "name: hygiene\njobs: {}\n")

    code, out = run(seal, ["mode", "local"], shared_repo, capsys)

    assert code == 0, out
    assert os.path.isfile(path), "someone else's workflow was deleted"
    assert "not written by this plugin" in out
    assert "read nothing" in out or "reads nothing" in out


def test_local_to_shared_writes_the_workflow_pinned_to_the_version(
    local_repo, seal, capsys
):
    """S23. A workflow that keeps `v<version>` fails CI's `git clone
    --branch` on the first pull request, so the substitution is what makes
    the file worth writing at all."""
    code, out = run(seal, ["mode", "shared"], local_repo, capsys)

    assert code == 0, out
    path = os.path.join(str(local_repo), WORKFLOW)
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    with open(
        os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8"
    ) as handle:
        version = json.load(handle)["version"]
    assert seal.PLACEHOLDER not in text, "the placeholder reached the written file"
    assert f"--branch v{version}" in text
    assert any(
        ".github/workflows/hygiene.yml" in line for line in porcelain(local_repo)
    )


def test_an_existing_workflow_is_never_overwritten(local_repo, seal, capsys):
    """S24. The same stance the skill's bootstrap takes at first setup, and
    the same one every other write in this command takes."""
    path = os.path.join(str(local_repo), WORKFLOW)
    os.makedirs(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("name: someone else's\n")

    code, out = run(seal, ["mode", "shared"], local_repo, capsys)

    assert code == 0, out
    with open(path, encoding="utf-8") as handle:
        assert handle.read() == "name: someone else's\n"
    assert "left alone" in out


def test_a_version_that_cannot_be_read_writes_no_workflow(
    local_repo, seal, capsys, tmp_path, monkeypatch
):
    """S25. Writing a workflow pinned to nothing is worse than writing none:
    the first fails CI's clone on every pull request and the second is a
    documented by-hand step, which the report names."""
    monkeypatch.setattr(seal, "PLUGIN_ROOT", str(tmp_path / "not-a-plugin"))

    code, out = run(seal, ["mode", "shared"], local_repo, capsys)

    assert code == 0, out
    assert not os.path.exists(os.path.join(str(local_repo), WORKFLOW))
    assert "was NOT written" in out
    assert "templates/hygiene.yml" in out, "the by-hand step is not named"


# --- S26: worktrees ---------------------------------------------------------


def test_another_worktree_is_named(shared_repo, seal, capsys, tmp_path):
    """S26. Measured 2026-09-03: switching from one worktree leaves every
    other one holding the committed root on its own branch, so the two read
    two different roots until the commit reaches both. It heals itself and
    loses nothing — the other copy is the committed one — so it is named
    rather than refused."""
    other = tmp_path / "linked"
    git(shared_repo, "worktree", "add", "-q", str(other), "feature/x")

    code, out = run(seal, ["mode", "local"], shared_repo, capsys)

    assert code == 0, out
    assert "another worktree" in out
    assert os.path.basename(str(other)) in out


# --- what a person reads: the documents this changed ------------------------


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


@pytest.mark.parametrize("readme", ["README.md", "README.ko.md"])
def test_both_readmes_name_the_command_before_the_by_hand_lines(readme):
    """The issue's fifth done-when: the section stops being two shell lines
    and starts naming a command. Order is the assertion — the by-hand pair
    stays, and a person who reads the section top to bottom meets the command
    first."""
    text = read(readme)
    assert "seal mode local" in text and "seal mode --check" in text, readme
    assert text.index("seal mode local") < text.index('git rm -r --cached "$('), readme


def test_the_config_template_ships_the_row_with_no_value():
    """A template declaring `shared` would hand every local-mode repository a
    row that is wrong from the moment it is copied — and the fix the command
    then offers is `--apply`, which would move their root into the tree
    through the one door that does not open both ways."""
    text = read("templates", "config.md")
    assert "| Mode |  |" in text, "the template's Mode row carries a value"
    assert "## Mode" in text


@pytest.mark.parametrize(
    "parts", [(".github", "workflows", "hygiene.yml"), ("templates", "hygiene.yml")]
)
def test_both_hygiene_workflows_run_the_check(parts):
    """The check has to reach a pull request in this repository AND in every
    repository shared mode sets up, or it names a disagreement nowhere."""
    text = read(*parts)
    assert "mode --check" in text, "/".join(parts)
