"""The commit gate judged the shell's cwd, not the repository being committed to.

`git -C <repo> commit` names its own repository. The gate resolved everything
from the payload's `cwd` and never read the command, so a commit landing in a
repository that never opted in was gated against whichever repository the shell
happened to be sitting in — and a session testing hooks, which builds a scratch
repository and drives it with `-C` from inside the repository under
development, answered a prompt on every command.

The worktree guard was fixed for this same defect, recorded in the changelog, and its
`-C` parsing is what this gate now reads the target out of.

Reading `-C` opened a second hole (issue #56). The gate sees the command
before the shell expands it, so `git -C "$WT" commit` hands it the literal
characters `$WT` — a directory that does not exist. The gate resolved no
repository there and said nothing, which is indistinguishable from having
checked one and found it clean. Every agent in that release session was
instructed to write exactly that form, and their commits went through
unreviewed. An unresolvable target now stops the commit instead.
"""

import atexit
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
from conftest import decision_of, declare_routing, fired, load_hook_module, run_hook

gate = load_hook_module("commit-review-gate.py", "crg_target")
reader = load_hook_module("cmdline.py", "cmdline_cd")


def sh(path):
    r"""`path` as one shell word.

    These commands are read the way the harness hands them over: a string
    that a POSIX shell is about to run, because the `Bash` matcher in
    `hooks/hooks.json` is the only PreToolUse entry that carries commit
    commands. Interpolating a native path raw made the test string mean
    something else on Windows -- the shell drops an unquoted backslash, so
    `git -C C:\Users\x` arrived at the gate as `C:UsersX` and the
    second target resolved under the first. Nothing about the gate was wrong
    there; the test was writing a command no shell would carry.
    """
    return shlex.quote(str(path))


_GATE_REPO_TEMPLATE = None


def _gate_repo_template():
    """A repo with one commit and a staged change, built once per process --
    `make_repo` is called 57 times in this file, always onto this shape."""
    global _GATE_REPO_TEMPLATE
    if _GATE_REPO_TEMPLATE is None:
        d = Path(tempfile.mkdtemp(prefix="specseal-gate-repo-template-")) / "repo"
        subprocess.run(["git", "init", "-q", str(d)], check=True)

        def git(*a):
            subprocess.run(["git", "-C", str(d), *a], capture_output=True, check=True)

        (d / "f.py").write_text("x = 1\n")
        git("add", "-A")
        git(
            "-c",
            "user.email=e@example.com",
            "-c",
            "user.name=e",
            "commit",
            "-qm",
            "base",
        )
        (d / "f.py").write_text("x = 2\n")
        git("add", "-A")
        atexit.register(shutil.rmtree, d, True)
        _GATE_REPO_TEMPLATE = d
    return _GATE_REPO_TEMPLATE


def make_repo(path, opted_in):
    """A repo with one commit, `seal/` when it opts in, and a staged change."""
    shutil.copytree(_gate_repo_template(), path)
    if opted_in:
        (path / "seal").mkdir()
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


# --- the parsing half -----------------------------------------------------


def test_the_invocation_reports_the_chdir_it_used_to_only_skip():
    found, clean = gate.commit_invocations("git -C /srv/app commit -m x")
    assert clean and len(found) == 1
    assert found[0].args == ["-m", "x"]
    assert found[0].chdirs == ["/srv/app"], (
        "the value that decides WHICH repository the commit lands in was dropped"
    )


def test_a_plain_commit_carries_no_chdir():
    found, _ = gate.commit_invocations("git commit -m x")
    assert found[0].chdirs == []


def test_repeated_chdirs_compose_the_way_git_resolves_them(tmp_path):
    """Measured against git 2.50: `git -C a -C b` lands in `a/b`, not `b`."""
    targets = gate.commit_targets(
        str(tmp_path), gate.commit_invocations("git -C a -C b commit -m x")[0]
    )
    assert [t for t, _ in targets] == [str(tmp_path / "a" / "b")]


def test_each_repository_the_command_commits_to_is_judged(tmp_path):
    """One command can commit twice; the second target must not be lost."""
    targets = gate.commit_targets(
        str(tmp_path),
        gate.commit_invocations(
            f"git commit -m x && git -C {sh(tmp_path / 'o')} commit"
        )[0],
    )
    assert [t for t, _ in targets] == [str(tmp_path), str(tmp_path / "o")]


# --- the shell walk: which directory each segment runs in -----------------


def joined(command):
    """The operator that joined each segment to the one before it."""
    items, clean = reader.split_segments_with_separators(command)
    assert clean, command
    return [sep for sep, _ in items]


def judgment_text(command):
    """`command` as the gate's JUDGMENT read sees it.

    Resolved at call time and tolerant of a `cmdline` that predates the
    function, because these cases are run against older revisions to show
    they were red there. A helper that raises `AttributeError` is not a case
    catching a defect — it is a case that never ran, and counting it as red
    inflates the accounting exactly the way a test that cannot fail inflates
    the green.
    """
    drop = getattr(reader, "drop_heredoc_bodies", None)
    return drop(command) if drop else command


def commit_dirs(command, cwd):
    """Every directory the `git commit` in `command` may run in.

    Through the judgment read, because that is what the gate performs — a
    helper that skipped it would be asking a question no gate asks, and would
    have reported a heredoc body as commands.
    """
    items, clean = reader.split_segments_with_separators(judgment_text(command))
    assert clean, command
    out = []
    for tokens, wheres in reader.walk_directories(items, str(cwd)):
        parsed = reader.parse_git(tokens)
        if parsed and parsed[0] == "commit":
            out.extend(wheres)
    return out


def unreadable(wheres):
    return [isinstance(w, reader.Unresolved) for w in wheres]


def test_the_reader_keeps_the_operator_that_joined_two_segments():
    """`&&` and `||` are opposites in a shell and were indistinguishable here.

    Measured on the unfixed module: all three forms returned
    `[['cd','/tmp/x'], ['git','commit']]`, so a design judging only the `cd`
    destination would judge the wrong repository with confidence on `||`, and
    one judging every reachable directory would keep asking about the
    session's own on `&&`.
    """
    for sep in ("&&", ";", "||", "|"):
        assert joined(f"cd /tmp/x {sep} git commit") == ["", sep], sep


def test_the_old_splitter_answers_exactly_what_it_always_did():
    """Three call sites read the two-element tuple; the separator arrives
    beside it rather than inside it."""
    assert reader.split_segments("cd /tmp/x && git commit") == (
        [["cd", "/tmp/x"], ["git", "commit"]],
        True,
    )


def test_a_cd_carries_the_commit_that_follows_it(tmp_path):
    """`&&` runs the commit only where the `cd` arrived, so B is the answer."""
    assert commit_dirs(f"cd {sh(tmp_path / 'b')} && git commit -m x", tmp_path) == [
        str(tmp_path / "b")
    ]


def test_a_semicolon_carries_the_commit_to_both(tmp_path):
    """`;` is not `&&`, and this loop used to run both through one assertion.

    `;` runs what follows whether the `cd` succeeded or not, so a failed `cd`
    leaves the commit in the directory the shell was already in -- executed:
    `bash -c 'cd /no/such/dir ; pwd'` prints the directory it started in. The
    row was added beside the `&&` one with no grounds and pinned the defect as
    the expected answer; issue #72 names it, and this is the assertion that
    replaces it.
    """
    assert commit_dirs(f"cd {sh(tmp_path / 'b')} ; git commit -m x", tmp_path) == [
        str(tmp_path / "b"),
        str(tmp_path),
    ]


def test_a_relative_cd_composes_against_the_directory_the_shell_is_in(tmp_path):
    assert commit_dirs("cd sub && git commit -m x", tmp_path) == [str(tmp_path / "sub")]


def test_a_command_with_no_cd_still_answers_the_shells_own_directory(tmp_path):
    assert commit_dirs("git commit -m x", tmp_path) == [str(tmp_path)]


