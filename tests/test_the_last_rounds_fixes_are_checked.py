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

import importlib.util
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
    """S2. The passing shape a finished run writes: round 1 names round 2 as
    what opened its fixes, and round 2 is the verifying round that opened
    nothing needing one.

    This case is why the field is read on EVERY record. Read on the last one
    alone, `round-N` is unreachable — a checker has to be later and the last
    record has none — and the first version of this test stayed green under a
    mutation that broke the lookup entirely, because round 1's cell was never
    opened.
    """
    declared(
        repo,
        round1=lambda sha: record(sha, "round-2"),
        round2=lambda sha: record(sha, "no fixes to check", verdict="answered"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_an_earlier_record_missing_the_row_fails(repo):
    """S2b. The scope, from the other side: a chain whose last record is
    honest and whose round 1 says nothing is still a chain with an unanswered
    round."""
    declared(
        repo,
        round1=lambda sha: record(sha, None),
        round2=lambda sha: record(sha, "no fixes to check", verdict="answered"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "round-1.md" in out


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


# --- the verdict cell as this repository actually spells it -----------------
#
# `CLOSED_WORDS` and `FIX_WORDS` are spelled bare and no round record is. Every
# closed verdict in `specs/*/rounds/round-*.md` reads `**fixed**`, usually with
# the commit that closed it beside the word, so the normalizer that lowercased
# and stripped a full stop matched none of them. The three cases below pin both
# directions of that gap and the one reading that must NOT change.

BOLD_FIX = "**fixed** `abc123d`"
BOLD_FIX_WITH_TAIL = "**fixed** `abc123d`, closed by a final commit"
# A long `answered` cell that mentions a fix made elsewhere. The shape is one
# this repository already writes — `answered, and **sharpened** in `96a1ae3` —
# …` on `round-2.md` — with a fix word in it, which is what makes it able to
# fail. A reader that looked for a fix word ANYWHERE in the cell would call
# this round's own work a fix and refuse `no fixes to check` beside it, which
# is the value's own terminal state.
ANSWERED_MENTIONING_A_FIX = (
    "answered — the finding it confirms was **fixed** in `abc123d`, and this "
    "row is the confirmation rather than more work"
)


@pytest.mark.parametrize("verdict", [BOLD_FIX, BOLD_FIX_WITH_TAIL])
def test_a_fix_word_in_bold_beside_its_commit_is_a_fix(repo, verdict):
    """The refusal that had never once fired.

    `no fixes to check` beside `**fixed** `abc123d`` is the same
    contradiction-inside-one-file as `no fixes to check` beside a bare
    `fixed`, and until the normalizer saw through emphasis and the citation it
    was the spelling every record in this repository used.
    """
    declared(repo, round1=lambda sha: record(sha, "no fixes to check", verdict))
    code, out = run(repo)
    assert code == 1, out
    assert "closed on a fix" in out


def test_a_blocking_finding_closed_in_bold_is_closed(repo):
    """The same normalizer, in the direction that fails safe.

    A 🔴 closed as `**fixed** `abc123d`` read as still open, so a record whose
    blocking finding was genuinely fixed failed its own `Pass`. The work item
    here is one the grandfathering clause covers, so `nobody` is a notice and
    the only thing that can fail this record is the verdict cell.
    """
    declared(
        repo,
        round1=lambda sha: record(
            sha, "nobody — the run ended here", BOLD_FIX, finding="🔴 1"
        ),
    )
    code, out = run(repo)
    assert code == 0, out


def test_an_answered_cell_that_mentions_a_fix_is_not_a_fix(repo):
    """The cut is AT the citation, not a search for a fix word inside the cell.

    A reader scanning for `fixed` anywhere would find `sharpened in `abc123d``
    here and refuse a record whose round wrote no code at all. This is the
    reading the normalizer must not acquire while it gains the two above.
    """
    declared(
        repo,
        round1=lambda sha: record(sha, "no fixes to check", ANSWERED_MENTIONING_A_FIX),
    )
    code, out = run(repo)
    assert code == 0, out


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
    its explanation read as its answer.

    The commented row is on a line of its own, starting with a pipe, because
    that is what a template's example looks like and it is the only shape a
    reader that skipped `strip_comments` would actually pick up. Its value is
    a VALID one, and the record's verdict closes without a fix, so a reader
    that saw the comment would exit 0 rather than exit 1 for a different
    reason — the first version of this case put `round-2` there and stayed
    green under its own mutation, because a checker that does not exist fails
    too.
    """
    body = record("0" * 40, None, verdict="answered").replace(
        "- [x] Pass",
        "<!--\n| Fixes checked by | no fixes to check |\n-->\n\n- [x] Pass",
    )
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", body)
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "no `| Fixes checked by" in out


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


def test_the_protocol_carries_the_field_and_moved_its_draft():
    protocol = read("docs", "review-handoff-protocol.md")
    assert "| Fixes checked by |" in protocol
    assert "Draft 0.5" in protocol, "a changed field moves the draft"
    assert "no round after them" in protocol, (
        "the protocol lost WHY the last round is different, which is the half "
        "that stops the field being read as decoration"
    )


# The trade each document has to state, and the needle has to be unique to the
# section that states it. `teaches people to write none` was the first
# spelling and it has sat at `chain_check.py:82` since the initial commit,
# about a different gate: deleting the whole 45-line FIXES CHECKED BY section
# left this case green. A needle that survives deleting what it guards is
# worth nothing, and this case's own docstring had already said so about a
# shorter spelling.
NOBODY_COSTS = {
    ("docs", "review-chain-spec.md"): "teaches people to write none",
    ("skills", "code-review", "scripts", "chain_check.py"): (
        "can still ship with its final fixes unopened"
    ),
}


@pytest.mark.parametrize("parts", sorted(NOBODY_COSTS))
def test_the_documents_say_what_nobody_costs(parts):
    """A trade nobody wrote down gets reverted by whoever finds it, and this
    one is the difference between refusing a claim and refusing a state."""
    text = flat(*parts)
    assert "honest" in text, "/".join(parts)
    assert NOBODY_COSTS[parts] in text, "/".join(parts)


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


# Option A is prose in four documents and nothing in the code enforces it, so
# these cases are the whole of what holds it. A needle that is merely PRESENT
# holds nothing: `"diff of" in text and "fixes" in text` stayed green with
# BOTH of option A's axes inverted — spawn before the fixes, target the whole
# branch — because `fixes` appears four to eighteen times in every carrier.
#
# So each rule is pinned as the whole row or the whole sentence that states
# it, and beside it the spellings an inversion would have to produce. The
# positive is what refuses a rewrite; the negative is what refuses a document
# that keeps the sentence and states the opposite somewhere else.

WHEN_SPAWNED = {
    ("docs", "review-chain-spec.md"): (
        "It is spawned after the previous round's fixes are committed, its "
        "target is the diff of those fixes, and its job is the answers rather "
        "than new findings"
    ),
    ("skills", "code-review", "SKILL.md"): (
        "| When | **after the fixes** for the previous round are committed — "
        "never before, or it reviews what has already been reviewed |"
    ),
    ("agents", "warden.md"): (
        "it is spawned after the previous round's fixes are committed, and "
        "its target is the diff of those fixes rather than the branch"
    ),
    ("agents", "smith.md"): (
        "spawned after your fixes are committed, targeted at the diff of "
        "those fixes, asking whether each closed finding is actually closed"
    ),
}
SPAWNED_BACKWARDS = (
    "spawned before",
    "before the previous round's fixes are committed",
    "before your fixes are committed",
    "**before the fixes**",
)

WHAT_IT_TARGETS = {
    ("docs", "review-chain-spec.md"): (
        "| Target | the branch, or what the prompt narrows it to | the diff "
        "of the previous round's fixes |"
    ),
    ("skills", "code-review", "SKILL.md"): (
        "| Target | the **diff of those fixes**, not the branch. That is what "
        "keeps it bounded: it is the cheapest round of the run |"
    ),
    ("agents", "warden.md"): (
        "its target is the diff of those fixes rather than the branch"
    ),
    ("agents", "smith.md"): "targeted at the diff of those fixes",
}
TARGETED_BACKWARDS = (
    "target is the branch",
    "targeted at the branch",
    "the whole branch",
    "the diff of those fixes rather than the branch, or the branch",
)

# The warden carries no cap rule and is not in this one: whether a round ends
# the run is the orchestrator's arithmetic, and the reviewer's part is saying
# whether it opened anything.
CAP_RULE = {
    ("docs", "review-chain-spec.md"): (
        "**A round that opens nothing needing a fix does not consume the "
        "cap.** The cap counts rounds that found something"
    ),
    ("skills", "code-review", "SKILL.md"): (
        "**A round that opens nothing needing a fix does not consume the "
        "cap.** The cap counts rounds that found something"
    ),
    ("agents", "smith.md"): (
        "A round that opens nothing needing a fix **does not consume the "
        "cap**, because the cap counts rounds that found something"
    ),
}
CAP_BACKWARDS = (
    "does consume the cap",
    "still consumes the cap",
    "consumes the cap like every other",
)


@pytest.mark.parametrize("parts", sorted(WHEN_SPAWNED))
def test_the_verifying_round_is_spawned_after_the_fixes(parts):
    """Spawned before them, it reviews the commit the previous round already
    reviewed — the round happens, costs a spawn, and reads nothing new."""
    text = flat(*parts)
    assert WHEN_SPAWNED[parts] in text, "/".join(parts)
    for backwards in SPAWNED_BACKWARDS:
        assert backwards not in text, f"{'/'.join(parts)}: {backwards}"


@pytest.mark.parametrize("parts", sorted(WHAT_IT_TARGETS))
def test_the_verifying_rounds_target_is_the_previous_rounds_fixes(parts):
    """Which is what makes it bounded, and the reason it is not option C of
    issue #33: the surface is a diff rather than a branch. Widened back to the
    branch it is an ordinary round, and the run gains a full walk it was
    promised it would not pay for."""
    text = flat(*parts)
    assert WHAT_IT_TARGETS[parts] in text, "/".join(parts)
    for backwards in TARGETED_BACKWARDS:
        assert backwards not in text, f"{'/'.join(parts)}: {backwards}"


@pytest.mark.parametrize("parts", sorted(CAP_RULE))
def test_the_cap_counts_rounds_that_found_something(parts):
    """The cap could not tell a round that found nothing from a round whose
    fixes nobody read, and it ended the run at both. Inverted, the verifying
    round costs a round the run does not have and the ending it was built to
    replace comes straight back."""
    text = flat(*parts)
    assert CAP_RULE[parts] in text, "/".join(parts)
    for backwards in CAP_BACKWARDS:
        assert backwards not in text, f"{'/'.join(parts)}: {backwards}"


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


def test_the_reviewer_knows_a_diff_can_be_its_target():
    """The warden's scope rules are written for a branch. A round whose
    target is a diff has to be a shape it recognises, or it widens."""
    warden = flat("agents", "warden.md")
    assert "verifying round" in warden
    assert "not new findings" in warden or "rather than new findings" in warden


def test_the_smiths_account_of_the_bound_matches_the_spec():
    """`agents/smith.md` states the bound for a session that never opens the
    policy. Round 3 of the previous work item is what happens when two
    documents describe one rule and only one of them is updated.

    Both numbers and both conditions, as one sentence. `three rounds` alone
    left the second half free: the ceiling could move, or stop being tied to
    an open 🔴, and this case would not have noticed.
    """
    smith = flat("agents", "smith.md")
    assert (
        "**three rounds, then it ends whether or not everything was "
        "resolved; five while a 🔴 is open, and only to close it**" in smith
    )
    assert "verifying round" in smith
    spec = flat("docs", "review-chain-spec.md")
    assert "Rounds are capped at **three**, and at **five while a 🔴 is open**." in spec


def reader_module():
    """`unverified_check.py`, the same module `chain_check` loads.

    One reader, not two. `strip_comments` decides what counts as a row here
    exactly as it does when the check reads a record, and a second
    implementation in this file would be free to drift from it.
    """
    path = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")
    spec = importlib.util.spec_from_file_location("specseal_reader_for_tests", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_template_row_is_a_row_and_not_an_explanation():
    """The row a session copies, pinned as a row and as a placeholder.

    Counting raw lines counted the explanation as a row, so the whole field
    could be moved INSIDE the comment block beside the table and the count
    stayed at one — while `chain_check` reads a commented row as absent, which
    `test_a_cell_inside_a_comment_is_not_the_row` pins from the other side. A
    template whose only mention is commented ships a record that fails the
    moment it is written.

    The value is pinned too. `test_the_three_values_are_spelled_the_same_
    everywhere` reads the whole file, comments included, so `no fixes to
    check` could be misspelled in the row and left right in the paragraph
    below it, and every case stayed green.
    """
    lines = reader_module().strip_comments(
        read("templates", "sdd-round.md").splitlines()
    )
    rows = [line for line in lines if line.strip().startswith("| Fixes checked by")]
    assert len(rows) == 1, (
        f"the template's field table has {len(rows)} such rows outside its "
        "comments — a row a session cannot copy is not a row"
    )
    value = rows[0].split("|")[2].strip()
    assert value.startswith("<") and value.endswith(">"), (
        f"a template must not ship a claim, and `{value}` is one"
    )
    assert "a LATER round" in value, (
        "without this the row reads as an ordinary cross-reference and "
        "`round-1` on round-1.md is what somebody writes"
    )
    for spelling in ("`round-<N>`", "`no fixes to check`", "`nobody — <why>`"):
        assert spelling in value, (
            f"the row offers no `{spelling}`, so a session writing from this "
            "template writes a value `chain_check.py` refuses"
        )
