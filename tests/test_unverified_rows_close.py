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
import random
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
    """The workflow runs `--baseline origin/<base> seal/specs/`. A change that
    deletes the scan path wholesale was told it had mistyped an argument, while
    the    record it removed went unmentioned."""
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


# --- #272: the baseline is the pull request's base, and the base moves -------


def forked(tmp_path, section=CANONICAL):
    """A repository whose `base` and `work` branches sit on one fork point.

    Checked out on `work`, which is where a feature branch lives. Each case
    below moves `base` forward the way a release branch does when another work
    item squashes into it, and then asks what THIS branch removed."""
    d = tmp_path / "repo"
    shutil.copytree(_bare_inited_repo_template(), d)

    def git(*a):
        subprocess.run(["git", "-C", str(d), *a], check=True, capture_output=True)

    p = write(d, section)
    git("add", "-A")
    git("commit", "-qm", "the fork point")
    git("branch", "base")
    git("switch", "-q", "-c", "work")
    return d, p, git


def squash_a_sibling_into_the_base(d, git, name="1780000001-squashed-sibling"):
    """What the base branch does when another work item is squashed into it.

    The sibling's `overview.md` is then at the base and was never on this
    branch at all -- which is the whole of #272."""
    git("switch", "-q", "base")
    other = d / "specs" / name
    other.mkdir(parents=True)
    (other / "overview.md").write_text(
        f"# {name} — overview\n\n" + CANONICAL, encoding="utf-8"
    )
    git("add", "-A")
    git("commit", "-qm", "another work item, squashed into the base")
    git("switch", "-q", "work")