def test_or_reaches_the_directory_the_cd_did_not_leave(tmp_path):
    """`cd X || git commit` commits where the shell already was, and the
    session's own directory is what a reader dropping the operator loses."""
    assert commit_dirs(f"cd {sh(tmp_path / 'b')} || git commit -m x", tmp_path) == [
        str(tmp_path),
        str(tmp_path / "b"),
    ]


def test_a_pipeline_does_not_move_the_shell_that_commits(tmp_path):
    """Both sides of a pipeline run in subshells, so a `cd` in one does not
    move the shell the next command runs in.

    Executed: `bash -c 'cd <B> | pwd'` from `<A>` prints `<A>`. The reader
    treated `|` as ordinary sequencing and answered `<B>` alone, so a commit
    landing in the session's own repository was judged against a repository it
    never touches — and where that other repository carried a routing
    declaration, the arm went silent. `&` was already branching for exactly
    this reason; `|` and `|&` have the same property and did not get the same
    answer.
    """
    b = tmp_path / "b"
    for sep in ("|", "|&"):
        got = [
            str(w) for w in commit_dirs(f"cd {sh(b)} {sep} git commit -m x", tmp_path)
        ]
        assert str(tmp_path) in got, f"{sep}: the shell never left {tmp_path}"
        assert str(b) in got, f"{sep}: a shell with `lastpipe` set does land there"


def test_an_operator_at_the_end_of_a_line_is_still_that_operator(tmp_path):
    """A newline behind an operator glued itself onto it.

    The newline is converted to `;` character by character, and shlex groups a
    RUN of punctuation into ONE token — so `cd <B> ||` followed by a newline
    arrived as the single token `||;`, which is in neither `BRANCHING` nor the
    plain-`;` path. Measured tokens: `||;`, `|;`, `&;`.

    Writing the operator at the end of the line is the ordinary way to write a
    long command, so this is the common form rather than a constructed one,
    and it was silent where the commit before this work item stopped it.
    """
    b = tmp_path / "b"
    for sep in ("||", "|", "|&", "&"):
        items, clean = reader.split_segments_with_separators(
            f"cd {sh(b)} {sep}\ngit commit -m x"
        )
        assert clean
        assert [s for s, _ in items] == ["", sep], (
            f"{sep} followed by a newline arrived as one glued token"
        )
        got = [
            str(w) for w in commit_dirs(f"cd {sh(b)} {sep}\ngit commit -m x", tmp_path)
        ]
        assert str(tmp_path) in got, f"{sep}: the session's own directory dropped out"


def test_the_first_operator_after_a_segment_is_the_one_that_binds(tmp_path):
    """`&&` at the end of a line is `&&`, not the newline that follows it."""
    b = tmp_path / "b"
    items, _ = reader.split_segments_with_separators(f"cd {sh(b)} &&\ngit commit -m x")
    assert [s for s, _ in items] == ["", "&&"]


def test_a_branch_that_skips_a_cd_keeps_the_directory_it_skipped_from(tmp_path):
    """`cd N || cd B && git commit` reaches N and B, and the reader kept
    neither of them for the right reason.

    If the first `cd` works the second is skipped and the commit lands in N;
    if it fails the commit lands in B. The union was formed by looking only at
    the operator that FOLLOWS a segment, so the second `cd` overwrote it and N
    stopped being a candidate. A segment joined by a branching operator may
    never run, so the states in front of it have to survive past it.
    """
    n, b = tmp_path / "n", tmp_path / "b"
    got = [
        str(w)
        for w in commit_dirs(f"cd {sh(n)} || cd {sh(b)} && git commit -m x", tmp_path)
    ]
    assert str(n) in got, "the branch where the second cd is skipped"
    assert str(b) in got, "the branch where the first cd failed"


def test_a_heredoc_body_is_data_and_not_commands(tmp_path):
    """Writing a script and then committing it is ordinary, and the script is
    not a command the shell runs.

    A newline was unconditionally a segment separator, so a `cd` written INSIDE
    a heredoc body moved the reader's shell and the commit two lines later was
    judged against a repository the shell never entered. The session's own
    directory was not in the candidate list at all — this is not over-collecting
    and missing, it is being confidently wrong.

    `drop_comments` in the same module exists for the same reason: a JUDGMENT
    read has to drop what the shell will not execute.
    """
    b = tmp_path / "b"
    for opener in ("<<'EOF'", '<<"EOF"', "<<EOF", "<<-EOF"):
        command = (
            f"cat > run.sh {opener}\n"
            f"cd {sh(b)}\n"
            "make\n"
            "EOF\n"
            "git add -A && git commit -m x"
        )
        got = [str(w) for w in commit_dirs(command, tmp_path)]
        assert got == [str(tmp_path)], f"{opener}: {got}"


def test_a_herestring_is_not_a_heredoc(tmp_path):
    """`<<<` feeds one word to stdin and opens no body, so nothing after it
    may be swallowed."""
    got = [str(w) for w in commit_dirs("cat <<<hello\ngit commit -m x", tmp_path)]
    assert got == [str(tmp_path)], got


def test_a_heredoc_that_never_terminates_swallows_the_rest(tmp_path):
    """An unterminated body runs to the end of the input -- `git commit -m x`
    on the last line is swallowed WITH it, not read as a live segment of its
    own the way a naive drop that missed the unterminated case would.

    It still surfaces as a hidden commit needing review (issue #75), the same
    accepted cost as `cat > run.sh <<'EOF' … git commit … EOF`: nothing here
    can tell "cat, so this is data" from "bash, so this runs" without the
    interpreter enumeration issue #75 rejects, so a swallowed body that reads
    as a commit stops whether or not its heredoc ever terminated.
    """
    command = f"cat <<'EOF'\ncd {sh(tmp_path / 'b')}\ngit commit -m x"
    found, _clean = gate.commit_invocations(command, str(tmp_path))
    assert len(found) == 1
    # `gate.Unresolved`, not `reader.Unresolved`: `commit_invocations` wraps
    # the base using the `cmdline` module IT imported, a separate load from
    # this file's own `reader`, so the two classes fail `isinstance` against
    # each other despite naming the same type.
    assert isinstance(found[0].base, gate.Unresolved)
    assert found[0].base.why == gate.Unresolved.CONSTRUCT


def test_a_heredoc_body_does_not_hide_a_commit_that_follows_it(tmp_path):
    """The other direction, so the drop cannot quietly grow: what comes AFTER
    the terminator is a command again."""
    command = "cat > run.sh <<'EOF'\nhello\nEOF\ngit commit -m x"
    found, _clean = gate.commit_invocations(command, str(tmp_path))
    assert len(found) == 1


def test_an_interpreter_fed_heredoc_body_that_commits_stops(tmp_path):
    """issue #75: `bash <<'EOF'` hands its body to a shell that EXECUTES it,
    unlike `cat`, which only reads it as data (the case above). The reader
    cannot tell the two apart without the interpreter enumeration issue #75
    rejects, so a dropped body that reads as a commit stops either way — the
    accepted cost is a stop on a script that WRITES those words without
    running them, covered by `test_a_heredoc_body_is_data_and_not_commands`
    remaining green.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run("bash <<'EOF'\ngit commit -m x\nEOF", here, session="h")
    assert decision_of(out) == "deny", decision_of(out)


def test_an_eval_argument_that_commits_stops(tmp_path):
    """issue #75: `eval 'git commit -m x'` really commits, and the segment's
    own command word is `eval`, not `git` — invisible to `parse_git` before
    this fix. `eval` concatenates its arguments and re-parses the result,
    which is the same question `_hides_a_commit` already answers for a
    dropped heredoc body.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run("eval 'git commit -m x'", here, session="e")
    assert decision_of(out) == "deny", decision_of(out)


