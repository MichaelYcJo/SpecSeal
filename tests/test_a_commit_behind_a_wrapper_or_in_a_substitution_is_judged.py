"""A commit behind a wrapper that runs its arguments, or inside a command
substitution, is a commit (#670).

Found while building phase 4 of work item `1790644505` and confirmed by the
orchestrator at `3911a8cf`: `exec`, `timeout`, `nice` and `xargs` in front of
`git commit`, and `$( … )` or backticks around one, each reached the commit
gate as no commit at all, while `env git commit` was judged. The reader knew
five wrappers by name and stopped at the first word it did not know, and it
never looked inside a substitution.

Three readings are added, all in the stricter direction:

- **A wrapper that runs its operands as a command** is read past to the word
  it runs (`cmdline.RUNNERS`, enumerated in `phases/phase-5.md`). Directly
  followed by `git`, the commit is judged where the shell is, as `env git
  commit` always was; behind the wrapper's own options or operands, which this
  reader does not parse, the first `git` word stands in for the command word
  and the directory is unresolved.
- **A command that hands a string to a shell** -- `sh -c`, `bash -c`, `su
  -c`, `script -c`, `env -S`, `watch '…'` -- has that string read as a
  command, the way `eval`'s argument already was.
- **A command substitution** -- `$( … )`, backticks, `<( … )`, `>( … )` -- has
  its body read as a command. A commit there runs in a subshell the walk does
  not place, so it is a stop wherever the session's own repository opted in.
"""

import io
import json
import os
import sys

import pytest
from conftest import load_hook_module
from test_no_shape_the_base_stops_reads_silent import make_repo

gate = load_hook_module("commit-review-gate.py", "crg_wrappers")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hooks"))
import cmdline  # noqa: E402  -- the plain name both gates import

C = "git commit -m x"
HERE, UNRESOLVED = "here", "unresolved"

# #670's four wrappers and the rest of the enumeration, each in the shape it
# is used in: directly in front of `git` it keeps the directory, behind its
# own operand or option it does not.
WRAPPED = {
    "exec": (f"exec {C}", HERE),
    "nice": (f"nice {C}", HERE),
    "nice -n": (f"nice -n 5 {C}", UNRESOLVED),
    "timeout": (f"timeout 5 {C}", UNRESOLVED),
    "xargs": (f"echo a | xargs {C}", HERE),
    "xargs -I": (f"echo a | xargs -I{{}} {C}", UNRESOLVED),
    "stdbuf": (f"stdbuf -oL {C}", UNRESOLVED),
    "setsid": (f"setsid {C}", HERE),
    "ionice": (f"ionice -c 3 {C}", UNRESOLVED),
    "taskset": (f"taskset 1 {C}", UNRESOLVED),
    "chrt": (f"chrt -i 0 {C}", UNRESOLVED),
    "flock": (f"flock /tmp/l {C}", UNRESOLVED),
    "chroot": (f"chroot / {C}", UNRESOLVED),
    "unshare": (f"unshare -r {C}", UNRESOLVED),
    "nsenter": (f"nsenter -t 1 {C}", UNRESOLVED),
    "prlimit": (f"prlimit --nofile=10 {C}", UNRESOLVED),
    "setpriv": (f"setpriv --reuid=1 {C}", UNRESOLVED),
    "runuser": (f"runuser -u u -- {C}", UNRESOLVED),
    "doas": (f"doas {C}", HERE),
    "pkexec": (f"pkexec {C}", HERE),
    "caffeinate": (f"caffeinate -i {C}", UNRESOLVED),
    "arch": (f"arch -arm64 {C}", UNRESOLVED),
    "strace": (f"strace -f {C}", UNRESOLVED),
    "ltrace": (f"ltrace {C}", HERE),
    "valgrind": (f"valgrind {C}", HERE),
    "gtimeout": (f"gtimeout 5 {C}", UNRESOLVED),
    "gnice": (f"gnice {C}", HERE),
    "gnohup": (f"gnohup {C}", HERE),
    "gstdbuf": (f"gstdbuf -oL {C}", UNRESOLVED),
    "genv": (f"genv -i {C}", UNRESOLVED),
    "gchroot": (f"gchroot / {C}", UNRESOLVED),
    "runcon": (f"runcon -t t {C}", UNRESOLVED),
    "find -exec": (f"find . -name f -exec {C} {{}} +", UNRESOLVED),
    "parallel": (f"parallel {C} ::: a", HERE),
    "watch -n": (f"watch -n 5 {C}", UNRESOLVED),
    "script, argv form": (f"script /dev/null {C}", UNRESOLVED),
    # The five the base already named, behind an option it stopped at.
    "env -i": (f"env -i {C}", UNRESOLVED),
    "sudo -u": (f"sudo -u a {C}", UNRESOLVED),
    "command -p": (f"command -p {C}", UNRESOLVED),
}

