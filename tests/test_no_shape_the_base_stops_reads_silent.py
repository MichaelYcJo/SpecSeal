"""Every command the release branch's commit gate stops still stops, with the
person's `automation` press and without it.

Work item `1790644505` changes WHO a stop is put to in a session whose person
pressed `automation`: the model, by a `deny`, instead of the person, by an
`ask`. It changes nothing about WHETHER the gate stops. That is the owner's
constraint for the work: no command shape may read silent where
`release/v0.16.0`'s gate judges it, because a false silent is a real commit
nobody judged, and that is worse than a prompt.

The corpus below is the shapes that were measured to leak the last time the
reading was narrowed. Work item `1790635415` tried two narrowings, trusting an
existing `cd` target not to fail and reading a heredoc body fed to a known
interpreter as data, and its rounds 2 and 3 each found commands that the
narrowed gate read silent while a real bash ran the commit. Those rounds'
tables (`seal/specs/1790635415-a-gate-that-fails-to-load-says-so/rounds/
round-2-report.md` and `round-3-report.md`, on
`fix/28-a-gate-that-fails-to-load-says-so`) are rebuilt here row by row,
controls included, beside the four shapes that prompted the person in the
measured run and #662's reverse direction.

Each command is issued twice without the press and twice with it, in a fresh
session each way, because the base answers a first stop and a later one
differently. None of the four answers may be silence. The case passes on the
base, where the press is never read; it went red when the press branch was
mutated to return silence (`phases/phase-1.md` of the work item records the
run).
"""

import io
import json
import os
import shlex
import subprocess
import sys

import pytest
from conftest import declare_routing, load_hook_module
from test_the_guard_asks_once_per_session import ask_entries, write_transcript

gate = load_hook_module("commit-review-gate.py", "crg_no_new_silent")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hooks"))
import cmdline  # noqa: E402  -- the plain name both gates import
import worktree_consent  # noqa: E402  -- the plain name the gate imports

# A program that hands its stdin to a shell, which is what makes a heredoc
# body a command rather than data. Round 2 ran each with a body that created a
# file, and the file existed afterwards.
PY = "import os,sys; os.system(sys.stdin.read())"
PERL = 'system(join("",<STDIN>))'
BODY = "git commit -m x"


def q(text):
    return shlex.quote(str(text))


def heredoc(head, delimiter="EOF"):
    return f"{head}\n{BODY}\n{delimiter}"


def make_repo(path, declared=False):
    """An opted-in repository with one commit and a staged change."""
    path.mkdir(parents=True)
    run = lambda *a: subprocess.run(
        ["git", "-C", str(path), *a], check=True, capture_output=True
    )
    run("init", "-q")
    (path / "f").write_text("1\n")
    run("add", "f")
    run("-c", "user.email=e@example.com", "-c", "user.name=e", "commit", "-qm", "b")
    (path / "f").write_text("2\n")
    run("add", "f")
    (path / "seal").mkdir()
    if declared:
        declare_routing(path)
    return path


