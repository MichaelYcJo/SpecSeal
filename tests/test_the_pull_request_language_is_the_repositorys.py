"""The pull request language is the repository's, stated in `seal/config.md`.

`skills/commit-pr-convention/SKILL.md` required English at five places, and a
repository whose team writes another language had nowhere to say otherwise.
One row now answers for all four prose surfaces — commit subject, commit
body, pull request title, pull request body — and absence means English, so
a repository that says nothing is unaffected (#82).

Nothing in `hooks/` reads this file, and the reason is recorded rather than
left as an absence a later reader takes for an oversight: judging what
language a commit message is in means being wrong about names, identifiers
and quoted English, and a wrong stop blocks a correct commit. The mechanism
is the skill's text, the way it already is for the prefix vocabulary. So
every case here is over prose, and each one pins a phrase chosen so that the
drift it guards against cannot survive it.

The absence half of each pair is what makes these worth having. A document
can gain the corrected sentence and keep the old one two sections down, which
is how two answers ship at once — `tests/test_one_word_one_meaning.py` is
this repository's precedent for pinning both halves.
"""

import os
import re

import pytest

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
    """The file as one line, so a pinned phrase survives re-wrapping."""
    return " ".join(read(*parts).split())


SKILL = ("skills", "commit-pr-convention", "SKILL.md")
TEMPLATE = ("templates", "config.md")


# --- the row, and where it is read from -------------------------------------


def test_the_skill_names_the_file_and_the_row():
    """S1. Both halves: a session that knows the path but not the row does
    not know what to look for, and one that knows the row but not the path
    has nowhere to look."""
    text = flat(*SKILL)
    assert "config.md" in text, "the skill does not name the file it reads"
    assert "Pull request language" in text, "the skill does not name the row"


def test_the_root_is_resolved_rather_than_spelled():
    """S3. Local mode (#80) keeps the whole root under the common git
    directory. A skill that spells `<repo>/seal/` and stops sends a
    local-mode session to a path that is not there, and the config it then
    reports missing is the file that exists."""
    text = flat(*SKILL)
    assert "git rev-parse --git-common-dir" in text, (
        "the skill spells one place for the root, so a local-mode repository "
        "cannot carry a config at all"
    )
    assert "<repo>/seal/" in text, "the shared place went with the fix"


def test_absence_means_english_in_both_of_its_spellings():
    """S2. `No file` and `no row` are two different absences and a reader
    hits them at different moments — one before creating anything, one while
    reading a config somebody else wrote. Answering only the first leaves the
    second looking like an error."""
    text = flat(*SKILL)
    assert "No file, or no such row, means English" in text, (
        "the default is not stated where the path is, so a session that finds "
        "no row has to guess"
    )


# --- the five places that used to say English -------------------------------


RETIRED = [
    (
        "`<prefix>: <one line, starting lower-case>`, English.",
        "the commit subject",
    ),
    (
        "**English, in the subject and in the body.**",
        "the commit body",
    ),
    (
        "**The same prefix vocabulary as the commits, and English.**",
        "the pull request title",
    ),
    (
        "Are the title and body English?",
        "the self-check question",
    ),
]


@pytest.mark.parametrize("phrase, surface", RETIRED)
def test_the_surface_no_longer_requires_english_of_everyone(phrase, surface):
    assert phrase not in flat(*SKILL), (
        f"{surface} still requires English of every repository: {phrase!r}"
    )


def test_the_pull_request_body_section_no_longer_opens_with_english():
    """The fifth surface, which cannot be pinned by the phrase alone: a bare
    `**English.**` is two words and would match inside a sentence that is
    only describing the default. Pinned by its position instead — the first
    line of the section."""
    section = read(*SKILL).split("## Pull request bodies", 1)
    assert len(section) == 2, "the section was renamed; this case is now blind"
    first = section[1].strip().splitlines()[0]
    assert (
        first
        != "**English.** The prose and structure rules are `writing-style`'s, and it is"
    ), "the pull request body section still opens by requiring English"
    assert "language" in first, (
        f"it opens with neither the row nor a language: {first!r}"
    )


@pytest.mark.parametrize(
    "surface, phrase",
    [
        ("the commit subject", "in the repository's language"),
        ("the commit body", "One language, in the subject and in the body"),
        ("the pull request title", "and the same language"),
        ("the self-check question", "Pull request language` row names"),
    ],
)
def test_the_surface_defers_to_the_row_instead(surface, phrase):
    """The presence half. Removing the English requirement and saying nothing
    in its place leaves a session with no rule at all, which is worse than
    the rule that was too narrow."""
    assert phrase in flat(*SKILL), f"{surface} names no language rule at all"


# --- what the row deliberately does not reach -------------------------------


def test_the_prefix_vocabulary_is_not_translated():
    """S4. A translated prefix breaks the two things prefixes are for: a
    person scanning a log, and anything that parses one. The exclusion is
    stated in the skill AND in the template, because a person writing the
    config reads the second and never the first."""
    for parts, who in ((SKILL, "the skill"), (TEMPLATE, "the template")):
        text = flat(*parts)
        assert "prefix" in text and "not translated" in text, (
            f"{who} does not exclude the prefix vocabulary, so a Korean "
            "repository can read the row as licensing `기능:`"
        )


