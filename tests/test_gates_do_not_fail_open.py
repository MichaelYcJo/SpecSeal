"""The reading direction: a reader that cannot decode must not answer "nothing".

`tests/test_console_is_not_utf8.py` holds the writing direction — a gate that
raises while printing dies with empty stdout. This file holds the other one,
which is quieter and worse.

`subprocess.run(..., text=True)` decodes a child's output with whatever
locale the parent had. git speaks UTF-8 on every platform. When the decode fails, the
exception is raised on subprocess's **reader thread and does not propagate**:
the call returns normally with `stdout` set to `None`. Nothing crashes. The
guard reads no other session and reports a single stream; the gate resolves no
repository and stays silent; the check finds no round record and exits 0.

Every one of those is an allow, produced by a reader that was never told what
encoding its input is in. `hooks/worktree-guard.py` names this direction itself
as the one to avoid.

Platform-independent by construction: the `None` state is produced directly,
because that is the state the reader thread leaves behind, and reproducing the
thread death would need a locale the test cannot set portably.
"""

import importlib.util
import os
import subprocess

import pytest

ROOT = os.path.join(os.path.dirname(__file__), "..")
KOREAN = "한글"


def load(relative, name):
    path = os.path.join(ROOT, *relative.split("/"))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


optin = load("hooks/optin.py", "specseal_optin_failopen")


def git_repo(where):
    where.mkdir(parents=True, exist_ok=True)
    for args in (
        ["init", "-q"],
        ["config", "user.email", "t@t.example"],
        ["config", "user.name", "t"],
    ):
        subprocess.run(
            ["git", "-C", str(where), *args], check=True, capture_output=True
        )
    (where / "f.txt").write_text("one\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(where), "add", "-A"], check=True, capture_output=True
    )
    subprocess.run(
        ["git", "-C", str(where), "commit", "-qm", "base"],
        check=True,
        capture_output=True,
    )
    return where


def test_a_reader_that_decoded_nothing_answers_empty_rather_than_raising(monkeypatch):
    """The `None` stdout, produced directly.

    This is what the dead reader thread leaves behind, and it is the state that
    made `optin.repo_root` raise `AttributeError` out of the commit gate — a
    PreToolUse hook exiting non-zero is a non-blocking error, so the command it
    was judging went through unjudged.

    The module's own docstring states the direction: everything here fails
    toward "not opted in", and that is `""`, not an exception.
    """

    def decoded_nothing(*args, **kwargs):
        return subprocess.CompletedProcess(args, 0, stdout=None, stderr=None)

    monkeypatch.setattr(optin.subprocess, "run", decoded_nothing)
    assert optin.repo_root(str(ROOT)) == ""
    assert optin.opted_in(str(ROOT)) is False
    assert optin.parity_config(str(ROOT)) == ""


def test_a_repository_whose_path_the_locale_cannot_carry_still_resolves(tmp_path):
    """The encoding half, asked of the answer rather than of the source.

    Under `text=True` this returns one of two wrong things depending on the
    ambient codepage: nothing at all where the decode fails outright (cp949,
    and the reader-thread death above), or a plausible-looking path that does
    not exist where the codepage decodes every byte to something (cp1252 turns
    the UTF-8 bytes of Korean into Latin-1 letters, and `opted_in` then answers
    False about a repository that is opted in).

    Asserting that the answer names a directory that EXISTS catches both, and
    on a UTF-8 locale it is a no-op — the same shape as every other
    substitution in this work item.
    """
    repo = git_repo(tmp_path / KOREAN / "repo")
    (repo / ".specseal").mkdir()
    got = optin.repo_root(str(repo))
    assert got, "the root came back empty for a repository that is right there"
    assert os.path.isdir(got), f"resolved to a directory that does not exist: {got!r}"
    assert os.path.normpath(got) == os.path.normpath(str(repo))
    assert optin.opted_in(str(repo)) is True


def test_the_process_probe_survives_output_it_cannot_decode(monkeypatch):
    """`tasklist` is the only process probe Windows has — there is no `ps` and
    no `/proc` — and it answers in the OEM codepage, so it is the one reader in
    this tree whose source is not UTF-8.

    Under `text=True` its reader thread died and `r.stdout` came back `None`,
    which `.splitlines()` then hit OUTSIDE the `try`. The guard's session
    detection went blind on exactly the consoles most likely to be non-UTF-8,
    and blind means `reliable` is False, which means every branch switch
    reaches the cannot-tell arm.
    """
    guard = load("hooks/worktree-guard.py", "specseal_guard_failopen")
    if not hasattr(guard, "lease_owner_alive"):
        pytest.skip("the probe moved; this case names it by function")

    def decoded_nothing(*args, **kwargs):
        return subprocess.CompletedProcess(args, 0, stdout=None, stderr=None)

    monkeypatch.setattr(guard.subprocess, "run", decoded_nothing)
    monkeypatch.setattr(guard.sys, "platform", "win32")
    # False — "this pid is not running" — and not a traceback. Answering the
    # question wrongly is a separate matter from failing to answer it at all,
    # and only the second one takes the caller down with it.
    assert guard.lease_owner_alive(1) is False
