"""The gate names a way past itself, and that way has to actually run.

For three releases the prompt said to re-issue the command "with `[no-review]`
as a BARE WORD". Following it produced:

    error: pathspec '[no-review]' did not match any file(s) known to git

After `git commit`, a bare word is a pathspec. The marker was being READ
correctly and TYPED somewhere git would never accept, so the gate stopped the
commit, the escape it offered failed, and approving the prompt was left as the
only thing that worked — which is the outcome the wording exists to avoid
(issue #50).

The issue proposed a trailing `# [no-review]` comment. Measured, that is not
the fix either: it commits under bash and under `zsh -c`, and fails in an
INTERACTIVE zsh, whose default leaves `#` uncommented and then refuses
`[no-review]` as an unmatched glob before git is reached. That last case is
not automated here — an interactive shell in CI sources a user's rc and needs
a tty — so it is recorded rather than run: `printf 'git commit -m x  #
[no-review]\\n' | zsh -i` gives `zsh: no matches found: [no-review]`.

What is run here is the form the gate now advises, in every non-interactive
shell available, against real git.
"""

import atexit
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
from conftest import (
    ATE_THE_PROBE,
    NOT_A_SHELL,
    decision_of,
    load_hook_module,
    run_hook,
    shell_probe,
)

gate = load_hook_module("commit-review-gate.py", "crg_waiver")


NAMED_SHELLS = ("sh", "bash", "zsh")
SHELL_PROBE = {s: shell_probe(s) for s in NAMED_SHELLS if shutil.which(s)}
SHELLS = [s for s, why in SHELL_PROBE.items() if why is None]
# Split by WHY the name dropped out, because the two need opposite treatment.
#
# A name that is not a shell at all has to be droppable: `windows-latest`
# resolves `bash` to the WSL launcher, and the probe exists to remove exactly
# that. Failing on it would fail the runner for doing what it was asked.
#
# A working shell that answered wrong is the silent shrink instead -- one
# `echo` in a developer's `.zshenv` and this file's cases stop running in
# `zsh` while still reporting a pass. `assert SHELLS` sees an empty list and
# not a shrunken one, so that case is asserted on separately below.
UNUSABLE_SHELLS = {
    s: w for s, w in SHELL_PROBE.items() if w and w.endswith(NOT_A_SHELL)
}
POLLUTED_SHELLS = {
    s: w for s, w in SHELL_PROBE.items() if w and w.endswith(ATE_THE_PROBE)
}


_WAIVER_REPO_TEMPLATE = None


def _waiver_repo_template():
    """A repo with one commit and a staged change, built once per process."""
    global _WAIVER_REPO_TEMPLATE
    if _WAIVER_REPO_TEMPLATE is None:
        d = Path(tempfile.mkdtemp(prefix="specseal-waiver-repo-template-")) / "repo"
        subprocess.run(["git", "init", "-q", str(d)], check=True)

        def g(*a):
            subprocess.run(["git", "-C", str(d), *a], check=True, capture_output=True)

        (d / "f.py").write_text("x = 1\n")
        g("add", "-A")
        g(
            "-c",
            "user.email=e@example.com",
            "-c",
            "user.name=e",
            "commit",
            "-qm",
            "base",
        )
        (d / "f.py").write_text("x = 2\n")
        g("add", "-A")
        atexit.register(shutil.rmtree, d, True)
        _WAIVER_REPO_TEMPLATE = d
    return _WAIVER_REPO_TEMPLATE


def opted_in_repo(tmp_path):
    """A repo the gate fires in, with a staged change ready to commit."""
    d = tmp_path / "repo"
    shutil.copytree(_waiver_repo_template(), d)
    (d / "seal").mkdir()
    return d


def payload(cmd, repo):
    return {
        "tool_name": "Bash",
        "session_id": "s1",
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }


@pytest.mark.parametrize(
    "command",
    [
        ": '[no-review]'; git commit -m x",
        "git commit -m x  # [no-review]",
        "git commit -m x  # don't [no-review]",
        "git commit -m x  # it's [no-review], deliberately",
    ],
)
def test_an_apostrophe_beside_the_marker_does_not_silence_the_waiver(tmp_path, command):
    """Whether the command parses is measured on the command as WRITTEN.

    The judgment read drops comments, so a command carrying an apostrophe in
    one parses cleanly once the comment is gone. That answer used to be handed
    to the CONSENT read, which then ran its strict bare-word scan on the RAW
    command — where the same apostrophe opens a quote that never closes and
    swallows the marker. The waiver was honoured before the judgment read
    started dropping comments and refused after, with nothing to tell the user
    why.

    Two of these rows carry an apostrophe and two do not; all four are the
    author writing the marker on purpose.
    """
    repo = opted_in_repo(tmp_path)
    assert decision_of(run_hook("commit-review-gate.py", payload(command, repo))) == (
        "silent"
    ), command


