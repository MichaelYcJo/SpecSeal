"""#386: the release note publishes itself, or the job goes red saying why.

Publishing a GitHub Release was a habit and nothing else, and three
consecutive releases skipped it. The repair is a workflow the tag push fires,
so the four directions that matter are the four this module holds:

  A1  a gathered `## X.Y.Z` section becomes the release note at that tag
  A2  a release already at the tag is left exactly as it is, exit 0
  A3  a tag with no release file goes RED, naming the tag and the file
  A4  the title is the `release: X.Y.Z — <symptoms>` line, and where no such
      line is readable it is the tag name and the log says which was used
  A5  the note is a summary read from the release's pull requests -- counts,
      one line per change under its type with the issues it closed, every
      outside contributor thanked by handle -- over the gathered section,
      folded; with no pull request to read it is the section alone (#572)

**Nothing here reaches GitHub.** `gh` is replaced at the module's own `run`
and `release_exists`, following `tests/test_a_merged_ticket_says_so_on_the_tracker.py`'s
fake tracker — the calls are recorded as argument tuples, in order, so a case
can assert about a write that did NOT happen as well as one that did. Two of
the four scenarios are exactly that.

**The release's own file is a fixture, `changelog/X.Y.Z.md` since #728, and
one case builds it with the real gatherer.**
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

# The release's own file, as the gather writes it (#728).
RELEASE_FILE = f"""## {VERSION} — 2026-01-02

<!-- specs/1700000000-a-work-item -->
{NOTES}
"""

# The release before it, in a file of its own, which must not reach the note.
OLDER_FILE = "## 1.2.2 — 2026-01-01\n\n- the release before it\n"


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


def wire(
    monkeypatch,
    tmp_path,
    changelog=RELEASE_FILE,
    message="",
    existing=(),
    pulls=(),
    **env,
):
    """The script, with fixture release files and no route to GitHub.
    `changelog` is the tagged release's own file; None leaves it out."""
    mod = publisher()
    monkeypatch.setattr(
        mod,
        "merged_pulls",
        lambda repo, version: None if pulls is None else list(pulls),
    )
    tracker = Releases(existing)
    tracker.message = message
    (tmp_path / "changelog").mkdir(exist_ok=True)
    (tmp_path / "changelog" / "1.2.2.md").write_text(OLDER_FILE, encoding="utf-8")
    if changelog is not None:
        (tmp_path / "changelog" / f"{VERSION}.md").write_text(
            changelog, encoding="utf-8"
        )
    monkeypatch.setattr(mod, "ROOT", str(tmp_path))
    monkeypatch.setattr(mod, "run", tracker.run)
    monkeypatch.setattr(mod, "release_exists", tracker.exists)
    monkeypatch.setenv("TAG", env.pop("TAG", TAG))
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.delenv("DRY_RUN", raising=False)
    # A run on CI has its own step's output file here; a case that wants one
    # names its own (S4 of work item 1790993139).
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
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


