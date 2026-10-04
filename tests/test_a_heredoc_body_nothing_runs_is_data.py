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

import shlex
import subprocess

import pytest
from conftest import decision_of, declare_routing, load_hook_module, run_hook

reader = load_hook_module("cmdline.py", "cmdline_heredoc_data")
gate = load_hook_module("commit-review-gate.py", "crg_heredoc_data")

# What the base answered for each of #739's three calls: the refusal for a
# command it cannot place, which names no repository a person can act on.
CONSTRUCT = "contains something the gate cannot read as a plain command"


def make_repo(path, declared=False):
    """An opted-in repository with one commit and a staged change, and no git
    hooks, so the PreToolUse reading is the one that judges."""
    path.mkdir(parents=True)
    run = lambda *a: subprocess.run(
        ["git", "-C", str(path), *a], check=True, capture_output=True
    )
    run("init", "-q")
    (path / "f").write_text("1\n", encoding="utf-8")
    run("add", "f")
    run("-c", "user.email=e@example.com", "-c", "user.name=e", "commit", "-qm", "b")
    (path / "f").write_text("2\n", encoding="utf-8")
    run("add", "f")
    (path / "seal").mkdir()
    (path / "seal" / "config.md").write_text(
        "| Item | Value |\n|---|---|\n| Mode | shared |\n", encoding="utf-8"
    )
    if declared:
        declare_routing(path)
    return path


def decide(command, cwd):
    """The gate's decision and its reason, through `main()` as the harness
    calls it."""
    out = run_hook(
        "commit-review-gate.py",
        {
            "tool_name": "Bash",
            "tool_input": {"command": command},
            "cwd": str(cwd),
            "session_id": "heredoc-data",
        },
    )
    return decision_of(out), out


# --- the reader says what each body is (phase 1) ------------------------------

