"""A changelog fragment a commit after the build left behind is named (#797).

A work item's `changelog.md` is written by the build's last phase, and the
release gathers it verbatim. Every commit after the build — a fix pass, a fix
written after the last round, an integration commit after a sibling's squash
— can change what the work item ships, and until this arm nothing asked
whether the fragment still said so. 0.18.2 shipped three fragments their own
review rounds had made false, and #795 corrected them by hand.

`chain_check.fragment_left_behind` names the commits. It PRINTS and never
refuses, so every case here also asserts the exit status the same tree has
with the arm removed (S8): the arm is patched out in a second run and the two
codes are compared. `docs/the-record-layout.md` owns the rule the notice
names, and the last case pins that the section it names exists.

Every case builds a scratch repository with a real base branch, because the
arm is about which commits git can see after round 1's `Target SHA`. Git is
driven from Python (contract §8). The work item's id predates every cutoff
in `chain_check.py`, so the other arms print rather than fail and a case's
exit status is the arm's business alone.
"""

import importlib.util
import os
import shutil
import subprocess

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")
RULE_DOC = os.path.join(ROOT, "docs", "the-record-layout.md")

ITEM = "seal/specs/1787700000-a-work-item"
FRAGMENT = f"{ITEM}/changelog.md"
ROUNDS = f"{ITEM}/rounds"
# The section the notice names, spelled here rather than read from the
# script, so a case that asserts the notice names it is not agreeing with
# whatever the script happens to say (the reason
# `tests/test_chain_check_at_the_pull_request.py` gives for `GATE_FROM`).
SECTION = "A commit after the build brings its changelog fragment along"


