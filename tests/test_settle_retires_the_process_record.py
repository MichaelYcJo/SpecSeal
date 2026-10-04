"""`settle --retire-process` takes a released work item's process record and
leaves the rest of its directory for the fold (#729).

A work item's directory holds two kinds of file. The SDD set and `routing.md`
say what was decided and why; the process record — `rounds/`, `phases/`,
`survivors.md` and the files written only for a pull request — is read by
no check after the release that ships the item. Measured when this shipped, it
was 62% of the files under `seal/specs/` and 67% of the bytes, and it waited
on the fold, a judgment it does not need. So it leaves by an arm of its own,
which writes no prose and judges nothing.

Every case runs the command as a person types it, against a scratch
repository, and asks what it removed, what it kept, and what it printed.
"""

import importlib.util
import io
import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "settle", "scripts", "settle.py")
SKILL = os.path.join(ROOT, "skills", "settle", "SKILL.md")


def load():
    spec = importlib.util.spec_from_file_location("settle_process", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


settle = load()

ALPHA = "1700000001-alpha"
BETA = "1700000002-beta"

LEDGER = """# spec-to-code map

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| a row from before the fragments existed | `hooks/old.py#thing@11111111` | read | 2026-01-01 | |
"""

CLOSED_TODO = """# todo

| Fact | Where it goes |
|---|---|
| ✅ something a reviewer left | merged into the fragment |
"""

OPEN_TODO = """# todo

| Fact | Where it goes |
|---|---|
| something a reviewer left that never landed | the work item's fragment |
"""

OVERVIEW = "# overview\n\nWhy.\n\n## Not verified\n\nnone — every item was run\n"

# What stays until the fold, and what this arm takes: spec D4, spelled out
# here rather than imported, so the case can disagree with the code.
DURABLE = (
    "routing.md",
    "spec.md",
    "plan.md",
    "questions.md",
    "overview.md",
    "changelog.md",
)
PROCESS = {
    "rounds/round-1.md": "# round 1\n",
    "rounds/round-1-report.md": "# report\n",
    "rounds/round-2.md": "# round 2\n",
    "phases/phase-1.md": "# phase 1\n",
    "survivors.md": "# survivors\n",
    "broad-gate.md": "# broad gate\n",
    "handoff.md": "# handoff\n",
    "pr.ko.md": "# 본문\n",
    "tests-todo.md": CLOSED_TODO,
    "evidence-todo.md": CLOSED_TODO,
}
TAKEN = (
    "rounds/",
    "phases/",
    "survivors.md",
    "broad-gate.md",
    "handoff.md",
    "pr.ko.md",
    "tests-todo.md",
    "evidence-todo.md",
)


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def item(repo, name, extra=None):
    """A work item directory holding the SDD set and the whole process record."""
    base = repo / "seal" / "specs" / name
    for durable in DURABLE:
        body = OVERVIEW if durable == "overview.md" else f"# {name} {durable}\n"
        write(base / durable, body)
    for rel, body in {**PROCESS, **(extra or {})}.items():
        write(base / rel, body)
    return base


@pytest.fixture
def repo(tmp_path):
    """`alpha` is released — present at the commit `--released-at` names — and
    `beta` is this branch's own work, on disk and in no commit."""
    repo = tmp_path / "repo"
    write(repo / "docs" / "one-root.md", "# a policy\n\nA rule.\n")
    write(repo / "seal" / "ledger.md", LEDGER)
    item(repo, ALPHA)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "x@example.com")
    git(repo, "config", "user.name", "x")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "released")
    item(repo, BETA)
    return repo


def run(repo, *args):
    """`(exit code, stdout + stderr)` of the command as a person runs it."""
    r = subprocess.run(
        [sys.executable, SCRIPT, "--root", str(repo), "--released-at", "HEAD", *args],
        capture_output=True,
        encoding="utf-8",
    )
    return r.returncode, r.stdout + r.stderr


def files_of(directory):
    return sorted(
        str(p.relative_to(directory)).replace(os.sep, "/")
        for p in directory.rglob("*")
        if p.is_file()
    )


