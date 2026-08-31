"""Who opened the fixes that closed the last round's findings.

`Pass` answers whether a round's findings are closed. It cannot answer who
read the work that closed them, and for every round but the last the answer
was structural rather than recorded: each verdict needs an answer in the round
that follows, so the round that follows is the reader. The last round has none.

Measured across two consecutive work items in this repository (#33). Round 2
of the first found SEVEN defects inside round 1's own fixes -- a hit rate of
100% on the one set of fixes anybody looked at -- and round 2's fixes then went
in unread, with `- [x] Pass` ticked by the session that wrote them. The work
item after it ended the same way and said so in an HTML comment, which is a
sentence no check can read.

Two things close it and they are pinned separately here.

  the field    `| Fixes checked by |`, with three values and no others, read
               by `chain_check.py` on the LAST record. Only a LATER round may
               be named, so a round cannot certify its own fixes
  the round    a review run ends with a VERIFYING round, spawned after the
               previous round's fixes are committed and targeted at the diff
               of them. A round that opens nothing needing a fix does not
               consume the cap

The prose cases are prose assertions, and prose assertions are worth exactly
what their substrings are chosen to be. Each picks a phrase that cannot
survive the drift it is guarding against.
"""

import json
import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")

ITEM = "specs/1787700000-a-work-item"
ROUNDS = f"{ITEM}/rounds"


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    return " ".join(read(*parts).split())


