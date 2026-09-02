"""A path the command defines one line earlier was still a path the gate could
not read.

`SB=/abs/path; git -C "$SB" commit` names its destination twice: once as an
assignment three readers step past and throw away, once as a `$SB` the
`EXPANDS` test calls unresolvable. A review agent's scratch-repo probes were
written that way, two of them reached a user who was not driving the session
as permission prompts inside five minutes, and stopping the agent to end the
prompts cost the review round.

The reader now keeps the names a command string writes for ITSELF. What it
must NOT do is guess at an environment this process cannot see: `git -C "$WT"`
with no assignment in the string stays unresolvable, because a hook's
environment is not the shell's and an answer from it would be silently wrong
wherever the two differ, and a loop variable stays unresolvable because it has as many
values as the loop has iterations. Those two are the cases that keep the
change bounded, and they are asserted here beside the ones that now resolve.
"""

import json
import os
import shlex
import subprocess

from conftest import decision_of, declare_routing, fired, load_hook_module, run_hook

reader = load_hook_module("cmdline.py", "cmdline_named")
gate = load_hook_module("commit-review-gate.py", "crg_named")

SESSION = "/session"


def sh(path):
    """`path` as one shell word — see the note in the sibling gate test."""
    return shlex.quote(str(path))


def commits(command, cwd=SESSION):
    """[(chdirs, where)] for each `git commit` — what the walk hands the gate.

    `chdirs` are `parse_git`'s `-C` values and `where` is the directory the
    segment's shell is in. Those two are exactly what this change moves, and
    reading them separately is what tells a resolved `-C` apart from a
    resolved `cd`.
    """
    text = reader.drop_heredoc_bodies(reader.drop_comments(command))
    items, clean = reader.split_segments_with_separators(text)
    assert clean, command
    out = []
    for tokens, wheres in reader.walk_directories(items, cwd):
        parsed = reader.parse_git(tokens)
        if parsed and parsed[0] == "commit":
            out.extend((tuple(parsed[2]), where) for where in wheres)
    return out


def targets(command, cwd=SESSION):
    """The directories the commits land in, composed the way the gate does.

    What comes back has been through `apply_chdir`, which ends in
    `os.path.normpath` -- so on Windows `/one` arrives as `\\one`. An expected
    path written as a bare literal is therefore a test that passes on two of
    the three matrix legs and fails on the third: four assertions here did
    exactly that, one of them for two releases. Put the expected value through
    `os.path.normpath` too.
    """
    return [str(reader.compose(where, list(ch))) for ch, where in commits(command, cwd)]


# --- what now resolves ----------------------------------------------------


def test_a_name_the_command_defined_names_the_repository():
    """S1. The one-assignment shape, which is the common one."""
    assert commits('SB=/abs/path; git -C "$SB" commit -m x') == [
        (("/abs/path",), SESSION)
    ]


def test_the_braced_spelling_reads_the_same():
    """S1. `${SB}` is the same name written the other way, and a reader that
    filled one and not the other would answer differently for two spellings of
    one command."""
    assert commits('SB=/abs/path; git -C "${SB}" commit -m x') == [
        (("/abs/path",), SESSION)
    ]


def test_a_name_composed_with_a_suffix_resolves():
    """S2. `"$SB/r1"` is how a scratch repository is actually named."""
    assert commits('SB=/abs/path; git -C "$SB/r1" commit -m x') == [
        (("/abs/path/r1",), SESSION)
    ]


def test_a_cd_to_a_name_the_command_defined_moves_the_shell():
    """S1 through the other operand. `_cd_target` and `parse_git` are two
    call sites reading one fact, and fixing one would answer differently for
    `cd "$SB" && git commit` than for `git -C "$SB" commit`."""
    assert targets('SB=/abs/path; cd "$SB" && git commit -m x') == [
        os.path.normpath("/abs/path")
    ]
    assert targets('SB=/abs/path; cd "$SB/r1" && git commit -m x') == [
        os.path.normpath("/abs/path/r1")
    ]


def test_a_value_built_from_an_earlier_name_resolves():
    """`B=$A/sub` records what `$A` already resolved to, because the value is
    substituted as it is bound."""
    assert commits('A=/base; B=$A/sub; git -C "$B" commit -m x') == [
        (("/base/sub",), SESSION)
    ]


def test_the_later_assignment_is_the_one_used():
    """S5, first half."""
    assert commits('SB=/one; SB=/two; git -C "$SB" commit -m x') == [
        (("/two",), SESSION)
    ]


# --- what must still stop -------------------------------------------------


def test_an_environment_variable_is_still_unresolvable():
    """S3, and it is the line the whole mechanism is bounded by.

    `$WT` comes from a shell this process cannot see. A reader that answered
    from its OWN environment would be silently wrong wherever the two differ,
    which is the confident-wrong direction `understood`'s docstring exists to
    end. The `$` has to survive into the operand.
    """
    assert commits('git -C "$WT" commit -m x') == [(("$WT",), SESSION)]


def test_an_undefined_name_beside_a_defined_one_is_still_unresolvable():
    """The same, with the mechanism switched on. An environment that holds
    `SB` must not answer for `OTHER`."""
    assert commits('SB=/x; git -C "$OTHER" commit -m x') == [(("$OTHER",), SESSION)]


