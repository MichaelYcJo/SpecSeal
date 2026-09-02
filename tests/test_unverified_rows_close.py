"""The record of what was never verified has to be readable, and rows have to
leave it by being closed rather than deleted.

Every case here is a way the corpus already drifted or a way a tolerant reader
would have reported zero. Zero is the dangerous answer: it is indistinguishable
from "everything has been closed", which is the sentence this repository exists
to make expensive.
"""

import atexit
import importlib.util
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
from conftest import symlink_or_skip

ROOT = os.path.join(os.path.dirname(__file__), "..")
SCRIPT = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")


def load():
    spec = importlib.util.spec_from_file_location("unverified_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


uc = load()
CLOSED_MARK = uc.CLOSED

CANONICAL = """## Not verified

| Item | Who must answer |
|---|---|
| how the gate renders in a TUI | user, on the next session |
| whether Windows hooks fire | a maintainer with a Windows machine |
"""


def write(tmp_path, section, name="1780000000-work"):
    d = tmp_path / "specs" / name
    d.mkdir(parents=True)
    p = d / "overview.md"
    p.write_text(
        f"# {name} — overview\n\n## Not done\n\nsomething.\n\n{section}",
        encoding="utf-8",
    )
    return str(p)


def run(argv):
    """The CLI's exit code, so a test asserts what CI would see."""
    return uc.main(argv)


def test_unmarked_rows_are_counted_open(tmp_path):
    """The default has to be open. If an unmarked row read as closed, doing
    nothing would close the record."""
    op, cl, err = uc.check_file(write(tmp_path, CANONICAL))
    assert not err
    assert len(op) == 2 and not cl


def test_a_marked_row_counts_closed_and_keeps_its_text(tmp_path):
    """Closing is marking, so the item stays legible after it is closed."""
    section = CANONICAL.replace(
        "| how the gate renders in a TUI | user, on the next session |",
        "| ✅ how the gate renders in a TUI | seen on screen 2026-08-25, session log |",
    )
    op, cl, err = uc.check_file(write(tmp_path, section))
    assert not err
    assert len(op) == 1
    assert cl[0][1] == "how the gate renders in a TUI"


def test_a_bare_check_mark_does_not_close_anything(tmp_path):
    """A tick with nothing after it is the checkbox this repo refuses
    everywhere else — `plan.md`'s Verified-by column exists for the same
    reason."""
    section = CANONICAL.replace(
        "| how the gate renders in a TUI | user, on the next session |",
        "| ✅ | done |",
    )
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "bare" in err[0][1]


def test_a_row_with_an_empty_cell_fails(tmp_path):
    section = CANONICAL + "| an item with no answerer | |\n"
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "empty cell" in err[0][1]


def test_the_template_placeholder_row_fails(tmp_path):
    """A spec bootstrapped from the template and never filled in used to read
    as one open item with no content."""
    section = CANONICAL + "| <what was not verified> | <who answers it> |\n"
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "placeholder" in err[0][1]


@pytest.mark.parametrize(
    "heading",
    [
        "## Not verified (who must answer)",
        "## Blocked / not verified (who must answer)",
        "## Not Verified",
    ],
)
def test_a_heading_spelling_it_does_not_know_is_an_error_not_a_zero(tmp_path, heading):
    """All three spellings are real. Two of them were in this corpus, and one
    kept its rows out of the hand count that opened this work. The failure
    being prevented is a reader that shrugs and returns zero."""
    section = CANONICAL.replace("## Not verified", heading)
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err
    assert "no `## Not verified` section" in err[0][1]
    assert heading in err[0][1], "the error has to name the spelling it found"


def test_the_old_column_name_fails(tmp_path):
    """Three overviews used `| Item | Who |`. One accepted spelling is what
    keeps the next one from being invented silently."""
    section = CANONICAL.replace("| Item | Who must answer |", "| Item | Who |")
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "header is" in err[0][1]


def test_a_missing_section_is_an_error(tmp_path):
    p = write(tmp_path, "## Fed back into the spec\n\nnone.\n")
    _, _, err = uc.check_file(p)
    assert err and "no `## Not verified` section" in err[0][1]


def test_two_sections_are_an_error(tmp_path):
    _, _, err = uc.check_file(write(tmp_path, CANONICAL + "\n" + CANONICAL))
    assert err and "more than one" in err[0][1]


def test_prose_where_the_table_belongs_fails(tmp_path):
    """Four overviews recorded this as bullet prose. Prose is not countable,
    and a section that cannot be counted is not a record of how much is open."""
    section = "## Not verified\n\n- the TUI rendering, nobody has seen it\n"
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "found prose" in err[0][1]


def test_an_empty_table_fails(tmp_path):
    section = "## Not verified\n\n| Item | Who must answer |\n|---|---|\n"
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "no rows" in err[0][1]


def test_none_is_how_a_work_item_says_nothing_is_open(tmp_path):
    """Saying it explicitly is the point — silence and "nothing open" have to
    look different in the file, not only in the tally."""
    section = "## Not verified\n\nnone — every claim in this item was executed.\n"
    op, cl, err = uc.check_file(write(tmp_path, section))
    assert not err and not op and not cl


def test_none_and_a_table_together_fail(tmp_path):
    section = (
        "## Not verified\n\nnone — nothing open.\n\n" + CANONICAL.split("\n", 2)[2]
    )
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "`none` and a table" in err[0][1]


def test_a_fenced_example_is_not_a_second_section(tmp_path):
    """An overview that quotes this very format would otherwise report itself
    as having two sections."""
    fenced = CANONICAL + "\n```markdown\n## Not verified\n\n| Item | Who |\n```\n"
    op, _, err = uc.check_file(write(tmp_path, fenced))
    assert not err and len(op) == 2


def test_escaped_pipes_inside_a_cell_do_not_split_it(tmp_path):
    section = CANONICAL + "| whether `a \\| b` parses | the next session |\n"
    op, _, err = uc.check_file(write(tmp_path, section))
    assert not err and len(op) == 3


def test_a_scan_that_finds_no_overview_exits_2(tmp_path, capsys):
    """Zero files and zero open items are different answers. Reporting the
    first as the second is how a wrong path reads as a clean record."""
    (tmp_path / "empty").mkdir()
    assert run([str(tmp_path / "empty")]) == 2
    assert "nothing was checked" in capsys.readouterr().err


def test_open_items_do_not_fail_the_run(tmp_path, capsys):
    """Never a red build for an honest row: 45 were open when this shipped,
    and punishing them teaches sessions to write none."""
    write(tmp_path, CANONICAL)
    assert run([str(tmp_path)]) == 0
    assert "2 open" in capsys.readouterr().out


def test_zero_open_and_unreadable_are_different_exits_and_different_words(
    tmp_path, capsys
):
    """The requirement in one case: a reader must never confuse "everything is
    closed" with "this could not be read"."""
    closed = tmp_path / "closed"
    closed.mkdir()
    write(closed, "## Not verified\n\nnone — all executed.\n")
    assert run([str(closed)]) == 0
    clean = capsys.readouterr().out
    assert "open: 0" in clean

    broken = tmp_path / "broken"
    broken.mkdir()
    write(broken, "## Not verified\n\n- prose\n")
    assert run([str(broken)]) == 1
    bad = capsys.readouterr().out
    assert "could not be read" in bad
    assert "open: 0" not in bad


_BARE_INITED_REPO_TEMPLATE = None


def _bare_inited_repo_template():
    """A git-inited, identity-configured, empty repo -- what every `git_repo()`
    call needs before it writes and commits its own (test-specific) content."""
    global _BARE_INITED_REPO_TEMPLATE
    if _BARE_INITED_REPO_TEMPLATE is None:
        d = (
            Path(tempfile.mkdtemp(prefix="specseal-bare-inited-repo-template-"))
            / "repo"
        )
        subprocess.run(["git", "init", "-q", str(d)], check=True)
        subprocess.run(
            ["git", "-C", str(d), "config", "user.email", "t@example.com"],
            check=True,
        )
        subprocess.run(["git", "-C", str(d), "config", "user.name", "t"], check=True)
        atexit.register(shutil.rmtree, d, True)
        _BARE_INITED_REPO_TEMPLATE = d
    return _BARE_INITED_REPO_TEMPLATE


def git_repo(tmp_path, section):
    d = tmp_path / "repo"
    shutil.copytree(_bare_inited_repo_template(), d)

    def git(*a):
        subprocess.run(["git", "-C", str(d), *a], check=True, capture_output=True)

    p = write(d, section)
    git("add", "-A")
    git("commit", "-qm", "base")
    return d, p


def test_deleting_a_row_fails_against_the_baseline(tmp_path, capsys):
    """The whole convention rests on this. Without it, the cheapest way to
    lower the count stays "delete the line", and a closed item and a tidied-up
    one become the same edit."""
    d, p = git_repo(tmp_path, CANONICAL)
    text = open(p, encoding="utf-8").read()
    kept = "\n".join(ln for ln in text.splitlines() if "Windows" not in ln)
    with open(p, "w", encoding="utf-8") as f:
        f.write(kept + "\n")
    assert run([str(d), "--baseline", "HEAD"]) == 1
    out = capsys.readouterr().out
    assert "2 rows at HEAD, 1 here" in out


def test_closing_a_row_passes_the_baseline(tmp_path):
    """Marking keeps the row, so the count does not fall and the check is
    silent — the convention has to be the cheap path, not the expensive one."""
    d, p = git_repo(tmp_path, CANONICAL)
    text = open(p, encoding="utf-8").read()
    with open(p, "w", encoding="utf-8") as f:
        f.write(text.replace("| whether Windows", "| ✅ whether Windows"))
    assert run([str(d), "--baseline", "HEAD"]) == 0


def test_an_old_spelling_base_is_compared_again(tmp_path):
    """How the heading is found is the one argument the reader takes. A base
    revision written before this normalization is still a countable record,
    and refusing to read it stopped comparing four files that had been
    compared the commit before."""
    old = CANONICAL.replace("## Not verified", "## Not verified (who must answer)")
    d, p = git_repo(tmp_path, old)
    text = open(p, encoding="utf-8").read()
    with open(p, "w", encoding="utf-8") as f:
        f.write(
            text.replace(
                "## Not verified (who must answer)", "## Not verified"
            ).replace(
                "| whether Windows hooks fire | a maintainer with a Windows machine |\n",
                "",
            )
        )
    assert run([str(d), "--baseline", "HEAD"]) == 1


def test_the_canonical_heading_wins_over_a_looser_match_in_the_base(tmp_path, capsys):
    """The looser matcher must not select a different section from the one the
    working tree reads. A file holding both used to be reported as having lost
    rows nobody removed."""
    both = (
        CANONICAL + "\n### Not verified on Windows\n\n| a | b |\n|---|---|\n| x | y |\n"
    )
    d, _ = git_repo(tmp_path, both)
    assert run([str(d), "--baseline", "HEAD"]) == 0
    out = capsys.readouterr().out
    assert "not compared" not in out, (
        "exit 0 is not enough — without the canonical heading winning, the "
        "base matches twice, reads as unreadable, and is skipped rather than "
        "compared"
    )


def test_a_base_no_reader_can_make_sense_of_is_reported_as_not_compared(
    tmp_path, capsys
):
    """Not counted as zero, and not an error either: the author cannot edit a
    commit that already happened, and a count nobody can take is the one
    number this must not print."""
    d, p = git_repo(tmp_path, "## Not verified\n\n- the TUI rendering, as prose\n")
    with open(p, "w", encoding="utf-8") as f:
        f.write("# w — overview\n\n" + CANONICAL)
    assert run([str(d), "--baseline", "HEAD"]) == 0
    out = capsys.readouterr().out
    assert "not compared" in out
    assert "found prose" in out


def test_this_repositorys_own_overviews_are_all_readable():
    """The corpus is the real test. It also states the rule for new work: a
    spec directory that writes an overview writes this section in it."""
    assert run([os.path.join(ROOT, "seal", "specs")]) == 0


def collapsed(*parts):
    """File text with newlines flattened, so a match is not asserting where
    the author happened to wrap a line."""
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return " ".join(f.read().split())


def test_the_template_is_the_shape_the_checker_reads(tmp_path):
    """Template and checker drift apart silently otherwise: every new work
    item would copy a section the release check then refuses."""
    with open(
        os.path.join(ROOT, "templates", "sdd-overview.md"), encoding="utf-8"
    ) as f:
        template = f.read()

    d = tmp_path / "specs" / "1780000000-work"
    d.mkdir(parents=True)
    p = d / "overview.md"

    p.write_text(template, encoding="utf-8")
    _, _, err = uc.check_file(str(p))
    assert err and "placeholder" in err[0][1], (
        "a template copied and never filled in has to fail, or an empty record "
        "passes as a complete one"
    )

    filled = template.replace("<what was not verified>", "the TUI rendering").replace(
        "<who or what can answer it>", "user, on the next session"
    )
    p.write_text(filled, encoding="utf-8")
    op, _, err = uc.check_file(str(p))
    assert not err and len(op) == 1


def test_the_memo_no_longer_asks_for_what_the_diff_holds():
    """Item 2 wanted a line per file, which is `git diff --stat` retyped from
    memory after the fact."""
    skill = collapsed("skills", "implement", "SKILL.md")
    assert "each file path with a one-line description" not in skill
    assert "not a summary of the work" in skill
    assert "`git diff --stat` already holds the file list" in skill


def test_the_memo_keeps_one_line_of_purpose():
    """Below the six-file line no `spec.md` is written, so this line is the
    only place the purpose stays in the repository."""
    skill = collapsed("skills", "implement", "SKILL.md")
    assert "Why this work exists and what the result changes — **one line**" in skill
    assert "the only place the purpose stays in the repository" in skill
    with open(
        os.path.join(ROOT, "templates", "sdd-overview.md"), encoding="utf-8"
    ) as f:
        assert "## Why this work exists" in f.read()


def test_the_ladder_does_not_still_say_at_the_end():
    """Three of the four parts are written when they happen. A ladder that
    still says `overview.md at the end` contradicts the step above it, and the
    contradiction is what sessions resolve by reconstructing at the end."""
    skill = collapsed("skills", "implement", "SKILL.md")
    assert "`overview.md` at the end" not in skill
    assert (
        "opened at the first divergence, unverified item, or fed-back clause" in skill
    )
    assert "only the closing memo, kept as you go" in collapsed("agents", "smith.md")


def test_the_skill_states_the_closing_convention():
    """The writer of a row is the one who has to know how it closes."""
    skill = collapsed("skills", "implement", "SKILL.md")
    assert "closed by marking it, never by deleting it" in skill
    assert "unverified-check --baseline" in skill


def test_a_comment_beside_the_section_is_not_read_as_content(tmp_path):
    """The template ships its guidance as a comment in this section, and an
    overview keeps it. Reading it as prose would fail every filled-in copy."""
    section = (
        "## Not verified\n\n<!-- guidance:\n| ✅ <item> | <what closed it> |\n-->\n\n"
        + CANONICAL.split("\n", 2)[2]
    )
    op, _, err = uc.check_file(write(tmp_path, section))
    assert not err and len(op) == 2


# --- round 2: what the first round's tests did not hold ----------------------


def test_a_row_with_three_cells_is_an_error_not_a_traceback():
    """`item, who = cells` unpacks two. Without the length guard this raises
    ValueError, and a gate that crashes is a gate nobody can read."""
    section = CANONICAL + "| an item | an answerer | a third cell |\n"
    _, _, err = uc.parse_section(section.splitlines()[2:], 3)
    assert err and "3 cells" in err[0][1]


def test_a_missing_separator_row_is_an_error(tmp_path):
    """Without it the header's own row would be read as the first item."""
    section = "## Not verified\n\n| Item | Who must answer |\n| an item | someone |\n"
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "separator" in err[0][1]


def test_an_empty_section_is_an_error_not_a_traceback(tmp_path):
    """`content[0]` on an empty section is an IndexError. The section also has
    to say something: silence and "nothing open" are different claims."""
    section = "## Not verified\n\n## Fed back into the spec\n\nnone.\n"
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "empty" in err[0][1]


def test_a_second_header_or_separator_inside_the_section_is_an_error(tmp_path):
    """Two tables in one section made `|---|---|` count as an open item."""
    section = (
        CANONICAL + "\n| Item | Who must answer |\n|---|---|\n| another | someone |\n"
    )
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "one table" in err[0][1]


def test_rows_after_a_fenced_example_are_still_counted(tmp_path):
    """The reader used to stop at the fence, so anything below an example
    vanished — the silent omission this tool exists to refuse."""
    section = (
        CANONICAL
        + "\n```markdown\n| Item | Who must answer |\n```\n\n| a third item | someone |\n"
    )
    op, _, err = uc.check_file(write(tmp_path, section))
    assert not err, err
    assert len(op) == 3


def test_adding_a_fenced_example_is_not_read_as_a_deletion(tmp_path):
    """The strict reader truncated at the fence and the base reader skipped
    it, so the two disagreed and an honest edit came back as a deleted row."""
    d, p = git_repo(tmp_path, CANONICAL)
    text = open(p, encoding="utf-8").read()
    with open(p, "w", encoding="utf-8") as f:
        f.write(
            text.replace(
                "| how the gate renders in a TUI | user, on the next session |\n",
                "| how the gate renders in a TUI | user, on the next session |\n"
                "\n```\nan example\n```\n\n",
            )
        )
    assert run([str(d), "--baseline", "HEAD"]) == 0


def test_deleting_the_whole_file_fails_the_baseline(tmp_path, capsys):
    """Deleting the file was cheaper and quieter than deleting one row from
    it: the scan walks the current tree, so a file that is gone never enters
    the comparison at all."""
    d, p = git_repo(tmp_path, CANONICAL)
    # A second overview, so the scan is not empty and cannot exit 2 instead.
    other = d / "specs" / "1780000001-other"
    other.mkdir(parents=True)
    (other / "overview.md").write_text("# o\n\n" + CANONICAL, encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "two"], check=True, capture_output=True
    )
    os.remove(p)
    assert run([str(d), "--baseline", "HEAD"]) == 1
    assert "present at HEAD and not here" in capsys.readouterr().out