def load():
    """A fresh copy of the checker, so `WORKTREE` and a patch never leak."""
    spec = importlib.util.spec_from_file_location("specseal_chain_797", CHECK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def change(repo, *paths, message="a change"):
    """One commit appending a line to each path, its full SHA returned."""
    for rel in paths:
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
    return commit(repo, message)


def _build(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("fragment-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def declaration(review="through the review chain"):
    return (
        "# 1787700000-a-work-item — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        f"| Review | {review} |\n"
        "| Destination | open the pull request |\n"
        "| Branch | feature |\n"
    )


def record(number, target, fix_range="none"):
    return (
        f"# round {number}\n\n"
        "| Field | Value |\n|---|---|\n"
        f"| Target SHA | {target} |\n"
        "| Fixes checked by | nobody — the run ended here |\n"
        f"| Fix range | {fix_range} |\n\n"
        "- [x] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        "| 🟡 1 | something | `f.py:1` | fixed | grounds |\n"
    )


def built(repo, review="through the review chain", fragment=True):
    """The build: a declaration, a fragment and a behaviour path, one commit."""
    write(repo, f"{ITEM}/routing.md", declaration(review))
    if fragment:
        write(repo, FRAGMENT, "- the build's entry\n")
    write(repo, "hooks/x.py", "x = 1\n")
    return commit(repo, "build")


def open_round(repo, number, target):
    """The round's record, committed before its fixes, as `close` expects."""
    write(repo, f"{ROUNDS}/round-{number}.md", record(number, target))
    return commit(repo, f"round {number}")


def close_round(repo, number, target, start, end):
    """The record's `Fix range`, as `round-record close` writes it."""
    count = git(repo, "rev-list", "--count", f"{start}..{end}").stdout.strip()
    span = f"`{start[:7]}..{end[:7]}`, {count} commits"
    write(repo, f"{ROUNDS}/round-{number}.md", record(number, target, span))
    return commit(repo, f"close round {number}")


def merge(repo, message, *heads):
    """A `--no-ff` merge of `heads` into whatever is checked out."""
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "merge",
        "-q",
        "--no-ff",
        "-m",
        message,
        *heads,
    )
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def check(repo, monkeypatch, capsys, arm=True):
    mod = load()
    if not arm:
        monkeypatch.setattr(mod, "fragment_left_behind", lambda *a, **k: ([], []))
    for name in ("GITHUB_EVENT_PATH", "GITHUB_HEAD_REF", "GITHUB_ACTIONS"):
        monkeypatch.delenv(name, raising=False)
    code = mod.main(["--baseline", "base", "--root", str(repo)])
    return code, capsys.readouterr().out


def judged(repo, monkeypatch, capsys):
    """The check's code and output — and S8: the code is the one the same tree
    has with the arm removed, whatever the arm printed."""
    code, out = check(repo, monkeypatch, capsys)
    without, _ = check(repo, monkeypatch, capsys, arm=False)
    assert code == without, (
        f"the arm moved the exit status from {without} to {code}. It prints "
        f"and never refuses — a stop in an unattended run for a fragment "
        f"that may be honest is what the measurement rejected:\n{out}"
    )
    return code, out


def notice(out):
    """The arm's line, or None. Every notice it writes names the section."""
    lines = [line for line in out.splitlines() if SECTION in line]
    assert len(lines) <= 1, f"one notice per work item, not {len(lines)}:\n{out}"
    return lines[0] if lines else None


# --- S1, S10: a fix range leaves the fragment behind -------------------------


def test_a_fix_range_that_leaves_the_fragment_behind_is_named(
    repo, monkeypatch, capsys
):
    """S1 and S10. The notice names the commit, the round whose range holds
    it, the behaviour path, the fragment, and the section that owns the rule
    — and says nothing is owed where the fragment still says what ships."""
    target = built(repo)
    start = open_round(repo, 1, target)
    fix = change(repo, "hooks/x.py", message="fix")
    close_round(repo, 1, target, start, fix)

    code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, f"nothing named the fix that left it behind:\n{out}"
    assert code == 0, out
    assert fix[:7] in line, line
    assert "round 1's fix range" in line, line
    assert "hooks/x.py" in line, line
    assert FRAGMENT in line, line
    assert "docs/the-record-layout.md" in line, line
    assert "as it stands" in line, (
        "the notice has to say the release gathers the fragment unchanged — "
        "that is the whole reason it is worth a line"
    )
    assert "nothing is owed" in line, (
        "an honest unchanged fragment is the common case; the notice must say "
        "so, or it reads as a refusal nobody can answer"
    )
    assert start[:7] not in line and target[:7] not in line, (
        "the round's own record commit changed only `seal/` and the build is "
        f"round 1's target — neither is a late behaviour commit:\n{line}"
    )


def test_a_head_that_moved_while_round_one_ran_is_after_the_build(
    repo, monkeypatch, capsys
):
    """The row may name two SHAs, the second a HEAD that moved mid-review
    (`templates/sdd-round.md`). The first is where the build ended, so a
    behaviour commit between the two is after it."""
    target = built(repo)
    moved = change(repo, "hooks/x.py", message="while round 1 ran")
    write(repo, f"{ROUNDS}/round-1.md", record(1, f"{target} and {moved}"))
    commit(repo, "round 1")

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert moved[:7] in line, line


# --- S2: the fragment is brought along --------------------------------------


@pytest.mark.parametrize("where", ["same commit", "later commit"])
def test_a_fragment_brought_along_is_not_named(repo, monkeypatch, capsys, where):
    """S2. In the fix's own commit or in a later one, the fragment changing
    after the last behaviour commit is the rule followed."""
    target = built(repo)
    start = open_round(repo, 1, target)
    if where == "same commit":
        fix = change(repo, "hooks/x.py", FRAGMENT, message="fix")
    else:
        change(repo, "hooks/x.py", message="fix")
        fix = change(repo, FRAGMENT, message="the fragment, brought along")
    close_round(repo, 1, target, start, fix)

    code, out = judged(repo, monkeypatch, capsys)
    assert code == 0, out
    assert notice(out) is None, out


def test_only_the_commits_after_the_fragments_last_change_are_named(
    repo, monkeypatch, capsys
):
    """S2's other half: a fragment brought along by one fix is not brought
    along by the next one, and the line is its LAST change, not its first."""
    target = built(repo)
    start = open_round(repo, 1, target)
    early = change(repo, "hooks/x.py", FRAGMENT, message="fix one")
    middle = change(repo, "hooks/x.py", message="fix two")
    change(repo, FRAGMENT, message="the fragment, brought along again")
    late = change(repo, "hooks/x.py", message="fix three")
    close_round(repo, 1, target, start, late)

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert late[:7] in line, line
    assert early[:7] not in line and middle[:7] not in line, line


# --- S3, S4: what counts as a behaviour path --------------------------------


def test_a_range_touching_only_tests_and_seal_is_not_named(repo, monkeypatch, capsys):
    """S3. A `tests` directory at any depth and the `seal/` root are not what
    a release ships."""
    target = built(repo)
    start = open_round(repo, 1, target)
    fix = change(
        repo,
        "tests/test_x.py",
        "skills/x/tests/test_y.py",
        f"{ITEM}/overview.md",
        message="fix",
    )
    close_round(repo, 1, target, start, fix)

    _code, out = judged(repo, monkeypatch, capsys)
    assert notice(out) is None, out


@pytest.mark.parametrize("path", ["agents/smith.md", "skills/x/SKILL.md"])
def test_an_instruction_is_behaviour(repo, monkeypatch, capsys, path):
    """S4. An agent's or a skill's instructions are observable behaviour
    (`skills/implement/SKILL.md` §3), so a range changing one is named."""
    target = built(repo)
    start = open_round(repo, 1, target)
    fix = change(repo, path, message="fix")
    close_round(repo, 1, target, start, fix)

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert path in line and fix[:7] in line, line


def test_a_wide_commit_lists_three_paths_and_counts_the_rest(repo, monkeypatch, capsys):
    """The commit is what the reader opens; the paths say why it was named,
    and a sweep across forty files must not make the line forty paths long."""
    target = built(repo)
    start = open_round(repo, 1, target)
    fix = change(repo, "bin/a", "bin/b", "bin/c", "bin/d", message="fix")
    close_round(repo, 1, target, start, fix)

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert "bin/a, bin/b, bin/c and 1 more" in line, line
    assert "bin/d" not in line, line


# --- S5: after the last round, and between rounds ----------------------------


@pytest.mark.parametrize("closed", [True, False])
def test_a_commit_after_the_last_round_says_so(repo, monkeypatch, capsys, closed):
    """S5. After a resolving `Fix range`, and after the record's `Target SHA`
    where the range reads `none`."""
    target = built(repo)
    start = open_round(repo, 1, target)
    if closed:
        fix = change(repo, "tests/test_x.py", message="fix")
        close_round(repo, 1, target, start, fix)
    late = change(repo, "bin/x", message="after the rounds")

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert late[:7] in line, line
    assert "after the last round" in line, line
    assert "bin/x" in line, line


def test_each_commit_is_attributed_to_the_range_that_holds_it(
    repo, monkeypatch, capsys
):
    """Two rounds: each fix is named with its own round, and a commit between
    the two ranges is named as outside every one of them."""
    target = built(repo)
    start = open_round(repo, 1, target)
    first = change(repo, "hooks/x.py", message="fix one")
    close_round(repo, 1, target, start, first)
    between = change(repo, "hooks/x.py", message="between the rounds")
    start = open_round(repo, 2, between)
    second = change(repo, "hooks/x.py", message="fix two")
    close_round(repo, 2, between, start, second)

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert f"`{first[:7]}` (round 1's fix range" in line, line
    assert f"`{between[:7]}` (outside every round's fix range" in line, line
    assert f"`{second[:7]}` (round 2's fix range" in line, line


# --- S6: an integration after a sibling's squash -----------------------------


def integrate(repo):
    """A sibling's squash lands on the base and is merged into the feature."""
    git(repo, "switch", "-q", "base")
    sibling = change(repo, "hooks/y.py", message="a sibling's squash")
    git(repo, "switch", "-q", "feature")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "merge",
        "-q",
        "--no-ff",
        "-m",
        "integrate the base",
        "base",
    )
    return sibling


def test_the_merge_of_the_base_names_nothing(repo, monkeypatch, capsys):
    """S6. The sibling's commit is the sibling's fragment's business."""
    target = built(repo)
    open_round(repo, 1, target)
    sibling = integrate(repo)

    _code, out = judged(repo, monkeypatch, capsys)
    assert notice(out) is None, out
    assert sibling[:7] not in out, out


def test_an_own_commit_after_the_merge_is_named_alone(repo, monkeypatch, capsys):
    """S6. The item's own commit after the integration counts like any
    other, and the sibling's commit it brought stays unnamed."""
    target = built(repo)
    open_round(repo, 1, target)
    sibling = integrate(repo)
    own = change(repo, "hooks/y.py", message="adapt to the sibling")

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert own[:7] in line, line
    assert sibling[:7] not in line, line


def ci_merge_ref(repo):
    """What `actions/checkout` gives a `pull_request` run with no `ref:`: the
    pull request's head merged into the base, the base as the FIRST parent,
    on a detached HEAD."""
    head = git(repo, "rev-parse", "feature").stdout.strip()
    git(repo, "switch", "-q", "--detach", "base")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "merge",
        "-q",
        "--no-ff",
        "-m",
        "Merge the pull request's head into the base",
        head,
    )


