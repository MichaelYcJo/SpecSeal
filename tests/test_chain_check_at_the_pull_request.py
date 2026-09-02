"""The review chain is enforced at the pull request now, not at every commit.

The commit gate could never tell "routed to the chain, not reviewed yet" from
"nobody decided anything" — the two are byte-identical to it — so it asked
every time. Recording the answer lets it stay quiet, and the answer is only
allowed to make it quiet because the check MOVED rather than disappearing.
This is where it moved to.

Every case here builds a scratch repository with a real base branch and a real
HEAD, because the check is about what git can see between two refs. The
verdicts are read from the script's exit code, not from its prose.
"""

import json
import os
import shutil
import subprocess
import sys

import pytest
from conftest import load_hook_module, symlink_or_skip

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")

CHAIN = "through the review chain"
DIRECT = "straight to the PR"
ITEM = "seal/specs/1787700000-a-work-item"
# One level down, because `round-N` is the only member of the SDD set that is
# plural and unbounded. A record left at `ITEM` itself is a stray and fails.
ROUNDS = f"{ITEM}/rounds"


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


def _build_chain_repo(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _chain_repo_template(tmp_path_factory):
    d = tmp_path_factory.mktemp("chain-repo-template") / "repo"
    _build_chain_repo(d)
    return d


@pytest.fixture
def repo(tmp_path, _chain_repo_template):
    """A repository with a `base` branch and a feature branch checked out."""
    d = tmp_path / "repo"
    shutil.copytree(_chain_repo_template, d)
    return d


def declaration(review=CHAIN, branch="feature"):
    return (
        "# 1787700000-a-work-item — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        f"| Review | {review} |\n"
        "| Destination | open the pull request |\n"
        f"| Branch | {branch} |\n"
    )


def record(
    sha,
    passed=False,
    verdict="fixed",
    finding="🔴 1",
    extra="",
    pr=None,
    checked_by="nobody — the run ended here",
):
    box = "x" if passed else " "
    # The `| PR |` row is optional, and `not yet opened` is what a review that
    # finished before its pull request writes there.
    pr_row = f"| PR | {pr} |\n" if pr is not None else ""
    # `Fixes checked by` is NOT optional, and the default is the one value
    # that is honest for a record with no later round beside it. Passing
    # `None` leaves the row out, which is a state of its own and has its own
    # cases in `test_the_last_rounds_fixes_are_checked.py`.
    who = f"| Fixes checked by | {checked_by} |\n" if checked_by is not None else ""
    return (
        "# round 1\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n{pr_row}{who}\n"
        f"- [{box}] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        f"| {finding} | something | `f.py:1` | {verdict} | grounds |\n"
        f"{extra}"
    )


def run(repo, draft=None, payload=None, branch=None):
    """`draft=True/False` writes the event payload GitHub hands a workflow.

    `None` is the local run: no payload, so the check cannot see a pull
    request at all. That state is judged strictly on purpose — see
    `pull_request_state`.

    `payload` writes the file verbatim, for the shapes `draft=` cannot say: a
    payload that will not parse, one with no pull request in it, and one whose
    `draft` is the STRING `"false"`. `branch` sets `GITHUB_HEAD_REF`, which is
    where the branch comes from in a workflow because a pull-request checkout
    is a detached merge commit.
    """
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    if branch is not None:
        env["GITHUB_HEAD_REF"] = branch
    if payload is not None:
        path = repo / "event.json"
        path.write_text(payload, "utf-8")
        env["GITHUB_EVENT_PATH"] = str(path)
    elif draft is not None:
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


# --- the four declaration states --------------------------------------------


def test_a_chain_declaration_with_no_round_record_fails(repo):
    """S6. The round record is the pull request's only evidence — the local
    mark cannot travel here."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    code, out = run(repo)
    assert code == 1, out
    assert "holds no `round-N.md`" in out
    assert f"{ROUNDS}/" in out, (
        "the failure has to name the directory it looked in. A repository "
        "whose records are still one level up reads this as a review that "
        "never happened, and is told nothing about why"
    )


def test_a_chain_declaration_with_a_record_passes(repo):
    """S7."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 0, out


def test_a_pull_request_with_no_declaration_passes_with_a_notice(repo):
    """S8. Failing here would teach sessions not to declare, which voids the
    condition — the same reasoning `unverified_check.py` gives for not failing
    on an honest open row."""
    write(repo, "g.py", "y = 2\n")
    commit(repo, "no declaration")
    code, out = run(repo)
    assert code == 0, out
    assert "examined nothing" in out, (
        "the notice has to say what was NOT CHECKED. `no declaration found` "
        "describes the check's own state and reads as routine"
    )


def test_an_unreadable_declaration_fails(repo):
    """S9. A tolerant read reports `no declaration`, which is exactly what a
    branch that never declared looks like."""
    write(repo, f"{ITEM}/routing.md", "# routing\n\nwe are going to review it\n")
    commit(repo, "prose")
    code, out = run(repo)
    assert code == 1, out
    assert "not a readable declaration" in out


def test_a_direct_declaration_needs_nothing_and_is_printed(repo):
    write(repo, f"{ITEM}/routing.md", declaration(review=DIRECT))
    commit(repo, "declare direct")
    code, out = run(repo)
    assert code == 0, out
    assert DIRECT in out, "a decision nobody sees is not a record"


# --- the round record it finds ----------------------------------------------


def test_a_record_reviewing_a_commit_off_this_branch_fails(repo):
    """The target has to be an ancestor. A SHA from somewhere else is a review
    of something this pull request does not contain."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record("0" * 40))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "not an ancestor" in out


def test_a_record_with_no_target_sha_fails(repo):
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        "# round 1\n\n- [ ] Pass\n\n## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n|---|---|---|---|---|\n"
        "| 🟡 1 | x | `f.py:1` | answered | g |\n",
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "which commit this round actually looked at" in out


def test_the_last_round_is_the_one_read(repo):
    """Earlier verdicts are not archived — every one needs an answer in the
    round that follows, so the last file is the state.

    Ordered numerically: `round-10.md` sorts before `round-2.md` as text.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-2.md", record(sha, passed=True, verdict="open"))
    write(repo, f"{ROUNDS}/round-10.md", record(sha, passed=True, verdict="fixed"))
    commit(repo, "rounds")
    code, out = run(repo)
    assert code == 0, out
    assert "round-10.md" in out


# --- Pass against the verdict table -----------------------------------------


def test_a_checked_pass_beside_an_open_blocking_finding_fails(repo):
    """The state a checkbox alone would create. Both halves are in one file,
    so a machine can see the contradiction — and is made to."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "`Pass` is checked" in out


def test_an_unchecked_pass_fails_once_the_pull_request_is_ready(repo):
    """Reversed deliberately, and this docstring is the record of it.

    It used to read *an honest open finding is not what this fails for*, and
    that was written when nothing anywhere required `Pass` ever to be
    checked: a work item could declare the chain, run its rounds, leave every
    verdict open and open a pull request, and no gate in the repository had
    an opinion. `was it reviewed` was enforced and `did it pass` was not.

    The order is what settles it. In this design the chain runs BEFORE the
    pull request — smith, then warden, then the PR — so an unchecked `Pass`
    at the pull request means the chain was skipped or is still running.
    Neither is a state to open a ready pull request in. The escape is below:
    open it as a draft.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "`Pass` is not checked" in out


def test_an_unchecked_pass_passes_on_a_draft_pull_request(repo):
    """The escape hatch, and the only one. A review still running has
    somewhere to be: a draft pull request is not a request to merge."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo, draft=True)
    assert code == 0, out
    assert "draft" in out


def test_a_run_that_cannot_see_a_pull_request_is_judged_as_a_ready_one(repo):
    """The unknown is judged strictly, and the reason is printed.

    Treating it as a draft would make `no pull-request context` the quietest
    way past this check that exists — quieter than `[no-review]`, which at
    least stays in the command. Passing in silence is the one outcome ruled
    out, so the verdict says which state it assumed and why."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "no pull-request event payload" in out


def test_a_checked_pass_beside_an_open_NON_blocking_finding_passes(repo):
    """🟡 does not block a merge, so it does not block a pass. The cap lets
    extra rounds only for 🔴, and this is the same line."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record(sha, passed=True, verdict="open", finding="🟡 1"),
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 0, out


def test_a_verdict_word_it_does_not_recognise_counts_as_open(repo):
    """The direction has to be toward the finding still being open. A word
    this cannot read, counted as closed, is the tolerant read the whole file
    refuses."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="looked at"))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "looked at" in out


def test_a_record_with_no_pass_checkbox_fails(repo):
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        f"# round 1\n\n| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n\n"
        "## Verdicts\n\n| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n| 🟢 1 | x | `f.py:1` | fixed | g |\n",
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "did it pass" in out


def test_an_unreadable_verdict_table_fails(repo):
    """Zero open findings and a table nobody can read are the same number.
    Only one of them means the review is done."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        f"# round 1\n\n| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n\n"
        "- [x] Pass\n\n## Verdicts\n\nwe found nothing worth writing down\n",
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "holds no table" in out


def test_a_blocking_finding_inside_a_fenced_block_is_not_a_finding(repo):
    """One reader, not two. A 🔴 inside a code fence or an HTML comment must
    not count here for exactly the reason it does not count in
    `unverified_check.py` — two readers of the same markdown drifted apart in
    four places across three rounds in this repository."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record(sha, passed=True, verdict="fixed")
        + "\n```\n| 🔴 9 | quoted | `f.py:1` | open | from another round |\n```\n"
        + "<!-- | 🔴 8 | commented | `f.py:1` | open | a note | -->\n",
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 0, out


# --- where a round record has to come from ----------------------------------


def test_an_uncommitted_round_record_is_not_evidence(repo):
    """The declaration comes from `git diff` and the records used to come
    from `os.listdir`, so two values built by two rules were compared. A file
    nobody committed cannot be a pull request's evidence — CI never sees it.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True))
    # deliberately not committed
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "holds no `round-N.md`" in out


def test_a_symbolic_link_cannot_stand_in_for_the_last_round(repo):
    """The LAST round is the one whose verdict speaks, so anything that can
    add a name at the end decides which file is read.

    Reproduced before the fix: with a failing `round-2.md` committed, a
    tracked link `round-3.md` -> the clean `round-1.md` turned exit 1 into
    exit 0. The failing round was still sitting right there."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="fixed"))
    write(repo, f"{ROUNDS}/round-2.md", record(sha, passed=True, verdict="open"))
    commit(repo, "two rounds")
    symlink_or_skip("round-1.md", repo / ROUNDS / "round-3.md")
    commit(repo, "a link named round-3")
    assert (
        git(repo, "ls-tree", "HEAD", f"{ROUNDS}/round-3.md").stdout.split()[0]
        == "120000"
    ), "the link has to reach git as a link, or this case proves nothing"
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "round-2.md" in out


def test_a_declaration_already_in_the_base_is_still_checked(repo):
    """`changed_routing` reads what this pull request TOUCHED, so a pull
    request adding only round records to an item declared in an earlier one
    found nothing and printed `declared neither way` — a sentence about a
    tree holding the declaration right there.

    The branch is the key the commit gate already uses, and it is the key
    here too."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    git(repo, "branch", "-f", "base", "HEAD")
    write(repo, "g.py", "y = 2\n")
    commit(repo, "work with no declaration in the diff")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "holds no `round-N.md`" in out
    assert "examined nothing" not in out


# --- S10 of the 0.4.0 root move: a declaration the pull request only moved --


OLD_ITEM = "specs/1780000000-released"


def move_into_seal(repo, *items):
    """The root move as `hooks/root-migrate.py` and this repository's own
    branch make it: a staged `git mv` of each work item under `seal/specs/`."""
    (repo / "seal" / "specs").mkdir(parents=True, exist_ok=True)
    for item in items:
        git(repo, "mv", item, f"seal/{item}")


def test_a_declaration_the_pull_request_only_renamed_is_not_judged(repo):
    """The root move renames every declaration in the repository, and each
    shows up in `git diff --name-only` under its new path exactly as an added
    one would. Judged, the move would put every released work item under
    review on the pull request that moved it — fifteen here — each needing
    its round records' Target SHA to resolve. A declaration the pull request
    only moved is not one it made."""
    write(repo, f"{OLD_ITEM}/routing.md", declaration(branch="released"))
    commit(repo, "a released work item, declared for a branch that is not this one")
    git(repo, "branch", "-f", "base", "HEAD")
    move_into_seal(repo, OLD_ITEM)
    commit(repo, "the root move")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "1780000000-released" not in out, out
    assert "examined nothing" in out, (
        "this branch declared nothing, and the notice says so"
    )


def test_the_branchs_own_declaration_is_still_judged_after_the_move(repo):
    """The set the check judges is what the pull request added or edited PLUS
    the declaration for this branch — so the move of this branch's own item
    does not hide it, and the fourteen it moved beside it stay out."""
    write(repo, "specs/1787700000-a-work-item/routing.md", declaration())
    write(repo, f"{OLD_ITEM}/routing.md", declaration(branch="released"))
    commit(repo, "two work items declared, one for this branch")
    git(repo, "branch", "-f", "base", "HEAD")
    move_into_seal(repo, "specs/1787700000-a-work-item", OLD_ITEM)
    commit(repo, "the root move")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert ITEM in out and "holds no `round-N.md`" in out, out
    assert "1780000000-released" not in out, out


def test_a_declaration_the_pull_request_renamed_and_edited_is_judged(repo):
    """Only an EXACT rename is a move. A declaration the pull request moved
    and then changed carries an edit of its own, and the edit is what the
    check exists to read."""
    write(repo, f"{OLD_ITEM}/routing.md", declaration(branch="released"))
    commit(repo, "a released work item")
    git(repo, "branch", "-f", "base", "HEAD")
    move_into_seal(repo, OLD_ITEM)
    moved = repo / "seal" / OLD_ITEM / "routing.md"
    moved.write_text(
        moved.read_text(encoding="utf-8") + "\nEdited on the way over.\n",
        encoding="utf-8",
    )
    commit(repo, "the root move, with an edit")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "1780000000-released" in out, out


def test_a_working_tree_edit_cannot_close_a_round_git_carries_as_open(repo):
    """The names came from `git ls-tree` and the CONTENT came from `open()`.

    Round 2 moved half of this and left the other half, so the check was still
    comparing two values built by two rules — it just did it one line later.
    A record committed with an open blocking finding, edited on disk to read
    `fixed` and not committed, turned exit 1 into exit 0. CI never sees that
    edit; a local run always can.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="open"))
    commit(repo, "round 1, blocking finding open")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="fixed"))
    # deliberately not committed
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "`Pass` is checked" in out


