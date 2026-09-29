"""A commit written after a reserved word on the same line is a commit (#669).

Found while building work item `1790644505` and confirmed by the orchestrator
at `3911a8cf`: `for d in a; do git commit -m x; done`, `while …; do git commit
…; done` and `if true; then git commit …; fi` each reached the commit gate as
no commit at all. The shell splits them at `;`, so the commit arrives as a
segment whose first word is `do` or `then`, and `cmdline.parse_git` looked for
`git` in that position alone. A shell runs every one of those commits, and the
gate said nothing.

The same commands written across lines were always judged: `do` then stands
on a line of its own, the commit is its own segment, and the walk gives it the
unresolved directory a loop body has. So the reading after the fix is the
multi-line spelling's reading, and a case below holds the two spellings
against each other.

**Only stricter.** A reserved word that begins a command list is read past to
the command word after it. Where the command word cannot be found by position
-- a `case` arm, a function body, a coprocess -- the first `git` word in the
segment is read as the command word, and the segment's directory is
unresolved, which is a stop wherever the session's own repository opted in.
Nothing the base read as a commit reads differently, because every segment the
new reading reaches began with a word the base's reading refused.
"""

import io
import json
import os
import sys

import pytest
from conftest import load_hook_module
from test_no_shape_the_base_stops_reads_silent import make_repo

gate = load_hook_module("commit-review-gate.py", "crg_reserved_words")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hooks"))
import cmdline  # noqa: E402  -- the plain name both gates import

C = "git commit -m x"
UNRESOLVED, HERE = "unresolved", "here"

# (command, where its commit is judged). `here` is the directory the shell is
# in, as for any simple command; `unresolved` is what a loop or conditional
# body, a loop condition that runs again, and a construct whose command word
# is not found by position all get.
SHAPES = {
    # #669's three, as the issue names them.
    "for": (f"for d in a; do {C}; done", UNRESOLVED),
    "while": (f"while true; do {C}; break; done", UNRESOLVED),
    "if": (f"if true; then {C}; fi", UNRESOLVED),
    # The rest of the reserved words that begin a command list.
    "until": (f"until false; do {C}; done", UNRESOLVED),
    "select": (f"select d in a; do {C}; done", UNRESOLVED),
    "else": (f"if false; then :; else {C}; fi", UNRESOLVED),
    "elif": (f"if false; then :; elif {C}; then :; fi", UNRESOLVED),
    "an if condition": (f"if {C}; then :; fi", UNRESOLVED),
    "a while condition": (f"while {C}; do break; done", UNRESOLVED),
    # A group, a subshell, a negation and `time` behind one of them.
    "a group in a body": (f"for d in a; do {{ {C}; }}; done", UNRESOLVED),
    "a subshell in a body": (f"for d in a; do ( {C} ); done", UNRESOLVED),
    "a glued subshell in a body": (f"if true; then ({C}); fi", UNRESOLVED),
    "a negation in a body": (f"if true; then ! {C}; fi", UNRESOLVED),
    "time in a body": (f"for d in a; do time {C}; done", UNRESOLVED),
    "a negated commit": (f"! {C}", HERE),
    # Constructs whose command word is not found by position.
    "a case arm": (f"case x in a) {C};; esac", UNRESOLVED),
    "a later case arm": (f"case x in a) :;; b) {C};; esac", UNRESOLVED),
    "a function body": (f"f() {{ {C}; }}", UNRESOLVED),
    "a spaced function body": (f"f () {{ {C}; }}", UNRESOLVED),
    "a function keyword": (f"function f {{ {C}; }}", UNRESOLVED),
    "a coprocess": (f"coproc {C}", UNRESOLVED),
}

# Round 1 of 1790644505, yellow 4: the same class for `eval`. Each runs its
# `eval` in bash, and each was silent at the base and at `f25c6b1a`, because
# `_eval_argument` read past assignments alone.
EVALS = {
    "then": f"if true; then eval '{C}'; fi",
    "do, over a variable": 'for c in a; do eval "$c"; done',
    "a while condition": f"while eval '{C}'; do break; done",
    "!": f"! eval '{C}'",
    "time": f"time eval '{C}'",
    "command": f"command eval '{C}'",
    "builtin": f"builtin eval '{C}'",
    "a subshell": f"(eval '{C}')",
    "a spaced subshell": f"( eval '{C}' )",
    "a group": f"{{ eval '{C}'; }}",
}


@pytest.mark.parametrize("name", sorted(EVALS))
def test_an_eval_behind_the_same_words_is_read(name, tmp_path):
    """Seen red at `f25c6b1a`, where each returned nothing."""
    assert found(EVALS[name], tmp_path), name


def found(command, cwd):
    return gate.commit_invocations(command, str(cwd))[0]