def test_a_heredoc_body_mentioning_commit_in_prose_does_not_stop(tmp_path):
    """`_reads_as_commit` reuses `parse_git`'s own rule — a segment's own
    first token must literally be `git` — so a heredoc body that only
    MENTIONS the words does not invent an invocation out of prose."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run(
        "cat > notes.md <<'EOF'\nremember to git commit before lunch\nEOF",
        here,
        session="n",
    )
    assert not fired(out), f"prose inside a heredoc body stopped: {decision_of(out)}"


def test_an_eval_argument_that_does_not_commit_does_not_stop(tmp_path):
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run("eval 'echo hello'", here, session="q")
    assert not fired(out), f"an eval with no commit stopped: {decision_of(out)}"


def test_a_heredoc_nested_inside_a_heredoc_that_commits_stops(tmp_path):
    """issue #75, nesting: `bash <<'OUTER'` feeds its body to a shell that
    executes it, and that body itself opens `bash <<'INNER'` — a second
    interpreter reading a second body from stdin. `_hides_a_commit` used to
    call `drop_heredoc_bodies` on the outer body, which correctly strips the
    inner heredoc but never re-checked what it stripped, so a commit two
    heredocs deep produced no invocation at all.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run(
        "bash <<'OUTER'\nbash <<'INNER'\ngit commit -m x\nINNER\nOUTER",
        here,
        session="nest1",
    )
    assert decision_of(out) == "deny", decision_of(out)


def test_a_bare_eval_of_a_bare_eval_that_commits_stops(tmp_path):
    """`eval eval 'git commit -m x'` really commits twice over: the outer
    `eval` re-parses its arguments into `eval git commit -m x`, itself an
    `eval` invocation. `_eval_argument` peeled one layer and handed
    `_hides_a_commit` a string whose own first segment is `eval`, not `git`
    — nothing recursed into it before this fix.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run("eval eval 'git commit -m x'", here, session="nest2")
    assert decision_of(out) == "deny", decision_of(out)


def test_an_eval_argument_built_from_a_substitution_stops(tmp_path):
    """`eval "$(cat payload)"` and `eval "$CMD"` are ordinary ways to run a
    dynamically-built command, and this process cannot read what the
    substitution or variable expands to — the same fact that already makes
    `git -C "$WT"` Unresolved rather than silently passed.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run('eval "$(cat payload.txt)"', here, session="nest3")
    assert decision_of(out) == "deny", decision_of(out)


def test_the_quoted_heredoc_commit_form_still_parses(tmp_path):
    """The form Claude Code itself writes: the body sits inside `"$(…)"`, so
    the opener is quoted and no body is dropped."""
    command = "git commit -m \"$(cat <<'EOF'\nsubject\n\nbody\nEOF\n)\""
    found, clean = gate.commit_invocations(command, str(tmp_path))
    assert clean and len(found) == 1, (found, clean)


def test_a_failure_branch_survives_an_intervening_segment(tmp_path):
    """`cd <B> && make || git commit` commits where the shell is when the `cd`
    fails, and that is the session's own directory.

    Only the IMMEDIATELY next operator was consulted, so one segment between
    the `cd` and the `||` dropped the failure branch entirely. It is the
    mirror of what round 2's tagging closed, one operator further along.
    """
    b = tmp_path / "b"
    for middle in ("make", "test -f x", "git add -A", "npm run build && lint"):
        got = [
            str(w)
            for w in commit_dirs(f"cd {sh(b)} && {middle} || git commit -m x", tmp_path)
        ]
        assert str(tmp_path) in got, f"{middle}: {got}"


def test_the_common_cross_repository_form_gains_nothing(tmp_path):
    """The cost the other option would have charged, pinned so it cannot be
    paid by accident.

    `cd <repo> && git commit` is the shape this work item exists to make
    silent when the target is declared, and it is the prompt-flood direction
    issue #45 named. Carrying the failure branch must not put the session's
    own directory back into this answer.
    """
    b = tmp_path / "b"
    assert [
        str(w) for w in commit_dirs(f"cd {sh(b)} && git commit -m x", tmp_path)
    ] == [str(b)]
    # The `;` form belongs to `test_a_semicolon_carries_the_commit_to_both`
    # above and not here. `;` runs what follows whether the `cd` worked or
    # not, so a failed `cd` leaves the commit in the session's own directory,
    # and issue #72 closed that — it is a second candidate the reader offers
    # on purpose, not the cost this case exists to keep at zero.