@pytest.mark.parametrize("sibling_landed", [True, False])
def test_the_ci_merge_ref_names_the_items_commit_and_not_the_siblings(
    repo, monkeypatch, capsys, sibling_landed
):
    """Round 1's 🔴 1 of #797, and S8 of #860. From CI's merge ref the
    first-parent walk was the base's: it read a sibling's squash as *after
    the last round* and never reached the item's own fix. The walk is the
    commits that descend from round 1's target, and the sibling's descends
    from it never, so CI names what a branch checkout names with no case of
    its own for the merge ref."""
    target = built(repo)
    start = open_round(repo, 1, target)
    fix = change(repo, "hooks/x.py", message="fix")
    close_round(repo, 1, target, start, fix)
    sibling = None
    if sibling_landed:
        git(repo, "switch", "-q", "base")
        sibling = change(repo, "hooks/sibling.py", message="a sibling's squash")
        git(repo, "switch", "-q", "feature")
    ci_merge_ref(repo)

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, f"the merge ref hid the item's own fix:\n{out}"
    assert f"`{fix[:7]}` (round 1's fix range" in line, line
    assert "after the last round" not in line, line
    if sibling is not None:
        assert sibling[:7] not in line, line


def test_a_topic_merged_into_the_branch_names_the_branchs_fix_and_the_topics_commit(
    repo, monkeypatch, capsys
):
    """S9 of #860, its first half. A topic cut from the branch after round 1's
    target and merged back in is the item's own history, whichever parent of
    the merge it sits behind. The first-parent walk read the branch's fix and
    never the topic's behaviour commit; the walk over the commits that
    descend from the target reads both."""
    target = built(repo)
    start = open_round(repo, 1, target)
    git(repo, "switch", "-qc", "side")
    side = change(repo, "hooks/side.py", message="a topic commit")
    git(repo, "switch", "-q", "feature")
    fix = change(repo, "hooks/x.py", message="fix")
    close_round(repo, 1, target, start, fix)
    merge(repo, "merge the topic", "side")

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert f"`{fix[:7]}` (round 1's fix range" in line, line
    assert f"`{side[:7]}` (outside every round's fix range" in line, (
        f"the topic's behaviour commit descends from round 1's target and was "
        f"not named:\n{line}"
    )


