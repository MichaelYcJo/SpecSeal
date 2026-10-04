"""A change writes a changelog fragment; the release gathers them.

Issue #46. Three branches ran in parallel on 2026-09-01, touched 34 files, and
shared exactly one — the changelog, in all three pairs. Nothing else
overlapped at all, so parallel work was never the thing that conflicted:
appending to one three-line region was.

What made it worth fixing is when the conflict arrives. `CONTRIBUTING.md` and
the `verify` skill both say nothing may be edited between the broad gate and
the pull request, so resolving a changelog conflict costs a second run of the
whole broad gate. Two of the three branches paid that or were about to.

The fix is one fragment per work item, gathered at release. This file holds
the gathering — that it happens, that it happens once, and that a release
pull request cannot go out with a fragment left behind.

Since #728 a release is a file of its own, `changelog/X.Y.Z.md`, and
`CHANGELOG.md` is the index heading each one with a link to it. The fixtures
here are laid out that way, and the cases under *this repository* hold the
real tree to it.
"""

import os
import re
import subprocess
import sys

import pytest
from conftest import gathered_entry, workflow_step

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


INDEX_HEAD = "# Changelog\n\nThe index.\n\n"


def entry(heading, version):
    """One release's entry in the index, as the gather writes it."""
    return f"{heading}\n\n[changelog/{version}.md](changelog/{version}.md)\n"


def lay_out(root, *sections):
    """`root` in the released layout: each section, heading line first, as
    `changelog/<version>.md`, and an index heading them in the order given."""
    (root / "changelog").mkdir(exist_ok=True)
    entries = []
    for text in sections:
        heading = text.split("\n", 1)[0]
        version = heading.split()[1]
        (root / "changelog" / f"{version}.md").write_text(text, encoding="utf-8")
        entries.append(entry(heading, version))
    (root / "CHANGELOG.md").write_text(
        INDEX_HEAD + "\n".join(entries), encoding="utf-8"
    )


def snapshot(root):
    """Every file the gather may write, by path, so a run that must write
    nothing can be shown to have created nothing as well."""
    out = {"CHANGELOG.md": (root / "CHANGELOG.md").read_text(encoding="utf-8")}
    directory = root / "changelog"
    if directory.is_dir():
        for path in sorted(directory.iterdir()):
            out[f"changelog/{path.name}"] = path.read_text(encoding="utf-8")
    return out


@pytest.fixture
def tree(tmp_path):
    """A repository shape with one released file and two fragments."""
    lay_out(tmp_path, "## 0.1.0 — 2026-09-01\n\n- the first release\n")
    for work_item_id, body in (
        ("1788229400-later", "- **the later one.** What it changes.\n"),
        ("1700000000-earlier", "- **the earlier one.** What it changes.\n"),
    ):
        d = tmp_path / "seal" / "specs" / work_item_id
        d.mkdir(parents=True)
        (d / "changelog.md").write_text(body, encoding="utf-8")
    return tmp_path


def changelog(tree, version="0.2.0"):
    """The release's own file, or "" where the gather has not written it."""
    path = tree / "changelog" / f"{version}.md"
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def index(tree):
    return (tree / "CHANGELOG.md").read_text(encoding="utf-8")


def headings(text):
    return re.findall(r"^## (.+)$", text, re.M)


def gather(tree, version="0.2.0", date="2026-09-15"):
    """Run the gather and prove it actually gathered.

    Round 1, 🟡 9: three cases here ran the gather and then asserted something
    that a script consisting of `sys.exit(0)` also satisfies. A return code is
    not an effect — the marker landing in the file is — so every case that
    depends on a gather having happened goes through this. The release's own
    file is where the section and the marker land (#728).
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
    """A heading that lands below a dated one reads as older than work that
    already shipped — the state `test_unreleased_sits_above_every_dated_section`
    was written for, after a rebase resolved the wrong way. Since #728 the
    order is the index's, and the section itself is a file."""
    gather(tree)
    found = headings(index(tree))
    assert found == ["0.2.0 — 2026-09-15", "0.1.0 — 2026-09-01"], found


