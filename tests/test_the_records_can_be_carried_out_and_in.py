"""`seal export` and `seal import`: a copy leaves the clone, and nothing is
overwritten taking one in.

Issue #81. In local mode the ledger and the work-item records live under the
common git directory, so a new machine or a re-clone starts with nothing.
Without a way to carry a copy that reads as *lose it* rather than *take a
copy*, which is what these two commands answer.

Three properties are what the cases are built around, because each of them
fails silently if it fails at all:

**Nothing beside the root leaves with it.** The smith mark, the worktree
choices, the review and parity marks, the throwaway opt-out and any lease sit
next to the root under the git directory, and none of them belongs to another
machine. The export walks the root and nothing else, so the exclusion is
structural — and a symbolic link inside the root is the one way back out of
that, which is why the link cases are here and not left to a reader's
confidence.

**A zip is untrusted input**, and the cases say precisely what that buys.
`extractall` is not used, but not for the reason usually given: measured
here, today's CPython already strips `..` and a leading `/` from a member's
name. What disqualifies it is that it overwrites, and that it writes through
a directory in the destination that is a symbolic link — the second is the
only escape that measured, so it has a case of its own AND a case that runs
`extractall` against the standard library to show the hazard is still there.
The name checks stay regardless: a defence that holds only while a
standard-library sanitiser keeps its shape is not one this file can claim.

**One walk feeds the zip and the digests.** A check assembled from two
enumerations drifts at the seam: the manifest would record what one of them
saw while the reminder compares against what the other sees, and the
difference reads as a work item somebody changed.
"""

import importlib.util
import json
import os
import subprocess
import zipfile

import pytest
from conftest import local_home, symlink_or_skip

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "implement", "scripts", "seal.py")

# Session state that sits BESIDE the root under the common git directory.
# `docs/one-root-by-lifetime.md` names the first four; the lease and this
# command's own state are the two that arrived later. None may ever be in a
# zip, and the case that asserts it builds every one of them.
BESIDE_THE_ROOT = (
    "specseal-implementer",
    "specseal-reviewed",
    "specseal-parity",
    "specseal-scratch",
    "specseal-last-export.json",
    "specseal-session-lease",
)