@pytest.fixture
def projects(monkeypatch, tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    monkeypatch.setattr(worktree_consent, "PROJECTS_ROOT", str(root))
    return root


def decisions(monkeypatch, capsys, command, cwd, session):
    """The gate's decision for `command`, issued twice in one session."""
    out = []
    for _ in range(2):
        payload = {
            "tool_name": "Bash",
            "tool_input": {"command": command},
            "cwd": str(cwd),
            "session_id": session,
        }
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
        gate.main()
        printed = capsys.readouterr().out.strip()
        out.append(
            json.loads(printed)["hookSpecificOutput"]["permissionDecision"]
            if printed
            else "silent"
        )
    return out


def with_and_without_the_press(monkeypatch, capsys, projects, command, cwd):
    write_transcript(projects, "pressed", ask_entries(cwd))
    assert worktree_consent.automation_answered(str(cwd), "pressed"), (
        "the fixture's press is not read, so the pressed half tests nothing"
    )
    return {
        "plain": decisions(monkeypatch, capsys, command, cwd, "plain"),
        "pressed": decisions(monkeypatch, capsys, command, cwd, "pressed"),
    }


def corpus(w, m, h):
    """(where it was measured, command). The session directory is opted in and
    undeclared, and `w` is a declared repository. `m` and `h` are the other
    paths the round-3 rows name."""
    return [
        # Round 2, red 1: the interpreter's program comes from somewhere
        # other than stdin, so the body is input to a program that runs it.
        (
            "r2: a program flag after the heredoc",
            heredoc(f"python3 <<'EOF' -c {q(PY)}"),
        ),
        ("r2: a bundled -Bc", heredoc(f"python3 -Bc{q(PY)} <<'EOF'")),
        ("r2: perl -e after the heredoc", heredoc(f"perl <<'EOF' -e {q(PERL)}")),
        ("r2: $(...) before the interpreter", heredoc("sh -s $(true) python3 <<'EOF'")),
        ("r2: ${...;...} before it", heredoc("sh -s ${x:-;X=} python3 - <<'EOF'")),
        ("r2: >& before the interpreter", heredoc("sh -s >&python3 <<'EOF'")),
        ("r2: control, bash reads stdin", heredoc("bash <<'EOF'")),
        ("r2: control, -c before the heredoc", heredoc(f"python3 -c {q(PY)} <<'EOF'")),
        # Round 2, yellow 2: an earlier segment moves or locks the `cd`
        # target, so the `cd` fails and the commit runs where the shell began.
        ("r2: mv, then cd", f"mv {q(w)} {q(m)} ; cd {q(w)} ; {BODY}"),
        ("r2: mv, then cd, on lines", f"mv {q(w)} {q(m)}\ncd {q(w)}\n{BODY}"),
        ("r2: chmod, then cd", f"chmod 000 {q(w)} ; cd {q(w)} ; {BODY}"),
        ("r2: control, a missing cd", f"cd {q(m)} ; {BODY}"),
        # Round 3, red 1: a `#` glued to the delimiter is literal to the
        # shell, and the flags after it run.
        (
            "r3: # glued to the delimiter",
            heredoc(f"python3 <<EOF#x -c {q(PY)}", "EOF#x"),
        ),
        ("r3: # glued, quoted", heredoc(f"python3 <<'EOF'#x -c {q(PY)}", "EOF#x")),
        ("r3: perl, # glued", heredoc(f"perl <<EOF#x -e {q(PERL)}", "EOF#x")),
        ("r3: control, genuinely data", heredoc("python3 - <<EOF#x", "EOF#x")),
        # Round 3, red 2: an assignment-shaped prefix runs before the `cd`,
        # or is no assignment at all and the `cd` never runs.
        ("r3: $(...) in a prefix", f"X=$(mv {q(w)} {q(m)}) cd {q(w)} ; {BODY}"),
        ("r3: an invalid name prefix", f"a.b=1 cd {q(w)} ; {BODY}"),
        (
            "r3: a prefix, then a cd",
            f"X=$(mv {q(w)} {q(m)}) cd {q(h)} ; cd {q(w)} ; {BODY}",
        ),
        ("r3: control, cd then ;", f"cd {q(w)} ; {BODY}"),
        # The four that prompted the person in session ab2760f5, rebuilt.
        (
            "measured: a heredoc edit, then a commit on the next line",
            f"cd {q(w)} && python3 - <<'EOF'\nprint(1)\nEOF\ngit add f && {BODY}",
        ),
        (
            "measured: ; after cd, no heredoc",
            f"cd {q(w)} && true ; git add f && {BODY}",
        ),
        (
            "measured: a patch whose body loops over a commit string",
            f"cd {q(w)} && python3 - <<'EOF'\ns = 'don\\'t'\n"
            f"for c in ['cd {w}; {BODY}']:\n    print(c)\nEOF",
        ),
        (
            "measured: a body line equal to the delimiter ends it early",
            f"cat > note.md <<'EOF'\nquoted:\nEOF\n{BODY}\nEOF",
        ),
        # Round 1 of 1790644505: a commit the #669/#670 reading finds in `w`,
        # then a string the splitter cannot close (`$'…'` with an escaped
        # quote), then a commit where the shell is. The base judged the
        # session's directory for the unread rest; a commit found in `w`
        # used to take that judgment away.
        (
            "r1: nice -C w, then $'…'",
            f"nice git -C {q(w)} commit -m x; echo $'it\\'s'; {BODY}",
        ),
        (
            "r1: do -C w, then $'…'",
            f"for d in a; do git -C {q(w)} commit -m x; done; echo $'it\\'s'; {BODY}",
        ),
        (
            "r1: cd w && nice, then $'…'",
            f"cd {q(w)} && nice {BODY}; echo $'it\\'s'; {BODY}",
        ),
        (
            "r1: timeout -C w, then $'…'",
            f"timeout 5 git -C {q(w)} commit -m x; echo $'it\\'s'; {BODY}",
        ),
        # Nested past the reader's recursion: a gate that raises is silence.
        (
            "r1: 500 nested substitutions",
            f"{BODY}; echo " + "$(" * 500 + "true" + ")" * 500,
        ),
    ]


def test_no_shape_the_base_stops_reads_silent(monkeypatch, capsys, projects, tmp_path):
    session = make_repo(tmp_path / "session")
    w = make_repo(tmp_path / "w", declared=True)
    shapes = corpus(w, tmp_path / "m", tmp_path)
    silent = []
    for name, command in shapes:
        for which, answers in with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        ).items():
            if "silent" in answers:
                silent.append(f"{name} [{which}]: {answers}")
        # Each shape meets a fresh budget, so its first answer is a first.
        for marker in (session / ".git" / "specseal-commit-choice").glob("*"):
            marker.unlink()
    assert not silent, "a command the base stops reads silent:\n" + "\n".join(silent)


