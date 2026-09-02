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


def test_the_default_is_stated_where_the_path_is():
    """S2. A session that finds no row is standing in this section, so the
    default has to be here rather than three sections down.

    This case used to pin `No file, or no such row, means English` — the two
    absences the first draft named. Round 1 🟡 3 found two more (an empty
    value, an unreadable or unparseable file), so the sentence became a rule
    over all of them and `test_the_skill_names_every_way_of_not_naming_one`
    is where each one is now checked. What is left here is the placement.
    """
    section = read(*SKILL).split(
        "## The language is the repository's, and it says so in a file", 1
    )
    assert len(section) == 2, "the section was renamed; this case is now blind"
    body = section[1].split("\n## ", 1)[0]
    assert "lands on English" in body, (
        "the default is not stated in the section that sends a session to "
        "the file, so whoever finds no row has to go looking for it"
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
    assumed to match it.

    Round 1 🟡 5: this used to assert `seal/config.md` does not EXIST, so a
    repository that legitimately created one — holding the template's own
    default row, even — turned it red. Existence was never the question. The
    row is, and it is read the same way a session reads it.
    """
    import glob

    mirrors = sorted(
        os.path.basename(p)
        for p in glob.glob(os.path.join(ROOT, "seal", "specs", "*", "pr.*.md"))
    )
    assert mirrors, "no mirror files at all — this case is blind"
    forbidden = f"pr.{LANGUAGE_CODES[configured_language()]}.md"
    assert forbidden not in mirrors, (
        f"{forbidden} is a mirror in the body's OWN language, which is not a "
        f"mirror. This repository's pull request language is "
        f"{configured_language()}"
    )


def test_a_config_holding_the_templates_default_row_reads_as_english(tmp_path):
    """tests-todo row 1, first half. The file the plugin ships a template for
    must not be the file that breaks the check."""
    home = tmp_path / "seal"
    home.mkdir()
    (home / "config.md").write_text(read(*TEMPLATE), encoding="utf-8")
    assert configured_language(tmp_path) == "English"
    assert LANGUAGE_CODES[configured_language(tmp_path)] == "en", (
        "so `pr.ko.md` stays a legitimate mirror and `pr.en.md` does not"
    )


def test_a_korean_row_is_what_flips_the_refused_mirror_name(tmp_path):
    """tests-todo row 1, second half. The row is read, not the file's
    presence — a different row gives a different answer."""
    home = tmp_path / "seal"
    home.mkdir()
    (home / "config.md").write_text(
        "| Item | Value |\n|---|---|\n| Pull request language | Korean |\n",
        encoding="utf-8",
    )
    assert configured_language(tmp_path) == "Korean"
    assert LANGUAGE_CODES[configured_language(tmp_path)] == "ko", (
        "in a Korean repository `pr.ko.md` is the body's own language and "
        "`pr.en.md` is the mirror — the opposite of this repository"
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
            # ANY line that is not a row of this table ends it, a row of a
            # different table included. Round 1 🟡 6: a three-cell row used
            # to be skipped as though it were not there, so a `| a | b | c |`
            # between two two-cell rows let the row AFTER it be read as part
            # of this table. That is the separator defect one shape over.
            if found:
                break
            continue
        found.append((match.group("item"), match.group("value")))
    return found


# The mirror cases above call these two. They live here because they are
# built on `items()`, and Python resolves a name when the call runs rather
# than where it sits.

LANGUAGE_CODES = {"English": "en", "Korean": "ko", "Japanese": "ja"}


def configured_language(root=None):
    """A repository's pull request language, read the way the skill says.

    Every way of not naming one lands on English, and there are four: no
    file, no such row, an empty value, and a file that cannot be read or does
    not parse as that table. The direction is deliberate — a config nobody
    can read must not stop a commit.
    """
    path = os.path.join(root or ROOT, "seal", "config.md")
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return "English"
    for item, value in items(text):
        if item == "Pull request language":
            return value.strip() or "English"
    return "English"


UNNAMED = [
    ("no file at all", None),
    ("a file with no such row", "| Item | Value |\n|---|---|\n| Other | x |\n"),
    ("an empty value", "| Item | Value |\n|---|---|\n| Pull request language |  |\n"),
    ("a file that does not parse as that table", "# notes\n\nno table here.\n"),
    ("a file whose table is another one", "| Field | Value |\n|---|---|\n| a | b |\n"),
]


@pytest.mark.parametrize("what, body", UNNAMED, ids=[w for w, _ in UNNAMED])
def test_every_way_of_not_naming_a_language_lands_on_english(what, body, tmp_path):
    """🟡 3, run rather than only asserted in prose. A session that meets one
    of these and stops, asks, or guesses is the failure; all five answer the
    same."""
    home = tmp_path / "seal"
    home.mkdir()
    if body is not None:
        (home / "config.md").write_text(body, encoding="utf-8")
    assert configured_language(tmp_path) == "English", what


def test_an_unreadable_config_lands_on_english_too(tmp_path):
    """The fifth way, which needs a filesystem rather than a string: a
    `config.md` that is a DIRECTORY. `open` raises `IsADirectoryError`, an
    `OSError` — the class the reader catches, chosen so a permission error
    lands the same way."""
    (tmp_path / "seal" / "config.md").mkdir(parents=True)
    assert configured_language(tmp_path) == "English"


def test_the_skill_names_every_way_of_not_naming_one():
    """tests-todo row 2. The prose half: the reader above can only be right
    if the document says the same thing, and a session reads the document."""
    text = flat(*SKILL)
    assert "Every way of not naming a language lands on English" in text, (
        "the rule is not stated as one rule, so its cases read as a list "
        "somebody may believe is complete"
    )
    for phrase in ("no file", "no such row", "an empty value", "does not parse"):
        assert phrase in text, f"the skill does not name {phrase!r} as one of them"


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


def test_a_row_of_another_table_ends_this_one():
    """tests-todo row 3, from round 1 🟡 6.

    A three-cell row used to be skipped as though it were not there, so
    everything after it was absorbed. The interesting half is the LAST
    assertion: the danger was never the odd row itself, it was the ordinary
    row behind it arriving as though it belonged here.
    """
    text = (
        "| Item | Value |\n"
        "|---|---|\n"
        "| Pull request language | Korean |\n"
        "| a | b | c |\n"
        "| Something else | x |\n"
    )
    assert items(text) == [("Pull request language", "Korean")], (
        "a row of a different table did not end this one"
    )
    assert ("Something else", "x") not in items(text), (
        "the row behind the foreign one was read as part of this table"
    )


def test_a_second_table_further_down_is_not_read_as_more_rows():
    """The same property at document scale, which is what `config.md`
    actually looks like: a table, prose, then another table."""
    text = (
        "| Item | Value |\n"
        "|---|---|\n"
        "| Pull request language | Korean |\n"
        "\n"
        "## notes\n"
        "\n"
        "| Item | Value |\n"
        "|---|---|\n"
        "| Pull request language | English |\n"
    )
    assert items(text) == [("Pull request language", "Korean")], (
        "the first table's answer must win; a second one further down is "
        "prose about the first, not more rows of it"
    )


# --- every template has a reader --------------------------------------------


def test_every_template_is_named_by_a_document_that_ships():
    """tests-todo row 4, from round 1 🟡 1.

    The finding was that `templates/config.md` was named by nothing except a
    line-width list, so a session told to write `seal/config.md` had no
    source for it. That is a property of the DIRECTORY rather than of the one
    file it was found on: any template no document names is a file a session
    cannot find, and it writes one from scratch instead.

    `tests/` is excluded on purpose. A test naming a template is what the
    finding was about — the mention that looks like a reader and is not.
    """
    import glob
    import subprocess

    readers = subprocess.run(
        [
            "git",
            "ls-files",
            "skills",
            "agents",
            "hooks",
            "docs",
            "README.md",
            "README.ko.md",
            "CONTRIBUTING.md",
            "CLAUDE.md",
            "seal/README.md",
        ],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    ).stdout.split()
    corpus = ""
    for relative in readers:
        try:
            with open(os.path.join(ROOT, relative), encoding="utf-8") as handle:
                corpus += handle.read()
        except OSError:
            continue
    assert corpus, "no shipped documents were read — this case is blind"

    unreachable = [
        os.path.basename(path)
        for path in sorted(glob.glob(os.path.join(ROOT, "templates", "*")))
        if f"templates/{os.path.basename(path)}" not in corpus
    ]
    assert not unreachable, (
        "templates no shipped document names, so a session bootstrapping one "
        f"has nothing to copy: {unreachable}"
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