def test_a_clean_copy_in_the_working_tree_cannot_hide_a_committed_failure(repo):
    """The mirror of the symbolic-link case, and it ran the other way.

    There, git carried a link and the check had to see through it. Here git
    carries the failing `round-2.md` as an ordinary file and the WORKING TREE
    holds a link to the clean `round-1.md` in its place. `unique_by_target`
    resolved both worktree paths to one real file, folded the record git
    carries out of the list, and the failing round was never opened.

    The fold is gone rather than narrowed: with the content read from git, a
    worktree path is not what is being counted any more, and the mode filter
    already refuses a link git knows about.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="fixed"))
    write(repo, f"{ROUNDS}/round-2.md", record(sha, passed=True, verdict="open"))
    commit(repo, "two rounds, the second one failing")
    assert (
        git(repo, "ls-tree", "HEAD", f"{ROUNDS}/round-2.md").stdout.split()[0]
        == "100644"
    ), "git has to carry round-2 as a regular file, or this case proves nothing"
    (repo / ROUNDS / "round-2.md").unlink()
    symlink_or_skip("round-1.md", repo / ROUNDS / "round-2.md")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "round-2.md" in out


# --- what the event payload is allowed to say -------------------------------


def test_a_string_draft_is_not_a_draft(repo):
    """`pr["draft"]` read the value for its truthiness, and every non-empty
    string is true. A payload carrying `"draft": "false"` was therefore read
    as a draft, and a draft is excused the checked `Pass` — the one
    requirement this branch added, turned off by four characters."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo, payload='{"pull_request": {"draft": "false"}}')
    assert code == 1, out
    assert "`Pass` is not checked" in out


