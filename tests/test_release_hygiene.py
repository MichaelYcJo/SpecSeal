"""Release hygiene beyond "the changelog mentions the version".

That one is bound in `test_chain_hooks_hardening.py`. These are the two other
ways a release goes wrong inside the tree: a version number written into a
file that outlives it, and a supported-Python floor that three files state
differently.
"""

import json
import os
import re
import subprocess

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read_text(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def version():
    with open(
        os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8"
    ) as f:
        return json.load(f)["version"]


def tracked(*prefixes):
    out = subprocess.run(
        ["git", "ls-files", *prefixes],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.split()
    return [rel for rel in out if not rel.endswith((".gif", ".png", ".jpg"))]


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
# replaced caught for free. `(?!\w)` keeps `v1.2.30` from reading as `1.2.3`,
# and `(?!\.\d)` keeps `2.0.1.5` from reading as a release of this plugin. The
# two are spelled apart because a single `(?![\w.])` also swallowed a version
# at the END OF A SENTENCE — `right for 0.8.3.` answered no offender, where the
# substring check this replaced caught it (review round 1).
VERSION_TOKEN = re.compile(r"(?<![\w.])v?(\d+\.\d+\.\d+)(?!\w)(?!\.\d)")

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
    "docs/flow.md",
    # A trailing slash is a PREFIX, not a path. `docs/experiments/` holds
    # dated records of what was measured on a particular day, on a particular
    # build of a particular tool — the file name carries the date. Rewriting
    # the version an experiment ran against would falsify the record, which is
    # the same argument the three exact paths above already carry, applied to
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
}


def as_release(token):
    """`v0.9.0` and `0.9.0` alike -> `(0, 9, 0)`, which compares."""
    return tuple(int(n) for n in token.lstrip("v").split("."))


def is_a_record_of_a_moment(rel):
    """Exact paths and, where an entry ends in `/`, everything beneath it."""
    return any(
        rel == entry or (entry.endswith("/") and rel.startswith(entry))
        for entry in RECORDS_OF_A_MOMENT
    )


def shipped_versions():
    """Every version `CHANGELOG.md` records as released."""
    return set(re.findall(r"^## (\d+\.\d+\.\d+)\b", read_text("CHANGELOG.md"), re.M))


def timers_in(rel, text, running):
    """Every version-shaped token in `text` at or above `running`.

    Answers `(line number, token)` pairs. Below `running` is history and is
    kept: `docs/issues-and-milestones.md` says in so many words that *the
    branch `release/v0.3.0` shipped as 0.2.0*, and a rule that cannot state
    that fact is refusing history rather than catching a timer. That case is
    what decides against widening to every version this repository has ever
    shipped (#179's second candidate).
    """
    if is_a_record_of_a_moment(rel):
        return []
    ceiling = as_release(running)
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        for match in VERSION_TOKEN.finditer(line):
            bare = match.group(1)
            if bare == ILLUSTRATIVE_VERSION:
                continue
            if (rel, bare) in VERSIONS_OF_ANOTHER_PRODUCT:
                continue
            if as_release(bare) >= ceiling:
                found.append((number, match.group(0)))
    return found


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
      other paragraph, `docs/flow.md` is a list headed by the version it
      tracks, and `docs/experiments/` holds dated measurements whose numbers
      are the reading.
    - `ILLUSTRATIVE_VERSION` — the value the repository already tells authors
      to write, with its own case above asserting it is not a real one.
    - `VERSIONS_OF_ANOTHER_PRODUCT` — a number that belongs to somebody
      else's release train, pinned to the file that names it.
    """
    running = version()
    offenders = []
    for rel in tracked(*LOADED):
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
            text = f.read()
        for number, token in timers_in(rel, text, running):
            offenders.append(f"{rel}:{number} names {token}")
    assert not offenders, (
        f"a loaded file names a version at or above the running {running}. "
        "Such a line is right for exactly one release and a timer before it: "
        "it goes red on the day that version ships, on the release's own "
        "preparation commit, after the broad gate has already run.\n  "
        + "\n  ".join(offenders)
        + f"\n\nWrite the illustrative {ILLUSTRATIVE_VERSION} instead, and "
        "say beside it why the number is not real — the paragraph at "
        '`docs/issues-and-milestones.md` §"A rolling log is titled after the '
        'version it rolled from" already does exactly that, and is the model '
        "to follow. If the number belongs to another product, declare it in "
        "`VERSIONS_OF_ANOTHER_PRODUCT` with the product it names. If the "
        "file's whole job is to name a moment, it belongs in "
        '`RECORDS_OF_A_MOMENT` with the argument CONTRIBUTING.md §"What a '
        'change to a gate must carry" asks for. A version BELOW the running '
        "one is history and is already allowed — nothing needs doing to it."
    )


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
    assert timers_in("docs/flow.md", text, RUNNING_IN_THE_FIXTURES) == []
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
    # `(?!\w)`'s own case. The line above does NOT pin it: `\d+` is greedy, so
    # `v1.2.30` is matched whole with or without that lookahead, and a run
    # that dropped it left every case in this module green. What only it
    # refuses is a third component followed by a LETTER — the same shape as
    # round 1's finding, where a lookaround's guard could not see its loss.
    assert (
        timers_in("docs/x.md", "tagged 0.9.0rc1 last week", RUNNING_IN_THE_FIXTURES)
        == []
    )
    assert (
        timers_in("docs/x.md", "the python floor is 3.12", RUNNING_IN_THE_FIXTURES)
        == []
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
    for parts in (("skills", "implement", "SKILL.md"), ("agents", "smith.md")):
        # Collapsed, because both files wrap these sentences at different
        # columns and a literal match would be asserting the line breaks.
        text = " ".join(read_text(*parts).split())
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


def test_the_script_only_ever_closes():
    """Fold the source before matching.

    The arguments go one per line, so `issue reopen` cannot occur as a literal
    and a forbidden-substring list over the raw text forbids nothing. The
    earlier version also carried `or "issue" in script`, whose right side is
    true of any file with the word in it."""
    folded = " ".join(
        read_text(".github", "scripts", "close_issues_on_release.py").split()
    )
    assert '"gh", "issue", "close", str(issue),' in folded, "the script stopped closing"
    for forbidden in ("reopen", "delete", "edit", "create", "comment", "transfer"):
        assert f'"gh", "issue", "{forbidden}"' not in folded, (
            f"the script gained `issue {forbidden}`. Only ever closes is what "
            "makes a re-run and a force-push safe to reason about"
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


def test_it_closes_the_issue_the_keyword_named_and_nothing_else(monkeypatch):
    """Swapping the key and value in `wanted` would close the pull requests
    instead of the issues, and no string check can see that."""
    m = _closer()
    closed = []
    monkeypatch.setattr(m, "arrived", lambda b, a: ["feat: a thing (#100)"])
    monkeypatch.setattr(m, "pull_request_body", lambda r, n: "Closes #88\ncloses #92")
    monkeypatch.setattr(m, "issue_state", lambda r, n: "closed" if n == 92 else "open")
    monkeypatch.setattr(m, "run", lambda *a: closed.append(a) or "")
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
    monkeypatch.setattr(m, "run", lambda *a: closed.append(a) or "")
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
    monkeypatch.setattr(m, "run", lambda *a: closed.append(a) or "")
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
    items = [
        n
        for n in os.listdir(os.path.join(seal, "specs"))
        if os.path.isfile(os.path.join(seal, "specs", n, "routing.md"))
    ]
    assert items, "no work item under seal/specs/ carries a routing.md"
    for old in (".specseal", "specs"):
        assert not os.path.exists(os.path.join(ROOT, old)), (
            f"{old}/ is back. Nothing reads it since 0.4.0; move it into seal/"
        )
