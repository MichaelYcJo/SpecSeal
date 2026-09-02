"""Whatever the reader ANSWERS about a name, bash answers the same.

The name environment in `hooks/cmdline.py` has one failure mode: answering
confidently with a path the shell is not in. A prompt is never that failure,
so a prompt is exempt here. What is not exempt is any input the reader
resolves to a directory: for every one of those, bash must leave `$SB` at the
same value.

Round 1 of the re-application found two body shapes an integer body count let
through -- a multi-line `case` arm pattern `a )` and the glued `f(){` -- and
both escaped a 1,790-input differential run because every wrapper in it was
one line long and the run lived in a session scratchpad. This is that run,
in the tree, with the multi-line wrappers, guarded the way
`tests/test_evidence_check.py::usable_bash` guards its own bash spawns, and
run against a single bash process so it costs one fork rather than one per
input.
"""

import itertools
import os
import re
import shlex
import subprocess

import pytest
from conftest import load_hook_module

reader = load_hook_module("cmdline.py", "cmdline_oracle")


def usable_bash():
    """Whether `bash` here actually executes what it is handed.

    On Windows, `bash` on PATH can resolve to the WSL stub in System32, which
    fails every command with its own exit code no matter what was asked. The
    real run happens on the ubuntu leg of CI.
    """
    try:
        r = subprocess.run(["bash", "-c", "exit 7"], capture_output=True, timeout=30)
    except OSError:
        return False
    return r.returncode == 7


# Compound-command shapes around one statement. The multi-line ones are the
# reason this file exists.
WRAPPERS = [
    "{c}",
    "if {c}; then :; fi",
    "if false; then {c}; fi",
    "if true; then :; else {c}; fi",
    "if false; then :; elif false; then {c}; fi",
    "if false; then if true; then :; fi; {c}; fi",
    "while false; do {c}; done",
    "for i in; do {c}; done",
    "case x in y) {c} ;; esac",
    "case x in x) {c} ;; esac",
    "case x in\ny )\n{c} ;;\nesac",
    "case x in\n(y)\n{c} ;;\nesac",
    "case x in\ny)\n{c};;\nesac",
    "case x in\nx )\n{c} ;;\nesac",
    "{{ {c}; }}",
    "( {c} )",
    "f() {{ {c}; }}",
    "f(){{\n{c}\n}}",
    "f() {{ {c}; }}; f",
    "function f {{ {c}; }}; f",
    "time {{ {c}; }}",
    "! {c}",
    "true && {c}",
    "false || {c}",
    "{c} | cat",
]

# What goes inside. Each is a statement the reader either binds, forgets, or
# refuses; several are followed by a second statement, because a body's
# SECOND statement is the one that used to bind as top level.
STATEMENTS = [
    "true",
    "echo hi",
    "echo fi",
    'echo ")"',
    "echo '('",
    "[ -d /nope ]",
    "read -r OT",
    "SB=/two",
    "SB=/two; SB=/three",
    "echo hi; SB=/three",
    "OT=/x; SB=/three",
    "export SB=/three",
    "SB+=/x",
    "SB=(/three)",
    "unset SB",
    "((SB=3))",
    'let "SB = 3"',
    ': "${SB:=/three}"',
    'echo "${SB:-/three}"',
    'eval "SB=/two"',
    "for SB in /two /three; do :; done",
    "for OT in a b; do :; done",
    "pushd /",
    "cd /two",
    "myfunc",
    "grep -c '(' /dev/null",
    'git log --oneline -1 -- "(x)"',
]


def answers(command):
    """The directories the reader says the commit lands in, or None."""
    text = reader.drop_heredoc_bodies(reader.drop_comments(command))
    items, clean = reader.split_segments_with_separators(text)
    if not clean:
        return None
    out = []
    for tokens, wheres in reader.walk_directories(items, "/session"):
        parsed = reader.parse_git(tokens)
        if parsed and parsed[0] == "commit":
            out.extend(str(reader.compose(w, list(parsed[2]))) for w in wheres)
    return out


def bash_answers(middles):
    """`{middle: value of $SB}` after `SB=/one; <middle>`, from ONE bash.

    Each input runs under `eval` in a subshell, so a syntax error in one is a
    runtime error there and not a parse error for the whole script. A marker
    line follows each; the value is the last line before the next marker, and
    an input whose subshell never reached its `printf` (an `exec`) has none.
    """
    script = []
    for at, middle in enumerate(middles):
        quoted = shlex.quote(f"SB=/one; {middle}")
        script.append(f'( eval {quoted}; printf "\\n%s" "$SB" ) </dev/null 2>/dev/null')
        script.append(f'printf "\\n@@{at}\\n"')
    r = subprocess.run(
        ["bash", "-c", "\n".join(script)],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    parts = re.split(r"\n@@(\d+)\n", r.stdout)
    out = {}
    # `re.split` with a group returns segment, marker, …, and a tail after the
    # last marker; the tail is nobody's segment.
    for segment, index in zip(parts[0:-1:2], parts[1::2], strict=True):
        middle = middles[int(index)]
        out[middle] = segment.split("\n")[-1] if segment else None
    return out


INPUTS = list(
    dict.fromkeys(w.format(c=c) for w, c in itertools.product(WRAPPERS, STATEMENTS))
)


@pytest.mark.skipif(
    not usable_bash(), reason="bash here does not execute what it is handed"
)
def test_whatever_the_reader_answers_bash_answers_too():
    oracle = bash_answers(INPUTS)
    resolved, disagreed = 0, []
    for middle in INPUTS:
        got = answers(f'SB=/one; {middle}; git -C "$SB" commit -m x')
        if got is None or any("$" in g for g in got):
            continue  # a prompt is never the failure this file is about
        want = oracle.get(middle)
        if want is None:
            continue  # the subshell never reached its printf -- no oracle
        resolved += 1
        if set(got) != {os.path.normpath(want)}:
            disagreed.append((middle, got, want))
    assert not disagreed, (
        f"{len(disagreed)} of {len(INPUTS)} inputs answered where bash disagrees:\n"
        + "\n".join(f"  {m!r}: reader {g} · bash {w!r}" for m, g, w in disagreed)
    )
    # A reader that prompts on everything passes the loop above vacuously, so
    # the corpus has to resolve a real share of itself for this to mean much.
    assert resolved > len(INPUTS) // 4, f"only {resolved} of {len(INPUTS)} resolved"


def test_the_corpus_carries_the_shapes_round_one_found():
    """The wrappers this file exists for are in it -- a regression net that
    lost its multi-line `case` would pass exactly as the one-line run did."""
    joined = "\n".join(WRAPPERS)
    for shape in ("\ny )\n", "\n(y)\n", "f(){", "elif", "then if"):
        assert shape in joined, f"the corpus lost {shape!r}"