@pytest.mark.parametrize(
    "comment",
    [
        "# stage everything; then commit",
        "git add -A  # stage; then",
        "# do the thing; done",
        "# check if it built; if so commit",
    ],
)
def test_a_comment_is_not_a_construct(tmp_path, comment):
    """The judgment read drops comments, so English in one is not shell.

    A comment segment's first token used to be `#`, which is neither a `cd`
    nor a `git`, so nothing read it and the gate did not need to drop it --
    `hooks/worktree-guard.py` dropped comments and this gate did not, and the
    difference cost nothing. Reading a segment for what CONSTRUCT it is ended
    that: `# stage everything; then commit` splits at the `;`, the next
    segment starts with the reserved word `then`, and an ordinary commit two
    lines later was stopped for a sentence in English.

    Driven through the gate rather than the reader, because the reader is not
    where the two reads diverge -- the gate's own line is.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    declare_routing(here)
    out = run(f"{comment}\ngit commit -m x", here, session="s1")
    assert not fired(out), f"a comment stopped an ordinary commit: {decision_of(out)}"


def test_a_line_continuation_leaves_the_destination_readable(tmp_path):
    """A long command wrapped across lines is the same command.

    An escaped newline survived as a character inside the token, so `cd` read
    as a two-argument `cd` and the destination fell to unreadable. It errs
    toward stopping, but a command that passes on one line was blocked for
    being wrapped.
    """
    b = tmp_path / "b"
    got = commit_dirs(f"cd {sh(b)} \\\n&& git commit -m x", tmp_path)
    assert [str(w) for w in got] == [str(b)], got
    assert not any(isinstance(w, reader.Unresolved) for w in got)


def test_two_exclusive_branches_are_not_walked_as_one(tmp_path):
    """`cd build || cd dist` reaches build OR dist, never `build/dist`.

    The second `cd` was applied to the state the FIRST one produced, so the
    reader offered a directory no run of the command can reach. It is
    fail-closed — an extra candidate is judged rather than missed — but the
    cost is not zero: a composed path exists nowhere, so it enters the
    unreadable partition, and that partition returns before the real verdict
    is used. The phantom then replaces the answer in the prompt.
    """
    got = [
        str(w) for w in commit_dirs("cd build || cd dist && git commit -m x", tmp_path)
    ]
    assert str(tmp_path / "build" / "dist") not in got, (
        "a directory no shell run can reach was offered as a candidate"
    )
    assert str(tmp_path / "build") in got and str(tmp_path / "dist") in got


def test_a_skipped_branch_does_not_execute_the_next_one(tmp_path):
    """The tag that makes the case above work, asserted on its own.

    A state that arrived by a branch that SUCCEEDED must not run a segment
    joined by `||`, and one that arrived by a branch that FAILED must not run
    a segment joined by `&&`.
    """
    got = [
        str(w) for w in commit_dirs("cd a || cd b || cd c && git commit -m x", tmp_path)
    ]
    for name in ("a", "b", "c"):
        assert str(tmp_path / name) in got, name
    assert str(tmp_path) not in got, (
        "with every cd failing the `&&` never runs, so the session's own "
        "directory is not a landing place"
    )
    assert len(got) == 3, got


def test_the_candidate_count_stays_linear_in_the_branches(tmp_path):
    """Measured before the fix: 16 segments produced 65536 candidates and a
    non-git command took 5.8 seconds. Each `||` adds one landing place, so the
    count is the number of branches rather than two to its power."""
    command = " || ".join(f"cd d{i}" for i in range(16)) + " && git commit -m x"
    got = commit_dirs(command, tmp_path)
    assert len(got) <= 20, f"{len(got)} candidates from 16 branches"


def test_a_command_the_reader_cannot_bound_is_unreadable_rather_than_slow(
    tmp_path,
):
    """The cap, which is containment and not a fix.

    Three shapes still multiply, and the candidates in all of them are REAL
    rather than phantom: a chain of pipe stages, where the reader keeps the
    moved directory beside the unmoved one, and chains of `;` or of `&&` and
    `||`, where each one parks a further failure branch. Counting the `cd`
    segments in front of the commit, they reach the cap at seven, seven and
    nine-or-ten — and the pipe chain at six when the commit is joined by `;`,
    which parks a branch at every stage on top of the pipe keeping both. Past
    the cap the whole command reads as a directory the reader could not
    compute, which is the failure direction this module already has — a stop,
    never a guess.
    """
    # Fourteen stages, not forty: without the cap this is 16384 candidates,
    # which the reader still computes in well under a second, so the case
    # FAILS rather than hanging. A red nobody can wait for is not a red.
    command = " | ".join(f"cd d{i}" for i in range(14)) + " ; git commit -m x"
    got = commit_dirs(command, tmp_path)
    assert len(got) <= reader.STATE_CAP
    assert any(isinstance(w, reader.Unresolved) for w in got), (
        "past the cap the answer has to say it is not an answer"
    )


def test_a_pipeline_in_front_of_a_cd_does_not_hide_the_session(tmp_path):
    """The mirror of the case above: the branching operator is BEFORE the
    `cd`, so the `cd` segment itself may never run."""
    b = tmp_path / "b"
    got = [
        str(w)
        for w in commit_dirs(f"echo hi | cd {sh(b)} && git commit -m x", tmp_path)
    ]
    assert str(tmp_path) in got


def test_one_directory_is_named_once(tmp_path):
    """Two ways of reaching the same directory are one candidate, not two.
    `cd N || cd B` reached B from both branches and reported it twice."""
    n, b = tmp_path / "n", tmp_path / "b"
    got = [
        str(w)
        for w in commit_dirs(f"cd {sh(n)} || cd {sh(b)} && git commit -m x", tmp_path)
    ]
    assert len(got) == len(set(got)), got


def test_a_subshell_with_no_subcommand_is_not_a_git_invocation():
    """`parse_git` documents "None when no subcommand", and stripping the
    closing parenthesis could leave the empty string instead — a value that
    reads as a subcommand to anything testing it for identity."""
    assert reader.parse_git(["(", "git", ")"]) is None
    assert reader.parse_git(["(git", ")"]) is None
    assert reader.parse_git(["git"]) is None


def test_a_destination_the_reader_cannot_expand_is_not_a_directory(tmp_path):
    """The gate reads the command BEFORE the shell expands it, which is the
    same fact that made `git -C "$WT"` unresolvable (issue #56)."""
    for dest in ('"$WT"', "'$WT'", "/tmp/x*", "{a,b}"):
        wheres = commit_dirs(f"cd {dest} && git commit -m x", tmp_path)
        assert unreadable(wheres) == [True], dest


def test_a_subshell_does_not_hide_the_cd_by_hiding_the_word(tmp_path):
    """`(cd X && git commit)` tokenizes its first word as `(cd`, so the cd was
    invisible while the commit was not — the fail-open reproduced with one
    parenthesis. Where the commit runs cannot be read, so it is not read."""
    wheres = commit_dirs(f"(cd {sh(tmp_path / 'b')} && git commit -m x)", tmp_path)
    assert wheres and all(unreadable(wheres)), wheres


def test_cd_dash_goes_back_to_the_directory_before_it(tmp_path):
    command = f"cd {sh(tmp_path / 'b')} && cd - && git commit -m x"
    assert commit_dirs(command, tmp_path) == [str(tmp_path)]


def test_cd_dash_with_nothing_behind_it_is_unreadable(tmp_path):
    wheres = commit_dirs("cd - && git commit -m x", tmp_path)
    assert unreadable(wheres) == [True]


def test_an_unreadable_directory_still_says_what_it_could_not_read(tmp_path):
    """The prompt for an unresolved target prints the directories it could
    not identify, so the text has to survive being marked unreadable."""
    (where,) = commit_dirs('cd "$WT" && git commit -m x', tmp_path)
    assert "$WT" in str(where)


def test_an_absolute_chdir_recovers_a_directory_the_reader_had_lost(tmp_path):
    """`-C` with an absolute path does not depend on where the shell is."""
    command = f'cd "$WT" && git -C {sh(tmp_path / "b")} commit -m x'
    found, clean = gate.commit_invocations(command, str(tmp_path))
    assert clean
    targets = gate.commit_targets(str(tmp_path), found)
    assert [str(t) for t, _ in targets] == [str(tmp_path / "b")]
    assert unreadable([t for t, _ in targets]) == [False]


# --- the decision half ----------------------------------------------------


def test_a_commit_aimed_elsewhere_is_judged_there(tmp_path):
    """The measured defect: the prompt belonged to a repo the commit never touches."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    there = make_repo(tmp_path / "scratch", opted_in=False)
    out = run(f"git -C {sh(there)} commit -m 'scratch'", here)
    assert decision_of(out) == "silent", (
        f"the commit lands in {there}, which never opted in; the gate judged the shell"
    )


def test_a_commit_in_the_repository_the_shell_sits_in_still_gates(tmp_path):
    """The fix must not cost the gate its actual job."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    assert fired(run("git commit -m 'change'", here))


def test_the_gate_fires_for_the_named_repository_from_outside(tmp_path):
    """The other direction: the shell is elsewhere and the commit lands in the repo."""
    here = make_repo(tmp_path / "plain", opted_in=False)
    there = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run(f"git -C {sh(there)} commit -m 'change'", here)
    assert fired(out)
    assert (
        "[no-review]"
        in json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    )


def reason_of(out):
    return json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


def test_a_cd_reaches_the_repository_the_commit_lands_in(tmp_path):
    """S1. The measured fail-open: `cd <repo> && git commit` was judged
    against the directory the session started in, so the same commit into the
    same repository was stopped when written with `-C` and silent when
    written with `cd`."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    there = make_repo(tmp_path / "scratch", opted_in=True)
    out = run(f"cd {sh(there)} && git commit -m x", here, session="s1")
    assert fired(out)
    reason = reason_of(out)
    assert str(there) in reason, "the verdict is about the repository the commit misses"
    assert str(here) not in reason


def test_a_cd_inside_one_repository_costs_what_it_always_did(tmp_path):
    """S2. The same-root shortcut, which is what keeps this fix cheap.

    Where every directory the command reaches sits in one repository, the
    operator does not matter and neither does the `cd`: the verdict and the
    prompt are the ones the gate gave before it could read either. Without
    this, `cd src && git commit` — the common harmless form — costs a prompt
    of its own, which is the prompt volume issue #45 exists to reduce.

    This case compares two forms inside ONE build, so a regression that moves
    both is invisible to it. `test_the_same_root_forms_answer_what_the_release_did`
    below is the half that cannot: it drives the LAST RELEASE's gate.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    (here / "src").mkdir()
    plain = run("git commit -m x", here, session="plain")
    walked = run(f"cd {sh(here / 'src')} && git commit -m x", here, session="walked")
    assert decision_of(plain) == decision_of(walked) == "deny"
    assert reason_of(plain) == reason_of(walked), (
        "a cd within one repository changed the prompt the user sees"
    )


def released_hooks(dest):
    """The last release's `hooks/` written into `dest`, and the tag it came from.

    A tag, not a SHA. The reason first given for leaving this unpinned — that
    a hard-coded commit stops resolving once the branch is squashed — is true
    of a SHA and false of a tag, and `git describe --tags --abbrev=0` keeps
    naming "the release this is measured against" after the next release too.
    Read file by file rather than through `tar`, so nothing depends on an
    archive format or on `tarfile`'s extraction filter.
    """
    root = Path(__file__).resolve().parent.parent
    tag = subprocess.run(
        ["git", "-C", str(root), "describe", "--tags", "--abbrev=0", "HEAD"],
        capture_output=True,
        encoding="utf-8",
    ).stdout.strip()
    assert tag, (
        "no tag is reachable from HEAD, so the released gate cannot be built. "
        "A clone without tags cannot answer this and must not read as a pass "
        "— fetch them (`git fetch --tags`, or `fetch-depth: 0` in CI)"
    )
    listing = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "--name-only", tag, "hooks/"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    dest.mkdir(parents=True, exist_ok=True)
    for rel in listing:
        if not rel.endswith((".py", ".json")):
            continue
        blob = subprocess.run(
            ["git", "-C", str(root), "show", f"{tag}:{rel}"],
            capture_output=True,
            check=True,
        ).stdout
        (dest / Path(rel).name).write_bytes(blob)
    return tag


def test_the_same_root_forms_answer_what_the_release_did(tmp_path):
    """The same-root shortcut against the gate people are actually running.

    Six forms whose directories all sit in one repository. Every one has to
    return the same decision AND the same reason text as the last release —
    the reason as well, because that is what the user reads, and a prompt that
    changed wording for a `cd` the release could not even see would be a new
    prompt wearing an old verdict.

    A different session id per revision: the budget marker lives in the
    repository's git dir, so a shared id would make the second run meet the
    `ask` that follows a `deny` and report a difference that is the test's own
    doing.

    One difference is deliberate and is masked rather than tolerated loosely.
    The release resolved the printed root with a `rev-parse --show-toplevel`
    of its own, and git answers with forward slashes on every platform, so on
    Windows it addressed the user in a dialect no Windows path is written in.
    This gate routes that through `optin.repo_root`, which spells the path the
    way the platform does. Caught by CI on the Windows runner, where the two
    spellings are the whole of the difference and the verdicts are identical.

    Masking the path — rather than comparing decisions alone — is what keeps
    the pin able to fail: a wording change anywhere else in the prompt still
    turns it red, which is the property this case was added for.

    WHAT IS COMPARED ACROSS RELEASES, AND WHAT IS NOT. The fear in the
    paragraph above is a prompt that changed *for one form* — the `cd` the
    release could not see getting different words from the plain commit. That
    is a per-form property, and comparing whole texts across releases is a
    coarse way to reach it: it also pins the WAYS-ON list, which is advice and
    is expected to improve. It went red the first time that list gained an
    option, on a change that touched no form at all.

    So the two properties are separated and both are asserted. Across
    releases, per form: the decision and the STATE — the sentences saying what
    is wrong, which is the part a verdict is made of. Across the six forms,
    within each revision: the ENTIRE reason, byte for byte. A prompt that
    changed wording for one form fails the second check whichever release it
    is in, which is the property this case was added for, stated directly
    rather than through a proxy.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    (here / "src").mkdir()
    # The released hooks read the root at its 0.3 address. Both roots are
    # present so each revision sees an opted-in repository, and the comparison
    # stays about the command forms, which is the only thing it is about.
    (here / ".specseal").mkdir()
    old = tmp_path / "released"
    tag = released_hooks(old)

    def released(command, cwd, session):
        r = subprocess.run(
            [sys.executable, str(old / "commit-review-gate.py")],
            input=json.dumps(
                {
                    "tool_name": "Bash",
                    "tool_input": {"command": command},
                    "cwd": str(cwd),
                    "session_id": session,
                }
            ),
            capture_output=True,
            encoding="utf-8",
            timeout=60,
        )
        if not r.stdout.strip():
            return ("silent", "")
        d = json.loads(r.stdout)["hookSpecificOutput"]
        return (d["permissionDecision"], d["permissionDecisionReason"])

    def one_spelling(verdict):
        """`verdict` with the repository's own path reduced to one address."""
        decision, reason = verdict
        native = str(here)
        for spelling in (native, native.replace("\\", "/")):
            reason = reason.replace(spelling, "<repo>")
        return decision, reason

    forms = [
        ("git commit -m x", here),
        (f"cd {sh(here / 'src')} && git commit -m x", here),
        ("cd src && git commit -m x", here),
        ("cd . && git commit -m x", here),
        (f"cd {sh(here)} && git commit -m x", here / "src"),
        ("git -C src commit -m x", here),
    ]

    def state_half(reason):
        """The reason minus its ways-on list.

        The list starts at whichever of the two headers this prompt carries —
        the deny spends its reason on the question, the ask renders buttons.
        A reason with neither RAISES. Returning it whole was the safe-looking
        direction and is the quiet one: the comparison would go back to
        pinning the entire text, which is what this rewrite exists to stop,
        and nothing would say so. Every prompt this gate emits carries one of
        the two headers -- both `question_reason` shapes, `ask_reason`, and
        the unreadable arm's two branches -- so reaching the end means a
        header was reworded, which is exactly when someone needs to look.
        """
        if not reason:
            return reason
        for header in (
            "\n\nDo not choose for the user.",
            "\n\nApproving is the waiver",
        ):
            if header in reason:
                return reason.split(header, 1)[0]
        raise AssertionError(
            "no ways-on header found, so this comparison would silently "
            f"widen back to the whole text: {reason[:200]!r}"
        )

    was_all, now_all = [], []
    for i, (command, cwd) in enumerate(forms):
        was = one_spelling(released(command, cwd, f"rel{i}"))
        now = run(command, cwd, session=f"new{i}")
        now = one_spelling(
            ("silent", "")
            if not now.strip()
            else (
                json.loads(now)["hookSpecificOutput"]["permissionDecision"],
                json.loads(now)["hookSpecificOutput"]["permissionDecisionReason"],
            )
        )
        was_all.append((command, was))
        now_all.append((command, now))
        assert was[0] == now[0], f"{command!r} differs from {tag}: {was[0]} -> {now[0]}"
        assert state_half(was[1]) == state_half(now[1]), (
            f"{command!r}'s STATE differs from {tag}\n"
            f"was: {state_half(was[1])[:200]}\nnow: {state_half(now[1])[:200]}"
        )

    # No form may be told anything the others are not, in either revision.
    for label, group in ((tag, was_all), ("this revision", now_all)):
        first_command, first = group[0]
        for command, verdict in group[1:]:
            assert verdict == first, (
                f"in {label}, {command!r} answers differently from "
                f"{first_command!r}, and both sit in one repository\n"
                f"{first_command!r}: {first[0]} {first[1][:200]}\n"
                f"{command!r}: {verdict[0]} {verdict[1][:200]}"
            )


def test_a_declaration_still_silences_a_cd_within_its_own_repository(tmp_path):
    """The other half of S2: the answer given for this repository still
    answers for a commit that lands in this repository."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    (here / "src").mkdir()
    declare_routing(here)
    assert decision_of(run(f"cd {sh(here / 'src')} && git commit -m x", here)) == (
        "silent"
    )


def test_or_reaches_both_the_session_and_the_destination(tmp_path):
    """S3. `||` runs the commit where the shell already was, and reaches the
    destination only when the `cd` failed. Both are targets, and the operator
    is the only thing that says so."""
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    out = run(f"cd {sh(there)} || git commit -m x", here, session="s1")
    assert fired(out)
    reason = reason_of(out)
    assert str(here) in reason and str(there) in reason
    assert "also commits into" in reason


def test_a_pipeline_does_not_spend_another_repositorys_declaration(tmp_path):
    """The same forgery as S7, reached through a pipeline instead of `&&`.

    Measured before the fix: `cd <B> | git commit` was SILENT where the parent
    commit denied. The commit lands in the session's own repository, which has
    nothing recorded; the declaration that silenced it belongs to `<B>`.
    """
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    declare_routing(there)
    for sep in ("|", "|&"):
        out = run(f"cd {sh(there)} {sep} git commit -m x", here, session=f"pipe{sep}")
        assert fired(out), (
            f"{sep}: {there}'s declaration answered for a commit in {here}"
        )
        assert str(here) in reason_of(out), sep


def test_a_heredoc_body_does_not_spend_another_repositorys_declaration(tmp_path):
    """S7's forgery, reached through a heredoc instead of an operator."""
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    declare_routing(there)
    command = (
        f"cat > run.sh <<'EOF'\ncd {sh(there)}\nmake\nEOF\n"
        "git add -A && git commit -m x"
    )
    out = run(command, here, session="heredoc")
    assert fired(out), f"{there}'s declaration answered for a commit in {here}"
    assert str(here) in reason_of(out)


def test_a_middle_segment_does_not_spend_another_repositorys_declaration(tmp_path):
    """The same forgery, reached by putting one segment between the `cd` and
    the `||` that consumes its failure."""
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    declare_routing(there)
    out = run(f"cd {sh(there)} && make || git commit -m x", here, session="middle")
    assert fired(out)
    assert str(here) in reason_of(out)


def test_a_skipped_branch_still_reaches_the_gate(tmp_path):
    """`cd <N> || cd <B> && git commit` was silent before the fix: only `<B>`
    survived as a candidate, and `<B>` carries a declaration."""
    here = make_repo(tmp_path / "repoA", opted_in=True)
    nowhere = make_repo(tmp_path / "repoN", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    declare_routing(there)
    out = run(
        f"cd {sh(nowhere)} || cd {sh(there)} && git commit -m x", here, session="skip"
    )
    assert fired(out)
    assert str(nowhere) in reason_of(out), "the branch where the second cd is skipped"


def test_a_cd_the_gate_cannot_read_stops_the_commit(tmp_path):
    """S4. The gate reads the command before the shell expands it, so `cd
    "$WT"` names a directory it cannot identify. That is not a repository
    checked and found clean; it joins the partition an unresolvable `-C`
    already has (docs/review-chain-spec.md)."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run('cd "$WT" && git commit -m x', here, session="s1")
    # The parent commit ALSO denies here, for the ordinary reason — it judged
    # the session's own repository, which has no review mark. So the decision
    # alone distinguishes nothing, and the two assertions below are what do:
    # the prompt has to be the unreadable-target one, naming the value it
    # could not expand.
    assert decision_of(out) == "deny"
    reason = reason_of(out)
    assert "$WT" in reason, "the prompt has to name what it could not read"
    assert "could not be read" in reason, (
        "this is the ordinary review prompt, which is what the parent commit "
        "returned — the target was judged rather than reported as unreadable"
    )


def test_the_prompt_offers_the_way_out_that_exists(tmp_path):
    """Two ways a target goes unreadable, and only one of them has a value to
    write out.

    The unreadable-target prompt leads with "write the absolute path in place
    of the unresolved value", which is a real instruction for `cd "$WT"` and
    an impossible one for an `eval` — there is no such value, and the
    directory named is the session's own. Both arms then collapsed onto
    `[no-review]`, which is the standing waiver this gate exists to avoid.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)

    value = reason_of(run('cd "$WT" && git commit -m x', here, session="v"))
    assert "could not resolve to a repository" in value
    assert "Write the path out" in value, value

    construct = reason_of(
        run("eval 'cd /elsewhere' && git commit -m x", here, session="c")
    )
    assert "cannot read as a plain command" in construct, construct
    assert "Say where it commits" in construct, construct
    assert "Write the path out" not in construct, (
        "the construct arm offers an instruction that cannot be followed"
    )


def test_one_directory_is_announced_once(tmp_path):
    """The reader can reach one directory twice, for two different reasons.
    The prompt counts directories, not states.

    `cd "$WT" && eval '…' | git commit` reaches `<cwd>/$WT` as a value that
    could not be expanded and again as a state an `eval` marked, and the
    prompt announced "2 directories" naming the same path twice — the reader's
    bookkeeping leaking into what the user reads.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    reason = reason_of(
        run("cd \"$WT\" && eval 'cd /elsewhere' | git commit -m x", here, session="d")
    )
    first = reason.splitlines()[0]
    assert "2 directories" not in first, first
    assert first.count("$WT") == 1, first


@pytest.mark.parametrize(
    "command",
    [
        "cd \"$WT\" || eval 'cd /elsewhere' || git commit -m x",
        # Both reasons at ONE path. The prompt lists paths once and judges the
        # arm over every target, and only this shape tells the two apart --
        # judging over the deduplicated list gives the construct arm, which
        # says nothing about writing a path out and cannot speak for `$WT`.
        "cd \"$WT\" | eval 'cd /elsewhere' || git commit -m x",
    ],
)
def test_a_command_reaching_both_kinds_does_not_get_the_narrower_prompt(
    tmp_path, command
):
    """One command can reach both, and the prompt has to answer for both.

    `cd "$WT"` leaves a target the reader could not expand and the `eval`
    leaves one it could not follow. The construct wording says nothing about
    writing a path out, so it cannot speak for the value half.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    both = reason_of(run(command, here, session="b"))
    assert "Write the path out" in both, both


def test_a_cd_into_no_repository_stops_rather_than_going_silent(tmp_path):
    """A `cd` names a directory the way a `-C` does, and the stop follows from
    that rather than from the destination looking odd.

    Found by the broad gate, not by design: reading the `cd` while still
    counting only `-C` as "the command named a directory" sent
    `cd sub && git commit` — where `sub` is no repository — to the early
    return in `judge`, which is silence. That is issue #56's fail-open reached
    through the new door, and the case that caught it
    (`tests/test_chain_hooks_hardening.py:91`) predates this work.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run("cd sub && git commit -m x", here, session="s1")
    assert decision_of(out) == "deny"
    assert "sub" in reason_of(out), "the prompt has to name what it could not read"


def test_an_unreadable_cd_says_nothing_where_the_plugin_has_no_standing(tmp_path):
    """Standing comes from the session's own repository, exactly as it does
    for an unreadable `-C`. A globally installed plugin does not prompt in a
    repository that never opted in."""
    here = make_repo(tmp_path / "plain", opted_in=False)
    assert decision_of(run('cd "$WT" && git commit -m x', here, session="s1")) == (
        "silent"
    )


def test_a_subshell_does_not_carry_a_commit_past_the_gate(tmp_path):
    """S5. `(cd <repo> && git commit)` tokenizes its first word as `(cd`, so
    the cd was invisible and the commit was not — the fail-open reproduced
    with one parenthesis."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    there = make_repo(tmp_path / "scratch", opted_in=True)
    declare_routing(here)
    out = run(f"(cd {sh(there)} && git commit -m x)", here, session="s1")
    assert decision_of(out) != "silent", (
        "the declaration in the session's repository carried a commit that "
        "may land in another one"
    )


def test_a_subshell_commit_with_no_trailing_argument_is_still_a_commit(tmp_path):
    """`(git commit)` puts the closing parenthesis on the SUBCOMMAND.

    `parse_git` then read it as `commit)`, no invocation was found, and the
    gate returned before any of this work's walking was used. The `-m x` form
    hides it because the paren attaches to the argument instead — which is
    why the S5 case above passed while this one did not.

    Silent before this change as well, so it is not a regression. It is fixed rather
    than documented as an exception because `spec.md` S5 and
    `docs/review-chain-spec.md` both claim the subshell case is closed, and a
    commit inside a subshell commits for real.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    assert fired(run("(git commit)", here, session="s1")), (
        "a commit wrapped in a bare subshell was invisible to the gate"
    )

    there = make_repo(tmp_path / "scratch", opted_in=True)
    declare_routing(here)
    assert decision_of(run(f"(cd {sh(there)} && git commit)", here, session="s2")) != (
        "silent"
    )


def test_cd_dash_is_judged_where_the_shell_returns_to(tmp_path):
    """S6. The previous directory is state the reader has to carry, and
    carrying it is what keeps an ordinary shell form from stopping."""
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    third = make_repo(tmp_path / "repoC", opted_in=True)

    # Two steps, so the answer is NOT the directory the session started in.
    # A one-step `cd B && cd - && git commit` returns to the session's own
    # repository, which is also what a reader that cannot follow `cd` at all
    # answers — the case passed unchanged on the parent commit and so
    # distinguished nothing.
    out = run(
        f"cd {sh(third)} && cd {sh(there)} && cd - && git commit -m x",
        here,
        session="s1",
    )
    assert fired(out)
    reason = reason_of(out)
    assert str(third) in reason, "the shell returned to repoC, and the verdict follows"
    assert str(here) not in reason, "the session's own repository is not the target"
    assert str(there) not in reason, "the shell came back; the verdict did not"


def test_a_declaration_does_not_travel_to_another_repository(tmp_path):
    """S7. The direction that forges what this project sells.

    `A` was given a routing answer for its own branch. The commit lands in
    `B`, which has no declaration and no review mark. Measured on the unfixed
    gate: the declaration found in `A` made the arm silent, so the commit went
    through unjudged — and there was no moment at which anyone could have
    typed a waiver or clicked a prompt. The same command with `git -C` denied.
    """
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    declare_routing(here)

    assert decision_of(run("git commit -m x", here, session="s1")) == "silent", (
        "the declaration has to keep answering for its own repository"
    )
    out = run(f"cd {sh(there)} && git commit -m x", here, session="s1")
    assert fired(out), "a declaration given for repoA silenced a commit into repoB"
    assert str(there) in reason_of(out)


def test_a_chdir_the_gate_cannot_resolve_stops_the_commit(tmp_path):
    """Issue #56. This used to be silent, and silence was the whole hole.

    A `-C` value that resolves to no repository is not a repository the gate
    checked and found clean. It is a repository the gate never saw. Those had
    the same outcome — nothing — and the second is the one that ships an
    unreviewed commit.

    It reverses `test_a_chdir_to_no_repository_decides_nothing`, which pinned
    the silence as intended behaviour on the grounds that a non-existent path
    is not opted in. That reasoning holds only if the path is what it looks
    like, and the next case shows it need not be.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run(f"git -C {sh(tmp_path / 'nowhere')} commit -m 'x'", here, session="s1")
    assert decision_of(out) == "deny"
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "nowhere" in reason, "the prompt has to name what it could not read"


def test_a_shell_variable_reaches_the_gate_unexpanded(tmp_path):
    """The form every agent in the release session was told to write.

    The hook reads `tool_input.command` before the shell touches it, so the
    `-C` value arrives as the four characters `$WT`. It names no directory,
    and the repository the commit really lands in is never looked at.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    assert fired(run('git -C "$WT" commit -m x', here, session="s1"))


def test_the_marker_still_waives_an_unreadable_target(tmp_path):
    """Both answers have to continue, and the second one is the token."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    out = run('git -C "$WT" commit -m x [no-review]', here, session="s1")
    assert decision_of(out) == "silent"


def test_a_second_attempt_falls_to_the_plain_prompt(tmp_path):
    """The budget is the gate's existing one: deny once per session per repo."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    assert decision_of(run('git -C "$WT" commit -m x', here, session="s2")) == "deny"
    assert decision_of(run('git -C "$WT" commit -m x', here, session="s2")) == "ask"


def test_an_unreadable_target_says_nothing_where_the_plugin_has_no_standing(
    tmp_path,
):
    """A globally installed plugin must not prompt in repositories that never
    opted in. The session's own repository is what gives the gate standing to
    speak about a target it cannot identify — it is not used to judge that
    target, which would answer for a repository the commit may never touch."""
    here = make_repo(tmp_path / "plain", opted_in=False)
    assert decision_of(run('git -C "$WT" commit -m x', here, session="s1")) == "silent"


def test_a_directory_with_the_home_marker_but_no_repository(tmp_path):
    """`seal/` outside a repository is still not an opt-in.

    Two halves, and they now differ. Named by a `-C`, it is a target the gate
    could not resolve, so it stops (above). Sitting in it with no `-C`, there
    is no repository and no command naming one, so there is nothing to stop.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    fake = tmp_path / "looks-opted-in"
    (fake / "seal").mkdir(parents=True)
    assert fired(run(f"git -C {sh(fake)} commit -m 'x'", here, session="s1"))
    assert decision_of(run("git commit -m 'x'", fake, session="s1")) == "silent"


def test_the_prompt_names_the_repository_the_verdict_is_about(tmp_path):
    """Measured: a review run where the session sits marks the WRONG repo.

    Shell in repoA, commit into repoB, both opted in. The mark has to land in
    repoB; a mark in repoA changes nothing. The prompt is the only place that
    can say so, and it used to name no repository at all — so the model ran
    the review in its own cwd, the gate kept stopping the commit, and the
    budget ran out into an `ask` that ships repoB unreviewed on one click.
    """
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    command = f"git -C {sh(there)} commit -m 'change'"

    # The deny carries the options; the `ask` after it carries only the state
    # and the ways on — and the `ask` is the one that ships the commit on a
    # single click, so both have to name the repository.
    first = run(command, here, session="s1")
    assert decision_of(first) == "deny"
    denied = json.loads(first)["hookSpecificOutput"]["permissionDecisionReason"]
    assert f"AGAINST {there}" in denied, "the review is not steered at the target repo"

    after = run(command, here, session="s1")
    assert decision_of(after) == "ask"
    asked = json.loads(after)["hookSpecificOutput"]["permissionDecisionReason"]
    assert f"review chain against {there}" in asked

    # The state is the FIRST paragraph of both reasons and the sentence a
    # person reads before anything else. Asserting the whole reason would let
    # the way on satisfy it alone, so this one looks at the state itself.
    for label, reason in (("deny", denied), ("ask", asked)):
        assert str(there) in reason.split("\n\n")[0], (
            f"the {label} state does not say which repository it is about"
        )


def test_the_parity_arm_names_the_repository_too(tmp_path):
    """The other arm had no case at all, so its address was never read.

    `[no-review]` waives the review arm, leaving the migration-config arm
    alone in the prompt — the same three places have to carry the target.
    """
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    (there / "seal" / "parity.md").write_text("# migration config\n")
    command = f"git -C {sh(there)} commit -m 'change' [no-review]"

    first = run(command, here, session="s1")
    assert decision_of(first) == "deny"
    denied = json.loads(first)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "[no-parity]" in denied, "the review arm was supposed to be waived"
    assert "[no-review]" not in denied
    assert str(there) in denied.split("\n\n")[0], "the state names no repository"
    assert f"in {there}'s migration config" in denied, "the comparison is not steered"

    after = run(command, here, session="s1")
    asked = json.loads(after)["hookSpecificOutput"]["permissionDecisionReason"]
    assert decision_of(after) == "ask"
    assert f"compare {there} against the original" in asked
    assert str(there) in asked.split("\n\n")[0]


def test_a_mark_in_the_shells_repository_does_not_answer_for_the_target(tmp_path):
    """The fact the prompt exists to convey, pinned on its own."""
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)

    def mark(repo):
        gd = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        ).stdout.strip()
        head = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        ).stdout.strip()
        (Path(gd) / "specseal-reviewed").write_text(head)

    command = f"git -C {sh(there)} commit -m 'change'"
    mark(here)
    assert fired(run(command, here)), (
        "a mark in the shell's repo answered for the target"
    )
    mark(there)
    assert decision_of(run(command, here)) == "silent"


