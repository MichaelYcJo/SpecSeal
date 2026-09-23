"""#386: the release note publishes itself, or the job goes red saying why.

Publishing a GitHub Release was a habit and nothing else, and three
consecutive releases skipped it. The repair is a workflow the tag push fires,
so the four directions that matter are the four this module holds:

  A1  a gathered `## X.Y.Z` section becomes the release note at that tag
  A2  a release already at the tag is left exactly as it is, exit 0
  A3  a tag with no changelog section goes RED, naming the tag and the file
  A4  the title is the `release: X.Y.Z — <symptoms>` line, and where no such
      line is readable it is the tag name and the log says which was used

**Nothing here reaches GitHub.** `gh` is replaced at the module's own `run`
and `release_exists`, following `tests/test_a_merged_ticket_says_so_on_the_tracker.py`'s
fake tracker — the calls are recorded as argument tuples, in order, so a case
can assert about a write that did NOT happen as well as one that did. Two of
the four scenarios are exactly that.

**The changelog is a fixture, and one case builds it with the real gatherer.**
`test_the_reader_reads_what_the_gatherer_writes` runs
`gather_changelog.py#section` and feeds its output to `publish_release_note.py`'s
reader. That is the whole link between the two scripts: the gatherer has no
section READER to import — it writes sections and locates the first `## ` line
to insert above — so a hand-written fixture would grade this module's idea of
the format rather than the format. If the gatherer's heading changes, that
case goes red at the seam instead of a release going out with empty notes.

**Shown red before it was committed (§15).** Each case was run against the
script with the one behaviour it pins removed, one at a time, and the
mutations and what each case said were recorded in
phase 1 of work item `1790076050-the-release-tail-is-three-acts-no-document-names`,
whose rule `docs/branch-and-release.md` §*Cutting a release* now carries.
"""

import importlib.util
import os

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(ROOT, ".github", "scripts")
SCRIPT = os.path.join(SCRIPTS, "publish_release_note.py")
GATHERER = os.path.join(SCRIPTS, "gather_changelog.py")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "publish-release.yml")

# `tests/test_release_hygiene.py` refuses a loaded document naming the running
# version or anything above it. These are illustrative, which is the form that
# document's own message points at.
VERSION = "1.2.3"
TAG = "v1.2.3"
REPO = "example/repo"
SYMPTOMS = "two acts nobody wrote down"
NOTES = "- **A thing that changed.** And what it changes for a reader."

CHANGELOG = f"""# Changelog

## {VERSION} — 2026-01-02

<!-- specs/1700000000-a-work-item -->
{NOTES}

## 1.2.2 — 2026-01-01

- the release before it, which must not reach the note
"""


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def publisher():
    return module(SCRIPT, "specseal_publish_release_note_for_tests")


def gatherer():
    return module(GATHERER, "specseal_gather_changelog_for_publish_tests")


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class Releases:
    """The releases a repository has, and every command the script ran.

    `calls` holds the argument tuples as the script passed them, in order, so
    a case can ask about absence — which is what A2 is entirely about.
    """

    def __init__(self, existing=()):
        self.existing = set(existing)
        self.calls = []

    def exists(self, repo, tag):
        return tag in self.existing

    def run(self, *args):
        self.calls.append(args)
        if args[:3] == ("gh", "release", "create"):
            self.existing.add(args[3])
            return ""
        if args[:2] == ("git", "log"):
            return self.message
        raise AssertionError(f"unexpected command: {args}")

    message = ""

    def creates(self):
        return [a for a in self.calls if a[:3] == ("gh", "release", "create")]


