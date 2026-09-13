"""`round_record.py new` says when the commit the round read is not HEAD.

`new` is the last command the orchestrator runs before it dispatches a fix
pass. It is handed the commit the reviewer read and it can ask git for the
branch's HEAD, and until this work item it compared the two for nothing — so a
record being written after its own fixes was first said out loud at the pull
request, by `chain_check.written_late`, on a line no later commit can clear.
Work item 1789034970 is where that ends: red on a line nothing could fix, and
three bad exits.

**It prints and refuses nothing, and that is a measurement rather than a
preference.** Phase 1 of this work item measured what the refusal shape would
have cost, against a criterion fixed before the number was taken: over this
repository's own pre-squash branches — the only place the moment survives,
since a feature branch squashes into its release branch and takes the reviewed
commit with it — 40 records of 152 have a `Target SHA` that is not their adding
commit's first parent. Both of the two opened by hand differ because the
round's own paperwork landed between the review and the record.

So there are two cases here and they are the two halves of that verdict: the
ordinary equal round says nothing new, and the moved round prints the commits
between with both readings of them.

This module carries its own fixtures rather than importing
`tests/test_the_record_is_generated.py`'s. That module pins one DERIVATION per
case — what lands in which cell — and these pin what `new` says on the way past
about a commit it does not write anywhere. Sharing a scratch repository would
have tied a case about the output stream to a session-scoped fixture built for
cells.

Both cases were seen red before the observation existed — the file it is in
says how, and `phases/phase-2.md` says what the failure looked like.
"""

import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GENERATOR = os.path.join(ROOT, "skills", "code-review", "scripts", "round_record.py")

# Begun after every cutoff `chain_check.py` carries, so nothing here passes on
# a grandfathering.
ITEM = "seal/specs/1799000000-a-later-work-item"
ROUNDS = f"{ITEM}/rounds"
RAN_BY = "specseal:warden on a model"
ASKED = "Attack the parser first.\n"

# The sentence that must be absent from an ordinary round's output, and the
# two readings that must be present in a moved one's.
MOVED = "is not the branch's HEAD"
FIX_PASS_READING = "the fix pass for this round has already run"
MID_REVIEW_READING = "Or HEAD moved during the review"


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


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("head-moved-template") / "repo"
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def declared(repo):
    """The routing declaration committed. Its commit is round 1's natural
    `Target SHA`, and with nothing after it, HEAD."""
    write(
        repo,
        f"{ITEM}/routing.md",
        f"# {os.path.basename(ITEM)} — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n"
        "| Branch | feature |\n",
    )
    return commit(repo, "declare")


def report():
    return (
        "# what the round found\n\nProse about the finding.\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n|---|---|---|---|---|\n"
        "| 🔴 1 | the parser drops a row | `f.py:1` | open | executed |\n\n"
        "## Executed probes\n\n| What was run | Result |\n|---|---|\n"
        "| `pytest tests/test_x.py -q` | 3 passed |\n\n"
        "Needs a fix: yes — 🔴 1\nLoses a record or crashes: no\n"
    )


