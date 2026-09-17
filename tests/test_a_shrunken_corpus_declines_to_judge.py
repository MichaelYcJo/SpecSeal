"""The three helpers five modules now share, and the sentence a person reads.

`git ls-files` lists the index, so a tracked file the working tree has deleted
is on the list and not on disk. Five helpers in this suite used to open every
listed path, and the walk ended at the first of them: no file after it was
read and the rule the walk holds reported nothing (#432, #282).

The repair is `conftest.on_disk`, and the half that needed deciding is what a
case does with the paths it skipped. A sweep that judges what it finds is
strictly better off — on that tree it used to report nothing about any file.
A case that reads the corpus to prove an entry is still ALIVE is not: to it a
skipped file and a deleted entry are the same evidence, so a silent skip buys
it a false alarm. Those decline, through `decline_if_shrunken`.

**The reason string is why this module exists.** It is text a person reads at
a release and acts on, which `skills/agent-contract/SKILL.md` §14 says has to
be pinned in the commit that writes it — and `seal/follow-up.md`'s seventh
row is that omission in an earlier release, a refusal whose second half
nothing held. The three call sites pin their own `what`; the shape is pinned
here, once, because one function produces all three sentences.
"""

import os
import subprocess

import pytest
from conftest import build_tracked_tree, decline_if_shrunken, on_disk, shrunken_corpus


def test_on_disk_splits_a_listing_by_what_the_tree_actually_has(tmp_path):
    root = build_tracked_tree(
        tmp_path / "r",
        {"a.md": "one\n", "b/c.md": "two\n", "d.md": "three\n"},
        deleted=["b/c.md"],
    )
    present, missing = on_disk(root, ["a.md", "b/c.md", "d.md"])
    assert present == ["a.md", "d.md"]
    assert missing == ["b/c.md"]


def test_on_disk_keeps_the_order_it_was_given(tmp_path):
    """A corpus is walked in the order git listed it, and a refusal naming
    `rel:line` is read against that order."""
    root = build_tracked_tree(tmp_path / "r", {"a.md": "", "b.md": "", "c.md": ""})
    present, missing = on_disk(root, ["c.md", "a.md", "b.md"])
    assert present == ["c.md", "a.md", "b.md"]
    assert missing == []


def test_a_directory_on_the_list_is_not_a_file_that_is_there(tmp_path):
    """`os.path.isfile` rather than `os.path.exists`: a path git named that
    is now a directory has no content to read, and `open` would raise on it
    exactly the way a missing file does."""
    root = build_tracked_tree(tmp_path / "r", {"a.md": "one\n"})
    os.mkdir(os.path.join(root, "b"))
    present, missing = on_disk(root, ["a.md", "b"])
    assert present == ["a.md"] and missing == ["b"]


def test_the_reason_names_every_path_and_what_declined():
    """A count alone is a claim removed from the corpus without a word, which
    `seal/follow-up.md`'s first row calls the one direction a checker of
    claims must not fail in. The reader needs the paths in order to judge
    them by hand."""
    reason = shrunken_corpus(
        ["seal/ledger/two.md", "docs/one.md"], "the KEEP allowlist's liveness check"
    )
    assert "docs/one.md" in reason
    assert "seal/ledger/two.md" in reason
    assert "2 tracked path(s)" in reason
    assert "the KEEP allowlist's liveness check" in reason
    assert "not judging" in reason


def test_the_reason_sorts_the_paths_it_names():
    """The set a caller hands over comes from a walk, so an unsorted reason
    would read differently run to run for the same tree."""
    reason = shrunken_corpus(["b.md", "a.md"], "x")
    assert reason.index("a.md") < reason.index("b.md")


def test_declining_is_silent_when_nothing_is_missing():
    """The guard must not turn a check off on a whole tree, which is the one
    way this repair could report less than the crash it replaces."""
    assert decline_if_shrunken([], "x") is None


def test_declining_raises_the_skip_carrying_that_reason():
    with pytest.raises(pytest.skip.Exception) as declined:
        decline_if_shrunken(["docs/one.md"], "the KEEP allowlist's liveness check")
    assert str(declined.value) == shrunken_corpus(
        ["docs/one.md"], "the KEEP allowlist's liveness check"
    )


def test_the_builder_leaves_a_deleted_file_tracked(tmp_path):
    """The fixture shape itself, because a fixture that staged the removal
    would build the tree this defect is NOT about."""
    root = build_tracked_tree(
        tmp_path / "r", {"a.md": "one\n", "b.md": "two\n"}, deleted=["b.md"]
    )
    listed = subprocess.run(
        ["git", "-C", str(root), "ls-files"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    assert listed == ["a.md", "b.md"], listed
    assert not os.path.exists(os.path.join(root, "b.md"))