@pytest.mark.parametrize("fragment_after_the_merge", [True, False])
def test_a_fragment_change_clears_exactly_the_commits_it_descends_from(
    repo, monkeypatch, capsys, fragment_after_the_merge
):
    """S9 of #860, its second half. A commit is named when no own commit that
    changed the fragment descends from it. The fragment brought along on the
    main line after the topic is merged clears the topic's commit; brought
    along on the main line before the merge, it does not, because the topic's
    commit is not in its history — and no tie-break between two commits
    neither of which descends from the other decides it."""
    target = built(repo)
    open_round(repo, 1, target)
    git(repo, "switch", "-qc", "side")
    side = change(repo, "hooks/side.py", message="a topic commit")
    git(repo, "switch", "-q", "feature")
    fix = change(repo, "hooks/x.py", message="fix")
    if fragment_after_the_merge:
        merge(repo, "merge the topic", "side")
        change(repo, FRAGMENT, message="the fragment, brought along")
    else:
        change(repo, FRAGMENT, message="the fragment, brought along")
        merge(repo, "merge the topic", "side")

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    if fragment_after_the_merge:
        assert line is None, out
        return
    assert line is not None, f"the topic's commit was cleared:\n{out}"
    assert side[:7] in line, line
    assert fix[:7] not in line, (
        f"the fix is in the fragment commit's history and was named:\n{line}"
    )