# --- S1: exactly the leave-list goes, and the SDD set stands ---------------


def test_the_process_record_leaves_and_the_sdd_set_stays(repo):
    code, text = run(repo, "--retire-process")
    assert code == 0, text
    alpha = repo / "seal" / "specs" / ALPHA
    assert files_of(alpha) == sorted(DURABLE), files_of(alpha)
    for taken in TAKEN:
        assert f"removed seal/specs/{ALPHA}/{taken}" in text, (taken, text)
    assert "retired the process record of 1 work item (10 files); 0 kept" in text, text


def test_a_directory_is_removed_with_its_file_count(repo):
    """A person reading `removed …/rounds/` cannot tell one file from forty,
    and the count is what they compare with the dry run."""
    _, text = run(repo, "--retire-process")
    assert f"removed seal/specs/{ALPHA}/rounds/  (3 files)" in text, text
    assert f"removed seal/specs/{ALPHA}/phases/  (1 file)" in text, text


# --- S2: an unreleased item is not a candidate -----------------------------


def test_an_unreleased_item_is_not_touched_or_named(repo):
    beta = repo / "seal" / "specs" / BETA
    before = files_of(beta)
    code, text = run(repo, "--retire-process")
    assert code == 0, text
    assert files_of(beta) == before
    assert BETA not in text, text


# --- S3: an open todo row keeps the whole item -----------------------------


@pytest.mark.parametrize("todo", ["evidence-todo.md", "tests-todo.md"])
def test_an_open_todo_row_keeps_the_item_whole(repo, todo):
    write(repo / "seal" / "specs" / ALPHA / todo, OPEN_TODO)
    alpha = repo / "seal" / "specs" / ALPHA
    before = files_of(alpha)
    code, text = run(repo, "--retire-process")
    assert code == 1, text
    assert files_of(alpha) == before, "a held item lost part of its record"
    assert settle.PROCESS_TODO_HEADING in text, text
    assert f"    {ALPHA}  (1 open row in {todo})" in text, text
    assert "retired the process record of 0 work items (0 files); 1 kept" in text


# --- S4: a file on neither list stays and is named --------------------------


def test_a_file_on_neither_list_stays_and_is_named(repo):
    write(repo / "seal" / "specs" / ALPHA / "notes.md", "# notes\n")
    code, text = run(repo, "--retire-process")
    assert code == 0, text
    assert (repo / "seal" / "specs" / ALPHA / "notes.md").is_file()
    assert settle.PROCESS_UNKNOWN_HEADING in text, text
    assert f"    seal/specs/{ALPHA}/notes.md" in text, text
    assert not (repo / "seal" / "specs" / ALPHA / "rounds").exists()


# --- S8: local mode is refused ---------------------------------------------