def test_renaming_the_work_item_directory_fails_the_baseline(tmp_path, capsys):
    """A rename is indistinguishable from a deletion here, and saying so out
    loud is the right default: Q5 fixed the filename, so a legitimate rename
    of one of these is rare."""
    d, p = git_repo(tmp_path, CANONICAL)
    os.rename(os.path.dirname(p), os.path.join(str(d), "specs", "1780000000-renamed"))
    assert run([str(d), "--baseline", "HEAD"]) == 1
    assert "present at HEAD and not here" in capsys.readouterr().out


def test_a_baseline_ref_that_does_not_resolve_exits_2(tmp_path, capsys):
    """The comparison silently did nothing and the run passed. In CI that is
    one shallow checkout away: the base branch is not there, every file reads
    as new, and the deletion check reports success without running."""
    d, _ = git_repo(tmp_path, CANONICAL)
    assert run([str(d), "--baseline", "origin/nosuchbranch"]) == 2
    assert "does not resolve" in capsys.readouterr().err


@pytest.mark.parametrize("invisible", ["️", "​", "⁠"])
def test_an_invisible_character_does_not_turn_a_bare_mark_into_a_closing(
    tmp_path, invisible
):
    """`| ✅️ | done |` is what many keyboards emit, and on screen it is the
    bare mark this refuses. `.strip()` does not remove any of these."""
    section = CANONICAL.replace(
        "| how the gate renders in a TUI | user, on the next session |",
        f"| {CLOSED_MARK}{invisible} | done |",
    )
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "bare" in err[0][1]