def test_a_parity_arm_is_not_waived_by_a_newly_read_commit(
    monkeypatch, capsys, projects, tmp_path
):
    """Round 1 of 1790644505. `[no-review]` waives an unresolved target whole,
    and the base's fallback for a command the splitter could not finish still
    judged the session's own directory, whose parity arm `[no-review]` does
    not answer. A commit the #670 reading found in a substitution or a shell
    string used to take that fallback away."""
    session = make_repo(tmp_path / "session", declared=True)
    (session / "seal" / "parity.md").write_text("# parity\n")
    (session / "a.py").write_text("x = 1\n")
    subprocess.run(["git", "-C", str(session), "add", "a.py"], check=True)
    for command in (
        f": '[no-review]'; echo $({BODY}) $'it\\'s'",
        f": '[no-review]'; sh -c '{BODY}'; echo $'it\\'s'",
    ):
        answers = with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        )
        for which, got in answers.items():
            assert "silent" not in got, (command, which, got)


def test_a_commit_found_before_a_nesting_too_deep_still_stops(
    monkeypatch, capsys, projects, tmp_path
):
    """Round 2 of 1790644505. A reader that overflows on 500 nested
    substitutions used to discard the commit it had already found in `u`,
    leaving only the declared session directory to judge."""
    session = make_repo(tmp_path / "session", declared=True)
    u = make_repo(tmp_path / "u")
    deep = "$(" * 500 + "true" + ")" * 500
    for command in (
        f"git -C {q(u)} commit -m x; echo {deep}",
        f"cd {q(u)} && {BODY}; echo {deep}",
        f"git -C {q(u)} commit -m x; echo " + "$(echo " * 500 + "1" + ")" * 500,
    ):
        answers = with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        )
        for which, got in answers.items():
            assert "silent" not in got, (command[:60], which, got)


def test_a_cd_behind_a_redirection_is_not_read_as_staying_put(
    monkeypatch, capsys, projects, tmp_path
):
    """#674, `spec.md` W1. From a declared session directory, `2>/dev/null cd
    U && git commit` commits in U, which declares nothing. At `86256492` the
    walk did not see a `cd` behind the redirection and read the shell as
    staying where it was, so the commit was judged against the session's
    declaration alone and was silent. A `cd` behind a prefix was already
    refused as unreadable; a redirection is one more thing in front of it."""
    session = make_repo(tmp_path / "session", declared=True)
    u = make_repo(tmp_path / "u")
    for command in (
        f"2>/dev/null cd {q(u)} && {BODY}",
        f"2> /dev/null cd {q(u)} && {BODY}",
        f">/dev/null pushd {q(u)} && {BODY}",
        f"time 2>/dev/null cd {q(u)} && {BODY}",
    ):
        answers = with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        )
        for which, got in answers.items():
            assert "silent" not in got, (command, which, got)


NESTINGS = {
    "$(": ("$(echo ", ")"),
    "<(": ("<(cat ", ")"),
    '"$(': ('"$(echo ', ')"'),
}


@pytest.mark.parametrize("kind", sorted(NESTINGS))
def test_a_deep_nesting_is_read_to_a_bound(monkeypatch, kind):
    """#674, `spec.md` S9. A body nested inside another is read to
    `NESTING_READ` levels and then counts as one that might commit, instead of
    being read until the interpreter's recursion limit answers. At
    `86256492` the reader rescanned the rest of the body some 330 times before
    `RecursionError`, which took thirty seconds on 4000 levels."""
    opener, closer = NESTINGS[kind]
    text = opener * 4000 + "true" + closer * 4000
    calls = []
    original = gate._reads_a_commit

    def counting(body):
        calls.append(1)
        return original(body)

    monkeypatch.setattr(gate, "_reads_a_commit", counting)
    assert gate._hides_a_commit(text) is True
    # Exactly the bound: a count below it means the recursion limit answered
    # first, which is the reliance contract §13 distrusts, and a count above
    # it means the bound did not hold.
    assert len(calls) == gate.NESTING_READ, len(calls)