@pytest.fixture
def seal():
    spec = importlib.util.spec_from_file_location("specseal_seal", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def with_records(repo, home, item="1788000000-a-work-item"):
    """A root holding one work item's directory and its ledger fragment."""
    work = home / "specs" / item
    work.mkdir(parents=True, exist_ok=True)
    (work / "spec.md").write_text("# spec\n", encoding="utf-8")
    (work / "routing.md").write_text("# routing\n", encoding="utf-8")
    (home / "ledger").mkdir(exist_ok=True)
    (home / "ledger" / f"{item}.md").write_text("# rows\n", encoding="utf-8")
    (home / "ledger.md").write_text("# the ledger\n", encoding="utf-8")
    return home


@pytest.fixture
def local(repo):
    """A local-mode repository with a remote and one work item."""
    git(repo, "remote", "add", "origin", "git@example.com:org/thing.git")
    return with_records(repo, local_home(repo))


def run(seal, argv, cwd, capsys):
    """(exit code, stdout) for one invocation."""
    code = seal.main(argv, cwd=str(cwd))
    return code, capsys.readouterr().out


def only_zip(directory):
    found = sorted(p for p in os.listdir(directory) if p.endswith(".zip"))
    assert len(found) == 1, f"expected one zip in {directory}, found {found}"
    return os.path.join(directory, found[0])


def files_under(path):
    out = []
    for dirpath, _dirnames, filenames in os.walk(path):
        for name in filenames:
            full = os.path.join(dirpath, name)
            out.append(os.path.relpath(full, path).replace(os.sep, "/"))
    return sorted(out)


# --- S1, S4: the zip and its manifest ---------------------------------------


def test_export_writes_the_zip_outside_the_working_tree(seal, repo, local, capsys):
    """S1. The default lands beside the clone, never in it: the normal place
    to run this is the repository root, and an untracked zip there is one
    `git add -A` from committing the records local mode keeps out of the
    tree."""
    code, out = run(seal, ["export"], repo, capsys)
    assert code == 0, out
    written = only_zip(repo.parent)
    assert os.path.basename(written).startswith("seal-repo-")
    assert os.path.basename(written).endswith(".zip")
    assert git(repo, "status", "--porcelain") == "", (
        "the export dirtied the working tree"
    )
    assert zipfile.ZipFile(written).namelist() == [
        "manifest.json",
        "seal/ledger.md",
        "seal/ledger/1788000000-a-work-item.md",
        "seal/specs/1788000000-a-work-item/routing.md",
        "seal/specs/1788000000-a-work-item/spec.md",
    ]


def test_the_manifest_names_the_remote_the_head_and_the_items(
    seal, repo, local, capsys
):
    """S4. The remote and the HEAD are the manifest's whole reason for
    existing: they are what lets an import say *this is from another
    repository* instead of merging one project's records into another's."""
    code, out = run(seal, ["export"], repo, capsys)
    assert code == 0, out
    manifest = json.loads(zipfile.ZipFile(only_zip(repo.parent)).read("manifest.json"))
    assert manifest["format"] == 1
    assert manifest["mode"] == "local"
    assert manifest["remote"] == "git@example.com:org/thing.git"
    assert manifest["head"] == git(repo, "rev-parse", "HEAD")
    assert manifest["exported_at"].endswith("Z")
    assert list(manifest["items"]) == ["1788000000-a-work-item"]


def test_a_second_export_on_the_same_day_does_not_overwrite_the_first(
    seal, repo, local, capsys
):
    """Nothing this command writes ever replaces a file, and the zip is the
    first place that rule has to hold."""
    assert run(seal, ["export"], repo, capsys)[0] == 0
    (local / "ledger.md").write_text("# changed\n", encoding="utf-8")
    assert run(seal, ["export"], repo, capsys)[0] == 0
    zips = sorted(p for p in os.listdir(repo.parent) if p.endswith(".zip"))
    assert len(zips) == 2, zips
    # Not `zips[1]`: `-` sorts before `.`, so the numbered one comes first.
    assert any(name.endswith("-2.zip") for name in zips), zips


# --- S2, S3: what never leaves the clone ------------------------------------


def test_no_session_state_beside_the_root_is_in_the_zip(seal, repo, local, capsys):
    """S2. The mark, the choices, the two review marks, the opt-out and the
    lease all sit beside the root, and none of them belongs to another
    machine."""
    common = repo / ".git"
    for name in BESIDE_THE_ROOT:
        if name == "specseal-scratch":
            continue  # it would take the opt-in back; its own case is below
        (common / name).write_text("session state\n", encoding="utf-8")
    (common / "specseal-worktree-choice").mkdir()
    (common / "specseal-worktree-choice" / "a-branch").write_text("x")

    code, out = run(seal, ["export"], repo, capsys)
    assert code == 0, out
    members = zipfile.ZipFile(only_zip(repo.parent)).namelist()
    for name in (*BESIDE_THE_ROOT, "specseal-worktree-choice"):
        assert not any(name in member for member in members), (
            f"{name} is session state and reached the zip: {members}"
        )


def test_a_link_out_of_the_root_is_skipped_and_named(seal, repo, local, capsys):
    """S3. The root being its own directory is what makes the exclusion
    structural, and a symbolic link inside it is the one way back out. The
    target's bytes must not be in the zip, and the skip must be reported —
    silently dropping a file from a copy is how a copy is discovered to be
    incomplete on the machine that has nothing else."""
    (repo / ".git" / "specseal-implementer").write_text("secret-branch\n")
    symlink_or_skip(os.path.join("..", "specseal-implementer"), str(local / "leak.md"))
    code, out = run(seal, ["export"], repo, capsys)
    assert code == 0, out
    assert "skipped the symbolic link seal/leak.md" in out

    archive = zipfile.ZipFile(only_zip(repo.parent))
    assert "seal/leak.md" not in archive.namelist()
    assert not any(b"secret-branch" in archive.read(m) for m in archive.namelist())


def test_a_link_leaves_the_digest_alone_too(seal, repo, local, capsys):
    """The seam. Links are excluded by the walk, so they are absent from the
    members and from the digests together — excluding them at the zip alone
    would make every export of a repository holding one report a change that
    nothing made."""
    item = local / "specs" / "1788000000-a-work-item"
    before = seal.work_item_digests(seal.root_files(str(local))[0])
    symlink_or_skip(os.path.join("..", "..", "ledger.md"), str(item / "link.md"))
    after = seal.work_item_digests(seal.root_files(str(local))[0])
    assert before == after, "a symbolic link changed a work item's digest"


def test_the_zips_members_are_exactly_what_the_walk_yields(seal, repo, local, capsys):
    """The seam, pinned from the other side. Two enumerations drift; this
    asserts there is one."""
    assert run(seal, ["export"], repo, capsys)[0] == 0
    walked = [rel for rel, _disk in seal.root_files(str(local))[0]]
    members = zipfile.ZipFile(only_zip(repo.parent)).namelist()
    assert [m[len("seal/") :] for m in members if m != "manifest.json"] == walked


# --- S5 to S9: the import's outcomes ----------------------------------------


@pytest.fixture
def carried(seal, repo, local, capsys, tmp_path):
    """A zip from `local`, and a second local-mode clone to take it into."""
    assert run(seal, ["export"], repo, capsys)[0] == 0
    zip_path = only_zip(repo.parent)
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "init", "-q", str(other)], check=True)
    git(other, "config", "user.email", "t@t")
    git(other, "config", "user.name", "t")
    git(other, "remote", "add", "origin", "https://example.com/org/thing")
    return zip_path, other, local_home(other)