def test_the_wrapper_is_present_and_executable():
    """bin/ lands on the Bash tool's PATH while the plugin is enabled, so the
    wrapper resolves the script relative to itself and a .cmd sibling ships
    for the platform that cannot run a POSIX shebang."""
    posix = os.path.join(ROOT, "bin", "unverified-check")
    windows = os.path.join(ROOT, "bin", "unverified-check.cmd")
    assert os.path.isfile(posix), "bin/unverified-check missing"
    assert os.path.isfile(windows), "bin/unverified-check.cmd missing"
    assert os.access(posix, os.X_OK), "bin/unverified-check not executable"
    assert os.path.isfile(SCRIPT), "the wrapper points at a missing script"


# --- round 3: the two comparisons had doors of their own -----------------------


def test_a_symlinked_path_still_compares(tmp_path):
    """`git rev-parse --show-toplevel` answers with links resolved and
    `abspath` does not, so reaching the tree through one — `/tmp` on macOS,
    a code directory linked from home — made every repo-relative path match
    no line of `ls-tree`. Both comparisons then did nothing and passed."""
    d, p = git_repo(tmp_path, CANONICAL)
    link = tmp_path / "link"
    symlink_or_skip(str(d), str(link))
    text = open(p, encoding="utf-8").read()
    with open(p, "w", encoding="utf-8") as f:
        f.write(
            text.replace(
                "| whether Windows hooks fire | a maintainer with a Windows machine |\n",
                "",
            )
        )
    assert run([str(link), "--baseline", "HEAD"]) == 1