def test_a_second_repository_is_announced_in_the_first_prompt(tmp_path):
    """One command, two repositories, one decision — say the next one is coming."""
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    command = f"git commit -m x && git -C {sh(there)} commit -m y"

    # The two decisions mean opposite things. A deny cancels the command, so
    # the retry meets repoB; an approved `ask` runs the command whole —
    # measured, both commits land and repoB is never asked about.
    denied = run(command, here, session="s1")
    assert decision_of(denied) == "deny"
    first = json.loads(denied)["hookSpecificOutput"]["permissionDecisionReason"]
    assert str(there) in first, "the retry meets repoB with no warning it was coming"
    assert "the retry meets the next" in first

    asked = run(command, here, session="s1")
    assert decision_of(asked) == "ask"
    second = json.loads(asked)["hookSpecificOutput"]["permissionDecisionReason"]
    assert str(there) in second
    assert "never asked about separately" in second, (
        "the ask path promises a question that approving makes sure never comes"
    )


def test_the_announcement_names_a_root_not_the_directory_given(tmp_path):
    """The other half of grouping by root, which nothing was holding.

    `test_a_subdirectory_is_not_a_further_repository` pins the merging — that
    no announcement appears. When one DOES appear it has to name the same
    thing the two arms name, which is a repository. Reverting the announcement
    to the directory left every case green.
    """
    here = make_repo(tmp_path / "repoA", opted_in=True)
    there = make_repo(tmp_path / "repoB", opted_in=True)
    (there / "sub").mkdir()
    out = run(f"git commit -m x && git -C {sh(there / 'sub')} commit -m y", here)
    assert fired(out)
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "also commits into" in reason
    assert str(there / "sub") not in reason, (
        "the announcement names a directory where the arms name a repository"
    )
    assert str(there) in reason