# A string handed to a shell to parse. Its directory is unresolved, as
# `eval`'s already was.
HANDED = {
    "bash -c": f"bash -c '{C}'",
    "sh -c": f'sh -c "{C}"',
    "zsh -c": f"zsh -c '{C}'",
    "dash -c": f"dash -c '{C}'",
    "bash -ec": f"bash -ec '{C}'",
    "bash -o errexit -c": f"bash -o errexit -c '{C}'",
    "sudo sh -c": f"sudo sh -c '{C}'",
    "xargs sh -c": f"echo a | xargs -I{{}} sh -c '{C}'",
    "su -c": f"su - u -c '{C}'",
    "su --command=": f"su --command='{C}' u",
    "script -c": f"script -q -c '{C}' /dev/null",
    "env -S": f"env -S '{C}'",
    "watch, one string": f"watch '{C}'",
    "env -S glued": f"env -S'{C}'",
    "env --split-string=": f"env --split-string='{C}'",
    "a command word the shell expands": 'sh -c "$CMD"',
    "a command in the string behind a list opener": f"bash -c 'if true; then {C}; fi'",
}

SUBSTITUTED = {
    "$( )": f"echo $({C})",
    "$( ) in double quotes": f'echo "$({C})"',
    "backticks": f"echo `{C}`",
    "an assignment's value": f"x=$({C}; echo) && ls",
    "<( )": f"cat <({C})",
    ">( )": f"echo a > >({C})",
    "nested": f"echo $(echo $({C}))",
    "a case inside": f"echo $(case x in a) {C};; esac)",
    "inside ${ }": f"echo ${{x:-$({C})}}",
    "inside an arithmetic expansion": f"echo $(( $({C}) ))",
    "inside a heredoc body a shell runs": f"bash <<'EOF'\necho $({C})\nEOF",
    "an unterminated one": f"echo $({C}",
    "a shell string inside a substitution": f"echo $(bash -c '{C}')",
    # #674, phase 1: a host glued to a subshell's `(`, and a commit behind a
    # redirection inside a substitution.
    "(sh -c)": f"(sh -c '{C}')",
    "(bash -c) after a list": f"true; (bash -c '{C}')",
    "a redirected commit in $( )": f"echo $(2>/dev/null {C})",
}


def found(command, cwd):
    return gate.commit_invocations(command, str(cwd))[0]


@pytest.mark.parametrize("name", sorted(WRAPPED))
def test_a_wrapped_commit_is_read(name, tmp_path):
    """Seen red at `768377bf`, where each returned nothing."""
    command, where = WRAPPED[name]
    invocations = found(command, tmp_path)
    assert invocations, f"{name}: no commit read in {command!r}"
    for inv in invocations:
        unresolved = isinstance(inv.base, cmdline.Unresolved)
        assert unresolved == (where == UNRESOLVED), (name, inv.base)


