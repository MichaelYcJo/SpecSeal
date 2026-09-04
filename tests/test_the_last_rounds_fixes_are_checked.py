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
               by `chain_check.py` on EVERY record -- `Pass` is the claim read
               on the last one alone. Only a LATER round may be named, so a
               round cannot certify its own fixes, and reading the last record
               alone would leave that value unreachable
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

# A work item begun before `chain_check.STRICT_FROM`, so `Pass` beside
# `nobody` prints here instead of failing.
ITEM = "seal/specs/1787700000-a-work-item"
ROUNDS = f"{ITEM}/rounds"
# One begun after it. The two directories differ only in the second their
# names start with, which is the whole of what the grandfathering reads.
STRICT_ITEM = "seal/specs/1799000000-a-later-work-item"


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


def declaration(item=None):
    return (
        f"# {os.path.basename(item or ITEM)} — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n"
        "| Branch | feature |\n"
    )


def record(sha, checked_by, verdict="fixed", finding="🟢 1", passed=True):
    """A passing round record but for the `Fixes checked by` cell.

    Everything else is deliberately clean -- a checked `Pass`, a reachable
    target, a closed finding -- so a failure can only have come from the one
    row each case is about. `checked_by=None` leaves the row out, and
    `passed=False` leaves the box unticked, which is the other half of the
    `Pass` beside `nobody` refusal.
    """
    who = f"| Fixes checked by | {checked_by} |\n" if checked_by is not None else ""
    # The fix-surface rows are `none` so a failure can only come from the row
    # each case is about; `STRICT_ITEM` began after `SURFACE_FROM`, so leaving
    # them out would fail every record for a rule this file is not pinning.
    who += "| Contract changes | none |\n| New units | none |\n"
    # The floor row goes in for the same reason and against the same cutoff:
    # `STRICT_ITEM` began after `chain_check.FLOOR_FROM`, so a record without
    # it would fail every case here for a rule this file does not pin.
    who += "| Loses a record or crashes | no |\n| Needs a fix | no |\n"
    return (
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n{who}\n"
        f"- [{'x' if passed else ' '}] Pass\n\n"
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


def declared(repo, *, item=None, **rounds):
    """Write the declaration and one record per `roundN=body` keyword.

    `item` picks the work-item directory, which is not decoration: its
    timestamp prefix is what `chain_check.STRICT_FROM` compares against, so
    the default `ITEM` is grandfathered and `STRICT_ITEM` is not.

    Each record lands in its own commit and is handed the HEAD that existed
    before it, so round 2's `Target SHA` is a DESCENDANT of round 1's. That
    is what a real run looks like — the fixes are what moved HEAD between the
    rounds — and it matters here: every record sharing one commit made the
    passing shape indistinguishable from a round that reviewed the same tree
    it was supposed to be checking the fixes to.
    """
    item = item or ITEM
    write(repo, f"{item}/routing.md", declaration(item))
    sha = commit(repo, "declare")
    for name, body in rounds.items():
        write(repo, f"{item}/rounds/{name.replace('round', 'round-')}.md", body(sha))
        sha = commit(repo, name)
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


def test_a_checker_that_reviewed_the_same_commit_fails(repo):
    """S4b. The number is later and the review is not.

    Rounds are cheap to number and expensive to run. Two records carrying one
    `Target SHA` mean round 2 opened the tree round 1 opened — and the fixes
    that closed round 1 were written after both of them, so no part of what
    the cell claims happened. Comparing round numbers alone said nothing
    about this and exited 0.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, "round-2"))
    write(
        repo,
        f"{ROUNDS}/round-2.md",
        record(sha, "no fixes to check", verdict="answered"),
    )
    commit(repo, "both rounds in one commit")
    code, out = run(repo)
    assert code == 1, out
    assert "reviewed the same commit" in out


def test_a_checker_that_reviewed_an_earlier_commit_fails(repo):
    """S4c. The same fact one step weaker, and it is the shape a rebase or a
    copied record produces: round 2's target is an ancestor of round 1's, so
    it read a tree that predates the fixes it claims to have opened."""
    write(repo, f"{ITEM}/routing.md", declaration())
    early = commit(repo, "declare")
    write(repo, "f.py", "x = 2\n")
    late = commit(repo, "move HEAD")
    write(repo, f"{ROUNDS}/round-1.md", record(late, "round-2"))
    write(
        repo,
        f"{ROUNDS}/round-2.md",
        record(early, "no fixes to check", verdict="answered"),
    )
    commit(repo, "rounds")
    code, out = run(repo)
    assert code == 1, out
    assert "reviewed an EARLIER tree" in out


def two_targets(first, second):
    """A `Target SHA` cell naming both commits, the way the template allows.

    `templates/sdd-round.md` says *both, if HEAD moved mid-review*, and every
    comparison below has to read the NEWEST of them on each side. Reading the
    checker's newest against this record's FIRST was a hole: it let a round
    that read exactly what this round read pass as its checker.
    """
    return f"`{first}`, and `{second}` after this round's fixes"


def test_a_checker_whose_newest_tree_is_this_records_newest_fails(repo):
    """S4d. The two-SHA spelling of the same-commit refusal.

    Round 1 opened `A` and saw `B` before it finished; round 2 opened `B`.
    Nothing moved between them, so round 2 read exactly what round 1 read and
    cannot have opened the fixes that closed it — the identical fact
    `test_a_checker_that_reviewed_the_same_commit_fails` pins for one SHA
    each. Compared against round 1's FIRST SHA this exited 0, where two
    records at a single shared SHA correctly exited 1.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    early = commit(repo, "declare")
    write(repo, "f.py", "x = 2\n")
    late = commit(repo, "HEAD moved mid-review")
    write(repo, f"{ROUNDS}/round-1.md", record(two_targets(early, late), "round-2"))
    write(
        repo,
        f"{ROUNDS}/round-2.md",
        record(late, "no fixes to check", verdict="answered"),
    )
    commit(repo, "rounds")
    code, out = run(repo)
    assert code == 1, out
    assert "reviewed the same commit" in out


def test_a_checker_that_moved_past_this_records_tree_passes(repo):
    """The other side of the same read, and the reason it is `theirs[-1]`.

    Round 2 opened the tree round 1 reviewed and then HEAD moved, so its
    newest tree is later than anything round 1 saw. That is a real verifying
    round with a real fix diff in it, and reading the checker's FIRST SHA
    instead would refuse it for the commit it started at.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    early = commit(repo, "declare")
    write(repo, "f.py", "x = 2\n")
    late = commit(repo, "the fixes")
    write(repo, f"{ROUNDS}/round-1.md", record(early, "round-2"))
    write(
        repo,
        f"{ROUNDS}/round-2.md",
        record(two_targets(early, late), "no fixes to check", verdict="answered"),
    )
    commit(repo, "rounds")
    code, out = run(repo)
    assert code == 0, out


def test_two_records_naming_one_commit_git_cannot_see_still_fails(repo):
    """The squash path, which is the only reading left when git has neither.

    A squash discards the commits a round reviewed, so *cannot be compared* is
    the ordinary state of a merged record and passing there is right. What is
    still refusable is two records naming the SAME unresolvable commit: the
    written cells are equal whatever git can no longer resolve, and the
    inversion is established without resolving anything.

    Neither of the first two records is the run's last, so no reachability
    claim is made about the commit they name — that check reads `records[-1]`
    alone, and round 3 carries a commit this repository does carry.
    """
    gone = "0" * 40
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(gone, "round-2"))
    write(repo, f"{ROUNDS}/round-2.md", record(gone, "round-3"))
    write(
        repo,
        f"{ROUNDS}/round-3.md",
        record(sha, "no fixes to check", verdict="answered"),
    )
    commit(repo, "rounds")
    code, out = run(repo)
    assert code == 1, out
    assert "reviewed the same commit" in out


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
# closed verdict in `seal/specs/*/rounds/round-*.md` reads `**fixed**`, usually
# with
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
    """Only the HEAD of the cell is consulted, never the whole of it.

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


# Round 2 opened a 🔴 at the site round 1 was closing, and the four cases below
# are the replacement's own coverage.
#
# What round 1 shipped located the commit citation with a regex and cut the
# cell there. The pattern required a digit inside the hex run, so on a real
# abbreviation carrying none it did not cut LATE -- it did not cut at all, and
# `**fixed** `deadbee`` normalized to `fixed deadbee`, a verdict in neither
# set. A 🔴 that was properly closed read as still open, at about one
# seven-character abbreviation in 959 and in the exact spelling this
# repository's house style writes.
#
# `verdict_of` now matches the vocabulary as a PREFIX of the cell and never
# recognises a commit at all, so the digit question is gone rather than moved.
# These pin the two directions of that and the two readings it must not
# acquire while gaining them.

NO_DIGIT_CITATIONS = ["deadbee", "defaced", "acceded", "dbaeded"]


@pytest.mark.parametrize("abbrev", NO_DIGIT_CITATIONS)
def test_a_commit_abbreviation_with_no_digit_is_still_a_fix(repo, abbrev):
    """The blocker, in the direction that let a contradiction through.

    Each of these is seven characters of [0-9a-f] and carries no digit, which
    is the whole of what the old pattern needed to fail. `no fixes to check`
    beside `**fixed** `deadbee`` is the same contradiction-inside-one-file as
    beside `**fixed** `abc123d``, and it exited 0.
    """
    declared(
        repo,
        round1=lambda sha: record(sha, "no fixes to check", f"**fixed** `{abbrev}`"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "closed on a fix" in out


@pytest.mark.parametrize("abbrev", NO_DIGIT_CITATIONS)
def test_a_blocking_finding_closed_at_such_a_commit_is_closed(repo, abbrev):
    """The same defect in the direction that fails a correct record.

    This is what round 2 executed: a 🔴 closed as `**fixed** `deadbee`` read
    as still open, so a round that closed its blocker honestly could not check
    its own `Pass`.
    """
    declared(
        repo,
        round1=lambda sha: record(
            sha,
            "nobody — the run ended here",
            f"**fixed** `{abbrev}`",
            finding="🔴 1",
        ),
    )
    code, out = run(repo)
    assert code == 0, out


def test_a_cell_that_negates_the_verdict_word_counts_open(repo):
    """The unsafe direction stays closed.

    `not fixed` begins with no word in the vocabulary, so it is not a verdict
    this can read and an unreadable verdict counts OPEN — the direction
    `CLOSED_WORDS` states above itself. A reader that looked for `fixed`
    anywhere in the cell would close a 🔴 the cell says is not closed.
    """
    declared(
        repo,
        round1=lambda sha: record(
            sha, "nobody — the run ended here", "not fixed", finding="🔴 1"
        ),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "not fixed" in out


def test_the_vocabulary_is_matched_as_a_word_and_not_as_a_prefix(repo):
    """`not a defect` and `not a defective reading` are opposite verdicts.

    The match ends at a space or a comma. Without that boundary the shorter
    spelling swallows the longer one and a 🔴 whose grounds say the reviewer's
    reading was defective reads as a 🔴 the reviewer withdrew.
    """
    declared(
        repo,
        round1=lambda sha: record(
            sha,
            "nobody — the run ended here",
            "not a defective reading of the spec, so still open",
            finding="🔴 1",
        ),
    )
    code, out = run(repo)
    assert code == 1, out


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


# --- `Pass` beside `nobody`, and the cutoff that makes it fail -------------
#
# Q1, answered by the repository owner: refuse it, but only for records whose
# work item began after the rule landed. Grounds, and they are the owner's — a
# check whose first production act is red on merged history nobody can repair
# is a check people learn to skip, and a check whose strongest statement is a
# print does not stop a failure mode measured at a 100% hit rate.


def test_pass_beside_nobody_fails_a_work_item_begun_after_the_cutoff(repo):
    """The refusal, on the only records that can honestly answer it.

    `Pass` says no finding in this round's table is open; `nobody` says the
    work that closed them was read by no one. Both can be true, which is why
    this is not the contradiction-inside-one-file the other refusals catch —
    it is a state, refused for the items that could have avoided it.
    """
    declared(
        repo,
        item=STRICT_ITEM,
        round1=lambda sha: record(sha, "nobody — the run ended here"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "opened by nobody" in out
    assert "costs no round" in out, (
        "a refusal with no way out is a wall — the way out is one verifying "
        "round, and under the cap rule it costs nothing"
    )


def test_the_same_record_only_prints_for_an_item_begun_before_it(repo):
    """The grandfathering, which is the whole of what makes the refusal
    shippable. `seal/specs/1788184145-…/rounds/round-3.md` is in exactly this
    state
    in this repository, it is merged, and there is no honest repair: writing a
    `round-4.md` for a review nobody ran fabricates one, and unchecking its
    `Pass` fails the ready-pull-request rule instead."""
    declared(repo, round1=lambda sha: record(sha, "nobody — the run ended here"))
    code, out = run(repo)
    assert code == 0, out
    assert "opened by nobody" in out


def test_a_work_item_begun_at_the_cutoff_second_is_held_to_the_rule(repo):
    """The boundary is `>=`, and the item sitting on it is this one.

    `STRICT_FROM` is the id of the work item that added the rule, so the first
    item the rule reaches is the one that wrote it — that is the whole of what
    "a fresh install creates every work item after it" rests on. The two
    fixtures either side of it are hundreds of millions of seconds away and
    hold the boundary at neither, so `>=` could become `>` and the item that
    wrote the rule would quietly excuse itself.

    The second is read from `chain_check.py` rather than typed here. Typed, it
    would pin a number instead of the boundary, and a release that moved the
    cutoff would leave this case testing an ordinary grandfathered item.
    """
    began = check_module().STRICT_FROM
    declared(
        repo,
        item=f"seal/specs/{began}-the-item-that-wrote-the-rule",
        round1=lambda sha: record(sha, "nobody — the run ended here"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "opened by nobody" in out


def test_an_unchecked_pass_beside_nobody_is_not_the_claim(repo):
    """A review still running has not claimed anything. The refusal is about
    the two claims standing together, not about `nobody` on its own."""
    declared(
        repo,
        item=STRICT_ITEM,
        round1=lambda sha: record(
            sha, "nobody — the run ended here", verdict="answered", passed=False
        ),
    )
    code, out = run(repo, draft=True)
    assert code == 0, out
    assert "opened by nobody" in out


def test_an_earlier_records_nobody_is_not_the_reviews_verdict(repo):
    """`Pass` is read on the last record alone, so a checked box on round 1 is
    not the review claiming to have passed. Refusing there would fail a run
    that is behaving correctly — round 1 says `nobody` only when no round 2
    ever came, and if one did the cell names it."""
    declared(
        repo,
        item=STRICT_ITEM,
        round1=lambda sha: record(sha, "nobody — a spawn that never returned"),
        round2=lambda sha: record(sha, "no fixes to check", verdict="answered"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_a_work_item_with_no_timestamp_prefix_is_grandfathered(repo):
    """A repository that names its work items some other way has no date to
    compare. Failing its records would be failing them for a naming
    convention rather than for a state anyone chose."""
    declared(
        repo,
        item="seal/specs/a-work-item-with-no-date",
        round1=lambda sha: record(sha, "nobody — the run ended here"),
    )
    code, out = run(repo)
    assert code == 0, out
    assert "opened by nobody" in out


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


# --- three branches the first round of cases never reached ------------------


def test_a_word_that_merely_starts_with_nobody_is_not_nobody(repo):
    """The separator after `nobody`. Without it, any word beginning with
    those six letters would be read as the disclosure and its remainder as
    the reason — a tolerant read of the one value that exists to be exact."""
    declared(repo, round1=lambda sha: record(sha, "nobodys fault, really"))
    code, out = run(repo)
    assert code == 1, out
    assert "none of the three values" in out


def test_a_value_in_backticks_is_the_value(repo):
    """Every document shows the values in code fences, so a session copying
    one writes the fences too. Refusing that would fail a record for its
    markdown."""
    declared(
        repo,
        round1=lambda sha: record(sha, "`no fixes to check`", verdict="answered"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_a_checker_named_with_its_md_suffix_is_the_same_checker(repo):
    """`round-2.md` is what somebody writes after copying a filename, and it
    names the same record `round-2` does."""
    declared(
        repo,
        round1=lambda sha: record(sha, "round-2.md"),
        round2=lambda sha: record(sha, "no fixes to check", verdict="answered"),
    )
    code, out = run(repo)
    assert code == 0, out


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
        "would teach people to write none, which is the reasoning "
        "`unverified_check.py` already runs on"
    ),
}


@pytest.mark.parametrize("parts", sorted(NOBODY_COSTS))
def test_the_documents_say_what_nobody_costs(parts):
    """A trade nobody wrote down gets reverted by whoever finds it, and this
    one is the difference between refusing a claim and refusing a state."""
    text = flat(*parts)
    assert "honest" in text, "/".join(parts)
    assert NOBODY_COSTS[parts] in text, "/".join(parts)


@pytest.mark.parametrize("parts", sorted(NOBODY_COSTS))
def test_the_documents_say_why_older_records_are_excused(parts):
    """The grandfathering is the half a reader deletes as an oversight.

    Without the reason beside it, `STRICT_FROM` reads as a leftover constant
    somebody forgot to remove, and removing it turns this repository's own
    release pull request red on a record that is already merged.
    """
    text = flat(*parts)
    assert "a check people learn to skip" in text, "/".join(parts)
    assert "costs no round" in text or "does not consume the cap" in text, (
        "a refusal that names no way out is a wall, and the way out is the "
        "one thing a session meeting this failure needs to be told"
    )


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
# it, and beside it the spellings an inversion would have to produce IN THAT
# SENTENCE. The positive refuses a rewrite in place; the negative refuses the
# handful of spellings such a rewrite reaches for first.
#
# What neither refuses is a document that keeps the sentence and states the
# opposite in a paragraph somewhere else. Round 2 executed three such
# additions and all three passed. Enumeration cannot close that: a
# contradiction can be spelled any number of ways, and a check that refused
# every sentence resembling one would refuse the reasoning these documents are
# made of. So the reach is the narrow one — a rule here cannot be REWRITTEN
# silently — and a second rule added beside it contradicting the first is a
# reviewer's finding rather than this file's. Said as a reach these cases have,
# it would be the same counterfeit the paragraph above is about.

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


# The run's terminal condition needs somewhere to be written down. The warden
# is told to say whether it opened anything needing a fix, and for one release
# neither its report format nor the record template had a field for that
# answer — so the thing the run ends on lived in a transcript. These pin the
# channel end to end: the reviewer's line, the record's row, and the sentence
# saying the row is not the verdict table restated.

NEEDS_A_FIX = (
    ("agents", "warden.md"),
    ("skills", "code-review", "SKILL.md"),
    ("templates", "sdd-round.md"),
    ("docs", "review-handoff-protocol.md"),
)


@pytest.mark.parametrize("parts", NEEDS_A_FIX)
def test_the_answer_the_run_ends_on_has_a_field(parts):
    """The phrase, in every document that describes the field.

    This is the weak half deliberately: the phrase surviving anywhere in the
    file is what it asks, so a file can lose the ROW and keep this green. The
    two cases below are the strong half, one per document that carries a row,
    and they are what a rename has to get past.
    """
    text = flat(*parts)
    assert "Needs a fix" in text, "/".join(parts)
    assert "with grounds" in text or "answers with grounds" in text, (
        f"{'/'.join(parts)}: without this the row reads as the verdict count "
        "restated, and a round that reported findings the smith can answer "
        "gets counted as one that did not end the run"
    )


def test_the_protocol_carries_the_field_as_a_row_of_its_table():
    """The row a tool implementing the protocol reads, counted as a row.

    The case above asks only that the phrase survives, and it survives in four
    paragraphs of prose below the table — so renaming the row to
    `| Needs fixing |` left every case green while the field a record has to
    carry stopped being named anywhere a parser looks. The template's own row
    is already counted this way, through the same reader; the protocol's was
    not, and the protocol is the half that is tool-agnostic.
    """
    lines = reader_module().strip_comments(
        read("docs", "review-handoff-protocol.md").splitlines()
    )
    rows = [line for line in lines if line.strip().startswith("| Needs a fix")]
    assert len(rows) == 1, (
        f"the protocol's field table has {len(rows)} `Needs a fix` rows "
        "outside its comments — the prose below repeats the phrase, so only "
        "the row itself says what a record must carry"
    )
    required = rows[0].split("|")[2].strip()
    assert required.startswith("yes"), (
        f"the Required column reads `{required}` — a field the protocol does "
        "not require is a field a record can leave out"
    )


def test_the_record_template_carries_the_row_a_session_copies():
    """The warden's line has to land somewhere a session actually writes.

    The same failure as `Fixes checked by`: a field described in a comment
    beside a table it is not in is a field nobody fills.
    """
    lines = reader_module().strip_comments(
        read("templates", "sdd-round.md").splitlines()
    )
    rows = [line for line in lines if line.strip().startswith("| Needs a fix")]
    assert len(rows) == 1, (
        f"the template's field table has {len(rows)} `Needs a fix` rows "
        "outside its comments"
    )
    value = rows[0].split("|")[2].strip()
    assert value.startswith("<") and value.endswith(">"), value
    assert "`no`" in value and "`yes" in value


def test_the_reviewer_writes_the_line_the_orchestrator_copies():
    """Two agents and one string. The warden emits it, the orchestrator moves
    it into the record, and a rename on one side alone silently drops it."""
    warden = flat("agents", "warden.md")
    skill = flat("skills", "code-review", "SKILL.md")
    assert "Needs a fix: no" in warden
    assert "`Needs a fix: no`" in skill or "Needs a fix: no" in skill
    assert "| Needs a fix |" in skill, (
        "the orchestrator has to be told which row the line goes into, or the "
        "answer reaches the report and stops there"
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


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reader_module():
    """`unverified_check.py`, the same module `chain_check` loads.

    One reader, not two. `strip_comments` decides what counts as a row here
    exactly as it does when the check reads a record, and a second
    implementation in this file would be free to drift from it.
    """
    return _load(
        "specseal_reader_for_tests",
        os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py"),
    )


def check_module():
    """`chain_check.py` itself, for the constants a fixture has to sit on.

    Every case above runs the check as a subprocess, which is what a hook
    does. This is for the one thing a subprocess cannot hand back: the value
    of `STRICT_FROM`, so the work item on the cutoff can be built at whatever
    second the cutoff currently is rather than at a number typed here.
    """
    return _load("specseal_check_for_tests", CHECK)


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
