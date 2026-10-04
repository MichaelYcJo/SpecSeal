"""The one heredoc shape `hooks/one_heredoc.py` admits, slot by slot, and a
string that fails each of its clauses A-E (#739, #763).

Work item `1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data`,
`spec.md` §*The shape* and scenario S4's reader half. Every admitted string
here comes back as its reduced text, and every string that fails one clause
comes back as None, which is what makes the gate read it as before. The
gate's half of S4 is in `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py`.
"""

import ast
import os

import pytest
from conftest import load_hook_module

reader = load_hook_module("one_heredoc.py", "one_heredoc_exactly")

HOOK = os.path.join(os.path.dirname(__file__), "..", "hooks", "one_heredoc.py")

# A body the shell reading would find a commit in, on a line of its own.
BODY = "say `git commit` later\ngit commit -m x"

SINKS = ["cat > {w}", "cat >> {w}", "tee {w}", "tee -a {w}"]
PROGRAMS = ["python3 -", "python3 - {w}", "python3 - {w} {w}"]
WORDS = ["note.md", "./a/b-c_d.txt", "'a dir/with $ and `x`'"]
LEADS = ["", "cd /x/y && ", "cd '/Users/x/a b' && "]


def admitted():
    for lead in LEADS:
        for word in WORDS:
            for consumer in SINKS + PROGRAMS:
                yield lead + consumer.format(w=word)


@pytest.mark.parametrize("head", sorted(set(admitted())))
def test_each_slot_of_the_first_line_is_admitted(head):
    """S4: each sink form, the program with and without arguments, a plain
    and a single-quoted WORD, with and without the LEAD."""
    for end in ("EOF", "EOF\n", "EOF\n\n"):
        command = f"{head} <<'EOF'\n{BODY}\n{end}"
        assert reader.reduce(command) == head, repr(command)
        assert reader._match(command) == (head, BODY + "\n"), repr(command)


@pytest.mark.parametrize("delimiter", ["EOF", "A", "_", "9", "x_Y_1"])
def test_every_delimiter_of_the_alphabet_is_admitted(delimiter):
    command = f"cat > f <<'{delimiter}'\nbody\n{delimiter}"
    assert reader._match(command) == ("cat > f", "body\n")


def test_an_empty_body_is_a_body():
    assert reader._match("cat > f <<'EOF'\nEOF") == ("cat > f", "")
    assert reader._match("cat > f <<'EOF'\nEOF\n") == ("cat > f", "")
    assert reader._match("cat > f <<'EOF'\n\nEOF\n") == ("cat > f", "\n")


def test_the_body_ends_at_the_first_exact_line():
    """C: every line that is not exactly D stays in the body, and the first
    one that is ends it."""
    near = ["EOF ", " EOF", "\tEOF", "EOF\t", "EOF#x", "'EOF'", "EOFEOF", "EOF;"]
    body = "\n".join(near)
    command = f"tee f <<'EOF'\n{body}\nEOF\n"
    assert reader._match(command) == ("tee f", body + "\n")


def test_the_programs_suffix_is_kept_and_the_body_is_gone():
    """E and F: after `python3 -`, what follows the terminator is a suffix,
    and the reduced text is the first line, a newline, and that suffix."""
    command = (
        "cd /x && python3 - a.md <<'EOF'\n"
        f"{BODY}\nEOF\ngrep -c x a.md\ngit -C /x commit -m y\n"
    )
    assert reader.reduce(command) == (
        "cd /x && python3 - a.md\ngrep -c x a.md\ngit -C /x commit -m y\n"
    )


def test_a_programs_terminator_followed_only_by_newlines_has_no_body_left():
    for end in ("EOF", "EOF\n"):
        got = reader.reduce(f"python3 - <<'EOF'\n{BODY}\n{end}")
        assert got == "python3 -"
        assert "commit" not in got