def test_branch_names_stay_ascii():
    """S5. A branch name is typed into a shell and pasted into a URL."""
    for parts, who in ((SKILL, "the skill"), (TEMPLATE, "the template")):
        text = flat(*parts)
        assert "ASCII" in text, f"{who} does not hold branch names to ASCII"


def test_the_response_language_stays_out_of_the_repository_file():
    """S6. Issue #82's third done-when row, and
    `docs/one-root-by-lifetime.md` before it: what the session says to you is
    a person's setting. Two people in one repository can want different
    answers there and the same one here, which is why one file cannot hold
    both."""
    for parts, who in ((SKILL, "the skill"), (TEMPLATE, "the template")):
        text = flat(*parts)
        assert "response language" in text, (
            f"{who} does not say the response language is elsewhere, so the "
            "first person to look for it will add a row here"
        )
        assert "person's setting" in text, f"{who} says where but not why"


# --- the mirror -------------------------------------------------------------


def test_the_mirror_is_named_for_its_own_language():
    """S7. `pr.ko.md` meant "the Korean translation of an English body". Read
    as "the mirror, in Korean" it needs no rename here and generalises: the
    twelve files in `seal/specs/` are already correct, because this
    repository's pull request language is English.

    Both directions are asserted. One alone reads as an example rather than
    a rule, and an example is what a session copies literally."""
    text = flat(*SKILL)
    assert "pr.<lang>.md" in text, "the mirror's name is still fixed to one language"
    assert "pr.ko.md" in text and "pr.en.md" in text, (
        "only one direction is given, so the rule reads as an example"
    )


def test_the_existing_mirrors_are_consistent_with_the_rule():
    """The twelve committed files, checked against the rule rather than
    assumed to match it. This repository states no language, so the default
    is English and the mirror is Korean."""
    import glob

    mirrors = sorted(
        os.path.basename(p)
        for p in glob.glob(os.path.join(ROOT, "seal", "specs", "*", "pr.*.md"))
    )
    assert mirrors, "no mirror files at all — this case is blind"
    assert set(mirrors) == {"pr.ko.md"}, (
        f"a mirror is not in the other language: {sorted(set(mirrors))}. This "
        "repository names no pull request language, so the body is English "
        "and every mirror here is `pr.ko.md`"
    )
    assert not os.path.exists(os.path.join(ROOT, "seal", "config.md")), (
        "this repository now carries a config; if its row is not English the "
        "line above is the wrong assertion"
    )


# --- the template, parsed the way `parity.md` is ----------------------------


HEADER = re.compile(r"^\|\s*Item\s*\|\s*Value\s*\|\s*$")
ROW = re.compile(r"^\|\s*(?P<item>[^|]+?)\s*\|\s*(?P<value>[^|]*?)\s*\|\s*$")
# `|---|---|` matches ROW as cleanly as a real row does — three pipes and two
# cells — and reading it as one put `('---', '---')` first, which is what the
# first run of this file actually returned.
SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")


def items(text):
    """Every `| Item | Value |` row under the first such header, in order.

    Deliberately the shape `templates/parity.md` already uses, so a reader
    written for one reads the other.
    """
    found, seen_header = [], False
    for line in text.splitlines():
        if HEADER.match(line):
            seen_header = True
            continue
        if not seen_header or SEPARATOR.match(line.strip()):
            continue
        match = ROW.match(line)
        if not match:
            if line.strip().startswith("|"):
                continue  # a row of some other table
            if found:
                break
            continue
        found.append((match.group("item"), match.group("value")))
    return found


def test_the_template_is_one_item_value_table_whose_first_row_is_the_language():
    """S8. Parsed, not eyeballed: the file's whole job is to be read."""
    rows = items(read(*TEMPLATE))
    assert rows, "no `| Item | Value |` table in the template"
    assert rows[0] == ("Pull request language", "English"), (
        f"the first row is not the language defaulting to English: {rows[0]}"
    )


def test_the_check_can_fail():
    """A parser that finds a row in anything is not a parser."""
    assert items("# a document with no table\n\nprose.\n") == []
    assert items("| Field | Value |\n|---|---|\n| a | b |\n") == [], (
        "`parity.md`'s header is `| Field | Value |`; matching it here would "
        "make this reader agree with a file it is not reading"
    )
    assert items("| Item | Value |\n|---|---|\n| a | b |\n") == [("a", "b")], (
        "the separator is being read as a row again"
    )


def test_the_template_says_the_file_is_optional():
    """The property that makes creating it at setup unnecessary
    (`questions.md` Q1). A template that reads as mandatory is how every
    repository ends up carrying a file restating the default."""
    text = flat(*TEMPLATE)
    assert "optional" in text, "the template does not say the file is optional"
    assert "absent" in text.lower(), "it does not say what absence means"


# --- a new permanent file in the root is listed where the root is described --


@pytest.mark.parametrize(
    "parts",
    [
        ("templates", "seal-README.md"),
        ("seal", "README.md"),
        ("README.md",),
        ("README.ko.md",),
    ],
)
def test_the_layout_lists_the_config(parts):
    """S9. Four documents draw the root's contents and a file in none of them
    is a file nobody finds. `seal/README.md` is the template verbatim —
    `tests/test_first_setup_asks_once.py` pins that equality and
    `hooks/root-migrate.py#rewrite_readme` depends on it — so the two move as
    one edit."""
    assert "config.md" in read(*parts), (
        "/".join(parts) + " draws the root without the config file in it"
    )