def test_missing_records_are_added(seal, carried, capsys):
    """S5."""
    zip_path, other, home = carried
    code, out = run(seal, ["import", zip_path], other, capsys)
    assert code == 0, out
    assert "4 files added" in out
    assert files_under(home) == [
        "ledger.md",
        "ledger/1788000000-a-work-item.md",
        "specs/1788000000-a-work-item/routing.md",
        "specs/1788000000-a-work-item/spec.md",
    ]


def test_an_id_already_here_lands_beside_it_and_is_reported(seal, carried, capsys):
    """S6. The design's own spelling: `<id>.incoming.md` beside the existing
    file, reported and not asked about. The existing bytes are what the case
    is really about — an import that overwrote them would still print a
    perfectly good report."""
    zip_path, other, home = carried
    (home / "ledger").mkdir(parents=True)
    fragment = home / "ledger" / "1788000000-a-work-item.md"
    fragment.write_text("# rows this clone wrote\n", encoding="utf-8")

    code, out = run(seal, ["import", zip_path], other, capsys)
    assert code == 0, out
    assert fragment.read_text(encoding="utf-8") == "# rows this clone wrote\n", (
        "the import overwrote a file that was already here"
    )
    landed = home / "ledger" / "1788000000-a-work-item.incoming.md"
    assert landed.read_text(encoding="utf-8") == "# rows\n"
    assert "1788000000-a-work-item.incoming.md" in out


def test_identical_bytes_are_not_a_collision(seal, carried, capsys):
    """S7. Re-importing the same zip writes nothing at all, rather than a
    second pile of `.incoming` copies of files that are already there."""
    zip_path, other, home = carried
    assert run(seal, ["import", zip_path], other, capsys)[0] == 0
    before = files_under(home)
    code, out = run(seal, ["import", zip_path], other, capsys)
    assert code == 0, out
    assert files_under(home) == before, "a second import of the same zip wrote files"
    assert "4 files already here, byte for byte" in out


def test_a_second_differing_copy_is_numbered_never_overwritten(seal, carried, capsys):
    """S8. Losing the second copy silently is the only outcome worse than a
    file with a long name."""
    zip_path, other, home = carried
    (home / "ledger").mkdir(parents=True)
    (home / "ledger" / "1788000000-a-work-item.md").write_text("# mine\n")
    (home / "ledger" / "1788000000-a-work-item.incoming.md").write_text("# earlier\n")

    code, out = run(seal, ["import", zip_path], other, capsys)
    assert code == 0, out
    assert (home / "ledger" / "1788000000-a-work-item.md").read_text() == "# mine\n"
    assert (
        home / "ledger" / "1788000000-a-work-item.incoming.md"
    ).read_text() == "# earlier\n"
    assert (
        home / "ledger" / "1788000000-a-work-item.incoming-2.md"
    ).read_text() == "# rows\n"


def test_the_import_asks_nothing_and_names_the_next_command(seal, carried, capsys):
    """S9. "reported, not asked about" — and `evidence-check` is what says
    which rows drift against this tree, so the report names it rather than
    running it and reporting a pass nobody read."""
    zip_path, other, _home = carried
    code, out = run(seal, ["import", zip_path], other, capsys)
    assert code == 0
    assert "?" not in out.replace("nothing?", ""), f"the import asked something: {out}"
    assert "evidence-check ." in out


# --- S10, S11: the mode switch ----------------------------------------------