@pytest.mark.parametrize("name", sorted({**HANDED, **SUBSTITUTED}))
def test_a_commit_in_a_string_or_a_substitution_is_read_as_unreadable(name, tmp_path):
    """Seen red at `768377bf`, where each returned nothing."""
    command = {**HANDED, **SUBSTITUTED}[name]
    invocations = found(command, tmp_path)
    assert invocations, f"{name}: no commit read in {command!r}"
    assert any(isinstance(inv.base, cmdline.Unresolved) for inv in invocations), name


def test_every_enumerated_wrapper_has_a_shape():
    """The enumeration is the set, and every member of it is exercised here.
    A wrapper added to `RUNNERS` with no shape is a reading nothing pins."""
    named = {name.split()[0].rstrip(",") for name in WRAPPED}
    missing = sorted(set(cmdline.RUNNERS) - named - set(cmdline.WRAPPERS) - {"time"})
    assert not missing, missing


# What must NOT become a stop: each is either nothing at all or exactly the
# commit it always was, judged where it always was.
CONTROLS = {
    "a single-quoted substitution is text": "echo '$(git commit -m x)'",
    "a message read by a substitution": 'git commit -m "$(cat msg)"',
    "a value read before the commit": "x=$(git rev-parse HEAD) && git commit -m y",
    "a script a shell runs is not its arguments": 'bash run.sh "$x"',
    "a wrapper around no git": "timeout 5 make",
    "arithmetic": "echo $((1+2)) && git commit -m y",
    "a word after for": "for d in git commit; do :; done",
    "a conditional in a shell string": "bash -c '[ -f x ] && echo y'",
    "a group in a shell string": "bash -c '{ echo y; }'",
    # Round 1 of 1790644505, yellow 3: positional parameters no shell runs,
    # and `watch` as a word something else was handed.
    "find -exec sh -c with _ {}": "find . -name '*.py' -exec sh -c 'wc -l \"$1\"' _ {} \\;",
    "find -exec bash -c with bash {} +": "find . -type f -exec bash -c 'echo \"$@\"' bash {} +",
    "bash -c over a glob": 'bash -c \'for f in "$@"; do echo "$f"; done\' _ *.txt',
    "bash -c with an expanded $0": 'bash -c \'echo "$0"\' "$HOME"',
    "grep for watch": "grep -n watch *.py",
    "grep for watch in a substitution's list": "grep -l watch $(git ls-files)",
    "rg for watch": 'rg watch "$DIR"',
    # #674: `watch` as the file a redirection writes to is no program.
    "watch as a redirection's target": '2> watch -g "$CMD"',
    # #674, phase 2: a runner's options inside a string, with nothing after
    # them that expands.
    "a runner's options in a shell string": "sh -c 'nice -n 5 make all'",
    # A `case` word and a `for` list are data, never a program.
    "a case word that expands, in a string": "sh -c 'case $1 in a) echo;; esac' _ a",
    "a case word that expands, before a|b)": "sh -c 'case $1 in a|b) echo;; esac' _ a",
    "a for list that expands, in a string": "sh -c 'for f in $@; do echo; done' _ a",
}

# #674: round 1's seven controls, rewritten into each position the work item
# teaches the reader. A program word is read by where it stands, never by
# whether it is present, so a search word and a positional parameter stay what
# they were wherever the command itself is moved to (`spec.md` §*How the
# controls stay unasked*). Each is silent at `86256492` and must stay so.
ROUND_1_CONTROLS = (
    "find -exec sh -c with _ {}",
    "find -exec bash -c with bash {} +",
    "bash -c over a glob",
    "bash -c with an expanded $0",
    "grep for watch",
    "grep for watch in a substitution's list",
    "rg for watch",
)
POSITIONS = {
    "P5, behind 2>/dev/null": lambda c: f"2>/dev/null {c}",
    "P5, behind a spaced 2> target": lambda c: f"2> /dev/null {c}",
    "P10, glued to (": lambda c: f"({c})",
    "P7, a case arm": lambda c: f"case a in a) {c};; esac",
    "P7, a later arm": lambda c: f"case a in b) :;; a) {c};; esac",
    "P7, a spaced pattern": lambda c: f"case a in a ) {c};; esac",
    "P8, a function body": lambda c: f"f() {{ {c}; }}; f",
    "P8, a glued subshell body": lambda c: f"f() ({c}); f",
    "P8, function f": lambda c: f"function f {{ {c}; }}; f",
    "P9, a coprocess": lambda c: f"coproc {c}",
}
CONTROLS.update(
    {
        f"{name} [{position}]": rewrite(CONTROLS[name])
        for name in ROUND_1_CONTROLS
        for position, rewrite in POSITIONS.items()
    }
)