def test_a_payload_that_will_not_parse_is_judged_ready_and_says_so(repo):
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo, payload="{not json")
    assert code == 1, out
    assert "would not read" in out


def test_a_payload_naming_no_pull_request_is_judged_ready_and_says_so(repo):
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo, payload='{"repository": {"name": "x"}}')
    assert code == 1, out
    assert "names no pull request" in out


def test_a_branch_nobody_can_read_is_not_a_pull_request_that_declared_nothing(repo):
    """A detached HEAD with no `GITHUB_HEAD_REF` leaves no key to match a
    declaration by, and the notice said *this pull request declared neither
    way* — a sentence about a tree holding the declaration right there. The
    two states need different sentences: one is an author who declared
    nothing, the other is a run that could not look."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    git(repo, "branch", "-f", "base", "HEAD")
    write(repo, "g.py", "y = 2\n")
    commit(repo, "work with no declaration in the diff")
    git(repo, "checkout", "-q", "--detach")
    code, out = run(repo, draft=False)
    # Still a pass: the same reasoning `unverified_check.py` gives for an
    # honest open row. What changes is the sentence, and the sentence is the
    # whole value of the row.
    assert code == 0, out
    assert "declared neither way" not in out, out
    assert "branch" in out and "could not be read" in out, out


def test_a_target_naming_two_commits_has_both_checked(repo):
    """`templates/sdd-round.md:12` says *both, if HEAD moved mid-review*, and
    `docs/review-handoff-protocol.md:84` repeats it. The check read the whole
    cell as one ref, so the documented two-SHA form could not resolve and no
    round record has ever been allowed to use it."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, "h.py", "z = 3\n")
    second = commit(repo, "more work")
    body = record(sha, passed=True).replace(
        f"| Target SHA | {sha} |",
        f"| Target SHA | {sha} (reviewed); fixes landed at {second} |",
    )
    write(repo, f"{ROUNDS}/round-1.md", body)
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 0, out