def test_into_shared_creates_the_committed_root(seal, carried, capsys):
    """S10, one direction. Export, import into the other mode's root, commit —
    which is what `docs/one-root-by-lifetime.md` calls the mode switch."""
    zip_path, other, _local = carried
    shared = other / "seal"
    assert not shared.exists()
    code, out = run(seal, ["import", zip_path, "--into", "shared"], other, capsys)
    assert code == 0, out
    assert (shared / "ledger.md").read_text(encoding="utf-8") == "# the ledger\n"


def test_into_local_creates_the_root_under_the_git_directory(seal, carried, capsys):
    """S10, the other direction."""
    zip_path, other, home = carried
    home.rmdir()
    code, out = run(seal, ["import", zip_path, "--into", "local"], other, capsys)
    assert code == 0, out
    assert (home / "ledger.md").exists()
    assert git(other, "status", "--porcelain") == "", "the import dirtied the tree"


def test_neither_root_present_defaults_to_local(seal, carried, capsys):
    """The safe guess. Choosing shared would write this plugin's files into a
    tree that may be someone else's, which is the harm local mode exists to
    prevent."""
    zip_path, other, home = carried
    home.rmdir()
    code, out = run(seal, ["import", zip_path], other, capsys)
    assert code == 0, out
    assert (home / "ledger.md").exists()
    assert not (other / "seal").exists()


def test_both_roots_present_refuses_and_names_which_is_read(seal, carried, capsys):
    """S11. Writing into one while the other exists leaves a dead root the
    hooks never read, which is worse than a stop."""
    zip_path, other, home = carried
    (other / "seal").mkdir()
    before = files_under(home)
    code, out = run(seal, ["import", zip_path, "--into", "local"], other, capsys)
    assert code == 1
    assert "both roots exist" in out
    assert "read first" in out
    assert files_under(home) == before, "a refusal wrote files"


# --- S12: the shared-mode answer --------------------------------------------


def test_export_in_shared_mode_writes_no_zip_and_says_why(seal, repo, capsys):
    """S12. The zip would be a second copy of committed files that nothing
    keeps current, and git already carries the first. Exit 1 rather than 0 for
    the reason `fold_ledger.py` exits 1 for *nothing to fold*: a caller
    scripting `seal export && cp seal-*.zip …` must not copy nothing and
    report success."""
    with_records(repo, repo / "seal")
    code, out = run(seal, ["export"], repo, capsys)
    assert code == 1
    assert "shared mode" in out
    assert "seal/" in out
    assert "git rev-parse --git-common-dir" in out, (
        "the refusal has to carry the command that switches to local mode"
    )
    assert not [p for p in os.listdir(repo.parent) if p.endswith(".zip")]


# --- S13 to S15: the release reminder ---------------------------------------


def test_the_reminder_is_one_line_and_writes_nothing(seal, repo, local, capsys):
    """S13. The design fixes the wording, so the case compares the whole of
    stdout rather than searching it: `and nothing else` is half the
    requirement."""
    assert run(seal, ["export"], repo, capsys)[0] == 0
    (local / "specs" / "1788000000-a-work-item" / "spec.md").write_text("# edited\n")
    before = files_under(local)

    code, out = run(seal, ["export", "--check"], repo, capsys)
    assert code == 0
    assert out == "1 work items changed since the last export\n", repr(out)
    assert files_under(local) == before


def test_the_reminder_counts_an_added_and_a_removed_work_item(
    seal, repo, local, capsys
):
    """What `changed` means, stated where a reader can check it: a work item
    the export did not carry, and one it carried that is gone."""
    assert run(seal, ["export"], repo, capsys)[0] == 0
    with_records(repo, local, item="1788000001-another")
    (local / "specs" / "1788000000-a-work-item" / "spec.md").unlink()
    (local / "specs" / "1788000000-a-work-item" / "routing.md").unlink()
    (local / "ledger" / "1788000000-a-work-item.md").unlink()

    code, out = run(seal, ["export", "--check"], repo, capsys)
    assert code == 0
    assert out == "2 work items changed since the last export\n", repr(out)


def test_the_reminder_says_so_when_nothing_has_been_exported(seal, repo, local, capsys):
    """S14. `N changed since the last export` is meaningless with no last
    export, so that state gets its own line rather than a misleading number."""
    code, out = run(seal, ["export", "--check"], repo, capsys)
    assert code == 0
    assert "no export yet" in out
    assert "changed since the last export" not in out


