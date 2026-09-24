"""Release hygiene beyond "the changelog mentions the version".

That one is bound in `test_chain_hooks_hardening.py`. These are the two other
ways a release goes wrong inside the tree: a version number written into a
file that outlives it, and a supported-Python floor that three files state
differently.
"""

import ast
import json
import os
import re
import subprocess

from conftest import build_tracked_tree, git_listing, on_disk

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read_text(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def version(root=ROOT):
    with open(
        os.path.join(root, ".claude-plugin", "plugin.json"), encoding="utf-8"
    ) as f:
        return json.load(f)["version"]


def tracked(*prefixes, root=ROOT):
    """`(the files on disk under `prefixes`, the paths that are not)`.

    `root` is keyword-only so the prefixes keep the call shape they had, and
    it exists so a case can build a repository with a tracked-and-deleted file
    and watch the guard work; `conftest.on_disk` carries why the second half
    is returned rather than dropped.
    """
    out = git_listing(root, "ls-files", *prefixes)
    listed = [rel for rel in out if not rel.endswith((".gif", ".png", ".jpg"))]
    return on_disk(root, listed)


LOADED = (
    "skills",
    "agents",
    "docs",
    "templates",
    "README.md",
    "README.ko.md",
    "CONTRIBUTING.md",
    "install.sh",
    "uninstall.sh",
)

# A version-shaped token, with the optional `v` prefix the substring test this
# replaced caught for free. `(?!\.\d)` keeps `2.0.1.5` from reading as a
# release of this plugin, and it is the ONLY trailing guard: a single
# `(?![\w.])` swallowed a version at the END OF A SENTENCE — `right for
# 0.8.3.` answered no offender, where the substring check this replaced caught
# it (review round 1).
#
# There was a `(?!\w)` beside it, added for `v1.2.30`, and it is gone. `\d+`
# is greedy, so `v1.2.30` matches whole with or without it — measured — and
# its only remaining effect was to hide a LETTER-suffixed prerelease:
# `0.9.0rc1`, `0.9.0b1`, `0.9.0_final` all answered no offender while
# `0.9.0-rc1` was refused, so the rule turned on punctuation rather than on
# meaning. **A prerelease of a version that has not shipped is a timer**, in
# both spellings, which is what the substring check said and what the owner
# decided when the same lookahead produced a finding in three consecutive
# passes (review round 2).
#
# The LEADING `(?<![\w.])` is two guards written as one class, and each does a
# different job. Neither had an argument written down until #204, and the case
# that pins `x0.9.0` as allowed explained what the guard does rather than why
# such a token is not a timer.
#
# `\w` — a preceding word character makes the token part of a DIFFERENT
# identifier rather than another spelling of this one. `py3.13.9` names
# CPython, and no release of SpecSeal makes that number wrong. That is the
# asymmetry with the trailing side, where `rc1` is a prerelease of the SAME
# version and so is a timer: what precedes a version renames it, what follows
# it qualifies it.
#
# `.` — a preceding dot makes the match the TAIL of a longer dotted number.
# `1.9.9.9` is a build number rather than a release of anything, and without
# this half its tail `9.9.9` is refused as a version the line never named. The
# trailing `(?!\.\d)` catches such a number read from the front; this catches
# the same number read from the middle, and neither covers the other.
#
# **Neither argument reaches an uppercase `V`**, which is a version PREFIX and
# not a preceding word: `V0.9.0` is this plugin's own number in another
# spelling, and it was invisible wherever it was written (#204). So the prefix
# is `[vV]?` and both lookarounds are left exactly as they are — narrowing one
# for a single shape is what took another shape with it in round 1.
VERSION_TOKEN = re.compile(r"(?<![\w.])[vV]?(\d+\.\d+\.\d+)(?!\.\d)")

# The value the repository already tells an author to write where a real
# version would be wrong. `docs/issues-and-milestones.md` §"A rolling log is
# titled after the version it rolled from" is where that decision was made and
# where the reason for it sits; the check's own message points a reader there
# rather than restating it.
#
# It is exempt in EVERY loaded file rather than at one coordinate, because the
# whole point of an illustrative value is that the next author may write it
# anywhere. `VERSIONS_OF_ANOTHER_PRODUCT` below is pinned to its file for the
# opposite reason: that one is a fact about one comment.
ILLUSTRATIVE_VERSION = "1.2.3"

RECORDS_OF_A_MOMENT = (
    "docs/one-root-by-lifetime.md",
    "docs/one-root-by-lifetime.ko.md",
    # A trailing slash is a PREFIX, not a path. `docs/experiments/` holds
    # dated records of what was measured on a particular day, on a particular
    # build of a particular tool — the file name carries the date. Rewriting
    # the version an experiment ran against would falsify the record, which is
    # the same argument the two exact paths above already carry, applied to
    # a directory whose every future file has it too. That is what makes a
    # prefix defensible here where `docs/issues-and-milestones.md` — a
    # standing document edited every release — is not (#179).
    "docs/experiments/",
)

# A version that belongs to somebody else's product is above this plugin's
# running version by accident of arithmetic, and it is not a timer: no release
# of SpecSeal makes it wrong. Pinned to the file it is written in, so the
# exemption stays a fact about one comment rather than a hole the token can
# walk through anywhere.
VERSIONS_OF_ANOTHER_PRODUCT = {
    ("skills/implement/scripts/seal.py", "4.4.17"): (
        "bash's, named in a comment about the glob behaviour of that release"
    ),
    ("skills/implement/scripts/seal.py", "2.50.1"): (
        "git's, named in `remote_url`'s docstring as the build whose exit "
        "codes were measured. An exit code read off an unnamed git is not a "
        "measurement, and no release of SpecSeal makes the number wrong (#111)"
    ),
    ("skills/verify/scripts/broad_gate.py", "2.54.0"): (
        "git's, named in `names_a_branch`'s docstring as the build on which "
        "`--branch` was measured to EXPAND `@{-N}` and then check what it "
        "expanded to. The row above is the same fact about a different "
        "docstring, and the reason is the row above's reason: a property "
        "read off an unnamed git is not a measurement, and this one is the "
        "grounds for a guard a reader can otherwise only take on trust "
        "(#461). The pair is what makes this an entry rather than a reword — "
        "the class is *a loaded file naming the tool build a measurement was "
        "taken on*, it now has two members, and the exemption is keyed on "
        "(file, token) so neither one lets the number through anywhere else"
    ),
}


def as_release(token):
    """`v0.9.0` and `0.9.0` alike -> `(0, 9, 0)`, which compares."""
    return tuple(int(n) for n in token.lstrip("v").split("."))


# A `/` entry covers only files whose OWN NAME carries the date its argument
# rests on. `docs/experiments/README.md` is the conventions for writing a
# record — a standing document edited whenever they change — and rewriting a
# version in it falsifies no measurement. Without this, the prefix is the one
# entry a document can join by choosing its own path (review round 1).
#
# Read from the basename rather than from anywhere in the path, because a
# dated DIRECTORY would otherwise exempt every undated file inside it —
# `docs/experiments/2026-09-03-run/README.md` is the same standing document
# one level down, joining by where it sits.
DATED_RECORD = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def is_a_record_of_a_moment(rel):
    """Exact paths and, where an entry ends in `/`, every DATED file beneath
    it.

    Every entry is considered, never only the first that matches: an exact
    path written below the prefix that contains it has to keep working, and
    an early return made the list order-dependent (review round 2).
    """
    basename = rel.rsplit("/", 1)[-1]
    return any(
        rel == entry
        or (
            entry.endswith("/")
            and rel.startswith(entry)
            and DATED_RECORD.match(basename)
        )
        for entry in RECORDS_OF_A_MOMENT
    )


def shipped_versions():
    """Every version `CHANGELOG.md` records as released.

    Read by the illustrative-version case alone, and NOT the source of the
    shipped set `timers_in` keeps: the preparation commit writes the heading
    and bumps `plugin.json` together, so a changelog-derived set would wave
    through the very version being cut (#363).
    """
    return set(re.findall(r"^## (\d+\.\d+\.\d+)\b", read_text("CHANGELOG.md"), re.M))


def shipped_tags(root=ROOT):
    """Every version `root` has a `v*` tag for, bare.

    A tag exists only once the release reached `main`, which is what makes it
    the one truthful source for *shipped* — `CHANGELOG.md` gets its heading
    in the same commit that bumps the running version, and the version being
    cut is the timer the rule exists to catch. A tag that is not
    version-shaped is not a release and is dropped.
    """
    return {
        tag[1:]
        for tag in git_listing(root, "tag", "--list", "v*")
        if re.fullmatch(r"v\d+\.\d+\.\d+", tag)
    }


def timers_in(rel, text, running, shipped=frozenset()):
    """Every version-shaped token in `text` at or above `running`, less the
    ones `shipped` names.

    Answers `(line number, token)` pairs. Below `running` is history and is
    kept: `docs/issues-and-milestones.md` says in so many words that *the
    branch `release/v0.3.0` shipped as 0.2.0*, and a rule that cannot state
    that fact is refusing history rather than catching a timer. That case is
    what decides against widening to every version this repository has ever
    shipped (#179's second candidate).

    A tagged version is history by the same argument, one number higher
    (#363): `plugin.json` is bumped at the preparation commit, so from that
    commit until the next bump the running version is one that has already
    shipped, and the documents shipping with it could not name it. `shipped`
    is the set of tagged versions of the root being swept — never derived
    from `CHANGELOG.md`, whose heading lands in the bump's own commit.
    """
    if is_a_record_of_a_moment(rel):
        return []
    ceiling = as_release(running)
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        for match in VERSION_TOKEN.finditer(line):
            bare = match.group(1)
            if bare == ILLUSTRATIVE_VERSION or bare in shipped:
                continue
            # Either spelling. The refusal prints `match.group(0)` — `v4.4.17`,
            # not `4.4.17` — and tells the author to declare what it printed,
            # so a lookup on the bare token alone is a route nobody can take
            # (review round 2).
            if (rel, bare) in VERSIONS_OF_ANOTHER_PRODUCT or (
                rel,
                match.group(0),
            ) in VERSIONS_OF_ANOTHER_PRODUCT:
                continue
            if as_release(bare) >= ceiling:
                found.append((number, match.group(0)))
    return found


def what_to_write_instead():
    """The routes out of a refusal, as the failure message states them.

    #179's *Done when* makes this text a deliverable: the reason a real
    version may not be written has to reach the next author writing one, and
    the check's own message is where they will be standing. It is a function
    so a case can read the very words a person sees, rather than a copy of
    them that can drift.
    """
    return (
        f"Write the illustrative {ILLUSTRATIVE_VERSION} instead, and say "
        "beside it why the number is not real — the paragraph at "
        '`docs/issues-and-milestones.md` §"A rolling log is titled after the '
        'version it rolled from" already does exactly that, and is the model '
        "to follow. If the number belongs to another product, declare it in "
        "`VERSIONS_OF_ANOTHER_PRODUCT` with the product it names. If the "
        "file's whole job is to name a moment, it belongs in "
        '`RECORDS_OF_A_MOMENT` with the argument CONTRIBUTING.md §"What a '
        'change to a gate must carry" asks for. A version BELOW the running '
        "one, or one this repository has TAGGED, is history and is already "
        "allowed — nothing needs doing to it. "
        "And if the number is not a release at all — a date written with "
        "dots, say — there is no exemption for it and none is wanted: write "
        "it in a form that is not version-shaped. This repository writes a "
        "date as 2026-09-03, with dashes, which this check does not read."
    )


def refusal(running, offenders):
    """The whole text the check prints, so a case can read what it prints.

    Extracted for the same reason `what_to_write_instead` was: with the
    message inline in the `assert`, an edit that stops calling the builder
    leaves every case green — measured, review round 2.
    """
    return (
        f"a loaded file names a version at or above the running {running}. "
        "Such a line is right for exactly one release and a timer before it: "
        "it goes red on the day that version ships, on the release's own "
        "preparation commit, after the broad gate has already run.\n  "
        + "\n  ".join(offenders)
        + "\n\n"
        + what_to_write_instead()
    )


def test_the_message_has_a_route_for_every_token_the_check_refuses():
    """The message is a deliverable, and a refusal with no route is a wall.

    `timers_in` reads any `\\d+.\\d+.\\d+`, which is wider than "a release of
    this plugin" — and deliberately so, because narrowing the regex to
    exclude a shape is how round 1's finding 1 happened. So the message
    carries the routes instead, and every kind of token it can refuse needs
    one it can actually take.

    Three of the four shapes had a route already. A DATE written with dots
    did not: it is not a release of anything, so no exemption fits it and
    none should be added — this repository writes dates with dashes, which
    the check does not read at all.

    **What this case pins of the printed text is the routes and their
    attachment**, and nothing else. The last assertion reads `refusal`, which
    is what the check actually prints, so an edit detaching the routes from it
    goes red — that mutation used to leave every case here green (review round
    2, finding 7). The routes are one of the six leaves `ast.parse` gives for
    the expression `refusal` returns; the other five are read whole by
    `test_the_refusal_prints_every_piece_it_builds` below, which is where that
    count is taken.

    This paragraph used to say, as a measured fact, that what was still
    unpinned was ONLY `assert not offenders, refusal(running, offenders)`.
    Three mutations disprove it: deleting the offender join, deleting the
    `{running}` interpolation and deleting the timer paragraph each left this
    module at 30 passed (#203). The sentence this one replaced made the same
    mistake a round earlier — it used its own residual as grounds for leaving
    the whole message inline — which is how the real gap stayed open twice.
    **A residual is the survivor of the mutations that were actually run,
    never a limit**: what is absent from a measured list is unmeasured.
    """
    routes = what_to_write_instead()
    assert ILLUSTRATIVE_VERSION in routes, "no route for this repository's own version"
    assert "VERSIONS_OF_ANOTHER_PRODUCT" in routes, (
        "no route for a version belonging to another product — the shape "
        f"`3.13.9` has, and the one {sorted(VERSIONS_OF_ANOTHER_PRODUCT)} is"
    )
    assert "RECORDS_OF_A_MOMENT" in routes, "no route for a record of a moment"
    assert "BELOW" in routes, "the message does not say history is already allowed"
    assert "TAGGED" in routes, (
        "the message does not say a tagged version is history too (#363), so "
        "an author refused on the version that just shipped is sent to an "
        "exemption none of which is a truthful home for it"
    )
    # The date. Refused as `(2026, 9, 3)`, and no exemption fits it.
    assert "date" in routes, (
        "the message offers no route for a token that is not a release at "
        "all — `2026.09.03` reads as a version and none of the exemptions "
        "above is a truthful home for it"
    )
    assert routes in refusal("0.8.3", ["docs/x.md:1 names 0.9.0"]), (
        "the refusal no longer carries the routes — the text a person sees "
        "and the text this case reads have come apart"
    )


def test_the_refusal_prints_every_piece_it_builds():
    """Six elements, taken from `refusal`'s syntax tree, each read whole.

    A case that stops one short is the shape this repository produced nine
    times on one branch (#51, observation 6), and the three attempts that
    closed this gap on the original branch each missed a different separator
    (#203). A fourth attempt said it had enumerated by construction and had
    not: it counted "four pieces and three separators", which is a reading of
    the source rather than the source, and review round 1 measured 86
    characters of the timer paragraph that no assertion here touched.

    So the elements are the leaves `ast.parse` gives for the returned
    expression, under three normalisations stated here because the count
    depends on them: the `+` chain flattens, a `JoinedStr` expands to its
    parts, and a `Call` counts as ONE atom — its receiver and its arguments
    inside it. The chain flattens to four operands, and the first is one
    f-string — a single `JoinedStr` of three parts. Six leaves:

    1. `"a loaded file names a version at or above the running "`;
    2. the `{running}` interpolation;
    3. one constant running from the `.` after the version through
       `run.\\n  ` — the whole timer paragraph AND the separator that closes
       it, which is one element rather than two;
    4. `"\\n  ".join(offenders)`;
    5. `"\\n\\n"`;
    6. `what_to_write_instead()`, read here and by the case above.

    Element 3 is where reading failed twice over. It split that constant into
    a paragraph and a trailing separator, and it promoted the `"\\n  "` the
    join is called ON — the receiver, not an argument — to an element of its
    own. Under the rule above it is inside element 4 rather than beside it;
    a bare `ast.walk` of the expression does return it, which is why the rule
    is stated before the count and not after. That is how the count reached
    seven while the paragraph itself was read only at its two ends. Every
    element below is read WHOLE, so nothing between two spot-checks can go
    missing again.

    **Two mutations survive this set, and neither is a limit.** Handing the
    check's own `assert not offenders, refusal(running, offenders)` a literal
    leaves this module green, and so does emitting the routes before the
    refused lines.

    The first is pinnable, and nothing about pinning it needs this file's own
    source read — that sentence was written here and disproved in review round
    1 by writing the pin. `tracked` and `timers_in` are module globals, and
    swapping them the way
    `test_the_exemption_list_does_not_depend_on_the_order_it_is_written_in`
    already does one constant over raises the check, whose message compares
    equal to `refusal(running, offenders)`. It stays on this list until
    somebody plants that case. The second is pinnable only by rebuilding
    `refusal` inside the test, which is the assertion this case was designed
    not to be.

    A third class is unmeasured by design: nothing here pins that nothing was
    ADDED. A sentence inserted at the end of the timer paragraph, or a line
    inserted before the routes, leaves this module at 32 passed (round 2).
    Every element is read whole, so nothing can go missing. The pin is
    available and it is measured, not absent: the six pieces asserted below
    tile the text exactly, so `assert text ==` their concatenation costs one
    assertion and no literal this case does not already carry — 32 passed
    unmutated, and 1 failed on either insertion (round 3). It is declined
    because that concatenation IS `refusal` rebuilt in the test, which
    `plan.md` weighed and rejected. Declined on a measurement, not on a
    limit.

    What must not be written here again is that either one CANNOT be pinned.
    Three times now a limit nobody measured has gone into a record about this
    function and then stood as the grounds for looking no further.
    """
    running = RUNNING_IN_THE_FIXTURES
    first = "docs/a.md:1 names 0.9.0"
    second = "docs/b.md:2 names V0.9.0"
    text = refusal(running, [first, second])

    opening = f"a loaded file names a version at or above the running {running}."
    assert text.startswith(opening), (
        "the refusal no longer opens by naming what happened and the version "
        "it is measured against, so an author cannot tell which number made "
        f"these lines offenders. It opens {text[: len(opening)]!r}"
    )
    # Element 3, whole, in two contiguous halves — the first ends on the
    # comma the second opens after, so no character between them goes unread.
    # It used to be read at its two ends only: deleting the literal `it goes
    # red on the day that version ships, on the release's own `, or just
    # `preparation commit, `, each left this module at 32 passed (round 1).
    assert (
        ". Such a line is right for exactly one release and a timer before "
        "it: it goes red on the day that version ships," in text
    ), (
        "the reason went: the text says a line is refused and not why, which "
        "is the half that stops the next author writing another one"
    )
    assert (
        " on the release's own preparation commit, after the broad gate has "
        "already run." in text
    ), (
        "the timer's cost went — it fires on the release's own preparation "
        "commit, hours in, and that is what makes this worth a check rather "
        "than a convention"
    )
    assert first in text and second in text, (
        "the refused lines are gone: a person is told that a loaded file "
        "names a version and not which file, which line, or which token"
    )
    # The `"\n  "` that CLOSES element 3, read where it attaches; the two
    # halves above are the rest of that same element.
    assert f"\n  {first}" in text, (
        "the first refused line is glued to the sentence above it — the "
        "separator that opens the indented block went, and with it the only "
        "thing that makes the block a block"
    )
    # Element 4 whole — the join's output, whose own separator cannot be
    # observed with one offender, which is why the fixture passes two.
    assert f"{first}\n  {second}" in text, (
        "the refused lines run together on one line: the join's separator "
        "went, and a tree with one offender in it would never show that"
    )
    # Elements 5 and 6, whole.
    assert f"\n\n{what_to_write_instead()}" in text, (
        "the routes no longer stand off the refused lines as their own "
        "paragraph — either the blank line between them went, or the routes "
        "did"
    )


def test_the_illustrative_version_is_not_one_this_repository_could_ship():
    """The exemption above asserts its own precondition, or it hides the
    defect it was added beside.

    `ILLUSTRATIVE_VERSION` is exempt in every loaded file. On the day this
    repository ships that number, the exemption would wave through exactly the
    line the check exists to catch — and it would do so silently, because a
    bare string in an allow-list has no way to notice that it stopped being
    illustrative. So the value has to be one this repository has neither
    shipped nor is shipping, and this is where that stops being an assumption.
    """
    running = version()
    assert running != ILLUSTRATIVE_VERSION, (
        f"the illustrative version {ILLUSTRATIVE_VERSION} is now the running "
        "version, so the exemption in `timers_in` hides the defect it was "
        "written beside. Choose a value this repository will not reach and "
        'rewrite the paragraph at `docs/issues-and-milestones.md` §"A '
        'rolling log is titled after the version it rolled from" with it'
    )
    shipped = shipped_versions()
    assert shipped, "CHANGELOG.md records no releases — this case is blind"
    assert ILLUSTRATIVE_VERSION not in shipped, (
        f"the illustrative version {ILLUSTRATIVE_VERSION} has shipped "
        f"({sorted(shipped)}), so a loaded file naming it names a real "
        "release. Choose a value this repository has not reached"
    )


def timer_offenders(root=ROOT, running=None):
    """`rel:line names <token>` for every timer in the loaded files under
    `root`. `running` defaults to the version `root` itself declares.

    Round 1 ⬜ 7: it read `ROOT`'s `plugin.json` whatever `root` said, so a
    fixture repository was swept against this repository's running version —
    a helper taking a root and then not using it for half its inputs.
    """
    running = running or version(root)
    shipped = shipped_tags(root)
    offenders = []
    files, _ = tracked(*LOADED, root=root)
    for rel in files:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
            text = f.read()
        for number, token in timers_in(rel, text, running, shipped):
            offenders.append(f"{rel}:{number} names {token}")
    return offenders


def test_no_loaded_file_names_a_version_at_or_above_the_running_one():
    """A version number written into prose is right for exactly one release.

    The check this replaced read one number — the version in `plugin.json` —
    so a document naming a version that has NOT shipped yet was green every
    day until the day it shipped, and red on that release's own preparation
    commit, hours in, after the broad gate had already run. `0.9.0` sat in
    `docs/issues-and-milestones.md` for three releases that way (#179).

    So the comparison is read rather than the equality: **at or above the
    running version is a timer and is refused; below it is history and is
    kept.**

    Three exemptions, each argued where it is declared rather than here:

    - `RECORDS_OF_A_MOMENT` — files whose whole job is to name a moment.
      `seal/specs/` and `CHANGELOG.md` are outside the scanned set entirely.
      `docs/one-root-by-lifetime.md` is the 0.4.0 design and says so in every
      other paragraph, and `docs/experiments/` holds dated measurements whose
      numbers are the reading.
    - `ILLUSTRATIVE_VERSION` — the value the repository already tells authors
      to write, with its own case above asserting it is not a real one.
    - `VERSIONS_OF_ANOTHER_PRODUCT` — a number that belongs to somebody
      else's release train, pinned to the file that names it.
    """
    # One read of `plugin.json`, not two: `timer_offenders` needs the running
    # version and so does the refusal (round 1 ⬜ 7).
    running = version()
    offenders = timer_offenders(running=running)
    assert not offenders, refusal(running, offenders)


# The fixtures below run `timers_in` against text this repository does not
# have to contain, so the rule is pinned at its boundary rather than only at
# whatever the tree happens to hold today. `0.8.3` is a stand-in for "the
# running version" in each of them and is not read from `plugin.json`: a
# fixture that moves with the release proves nothing about the release after.
RUNNING_IN_THE_FIXTURES = "0.8.3"


def test_a_version_below_the_running_one_is_history_and_is_kept():
    """The case that decides against refusing every version ever shipped.

    `docs/issues-and-milestones.md` explains how to tell which release an
    issue shipped in by saying that *the branch `release/v0.3.0` shipped as
    0.2.0*. Both numbers are real, both are below the running version, and a
    rule that refuses them is refusing the repository's own history — which
    is #179's second candidate and why it was not taken.
    """
    history = "the branch `release/v0.3.0` shipped as 0.2.0"
    assert (
        timers_in("docs/issues-and-milestones.md", history, RUNNING_IN_THE_FIXTURES)
        == []
    )


def test_a_tagged_version_is_history_and_is_kept():
    """#363. The preparation commit bumps `plugin.json`, so from that commit
    until the next bump the running version is one that has ALREADY shipped
    — tagged, merged to `main`, recorded in the changelog — and the documents
    that ship with it could not name it. `timers_in`'s own docstring argues
    the ceiling from *below `running` is history*; a shipped version is
    history by that argument, and this is the sibling of the case above that
    pins it one number higher. The case above is not edited: below the
    running version stays history whether or not it is tagged.

    `shipped` is passed explicitly. What it is derived from is the case
    below's question, and the trap is there too."""
    text = "shipped as 0.8.3\nlands in 0.9.0\n"
    assert timers_in("docs/x.md", text, RUNNING_IN_THE_FIXTURES, shipped={"0.8.3"}) == [
        (2, "0.9.0")
    ], "a tagged running version is refused as a timer"
    assert timers_in("docs/x.md", text, RUNNING_IN_THE_FIXTURES, shipped=set()) == [
        (1, "0.8.3"),
        (2, "0.9.0"),
    ], "with nothing shipped the running version stopped being refused"


def test_the_shipped_set_is_the_tags_of_the_root_being_swept(tmp_path):
    """The trap #363 names: `CHANGELOG.md` gets its heading in the SAME
    commit that bumps `plugin.json`, so *shipped* derived from the changelog
    would wave through the very version being cut. A tag exists only after
    the release reaches `main`, so tags are the source and nothing else.

    The fixture tags its running version and names three: one below it, the
    running one, one above. Read against tags, only the one above is a
    timer; read against nothing, the running one is refused too, which is
    the reading this case exists to end."""
    root = build_tracked_tree(
        tmp_path / "r",
        {
            ".claude-plugin/plugin.json": json.dumps({"version": "0.2.0"}),
            "docs/live.md": "shipped in 0.1.0, then 0.2.0, and 0.3.0 is next\n",
        },
    )
    subprocess.run(["git", "-C", str(root), "tag", "v0.2.0"], check=True)
    subprocess.run(["git", "-C", str(root), "tag", "v-not-a-version"], check=True)
    assert shipped_tags(root) == {"0.2.0"}, (
        "the shipped set is not the bare versions of the root's `v*` tags"
    )
    assert timer_offenders(root) == ["docs/live.md:1 names 0.3.0"]


def test_this_checkout_has_tags_to_read_the_shipped_set_from():
    """A checkout without tags — shallow, or fetched without them — would
    read an empty shipped set and refuse the running version again, silently
    and exactly as before #363. That is a wrong deny that reads as the old
    rule working, so it is loud instead: this repository has shipped, and a
    checkout that cannot see a single `v*` tag is not one this sweep can
    judge. `test.yml` and `hygiene.yml` check out with `fetch-depth: 0`."""
    assert shipped_tags(ROOT), (
        "no `v*` tag is readable from this checkout, so the timer sweep "
        "cannot tell a shipped version from one being cut. CI checks out with "
        "`fetch-depth: 0`; a local clone needs `git fetch --tags`"
    )


def test_a_version_at_or_above_the_running_one_is_refused():
    """At the boundary, with the `v` prefix, and by line.

    `0.8.3` is refused because it is the running version — the behaviour the
    substring check this replaced already had. `0.9.0` is refused because it
    is above it, which is the whole of what #179 added, and `v0.9.0` is
    refused because the substring check caught the prefixed spelling for free
    and a regex must not quietly drop it.
    """
    text = "line one\nships as 0.9.0 next\ncut v0.9.0 today\nthe running 0.8.3\n"
    assert timers_in("docs/whatever.md", text, RUNNING_IN_THE_FIXTURES) == [
        (2, "0.9.0"),
        (3, "v0.9.0"),
        (4, "0.8.3"),
    ]


def test_a_two_digit_component_compares_as_a_number():
    """`0.10.0` is above `0.8.3`, and every string comparison says otherwise.

    This is the version #179's own body names as the one the next author
    writes, and it is the first release where the two orderings disagree. A
    check that compared the tokens as text would allow it — silently, and
    only until the day 0.10.0 shipped, which is the whole failure again.
    """
    assert timers_in("docs/x.md", "lands in 0.10.0", RUNNING_IN_THE_FIXTURES) == [
        (1, "0.10.0")
    ]
    assert timers_in("docs/x.md", "shipped in 0.10.0", "0.11.0") == []


def test_the_illustrative_version_is_allowed_in_any_loaded_file():
    """`1.2.3` is above the running version and is not a timer.

    It is exempt everywhere rather than at one coordinate, because the reason
    it exists is that the NEXT author writes it — in a file this exemption
    cannot know the name of.
    """
    text = f"titled `chore: flow measurement — after {ILLUSTRATIVE_VERSION}`"
    assert (
        timers_in("docs/issues-and-milestones.md", text, RUNNING_IN_THE_FIXTURES) == []
    )
    assert timers_in("agents/warden.md", text, RUNNING_IN_THE_FIXTURES) == []


def test_a_record_of_a_moment_keeps_every_version_it_names():
    """Both shapes of entry: an exact path, and `docs/experiments/` as a
    prefix covering every dated record written under it, now and later."""
    text = "measured on 2.1.259, which is above anything this plugin ships"
    assert (
        timers_in("docs/one-root-by-lifetime.md", text, RUNNING_IN_THE_FIXTURES) == []
    )
    assert (
        timers_in(
            "docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md",
            text,
            RUNNING_IN_THE_FIXTURES,
        )
        == []
    )
    # The prefix covers a file that does not exist yet, which is the point of
    # spelling it as a directory rather than listing today's two records.
    assert (
        timers_in(
            "docs/experiments/2099-01-01-not-written-yet.md",
            text,
            RUNNING_IN_THE_FIXTURES,
        )
        == []
    )
    # And it is a prefix of the path, not a substring of it: a document that
    # merely talks ABOUT the experiments directory is still scanned.
    assert timers_in(
        "docs/about-docs-experiments-2.1.259.md", text, RUNNING_IN_THE_FIXTURES
    ) == [(1, "2.1.259")]


def test_the_exemption_list_does_not_depend_on_the_order_it_is_written_in():
    """`RECORDS_OF_A_MOMENT` is the list a later author appends to, and
    appending at the end is the natural act.

    An early `return` on the first `/` entry whose prefix matched made every
    entry after it unreachable — so an exact path written below the prefix
    that contains it silently stopped working (review round 2). The failure
    direction is loud, a file the author meant to exempt goes red, but nothing
    said the order mattered.

    **An exact path is the only entry whose answer the order could change**,
    and this used to say a narrower prefix was the same mechanism (#205). It
    never was, in either implementation: every `/` entry takes the same
    `DATED_RECORD.match(basename)` check whether it is wide or narrow, so a
    narrower one is order-independent by construction. Only `rel == entry`
    skips that check. No assertion is added for it — pinning an arrangement
    that changes no answer is the failure this correction is about.
    """
    entries = RECORDS_OF_A_MOMENT
    try:
        globals()["RECORDS_OF_A_MOMENT"] = (
            "docs/experiments/",
            "docs/experiments/README.md",
        )
        assert is_a_record_of_a_moment("docs/experiments/README.md"), (
            "an exact entry written after the prefix that contains it is "
            "unreachable — the list has become order-dependent"
        )
    finally:
        globals()["RECORDS_OF_A_MOMENT"] = entries


def test_the_experiments_prefix_covers_only_a_dated_record():
    """The prefix's argument is the file name's date, so the entry is too.

    `docs/experiments/README.md` is the directory's conventions, edited
    whenever they change — the same standing-document shape #179 refused a
    prefix for in `docs/issues-and-milestones.md`. Left uncovered by this
    case, the prefix is the one exemption a document joins by choosing its
    own path.
    """
    text = "ships in 0.9.0"
    assert (
        timers_in(
            "docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md",
            text,
            RUNNING_IN_THE_FIXTURES,
        )
        == []
    )
    assert timers_in("docs/experiments/README.md", text, RUNNING_IN_THE_FIXTURES) == [
        (1, "0.9.0")
    ]
    # The date has to be in the FILE's own name, never merely somewhere in
    # the path. A dated DIRECTORY holding undated files is the same door one
    # level down — the file joins the exemption by where it sits, which is
    # the half of finding 2 that survived the first fix for it.
    assert timers_in(
        "docs/experiments/2026-09-03-run/README.md", text, RUNNING_IN_THE_FIXTURES
    ) == [(1, "0.9.0")]
    # And the name has to BEGIN with the date, which the README prescribes as
    # `<date>-<what-was-asked>.md`. A date appended to a standing document's
    # name is the cheapest way back through the same door.
    #
    # Two things anchor that independently — the pattern's `^` and `.match()`
    # — so a mutation dropping either ALONE changes nothing and this
    # assertion cannot see it. Dropping both together is what it catches, and
    # that is the mutation worth running against this line.
    assert timers_in(
        "docs/experiments/README-2026-09-03-conventions.md",
        text,
        RUNNING_IN_THE_FIXTURES,
    ) == [(1, "0.9.0")]
    # The shape is the README's own, `<date>-<what-was-asked>.md`. A bare
    # date is not that name, and neither is a loose one (review round 2).
    # Without these two, dropping the trailing `-` or loosening the component
    # widths left every case in this module green — and the first of those
    # silently widens the exemption.
    assert timers_in(
        "docs/experiments/2026-09-03.md", text, RUNNING_IN_THE_FIXTURES
    ) == [(1, "0.9.0")]
    assert timers_in(
        "docs/experiments/26-9-3-run.md", text, RUNNING_IN_THE_FIXTURES
    ) == [(1, "0.9.0")]


def test_the_declared_token_is_the_one_the_refusal_printed():
    """The route has to work on the token the message hands the author.

    The offender line prints `v4.4.17`, and an author who declares that
    spelling used to get no change at all — the lookup read the bare token
    and nothing said so (review round 2).
    """
    rel, text = "docs/x.md", "bash's glob changed in v9.9.9"
    assert timers_in(rel, text, RUNNING_IN_THE_FIXTURES) == [(1, "v9.9.9")]
    VERSIONS_OF_ANOTHER_PRODUCT[(rel, "v9.9.9")] = "bash's, as the refusal spells it"
    try:
        assert timers_in(rel, text, RUNNING_IN_THE_FIXTURES) == []
    finally:
        del VERSIONS_OF_ANOTHER_PRODUCT[(rel, "v9.9.9")]
    # And the BARE spelling keeps working, which is what the live entry uses.
    # Neither arm is pinned by that entry: `seal.py` writes `4.4.17` with no
    # `v`, so the printed and the bare token are the same string there and
    # dropping either arm leaves the tree green — measured.
    VERSIONS_OF_ANOTHER_PRODUCT[(rel, "9.9.9")] = "bash's, declared bare"
    try:
        assert timers_in(rel, text, RUNNING_IN_THE_FIXTURES) == []
    finally:
        del VERSIONS_OF_ANOTHER_PRODUCT[(rel, "9.9.9")]


def test_another_products_version_is_allowed_only_in_the_file_that_declares_it():
    """The exemption is a fact about one comment, so it is pinned to it.

    Unpinned, `4.4.17` would be waved through in any loaded file — including
    one where it really was this plugin's number, written by somebody who had
    no idea the token was spoken for.
    """
    text = "bash 4.4.17 changed how the glob answers"
    assert (
        timers_in("skills/implement/scripts/seal.py", text, RUNNING_IN_THE_FIXTURES)
        == []
    )
    assert timers_in("docs/somewhere-else.md", text, RUNNING_IN_THE_FIXTURES) == [
        (1, "4.4.17")
    ]


def test_a_number_that_is_not_a_version_is_not_read_as_one():
    """The lookaround, which is what a substring test did not need.

    A four-part number is not a release of this plugin, and a number that
    continues past the third component is a different one. Reading either as
    a version would refuse a line nobody can rewrite into an illustrative
    value, because it never named a version to begin with.
    """
    # Deliberately NOT `1.2.3.4`. Its first three components are the
    # illustrative version, so the exemption answers `[]` for it whether the
    # lookaround is here or not, and the assertion would pin nothing — which
    # is what the mutation run that dropped the lookaround showed.
    assert (
        timers_in("docs/x.md", "build 2.0.1.5 of something", RUNNING_IN_THE_FIXTURES)
        == []
    )
    assert timers_in(
        "docs/x.md", "the token v1.2.30 is its own", RUNNING_IN_THE_FIXTURES
    ) == [(1, "v1.2.30")]
    # The LEADING lookbehind, which the line above cannot see either.
    # `2.0.1.5`'s tail `0.1.5` is below the running version, so that line
    # answers `[]` whether the lookbehind is there or not — measured. Only a
    # four-part number whose tail is ABOVE it shows the loss, and a version
    # glued to a preceding word is the other half of the same guard.
    assert (
        timers_in("docs/x.md", "build 1.9.9.9 of something", RUNNING_IN_THE_FIXTURES)
        == []
    )
    assert (
        timers_in("docs/x.md", "the token x0.9.0 is not ours", RUNNING_IN_THE_FIXTURES)
        == []
    )
    # A prerelease of a version that has not shipped is a timer in both its
    # spellings. `0.9.0-rc1` was always refused; `0.9.0rc1` used to be
    # invisible, because a `(?!\w)` added for `v1.2.30` — which `\d+`'s greed
    # already covers — hid it (review round 2).
    assert timers_in(
        "docs/x.md", "tagged 0.9.0rc1 last week", RUNNING_IN_THE_FIXTURES
    ) == [(1, "0.9.0")]
    assert timers_in(
        "docs/x.md", "tagged 0.9.0-rc1 last week", RUNNING_IN_THE_FIXTURES
    ) == [(1, "0.9.0")]
    assert (
        timers_in("docs/x.md", "the python floor is 3.12", RUNNING_IN_THE_FIXTURES)
        == []
    )


def test_an_uppercase_v_is_a_prefix_and_not_a_preceding_word():
    """`V0.9.0` is this plugin's own version, and the check could not see it.

    The argument for the leading lookbehind is written beside the constant: a
    preceding word makes the token a different identifier, so `py3.13.9` names
    CPython and no release of this plugin makes it wrong. An uppercase `V` is
    not a preceding word — it is the version prefix in another spelling — so
    that argument never reached it, and the token was invisible in every loaded
    file (#204).

    The fix is `[vV]?` and NOT a narrowed lookbehind: round 1's finding was a
    lookaround narrowed for one shape taking another with it. The two shapes
    the widening must not disturb are asserted here beside it, because they are
    what a narrowing would have taken.
    """
    assert timers_in(
        "docs/x.md", "the token V0.9.0 is ours", RUNNING_IN_THE_FIXTURES
    ) == [(1, "V0.9.0")], (
        "an uppercase prefix hides this plugin's own version, and the refusal "
        "has to print the spelling the author wrote or the declaration route "
        "cannot be taken on it"
    )
    # The `\w` half, which the widening must not open one character to the
    # left: a word before the number renames it.
    assert (
        timers_in("docs/x.md", "built on py3.13.9 today", RUNNING_IN_THE_FIXTURES) == []
    ), "a composite identifier is read as this plugin's version"
    assert (
        timers_in(
            "docs/x.md", "the token PyV0.9.0 is not ours", RUNNING_IN_THE_FIXTURES
        )
        == []
    ), (
        "a word before the `V` no longer refuses the token — the widening "
        "reached the lookbehind, which is what it must not do"
    )


def test_a_version_that_ends_a_sentence_is_still_a_version():
    """The shape the check this replaced caught and a lookaround can lose.

    `version() in f.read()` was punctuation-blind, so `right for 0.8.3.` was
    an offender. A single `(?![\\w.])` refuses any following dot, which reads
    a sentence-final version as no version at all — and that one never fires
    later either, because the period is still there on the day the number
    becomes the running one.
    """
    assert timers_in(
        "docs/x.md", "Everything here is right for 0.8.3.", RUNNING_IN_THE_FIXTURES
    ) == [(1, "0.8.3")]
    assert timers_in(
        "docs/x.md", "- #179 goes into 0.9.0.", RUNNING_IN_THE_FIXTURES
    ) == [(1, "0.9.0")]
    assert timers_in("docs/x.md", "ships in 0.9.0...", RUNNING_IN_THE_FIXTURES) == [
        (1, "0.9.0")
    ]


def python_floor():
    """The supported floor, as ruff.toml states it: `py312` -> `3.12`."""
    with open(os.path.join(ROOT, "ruff.toml"), encoding="utf-8") as f:
        m = re.search(r'target-version = "py(\d)(\d+)"', f.read())
    assert m, "ruff.toml lost its target-version"
    return f"{m.group(1)}.{m.group(2)}"


def test_the_python_floor_is_the_same_number_everywhere():
    """Three places state it — the linter, the READMEs, the CI matrix — and a
    floor that disagrees with itself is worse than none: whoever reads the
    wrong one ships against an interpreter nobody tests."""
    floor = python_floor()
    for name in ("README.md", "README.ko.md"):
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            assert floor in f.read(), f"{name} does not state the {floor} floor"
    with open(
        os.path.join(ROOT, ".github", "workflows", "test.yml"), encoding="utf-8"
    ) as f:
        versions = re.findall(r'python: "(\d+\.\d+)"', f.read())
    assert versions, "the test matrix names no python versions"
    lowest = min(versions, key=lambda v: tuple(int(n) for n in v.split(".")))
    assert lowest == floor, (
        f"ruff.toml says {floor} and the lowest tested version is {lowest} — "
        "the floor is only real if CI stands on it"
    )


def test_update_tells_the_user_when_the_preset_block_changed():
    """`claude plugin update` installs the plugin, never the CLAUDE.md block.

    The block arrives only through `install.sh` or `/specseal:preset-setup`,
    both run by hand -- so a release can change a rule while every installed
    machine keeps stating the old one. The update command has to look and say
    so, or the change reaches no session that was already running."""
    with open(
        os.path.join(ROOT, "skills", "update", "SKILL.md"), encoding="utf-8"
    ) as f:
        update = f.read()
    assert "specseal:start" in update, (
        "the update command stopped comparing the preset block"
    )
    assert "/specseal:preset-setup" in update, (
        "the update command names no way to take a changed block"
    )
    assert "does not delete anything the user wrote" in update.lower(), (
        "taking a release started resolving overlaps with the user's own text"
    )


def test_update_reads_the_installed_copy_before_it_summarises():
    """#157. `claude plugin update` keys the install path by the version
    string and skips extraction when that directory already exists, so on a
    machine that had a directory by that name from an earlier numbering the
    installer reported success and the copy that would have loaded was eight
    releases old. The skill then summarised the marketplace CLONE's changelog
    — the right file in the wrong place — and the more thorough the summary,
    the more convincing the wrong answer.

    So a step between installing and summarising reads the INSTALLED copy:
    `installed_plugins.json` names the one `installPath`, and its
    `CHANGELOG.md`'s first heading has to be the version the installer just
    reported. A mismatch stops the procedure before the summary and prints
    the repair, with the two cautions the ticket measured: `.in_use/` holds a
    live session's PID files, and the one `installPath` is the directory
    that must not be deleted."""
    update = read_text("skills", "update", "SKILL.md")
    assert "**2b." in update, "no step reads the installed copy between 2 and 3"
    step = update[update.index("**2b.") : update.index("**3.")]
    flat = " ".join(step.split())
    for needed, why in (
        ("installed_plugins.json", "the file that names the installed copy"),
        ("installPath", "the field that names it"),
        ("CHANGELOG.md", "the file whose top heading says which version landed"),
        ("mismatch", "the word that makes the outcome a stop rather than a note"),
        (".in_use", "the directory the caution is about"),
        # The word, not the path: `.in_use` is also in the repair's `mkdir`,
        # so a step that lost the caution and kept the repair still said it.
        ("PID", "the caution about a live session's PID files"),
        ("rsync", "the repair"),
        ("stop", "the instruction not to reach the summary"),
    ):
        assert needed in flat, f"step 2b does not carry {needed!r}: {why}"
    assert "/Users/" not in flat, "a user path in a shipped skill"


def test_no_section_accumulates_entries_in_the_shared_file():
    """`## Unreleased` was the region every branch appended to.

    This case used to check that it sat ABOVE every dated section, after a
    rebase conflict resolved the wrong way sank it below one. That ordering
    stopped being the problem when the section stopped existing: entries
    accumulate as `seal/specs/<work-item-id>/changelog.md` fragments now, and
    the
    release gathers them into a dated section at the top. A heading by that
    name means somebody went back to the shared file, which is issue #46.

    The order still matters and is still checked — by
    `test_the_changelog_is_gathered_at_release.py`, against the gather script
    that produces it, which is the only thing that writes a section now.
    """
    with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
        headings = re.findall(r"^## (.+)$", f.read(), re.M)
    found = [h for h in headings if h.lower().startswith("unreleased")]
    assert not found, (
        f"CHANGELOG.md carries {found} again. An entry goes in "
        "seal/specs/<work-item-id>/changelog.md; `gather_changelog.py --version "
        "X.Y.Z` is what writes a section here"
    )


def duplicated_version_headings(text):
    """`[(version, [line numbers])]` for every version `## ` heads twice.

    #289: `gather_changelog.py` used to write a second `## X.Y.Z` when run
    twice for one version, and one release shipped with its entries split
    across two headings that read as two releases with the same number. The
    gather appends now; this is the half that keeps it closed, because the
    append is a one-line change a later edit can undo silently.
    """
    lines = {}
    for number, line in enumerate(text.splitlines(), 1):
        found = re.match(r"^## (\d+\.\d+\.\d+)\b", line)
        if found:
            lines.setdefault(found.group(1), []).append(number)
    return [(version, at) for version, at in lines.items() if len(at) > 1]


def test_a_version_heading_appears_once_in_a_changelog():
    """The reader, against a file that has the defect and one that does not,
    so the real-tree case below cannot pass by reading nothing."""
    split = (
        "# Changelog\n\n## 0.2.0 — d\n\n- a\n\n## 0.2.0 — d\n\n- b\n\n## 0.1.0 — c\n"
    )
    assert duplicated_version_headings(split) == [("0.2.0", [3, 7])]
    assert duplicated_version_headings("# Changelog\n\n## 0.2.0 — d\n\n- a\n") == []


def test_no_version_heads_two_sections_of_this_changelog():
    """This repository's own file. A second heading for one version is a
    second gather that did not append — the defect #289 measured at one
    release and removed by hand at the next."""
    found = duplicated_version_headings(read_text("CHANGELOG.md"))
    assert not found, "\n".join(
        f"CHANGELOG.md heads {version} twice, at lines {at}. One release, "
        "one section: merge the later heading's entries into the first and "
        "delete it"
        for version, at in found
    )


def test_no_version_heads_two_sections_of_this_ledger():
    """The gathered ledger, the same way. #540: `fold_ledger.py` wrote a
    second `## 0.9.3` heading when a fragment landed the day after the
    release-preparation commit (`4ac9bf35`), and the file carried both
    through seventeen ledger sections (`0.9.4` to `0.15.0`, counted after
    the second heading; eighteen tags after `v0.9.3`) while the ticket said
    nobody had run the fold twice. Seen red against that tree: `0.9.3
    twice, at lines [1673, 1764]`."""
    found = duplicated_version_headings(read_text("seal", "ledger.md"))
    assert not found, "\n".join(
        f"seal/ledger.md heads {version} twice, at lines {at}. One release, "
        "one section: move the later heading's work items under the first "
        "and delete it"
        for version, at in found
    )


def test_the_newest_changelog_entry_is_the_version_being_shipped():
    """`test_plugin_version_is_in_changelog` accepts the version appearing
    anywhere, and an older entry satisfies that forever. What has to hold is
    that the newest dated entry IS the shipping version: a bump with no entry
    and an entry with no bump are the two ways a release goes out unexplained.

    An `## Unreleased` heading is skipped. On `next` the entries collect there
    while `plugin.json` stays at the last release, which is the whole point of
    accumulating."""
    with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
        headings = re.findall(r"^## (.+)$", f.read(), re.M)
    dated = [h for h in headings if not h.lower().startswith("unreleased")]
    assert dated, "CHANGELOG has no released entry"
    newest = dated[0].split()[0]
    assert newest == version(), (
        f"CHANGELOG's newest entry is {newest}, plugin.json ships {version()}"
    )


def test_the_release_target_is_asked_before_the_work_starts():
    """The base branch decides whether a PR is a release, so it is a question
    with an answer available in the first minute.

    Left to the end it arrives after the branch exists and the changelog entry
    is already written under the wrong heading -- the same late-question
    failure the commit gate was moved forward to avoid."""
    # The branch question is part of the routing section, which is the
    # orchestrator's half of `implement` since #292; the yes/no tell it
    # answers to stays in the implementer's half. The skill is read as both.
    for parts, text in (
        (
            ("skills", "implement", "orchestration.md"),
            read_text("skills", "implement", "SKILL.md")
            + read_text("skills", "implement", "orchestration.md"),
        ),
        (("agents", "smith.md"), read_text("agents", "smith.md")),
    ):
        # Collapsed, because both files wrap these sentences at different
        # columns and a literal match would be asserting the line breaks.
        text = " ".join(text.split())
        assert "a PR into `main` is a release" in text, (
            f"{parts[-1]} stopped saying which base branch means a release"
        )
        assert "release branch is not" in text, (
            f"{parts[-1]} stopped saying which base branch does NOT release"
        )
        assert "accumulates" in text, (
            f"{parts[-1]} lost the accumulate half of the question"
        )
        # Round 1, 🔴 7. This used to require the literal `## Unreleased`, and
        # that is a heading THIS repository no longer has: entries accumulate
        # as `seal/specs/<work-item-id>/changelog.md` fragments. A `smith`
        # reading
        # its own contract therefore either created the heading — reddening
        # `test_no_section_accumulates_entries_in_the_shared_file` — or
        # appended under the newest released section, which is the collision
        # the fragments exist to remove. The two cases pulled against each
        # other and the contract was the one that was wrong.
        assert "## Unreleased" not in text, (
            f"{parts[-1]} prescribes a changelog heading again. Where an "
            "entry accumulates is the repository's convention, and a shipped "
            "contract that names one sends a session to write it"
        )
        assert "yes/no" in text, (
            f"{parts[-1]} stopped saying the question has two continuing "
            "answers, which is what keeps a `no` from stranding the work"
        )


def _closer():
    """The release-closing script, imported so its regexes can be read.

    Round 2: every string the first version of this case pinned also lives in
    the module docstring, so the whole script could be replaced by a seven-line
    stub carrying those words and all twelve tests passed. A string search
    cannot see what a regex matches."""
    import importlib.util

    path = os.path.join(ROOT, ".github", "scripts", "close_issues_on_release.py")
    spec = importlib.util.spec_from_file_location("close_issues_on_release", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_the_token_stays_the_smallest_that_can_close_an_issue():
    """Read the permissions block as a mapping, not as text.

    A substring search for `contents: write` passes `contents:  write` — two
    spaces, one value to YAML — and that is the exact widening the block's own
    comment says it guards. Measured green before this."""
    workflow = read_text(".github", "workflows", "close-issues-on-release.yml")
    block = re.search(r"^permissions:\n((?:  [\w-]+:.*\n)+)", workflow, re.M)
    assert block, "the workflow states no permissions block, so it inherits all"
    granted = dict(re.findall(r"^  ([\w-]+):\s*(\S+)\s*$", block.group(1), re.M))
    assert granted == {"contents": "read", "issues": "write"}, (
        f"the token's scopes changed: {granted}. Its only write is a close, "
        "and an untrusted pull request body is what steers it"
    )
    on = re.search(r"^on:\n((?:  .*\n|\n)*?)^\w", workflow, re.M)
    assert on and re.findall(r"^  ([\w_]+):", on.group(1), re.M) == ["push"], (
        "the workflow gained a second trigger. A push to `main` is the only "
        "moment a closing keyword is readable, and any trigger an untrusted "
        "pull request can fire hands it the `issues: write` token"
    )
    assert re.search(r"^\s*branches:\s*\[main\]\s*$", workflow, re.M), (
        "the push trigger no longer names `main` alone"
    )


def test_the_script_closes_and_takes_off_one_named_label_and_nothing_else():
    """Parse the source; never search it.

    The arguments go one per line, so `issue reopen` cannot occur as a literal
    and a forbidden-substring list over the raw text forbids nothing. Folding
    the source first was the answer to that for a long time, and it is not
    enough: a fold normalises whitespace and nothing else, so a comment
    between two words of the argv defeats it just as the line breaks did. Two
    review rounds of #450 each found that from a different side. The reader is
    `ast` now and the fold is gone.

    **What the parse closes, and what it does not.** It closes layout — the
    argv wrapped one word per line, a comment between two of its words, any
    whitespace at all — because the tree does not carry layout. It does NOT
    close a value that is not a string literal. `words` keeps only
    `ast.Constant` strings and `issue_argvs` compares the first three of them
    against `["gh", "issue", verb]`, so a name anywhere in those three
    positions is dropped, the prefix shifts by one, and the verb is never
    matched. Measured in round 3 of #450 and again in its fix pass, four
    spellings of a planted `gh issue reopen`: plain and comment-separated both
    red this case; `GH = "gh"` used as the first word, and the verb moved into
    a module constant, both leave it green.

    So this reader is strictly stronger than the fold and blind in a place the
    fold was blind too. Closing that means resolving module-level names before
    comparing, which is a different checker with its own argument to make;
    `seal/follow-up.md` carries it with the repository owner named.

    **This used to say `only ever closes`, and #450 changed what is true.**
    The script now also removes `size: now` from the issue it is closing —
    the moment `docs/issues-and-milestones.md` had already named as where a
    spent sizing label comes off, with nothing acting on it. So `issue edit`
    is no longer forbidden outright; what is forbidden is `issue edit` in any
    form but `--remove-label`, because the property being protected was never
    the verb. It is that a re-run and a force-push are safe to reason about,
    and both acts are idempotent: the close skips an issue already closed,
    and the removal is guarded by a read saying the label is there.

    Adding a label here would not be. That is the sibling's act
    (`label_merged_on_release_branch.py`, at the squash rather than at the
    close), and a second writer of labels is how two scripts come to disagree
    about which is the current answer.
    """
    # **Every claim in this case is parsed, and none is searched.**
    #
    # Round 1's finding 6 was that two flag assertions were not bound to the
    # call they judged, and bound them through `ast`. Round 2's finding 1 was
    # that the binding was then made conditional on the reader it replaced:
    # the block ran under `if edits:`, where `edits` was a folded-substring
    # count with `assert edits <= 1` above it — and that passes at ZERO. So
    # any re-spelling the substring missed took the count to zero, skipped the
    # parse, and left the case asserting nothing at all about what the script
    # edits. Measured by the round: the argv rewritten across lines with one
    # comment between its words and `"--add-assignee", "someone"` added exits
    # 0, while the script assigns a person on every label removal.
    #
    # **The same blindness was under the five forbidden verbs**, which is the
    # class rather than the coordinate (`agent-contract` §12): they were
    # substring searches too, so a re-spelled `gh issue reopen` walked past
    # them for exactly the reason the `edit` one did. The folded reader is
    # gone from this case entirely; there is one reader and it does not care
    # how the argv is laid out.
    tree = ast.parse(read_text(".github", "scripts", "close_issues_on_release.py"))
    # BOTH argv shapes this file uses: `run("gh", …)` spreads the words as
    # call arguments, and `subprocess.run(["gh", …], …)` passes a list. The
    # one `issue edit` is written the second way, and a reader that knew only
    # the first parsed zero calls and asserted nothing — measured, on the
    # first spelling of round 1's fix.
    argvs = [node.elts for node in ast.walk(tree) if isinstance(node, ast.List)]
    argvs += [node.args for node in ast.walk(tree) if isinstance(node, ast.Call)]

    def words(argv):
        return [
            a.value
            for a in argv
            if isinstance(a, ast.Constant) and isinstance(a.value, str)
        ]

    def issue_argvs(verb):
        """Every `gh issue <verb>` argv in the script, however it is laid out."""
        return [argv for argv in argvs if words(argv)[:3] == ["gh", "issue", verb]]

    # **What this gave up, recorded rather than restored.** The folded form
    # asserted `'"gh", "issue", "close", str(issue),' in folded` — the verb
    # AND that the fourth word of that argv is the issue number. This checks
    # the count, which the folded form did not check at all, and reads no
    # operand: a close rewritten to act on something other than `issue`
    # passes. The trade is taken deliberately and is the same one the `edit`
    # argv below already makes, where the flags are read and the operand is
    # not — an operand is a variable name, and a name is exactly what this
    # reader cannot resolve (see the docstring). Pinning it would mean
    # asserting on an `ast.Name`'s spelling, which breaks on a rename that
    # changes nothing. Round 3 of #450 named the silence; this comment is it.
    closes = issue_argvs("close")
    assert len(closes) == 1, (
        f"{len(closes)} `gh issue close` argv lists; the script exists to "
        "close, exactly once, in one place"
    )
    for forbidden in ("reopen", "delete", "create", "comment", "transfer"):
        assert not issue_argvs(forbidden), (
            f"the script gained `issue {forbidden}`. Closing and taking off "
            "one named label is what makes a re-run and a force-push safe to "
            "reason about"
        )
    edit_calls = issue_argvs("edit")
    # EXACTLY one, never `<= 1`: the label removal is behaviour this case
    # pins, so a script that stopped editing is a script that stopped
    # spending the label, and the old `<= 1` was what let the whole block be
    # skipped at zero.
    assert len(edit_calls) == 1, (
        f"{len(edit_calls)} `gh issue edit` argv lists; there is one, and it "
        "is the removal of a spent sizing label"
    )
    flags = {word for word in words(edit_calls[0]) if word.startswith("--")}
    assert flags == {"--repo", "--remove-label"}, (
        f"the one `gh issue edit` carries {sorted(flags)}. It may carry "
        "`--remove-label` and nothing else that writes: adding a label is "
        "the sibling's act at the squash, and any other write is not the "
        "removal this case says the one edit is"
    )


def test_only_a_keyword_before_a_number_closes_anything():
    """The regexes, read rather than searched for.

    The fenced `Closes #88` in `docs/branch-and-release.md` is the example a
    person copies, so a pull request body quoting the document must not close
    the issue the document names — and bodies here quote documents routinely.
    """
    m = _closer()
    assert m.keywords_in("Closes #88") == ["88"]
    assert m.keywords_in("Closes #88, closes #92") == ["88", "92"]
    assert m.keywords_in("Part of #90") == []
    assert m.keywords_in("see #90 and #92") == [], (
        "a bare number with no keyword closes an issue"
    )
    assert m.keywords_in("```\nCloses #88\n```") == [], (
        "a fenced example closes the issue it names"
    )
    assert m.keywords_in("see `Closes #54` in the doc") == [], (
        "an inline code span closes the issue it names"
    )
    assert m.keywords_in("```\nCloses #1\n```\nCloses #88") == ["88"], (
        "prose after a fence stopped being read"
    )
    assert m.MERGED_PR.search("feat: a thing (#100)").group(1) == "100"
    assert m.MERGED_PR.search("fix: the (#61) thing was wrong") is None, (
        "a number mid-subject is read as a merged pull request"
    )


# --- #266: the shapes the two patterns gave up ------------------------------
#
# Review round 1 of work item 1788844400 enumerated five well-formed shapes
# `FENCE` and `SPAN` did not mask, by construction rather than by reading. A
# closing keyword inside any of them was read as a claim, so a RELEASE closed
# the issue. Three are masked now and two are deliberately not; each of the
# five has a case, so a later widening or narrowing is a red rather than a
# drift. The direction is stated at the patterns: masking more closes fewer,
# and an unclosed issue is visible and re-runnable where a wrong close is a
# false record on the tracker.


def test_a_tilde_fence_masks_a_keyword():
    """`~~~` is a fence to CommonMark and to GitHub, and it was invisible here
    because the pattern spelled backticks."""
    m = _closer()
    assert m.keywords_in("~~~\nCloses #1\n~~~\nCloses #4") == ["4"], (
        "a keyword inside a tilde fence closes the issue it names"
    )
    # A fence closes on ITS delimiter. Read as any delimiter, this one ends
    # at the backticks and the keyword after them is prose.
    assert m.keywords_in("~~~\n```\nCloses #1\n~~~\nCloses #4") == ["4"], (
        "a tilde fence was closed by a backtick line inside it"
    )


def test_a_fence_indented_under_a_list_item_masks_a_keyword():
    """A fence inside a list item is indented to the item's content, and the
    pattern anchored the delimiter at column 0."""
    m = _closer()
    body = "- the example:\n  ```\n  Closes #2\n  ```\nCloses #4"
    assert m.keywords_in(body) == ["4"], (
        "a keyword inside a fence indented under a list item closes the issue"
    )


def test_a_double_backtick_span_masks_a_keyword():
    """A span opened with two backticks closes with two, and may hold a
    single backtick inside. The one-backtick pattern read `` ``#150`` `` as
    two EMPTY spans with the number in prose between them."""
    m = _closer()
    assert m.keywords_in("Closes ``#3``\nCloses #4") == ["4"], (
        "a double-backtick span around the number leaves the keyword read"
    )
    assert m.keywords_in("see ``Closes #3`` there\nCloses #4") == ["4"], (
        "a double-backtick span around the whole claim leaves it read"
    )
    # The inner backtick is UNPAIRED on purpose: with a pair, the one-backtick
    # arm masks the claim anyway and the double form's reach is unmeasured.
    assert m.keywords_in("see ``Closes #3 ` x`` and Closes #4") == ["4"], (
        "a double-backtick span holding a single backtick is cut at the inner backtick"
    )


def test_a_four_space_indented_block_is_still_read_as_a_claim():
    """Deliberately unmasked. Four spaces open an indented code block to
    CommonMark, and they are ALSO how this repository's pull request bodies
    continue a bullet's text onto the next line — so masking the shape would
    drop real claims, which is the wrong direction for a closer. Stated at
    the pattern; this case turns a future widening into a decision."""
    m = _closer()
    assert m.keywords_in("- a bullet whose text\n    Closes #5") == ["5"]


def test_an_html_comment_is_still_read_as_a_claim():
    """Deliberately unmasked, and for a different reason: whether GitHub
    acts on a keyword inside a comment is unmeasured (`questions.md` Q1 of
    work item 1790173209), and a measurement needs a scratch pull request on
    a tracker. Until it is taken the shape stays as it was."""
    m = _closer()
    assert m.keywords_in("<!-- Closes #6 -->") == ["6"]


def _offline(monkeypatch, m, closed):
    """Shut every door this module has to the tracker, and make an escape loud.

    **Why this exists** — CI, 2026-09-22, on the pull request that merged
    #450. Three cases below stubbed `arrived`, `pull_request_body`,
    `issue_state` and `run`, and that was the whole set of readers `main`
    used. The label work added one more: `main` now asks `issue_labels`
    whether the issue carries a spent `size: now`, and that goes through
    `_issue_api`, which nothing here had stubbed. So all three walked into a
    live `gh api` call.

    **They passed anyway on every machine that ran them**, because `gh` is
    authenticated on a developer's laptop and under the broad gate. CI's
    pytest job has no `GH_TOKEN`, correctly, and it was the first party in
    the whole run that could see it: `SystemExit: gh api issues/88 failed`,
    on both the ubuntu and macOS legs, against `4164 passed`.

    That is the defect worth naming: **a case that reaches the network cannot
    fail for the reason it claims to test**, and whether it passes depends on
    who is logged in rather than on the code. Stubbing the one reader that
    leaked would have fixed the instance; this closes the class.

    Two doors, and both are shut here:

    - `_issue_api` is the only READ into the tracker, and `issue_state`,
      `pull_request_body` and `issue_labels` all go through it. Cases that
      stub those three by name keep their own stubs; this catches whatever
      they did not name, now or later.
    - `subprocess.run` is what `run` and `drop_label` reach for, and it
      RAISES rather than returning a stub, so a future path that escapes
      fails loudly and identically for everyone instead of passing for
      whoever holds a token.
    """

    def no_network(*args, **kwargs):
        raise AssertionError(
            f"this case reached the network: {args[0] if args else kwargs}. "
            "A case that calls `gh` passes or fails on whether the runner is "
            "authenticated, not on the code under test — CI caught exactly "
            "that on #500 and no local run could have"
        )

    monkeypatch.setattr(m.subprocess, "run", no_network)
    # An issue that exists and carries no labels: consistent with the
    # `issue_state` stubs above it, and it leaves `spent` False, so no case
    # here changes what it asserts.
    monkeypatch.setattr(m, "_issue_api", lambda repo, number: ({"labels": []}, True))
    monkeypatch.setattr(m, "run", lambda *a: closed.append(a) or "")
    # The close goes through `attempt` since #536, so a refusal cannot end
    # the run; it is the third door, and every close through it succeeds.
    monkeypatch.setattr(m, "attempt", lambda *a: closed.append(a) or (True, ""))


def test_it_closes_the_issue_the_keyword_named_and_nothing_else(monkeypatch):
    """Swapping the key and value in `wanted` would close the pull requests
    instead of the issues, and no string check can see that."""
    m = _closer()
    closed = []
    monkeypatch.setattr(m, "arrived", lambda b, a: ["feat: a thing (#100)"])
    monkeypatch.setattr(m, "pull_request_body", lambda r, n: "Closes #88\ncloses #92")
    monkeypatch.setattr(m, "issue_state", lambda r, n: "closed" if n == 92 else "open")
    _offline(monkeypatch, m, closed)
    monkeypatch.setenv("AFTER", "x")
    monkeypatch.setenv("REPO", "example/repo")
    monkeypatch.delenv("DRY_RUN", raising=False)
    m.main()
    assert [a[3] for a in closed] == ["88"], (
        f"it closed {[a[3] for a in closed]}. #88 is the open issue the keyword "
        "named; #92 was already closed"
    )


def test_a_number_that_names_nothing_does_not_kill_the_run(monkeypatch):
    """Round 2: the fix for `(#61)` reached one call site and not the other.

    A typo in a merged body — `Closes #9999` — sent a 404 through the shared
    `run`, which exits. Issues after it in sorted order stayed open, and a
    re-run died in the same place."""
    m = _closer()
    closed = []
    monkeypatch.setattr(m, "arrived", lambda b, a: ["feat: a thing (#100)"])
    monkeypatch.setattr(m, "pull_request_body", lambda r, n: "Closes #9999\ncloses #88")
    monkeypatch.setattr(m, "issue_state", lambda r, n: None if n == 9999 else "open")
    _offline(monkeypatch, m, closed)
    monkeypatch.setenv("AFTER", "x")
    monkeypatch.setenv("REPO", "example/repo")
    monkeypatch.delenv("DRY_RUN", raising=False)
    m.main()
    assert [a[3] for a in closed] == ["88"], (
        f"it closed {[a[3] for a in closed]}. A number naming nothing must be "
        "stepped over, not fatal, and the issues after it must still close"
    )


def test_dry_run_writes_nothing(monkeypatch):
    m = _closer()
    closed = []
    monkeypatch.setattr(m, "arrived", lambda b, a: ["feat: a thing (#100)"])
    monkeypatch.setattr(m, "pull_request_body", lambda r, n: "Closes #88")
    monkeypatch.setattr(m, "issue_state", lambda r, n: "open")
    _offline(monkeypatch, m, closed)
    monkeypatch.setenv("AFTER", "x")
    monkeypatch.setenv("REPO", "example/repo")
    monkeypatch.setenv("DRY_RUN", "1")
    m.main()
    assert closed == [], (
        "DRY_RUN wrote. It exists because this script was run by hand for its "
        "output during development and closed a real issue"
    )


def test_no_korean_pr_body_claims_a_close_that_did_not_happen():
    """Round 1: two committed `pr.ko.md` files said their pull request closed
    an issue, and neither did.

    `닫습니다` is not a GitHub keyword, so it fired nothing and read as a
    settled fact to anyone opening the file — worse than the dead English
    keyword beside it, which at least looks like machinery. One of the two
    named #54, the issue this work item leaves open on purpose."""
    import glob

    for path in sorted(glob.glob(os.path.join(ROOT, "seal", "specs", "*", "pr.ko.md"))):
        text = open(path, encoding="utf-8").read()
        for line in text.splitlines():
            if "닫습니다" in line and "#" in line and "닫히지" not in line:
                raise AssertionError(
                    f"{os.path.relpath(path, ROOT)} claims a close: "
                    f"{line.strip()[:90]} — a feature pull request into "
                    "`release/*` closes nothing, so this reads as a fact that "
                    "is not one"
                )


def test_the_document_says_where_an_issue_actually_closes():
    """Three pull requests wrote a closing keyword into a base that is not the
    default branch, and GitHub closed nothing.

    #89 wrote `Closes #88`, #97 wrote `Closes #54`, #100 wrote `Closes #92`.
    All three merged into the release branch; #88 and #92 were closed by hand
    once somebody noticed and #54 is still open. The squash messages carry no
    keyword either, so the release merge does not fire one as a side effect —
    which leaves the `release/*` to `main` pull request body as the only place
    in the whole sequence where an issue closes at all.

    Four things have to survive together or the rule is not the rule: that a
    feature pull request's keyword does nothing, WHY (its base is not the
    default branch), that the squash message is not a second chance, and where
    the keywords go instead. Deleting any one of them leaves prose.

    Collapsed before matching, because both documents are hand-wrapped and a
    literal match would be asserting their line breaks.
    """
    doc = " ".join(read_text("docs", "branch-and-release.md").split())
    assert "closing keyword does nothing when the base is `release/vX.Y.Z`" in doc, (
        "the document stopped saying which base makes the keyword inert -- "
        "and round 1 found the earlier wording, which blamed the kind of "
        "branch, false for #87: a fix branch straight into `main` whose "
        "`Closes #75` fired"
    )
    assert "The base is what decides this, not the kind of branch" in doc, (
        "the exception went, so a hotfix headed for `main` reads this rule "
        "and throws away a close that would have fired"
    )
    assert "default branch, and that branch is `main`" in doc, (
        "the cause is stated with the wrong branch named as default, which "
        "inverts the whole rule while every other sentence still reads true"
    )
    assert "left no LINK either, though the mention survives" in doc, (
        "the link half went, or came back as the overstatement round 1 "
        "measured false: `closingIssuesReferences` is `[]` and no `connected` "
        "event exists, but the CROSS-REFERENCE does survive -- opening #88 "
        "still shows #89. `no record at all` is the claim to keep out"
    )
    assert "squash commit message does not carry the keyword either" in doc, (
        "nothing rules out the release merge firing the keyword as a side "
        "effect, which is the reading that makes the rule look unnecessary"
    )
    assert "a workflow reads the keywords instead" in doc, (
        "the document names no mechanism that closes an issue at all"
    )
    assert "keyword repeats before every number" in doc, (
        "the collected form lost the reason it repeats the keyword — a bare "
        "`Closes #88, #92` closes one issue of two and reads as though it "
        "closed both"
    )
    # Round 1: every assertion above pins PROSE, and what gets copied into a
    # release pull request body is the CODE BLOCK. Rewriting it to the exact
    # form the paragraph beneath it warns against left all five green.
    # The example is what a person copies. Round 1 rewrote it into the exact
    # form the paragraph beneath warns against and every prose assertion
    # stayed green, so the block itself is pinned.
    assert "```\nCloses #88\n```" in read_text("docs", "branch-and-release.md"), (
        "the example block went, or grew back into a list -- one keyword and "
        "one number is what a feature pull request writes, and it is the only "
        "form the workflow reads"
    )
    assert "skipped rather than\n" not in doc  # collapsed doc; guard the phrase below
    assert "an issue already closed is skipped rather than" in doc, (
        "the workflow's only-ever-closes property left the document, which is "
        "what makes a re-run safe to reason about"
    )
    assert "A force-push is a different case and not a safe one" in doc, (
        "the document went back to calling a force-push harmless. It is not "
        "idempotent, it FAILS -- GitHub sends the displaced SHA and the range "
        "cannot be resolved -- and the two are different claims"
    )
    assert "sanctions no shorter form" in doc, (
        "the reason the keyword repeats went. It is what the documentation "
        "PRESCRIBES -- an earlier draft asserted the bare list closes only "
        "the first issue, which no source says and round 1 caught"
    )
    assert "`Part of #N` remains the form" in doc, (
        "the feature-pull-request form is gone -- the rule now says what does "
        "not work and nothing about what to write instead"
    )
    # The rule has to sit INSIDE the release sequence. `plan.md` rejected
    # appending it to the end of the file in writing, and moving it there was
    # green: a substring search reads a document as a bag of sentences.
    shapes = doc.index("The two merge shapes are not interchangeable")
    rule = doc.index("closing keyword does nothing when the base is")
    version = doc.index("The version is provisional until the content settles")
    assert shapes < rule < version, (
        "the rule left the release sequence -- a reader walking the sequence "
        "to write the release pull request no longer arrives at it"
    )
    assert "by a workflow rather than by anybody's hand" in doc, (
        "the bullet a sequence reader meets first went back to naming the "
        "release pull request body as the place an issue closes. It sat sixty "
        "lines above the paragraph that replaced it, so a reader walking the "
        "sequence got the old answer and stopped -- and then wrote no "
        "`Closes #N` for the workflow to read"
    )
    for pr in ("#37", "#38", "#39"):
        assert pr in doc, (
            f"{pr} is gone — a rule with no incident behind it is prose, and "
            "these three are what the rule was written from"
        )
    pointer = " ".join(read_text("CONTRIBUTING.md").split())
    assert "which issues a release closes" in pointer, (
        "CONTRIBUTING's release section stopped naming this among what "
        "`docs/branch-and-release.md` holds, so a reader deciding whether to "
        "open it before a merge is not told the answer is in there"
    )


def test_the_pull_request_checks_the_chain_it_was_routed_to():
    """The step cannot be dropped without a failure here.

    Moving enforcement off the commit and onto the pull request is only
    honest while the pull request actually checks. A workflow with the
    declaration and no step is the standing waiver `docs/review-chain-spec.md`
    refuses to build — quieter than the one it replaced, because a declaration
    that nothing reads leaves no trace at all.
    """
    workflow = open(
        os.path.join(ROOT, ".github", "workflows", "hygiene.yml"), encoding="utf-8"
    ).read()
    assert "chain_check.py" in workflow, "the chain check is not wired into CI"
    assert "--baseline" in workflow
    assert os.path.isfile(
        os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")
    ), "the workflow calls a script that is not there"


def test_the_chain_check_reuses_the_reader_rather_than_writing_a_second():
    """Two readers of the same markdown drifted apart in four places across
    three review rounds here, and closing one pair opened another. A 🔴 inside
    a comment or a fenced block has to be invisible to both."""
    check = open(
        os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py"),
        encoding="utf-8",
    ).read()
    assert "unverified_check.py" in check
    assert "reader.readable(" in check, (
        "the check reads lines the shared reader never normalized"
    )
    assert "def split_row" not in check, "a second row reader"


def test_this_repository_has_one_root_laid_out_by_lifetime():
    """S1 of the root move to `seal/`. It holds the whole tree — the rows
    that outlive a work item at its top, every work item whole under
    `specs/` — and neither of the two old roots exists. A `.specseal/` here
    would opt nothing in and be read by nothing but the migration hook, which
    is the silence every gate would give this repository."""
    seal = os.path.join(ROOT, "seal")
    for rel in ("README.md", "ledger.md", "follow-up.md"):
        assert os.path.isfile(os.path.join(seal, rel)), rel
    # `seal/ledger/` holds fragments between releases and the release folds
    # them away; git keeps no empty directory, so right after a release the
    # directory is absent and that is the laid-out state, not a missing one.
    ledger_dir = os.path.join(seal, "ledger")
    if os.path.isdir(ledger_dir):
        stray = [n for n in os.listdir(ledger_dir) if not n.endswith(".md")]
        assert not stray, (
            f"seal/ledger/ holds something that is not a fragment: {stray}"
        )
    # `seal/specs/` is absent after a complete fold for the same reason
    # `seal/ledger/` is absent after a release, and that is the laid-out
    # state. `assert items` stood here — some work item carries a routing.md
    # — and it was a floor of one (#517); what it was about holds at any
    # size and is stronger: every entry under `seal/specs/` is a work item,
    # whole, which starts with the declaration written before its first edit.
    specs = os.path.join(seal, "specs")
    if os.path.isdir(specs):
        loose = [
            n
            for n in sorted(os.listdir(specs))
            if not os.path.isfile(os.path.join(specs, n, "routing.md"))
        ]
        assert not loose, (
            f"seal/specs/ holds something that is not a work item: {loose}"
        )
    for old in (".specseal", "specs"):
        assert not os.path.exists(os.path.join(ROOT, old)), (
            f"{old}/ is back. Nothing reads it since 0.4.0; move it into seal/"
        )


def test_the_timer_sweep_survives_a_tracked_file_the_tree_deleted(tmp_path):
    """#432's class in the module the release checklist runs at step 3.

    This sweep is the one a release meets first: `fold_ledger.py` removes
    every `seal/ledger/` fragment as its last act and the whole gate then runs
    before anything is staged, so the index lists paths the disk does not
    have. The running version and the timer are both fixture values, for the
    reason `RUNNING_IN_THE_FIXTURES` already gives: a fixture that moves with
    the release proves nothing about the release after. Neither is
    `ILLUSTRATIVE_VERSION`, which `timers_in` exempts by name.
    """
    root = build_tracked_tree(
        tmp_path / "r",
        {
            "docs/live.md": "shipping in 0.9.0\n",
            "docs/folded.md": "the fragment the fold removes\n",
        },
        deleted=["docs/folded.md"],
    )
    files, missing = tracked(*LOADED, root=root)
    assert missing == ["docs/folded.md"], missing
    assert files == ["docs/live.md"], files
    assert timer_offenders(root, running=RUNNING_IN_THE_FIXTURES) == [
        "docs/live.md:1 names 0.9.0"
    ]


def test_the_running_version_comes_from_the_root_being_swept(tmp_path):
    """Round 1 ⬜ 7. A helper that takes a root and then reads `plugin.json`
    from somewhere else sweeps a fixture against this repository's release.

    The fixture declares its own version below both numbers in its documents,
    so one is a timer and the other is history. Read against THIS repository's
    version instead, both would be history and the sweep would report nothing
    — which is how the wrong root hides rather than fails.
    """
    root = build_tracked_tree(
        tmp_path / "r",
        {
            ".claude-plugin/plugin.json": json.dumps(
                {"version": RUNNING_IN_THE_FIXTURES}
            ),
            "docs/live.md": "shipping in 0.9.0\n",
            "docs/history.md": "shipped in 0.8.2\n",
        },
    )
    assert version(root) == RUNNING_IN_THE_FIXTURES
    assert timer_offenders(root) == ["docs/live.md:1 names 0.9.0"]