def test_a_loop_variable_keeps_its_prompt_and_names_itself():
    """S4. `$n` has as many values as the loop has iterations, and one of them
    is not an answer.

    The operand comes back with `$SB` filled and `$n` standing, so the text a
    prompt prints names the part that could not be read rather than the part
    that could — which is what makes "write this one out" a usable
    instruction.
    """
    assert commits('SB=/p; git -C "$SB/r$n" commit -m x') == [(("/p/r$n",), SESSION)]


def test_the_expansion_operators_are_left_standing():
    """Everything one step out from a bare name stays unresolvable: an
    operator that takes a WORD, a command substitution, an arithmetic
    expansion, and a positional parameter."""
    for operand, expected in (
        ("${SB:-/y}", "${SB:-/y}"),
        ("${#SB}", "${#SB}"),
        ("$(pwd)", "$(pwd)"),
        ("$((1+1))", "$((1+1))"),
        ("$1", "$1"),
        ("$@", "$@"),
    ):
        assert commits(f'SB=/x; git -C "{operand}" commit -m x') == [
            ((expected,), SESSION)
        ], operand


def test_the_expands_test_still_stands_in_front_of_the_shell():
    """The substitution goes IN FRONT of the `EXPANDS` test and never replaces
    it, so a value carrying a glob is still a set of paths rather than one."""
    kind, operand = reader._cd_target(["cd", "/a*b"])
    assert (kind, operand) == ("unknown", "/a*b")
    where = commits('SB="/a*b"; cd "$SB" && git commit -m x')[0][1]
    assert isinstance(where, reader.Unresolved), (
        f"a glob named through a variable became one path: {where!r}"
    )


def test_an_assignment_in_the_same_segment_does_not_expand_in_it():
    """`SB=/x git -C "$SB"` — bash expands the arguments before it applies the
    assignment, so the shell does not see `/x` here either."""
    assert commits('SB=/abs/path git -C "$SB" commit -m x') == [(("$SB",), SESSION)]


# --- where an assignment may come from ------------------------------------


def test_an_assignment_the_reader_cannot_place_never_enters():
    """S5, second half. `understood` already refuses to say where these leave
    the shell, and a name is no easier than a directory.

    A subshell is on this list twice over: bash discards its assignments when
    it exits, so answering `/inside` would be wrong about bash and not only
    about what this reader can see.
    """
    for name, command in (
        ("a function body", 'f() { SB=/inside; }; f; git -C "$SB" commit -m x'),
        ("a loop body", 'for i in 1; do SB=/inside; done; git -C "$SB" commit -m x'),
        ("a subshell", '(SB=/inside); git -C "$SB" commit -m x'),
        ("an eval", "eval 'SB=/inside'; git -C \"$SB\" commit -m x"),
    ):
        assert [ch for ch, _ in commits(command)] == [("$SB",)], name


def test_a_pipeline_stage_leaves_the_parent_shells_name_alone():
    """bash runs each stage in a subshell: `A=1 | true; echo $A` prints
    nothing. The same fact that keeps a pipeline from moving the parent
    shell's DIRECTORY keeps it from writing its names."""
    for sep in ("|", "|&", "&"):
        assert [ch for ch, _ in commits(f'SB=/x {sep} git -C "$SB" commit -m y')] == [
            ("$SB",)
        ], sep


def test_an_assignment_this_reader_does_not_model_empties_the_name():
    """`A+=x` appends and `a[0]=x` writes one element. An earlier `SB=/one`
    left standing through either would answer confidently with a path the
    shell never reaches — the single failure mode this mechanism has."""
    for form in ("SB+=/two", "SB[0]=/two"):
        assert commits(f'SB=/one; {form}; git -C "$SB" commit -m x') == [
            (("$SB",), SESSION)
        ], form


def test_a_name_rebound_to_something_unresolvable_stops_again():
    """The later assignment wins even when it loses the answer: a reader that
    kept `/one` here would name a repository the shell left two segments
    ago."""
    assert commits('SB=/one; SB=$WT; git -C "$SB" commit -m x') == [(("$WT",), SESSION)]


# --- the checks can fail --------------------------------------------------


def test_the_substitution_can_fail():
    """`verify`'s second condition, at the unit that does the work.

    `_substitute` returning its operand unchanged would leave every case above
    green except the six that now resolve, and one that filled every `$`
    would take S3 and S4 with it. Both directions are asserted here.
    """
    assert reader._substitute("$SB/r1", {"SB": "/x"}) == "/x/r1"
    assert reader._substitute("${SB}/r1", {"SB": "/x"}) == "/x/r1"
    assert reader._substitute("$SB", {}) == "$SB"
    assert reader._substitute("$WT", {"SB": "/x"}) == "$WT"
    assert reader._substitute("${SB:-/y}", {"SB": "/x"}) == "${SB:-/y}"
    assert reader._substitute("$SBX", {"SB": "/x"}) == "$SBX"
    assert reader._substitute("/plain/path", {"SB": "/x"}) == "/plain/path"


def test_a_value_holding_a_dollar_is_never_rescanned():
    """One pass, so nothing here loops: what a substitution writes is not
    read again."""
    assert reader._substitute("$A", {"A": "$A", "B": "/x"}) == "$A"
    assert reader._substitute("$B", {"B": "$A/y", "A": "/loop"}) == "$A/y"


# --- the gate, executed ---------------------------------------------------


def reason_of(out):
    return json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


