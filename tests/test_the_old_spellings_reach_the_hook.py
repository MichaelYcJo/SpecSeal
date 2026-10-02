"""The old consent spellings reach the git hook, for one Bash call only
(#692, `questions.md` P3 answer (a), W6).

`hooks/tokens.py` reads the bare words, `hooks/answers.py` keeps them, and the
two PreToolUse/PostToolUse gates around them write and clear. What a hook does
with an answer is `tests/test_the_commit_gate_decides_at_the_commit.py`'s.
"""

import io
import json
import os
import sys
import time
from pathlib import Path

import pytest
from conftest import load_hook_module

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hooks"))
import answers
import tokens

writer = load_hook_module("answer-write.py", "answer_write_under_test")
clearer = load_hook_module("answer-clear.py", "answer_clear_under_test")


@pytest.mark.parametrize(
    "command, found",
    [
        (": '[no-review]'; git commit -m x", ("[no-review]",)),
        ("git worktree add ../wt f  # [worktree-ok]", ("[worktree-ok]",)),
        ("(git worktree add ../wt f [worktree-ok])", ("[worktree-ok]",)),
        (
            ": '[no-review]' '[no-parity]'; git commit -m x",
            ("[no-review]", "[no-parity]"),
        ),
        ('git commit -m "drop [no-review] later"', ()),
        ("git commit -m x[no-review]", ()),
        ("echo 'it''s [no-review]", ()),
        ("git commit -m x", ()),
    ],
    ids=[
        "the no-op form",
        "in a comment",
        "riding a parenthesis",
        "two",
        "inside a message",
        "glued to a word",
        "an unbalanced quote reads nothing",
        "none",
    ],
)
def test_a_token_is_a_bare_word_and_nothing_else(command, found):
    assert tokens.given(command) == found


A = ": '[no-review]'; bin/test && git commit -m a"
B = "git commit -m b"


def shell(command):
    """The argv the Bash tool's shell carries for COMMAND, as `ps -ww -o
    args=` printed it on macOS in this harness: the command inside `eval
    '…'`, each `'` written `'"'"'`, and a newline as `\\012`."""
    quoted = command.replace("'", "'\"'\"'").replace("\n", "\\012")
    return (
        "/bin/zsh -c source /Users/x/.claude/shell-snapshots/snapshot-zsh-1.sh "
        f"2>/dev/null || true && eval '{quoted}' < /dev/null && pwd -P >| /tmp/c"
    )


def test_an_answer_is_given_to_the_call_that_carried_it_and_no_other(tmp_path):
    """Round 1's 🟡 9: the parent and every subagent share one session id, so
    a token keyed by the session alone waived another agent's commit while
    the call that carried it ran."""
    root = str(tmp_path)
    answers.write("s1", "call-a", A, ("[no-review]",), root=root)
    assert answers.given("s1", "[no-review]", [shell(A)], root=root)
    assert not answers.given("s1", "[no-review]", [shell(B)], root=root)
    assert not answers.given("s1", "[no-parity]", [shell(A)], root=root)
    assert not answers.given("s2", "[no-review]", [shell(A)], root=root)
    assert not answers.given("s1", "[no-review]", [], root=root)


def test_another_call_neither_replaces_nor_clears_an_answer(tmp_path):
    """The other half of 🟡 9: the writer cleared the session's answers for
    every new call, so a second agent's Bash call took the first's away."""
    root = str(tmp_path)
    answers.write("s1", "call-a", A, ("[no-review]",), root=root)
    answers.write("s1", "call-b", B, (), root=root)
    answers.clear("s1", "call-b", root=root)
    assert answers.given("s1", "[no-review]", [shell(A)], root=root)
    answers.clear("s1", "call-a", root=root)
    assert not answers.given("s1", "[no-review]", [shell(A)], root=root)


@pytest.mark.parametrize(
    "command",
    [
        ": '[no-review]'; echo \"it's\" && git commit -m x",
        ": '[no-review]'\ngit commit -m x",
        ": '[no-review]'; git commit -m 'é 한글'",
    ],
    ids=["a quote", "a newline", "non-ascii"],
)
def test_the_shells_own_spelling_of_the_command_still_matches(tmp_path, command):
    root = str(tmp_path)
    answers.write("s1", "call-a", command, ("[no-review]",), root=root)
    printed = shell(command).replace("é", "\\303\\251")
    assert answers.given("s1", "[no-review]", [printed], root=root)


def test_the_argv_is_read_only_when_an_answer_is_there(tmp_path):
    def unread():
        raise AssertionError("the process table was walked for nothing")

    assert not answers.given("s1", "[no-review]", unread, root=str(tmp_path))


def test_an_answer_older_than_a_bash_call_can_run_is_not_given(tmp_path):
    root = str(tmp_path)
    answers.write("s1", "call-a", A, ("[no-review]",), root=root)
    path = tmp_path / "s1" / "call-a" / "no-review"
    old = time.time() - answers.FRESH - 5
    os.utime(path, (old, old))
    assert not answers.given("s1", "[no-review]", [shell(A)], root=root)


