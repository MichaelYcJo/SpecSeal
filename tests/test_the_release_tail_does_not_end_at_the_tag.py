"""#386 and #417: the checklist does not stop at the tag, and the merge-method
rule names the reader that arrived from outside.

  A5  a reader working down `docs/release-checklist.md` passes the tag and
      meets two boxes, each carrying the command that answers it
  A8  `docs/branch-and-release.md` names an outside directory's pinned commit
      among the readers that point at a release branch's commits by SHA, and
      the fixed-name sentence sits beside it

**A box carrying no command is the defect this work item is about**, one layer
up: #386's measurement is that a step written as a sentence beside a step with
a reader is the one that stops happening. So the command is asserted, not only
the box — and it is asserted to be a command the tree can actually run, which
is what `test_each_box_names_something_that_exists` is for. A box naming a
script nobody wrote reads exactly like a box naming one somebody did.

**Position is asserted, not just presence.** A5's *Then* is that the boxes
follow the tag. A box above `git tag` would be read before the act it is about
has happened, and a reader working down the file would tick it against the
previous release.

**Every assertion reads the file with its wraps collapsed.** These documents
are hand-wrapped at 88 columns (`tests/test_docs_line_wrap.py` covers
`docs/release-checklist.md`), so a phrase pinned as written on one line breaks
the moment a word is added earlier in the paragraph — the reader
`tests/test_a_release_is_sized_by_a_criterion.py` already uses, for the reason
its own docstring gives.

**Shown red before it was committed (§15).** Each case was run against the two
documents with the sentence or box it pins removed; the mutations and what
each case said were recorded in
phase 2 of work item `1790076050-the-release-tail-is-three-acts-no-document-names`,
whose rule `docs/branch-and-release.md` §*Cutting a release* now carries.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CHECKLIST = "docs/release-checklist.md"
BRANCHING = "docs/branch-and-release.md"

# The two commands the boxes carry. Each is a real invocation, and the second
# element is the file it has to reach, so a renamed script fails here rather
# than at a release.
COMMANDS = (
    ("gh release view vX.Y.Z", None),
    (
        "python3 .github/scripts/plugin_directory_check.py",
        ".github/scripts/plugin_directory_check.py",
    ),
)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def flat(text):
    """The text with every run of whitespace collapsed to one space."""
    return " ".join(text.split())


def section(rel, heading):
    """One `##` section's text, heading included, up to the next `##`."""
    text = read(rel)
    start = text.index(heading)
    rest = text[start + len(heading) :]
    after = re.search(r"^## ", rest, re.M)
    return heading + (rest[: after.start()] if after else rest)


def after_the_tag():
    """`docs/release-checklist.md` §6 from the tag push onward.

    A5's *Then* is about what FOLLOWS the tag. A box above `git tag` is one a
    reader working down the file ticks against the release before this one.
    """
    body = section(CHECKLIST, "## 6. After the merge")
    return body[body.index("git tag vX.Y.Z") :]


def boxes(text):
    """Every checklist box in `text`, each flattened to one line."""
    found = []
    for line in text.splitlines():
        if line.lstrip().startswith("- [ ]"):
            found.append([line])
        elif found and line.strip() and line.startswith(" " * 6):
            found[-1].append(line)
        elif found and not line.strip():
            found.append(None)
            found = [f for f in found if f is not None]
    return [flat(" ".join(block)) for block in found]


# --- A5 --------------------------------------------------------------------


def test_two_boxes_follow_the_tag_and_each_carries_its_command():
    """A5. Both halves, because either alone is the failure: a box with no
    command cannot be acted on, and a command with no box is not a step."""
    tail = after_the_tag()
    for command, _ in COMMANDS:
        assert command in flat(tail), (
            f"{CHECKLIST} §6 does not carry {command!r} after the tag, so the "
            "box it answers is one a reader cannot act on"
        )
        owning = [b for b in boxes(tail) if command in b]
        assert owning, (
            f"{command!r} is in §6 but not inside a box — a command beside a "
            "step is the shape #386 measured being skipped three times"
        )


def test_the_note_box_says_it_confirms_rather_than_performs():
    """The workflow publishes the note; the box reads whether it did. A box a
    reader takes to be the act itself is a box that gets ticked by hand on the
    release where the job went red."""
    box = [b for b in boxes(after_the_tag()) if "gh release view" in b]
    assert box, "no box carries the release-note command"
    assert "confirms the workflow fired" in box[0], (
        "the box does not say it confirms rather than performs, so a reader "
        "who finds nothing published is told nothing about where to look"
    )
    assert "publish-release.yml" in box[0], (
        "the box does not name the workflow, so there is nothing to go read "
        "when the release note is missing"
    )
    # Naming the workflow and giving a way to READ its run are two things,
    # and the box carried the first while losing the second under a measured
    # mutation. A reader who finds no release is one command short of knowing
    # why, and this repository's whole argument for the workflow shape is that
    # the answer should not be somebody remembering where to click.
    assert "gh run list" in box[0], (
        "the box names the workflow without a command that reads its run, so "
        "a missing release note sends the reader to a UI rather than to an "
        "answer"
    )