def test_the_reminder_never_fails_a_shared_mode_release(seal, repo, capsys):
    """S15. A release script runs this unconditionally, and a shared-mode
    repository has nothing to be reminded about — the records are already in
    the commit range."""
    with_records(repo, repo / "seal")
    code, out = run(seal, ["export", "--check"], repo, capsys)
    assert code == 0
    assert "committed" in out


def test_the_reminder_ignores_a_root_level_file(seal, repo, local, capsys):
    """The gap this command does NOT paper over. `follow-up.md` is not a work
    item, so a change confined to it reports 0 — the line the design fixes
    says *work items*, and widening it is the owner's call (Q1 in the work
    item's questions.md), not this command's."""
    assert run(seal, ["export"], repo, capsys)[0] == 0
    (local / "follow-up.md").write_text("# a new follow-up row\n", encoding="utf-8")
    code, out = run(seal, ["export", "--check"], repo, capsys)
    assert code == 0
    assert out == "0 work items changed since the last export\n", repr(out)


# --- S16 to S20: the fail directions ----------------------------------------


def test_neither_command_invents_a_root(seal, repo, capsys):
    """S16. Creating one would pick the mode for the user, which is the one
    question first setup exists to ask."""
    for argv in (["export"], ["export", "--check"]):
        code, out = run(seal, argv, repo, capsys)
        assert code == 1, argv
        assert "shared mode" in out and "local mode" in out
        assert not (repo / "seal").exists()
        assert not (repo / ".git" / "seal").exists()


def test_a_throwaway_repository_is_named_as_one(seal, repo, local, capsys):
    """The opt-out reaches this command through `optin.home_at`, and a
    fixture built to be thrown away has nothing worth exporting. Saying which
    marker did it beats a message about a root that is plainly there."""
    (repo / ".git" / "specseal-scratch").write_text("")
    code, out = run(seal, ["export"], repo, capsys)
    assert code == 1
    assert "specseal-scratch" in out


def test_a_file_that_is_not_a_zip_leaves_the_root_alone(seal, carried, capsys):
    """S17."""
    _zip_path, other, home = carried
    bad = other.parent / "not-a-zip.zip"
    bad.write_text("hello")
    before = files_under(home)
    code, out = run(seal, ["import", str(bad)], other, capsys)
    assert code == 1
    assert "not a readable zip" in out
    assert files_under(home) == before