def short(d, ref="HEAD"):
    out = subprocess.run(
        ["git", "-C", str(d), "rev-parse", ref],
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    return out.stdout.strip()[:7]


def test_a_work_item_squashed_after_the_fork_is_not_this_branchs_removal(
    tmp_path, capsys
):
    """#272, and the case the repair exists for. On 0.9.2 three of four
    branches met this: the moment one work item squashed into the release
    branch, every sibling cut before that squash read the squashed item's
    `overview.md` as rows that left the record. The message was right about
    what it measured and wrong about what happened -- nothing left, the base
    moved.

    The merge base is the last commit this branch and the base agreed on, so a
    file present there and absent here was removed by this branch. A file that
    arrived on the base after the fork is not this branch's business."""
    d, _, git = forked(tmp_path)
    squash_a_sibling_into_the_base(d, git)
    assert run([str(d), "--baseline", "base"]) == 0
    out = capsys.readouterr().out
    assert "left the record" not in out, out
    assert "squashed-sibling" not in out, out


def test_the_moved_base_does_not_excuse_this_branchs_own_deletion(tmp_path, capsys):
    """The control. Without it the repair is indistinguishable from making the
    arm inert, which is the direction that loses a real removal.

    Same moved base, and this branch really did delete its own record."""
    d, p, git = forked(tmp_path)
    squash_a_sibling_into_the_base(d, git)
    os.remove(p)
    assert run([str(d), "--baseline", "base"]) == 1
    out = capsys.readouterr().out
    assert "1780000000-work" in out, out
    # And still only its own: the sibling is not reported alongside it.
    assert "squashed-sibling" not in out, out


def test_a_row_the_base_gained_after_the_fork_is_not_a_deletion(tmp_path, capsys):
    """The row-count arm reads the base revision too, through
    `git show <ref>:<path>`, so it is in the same class as the arm the ticket
    names -- the ticket's own repair section says otherwise, and that is what
    reading it rather than assuming it settles (questions.md Q1).

    Reachable the moment the base gains a row in THIS branch's overview after
    the fork: a row closed on the base, or one added there by a later work
    item."""
    d, p, git = forked(tmp_path)
    git("switch", "-q", "base")
    text = open(p, encoding="utf-8").read()
    with open(p, "w", encoding="utf-8") as f:
        f.write(text + "| whether the hooks fire on Windows | the same maintainer |\n")
    git("add", "-A")
    git("commit", "-qm", "a third row, on the base")
    git("switch", "-q", "work")
    assert run([str(d), "--baseline", "base"]) == 0
    out = capsys.readouterr().out
    assert "left the record" not in out, out


def test_the_moved_base_does_not_excuse_a_deleted_row(tmp_path, capsys):
    """The row arm's control, for the same reason as the file arm's."""
    d, p, git = forked(tmp_path)
    squash_a_sibling_into_the_base(d, git)
    text = open(p, encoding="utf-8").read()
    with open(p, "w", encoding="utf-8") as f:
        f.write(
            text.replace(
                "| whether Windows hooks fire | a maintainer with a Windows machine |\n",
                "",
            )
        )
    assert run([str(d), "--baseline", "base"]) == 1
    assert "2 rows at" in capsys.readouterr().out


def test_a_moved_base_report_names_the_merge_base_it_compared(tmp_path, capsys):
    """A refusal is read and acted on, so it names the revision it actually
    compared against -- in the shortest form that is true. Naming `base` here
    would send the reader to a commit this run never opened.

    The sibling cases above assert the other half: with `--baseline HEAD`, the
    ref IS the merge base, so the ref's own name is the true short form and
    every earlier case still reads `present at HEAD and not here`."""
    d, p, git = forked(tmp_path)
    squash_a_sibling_into_the_base(d, git)
    os.remove(p)
    assert run([str(d), "--baseline", "base"]) == 1
    out = capsys.readouterr().out
    assert f"the merge-base of base and HEAD ({short(d)})" in out, out
    assert "present at base and not here" not in out, out


def test_a_base_that_is_the_merge_base_is_named_by_its_ref_alone(tmp_path, capsys):
    """The shortest true form, stated as its own case rather than left to the
    earlier ones. Where the ref's commit IS the merge base -- every local run
    against `HEAD`, and CI, where the checkout is the merge of the head into
    the base -- the extra words carry nothing."""
    d, p, _ = forked(tmp_path)
    os.remove(p)
    assert run([str(d), "--baseline", "base"]) == 1
    out = capsys.readouterr().out
    assert "present at base and not here" in out, out
    assert "merge-base" not in out, out


def test_a_baseline_that_shares_no_history_with_head_exits_2(tmp_path, capsys):
    """A comparison against nothing is not a comparison -- the same answer the
    module already gives for a ref that does not resolve. Without a common
    commit there is no question of the form "what did THIS branch remove", so
    there is nothing to degrade to.

    A shallow clone whose base ref resolves while the common ancestor sits
    beyond the graft lands here too. Both workflows set `fetch-depth: 0`;
    questions.md Q2 carries the case that does not."""
    d, _, git = forked(tmp_path)
    git("switch", "-q", "--orphan", "unrelated")
    (d / "readme.md").write_text("no commit in common\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "an unrelated root")
    git("switch", "-q", "work")
    assert run([str(d), "--baseline", "unrelated"]) == 2
    err = capsys.readouterr().err
    assert "share no history" in err, err
    assert "nothing was compared" in err, err


def test_a_scan_path_that_only_the_base_ever_had_is_a_mistyped_argument(
    tmp_path, capsys
):
    """The missing-path arm asks the same `overviews_at` question, so it moves
    with the other two rather than being left on the tip.

    A path this branch never had, and that the fork point never held either,
    is a mistyped argument from this branch — whatever the base's tip carries
    now. Left on the tip it read as a work item this branch had deleted, which
    is #272 arriving through the third door."""
    d, _, git = forked(tmp_path)
    squash_a_sibling_into_the_base(d, git)
    gone = d / "specs" / "1780000001-squashed-sibling"
    assert run([str(gone), "--baseline", "base"]) == 2
    err = capsys.readouterr().err
    assert "no such path" in err, err


def test_a_merge_base_that_answers_with_nothing_is_not_a_comparison(
    tmp_path, monkeypatch, capsys
):
    """`git merge-base` answering exit 0 with an empty line is not a revision,
    and an empty string reaching `git ls-tree` lists nothing — the silent zero
    this whole module refuses, reached through the one code path that cannot
    be driven by a fixture.

    Induced rather than found, the way the `relpath` cases below are, so it
    runs on every leg. No git this repository requires answers that way; the
    guard is here because the alternative to a guard is a pass."""
    d, _, git = forked(tmp_path)
    squash_a_sibling_into_the_base(d, git)
    real_run = subprocess.run

    def empty_merge_base(argv, *a, **kw):
        if isinstance(argv, list) and "merge-base" in argv:
            return subprocess.CompletedProcess(argv, 0, "\n", "")
        return real_run(argv, *a, **kw)

    monkeypatch.setattr(uc.subprocess, "run", empty_merge_base)
    assert run([str(d), "--baseline", "base"]) == 2
    assert "share no history" in capsys.readouterr().err


def test_a_ref_that_resolves_to_nothing_is_a_ref_that_does_not_resolve(
    tmp_path, monkeypatch, capsys
):
    """`commit_of` answers two questions at once — whether the ref resolves and
    which commit it is — and `chain_check.py` loads it for the first through
    `resolves`. `rev-parse --verify --quiet` exits 1 for a name it cannot find,
    so the empty-output guard is reached only by a git that exits 0 and prints
    nothing, and a mutation loop found it the one branch here no fixture drives.

    Induced, like the merge-base case above and the `relpath` cases below. What
    it pins is that an empty answer is a refusal rather than a truthy sentinel
    travelling into `base_label` and out to `chain_check.py` as a resolved
    ref."""
    d, _, _ = forked(tmp_path)
    real_run = subprocess.run

    def empty_verify(argv, *a, **kw):
        if isinstance(argv, list) and "--verify" in argv:
            return subprocess.CompletedProcess(argv, 0, "\n", "")
        return real_run(argv, *a, **kw)

    monkeypatch.setattr(uc.subprocess, "run", empty_verify)
    assert uc.resolves(str(d), "base") is False
    assert run([str(d), "--baseline", "base"]) == 2
    assert "does not resolve" in capsys.readouterr().err


@pytest.mark.parametrize(
    "doc",
    [
        "README.md",
        "README.ko.md",
        os.path.join("docs", "one-root-by-lifetime.md"),
        os.path.join("docs", "one-root-by-lifetime.ko.md"),
        os.path.join("docs", "release-checklist.md"),
        os.path.join("skills", "verify", "SKILL.md"),
        os.path.join(".github", "workflows", "hygiene.yml"),
        os.path.join("templates", "hygiene.yml"),
    ],
)
def test_the_documents_state_the_merge_base_footing(doc):
    """Eight files told a reader that `--baseline` compares against the base
    revision, and after #272 it compares against the fork point. A corrected
    behaviour whose old sentence survives somewhere else is #180's class, and
    eight places is where this one could survive.

    A positive assertion, the way `test_the_skill_states_the_closing_convention`
    is: the sentence has to be there, rather than the old wording having to be
    absent. Nothing else in these files had reason to name a merge base."""
    text = open(os.path.join(ROOT, doc), encoding="utf-8").read()
    assert "merge-base" in text or "merge base" in text, (
        f"{doc} describes `unverified-check --baseline` and does not say the "
        "comparison is against the merge base"
    )


# --- a fold is not this branch's deletion ----------------------------------


def fold_into_docs(repo, work_item_id, document="a-segment.md"):
    """Record `work_item_id` as folded, the way `settle`'s procedure does.

    The fold record is the provenance comment the folded prose carries in
    `docs/`, which is the marker `.github/scripts/fold_ledger.py#marker` and
    `.github/scripts/gather_changelog.py#marker` already write. Nothing else
    is written: a record derived from the destination cannot disagree with
    it, which is why there is no second file to keep in step.
    """
    docs = repo / "docs"
    docs.mkdir(exist_ok=True)
    (docs / document).write_text(
        f"# a segment\n\nOne standing statement.\n<!-- specs/{work_item_id} -->\n",
        encoding="utf-8",
    )


def test_a_folded_work_item_is_not_read_as_this_branchs_deletion(tmp_path, capsys):
    """A1. `settle` removes a released work item's directory after its SDD set
    has been folded into `docs/`, and this arm used to call that a deletion —
    97 of them in one commit, which is what made the fold impossible rather
    than merely noisy.

    The discriminator is the fold record, not the removal: a directory whose
    work item carries no marker anywhere in `docs/` is still this branch's
    deletion and still fails."""
    d, p = git_repo(tmp_path, CANONICAL)
    other = d / "specs" / "1780000001-other"
    other.mkdir(parents=True)
    (other / "overview.md").write_text("# o\n\n" + CANONICAL, encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "two"], check=True, capture_output=True
    )
    shutil.rmtree(os.path.dirname(p))
    fold_into_docs(d, "1780000000-work")
    assert run([str(d), "--baseline", "HEAD"]) == 0
    out = capsys.readouterr().out
    assert "present at HEAD and not here" not in out
    assert "1780000000-work" in out and "folded" in out, (
        f"the run says nothing about the directory it stopped reporting: {out}"
    )


def test_an_unfolded_removal_beside_a_folded_one_still_fails(tmp_path, capsys):
    """The other half of A1, and the one that keeps the exemption from being
    a way past the check: two directories leave in one commit and only one of
    them has been absorbed by a policy document."""
    d, p = git_repo(tmp_path, CANONICAL)
    for name in ("1780000001-other", "1780000002-third"):
        other = d / "specs" / name
        other.mkdir(parents=True)
        (other / "overview.md").write_text("# o\n\n" + CANONICAL, encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "three"], check=True, capture_output=True
    )
    shutil.rmtree(os.path.dirname(p))
    shutil.rmtree(str(d / "specs" / "1780000001-other"))
    fold_into_docs(d, "1780000000-work")
    assert run([str(d), "--baseline", "HEAD"]) == 1
    out = capsys.readouterr().out
    assert "1780000001-other" in out and "present at HEAD and not here" in out
    assert "1780000000-work/overview.md" not in out.split("rows left the record")[-1]


