"""The reader answered "nothing moved" for every construct it did not model.

Issue #72. `hooks/cmdline.py` walks a command's segments to say which
repository its `git commit` lands in, and its default for an unmodelled
construct was that the shell stayed where it was. That is a confident answer,
not an absent one, and it is wrong in both directions at once: a stop where
the session's own directory needs review, and a silence where that directory
carries a routing declaration and the commit lands somewhere else.

Five constructs were measured that way -- a `cd` inside a function body, a
sourced script, an `eval`, a `pushd`, and a loop. `command cd <path>` is a
sixth found here: `WRAPPERS` is read past when looking for `git` and not when
looking for `cd`.

The reader now enumerates what it UNDERSTANDS and routes everything else to
`Unresolved`, which `docs/review-chain-spec.md` already treats as a stop
rather than a pass. The tests below are in two halves, and both are load
bearing: the constructs that must now stop, and the two ordinary shapes that
must not have gained a single candidate.
"""

import os
import shlex
import subprocess

import pytest
from conftest import load_hook_module, shell_probe

reader = load_hook_module("cmdline.py", "cmdline_understood")
wg = load_hook_module("worktree-guard.py", "wg_understood")

SESSION = "/session"
TARGET = "/target"
# `TARGET` as the READER spells it back, which is not always how it was typed.
#
# The two constants are NOT symmetric, and the `windows-latest` job is the only
# thing that says so. `SESSION` is handed to `walk_directories` as the starting
# cwd and comes back untouched, so it answers in the spelling above. `TARGET`
# is reached through `cd`, and `apply_chdir` normalises, so on Windows it
# answers `\\target`. One run asserted the typed spelling for both and eight
# cases failed; the next asserted the normalised spelling for both and twelve
# did. The runner printed the asymmetry outright -- `['\\target', '/session']`
# in one answer list.
#
# The rule the two runs together establish: a directory the reader CONSTRUCTS
# is normalised -- `cd /target`, and `<cwd>/$WT` from `cd "$WT"`, both come back
# with the platform's separator. The cwd it was HANDED is returned as given.
# `test_one_directory_reached_two_ways_stays_two_answers` is the case that
# separates them: it builds `{SESSION}/$WT` and needs the normalised form, and
# its absence from the second run's failures is what proved it.
#
# That mixed spelling is a property of the reader, not of this work item:
# nothing here touches a path separator (the arithmetic scan is
# character-level, the understood check token-level) and it is the same at
# `release/v0.22.0`. It is recorded in `round-4.md` rather than fixed here.
TARGET_READ = os.path.normpath(TARGET)


def commit_wheres(command, cwd=SESSION):
    """Every directory the `git commit` in `command` may run in.

    Through the judgment read, because that is what both gates perform.
    """
    text = reader.drop_heredoc_bodies(reader.drop_comments(command))
    items, clean = reader.split_segments_with_separators(text)
    assert clean, command
    out = []
    for tokens, wheres in reader.walk_directories(items, cwd):
        parsed = reader.parse_git(tokens)
        if parsed and parsed[0] == "commit":
            out.extend(wheres)
    return out


def unreadable(wheres):
    return [w for w in wheres if isinstance(w, reader.Unresolved)]


# Each row is (name, the command, what a real shell does with the `cd`). The
# third element is what the probe below runs, so the deny is grounded in where
# bash actually lands rather than in an argument about where it might.
MOVES_THE_SHELL = [
    ("a function body", "f() { cd %s; }; f; git commit -m x", "f() { cd %s; }; f"),
    (
        "a spaced function body",
        "f () { cd %s; }; f; git commit -m x",
        "f () { cd %s; }; f",
    ),
    ("an eval", "eval 'cd %s'; git commit -m x", "eval 'cd %s'"),
    ("a pushd", "pushd %s; git commit -m x", "pushd %s >/dev/null"),
    (
        "a for loop",
        "for d in %s; do cd $d; done; git commit -m x",
        "for d in %s; do cd $d; done",
    ),
    (
        "a while loop",
        "while true; do cd %s; break; done; git commit -m x",
        "while true; do cd %s; break; done",
    ),
    ("a sourced script by dot", ". %s/s.sh; git commit -m x", ". %s/s.sh"),
    ("a sourced script by source", "source %s/s.sh; git commit -m x", "source %s/s.sh"),
    ("a wrapper before cd", "command cd %s && git commit -m x", "command cd %s"),
    (
        "a wrapper with an option",
        "command -p cd %s && git commit -m x",
        "command -p cd %s",
    ),
    (
        "a wrapper with an end-of-options",
        "command -- cd %s && git commit -m x",
        "command -- cd %s",
    ),
    (
        "a wrapper around a variable",
        "C=cd; command $C %s && git commit -m x",
        "C=cd; command $C %s",
    ),
]

NAMES = [row[0] for row in MOVES_THE_SHELL]