# The same hosts, where the string they run IS an expansion or holds the
# commit: each must still stop (round 1 of 1790644505, yellow 3's fence).
STILL_HANDED = {
    "sh -c $CMD": 'sh -c "$CMD"',
    "bash -o errexit -c $CMD": 'bash -o errexit -c "$CMD"',
    "su -c $CMD root": 'su -c "$CMD" root',
    "su root -c $CMD": 'su root -c "$CMD"',
    "su --command=$CMD": 'su --command="$CMD" root',
    "watch -n 1 $CMD": 'watch -n 1 "$CMD"',
    "env -S $CMD": 'env -S "$CMD"',
    "sudo sh -c $CMD": 'sudo sh -c "$CMD"',
    "bash -lc $CMD": 'bash -lc "$CMD"',
    "positional parameters that are the commit": "bash -c '\"$@\"' _ git commit -m x",
    # Round 2 of 1790644505: a word before the `-c` flag, and `watch` behind
    # a runner's own options, a list opener or a subshell, used to hide the
    # string.
    "bash --rcfile f -c $CMD": 'bash --rcfile /dev/null -c "$CMD"',
    "bash --init-file f -c $CMD": 'bash --init-file /dev/null -c "$CMD"',
    "bash 2>/dev/null -c $CMD": 'bash 2>/dev/null -c "$CMD"',
    "nice -n 5 watch $CMD": 'nice -n 5 watch -g "$CMD"',
    "timeout 60 watch $CMD": 'timeout 60 watch -g "$CMD"',
    "sudo -E watch $CMD": 'sudo -E watch "$CMD"',
    "then watch $CMD": 'if true; then watch -g "$CMD"; fi',
    "( watch $CMD )": '( watch -g "$CMD" )',
    "! watch $CMD": '! watch -g "$CMD"',
    # #674, phase 1: a program word behind a redirection, and a host glued to
    # the `(` that opens a subshell. Each is silent at `86256492`.
    "2>/dev/null eval $X": '2>/dev/null eval "$X"',
    "2> /dev/null eval $X": '2> /dev/null eval "$X"',
    "2>/dev/null watch $CMD": '2>/dev/null watch -g "$CMD"',
    "2> /dev/null watch $CMD": '2> /dev/null watch -g "$CMD"',
    "<<<x watch $CMD": '<<<x watch -g "$CMD"',
    "sh -c with 2>/dev/null before $CMD": "sh -c '2>/dev/null $CMD'",
    "sh -c with 2> /dev/null before $CMD": "sh -c '2> /dev/null $CMD'",
    "(watch $CMD)": '(watch -g "$CMD")',
    "(sh -c $CMD)": '(sh -c "$CMD")',
    "(nice watch $CMD)": '(nice watch -g "$CMD")',
    # #674, phase 2: `watch` inside a compound command's header -- a `case`
    # arm, a function body, a coprocess -- and a string's command word in the
    # same places or behind a runner's own options. Each is silent at
    # `86256492`, where the program was looked for only at the segment's start.
    "a case arm watch $CMD": 'case a in a) watch -g "$CMD";; esac',
    "a case arm (a) watch $CMD": 'case a in (a) watch -g "$CMD";; esac',
    "a case arm a ) watch $CMD": 'case a in a ) watch -g "$CMD";; esac',
    "a later case arm watch $CMD": 'case a in b) :;; a) watch -g "$CMD";; esac',
    "a case arm a|b) watch $CMD": 'case a in a|b) watch -g "$CMD";; esac',
    "a case arm in a then watch $CMD": (
        'if true; then case a in a) watch -g "$CMD";; esac; fi'
    ),
    "a function body watch $CMD": 'f() { watch -g "$CMD"; }; f',
    "a spaced definition watch $CMD": 'f () { watch -g "$CMD"; }; f',
    "a glued definition watch $CMD": 'f(){ watch -g "$CMD"; }; f',
    "function f watch $CMD": 'function f { watch -g "$CMD"; }; f',
    "function f() watch $CMD": 'function f() { watch -g "$CMD"; }; f',
    "function f () watch $CMD": 'function f () { watch -g "$CMD"; }; f',
    "a subshell body watch $CMD": 'f() ( watch -g "$CMD" ); f',
    "a case in a subshell watch $CMD": '(case a in a) watch -g "$CMD";; esac)',
    "coproc watch $CMD": 'coproc watch -g "$CMD"',
    "coproc NAME { watch $CMD }": 'coproc W { watch -g "$CMD"; }',
    "coproc { watch $CMD }": 'coproc { watch -g "$CMD"; }',
    "sh -c a function body $CMD": "sh -c 'f() { $CMD; }; f'",
    "sh -c a case arm $CMD": "sh -c 'case a in a) $CMD;; esac'",
    "sh -c function f $CMD": "sh -c 'function f { $CMD; }; f'",
    "sh -c coproc $CMD": "sh -c 'coproc $CMD'",
    "sh -c nice -n 5 $CMD": "sh -c 'nice -n 5 $CMD'",
    "sh -c timeout 5 $CMD": "sh -c 'timeout 5 $CMD'",
    "bash -c sudo -u x $CMD": "bash -c 'sudo -u x \"$CMD\"'",
}