def test_a_truncated_zip_leaves_the_root_alone(seal, carried, capsys):
    """S17, the half a `BadZipFile` does not always cover: a file whose
    header reads and whose body does not."""
    zip_path, other, home = carried
    data = open(zip_path, "rb").read()
    cut = other.parent / "cut.zip"
    cut.write_bytes(data[: len(data) // 2])
    before = files_under(home)
    code, out = run(seal, ["import", str(cut)], other, capsys)
    assert code == 1, out
    assert files_under(home) == before


@pytest.mark.parametrize(
    "name",
    [
        "seal/../../escape.md",
        "../escape.md",
        "/etc/passwd",
        "C:\\windows\\x.md",
        "seal/a\\..\\..\\b.md",
        "seal/nested/../../../out.md",
    ],
)
def test_a_member_that_climbs_out_refuses_the_whole_zip(seal, carried, capsys, name):
    """S19. `extractall` writes a member wherever its name says, so it is not
    used; this is the pin on that. The whole archive is refused rather than
    the member, because a partial copy from a hostile zip is still a decision
    the zip made."""
    _zip_path, other, home = carried
    hostile = other.parent / "hostile.zip"
    with zipfile.ZipFile(hostile, "w") as archive:
        archive.writestr("manifest.json", json.dumps({"format": 1, "remote": ""}))
        archive.writestr(name, "x")
    before = files_under(home)

    code, out = run(seal, ["import", str(hostile)], other, capsys)
    assert code == 1, out
    assert "will not write" in out
    assert files_under(home) == before, "a refused zip still wrote something"
    assert not (other.parent / "escape.md").exists()
    assert not (other.parent / "out.md").exists()


def test_a_symlink_member_refuses_the_zip(seal, carried, capsys):
    """S19. A link written into the root is a way to reach outside it on the
    NEXT export — the loop the export's own link handling closes from the
    other end."""
    _zip_path, other, home = carried
    hostile = other.parent / "linky.zip"
    with zipfile.ZipFile(hostile, "w") as archive:
        archive.writestr("manifest.json", json.dumps({"format": 1, "remote": ""}))
        info = zipfile.ZipInfo("seal/leak.md")
        info.external_attr = (0o120777 << 16) | 0o200000
        archive.writestr(info, "../specseal-implementer")
    before = files_under(home)

    code, out = run(seal, ["import", str(hostile)], other, capsys)
    assert code == 1, out
    assert "symbolic link" in out
    assert files_under(home) == before


def test_a_linked_directory_in_the_destination_refuses_the_zip(seal, carried, capsys):
    """The only escape that MEASURED, and the reason the traversal cases above
    are defence rather than the whole story.

    On the CPython this ships on, `extractall` already strips `..` and a
    leading `/`. What it does not do is refuse to write through a directory in
    the DESTINATION that is a symbolic link — and neither does a plain
    `open()`, which is what this module writes with. So `seal/specs` pointed
    elsewhere would put every work item there, and that is checked for before
    anything is written.
    """
    zip_path, other, home = carried
    outside = other.parent / "outside"
    outside.mkdir()
    symlink_or_skip(str(outside), str(home / "specs"))

    code, out = run(seal, ["import", zip_path], other, capsys)
    assert code == 1, out
    assert "symbolic link" in out
    assert files_under(outside) == [], "a record was written outside the root"
    assert not (home / "ledger.md").exists(), "a refusal wrote a file"


def test_extractall_would_have_written_through_that_link(seal, tmp_path):
    """The counterfeit rule, applied to the case above: it has to be able to
    fail. This is the behaviour it guards against, run against the standard
    library rather than asserted about it — so a build that quietly went back
    to `extractall` would be caught by the case above rather than by nobody.
    """
    destination = tmp_path / "root"
    (destination).mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    symlink_or_skip(str(outside), str(destination / "specs"))
    archive = tmp_path / "h.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("specs/1788000000-x/spec.md", "LANDED")

    zipfile.ZipFile(archive).extractall(destination)
    assert (outside / "1788000000-x" / "spec.md").read_text() == "LANDED", (
        "extractall no longer follows a linked destination directory — "
        "re-measure what the import's own check is still buying"
    )


def test_a_member_that_is_neither_the_manifest_nor_under_the_root_refuses(
    seal, carried, capsys
):
    """A member this build has no place for is a zip it does not understand,
    and writing the parts it does understand is guessing."""
    _zip_path, other, _home = carried
    odd = other.parent / "odd.zip"
    with zipfile.ZipFile(odd, "w") as archive:
        archive.writestr("manifest.json", json.dumps({"format": 1, "remote": ""}))
        archive.writestr("elsewhere/x.md", "x")
    code, out = run(seal, ["import", str(odd)], other, capsys)
    assert code == 1, out
    assert "is not under seal/" in out


def test_a_zip_from_another_repository_refuses_and_names_the_flag(
    seal, carried, capsys
):
    """S18. Records are keyed by work-item id, so merging another project's
    spreads through the root with nothing to tell them apart afterwards. A
    refusal that names no way past it is a wall, so the flag is in the
    message."""
    _zip_path, other, home = carried
    foreign = other.parent / "foreign.zip"
    with zipfile.ZipFile(foreign, "w") as archive:
        archive.writestr(
            "manifest.json",
            json.dumps(
                {"format": 1, "remote": "git@example.com:org/somewhere-else.git"}
            ),
        )
        archive.writestr("seal/ledger.md", "# theirs\n")
    before = files_under(home)

    code, out = run(seal, ["import", str(foreign)], other, capsys)
    assert code == 1, out
    assert "another repository" in out
    assert "--allow-other-repo" in out
    assert files_under(home) == before

    code, out = run(seal, ["import", str(foreign), "--allow-other-repo"], other, capsys)
    assert code == 0, out
    assert (home / "ledger.md").read_text(encoding="utf-8") == "# theirs\n"


def test_two_spellings_of_one_repository_are_one_repository(seal, carried, capsys):
    """The `carried` fixture exports from a clone whose remote is
    `git@example.com:org/thing.git` and imports into one whose remote is
    `https://example.com/org/thing` — ssh at one machine and https at another
    is the ordinary case, and comparing the strings would refuse every real
    import."""
    zip_path, other, _home = carried
    code, out = run(seal, ["import", zip_path], other, capsys)
    assert code == 0, out
    assert "another repository" not in out


@pytest.mark.parametrize(
    "left,right",
    [
        ("git@example.com:org/repo.git", "https://example.com/org/repo"),
        ("ssh://git@example.com/org/repo.git", "https://example.com/org/repo/"),
        ("HTTPS://Example.com/Org/Repo.git", "https://example.com/org/repo"),
    ],
)
def test_remote_urls_reduce_to_host_and_path(seal, left, right):
    assert seal.normalise_remote(left) == seal.normalise_remote(right)


def test_a_port_is_not_read_as_an_scp_separator(seal):
    """The colon becomes `/` only where there was no scheme. Otherwise
    `https://example.com:8443/x` reduces to `example.com/8443/x`, and two
    ports of one host stop comparing equal to themselves."""
    assert seal.normalise_remote("https://example.com:8443/org/repo") == (
        "example.com:8443/org/repo"
    )


def test_two_different_repositories_do_not_reduce_to_one(seal):
    """The direction the normalisation must not be wrong in."""
    assert seal.normalise_remote("git@example.com:org/a.git") != seal.normalise_remote(
        "git@example.com:org/b.git"
    )
    assert seal.normalise_remote("git@example.com:org/a") != seal.normalise_remote(
        "git@other.example:org/a"
    )


@pytest.mark.parametrize(
    "manifest", [None, {"format": 99}, {}, ["not", "an", "object"]]
)
def test_a_manifest_this_build_cannot_read_refuses(seal, carried, capsys, manifest):
    """S20. A zip whose fields moved, read by a build that assumes the old
    ones, places records at the wrong paths — and that merge is the operation
    this command exists to make safe."""
    _zip_path, other, home = carried
    path = other.parent / "odd-manifest.zip"
    with zipfile.ZipFile(path, "w") as archive:
        if manifest is not None:
            archive.writestr("manifest.json", json.dumps(manifest))
        archive.writestr("seal/ledger.md", "x")
    before = files_under(home)

    code, out = run(seal, ["import", str(path)], other, capsys)
    assert code == 1, out
    assert files_under(home) == before


# --- the wrappers ------------------------------------------------------------


@pytest.mark.parametrize("readme", ["README.md", "README.ko.md"])
def test_both_readmes_carry_the_pair_and_the_rule_that_makes_it_safe(readme):
    """`CONTRIBUTING.md`: both READMEs move together, and they must tell the
    same story about what exists. Until this work item they both said the pair
    arrives with #81.

    The never-overwrite rule is asserted rather than just the command names,
    because that is the property a reader has to know before running `import`
    on a clone that already holds records — a command that quietly merged
    would be reported the same way by a README that only lists it.
    """
    with open(os.path.join(ROOT, readme), encoding="utf-8") as handle:
        text = handle.read()
    assert "seal export" in text and "seal import" in text
    assert ".incoming" in text, f"{readme} does not say where a collision lands"
    assert "#81" not in text, (
        f"{readme} still calls the pair later work, and it is here"
    )


def test_the_root_readme_and_its_template_say_it_too():
    """The template is what a first setup bootstraps a user's root from, and
    `tests/test_first_setup_asks_once.py` asserts the two are byte-identical —
    so the rule lands in every repository that opts in, not only this one."""
    for parts in (("seal", "README.md"), ("templates", "seal-README.md")):
        with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
            text = handle.read()
        assert "seal export" in text and "seal import" in text, "/".join(parts)
        assert "specseal-last-export.json" in text, (
            "/".join(parts) + " does not name the state that must not travel"
        )


def test_both_wrappers_ship_and_point_at_this_script():
    """`bin/` is on the Bash tool's PATH while the plugin is enabled, and
    cmd.exe resolves a bare `seal` to the `.cmd` twin through PATHEXT. Four
    such pairs existed; a new command means both files or it means one
    platform."""
    posix = os.path.join(ROOT, "bin", "seal")
    windows = os.path.join(ROOT, "bin", "seal.cmd")
    assert os.path.isfile(posix), "bin/seal missing"
    assert os.path.isfile(windows), "bin/seal.cmd missing"
    with open(posix, encoding="utf-8") as handle:
        assert "skills/implement/scripts/seal.py" in handle.read()
    with open(windows, encoding="utf-8") as handle:
        text = handle.read()
    assert "skills\\implement\\scripts\\seal.py" in text
    assert "py -3" in text and "python " in text, (
        "the .cmd twin prefers `py -3` and falls back to `python`"
    )