def test_a_target_whose_second_commit_is_off_this_branch_fails(repo):
    """Both have to be ancestors, or the second SHA is a place to hide one."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    body = record(sha, passed=True).replace(
        f"| Target SHA | {sha} |",
        f"| Target SHA | {sha} (reviewed); fixes landed at deadbeef1234567 |",
    )
    write(repo, f"{ROUNDS}/round-1.md", body)
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "deadbeef1234567" in out


# --- the check itself has to be able to fail --------------------------------


def test_an_unresolvable_baseline_is_not_a_pass(repo):
    """A shallow checkout lands here, and passing it reports a check that
    never ran."""
    r = subprocess.run(
        [sys.executable, CHECK, "--baseline", "origin/nope", "--root", str(repo)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    assert r.returncode == 2, r.stdout + r.stderr
    assert "does not resolve" in r.stdout + r.stderr


# --- what a squash destroys, and what it must not excuse ---------------------
#
# `CONTRIBUTING.md` has feature branches squash into the release branch, and
# the commits a round reviewed are exactly what a squash discards. Requiring
# the target to be an ancestor of HEAD asserted a property the branching model
# destroys on purpose, and it failed on this repository's own release.
#
# Narrowing the requirement to records the pull request CHANGED does not reach
# it: a new work item's round records are added relative to `main`, so they are
# in every release pull request's diff. Measured before writing these — the
# release → `main` diff listed all five. So the requirement moved instead: an
# ancestor of HEAD, or of the branch the declaration names.


def squashed(repo, target_on_feature=True):
    """A release branch carrying `feature` as one squashed commit.

    Returns the SHA the round record names — a commit that exists on
    `feature` and, after the squash, nowhere in the release branch's history.
    """
    write(repo, f"{ITEM}/routing.md", declaration(branch="feature"))
    commit(repo, "declare")
    write(repo, "f.py", "x = 2\n")
    reviewed = commit(repo, "the work the round reviewed")
    write(repo, f"{ROUNDS}/round-1.md", record(reviewed, passed=True))
    commit(repo, "round 1")
    git(repo, "switch", "-qc", "release", "base")
    git(repo, "merge", "--squash", "-q", "feature")
    commit(repo, "squash feature into the release branch")
    if target_on_feature:
        subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "merge-base",
                "--is-ancestor",
                reviewed,
                "feature",
            ],
            check=True,
            capture_output=True,
        )
    return reviewed


def test_a_target_the_squash_discarded_passes_when_the_branch_still_has_it(repo):
    """#61. The record IS in this pull request's diff, and its target is not
    an ancestor of HEAD — both true, and the review really happened."""
    reviewed = squashed(repo)
    assert (
        subprocess.run(
            ["git", "-C", str(repo), "merge-base", "--is-ancestor", reviewed, "HEAD"]
        ).returncode
        != 0
    ), "the fixture did not actually squash the reviewed commit away"
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "must be reachable from HEAD or refs/heads/feature" in out


def test_a_target_the_squash_discarded_fails_once_nothing_carries_it(repo):
    """This used to pin the cost of reading the BRANCH: delete a feature
    branch before its release reaches `main` and that pull request goes red.
    It went red — a release pull request, six commits across five work
    items, five branches deleted by hand. The branch is no longer the only
    place looked at, so what is pinned here now is the remaining failure: a
    target nothing carries at all.

    The message is asserted because a red build whose cause is a checkout
    that never fetched `refs/pull/*/head` is unreadable without it, and that
    is a different repair from a lost commit."""
    squashed(repo)
    git(repo, "branch", "-qD", "feature")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "not an ancestor of HEAD" in out
    assert "refs/pull/*/head" in out, (
        "the failure has to name the fetch — the commit is usually still "
        "there, on a ref this clone never asked for"
    )


def test_a_merged_record_whose_commits_are_gone_is_not_re_examined(repo):
    """A record that arrived in an earlier merge is history. Its SHAs are
    expected to be gone, and asserting anything about them now re-fails a
    review that already passed at the pull request which added it."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record("0" * 40, passed=True))
    commit(repo, "round 1")
    git(repo, "branch", "-f", "base", "HEAD")
    write(repo, "g.py", "y = 2\n")
    commit(repo, "later work, touching neither the declaration nor the record")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "not changed by this pull request" in out
    assert "0000000" not in out, (
        "a SHA nothing resolves is the expected state for a merged record; "
        "naming it reads as a finding"
    )