def test_a_marker_quoted_in_prose_is_not_a_fold_record(tmp_path, capsys):
    """The line-anchored test `fold_ledger.py#is_marked` already pays for: a
    document that quotes the marker's shape inline, which every document
    describing the convention does, must not read as a fold."""
    d, p = git_repo(tmp_path, CANONICAL)
    other = d / "specs" / "1780000001-other"
    other.mkdir(parents=True)
    (other / "overview.md").write_text("# o\n\n" + CANONICAL, encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "two"], check=True, capture_output=True
    )
    shutil.rmtree(os.path.dirname(p))
    docs = d / "docs"
    docs.mkdir()
    (docs / "how-it-works.md").write_text(
        "Each folded sentence carries `<!-- specs/1780000000-work -->` inline.\n",
        encoding="utf-8",
    )
    assert run([str(d), "--baseline", "HEAD"]) == 1
    assert "present at HEAD and not here" in capsys.readouterr().out


def test_a_marker_inside_a_fenced_block_is_not_a_fold_record(tmp_path):
    """Round 1's 🔴. The line anchor says the marker stands alone on its line
    and never says the line is prose, so a document that QUOTES the convention
    in a fenced block satisfied the removal guard.

    The shape is the project's own: `skills/settle/SKILL.md` §2 — the one
    document a session reads before it folds — shows the marker inside a
    fenced block with a real released work item id, so a session copying that
    example into the policy it is writing hands `settle --retire` a real
    directory to delete. Measured before the fix: the retirement removed it at
    exit 0."""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a-policy.md").write_text(
        "# a segment\n\nEach folded sentence carries its comment:\n\n"
        "```markdown\n<!-- specs/1780000000-work -->\nA standing statement.\n```\n",
        encoding="utf-8",
    )
    assert uc.folded_items(str(tmp_path)) == set()
    # Positive direction in the same fixture, so the fix cannot be "find
    # nothing ever": a marker outside the fence is still a fold record.
    (docs / "b-policy.md").write_text(
        "# another\n\n<!-- specs/1780000001-other -->\nA standing statement.\n",
        encoding="utf-8",
    )
    assert uc.folded_items(str(tmp_path)) == {"1780000001-other"}


@pytest.mark.parametrize(
    "body, found",
    [
        ("<!-- specs/x-1 -->\n", {"x-1"}),
        ("```markdown\n<!-- specs/x-2 -->\n```\n", set()),
        ("~~~\n<!-- specs/x-3 -->\n~~~\n", set()),
        # A ``` inside a ```` block does not close it, which is CommonMark and
        # which `blank_fences` already implements — the reason this reuses
        # that reader instead of writing a second one.
        ("````\n```markdown\n<!-- specs/x-4 -->\n```\n````\n", set()),
        ("```\n<!-- specs/x-5 -->\n", set()),
        ("```\nx\n```\n<!-- specs/x-6 -->\n", {"x-6"}),
        ("see `<!-- specs/x-7 -->` here\n", set()),
    ],
)
def test_every_fence_shape_a_policy_document_can_carry(tmp_path, body, found):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text(body, encoding="utf-8")
    assert uc.folded_items(str(tmp_path)) == found