def test_a_branch_rebuilt_on_the_base_names_its_own_commits_and_not_the_siblings(
    repo, monkeypatch, capsys
):
    """S7, #805's shape. The branch is reset to the base and its old tip
    merged in, so the merge's FIRST parent is the base, and one more own
    commit lands on top. HEAD is no merge, so the walk that read HEAD's
    parent order went down the base: it named a sibling's squash and missed
    the item's own lagging fix. Descent from round 1's target separates the
    two whatever the parent order."""
    target = built(repo)
    start = open_round(repo, 1, target)
    fix = change(repo, "hooks/x.py", message="a lagging fix")
    close_round(repo, 1, target, start, fix)
    old = git(repo, "rev-parse", "feature").stdout.strip()
    git(repo, "switch", "-q", "base")
    sibling = change(repo, "hooks/sibling.py", message="a sibling's squash")
    git(repo, "switch", "-q", "feature")
    git(repo, "reset", "-q", "--hard", "base")
    merge(repo, "the old branch, merged onto the base", old)
    own = change(repo, "hooks/z.py", message="one more own commit")

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert sibling[:7] not in line, (
        f"a sibling's squash on the base was named as the item's:\n{line}"
    )
    assert f"`{fix[:7]}` (round 1's fix range" in line, line
    assert f"`{own[:7]}` (after the last round" in line, line


def test_of_several_merged_heads_only_the_commits_descending_from_round_one_are_named(
    repo, monkeypatch, capsys
):
    """S8 of #860. An octopus of the base, an unrelated head and the branch:
    the branch's fix descends from round 1's target and the unrelated head's
    commit does not, whichever parent each sits behind."""
    target = built(repo)
    start = open_round(repo, 1, target)
    fix = change(repo, "hooks/x.py", message="fix")
    close_round(repo, 1, target, start, fix)
    git(repo, "switch", "-q", "base")
    git(repo, "switch", "-qc", "unrelated")
    stray = change(repo, "hooks/stray.py", message="an unrelated head")
    git(repo, "switch", "-q", "--detach", "base")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "merge",
        "-q",
        "--no-ff",
        "-m",
        "an octopus",
        "unrelated",
        "feature",
    )

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert fix[:7] in line, line
    assert stray[:7] not in line, line