def wire(monkeypatch, tmp_path, changelog=CHANGELOG, message="", existing=(), **env):
    """The script, with a fixture changelog and no route to GitHub."""
    mod = publisher()
    tracker = Releases(existing)
    tracker.message = message
    (tmp_path / "CHANGELOG.md").write_text(changelog, encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", str(tmp_path))
    monkeypatch.setattr(mod, "run", tracker.run)
    monkeypatch.setattr(mod, "release_exists", tracker.exists)
    monkeypatch.setenv("TAG", env.pop("TAG", TAG))
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.delenv("DRY_RUN", raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return mod, tracker


def title_line(version=VERSION, symptoms=SYMPTOMS):
    """A tagged commit's message, in the shape this repository's history has.

    The subject is GitHub's, written by the merge button; the prescribed line
    is below it. That split is the measurement #386's own sentence got wrong,
    so the fixture carries it rather than a bare title line.
    """
    return f"Merge pull request #500 from owner/release/v{version}\n\nrelease: {version} — {symptoms}\n"


# --- A1: the section becomes the note --------------------------------------


def test_the_gathered_section_becomes_the_release_note(monkeypatch, tmp_path, capsys):
    """A1. The body is what the preparation commit already gathered, and only
    that version's section — a note carrying the release before it would be
    wrong in the one direction nobody re-reads."""
    mod, tracker = wire(monkeypatch, tmp_path, message=title_line())
    assert mod.main() == 0
    created = tracker.creates()
    assert len(created) == 1, tracker.calls
    args = created[0]
    assert args[3] == TAG
    body = args[args.index("--notes") + 1]
    assert NOTES in body
    assert "the release before it" not in body, (
        "the note carries the previous release's section too — the reader ran "
        "past the next `## ` heading"
    )
    assert f"## {VERSION}" not in body, (
        "the heading is in the body; it carries the date GitHub already shows"
    )
    assert "published the release" in capsys.readouterr().out


# --- A2: an existing note is never republished -----------------------------


def test_an_existing_release_is_left_exactly_as_it_is(monkeypatch, tmp_path, capsys):
    """A2. A re-pushed tag and a re-run job both land here. The note may have
    been edited by hand after publication, so the only safe act is none."""
    mod, tracker = wire(monkeypatch, tmp_path, message=title_line(), existing=(TAG,))
    assert mod.main() == 0
    assert tracker.calls == [], (
        "something ran against GitHub for a release that already exists"
    )
    assert "already exists" in capsys.readouterr().out


# --- A3: a missing section goes red ----------------------------------------


def test_a_tag_with_no_changelog_section_goes_red(monkeypatch, tmp_path, capsys):
    """A3. This is the release shipping unexplained, and the body is the whole
    of what the job publishes — so it is the one direction that fails."""
    mod, tracker = wire(
        monkeypatch,
        tmp_path,
        changelog="# Changelog\n\n## 1.2.2 — 2026-01-01\n\n- an older one\n",
        message=title_line(),
    )
    assert mod.main() == 1
    assert tracker.creates() == [], "it published a release with no notes"
    out = capsys.readouterr().out
    assert TAG in out and "CHANGELOG.md" in out, (
        "the message names neither the tag nor the file it looked in, so the "
        "job log does not say what to fix"
    )
    assert "gather_changelog.py" in out, (
        "the message does not name the command that writes the section"
    )


def test_a_tag_that_is_not_a_version_goes_red(monkeypatch, tmp_path, capsys):
    """A3's neighbour. `v*` matches `vnext` too, and a tag this cannot name a
    version for has no section to look for — so it says so instead of
    guessing one, the way `label_merged_on_release_branch.py` refuses a branch
    name it cannot read a version out of."""
    mod, tracker = wire(monkeypatch, tmp_path, TAG="vnext")
    assert mod.main() == 1
    assert tracker.calls == []
    assert "not a vX.Y.Z tag" in capsys.readouterr().out


# --- A4: where the title comes from, both branches -------------------------


def test_the_title_is_the_line_the_checklist_prescribes(monkeypatch, tmp_path, capsys):
    """A4, first branch. `docs/release-checklist.md` §5 prescribes
    `release: X.Y.Z — <symptoms>` for the release pull request, and the merge
    commit's BODY carries it — the subject is GitHub's own line."""
    mod, tracker = wire(monkeypatch, tmp_path, message=title_line())
    assert mod.main() == 0
    args = tracker.creates()[0]
    assert args[args.index("--title") + 1] == f"{VERSION} — {SYMPTOMS}"
    assert "the tagged commit's `release:` line" in capsys.readouterr().out, (
        "the log does not say which source the title came from, so a wrong "
        "title cannot be traced to the end that produced it"
    )


@pytest.mark.parametrize(
    "message",
    [
        pytest.param(
            "Merge pull request #500 from owner/release/v1.2.3\n", id="absent"
        ),
        # Measured in this repository's own history: v0.12.3's line carries no
        # symptoms. Reading a title out of it gives the version alone, which is
        # the tag name minus one character — so it is not the prescribed line
        # and takes the fallback rather than producing a near-duplicate.
        pytest.param(f"release: {VERSION}\n", id="no symptoms"),
        # A line for a different release, which a cherry-pick or a retag can
        # leave on the commit a tag names.
        pytest.param("release: 9.9.9 — somebody else's symptoms\n", id="wrong version"),
    ],
)
def test_without_that_line_the_title_is_the_tag_and_the_log_says_so(
    monkeypatch, tmp_path, capsys, message
):
    """A4, second branch. Nothing holds the commit-message convention, so a
    missing line falls back rather than failing: a wrong title is visible and
    fixable in one edit, where a failed job at the tag is a release that stops
    after `main` has already moved."""
    mod, tracker = wire(monkeypatch, tmp_path, message=message)
    assert mod.main() == 0
    args = tracker.creates()[0]
    assert args[args.index("--title") + 1] == TAG
    out = capsys.readouterr().out
    assert "the tag name" in out and "no `release:` line" in out, (
        "the fallback is silent, so a title nobody chose reads as one somebody did"
    )


# --- the seam with the script that writes the section ----------------------


def test_the_reader_reads_what_the_gatherer_writes(tmp_path):
    """The two scripts agree by construction rather than by a comment.

    `gather_changelog.py` has no section reader to import: it writes sections
    and finds the first `## ` line to insert above. So the reader here is new
    code, and what keeps it honest is being run against the real writer's
    output. A heading change in the gatherer fails here, at the seam, instead
    of publishing a release with empty notes.
    """
    gather = gatherer()
    block = gather.section(VERSION, "2026-01-02", [("1700000000-a-work-item", NOTES)])
    text = gather.insert(
        "# Changelog\n\n## 1.2.2 — 2026-01-01\n\n- older\n", block, VERSION
    )
    assert publisher().section_body(text, VERSION) is not None, (
        "the reader no longer recognises the section the gatherer writes, so "
        "every release would publish with no notes at all"
    )
    assert NOTES in publisher().section_body(text, VERSION)


# --- the workflow that runs it ---------------------------------------------


def workflow():
    """The workflow with its comment lines removed.

    A setting that exists only in a comment is not a setting —
    `tests/test_ci_gives_the_checks_what_they_need.py` measured that dropping
    a real line and keeping the comment above it left its checks green.
    """
    return "\n".join(
        line
        for line in read(WORKFLOW).splitlines()
        if not line.lstrip().startswith("#")
    )


def test_the_workflow_fires_on_the_tag_and_writes_nothing_else():
    """The trigger is the whole design decision. Hanging this from the push to
    `main` would put it before the tag exists, so the job would have to create
    one — and `docs/branch-and-release.md` says the tag is the maintainer's."""
    text = workflow()
    assert "tags: ['v*']" in text, "the workflow no longer fires on a tag push"
    assert "branches:" not in text, (
        "this fires on a branch push as well; at the push to `main` the tag "
        "does not exist yet and the job would have to create it"
    )
    assert "contents: write" in text
    for scope in ("issues:", "pull-requests:", "packages:"):
        assert scope not in text, f"the job declares {scope}, which it does not use"
    assert "publish_release_note.py" in text


def test_the_workflow_is_not_a_step_of_the_release_job():
    """`tests/test_the_gate_names_every_step_ci_runs.py` partitions every step
    of `hygiene.yml`'s `release` job against `broad_gate.py`'s arms. This is a
    workflow of its own, on a different trigger, and adding a step there
    instead would have grown that partition for a job nothing local can run."""
    hygiene = read(os.path.join(ROOT, ".github", "workflows", "hygiene.yml"))
    assert "publish_release_note.py" not in hygiene