# --- the field, executed against a real repository --------------------------


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def commit(repo, message):
    git(repo, "add", "-A")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "commit",
        "-qm",
        message,
    )
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def _build(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("checked-by-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def declaration():
    return (
        "# 1787700000-a-work-item — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n"
        "| Branch | feature |\n"
    )


def record(sha, checked_by, verdict="fixed", finding="🟢 1"):
    """A passing round record but for the `Fixes checked by` cell.

    Everything else is deliberately clean -- a checked `Pass`, a reachable
    target, a closed finding -- so a failure can only have come from the one
    row each case is about. `checked_by=None` leaves the row out.
    """
    who = f"| Fixes checked by | {checked_by} |\n" if checked_by is not None else ""
    return (
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n{who}\n"
        "- [x] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        f"| {finding} | something | `f.py:1` | {verdict} | grounds |\n"
    )


def run(repo, draft=None):
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    if draft is not None:
        path = repo / "event.json"
        path.write_text(json.dumps({"pull_request": {"draft": draft}}), "utf-8")
        env["GITHUB_EVENT_PATH"] = str(path)
    r = subprocess.run(
        [sys.executable, CHECK, "--baseline", "base", "--root", str(repo)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env=env,
    )
    return r.returncode, r.stdout + r.stderr


def declared(repo, **rounds):
    """Write the declaration and one record per `roundN=body` keyword."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    for name, body in rounds.items():
        write(repo, f"{ROUNDS}/{name.replace('round', 'round-')}.md", body(sha))
    commit(repo, "rounds")
    return sha


def test_a_record_with_no_such_row_fails(repo):
    """S1. `Pass` cannot answer this, so a record carrying only `Pass` leaves
    the question the field was added for unanswered."""
    declared(repo, round1=lambda sha: record(sha, None))
    code, out = run(repo)
    assert code == 1, out
    assert "Fixes checked by" in out
    assert "who opened the work that closed them" in out, (
        "the failure has to say what the row is FOR — a message naming only "
        "the missing row reads as a schema change nobody explained"
    )


def test_a_later_round_that_exists_is_a_checker(repo):
    """S2. The passing shape, and the one the verifying round writes."""
    declared(
        repo,
        round1=lambda sha: record(sha, "round-2"),
        round2=lambda sha: record(sha, "no fixes to check", verdict="answered"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_a_round_cannot_check_its_own_fixes(repo):
    """S3, and this is issue #33's refusal.

    The fixer and the checker being the same is exactly the state that was
    only ever visible in a transcript.
    """
    declared(repo, round1=lambda sha: record(sha, "round-1"))
    code, out = run(repo)
    assert code == 1, out
    assert "cannot check its own fixes" in out


def test_an_earlier_round_cannot_be_the_checker(repo):
    """S4. A round that ran BEFORE the fixes existed cannot have read them,
    and `round-1` on `round-2.md` is the spelling somebody reaches for when
    the row feels like an ordinary cross-reference."""
    declared(
        repo,
        round1=lambda sha: record(sha, "no fixes to check", verdict="answered"),
        round2=lambda sha: record(sha, "round-1"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "before these fixes existed" in out


def test_a_checker_git_does_not_carry_fails(repo):
    """S5. The claim git can contradict, and the reason the check reads the
    repository instead of the record's word for it."""
    declared(repo, round1=lambda sha: record(sha, "round-4"))
    code, out = run(repo)
    assert code == 1, out
    assert "round-4" in out
    assert "no such record" in out


def test_no_fixes_to_check_passes_when_nothing_closed_on_a_fix(repo):
    """S6. The verifying round's terminal state: a 🟡 answered with grounds
    closes a finding and writes no code for anyone to open."""
    declared(
        repo,
        round1=lambda sha: record(sha, "no fixes to check", verdict="answered"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_no_fixes_to_check_beside_a_fix_fails(repo):
    """S7. A contradiction inside one file, which is the one class of claim
    this check has always refused."""
    declared(repo, round1=lambda sha: record(sha, "no fixes to check"))
    code, out = run(repo)
    assert code == 1, out
    assert "closed on a fix" in out


def test_nobody_with_a_reason_passes_and_says_so(repo):
    """S8, and the trade this release makes rather than hides.

    A run can still ship with its last fixes unopened. What changes is that
    the state is in the diff and printed on every CI run instead of living in
    a session that has ended. Failing for an honest disclosure is what teaches
    people to write none — `unverified_check.py` gives the same reasoning.
    """
    declared(repo, round1=lambda sha: record(sha, "nobody — the run ended here"))
    code, out = run(repo)
    assert code == 0, out
    assert "opened by nobody" in out, (
        "passing in silence would make this the quietest way past the check "
        "that exists, which is what the row was added to stop"
    )


def test_nobody_with_no_reason_fails(repo):
    """S9. Without the reason the cell records that something is missing and
    not what, which is not a disclosure."""
    declared(repo, round1=lambda sha: record(sha, "nobody"))
    code, out = run(repo)
    assert code == 1, out
    assert "does not say why" in out


def test_a_session_is_not_one_of_the_three_values(repo):
    """S10. Read loosely, the answer this field exists to refuse would pass as
    an answer to it."""
    declared(repo, round1=lambda sha: record(sha, "the session that wrote them"))
    code, out = run(repo)
    assert code == 1, out
    assert "none of the three values" in out


def test_a_draft_pull_request_is_excused_the_pass_and_not_this(repo):
    """S11. The two are excused differently because they mean different
    things: an unchecked `Pass` on a draft is a review that has not finished,
    and a checker that does not exist is wrong at every stage of a run."""
    declared(repo, round1=lambda sha: record(sha, "round-9"))
    code, out = run(repo, draft=True)
    assert code == 1, out
    assert "round-9" in out


def test_the_row_is_read_from_git_not_from_the_working_tree(repo):
    """The property the whole file was hardened for: a record committed with
    a bad cell and edited on disk to read well must still fail."""
    declared(repo, round1=lambda sha: record(sha, "round-1"))
    (repo / ROUNDS / "round-1.md").write_text(
        record("0" * 40, "nobody — fixed on disk"), encoding="utf-8"
    )
    code, out = run(repo)
    assert code == 1, out
    assert "cannot check its own fixes" in out


def test_a_cell_inside_a_comment_is_not_the_row(repo):
    """One reader, not two. The template explains the field in a comment
    beside it, and a record that keeps the template's comment must not have
    its explanation read as its answer."""
    body = record("0" * 40, None).replace(
        "- [x] Pass",
        "<!-- | Fixes checked by | round-2 | -->\n\n- [x] Pass",
    )
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", body)
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "Fixes checked by" in out


# --- the field, as every document that describes it spells it ---------------


def test_the_three_values_are_spelled_the_same_everywhere():
    """Four files carry this vocabulary and a fifth enforces it. A value
    spelled one way in the template and another in the check is a record a
    session writes from the template and CI refuses."""
    for parts in (
        ("templates", "sdd-round.md"),
        ("docs", "review-handoff-protocol.md"),
        ("docs", "review-chain-spec.md"),
        ("skills", "code-review", "scripts", "chain_check.py"),
    ):
        text = read(*parts)
        assert "Fixes checked by" in text, "/".join(parts)
        assert "no fixes to check" in text, "/".join(parts)
        assert "nobody" in text, "/".join(parts)


def test_the_template_ships_the_row_and_not_an_answer():
    tpl = read("templates", "sdd-round.md")
    assert "| Fixes checked by |" in tpl
    assert "a LATER round" in tpl, (
        "without this the row reads as an ordinary cross-reference and "
        "`round-1` on round-1.md is what somebody writes"
    )
    assert "| Fixes checked by | round-" not in tpl, "a template must not ship a claim"


def test_the_protocol_carries_the_field_and_moved_its_draft():
    protocol = read("docs", "review-handoff-protocol.md")
    assert "| Fixes checked by |" in protocol
    assert "Draft 0.5" in protocol, "a changed field moves the draft"
    assert "no round after them" in protocol, (
        "the protocol lost WHY the last round is different, which is the half "
        "that stops the field being read as decoration"
    )


def test_the_documents_say_what_nobody_costs():
    """A trade nobody wrote down gets reverted by whoever finds it, and this
    one is the difference between refusing a claim and refusing a state."""
    for parts in (
        ("docs", "review-chain-spec.md"),
        ("skills", "code-review", "scripts", "chain_check.py"),
    ):
        assert "teach" in read(*parts).lower(), "/".join(parts)


# --- the verifying round ----------------------------------------------------


CARRIERS = (
    ("docs", "review-chain-spec.md"),
    ("skills", "code-review", "SKILL.md"),
    ("agents", "warden.md"),
    ("agents", "smith.md"),
)


def test_every_document_that_runs_the_chain_names_the_verifying_round():
    """Four files decide how a run ends and only two are always loaded. One
    of them keeping the old ending is how two answers ship at once."""
    for parts in CARRIERS:
        assert "verifying round" in flat(*parts), "/".join(parts)


def test_the_verifying_rounds_target_is_the_previous_rounds_fixes():
    """Which is what makes it bounded, and the reason it is not option C of
    issue #33: the surface is a diff rather than a branch."""
    for parts in CARRIERS:
        text = flat(*parts)
        assert "diff of" in text and "fixes" in text, "/".join(parts)


def test_the_cap_counts_rounds_that_found_something():
    """The cap could not tell a round that found nothing from a round whose
    fixes nobody read, and it ended the run at both."""
    for parts in (("docs", "review-chain-spec.md"), ("agents", "smith.md")):
        text = flat(*parts)
        assert "does not consume the cap" in text, "/".join(parts)


def test_the_spec_says_the_verifying_round_cannot_loop():
    """A rule that lifts a bound has to say why nothing runs away, or the
    next reader adds a second bound to be safe."""
    spec = flat("docs", "review-chain-spec.md")
    assert "Nothing here can loop" in spec
    assert "by definition the last one" in spec


def test_the_condition_is_not_that_the_round_found_nothing():
    """Option C was rejected. A verifying round that raises a 🟡 the smith
    answers with grounds has opened nothing needing a fix, and the run ends
    there — without this sentence the rule reads as C and gets built as C."""
    spec = flat("docs", "review-chain-spec.md")
    assert "wrote no code nobody read" in spec


def test_the_orchestrator_is_told_when_to_spawn_it():
    """`code-review` is what the session running the chain reads. A rule
    stated only in the policy reaches the reader who went looking for it."""
    skill = flat("skills", "code-review", "SKILL.md")
    assert "after the fixes" in skill, (
        "the ordering is the whole of option A — a verifying round spawned "
        "before the fixes land reviews the thing that was already reviewed"
    )


def test_the_reviewer_knows_a_diff_can_be_its_target():
    """The warden's scope rules are written for a branch. A round whose
    target is a diff has to be a shape it recognises, or it widens."""
    warden = flat("agents", "warden.md")
    assert "verifying round" in warden
    assert "not new findings" in warden or "rather than new findings" in warden


def test_the_smiths_account_of_the_bound_matches_the_spec():
    """`agents/smith.md` states the bound for a session that never opens the
    policy. Round 3 of the previous work item is what happens when two
    documents describe one rule and only one of them is updated."""
    smith = flat("agents", "smith.md")
    assert "three rounds" in smith
    assert "verifying round" in smith


def test_the_check_can_fail():
    """Every prose assertion above is a substring, and a substring test that
    cannot go red is a comment. This is the mutation, run in-process."""
    text = flat("docs", "review-chain-spec.md")
    assert "verifying round" in text
    assert "verifying round" not in text.replace("verifying round", "")
