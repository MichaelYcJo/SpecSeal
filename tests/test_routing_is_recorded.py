"""The routing answer is recorded, so the gate stops re-deriving it.

The answer to "does this work go through the review chain" is given before the
first edit. Nothing received it, so the gate re-derived it at every commit from
the absence of a review mark -- a mark that only exists after a review passes.
Every commit of every round was stopped on its way to the reviewer the answer
had already named.

A declaration under `.specseal/routing/` is what the gate reads instead.
Enforcement does not disappear; it moves to the pull request, where CI checks a
branch that said "through the chain" against its review record.

Failure direction: a declaration that cannot be read is not a declaration. The
gate falls back to what it does today rather than falling silent, because a
gate a corrupt file switches off is the standing waiver the chain spec forbids.
"""

import json
import os
import subprocess

from conftest import decision_of, fired, load_hook_module, run_hook

routing = load_hook_module("routing.py", "specseal_routing")

CHAIN = "through the review chain"
DIRECT = "straight to the PR"


def payload(cmd, repo, session="s1", **extra):
    p = {
        "tool_name": "Bash",
        "session_id": session,
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }
    p.update(extra)
    return p


def opt_in(repo):
    (repo / ".specseal").mkdir(exist_ok=True)


def branch_of(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def declare(
    repo,
    review=CHAIN,
    destination="open the pull request",
    branch=None,
    item="1787708604-a-work-item",
    body=None,
    implementation=None,
):
    """Write a routing declaration, or arbitrary `body` when given.

    `implementation` is left out by default, which is what every declaration
    written before that axis existed looks like.
    """
    d = repo / "specs" / item
    d.mkdir(parents=True, exist_ok=True)
    if body is None:
        third = f"| Implementation | {implementation} |\n" if implementation else ""
        body = (
            f"# {item} -- routing\n\n"
            "| Axis | Answer |\n"
            "|---|---|\n"
            f"| Review | {review} |\n"
            f"| Destination | {destination} |\n"
            f"{third}"
            f"| Branch | {branch or branch_of(repo)} |\n"
        )
    path = d / "routing.md"
    path.write_text(body, encoding="utf-8")
    return path


def two_axis_text(branch="feature/x"):
    """A declaration in the shape every one written before the third axis had."""
    return (
        "| Axis | Answer |\n|---|---|\n"
        f"| Review | {CHAIN} |\n"
        "| Destination | open the pull request |\n"
        f"| Branch | {branch} |\n"
    )


def gate(repo, cmd="git commit -m x", **kw):
    return run_hook("commit-review-gate.py", payload(cmd, repo, **kw))


# --- the answer is read, both ways ------------------------------------------


def test_a_declared_chain_item_commits_without_a_prompt(repo):
    """S1. The whole point: the answer was given, so it is not asked again."""
    opt_in(repo)
    declare(repo, review=CHAIN)
    assert decision_of(gate(repo)) == "silent"


def test_a_declared_direct_item_commits_without_a_prompt(repo):
    """S4. Declaring is the routing answer; requiring `[no-review]` as well
    would be requiring the same answer twice."""
    opt_in(repo)
    declare(repo, review=DIRECT)
    assert decision_of(gate(repo)) == "silent"


# --- and everything that is not a readable answer falls back -----------------


def test_no_declaration_behaves_exactly_as_before(repo):
    """S2. The gate a repository that declares nothing meets is unchanged."""
    opt_in(repo)
    assert decision_of(gate(repo)) == "deny"
    assert decision_of(gate(repo)) == "ask"


def test_a_malformed_declaration_does_not_silence_the_gate(repo):
    """S3. Toward asking, never toward silence -- a gate a corrupt file turns
    off has nothing left to do but stay quiet."""
    opt_in(repo)
    declare(repo, body="# routing\n\nwe decided to go through the review chain.\n")
    assert fired(gate(repo))


def test_an_unknown_answer_is_not_an_answer(repo):
    """The vocabulary is fixed. `maybe` is not one of the two ways on."""
    opt_in(repo)
    declare(repo, review="maybe later")
    assert fired(gate(repo))


def test_an_empty_routing_directory_changes_nothing(repo):
    opt_in(repo)
    (repo / ".specseal" / "routing").mkdir(parents=True)
    assert fired(gate(repo))


# --- the declaration is scoped to a branch ----------------------------------


def test_another_branch_s_declaration_does_not_apply_here(repo):
    """Declarations accumulate over a repository's life. Without a scope, the
    first work item ever declared would silence the gate forever."""
    opt_in(repo)
    declare(repo, review=CHAIN, branch="feature/somewhere-else")
    assert fired(gate(repo))


def test_two_declarations_for_one_branch_are_ambiguous(repo):
    """Two answers for the same branch is not an answer. Toward asking."""
    opt_in(repo)
    declare(repo, review=CHAIN, item="1787708604-one")
    declare(repo, review=DIRECT, item="1787708605-two")
    assert fired(gate(repo))


def test_a_declaration_for_another_branch_leaves_this_one_readable(repo):
    """One stale declaration must not make a live one ambiguous."""
    opt_in(repo)
    declare(repo, review=CHAIN, item="1787708604-here")
    declare(repo, review=CHAIN, item="1787700000-elsewhere", branch="feature/old")
    assert decision_of(gate(repo)) == "silent"


# --- the gate names the way out it already accepts ---------------------------


def reason_of(stdout):
    """The text the gate hands the model, or "" when it stayed silent."""
    if not stdout.strip():
        return ""
    return json.loads(stdout)["hookSpecificOutput"]["permissionDecisionReason"]


def test_an_uncommitted_declaration_silences_the_commit_that_adds_it(repo):
    """The fact the gate's first option rests on, asserted directly.

    `declarations()` opens the path rather than asking git, so a declaration
    that exists only in the working tree is already in force. That is what
    makes "write the declaration first" a real way out of a work item's FIRST
    commit: there is no order in which the file must be committed before it
    counts, and so no first-commit waiver to spend. The tests above rely on
    this without saying so -- none of them commits the file -- and an
    unstated premise is one a later change moves silently.
    """
    opt_in(repo)
    path = declare(repo)
    tracked = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--error-unmatch", str(path)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert tracked.returncode != 0, "the premise is an UNCOMMITTED declaration"
    assert decision_of(gate(repo)) == "silent"


def test_the_first_prompt_names_the_declaration_as_a_way_out(repo):
    """Three ways out, and the prompt named two.

    A session starting a work item was handed "review it first" and "commit
    without a review" -- the two answers that do not fit -- and none of the
    one that does. Measured: a session read the missing option as a
    chicken-and-egg the design does not have and put it to the user twice.
    """
    opt_in(repo)
    out = gate(repo)
    assert decision_of(out) == "deny"
    reason = reason_of(out)
    assert '1. "Declare the routing"' in reason
    assert "specs/<work-item-id>/routing.md" in reason
    assert "IN A COMMAND OF ITS OWN" in reason, (
        "the option stopped saying the one thing that makes it work"
    )


def test_the_first_option_does_not_let_the_model_pick_the_review_answer(repo):
    """`straight to the PR` written by the model is a waiver with no word in it.

    The option tells the model to write the declaration and said nothing about
    which Review answer to write. `straight to the PR` silences this arm for
    every later commit on the branch and `chain_check.py` requires nothing of
    it at the pull request -- so a model filling that row in for itself takes
    the waiver the option below spells out, and takes it more quietly: the
    `[no-review]` form leaves the word in the command where a reader can point
    at it, and this leaves nothing anywhere but one line of a file it was just
    told to write.
    """
    opt_in(repo)
    reason = reason_of(gate(repo))
    assert "USER'S answer" in reason, (
        "the option stopped saying who decides the Review row"
    )
    for spelling in ("through the review chain", "straight to the PR"):
        assert spelling in reason, f"the option names only one answer: {spelling}"


def test_the_first_prompt_counts_the_options_it_lists(repo):
    """The header tells the model to offer EXACTLY that many.

    Written down rather than derived, the number goes stale the moment an
    option is added -- and the model obeys the number, so the third option is
    the one it drops.
    """
    opt_in(repo)
    reason = reason_of(gate(repo))
    assert "exactly these three options:" in reason
    assert "these two options" not in reason
    for label in (
        '1. "Declare the routing"',
        '2. "Review it first"',
        '3. "Commit without a review"',
    ):
        assert label in reason, f"the prompt lost `{label}`"


def test_the_second_prompt_names_it_too(repo):
    """The `ask` prompt is what every attempt after the first reaches.

    Leaving it at two ways sent a session that had just read the third option
    back to a sentence saying there were only two.
    """
    opt_in(repo)
    assert decision_of(gate(repo)) == "deny"
    out = gate(repo)
    assert decision_of(out) == "ask"
    reason = reason_of(out)
    assert "specs/<work-item-id>/routing.md" in reason
    assert "for any commit" in reason, (
        "the two-way sentence must scope itself once a third way follows it"
    )


def test_the_third_way_names_its_arm_where_two_are_listed(repo):
    """`this arm` points at nothing in a prompt that lists two of them.

    With review and parity both firing, `ask_reason` prints the two states
    together and then the review arm's sentence. Written as "it silences this
    arm ... re-issue the commit unchanged" it made a promise the gate does not
    keep: executed, writing the declaration and re-issuing gets the parity arm
    and one more prompt. The sentence has to name the arm it belongs to and
    say what it does NOT do.
    """
    opt_in(repo)
    (repo / ".specseal" / "parity.md").write_text("# migration config\n")
    (repo / "code.py").write_text("x = 1\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True
    )
    assert decision_of(gate(repo)) == "deny"
    reason = reason_of(gate(repo))
    assert "[no-review]" in reason and "[no-parity]" in reason, (
        "this case is only about the prompt where BOTH arms are listed"
    )
    assert "REVIEW arm" in reason, (
        "the third way does not say which of the two arms it is a way out of"
    )
    assert "silences NOTHING ELSE" in reason, (
        "the sentence still reads as though the commit then goes through"
    )
    # Case-insensitive: the first version of this check read the lower-case
    # spelling only, and a mutation that opened the sentence with `Re-issue`
    # walked straight through it.
    assert "re-issue the commit unchanged" not in reason.lower(), (
        "`unchanged` promises a commit the other arm still stops"
    )


def test_the_parity_arm_gains_no_third_way(repo):
    """Nothing declares a comparison against the original in advance.

    The routing sentence rides on the review arm, so an arm that has no such
    way out must not inherit one -- offering it there would name a file that
    silences nothing.
    """
    opt_in(repo)
    (repo / ".specseal" / "parity.md").write_text("# migration config\n")
    declare(repo, review=CHAIN)
    (repo / "code.py").write_text("x = 1\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True
    )
    assert decision_of(gate(repo)) == "deny"
    reason = reason_of(gate(repo))
    assert "[no-parity]" in reason
    # The PROPERTY, not a filename. `"routing.md" not in reason` said the same
    # thing today and would go red on a parity prompt that got MORE accurate --
    # one that says in so many words that a declaration does not silence this
    # arm. What must not happen is the review arm's sentence riding along.
    assert "There is a third way" not in reason, (
        "the parity arm inherited the review arm's `also` sentence"
    )


# --- what the declaration does not touch ------------------------------------


def test_the_declaration_does_not_waive_the_parity_arm(repo):
    """Routing answers whether a reviewer sees the work. Whether the original
    was consulted is a different question, and nobody answered it."""
    opt_in(repo)
    (repo / ".specseal" / "parity.md").write_text("# migration config\n")
    declare(repo, review=CHAIN)
    (repo / "code.py").write_text("x = 1\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True
    )
    out = gate(repo)
    assert fired(out)
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "[no-parity]" in reason
    assert "[no-review]" not in reason


def test_no_review_still_waives_one_command_on_its_own(repo):
    """S5. The token keeps its meaning for a commit with no work item."""
    opt_in(repo)
    assert decision_of(gate(repo, cmd="git commit -m x [no-review]")) == "silent"


def test_declaring_does_not_opt_a_repository_in(repo):
    """The declaration sits beside the work item, not under `.specseal/`, so
    writing one says nothing about whether this repository runs the workflow.
    That separation is what keeps a declaration from creating the plugin's home
    as a side effect -- see the legacy-home test below."""
    declare(repo, review=CHAIN)
    assert not (repo / ".specseal").exists()
    assert decision_of(gate(repo)) == "silent"  # never opted in: nothing to gate
    opt_in(repo)
    assert decision_of(gate(repo)) == "silent"  # opted in, and now declared


# --- the home question the location dissolves --------------------------------


def test_declaring_never_creates_the_plugin_home(repo):
    """Routing lives under `specs/`, which is neither the home nor the signal.

    Had it lived under `.specseal/`, writing a declaration would have created
    the directory whose existence IS the opt-in. Answering a question about
    where this work item is going would then have switched four gates on in a
    repository that never asked for them.
    """
    declare(repo, review=CHAIN)
    assert not (repo / ".specseal").exists()
    assert decision_of(gate(repo)) == "silent"


def test_a_routing_only_work_item_is_a_whole_work_item(repo):
    """Below the SDD ladder nothing is written -- no `spec.md`, no closing
    memo -- so those changes used to leave no trace at all. They are most of
    what the gate sees, which is why they get an id and a directory."""
    opt_in(repo)
    path = declare(repo, review=DIRECT, item="1787700000-a-typo-fix")
    assert sorted(os.listdir(path.parent)) == ["routing.md"]
    assert decision_of(gate(repo)) == "silent"


# --- the third axis: read when present, absent when not ----------------------


def test_a_two_axis_declaration_is_still_a_declaration():
    """S1. Twelve of these are committed in this repository at the base of
    this work, thirteen at its head. A third axis that
    invalidated them would un-silence the commit gate on every one."""
    parsed = routing.parse(two_axis_text())
    assert parsed is not None
    assert parsed["review"] == CHAIN
    assert parsed["implementation"] is None


def test_the_third_axis_is_read_when_it_is_there():
    """S2."""
    for answer in routing.IMPLEMENTATION_ANSWERS:
        text = two_axis_text().replace(
            "| Branch |", f"| Implementation | {answer} |\n| Branch |"
        )
        assert routing.parse(text)["implementation"] == answer, answer


def test_an_unreadable_third_axis_reads_as_unanswered_not_as_no_declaration():
    """S3. The failure direction is "this axis was not answered", never "this
    file is not a declaration" -- the second would take the review answer down
    with it, which is a gate un-silenced by a typo in a row nothing gates on."""
    text = two_axis_text().replace(
        "| Branch |", "| Implementation | whoever gets to it |\n| Branch |"
    )
    parsed = routing.parse(text)
    assert parsed is not None, "an unreadable third axis rejected the declaration"
    assert parsed["implementation"] is None
    assert parsed["review"] == CHAIN


def test_the_commit_gate_decides_the_same_with_the_row_and_without_it(repo):
    """S1 + S3 at the gate rather than at the parser. Adding the axis must not
    move the decision the two older axes produce."""
    opt_in(repo)
    declare(repo, review=CHAIN)
    assert decision_of(gate(repo)) == "silent"
    declare(repo, review=CHAIN, implementation="smith")
    assert decision_of(gate(repo)) == "silent"
    declare(repo, review=CHAIN, implementation="whoever gets to it")
    assert decision_of(gate(repo)) == "silent"


def test_every_declaration_in_this_repository_still_parses():
    """Executed against the real files, not a fixture: the twelve committed here
    are the population the optional row exists for."""
    import glob

    root = os.path.join(os.path.dirname(__file__), "..")
    found = sorted(glob.glob(os.path.join(root, "specs", "*", "routing.md")))
    assert found, "no declarations found -- the check would pass vacuously"
    for path in found:
        with open(path, encoding="utf-8") as f:
            assert routing.parse(f.read()) is not None, path