# #674, phase 1: a commit behind a redirection written in front of `git`, or
# between `git` and its subcommand. A redirection moves no shell, so each
# commit is judged where the shell is, as the same commit without the
# redirection is. Each read as no commit at `86256492`.
REDIRECTED = {
    "2>/dev/null git": f"2>/dev/null {C}",
    "2> /dev/null git": f"2> /dev/null {C}",
    ">/dev/null git": f">/dev/null {C}",
    ">>log git": f">>log {C}",
    "<f git": f"</dev/null {C}",
    "<>f git": f"<>/dev/null {C}",
    "<<<x git": f"<<<x {C}",
    "<<< x git": f"<<< x {C}",
    "<<EOF git": f"<<EOF {C}\nbody\nEOF",
    "<< EOF git": f"<< EOF {C}\nbody\nEOF",
    "<<-EOF git": f"<<-EOF {C}\nbody\n\tEOF",
    "{fd}>f git": f"{{fd}}>/dev/null {C}",
    "zsh >!f git": f">!/dev/null {C}",
    "zsh >>!f git": f">>!/dev/null {C}",
    # Glued, `>!f` also reads as `>` with the target `!f`; spaced, only the
    # operator's own spelling keeps `f` from being read as the program.
    "zsh >! f git": f">! /dev/null {C}",
    "zsh >>! f git": f">>! /dev/null {C}",
    "2> >(tee log) git": f"2> >(tee log) {C}",
    "an assignment, then 2>/dev/null git": f"X=1 2>/dev/null {C}",
    "2>/dev/null, then an assignment": f"2>/dev/null X=1 {C}",
    "git 2>/dev/null commit": "git 2>/dev/null commit -m x",
    "git 2> /dev/null commit": "git 2> /dev/null commit -m x",
    "git -c k=v 2>/dev/null commit": "git -c k=v 2>/dev/null commit -m x",
}

# Behind a redirection AND somewhere else the walk does not place: the
# directory is unresolved for the other reason, as it was without the
# redirection.
REDIRECTED_UNPLACED = {
    "2>/dev/null nice -n 5 git": f"2>/dev/null nice -n 5 {C}",
    "then 2>/dev/null git": f"if true; then 2>/dev/null {C}; fi",
}