def test_a_tracked_overview_under_a_skipped_directory_is_not_read_as_deleted(tmp_path):
    """The scan skips build/ and node_modules/; the base listing did not. A
    tracked overview.md under one of them was absent from every scan and so
    reported deleted on every run — a red build the author could only clear
    by renaming the directory."""
    d, _ = git_repo(tmp_path, CANONICAL)
    buried = d / "build" / "x"
    buried.mkdir(parents=True)
    (buried / "overview.md").write_text("# b\n\n" + CANONICAL, encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "build"], check=True, capture_output=True
    )
    assert run([str(d), "--baseline", "HEAD"]) == 0


def test_deleting_every_overview_reports_the_deletion_not_an_empty_scan(
    tmp_path, capsys
):
    """The scan finding nothing used to exit 2 saying "nothing was checked",
    which reads as a mistyped argument rather than a record that just left. A
    repository with one work item reaches this by deleting one file."""
    d, p = git_repo(tmp_path, CANONICAL)
    os.remove(p)
    assert run([str(d), "--baseline", "HEAD"]) == 1
    assert "present at HEAD and not here" in capsys.readouterr().out


def test_a_row_of_invisible_cells_is_not_an_open_item(tmp_path):
    """Two zero-width spaces read as "not empty" and counted as an item
    nobody can see. Against the row-count comparison that is a way to delete
    a real row and keep the number."""
    section = CANONICAL.replace(
        "| how the gate renders in a TUI | user, on the next session |",
        "| ​ | ​ |",
    )
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "empty cell" in err[0][1]