def test_the_shipped_skill_copied_into_docs_records_no_fold(tmp_path):
    """The class rather than the instance. `skills/settle/SKILL.md` is what a
    session reads before it writes the policy, and its worked example carries
    a real released work item id. Pasting the skill itself into `docs/` is the
    worst case a copy can produce, and it must record nothing."""
    docs = tmp_path / "docs"
    docs.mkdir()
    skill = os.path.join(ROOT, "skills", "settle", "SKILL.md")
    with open(skill, encoding="utf-8") as f:
        text = f.read()
    assert "<!-- specs/" in text, (
        "the skill no longer shows the marker, so this case is vacuous — it "
        "exists because the skill's own example is the reachable path"
    )
    (docs / "pasted.md").write_text(text, encoding="utf-8")
    assert uc.folded_items(str(tmp_path)) == set()


def test_a_marker_below_the_top_level_of_docs_is_not_a_fold_record(tmp_path):
    """`spec.md` G2 and `skills/settle/SKILL.md` §2 fix the destination as a
    flat `docs/`, so a fold never writes below the top level and a marker
    below it is somebody's notes. This repository's own `docs/experiments/` is
    four scratch files, and a quoted marker in one of them excused a removal
    nothing absorbed."""
    docs = tmp_path / "docs"
    (docs / "experiments").mkdir(parents=True)
    (docs / "experiments" / "2026-09-03-a-note.md").write_text(
        "<!-- specs/1780000000-work -->\n", encoding="utf-8"
    )
    assert uc.folded_items(str(tmp_path)) == set()
    (docs / "a-policy.md").write_text(
        "<!-- specs/1780000000-work -->\n", encoding="utf-8"
    )
    assert uc.folded_items(str(tmp_path)) == {"1780000000-work"}


def test_the_folded_line_reads_as_a_sentence(tmp_path, capsys):
    """§14: the line a person reads in the hygiene workflow's output. It
    carried a space before its comma and nothing pinned it, so nothing would
    have caught it changing either."""
    d, p = git_repo(tmp_path, CANONICAL)
    other = d / "specs" / "1780000001-other"
    other.mkdir(parents=True)
    (other / "overview.md").write_text("# o\n\n" + CANONICAL, encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "two"], check=True, capture_output=True
    )
    shutil.rmtree(os.path.dirname(p))
    fold_into_docs(d, "1780000000-work")
    assert run([str(d), "--baseline", "HEAD"]) == 0
    out = capsys.readouterr().out
    assert "<!-- specs/1780000000-work -->, so what this" in out, out
    assert " --> ," not in out, f"a space before the comma: {out}"


def test_a_marker_inside_a_commented_out_draft_is_not_a_fold_record(tmp_path):
    """Round 2's 🔴, and the other half of round 1's. A line stops being live
    three ways: a fence is a quotation, an enclosing comment is a parked draft
    and a code span is a quotation too. Round 1 closed the first; this closes
    the second, and round 4 of this work item's own chain closed the third.

    Measured before the fix: a `docs/` document with a draft section commented
    out around a real marker made `settle --retire` remove the directory at
    exit 0, nothing having absorbed it."""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a-policy.md").write_text(
        "# a segment\n\n<!-- a draft section, parked\n\n"
        "<!-- specs/1780000000-work -->\nA statement nobody has agreed to.\n\n-->\n",
        encoding="utf-8",
    )
    assert uc.folded_items(str(tmp_path)) == set()
    (docs / "b-policy.md").write_text(
        "<!-- specs/1780000001-other -->\nA standing statement.\n", encoding="utf-8"
    )
    assert uc.folded_items(str(tmp_path)) == {"1780000001-other"}


@pytest.mark.parametrize(
    "body, found",
    [
        # A marker is itself a comment, which is why the state a line STARTED
        # in is the question and the line's surviving text is not.
        ("<!-- specs/c-1 -->\n", {"c-1"}),
        ("<!-- parked\n<!-- specs/c-2 -->\n-->\n", set()),
        # The draft closes before the marker, so the marker is live again.
        ("<!-- parked\n-->\n<!-- specs/c-3 -->\n", {"c-3"}),
        # An unclosed comment runs to the end of the file.
        ("<!-- parked\n<!-- specs/c-4 -->\n", set()),
        # Opened and closed on one line before the marker on the next.
        ("<!-- a note --> and prose\n<!-- specs/c-5 -->\n", {"c-5"}),
        # Both ways of not being live at once.
        ("<!-- parked\n```\n<!-- specs/c-6 -->\n```\n-->\n", set()),
        # An opener quoted inside a code span is prose, not a draft. Three
        # top-level `docs/` documents quote the marker's shape inside
        # backticks today, each closed on its own line; one `<!--` alone in a
        # sentence would park every marker below it (round 3, finding 2).
        ("see `<!--` here\n<!-- specs/c-7 -->\n", {"c-7"}),
        # And its mirror. A CLOSER quoted inside a span is left alone, because
        # inside a comment nothing is markdown and the quotation really does
        # end the draft. So the marker below it is live and this IS a fold
        # record — the one shape where the narrowed pass reads MORE than the
        # pass that blanked every span, and `settle --retire` removes the
        # directory at exit 0. Deliberate, and pinned here so that a later
        # edit cannot take the direction back in silence.
        ("<!-- parked\nprose with `-->` in it\n<!-- specs/c-8 -->\n-->\n", {"c-8"}),
    ],
)
def test_every_comment_shape_a_policy_document_can_carry(tmp_path, body, found):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text(body, encoding="utf-8")
    assert uc.folded_items(str(tmp_path)) == found