# Each string below fails exactly the clause it is filed under, and carries a
# commit-bearing body, so None here is the gate reading it as before.
FAILS = {
    # A. Bytes where a reader and some shell were measured or can be shown to
    # disagree, anywhere in the command.
    "A: a carriage return in the body": f"cat > f <<'EOF'\n{BODY}\r\nEOF",
    "A: a carriage return on the terminator": f"cat > f <<'EOF'\n{BODY}\nEOF\r\nEOF",
    "A: a carriage return ending line 1": f"cat > f <<'EOF'\r\n{BODY}\nEOF",
    "A: a NUL in the body": f"cat > f <<'EOF'\n\0{BODY}\nEOF",
    "A: a backslash-newline in the body": f"cat > f <<'EOF'\nx\\\n{BODY}\nEOF",
    "A: a backslash-newline before the terminator": f"cat > f <<'EOF'\n{BODY}\\\nEOF",
    "A: a backslash-newline in a program's suffix": (
        "python3 - <<'EOF'\nprint(1)\nEOF\ngit \\\ncommit -m x"
    ),
    # B. The first line, character for character.
    "B: a space before the line": f" cat > f <<'EOF'\n{BODY}\nEOF",
    "B: two spaces": f"cat  > f <<'EOF'\n{BODY}\nEOF",
    "B: a tab": f"cat >\tf <<'EOF'\n{BODY}\nEOF",
    "B: a glued redirection": f"cat >f <<'EOF'\n{BODY}\nEOF",
    "B: a glued opener": f"cat > f<<'EOF'\n{BODY}\nEOF",
    "B: an unquoted delimiter": f"cat > f <<EOF\n{BODY}\nEOF",
    "B: a double-quoted delimiter": f'cat > f <<"EOF"\n{BODY}\nEOF',
    "B: a partly quoted delimiter": f"cat > f <<E'OF'\n{BODY}\nEOF",
    "B: an ANSI-C delimiter": f"cat > f <<$'EOF'\n{BODY}\nEOF",
    "B: a backslash delimiter": f"cat > f <<\\EOF\n{BODY}\nEOF",
    "B: the tab-stripping opener": f"cat > f <<-'EOF'\n{BODY}\nEOF",
    "B: a blank in the delimiter": f"cat > f <<'E F'\n{BODY}\nE F",
    "B: a dash in the delimiter": f"cat > f <<'E-F'\n{BODY}\nE-F",
    "B: an empty delimiter": f"cat > f <<''\n{BODY}\n",
    "B: text after the delimiter": f"cat > f <<'EOF' && echo\n{BODY}\nEOF",
    "B: a trailing space after the delimiter": f"cat > f <<'EOF' \n{BODY}\nEOF",
    "B: a comment after the delimiter": f"cat > f <<'EOF' #x\n{BODY}\nEOF",
    "B: a glued # after the delimiter": f"cat > f <<'EOF'#x\n{BODY}\nEOF#x",
    "B: cat to standard output": f"cat <<'EOF'\n{BODY}\nEOF",
    "B: a shell consumer": f"bash <<'EOF'\n{BODY}\nEOF",
    "B: an unversioned python": f"python - <<'EOF'\n{BODY}\nEOF",
    "B: a python flag": f"python3 -u - <<'EOF'\n{BODY}\nEOF",
    "B: python3 -c": f"python3 -c 'import os' <<'EOF'\n{BODY}\nEOF",
    "B: python3 without -": f"python3 <<'EOF'\n{BODY}\nEOF",
    "B: a flag after python3 -": f"python3 - -c x <<'EOF'\n{BODY}\nEOF",
    "B: a parameter as the target": f"cat > \"$F\" <<'EOF'\n{BODY}\nEOF",
    "B: a bare parameter as the target": f"cat > $F <<'EOF'\n{BODY}\nEOF",
    "B: a parameter as the program's argument": f"python3 - $F <<'EOF'\n{BODY}\nEOF",
    "B: a glob in the target": f"cat > *.md <<'EOF'\n{BODY}\nEOF",
    "B: a tilde in the target": f"cat > ~/f <<'EOF'\n{BODY}\nEOF",
    "B: a double-quoted target": f"cat > \"f\" <<'EOF'\n{BODY}\nEOF",
    "B: an assignment LEAD": f"F=/x && cat > f <<'EOF'\n{BODY}\nEOF",
    "B: an assignment prefix": f"F=/x cat > f <<'EOF'\n{BODY}\nEOF",
    "B: a substitution in the LEAD": f"cd $(ls -d /x) && cat > f <<'EOF'\n{BODY}\nEOF",
    "B: a LEAD joined by ;": f"cd /x; cat > f <<'EOF'\n{BODY}\nEOF",
    "B: two LEADs": f"cd /x && cd y && cat > f <<'EOF'\n{BODY}\nEOF",
    "B: a pipe after the sink": f"cat > f <<'EOF' | sh\n{BODY}\nEOF",
    "B: a second redirection": f"cat > f 2>&1 <<'EOF'\n{BODY}\nEOF",
    "B: tee to two files": f"tee a b <<'EOF'\n{BODY}\nEOF",
    "B: the opener on line 2": f"echo hi\ncat > f <<'EOF'\n{BODY}\nEOF",
    "B: no newline at all": "cat > f <<'EOF'",
    "B: an unterminated single quote in a WORD": f"cat > 'f <<'EOF'\n{BODY}\nEOF",
    # C. The terminator: a line exactly D, and nothing stripped first.
    "C: no terminator": f"cat > f <<'EOF'\n{BODY}",
    "C: only a terminator with a trailing blank": f"cat > f <<'EOF'\n{BODY}\nEOF ",
    "C: only an indented terminator": f"cat > f <<'EOF'\n{BODY}\n\tEOF",
    "C: only a terminator with a # tail": f"cat > f <<'EOF'\n{BODY}\nEOF #",
    # D. Exactly one `<<` outside the body.
    "D: a second heredoc in the suffix": (
        f"python3 - <<'EOF'\nprint(1)\nEOF\nbash <<'X'\n{BODY}\nX"
    ),
    "D: a here-string in the suffix": (
        "python3 - <<'EOF'\nprint(1)\nEOF\nbash <<< 'git commit -m x'"
    ),
    "D: an arithmetic shift in the suffix": (
        "python3 - <<'EOF'\nprint(1)\nEOF\nn=$((1<<2)); git commit -m x"
    ),
    "D: a `<<` inside a quoted WORD": f"cat > 'a<<b' <<'EOF'\n{BODY}\nEOF",
    # E. After a sink, nothing but newlines.
    "E: a command after a sink": f"cat > f <<'EOF'\n{BODY}\nEOF\ngit commit -m x",
    "E: a command after a sink's blank line": (
        f"cat > f <<'EOF'\n{BODY}\nEOF\n\nbash f"
    ),
    "E: a space after a sink": f"cat > f <<'EOF'\n{BODY}\nEOF\n ",
    "E: a comment after a sink": f"tee f <<'EOF'\n{BODY}\nEOF\n# done",
}


@pytest.mark.parametrize("name", sorted(FAILS))
def test_a_string_that_fails_one_clause_is_no_match(name):
    assert reader.reduce(FAILS[name]) is None, repr(FAILS[name])
    assert reader._match(FAILS[name]) is None


@pytest.mark.parametrize("value", [None, b"cat > f <<'EOF'\nx\nEOF", 1])
def test_a_command_that_is_not_text_is_no_match(value):
    assert reader.reduce(value) is None


def test_a_body_line_equal_to_the_delimiter_ends_it_however_it_is_quoted():
    """C, from the other side: the reader does not look inside the body for
    quotes, so a delimiter line inside what looks like a string still ends
    the body -- and a sink with anything after that is no match (E)."""
    command = "cat > f <<'EOF'\ns = '''\nEOF\n'''\nEOF"
    assert reader.reduce(command) is None


def test_the_reader_imports_nothing_but_re():
    """The owner's instruction that the decision not rest on the shared
    splitter, made checkable: no `cmdline`, `cmdline_base` or `tokens`, and no
    shell lexer."""
    with open(HOOK, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module)
    assert imported == {"re"}, imported