def test_a_separator_hidden_by_an_invisible_character_is_still_a_separator(tmp_path):
    """`|-​--|---|` misses the separator pattern, so the row that round 1
    refused to count as an item came back as one."""
    section = CANONICAL + "|-​--|---|\n"
    _, _, err = uc.check_file(write(tmp_path, section))
    assert err and "one table" in err[0][1]


def test_an_unreadable_section_does_not_also_report_a_deletion(tmp_path, capsys):
    """A misspelt heading returns zero rows, and comparing that zero told the
    author to restore rows that are still sitting in the file."""
    d, p = git_repo(tmp_path, CANONICAL)
    text = open(p, encoding="utf-8").read()
    with open(p, "w", encoding="utf-8") as f:
        f.write(text.replace("## Not verified", "## Not verified (who must answer)"))
    assert run([str(d), "--baseline", "HEAD"]) == 1
    out = capsys.readouterr().out
    assert "no `## Not verified` section" in out
    assert "rows at HEAD" not in out, "the rows never left the file"


def test_a_tilde_fence_is_a_fence(tmp_path):
    """CommonMark accepts `~~~`, and an example wrapped in one used to be read
    as rows — a red build on an honest document whose only remedy was to
    change fence style."""
    section = (
        CANONICAL
        + "\n~~~markdown\n| Item | Who must answer |\n~~~\n\n| a third item | someone |\n"
    )
    op, _, err = uc.check_file(write(tmp_path, section))
    assert not err, err
    assert len(op) == 3


