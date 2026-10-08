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


# --- #773: a waiver inside a here-document body is data -----------------------
#
# Work item `1791119070-a-waiver-inside-a-here-document-body-is-data`,
# scenarios S1, S2, S3, S5 and S6. Both consent reads, `has_marker` here and
# `hooks/tokens.py#given` for the git hook, read the command without its
# here-document bodies, and only where the base read also found the token.
# Each command is built from named parts -- the opener, the body, the suffix --
# and judged through the hook's decision function, never run as a command.
# "The tokenless verdict" is the same command with the body's token replaced
# by a plain word, judged in a fresh session.

WAIVER = "[no-review]"


def commit_into(repo):
    """The suffix every case commits with: a `git -C` the reader can place."""
    return f"git -C {q(repo)} add f && git -C {q(repo)} commit -m x"


def tokenless(command):
    """`command` with the waiver replaced by a word that waives nothing."""
    assert WAIVER in command
    return command.replace(WAIVER, "later")


def s1_program_body(target):
    """The one shape with the program: a Python string literal holds the
    token, and the suffix commits into `target` (#769 round 1's probe)."""
    body = f'note = "{WAIVER}"\nprint(note)'
    return f"python3 - <<'EOF'\n{body}\nEOF\n{commit_into(target)}"


# Openers the one-shape reader refuses, each feeding a body no shell runs:
# `spec.md` case 3.
OUTSIDE_THE_SHAPE = {
    "a sink with an unquoted delimiter": "cat > {scratch} <<EOF",
    "a sink with a double-quoted delimiter": 'cat > {scratch} <<"EOF"',
    "another interpreter": "python - <<'EOF'",
}


def s2_body_outside_the_shape(opener, scratch, target):
    """An opener `one_heredoc` refuses, the token alone on a body line, and a
    commit after the terminator."""
    return f"{opener.format(scratch=q(scratch))}\n{WAIVER}\nEOF\n{commit_into(target)}"


def test_s1_a_token_in_the_program_body_waives_nothing(tmp_path):
    """S1, `spec.md` case 2. Red at `94d7b2e0`: the base read the literal's
    token as a bare word and the commit into the undeclared repository went
    through silent."""
    session = make_repo(tmp_path / "session")
    target = make_repo(tmp_path / "undeclared")
    command = s1_program_body(target)
    assert gate.one_heredoc.reduce(command) is not None
    got, out = decide(command, session, "with")
    assert got == decide(tokenless(command), session, "without")[0], out
    assert got in ("deny", "ask"), out


@pytest.mark.parametrize("name", sorted(OUTSIDE_THE_SHAPE))
def test_s2_a_token_in_a_body_outside_the_shape_waives_nothing(tmp_path, name):
    """S2, `spec.md` case 3. Red at `94d7b2e0` for each opener: the body's
    token silenced the commit after the terminator."""
    session = make_repo(tmp_path / "session")
    target = make_repo(tmp_path / "undeclared")
    command = s2_body_outside_the_shape(
        OUTSIDE_THE_SHAPE[name], tmp_path / "pr.md", target
    )
    assert gate.one_heredoc.reduce(command) is None
    got, out = decide(command, session, "with")
    assert got == decide(tokenless(command), session, "without")[0], out
    assert got in ("deny", "ask"), out


DOCUMENTED = {
    "the no-op in front, outside the shape": (
        ": '{w}'; cat > {scratch} <<EOF\nbody\nEOF\n{commit}"
    ),
    "a trailing comment after the terminator, outside the shape": (
        "cat > {scratch} <<EOF\nbody\nEOF\n{commit}  # {w}"
    ),
    "a trailing comment on the program's suffix": (
        "python3 - <<'EOF'\nprint(1)\nEOF\n{commit}  # {w}"
    ),
    # #868: an apostrophe AFTER the token in its comment keeps it; one before
    # it is `test_a_waiver_behind_an_apostrophe_in_its_comment_waives_nothing`.
    "a trailing comment with an apostrophe after the waiver": (
        "cat > {scratch} <<EOF\nbody\nEOF\n{commit}  # {w} -- it's a probe"
    ),
}


def documented(name, scratch, target):
    return DOCUMENTED[name].format(
        w=WAIVER, scratch=q(scratch), commit=commit_into(target)
    )


@pytest.mark.parametrize("name", sorted(DOCUMENTED))
def test_s3_the_documented_forms_still_waive_beside_a_body(tmp_path, name):
    """S3. Green before and after: the token typed outside every body, in front
    or in a comment, still waives. The tokenless command stops, so the token is
    what silences it."""
    session = make_repo(tmp_path / "session")
    target = make_repo(tmp_path / "undeclared")
    command = documented(name, tmp_path / "pr.md", target)
    got, out = decide(command, session, "with")
    assert got == "silent", out
    assert decide(tokenless(command), session, "without")[0] in ("deny", "ask")


def test_a_waiver_behind_an_apostrophe_in_its_comment_waives_nothing(tmp_path):
    """#868 In 3, the cost the frame named: `# don't [no-review]` opens a quote
    at the apostrophe to the one token reader, which reads comments on
    purpose, so the waiver after it is inside a quote that never closes and
    reads as nothing. It waived through `has_marker`'s substring fallback
    until work item 1791384157, and was the documented form this module
    pinned as S3's `a trailing comment with an apostrophe`. No recorded run
    held one (`phases/phase-1.md`). It meets the tokenless verdict now, and
    the waiver typed in front is the way on."""
    session = make_repo(tmp_path / "session")
    target = make_repo(tmp_path / "undeclared")
    command = (
        f"cat > {q(tmp_path / 'pr.md')} <<EOF\nbody\nEOF\n"
        f"{commit_into(target)}  # don't {WAIVER}"
    )
    got, out = decide(command, session, "with")
    assert got == decide(tokenless(command), session, "without")[0], out
    assert got in ("deny", "ask"), out
    assert decide(f": '{WAIVER}'; {command}", session, "front")[0] == "silent"


