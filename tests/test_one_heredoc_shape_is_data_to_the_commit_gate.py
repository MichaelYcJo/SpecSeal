"""The one heredoc shape is data to the commit gate, and every other body is
read as it was (#739, #763).

Work item `1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data`,
scenarios S1-S5 and S7. Where `hooks/one_heredoc.py` matches a command, the
gate reads it with the body taken out; where it does not, nothing changed.

"Silent" is the gate's `main()` in an opted-in session directory with no git
hooks installed. A case that says something stops runs from a DECLARED
session directory wherever it can, so that the body is the only thing on the
command that could stop it.
"""

import json
import shlex
import subprocess

import pytest
from conftest import decision_of, declare_routing, load_hook_module, run_hook
from test_one_heredoc_shape_is_read_exactly import FAILS, admitted

gate = load_hook_module("commit-review-gate.py", "crg_one_heredoc")

# What the base answers for a body it reads as a commit: the refusal for a
# command it cannot place, which names no repository a person can act on.
CONSTRUCT = "contains something the gate cannot read as a plain command"

# #739's own bodies. Each carries a commit the shell reading finds: in a
# double-quoted backtick pair, and on a line of its own.
PR_BODY = "quotes `git -C /x commit -m y`\ngit commit -m x"
PY_BODY = (
    'note = """\nrun `git commit` later\ngit commit -m x\n"""\n'
    'open("m.md", "a", encoding="utf-8").write(note)'
)


def q(text):
    return shlex.quote(str(text))


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
    if declared:
        declare_routing(path)
    return path


def decide(command, cwd, session="one-heredoc"):
    out = run_hook(
        "commit-review-gate.py",
        {
            "tool_name": "Bash",
            "tool_input": {"command": command},
            "cwd": str(cwd),
            "session_id": session,
        },
    )
    return decision_of(out), out


# --- S1: refusal 1, as recorded -----------------------------------------------


def refusal_1(where):
    """A LEAD `cd` to a plain path, a Python program on stdin appending to a
    memory file, and a `grep` count after the terminator."""
    return f"cd {q(where)} && python3 - <<'EOF'\n{PY_BODY}\nEOF\ngrep -c git m.md"


def test_refusal_1_as_recorded_is_silent(tmp_path):
    """S1. Red at `e141980a`: a deny with the text for a command the gate
    cannot place."""
    session = make_repo(tmp_path / "session")
    got, out = decide(refusal_1(session), session)
    assert got == "silent", out


# --- S2: refusals 2 and 3, restated -------------------------------------------


def test_refusal_2_restated_the_sink_alone_is_silent(tmp_path):
    """S2. The body written to a path spelled out, in a call of its own; the
    `gh` line holds no heredoc and was silent at the base already."""
    session = make_repo(tmp_path / "session")
    scratch = tmp_path / "scratch" / "pr.md"
    for command in (
        f"cat > {q(scratch)} <<'EOF'\n{PR_BODY}\nEOF\n",
        f"tee {q(scratch)} <<'EOF'\n{PR_BODY}\nEOF",
        f"cd {q(session)} && cat >> pr.md <<'EOF'\n{PR_BODY}\nEOF",
        f"gh pr edit 1 --body-file {q(scratch)} && gh pr ready 1",
    ):
        got, out = decide(command, session)
        assert got == "silent", (command, out)


def refusal_3_restated(where, repo):
    """A LEAD `cd`, the path found inside the Python program, and the same
    `git -C` lines after the terminator."""
    return (
        f"cd {q(where)} && python3 - <<'EOF'\n{PY_BODY}\nEOF\n"
        f"git -C {q(repo)} add f && git -C {q(repo)} commit -m x"
    )


def test_refusal_3_restated_is_judged_where_its_commit_lands(tmp_path):
    """S2. The body says nothing about where the commit lands, so the one
    invocation left is the real one, with its `-C`: silent for a declared
    repository, and a stop naming an undeclared one rather than the
    unplaceable-construct text. Red at `e141980a` for the declared one."""
    session = make_repo(tmp_path / "session")
    for repo, expected in (
        (make_repo(tmp_path / "declared", declared=True), "silent"),
        (make_repo(tmp_path / "undeclared"), "deny"),
    ):
        got, out = decide(refusal_3_restated(session, repo), session)
        assert got == expected, out
        assert CONSTRUCT not in out, out
        if expected == "deny":
            # The reason as the hook wrote it, decoded: on Windows the JSON
            # escapes every backslash of the path, so the raw stdout never
            # holds `str(repo)` verbatim.
            reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
            assert str(repo) in reason, out


# --- S3: refusals 2 and 3, as recorded: the cost Q2 accepts -------------------