# --- round 4: one reader, and the pairs it retires ---------------------------


def test_a_second_not_verified_heading_is_not_counted_by_the_base_reader(tmp_path):
    """The loose reader counted every heading that mentioned "not verified",
    the strict one counted the canonical section, and a file holding both
    reported a deletion nobody had made. The author's only remedy was to
    rename a heading that was never this tool's business."""
    section = (
        CANONICAL + "\n### Not verified on Windows\n\n| a | b |\n|---|---|\n| x | y |\n"
    )
    d, _ = git_repo(tmp_path, section)
    assert run([str(d), "--baseline", "HEAD"]) == 0


def test_an_invisible_separator_in_the_base_is_not_counted_as_a_row(tmp_path):
    """The cell normalization landed in one reader and not the other, so a
    zero-width space in the base made a separator count as a row there and
    not here — a deletion report on a file nobody touched."""
    hidden = CANONICAL.replace("|---|---|", "|-​--|---|")
    d, p = git_repo(tmp_path, hidden)
    with open(p, "w", encoding="utf-8") as f:
        f.write("# w — overview\n\n" + CANONICAL)
    assert run([str(d), "--baseline", "HEAD"]) == 0


def test_a_tracked_symlink_is_not_reported_as_deleted(tmp_path):
    """`ls-tree` lists a tracked link under its own path. Resolving every
    scanned file — the round-2 fix, applied one level too deep — made a link
    that is right there read as gone."""
    d, _ = git_repo(tmp_path, CANONICAL)
    linked = d / "specs" / "1780000001-link"
    linked.mkdir()
    symlink_or_skip(
        os.path.join("..", "1780000000-work", "overview.md"),
        str(linked / "overview.md"),
    )
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "link"], check=True, capture_output=True
    )
    assert run([str(d), "--baseline", "HEAD"]) == 0


def test_a_deleted_scan_path_is_compared_not_called_a_bad_argument(tmp_path, capsys):
    """The workflow runs `--baseline origin/<base> specs/`. A change that
    deletes specs/ wholesale was told it had mistyped an argument, while the
    record it removed went unmentioned."""
    d, _ = git_repo(tmp_path, CANONICAL)
    subprocess.run(["rm", "-rf", str(d / "specs")], check=True)
    assert run([str(d / "specs"), "--baseline", "HEAD"]) == 1
    assert "present at HEAD and not here" in capsys.readouterr().out


def test_deleting_a_file_through_a_symlinked_path_is_caught(tmp_path):
    """The row check and the file check resolve paths separately, so the
    symlink case has to be shown for both. The sibling test above deletes a
    row; this one deletes the file."""
    d, p = git_repo(tmp_path, CANONICAL)
    other = d / "specs" / "1780000001-other"
    other.mkdir(parents=True)
    (other / "overview.md").write_text("# o\n\n" + CANONICAL, encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "two"], check=True, capture_output=True
    )
    link = tmp_path / "link"
    symlink_or_skip(str(d), str(link))
    os.remove(p)
    assert run([str(link), "--baseline", "HEAD"]) == 1


def reported_paths(out):
    """The path each report line names, in EITHER output shape.

    `annotate` emits `::error file=<path>,line=<n>::…` when `GITHUB_ACTIONS` is
    set and `<path>:<line>  …` anywhere else. This test read only the second
    shape, so it passed on a developer's machine and failed in the only place
    the check actually runs — 1 failed, 524 passed on all three runners, while
    the same tree was green locally. `run`'s own docstring says a test here
    asserts what CI would see; reading one of the two shapes is how that stopped
    being true.
    """
    found = []
    for ln in out.splitlines():
        if ln.startswith("::"):
            _, _, rest = ln.partition(" file=")
            path, _, _ = rest.partition(",line=")
            if path:
                found.append(path)
        elif "overview.md:" in ln:
            found.append(ln.split(":")[0])
    return found