def generate(repo, target, n=1, extra=()):
    """Run `new`; return (exit code, output)."""
    scratch = repo.parent
    report_path = scratch / f"report-{n}.md"
    asked_path = scratch / f"asked-{n}.md"
    report_path.write_text(report(), encoding="utf-8")
    asked_path.write_text(ASKED, encoding="utf-8")
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    env["GH_PROMPT_DISABLED"] = "1"
    env["GH_NO_UPDATE_NOTIFIER"] = "1"
    r = subprocess.run(
        [
            sys.executable,
            GENERATOR,
            "new",
            "--item",
            str(repo / ITEM),
            "--round",
            str(n),
            "--target",
            target,
            "--report",
            str(report_path),
            "--asked",
            str(asked_path),
            "--ran-by",
            RAN_BY,
            "--baseline",
            "base",
            *extra,
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env=env,
    )
    return r.returncode, r.stdout + r.stderr


# --- A1: the ordinary correct round -----------------------------------------


def test_the_round_that_read_head_is_told_nothing_new(repo):
    """A1. The commonest state by far, and the one an observation that fires
    unconditionally would bury under a paragraph about nothing."""
    reviewed = declared(repo)
    _code, out = generate(repo, reviewed)
    assert "round-record: wrote" in out, out
    assert MOVED not in out, (
        "HEAD is the commit the round read, so there is nothing to say"
    )
    assert FIX_PASS_READING not in out, out


# --- A2: the fix pass ran first ---------------------------------------------


def test_a_round_whose_fixes_already_landed_is_told_which_commits(repo):
    """A2. What the whole work item is about: the fix pass ran before the
    record was written, and `new` is the last moment anybody can act on it."""
    reviewed = declared(repo)
    write(repo, "f.py", "x = 2\n")
    commit(repo, "fix: the parser drops a row")
    write(repo, "g.py", "y = 1\n")
    later = commit(repo, "docs: round 1's paragraph")

    _code, out = generate(repo, reviewed)
    assert MOVED in out, out
    assert reviewed[:7] in out, "the line does not name the commit the round read"
    assert later[:7] in out, "the line does not name HEAD"
    assert "2 commits stand between them" in out, out


def test_the_line_lists_the_subjects_and_not_a_count(repo):
    """The orchestrator's whole judgment here is which KIND of commit landed,
    and a fix pass and a round paragraph are indistinguishable in a number.
    Phase 1 measured the two apart by reading exactly these subjects."""
    reviewed = declared(repo)
    write(repo, "f.py", "x = 2\n")
    fix = commit(repo, "fix: the parser drops a row")
    write(repo, "g.py", "y = 1\n")
    commit(repo, "docs: round 1's paragraph")

    _code, out = generate(repo, reviewed)
    assert f"{fix[:7]} fix: the parser drops a row" in out, out
    assert "docs: round 1's paragraph" in out, out


def test_the_line_carries_both_readings(repo):
    """Two things it can mean, and `new` can tell them apart for neither. A
    line that stated one reading would send the orchestrator to the wrong
    repair three times in four."""
    reviewed = declared(repo)
    write(repo, "f.py", "x = 2\n")
    commit(repo, "fix: the parser drops a row")

    _code, out = generate(repo, reviewed)
    assert FIX_PASS_READING in out, out
    assert MID_REVIEW_READING in out, out
    assert "Target SHA" in out, (
        "the mid-review reading has a home the template already asks for, and "
        "a reading with no repair beside it is a sentence nobody can act on"
    )


def test_nothing_is_refused_and_the_line_says_so(repo):
    """`agent-contract` §14 and the measurement together. Phase 1 found 40 of
    152 correct records differing this way, so a refusal would fire on one
    correct run in four — and a printed line that READS like a refusal costs
    the orchestrator the same stop."""
    reviewed = declared(repo)
    write(repo, "f.py", "x = 2\n")
    commit(repo, "fix: the parser drops a row")

    code, out = generate(repo, reviewed)
    assert "Nothing is refused here" in out, out
    assert "40 records of 152" in out, (
        "the evidence for refusing nothing belongs beside the decision"
    )
    # The record was written, which is the half a refusal would have taken.
    assert (repo / ROUNDS / "round-1.md").exists(), out
    # `new` returns the check's own exit code, and this observation does not
    # touch it. Round 1 has an open 🔴 and an unticked `Pass`, which the check
    # judges as a draft and lets stand.
    assert code == 0, out


def test_a_target_given_as_a_revision_is_named_by_its_sha(repo):
    """`--target` legitimately takes `HEAD~1` or a branch name, and a line
    reading *the round read HEAD~1* names nothing anybody can open later.

    This case pins the PRINTED line alone, and deliberately not the record's
    own cell. `build` writes `--target` into `Target SHA` exactly as it was
    typed, so a revision there produces `| Target SHA | HEAD~1 |` and
    `chain_check` then reports *no `| Target SHA | … |` row naming a commit* —
    observed in this module's own red run of 2026-09-13. That is a defect this
    work item found and deliberately did not take: `spec.md` §Data & interfaces
    says nothing about `--target`'s signature moving, and the state is loud
    rather than silent, because `new` ends in the very check that reports it.
    `overview.md` §Not done carries the grounds.
    """
    reviewed = declared(repo)
    write(repo, "f.py", "x = 2\n")
    commit(repo, "fix: the parser drops a row")

    _code, out = generate(repo, "HEAD~1")
    assert MOVED in out, out
    assert reviewed[:7] in out, out
    assert "read HEAD~1" not in out, out