QUOTINGS = {
    "<<'EOF'": True,
    '<<"EOF"': True,
    "<<E'O'F": True,
    "<<EOF": False,
    "<<$'EOF'": False,
    '<<$"EOF"': False,
    # A backslash fails closed wherever it stands (#763): the shell removes a
    # backslash-newline before it reads the word, so the reader cannot be
    # sure which parts of the word were quoted.
    "<<\\EOF": False,
    "<<E\\\nOF": False,
    "<<'E\\\nOF'": False,
    '<<"E\\\nOF"': False,
    "<<'E'\\\n'OF'": False,
    # A newline or a backtick inside the word is not one the reader can be
    # sure of either.
    "<<'E\nOF'": False,
    "<<'E`x`OF'": False,
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


# --- the gate reads only what can run (phase 2) -------------------------------

# A body that the shell reading finds a commit in. A commit named only inside
# single quotes or in a `#` line was already silent at the base, so each body
# here carries one in command position or in a double-quoted backtick.
PR_BODY = "quotes `git -C /x commit -m y`\ngit commit -m x"
PY_BODY = "open('m.md', 'a').write(\"run `git commit` later\")\n# then git commit -m x"
GH = "gh pr edit 1 --body-file pr.md; gh pr ready 1"


def pr_command(opener="<<'EOF'", end="EOF"):
    """#739's second call: a pull request body written to a file, then
    handed to `gh`."""
    return f"cat > pr.md {opener}\n{PR_BODY}\n{end}\n{GH}"


def py_command(opener="<<'EOF'", end="EOF"):
    """#739's first call: a Python program that appends a note to a file."""
    return f"python3 - {opener}\n{PY_BODY}\n{end}"


def test_a_pull_request_body_that_quotes_a_commit_is_silent(tmp_path):
    """S1, #739's second row. Red at `101f9bd0`: a deny with the text for a
    command the gate cannot place."""
    session = make_repo(tmp_path / "session")
    got, out = decide(pr_command(), session)
    assert got == "silent", out


def test_a_python_program_that_mentions_a_commit_is_silent(tmp_path):
    """S2, #739's first row. Red at `101f9bd0` the same way."""
    session = make_repo(tmp_path / "session")
    got, out = decide(py_command(), session)
    assert got == "silent", out


def test_the_real_commit_after_a_python_body_is_judged_where_it_lands(tmp_path):
    """S3, #739's third row. The body says nothing about where the commit
    lands, so the one invocation left is the real one, with its `-C`: silent
    for a declared repository, and a stop for an undeclared one that names
    that repository instead of the unplaceable-construct text."""
    session = make_repo(tmp_path / "session")
    for repo, expected in (
        (make_repo(tmp_path / "declared", declared=True), "silent"),
        (make_repo(tmp_path / "undeclared"), "deny"),
    ):
        r = shlex.quote(str(repo))
        command = (
            f"python3 - \"$F\" <<'EOF' && git -C {r} add f && git -C {r} commit -m x\n"
            f's = "`git commit`"\nEOF'
        )
        found, clean = gate.commit_invocations(command, str(session))
        assert clean and [list(inv.chdirs) for inv in found] == [[str(repo)]], found
        got, out = decide(command, session)
        assert got == expected, out
        assert CONSTRUCT not in out, out


QUOTED_OPENERS = {
    "<<-'EOF'": "\tEOF",
    '<<"EOF"': "EOF",
    "<<E'O'F": "EOF",
}


@pytest.mark.parametrize("opener", sorted(QUOTED_OPENERS))
def test_every_quoting_of_the_delimiter_is_data(tmp_path, opener):
    """S4. `<<-` strips the tabs from the body and the terminator and changes
    nothing else; red at `101f9bd0` for each."""
    session = make_repo(tmp_path / "session")
    end = QUOTED_OPENERS[opener]
    for command in (pr_command(opener, end), py_command(opener, end)):
        if opener.startswith("<<-"):
            command = command.replace(PR_BODY, "\t" + PR_BODY.replace("\n", "\n\t"))
        got, out = decide(command, session)
        assert got == "silent", (command, out)


@pytest.mark.parametrize("opener", ["<<EOF", "<<$'EOF'", "<<-EOF", "<<\\EOF"])
def test_an_unquoted_delimiter_keeps_the_body_read(tmp_path, opener):
    """S5. The outer shell expands `$( … )` and backticks in such a body, and
    reading it for those alone needs a scanner this work does not build."""
    session = make_repo(tmp_path / "session")
    for command in (pr_command(opener), py_command(opener)):
        got, out = decide(command, session)
        assert got in ("deny", "ask"), (command, out)


def test_a_body_whose_terminator_never_arrives_stays_read(tmp_path):
    """R2b. The body runs to the end of the input, and the lines a reader with
    another delimiter would call commands are in it."""
    session = make_repo(tmp_path / "session")
    got, out = decide(f"cat > pr.md <<'EOF'\n{PR_BODY}\n{GH}", session)
    assert got == "deny", out


# Every consumer, wrapper and construct the rule leaves read (spec §*Shapes*).
# Each one runs its body, or can be made to, or is a spelling the rule does
# not recognise as plain.
CONSUMERS_READ = [
    "bash <<'EOF'",
    "sh -s <<'EOF'",
    "zsh <<'EOF'",
    "cat <<'EOF' | sh",
    "cat <<'EOF' | bash -s",
    "cat <<'EOF' | python3 -",
    "source /dev/stdin <<'EOF'",
    ". /dev/stdin <<'EOF'",
    "exec bash <<'EOF'",
    "sudo bash <<'EOF'",
    "env cat <<'EOF'",
    "command cat <<'EOF'",
    "/bin/cat <<'EOF'",
    "\\cat <<'EOF'",
    "'cat' <<'EOF'",
    "X=1 cat <<'EOF'",
    "$SH <<'EOF'",
    "perl - <<'EOF'",
    "node - <<'EOF'",
    "xargs <<'EOF'",
    "ssh host <<'EOF'",
    "python3 -c 'import sys' <<'EOF'",
    "python3 -Bc'import sys' <<'EOF'",
    "python3 <<'EOF' -c 'import sys'",
    "python3 x.py <<'EOF'",
    "python3 $X <<'EOF'",
    "python3 -u - <<'EOF'",
    "cat 0<<'EOF'",
    "cat 3<<'EOF'",
    "cat <<'EOF' &",
    "cat <<'EOF' >&python3",
    "{ cat; } <<'EOF'",
    "( cat ) <<'EOF'",
    "if true; then cat <<'EOF'",
    "for x in a; do cat <<'EOF'",
    "f() { cat; }; f <<'EOF'",
    "cat <<'EOF' > >(bash)",
    "cat <<'EOF' $(true)",
    "git -c core.hooksPath=/x status; cat <<'EOF'",
    "cat <<'EOF' | git am",
    "cat <<'EOF' | gh extension exec x",
]


@pytest.mark.parametrize("head", CONSUMERS_READ)
def test_a_body_something_can_run_is_still_read(tmp_path, head):
    """S6. Green at `101f9bd0` and after: each stops for the commit in its
    body. Run from a declared repository, so the body is the only thing that
    can stop it."""
    session = make_repo(tmp_path / "session", declared=True)
    got, out = decide(f"{head}\ngit commit -m x\nEOF", session)
    assert got in ("deny", "ask"), out


FILE_RUNNERS = [
    "bash f.sh",
    "sh f.sh",
    "./f.sh",
    "source f.sh",
    "make",
    "python3 - <<'P'\nimport os; os.system('sh f.sh')\nP",
    "git commit -m y",
    "git add f.sh",
    "gh pr create --body-file f.sh",
    "gh pr checkout 1",
    "gh alias import f.sh",
    # `gh` runs a program its configuration names -- a pager, a browser, an
    # editor -- except in the two subcommands that provably run nothing
    # local (#763).
    "gh api repos/x/y --input f.sh",
    "gh pr view 1 --web",
    "gh pr edit 1",
    # A program the plain words hide: a process substitution, a backtick
    # pair, and a `$'…'` whose escaped quote `shlex` reads as two quotes, so
    # it sees one `echo` where bash runs `sh f.sh` between two.
    "cat <(bash f.sh)",
    "echo >(sh f.sh)",
    "echo `sh f.sh`",
    "echo $'\\'' ; sh f.sh ; echo \\'",
    # A body behind an unquoted delimiter: the outer shell runs its
    # substitution, which runs the file the first body was written to.
    "cat <<B\n$(sh f.sh)\nB",
    # The same, split by a backslash-newline the shell removes first.
    "cat <<B\n$\\\n(sh f.sh)\nB",
]


@pytest.mark.parametrize("runner", FILE_RUNNERS)
def test_a_written_file_a_line_could_run_keeps_its_body_read(tmp_path, runner):
    """S7. A sink that writes a file is data only where nothing on the line
    can run that file: a shell or a Python program can, and git runs hooks,
    which a file the line wrote may be. From a declared repository, so the
    body is the only thing that can stop it."""
    session = make_repo(tmp_path / "session", declared=True)
    for writer in (
        "cat > f.sh <<'EOF'",
        "tee f.sh <<'EOF'",
        "cat <<'EOF' | tee f.sh",
        "cat <<'EOF' &> f.sh",
    ):
        command = f"{writer}\ngit commit -m x\nEOF\n{runner}"
        got, out = decide(command, session)
        assert got in ("deny", "ask"), (command, out)


NESTED = [
    "bash <<<\"$(cat <<'EOF'\ngit commit -m x\nEOF\n)\"",
    "source <(cat <<'EOF'\ngit commit -m x\nEOF\n)",
    "eval \"$(cat <<'EOF'\ngit commit -m x\nEOF\n)\"",
    "bash <<'O'\ncat > f <<'I'\ngit commit -m x\nI\nbash f\nO",
    "sh -c \"$(cat <<'EOF'\ngit commit -m x\nEOF\n)\"",
]


@pytest.mark.parametrize("command", NESTED)
def test_a_body_below_the_top_level_is_still_read(tmp_path, command):
    """S8. A substitution's value goes wherever the command around it sends
    it, and the reading inside cannot see where, so R1 keeps every body below
    the top level read."""
    session = make_repo(tmp_path / "session", declared=True)
    got, out = decide(command, session)
    assert got in ("deny", "ask"), out


def test_a_written_file_nothing_on_the_line_runs_is_data(tmp_path):
    """R2f's other side. A sink's file beside the `gh` subcommands that
    provably run nothing local, beside `cd` and beside `echo`, is data; red at
    `101f9bd0`."""
    session = make_repo(tmp_path / "session")
    for after in (GH, "cd . && echo done"):
        command = f"cat > pr.md <<'EOF'\n{PR_BODY}\nEOF\n{after}"
        got, out = decide(command, session)
        assert got == "silent", (command, out)


@pytest.mark.parametrize(
    "command",
    [
        f"cat <<'A' > pr.md\n{PR_BODY}\nA\npython3 - <<'B'\n{PY_BODY}\nB",
        f"cat <<'A' | grep -v x > /dev/null\n{PR_BODY}\nA",
        f"cat <<'A' <<'B'\n{PR_BODY}\nA\n{PR_BODY}\nB",
        # A file another pipeline writes is not one this body reached.
        f"cat <<'A' | grep -v x\n{PR_BODY}\nA\necho y > out.txt; git status",
    ],
)
def test_two_bodies_and_a_pipeline_are_each_judged(tmp_path, command):
    """R2d and R2f together: each body is matched to its own opener, a sink
    feeding a plain pipeline is data, and a sink writing a file beside a
    Python program is not."""
    session = make_repo(tmp_path / "session")
    got, out = decide(command, session)
    expected = "deny" if "python3" in command else "silent"
    assert got == expected, (command, out)


tokens = load_hook_module("tokens.py", "tokens_heredoc_data")


@pytest.mark.parametrize(
    "command, expected",
    [
        # R2e is a closed list: a plain program that owns a body is not on it.
        ("grep x <<'EOF'\nbody\nEOF", [False]),
        ("git commit -F - <<'EOF'\nbody\nEOF", [False]),
        ("cat <<'EOF'\nbody\nEOF", [True]),
        ("python3 - <<'EOF'\nbody\nEOF", [True]),
        # R2c: a word that steps around git's hooks keeps every body read.
        ("cat <<'EOF' CLAUDECODE=\nbody\nEOF", [False]),
        # R2c: a `git -c` sets only a key `is_plain` allows.
        ("git -c alias.x=y status; cat <<'EOF'\nbody\nEOF", [False]),
        ("git -c user.name=y status; cat <<'EOF'\nbody\nEOF", [True]),
        # R2c carries every word guard of `is_plain`: an `--output` option
        # writes a file no redirection names, `printf -v` assigns a variable,
        # and a body behind an unquoted delimiter is expanded by the outer
        # shell, so no body on such a line is data (round 2: the owner's
        # structural rule). A backslash-newline joins `$` and `(` before the
        # expansion, `${x:=…}` assigns, and the file another body was written
        # to is what an expansion can reach.
        (
            "cat <<'EOF' | git diff --no-index --output=h - /dev/null\nbody\nEOF",
            [False],
        ),
        ("printf -v PATH %s .; cat <<'EOF'\nbody\nEOF", [False]),
        ("cat > f.sh <<'A'\nbody\nA\ncat <<B\n$(sh f.sh)\nB", [False, False]),
        ("cat > f.sh <<'A'\nbody\nA\ncat <<B\n`sh f.sh`\nB", [False, False]),
        ("cat > f.sh <<'A'\nbody\nA\ncat <<B\n$\\\n(sh f.sh)\nB", [False, False]),
        ("cat > f.sh <<'A'\nbody\nA\ncat <<B\n${x:=y}\nB", [False, False]),
        ("cat <<'A'\nbody\nA\ncat <<B\nplain text\nB", [False, False]),
        # A line whose bodies are all quoted keeps its verdicts.
        ("cat <<'A'\nbody\nA\ncat <<'B'\n$(sh f.sh)\nB", [True, True]),
        ("cat > f.sh <<'A'\nbody\nA\npython3 - <<'B'\nprint(1)\nB", [False, True]),
        # R2d: an opener the line reads differently from the reader -- here
        # `<<- 'EOF'`, whose dash stands apart -- keeps every body read.
        ("cat <<- 'EOF'\nbody\nEOF", [False]),
        ("cat <<-'EOF'\nbody\nEOF", [True]),
        # #763: where line continuation lets the reader's view of an opener
        # differ from the shell's, every body on the line is read -- a
        # backslash-newline inside a delimiter word, and one splitting the
        # `<<` itself so the reader opens no body where the shell does.
        ("cat <<'A'\nbody\nA\ncat <<E\\\nOF\nbody\nEOF", [False, False]),
        ("cat <<'A'\nbody\nA\ncat <\\\n<cat\necho hi\ncat", [False]),
        # R2f: a write over a program the line runs from `PATH`, `git`
        # among them where `gh` runs it.
        ("cat > bin/grep <<'A'\nbody\nA\ngrep x f", [False]),
        ("cat > git <<'A'\nbody\nA\ngh pr ready 1", [False]),
        ("cat > pr.md <<'A'\nbody\nA\ngh pr edit 1 --body-file pr.md", [True]),
    ],
)
def test_the_rule_answers_per_body(command, expected):
    assert tokens.heredoc_data(command) == expected