@pytest.mark.parametrize("name", sorted(REDIRECTED))
def test_a_commit_behind_a_redirection_is_read_where_the_shell_is(name, tmp_path):
    """Seen red at `86256492`, where each returned nothing."""
    invocations = found(REDIRECTED[name], tmp_path)
    assert invocations, f"{name}: no commit read"
    for inv in invocations:
        assert not isinstance(inv.base, cmdline.Unresolved), (name, inv.base)


@pytest.mark.parametrize("name", sorted(REDIRECTED_UNPLACED))
def test_a_commit_behind_a_redirection_and_a_construct_is_unplaced(name, tmp_path):
    invocations = found(REDIRECTED_UNPLACED[name], tmp_path)
    assert invocations, f"{name}: no commit read"
    assert all(isinstance(inv.base, cmdline.Unresolved) for inv in invocations), name


@pytest.mark.parametrize("name", sorted({**REDIRECTED, **REDIRECTED_UNPLACED}))
def test_the_gate_stops_a_redirected_commit(monkeypatch, capsys, tmp_path, name):
    command = {**REDIRECTED, **REDIRECTED_UNPLACED}[name]
    repo = make_repo(tmp_path / "repo")
    assert say(monkeypatch, capsys, command, repo) == "deny", name


@pytest.mark.parametrize("name", ["2>/dev/null git", "git 2>/dev/null commit"])
def test_a_redirected_commit_in_a_declared_repository_is_silent(
    monkeypatch, capsys, tmp_path, name
):
    """The redirection is read past, not read as a construct: a declared
    repository answers the commit the way it answers `git commit` bare."""
    repo = make_repo(tmp_path / "repo", declared=True)
    assert say(monkeypatch, capsys, REDIRECTED[name], repo) == "silent", name


def test_a_redirection_whose_target_is_named_git_still_reads_as_git(tmp_path):
    """`spec.md` decision 1. `2>/x/git commit` reads as a git invocation at
    `86256492`, because the reader took the whole word's last component.
    Reading past every redirection would read it as none, so the base's answer
    is kept wherever it found one."""
    assert found("2>/x/git commit -m x", tmp_path)


# #674, `questions.md` Q3's header half: every header spelling, as the splitter
# hands it back, and the word `header_end` says the command starts at. A
# spelling read by position costs nothing; `UNPLACEABLE` is the stand-in, which
# is a stop. None is a segment that opens with no header at all.
U = "UNPLACEABLE"
HEADERS = {
    "case W in P)": (["case", "a", "in", "a)", "watch"], 4),
    "case W in (P)": (["case", "a", "in", "(a)", "watch"], 4),
    "case W in P )": (["case", "a", "in", "a", ")", "watch"], 5),
    "case W in P, the rest past a |": (["case", "a", "in", "a"], 4),
    "case W, in on the next line": (["case", "a"], 2),
    "in, then a pattern": (["in", "a)", "watch"], 2),
    "a later arm P)": (["b)", "watch"], 1),
    "a later arm P )": (["b", ")", "watch"], 2),
    "a case behind then": (["then", "case", "a", "in", "a)", "watch"], 5),
    "a case glued to (": (["(case", "a", "in", "a)", "watch"], 4),
    "f() {": (["f()", "{", "watch"], 2),
    "f() (": (["f()", "(", "watch"], 2),
    "f() (glued": (["f()", "(watch"], 1),
    "f(), body on the next line": (["f()"], 1),
    "f ()": (["f", "()", "{", "watch"], 3),
    "f(){": (["f(){", "watch"], 1),
    "function f {": (["function", "f", "{", "watch"], 3),
    "function f() {": (["function", "f()", "{", "watch"], 3),
    "function f () {": (["function", "f", "()", "{", "watch"], 4),
    "function f(){": (["function", "f(){", "watch"], 2),
    "function f, body on the next line": (["function", "f"], 2),
    "coproc CMD": (["coproc", "watch"], 1),
    "coproc {": (["coproc", "{", "watch"], 2),
    "coproc (glued": (["coproc", "(watch"], 1),
    "coproc NAME {": (["coproc", "W", "{", "watch"], 3),
    "a case with no in": (["case", "a", "b", "c)"], U),
    "a pattern with no )": (["case", "a", "in", "a", "b", "c"], U),
    "a definition with no body": (["f()", "watch"], U),
    "no header: a program": (["grep", "-n", "watch"], None),
    "no header: case as an argument": (["echo", "case", "a)"], None),
    "no header: a for list": (["for", "x", "in", "a"], None),
}