@pytest.mark.parametrize(
    "changelog",
    [
        pytest.param(None, id="no release file"),
        pytest.param("## 1.2.2 — 2026-01-01\n\n- misfiled\n", id="no heading"),
    ],
)
def test_a_tag_with_no_changelog_section_goes_red(
    monkeypatch, tmp_path, capsys, changelog
):
    """A3. This is the release shipping unexplained, and the body is the whole
    of what the job publishes — so it is the one direction that fails. S9 of
    #728: the file it names is the release's own, `changelog/X.Y.Z.md`."""
    mod, tracker = wire(
        monkeypatch, tmp_path, changelog=changelog, message=title_line()
    )
    assert mod.main() == 1
    assert tracker.creates() == [], "it published a release with no notes"
    out = capsys.readouterr().out
    assert TAG in out and f"changelog/{VERSION}.md" in out, (
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


# --- A5: the note is a summary over the section --------------------------


def pull(number, login, title="docs: a sentence", body="", is_bot=False):
    return {
        "number": number,
        "title": title,
        "body": body,
        "author": {"login": login, "is_bot": is_bot},
    }


OWNER = REPO.split("/")[0]

RELEASE = [
    pull(9, OWNER, f"chore: release {VERSION} — the gathering", "Closes #1"),
    pull(10, OWNER, "fix: the owner's own change", "Closes #100 and fixes #101"),
    pull(11, "someone", "docs: explain a thing", "Closes #102"),
    pull(12, "dependabot[bot]", "chore: bump", is_bot=True),
    pull(13, "app/renovate", "chore: bump again"),
    pull(14, "someone", "fix(gate): and a second thing (#103)", "Closes #103"),
    pull(15, "another", "feat: a third", "Quotes `Closes #999` and closes #100"),
    pull(16, OWNER, "an untyped title"),
]


def body_of(tracker):
    args = tracker.creates()[0]
    return args[args.index("--notes") + 1]


def published(monkeypatch, tmp_path, pulls):
    mod, tracker = wire(monkeypatch, tmp_path, message=title_line(), pulls=pulls)
    assert mod.main() == 0
    return mod, body_of(tracker)


def lines_under(body, heading):
    """The `- ` lines between `heading` and the next heading or fold."""
    rest = body[body.index(heading) + len(heading) :]
    out = []
    for line in rest.splitlines()[1:]:
        if line.startswith(("### ", "<details>")):
            break
        if line.startswith("- "):
            out.append(line)
    return out


def test_every_change_is_one_line_under_its_type(monkeypatch, tmp_path):
    """A5. The list is a partition of the release: every pull request but the
    preparation lands under exactly one heading, an unknown or missing type
    under Other, and each line names the issues its body closes -- read the
    way the closer reads them, so a quoted keyword closes nothing."""
    _, body = published(monkeypatch, tmp_path, RELEASE)
    assert lines_under(body, "### 🐛 Fixes") == [
        "- The owner's own change (#10) · closes #100, #101",
        "- And a second thing (#14) · closes #103 — thanks @someone",
    ]
    assert lines_under(body, "### ✨ Features") == [
        "- A third (#15) · closes #100 — thanks @another"
    ]
    assert lines_under(body, "### 📚 Docs") == [
        "- Explain a thing (#11) · closes #102 — thanks @someone"
    ]
    assert lines_under(body, "### 🧹 Chores") == ["- Bump (#12)", "- Bump again (#13)"]
    assert lines_under(body, "### 📦 Other") == ["- An untyped title (#16)"]
    assert "#9)" not in body, "the preparation pull request is listed as a change"
    assert "#999" not in body, "a keyword inside a code span was read as a claim"
    assert (
        body.index("### ✨ Features")
        < body.index("### 🐛 Fixes")
        < body.index("### 📚 Docs")
    ), "the headings are not in the order the note is meant to read in"


def test_the_glance_counts_the_release(monkeypatch, tmp_path):
    """A5. Seven changes, four distinct issues closed (#100 twice counts
    once), two outside people however many pull requests they made."""
    mod, body = published(monkeypatch, tmp_path, RELEASE)
    glance = body[: body.index("### ✨ Features")]
    assert glance.startswith(mod.GLANCE_HEADING)
    assert "| 🔀 Pull requests | **7** |" in glance
    assert "| ✅ Issues closed | **4** |" in glance
    assert "| 🙌 Outside contributors | **2** |" in glance


def test_an_outside_contributor_is_thanked_by_handle(monkeypatch, tmp_path):
    """A5. The owner's pull requests and a bot's are the release's own work;
    anybody else's is a contribution, and the note names who made it."""
    mod, body = published(monkeypatch, tmp_path, RELEASE)
    assert lines_under(body, mod.THANKS_HEADING) == [
        "- **@someone** — Explain a thing (#11); And a second thing (#14)",
        "- **@another** — A third (#15)",
    ]
    for excluded in (OWNER, "dependabot", "renovate"):
        assert f"@{excluded}" not in body, f"{excluded} is thanked for its own work"


def test_the_section_is_kept_folded_under_the_summary(monkeypatch, tmp_path):
    """A5. The gathered section is the reasoning, and none of it is lost: it
    follows the summary whole, inside a fold, with a link to the file."""
    mod, body = published(monkeypatch, tmp_path, RELEASE)
    section = mod.section_body(RELEASE_FILE, VERSION)
    fold = body[body.index("<details>") :]
    assert f"<summary>{mod.FULL_SUMMARY}</summary>\n\n{section}\n\n</details>" in fold
    # S9 of #728: the link is the release's own file at the tag.
    link = f"[`changelog/{VERSION}.md` at {TAG}]"
    link += f"(https://github.com/{REPO}/blob/{TAG}/changelog/{VERSION}.md)"
    assert fold.endswith(link), fold[-200:]
    assert "the release before it" not in body, "an older release reached the note"
    assert body.index(mod.UPDATE_HEADING) < body.index("<details>")
    assert "/specseal:update" in body


def test_a_release_with_no_outside_contribution_thanks_nobody(monkeypatch, tmp_path):
    """A5, the other direction. Most releases carry only the owner's work:
    the summary is there, and no credit line or count is invented."""
    mod, body = published(monkeypatch, tmp_path, [pull(10, OWNER, "fix: a thing")])
    assert mod.THANKS_HEADING not in body
    assert "Outside contributors" not in body
    assert "thanks @" not in body


@pytest.mark.parametrize(
    "pulls",
    [
        pytest.param(None, id="the list could not be read"),
        pytest.param([], id="no pull request"),
        pytest.param([RELEASE[0]], id="only the preparation"),
    ],
)
def test_with_nothing_to_summarise_the_note_is_the_section(
    monkeypatch, tmp_path, capsys, pulls
):
    """A5 adds no way to fail the tag's job: a summary that cannot be built
    leaves the note the section alone, as it was before #572."""
    mod, body = published(monkeypatch, tmp_path, pulls)
    assert body == mod.section_body(RELEASE_FILE, VERSION)
    if pulls is None:
        assert "no outside contribution" not in capsys.readouterr().out, (
            "a list that could not be read is reported as a release nobody helped"
        )


def test_the_list_is_read_from_the_release_branch(monkeypatch):
    """The set is the pull requests merged into `release/vX.Y.Z` — the base
    every feature branch squashes into — and a failed `gh` call is None."""
    mod = publisher()
    seen = []

    class Done:
        def __init__(self, code, out="", err=""):
            self.returncode, self.stdout, self.stderr = code, out, err

    def fake(args, **_):
        seen.append(args)
        return Done(0, '[{"number": 1, "title": "t", "author": {"login": "x"}}]')

    monkeypatch.setattr(mod.subprocess, "run", fake)
    assert mod.merged_pulls(REPO, VERSION)[0]["number"] == 1
    args = seen[0]
    assert args[args.index("--base") + 1] == f"release/v{VERSION}"
    assert "body" in args[args.index("--json") + 1].split(","), (
        "the body is not fetched, so no line can say which issues it closed"
    )
    # #718: the seal reads the capped label and the head branch from the same
    # call, so the list is fetched once for the note and the seal alike.
    fields = args[args.index("--json") + 1].split(",")
    assert "labels" in fields and "headRefName" in fields, fields
    assert args[args.index("--state") + 1] == "merged"
    assert args[args.index("--repo") + 1] == REPO

    monkeypatch.setattr(
        mod.subprocess, "run", lambda args, **_: Done(1, err="HTTP 502")
    )
    assert mod.merged_pulls(REPO, VERSION) is None


# --- S4 of work item 1790993139: the job says whether it created the release --


@pytest.mark.parametrize(
    "existing, created",
    [((), "true"), ((TAG,), "false")],
    ids=["created", "already there"],
)
def test_the_job_says_whether_it_created_the_release(
    monkeypatch, tmp_path, existing, created
):
    """S4 (#718). `created` goes to `$GITHUB_OUTPUT`: `true` after the
    release is created, `false` where one was already at the tag, so the seal
    job, which edits the note, runs only on a note this run wrote. Seen red
    against the `main` that wrote nothing."""
    out = tmp_path / "github_output"
    mod, _ = wire(
        monkeypatch,
        tmp_path,
        message=title_line(),
        existing=existing,
        GITHUB_OUTPUT=str(out),
    )
    assert mod.main() == 0
    assert out.read_text(encoding="utf-8") == f"created={created}\n"


def test_without_an_output_file_nothing_is_written_and_nothing_raises(
    monkeypatch, tmp_path, capsys
):
    """S4. On a laptop there is no `$GITHUB_OUTPUT`: nothing is written. Where
    the file cannot be written, that is printed and ignored, and the release
    is still published with exit 0."""
    mod, tracker = wire(monkeypatch, tmp_path, message=title_line())
    assert mod.main() == 0
    assert len(tracker.creates()) == 1
    assert not (tmp_path / "github_output").exists()
    blocked = tmp_path / "a-directory"
    blocked.mkdir()
    mod, tracker = wire(
        monkeypatch, tmp_path, message=title_line(), GITHUB_OUTPUT=str(blocked)
    )
    assert mod.main() == 0
    assert len(tracker.creates()) == 1
    assert "could not write created=true" in capsys.readouterr().out


def test_the_glance_block_is_built_by_one_function_and_its_sealed_twin_by_another(
    monkeypatch, tmp_path
):
    """S1's shape (#718). The note's glance block is exactly `glance`'s, so
    the seal can find it by the same function; `sealed_glance` is the heading,
    the image, a blank line and one line carrying every row the table had, in
    its order. Since #832 the image is an `<img>` carrying its display
    width, because the PNG is drawn at twice that size for a high-density
    screen and Markdown's image syntax has no width; and the alt text and
    the URL are escaped for the attribute they sit in, so a quote cannot end
    it early. Seen red against the Markdown image, and by the escape
    removed."""
    mod, body = published(monkeypatch, tmp_path, RELEASE)
    work, closed, people = mod.tally(RELEASE, OWNER)
    block = mod.glance(work, closed, people)
    assert body.startswith(block + "\n\n### ✨ Features"), body[:400]
    assert mod.sealed_glance(
        "https://example.com/seal.png", "a seal", 160, work, closed, people
    ) == (
        f"{mod.GLANCE_HEADING}\n\n"
        '<img src="https://example.com/seal.png" alt="a seal" width="160">\n\n'
        "🔀 Pull requests **7** · ✅ Issues closed **4** · 🙌 Outside contributors **2**"
    )
    alone = [pull(10, OWNER, "fix: one", "Closes #100")]
    work, closed, people = mod.tally(alone, OWNER)
    assert mod.sealed_glance("u", "a", 160, work, closed, people).endswith(
        "🔀 Pull requests **1** · ✅ Issues closed **1**"
    )
    odd = mod.sealed_glance('u?a=1&b="2"', 'a "seal" <b>', 80, work, closed, people)
    assert (
        '<img src="u?a=1&amp;b=&quot;2&quot;" alt="a &quot;seal&quot; &lt;b&gt;" '
        'width="80">'
    ) in odd, odd


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
    # A release file is the section, as a new gather writes it (#728), and
    # the same file after a second gather appended into it.
    later = gather.insert(
        block, gather.section(VERSION, "d", [("2-b", "later")]), VERSION
    )
    for text in (block, later):
        assert publisher().section_body(text, VERSION) is not None, (
            "the reader no longer recognises the section the gatherer writes, so "
            "every release would publish with no notes at all"
        )
        assert NOTES in publisher().section_body(text, VERSION)
    assert "later" in publisher().section_body(later, VERSION)


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


def job(text, name):
    """One job's lines of the comment-free workflow, from its `  <name>:`
    line to the next job or the end."""
    lines = text.splitlines()
    start = lines.index(f"  {name}:")
    end = next(
        (
            i
            for i in range(start + 1, len(lines))
            if lines[i].startswith("  ") and not lines[i].startswith("   ")
        ),
        len(lines),
    )
    return lines[start:end]


def steps(lines):
    """A job's steps, each as its lines, split at every `      - ` line."""
    out = []
    for line in lines:
        if line.startswith("      - "):
            out.append([line])
        elif out:
            out[-1].append(line)
    return out


def test_the_workflow_fires_on_the_tag_and_writes_one_release_one_asset_one_edit():
    """S5 (#718). The trigger is the whole design decision: hanging this from
    the push to `main` would put it before the tag exists. Under
    `contents: write` it writes three things now -- one release (`publish`),
    one asset on it and one edit of its note (`seal`) -- and still declares no
    other scope. `publish` has no `needs` and says whether it created the
    release; `seal` needs it, runs only on `created == 'true'`, and every one
    of its steps is `continue-on-error`, so nothing the seal meets can turn
    the workflow red. A hung suite ends at the step's `timeout-minutes`, and
    the job's own timeout sits under a job-level `continue-on-error` (round
    1's 🟡 4). The token is on the drawing step alone, and the checkout does
    not persist it in `.git/config`, so the suite at the tag runs with none
    (round 1's 🟡 5). Seen red against the workflow with no `seal` job, and
    the two round-1 halves against the workflow without them."""
    text = workflow()
    assert "tags: ['v*']" in text, "the workflow no longer fires on a tag push"
    assert "branches:" not in text, (
        "this fires on a branch push as well; at the push to `main` the tag "
        "does not exist yet and the job would have to create it"
    )
    assert "contents: write" in text
    for scope in ("issues:", "pull-requests:", "packages:"):
        assert scope not in text, (
            f"the workflow declares {scope}, which it does not use"
        )
    publish = job(text, "publish")
    assert not any(line.strip().startswith("needs:") for line in publish), publish
    assert "      created: ${{ steps.note.outputs.created }}" in publish, publish
    assert any("publish_release_note.py" in line for line in publish)
    seal = job(text, "seal")
    assert "    needs: publish" in seal, seal
    assert "    if: needs.publish.outputs.created == 'true'" in seal, seal
    assert (
        "    timeout-minutes: 60" in seal and "    continue-on-error: true" in seal
    ), seal
    held = steps(seal)
    # Six since #832: the step that installs `rsvg-convert` joined them.
    assert len(held) == 6, held
    assert any(line.strip() == "persist-credentials: false" for line in held[0]), held[
        0
    ]
    for step in held:
        assert any(line.strip() == "continue-on-error: true" for line in step), step
    tokened = [step for step in held if any("GH_TOKEN" in line for line in step)]
    assert len(tokened) == 1 and any("release_seal.py" in line for line in tokened[0])
    suite = [step for step in held if any("--junitxml" in line for line in step)]
    assert len(suite) == 1 and any("id: suite" in line for line in suite[0]), suite
    assert any(line.strip() == "timeout-minutes: 30" for line in suite[0]), suite
    assert any(
        "SUITE_OUTCOME: ${{ steps.suite.outcome }}" in line for line in tokened[0]
    ), tokened


def test_the_seal_job_installs_rsvg_convert_before_the_suite_and_the_draw():
    """S6 (#832). The runner image carries no `rsvg-convert`, so the `seal`
    job installs `librsvg2-bin` with `apt-get`, without the recommended
    packages, in a step of its own that is `continue-on-error` like every
    other: an install that fails costs the image, and `release_seal.py`
    says so on its `::warning::` line. The step comes before the suite, so
    the suite at the tag runs the case that draws the seal with the real
    binary, and so before the draw. Seen red against the job without it,
    and with it placed after the draw.

    The package lists are refreshed first, and the refresh does not gate
    the install: `apt-get update` exits non-zero when any one list fails,
    a third-party list the package does not come from included, so `&&`
    after it skipped an install that would have worked (round 1's ⬜ 8). A
    bare `;` skipped it too, because a step with no `shell:` runs under
    `bash -e`, so the refresh is followed by `|| true` (round 2's 🟡 2).
    Seen red against the `;` step."""
    held = steps(job(workflow(), "seal"))
    installs = [
        at
        for at, step in enumerate(held)
        if any(
            "sudo apt-get install -y --no-install-recommends librsvg2-bin" in line
            for line in step
        )
    ]
    assert len(installs) == 1, held
    (at,) = installs
    assert any(line.strip() == "continue-on-error: true" for line in held[at])
    run = next(line for line in held[at] if "librsvg2-bin" in line)
    assert "sudo apt-get update || true;" in run, run
    assert "apt-get update &&" not in run, run
    suite = next(
        n for n, step in enumerate(held) if any("--junitxml" in s for s in step)
    )
    draw = next(
        n for n, step in enumerate(held) if any("release_seal.py" in s for s in step)
    )
    assert at < suite < draw, (at, suite, draw)


def test_the_workflow_is_not_a_step_of_the_release_job():
    """`tests/test_the_gate_names_every_step_ci_runs.py` partitions every step
    of `hygiene.yml`'s `release` job against `broad_gate.py`'s arms. This is a
    workflow of its own, on a different trigger, and adding a step there
    instead would have grown that partition for a job nothing local can run."""
    hygiene = read(os.path.join(ROOT, ".github", "workflows", "hygiene.yml"))
    assert "publish_release_note.py" not in hygiene