def test_a_merged_record_is_still_read_for_everything_else(repo):
    """Only the reachability claim is dropped. A merged record that contradicts
    itself is still a contradiction, and the pull request can still fix it."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record("0" * 40, passed=True, verdict="still looking"),
    )
    commit(repo, "round 1")
    git(repo, "branch", "-f", "base", "HEAD")
    write(repo, "g.py", "y = 2\n")
    commit(repo, "later work")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "still looking" in out


def test_a_record_new_in_the_pull_request_naming_a_foreign_commit_still_fails(repo):
    """The teeth the relaxation must not remove. `other` is a real commit in
    this repository, reachable from a ref — and the declaration does not name
    that branch, so it is still a review of something this pull request does
    not carry."""
    git(repo, "switch", "-qc", "other", "base")
    write(repo, "h.py", "z = 3\n")
    foreign = commit(repo, "a commit on a branch nobody declared")
    git(repo, "switch", "-q", "feature")
    write(repo, f"{ITEM}/routing.md", declaration(branch="feature"))
    commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(foreign, passed=True))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert foreign[:7] in out
    assert "not an ancestor of HEAD or refs/heads/feature" in out


# --- a record left at the old location ---------------------------------------


def test_a_record_still_at_the_top_level_fails_naming_it_and_the_destination(repo):
    """S3, the CI half. Two substrings, not merely a non-zero exit.

    No fallback ships and nothing migrates a repository that updates the
    plugin, so a work item whose records stayed flat fails its pull request.
    That is only bearable because the failure says which file and where it
    goes; degraded to `holds no round-N.md` it says a review never happened,
    which is false and unactionable at once.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ITEM}/round-1.md", record(sha, passed=True))
    commit(repo, "round 1, at the old location")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"{ITEM}/round-1.md" in out, out
    assert f"{ITEM}/rounds/" in out, out


