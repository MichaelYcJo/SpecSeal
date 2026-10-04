"""A here-document body nothing on the line can run is data to the commit gate
(#739, work item `1791076831-a-here-document-body-is-data-to-the-commit-gate`).

The commit gate drops every heredoc body before it walks a command, and then
reads each dropped body back as shell to ask whether it commits. That second
reading is right for `bash <<'EOF'`, whose body a shell runs, and wrong for
`cat > pr.md <<'EOF'`, whose body is the text of a file. #739 measured three
whole Bash calls refused for a body that only MENTIONED a commit, in a session
whose first goal is a run that does not stop.

`spec.md` §*The rule (R)* is the contract these cases pin. A body is data only
in one positively described shape: its delimiter is quoted and its terminator
arrives, the line is plain, the body's consumer is `cat`, `tee` or a Python
program read from stdin, and nothing on the line can run a file the body
reached. Every other body is read exactly as before, which is what the second
half of this module holds in place.
"""

import pytest
from conftest import load_hook_module

reader = load_hook_module("cmdline.py", "cmdline_heredoc_data")


# --- the reader says what each body is (phase 1) ------------------------------

QUOTINGS = {
    "<<'EOF'": True,
    '<<"EOF"': True,
    "<<\\EOF": True,
    "<<E'O'F": True,
    "<<EOF": False,
    "<<$'EOF'": False,
    '<<$"EOF"': False,
}


@pytest.mark.parametrize("opener", sorted(QUOTINGS))
def test_each_body_says_whether_its_delimiter_was_quoted(opener):
    """R2a. A delimiter is quoted when the word as written holds a quote or a
    backslash and no `$`: what bash makes of `$'…'` there is not settled, and
    an unsettled case keeps the reading that stops."""
    records = reader.heredocs(f"cat {opener}\nbody\nEOF\n")
    assert [r.quoted for r in records] == [QUOTINGS[opener]], records


@pytest.mark.parametrize("opener", ["<<-'EOF'", "<<-EOF"])
def test_a_tab_stripped_body_reports_the_same_way(opener):
    """R2a for `<<-`: the dash changes where the terminator is found, not
    whether the delimiter was quoted."""
    records = reader.heredocs(f"cat {opener}\n\tbody\n\tEOF\n")
    assert len(records) == 1, records
    assert records[0].dashed and records[0].terminated, records
    assert records[0].quoted is ("'" in opener), records


def test_a_body_whose_terminator_never_arrives_says_so():
    """R2b. The body runs to the end of the input, as it always did, and the
    record says the delimiter line never came."""
    done = reader.heredocs("cat <<'EOF'\nbody\nEOF\n")
    open_ended = reader.heredocs("cat <<'EOF'\nbody\ngit commit -m x")
    assert [r.terminated for r in done] == [True]
    assert [r.terminated for r in open_ended] == [False]
    assert open_ended[0].text == "body\ngit commit -m x"


def test_two_bodies_come_back_in_delimiter_order_each_with_its_own_answer():
    records = reader.heredocs("cat <<'A' <<B\na\nA\nb\nB\n")
    assert [(r.text, r.quoted, r.delimiter) for r in records] == [
        ("a", True, "A"),
        ("b", False, "B"),
    ]


SAME_AS_EVER = [
    "cat > run.sh <<'EOF'\ncd /x\nmake\nEOF\ngit add -A && git commit -m x",
    "cat <<-EOF\n\tx\n\tEOF\ngit commit -m x",
    "cat <<'EOF'\nnever ends",
    "cat <<'A' <<B\na\nA\nb\nB\necho done",
    "git commit -m \"$(cat <<'EOF'\nsubject\nEOF\n)\"",
    "n=$((1<<2))\ngit commit -m x",
    "cat <<<hello\ngit commit -m x",
    "python3 - <<EOF#x -c 'x'\nbody\nEOF#x",
]


@pytest.mark.parametrize("command", SAME_AS_EVER)
def test_the_two_old_views_are_views_of_the_records(command):
    """S11. `drop_heredoc_bodies` and `heredoc_bodies` keep their outputs: the
    bodies are the records' texts, and the stripped command is what it was."""
    assert reader.heredoc_bodies(command) == [r.text for r in reader.heredocs(command)]
    lines = reader.drop_heredoc_bodies(command).split("\n")
    for record in reader.heredocs(command):
        for line in record.text.split("\n") if record.text else ():
            assert line not in lines, (command, lines)