def test_refusals_2_and_3_as_recorded_still_stop(tmp_path):
    """S3. Green before and after: an assignment LEAD, a parameter as the
    target or the argument, a substitution, and programs after a sink each
    leave the grammar, so the body is read as at the base."""
    session = make_repo(tmp_path / "session", declared=True)
    declared = make_repo(tmp_path / "declared", declared=True)
    scratch = q(tmp_path / "pr.md")
    for command in (
        f"F={scratch}; cat > \"$F\" <<'EOF'\n{PR_BODY}\nEOF\n"
        f'cd {q(session)} && gh pr edit 1 --body-file "$F" && gh pr ready 1',
        f"F=$(ls -d {q(tmp_path)}/*.md) && python3 - \"$F\" <<'EOF'\n{PY_BODY}\nEOF\n"
        f"git -C {q(declared)} add f && git -C {q(declared)} commit -m x",
    ):
        got, out = decide(command, session)
        assert got in ("deny", "ask"), (command, out)
        assert CONSTRUCT in out, out


# --- S4: the shape's edges, through the gate ----------------------------------


@pytest.mark.parametrize("head", sorted(set(admitted())))
def test_each_slot_of_the_shape_is_silent(tmp_path, head):
    """S4. Each sink form and the program, with and without arguments and the
    LEAD, a plain and a single-quoted WORD, with a commit-bearing body."""
    session = make_repo(tmp_path / "session")
    body = PY_BODY if "python3" in head else PR_BODY
    got, out = decide(f"{head} <<'EOF'\n{body}\nEOF\n", session)
    assert got == "silent", out


# A string that fails a clause and holds no body the shell reading finds a
# commit in has nothing for the base to stop.
NO_BODY = {"B: no newline at all"}


@pytest.mark.parametrize("name", sorted(set(FAILS) - NO_BODY))
def test_a_string_that_fails_one_clause_still_stops(tmp_path, name):
    """S4. Each fails exactly the clause its name gives and carries a
    commit-bearing body, so the gate reads it as at the base, and stops."""
    session = make_repo(tmp_path / "session", declared=True)
    got, out = decide(FAILS[name], session)
    assert got in ("deny", "ask"), (FAILS[name], out)


# --- S5: #760's findings and must-stop lists, rebuilt as fixtures -------------

COMMIT = "git commit -m x"

FINDINGS = {
    "round 2 red 1: a second unquoted body whose $( a backslash-newline splits": (
        f"cat > f.sh <<'A'\n{COMMIT}\nA\ncat <<B\n$\\\n(sh f.sh)\nB"
    ),
    "round 3 red 1: a backslash-newline inside the delimiter word": (
        f"cat > f <<'E\\\nOF'\n{COMMIT}\nEOF"
    ),
    "#763 red 1: a backslash-newline in an unquoted second delimiter": (
        f"cat <<'A'\nbody\nA\ncat <<E\\\nOF\n{COMMIT}\nEOF"
    ),
    "#763 red 1: a backslash-newline splitting the opener": (
        f"cat > f.sh <<'A'\n{COMMIT}\nA\ncat <\\\n<B\nsh f.sh\nB"
    ),
    "post-review red 1: the delimiter plus a CR, then a second opener": (
        f"cat > f <<'EOF'\nEOF\r\nbash <<'B'\n{COMMIT}\nB\nEOF"
    ),
    "post-review red 2: a # tail under a delimiter ending in a blank": (
        f"cat > f <<'EOF '\nEOF #\nbash <<'B'\n{COMMIT}\nB\nEOF "
    ),
    "round 3 yellow 2: a file written over a program the line runs from PATH": (
        f"cat > bin/grep <<'A'\n{COMMIT}\nA\ngrep x f"
    ),
    "post-review yellow 3: gh runs git from PATH": (
        f"cat > git <<'A'\n{COMMIT}\nA\ngh pr ready 1"
    ),
    "post-review yellow 3: ssh -G runs a Match exec": (
        f"cat > cfg <<'A'\n{COMMIT}\nA\nssh -G -F cfg host"
    ),
    "1790635415 r2: a program flag after the heredoc": (
        f"python3 <<'EOF' -c 'import os,sys; os.system(sys.stdin.read())'\n{COMMIT}\nEOF"
    ),
    "1790635415 r2: a bundled -Bc": (
        f"python3 -Bc'import os,sys; os.system(sys.stdin.read())' <<'EOF'\n{COMMIT}\nEOF"
    ),
    "1790635415 r2: $(...) before the program": (
        f"sh -s $(true) python3 <<'EOF'\n{COMMIT}\nEOF"
    ),
    "1790635415 r2: ${...;...} before it": (
        f"sh -s ${{x:-;X=}} python3 - <<'EOF'\n{COMMIT}\nEOF"
    ),
    "1790635415 r3: # glued to a quoted delimiter": (
        f"python3 <<'EOF'#x -c 'import os'\n{COMMIT}\nEOF#x"
    ),
}