def test_a_subdirectory_is_not_a_further_repository(tmp_path):
    """Measured: the announcement named a directory that is no repository.

    `git commit && git -C <repo>/sub commit` names two directories and one
    repository. Grouping by the string judged that repository twice and told
    the user a second one was waiting — a path that `git rev-parse` does not
    call a repository at all.
    """
    here = make_repo(tmp_path / "repoA", opted_in=True)
    (here / "sub").mkdir()
    out = run(f"git commit -m x && git -C {sh(here / 'sub')} commit -m y", here)
    assert fired(out)
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "also commits into" not in reason, (
        "a subdirectory of the same repository was announced as another one"
    )


def test_a_subdirectory_commit_does_not_hide_the_migration_arm(tmp_path):
    """Grouping by root left the group one cwd, and a pathspec needs its own.

    A pathspec is resolved against the directory git runs in. With the group's
    cwd taken from whichever invocation came first, `git -C <repo>/sub commit
    && git -C <repo> commit -m y f.py` looked for `<repo>/sub/f.py`, found
    nothing, and `touches_code` reported a commit carrying no files — so the
    migration-config arm lost its grounds and went silent.

    The review mark is written here, which is the ordinary state of a
    repository that has just been reviewed. That leaves the migration-config
    arm as the only gate, and a commit with no comparison against the original
    went out with no prompt at all.
    """
    repo = tmp_path / "repoP"
    (repo / "seal").mkdir(parents=True)
    (repo / "seal" / "parity.md").write_text("# migration config\n")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)

    def git(*a):
        return subprocess.run(
            ["git", "-C", str(repo), *a],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        ).stdout.strip()

    (repo / "f.py").write_text("x = 1\n")
    git("add", "-A")
    git("-c", "user.email=e@example.com", "-c", "user.name=e", "commit", "-qm", "base")
    (repo / "sub").mkdir()
    # Unstaged on purpose: the pathspec form is then the only view that sees it.
    (repo / "f.py").write_text("x = 2\n")
    Path(git("rev-parse", "--absolute-git-dir"), "specseal-reviewed").write_text(
        git("rev-parse", "HEAD")
    )

    outside = tmp_path / "elsewhere"
    outside.mkdir()
    plain = f"git -C {sh(repo)} commit -m y f.py"
    subdir_first = f"git -C {sh(repo / 'sub')} commit -m x && {plain}"

    assert fired(run(plain, outside)), "the fixture has to reach the parity arm"
    assert fired(run(subdir_first, outside)), (
        "a subdirectory commit in front of it silenced the migration-config arm"
    )