def test_a_gather_writes_the_release_file_and_its_index_entry(tree):
    """S4 of #728. The release's file is the section, heading first, each
    fragment under its marker in id order; the index gains the same heading
    line and the link to the file, above every older entry, and nothing else
    of the index moves."""
    r = gather(tree)
    assert changelog(tree) == (
        "## 0.2.0 — 2026-09-15\n\n"
        "<!-- specs/1700000000-earlier -->\n"
        "- **the earlier one.** What it changes.\n\n"
        "<!-- specs/1788229400-later -->\n- **the later one.** What it changes.\n"
    )
    assert index(tree) == (
        INDEX_HEAD
        + entry("## 0.2.0 — 2026-09-15", "0.2.0")
        + "\n"
        + entry("## 0.1.0 — 2026-09-01", "0.1.0")
    )
    out = " ".join(r.stdout.split())
    assert "into changelog/0.2.0.md, ## 0.2.0 — 2026-09-15" in out, out
    assert "CHANGELOG.md now heads its index with ## 0.2.0 — 2026-09-15" in out, out


def test_an_index_with_no_release_yet_takes_the_first_entry_below_its_text():
    """The first release a repository gathers meets an index with no `## `
    line to go above: the entry follows the index's own text after one blank
    line, and the file ends with one newline. An index that already heads
    the version is returned as it is."""
    gather_mod = load(SCRIPT, "specseal_gather_first_index_entry")
    text = gather_mod.indexed(INDEX_HEAD, "## 0.1.0 — d", "0.1.0")
    assert text == INDEX_HEAD + entry("## 0.1.0 — d", "0.1.0"), repr(text)
    assert gather_mod.indexed(text, "## 0.1.0 — e", "0.1.0") == text, (
        "an index that already heads the version took a second entry"
    )


