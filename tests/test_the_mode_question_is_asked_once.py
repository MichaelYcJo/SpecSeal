"""A root nobody chose a mode for is a state something names.

Issue #151, reported from a monorepo on its first work item under SpecSeal:
the session created `seal/` and started working. Nothing asked about shared or
local mode, and nothing asked the migration question.

Three files each said something correct and the three together left no route
to the question. `hooks/optin.py` says the root's existence IS the
declaration; `skills/implement/SKILL.md` §Bootstrap says the mode question is
asked there and nowhere else; and the preset block in `CLAUDE.md` — which
`install.sh` copies into `~/.claude/CLAUDE.md`, so it loads in every project on
the machine — tells a session to write `seal/specs/<id>/routing.md` before the
first edit. That write creates `seal/`. Creating `seal/` opts the repository
in. The question lived in a skill the session had no reason to load.

This file pins the half that OBSERVES it. `tests/test_first_setup_asks_once.py`
pins the half that points at it — the preset sentence, and the bootstrap the
sentence sends a session to.

The scenario ids are `seal/specs/1788817289-local-mode-from-first-setup-to-
the-gate/spec.md`'s. Every case was written before `hooks/mode-gate.py` and
`hooks/config.py` existed and seen red — as a collection error, which is a
red this file's own first case makes explicit rather than leaving to a reader
to trust.
"""

import importlib.util
import json
import os
import subprocess

import pytest
from conftest import decision_of, load_hook_module, local_home, run_hook

GATE = "mode-gate.py"


@pytest.fixture
def config():
    return load_hook_module("config.py", "specseal_config_for_tests")


def payload(cmd, repo, session="s1", tool="Bash", **extra):
    p = {
        "tool_name": tool,
        "session_id": session,
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }
    p.update(extra)
    return p