def s5_shell_body(target, in_front=False):
    """A body `bash` runs, holding a commit; the token either inside the body,
    in front of that commit, or typed in front of the Bash call's own command."""
    commit = commit_into(target)
    if in_front:
        return f": '{WAIVER}'; bash <<EOF\n{commit}\nEOF\n"
    return f"bash <<EOF\n: '{WAIVER}'; {commit}\nEOF\n"


def test_s5_a_token_inside_a_body_a_shell_runs_waives_nothing(tmp_path):
    """S5, `spec.md` case 4: the cost the frame accepted, pinned. Red at
    `94d7b2e0`, where the token inside the body silenced the commit the body
    runs. Now it gets the tokenless verdict, and the same token typed in front
    of the Bash call's own command is the way on."""
    session = make_repo(tmp_path / "session")
    target = make_repo(tmp_path / "undeclared")
    command = s5_shell_body(target)
    got, out = decide(command, session, "with")
    assert got == decide(tokenless(command), session, "without")[0], out
    assert got in ("deny", "ask"), out
    assert decide(s5_shell_body(target, in_front=True), session, "front")[0] == (
        "silent"
    )


# Two commands where taking the body out turns the raw text's split around, so
# the read without bodies finds the token where the base read did not
# (`plan.md` alternative F). Neither is a command a shell would run; each is
# here because the AND is the only thing that refuses it.
#   * the body's lone `"` quotes the token in the raw text; without the body,
#     the quote after the token never closes and the substring fallback reads
#     it (has_marker's half);
#   * the raw text never closes its last quote and reads nothing; without the
#     body, every quote closes and the token is a bare word (given's half).
NEWLY_READ = {
    "has_marker": f'cat <<EOF\n"\nEOF\necho {WAIVER} "',
    "given": f'cat <<EOF\n"\nEOF\necho {WAIVER} "\n"',
}


def base_marker(command):
    """`has_marker` as it stood at `94d7b2e0`: the strict scan over the raw
    command where it splits cleanly, the substring test where it does not."""
    segments, clean = gate.split_segments(command)
    if not clean:
        return WAIVER in command
    return any(tok == WAIVER for toks in segments for tok in toks)


def base_given(command):
    """`tokens.given` as it stood at `94d7b2e0`: the bare words of the raw
    command."""
    found = {w.strip("()") for w in gate.tokens.words(command)}
    return {t for t in gate.tokens.KNOWN if t in found}


def every_case(tmp_path):
    scratch, target = tmp_path / "pr.md", tmp_path / "undeclared"
    yield s1_program_body(target)
    for opener in OUTSIDE_THE_SHAPE.values():
        yield s2_body_outside_the_shape(opener, scratch, target)
    for name in DOCUMENTED:
        yield documented(name, scratch, target)
    yield s5_shell_body(target)
    yield s5_shell_body(target, in_front=True)
    yield from NEWLY_READ.values()


def test_s6_neither_read_honours_a_token_the_base_did_not(tmp_path):
    """S6. For every command above, each read finds a token only where the
    base read found it. `NEWLY_READ` turns red the moment either read drops
    the AND with its base read; the rest are green at `94d7b2e0` by
    definition.

    Since #868 the two reads are one (`has_marker` is `tokens.given`), and
    it reads the words before a split fails, so its base is the two base
    reads together: it finds a token only where one of them did. The
    documented comment with an apostrophe after the waiver is the case the
    strict base `given` refused and `has_marker` read."""
    for command in every_case(tmp_path):
        bases = base_given(command) | ({WAIVER} if base_marker(command) else set())
        assert not gate.has_marker(command, WAIVER) or base_marker(command), command
        assert set(gate.tokens.given(command)) <= bases, command
    assert not base_marker(NEWLY_READ["has_marker"])
    assert not gate.has_marker(NEWLY_READ["has_marker"], WAIVER)
    assert not base_given(NEWLY_READ["given"])
    assert gate.tokens.given(NEWLY_READ["given"]) == ()


# --- #868 In 3: the waiver has one reader --------------------------------------


@pytest.mark.parametrize(
    "command",
    [
        # The waiver typed inside a quote that never closes: prose to a shell
        # that would refuse to run the command, never a bare word.
        "git commit -m 'x [no-review]",
        'git commit -m "x [no-review]',
    ],
)
def test_a_waiver_only_a_substring_holds_waives_nothing(tmp_path, command):
    """S7 of work item 1791384157 (#868). `has_marker` read a command that
    does not split by the substring test, so a `[no-review]` inside an
    unclosed quote waived the review arm. It reads through `tokens.given` now,
    which takes no word from inside a quote, so the review arm is missing and
    the refusal names the waiver typed in front, which splits. Red at
    `5623d728`, where the gate was silent."""
    repo = make_repo(tmp_path / "undeclared")
    got, out = decide(f"cd {q(repo)} && {command}", repo)
    assert got in ("deny", "ask"), out
    assert "No review is recorded" in out and ": '[no-review]'" in out, out
