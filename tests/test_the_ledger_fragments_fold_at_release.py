"""A work item writes a ledger fragment; the release folds them.

Issue #78. Every work item writes its evidence rows to
`seal/ledger/<id>.md` and nothing ever folded them into `seal/ledger.md`,
so the directory gained one file per work item forever and almost every pull
request touched it. The fragment layout exists to stop two branches queueing
at one file, and after the merge there is no branch left to queue
(`docs/one-root-by-lifetime.md`, "What happens at a release", step 1).

Step 3 of the same section is the guard: a fact that must outlive the release
has to have reached the ledger, and `seal/specs/<id>/evidence-todo.md` is where a
reviewer lists the ones still waiting. The fold refuses while any such file
has an open row.

This file holds both halves — that the fold happens, that it is a move and
not a deletion, that it refuses in the right places, and that a release pull
request cannot go out with a fragment or an open row left behind. It is the
shape of `test_the_changelog_is_gathered_at_release.py`, because the script is
the shape of `gather_changelog.py`.
"""

import glob
import importlib.util
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, ".github", "scripts", "fold_ledger.py")
CHECKER = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")


def _load_checker():
    spec = importlib.util.spec_from_file_location("specseal_evidence_check", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ec = _load_checker()


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


def check(root):
    """`evidence_check.py` on the fixture — the totals line and the exit."""
    r = subprocess.run(
        [sys.executable, CHECKER, "."],
        cwd=str(root),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    totals = [line for line in r.stdout.splitlines() if line.startswith("total:")]
    assert totals, r.stdout
    return totals[0], r.returncode


SERVICE = (
    "import os\n\n\ndef handler(x):\n    y = x + 1\n    return y\n\n\n"
    "def parse(s):\n    return s.split()\n\n\n"
    "class Box:\n    def open(self):\n        return self\n"
)


def unit_hash(anchor):
    """The hash a row citing `src/service.py#<anchor>` carries in the fixture."""
    a, b = ec.resolve("src/service.py", anchor, SERVICE)[0]
    return ec.content_hash(SERVICE.splitlines()[a - 1 : b])


def handler_hash():
    return unit_hash("handler")


LEDGER_HEAD = (
    "# spec-to-code map\n\n> The gathered ledger.\n\n## Coordinates\n\n"
    "| Item | Value |\n|---|---|\n| Coordinate notation | `path#anchor@hash` |\n\n"
    "## An area from before the fragments\n\n"
    "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
    "|---|---|---|---|---|\n"
    "| the old claim | `src/service.py#handler@{h}` | read | 2026-09-01 | |\n"
)


def row(claim, h, note="", anchor="handler"):
    return (
        f"| {claim} | `src/service.py#{anchor}@{h}` | executed | 2026-09-02 | {note} |"
    )


def fragment(work_item_id, preamble, rows):
    return (
        f"# {work_item_id}\n\n{preamble}\n\n## The area this work item wrote\n\n"
        "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
    )


@pytest.fixture
def tree(tmp_path):
    """A repository shape: a gathered ledger, two fragments whose rows resolve,
    a cited file, and a work item whose evidence-todo file is drained."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    h = handler_hash()
    (tmp_path / "seal" / "ledger").mkdir(parents=True)
    (tmp_path / "seal" / "ledger.md").write_text(
        LEDGER_HEAD.format(h=h), encoding="utf-8"
    )
    later = fragment(
        "1788229400-later",
        "Rows for the later work item.",
        [
            row(
                "the later claim",
                unit_hash("parse"),
                "a note with a | pipe escaped as \\|",
                anchor="parse",
            )
        ],
    )
    earlier = fragment(
        "1700000000-earlier",
        "Rows for the earlier work item.",
        [
            row("the earlier claim", unit_hash("Box"), anchor="Box"),
            row("the earlier second claim", unit_hash("Box.open"), anchor="Box.open"),
        ],
    )
    (tmp_path / "seal" / "ledger" / "1788229400-later.md").write_text(
        later, encoding="utf-8"
    )
    (tmp_path / "seal" / "ledger" / "1700000000-earlier.md").write_text(
        earlier, encoding="utf-8"
    )
    d = tmp_path / "seal" / "specs" / "1788229400-later"
    d.mkdir(parents=True)
    (d / "evidence-todo.md").write_text(
        "# verified facts to merge\n\ndrained — both rows merged at abc1234.\n\n"
        "| Claim | Grounds | Label |\n|---|---|---|\n"
        "| the later claim | `src/service.py#handler` | Executed |\n",
        encoding="utf-8",
    )
    return tmp_path


def ledger(tree):
    return (tree / "seal" / "ledger.md").read_text(encoding="utf-8")


def release_file(tree, version="0.4.0"):
    return tree / "seal" / "releases" / f"{version}.md"


def released(tree, version="0.4.0"):
    """The release file the fold wrote — the section, byte for byte (#547)."""
    return release_file(tree, version).read_text(encoding="utf-8")


def fragments_left(tree):
    d = tree / "seal" / "ledger"
    return sorted(p.name for p in d.iterdir()) if d.exists() else []


def fold(tree, version="0.4.0", date="2026-09-15"):
    """Run the fold and prove it actually folded.

    A return code is not an effect — the marker landing in the file and the
    fragment leaving the directory are — so every case that depends on a fold
    having happened goes through this.
    """
    shared = ledger(tree)
    r = run("--version", version, "--date", date, root=tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert release_file(tree, version).is_file(), (
        f"exited 0 and wrote no release file:\n{r.stdout}"
    )
    text = released(tree, version)
    assert text.startswith(f"## {version} — "), (
        f"the file does not begin with the heading:\n{text}"
    )
    assert "<!-- specs/" in text, f"exited 0 and wrote no marker:\n{text}"
    assert ledger(tree) == shared, "a fold wrote to seal/ledger.md (#547)"
    assert f"into seal/releases/{version}.md" in r.stdout, r.stdout
    return r


def evidence_todo(tree, work_item_id, text):
    d = tree / "seal" / "specs" / work_item_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "evidence-todo.md").write_text(text, encoding="utf-8")


OPEN_FILE = (
    "# verified facts to merge\n\n| Claim | Grounds | Label |\n|---|---|---|\n"
    "| a fact nobody merged | `src/service.py#handler` | Executed |\n"
)


# --- the fold is a move -----------------------------------------------------


def test_every_row_reaches_the_ledger_byte_for_byte_and_the_fragment_is_gone(tree):
    """A move, not a deletion: the ticket's first "done when"."""
    before = {
        name: (tree / "seal" / "ledger" / name).read_text(encoding="utf-8")
        for name in fragments_left(tree)
    }
    fold(tree)
    text = released(tree)
    for name, frag in before.items():
        rows = [line for line in frag.splitlines() if line.startswith("| ")]
        assert rows, f"the fixture fragment {name} has no rows to move"
        for line in rows:
            assert line in text.splitlines(), f"row moved changed or lost:\n{line}"
    assert fragments_left(tree) == [], fragments_left(tree)


def test_the_directory_is_removed_when_it_is_empty(tree):
    fold(tree)
    assert not (tree / "seal" / "ledger").exists()


def test_the_rows_that_were_already_in_the_ledger_stay(tree):
    fold(tree)
    assert "| the old claim |" in ledger(tree)


def test_each_work_item_is_marked_and_headed(tree):
    fold(tree)
    text = released(tree)
    assert "<!-- specs/1788229400-later -->\n### 1788229400-later" in text, text
    assert "<!-- specs/1700000000-earlier -->\n### 1700000000-earlier" in text, text


def test_the_fragment_headings_sit_under_the_work_item(tree):
    """The fragment's `## area` becomes `####`, its `# <id>` title is the
    `###` heading above, and the preamble survives between them."""
    fold(tree)
    text = released(tree)
    assert "#### The area this work item wrote" in text, text
    assert "\n# 1788229400-later\n" not in text, text
    assert "Rows for the later work item." in text, text


def test_the_release_file_is_the_section_and_the_shared_ledger_is_untouched(tree):
    """#547, S5. The release file begins with the version heading, heads
    nothing else, and `seal/ledger.md` keeps its areas and gains no section:
    a release's rows are its own file, and the shared file holds what is
    nobody's release."""
    fold(tree)
    assert re.findall(r"^## (.+)$", released(tree), re.M) == ["0.4.0 — 2026-09-15"]
    assert released(tree).startswith("## 0.4.0 — 2026-09-15\n\n<!-- specs/")
    assert released(tree).endswith("|\n"), repr(released(tree)[-40:])
    assert "\n\n\n" not in released(tree)
    headings = re.findall(r"^## (.+)$", ledger(tree), re.M)
    assert headings == ["Coordinates", "An area from before the fragments"], headings


def test_the_work_items_are_in_id_order(tree):
    fold(tree)
    text = released(tree)
    assert text.index("1700000000-earlier") < text.index("1788229400-later"), text


def test_folding_twice_finds_nothing_and_writes_nothing(tree):
    fold(tree)
    once = released(tree)
    second = run("--version", "0.4.0", "--date", "2026-09-15", root=tree)
    assert second.returncode == 1, second.stdout
    assert "nothing to fold" in second.stdout, second.stdout
    assert released(tree) == once


def test_a_fragment_whose_marker_is_already_in_the_ledger_is_refused(tree):
    """Folding it again would put the same rows in the file twice with no way
    to tell which is current. A stop naming the file is cheaper. #547, S8:
    the marker stands in a release file now, and the refusal names it."""
    fold(tree)
    once = released(tree)
    (tree / "seal" / "ledger").mkdir()
    (tree / "seal" / "ledger" / "1788229400-later.md").write_text(
        fragment(
            "1788229400-later", "Re-created.", [row("late claim", handler_hash())]
        ),
        encoding="utf-8",
    )
    r = run("--version", "0.4.1", "--date", "2026-09-16", root=tree)
    assert r.returncode == 1, r.stdout
    assert "seal/ledger/1788229400-later.md" in r.stdout, r.stdout
    assert "already" in r.stdout, r.stdout
    assert "seal/releases/0.4.0.md" in r.stdout, (
        "the file the marker stands in is not named"
    )
    assert released(tree) == once, "the refusal wrote to the release file"
    assert not release_file(tree, "0.4.1").exists(), "the refusal wrote a release file"
    assert fragments_left(tree) == ["1788229400-later.md"], "the refusal removed it"


# --- a second fold for one version (#540) ---------------------------------


LATE = "1788300000-late"


def late_fragment(tree):
    """A fragment landing after the release pull request went red: the
    ordinary shape a second fold for the same version answers."""
    (tree / "seal" / "ledger").mkdir(exist_ok=True)
    (tree / "seal" / "ledger" / f"{LATE}.md").write_text(
        fragment(
            LATE,
            "Landed after the preparation commit.",
            [row("the late claim", unit_hash("parse"), anchor="parse")],
        ),
        encoding="utf-8",
    )


def test_a_second_fold_for_the_same_version_joins_its_section(tree):
    """#540. `seal/ledger.md` headed `0.9.3` twice through seventeen ledger
    sections (`0.9.4` to `0.15.0`, counted after the second heading): the
    first fold ran at the preparation commit, the pull request went red, a
    fragment landed thirty-one minutes later (`bee7ae99` at 02:04, then
    `4ac9bf35` at 02:35, 2026-09-09 +0900), and the second fold wrote a second
    `## 0.9.3` heading below everything — one release's rows split across
    two sections that read as two releases. The section is joined now, it
    keeps the first fold's date over `--date`, and the file heads the
    version once. The gather's case is the pattern (#289)."""
    fold(tree)
    late_fragment(tree)
    shared = ledger(tree)
    second = run("--version", "0.4.0", "--date", "2026-09-16", root=tree)
    assert second.returncode == 0, second.stdout + second.stderr
    text = released(tree)
    headings = re.findall(r"^## (.+)$", text, re.M)
    assert headings == ["0.4.0 — 2026-09-15"], (
        f"the second fold wrote a second heading, or re-dated the first: {headings}"
    )
    assert ledger(tree) == shared, "the second fold wrote to seal/ledger.md"
    assert "2026-09-16" not in text, text
    assert f"<!-- specs/{LATE} -->\n### {LATE}" in text, text
    # Under the heading, after the work item the first fold wrote.
    assert text.index("### 1788229400-later") < text.index(f"### {LATE}"), text
    assert "| the late claim |" in text, text
    assert "\n\n\n" not in text, f"a run of blank lines:\n{text}"
    assert fragments_left(tree) == [], fragments_left(tree)
    assert (
        "folded 1 fragments into seal/releases/0.4.0.md under ## 0.4.0 — 2026-09-15 "
        "(appended into the existing file)"
    ) in second.stdout, second.stdout
    assert f"seal/ledger/{LATE}.md" in second.stdout, second.stdout
    check = run("--check", root=tree)
    assert check.returncode == 0, check.stdout
    assert (
        "3 work items marked across seal/ledger.md and 1 release file" in check.stdout
    ), check.stdout


def test_the_kept_date_wins_over_today_as_well(tree):
    """S5's second half: with no `--date` at all, today's date is not written
    either — the heading a reader sees is the release date, which is the
    first fold's (Q5, measured here)."""
    fold(tree)
    late_fragment(tree)
    second = run("--version", "0.4.0", root=tree)
    assert second.returncode == 0, second.stdout + second.stderr
    headings = re.findall(r"^## (.+)$", released(tree), re.M)
    assert headings == ["0.4.0 — 2026-09-15"], headings


def test_a_dry_run_of_a_second_fold_shows_the_section_it_appends_into(tree):
    """S6. The preview a person reads before the write says which heading
    the rows join, dated as the file has it — not a fresh heading with a new
    date that the write then does not make."""
    fold(tree)
    late_fragment(tree)
    before = released(tree)
    left = fragments_left(tree)
    r = run("--version", "0.4.0", "--date", "2026-09-16", "--dry-run", root=tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "appending into the existing file:" in r.stdout, r.stdout
    assert "## 0.4.0 — 2026-09-15" in r.stdout, r.stdout
    assert "2026-09-16" not in r.stdout, r.stdout
    assert f"<!-- specs/{LATE} -->" in r.stdout, r.stdout
    assert released(tree) == before, "--dry-run wrote to the release file"
    assert fragments_left(tree) == left, "--dry-run removed a fragment"


def test_check_refuses_a_release_file_that_heads_its_version_twice(tree):
    """#540's S8, re-pointed to the release file (#547, S10). A doubled
    heading is a state `--check` could see and did not refuse — the real
    ledger carried one from `4ac9bf35` to `9f846733` with `--check` green on
    every release in between. It names the file, the version and both lines,
    and the fragment report is still printed beside it."""
    fold(tree)
    text = released(tree) + "\n## 0.4.0 — 2026-09-16\n\nRows under a second heading.\n"
    release_file(tree).write_text(text, encoding="utf-8")
    lines = text.split("\n")
    first = lines.index("## 0.4.0 — 2026-09-15") + 1
    second = lines.index("## 0.4.0 — 2026-09-16") + 1
    late_fragment(tree)
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "seal/releases/0.4.0.md" in r.stdout, r.stdout
    assert str(first) in r.stdout and str(second) in r.stdout, (first, second, r.stdout)
    assert "one release, one file" in r.stdout, r.stdout
    assert f"seal/ledger/{LATE}.md" in r.stdout, r.stdout
    assert "\\" not in r.stdout, r.stdout


def test_check_refuses_a_release_file_named_for_another_version(tree):
    """#547, S10's second half: the file's name and its heading are two
    spellings of one fact, and the fold and every reader key on the name."""
    fold(tree)
    release_file(tree).rename(release_file(tree, "0.4.1"))
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "seal/releases/0.4.1.md" in r.stdout, r.stdout
    assert "heads 0.4.0" in r.stdout, r.stdout


def test_check_refuses_a_release_left_in_the_shared_ledger(tree):
    """#547, S10. After the split `seal/ledger.md` heads no release; a
    section standing there is a fold written to the old place or a split
    not run, and the refusal names the version, the line and the repair.
    The fragment and open-row reports still print beside it."""
    fold(tree)
    shared = ledger(tree) + "\n## 0.4.1 — 2026-09-16\n\nRows folded to the old place.\n"
    (tree / "seal" / "ledger.md").write_text(shared, encoding="utf-8")
    line = shared.split("\n").index("## 0.4.1 — 2026-09-16") + 1
    late_fragment(tree)
    evidence_todo(tree, "1600000000-released-long-ago", OPEN_FILE)
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "seal/ledger.md still heads a release" in r.stdout, r.stdout
    assert f"0.4.1  at line {line}" in r.stdout, r.stdout
    assert "fold_ledger.py --split" in r.stdout, r.stdout
    assert f"seal/ledger/{LATE}.md" in r.stdout, r.stdout
    assert "1600000000-released-long-ago/evidence-todo.md" in r.stdout, r.stdout


def test_a_fold_refuses_a_release_file_that_does_not_head_its_version(tree):
    """#547. A file at `seal/releases/<version>.md` that does not head that
    version is a tree a person should look at, and joining it would write
    the rows under a heading nobody can find. Nothing is written."""
    release_file(tree).parent.mkdir()
    release_file(tree).write_text(
        "## 0.3.9 — 2026-09-01\n\nWrong file.\n", encoding="utf-8"
    )
    left = fragments_left(tree)
    r = run("--version", "0.4.0", "--date", "2026-09-15", root=tree)
    assert r.returncode == 1, r.stdout
    assert "seal/releases/0.4.0.md" in r.stdout and "0.4.0" in r.stdout, r.stdout
    assert released(tree).startswith("## 0.3.9"), "the refusal wrote to the file"
    assert fragments_left(tree) == left, "the refusal removed a fragment"


def test_a_marker_quoted_in_the_ledgers_prose_is_not_a_folded_work_item(tree):
    """Round 1, 🟡 3. A substring test read the marker's shape in prose as a
    fold that had happened, and refused with advice to remove the fragment —
    the only copy of the rows. The mark is a line of its own."""
    text = ledger(tree).replace(
        "> The gathered ledger.",
        "> The gathered ledger. A folded item is marked like "
        "`<!-- specs/1788229400-later -->`.",
    )
    assert "<!-- specs/1788229400-later -->" in text
    (tree / "seal" / "ledger.md").write_text(text, encoding="utf-8")
    fold(tree)
    assert "| the later claim |" in released(tree)
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout
    assert "2 work items marked" in r.stdout, r.stdout


def test_the_messages_print_slash_joined_paths_on_every_platform(tree):
    """Round 1, 🔴 1. `os.path.join` printed `.specseal\\map` on Windows and
    three assertions expected `/`. A backslash in either message is the
    regression, on every leg and not only the Windows one."""
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "\\" not in r.stdout, r.stdout
    fold(tree)
    (tree / "seal" / "ledger").mkdir()
    (tree / "seal" / "ledger" / "1788229400-later.md").write_text(
        fragment("1788229400-later", "Again.", [row("late", handler_hash())]),
        encoding="utf-8",
    )
    for args in (("--version", "0.4.1"), ("--check",)):
        r = run(*args, root=tree)
        assert r.returncode == 1, r.stdout
        assert "seal/ledger/1788229400-later.md" in r.stdout, r.stdout
        assert "\\" not in r.stdout, r.stdout


U2028_ROW = "| a claim\u2028with a line separator | `src/service.py#handler` | c |"


def test_a_row_holding_a_line_separator_arrives_as_one_row(tree):
    """Round 1, 🟡 5 (probe B). `splitlines()` breaks on U+2028, which is
    not a newline to the file, so one row became two lines."""
    (tree / "seal" / "ledger" / "1788229400-later.md").write_text(
        fragment("1788229400-later", "Odd bytes.", [U2028_ROW]), encoding="utf-8"
    )
    fold(tree)
    assert U2028_ROW in released(tree).split("\n"), released(tree)


def test_the_last_row_keeps_its_trailing_whitespace_and_a_fenced_hash_is_text(tree):
    """Round 1, 🟡 5 (probes A and C). `strip()` took the last row's trailing
    tab, and a `#` line inside a code fence was demoted as a heading."""
    last = row("the last claim", unit_hash("parse"), anchor="parse") + " \t"
    body = (
        "# 1788229400-later\n\nA note:\n\n```\n# not a heading\n```\n\n"
        "## The area\n\n| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
        "|---|---|---|---|---|\n" + last + "\n"
    )
    (tree / "seal" / "ledger" / "1788229400-later.md").write_text(
        body, encoding="utf-8"
    )
    fold(tree)
    lines = released(tree).split("\n")
    assert last in lines, "the trailing whitespace was stripped"
    assert "# not a heading" in lines, "the fenced line was demoted"
    assert "#### The area" in lines


def test_a_blank_line_above_the_title_and_a_tilde_fence_are_read_right(tree):
    """Round 2, 🟡 4. A whitespace-only first line left the title to be
    demoted into a second `### <id>`, and only ``` counted as a fence, so a
    `#` line inside `~~~` was demoted. A fence closes on its own kind only."""
    body = (
        "   \n# 1788229400-later\n\nA note:\n\n~~~\n# not a heading\n```\n"
        "# still not a heading\n~~~\n\n## The area\n\n"
        "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
        "|---|---|---|---|---|\n" + row("the claim", handler_hash()) + "\n"
    )
    (tree / "seal" / "ledger" / "1788229400-later.md").write_text(
        body, encoding="utf-8"
    )
    fold(tree)
    lines = released(tree).split("\n")
    assert lines.count("### 1788229400-later") == 1, "the title was demoted twice"
    assert "# not a heading" in lines, "the ~~~ fence was not recognised"
    assert "# still not a heading" in lines, "a ``` inside ~~~ closed the fence"
    assert "#### The area" in lines


def test_dry_run_writes_and_removes_nothing(tree):
    before = ledger(tree)
    left = fragments_left(tree)
    r = run("--version", "0.4.0", "--date", "2026-09-15", "--dry-run", root=tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "## 0.4.0 — 2026-09-15" in r.stdout, r.stdout
    assert "<!-- specs/1700000000-earlier -->" in r.stdout, r.stdout
    assert ledger(tree) == before, "--dry-run wrote to the ledger"
    assert not (tree / "seal" / "releases").exists(), "--dry-run wrote a release file"
    assert fragments_left(tree) == left, "--dry-run removed a fragment"


def test_an_empty_fragment_is_removed_and_named_and_gets_no_marker(tree):
    """A marker with nothing under it would make `--check` say the rows
    arrived when there were none."""
    (tree / "seal" / "ledger" / "1788300000-empty.md").write_text(
        "# 1788300000-empty\n\n", encoding="utf-8"
    )
    r = fold(tree)
    assert "1788300000-empty.md  (empty, removed)" in r.stdout, r.stdout
    assert "1788300000-empty" not in released(tree)
    assert fragments_left(tree) == []


def test_a_missing_ledger_is_a_failure_not_a_fresh_start(tree):
    """Nothing to fold INTO is a broken tree; creating one would hide it."""
    (tree / "seal" / "ledger.md").unlink()
    r = run("--version", "0.4.0", root=tree)
    assert r.returncode == 1, r.stdout
    assert fragments_left(tree) == ["1700000000-earlier.md", "1788229400-later.md"]


# --- a fragment's own marker line (#553) ------------------------------------


def marker_lines(text, work_item_id):
    return [
        n
        for n, ln in enumerate(text.split("\n"), 1)
        if ln == f"<!-- specs/{work_item_id} -->"
    ]


def test_a_fragment_that_begins_with_its_own_marker_is_folded_with_one_marker(tree):
    """#553. Twenty fragments began with their own `<!-- specs/<id> -->`
    line; the fold wrote its marker in front and copied the fragment whole,
    so each marker stood twice in `seal/ledger.md` and `--check` counted
    118 work items over 98 folded sections. The leading marker is the
    fragment's own and is dropped; the fold's is the one that stands."""
    (tree / "seal" / "ledger" / "1788229400-later.md").write_text(
        "<!-- specs/1788229400-later -->\n\n"
        + fragment(
            "1788229400-later",
            "Began with its own marker.",
            [row("the later claim", unit_hash("parse"), anchor="parse")],
        ),
        encoding="utf-8",
    )
    fold(tree)
    text = released(tree)
    assert marker_lines(text, "1788229400-later") == [
        text.split("\n").index("### 1788229400-later")
    ], f"the marker stands more than once, or not above its heading:\n{text}"
    assert "| the later claim |" in text, text
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout
    assert "2 work items marked" in r.stdout, r.stdout


@pytest.mark.parametrize("where", ["seal/ledger.md", "seal/releases/0.4.0.md"])
def test_check_refuses_a_marker_that_stands_twice(tree, where):
    """#553. A marker standing twice is a fold from before the leading line
    was dropped, or a hand edit; `--check` names the file and both lines,
    the way it names a doubled heading, and the fragment report still prints.
    Two shapes of the one defect: `seal/releases/0.4.0.md` marks the work
    item twice in one file, and `seal/ledger.md` marks it once beside the
    release file's marker — one work item in two files, which the count
    reads as two just the same."""
    fold(tree)
    path = tree / where
    text = path.read_text(encoding="utf-8")
    text += "\n<!-- specs/1788229400-later -->\n\nA second marker for one work item.\n"
    path.write_text(text, encoding="utf-8")
    at = marker_lines(text, "1788229400-later")
    late_fragment(tree)
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert where in r.stdout, r.stdout
    assert "1788229400-later" in r.stdout, r.stdout
    assert all(f"{where}:{n}" in r.stdout for n in at), (at, r.stdout)
    assert "seal/releases/0.4.0.md:" in r.stdout, r.stdout
    assert "one work item, one marker" in r.stdout, r.stdout
    assert f"seal/ledger/{LATE}.md" in r.stdout, r.stdout


# --- --split: the sections folded before #547 move once --------------------


def ledger_hash(text, heading):
    """The hash a row citing `seal/ledger.md#"<heading>"` carries."""
    a, b = ec.resolve("seal/ledger.md", f'"{heading}"', text)[0]
    return ec.content_hash(text.splitlines()[a - 1 : b])


SPLIT_HEAD = (
    "# spec-to-code map\n\n> The gathered ledger.\n\n## Coordinates\n\n"
    "| Item | Value |\n|---|---|\n| Coordinate notation | `path#anchor@hash` |\n\n"
    "## An area from before the fragments\n\n"
    "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
    "|---|---|---|---|---|\n"
    "| the old claim | `src/service.py#handler@{h}` | read | 2026-09-01 | |\n"
    "{standing}"
)
SECTION_A = (
    "## 0.1.0 — 2026-01-01\n\n<!-- specs/1700000001-alpha -->\n### 1700000001-alpha\n\n"
    "#### An area alpha wrote\n\n```\n# a fenced line, not a heading\n```\n\n"
    "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
    "|---|---|---|---|---|\n"
    "| alpha's claim | `src/service.py#parse@{p}` | read | 2026-01-01 | |\n\n"
)
SECTION_B = (
    "## 0.2.0 — 2026-02-01\n\n<!-- specs/1700000002-beta -->\n### 1700000002-beta\n\n"
    "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
    "|---|---|---|---|---|\n"
    "| beta's claim | `src/service.py#Box@{b}` | read | 2026-02-01 | |\n\n"
)
SECTION_C = (
    "## 0.3.0 — 2026-03-01\n\n<!-- specs/1700000003-gamma -->\n### 1700000003-gamma\n\n"
    "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
    "|---|---|---|---|---|\n"
    "| gamma cites alpha's folded rows | {self_anchor} | read | 2026-03-01 | |\n"
)


@pytest.fixture
def split_tree(tmp_path):
    """A ledger in the pre-#547 shape: a header, the standing areas, three
    folded release sections — one with a `####` heading and a fenced `#`
    line — and a row in the last section anchored into the first, the shape
    of this repository's one self-anchored row. No fragment is left."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    head = SPLIT_HEAD.format(h=handler_hash(), standing="")
    a = SECTION_A.format(p=unit_hash("parse"))
    b = SECTION_B.format(b=unit_hash("Box"))
    draft = head + "\n" + a + b + SECTION_C.format(self_anchor="`x`")
    h_alpha = ledger_hash(draft, "### 1700000001-alpha")
    h_area = ledger_hash(draft, "## Coordinates")
    standing = (
        f'| the notation is read first | `seal/ledger.md#"## Coordinates"@{h_area}` '
        "| read | 2026-09-01 | |\n"
    )
    anchor = f'`seal/ledger.md#"### 1700000001-alpha"@{h_alpha}`'
    text = (
        SPLIT_HEAD.format(h=handler_hash(), standing=standing)
        + "\n"
        + a
        + b
        + SECTION_C.format(self_anchor=anchor)
    )
    (tmp_path / "seal").mkdir()
    (tmp_path / "seal" / "ledger.md").write_text(text, encoding="utf-8")
    return tmp_path


def table_rows(text):
    return [line for line in text.split("\n") if line.startswith("| ")]


def test_the_split_moves_every_release_section_byte_for_byte(split_tree):
    """#547, S11. Each `## X.Y.Z` section of `seal/ledger.md` becomes
    `seal/releases/<X.Y.Z>.md`, its text from the heading to the next `## `
    ending in one newline; `seal/ledger.md` keeps the header and the
    standing areas; every table row of the file before is in exactly one
    file after, and the rewritten anchor is the only row whose bytes moved."""
    before = ledger(split_tree)
    r = run("--split", root=split_tree)
    assert r.returncode == 0, r.stdout + r.stderr
    names = sorted(p.name for p in (split_tree / "seal" / "releases").iterdir())
    assert names == ["0.1.0.md", "0.2.0.md", "0.3.0.md"], names
    lines = before.split("\n")
    for version in ("0.1.0", "0.2.0"):
        start = next(n for n, ln in enumerate(lines) if ln.startswith(f"## {version} "))
        end = next(
            n for n in range(start + 1, len(lines)) if lines[n].startswith("## ")
        )
        want = "\n".join(lines[start:end]).rstrip("\n") + "\n"
        assert released(split_tree, version) == want, version
    assert "# a fenced line, not a heading" in released(split_tree, "0.1.0")
    shared = ledger(split_tree)
    assert re.findall(r"^## (.+)$", shared, re.M) == [
        "Coordinates",
        "An area from before the fragments",
    ], shared
    assert shared.endswith("| read | 2026-09-01 | |\n"), repr(shared[-60:])
    assert not shared.endswith("\n\n"), repr(shared[-60:])
    after = table_rows(shared)
    for version in ("0.1.0", "0.2.0", "0.3.0"):
        after += table_rows(released(split_tree, version))
    moved = [row.replace("seal/releases/0.1.0.md#", "seal/ledger.md#") for row in after]
    assert sorted(moved) == sorted(table_rows(before)), (
        "a row was lost, added or changed"
    )
    check = run("--check", root=split_tree)
    assert check.returncode == 0, check.stdout
    assert (
        "3 work items marked across seal/ledger.md and 3 release files" in check.stdout
    )


def test_a_second_split_has_nothing_to_move(split_tree):
    assert run("--split", root=split_tree).returncode == 0
    shared = ledger(split_tree)
    r = run("--split", root=split_tree)
    assert r.returncode == 1, r.stdout
    assert "nothing to split" in r.stdout, r.stdout
    assert ledger(split_tree) == shared


def test_the_split_refuses_a_target_that_exists_and_writes_nothing(split_tree):
    """#547, judgment 7: a target present before the split is a tree in a
    state nobody planned, and joining it would hide that. The join is the
    fold's; the split refuses and names the file."""
    before = ledger(split_tree)
    target = release_file(split_tree, "0.2.0")
    target.parent.mkdir()
    target.write_text("## 0.2.0 — 2026-02-01\n\nAlready here.\n", encoding="utf-8")
    r = run("--split", root=split_tree)
    assert r.returncode == 1, r.stdout
    assert "seal/releases/0.2.0.md" in r.stdout and "exists" in r.stdout, r.stdout
    assert ledger(split_tree) == before, "the refusal wrote to seal/ledger.md"
    assert sorted(p.name for p in target.parent.iterdir()) == ["0.2.0.md"]
    assert target.read_text(encoding="utf-8").endswith("Already here.\n")


def test_the_split_refuses_a_version_the_ledger_heads_twice(split_tree):
    """C's reader (#540), asked before anything moves: two sections for one
    version would need joining, which is a person's call."""
    text = ledger(split_tree) + "\n## 0.2.0 — 2026-02-02\n\nA second section.\n"
    (split_tree / "seal" / "ledger.md").write_text(text, encoding="utf-8")
    r = run("--split", root=split_tree)
    assert r.returncode == 1, r.stdout
    assert "0.2.0" in r.stdout and "twice" in r.stdout, r.stdout
    assert ledger(split_tree) == text
    assert not (split_tree / "seal" / "releases").exists()


def test_the_split_rewrites_an_anchor_into_a_moved_section(split_tree):
    """#547, S12. A row citing `seal/ledger.md#"### <id>"@<h>` whose heading
    moved cites `seal/releases/<X.Y.Z>.md#"### <id>"@<h>` after, the same
    hash, because the anchored region is byte-identical in its new file. An
    anchor into the standing area is left as it is. The checker reports
    both OK before and after."""
    before_line, before_rc = check(split_tree)
    assert (
        before_rc == 0 and "0 drifted" in before_line and "0 broken" in before_line
    ), before_line
    old = re.search(
        r'seal/ledger\.md#"### 1700000001-alpha"@([0-9a-f]+)', ledger(split_tree)
    )
    r = run("--split", root=split_tree)
    assert r.returncode == 0, r.stdout
    moved = released(split_tree, "0.3.0")
    assert f'`seal/releases/0.1.0.md#"### 1700000001-alpha"@{old.group(1)}`' in moved, (
        moved
    )
    assert 'seal/ledger.md#"### 1700000001-alpha"' not in moved, moved
    assert 'seal/ledger.md#"## Coordinates"@' in ledger(split_tree)
    after_line, after_rc = check(split_tree)
    assert after_rc == 0, after_line
    assert "0 drifted" in after_line and "0 broken" in after_line, after_line
    assert "rewrote 1 anchor" in r.stdout, r.stdout


def test_the_split_names_only_the_anchors_it_cannot_place(split_tree):
    """#547, round 1's 🟡 1. The split reads an anchor the way the checker
    does: a quoted locator whose first part is a heading is a heading path,
    anything else is one whole line, and only a coordinate with a hash is an
    anchor. So a line the standing area keeps is left and not named, a
    backticked mention with no hash is prose, and a line inside a moved
    section follows it to the release file — keyed on the whole line, since
    a ` / ` in it does not make it a heading path."""
    path = split_tree / "seal" / "ledger.md"
    text = path.read_text(encoding="utf-8").replace(
        "### 1700000002-beta\n\n",
        "### 1700000002-beta\n\nA sentence beta wrote / with a slash in it.\n\n",
    )
    kept = ledger_hash(text, "> The gathered ledger.")
    line = ledger_hash(text, "A sentence beta wrote / with a slash in it.")
    rows = (
        f'| a header line | `seal/ledger.md#"> The gathered ledger."@{kept}` '
        "| read | 2026-09-01 | |\n"
        f'| a moved line | `seal/ledger.md#"A sentence beta wrote / with a slash in it."@{line}` '
        '| read | 2026-09-01 | the shape `seal/ledger.md#"<heading>"` |\n'
    )
    at = text.index("\n", text.index("| the old claim |")) + 1
    path.write_text(text[:at] + rows + text[at:], encoding="utf-8")
    before_line, before_rc = check(split_tree)
    assert before_rc == 0 and "0 broken" in before_line, before_line
    r = run("--split", root=split_tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "could not place" not in r.stdout, r.stdout
    shared = ledger(split_tree)
    assert f'`seal/ledger.md#"> The gathered ledger."@{kept}`' in shared, shared
    assert (
        f'`seal/releases/0.2.0.md#"A sentence beta wrote / with a slash in it."@{line}`'
        in shared
    ), shared
    after_line, after_rc = check(split_tree)
    assert after_rc == 0 and "0 broken" in after_line, after_line


def test_a_line_the_standing_area_also_holds_is_named_not_moved(split_tree):
    """#547, round 2's ⬜ 3. A line in the standing area and in a moved
    section is two places to the checker, which the row's hash decides; the
    split reads no hash, so it names the anchor and moves nothing."""
    path = split_tree / "seal" / "ledger.md"
    text = (
        path.read_text(encoding="utf-8")
        .replace(
            "## An area from before the fragments\n\n",
            "## An area from before the fragments\n\nShared line.\nMore standing text.\n\n",
        )
        .replace("### 1700000002-beta\n\n", "### 1700000002-beta\n\nShared line.\n\n")
    )
    a, b = ec.resolve("seal/ledger.md", '"Shared line."', text)[0]
    h = ec.content_hash(text.splitlines()[a - 1 : b])
    row = f'| a standing line | `seal/ledger.md#"Shared line."@{h}` | read | 2026-09-01 | |\n'
    at = text.index("\n", text.index("| the old claim |")) + 1
    path.write_text(text[:at] + row + text[at:], encoding="utf-8")
    r = run("--split", root=split_tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert 'seal/ledger.md  seal/ledger.md#"Shared line."' in r.stdout, r.stdout
    after_line, after_rc = check(split_tree)
    assert after_rc == 0 and "0 drifted" in after_line, after_line


def test_a_line_two_moved_sections_and_the_standing_area_hold_is_named(split_tree):
    """#547, round 2's ⬜ 3, its second shape. A line two moved sections share
    drops out of `moved`; if the standing area holds it too, keeping the
    anchor is a guess the row's hash may contradict. Here the row's hash is
    beta's copy, so keeping it would leave it pointing at the standing one."""
    path = split_tree / "seal" / "ledger.md"
    text = (
        path.read_text(encoding="utf-8")
        .replace(
            "## An area from before the fragments\n\n",
            "## An area from before the fragments\n\nShared line.\nMore standing text.\n\n",
        )
        .replace("### 1700000001-alpha\n\n", "### 1700000001-alpha\n\nShared line.\n\n")
        .replace(
            "### 1700000002-beta\n\n",
            "### 1700000002-beta\n\nShared line.\nBeta's own.\n\n",
        )
    )
    beta = text.split("\n").index("### 1700000002-beta") + 1
    regions = ec.resolve("seal/ledger.md", '"Shared line."', text)
    a, b = next((a, b) for a, b in regions if a > beta)
    h = ec.content_hash(text.splitlines()[a - 1 : b])
    row = f'| beta\'s line | `seal/ledger.md#"Shared line."@{h}` | read | 2026-09-01 | |\n'
    at = text.index("\n", text.index("| the old claim |")) + 1
    path.write_text(text[:at] + row + text[at:], encoding="utf-8")
    r = run("--split", "--dry-run", root=split_tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "could not place" in r.stdout, r.stdout
    assert 'seal/ledger.md  seal/ledger.md#"Shared line."' in r.stdout, r.stdout


def test_the_split_reads_an_escaped_quote_the_way_the_checker_does(split_tree):
    """#547, round 1's 🟡 1, its fourth symptom. A locator holding `\\"` is
    one locator to the checker; the split reads it whole and rewrites it."""
    path = split_tree / "seal" / "ledger.md"
    said = 'A sentence beta wrote, "quoted" inside.'
    text = path.read_text(encoding="utf-8").replace(
        "### 1700000002-beta\n\n", f"### 1700000002-beta\n\n{said}\n\n"
    )
    h = ledger_hash(text, said)
    escaped = said.replace('"', '\\"')
    row = (
        f'| a quoted line | `seal/ledger.md#"{escaped}"@{h}` | read | 2026-09-01 | |\n'
    )
    at = text.index("\n", text.index("| the old claim |")) + 1
    path.write_text(text[:at] + row + text[at:], encoding="utf-8")
    before_line, before_rc = check(split_tree)
    assert before_rc == 0 and "0 broken" in before_line, before_line
    r = run("--split", root=split_tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "could not place" not in r.stdout, r.stdout
    assert f'`seal/releases/0.2.0.md#"{escaped}"@{h}`' in ledger(split_tree), r.stdout
    after_line, after_rc = check(split_tree)
    assert after_rc == 0 and "0 broken" in after_line, after_line


def test_each_identical_rewrite_prints_its_own_line(split_tree):
    """#547, round 1's ⬜ 9. Two rows in one file citing the same moved
    heading are two rewrites at two lines; the first occurrence's line was
    printed for both."""
    path = split_tree / "seal" / "ledger.md"
    text = path.read_text(encoding="utf-8")
    row = next(ln for ln in text.split("\n") if "gamma cites alpha" in ln)
    path.write_text(
        text.replace(row, row + "\n" + row.replace("gamma cites", "gamma again cites")),
        encoding="utf-8",
    )
    r = run("--split", "--dry-run", root=split_tree)
    assert r.returncode == 0, r.stdout + r.stderr
    printed = re.findall(r"^  seal/releases/0\.3\.0\.md:(\d+)  ", r.stdout, re.M)
    assert len(printed) == 2 and printed[0] != printed[1], r.stdout


def test_a_dry_run_of_the_split_says_what_would_move_and_writes_nothing(split_tree):
    """#547, S13. The preview a person reads at the release: each version,
    its line range and row count, and each anchor it would rewrite."""
    before = ledger(split_tree)
    r = run("--split", "--dry-run", root=split_tree)
    assert r.returncode == 0, r.stdout + r.stderr
    lines = before.split("\n")
    start = next(n for n, ln in enumerate(lines) if ln.startswith("## 0.1.0 ")) + 1
    assert f"0.1.0  lines {start}-" in r.stdout, r.stdout
    assert "seal/releases/0.1.0.md  (1 row)" in r.stdout, r.stdout
    assert "seal/releases/0.3.0.md  (1 row)" in r.stdout, r.stdout
    assert 'seal/ledger.md#"### 1700000001-alpha"' in r.stdout, r.stdout
    assert "-> seal/releases/0.1.0.md" in r.stdout, r.stdout
    assert "nothing written" in r.stdout, r.stdout
    assert ledger(split_tree) == before
    assert not (split_tree / "seal" / "releases").exists()


SELF_ANCHORED = {
    "### 1788331011-two-roots-hold-three-lifetimes": "0.4.0",
    "### 1788398967-local-modes-records-never-leave-the-clone": "0.5.0",
}


def test_the_split_rehearsed_over_this_repositorys_ledger(tmp_path):
    """#547, S14. The real split runs once, at the release-preparation commit
    that ships this work; this is the rehearsal, over a copy of this
    repository's `seal/ledger.md`, every run.

    Every release section becomes a file named for its version; every table
    row of the copy stands in exactly one file after, the self-anchored row's
    two anchors excepted, which move to the release files their headings
    moved to with the same hash and resolve OK there; and `check_ledger`
    gives the same `(status, coordinate)` set before and after, in process,
    for every other anchor.

    Once the real split has run, `seal/ledger.md` heads no release and there
    is nothing left to rehearse, so the case asserts the result instead:
    release files are there, and the two anchors point into them. Green on
    both shapes of the tree, and vacuous on neither."""
    real = read("seal", "ledger.md")
    if not re.search(r"^## \d+\.\d+\.\d+", real, re.M):
        releases = os.path.join(ROOT, "seal", "releases")
        assert os.path.isdir(releases) and os.listdir(releases), (
            "seal/ledger.md heads no release and seal/releases/ is empty"
        )
        corpus = "\n".join(
            read("seal", "releases", n) for n in sorted(os.listdir(releases))
        )
        for heading, version in SELF_ANCHORED.items():
            assert f'seal/releases/{version}.md#"{heading}"@' in corpus, heading
        return
    (tmp_path / "seal").mkdir()
    copy = tmp_path / "seal" / "ledger.md"
    copy.write_text(real, encoding="utf-8")
    versions = re.findall(r"^## (\d+\.\d+\.\d+)", real, re.M)
    assert len(versions) == len(set(versions)), (
        f"the ledger heads a version twice: {versions}"
    )
    hashes = {
        h: re.search(rf'seal/ledger\.md#"{re.escape(h)}"@([0-9a-f]+)', real).group(1)
        for h in SELF_ANCHORED
    }
    before = {
        (status, coord)
        for status, coord, _ in ec.check_ledger(str(copy), ROOT, {})
        if not coord.startswith("seal/ledger.md#")
    }
    assert before, "the checker found nothing in the copy"

    r = run("--split", root=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    releases = tmp_path / "seal" / "releases"
    assert sorted(p.name for p in releases.iterdir()) == sorted(
        f"{v}.md" for v in versions
    )
    files = [copy, *sorted(releases.iterdir())]
    texts = {p: p.read_text(encoding="utf-8") for p in files}
    assert not re.search(r"^## \d+\.\d+\.\d+", texts[copy], re.M)
    assert "rewrote 2 anchors" in r.stdout, r.stdout

    rows_after = [row for p in files for row in table_rows(texts[p])]
    for heading, version in SELF_ANCHORED.items():
        rows_after = [
            row.replace(
                f'seal/releases/{version}.md#"{heading}"', f'seal/ledger.md#"{heading}"'
            )
            for row in rows_after
        ]
    assert sorted(rows_after) == sorted(table_rows(real)), (
        "a row was lost, added or changed"
    )

    after = set()
    for p in files:
        for status, coord, _ in ec.check_ledger(str(p), ROOT, {}):
            if not coord.startswith(("seal/ledger.md#", "seal/releases/")):
                after.add((status, coord))
    assert after == before, (sorted(before - after)[:5], sorted(after - before)[:5])

    moved = "\n".join(texts.values())
    for heading, version in SELF_ANCHORED.items():
        new = f'seal/releases/{version}.md#"{heading}"@{hashes[heading]}'
        assert new in moved, f"the anchor was not rewritten to {new}"
        row = next(ln for ln in moved.split("\n") if new in ln)
        found = {
            (status, coord)
            for status, coord, _ in ec.check_text(row, str(tmp_path), {})
            if coord.startswith("seal/releases/")
        }
        assert ("OK", f'seal/releases/{version}.md#"{heading}"') in found, found


# --- the checker cannot tell ------------------------------------------------


def test_the_checker_reports_the_same_totals_before_and_after(tree):
    """A row is a content anchor, so moving it between files changes nothing
    the checker measures. Both runs are executed here, not inferred."""
    before, before_rc = check(tree)
    assert before_rc == 0 and "0 broken" in before and "0 drifted" in before, before
    assert "4 ok" in before, before  # one old row, three fragment rows
    fold(tree)
    after, after_rc = check(tree)
    assert (after, after_rc) == (before, before_rc), (before, after)


def test_a_row_a_fragment_repeats_from_the_shared_ledger_is_still_counted_twice(tree):
    """`check_ledger` de-duplicates on (coordinate, hash) within one file.
    Before #547 a row a fragment repeated from `seal/ledger.md` counted
    twice before the fold and once after, because the fold put it in the
    same file; the fold writes a release file now, so the repeat stays in a
    file of its own and the total does not move. The one thing a fold used
    to change is gone, and a release reading the same total is the shape."""
    (tree / "seal" / "ledger" / "1788229400-later.md").write_text(
        fragment(
            "1788229400-later",
            "A repeat.",
            [row("the old claim again", handler_hash())],
        ),
        encoding="utf-8",
    )
    before, _ = check(tree)
    assert "4 ok" in before, before
    fold(tree)
    after, rc = check(tree)
    assert "4 ok" in after and rc == 0, after


# --- the guard --------------------------------------------------------------


def test_an_open_evidence_todo_row_refuses_the_fold_and_touches_nothing(tree):
    evidence_todo(tree, "1700000000-earlier", OPEN_FILE)
    before = ledger(tree)
    left = fragments_left(tree)
    r = run("--version", "0.4.0", "--date", "2026-09-15", root=tree)
    assert r.returncode == 1, r.stdout
    assert "seal/specs/1700000000-earlier/evidence-todo.md" in r.stdout, r.stdout
    assert "1 open row" in r.stdout, r.stdout
    assert ledger(tree) == before, "the refusal wrote to the ledger"
    assert fragments_left(tree) == left, "the refusal removed a fragment"


def test_the_guard_reads_every_work_item_in_the_tree_not_only_folded_ones(tree):
    """Q1: a work item released earlier whose file was never drained blocks
    this release too. It has no fragment left, and it still stops the fold."""
    evidence_todo(tree, "1600000000-released-long-ago", OPEN_FILE)
    r = run("--version", "0.4.0", root=tree)
    assert r.returncode == 1, r.stdout
    assert "1600000000-released-long-ago" in r.stdout, r.stdout


@pytest.mark.parametrize(
    "shape, text",
    [
        (
            "drained above the table",
            "# facts\n\ndrained — all rows merged at abc1234.\n\n"
            "| Claim | Grounds | Label |\n|---|---|---|\n| a | b | c |\n",
        ),
        (
            "drained below the table",
            "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n| a | b | c |\n\n"
            "drained — applied by the round-1 fix pass.\n",
        ),
        (
            "drained in bold",
            "# facts\n\n**Drained.**\n\n"
            "| Claim | Grounds | Label |\n|---|---|---|\n| a | b | c |\n",
        ),
        (
            "every row marked",
            "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n"
            "| ✅ a | merged at abc1234 | c |\n| ✅ b | merged at abc1234 | c |\n",
        ),
        (
            "header and no body row",
            "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n",
        ),
        ("no table at all", "# facts\n\nnothing was prescribed.\n"),
    ],
)
def test_a_closed_evidence_todo_file_does_not_refuse(tree, shape, text):
    evidence_todo(tree, "1700000000-earlier", text)
    r = run("--version", "0.4.0", "--date", "2026-09-15", root=tree)
    assert r.returncode == 0, f"{shape}:\n{r.stdout}{r.stderr}"


@pytest.mark.parametrize(
    "shape, text",
    [
        (
            "not drained is not drained",
            "# facts\n\nnot drained yet.\n\n"
            "| Claim | Grounds | Label |\n|---|---|---|\n| a | b | c |\n",
        ),
        (
            "one row marked, one not",
            "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n"
            "| ✅ a | merged | c |\n| b | still waiting | c |\n",
        ),
        (
            "drained inside a table cell does not close the file",
            "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n"
            "| drained | b | c |\n",
        ),
    ],
)
def test_an_open_shape_refuses(tree, shape, text):
    evidence_todo(tree, "1700000000-earlier", text)
    r = run("--version", "0.4.0", root=tree)
    assert r.returncode == 1, f"{shape}:\n{r.stdout}"
    assert "1700000000-earlier/evidence-todo.md" in r.stdout, r.stdout


def test_a_line_separator_in_a_cell_does_not_close_the_file(tree):
    """Round 1, 🟡 4 (probe E). `splitlines()` read the cell's tail after
    U+2028 as a line of its own, and `drained` there closed the file: zero
    open rows where one was — the silent direction for a guard."""
    evidence_todo(
        tree,
        "1700000000-earlier",
        "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n"
        "| a claim\u2028drained | b | c |\n",
    )
    r = run("--version", "0.4.0", root=tree)
    assert r.returncode == 1, r.stdout
    assert "1700000000-earlier/evidence-todo.md  (1 open row)" in r.stdout, r.stdout


def test_a_work_item_without_the_file_has_no_open_row(tree):
    """The fixture's second work item has no `seal/specs/` directory at all."""
    assert not (tree / "seal" / "specs" / "1700000000-earlier").exists()
    fold(tree)


# --- --check ----------------------------------------------------------------


def test_check_fails_while_a_fragment_is_left(tree):
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "seal/ledger/1788229400-later.md" in r.stdout, r.stdout
    assert "seal/ledger/1700000000-earlier.md" in r.stdout, r.stdout


def test_check_fails_on_an_open_evidence_todo_row_even_with_nothing_to_fold(tree):
    """Q3: a fold done by hand still meets the guard at the release pull
    request, the last moment anyone is looking."""
    fold(tree)
    evidence_todo(tree, "1600000000-released-long-ago", OPEN_FILE)
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "1600000000-released-long-ago/evidence-todo.md" in r.stdout, r.stdout


def test_check_passes_once_folded_and_says_what_it_counted(tree):
    fold(tree)
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout
    # A `--check` that exits 0 because it found nothing at all would satisfy
    # the line above. It has to say it saw both work items, and where.
    assert "2 work items marked across seal/ledger.md and 1 release file" in r.stdout, (
        r.stdout
    )


def test_a_copy_edit_to_a_folded_section_does_not_reopen_it(tree):
    """Marked, not matched: re-wording a folded note leaves `--check` green."""
    fold(tree)
    text = released(tree).replace("the later claim", "the later claim, reworded")
    release_file(tree).write_text(text, encoding="utf-8")
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout


def test_check_names_a_left_fragment_whose_marker_is_already_there(tree):
    fold(tree)
    (tree / "seal" / "ledger").mkdir()
    (tree / "seal" / "ledger" / "1788229400-later.md").write_text(
        fragment("1788229400-later", "Re-created.", [row("late", handler_hash())]),
        encoding="utf-8",
    )
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "compare by hand" in r.stdout, r.stdout


# --- this repository --------------------------------------------------------


def test_the_release_pull_request_runs_the_check():
    """A convention nothing enforces is a convention somebody forgets at the
    release, which is the last moment anyone is looking."""
    workflow = read(".github", "workflows", "hygiene.yml")
    assert "fold_ledger.py --check" in workflow, (
        "the release workflow does not check the ledger fragments"
    )
    assert os.path.isfile(SCRIPT), "the workflow calls a script that is not there"


def test_the_check_only_runs_for_a_release():
    """On a feature pull request every fragment on the branch is legitimately
    unfolded — running it there would fail every branch that writes one."""
    workflow = read(".github", "workflows", "hygiene.yml")
    step = workflow.split("every ledger fragment folded into the gathered ledger")[1]
    step = step.split("- name:")[0]
    assert 'github.base_ref }}" != "main"' in step, (
        "the step no longer skips itself outside a release pull request"
    )


def test_no_document_says_the_fragments_are_never_gathered():
    """Every place that said so now says what is true: rows go in the
    fragment during development and the release folds them into `map.md`."""
    for parts in (
        ("CLAUDE.md",),
        ("CONTRIBUTING.md",),
        ("README.md",),
        ("README.ko.md",),
        ("seal", "README.md"),
        ("seal", "ledger.md"),
        ("templates", "ledger.md"),
        ("templates", "seal-README.md"),
        ("skills", "implement", "SKILL.md"),
        ("skills", "evidence-check", "SKILL.md"),
        ("docs", "branch-and-release.md"),
    ):
        text = flat(*parts)
        for old in (
            "never gathered",
            "never are",
            "Fragments are never gathered back",
            "stays where it is forever",
            "다시 합치지 않는다",
        ):
            assert old not in text, "/".join(parts) + f" still says: {old}"


def test_the_release_sequence_names_the_fold_beside_the_gather():
    """The sequence in `docs/branch-and-release.md` is walked by whoever cuts
    a release, and `CONTRIBUTING.md` holds the commands. A step that is only
    in a workflow comment is a step that gets discovered by a red build."""
    for parts in (("docs", "branch-and-release.md"), ("CONTRIBUTING.md",)):
        text = flat(*parts)
        assert "fold_ledger.py" in text, (
            "/".join(parts) + " does not name the script that folds the ledger"
        )
        assert text.index("gather_changelog.py") < text.index("fold_ledger.py"), (
            "/".join(parts) + " names the fold before the gather it belongs beside"
        )


THIS_WORK_ITEM = "1788326734-the-ledger-fragments-are-never-gathered"


def folded_ledgers(root):
    """`seal/ledger.md` and every release file, where a folded section can
    stand: in the shared file until `--split` moves it, in
    `seal/releases/<X.Y.Z>.md` after (#547)."""
    paths = [os.path.join(root, "seal", "ledger.md")]
    paths += sorted(glob.glob(os.path.join(root, "seal", "releases", "*.md")))
    out = []
    for path in paths:
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                out.append(f.read())
    return out


def this_work_items_rows_are_in_the_ledger(root):
    """The fragment while it exists, its folded section in a ledger after.

    Round 1, 🔴 2: reading the fragment alone is a permanent test of a file
    that lives between releases, which is the shape the dependency rule names
    "would break on removal" — the release-preparation commit would have
    turned the tests red on its own pull request.
    """
    frag = os.path.join(root, "seal", "ledger", f"{THIS_WORK_ITEM}.md")
    if os.path.isfile(frag):
        with open(frag, encoding="utf-8") as f:
            text = f.read()
        where = "the fragment"
    else:
        marker = f"<!-- specs/{THIS_WORK_ITEM} -->"
        holding = [t for t in folded_ledgers(root) if marker in t.split("\n")]
        assert holding, "this work item wrote no ledger fragment, and no fold marked it"
        text = holding[0].split(marker, 1)[1]
        where = "the folded section"
    assert "fold_ledger.py#" in text, f"{where} cites nothing in the script"


def test_this_work_item_wrote_its_own_fragment():
    """Dogfood. A convention the branch introducing it did not follow is one
    nobody has tried."""
    this_work_items_rows_are_in_the_ledger(ROOT)


def test_this_work_items_rows_are_still_found_after_the_release_folds_them(tree):
    """The same body, on the fixture with a fragment for this work item placed
    there and folded. Round 2, 🔴 1 and 🟡 2: the first version copied the
    real tree, so once the release-preparation commit had folded it the copy
    held nothing to fold and the test went red on `main`; and the `specs/`
    copy made any open evidence-todo row in the tree fail it, which is the
    review's own mid-state."""
    frag = tree / "seal" / "ledger" / f"{THIS_WORK_ITEM}.md"
    frag.write_text(
        fragment(
            THIS_WORK_ITEM,
            "Rows for this work item.",
            [row("the fold", handler_hash(), "`.github/scripts/fold_ledger.py#main`")],
        ),
        encoding="utf-8",
    )
    this_work_items_rows_are_in_the_ledger(str(tree))
    fold(tree)
    assert not frag.exists(), "the fold removed nothing"
    this_work_items_rows_are_in_the_ledger(str(tree))