def test_strip_comments_reads_through_the_one_comment_scanner(monkeypatch):
    """`strip_comments` keeps no private copy of the comment walk.

    It used to share `comment_scan` with `opens_outside_a_comment`, and this
    case was named for that pair. The pair is gone: `live_lines` carries the
    comment state itself now, so `comment_scan` has one reader left. What is
    still worth pinning is the half that has not changed — a second copy of
    the walk inside `strip_comments` would answer identically to the real one
    and no assertion comparing outputs could see it (round 3 of the parent
    chain, finding 4), so the scanner is replaced at module level and the
    reader has to answer from the stub."""
    lines = [
        "prose <!-- open",
        "still inside",
        "closed --> and prose again",
        "<!-- specs/x-1 -->",
    ]
    assert uc.strip_comments(lines) == [
        "prose ",
        "",
        " and prose again",
        "",
    ]
    monkeypatch.setattr(uc, "comment_scan", lambda lines: iter([(False, "SENTINEL")]))
    assert uc.strip_comments(lines) == ["SENTINEL"]


@pytest.mark.parametrize(
    "line, opens",
    [
        # A comment opener inside a code span is a quotation and opens nothing.
        ("a `<!--` c", False),
        # A backtick string closes at the next one of EQUAL length, so the
        # single backtick inside this double-backtick span is span content and
        # the opener after it is still quoted.
        ("``a ` <!--`` c", False),
        # Closed span, then a real opener outside it.
        ("`a` <!-- b", True),
        # An unmatched backtick run is literal text, so the opener is real.
        ("`open <!--", True),
        ("no span <!--", True),
        ("no span at all", False),
    ],
)
def test_a_code_span_closes_at_a_backtick_string_of_equal_length(line, opens):
    """CommonMark 6.1's span rule, asked of the scan that now implements it:
    equal-length backtick strings, an unmatched one left literal. Observed
    where it matters rather than through a blanked string — whether the line
    leaves a comment open, which is what the next line's liveness answers."""
    answer = [live for _, live in uc.live_lines([line, "<!-- specs/x-1 -->"])]
    assert answer[0] is True
    assert answer[1] is not opens


def test_the_scan_decides_a_fence_before_a_comment_or_a_span():
    """Precedence, half one. A fence opener owns its whole line, so a comment
    opener or a backtick run on the same line is fenced content and opens
    nothing — and the lines inside the block are not live however they read."""
    lines = ["```markdown <!--", "<!-- specs/x-1 -->", "```", "<!-- specs/x-2 -->"]
    assert [live for _, live in uc.live_lines(lines)] == [True, False, False, True]


def test_the_first_delimiter_on_the_line_wins():
    """Precedence, half two. Where a comment opener and a backtick run are
    both ahead, whichever comes first in the text decides: the opener first
    parks what follows, the backtick run first quotes it."""
    run_first = [live for _, live in uc.live_lines(["x `<!--` y", "after"])]
    opener_first = [live for _, live in uc.live_lines(["x <!-- `y`", "after"])]
    assert run_first == [True, True]
    assert opener_first == [True, False]


def a_reading_from_the_commonmark_rules(lines):
    """A reference reading of a markdown document, written from the format.

    Nothing here is named after, or copied from, a choice `live_lines` made —
    that was round 5's finding 2, where this function's block rule was the
    reader's own and the case built on it could not report the reader being
    wrong. Every rule below cites the specification it comes from, so a
    disagreement is settled by reading the spec rather than by reading the
    module under test.

    - **Fenced code blocks** (CommonMark 4.5): a line whose first non-space
      run is three or more backticks or tildes opens one; a line whose run is
      the same character and at least as long closes it. Nothing inside is
      parsed.
    - **HTML comments** (CommonMark 6.6, raw HTML): `<!--` opens and the next
      `-->` closes, and between them the document is not markdown at all, so
      backticks are ordinary characters.
    - **Code spans** (CommonMark 6.1): a backtick string is closed by the
      next backtick string of equal length; one with no partner is literal
      text. A code span is inline content of a leaf block, so its partner
      must lie in the same block.
    - **Where a block ends** (CommonMark 4.1, 4.2, 4.3, 4.5, 4.8, 5.1, 5.2
      and GFM 4.10): a blank line, a thematic break, an ATX heading, a fence
      delimiter, a block quote marker, a list item marker, a setext
      underline, or a table row. **A richer list is a WEAKER case, not a
      safer one**, and the sentence here used to claim the opposite. Every
      extra stop shortens `partner_in_this_block`, which makes this reading
      see fewer spans, which makes it call MORE lines live — and the only
      violation this case can report is the scan live where this reading
      parks. So each rule is the format's rule and no other, and the two
      indentation bounds below are where that stopped being true (round 6,
      finding 2).

    A line is live when it begins outside all three.
    """

    def block_ends_at(line):
        indent = len(line) - len(line.lstrip(" "))
        s = line.strip()
        if not s:
            return True
        if s.startswith("|") or s.startswith(">"):
            return True
        if indent <= 3 and s.startswith("#"):
            # CommonMark 4.2: one to six hashes, then a space, a tab or the
            # end of the line. The guard this replaces read
            # `s.lstrip("#").startswith((" ", ""))`, and `str.startswith("")`
            # is true of every string, so it asserted nothing.
            n = len(s) - len(s.lstrip("#"))
            if 1 <= n <= 6 and (len(s) == n or s[n] in " \t"):
                return True
        if set(s) == {"="}:
            return True
        if indent <= 3 and len(s) >= 3 and s[0] in "`~" and s[:3] == s[0] * 3:
            return True
        if len(s) >= 3 and s[0] in "*-_" and set(s.replace(" ", "")) == {s[0]}:
            return True
        if s[:2] in ("- ", "* ", "+ "):
            return True
        return s[:2] in ("1.", "1)") and len(s) > 2 and s[2] in " \t"

    def runs(text, at):
        n = 0
        while at + n < len(text) and text[at + n] == "`":
            n += 1
        return n

    def partner_in_this_block(start_line, start_at, width):
        # Every line reached here is a LATER line than the run's own, so each
        # one is checked: a block that ends on the first of them ends the
        # paragraph the run was opened in.
        for i in range(start_line, len(lines)):
            if block_ends_at(lines[i]):
                return False
            text = lines[i]
            j = start_at if i == start_line else 0
            while j < len(text):
                if text[j] == "`":
                    n = runs(text, j)
                    if n == width:
                        return True
                    j += n
                else:
                    j += 1
        return False

    def fence_of(line):
        # CommonMark 4.5 bounds an opening fence to three spaces. Stripping
        # the line first was the one rule this reading still took from
        # `live_lines`, and while it did, this case agreed with the scan on
        # the very shape that removed a directory (round 6, finding 2).
        if len(line) - len(line.lstrip(" ")) > 3:
            return None
        s = line.strip()
        if len(s) < 3 or s[0] not in "`~":
            return None
        n = runs(s, 0) if s[0] == "`" else len(s) - len(s.lstrip("~"))
        return s[0] * n if n >= 3 else None

    fence = None
    in_comment = False
    open_span = None
    verdict = []
    for n, line in enumerate(lines):
        verdict.append(fence is None and not in_comment and open_span is None)
        if fence is not None:
            closing = fence_of(line)
            if closing and closing[0] == fence[0] and len(closing) >= len(fence):
                fence = None
            continue
        if not in_comment and open_span is None and fence_of(line) is not None:
            fence = fence_of(line)
            continue
        i = 0
        while i < len(line):
            if in_comment:
                if line.startswith("-->", i):
                    in_comment, i = False, i + 3
                else:
                    i += 1
            elif open_span is not None:
                width = runs(line, i)
                if width == open_span:
                    open_span, i = None, i + width
                else:
                    i += width if width else 1
            elif line.startswith("<!--", i):
                in_comment, i = True, i + 4
            elif line[i] == "`":
                width = runs(line, i)
                j, closed = i + width, None
                while j < len(line):
                    here = runs(line, j)
                    if here == width:
                        closed = j + here
                        break
                    j += here if here else 1
                if closed is not None:
                    i = closed
                elif partner_in_this_block(n + 1, 0, width):
                    open_span, i = width, len(line)
                else:
                    i += width
            else:
                i += 1
    return verdict