def make_repo(path, opted_in):
    """A repository with one commit, and `.specseal/` when it opts in."""
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    git = lambda *a: subprocess.run(
        ["git", "-C", str(path), *a], check=True, capture_output=True
    )
    (path / "f.py").write_text("x = 1\n")
    git("add", "-A")
    git("-c", "user.email=e@example.com", "-c", "user.name=e", "commit", "-qm", "base")
    (path / "f.py").write_text("x = 2\n")
    git("add", "-A")
    if opted_in:
        (path / ".specseal").mkdir()
    return path


def run(command, cwd, session=None):
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": str(cwd),
    }
    if session:
        payload["session_id"] = session
    return run_hook("commit-review-gate.py", payload)


def test_the_gate_reaches_a_repository_the_command_named_for_itself(tmp_path):
    """S2 at the gate, in the direction that costs a prompt today.

    The shell sits in a repository that never opted in; the commit lands in
    one that did. Written out, that stops. Written as an assignment and a
    `$SB`, it used to resolve to a directory that exists nowhere — so the gate
    asked about a path the user never typed instead of about the repository.
    """
    here = make_repo(tmp_path / "plain", opted_in=False)
    there = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run(f'SB={sh(there)}; git -C "$SB" commit -m x', here, session="named")
    assert fired(out)
    assert str(there) in reason_of(out), (
        "the verdict is about the repository the commit lands in"
    )


def test_a_declaration_silences_the_name_the_way_it_silences_the_path(tmp_path):
    """S1's other direction, and the one the original probes measured: the repository
    IS declared, so the written-out form is silent and the named form asked."""
    here = make_repo(tmp_path / "plain", opted_in=False)
    there = make_repo(tmp_path / "opted-in", opted_in=True)
    declare_routing(there)
    out = run(f'SB={sh(there)}; git -C "$SB" commit -m x', here, session="declared")
    assert decision_of(out) == "silent", (
        f"{there} carries a declaration; the gate judged a path nobody typed"
    )


def test_the_named_form_answers_what_the_written_out_form_answers(tmp_path):
    """Byte-identical, because the two commands reach the same repository.

    Comparing the two prompts is what catches a fix that resolves the target
    and then describes it differently — a user reading the two would have no
    way to tell that one command is the other one written out.
    """
    here = make_repo(tmp_path / "plain", opted_in=False)
    there = make_repo(tmp_path / "opted-in", opted_in=True)
    written = run(f"git -C {sh(there)} commit -m x", here, session="written")
    named = run(f'SB={sh(there)}; git -C "$SB" commit -m x', here, session="named2")
    assert decision_of(written) == decision_of(named) == "deny"
    assert reason_of(written) == reason_of(named)


def test_a_cd_to_a_named_path_reaches_the_same_repository(tmp_path):
    """The `cd` operand at the gate, which is the second of the two call
    sites the spec names."""
    here = make_repo(tmp_path / "plain", opted_in=False)
    there = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run(f'SB={sh(there)}; cd "$SB" && git commit -m x', here, session="cd")
    assert fired(out)
    assert str(there) in reason_of(out)