@pytest.mark.parametrize("in_ci", [False, True])
def test_both_deletion_reports_name_paths_on_the_same_footing(
    tmp_path, capsys, monkeypatch, in_ci
):
    """One line came from `relpath(path, cwd)` and the other from `ls-tree`'s
    repo-relative path. They agreed only when the command ran at the
    repository root, and the README hands this command to users.

    Run in both output shapes, because the paths are the subject and the shape
    is not — and because pinning one shape is what let this pass everywhere
    except CI.
    """
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    if in_ci:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
    d, p = git_repo(tmp_path, CANONICAL)
    other = d / "specs" / "1780000001-other"
    other.mkdir(parents=True)
    (other / "overview.md").write_text("# o\n\n" + CANONICAL, encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "two"], check=True, capture_output=True
    )
    os.remove(p)  # the file check reports this one
    text = open(other / "overview.md", encoding="utf-8").read()
    with open(other / "overview.md", "w", encoding="utf-8") as f:
        f.write(text.replace("| whether Windows hooks fire", "| ✅ whether Windows"))
        # closed, not deleted -- now drop a row so the row check reports too
    with open(other / "overview.md", "w", encoding="utf-8") as f:
        f.write(
            text.replace(
                "| whether Windows hooks fire | a maintainer with a Windows machine |\n",
                "",
            )
        )

    here = os.getcwd()
    os.chdir(str(d / "specs"))
    try:
        assert run([".", "--baseline", "HEAD"]) == 1
        paths = reported_paths(capsys.readouterr().out)
    finally:
        os.chdir(here)
    assert len(paths) == 2, paths
    assert all(q.startswith("1780000") for q in paths), paths


# --- round 5: what the matcher argument left to settle ------------------------


def test_a_path_two_levels_gone_still_names_its_repository(tmp_path, capsys):
    """`repo_root` steps back one level on its own, so this only earns its
    place deeper than that — and `specs/<item>/` is exactly two."""
    d, _ = git_repo(tmp_path, CANONICAL)
    gone = d / "specs" / "1780000000-work"
    subprocess.run(["rm", "-rf", str(gone)], check=True)
    assert run([str(gone / "overview.md"), "--baseline", "HEAD"]) == 1
    assert "present at HEAD and not here" in capsys.readouterr().out


def test_a_mistyped_path_is_still_a_mistyped_path(tmp_path, capsys):
    """The guard was narrowed so a deleted scan path could be compared, and
    that let `specs/ spces/` pass in silence. A path with nothing under it at
    the base is a typo, not a question."""
    d, _ = git_repo(tmp_path, CANONICAL)
    assert run([str(d / "specs"), str(d / "spces"), "--baseline", "HEAD"]) == 2
    assert "nothing under it" in capsys.readouterr().err


def test_a_tracked_symlink_is_counted_once(tmp_path, capsys):
    """One record, two paths. Counting both doubles its open items, and
    dropping one from the presence check reports a file that is right there
    as deleted — so the two questions are answered differently on purpose."""
    d, _ = git_repo(tmp_path, CANONICAL)
    linked = d / "specs" / "1780000001-link"
    linked.mkdir()
    symlink_or_skip(
        os.path.join("..", "1780000000-work", "overview.md"),
        str(linked / "overview.md"),
    )
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "link"], check=True, capture_output=True
    )
    assert run([str(d), "--baseline", "HEAD"]) == 0
    out = capsys.readouterr().out
    assert "1 overviews · 2 open" in out, out


def test_the_summary_names_how_many_were_not_compared(tmp_path, capsys):
    """The tally is the line most readers stop at, so a file left out of the
    comparison has to be visible there and not only in the block below."""
    d, p = git_repo(tmp_path, "## Not verified\n\n- prose at the base\n")
    with open(p, "w", encoding="utf-8") as f:
        f.write("# w — overview\n\n" + CANONICAL)
    assert run([str(d), "--baseline", "HEAD"]) == 0
    assert "· 1 not compared" in capsys.readouterr().out


def test_a_legacy_column_name_in_the_base_is_read_but_not_in_the_tree(tmp_path):
    """The four files this branch normalized renamed the column as well as the
    heading, so relaxing the heading alone would still have stopped comparing
    them. The relaxation is the base's alone: the working tree is held to the
    exact header, or the spelling drifts back in through the front door."""
    legacy = CANONICAL.replace("## Not verified", "## Not verified (who must answer)")
    legacy = legacy.replace("| Item | Who must answer |", "| Item | Who |")
    d, p = git_repo(tmp_path, legacy)
    text = open(p, encoding="utf-8").read()
    with open(p, "w", encoding="utf-8") as f:
        f.write(
            text.replace("## Not verified (who must answer)", "## Not verified")
            .replace("| Item | Who |", "| Item | Who must answer |")
            .replace(
                "| whether Windows hooks fire | a maintainer with a Windows machine |\n",
                "",
            )
        )
    assert run([str(d), "--baseline", "HEAD"]) == 1

    _, _, tree_errors = uc.check_text(legacy.replace(" (who must answer)", ""))
    assert tree_errors and "header is" in tree_errors[0][1]