def documents_with_several_spans_on_a_line(count, seed=20260922):
    """Documents whose lines can carry several code spans, unclosed backtick
    runs, and the block starts a span could be asked to reach past.

    The generator is half of what a fuzz is worth. With at most one span per
    line every formulation of this rule scored zero, and round 5's defect
    needs an unclosed run, a block start on a later line and the run's
    partner after it — so the tokens below include the delimiters, backtick
    runs of two lengths, a table row, a heading, a bullet and a fence.
    """
    rng = random.Random(seed)
    tokens = [
        "<!--",
        "-->",
        "`",
        "``",
        "text",
        " ",
        "<!-- specs/a -->",
        "| row |",
        "```",
        "# head",
        "- item",
        "> quote",
        # The shapes a paragraph rule can be WRONG about, without which the
        # case cannot report the class it is written for. Reverting any of
        # the three paragraph corrections reddened nothing until these
        # arrived (round 6, findings 3 and 4): a hash with no space and seven
        # hashes are paragraph text, an ordered marker that is not 1 does not
        # interrupt a paragraph, a run of `=` is a setext underline, and four
        # spaces before a delimiter is an indented code block.
        "#nospace",
        "####### seven",
        "3. item",
        "===",
        "    ```",
    ]

    def line():
        # One token alone some of the time. A setext underline and an
        # indented delimiter are only themselves when nothing follows them on
        # the line, and while every line was a join of several tokens the
        # case could not see either (round 6, findings 1 and 3).
        if rng.random() < 0.25:
            return rng.choice(tokens)
        return "".join(rng.choice(tokens) for _ in range(rng.randint(1, 8)))

    return [[line() for _ in range(rng.randint(1, 7))] for _ in range(count)]


def test_the_scan_never_reads_live_what_the_format_parks():
    """The safety direction, against a reading written from the format.

    Not full agreement: `live_lines` computes two readings and parks a line
    wherever they differ, so it deliberately parks lines the format calls
    live, and a case demanding agreement would forbid the thing that ends
    this class. What may never happen is the other direction — the scan
    calling a line live that the format parks — because that is the line a
    marker sits on when `settle --retire` removes a work item's directory
    with nothing having absorbed it. Five review rounds each found one shape
    of exactly that.
    """
    unsafe, live_seen = [], 0
    for lines in documents_with_several_spans_on_a_line(2000):
        scan = [live for _, live in uc.live_lines(lines)]
        truth = a_reading_from_the_commonmark_rules(lines)
        live_seen += sum(1 for v in scan if v)
        for n in range(len(lines)):
            if scan[n] and not truth[n]:
                unsafe.append((lines, n, scan, truth))
    assert not unsafe, (
        f"{len(unsafe)} line(s) read live where the format parks; first: {unsafe[0]}"
    )
    # Not vacuous: a reader that parked everything would satisfy the above.
    assert live_seen > 2000, live_seen


