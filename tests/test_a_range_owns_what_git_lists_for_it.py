"""A range owns exactly the commits git lists for it, in every merge shape.

`docs/the-record-layout.md` §*A range owns the commits that descend from its
start* states the rule once: a range `a..b` owns exactly the commits `git log
--ancestry-path --no-merges a..b` lists (`chain_check.own_commits`). Three
review rounds of #860 each found a sentence beside that rule — an example
phrased by merge shape or by time — false in a shape its author had not
built. The reframe after round 3 moved every shape here: a shape is a case
asserting what `own_commits` returns, never a sentence in a document. A shape
this module lacks is answered by running `own_commits` on it, and the answer
may become a case here.

Each case builds the history the round's probe built and asserts the subjects
of the commits `own_commits(T, HEAD)` lists, as a set, since commits made in
one second have no order git promises — and `touched`'s paths where the probe
read them. `T` is the range's start: round 1's target, or a record's `Fix
range` start. Each case was seen red by a mutation of `own_commits`, with
`--ancestry-path` dropped or `--first-parent` added (`phases/phase-5.md` of
work item 1791384160 says which mutation turned which case).

Git is driven from Python (contract §8); each repository is built inside the
case.
"""

import shutil

import pytest
from test_the_record_is_generated import check_module, generator_module, git, write


def commit(repo, message, path=None):
    """One commit appending `message` to `path` (or an empty one), its SHA."""
    if path is not None:
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "a", encoding="utf-8") as handle:
            handle.write(f"{message}\n")
        git(repo, "add", "-A")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "commit",
        "-q",
        "--allow-empty",
        "-m",
        message,
    )
    return git(repo, "rev-parse", "HEAD").stdout.strip()


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


def switch(repo, *args):
    git(repo, "switch", "-q", *args)