@pytest.mark.parametrize("name", sorted(SHAPES))
def test_the_commit_is_read(name, tmp_path):
    """Seen red at `ade83e4e`, where every one of these returned nothing."""
    command, where = SHAPES[name]
    invocations = found(command, tmp_path)
    assert invocations, f"{name}: no commit read in {command!r}"
    for inv in invocations:
        unresolved = isinstance(inv.base, cmdline.Unresolved)
        assert unresolved == (where == UNRESOLVED), (name, inv.base)


# The same command with the reserved word on a line of its own, which is the
# spelling the base already read.
ACROSS_LINES = {
    "for": f"for d in a; do\n{C}\ndone",
    "while": f"while true; do\n{C}\nbreak\ndone",
    "if": f"if true; then\n{C}\nfi",
    "else": f"if false; then :; else\n{C}\nfi",
    "an if condition": f"if\n{C}\nthen :; fi",
    "a case arm": f"case x in a)\n{C}\n;; esac",
    "a function body": f"f() {{\n{C}\n}}",
}


def test_the_one_line_spelling_is_judged_as_the_multi_line_one(tmp_path):
    """The base always judged a body written across lines. The same body on
    one line is now judged the same way, which is the argument that the new
    reading invents nothing. The multi-line half passes at the base too."""
    for name, multi in ACROSS_LINES.items():
        one = [type(i.base) for i in found(SHAPES[name][0], tmp_path)]
        many = [type(i.base) for i in found(multi, tmp_path)]
        assert many == [cmdline.Unresolved], (name, "the base's own reading moved")
        assert one == many, name


def test_a_directory_already_unreadable_keeps_its_reason(tmp_path):
    """An expanded value the walk already could not read stays a VALUE, so the
    stop still tells the model to write the path out rather than naming a
    construct it did not meet."""
    (inv,) = found('cd "$WT" && if git commit -m x; then :; fi', tmp_path)
    assert isinstance(inv.base, cmdline.Unresolved)
    assert inv.base.why == cmdline.Unresolved.VALUE


def test_a_reserved_word_that_begins_no_command_list_reads_nothing(tmp_path):
    """The words after `for`, `select`, `case` and `in` are names and words,
    and a closer ends a list. Nothing here is a command, so nothing is read."""
    for command in (
        "for d in git commit; do :; done",
        "select d in git commit; do :; done",
        "[[ git == commit ]]",
        "echo git commit",
    ):
        assert not found(command, tmp_path), command


def test_the_guard_reads_the_same_command_word(tmp_path):
    """`parse_git` is the one reading both gates and the consent writer use,
    so a switch or a creation in a loop body is read as one too."""
    for tokens, sub in (
        (["do", "git", "switch", "main"], "switch"),
        (["then", "!", "git", "worktree", "add", "../wt"], "worktree"),
        (["else", "{", "git", "checkout", "main"], "checkout"),
    ):
        parsed = cmdline.parse_git(tokens)
        assert parsed and parsed[0] == sub, tokens


def say(monkeypatch, capsys, command, cwd):
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": str(cwd),
        "session_id": "s",
    }
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    gate.main()
    printed = capsys.readouterr().out.strip()
    return (
        json.loads(printed)["hookSpecificOutput"]["permissionDecision"]
        if printed
        else "silent"
    )


@pytest.mark.parametrize("name", sorted(SHAPES))
def test_the_gate_stops_the_commit(monkeypatch, capsys, tmp_path, name):
    """Through `main()`, in an opted-in repository with no declaration: every
    shape stops, where at `ade83e4e` every one of them was silent."""
    repo = make_repo(tmp_path / "repo")
    assert say(monkeypatch, capsys, SHAPES[name][0], repo) == "deny", name


def test_a_declared_repository_still_stops_a_commit_it_cannot_place(
    monkeypatch, capsys, tmp_path
):
    """An unresolved directory stops before any declaration is read, the way
    the multi-line spelling always has; the negated commit, which runs where
    the shell is, stays silent in a declared repository like any commit."""
    repo = make_repo(tmp_path / "repo", declared=True)
    for name, (command, where) in SHAPES.items():
        expected = "silent" if where == HERE else "deny"
        assert say(monkeypatch, capsys, command, repo) == expected, name
        for marker in (repo / ".git" / "specseal-commit-choice").glob("*"):
            marker.unlink()


def test_a_heredoc_body_that_loops_over_a_commit_stops(monkeypatch, capsys, tmp_path):
    """`_hides_a_commit` reads a body through the same `parse_git`."""
    repo = make_repo(tmp_path / "repo")
    body = f"bash <<'EOF'\nfor d in a; do {C}; done\nEOF"
    assert gate._hides_a_commit(body.split("\n", 1)[1].rsplit("\n", 1)[0])
    assert say(monkeypatch, capsys, body, repo) == "deny"
