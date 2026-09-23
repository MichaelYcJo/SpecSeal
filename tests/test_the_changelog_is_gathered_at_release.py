"""A change writes a changelog fragment; the release gathers them.

Issue #46. Three branches ran in parallel on 2026-09-01, touched 34 files, and
shared exactly one — `CHANGELOG.md`, in all three pairs. Nothing else
overlapped at all, so parallel work was never the thing that conflicted:
appending to one three-line region was.

What made it worth fixing is when the conflict arrives. `CONTRIBUTING.md` and
the `verify` skill both say nothing may be edited between the broad gate and
the pull request, so resolving a changelog conflict costs a second run of the
whole broad gate. Two of the three branches paid that or were about to.

The fix is one fragment per work item, gathered at release. This file holds
the gathering — that it happens, that it happens once, and that a release
pull request cannot go out with a fragment left behind.
"""

import os
import re
import subprocess
import sys

import pytest
from conftest import gathered_entry

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, ".github", "scripts", "gather_changelog.py")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    return " ".join(read(*parts).split())


def run(*args, root=None):
    return subprocess.run(
        [sys.executable, SCRIPT, *args, "--root", str(root)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


@pytest.fixture
def tree(tmp_path):
    """A repository shape with a released changelog and two fragments."""
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n## 0.1.0 — 2026-09-01\n\n- the first release\n",
        encoding="utf-8",
    )
    for work_item_id, body in (
        ("1788229400-later", "- **the later one.** What it changes.\n"),
        ("1700000000-earlier", "- **the earlier one.** What it changes.\n"),
    ):
        d = tmp_path / "seal" / "specs" / work_item_id
        d.mkdir(parents=True)
        (d / "changelog.md").write_text(body, encoding="utf-8")
    return tmp_path


def changelog(tree):
    return (tree / "CHANGELOG.md").read_text(encoding="utf-8")


def gather(tree, version="0.2.0", date="2026-09-15"):
    """Run the gather and prove it actually gathered.

    Round 1, 🟡 9: three cases here ran the gather and then asserted something
    that a script consisting of `sys.exit(0)` also satisfies. A return code is
    not an effect — the marker landing in the file is — so every case that
    depends on a gather having happened goes through this.
    """
    r = run("--version", version, "--date", date, root=tree)
    assert r.returncode == 0, r.stdout + r.stderr
    text = changelog(tree)
    assert f"## {version} — {date}" in text, (
        f"the gather exited 0 and wrote no section:\n{text}"
    )
    assert "<!-- specs/" in text, f"the gather exited 0 and wrote no marker:\n{text}"
    return r


def test_every_fragment_reaches_the_released_section(tree):
    r = run("--version", "0.2.0", "--date", "2026-09-15", root=tree)
    assert r.returncode == 0, r.stdout + r.stderr
    text = changelog(tree)
    assert "## 0.2.0 — 2026-09-15" in text, text
    assert "the later one" in text and "the earlier one" in text, text


def test_the_new_section_lands_above_the_released_ones(tree):
    """A section that lands below a dated one reads as older than work that
    already shipped — the state `test_unreleased_sits_above_every_dated_section`
    was written for, after a rebase resolved the wrong way."""
    gather(tree)
    headings = re.findall(r"^## (.+)$", changelog(tree), re.M)
    assert headings[0].startswith("0.2.0"), headings


def test_the_entries_are_in_work_item_order(tree):
    """The id is unix seconds, so ordering by it is chronological — and, more
    to the point, deterministic. A section whose order depends on the
    filesystem cannot be compared with the run before it."""
    gather(tree)
    text = changelog(tree)
    assert text.index("the earlier one") < text.index("the later one"), text


def test_gathering_twice_writes_one_copy(tree):
    """Release preparation is re-runnable, and a half-finished release is
    where somebody runs it twice."""
    gather(tree)
    second = run("--version", "0.2.0", "--date", "2026-09-15", root=tree)
    assert second.returncode == 1, second.stdout
    assert changelog(tree).count("the later one") == 1, changelog(tree)


def test_a_second_gather_for_the_same_version_appends_into_its_section(tree):
    """#289. A release pull request finding something is the ordinary shape:
    the first gather ran at the preparation commit, the pull request went
    red, a fragment landed, and the second gather wrote a SECOND `## X.Y.Z`
    heading — one release's entries split across two sections that read as
    two releases with the same number. The section is appended into now, it
    keeps the first gather's date, and the file holds one heading."""
    gather(tree)
    late = tree / "seal" / "specs" / "1788300001-late"
    late.mkdir(parents=True)
    (late / "changelog.md").write_text(
        "- **the late one.** A repair.\n", encoding="utf-8"
    )
    second = run("--version", "0.2.0", "--date", "2026-09-16", root=tree)
    assert second.returncode == 0, second.stdout + second.stderr
    text = changelog(tree)
    headings = re.findall(r"^## (.+)$", text, re.M)
    assert headings == ["0.2.0 — 2026-09-15", "0.1.0 — 2026-09-01"], (
        f"the second gather wrote a second heading, or re-dated the first: {headings}"
    )
    assert "the late one" in text, text
    # Inside the section, after the entries the first gather wrote and
    # before the release below it.
    assert (
        text.index("the later one")
        < text.index("the late one")
        < text.index("## 0.1.0")
    ), text
    assert "<!-- specs/1788300001-late -->" in text, text
    check = run("--check", root=tree)
    assert check.returncode == 0, check.stdout
    assert "3 changelog fragments, all gathered" in check.stdout, check.stdout


def test_a_dry_run_of_a_second_gather_shows_the_section_it_appends_into(tree):
    """The preview a person reads before the write says which heading the
    entries join, dated as the file has it — not a fresh heading with today's
    date that the write then does not make."""
    gather(tree)
    late = tree / "seal" / "specs" / "1788300001-late"
    late.mkdir(parents=True)
    (late / "changelog.md").write_text(
        "- **the late one.** A repair.\n", encoding="utf-8"
    )
    before = changelog(tree)
    r = run("--version", "0.2.0", "--date", "2026-09-16", "--dry-run", root=tree)
    assert r.returncode == 0, r.stdout
    assert "## 0.2.0 — 2026-09-15" in r.stdout, r.stdout
    assert "2026-09-16" not in r.stdout, r.stdout
    assert changelog(tree) == before, "--dry-run wrote to the file"


def test_a_release_with_nothing_to_gather_fails(tree):
    """A release with no entries is one nobody can read. `hooks/version-check.py`
    tells a user a new version exists and the changelog is where they find out
    what is in it, so an empty release is a failure rather than a no-op."""
    gather(tree)
    r = run("--version", "0.3.0", "--date", "2026-10-01", root=tree)
    assert r.returncode == 1, r.stdout
    assert "nothing to gather" in r.stdout, r.stdout


def test_check_fails_while_a_fragment_is_outstanding(tree):
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "seal/specs/1788229400-later/changelog.md" in r.stdout, r.stdout
    assert "seal/specs/1700000000-earlier/changelog.md" in r.stdout, r.stdout


def test_check_passes_once_they_are_gathered(tree):
    gather(tree)
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout
    # A `--check` that exits 0 because it found no fragments at all would
    # satisfy the line above. It has to say it looked at both.
    assert "2 changelog fragments, all gathered" in r.stdout, r.stdout


def test_a_copy_edit_to_a_released_entry_does_not_reopen_it(tree):
    """The reason gathering is marked rather than matched.

    Matching a fragment's text against the file works exactly once. Any later
    wording fix to a released entry — a typo, a re-wrap — would make its
    fragment read as ungathered again, and a release pull request would go red
    forever with no way to close it but re-gathering an entry that is already
    there.
    """
    gather(tree)
    text = changelog(tree)
    assert "<!-- specs/1788229400-later -->" in text, text
    text = text.replace("the later one", "the later one, reworded")
    (tree / "CHANGELOG.md").write_text(text, encoding="utf-8")
    assert "the later one." not in changelog(tree), (
        "the re-wording did not land, so this proves nothing about matching"
    )
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout
    assert "2 changelog fragments, all gathered" in r.stdout, r.stdout


def test_a_fragment_deleted_from_the_file_by_hand_is_reported(tree):
    """The other direction, or the case above passes by never failing."""
    gather(tree)
    text = changelog(tree).replace("<!-- specs/1788229400-later -->", "")
    (tree / "CHANGELOG.md").write_text(text, encoding="utf-8")
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "1788229400-later" in r.stdout, r.stdout


def test_dry_run_writes_nothing(tree):
    """The precedent is `close_issues_on_release.py`'s `DRY_RUN`, which exists
    because that script was run by hand for its output during development and
    closed a real issue."""
    before = changelog(tree)
    r = run("--version", "0.2.0", "--date", "2026-09-15", "--dry-run", root=tree)
    assert r.returncode == 0, r.stdout
    assert "## 0.2.0 — 2026-09-15" in r.stdout
    assert changelog(tree) == before, "--dry-run wrote to the file"


def test_an_empty_fragment_is_not_gathered_as_a_blank_entry(tree):
    """A work item that opened the file and wrote nothing has no entry, and a
    marker with nothing under it would make `--check` green for a change that
    ships unexplained."""
    d = tree / "seal" / "specs" / "1788300000-empty"
    d.mkdir(parents=True)
    (d / "changelog.md").write_text("\n\n", encoding="utf-8")
    gather(tree)
    text = changelog(tree)
    # The positive control. Without it this case passes when the gather wrote
    # nothing at all, which is the loudest possible failure reading as a pass.
    assert "<!-- specs/1788229400-later -->" in text, text
    assert "<!-- specs/1700000000-earlier -->" in text, text
    assert "1788300000-empty" not in text, text


# --- this repository --------------------------------------------------------


def test_the_release_pull_request_runs_the_check():
    """A convention nothing enforces is a convention somebody forgets at the
    release, which is the last moment anyone is looking."""
    workflow = read(".github", "workflows", "hygiene.yml")
    assert "gather_changelog.py --check" in workflow, (
        "the release workflow does not check the fragments"
    )
    assert os.path.isfile(SCRIPT), "the workflow calls a script that is not there"


def test_the_check_only_runs_for_a_release():
    """On a feature pull request every fragment on the branch is legitimately
    ungathered — running it there would fail every branch that writes one."""
    workflow = read(".github", "workflows", "hygiene.yml")
    step = workflow.split("every changelog fragment reached the released file")[1]
    step = step.split("- name:")[0]
    assert 'github.base_ref }}" != "main"' in step, (
        "the step no longer skips itself outside a release pull request"
    )


def test_the_accumulation_section_no_longer_exists():
    """`## Unreleased` is what the fragments replace.

    A heading by that name means somebody went back to appending to the shared
    file, which is the whole defect. `test_release_hygiene.py` used to check
    that it sat above every dated section; there is no longer one to place.
    """
    headings = re.findall(r"^## (.+)$", read("CHANGELOG.md"), re.M)
    unreleased = [h for h in headings if h.lower().startswith("unreleased")]
    assert not unreleased, (
        f"CHANGELOG.md has {unreleased} again. An entry goes in "
        "seal/specs/<work-item-id>/changelog.md, and the release gathers them"
    )


def test_the_documents_send_a_change_to_its_own_fragment():
    """Three documents decide where an entry goes, and a reader stops at the
    first one that answers. All three have to say the same thing."""
    for parts in (
        ("CONTRIBUTING.md",),
        ("docs", "branch-and-release.md"),
        ("CLAUDE.md",),
    ):
        text = flat(*parts)
        assert "seal/specs/<work-item-id>/changelog.md" in text, (
            "/".join(parts) + " does not name the file a change writes"
        )


def test_the_release_sequence_names_the_gather_step():
    """The sequence in `docs/branch-and-release.md` is walked by whoever cuts
    a release. A step that is only in a workflow comment is a step that gets
    discovered by a red build."""
    doc = flat("docs", "branch-and-release.md")
    assert "gather_changelog.py" in doc, (
        "the release sequence does not name the script that gathers the entries"
    )
    # The PRESCRIPTIONS, not the word. Saying what `## Unreleased` used to be
    # is what a reader arriving from the old rule needs; telling them to write
    # into it, or to rename it at the release, is the thing that has to be
    # gone. Both spellings below were in this document.
    for old_rule in (
        "put their entry under `## Unreleased`",
        "renames `## Unreleased`",
        "Renaming `## Unreleased`",
    ):
        assert old_rule not in doc, f"the sequence still says: {old_rule}"
    assert "There is no accumulation section any more" in doc, (
        "the document leaves a reader who knows the old rule to work out on "
        "their own that the heading is gone rather than moved"
    )


def test_this_work_item_wrote_its_own_fragment():
    """Dogfood. A convention the branch introducing it did not follow is one
    nobody has tried.

    Once the work item is released and retired, the fragment is gone and
    the marker `gather_changelog.py` wrote above its body is the proof it
    existed — a hand edit of `CHANGELOG.md` leaves no marker behind."""
    item = "1788229400-every-branch-appends-to-the-same-two-files"
    frag = os.path.join(ROOT, "seal", "specs", item, "changelog.md")
    if os.path.isfile(frag):
        with open(frag, encoding="utf-8") as f:
            assert f.read().strip(), "the fragment is empty"
        return
    body = gathered_entry(ROOT, item)
    assert body is not None, "this work item edited CHANGELOG.md instead"
    assert body.strip(), "the gathered fragment is empty"


def test_a_gathered_body_line_opening_with_an_issue_number_is_kept(tmp_path):
    """#497 round 1 ⬜ 8. The block ends at the next marker or heading, and a
    heading is `#` and then a space; a body line wrapped onto `#120` is the
    entry's own sentence, and cutting it there reads as a shorter entry."""
    (tmp_path / "CHANGELOG.md").write_text(
        "## [1.0.0]\n\n<!-- specs/1799000000-an-item -->\n- **A thing changed**, per\n"
        "#120, and the rest of it.\n\n## [0.9.0]\n- an older entry\n",
        encoding="utf-8",
    )
    body = gathered_entry(str(tmp_path), "1799000000-an-item")
    assert "#120, and the rest of it." in body, body
    assert "an older entry" not in body, body


# --- the check after a fold ------------------------------------------------


def test_the_check_says_how_many_markers_it_read(tree):
    """A2, the half that is a report. `--check` judged only by the fragments
    on disk, so its one success line said nothing about the file it is
    checking against. `fold_ledger.py --check` has printed both numbers since
    it shipped; this is the sibling catching up."""
    gather(tree)
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout
    assert "2 work items marked in CHANGELOG.md" in r.stdout, r.stdout


def test_a_corpus_with_no_fragment_and_no_marker_is_not_a_pass(tmp_path):
    """A2. After `settle` removes a released work item's directory the
    fragment glob goes empty, and an empty glob means every fragment reached
    the file — so the check passed having examined nothing, which reads as
    *all gathered*.

    That is the silent direction `unverified_check.py`'s own docstring argues
    against one file over: a tolerant reader reports zero and zero is
    indistinguishable from success. So the check judges by the markers the
    file carries, and a corpus with neither is refused rather than passed."""
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n## 0.1.0 — 2026-09-01\n\n- an entry with no marker\n",
        encoding="utf-8",
    )
    r = run("--check", root=tmp_path)
    assert r.returncode == 1, r.stdout
    assert "examined nothing" in r.stdout, r.stdout


def test_a_folded_corpus_still_passes_on_its_markers(tmp_path):
    """The other half, and the one that makes the fold possible at all: every
    fragment has been gathered and every directory has been retired, so there
    is nothing left on disk and the file carries the record of all of it."""
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n## 0.1.0 — 2026-09-01\n\n"
        "<!-- specs/1700000000-earlier -->\n- the earlier one\n\n"
        "<!-- specs/1788229400-later -->\n- the later one\n",
        encoding="utf-8",
    )
    r = run("--check", root=tmp_path)
    assert r.returncode == 0, r.stdout
    assert "2 work items marked in CHANGELOG.md" in r.stdout, r.stdout


def test_a_marker_quoted_inline_is_not_a_gathered_work_item(tmp_path):
    """The count is line-anchored for the reason `fold_ledger.py#is_marked`
    already pays for: `CHANGELOG.md`'s own entries describe the convention,
    and a bare substring count read the description as a work item."""
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n## 0.1.0 — 2026-09-01\n\n"
        "- each entry carries `<!-- specs/<work-item-id> -->` above it\n",
        encoding="utf-8",
    )
    r = run("--check", root=tmp_path)
    assert r.returncode == 1, r.stdout
    assert "examined nothing" in r.stdout, r.stdout