def test_an_answer_stamped_a_clock_tick_ahead_is_given_and_one_far_ahead_is_not(
    tmp_path,
):
    """#692's Windows pass: Python 3.12's `time.time()` there trails the
    stamp NTFS gives a write by up to a tick, so an answer read right after
    it was written read as written in the future, and a different case of
    `test_the_shells_own_spelling_of_the_command_still_matches` failed in
    each run. A stamp set well into the future is still no answer."""
    root = str(tmp_path)
    answers.write("s1", "call-a", A, ("[no-review]",), root=root)
    stamped = os.stat(tmp_path / "s1" / "call-a" / "no-review").st_mtime
    tick = 0.016
    assert answers.given("s1", "[no-review]", [shell(A)], root=root, now=stamped - tick)
    assert not answers.given(
        "s1", "[no-review]", [shell(A)], root=root, now=stamped - 3600
    )


def test_a_call_left_behind_is_pruned_by_the_next_write(tmp_path):
    """A call another gate denied never reaches `post-bash`."""
    root = str(tmp_path)
    answers.write("s1", "call-a", A, ("[no-review]",), root=root)
    old = time.time() - answers.FRESH - 5
    os.utime(tmp_path / "s1" / "call-a", (old, old))
    answers.write("s1", "call-b", B, (), root=root)
    assert not (tmp_path / "s1" / "call-a").exists()


def test_a_session_or_call_id_cannot_name_a_directory_outside(tmp_path):
    answers.write("../../escaped", "c", A, ("[no-review]",), root=str(tmp_path / "a"))
    answers.write("s1", "../../escaped", A, ("[no-review]",), root=str(tmp_path / "a"))
    assert not (tmp_path / "escaped").exists()
    assert answers.directory("..") == ""


@pytest.mark.parametrize("token", ["[shared-tree-ok]", "[worktree-ok]"])
def test_the_tree_answers_are_not_carried(tmp_path, token):
    """The switch and creation arms decide before git runs and read their own
    tokens from the command (option 1, P6), so nothing is written for them."""
    assert answers.write("s1", "c", A, (token,), root=str(tmp_path)) == []


def run(module, monkeypatch, payload):
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    module.main()


def test_the_gates_write_before_the_call_and_clear_after_it(monkeypatch, tmp_path):
    monkeypatch.setenv(answers.OVERRIDE, str(tmp_path))
    payload = {
        "tool_name": "Bash",
        "session_id": "s1",
        "tool_use_id": "toolu_a",
        "tool_input": {"command": A},
    }
    run(writer, monkeypatch, payload)
    assert answers.given("s1", "[no-review]", [shell(A)])
    run(clearer, monkeypatch, payload)
    assert not answers.given("s1", "[no-review]", [shell(A)])


def test_two_calls_carrying_tokens_at_once_keep_their_own(monkeypatch, tmp_path):
    monkeypatch.setenv(answers.OVERRIDE, str(tmp_path))
    c = ": '[no-parity]'; git commit -m c"
    for call, command in (("toolu_a", A), ("toolu_c", c)):
        run(
            writer,
            monkeypatch,
            {
                "tool_name": "Bash",
                "session_id": "s1",
                "tool_use_id": call,
                "tool_input": {"command": command},
            },
        )
    assert answers.given("s1", "[no-review]", [shell(A)])
    assert not answers.given("s1", "[no-review]", [shell(c)])
    assert answers.given("s1", "[no-parity]", [shell(c)])


def test_two_calls_are_kept_apart_by_id_and_by_command():
    assert answers.call_id("toolu_a", A) != answers.call_id("toolu_b", A)
    assert answers.call_id(None, A) != answers.call_id(None, B)
    assert answers.call_id(None, A) == answers.call_id("", A)


def test_a_payload_with_no_tool_use_id_is_keyed_by_its_command(monkeypatch, tmp_path):
    monkeypatch.setenv(answers.OVERRIDE, str(tmp_path))
    payload = {"tool_name": "Bash", "session_id": "s1", "tool_input": {"command": A}}
    run(writer, monkeypatch, payload)
    assert answers.given("s1", "[no-review]", [shell(A)])
    run(clearer, monkeypatch, payload)
    assert not answers.given("s1", "[no-review]", [shell(A)])


def test_the_writer_ignores_another_tool(monkeypatch, tmp_path):
    monkeypatch.setenv(answers.OVERRIDE, str(tmp_path))
    run(
        writer,
        monkeypatch,
        {
            "tool_name": "Write",
            "session_id": "s1",
            "tool_input": {"command": "[no-review]"},
        },
    )
    assert not answers.given("s1", "[no-review]", ["[no-review]"])


def test_the_store_lives_under_the_plugins_own_directory(monkeypatch):
    monkeypatch.delenv(answers.OVERRIDE, raising=False)
    assert answers.root_dir() == os.path.join(
        os.path.expanduser("~"), ".claude", "specseal", "answers"
    )
