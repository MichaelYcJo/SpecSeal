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


def test_an_answer_is_given_until_the_next_call_replaces_it(tmp_path):
    answers.write("s1", ("[no-review]",), root=str(tmp_path))
    assert answers.given("s1", "[no-review]", root=str(tmp_path))
    assert not answers.given("s1", "[no-parity]", root=str(tmp_path))
    assert not answers.given("s2", "[no-review]", root=str(tmp_path))
    answers.write("s1", (), root=str(tmp_path))
    assert not answers.given("s1", "[no-review]", root=str(tmp_path))


def test_an_answer_older_than_a_bash_call_can_run_is_not_given(tmp_path):
    answers.write("s1", ("[no-review]",), root=str(tmp_path))
    path = tmp_path / "s1" / "no-review"
    old = time.time() - answers.FRESH - 5
    os.utime(path, (old, old))
    assert not answers.given("s1", "[no-review]", root=str(tmp_path))


def test_a_session_id_cannot_name_a_directory_outside(tmp_path):
    answers.write("../../escaped", ("[no-review]",), root=str(tmp_path / "a"))
    assert not (tmp_path / "escaped").exists()
    assert answers.directory("..") == ""


@pytest.mark.parametrize("token", ["[shared-tree-ok]", "[worktree-ok]"])
def test_the_tree_answers_are_not_carried(tmp_path, token):
    """The switch and creation arms decide before git runs and read their own
    tokens from the command (option 1, P6), so nothing is written for them."""
    assert answers.write("s1", (token,), root=str(tmp_path)) == []


def run(module, monkeypatch, payload):
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    module.main()


def test_the_gates_write_before_the_call_and_clear_after_it(monkeypatch, tmp_path):
    monkeypatch.setenv(answers.OVERRIDE, str(tmp_path))
    payload = {
        "tool_name": "Bash",
        "session_id": "s1",
        "tool_input": {"command": ": '[no-review]'; git commit -m x"},
    }
    run(writer, monkeypatch, payload)
    assert answers.given("s1", "[no-review]")
    run(clearer, monkeypatch, payload)
    assert not answers.given("s1", "[no-review]")


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
    assert not answers.given("s1", "[no-review]")


def test_the_store_lives_under_the_plugins_own_directory(monkeypatch):
    monkeypatch.delenv(answers.OVERRIDE, raising=False)
    assert answers.root_dir() == os.path.join(
        os.path.expanduser("~"), ".claude", "specseal", "answers"
    )