@pytest.mark.parametrize(
    "name, body, found",
    [
        # Round 1. Inside a draft nothing is markdown, so the quoted closing
        # delimiter really ends it and the marker below is a fold record.
        (
            "a closer quoted alone inside a draft",
            "<!-- a draft, parked\nprose with `-->` in it\n<!-- specs/s-1 -->\n-->\n",
            {"s-1"},
        ),
        # Round 2. A span quoting a COMPLETE comment keeps its closer, for the
        # same reason: the quotation is not one while the draft is open.
        (
            "a whole comment quoted inside a draft",
            "<!-- a draft, parked\nends with `<!-- a note -->` whole\n<!-- specs/s-2 -->\n-->\n",
            {"s-2"},
        ),
        # Round 3. A closer and then an opener inside ONE span: the draft ends
        # and re-opens, so the marker begins inside it.
        (
            "a closer then an opener in one span",
            "<!-- a draft, parked\nquotes `--> and then <!--` here\n<!-- specs/s-3 -->\n-->\n",
            set(),
        ),
        # Round 4. The same pair in two different spans on one line.
        (
            "a closer and an opener in different spans",
            "<!-- a draft, parked\n`-->` and then `<!--` more\n<!-- specs/s-4 -->\n-->\n",
            set(),
        ),
        # Round 5. An unclosed run, a draft opener on the next line, the
        # partner after it. The crossing reading calls the opener quoted and
        # the literal reading calls it real; they disagree, so the line parks.
        (
            "a span reaching past a draft opener",
            "prose with an unclosed `run\n<!-- a draft, parked\nclosing ` here\n<!-- specs/s-5 -->\n-->\n",
            set(),
        ),
        # The door `overview.md` carried from round 2: a marker between the
        # two halves of a code span. The literal reading calls it live and the
        # crossing reading parks it.
        (
            "a marker inside a multi-line code span",
            "a span opens `here\n<!-- specs/s-6 -->\nand closes` there\n",
            set(),
        ),
        # Round 6. A fence delimiter indented four spaces is an indented code
        # block, not a delimiter. One of them inverts the fence state for the
        # rest of the file, and the marker quoted inside the real fenced
        # example below becomes a fold record — `settle --retire` removing
        # the work item's directory at exit 0 with nothing having absorbed
        # it. The generator builds no indentation, so this arrives as a row.
        (
            "a marker in a fenced example under an indented delimiter",
            "A fence opens with\n\n    ```python\n\nand closes with a run "
            "at least as long.\n\n```markdown\n<!-- specs/s-8 -->\n```\n",
            set(),
        ),
        # And the control, without which every answer above is satisfied by a
        # reader that parks the whole document.
        (
            "a genuine marker, nothing quoted",
            "# a policy\n\n<!-- specs/s-7 -->\nThe standing statement.\n",
            {"s-7"},
        ),
    ],
)
def test_every_shape_five_review_rounds_named(tmp_path, name, body, found):
    """One row per shape a review round of this work item found, and the two
    controls. Each of the five was a directory removed at exit 0 or a row
    filed under another work item's id, and each was found by a round rather
    than by a case, which is what this family exists to change."""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text(body, encoding="utf-8")
    assert uc.folded_items(str(tmp_path)) == found, name


def test_the_three_named_markers_are_live_in_this_repositorys_ledger():
    """The corpus floor, as a case rather than as a figure in a record. These
    three markers are the ones the naive comment rule lost at round 0, and
    every formulation since has had to keep them.

    Every OCCURRENCE, not a dictionary keyed on the line. `seal/ledger.md`
    carries eleven marker lines twice, so keying on the text kept only the
    last state of each and a regression parking the first of a pair was
    invisible — the same shape as the oracle that could not see the class it
    was written for (round 6, finding 5)."""
    ledger = os.path.join(ROOT, "seal", "ledger.md")
    with open(ledger, encoding="utf-8") as f:
        lines = f.read().split("\n")
    occurrences = [
        (n, line.strip(), state)
        for n, (line, state) in enumerate(uc.live_lines(lines), 1)
        if line.startswith(uc.OPENER + " specs/")
    ]
    parked = [(n, line) for n, line, state in occurrences if not state]
    assert not parked, parked
    for want in (
        "1788472135-the-run-outlives-its-last-finding",
        "1788613827-a-runs-report-carries-one-comparison-table",
        "1788844127-the-reviewers-report-reaches-the-record-retyped",
    ):
        assert any(f"specs/{want} " in line for _, line, _ in occurrences), want
    assert len(occurrences) >= 90, len(occurrences)
    assert len({line for _, line, _ in occurrences}) >= 80, len(occurrences)


def test_readable_would_erase_every_fold_record():
    """Why the pair `check_text` uses is the wrong reader here, asked of the
    code rather than asserted in a comment. Round 2 confirmed the rejection by
    execution and this is the standing form of it."""
    marker = ["<!-- specs/1780000000-work -->", "A standing statement."]
    assert uc.readable("\n".join(marker))[0] == ""
    assert next(iter(uc.live_lines(marker)))[1] is True


# --- #517 D3: a spec-less directory is retired by the rule, not by a record -

CLOSED_SECTION = """## Not verified

| Item | Who must answer |
|---|---|
| ✅ how the gate renders in a TUI | seen on screen, 2026-01-01 |
"""


def moment_repo(tmp_path, section, spec=False, name="1780000009-release-0-1-0"):
    """A committed spec-less work item — a routing declaration and a memo —
    beside the fixture's own, and the path of its directory."""
    d, _ = git_repo(tmp_path, CANONICAL)
    item = d / "specs" / name
    item.mkdir(parents=True)
    (item / "routing.md").write_text(f"# {name} — routing\n", encoding="utf-8")
    (item / "overview.md").write_text(f"# {name}\n\n{section}", encoding="utf-8")
    if spec:
        (item / "spec.md").write_text("# a spec\n\nA rule.\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "moment"],
        check=True,
        capture_output=True,
    )
    return d, item


def test_a_rule_retirement_is_not_this_branchs_deletion(tmp_path, capsys):
    """A6. `settle --retire` removes a released directory that held no
    `spec.md` and nothing open, with no marker anywhere — and this arm used to
    call that a deletion, so the first fold under the rule arm would have been
    refused for every directory it removed."""
    d, item = moment_repo(tmp_path, CLOSED_SECTION)
    shutil.rmtree(item)
    assert run([str(d), "--baseline", "HEAD"]) == 0
    out = capsys.readouterr().out
    assert "present at HEAD and not here" not in out, out
    assert "retired by the rule" in out and item.name in out, out
    assert "1 retired by the rule" in out, out
    assert "folded into" not in out, "a rule retirement is named as a fold"