def test_the_legacy_read_still_wants_an_item_column(tmp_path):
    """A relaxation with no floor reads any two-column table as the record."""
    odd = CANONICAL.replace("| Item | Who must answer |", "| Thing | Who |")
    _, _, errors = uc.check_text(odd, heading=uc.LOOSE_HEADING, strict_header=False)
    assert errors and "header is" in errors[0][1]


# --- the two path dialects: what git is told, and what the caller is shown ----


def test_a_path_handed_to_git_is_spelled_the_way_git_spells_it(monkeypatch):
    r"""Repo-relative paths are built with `os.path.relpath` and then spent as
    `git show <ref>:<rel>` and compared against `ls-tree` output. git answers
    and accepts `/` on every platform, so on Windows the two sides were built
    by two rules: `show` returned None and the row check silently compared
    nothing, while the presence check matched no path and called every tracked
    overview deleted.

    The substitution is asserted with `os.sep` monkeypatched, because
    `git_path` reads it at call time. Round 1 was right that the `os.path.join`
    form alone asserts `x == x` on the three POSIX legs, so the branch it
    exists for was bound on Windows only -- which is the shape this work item
    is otherwise about removing."""
    joined = os.path.join("specs", "1780000000-work", "overview.md")
    assert uc.git_path(joined) == "specs/1780000000-work/overview.md"

    # The Windows branch, on every platform.
    monkeypatch.setattr(os, "sep", "\\")
    assert uc.git_path("specs\\1780000000-work\\overview.md") == (
        "specs/1780000000-work/overview.md"
    )
    # Idempotent there too: `overviews_at` returns git's spelling and a path
    # that already came from git goes through here unchanged.
    assert uc.git_path("specs/1780000000-work/overview.md") == (
        "specs/1780000000-work/overview.md"
    )

    # And the POSIX branch does NOT substitute, so a backslash that is part of
    # a real filename survives.
    monkeypatch.setattr(os, "sep", "/")
    assert uc.git_path("specs/odd\\name.md") == "specs/odd\\name.md"


def test_a_report_survives_a_path_with_no_relative_form(monkeypatch):
    r"""`os.path.relpath` raises on Windows when the two paths are on different
    drives -- measured: `ValueError: path is on mount 'D:', start on mount
    'C:'`. It is the reporting footing for every line the tool prints, so a run
    with the workspace and the temp directory on two volumes died before
    printing a single row.

    Driven by making `relpath` raise rather than by finding two drives, so the
    ubuntu leg runs this case too."""

    def refuses(path, start=None):
        raise ValueError("path is on mount 'D:', start on mount 'C:'")

    monkeypatch.setattr(os.path, "relpath", refuses)
    where = os.path.abspath(os.path.join("x", "overview.md"))
    assert uc.display_path(where, os.path.abspath("y")) == where
    # The git-facing half answers None instead, because there is no
    # repo-relative form of a path that is not in the repository.
    assert uc.repo_relative(where, os.path.abspath("y")) is None


def test_a_path_on_another_volume_stops_the_run_instead_of_aborting_it(
    tmp_path, monkeypatch, capsys
):
    r"""Round 1, finding 2: `display_path` guarded the two reporting sites and
    the four git-facing ones kept a bare `relpath`. Executed then, the run
    printed one row and died mid-report with the same `ValueError` the helper
    existed to prevent.

    Every argument is read against ONE repository, the one the first argument
    is in. That was always the rule and nothing stated it, so this says it: a
    path with no relative form to that root is not in it, and the answer is
    exit 2 with the path named, not a traceback and not a silent zero.

    The raise is induced rather than found, so this runs on every leg. It is
    scoped to the second argument, so everything the first one needs still
    resolves and the case reaches the check rather than falling over earlier."""
    d, _ = git_repo(tmp_path, CANONICAL)
    elsewhere = tmp_path / "elsewhere"
    (elsewhere / "specs").mkdir(parents=True)

    real_relpath = os.path.relpath

    def refuses_for_elsewhere(path, start=None):
        if "elsewhere" in str(path):
            raise ValueError("path is on mount 'D:', start on mount 'C:'")
        return real_relpath(path, start)

    monkeypatch.setattr(os.path, "relpath", refuses_for_elsewhere)
    assert run([str(d), str(elsewhere), "--baseline", "HEAD"]) == 2
    err = capsys.readouterr().err
    assert "is not in" in err and "another volume" in err, err