def test_the_worktree_guard_is_no_longer_load_bearing_for_this_gate(tmp_path):
    """The fail-open this file used to pin as a cost is gone, not documented.

    The gate reached `parse_git` and `apply_chdir` by loading
    `hooks/worktree-guard.py` from disk. That load could fail, and the gate
    kept running with no parser at all — which read as "every command is
    unparseable" and produced three wrong answers at once: an unreviewed
    commit aimed at an opted-in repository went silent, a sentence merely
    mentioning git and commit prompted, and `[no-review]` waived from inside
    the commit message through the substring fallback.

    The first of those is the same shape as issue #56 — the gate saying
    nothing for a reason that has nothing to do with review.

    `hooks/cmdline.py` now owns both functions and the guard only re-exports
    them, so this gate imports them by plain name and the guard is not in the
    path at all. Removing the load removed the cost; there was no reason to
    keep paying it to keep the note.
    """
    opted = make_repo(tmp_path / "opted-in", opted_in=True)
    plain = make_repo(tmp_path / "plain", opted_in=False)
    hooks = tmp_path / "hooks"
    shutil.copytree(Path(__file__).resolve().parent.parent / "hooks", hooks)

    def gate(command, cwd):
        r = subprocess.run(
            [sys.executable, str(hooks / "commit-review-gate.py")],
            input=json.dumps(
                {
                    "tool_name": "Bash",
                    "tool_input": {"command": command},
                    "cwd": str(cwd),
                }
            ),
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        return decision_of(r.stdout)

    aimed_at_opted_in = f"git -C {sh(opted)} commit -m x"
    prose = 'echo "remember to git commit later"'
    in_message = "git commit -m 'fix [no-review] later'"

    before = (
        gate(aimed_at_opted_in, plain),
        gate(prose, opted),
        gate(in_message, opted),
    )
    assert before == ("ask", "silent", "ask"), before

    for broken in ("def broken(:\n", None):
        if broken is None:
            (hooks / "worktree-guard.py").unlink()
        else:
            (hooks / "worktree-guard.py").write_text(broken)
        after = (
            gate(aimed_at_opted_in, plain),
            gate(prose, opted),
            gate(in_message, opted),
        )
        assert after == before, (
            f"a broken worktree guard changed this gate's verdicts: {after}"
        )


def test_the_gate_does_not_load_a_sibling_hook_at_all(tmp_path):
    """The mechanism, not just its effect. A later change could reinstate the
    load and leave the case above green by re-exporting the same functions —
    until the day the sibling breaks."""
    source = (
        Path(__file__).resolve().parent.parent / "hooks" / "commit-review-gate.py"
        # Named, because this file's own subject is a tree that does not assume
        # the ambient codepage: the gate's source carries em dashes, and reading it
        # without saying UTF-8 made this case fail on a cp949 console for a reason
        # that had nothing to do with what it asserts.
    ).read_text(encoding="utf-8")
    assert "from cmdline import" in source
    for loader in ("_sibling(", "spec_from_file_location", "importlib"):
        assert loader not in source, f"the gate loads a hook from disk again: {loader}"


def test_a_broken_command_reader_leaves_no_verdict_rather_than_a_wrong_one(tmp_path):
    """`cmdline.py` is imported by name, so a broken one is an ImportError at
    module load and the gate never runs.

    `hooks/dispatch.py` turns that into exit 0 and no output, which reads
    exactly like an allow — the silence this repository already has a rider
    on, at `dispatch.py`'s own `except Exception`. What changed here is that
    it is now the ONLY way the parsing can go missing, instead of one of two.
    A gate that did not load has no verdict; a gate that loaded with no parser
    had three wrong ones.
    """
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    hooks = tmp_path / "hooks"
    shutil.copytree(Path(__file__).resolve().parent.parent / "hooks", hooks)
    payload = json.dumps(
        {
            "tool_name": "Bash",
            "tool_input": {"command": "git commit -m 'change'"},
            "cwd": str(here),
        }
    )

    def dispatch():
        r = subprocess.run(
            [sys.executable, str(hooks / "dispatch.py"), "pre-bash"],
            input=payload,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        return decision_of(r.stdout)

    assert dispatch() == "ask", "the fixture itself has to reach the gate"
    (hooks / "cmdline.py").write_text("def broken(:\n")
    assert dispatch() == "silent", (
        "recorded, not endorsed: dispatch swallows the ImportError and the "
        "absence of a gate reads as an allow"
    )