def test_the_form_the_gate_advises_is_the_one_that_runs(tmp_path):
    """Both halves, executed: git accepts it and the gate reads the marker.

    Either half alone is the defect. A form git accepts but the gate cannot
    read stops the commit anyway; a form the gate reads but git rejects is
    what shipped.
    """
    assert SHELLS, f"no shell to test the advice in; unusable: {UNUSABLE_SHELLS}"
    assert not POLLUTED_SHELLS, (
        f"{POLLUTED_SHELLS} are working shells on PATH, so the advised form "
        "should have run in them and did not"
    )
    # The WSL launcher is a Windows fact, and the drop it earns is unconditional
    # only because `os.name` was never asked. On POSIX a name that resolves and
    # then refuses to run a command is a broken environment, not a runner doing
    # what it was told, and letting it drop in silence is half of the shrink
    # round 1's finding 10 named.
    if os.name != "nt":
        assert not UNUSABLE_SHELLS, (
            f"{UNUSABLE_SHELLS} are on PATH and would not run a command; the "
            "runner's WSL `bash` is a Windows-only reason to drop one"
        )
    for shell in SHELLS:
        repo = opted_in_repo(tmp_path / shell)
        cmd = ": '[no-review]'; git commit -m x"
        assert decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == (
            "silent"
        ), f"{shell}: the gate did not read the marker"
        r = subprocess.run(
            # Quoted, because this string is about to be a real shell
            # command: an unquoted native path loses its separators to the
            # shell before `cd` ever sees it, and the test then measured
            # whether `cd` can reach a directory that does not exist.
            [shell, "-c", f"cd {shlex.quote(str(repo))} && {cmd}"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            env={
                **os.environ,
                "GIT_AUTHOR_NAME": "e",
                "GIT_AUTHOR_EMAIL": "e@e.example",
                "GIT_COMMITTER_NAME": "e",
                "GIT_COMMITTER_EMAIL": "e@e.example",
            },
        )
        assert r.returncode == 0, f"{shell}: git rejected the advised form\n{r.stderr}"


@pytest.mark.parametrize(
    "cmd",
    ["git commit -m x [no-review]", "git commit -m x '[no-review]'"],
)
def test_the_form_that_was_advised_is_rejected_by_git(tmp_path, cmd):
    """The defect itself, pinned. The gate reads it; git will not take it."""
    assert SHELLS, f"no shell to run the rejected form in; unusable: {UNUSABLE_SHELLS}"
    repo = opted_in_repo(tmp_path / "broken")
    assert decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == (
        "silent"
    ), "the marker is read — reading was never the problem"
    r = subprocess.run(
        # The first shell that answered the probe, not the name `bash`:
        # on a `windows-latest` runner that name is the WSL launcher.
        [SHELLS[0], "-c", f"cd {shlex.quote(str(repo))} && {cmd}"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert r.returncode != 0
    assert "pathspec" in r.stderr, r.stderr


def test_every_prompt_shows_the_runnable_form(tmp_path):
    """A prompt that names a marker has to show where it goes.

    All three arms are checked — review, parity, and the unresolved target —
    because the sentence was copied between them and a fix to one leaves the
    others saying the thing that fails.
    """
    repo = opted_in_repo(tmp_path / "prompts")
    (repo / "seal" / "parity.md").write_text("| Original repo | org/legacy |\n")
    seen = []
    for cmd, session in (
        ("git commit -m x", "s1"),  # deny: both arms, question form
        ("git commit -m x", "s1"),  # ask: both arms, plain form
        ('git -C "$WT" commit -m x', "s2"),  # the unresolved target
    ):
        out = run_hook(
            "commit-review-gate.py", payload(cmd, repo) | {"session_id": session}
        )
        seen.append(json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"])
    for reason in seen:
        assert ": '[no-" in reason, f"no runnable form in:\n{reason}"
        assert "as a BARE WORD" not in reason, (
            "the prompt still tells the user to type a pathspec"
        )
        # The SHAPE of every form a prompt prints, not just that one is
        # present. `": '[no-" in reason` is a prefix test, and it passes a
        # prompt advising `git commit … : '[no-review]'` -- the pathspec form
        # git rejects, which is the whole defect this file exists for.
        # Measured: that mutation passed the entire suite. The guard that used
        # to catch it was the cross-release text pin in
        # `test_the_same_root_forms_answer_what_the_release_did`, and that pin
        # was deliberately narrowed to the STATE half, so the option BODIES --
        # where these forms live -- had nothing looking at them.
        for form in re.findall(r"`([^`]*\[no-[a-z]+\][^`]*)`", reason):
            assert re.match(r"^: (?:'\[no-[a-z]+\] ?'|'\[no-[a-z]+\]' ?)+; ", form), (
                f"a form git rejects reached a prompt: {form!r}"
            )


def test_the_helper_keeps_the_marker_out_of_the_git_command():
    """What makes the form work: the marker is never an argument to git."""
    form = gate.waiver_form(["[no-review]", "[no-parity]"])
    assert form.startswith(": '[no-review]' '[no-parity]';")
    assert form.index("[no-review]") < form.index(";"), (
        "a marker after the separator is an argument to whatever follows"
    )