def test_a_stray_does_not_report_as_a_review_that_never_happened(repo):
    """The sentence that would replace the one above if the stray check were
    dropped. It is what every un-migrated repository would see.

    The positive half is asserted alongside the negative one deliberately.
    On its own, `not in out` also passes when the check says NOTHING, which
    is the second way this could go wrong and the quieter of the two.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ITEM}/round-1.md", record(sha, passed=True))
    commit(repo, "round 1, at the old location")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"{ITEM}/round-1.md" in out, out
    assert "holds no `round-N.md`" not in out, out
    # The command it prescribes has to run. `git mv` alone fails with
    # `destination directory does not exist`, and the slash-less retry that
    # follows renames the record to a FILE. Asserted on the RENDERED message
    # rather than the source, because a source check is defeated by degrading
    # the command to its own name.
    assert "mkdir" in out and "git mv" in out, out


def test_a_round_record_git_carries_as_a_file_is_named(repo):
    """`rounds` as a BLOB, the state the slash-less `git mv` retry produces.

    The filesystem reader learned this in round 1 and this one did not, so the
    same repository was told two different things about the same tree: the
    hook named the state, and the pull request said `holds no round-N.md` —
    which this file's own header calls true and indistinguishable from a work
    item that skipped its review. Worse here, because the `mkdir` that message
    then prescribes fails with `File exists`.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ITEM}/rounds", record(sha, passed=True))
    commit(repo, "rounds as a file")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "is not a directory" in out, out
    assert "holds no `round-N.md`" not in out, out


def test_rounds_as_a_tracked_symlink_is_named_too(repo):
    """The same state, in the spelling git uses for a link.

    Round 2 added the FILE check here and built it on `tracked_files`, whose
    mode allow-list is `100644`/`100755`. Git carries a symbolic link as
    `120000`, so it fell straight through and the two readers went back to
    opposite answers for one tree — the exact state the function was added
    for. Not hypothetical: `tracked_files`'s own docstring records a tracked
    symbolic link turning exit 1 into exit 0 in this repository.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ITEM}/real-round-1.md", record(sha, passed=True))
    symlink_or_skip("real-round-1.md", repo / ITEM / "rounds")
    commit(repo, "rounds as a symlink")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "is not a directory" in out, out
    assert "holds no `round-N.md`" not in out, out


def dir_link(repo, item):
    """`rounds` as a symlink to a DIRECTORY that holds a record.

    Round 4's fourth shape. The hook follows the link, reads the record and
    says nothing; the pull-request check sees `120000`, is not a tree, and
    fails telling the reader to `mkdir` a path that already exists. Three
    shapes were enumerated and the fourth split them again.
    """
    real = item / "real-rounds"
    real.mkdir()
    (real / "round-1.md").write_text("| Target SHA | `x` |\n", encoding="utf-8")
    symlink_or_skip("real-rounds", item / "rounds")


def test_the_two_readers_agree_on_every_shape_of_rounds(repo):
    """One tree, one answer. The hook and the pull-request check are separate
    implementations of `rounds_unreadable`, and every round so far has found
    them disagreeing on a shape one of them had not been taught.
    """
    guard = load_hook_module("routing.py", "routing_agree")
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    item = repo / ITEM

    def both(build):
        for stale in (item / "rounds",):
            if stale.is_symlink() or stale.is_file():
                stale.unlink()
            elif stale.is_dir():
                shutil.rmtree(stale)
        build()
        commit(repo, "shape")
        _, out = run(repo, draft=False)
        return guard.rounds_unreadable(str(item)), "is not a directory" in out

    write(repo, f"{ITEM}/real-round-1.md", record(sha, passed=True))
    commit(repo, "a record to point at")

    # The expected VALUE, not only that the two agree. Round 4 blinded both
    # implementations at once — `return False` in each — and this test stayed
    # green: a property test for "they answer alike" passes the state where
    # neither answers at all, which is the final form of the class it exists
    # to close.
    shapes = {
        "blob": (lambda: (item / "rounds").write_text("x", encoding="utf-8"), True),
        "symlink": (
            lambda: symlink_or_skip("real-round-1.md", item / "rounds"),
            True,
        ),
        "dir-symlink": (lambda: dir_link(repo, item), True),
        "tree": (
            lambda: (
                (item / "rounds").mkdir(),
                write(repo, f"{ITEM}/rounds/round-1.md", record(sha, passed=True)),
            ),
            False,
        ),
    }
    for name, (build, unreadable) in shapes.items():
        hook, check = both(build)
        assert hook == check == unreadable, (
            f"{name}: expected {unreadable}; the hook says {hook} and the "
            f"pull-request check says {check}"
        )


def test_a_stray_beside_a_real_record_still_has_its_pass_read(repo):
    """A stray must not become a way past the verdict check. Reporting it and
    then stopping would let a work item hide a failing round in `rounds/`
    behind one stale file at the top level."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ITEM}/round-1.md", record(sha, passed=True))
    write(repo, f"{ROUNDS}/round-2.md", record(sha, passed=True, verdict="open"))
    commit(repo, "one stray, one real")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"{ITEM}/round-1.md" in out, out
    assert "`Pass` is checked" in out, out