def test_the_reverse_direction_still_stops(monkeypatch, capsys, projects, tmp_path):
    """#662's second box. From a declared session directory, `cd U ; git
    commit` also reaches U whenever the `cd` works, and U declares nothing."""
    session = make_repo(tmp_path / "session", declared=True)
    u = make_repo(tmp_path / "u")
    answers = with_and_without_the_press(
        monkeypatch, capsys, projects, f"cd {q(u)} ; {BODY}", session
    )
    for which, got in answers.items():
        assert "silent" not in got, (which, got)


W1_PREFIXES = [
    "2>/dev/null cd sub &&",
    ">/dev/null pushd sub &&",
    ">/dev/null source /dev/null;",
    "2>/dev/null eval true;",
    "2>/dev/null $CMD;",
    "<<<x cd sub &&",
    "X=1 2>/dev/null cd sub &&",
    "time 2>/dev/null cd sub &&",
]


@pytest.mark.parametrize("prefix", W1_PREFIXES)
def test_w1_keeps_the_directory_the_base_judged_under_a_waiver(
    monkeypatch, capsys, projects, tmp_path, prefix
):
    """Round 1 of 1790660768, red 1. W1's refusal REPLACED the directory the
    base judged with an unresolved one, and `[no-review]` waives an
    unresolved target whole -- so the parity arm the base judged in the
    session's directory went silent, while bash commits there."""
    session = make_repo(tmp_path / "session", declared=True)
    (session / "sub").mkdir(exist_ok=True)
    (session / "seal" / "parity.md").write_text("# parity\n")
    (session / "a.py").write_text("x = 1\n")
    subprocess.run(["git", "-C", str(session), "add", "a.py"], check=True)
    command = f": '[no-review]'; {prefix} {BODY}"
    for which, got in with_and_without_the_press(
        monkeypatch, capsys, projects, command, session
    ).items():
        assert "silent" not in got, (command, which, got)


@pytest.mark.parametrize(
    "shape",
    [
        ">/dev/null source /dev/null; cd u2 && {body}",
        "2>/dev/null eval true; cd u2 && {body}",
        "2>/dev/null cd .; cd u2 && {body}",
        'SB={u2}; 2>/dev/null source /dev/null; git -C "$SB" commit -m x',
    ],
)
def test_w1_keeps_the_directory_the_base_judged_outside_an_opted_in_session(
    monkeypatch, capsys, tmp_path, shape
):
    """Round 1 of 1790660768, red 1. From a directory that is not opted in, an
    unresolved target is silence, and a later relative `cd`, or a name bound
    before the refused segment, stays unresolved behind it. The base resolved
    `u2`, which is opted in, and bash commits there."""
    plain = tmp_path / "plain"
    plain.mkdir()
    u2 = make_repo(plain / "u2")
    command = shape.format(body=BODY, u2=q(u2))
    got = decisions(monkeypatch, capsys, command, plain, "s")
    assert "silent" not in got, (command, got)


@pytest.mark.parametrize("header", ["case a in a) ", "f() { ", "coproc "])
def test_past_the_header_bound_the_reading_stops(header):
    """Round 1 of 1790660768, red 2. Past `HEADERS_READ` headers, one inside
    the next, both header readings answer in the stopping direction; one
    header fewer, the same segment is read to its end and names nothing."""

    bound = cmdline.HEADERS_READ
    for depth, expected in ((bound - 1, False), (bound, True)):
        tokens = (header * depth + "true watch").split()
        assert cmdline._is_the_program(tokens, len(tokens) - 1) is expected, depth
        assert cmdline.names_an_unknown_command(header * depth + "true") is expected


@pytest.mark.parametrize("header", ["case a in a) ", "f() { ", "coproc "])
def test_a_deep_header_nesting_keeps_the_commits_found(
    monkeypatch, capsys, projects, tmp_path, header
):
    """Round 1 of 1790660768, red 2. The header readings recursed once per
    header, so 1,200 of them raised `RecursionError` past `_hides_a_commit`
    into `main`, which dropped the commit already found in `u`."""
    session = make_repo(tmp_path / "session", declared=True)
    u = make_repo(tmp_path / "u")
    for command in (
        f"cd {q(u)} && {BODY}; sh -c '" + header * 1200 + "true'",
        f"git -C {q(u)} commit -m x; " + header * 1200 + "watch -g x",
    ):
        for which, got in with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        ).items():
            assert "silent" not in got, (command[:60], which, got)