def test_an_honest_fragment_on_the_ci_merge_ref_is_not_named(repo, monkeypatch, capsys):
    """Round 1's 🔴 1, the other direction: an item that brought its fragment
    along was told a sibling's squash had left it behind."""
    target = built(repo)
    start = open_round(repo, 1, target)
    fix = change(repo, "hooks/x.py", FRAGMENT, message="fix")
    close_round(repo, 1, target, start, fix)
    git(repo, "switch", "-q", "base")
    change(repo, "hooks/sibling.py", message="a sibling's squash")
    git(repo, "switch", "-q", "feature")
    ci_merge_ref(repo)

    _code, out = judged(repo, monkeypatch, capsys)
    assert notice(out) is None, out


@pytest.mark.parametrize("destination", ["tests/x.py", "seal/x.py"])
def test_a_behaviour_file_moved_out_of_what_ships_is_named(
    repo, monkeypatch, capsys, destination
):
    """Round 1's 🟡 2. With rename detection a move is listed by its
    destination alone, so a hook moved under `tests/` or `seal/` left what
    ships and was never named — and whether a move was detected followed the
    reader's own `diff.renames`."""
    target = built(repo)
    open_round(repo, 1, target)
    (repo / destination).parent.mkdir(parents=True, exist_ok=True)
    git(repo, "mv", "hooks/x.py", destination)
    moved = commit(repo, "move the hook out of what ships")

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert moved[:7] in line and "hooks/x.py" in line, line


# --- S7: the silent states ---------------------------------------------------


def test_no_round_one_is_silent(repo, monkeypatch, capsys):
    """No `round-1.md`: nothing says where the build ended."""
    target = built(repo)
    write(repo, f"{ROUNDS}/round-2.md", record(2, target))
    commit(repo, "a round 2 alone")
    change(repo, "hooks/x.py", message="a late fix")

    _code, out = judged(repo, monkeypatch, capsys)
    assert notice(out) is None, out


def test_an_unresolvable_target_is_silent(repo, monkeypatch, capsys):
    """Round 1's `Target SHA` squashed away: no line to draw."""
    built(repo)
    open_round(repo, 1, "0123456789abcdef0123456789abcdef01234567")
    change(repo, "hooks/x.py", message="a late fix")

    _code, out = judged(repo, monkeypatch, capsys)
    assert notice(out) is None, out


def test_a_target_head_does_not_descend_from_is_silent(repo, monkeypatch, capsys):
    """A rebase leaves round 1's target resolving and off the branch. Walking
    `<target>..HEAD` would then read the build itself as late, and nothing
    after the build changes a behaviour path here."""
    git(repo, "switch", "-qc", "elsewhere")
    elsewhere = change(repo, "f.py", message="the build before a rebase")
    git(repo, "switch", "-q", "feature")
    built(repo)
    change(repo, "hooks/x.py", message="the build's last commit")
    open_round(repo, 1, elsewhere)

    _code, out = judged(repo, monkeypatch, capsys)
    assert notice(out) is None, out


def test_no_fragment_at_head_is_silent(repo, monkeypatch, capsys):
    """Whether an item owes a fragment is not this question."""
    target = built(repo, fragment=False)
    open_round(repo, 1, target)
    change(repo, "hooks/x.py", message="a late fix")

    _code, out = judged(repo, monkeypatch, capsys)
    assert notice(out) is None, out


def test_straight_to_the_pr_is_silent(repo, monkeypatch, capsys):
    """No rounds, so nothing separates the build from what came after it."""
    target = built(repo, review="straight to the PR")
    open_round(repo, 1, target)
    change(repo, "hooks/x.py", message="a late fix")

    _code, out = judged(repo, monkeypatch, capsys)
    assert notice(out) is None, out


# --- the section the notice names --------------------------------------------


def test_the_section_the_notice_names_exists():
    """A notice sending its reader to a heading nobody wrote is a dead link.
    The script's constant and the document's heading are one spelling."""
    mod = load()
    assert mod.FRAGMENT_RULE == SECTION
    with open(RULE_DOC, encoding="utf-8") as f:
        headings = [line.lstrip("#").strip() for line in f if line.startswith("## ")]
    assert SECTION in headings, headings