def _build(d):
    """`base` holds one commit; `feature` is cut from it."""
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "README.md", "# a fixture\n")
    git(d, "add", "-A")
    commit(d, "root")
    switch(d, "-c", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("own-commits-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def owned(repo, start, end="HEAD"):
    """The subjects of the commits `own_commits(start, end)` lists, as a set."""
    commits = check_module().own_commits(str(repo), start, end)
    assert commits is not None, "git failed under own_commits"
    return {
        git(repo, "log", "-1", "--format=%s", full).stdout.strip()
        for full, _short, _changes in commits
    }


def touched(repo, start, end="HEAD"):
    full = git(repo, "rev-parse", end).stdout.strip()
    return generator_module().touched(str(repo), start, full)


def test_a_back_merge_then_a_commit_on_the_base(repo):
    """Shape A (round 1). The base merges the branch after `T`, a commit lands
    on the base, and the branch merges the base: that commit has `T` as an
    ancestor, so it is listed, and its path is read."""
    t = commit(repo, "T", "own.py")
    commit(repo, "f1", "own.py")
    switch(repo, "base")
    merge(repo, "the base merges the branch", "feature")
    commit(repo, "S", "sib.py")
    switch(repo, "feature")
    merge(repo, "the branch merges the base", "base")
    commit(repo, "f2", "own.py")
    assert owned(repo, t) == {"f1", "S", "f2"}
    assert touched(repo, t) == ["own.py", "sib.py"]


def test_the_base_merges_a_commit_older_than_the_start(repo):
    """Shape A2 (round 2). The base merges the branch at a commit made before
    `T`, then a commit lands on the base, and the branch merges the base:
    that commit does not have `T` as an ancestor, so it is not listed."""
    p1 = commit(repo, "p1", "own.py")
    t = commit(repo, "T", "own.py")
    switch(repo, "base")
    merge(repo, "the base merges the stack", p1)
    commit(repo, "S", "sib.py")
    switch(repo, "feature")
    merge(repo, "the branch merges the base", "base")
    commit(repo, "f2", "own.py")
    assert owned(repo, t) == {"f2"}
    assert touched(repo, t) == ["own.py"]


def test_a_topic_cut_before_the_start_and_merged_after(repo):
    """Shape B (round 1). A topic cut before `T` makes a commit and is merged
    after `T`: that commit does not have `T` as an ancestor."""
    switch(repo, "-c", "topic")
    commit(repo, "topic-fix", "topic.py")
    switch(repo, "feature")
    t = commit(repo, "T", "own.py")
    commit(repo, "f", "own.py")
    merge(repo, "the branch merges the topic", "topic")
    assert owned(repo, t) == {"f"}
    assert touched(repo, t) == ["own.py"]


def test_a_topic_that_merges_the_start_and_then_commits(repo):
    """Shape B2 (round 2). A topic cut before `T` merges the branch at `T`,
    then makes a commit, and is merged: that commit has `T` as an ancestor."""
    switch(repo, "-c", "topic")
    switch(repo, "feature")
    t = commit(repo, "T", "own.py")
    switch(repo, "topic")
    merge(repo, "the topic merges the branch", t)
    commit(repo, "topic-fix", "topic.py")
    switch(repo, "feature")
    merge(repo, "the branch merges the topic", "topic")
    assert owned(repo, t) == {"topic-fix"}
    assert touched(repo, t) == ["topic.py"]


def test_a_topic_that_commits_and_then_merges_the_start(repo):
    """Shape B3 (round 3). A topic cut before `T` makes a commit, then merges
    the branch at `T`, and is merged: that commit does not have `T` as an
    ancestor, and nothing is listed."""
    switch(repo, "-c", "topic")
    commit(repo, "topic-fix", "topic.py")
    switch(repo, "feature")
    t = commit(repo, "T", "own.py")
    switch(repo, "topic")
    merge(repo, "the topic merges the branch", t)
    switch(repo, "feature")
    merge(repo, "the branch merges the topic", "topic")
    assert owned(repo, t) == set()
    assert touched(repo, t) == []


def test_a_branch_cut_from_the_base_before_it_merged_the_start(repo):
    """Shape C (round 3). The base merges the branch at `T`; a branch cut
    from the base before that merge makes a commit and is merged into the
    base; the branch merges the base. That commit does not have `T` as an
    ancestor."""
    t = commit(repo, "T", "own.py")
    switch(repo, "base")
    switch(repo, "-c", "other")
    switch(repo, "base")
    merge(repo, "the base merges the branch", t)
    switch(repo, "other")
    commit(repo, "S", "sib.py")
    switch(repo, "base")
    merge(repo, "the base merges the other branch", "other")
    switch(repo, "feature")
    commit(repo, "f2", "own.py")
    merge(repo, "the branch merges the base", "base")
    assert owned(repo, t) == {"f2"}
    assert touched(repo, t) == ["own.py"]


def shape_d(repo):
    """Shape D (round 3). The base merges the branch at `T`, a commit lands on
    the base, and the branch makes `f2` without merging the base."""
    t = commit(repo, "T", "own.py")
    switch(repo, "base")
    merge(repo, "the base merges the branch", t)
    commit(repo, "S", "sib.py")
    switch(repo, "feature")
    commit(repo, "f2", "own.py")
    return t


def test_a_back_merge_read_from_the_branch_and_from_cis_merge_ref(repo):
    """Shape D, read from both checkouts in one case. On the branch HEAD does
    not reach the base's commit, so only `f2` is listed. On CI's merge ref —
    the pull request's head merged into the base, the base as the first
    parent — HEAD reaches it, and it has `T` as an ancestor, so it is listed
    beside `f2`. One case rather than two, because the branch's half is a
    straight line every reading of a range agrees on, and no mutation of
    `own_commits` could turn it red alone."""
    t = shape_d(repo)
    assert owned(repo, t) == {"f2"}
    assert touched(repo, t) == ["own.py"]
    switch(repo, "--detach", "base")
    merge(repo, "merge the pull request's head into the base", "feature")
    assert owned(repo, t) == {"S", "f2"}
    assert touched(repo, t) == ["own.py", "sib.py"]