def test_local_mode_is_refused_and_nothing_is_removed(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    local = repo / ".git" / "seal" / "specs" / ALPHA
    write(local / "spec.md", "# a\n")
    write(local / "rounds" / "round-1.md", "# round 1\n")
    code, text = run(repo, "--retire-process")
    assert code == 2, text
    assert "which is local mode" in text, text
    assert (local / "rounds" / "round-1.md").is_file()


# --- S9: a ledger row anchored inside a removed file keeps the item --------

INSIDE_ROW = (
    "| a claim read in a round record | "
    f'`seal/specs/{ALPHA}/rounds/round-1.md#"# round 1"@abcdef12` '
    "| read | 2026-01-01 | |"
)
SPEC_ROW = (
    "| a claim read in a spec | "
    f'`seal/specs/{ALPHA}/spec.md#"# {ALPHA} spec.md"@abcdef12` '
    "| read | 2026-01-01 | |"
)


def test_a_row_anchored_inside_the_process_record_keeps_the_item(repo):
    write(repo / "seal" / "ledger.md", LEDGER + INSIDE_ROW + "\n")
    code, text = run(repo, "--retire-process")
    assert code == 1, text
    assert (repo / "seal" / "specs" / ALPHA / "rounds" / "round-1.md").is_file()
    assert settle.PROCESS_ANCHORED_HEADING in text, text
    assert "    seal/ledger.md:6  a claim read in a round record" in text, text
    assert settle.REMOVED_SAYS in text, text


def test_a_row_anchored_in_the_sdd_set_does_not_hold_the_process_record(repo):
    """The file it anchors stays, so nothing it cites stops resolving — the
    one direction `anchored_rows`' own prefix test would get wrong here."""
    write(repo / "seal" / "ledger.md", LEDGER + SPEC_ROW + "\n")
    code, text = run(repo, "--retire-process")
    assert code == 0, text
    assert not (repo / "seal" / "specs" / ALPHA / "rounds").exists()
    assert settle.PROCESS_ANCHORED_HEADING not in text, text


# --- D4: a citation outside seal/specs/ is listed and never refused --------


def test_a_citation_into_a_removed_file_is_listed_and_refuses_nothing(repo):
    write(
        repo / "docs" / "one-root.md",
        "# a policy\n\nA rule.\n\n"
        f"Measured in `seal/specs/{ALPHA}/rounds/round-1.md`.\n"
        f"Decided in `seal/specs/{ALPHA}/spec.md`.\n",
    )
    git(repo, "add", "docs")
    git(repo, "commit", "-qm", "a citation")
    code, text = run(repo, "--retire-process")
    assert code == 0, text
    assert settle.PROCESS_CITED_HEADING in text, text
    assert "        cited from docs/one-root.md:5" in text, text
    assert "docs/one-root.md:6" not in text, (
        "a citation into a file that stays was listed as one that stops resolving"
    )


# --- the second run, and the flag beside `--retire` ------------------------


def test_a_second_run_finds_nothing_left_and_exits_0(repo):
    run(repo, "--retire-process")
    code, text = run(repo, "--retire-process")
    assert code == 0, text
    assert settle.PROCESS_DONE in text, text


def test_the_two_retirements_are_never_asked_at_once(repo):
    code, text = run(repo, "--retire", "--retire-process")
    assert code == 2, text
    assert "not allowed with argument" in text, text
    assert (repo / "seal" / "specs" / ALPHA / "rounds").is_dir()


# --- S10: the dry run says what the arm would take -------------------------


def test_the_report_says_what_the_arm_would_take(repo):
    before = files_of(repo)
    code, text = run(repo)
    assert code == 0, text
    assert files_of(repo) == before, "the report removed something"
    assert settle.PROCESS_HEADING in text, text
    assert "    10 files in 1 released work item" in text, text


def test_the_report_names_what_the_arm_would_keep(repo):
    write(repo / "seal" / "specs" / ALPHA / "evidence-todo.md", OPEN_TODO)
    write(repo / "seal" / "specs" / ALPHA / "notes.md", "# notes\n")
    _, text = run(repo)
    section = text.split(settle.PROCESS_HEADING, 1)[1]
    assert "    0 files in 0 released work items" in section, section
    assert f"    {ALPHA}  kept: 1 open row in evidence-todo.md" in section, section
    assert f"    seal/specs/{ALPHA}/notes.md  not a process record, kept" in section


def test_a_survey_with_no_process_key_is_still_reported():
    """`report` reads the section off `survey`; a survey from before the arm
    existed carries no `process` key and must still be reported."""
    found = {
        "base": "x",
        "base_label": "x",
        "grouped": {},
        "ungrouped": [],
        "skipped": [],
        "unreleased": [],
        "rule": [],
        "rule_kept": [],
        "rule_base_kept": [],
        "folded": [],
        "anchored": [],
        "retiring": [],
    }
    out = io.StringIO()
    assert settle.report(found, "HEAD", out=out) == 0
    assert settle.PROCESS_HEADING not in out.getvalue()


# --- §14: what a person reads is documented where they look for it --------


def flat(text):
    return " ".join(text.split())


def test_the_skill_quotes_every_line_the_arm_prints():
    with open(SKILL, encoding="utf-8") as f:
        text = flat(f.read())
    assert "settle --retire-process" in text
    for name in (
        "PROCESS_HEADING",
        "PROCESS_TODO_HEADING",
        "PROCESS_ANCHORED_HEADING",
        "PROCESS_UNKNOWN_HEADING",
        "PROCESS_CITED_HEADING",
        "PROCESS_DONE",
    ):
        line = flat(getattr(settle, name))
        assert line in text, f"skills/settle/SKILL.md does not quote {name}: {line}"


# --- S11: every document that says how long a record stays says this -------


def document(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return flat(f.read())


@pytest.mark.parametrize(
    "parts, standing, gone",
    [
        (
            ("docs", "the-record-layout.md"),
            "Built by #729.",
            "is decided in principle and not built (F3)",
        ),
        (
            ("docs", "release-checklist.md"),
            "First, the process record. This part is never skipped.",
            "the honest answer on a busy release is to skip this step",
        ),
        (
            ("docs", "review-handoff-protocol.md"),
            "The round records leave first, with the rest of the process record",
            "and the whole directory, round records included, is then removed",
        ),
        (
            ("skills", "implement", "SKILL.md"),
            "`settle --retire-process` removes them after the release",
            "closed at merge and kept",
        ),
        (
            ("agents", "framer.md"),
            "a released work item's round records leave the tree at the next release",
            "Their round records included. A decision",
        ),
        (
            ("seal", "README.md"),
            "removed by `settle --retire-process` at the next release",
            "each work item whole under `seal/specs/<work-item-id>/`, where it "
            "waits until `settle` folds it. **That step exists now**: `settle` "
            "names the released work items whose `spec.md` no `docs/` policy has "
            "absorbed yet, a session writes one standing statement per segment, "
            "and `settle --retire` then removes the directories that statement "
            "covers, along with every released one that wrote no `spec.md` and "
            "holds nothing open, which states no rule to fold. A fold is",
        ),
        # Two copies of one sentence, in the module docstring and in
        # `whole_range`'s, so each is pinned by the words that follow it.
        (
            ("skills", "code-review", "scripts", "survivor_check.py"),
            "stands until `settle --retire-process` takes it, after the release "
            "that ships it, so one merged row",
            "lives until the release that ships it",
        ),
        (
            ("skills", "code-review", "scripts", "survivor_check.py"),
            "stands until `settle --retire-process` takes it, after the release "
            "that ships it -- so one merged declaration",
            "lives until the release that ships it",
        ),
    ],
)
def test_each_carrier_says_when_the_process_record_leaves(parts, standing, gone):
    """Spec D6's carriers, each found by a phrase that stated a lifetime.
    `standing` is the new wording and `gone` the sentence it replaced, which
    said the process record waited for the fold or stayed for good."""
    text = document(*parts)
    assert standing in text, f"{'/'.join(parts)} does not say {standing!r}"
    assert gone not in text, f"{'/'.join(parts)} still says {gone!r}"


# --- round 1's fixes -------------------------------------------------------

# 🟡 2: a citation's path, as prose writes it. Built as every name on the
# arm's list times every way a sentence can follow a file name, so a shape is
# never one that was thought of; and the same tails after a name that is not
# on the list, or after a name that continues past the list's spelling.
TAILS = (
    "",
    ".",
    ",",
    ";",
    ":",
    "!",
    "?",
    ":40",
    ":40-45",
    "#anchor",
    "#L40",
    "@abcdef12",
    "\\",
    "…",
    "—then",
    ".\u00a0",
)
TAKEN_NAMES = (
    "rounds",
    "phases",
    "survivors.md",
    "broad-gate.md",
    "handoff.md",
    "tests-todo.md",
    "evidence-todo.md",
    "pr.ko.md",
)
NOT_TAKEN = (
    "spec.md",
    "overview.md",
    "routing.md",
    "notes.md",
    "handoff.md.bak",
    "rounds-old",
    "phasesx",
    "survivors.mdx",
)


@pytest.mark.parametrize("tail", TAILS)
@pytest.mark.parametrize(
    "name", (*TAKEN_NAMES, "rounds/", "rounds/round-1.md", "phases/phase-2.md")
)
def test_a_citation_into_a_taken_file_is_read_whatever_follows_it(name, tail):
    """Round 1, 🟡 2: `handoff.md:40`, `survivors.md.`, `pr.ko.md,` and a
    bare `rounds` all name a file the arm takes, and were not listed."""
    assert settle.cites_a_process_record(name + tail), name + tail


@pytest.mark.parametrize("tail", TAILS)
@pytest.mark.parametrize("name", (*NOT_TAKEN, "rounds-old/round-1.md"))
def test_a_citation_into_a_file_that_stays_is_not_read_as_one(name, tail):
    assert not settle.cites_a_process_record(name + tail), name + tail


def test_a_citation_written_as_prose_is_listed(repo):
    """The same, end to end: a citation outside backticks ends with the
    sentence's punctuation, a `path:line` ends with its line, and a directory
    is named with no slash. Each still names a file the arm takes, and a
    citation into `spec.md` written the same way is not listed."""
    write(
        repo / "docs" / "one-root.md",
        "# a policy\n\nA rule.\n\n"
        f"Measured in seal/specs/{ALPHA}/survivors.md.\n"
        f"See seal/specs/{ALPHA}/handoff.md:40 for it.\n"
        f"The `seal/specs/{ALPHA}/rounds` directory.\n"
        f"In seal/specs/{ALPHA}/pr.ko.md, which.\n"
        f"Decided in seal/specs/{ALPHA}/spec.md.\n",
    )
    git(repo, "add", "docs")
    git(repo, "commit", "-qm", "prose citations")
    code, text = run(repo, "--retire-process")
    assert code == 0, text
    for line in (5, 6, 7, 8):
        assert f"        cited from docs/one-root.md:{line}" in text, (line, text)
    assert "docs/one-root.md:9" not in text, text


def test_the_fold_reads_a_reference_into_the_process_record_at_the_tag():
    """Round 1, 🟡 1: the SDD set that stays names its own round and phase
    records by relative path, and after the arm those resolve at the release
    tag. The arm's section and the fold's first step both say so."""
    with open(SKILL, encoding="utf-8") as f:
        text = flat(f.read())
    assert "The SDD set that stays still points into what left." in text
    assert "`git show v<X.Y.Z>:seal/specs/<id>/phases/phase-2.md`" in text
    first_step = text.split("### 1. Read what is waiting", 1)[1].split("### 2.", 1)[0]
    assert "read it at the tag of the release that shipped the item" in first_step


# Round 1, 🟡 1: each sentence that said nothing reads the process record now
# says what holds — no check reads it, and a person following a reference
# into it reads it at the release tag.
@pytest.mark.parametrize(
    "parts",
    [
        ("skills", "settle", "SKILL.md"),
        ("skills", "settle", "scripts", "settle.py"),
        ("docs", "the-record-layout.md"),
        ("docs", "release-checklist.md"),
    ],
)
def test_no_carrier_says_nothing_reads_the_process_record(parts):
    text = document(*parts)
    for said in (
        "read by nothing after",
        "Nothing reads that part",
        "nothing reads it",
        "which nothing reads after the release",
    ):
        assert said not in text, f"{'/'.join(parts)} still says {said!r}"
    low = text.lower()
    assert "no check reads" in low or "read by no check" in low, parts


def test_the_design_records_dated_section_says_no_check_reads_it():
    for edition, gone, standing in (
        (
            "one-root-by-lifetime.md",
            "nothing reads it once its release has merged",
            "no check reads it once its release has merged",
        ),
        (
            "one-root-by-lifetime.ko.md",
            "이것을 읽는 곳이 없습니다",
            "이것을 읽는 검사가 없고",
        ),
    ):
        text = document("docs", edition)
        assert gone not in text, edition
        assert standing in text, edition