def test_a_rule_retirement_with_an_open_row_at_the_base_still_fails(tmp_path, capsys):
    d, item = moment_repo(tmp_path, CANONICAL)
    shutil.rmtree(item)
    assert run([str(d), "--baseline", "HEAD"]) == 1
    assert "present at HEAD and not here" in capsys.readouterr().out


def test_a_spec_at_the_base_is_still_a_deletion(tmp_path, capsys):
    """The merge-base is asked, not the tree the branch left: a spec deleted in
    one commit and its directory in the next is a deletion."""
    d, item = moment_repo(tmp_path, CLOSED_SECTION, spec=True)
    shutil.rmtree(item)
    assert run([str(d), "--baseline", "HEAD"]) == 1
    assert "present at HEAD and not here" in capsys.readouterr().out


def test_a_spec_deleted_by_an_earlier_merge_is_still_a_deletion(tmp_path, capsys):
    """Round 1's finding 3: a base whose `spec.md` an earlier commit already
    deleted still read as a spec-less work item. The predicate asks history."""
    d, item = moment_repo(tmp_path, CLOSED_SECTION, spec=True)
    (item / "spec.md").unlink()
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qam", "an earlier pull request drops it"],
        check=True,
        capture_output=True,
    )
    shutil.rmtree(item)
    assert run([str(d), "--baseline", "HEAD"]) == 1
    out = capsys.readouterr().out
    assert "present at HEAD and not here" in out, out
    assert "retired by the rule" not in out, out


def test_a_history_git_cannot_read_counts_as_a_spec_written(tmp_path):
    """`wrote_a_spec`'s failure direction: a git that cannot answer keeps the
    directory, because *never wrote one* is the answer that removes it."""
    assert uc.wrote_a_spec(str(tmp_path), None, "seal/specs/1780000009-x")


def test_a_removed_memo_in_a_directory_that_stays_is_not_a_retirement(tmp_path, capsys):
    """A retirement removes the directory. Deleting only the memo of a
    spec-less directory that stays is deleting a record, whatever it held."""
    d, item = moment_repo(tmp_path, CLOSED_SECTION)
    (item / "overview.md").unlink()
    assert run([str(d), "--baseline", "HEAD"]) == 1
    assert "present at HEAD and not here" in capsys.readouterr().out


def test_the_baseline_arm_asks_the_one_predicate(tmp_path, capsys, monkeypatch):
    """`plan.md` §*What breaks in six months*: the reader calls
    `retired_by_rule` rather than re-deriving it, so the next condition added
    to the predicate reaches this reader too."""
    d, item = moment_repo(tmp_path, CLOSED_SECTION)
    shutil.rmtree(item)
    asked = []
    monkeypatch.setattr(
        uc, "retired_by_rule", lambda root, ref, directory: asked.append(directory)
    )
    assert run([str(d), "--baseline", "HEAD"]) == 1
    assert asked == [f"specs/{item.name}"], asked


@pytest.mark.parametrize(
    "script",
    [
        ("skills", "code-review", "scripts", "chain_check.py"),
        ("skills", "code-review", "scripts", "survivor_check.py"),
        ("skills", "settle", "scripts", "settle.py"),
    ],
)
def test_every_reader_of_a_retirement_calls_the_one_predicate(script):
    """`plan.md` §*What breaks in six months*: four parties ask whether a
    removed directory was retired, and a predicate spelled in each would take
    the next condition in one and not the others. The behaviour is pinned per
    reader in its own module; this pins that each one reaches the answer by
    calling `retired_by_rule` on the module that owns it, so a reader that
    re-derives the rule inline goes red here even while it agrees today."""
    import ast

    with open(os.path.join(ROOT, *script), encoding="utf-8") as f:
        tree = ast.parse(f.read())
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "retired_by_rule"
    ]
    assert calls, (
        f"{'/'.join(script)} decides a retirement without asking the predicate"
    )
    assert not [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "retired_by_rule"
    ], f"{'/'.join(script)} defines a second `retired_by_rule`"


# --- G7: the root's own seal/specs/, empty or absent, is a settled state ----


def settled(tmp_path, keep_empty_dir):
    d = tmp_path / "repo"
    shutil.copytree(_bare_inited_repo_template(), d)
    (d / "seal").mkdir()
    (d / "seal" / "ledger.md").write_text("# ledger\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(d), "commit", "-qm", "settled"],
        check=True,
        capture_output=True,
    )
    if keep_empty_dir:
        (d / "seal" / "specs").mkdir()
    return d


@pytest.mark.parametrize("keep_empty_dir", [True, False], ids=["empty", "absent"])
@pytest.mark.parametrize("baseline", [True, False], ids=["baseline", "plain"])
def test_the_roots_own_specs_path_is_settled_when_nothing_is_under_it(
    tmp_path, capsys, keep_empty_dir, baseline
):
    """G7. Every pull request after a complete fold runs
    `--baseline origin/<base> seal/specs/`, the shipped `templates/hygiene.yml`
    included, and the path holds nothing at HEAD and held no overview at the
    merge base. That was *a typo*, exit 2 — so every such pull request red."""
    d = settled(tmp_path, keep_empty_dir)
    path = str(d / "seal" / "specs")
    argv = [path] + (["--baseline", "HEAD"] if baseline else [])
    assert run(argv) == 0, capsys.readouterr()
    out = capsys.readouterr()
    assert "holds no work item" in out.out + out.err, out


@pytest.mark.parametrize("baseline", [True, False], ids=["baseline", "plain"])
def test_any_other_missing_path_is_still_a_typo(tmp_path, capsys, baseline):
    d = settled(tmp_path, keep_empty_dir=False)
    argv = [str(d / "seal" / "spces")] + (["--baseline", "HEAD"] if baseline else [])
    assert run(argv) == 2
    assert "no such path" in capsys.readouterr().err
