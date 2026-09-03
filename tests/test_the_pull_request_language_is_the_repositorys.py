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

import glob
import os
import re
import subprocess

import pytest
from conftest import local_home

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
    assert "Commit and pull request language" in text, "the skill does not name the row"


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
        ("the self-check question", "Commit and pull request language` row names"),
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

    Round 2 found that fix reproducing the same defect one line over, and the
    two assertions below are in the order the finding pairs demand.
    """

    mirrors = sorted(
        os.path.basename(p)
        for p in glob.glob(os.path.join(ROOT, "seal", "specs", "*", "pr.*.md"))
    )
    assert mirrors, "no mirror files at all — this case is blind"

    # 🟡 7 first, and unconditionally: every mirror is named for A language.
    # Narrowing to "not the body's own" dropped that, and `pr.kr.md` — `kr`
    # is a country, `ko` the language — is the mistake twelve files are one
    # copy away from. It would have stayed green.
    unknown = sorted(
        name
        for name in set(mirrors)
        if name[len("pr.") : -len(".md")] not in set(LANGUAGE_CODES.values())
    )
    assert not unknown, (
        f"a mirror is not named for a language this file knows: {unknown}. "
        f"Known codes: {sorted(LANGUAGE_CODES.values())} — `kr` is a country "
        "and `ko` is the language, which is the near miss to check for first"
    )

    # 🔴 1: the template licenses "a language's English name" in as many
    # words, so `French` is a legitimate config and a three-entry dictionary
    # is always one short. A language with no code here is a gap in the
    # dictionary rather than a defect in the repository.
    language = configured_language()
    refused = mirror_to_refuse(language)
    if refused is None:
        pytest.skip(
            f"this repository's pull request language is {language!r} and "
            "this file has no code for it, so which mirror name to refuse "
            "cannot be computed. The rule still holds; adding the code to "
            "LANGUAGE_CODES is what makes it checkable again"
        )
    assert refused not in mirrors, (
        f"{refused} is a mirror in the body's OWN language, which is not a "
        f"mirror. This repository's pull request language is {language}"
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
        "| Item | Value |\n|---|---|\n| Commit and pull request language | Korean |\n",
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
        if not seen_header:
            if HEADER.match(line):
                seen_header = True
            continue
        # A header or a separator is this table's own furniture ABOVE its
        # first row, and somebody else's table BELOW it. Round 2 🟡 5: both
        # were stepped past wherever they appeared, so a stray separator or
        # a second `| Item | Value |` header let the rows behind it be read
        # as more of this one. Round 1's defect one line further along.
        if HEADER.match(line) or SEPARATOR.match(line.strip()):
            if found:
                break
            continue
        match = ROW.match(line)
        if not match:
            # And any other line that is not a row of this table ends it, a
            # row of a different shape included. Round 1 🟡 6: a row used
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
CODES_BY_NAME = {name.casefold(): code for name, code in LANGUAGE_CODES.items()}


def as_language_name(value):
    """A row's value reduced to the language name it spells.

    Markdown emphasis off both ends and case folded, because the row is typed
    by a person into a table cell: `**Korean**`, `_Korean_` and `korean` all
    name Korean. Nothing else is normalised — `Korean (KR)` is a different
    value and answering for it would be guessing.
    """
    return value.strip().strip("*_`").strip().casefold()


def mirror_to_refuse(language):
    """The one `pr.<code>.md` that cannot be a mirror, or None.

    None is an answer, not a failure. `templates/config.md` licenses "a
    language's English name" and says the reader is a model rather than a
    lookup table, so a value this dictionary does not hold is a legitimate
    config — round 2 🔴 1, where indexing it raised `KeyError` on `French`
    and turned a legitimate repository red. A table that must list every
    language is always one short.

    But None has to mean the language is ABSENT, not spelled differently.
    Round 3 finding 2: an exact lookup answered None for `**Korean**` and
    `korean`, so the mirror case skipped saying the file has no code for the
    language — which was false, and round 2's own probe table had already
    recorded `configured_language` returning `**Korean**` for an emphasised
    row. A person writing a markdown table emphasises a cell; that is the
    same value.
    """
    code = CODES_BY_NAME.get(as_language_name(language))
    return f"pr.{code}.md" if code else None


def config_homes(root):
    """The two places the root can be, in the order the skill reads them.

    `<repo>/seal/` first, then `$(git rev-parse --git-common-dir)/seal/`,
    which is where local mode keeps it (#80). Round 2 🟡 2: this reader
    joined the first and stopped, which is the very defect round 1 fixed in
    the prose — a Korean row under `.git/seal/` read back as English.

    git is asked rather than `.git/seal` spelled, because in a linked
    worktree `.git` is a FILE and the root belongs to the main tree's common
    directory. A path that is not a repository answers nothing and leaves
    the one home, which is what a `tmp_path` fixture is.
    """
    base = str(root or ROOT)
    homes = [os.path.join(base, "seal")]
    try:
        common = subprocess.run(
            ["git", "-C", base, "rev-parse", "--git-common-dir"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        common = ""
    common = (common or "").strip()
    if common:
        homes.append(os.path.join(base, common, "seal"))
    return homes


def configured_language(root=None):
    """A repository's commit and pull request language, read the way the skill says.

    Every way of not naming one lands on English, and there are four: no
    file, no such row, an empty value, and a file that cannot be read or does
    not parse as that table. The direction is deliberate — a config nobody
    can read must not stop a commit.

    The ROOT is resolved first and the config read from that one, the way
    `hooks/optin.py#home_at` resolves it: whichever of the two directories
    exists is the answer, and an unreadable file inside it is one of the
    four ways rather than a reason to look in the other place.
    """
    for home in config_homes(root):
        if not os.path.isdir(home):
            continue
        try:
            with open(os.path.join(home, "config.md"), encoding="utf-8") as handle:
                text = handle.read()
        except OSError:
            return "English"
        for item, value in items(text):
            if item == "Commit and pull request language":
                return value.strip() or "English"
        return "English"
    return "English"


# FOUR ways, in five ids. "Cannot be read or does not parse" is one way with
# two spellings, and the last two below are both that way — a file with no
# table at all, and one whose table belongs to something else. Round 2 ❓ 8
# settled the count: the skill's sentence says four, so four is the number,
# and keeping five shapes here costs nothing and exercises more.
UNNAMED = [
    ("no file at all", None),
    ("a file with no such row", "| Item | Value |\n|---|---|\n| Other | x |\n"),
    (
        "an empty value",
        "| Item | Value |\n|---|---|\n| Commit and pull request language |  |\n",
    ),
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


# --- round 2's findings, each with the case that would have caught it -------


def test_a_language_this_file_has_no_code_for_does_not_raise():
    """tests-todo row 5, from round 2 🔴 1.

    `templates/config.md` licenses any language's English name, so `French`
    is a legitimate config. Indexing a three-entry dictionary with it raised
    `KeyError` — not a failing assertion with a message, a traceback — which
    is round 1 🟡 5's own wording: a legitimate config still turned the case
    red.
    """
    assert mirror_to_refuse("French") is None, (
        "an unknown language must answer 'no name to refuse' rather than "
        "raising, so the case can skip with a reason instead of erroring"
    )
    assert mirror_to_refuse("English") == "pr.en.md"
    assert mirror_to_refuse("Korean") == "pr.ko.md", (
        "the two directions the skill gives as examples must both compute"
    )


@pytest.mark.parametrize(
    "value", ["**Korean**", "korean", "KOREAN", " Korean ", "_Korean_", "`Korean`"]
)
def test_a_language_spelled_differently_is_the_same_language(value):
    """tests-todo row 12, from round 3 finding 2.

    None has to mean the language is ABSENT. An exact lookup answered None
    for these, so the mirror case skipped with a message saying the file has
    no code for the language — false, and the skip hid the check. A person
    writing a markdown table emphasises a cell; that is the same value.
    """
    assert mirror_to_refuse(value) == "pr.ko.md", (
        f"{value!r} is Korean spelled by a person, and answering None for it "
        "makes the mirror case skip on a claim that is not true"
    )


def test_a_language_that_is_genuinely_absent_still_answers_none():
    """The other half, so the normalisation above does not become guessing.
    `French` is absent, and `Korean (KR)` is a different value this file has
    no business resolving."""
    assert mirror_to_refuse("French") is None
    assert mirror_to_refuse("Korean (KR)") is None, (
        "normalising past a parenthetical would be inventing an answer, not "
        "reading the row"
    )


def test_the_reader_finds_a_config_under_the_git_directory(repo):
    """tests-todo row 6, from round 2 🟡 2.

    The prose was fixed in round 1 and the reader shipped in the same commit
    joined `<root>/seal/` and stopped, so a local-mode repository's config
    was invisible to the one executable model of a session's reading this
    branch ships. `local_home` asks git for the common directory, the way
    the hooks do.
    """
    home = local_home(repo)
    (home / "config.md").write_text(
        "| Item | Value |\n|---|---|\n| Commit and pull request language | Korean |\n",
        encoding="utf-8",
    )
    assert configured_language(repo) == "Korean", (
        "a config under the local-mode root read back as English, which is "
        "the default meaning 'nobody said' — the wrong answer, silently"
    )


def test_the_tree_root_still_wins_over_the_git_directory(repo):
    """The order, not just the fallback. Whichever directory exists first is
    the root, so a repository holding both is answered by the committed one
    — `hooks/optin.py#home_at` resolves it that way and a reader that
    disagreed would send a session to the wrong file."""
    local = local_home(repo)
    (local / "config.md").write_text(
        "| Item | Value |\n|---|---|\n| Commit and pull request language | Korean |\n",
        encoding="utf-8",
    )
    shared = repo / "seal"
    shared.mkdir(parents=True, exist_ok=True)
    (shared / "config.md").write_text(
        "| Item | Value |\n|---|---|\n| Commit and pull request language | Japanese |\n",
        encoding="utf-8",
    )
    assert configured_language(repo) == "Japanese"


@pytest.mark.parametrize(
    "parts, who", [(SKILL, "the skill"), (TEMPLATE, "the template")]
)
def test_the_mirrors_home_is_resolved_and_excludes_the_git_directory(parts, who):
    """tests-todo row 7, from round 2 🟡 3.

    Round 1 fixed this in prose and nothing pinned it, in the file whose
    whole method is pinning prose. Three assertions, because the fix has
    three parts and any one of them can be edited away on its own: the home
    is resolved rather than spelled, the git directory is excluded, and the
    reason is given rather than asserted.
    """
    text = flat(*parts)
    assert "git directory" in text, (
        f"{who} does not say where the mirror must NOT go, so local mode "
        "gets a mirror nobody can open"
    )
    assert "commit candidate" in text or "cannot be committed" in text, (
        f"{who} excludes the git directory without the reason, so the next "
        "editor reads it as a preference"
    )
    assert "beside the documents the pull request already touches" in text, (
        f"{who} says where the mirror does not go and not where it does"
    )


def test_a_separator_below_the_rows_ends_the_table():
    """tests-todo row 9, from round 2 🟡 5, first shape."""
    text = (
        "| Item | Value |\n"
        "|---|---|\n"
        "| Commit and pull request language | Korean |\n"
        "|---|---|\n"
        "| Something else | x |\n"
    )
    assert items(text) == [("Commit and pull request language", "Korean")], (
        "a separator below the first row was stepped past, so the rows "
        "behind it were read as more of this table"
    )


def test_a_repeated_header_ends_the_table():
    """tests-todo row 9, second shape. An adjacent second table opens with
    the same header this one did, and that header is what used to set the
    flag a second time rather than end the first table."""
    text = (
        "| Item | Value |\n"
        "|---|---|\n"
        "| Commit and pull request language | Korean |\n"
        "| Item | Value |\n"
        "| Commit and pull request language | English |\n"
    )
    assert items(text) == [("Commit and pull request language", "Korean")], (
        "a repeated header did not end the table, so a second table's rows "
        "arrived as this one's"
    )


def test_a_mirror_named_for_a_country_is_caught():
    """tests-todo row 10, from round 2 🟡 7 — the can-it-fail half.

    `pr.kr.md` is one keystroke from `pr.ko.md` and twelve files are one
    copy away from it. The case above asserts the repository has none; this
    one asserts the rule those files are checked against actually rejects
    the near miss, rather than being a check that cannot fail.
    """
    known = set(LANGUAGE_CODES.values())
    assert "kr" not in known, (
        "`kr` is a country code; admitting it here would make the case above "
        "green for the exact mistake it exists to catch"
    )
    assert "ko" in known and "en" in known, (
        "the two codes this repository's mirrors actually use must be known, "
        "or every mirror reads as a near miss"
    )


def test_junk_above_the_first_row_is_still_tolerated():
    """The other direction, so the fix above does not become a stricter rule
    than the one intended: between the header and the first row, a separator
    is the table's own furniture and a blank line is nothing."""
    text = (
        "| Item | Value |\n|---|---|\n\n| Commit and pull request language | Korean |\n"
    )
    assert items(text) == [("Commit and pull request language", "Korean")]


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
    assert rows[0] == ("Commit and pull request language", "English"), (
        f"the first row is not the language defaulting to English: {rows[0]}"
    )
    # The second row is the records' own, and it is not the same question.
    # #106 split them because a repository can want Korean pull requests and
    # English specifications, and one row cannot say that.
    assert rows[1] == ("Record language", "English"), (
        f"the second row is not the record language defaulting to English: {rows[1]}"
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
        "| Commit and pull request language | Korean |\n"
        "| a | b | c |\n"
        "| Something else | x |\n"
    )
    assert items(text) == [("Commit and pull request language", "Korean")], (
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
        "| Commit and pull request language | Korean |\n"
        "\n"
        "## notes\n"
        "\n"
        "| Item | Value |\n"
        "|---|---|\n"
        "| Commit and pull request language | English |\n"
    )
    assert items(text) == [("Commit and pull request language", "Korean")], (
        "the first table's answer must win; a second one further down is "
        "prose about the first, not more rows of it"
    )


# --- every template has a reader --------------------------------------------


def shipped_templates(root):
    """Every TRACKED file under `<root>/templates/`, at any depth.

    Asked of `git ls-files`, which is the list the corpus is built from too,
    so both sides of the comparison agree about what exists. It answers
    repository-relative `/` paths, it descends, and it lists tracked
    dotfiles — the three properties round 2 needed.

    Round 3 finding 1: this globbed the WORKING TREE, and a glob and
    `git ls-files` disagree wherever `.gitignore` does. `.DS_Store` is
    ignored here and opening `templates/` in Finder creates one, so the check
    failed naming a file that is not a template and that `git status` does
    not show. Round 2's widening to dotfiles is what carried it in — the
    plain `*` it replaced happened to skip them.
    """
    out = subprocess.run(
        # `check=True`: round 4 finding 1, narrowed by round 5's 1. It closes
        # ONE state — a path git cannot read as a repository, which used to
        # answer `[]` and so read exactly like "there are no templates".
        # Two states this comment used to claim are not this argument's. A
        # repository with no tracked `templates/` answers `[]` at exit 0, and
        # that IS the true answer. A stubbed helper never reaches git at all,
        # and the existence assertion in
        # `test_an_untracked_file_under_templates_is_not_a_template` is what
        # catches that one, as its own docstring says.
        #
        # `-z`: round 4 finding 3. git C-escapes a non-ASCII path by default,
        # so the name came back in a spelling no prose can contain and the
        # check called it unreachable. Round 5's 2 measured which argument
        # does the work: `-z` alone turns the quoting off, and
        # `core.quotePath=false` alone does not.
        #
        # `core.quotePath=false` therefore changes nothing while `-z` is
        # here. It stays as the argument that WOULD be needed if `-z` were
        # ever dropped — so if one of the two is ever pruned, prune this one.
        [
            "git",
            "-c",
            "core.quotePath=false",
            "-C",
            str(root),
            "ls-files",
            "-z",
            "templates",
        ],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    ).stdout
    return sorted(name for name in (out or "").split("\0") if name.strip())


def unreachable_templates(root, listed):
    """The templates no PROSE document among `listed` names.

    Prose is `.md`. Round 2 🟡 4: reading `skills/`, `agents/` and `hooks/`
    whole takes their Python in too, and a template named only in a code
    comment is as unreachable as one named nowhere — a session bootstrapping
    a file does not read `chain_check.py` to find out what to copy.
    """
    corpus = ""
    for relative in listed:
        if not relative.endswith(".md"):
            continue
        try:
            with open(os.path.join(str(root), relative), encoding="utf-8") as handle:
                corpus += handle.read()
        except OSError:
            continue
    return [name for name in shipped_templates(root) if name not in corpus]


def test_every_template_is_named_by_a_document_that_ships():
    """tests-todo row 4, from round 1 🟡 1.

    The finding was that `templates/config.md` was named by nothing except a
    line-width list, so a session told to write `seal/config.md` had no
    source for it. That is a property of the DIRECTORY rather than of the one
    file it was found on: any template no document names is a file a session
    cannot find, and it writes one from scratch instead.

    `tests/` is excluded on purpose. A test naming a template is what the
    finding was about — the mention that looks like a reader and is not.

    Round 2 🟡 4 found the same hole one layer down. Excluding `tests/` and
    then reading `skills/`, `agents/` and `hooks/` whole takes in their
    PYTHON, and `templates/sdd-round.md` was passing on four comments inside
    `skills/code-review/scripts/chain_check.py`. A comment is not a document
    a session bootstraps from, so the corpus is prose — `.md` only. Two
    narrowings went with it: the glob returned a subdirectory as one entry
    and never descended, and it skipped dotfiles.
    """
    # The same three arguments `shipped_templates` carries, for the same
    # reason. Round 5 finding 3: round 4 applied them to one of two sibling
    # calls, and this one still C-escaped a non-ASCII name and — through
    # `.split()`, which splits on ANY whitespace — cut a name with a space in
    # two. `unreachable_templates` then dropped that document from the corpus
    # through its `except OSError: continue`, in silence, and a template only
    # that document named was reported unreachable.
    #
    # No `check=True` here: the assertion on the next line already turns an
    # empty listing red, which is what that argument buys above.
    listed = subprocess.run(
        [
            "git",
            "-c",
            "core.quotePath=false",
            "ls-files",
            "-z",
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
    ).stdout
    listed = [name for name in listed.split("\0") if name.strip()]
    assert [name for name in listed if name.endswith(".md")], (
        "no shipped prose documents were listed — this case is blind"
    )
    assert shipped_templates(ROOT), "no templates found — this case is blind"
    unreachable = unreachable_templates(ROOT, listed)
    assert not unreachable, (
        "templates no shipped prose document names, so a session "
        f"bootstrapping one has nothing to copy: {unreachable}"
    )


def test_the_templates_check_reads_prose_only_and_descends(repo):
    """tests-todo rows 8 and 11, from round 2 🟡 4 and round 3 finding 1.

    Built on a real repository rather than a bare directory, because what is
    under test is now a `git ls-files` call: a fixture git never sees would
    report nothing and the case would pass having exercised nothing.

    Four properties in one tree. A Python comment must NOT count as a reader
    — that is round 2's finding. A template in a subdirectory or behind a dot
    must not hide. An UNTRACKED file must not be reported as a template at
    all, which is round 3's: `.DS_Store` is gitignored here and arrives from
    opening the folder in Finder.

    And tests-todo row 14, from round 5's 3: a prose document whose own NAME
    is not ASCII, or holds a space, has to reach the corpus. git C-escapes
    the first and `.split()` cut the second in two, and either way
    `unreachable_templates` dropped that document silently and called the
    template only it names unreachable. The two documents below carry the
    only mention of `templates/sub/buried.md`, so if either is dropped the
    assertion at the end of this case goes red.
    """
    (repo / "templates" / "sub").mkdir(parents=True)
    (repo / "templates" / "named.md").write_text("x", encoding="utf-8")
    (repo / "templates" / "sub" / "buried.md").write_text("x", encoding="utf-8")
    (repo / "templates" / ".hidden.md").write_text("x", encoding="utf-8")
    (repo / "doc.md").write_text("start from templates/named.md\n", encoding="utf-8")
    (repo / "안내.md").write_text(
        "templates/sub/buried.md 에서 시작합니다\n", encoding="utf-8"
    )
    (repo / "two words.md").write_text(
        "start from templates/.hidden.md\n", encoding="utf-8"
    )
    (repo / "code.py").write_text(
        "# see templates/sub/buried.md and templates/.hidden.md\n", encoding="utf-8"
    )
    subprocess.run(
        ["git", "-C", str(repo), "add", "-A"],
        check=True,
        capture_output=True,
    )
    # Written AFTER the add, so it is untracked exactly as the real one is.
    (repo / "templates" / ".DS_Store").write_bytes(b"\x00\x01")

    assert shipped_templates(repo) == [
        "templates/.hidden.md",
        "templates/named.md",
        "templates/sub/buried.md",
    ], (
        "either the listing does not descend or skips tracked dotfiles, or "
        "the untracked `.DS_Store` came back as a template"
    )

    assert unreachable_templates(repo, ["doc.md", "code.py"]) == [
        "templates/.hidden.md",
        "templates/sub/buried.md",
    ], (
        "a Python comment was accepted as a reader, which is exactly how "
        "`templates/sdd-round.md` passed on four comments in chain_check.py"
    )

    # Row 14. The two documents whose own names git used to mangle are the
    # only prose naming these two templates, so a corpus that drops either
    # one reports the template it names as unreachable — which is what this
    # empty list refuses.
    assert unreachable_templates(repo, ["안내.md", "two words.md"]) == [
        "templates/named.md",
    ], (
        "a prose document whose name is not ASCII, or holds a space, did not "
        "reach the corpus, so the template only it names reads as unreachable"
    )


# Hand-copied from `templates/sdd-round.md` and checked against it, so this
# list is the EXPECTATION and the template is what is checked. It is not a
# reading of `skills/code-review/SKILL.md`: round 4's census found four of
# these eleven absent from that file, and two more matching only as
# substrings. Naming it after the skill was the overclaim; the list is fine.
ROUND_RECORD_FIELDS = [
    "Target SHA",
    "PR",
    "Broad gate",
    "Fixes checked by",
    "Contract changes",
    "New units",
    "Needs a fix",
    "## Verdicts",
    "## Executed probes",
    "## Inherited coordinates",
    "## Deferred",
]


@pytest.mark.parametrize("field", ROUND_RECORD_FIELDS)
def test_the_round_template_carries_the_fields_it_is_expected_to(field):
    """tests-todo row 13, from round 3 finding 3, narrowed by round 4's 2.

    `ROUND_RECORD_FIELDS` is hand-copied from `templates/sdd-round.md` and
    checked against `templates/sdd-round.md`, so what runs is that the
    template still carries the fields THIS LIST expects — a pin on the
    template, and on nothing else.

    It used to call them "the fields the skill names", and round 4's census
    found four of the eleven absent from `skills/code-review/SKILL.md`, with
    `PR` and `## Verdicts` matching only as substrings. Round 3's own finding
    had said the template carries `PR` where the skill's row does not list
    it, and `PR` went into this list anyway. Nothing about the check changed
    here; the claim came down to it.

    What that gives up, so nobody reads more into it: drift on the SKILL side
    is invisible to this case. Closing that needs a second list and a second
    direction, which is a new unit — round 4 forbids one, and round 5 is the
    place to weigh whether it is worth having at all.
    """
    assert field in read("templates", "sdd-round.md"), (
        f"{field!r} is a field a round record is expected to carry and is "
        "not in `templates/sdd-round.md`, the file a round starts from"
    )


def test_the_sentence_no_longer_claims_an_order():
    """The absence half. Keeping the corrected sentence beside the old one is
    how two answers ship at once, and this file's method is pinning both."""
    text = flat("skills", "code-review", "SKILL.md")
    assert "templates/sdd-round.md" in text, (
        "the file's only mention in the prose corpus went, which makes it "
        "unreachable again"
    )
    assert "in the order the row above lists them" not in text, (
        "the order claim is back, and the template does not read that way"
    )


def test_an_untracked_file_under_templates_is_not_a_template(repo):
    """tests-todo row 11, from round 3 finding 1, isolated.

    The case above would also catch this, mixed in with two other
    properties. This one fails for one reason only: before the fix,
    `unreachable_templates` reported `templates/.DS_Store` and the check went
    red naming a file that is not a template and that `git status` hides.

    Round 4 finding 1: asserting `== []` twice pins only one direction. A
    helper that had stopped seeing anything would satisfy both, so the
    existence assertion below is what keeps this case from passing on
    silence.
    """
    (repo / "templates").mkdir(parents=True)
    (repo / "templates" / "named.md").write_text("x", encoding="utf-8")
    (repo / "doc.md").write_text("start from templates/named.md\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(repo), "add", "templates", "doc.md"],
        check=True,
        capture_output=True,
    )
    assert shipped_templates(repo) == ["templates/named.md"], (
        "the listing sees nothing, so every `== []` below would pass on "
        "silence rather than on the property they are here for"
    )
    assert unreachable_templates(repo, ["doc.md"]) == []

    (repo / "templates" / ".DS_Store").write_bytes(b"\x00\x01")
    assert unreachable_templates(repo, ["doc.md"]) == [], (
        "an untracked file under `templates/` is reported as an unreachable "
        "template, so anyone who opens the folder in Finder fails this check"
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


# --- the exclusion list, derived rather than compared ----------------------


def _checker(name, *parts):
    """Import a checker by path, the way this repository's own cases do."""
    import importlib.util

    path = os.path.join(ROOT, *parts)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _governs_nothing():
    """The `What no row governs` section of the template, flattened."""
    text = read(*TEMPLATE)
    start = text.index("## What no row governs")
    end = text.index("\n## ", start + 1)
    return " ".join(text[start:end].split())


def _literal_strings():
    """Every string the checkers match literally, read from the checkers.

    Derived, not copied. Round 1 of #106 found two headings missing from a
    hand-written list that had been copied into three documents — and the
    list's own grounds are *what a checker reads*, so a second source of it
    is a second source of the truth it claims to state.
    """
    chain = _checker(
        "chain_check", "skills", "code-review", "scripts", "chain_check.py"
    )
    unverified = _checker(
        "unverified_check", "skills", "verify", "scripts", "unverified_check.py"
    )
    found = {
        chain.VERDICTS,
        chain.VERDICT_COLUMN,
        chain.TARGET,
        chain.CHECKED_BY,
        chain.CONTRACT,
        chain.NEW_UNITS,
        chain.NONE_WORD,
        chain.NO_FIXES,
        chain.NOBODY,
        chain.BLOCKING,
        chain.PR_FIELD,
        unverified.HEADING,
        unverified.CLOSED,
        *unverified.HEADER,
        *chain.CLOSED_WORDS,
    }
    return sorted(found)


@pytest.mark.parametrize("literal", _literal_strings())
def test_the_exclusion_list_holds_every_string_a_checker_matches(literal):
    """S6. The list's grounds are *what a checker reads literally*, so it is
    checked against the checkers rather than against itself.

    Two were missing when this case was written — `## Verdicts` and
    `## Not verified` — and a repository that set `Record language` to another
    language would have translated both: the first makes `chain_check.py`
    report a record that says nothing about what it found, and the second
    turns `unverified_check.py` red on every pull request.
    """
    # Backticked, because the section spells every literal that way and a
    # BARE substring is satisfied by a longer entry that contains it —
    # `fixed` was held by `agreed, fixed` alone, and deleting the standalone
    # entry left this case green (round 2).
    assert f"`{literal}`" in _governs_nothing(), (
        f"a checker matches `{literal}` literally and the exclusion list does "
        "not hold it as an item of its own, so a repository translating its "
        "records breaks that checker with nothing to warn it"
    )


# Every shipped document that tells a session which row to read. A document
# naming the wrong row sends the session to a row that does not exist, and
# round 1 found two that had drifted with nothing red.
ROW_READERS = [
    ("templates", "config.md"),
    ("templates", "seal-README.md"),
    ("skills", "config", "SKILL.md"),
    ("skills", "implement", "SKILL.md"),
    ("skills", "commit-pr-convention", "SKILL.md"),
    ("skills", "code-review", "SKILL.md"),
    # Phase 3 of #107 re-pointed the warden's row here: the record-language
    # section was in two definitions in near-identical words and in the third
    # not at all, and it is §11 of the agent contract now. `agents/smith.md`
    # still carries its copy; phase 4 moves that one.
    ("skills", "agent-contract", "SKILL.md"),
    ("agents", "smith.md"),
]


@pytest.mark.parametrize("parts", ROW_READERS, ids=lambda p: "/".join(p))
def test_every_document_that_names_a_language_row_names_the_shipped_one(parts):
    """The pairing this branch was reviewed as one round for: a document
    naming the wrong row is invisible until somebody follows it."""
    text = flat(*parts)
    assert "Record language" in text, (
        f"{'/'.join(parts)} does not name `Record language`, the row that "
        "governs the prose it is about"
    )
    # Case-folded: `the \`pull request language\` row` in lower case is the
    # spelling that actually survives in this tree, and round 2 found it green.
    assert "pull request language" not in text.casefold().replace(
        "commit and pull request language", ""
    ), (
        f"{'/'.join(parts)} still names the row `Pull request language`, "
        "which #106 renamed"
    )


@pytest.mark.parametrize("field", ROUND_RECORD_FIELDS)
def test_the_exclusion_list_holds_every_field_a_pinned_case_reads(field):
    """The list's grounds are *a checker OR a pinned case*, and this is the
    pinned case.

    `_literal_strings()` reaches only what a checker holds in a module
    constant, so the second half of those grounds had nothing checking it —
    and round 2 found the fix for round 1 removing `Needs a fix` from the list
    while adding `Broad gate` on identical footing. Three section headings had
    never been on it at all.
    """
    assert f"`{field}`" in _governs_nothing(), (
        f"a pinned case reads `{field}` literally and the exclusion list does "
        "not hold it, so a repository translating its records is told it may"
    )