def test_the_directory_box_says_it_never_fails_a_release():
    """#417 rejected a gate keyed to the directory's state with a
    measurement. A box that reads as a gate gets treated as one, and the first
    release it reports *not listed* on stops for nothing."""
    box = [b for b in boxes(after_the_tag()) if "plugin_directory_check.py" in b]
    assert box, "no box carries the directory command"
    assert "reports and never fails" in box[0]
    for state in ("Not listed", "pinning an older commit"):
        assert state in box[0], (
            f"the box does not say what to do in the {state!r} state; the "
            "first answer it gives today is *not listed* in both directories"
        )


def test_each_box_names_something_that_exists():
    """A box naming a script nobody wrote reads exactly like a box naming one
    somebody did, and a reader finds out at the release."""
    for command, path in COMMANDS:
        if path is None:
            continue
        assert os.path.exists(os.path.join(ROOT, path)), (
            f"{CHECKLIST} §6 tells a reader to run {command!r} and {path} is "
            "not in the tree"
        )


# --- A8 --------------------------------------------------------------------


def squash_rule():
    """The paragraph enumerating who points at a release branch's commits.

    From the sentence that opens the enumeration to the next bold lead-in
    after the two this work item added, so a sentence dropped into a different
    part of the document does not satisfy these assertions.
    """
    text = read(BRANCHING)
    start = text.index("**What breaks when the last row is squashed**")
    rest = text[start:]
    end = rest.index("**This is enforced, and it was not always.**")
    return flat(rest[:end])


def test_an_outside_directory_is_in_the_enumeration():
    """A8. The rule already enumerated the rider stamps and the round records,
    both of which this repository can repair. The third reader cannot be
    repaired from here, which is the whole reason it is worth writing down."""
    rule = squash_rule()
    assert "A third reader points at those commits now" in rule, (
        f"{BRANCHING}'s squash rule no longer names the reader that arrived "
        "from outside the repository"
    )
    assert "outside this repository" in rule
    assert "pinning a commit of its source repository" in rule, (
        "the enumeration says a directory is a reader without saying what it "
        "pins, which is the fact that makes it one"
    )
    assert "docs/release-checklist.md` §6" in rule, (
        "nothing points from the rule to the box that reads what is pinned"
    )


def test_the_fixed_name_sentence_sits_beside_it():
    """A8's second half. #417 raised both together and they are one paragraph
    apart on purpose: a rename and a rewritten history break the same outside
    consumer, in the same way, for a reader who has no other reason to think
    about it."""
    rule = squash_rule()
    assert "The plugin's name is fixed" in rule, (
        f"{BRANCHING} no longer says the name is fixed; users have the plugin "
        "installed under its slug and nothing else in the tree says so"
    )
    assert "installed it under its slug" in rule, (
        "the sentence no longer says WHY the name is fixed — that people are "
        "already running it under that name — which is the half a reader "
        "needs to weigh a rename against"
    )
    assert ".claude-plugin/plugin.json` holds the one copy" in rule, (
        "the sentence says the name is fixed without saying where the one "
        "copy of it lives, so a reader cannot tell which spelling is the name"
    )


# --- the folded rule names the push that fires each act ---------------------


def release_tail_rule():
    """The standing statement the second fold wrote for this work item.

    From its fold marker in §*Cutting a release* to the next `###` heading, so
    the third-reader paragraph further down, which carries the same marker,
    is not read as part of it.
    """
    text = read(BRANCHING)
    marker = (
        "<!-- specs/1790076050-the-release-tail-is-three-acts-no-document-names -->"
    )
    start = text.index(marker) + len(marker)
    rest = text[start:]
    return flat(rest[: rest.index("### Work accumulates on a release branch")])


def test_the_label_acts_are_fired_by_the_merge_to_main_not_the_tag():
    """Round 1's 🔴 on the second fold. The statement's headline said the tag
    push fires every act after the tag, and the label acts run in the
    close-issues workflow, which fires on `push: branches: [main]` — before
    any tag exists. A reader trusting the headline looks for the label step
    in the wrong run. Nothing fires the directory check at all; a person runs
    it at the checklist's box."""
    rule = release_tail_rule()
    headline = rule[: rule.index("**", 2) + 2]
    assert "tag push" not in headline, (
        "the headline attributes every act to the tag push; the label acts "
        "fire on the merge to `main`"
    )
    assert "The merge to `main` fires the close-issues workflow" in rule, (
        "the statement does not say which push fires the label acts"
    )
    assert "Nothing fires it" in rule, (
        "the statement does not say the directory check is run by a person"
    )