# --- round 1: what the reachability rule got wrong -----------------------------
#
# Every case below is a defect round 1 reached by execution, not by reading.


def test_a_work_item_id_git_quotes_keeps_its_reachability_check(repo):
    """`git diff --name-only` quotes and octal-escapes a path holding
    non-ASCII, a quote or a backslash under `core.quotePath`, which is on by
    default. `round_records` builds its paths from `ls-tree`, which never
    quotes. The two met in the per-record membership test, it failed, and the
    reachability requirement DISAPPEARED for a record new in the pull request —
    exit 1 before the diff condition existed, exit 0 after it. The line read
    `already merged`, which is what hid it."""
    item = "seal/specs/1780000000-caf\u00e9"
    write(repo, f"{item}/routing.md", declaration(branch="feature").replace(ITEM, item))
    commit(repo, "declare")
    write(repo, f"{item}/rounds/round-1.md", record("deadbeef1234567", passed=True))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "deadbeef1234567" in out
    assert "no claim made" not in out, (
        "a record this pull request just added must never be reported as "
        "one it did not touch"
    )


def test_the_ci_shape_is_the_remote_ref_with_no_local_branch(repo, tmp_path):
    """A pull-request checkout is a detached merge commit with no local
    branches, so `refs/remotes/origin/<branch>` is the ONLY candidate CI can
    take — and it was the one candidate no case ran."""
    bare = tmp_path / "origin.git"
    git(repo, "init", "-q", "--bare", str(bare))
    reviewed = squashed(repo)
    git(repo, "remote", "add", "origin", str(bare))
    git(repo, "push", "-q", "origin", "feature")
    git(repo, "branch", "-qD", "feature")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "refs/remotes/origin/feature" in out
    assert reviewed[:7] not in out


def test_a_stale_remote_does_not_hide_the_local_branch_that_has_it(repo, tmp_path):
    """Taking the first candidate that resolves and stopping made a stale
    `origin/<branch>` shadow the local branch carrying the commit — and the
    failure advised restoring a branch that was sitting right there."""
    bare = tmp_path / "origin.git"
    git(repo, "init", "-q", "--bare", str(bare))
    git(repo, "remote", "add", "origin", str(bare))
    git(repo, "push", "-q", "origin", "feature")  # origin/feature pinned here
    reviewed = squashed(repo)  # feature moves on; the remote does not
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert reviewed[:7] not in out


def test_a_tag_cannot_stand_in_for_the_branch_it_shares_a_name_with(repo):
    """`rev-parse <name>` follows git's disambiguation order, where
    `refs/tags/` beats `refs/heads/` — measured, with a `warning: refname is
    ambiguous` that `git()` discards. A tag carrying a commit nobody reviewed
    satisfied the check while the branch's own commits were invisible."""
    git(repo, "switch", "-qc", "unreviewed", "base")
    write(repo, "h.py", "z = 3\n")
    never_reviewed = commit(repo, "a commit no round ever looked at")
    git(repo, "switch", "-q", "feature")
    squashed(repo)
    git(repo, "tag", "feature", never_reviewed)  # same name as the branch
    write(repo, f"{ROUNDS}/round-1.md", record(never_reviewed, passed=True))
    commit(repo, "point the record at the tag's commit")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert never_reviewed[:7] in out


def test_a_branch_cell_naming_a_revision_expression_admits_nothing(repo):
    """The bare name accepted anything git parses as a revision, so a
    `| Branch | main |` cell admitted every commit on `main`. Fully qualified,
    `refs/heads/base~1` is not a ref and contributes no candidate."""
    write(repo, f"{ITEM}/routing.md", declaration(branch="base"))
    commit(repo, "declare against the base branch")
    write(repo, f"{ROUNDS}/round-1.md", record("0" * 40, passed=True))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "refs/heads/base" in out, out