@pytest.mark.parametrize("name", sorted(HEADERS))
def test_header_end(name):
    tokens, want = HEADERS[name]
    want = cmdline.UNPLACEABLE if want == U else want
    assert cmdline.header_end(tokens) == want, name


def test_a_header_spelling_the_reader_cannot_place_falls_to_the_stand_in():
    """#674, `spec.md` §*Two stand-ins*. A header the positional reading does
    not recognise is read the way `86256492` read every header for `git`: any
    later `watch` counts as the program, and any later word that expands counts
    as the string's command word. A false one is a stop, never a silence."""
    tokens = ["case", "a", "b", "watch", "-g", "$CMD"]
    assert cmdline.header_end(tokens) == cmdline.UNPLACEABLE
    assert cmdline.command_strings(tokens) == ["$CMD"]
    assert cmdline.names_an_unknown_command("case a b echo $CMD")


def test_a_string_behind_a_runners_operand_stops_as_the_frame_chose(tmp_path):
    """`spec.md` (b). Behind a runner's own option or operand the reader cannot
    tell a value from the program, so a later word that expands counts, and a
    positional parameter handed to `wc` is such a word. The frame counted this
    as a cost rather than a defect (`plan.md` Alternatives F)."""
    command = "sh -c 'timeout 5 wc -l \"$1\"' _ f"
    assert found(command, tmp_path), command


def test_a_redirection_with_nothing_after_it_keeps_the_base_subcommand():
    """The same rule one scan over: `git 2>/dev/null` names no subcommand past
    the redirection, so the answer `86256492` gave is the one returned."""
    assert cmdline.parse_git(["git", "2>/dev/null"]) == ("2>/dev/null", [], [])
    assert cmdline.parse_git(["git", "2>/dev/null", "commit"]) == ("commit", [], [])


@pytest.mark.parametrize("name", sorted(STILL_HANDED))
def test_a_string_that_is_an_expansion_still_stops(monkeypatch, capsys, tmp_path, name):
    repo = make_repo(tmp_path / "repo", declared=True)
    assert say(monkeypatch, capsys, STILL_HANDED[name], repo) == "deny", name


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
    if not printed:
        return "silent"
    return json.loads(printed)["hookSpecificOutput"]["permissionDecision"]


ALL = {**{k: v[0] for k, v in WRAPPED.items()}, **HANDED, **SUBSTITUTED}


@pytest.mark.parametrize("name", sorted(ALL))
def test_the_gate_stops_it(monkeypatch, capsys, tmp_path, name):
    """Through `main()`, in an opted-in repository with no declaration."""
    repo = make_repo(tmp_path / "repo")
    assert say(monkeypatch, capsys, ALL[name], repo) == "deny", name


@pytest.mark.parametrize("name", sorted(CONTROLS))
def test_a_declared_repository_meets_no_new_stop(monkeypatch, capsys, tmp_path, name):
    """The ordinary shapes around a substitution or a wrapper cost nothing new:
    in a declared repository each is silent, as it was at `768377bf`."""
    repo = make_repo(tmp_path / "repo", declared=True)
    assert say(monkeypatch, capsys, CONTROLS[name], repo) == "silent", name


def test_the_controls_read_no_hidden_commit(tmp_path):
    for name, command in CONTROLS.items():
        hidden = [
            inv
            for inv in found(command, tmp_path)
            if isinstance(inv.base, cmdline.Unresolved)
        ]
        assert not hidden, name