@pytest.mark.parametrize("name,command,_probe", MOVES_THE_SHELL, ids=NAMES)
def test_a_construct_the_reader_does_not_model_stops_the_commit(name, command, _probe):
    """S1-S6. Not "the shell stayed here", which is an answer -- `Unresolved`,
    which is the reader saying it does not have one."""
    filled = command.replace("%s/s.sh", "/x/s.sh")
    if "%s" in filled:
        filled = filled % TARGET
    wheres = commit_wheres(filled)
    assert wheres, f"{name}: no commit was found at all"
    assert unreadable(wheres) == wheres, (
        f"{name}: the reader still answered with a directory: "
        f"{[str(w) for w in wheres]}"
    )


@pytest.mark.parametrize("name,_command,probe", MOVES_THE_SHELL, ids=NAMES)
def test_a_real_shell_really_lands_in_the_target(name, _command, probe, tmp_path):
    """The other half of the measurement, and the reason the stop is right.

    Every construct above leaves bash in the target directory, so the reader's
    old answer -- the session's own directory -- named a repository the commit
    was not going to land in. Without this, the tests above pin a stop with no
    evidence that anything was ever wrong.

    `sudo cd` is deliberately not here: it looks for a binary named `cd` and
    finds none, so it does NOT move the shell. The reader stops for it anyway,
    because keeping which wrapper forks would be one more enumeration.
    """
    why = shell_probe("bash")
    if why:
        pytest.skip(f"bash: {why}")
    target = tmp_path / "target"
    target.mkdir()
    # The sourced-script rows name a script beside the target; the others
    # ignore it. Writing it unconditionally keeps the table one shape.
    (tmp_path / "s.sh").write_text(f"cd {shlex.quote(str(target))}\n")
    filled = probe.replace("%s/s.sh", shlex.quote(str(tmp_path / "s.sh")))
    if "%s" in filled:
        filled = filled % shlex.quote(str(target))
    out = subprocess.run(
        ["bash", "-c", filled + "; pwd -P"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    landed = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else ""
    assert landed == str(target.resolve()), (
        f"{name}: bash landed in {landed!r}, so this row is not the case it "
        f"claims to be (stderr: {out.stderr.strip()!r})"
    )


def test_the_common_cross_repository_form_gains_nothing():
    """S11. `cd <repo> && git commit` is the shape issue #45 exists to keep
    silent, and the detector must not have widened it by one candidate."""
    wheres = commit_wheres(f"cd {TARGET} && git commit -m x")
    assert [str(w) for w in wheres] == [TARGET_READ]
    assert unreadable(wheres) == []


def test_the_commit_message_heredoc_gains_nothing():
    """S12. The form Claude Code itself writes. A `$(cat <<'EOF' ...)` body is
    a commit message, and the segment holding it is an ordinary `git`
    invocation -- nothing in it is a construct the reader fails to read.

    Driven with a segment IN FRONT of the commit, because a single-segment
    command's `running` is always `[(cwd, None)]` and no answer it produces
    can be unreadable. Without one the type assertion below cannot fail:
    measured, it stayed green under a mutation that made `understood()`
    return False for everything.
    """
    wheres = commit_wheres(
        "git add -A && git commit -m \"$(cat <<'EOF'\ntitle\nEOF\n)\""
    )
    assert [str(w) for w in wheres] == [SESSION]
    assert unreadable(wheres) == []


@pytest.mark.parametrize(
    "command",
    [
        f"cd {TARGET} && make && git commit -m x",
        f"cd {TARGET} && ./deploy.sh && git commit -m x",
        f"cd {TARGET} && git add -A && git commit -m x",
        "sudo git commit -m x",
        "env FOO=1 git commit -m x",
        "time git commit -m x",
        # A conditional expression holds no commands, so it cannot leave the
        # shell anywhere. `[[ … ]]` is a reserved word and `[` is `test`
        # spelled the other way -- read as a scope opener and as a glob
        # respectively, both stopped what `test -f f.py && git commit`, the
        # same condition in a third spelling, never stopped.
        "[ -f f.py ] && git commit -m x",
        "[[ -f f.py ]] && git commit -m x",
        "[ ! -f zzz ] && git commit -m x",
        "test -f f.py && git commit -m x",
        # `shopt` does not move a shell. It was a relocator for one round on
        # the grounds that `expand_aliases` turns alias expansion on, and an
        # alias written in the command is caught by `alias` itself while one
        # set by a profile is caught by nothing -- so it closed no door and
        # stopped `shopt -s globstar && git commit`.
        "shopt -s globstar && git commit -m x",
        "shopt -s nullglob && git commit -m x",
    ],
)
def test_an_ordinary_command_is_still_understood(command):
    """A wrapper, a script, a build tool -- none of them is a construct. A
    detector that stopped on these would be the "judge every directory named
    anywhere" option `plan.md` rejected, arriving by accident."""
    found = commit_wheres(command)
    assert found, f"no commit was found at all: {command!r}"
    assert unreadable(found) == []


@pytest.mark.parametrize(
    "command",
    [
        "n=$((1<<2))\ngit commit -m x",
        "n=$(( (1<<2) + 3 ))\ngit commit -m x",
        "echo $((n<<1))\ngit commit -m x",
    ],
)
def test_arithmetic_is_not_a_heredoc(command):
    """S7. `<<` inside `$((…))` is a left shift.

    Read as a redirect it took `2))` for a delimiter and dropped every line
    after it looking for one that matched, so the commit did not arrive
    misjudged -- it did not arrive at all, and a gate with no commit in front
    of it has nothing to say. The assertion is therefore that a commit is
    FOUND, and found where the shell actually is.
    """
    wheres = commit_wheres(command)
    assert wheres, "the commit after the arithmetic was swallowed entirely"
    assert [str(w) for w in wheres] == [SESSION], (
        "the commit after the arithmetic was swallowed with the heredoc body"
    )
    assert unreadable(wheres) == []


def test_a_heredoc_body_is_still_dropped():
    """The case `drop_heredoc_bodies` exists for, pinned beside the fix.

    A body is data. Stepping over arithmetic must not have taught the reader
    to walk into one -- `cd /elsewhere` here is a line written to a file, and
    the commit belongs to the session's own repository.
    """
    wheres = commit_wheres("cat > run.sh <<'EOF'\ncd /elsewhere\nEOF\ngit commit -m x")
    assert [str(w) for w in wheres] == [SESSION]


@pytest.mark.parametrize(
    "command",
    [
        f"cd {TARGET} ; git commit -m x",
        f"cd {TARGET} && make ; git commit -m x",
        f"cd {TARGET} && make\ngit commit -m x",
        f"cd {TARGET} && npm run build && lint ; git commit -m x",
    ],
)
def test_a_semicolon_consumes_the_failure_branch(command):
    """S8-S10. `;` and a newline run what follows either way.

    `||` was the only operator that consumed a parked failure, so a `cd` in
    front of a `;` read as though it could not fail and the directory the
    shell was already in dropped out of the answer. Where that directory is
    the session's own and the target carries a routing declaration, the
    declaration silenced a commit that could land in either.

    A newline is the same operator: `split_segments_with_separators` writes
    an unquoted one out as `;`, so the third row is the second row wrapped
    the way a long command is normally written.
    """
    found = commit_wheres(command)
    wheres = [str(w) for w in found]
    assert TARGET_READ in wheres, command
    assert SESSION in wheres, f"the failure branch of the `cd` is missing: {wheres}"
    # By TYPE, not by text. `Unresolved` subclasses `str`, so an answer that
    # has gone entirely unreadable spells the same two paths and passed the
    # two assertions above unchanged.
    assert unreadable(found) == []


def test_the_ampersand_form_is_still_the_target_alone():
    """The mirror of the case above, and the cost that must stay at zero.

    `&&` runs the commit only where the `cd` arrived. Making `;` branch must
    not have taught `&&` to, or every `cd <repo> && git commit` starts
    answering for the session's own repository too -- the prompt volume issue
    #45 exists to reduce.
    """
    found = commit_wheres(f"cd {TARGET} && git commit -m x")
    assert [str(w) for w in found] == [TARGET_READ]
    assert unreadable(found) == []


def test_a_semicolon_chain_reaches_the_cap_rather_than_multiplying():
    """`;` adds a branch point, so it adds a shape that multiplies.

    Measured at `STATE_CAP` = 64, counting the `cd` segments in front of the
    commit: a chain of `;`-joined `cd`s reads as a directory the reader could
    not compute from the seventh on. Before this change that chain did not
    multiply at all -- one candidate at any length -- because a `;` consumed
    nothing. Past the cap the answer says it is not an answer, which is this
    module's failure direction: a stop, never a guess.
    """
    command = " ; ".join(f"cd d{i}" for i in range(8)) + " ; git commit -m x"
    wheres = commit_wheres(command)
    assert len(wheres) <= reader.STATE_CAP
    assert unreadable(wheres) == wheres, (
        "past the cap the answer has to say it is not an answer"
    )


@pytest.mark.parametrize(
    "command",
    [
        "n=$[1<<2]\ngit commit -m x",
        "n=$[ (1<<2) + 3 ]\ngit commit -m x",
    ],
)
def test_the_older_arithmetic_spelling_is_arithmetic_too(command):
    """`$[…]` is bash's older spelling of `$((…))` and closes on ONE bracket.

    Left out of the branch that steps over arithmetic, it swallowed the commit
    below it exactly as `$((1<<2))` did -- measured with the commit really
    created in a scratch repository while the reader's segment list held no
    commit at all.
    """
    found = commit_wheres(command)
    assert found, "the commit after the arithmetic was swallowed entirely"
    assert [str(w) for w in found] == [SESSION]
    assert unreadable(found) == []


def test_a_parenthesis_in_a_string_does_not_stretch_the_arithmetic():
    """The depth count tracks quotes, because a shell does.

    Counting brackets blind, one `(` inside a string ran the region to the end
    of the input, and the heredoc body after it was raised as commands -- so
    `cat > run.sh <<'EOF'` with a `cd` in the body newly stopped a command
    that only writes a file.
    """
    command = (
        "x=$((printf '(' ) )\ncat > run.sh <<'EOF'\ncd /elsewhere\nEOF\ngit commit -m x"
    )
    found = commit_wheres(command)
    assert [str(w) for w in found] == [SESSION], "the heredoc body was read as commands"
    assert unreadable(found) == []


def test_cd_dash_does_not_launder_an_unreadable_shell():
    """`cd -` returns to a directory the reader recorded, and after a segment
    it could not follow that record is not where the shell has been.

    Returning the recorded previous directory washed the answer clean:
    `eval 'cd /A; cd /B' && cd - && git commit` answered the session's own
    directory with nothing marked unreadable, while bash stood in `/A`. It is
    the one place the invariant this work item introduces did not survive a
    segment.
    """
    found = commit_wheres("eval 'cd /A; cd /B' && cd - && git commit -m x")
    assert found and unreadable(found) == found, (
        f"the answer came back readable: {[str(w) for w in found]}"
    )


def test_cd_dash_with_no_previous_directory_invents_no_path():
    """A `cd -` the reader has no previous directory for is unreadable, not a
    path built out of the operand.

    `<cwd>/-` exists nowhere, and putting it in the prompt names a target the
    user never typed. The `;` merge feeds exactly that state -- a branch whose
    `cd` failed has no previous directory -- so a shape that used to need
    `cd -` as the very first segment became common.
    """
    found = commit_wheres("cd /A ; cd - ; git commit -m x")
    assert not [w for w in found if str(w).endswith("/-")], (
        f"a path nobody typed reached the answer: {[str(w) for w in found]}"
    )


def test_a_reserved_word_that_only_stands_in_front_is_not_a_scope():
    """`time` and `!` stand in FRONT of a command rather than opening a scope.

    Read as scope openers they stopped `time make && git commit` and
    `! grep -q zzz f && git commit`, both ordinary and both silent before this
    work item. The segment's own directory was never the question -- what
    changed was every segment after it.
    """
    for command in (
        "time make && git commit -m x",
        "! grep -q zzz f.py && git commit -m x",
    ):
        found = commit_wheres(command)
        # `unreadable([]) == []`, so an answer with no commit in it passes the
        # line below. A commit swallowed whole is not hypothetical here --
        # both the arithmetic case and the comment case produced exactly that.
        assert found, f"no commit was found at all: {command!r}"
        assert unreadable(found) == []
    # The pair: a `cd` behind one of them is unreadable, because whether the
    # word forks is what decides whether that `cd` reaches this shell.
    assert unreadable(commit_wheres(f"time cd {TARGET} && git commit -m x")) != []


def test_an_alias_on_cd_stops_the_commit():
    """`alias cd='cd <B>'` leaves both words in the command exactly as written.

    So this is a directory the reader got confidently wrong rather than a
    command it never saw -- which is why `alias` and `shopt` are relocators
    and not, like a command hidden in an `eval` string, issue #75's shape.
    Executed: bash stands in `<B>` while the reader answered `['/tmp', '/S']`
    with nothing marked unreadable.

    Not every candidate comes back unreadable, and that is the reader being
    consistent rather than a gap. An absolute `cd` does not depend on where
    the shell was, so `/tmp` is recovered clean -- the rule that lets
    `eval 'echo hi'; cd /tmp; git commit` answer `/tmp` instead of giving up.
    One unreadable candidate is what stops the commit, and that is what this
    asserts.

    What no enumeration reaches: an alias set by `BASH_ENV` or a profile,
    which never appears in the command string at all.
    """
    found = commit_wheres(f"alias cd='cd {TARGET}'\ncd /tmp\ngit commit -m x")
    assert unreadable(found), (
        f"nothing in the answer says the reader could not follow the alias: "
        f"{[str(w) for w in found]}"
    )


def test_an_unreadable_target_records_why_it_could_not_be_read():
    """The two ways a target goes unreadable need different ways out, so the
    reader records which one happened.

    For a value the shell would have expanded, writing the absolute path in
    its place is a real instruction. For a construct there is no value to
    replace and the directory carried is the last one the reader could name,
    usually the session's own -- so the same instruction changes nothing and
    the waiver becomes the only exit. `hooks/commit-review-gate.py` picks the
    arm off this field; without it, both failures got the value's prompt.
    """
    value = commit_wheres('cd "$WT" && git commit -m x')
    assert [w.why for w in value] == [reader.Unresolved.VALUE]

    construct = commit_wheres("eval 'cd /B' && git commit -m x")
    assert [w.why for w in construct] == [reader.Unresolved.CONSTRUCT]

    # A command can reach both, and they stay apart: `cd "$WT"` is the value
    # the reader could not expand and the `eval` is the construct it could not
    # follow. Collapsing them by type alone -- which is how the states used to
    # be keyed -- leaves one prompt speaking for both.
    both = commit_wheres("cd \"$WT\" || eval 'cd /B' || git commit -m x")
    assert sorted({w.why for w in both}) == [
        reader.Unresolved.CONSTRUCT,
        reader.Unresolved.VALUE,
    ], [(str(w), w.why) for w in both]


def test_one_directory_reached_two_ways_stays_two_answers():
    """The reason is part of what makes two states distinct, not a label on
    one of them.

    A pipeline leaves the parent shell where it was and carries the moved
    state beside it, so `cd "$WT" && eval '…' | git commit` reaches
    `<cwd>/$WT` twice: once as the value the reader could not expand, and once
    marked by the `eval` it could not follow. Keyed by type alone, which is
    how these states used to be told apart, the two collapse into whichever
    came first and one prompt then speaks for both.
    """
    both = commit_wheres("cd \"$WT\" && eval 'cd /B' | git commit -m x")
    at_value = {w.why for w in both if str(w) == os.path.normpath(f"{SESSION}/$WT")}
    assert at_value == {
        reader.Unresolved.VALUE,
        reader.Unresolved.CONSTRUCT,
    }, [(str(w), getattr(w, "why", None)) for w in both]


@pytest.mark.parametrize(
    "command",
    [
        "cd - && git commit -m x",
        "cd - ; git commit -m x",
    ],
)
def test_a_cd_dash_the_reader_cannot_retrace_says_construct(command):
    """The directory carried is one the reader named itself, so there is no
    value for the user to write out.

    Marked `VALUE`, the gate answers a `cd -` it cannot retrace with *"write
    the absolute path in place of the unresolved value"* — an instruction with
    no value to apply it to, which leaves the waiver as the only way past.
    That is the arm round 1 opened as a blocking finding, reached through a
    different door.
    """
    found = commit_wheres(command)
    reasons = {getattr(w, "why", None) for w in found}
    assert reader.Unresolved.CONSTRUCT in reasons, [
        (str(w), getattr(w, "why", None)) for w in found
    ]
    # `;` also carries the branch where the `cd -` FAILED, and that shell
    # really did stay put -- a readable answer, correctly. What must not be
    # here is `VALUE`, which is the arm with no value to write out.
    assert reader.Unresolved.VALUE not in reasons


def test_the_cap_collapse_says_construct(monkeypatch):
    """Past `STATE_CAP` the command reached more directories than the reader
    will answer for, and that is not a value anyone can write out either.

    Driven with the cap lowered rather than with a sixty-segment command, so
    the case reads as what it is about.
    """
    monkeypatch.setattr(reader, "STATE_CAP", 3)
    command = " ; ".join(f"cd a{i}" for i in range(6)) + " ; git commit -m x"
    found = commit_wheres(command)
    assert found and all(
        getattr(w, "why", None) == reader.Unresolved.CONSTRUCT for w in found
    ), [(str(w), getattr(w, "why", None)) for w in found]


def test_a_readable_directory_carries_no_reason():
    """The field is what tells an unreadable target from a readable one at the
    grouping key, so a plain answer must not grow one by accident."""
    assert [getattr(w, "why", None) for w in commit_wheres("git commit -m x")] == [None]


def test_a_hash_after_a_command_substitution_opens_no_comment():
    """`)` ends a word for a subshell and not for `$(…)`, and this reader
    cannot tell them apart.

    Executed: `bash -c 'echo $(echo a)#foo && echo X'` prints `a#foo` and then
    `X`, so bash runs everything after that `#`. Reading it as a comment
    opener deleted the `&& git commit` behind it — and once the commit gate's
    judgment read started dropping comments, that deletion reached a gate with
    no commit left to judge. A blank still opens one.
    """
    found = commit_wheres(f"cd {TARGET} && echo $(pwd)#note && git commit -m x")
    assert found, "the commit was deleted with a comment bash does not open"
    assert [str(w) for w in found] == [TARGET_READ]
    # The spaced form is a comment in bash too, so the commit really is gone
    # from what the shell would run -- and the reader answers for the segments
    # that remain rather than inventing one.
    spaced = commit_wheres(f"cd {TARGET} && echo $(pwd) # note && git commit -m x")
    assert spaced == []


@pytest.mark.parametrize(
    "command",
    [
        "cat <(echo a)#zzz ; git commit -m x",
        "echo <(echo a)#zzz ; git commit -m x",
        "echo a > >(cat)#zzz ; git commit -m x",
        "x=(a b)#zzz && git commit -m x",
        "files=(*.py)#zzz ; git commit -m x",
        "x=()#zzz && git commit -m x",
    ],
)
def test_a_hash_after_a_word_part_paren_opens_no_comment(command):
    """A `)` that closes something a WORD runs through opens no comment.

    `$(` is not the only opener. Four are: `$(`, the `<(` and `>(` of a
    process substitution, and the `(` of an array assignment `name=(`.
    Measured under bash 3.2.57 against a scratch repository -- every command
    here really creates a commit, and reading that `)` as a subshell's put a
    comment where bash opens none and deleted the commit behind it.

    Round 2 closed `$(` and round 4 found the other three still open, which
    is why the model is pinned here by construct rather than by example.
    """
    assert commit_wheres(command), command


def test_a_subshell_close_still_opens_one(command=None):
    """The other side of the same constant, so neither direction is free.

    `(echo a)#zzz` really is a comment to bash -- and bash creates no commit
    there, so the reader answering `blind` is correct. Teaching every `)` to
    leave the word running would make this case wrong.
    """
    assert not commit_wheres("(echo a)#zzz ; git commit -m x")


@pytest.mark.parametrize(
    "command",
    [
        "i=0\nwhile ((i<1)); do((i=i+(1<<2)))\nbreak; done\ngit commit -m x",
        "if true; then((x=1<<2))\nfi\ngit commit -m x",
        "if false; then :\nelse((x=1<<2))\nfi\ngit commit -m x",
        "!((1<<2))\ngit commit -m x",
        "{((x=1<<2))\n}\ngit commit -m x",
    ],
)
def test_arithmetic_glued_to_a_reserved_word_is_arithmetic_too(command):
    """`(` is a metacharacter, so a reserved word ends at it with no blank.

    Requiring one was a fail-open. Measured under bash 3.2.57 against a
    scratch repository: each of these really creates a commit. Read as a
    redirect, the `<<` took its delimiter out of the expression and swallowed
    every line after it, the commit included, and both gates stayed silent.
    """
    assert commit_wheres(command), command


def test_the_spaced_form_was_never_the_broken_one(command=None):
    """The control. One space was the whole difference, which is what said the
    defence was half built rather than absent."""
    assert commit_wheres(
        "i=0\nwhile ((i<1)); do ((i=i+(1<<2)))\nbreak; done\ngit commit -m x"
    )


def test_a_paren_pair_in_a_quoted_string_is_not_arithmetic(command=None):
    """The cost of dropping the blank, bounded where it is cheapest to check.

    Quotes are handled before the arithmetic branch, so a `((` inside them
    opens no region and a following heredoc body is still dropped. The two
    shapes that DO answer differently without the blank are both rejected by
    `bash -n`, and are recorded at the branch rather than pinned here.
    """
    found = commit_wheres(
        "echo '((' <<'EOF'\ngit commit -m sneaky\nEOF\ngit commit -m real"
    )
    assert len(found) == 1, f"the heredoc body was read as commands: {found}"


@pytest.mark.parametrize("op", ["@", "!", "*", "+", "?"])
def test_an_extglob_pattern_keeps_the_word_running(op):
    """extglob's five operators make `(` part of a WORD, the way `$(` does.

    Read as a command paren, the `)` ends the word and the `#` after it opens a
    comment bash does not -- which DELETES the commit behind it, and both gates
    then say nothing. Measured under bash 3.2.57 against a scratch repository:
    with `shopt -s extglob` on the line above, `ls -d @(a|b)#x ; git commit`
    really commits, 1 -> 2.

    `bash -n` calls it a syntax error and is WRONG here: `extglob` is a runtime
    shopt the parse check cannot see. Measure this family with `bash -O
    extglob`. Round 4 enumerated four openers and declared the list closed;
    this is the fifth time that constant has been found short.
    """
    assert commit_wheres(f"shopt -s extglob\nls -d {op}(a|b)#x ; git commit -m x")


# The seventeen operators that take a WORD, which is the whole family round 5
# generated. `${x:-((}` has no closing paren, so a reader with no `${…}` state
# ran the arithmetic region to the end of the input.
WORD_TAKING_EXPANSIONS = [
    "${x:-((}",
    "${x-((}",
    "${x:+((}",
    "${x+((}",
    "${y:=((}",
    "${y=((}",
    "${x:?((}",
    "${x?((}",
    "${x#((}",
    "${x##((}",
    "${x%((}",
    "${x%%((}",
    "${x/((/z}",
    "${x//((/z}",
    "${x/z/((}",
    "${x^((}",
    "${x,((}",
]


@pytest.mark.parametrize("expansion", WORD_TAKING_EXPANSIONS)
def test_a_paren_pair_inside_a_parameter_expansion_is_a_word(expansion):
    """Issue #78, and this expectation is the flip that says it landed.

    It used to assert `2` -- the sneaky commit inside the heredoc body counted
    as a second one, because the arithmetic region ran to the end of the input
    and the `<<` below it was never read as a redirect. Round 5 measured the
    family at 51 shapes across all seventeen operators and pinned the answer
    it gave rather than the answer bash gives, so that leaving it stayed a
    decision.

    Both paren models now count `${…}` nesting, so the `((` in here is the
    text bash treats it as, the heredoc opens, and the body is dropped. One
    commit, which is what bash makes.
    """
    found = commit_wheres(
        f"echo {expansion} <<'EOF'\ngit commit -m sneaky\nEOF\ngit commit -m real"
    )
    assert len(found) == 1, f"the heredoc body was read as commands: {found}"


def test_a_parameter_expansion_paren_no_longer_imports_the_body_s_cd():
    """The sharpest form, and the one that cost a person something.

    Executed under bash 3.2.57 against a scratch repository: bash prints `((`,
    stays in the directory it started in, and makes one commit -- 1 -> 2. The
    gate used to answer for `/target`, a path that exists only in the heredoc
    body, and DENIED a commit that had already been reviewed.

    It now answers for the directory the shell is actually in, which is the
    session's own. This assertion used to be `TARGET_READ in …`.
    """
    found = commit_wheres("echo ${x:-((} <<'EOF'\ncd /target\nEOF\ngit commit -m real")
    assert [str(w) for w in found] == [SESSION], found


def test_a_hash_inside_a_parameter_expansion_opens_no_comment():
    """The other paren model's own cost, which issue #78 reported as nothing.

    It was measured on six `${x:-((}#zzz` shapes, where this reader agrees
    with bash. A `#` after a BLANK inside the expansion was never measured and
    is a fail-OPEN: executed under bash 3.2.57, `echo ${x:-a #b} ; echo
    REACHED` prints `a #b` and then `REACHED`, so bash opens no comment and
    runs what follows -- while `drop_comments` returned `echo ${x:-a ` and the
    `git commit` behind it was gone from the segment list entirely.
    """
    assert commit_wheres("echo ${x:-a #b} ; git commit -m x") == [SESSION]
    assert "#b" in reader.drop_comments("echo ${x:-a #b} ; git commit -m x")


@pytest.mark.parametrize("expansion", WORD_TAKING_EXPANSIONS)
def test_the_six_shapes_the_comment_model_already_answered_are_unchanged(expansion):
    """S7's other half. `${…}#zzz` was measured against bash at round 5 and
    the reader agreed on all of it; teaching this model about `${…}` must not
    move an answer it already had right."""
    assert commit_wheres(f"echo {expansion}#zzz ; git commit -m x") == [SESSION]


def test_a_case_pattern_comment_does_not_take_the_segment_list():
    """An unbalanced `)` ends the word, which is what keeps a comment readable.

    A `case` pattern's `)` closes nothing this reader opened, and it is the
    place an unbalanced one actually occurs. Measured: bash opens a comment
    after it, and a comment left in place whose text holds an apostrophe opens
    a quote that never closes -- which took every later line, the commit
    included, out of the segment list.
    """
    command = (
        "case x in\nx)#don't\n  echo hit ;;\nesac\ncd /elsewhere && git commit -m x"
    )
    text = reader.drop_heredoc_bodies(reader.drop_comments(command))
    _, clean = reader.split_segments_with_separators(text)
    assert clean, "the apostrophe in a comment bash DOES open took the segment list"


def test_the_understood_check_can_fail():
    """The check has to be able to say no AND yes, or it is not a check.

    `verify`'s second condition: a check that cannot fail is a counterfeit
    seal. `understood` returning False for everything would make every test
    above pass and every command in the repository prompt.
    """
    assert reader.understood(["git", "commit", "-m", "x"]) is True
    assert reader.understood(["cd", "/tmp"]) is True
    assert reader.understood(["FOO=1", "make"]) is True
    assert reader.understood(["eval", "cd /tmp"]) is False
    assert reader.understood(["for", "d", "in", "x"]) is False
    assert reader.understood(["command", "-p", "cd", "/tmp"]) is False
    assert reader.understood(["command", "$C", "/tmp"]) is False
    assert reader.understood(["time", "make"]) is True


def test_the_guard_reads_the_same_answer():
    """S13. Issue #68's rounds twice fixed one gate and left the other, so the
    guard is asserted rather than assumed. It shares `walk_directories`
    through `hooks/worktree-guard.py:219`.

    `wg.cmdline` rather than the `reader` above: the guard reaches its reader
    with a plain `import cmdline`, which goes through `sys.modules`, while
    `load_hook_module` builds a second instance under its own name. The two
    `Unresolved` classes are then different objects and `isinstance` is False
    across them -- which is a test that passes for the wrong reason waiting to
    happen, since the failing direction is "nothing was unreadable".
    """
    walked = wg.walk_command(f"eval 'cd {TARGET}'; git switch main", SESSION)
    wheres = list(walked[-1][1])
    assert wheres and all(isinstance(w, wg.cmdline.Unresolved) for w in wheres), (
        f"the guard still answered with a directory: {[str(w) for w in wheres]}"
    )


@pytest.mark.parametrize("arith", ["$((1<<2))", "$[1<<2]"])
def test_arithmetic_inside_a_parameter_expansion_is_still_stepped_over(arith):
    """The direction `${…}` state can break, and the reason `$((` and `$[` are
    unconditional while a bare `((` is not.

    `$((1<<2))` is arithmetic wherever it is written, and the `<<` inside it is
    a shift. Suppressing the skip inside `${…}` would read that `<<` as a
    redirect naming the delimiter `2))}`, swallow every line after it, and take
    the `git commit` with it — a fail-OPEN, where the family this change closes
    was fail-closed. Executed: `echo ${x:-$((1<<2))}` prints `4` and reaches
    the next command.
    """
    found = commit_wheres(
        f"echo ${{x:-{arith}}} <<EOF\ncd /target\nEOF\ngit commit -m real"
    )
    assert [str(w) for w in found] == [SESSION], found


def test_an_unbalanced_expansion_leaves_the_heredoc_readable():
    """`${` with no `}` holds the count open to the end of the input, which is
    the state that could hide a real `((` region. Nothing else moves: the
    heredoc opener is read by a later branch, so the body is still dropped and
    the commit below it is still found."""
    found = commit_wheres("echo ${x <<EOF\ncd /target\nEOF\ngit commit -m real")
    assert [str(w) for w in found] == [SESSION], found


def test_only_a_dollar_brace_opens_the_expansion_count():
    """A bare `{` is a group or a brace expansion, not an expansion of a name.

    Measured under bash 3.2.57: `echo { #c ; echo REACHED` prints `{` and does
    NOT reach the next command, so bash opens a comment there. Counting a bare
    `{` would hold the expansion open past the `}` that never comes, leave the
    comment standing, and read `git commit` as a command bash never runs.
    """
    assert commit_wheres("echo { #c ; git commit -m x") == []
    assert reader.drop_comments("echo { #c ; git commit -m x") == "echo { "


def test_a_paren_inside_an_expansion_is_a_word_part_in_the_comment_model_too():
    """Both models, not one. This is the half issue #78's title is about.

    Asserted at `drop_comments` rather than through a shell: bash rejects
    `echo ${x:-((} zz)#c` outright — `syntax error near unexpected token ')'`,
    measured — so there is no behaviour to compare against. What is being
    pinned is that the two models answer the same question the same way, which
    is what makes their answers predictable when one of them is wrong.
    """
    text = "echo ${x:-((} zz)#c ; git commit -m x"
    assert reader.drop_comments(text) == text, (
        "the `)` ended the word, the `#` opened a comment, and the commit went"
    )


def test_a_hash_inside_an_expansion_closes_no_brace_in_either_model():
    """Round 1: `drop_comments` got `and not braces` and the heredoc splitter
    did not, so the two models answered one question two ways.

    `${x:-a #b}` opened a comment in the splitter that swallowed the closing
    `}`, `braces` stayed 1 to the end of the input, every `((` after it
    stopped being an arithmetic region, and a `<<` inside one opened a
    heredoc that ate the rest of the command. Measured: the `git worktree
    add` below such a line left the segment list entirely and the worktree
    guard went silent on a command bash really runs, `rc=0`.
    """
    command = "echo ${x:-a #b}\n((1<<2))\ngit worktree add -b nb ../wt"
    text = reader.drop_heredoc_bodies(reader.drop_comments(command))
    items, clean = reader.split_segments_with_separators(text)
    assert clean, command
    words = [tokens for _, tokens in items]
    assert any(t[:2] == ["git", "worktree"] for t in words), (
        f"the `git worktree add` left the segment list: {words}. A `#` inside "
        "an expansion must not close the brace count in either model"
    )


def test_a_heredoc_opener_inside_an_expansion_opens_no_body():
    """Round 2: `braces` reached the `#` and `((` branches and not `<<`.

    `${x:-<<E}` opened a heredoc whose delimiter was `E}`, the closing line
    never came, and every line below it was swallowed as a body -- so a
    `git worktree add` bash really runs, `rc=0`, left the segment list
    entirely. 32 of 333 generated inputs failed open this way and every one
    was this family.
    """
    command = "echo ${x:-<<E}\ngit worktree add -b nb ../wt"
    items, clean = reader.split_segments_with_separators(
        reader.drop_heredoc_bodies(reader.drop_comments(command))
    )
    assert clean, command
    words = [tokens for _, tokens in items]
    assert any(t[:2] == ["git", "worktree"] for t in words), (
        f"the `git worktree add` left the segment list: {words}"
    )


def test_an_unbalanced_expansion_still_lets_a_heredoc_open():
    """The guard the fix above needed, and the reason it is not one word.

    Adding `not braces` alone would let an UNBALANCED `${` hold the count to
    the end of the input, hiding every heredoc opener after it and reading a
    body as commands -- the fail-OPEN direction, and the opposite of what the
    count exists for. So an expansion counts only when a `}` closes it."""
    command = "echo ${x <<EOF\ncd /elsewhere\nEOF\ngit commit -m x"
    items, clean = reader.split_segments_with_separators(
        reader.drop_heredoc_bodies(reader.drop_comments(command))
    )
    assert clean, command
    words = [tokens for _, tokens in items]
    assert not any("cd" in t for t in words), (
        f"the heredoc body was read as commands: {words}. An unbalanced "
        "`${` must not hold the brace count open"
    )