def test_the_first_gather_creates_the_directory_and_the_first_entry(tmp_path):
    """A root with an index and no `changelog/` yet: the gather makes the
    directory, writes the release's file, and gives the index its first
    entry below the index's own text."""
    (tmp_path / "CHANGELOG.md").write_text(INDEX_HEAD, encoding="utf-8")
    d = tmp_path / "seal" / "specs" / "1700000000-earlier"
    d.mkdir(parents=True)
    (d / "changelog.md").write_text("- the earlier one\n", encoding="utf-8")
    r = run("--version", "0.1.0", "--date", "2026-09-01", root=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert changelog(tmp_path, "0.1.0") == (
        "## 0.1.0 — 2026-09-01\n\n<!-- specs/1700000000-earlier -->\n"
        "- the earlier one\n"
    )
    assert index(tmp_path) == INDEX_HEAD + entry("## 0.1.0 — 2026-09-01", "0.1.0")


def test_a_release_the_index_heads_without_its_file_keeps_the_index_date(tree):
    """A release file deleted by hand, or never staged, while the index kept
    its heading: the gather writes the file under the index's date, so the
    two copies of the heading stay one line, and the index is left as it is."""
    tree.joinpath("CHANGELOG.md").write_text(
        INDEX_HEAD
        + entry("## 0.2.0 — 2026-09-15", "0.2.0")
        + "\n"
        + entry("## 0.1.0 — 2026-09-01", "0.1.0"),
        encoding="utf-8",
    )
    listed = index(tree)
    r = run("--version", "0.2.0", "--date", "2026-09-16", root=tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert changelog(tree).startswith("## 0.2.0 — 2026-09-15\n\n"), changelog(tree)
    assert index(tree) == listed, index(tree)


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
    listed = index(tree)
    second = run("--version", "0.2.0", "--date", "2026-09-16", root=tree)
    assert second.returncode == 0, second.stdout + second.stderr
    text = changelog(tree)
    found = headings(text)
    assert found == ["0.2.0 — 2026-09-15"], (
        f"the second gather wrote a second heading, or re-dated the first: {found}"
    )
    # S5 of #728: the index already heads the release, so it takes no
    # second entry and its date stays the first gather's.
    assert index(tree) == listed, index(tree)
    assert "the late one" in text, text
    # Inside the section, after the entries the first gather wrote.
    assert text.index("the later one") < text.index("the late one"), text
    assert "<!-- specs/1788300001-late -->" in text, text
    # Round 1 of #536's work item (⬜ 2): the append arm re-joined the blank
    # lines it had walked back over. One blank line between two entries, as
    # the first gather writes them, no run of three newlines anywhere, and
    # one newline at the end of the file.
    assert "\n\n\n" not in text, f"a run of blank lines:\n{text}"
    assert text.endswith(
        "What it changes.\n\n<!-- specs/1788300001-late -->\n"
        "- **the late one.** A repair.\n"
    ), text
    check = run("--check", root=tree)
    assert check.returncode == 0, check.stdout
    assert "3 changelog fragments, all gathered" in check.stdout, check.stdout


def test_a_second_gather_into_the_last_section_ends_the_file_with_one_newline(
    tmp_path,
):
    """The other half of ⬜ 2: appending into the LAST section of a file
    left the file ending with three newlines. Every release file is its own
    last section now (#728)."""
    lay_out(
        tmp_path,
        "## 0.2.0 — 2026-09-15\n\n<!-- specs/1700000000-earlier -->\n"
        "- the earlier one\n",
    )
    d = tmp_path / "seal" / "specs" / "1788300001-late"
    d.mkdir(parents=True)
    (d / "changelog.md").write_text("- the late one\n", encoding="utf-8")
    r = run("--version", "0.2.0", "--date", "2026-09-16", root=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    text = changelog(tmp_path)
    assert text.endswith("- the late one\n"), repr(text[-40:])
    assert "\n\n\n" not in text, repr(text)


def test_a_second_gather_into_an_undated_heading_says_what_the_write_does(tmp_path):
    """⬜ 3: `existing_date` answered `None` for a heading with no date while
    `insert` appended into it, so the dry run printed a fresh heading dated
    today and the summary line said nothing about appending — and the write
    appended anyway. One predicate answers *is there a section* for both.
    The gatherer never writes an undated heading; a hand edit does."""
    lay_out(tmp_path, "## 0.2.0\n\n- an entry somebody wrote by hand\n")
    listed = index(tmp_path)
    d = tmp_path / "seal" / "specs" / "1788300001-late"
    d.mkdir(parents=True)
    (d / "changelog.md").write_text("- the late one\n", encoding="utf-8")
    dry = run("--version", "0.2.0", "--date", "2026-09-16", "--dry-run", root=tmp_path)
    assert dry.returncode == 0, dry.stdout
    assert "appending into the existing section" in dry.stdout, dry.stdout
    assert "2026-09-16" not in dry.stdout, dry.stdout
    r = run("--version", "0.2.0", "--date", "2026-09-16", root=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "appended into the existing section" in r.stdout, r.stdout
    assert headings(changelog(tmp_path)) == ["0.2.0"], changelog(tmp_path)
    assert index(tmp_path) == listed, index(tmp_path)


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
    before = snapshot(tree)
    r = run("--version", "0.2.0", "--date", "2026-09-16", "--dry-run", root=tree)
    assert r.returncode == 0, r.stdout
    assert "## 0.2.0 — 2026-09-15" in r.stdout, r.stdout
    assert "2026-09-16" not in r.stdout, r.stdout
    assert snapshot(tree) == before, "--dry-run wrote to a file"


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
    (tree / "changelog" / "0.2.0.md").write_text(text, encoding="utf-8")
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
    (tree / "changelog" / "0.2.0.md").write_text(text, encoding="utf-8")
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "1788229400-later" in r.stdout, r.stdout


def test_dry_run_writes_nothing(tree):
    """The precedent is `close_issues_on_release.py`'s `DRY_RUN`, which exists
    because that script was run by hand for its output during development and
    closed a real issue. S6 of #728: neither the index nor anything under
    `changelog/` changes, and no release file is created."""
    before = snapshot(tree)
    r = run("--version", "0.2.0", "--date", "2026-09-15", "--dry-run", root=tree)
    assert r.returncode == 0, r.stdout
    assert "## 0.2.0 — 2026-09-15" in r.stdout
    assert "into changelog/0.2.0.md" in r.stdout, r.stdout
    assert snapshot(tree) == before, "--dry-run wrote to a file"


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
    step = workflow_step(workflow, "every changelog fragment reached the released file")
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


VERSION_NAME = re.compile(r"^(\d+)\.(\d+)\.(\d+)\.md$")


def release_files_on_disk():
    """`[(version, text)]` for every `changelog/<X.Y.Z>.md` in the working
    tree, newest first. Listed from the disk, not from `git ls-files`: a
    release preparation runs the suite before the new file is staged (#728,
    spec D9), and an index line whose file the listing missed would read as
    a file that is not there."""
    directory = os.path.join(ROOT, "changelog")
    found = []
    for name in os.listdir(directory):
        parts = VERSION_NAME.match(name)
        if parts:
            with open(os.path.join(directory, name), encoding="utf-8") as f:
                found.append((tuple(map(int, parts.groups())), name[:-3], f.read()))
    return [(version, text) for _, version, text in sorted(found, reverse=True)]


def test_the_index_and_the_release_files_agree():
    """S2 of #728. Each `changelog/<v>.md` opens with its one `## ` line,
    naming `<v>`; `CHANGELOG.md` carries that same line once per file, newest
    first, each followed by the link to its file, and no other `## ` line.
    The heading lives in both places on purpose (spec D2), and this is what
    keeps the two copies one line."""
    files = release_files_on_disk()
    assert len(files) >= 44, f"{len(files)} release files — this case is blind"
    want = []
    for version, text in files:
        lines = text.split("\n")
        sections = [line for line in lines if line.startswith("## ")]
        assert sections == [lines[0]], (
            f"changelog/{version}.md has {sections} as its `## ` lines; a "
            "release file opens with its one heading and carries no other"
        )
        assert re.match(rf"## {re.escape(version)} — \S+$", lines[0]), lines[0]
        assert text.endswith("\n") and not text.endswith("\n\n"), (
            f"changelog/{version}.md does not end with exactly one newline"
        )
        want.append(f"{lines[0]}\n\n[changelog/{version}.md](changelog/{version}.md)")
    index = read("CHANGELOG.md")
    at = index.index("\n## ")
    assert "\n\n".join(want) + "\n" == index[at + 1 :], (
        "CHANGELOG.md's entries are not the release files' headings, newest "
        "first, each with the link to its file. The gather writes both: "
        "`gather_changelog.py --version X.Y.Z`"
    )


def test_the_documents_send_a_change_to_its_own_fragment():
    """Where an entry goes is decided in one home since #715,
    `docs/the-record-layout.md`, beside the release sequence that gathers it;
    `CONTRIBUTING.md` and `CLAUDE.md`, where a reader stops first, send the
    reader there by name rather than saying it a third and fourth time."""
    for parts in (("docs", "the-record-layout.md"), ("docs", "branch-and-release.md")):
        text = flat(*parts)
        assert "seal/specs/<work-item-id>/changelog.md" in text, (
            "/".join(parts) + " does not name the file a change writes"
        )
    for parts in (("CONTRIBUTING.md",), ("CLAUDE.md",)):
        assert "docs/the-record-layout.md" in flat(*parts), (
            "/".join(parts) + " does not send the reader to the fragment rule's home"
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
    existed — a hand edit of the released notes leaves no marker behind."""
    item = "1788229400-every-branch-appends-to-the-same-two-files"
    frag = os.path.join(ROOT, "seal", "specs", item, "changelog.md")
    if os.path.isfile(frag):
        with open(frag, encoding="utf-8") as f:
            assert f.read().strip(), "the fragment is empty"
        return
    body = gathered_entry(ROOT, item)
    assert body is not None, "this work item edited the released notes instead"
    assert body.strip(), "the gathered fragment is empty"


def test_a_gathered_body_line_opening_with_an_issue_number_is_kept(tmp_path):
    """#497 round 1 ⬜ 8. The block ends at the next marker or heading, and a
    heading is `#` and then a space; a body line wrapped onto `#120` is the
    entry's own sentence, and cutting it there reads as a shorter entry."""
    (tmp_path / "changelog").mkdir()
    (tmp_path / "changelog" / "1.0.0.md").write_text(
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
    assert "2 work items marked in changelog/" in r.stdout, r.stdout


def test_the_check_reads_the_markers_of_every_release_file(tmp_path):
    """S7 of #728. The markers are spread over the release files, and the
    check counts them all; a fragment whose marker stands in none of them is
    named, in the sentence that says where it should have gone."""
    lay_out(
        tmp_path,
        "## 0.2.0 — 2026-09-15\n\n<!-- specs/1788229400-later -->\n- later\n\n"
        "<!-- specs/1788229500-latest -->\n- latest\n",
        "## 0.1.0 — 2026-09-01\n\n<!-- specs/1700000000-earlier -->\n- earlier\n",
    )
    (tmp_path / "changelog" / "README.md").write_text(
        "<!-- specs/1600000000-not-a-release -->\n", encoding="utf-8"
    )
    gather_mod = load(SCRIPT, "specseal_gather_release_files")
    listed = [v for v, _ in gather_mod.release_files(str(tmp_path))]
    assert listed == ["0.2.0", "0.1.0"], listed
    r = run("--check", root=tmp_path)
    assert r.returncode == 0, r.stdout
    out = " ".join(r.stdout.split())
    want = "0 changelog fragments, all gathered; 3 work items marked in changelog/"
    assert want in out, out
    d = tmp_path / "seal" / "specs" / "1788300001-left"
    d.mkdir(parents=True)
    (d / "changelog.md").write_text("- left behind\n", encoding="utf-8")
    r = run("--check", root=tmp_path)
    assert r.returncode == 1, r.stdout
    out = " ".join(r.stdout.split())
    assert "changelog fragments that never reached a file under changelog/:" in out
    assert "seal/specs/1788300001-left/changelog.md" in out, out


def test_a_block_one_release_file_leaves_open_hides_nothing_in_another(tmp_path):
    """Each release file is read on its own. Read as one text, a fence the
    newer file never closed would hide every marker of the older one."""
    lay_out(
        tmp_path,
        "## 0.2.0 — 2026-09-15\n\n<!-- specs/1788229400-later -->\n- later\n\n"
        "```\nan example nobody closed\n",
        "## 0.1.0 — 2026-09-01\n\n<!-- specs/1700000000-earlier -->\n- earlier\n",
    )
    r = run("--check", root=tmp_path)
    assert r.returncode == 0, r.stdout
    assert "2 work items marked in changelog/" in r.stdout, r.stdout


def test_a_corpus_with_no_fragment_and_no_marker_is_not_a_pass(tmp_path):
    """A2. After `settle` removes a released work item's directory the
    fragment glob goes empty, and an empty glob means every fragment reached
    the file — so the check passed having examined nothing, which reads as
    *all gathered*.

    That is the silent direction `unverified_check.py`'s own docstring argues
    against one file over: a tolerant reader reports zero and zero is
    indistinguishable from success. So the check judges by the markers the
    release files carry, and a corpus with neither is refused rather than
    passed."""
    lay_out(tmp_path, "## 0.1.0 — 2026-09-01\n\n- an entry with no marker\n")
    r = run("--check", root=tmp_path)
    assert r.returncode == 1, r.stdout
    out = " ".join(r.stdout.split())
    assert "examined nothing" in out, out
    want = "no <!-- specs/<work-item-id> --> marker in any changelog/<X.Y.Z>.md"
    assert want in out, out


def test_a_folded_corpus_still_passes_on_its_markers(tmp_path):
    """The other half, and the one that makes the fold possible at all: every
    fragment has been gathered and every directory has been retired, so there
    is nothing left on disk and the release files carry the record of all of
    it."""
    lay_out(
        tmp_path,
        "## 0.1.0 — 2026-09-01\n\n"
        "<!-- specs/1700000000-earlier -->\n- the earlier one\n\n"
        "<!-- specs/1788229400-later -->\n- the later one\n",
    )
    r = run("--check", root=tmp_path)
    assert r.returncode == 0, r.stdout
    assert "2 work items marked in changelog/" in r.stdout, r.stdout


def test_a_marker_quoted_inline_is_not_a_gathered_work_item(tmp_path):
    """The count is line-anchored for the reason `fold_ledger.py#is_marked`
    already pays for: the released entries describe the convention, and a
    bare substring count read the description as a work item."""
    lay_out(
        tmp_path,
        "## 0.1.0 — 2026-09-01\n\n"
        "- each entry carries `<!-- specs/<work-item-id> -->` above it\n",
    )
    r = run("--check", root=tmp_path)
    assert r.returncode == 1, r.stdout
    assert "examined nothing" in r.stdout, r.stdout


# --- #584: a marker counts only on a live line --------------------------------

QUOTED_MARKER = {
    "fenced": "An entry quoting the marker:\n\n```\n<!-- specs/1788229400-later -->\n```\n",
    "inline": "- this entry names `<!-- specs/1788229400-later -->` in prose\n",
    "commented": "<!-- a draft entry\n<!-- specs/1788229400-later -->\n-->\n",
}


def quoting(tree, shape):
    """The fixture's file with the earlier work item gathered for real and
    the later one's marker only quoted, in `shape`."""
    lay_out(
        tree,
        "## 0.1.0 — 2026-09-01\n\n"
        "<!-- specs/1700000000-earlier -->\n- the earlier one\n\n"
        + QUOTED_MARKER[shape],
    )


@pytest.mark.parametrize("shape", sorted(QUOTED_MARKER))
def test_a_quoted_marker_gathers_nothing(tree, shape):
    """#584, S6. `ungathered` was a substring test, so a marker quoted in a
    fenced example, in prose or in a commented-out draft marked its fragment
    gathered, and `--check` passed a release that never shipped the entry.
    Its count was line-anchored and still read the fenced and commented
    shapes. A marker counts only on a live line
    (`docs/the-evidence-ledger.md` §*A marker counts only on a live line*)."""
    quoting(tree, shape)
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "seal/specs/1788229400-later/changelog.md" in r.stdout, r.stdout
    assert "seal/specs/1700000000-earlier/changelog.md" not in r.stdout, r.stdout


def test_a_quoted_marker_is_not_counted(tree):
    """#584, S6's count. `--check`'s success line counted every
    line-anchored marker, so a fenced or commented quotation of one counted
    as a work item that was gathered."""
    gather(tree)
    (tree / "changelog" / "0.2.0.md").write_text(
        changelog(tree) + "\n" + QUOTED_MARKER["fenced"] + "\n"
        "<!-- a draft\n<!-- specs/1700000000-earlier -->\n-->\n",
        encoding="utf-8",
    )
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout
    assert "2 work items marked in changelog/" in r.stdout, r.stdout


def load(path, name):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("shape", sorted(QUOTED_MARKER))
def test_the_gather_and_the_survivor_check_read_one_set_of_markers(
    tree, shape, monkeypatch
):
    """#584, S7. `survivor_check.py#gathered_fragments` excuses a gathered
    fragment from its sweep, and it reads the released markers through
    `live_lines`. The gather reading the same file by another rule is two
    answers to *was this entry shipped*."""
    quoting(tree, shape)
    text = changelog(tree, "0.1.0")
    gather_mod = load(SCRIPT, "specseal_gather_changelog")
    survivor = load(
        os.path.join(ROOT, "skills", "code-review", "scripts", "survivor_check.py"),
        "specseal_survivor_check",
    )
    monkeypatch.setattr(
        survivor, "read_blobs", lambda root, rev, paths: {p: text for p in paths}
    )
    frags = gather_mod.fragments(str(tree))
    missing = {
        i for i, _ in gather_mod.ungathered(gather_mod.live_markers(text), frags)
    }
    gathered = {i for i, _ in frags} - missing
    paths = ["changelog/0.1.0.md"]
    assert gathered == survivor.gathered_fragments(str(tree), "HEAD", paths)
    assert gathered == {"1700000000-earlier"}


# --- #586: a fragment's own `## ` line ends the released section -------------

HEADED = "1788250000-headed"


def headed(tree, body):
    """A third fragment, between the fixture's two in id order."""
    d = tree / "seal" / "specs" / HEADED
    d.mkdir(parents=True)
    (d / "changelog.md").write_text(body, encoding="utf-8")


@pytest.mark.parametrize("dry_run", [False, True])
def test_a_fragment_carrying_its_own_section_line_is_refused(tree, dry_run):
    """S9. The gatherer ends a section at the next line starting `## `, and so
    does `publish_release_note.py#section_body`. A fragment carrying one
    would ship every entry after it under no version and cut the release
    note short, so the gather refuses before it writes or prints a section,
    naming the fragment, the line number and the line, and what to do."""
    headed(tree, "- **an entry.** What it changes.\n\n## A heading of its own\n")
    before = snapshot(tree)
    args = ["--version", "0.2.0", "--date", "2026-09-15"]
    r = run(*args, *(["--dry-run"] if dry_run else []), root=tree)
    assert r.returncode == 1, r.stdout + r.stderr
    assert snapshot(tree) == before, "the refused gather wrote to a file"
    assert "## 0.2.0" not in r.stdout, "the refused gather printed a section"
    out = " ".join(r.stdout.split())
    assert f"seal/specs/{HEADED}/changelog.md:3: ## A heading of its own" in out, out
    assert "Demote each to `###` or lower" in out, out
    assert "a pull request into the release branch, then gather again" in out, out


@pytest.mark.parametrize(
    "line",
    ["### a subheading", "##", "  ## indented", "#### deeper", "##no space"],
)
def test_a_line_that_ends_no_section_is_gathered(tree, line):
    """S10. The refusal is exactly the predicate both release readers end a
    section with, `line.startswith("## ")`, and nothing wider: a deeper
    heading, a bare `##` and an indented one end no section there."""
    headed(tree, f"- **an entry.** What it changes.\n\n{line}\n")
    gather(tree)
    assert f"<!-- specs/{HEADED} -->" in changelog(tree)


def test_a_section_line_inside_a_fence_is_refused_too(tree):
    """Neither release reader knows a fence, so a `## ` line inside one ends
    their section all the same, and it is refused all the same."""
    headed(tree, "- **an entry.**\n\n  ```\n## inside a fence\n  ```\n")
    r = run("--version", "0.2.0", "--date", "2026-09-15", root=tree)
    assert r.returncode == 1, r.stdout
    assert f"seal/specs/{HEADED}/changelog.md:4: ## inside a fence" in r.stdout


def test_a_gathered_fragment_is_not_refused_again(tree):
    """Only what this run would gather is read. A fragment already in the
    file cannot be un-shipped by refusing the release."""
    gather(tree)
    (tree / "seal" / "specs" / "1788229400-later" / "changelog.md").write_text(
        "- **the later one.**\n\n## edited after it shipped\n", encoding="utf-8"
    )
    d = tree / "seal" / "specs" / "1788300001-next"
    d.mkdir(parents=True)
    (d / "changelog.md").write_text("- **the next one.**\n", encoding="utf-8")
    r = run("--version", "0.3.0", "--date", "2026-09-16", root=tree)
    assert r.returncode == 0, r.stdout


LEFT_OPEN = {
    "fence": "- **an entry.** It quotes:\n\n```\na block nobody closed\n",
    "comment": "- **an entry.** It mentions a bare " + "<" + "!--" + " in prose.\n",
}


@pytest.mark.parametrize("dry_run", [False, True])
@pytest.mark.parametrize("shape", sorted(LEFT_OPEN))
def test_a_fragment_that_leaves_a_block_open_is_refused(tree, shape, dry_run):
    """#584 round 1, finding 1; phase 9 of work item 1790635413. `section`
    writes each fragment verbatim and the next marker below it, and `insert`
    puts every older section below that. A fragment that opens a fenced block
    or an HTML comment and never closes it put all of those markers on lines
    `live_markers` cannot see: the gather exited 0, `--check` then called the
    entry below it missing, and the gather it advised wrote that entry a
    second time. Refused before anything is written or printed, beside the
    #586 refusal, naming the fragment."""
    headed(tree, LEFT_OPEN[shape])
    before = snapshot(tree)
    args = ["--version", "0.2.0", "--date", "2026-09-15"]
    r = run(*args, *(["--dry-run"] if dry_run else []), root=tree)
    assert r.returncode == 1, r.stdout + r.stderr
    assert snapshot(tree) == before, "the refused gather wrote to a file"
    assert "## 0.2.0" not in r.stdout, "the refused gather printed a section"
    out = " ".join(r.stdout.split())
    assert f"seal/specs/{HEADED}/changelog.md" in out, out
    assert "never close" in out and "Nothing was written" in out, out
    assert "seal/specs/1788229400-later/changelog.md" not in out, out


def test_a_fragment_that_closes_what_it_opens_is_gathered(tree):
    """The other half, so the refusal cannot pass by refusing everything: a
    fenced block and a comment that both close leave the next marker live."""
    headed(
        tree,
        "- **an entry.** It quotes:\n\n```\na block\n```\n\n"
        + "<"
        + "!-- a note -->\n",
    )
    gather(tree)
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout
    assert "3 work items marked in changelog/" in r.stdout, r.stdout


def test_the_documents_say_a_fragment_carries_no_section_line():
    """S11 for #586: the fragment convention's home and the house rule a
    session meets when it writes one both say it, and the module docstring
    lists the exit."""
    for parts in (("docs", "branch-and-release.md"), ("docs", "the-record-layout.md")):
        text = flat(*parts)
        assert "no line starting `## `" in text, "/".join(parts)
    head = flat(".github", "scripts", "gather_changelog.py").split('"""')[1]
    assert "a fragment carries a line starting `## `" in head, head