# --- the readers, one rule each ---------------------------------------------
#
# A body the shell would close later than the reader does loses the commands
# after the early close, and a body it closes earlier reads text as commands.
# Most such misses are covered twice over at the gate -- a later `$(` is
# still found -- so each rule is pinned here on the body itself.

BODIES = {
    "a plain one": ("echo $(a b)", ["a b"]),
    "a `)` in double quotes": ('echo $(printf ")") x', ['printf ")"']),
    "a `)` in single quotes": ("echo $(printf ')') x", ["printf ')'"]),
    "an escaped `)`": ("echo $(printf \\)) x", ["printf \\)"]),
    "a `)` in a heredoc": (
        "echo \"$(cat <<'EOF'\n)\nEOF\nb)\" x",
        ["cat <<'EOF'\n)\nEOF\nb"],
    ),
    "a `)` in a dashed heredoc": (
        "echo \"$(cat <<-'EOF'\n)\n\tEOF\nb)\" x",
        ["cat <<-'EOF'\n)\n\tEOF\nb"],
    ),
    "a case runs to the end": (
        "echo $(case x in a) b;; esac) c",
        ["case x in a) b;; esac) c"],
    ),
    "nested, outermost only": ("echo $(a $(b)) c", ["a $(b)"]),
    "backticks": ("echo `a` `b`", ["a", "b"]),
    "an escaped backtick inside": ("echo `a \\` b` c", ["a \\` b"]),
    "unterminated": ("echo $(a b", ["a b"]),
    "process substitutions": ("cat <(a) >(b)", ["a", "b"]),
    "single quotes are text": ("echo '$(a)' '`b`'", []),
    "a quoted `<(` is text": ('echo "<(a)"', []),
    "a herestring opens no heredoc": ('echo $(cat <<< "a" ; b) c', ['cat <<< "a" ; b']),
    "an apostrophe in double quotes is not a quote": ('echo "it\'s $(a)"', ["a"]),
    "a double-quoted `$(` runs": ('echo "$(a)"', ["a"]),
    "an escaped `$(` is text": ("echo \\$(a) b", []),
}


@pytest.mark.parametrize("name", sorted(BODIES))
def test_substitution_bodies(name):
    command, bodies = BODIES[name]
    assert cmdline.substitution_bodies(command) == bodies, name


TEXTS = {
    "bash -c": (["bash", "-c", "a b"], ["a b"]),
    "a cluster holding c": (["bash", "-ec", "a b"], ["a b"]),
    "every non-option word once -c is given": (
        ["bash", "-o", "errexit", "-c", "a b"],
        ["errexit", "a b"],
    ),
    "no -c: a script, not a string": (["bash", "run.sh", "a b"], []),
    "su --command=": (["su", "--command=a b", "u"], ["u", "a b"]),
    "su --command, separate": (["su", "--command", "a b"], ["a b"]),
    "--command is su's, not a shell's": (["bash", "--command", "a b"], []),
    "watch": (["watch", "-n", "5", "a b"], ["5", "a b"]),
    "env -S": (["env", "-S", "a b"], ["a b"]),
    "env -S glued": (["env", "-Sa b"], ["a b"]),
    "env --split-string=": (["env", "--split-string=a b"], ["a b"]),
    "behind a runner": (["sudo", "sh", "-c", "a b"], ["a b"]),
}


@pytest.mark.parametrize("name", sorted(TEXTS))
def test_reparsed_texts(name):
    tokens, texts = TEXTS[name]
    assert cmdline.reparsed_texts(tokens) == texts, name


def test_an_unknown_command_word_is_named_and_a_structural_one_is_not():
    assert cmdline.names_an_unknown_command("$CMD a")
    assert cmdline.names_an_unknown_command("echo; ${X} b")
    for text in ("[ -f x ] && echo y", "{ echo y; }", "echo $X", "if true; then :; fi"):
        assert not cmdline.names_an_unknown_command(text), text