def git_dir(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def opt_in_shared(repo):
    (repo / "seal").mkdir(exist_ok=True)
    return repo / "seal"


def write_config(home, text):
    with open(os.path.join(str(home), "config.md"), "w", encoding="utf-8") as f:
        f.write(text)


TABLE = "# Repository config\n\n| Item | Value |\n|---|---|\n{rows}"


def reason_of(out):
    return json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


# --- the reader: one parser for the Mode row -------------------------------


def test_the_row_is_read_from_the_root_the_folder_is_at(config, repo):
    """The reader answers for whichever root exists, so a local-mode
    repository is not read as one that declared nothing."""
    home = local_home(repo)
    write_config(home, TABLE.format(rows="| Mode | local |\n"))
    assert config.declared_mode(str(home)) == ("mode", "local")


@pytest.mark.parametrize(
    "text, expected",
    [
        (None, ("none", "")),
        (TABLE.format(rows="| Record language | Korean |\n"), ("none", "")),
        (TABLE.format(rows="| Mode |  |\n"), ("none", "")),
        ("not a table at all\n", ("none", "")),
        (TABLE.format(rows="| Mode | SHARED |\n"), ("mode", "shared")),
        (TABLE.format(rows="| Mode | whatever |\n"), ("unknown", "whatever")),
    ],
)
def test_the_four_spellings_of_undeclared_are_one_answer(config, repo, text, expected):
    """The same four `seal.py#declared` already had, because it is the same
    reader — moved, not rewritten. A row that names no mode is told apart from
    no row, because a claim nobody can act on is not the same as no claim."""
    home = opt_in_shared(repo)
    if text is not None:
        write_config(home, text)
    assert config.declared_mode(str(home)) == expected


def test_rows_above_the_header_are_not_rows_of_this_table(config, repo):
    """A mutation survived here, and the branch it broke is the one the
    docstring's whole claim rests on: the header is this table's furniture
    ABOVE its first row. Without it a `| Mode | local |` written into some
    other table earlier in the file — an example, a comparison — is read as
    the declaration.

    Uncovered because it arrived uncovered. The parser moved here from
    `seal.py`, and the suite that looks like its home,
    `tests/test_the_pull_request_language_is_the_repositorys.py`, carries a
    second copy of the loop rather than calling this one."""
    home = opt_in_shared(repo)
    write_config(
        home,
        "# Repository config\n\n"
        "An example of what NOT to write:\n\n"
        "| Mode | local |\n\n"
        "| Item | Value |\n|---|---|\n| Mode | shared |\n",
    )
    assert config.declared_mode(str(home)) == ("mode", "shared")


def test_the_command_and_the_gate_read_one_parser(config):
    """`seal mode` writes the row and the gate reads it. Two readers of one
    table is how a file passes one and fails the other; `seal.py` re-exports
    this one rather than keeping a copy."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(root, "skills", "implement", "scripts", "seal.py")
    spec = importlib.util.spec_from_file_location("specseal_seal_one_parser", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # By where the code was COMPILED, not by object identity: this test loads
    # `hooks/config.py` under a name of its own, so the two module objects
    # differ while the implementation behind them must not.
    owner = os.path.join("hooks", "config.py")
    for name in ("declared", "config_rows", "config_path"):
        where = getattr(module, name).__code__.co_filename
        assert where.endswith(owner), f"seal.{name} is compiled from {where}"
    assert config.declared_mode.__code__.co_filename.endswith(owner)


# --- S7-S10: the gate ------------------------------------------------------


def test_a_root_with_no_recorded_mode_is_named(repo):
    """S7. The state #151 is about: a root exists and nobody was asked."""
    opt_in_shared(repo)
    out = run_hook(GATE, payload("git commit -m x", repo))
    assert decision_of(out) == "deny"
    said = reason_of(out)
    assert "AskUserQuestion" in said
    assert "seal mode" in said
    assert "seal mode local" in said and "seal mode shared" in said


def test_the_prompt_says_what_each_answer_costs(repo):
    """Every answer has to continue (`implement` §1). Both do something and
    the prompt says which — one records where the folder already is, the other
    moves it."""
    opt_in_shared(repo)
    said = reason_of(run_hook(GATE, payload("git commit -m x", repo)))
    assert "committed" in said
    assert str(repo / "seal") in said


def test_a_recorded_mode_is_silent(repo):
    """S8. The row is the answer, so the question stops."""
    write_config(opt_in_shared(repo), TABLE.format(rows="| Mode | shared |\n"))
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "silent"


def test_a_local_root_with_a_recorded_mode_is_silent(repo):
    """The same, read at the other place. A gate that only looked at
    `<repo>/seal/` would nag every local-mode repository forever."""
    write_config(local_home(repo), TABLE.format(rows="| Mode | local |\n"))
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "silent"


def test_a_repository_with_no_root_is_silent(repo):
    """S9. A globally installed plugin must not nag a repository that never
    opted in — the rule `hooks/optin.py` exists to hold."""
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "silent"


def test_the_question_arrives_on_the_first_command_not_at_the_commit(repo):
    """The budget decided this, not the act #151 names. Scoping the gate to a
    commit puts the question beside the review arm's, at minute thirty, on a
    session that may have nobody at the keyboard — and `implement` §1 says the
    cost of a question is when it arrives. The count is the same either way,
    because the budget below is per session rather than per command."""
    opt_in_shared(repo)
    assert decision_of(run_hook(GATE, payload("ls -la", repo))) == "deny"


def test_the_second_attempt_in_a_session_only_asks(repo):
    """S10. A deny that repeats is an outage: nothing in an unattended run can
    get past it. The budget is one deny per session per repository, and `ask`
    is approvable."""
    opt_in_shared(repo)
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "deny"
    out = run_hook(GATE, payload("git commit -m x", repo))
    assert decision_of(out) == "ask"
    assert "seal mode" in reason_of(out)


def test_a_different_session_is_asked_too(repo):
    """The budget is per session, like the answer it spends. A session that
    never saw the question has not been asked it."""
    opt_in_shared(repo)
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "deny"
    assert (
        decision_of(run_hook(GATE, payload("git commit -m x", repo, session="s2")))
        == "deny"
    )


def test_an_unwritable_marker_counts_as_already_asked(repo):
    """The rule the chain spec states, and the direction matters: inverted,
    the deny repeats forever in exactly the environments that cannot write."""
    opt_in_shared(repo)
    with open(
        os.path.join(git_dir(repo), "specseal-mode-choice"), "w", encoding="utf-8"
    ) as f:
        f.write("not a directory")
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "ask"


def test_a_session_id_with_separators_stays_inside_the_git_dir(repo):
    """The id names a file. Measured on a sibling guard: `../../escaped` put
    an empty file at the repository root."""
    opt_in_shared(repo)
    run_hook(GATE, payload("git commit -m x", repo, session="../../escaped"))
    assert not (repo / "escaped").exists()


def test_the_subject_is_the_session_s_repository(repo, tmp_path):
    """`git -C <elsewhere>` moves git and does not move the session. Its
    sibling gate resolves the repository a COMMIT lands in, because a verdict
    about a change has to be about the repository that change reaches. This is
    not a verdict about a change: it is a fact about the workspace the session
    is sitting in, and that workspace is the one with the unrecorded root."""
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "-C", str(other), "init", "-q"], check=True)
    opt_in_shared(repo)
    out = run_hook(GATE, payload(f"git -C {other} commit -m x", repo))
    assert decision_of(out) == "deny", out
    assert str(repo) in reason_of(out)


def test_a_session_in_a_subdirectory_is_still_asked(repo):
    """A mutation survived here too, and it is the ordinary case: sessions sit
    in `src/` as often as at the top. Taking `cwd` for the repository root
    makes the gate look for `<cwd>/seal/`, find nothing, and go quiet for
    every session that is not at the top — silence that reads exactly like a
    repository with the row already written."""
    opt_in_shared(repo)
    sub = repo / "src"
    sub.mkdir()
    out = run_hook(GATE, payload("ls", sub))
    assert decision_of(out) == "deny", out
    said = reason_of(out)
    assert str(repo / "seal") in said
    assert str(sub) not in said, "the prompt names the subdirectory as the root"


def test_a_repository_that_is_not_this_one_is_not_judged(repo, tmp_path):
    """The other half of the same rule: a session sitting OUTSIDE an opted-in
    repository hears nothing about it, whatever its commands mention."""
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "-C", str(other), "init", "-q"], check=True)
    opt_in_shared(repo)
    assert (
        decision_of(run_hook(GATE, payload(f"git -C {repo} commit -m x", other)))
        == "silent"
    )


def test_the_gate_is_in_the_pre_bash_group():
    """A gate `hooks/hooks.json` never reaches decides nothing. The dispatch
    group is the wiring, and it is the half a passing gate cannot report on."""
    dispatch = load_hook_module("dispatch.py", "specseal_dispatch_for_mode_gate")
    assert GATE in dispatch.GROUPS["pre-bash"]