def test_an_environment_name_still_stops_the_gate(tmp_path):
    """S3 at the gate. The environment-variable answer must not move: the gate has no way
    to know what `$WT` holds, and a silence there is indistinguishable from a
    repository checked and found clean."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    declare_routing(here)
    assert fired(run('git -C "$WT" commit -m x', here, session="env")), (
        "the reader answered for a value only the user's shell holds"
    )


def test_an_assignment_in_front_of_a_command_is_that_commands_environment():
    """bash keeps a prefix assignment out of the shell: `A=1 true; echo "$A"`
    prints an empty line, measured under bash 3.2.57.

    So the shapes this reads are exactly the ones `understood` calls
    "assignments alone". `SB=/x make` looks like an assignment and is not one,
    and reading it would name a repository the shell never learned about.
    """
    for command in (
        'SB=/x make; git -C "$SB" commit -m y',
        'SB=/x true && git -C "$SB" commit -m y',
    ):
        assert [ch for ch, _ in commits(command)] == [("$SB",)], command


def test_two_assignments_in_one_segment_both_land():
    """`A=/a B=/b` alone is still assignments alone, and bash keeps both."""
    assert commits('A=/a B=/b; git -C "$A" commit -m x && git -C "$B" commit -m y') == [
        (("/a",), SESSION),
        (("/b",), SESSION),
    ]


def test_the_bind_refuses_a_subshell_of_its_own_accord():
    """`_bind`'s subshell guard is asserted at the unit, because the walk's
    `understood` check already refuses these and would keep the guard green
    if it were deleted — measured, removing it turns no case in this file red.

    Two things refusing one shape is deliberate: bash discards a subshell's
    assignments when it exits, so `(SB=/inside)` is wrong about bash and not
    only about what this reader can follow.
    """
    assert reader._bind({}, ["(SB=/inside)"]) == {}
    assert reader._bind({}, ["{", "SB=/inside"]) == {}
    assert reader._bind({}, ["SB=/inside"]) == {"SB": "/inside"}


def test_a_single_quoted_operand_is_filled_too_and_that_is_the_cost():
    """The measured cost of this mechanism, pinned as a DECISION.

    bash expands nothing inside single quotes: `ls -d '$SB'` names a directory
    literally called `$SB`, executed. This reader cannot tell the two quotings
    apart -- `shlex` runs in posix mode and takes both off, so `git -C '$SB'`
    and `git -C "$SB"` arrive as one token -- and it now answers `/x` for both
    where it used to answer `<cwd>/$SB` for both and was right about the first.

    That is the fail-OPEN direction, and it is accepted rather than closed. It
    needs a directory literally named `$SB`, single-quoted, in a command that
    also assigns `SB`. Closing it means carrying quote provenance out of the
    splitter, which changes how every argument in every command tokenizes.

    Asserting the CURRENT answer rather than the ideal one: if quote
    provenance ever lands, this expectation flips and the flip is the signal.
    """
    assert commits("SB=/x; git -C '$SB' commit -m y") == [(("/x",), SESSION)]


# --- round 1: the reader learned to fill a name and not to empty one ------

FORGETS = [
    # The segment RUNS something, so `_bind` refuses the name -- and refusing
    # to take it is only half. bash has `/two` here and the reader answered
    # `/one`, which is the confident wrong answer the mechanism is bounded to
    # avoid.
    "export SB=/two",
    "declare SB=/two",
    "readonly SB=/two",
    "typeset SB=/two",
    # A construct `understood` rejects. Its effect on a name is no more
    # knowable than its effect on the shell's directory.
    "if true; then SB=/two; fi",
    "for i in 1; do SB=/two; done",
    "while false; do SB=/two; done",
    "eval SB=/two",
    "( SB=/two )",
    # Writes a name with no `=` in the token at all.
    "read SB",
    "read -r SB",
    "mapfile SB",
    "getopts x SB",
    "printf -v SB /two",
    # Round 2: the name-writer check read the segment's FIRST token, so
    # anything in front of the builtin hid it. `IFS= read -r line` is the
    # canonical shell idiom, and `command`/`builtin`/`env` are the spellings
    # that reach past a function of the same name.
    "IFS= read -r SB",
    "command read SB",
    "builtin read SB",
    "env read SB",
    # `unset` does not write a name, it removes one, and to this reader the
    # effect is the same: the earlier value must not survive.
    "unset SB",
    # An assignment operator other than `=`, behind a prefix.
    "export SB+=/two",
    "export SB[0]=/two",
]


def test_a_name_a_segment_may_have_written_is_forgotten():
    """Round 1, and it is a REGRESSION rather than a gap.

    Before this branch every one of these reached the gate as `$SB`, because
    nothing was resolved at all. The branch resolved the first assignment and
    then held it across a segment that may have changed it, so a stop became
    a silence -- measured at the gate, `deny` at the base and `silent` here,
    with bash committing in a repository nothing had reviewed.
    """
    for middle in FORGETS:
        where = targets(f'SB=/one; {middle}; git -C "$SB" commit -m x')
        assert any("$SB" in w for w in where), (
            f"`{middle}` left `/one` standing: {where}. The reader has to "
            "forget a name it cannot follow, not keep the value from before"
        )


def test_the_subshell_refusal_forgets_rather_than_keeps():
    """`_bind`'s own subshell guard, reached directly.

    `( SB=/two )` is caught twice over -- the walk excludes a subshell join
    and `_bind` refuses one of its own accord -- so a mutation to either
    alone leaves the other standing. This calls `_bind` with the tokens, so
    the guard inside it is the only thing answering.
    """
    kept = reader._bind({"SB": "/one"}, shlex.split("( SB=/two )"))
    assert "SB" not in kept, (
        "`_bind`'s subshell guard returned the environment untouched, so a "
        "value from before the subshell survives it. Refusing to take a name "
        "and keeping the old one is the confident wrong answer"
    )
    # And the same for the branch that refuses a segment which runs something.
    kept = reader._bind({"SB": "/one"}, shlex.split("export SB=/two"))
    assert "SB" not in kept


def test_a_conditional_branch_does_not_bind_a_name():
    """`states` and `parked` model a conditional for the DIRECTORY and
    nothing modelled it for a name.

    Measured: `SB=/one; [ -d /nope ] && SB=/two; git -C "$SB" commit`
    answered `/two` where bash has `/one`. The branch may not run, so what it
    assigns is not something this reader can state."""
    for joined in ("&&", "||"):
        where = targets(f'SB=/one; true {joined} SB=/two; git -C "$SB" commit -m x')
        assert any("$SB" in w for w in where), (
            f"a `{joined}` branch bound a name the shell may never have set: {where}"
        )


BINDS = [
    ('SB=/one; git -C "$SB" commit -m x', "/one"),
    ('SB=/one; true; git -C "$SB" commit -m x', "/one"),
    ('SB=/a SB=/b; git -C "$SB" commit -m x', "/b"),
    ('A=/a; B=$A/x; git -C "$B" commit -m x', "/a/x"),
    ('A1=/a; git -C "$A1" commit -m x', "/a"),
]


def test_only_a_bare_name_operand_is_forgotten():
    """The other side of `_forget`'s permissiveness.

    Forgetting costs a prompt and keeping costs a repository nobody reviewed,
    so it leans toward forgetting -- but it must still be reading operands
    rather than dropping the environment whenever a name-writer appears."""
    kept = reader._bind({"SB": "/one"}, shlex.split("read SB.x"))
    assert kept.get("SB") == "/one", (
        "`SB.x` is not the name `SB`, and forgetting on it makes every "
        "name-writer segment a full reset"
    )
    kept = reader._bind({"SB": "/one"}, shlex.split("read OTHER"))
    assert kept.get("SB") == "/one", "a name-writer forgot a name it never named"


def test_forgetting_did_not_take_the_answers_with_it():
    """The other direction. A reader that forgets everything is correct and
    useless, and the shapes that DO resolve are the point of this work."""
    for command, expected in BINDS:
        where = targets(command)
        assert os.path.normpath(expected) in where, (
            f"{command!r} stopped resolving: {where}"
        )


# --- round 3: the wide reset was aimed rather than removed -----------------

# What each of these segments can do to a NAME is nothing: it carries none.
# Executed under bash 3.2.57, `SB=/one; <middle>; printf '%s' "$SB"` prints
# `/one` for every one of them, and every one of them prompted after that change,
# where any segment `understood` refused emptied the environment whole.
KEEPS = [
    "if [ -d /nope ]; then echo hi; fi",
    "if true; then echo hi; fi",
    "while [ -d /nope ]; do echo hi; done",
    "until true; do echo hi; done",
    "for i in a b; do echo $i; done",
    "case x in x) echo hi ;; esac",
    "( echo hi )",
    "{ echo hi; }",
    "pushd /tmp",
    "popd",
    "alias ls=ls",
]


def test_a_refused_segment_that_carries_no_name_keeps_the_environment():
    """Round 3, and the regression is this branch's own.

    An earlier commit on this branch cured a real fail-open -- an `eval` and a sourced script were
    answering with a path bash had left -- by emptying the environment for
    every segment `understood` refused. Six shapes that answered `/one` at
    before it prompted after it, and `if …; then … fi` is the commonest shape
    in a script, in a work item that exists to stop asking.
    """
    for middle in KEEPS:
        where = targets(f'SB=/one; {middle}; git -C "$SB" commit -m x')
        assert where == [os.path.normpath("/one")], (
            f"`{middle}` carries no name and cannot have written one, and the "
            f"reader lost `/one` across it: {where}"
        )


# The other side, and it is the side that decides whether the aim was safe.
# Each of these is a segment `understood` refuses that CAN leave a name
# somewhere this reader cannot state.
UNSEEN_FORGETS = [
    # Text this scan never sees. Asked of every word rather than the first,
    # because a structure word puts it second.
    ('eval "SB=/two"', "eval"),
    ('then eval "$x"', "an eval behind a structure word"),
    (". ./lib.sh", "a sourced script"),
    ("source ./lib.sh", "the other spelling of it"),
    ('trap "SB=/two" EXIT', "a trap, which runs later"),
    ('if eval "$x"; then :; fi', "an eval in a condition"),
    # The command word this process cannot read before expansion -- the same
    # refusal `understood` makes for the DIRECTORY, asked here for the name.
    ("then $cmd SB", "an unreadable command word"),
    # A loop writes the name it iterates, once per iteration, and no `=`
    # appears in the segment for `_forget` to find.
    ("for SB in /two /three; do :; done", "a loop over the name itself"),
    ("for ((SB=0; SB<3; SB++)); do :; done", "the arithmetic loop head"),
    ("select SB in /two; do break; done", "`select`, which writes it too"),
    # A name-writing builtin hidden behind structure. `_forget` asks this of
    # the word that RUNS, which is right where the reader knows what runs;
    # here it does not, so it is asked of every word.
    ("f() { read SB; }", "a definition whose body reads"),
    ("function f { read SB; }", "the other spelling of it"),
    ("while read -r SB; do :; done", "the canonical read loop"),
    ("if IFS= read -r SB; then :; fi", "a read in a condition"),
    # Assignments inside the refused segment, which `_forget` does find.
    ("if true; then SB=/two; fi", "an assignment in a branch that may not run"),
    ("{ SB=/two; }", "a brace group, which writes the parent's name"),
    ("( SB=/two )", "a subshell, which does not -- and is forgotten anyway"),
]


def test_the_aimed_reset_moves_the_gates_verdict_and_only_where_it_should(tmp_path):
    """The reader's answer is not the deliverable; the gate's verdict is.

    Measured on two real repositories, both carrying a routing declaration,
    with the session sitting in one of them. At `b76fd99` all eight shapes
    below returned `deny`, naming a `$SB` the user never typed. Six of them
    carry no name and now return `silent`, which is the answer the same
    command written out has always had. The two that CAN write a name still
    deny, and that is the half of the measurement that matters.
    """
    here = make_repo(tmp_path / "session", opted_in=True)
    there = make_repo(tmp_path / "opted-in", opted_in=True)
    declare_routing(here)
    declare_routing(there)
    for at, shape in enumerate(KEEPS[:6]):
        command = f'SB={sh(there)}; {shape}; git -C "$SB" commit -m x'
        out = run(command, here, session=f"kept{at}")
        assert decision_of(out) == "silent", (
            f"`{shape}` carries no name, `{there}` is declared, and the gate "
            f"asked about a path nobody typed: {reason_of(out)}"
        )
    for at, shape in enumerate(("if [ -d /nope ]; then SB=/two; fi", 'eval "SB=/two"')):
        command = f'SB={sh(there)}; {shape}; git -C "$SB" commit -m x'
        out = run(command, here, session=f"lost{at}")
        assert decision_of(out) == "deny", (
            f"`{shape}` can write the name, and the gate passed a commit "
            "whose repository this reader cannot name"
        )


def test_a_refused_segment_that_can_write_a_name_forgets_it():
    """The aim only holds if what it keeps is what carries no name.

    Every entry here answered `$SB` after that change because everything did.
    Keeping any one of them would answer confidently with a path the shell is
    not in, which is the one failure mode this whole mechanism is bounded to
    avoid.
    """
    for middle, why in UNSEEN_FORGETS:
        where = targets(f'SB=/one; {middle}; git -C "$SB" commit -m x')
        assert any("$SB" in w for w in where), (
            f"{why} -- `{middle}` -- left `/one` standing: {where}"
        )


def test_the_reset_still_empties_the_whole_environment_not_one_name():
    """An `eval` says nothing about which name it wrote, so no name survives
    it. `_forget` would drop what the segment NAMES, and an `eval` names
    nothing -- which is the difference between the two branches."""
    where = targets('SB=/one; OT=/other; eval "$x"; git -C "$OT" commit -m x')
    assert any("$OT" in w for w in where), (
        f"an `eval` left a second name standing: {where}. What it wrote is "
        "not something this reader can narrow to the names it can see"
    )
    # And the aimed branch does NOT empty the second name.
    assert targets('SB=/one; OT=/other; fi; git -C "$OT" commit -m x') == [
        os.path.normpath("/other")
    ]


def test_a_structure_word_does_not_hide_the_command_that_runs():
    """`_runs` reads past the compound-command structure to the word that
    actually runs, and `understood`'s two exceptions come with it: `[` and
    `[[` hold characters `EXPANDS` lists and are conditionals rather than
    globs. Without them `if [ -d <x> ]` empties the environment again, which
    is the shape this round exists to keep."""
    assert reader._runs(shlex.split("then echo hi")) == "echo"
    assert reader._runs(shlex.split("if [ -d /nope ]")) == "["
    assert reader._runs(shlex.split("f() { read SB")) == "read"
    assert reader._runs(shlex.split("fi")) is None
    # `case WORD in` -- the word is data being matched, not a command, so an
    # unreadable one says nothing about what ran.
    assert reader._runs(shlex.split("case $HOME in")) is None


def test_a_name_writer_read_blindly_costs_a_prompt_and_not_an_answer():
    """The cost of asking `NAME_WRITERS` of every word rather than of the
    word that runs. `echo read` writes nothing, and this reader forgets on it
    anyway -- a prompt, which is what the branch gave for everything before.
    It is recorded rather than fixed, because the direction is the safe one."""
    where = targets('SB=/one; then echo read SB; git -C "$SB" commit -m x')
    assert any("$SB" in w for w in where), where


def test_the_pipeline_branch_forgets_and_lastpipe_is_why():
    """Round 2 found nothing reaching this branch: turning it into `pass`
    left the suite green.

    `shopt -s lastpipe` runs a pipeline's last stage in the current shell, so
    `true | SB=/two` writes the parent's `SB` under a setting this process
    cannot see and `SB=/two | true` does not. Which of the two a segment is
    depends on a shell option, so the answer is the one this reader gives for
    anything it cannot state. The cost is one prompt where bash has `/one`.
    """
    for command in (
        'SB=/one; SB=/two | true; git -C "$SB" commit -m x',
        'SB=/one; true | SB=/two; git -C "$SB" commit -m x',
        'SB=/one; SB=/two & git -C "$SB" commit -m x',
    ):
        where = targets(command)
        assert any("$SB" in w for w in where), (
            f"the pipeline branch kept a name across a stage bash runs in a "
            f"subshell -- or wrote one under `lastpipe` that it cannot see: "
            f"{command!r} answered {where}"
        )


def test_the_arithmetic_loop_head_forgets_its_counter_and_not_the_rest():
    """`for ((i=0; i<3; i++))` arrives as the single token `for` `((i=0`, and
    `_name_at` reads a name from the START of a word -- so the `(` comes off
    first. A loop head this reader cannot read a name out of empties the
    environment instead, because which name it writes is not visible."""
    where = targets(
        "SB=/one; OT=/other; for ((SB=0; k<3; k++)); do :; done; "
        'git -C "$OT" commit -m x'
    )
    assert where == [os.path.normpath("/other")], (
        f"the arithmetic head took a name it never wrote with it: {where}"
    )
    # The counter itself, named only in the head. bash leaves `SB` at `3`.
    where = targets(
        'SB=/one; for ((SB=0; k<3; k++)); do :; done; git -C "$SB" commit -m x'
    )
    assert any("$SB" in w for w in where), (
        f"the loop counter kept the value from before the loop: {where}"
    )
    assert reader._unseen({"SB": "/one"}, shlex.split("for $v in a b")) == {}, (
        "a loop head with no readable name left a value standing"
    )


def test_the_blind_sweep_forgets_bare_names_only():
    """`_unseen` asks `NAME_WRITERS` of every word and then forgets the bare
    names beside it. The operand test is `end == len(tok)`, the same line
    `_forget` carries, and loosening it here survived every test while the
    same loosening in `_forget` did not: `read -rp 'SB> ' ans` would forget
    `SB` on the strength of a prompt string. Executed under bash 3.2.57 with
    stdin closed, `SB` is `/one` after it."""
    kept = reader._unseen(
        {"SB": "/one", "ans": "x"}, shlex.split("if read -rp 'SB> ' ans")
    )
    assert kept.get("SB") == "/one", "`SB> ` is not the name `SB`"
    assert "ans" not in kept, "the name the `read` writes survived it"
    where = targets(
        "SB=/one; if read -rp 'SB> ' ans; then :; fi; git -C \"$SB\" commit -m x"
    )
    assert where == [os.path.normpath("/one")], where


# --- a body's later statements are still inside the body -------------------

# Executed under bash 3.2.57: `SB=/one; <middle>; printf '%s' "$SB"` prints
# `/one` for every one of these, because the body never runs -- a false
# condition, an empty list, an arm that does not match, a function defined
# and never called -- or runs in a subshell. Once the reset was aimed the
# reader answered `/three` for all of them: the body's FIRST statement is
# refused with the structure word in front of it, and the SECOND arrives as a
# segment of its own, indistinguishable from a top-level assignment. The wide
# reset had hidden that by accident, because the closer emptied the
# environment, and a closer carries no name. 80 of the 82 fail-opens one
# differential run found against the wide reset were this shape.
BODIES = [
    "if false; then echo hi; SB=/three; fi",
    "if true; then :; else echo hi; SB=/three; fi",
    "while false; do echo hi; SB=/three; done",
    "until true; do echo hi; SB=/three; done",
    "for i in; do echo hi; SB=/three; done",
    "case x in y) echo hi; SB=/three ;; esac",
    "f() { echo hi; SB=/three; }",
    "function f { echo hi; SB=/three; }",
    "( echo hi; SB=/three )",
    "(SB=/two; SB=/three)",
    "if false; then { :; }; SB=/three; fi",
    "if false; then if true; then :; fi; SB=/three; fi",
    # A closer in argument position closes nothing -- bash reads `fi` as a
    # word there, and so does the count. These eight were what was left after
    # the first version counted a closer wherever it stood.
    "if false; then echo fi; SB=/three; fi",
    "f() { echo done; SB=/three; }",
    # The other spellings `_bind` handles, inside a body.
    "if false; then :; export SB=/three; fi",
    "if false; then :; SB+=/x; fi",
    # Round 1 of the re-application. A multi-line `case` puts its arm pattern
    # on a line of its own, and that `a )` is a `)` last in its segment --
    # exactly where a subshell's closer stands. The integer count took it as
    # one and reached zero before the arm body; the stack pops a `)` only when
    # a `(` is on top.
    "case x in\na )\necho hi; SB=/three ;;\nesac",
    "case x in\n(a)\necho hi; SB=/three ;;\nesac",
    "case x in\na)\nSB=/three;;\nesac",
    # The glued spelling: `f(){` is one token, neither in `OPENERS` nor a bare
    # `{`, so nothing opened and the second statement bound.
    "f(){ echo hi; SB=/three; }",
    # A quoted `")"` in argument position, last in its segment, closed the
    # count the same way the arm pattern did.
    'if false; then echo ")"; SB=/three; fi',
    # Nested bodies and an `elif` branch that does not run.
    "if false; then :; elif false; then echo hi; SB=/three; fi",
    "while false; do case x in y) echo hi; SB=/three ;; esac; done",
]


def test_a_bodys_later_statement_is_not_a_top_level_one():
    for middle in BODIES:
        where = targets(f'SB=/one; {middle}; git -C "$SB" commit -m x')
        assert any("$SB" in w for w in where), (
            f"`{middle}` -- a statement inside a body this reader cannot say "
            f"ran was bound as if it were top level: {where}"
        )


def test_the_body_ends_at_its_closer():
    """The count has to come back down, or the aim is lost again one level
    up: every assignment after the first compound command would be forgotten
    and the string would prompt from there on."""
    for command in (
        'SB=/one; if false; then echo hi; SB=/two; fi; SB=/three; git -C "$SB" commit -m x',
        'SB=/one; if false; then { :; }; SB=/two; fi; SB=/three; git -C "$SB" commit -m x',
        'SB=/one; ( echo hi ); SB=/three; git -C "$SB" commit -m x',
        'SB=/one; f() { echo hi; }; SB=/three; git -C "$SB" commit -m x',
        'SB=/one; case x in x) echo hi ;; esac; SB=/three; git -C "$SB" commit -m x',
        # The arithmetic head is not a subshell, so the loop nets to zero.
        'SB=/one; for ((k=0; k<2; k++)); do :; done; SB=/three; git -C "$SB" commit -m x',
        # A closer in argument position is a word, and does not close early.
        'SB=/one; if true; then echo fi; fi; SB=/three; git -C "$SB" commit -m x',
        # Round 1: the multi-line `case` ends at its `esac`, so the stack has
        # to pop `case` there -- with `stack.pop()` removed this one prompts.
        'SB=/one; case x in\na )\necho hi ;;\nesac; SB=/three; git -C "$SB" commit -m x',
        # And an opener outside command position opens nothing, so the
        # everyday shapes round 1 found newly prompting resolve again.
        "SB=/one; grep -c '(' f; SB=/three; git -C \"$SB\" commit -m x",
        'SB=/one; time { echo hi; }; SB=/three; git -C "$SB" commit -m x',
        'SB=/one; if true; then if true; then :; fi; fi; SB=/three; git -C "$SB" commit -m x',
    ):
        assert targets(command) == [os.path.normpath("/three")], command
    # A paren inside a commit message opened a body for the rest of the string.
    where = targets(
        'SB=/one; git commit -m "(wip) x"; SB=/three; git -C "$SB" commit -m x'
    )
    assert os.path.normpath("/three") in where, where


def test_what_opens_a_body_and_what_closes_one():
    def after(segment, stack=()):
        return reader._nesting(shlex.split(segment), list(stack))

    assert after("for ((SB=0") == ["for"]
    assert after("k++))") == []
    assert after("(cd /x") == ["("]
    assert after("case x in x)") == ["case"]
    assert after("( echo hi )") == []
    assert after("} > out", ["{"]) == []
    assert after("echo fi done esac", ["if"]) == ["if"]
    assert after("then if true", ["if"]) == ["if", "if"]
    # A `)` closes only a `(`: a multi-line arm pattern and a quoted `")"`
    # inside a `case` or an `if` close nothing.
    assert after("a )", ["case"]) == ["case"]
    assert after('echo ")"', ["if"]) == ["if"]
    # And every closer pops only its own opener.
    assert after("fi", ["case"]) == ["case"]
    # The glued function head opens a `{` body.
    assert after("f(){ echo hi") == ["{"]
    assert after("function f {") == ["{"]
    # Openers count in command position only.
    assert after('git commit -m "(wip) x"') == []
    assert after("grep -c '(' f") == []
    assert after("time { echo") == ["{"]
    assert after("! ( cd /x )") == []


def test_a_glued_closer_costs_a_prompt_and_not_an_answer():
    """`(cd <x> && make)` arrives as `(cd` … `make)`, and the glued closer is
    not counted because a `case` pattern `x)` looks the same. The count stays
    open and the assignment after it is forgotten -- a prompt where bash has
    `/three`. Recorded as the cost rather than fixed, because the direction is
    the safe one."""
    where = targets('SB=/one; (cd /x && echo hi); SB=/three; git -C "$SB" commit -m x')
    assert any("$SB" in w for w in where), where


def test_a_reserved_word_behind_a_prefix_is_not_a_simple_command():
    """`understood` asked the reserved-word question of the FIRST token only,
    and `!` and `time` are prefixes it steps past. `! for SB in /two /three`
    then reached `_bind` as something that runs, `_forget` found no `=` in
    it, and `/one` stood where bash has `/three`. Two of the 82."""
    assert not reader.understood(shlex.split("! for SB in /two /three"))
    assert not reader.understood(shlex.split("time pushd /x"))
    assert not reader.understood(shlex.split("command pushd /x"))
    # And what the prefixes still pass through.
    assert reader.understood(shlex.split("! true"))
    assert reader.understood(shlex.split("time echo hi"))
    assert reader.understood(shlex.split("command -p ls"))
    for middle in (
        "! for SB in /two /three; do :; done",
        "time for SB in /two; do :; done",
    ):
        where = targets(f'SB=/one; {middle}; git -C "$SB" commit -m x')
        assert any("$SB" in w for w in where), (
            f"`{middle}` kept the value from before the loop: {where}"
        )


# --- round 1 of the re-application: three writers and a call ---------------


def test_an_array_assignment_empties_the_name():
    """`SB=(/three)` makes an array whose `$SB` is `/three`, and the reader
    bound the text between the parens: `git -C "$SB"` composed `(/three)`
    onto the session directory. Unmodelled, so the name is emptied."""
    kept = reader._bind({"SB": "/one"}, shlex.split("SB=(/three)"))
    assert "SB" not in kept, "an array assignment kept the value from before it"
    where = targets('SB=(/three); git -C "$SB" commit -m x')
    assert any("$SB" in w for w in where), where


def test_a_call_to_a_function_the_string_defined_empties_the_environment():
    """`f() { SB=/three; }; SB=/one; f; git -C "$SB"` -- bash `/three`, the
    reader `/one`. The call is a plain word `understood` accepts and `_forget`
    finds nothing in, but the definition is in the same string, so the reader
    has seen the name."""
    for command in (
        'f() { SB=/three; }; SB=/one; f; git -C "$SB" commit -m x',
        'function f { SB=/three; }; SB=/one; OT=/o; f; git -C "$OT" commit -m x',
        'f(){ SB=/three; }; SB=/one; time f; git -C "$SB" commit -m x',
        'f () { SB=/three; }; SB=/one; if true; then f; fi; git -C "$SB" commit -m x',
        'f() { SB=/three; }; SB=/one; true && f; git -C "$SB" commit -m x',
    ):
        where = targets(command)
        assert any("$" in w for w in where), (
            f"{command!r} kept a name the call may have rewritten: {where}"
        )
    # A definition is not a call, and a word never defined here is a word.
    assert targets('f() { SB=/three; }; SB=/one; g; git -C "$SB" commit -m x') == [
        os.path.normpath("/one")
    ]


def test_the_writers_round_one_found_are_forgotten():
    """`((SB=3))`, `let "SB = 3"` and `${SB:=/three}` each write `SB` with no
    `NAME=` at the start of a word. Executed under bash 3.2.57: `SB` is `3`,
    `3` and -- for `:=` on a set name -- `/one`; the reader forgets on all of
    them, which is a prompt and never an answer."""
    for middle in (
        "((SB=3))",
        'let "SB = 3"',
        "let SB++",
        ': "${SB:=/three}"',
        'echo "${SB=/three}"',
        "if ((SB=3)); then :; fi",
        'while let "SB = 3"; do break; done',
        'if true; then : "${SB:=/three}"; fi',
    ):
        where = targets(f'SB=/one; {middle}; git -C "$SB" commit -m x')
        assert any("$SB" in w for w in where), f"`{middle}` kept `/one`: {where}"
    # The operators that read a name without writing it are left standing.
    assert targets(
        'SB=/one; echo "${SB:-/three}" "${#SB}"; git -C "$SB" commit -m x'
    ) == [os.path.normpath("/one")]