# Every consumer, wrapper and construct #760 left read. Each runs its body, or
# can be made to, or is a spelling the one shape does not admit.
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

FILE_RUNNERS = [
    "bash f.sh",
    "sh f.sh",
    "./f.sh",
    "source f.sh",
    "make",
    "python3 - <<'P'\nimport os; os.system('sh f.sh')\nP",
    "git add f.sh",
    "gh pr create --body-file f.sh",
    "gh pr checkout 1",
    "gh alias import f.sh",
    "gh api repos/x/y --input f.sh",
    "gh pr view 1 --web",
    "gh pr edit 1",
    "cat <(bash f.sh)",
    "echo >(sh f.sh)",
    "echo `sh f.sh`",
    "echo $'\\'' ; sh f.sh ; echo \\'",
    "cat <<B\n$(sh f.sh)\nB",
    "cat <<B\n$\\\n(sh f.sh)\nB",
]

WRITERS = [
    "cat > f.sh <<'EOF'",
    "tee f.sh <<'EOF'",
    "cat <<'EOF' | tee f.sh",
    "cat <<'EOF' &> f.sh",
]

NESTED = [
    "bash <<<\"$(cat <<'EOF'\ngit commit -m x\nEOF\n)\"",
    "source <(cat <<'EOF'\ngit commit -m x\nEOF\n)",
    "eval \"$(cat <<'EOF'\ngit commit -m x\nEOF\n)\"",
    "bash <<'O'\ncat > f <<'I'\ngit commit -m x\nI\nbash f\nO",
    "sh -c \"$(cat <<'EOF'\ngit commit -m x\nEOF\n)\"",
    "git commit -m \"$(cat <<'EOF'\nsubject\nEOF\n)\"; bash <<'B'\ngit commit -m x\nB",
]


def must_stop():
    rows = dict(FINDINGS)
    for head in CONSUMERS_READ:
        rows[f"consumer: {head}"] = f"{head}\n{COMMIT}\nEOF"
    for writer in WRITERS:
        for runner in FILE_RUNNERS:
            rows[f"writer: {writer} / {runner}"] = f"{writer}\n{COMMIT}\nEOF\n{runner}"
    for i, command in enumerate(NESTED):
        rows[f"nested {i}"] = command
    return rows


MUST_STOP = must_stop()


@pytest.mark.parametrize("name", sorted(MUST_STOP))
def test_what_760_found_still_stops(tmp_path, name):
    """S5. Green at `e141980a` and after: none of these is the one shape, so
    each body is read as shell, and the commit in it stops the command."""
    assert gate.one_heredoc.reduce(MUST_STOP[name]) is None, name
    session = make_repo(tmp_path / "session", declared=True)
    got, out = decide(MUST_STOP[name], session)
    assert got in ("deny", "ask"), (name, out)


# --- S7: the program's suffix is read the base's way --------------------------

SUFFIXES = [
    "git add f && git commit -m x",
    "git commit -m x",
    "cd {w} && git commit -m x",
    "git -C {w} commit -m x",
    "true ; git add f && git commit -m x",
    "echo done",
]


@pytest.mark.parametrize("suffix", SUFFIXES)
def test_the_suffix_decides_as_the_base_does_on_the_line_without_its_body(
    tmp_path, suffix
):
    """S7. The decision on the program shape equals the base's decision on the
    same line with the body taken out, from an undeclared session directory
    and a declared `w`, each in a fresh session."""
    session = make_repo(tmp_path / "session")
    w = make_repo(tmp_path / "w", declared=True)
    tail = suffix.format(w=q(w))
    whole = f"cd {q(w)} && python3 - <<'EOF'\n{PY_BODY}\nEOF\n{tail}"
    without = f"cd {q(w)} && python3 -\n{tail}"
    assert gate.one_heredoc.reduce(whole) == without
    assert decide(whole, session, "a")[0] == decide(without, session, "b")[0]


def test_the_reduction_reaches_the_unparsed_fallback(tmp_path):
    """A body that mentions both words no longer meets the base's fallback for
    a command the splitter cannot finish: the substring test reads the reduced
    text. The fallback judges the session's own directory, which is opted in
    and undeclared here, so at `e141980a` this stopped."""
    session = make_repo(tmp_path / "session")
    body_only = "python3 - <<'EOF'\nprint('git commit')\nEOF\necho $'it\\'s'"
    assert decide(body_only, session)[0] == "silent"
    found, clean = gate.commit_invocations(gate.one_heredoc.reduce(body_only))
    assert (found, clean) == ([], False)