def test_a_merged_record_still_needs_its_target_sha_row(repo):
    """Only the reachability claim is dropped for an untouched record.
    `check_round`'s docstring says the row itself is still required, and
    nothing pinned it."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    body = record("0" * 40, passed=True).replace(
        "| Target SHA | 0000000", "| Nope | 0000000"
    )
    write(repo, f"{ROUNDS}/round-1.md", body)
    commit(repo, "round 1 with no Target SHA row")
    git(repo, "branch", "-f", "base", "HEAD")
    write(repo, "g.py", "y = 2\n")
    commit(repo, "later work")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "which commit this round actually looked at" in out


# --- a reviewed commit outlives the branch it was on ------------------------


def reviewed_elsewhere(repo):
    """A commit that exists, is on no branch, and is not an ancestor of HEAD.

    Which is what every squashed review round's `Target SHA` becomes: the
    squash writes a new commit and the originals live on until whoever merged
    presses Delete branch.
    """
    git(repo, "switch", "-qc", "throwaway")
    write(repo, "g.py", "y = 1\n")
    commit(repo, "the commit the round reviewed")
    sha = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(repo, "switch", "-q", "feature")
    git(repo, "branch", "-qD", "throwaway")
    return sha


def declared_round(repo, sha, pr=None, branch="gone"):
    write(repo, f"{ITEM}/routing.md", declaration(branch=branch))
    commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, pr=pr, passed=True))
    commit(repo, "round 1")


def test_a_deleted_branch_is_what_this_used_to_fail_for(repo):
    """The control, and it is a real incident rather than a hypothetical.

    A release pull request went red naming six commits across five work
    items. `delete_branch_on_merge` is false in that repository, so nothing
    deleted the branches automatically — a paragraph asked people not to, and
    five were deleted anyway."""
    sha = reviewed_elsewhere(repo)
    declared_round(repo, sha)
    code, out = run(repo)
    assert code == 1, out
    assert "not an ancestor" in out


def test_the_pull_head_that_carried_it_is_enough(repo):
    """And it needs nothing written in the record. `refs/pull/<N>/head` is
    GitHub's, a squash does not touch it and deleting the branch does not
    either."""
    sha = reviewed_elsewhere(repo)
    git(repo, "update-ref", "refs/remotes/pull/7/head", sha)
    declared_round(repo, sha)
    code, out = run(repo)
    assert code == 0, out


def test_the_record_may_name_its_pull_request_and_then_the_ref_is_exact(repo):
    """The `| PR |` row was already in the template with nothing reading it.

    Where it names a number the check looks there, and a success cannot show
    that — the answer is the same either way. The FAILURE can: it names
    `refs/pull/7/head` instead of a namespace, so a reader is told which pull
    request was supposed to carry this and did not."""
    sha = reviewed_elsewhere(repo)
    # The row's number resolves, and it is not what carries the commit.
    git(repo, "update-ref", "refs/remotes/pull/7/head", "HEAD")
    declared_round(repo, sha, pr=7)
    code, out = run(repo)
    assert code == 1, out
    assert "refs/remotes/pull/7/head" in out, out


def test_a_pull_row_naming_a_ref_this_clone_lacks_is_left_out_of_the_message(repo):
    """The row is read for the message, so the message must not name a ref
    that is not here. `refs/pull/9/head` printed by a clone that never fetched
    the namespace reads as "that pull request does not carry it" when the true
    state is "this checkout never asked" — and those are different repairs.
    The fetch line covers the second one and says so."""
    sha = reviewed_elsewhere(repo)
    declared_round(repo, sha, pr=9)
    code, out = run(repo)
    assert code == 1, out
    assert "refs/remotes/pull/9/head" not in out, out
    assert "refs/pull/*/head" in out, out


def test_a_pull_row_naming_no_number_is_not_an_error(repo):
    """`not yet opened` is the honest value while the review runs, and the
    scan covers that case with nothing written at all."""
    sha = reviewed_elsewhere(repo)
    git(repo, "update-ref", "refs/remotes/pull/7/head", sha)
    declared_round(repo, sha, pr="not yet opened")
    code, out = run(repo)
    assert code == 0, out


def test_a_tag_carrying_the_commit_does_not_count(repo):
    """The narrowness is the point. `target_refs` records what resolving a
    bare name cost — `refs/tags/` beats `refs/heads/`, and a tag carrying a
    commit nobody reviewed satisfied the check. Accepting any ref that holds
    the SHA would re-open exactly that."""
    sha = reviewed_elsewhere(repo)
    git(repo, "tag", "reviewed", sha)
    declared_round(repo, sha)
    code, out = run(repo)
    assert code == 1, out


def test_the_failure_says_which_fetch_is_missing(repo):
    """`refs/pull/*/head` is not in a default clone, so "not fetched" and "not
    there" are different repairs. A message that confuses them sends somebody
    to restore a branch that would not have helped."""
    sha = reviewed_elsewhere(repo)
    declared_round(repo, sha)
    code, out = run(repo)
    assert code == 1, out
    assert "refs/pull/*/head" in out, out
