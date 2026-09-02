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

    Round 2 found that fix reproducing the same defect one line over, and the
    two assertions below are in the order the finding pairs demand.
    """
    import glob

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


def mirror_to_refuse(language):
    """The one `pr.<code>.md` that cannot be a mirror, or None.

    None is an answer, not a failure. `templates/config.md` licenses "a
    language's English name" and says the reader is a model rather than a
    lookup table, so a value this dictionary does not hold is a legitimate
    config — round 2 🔴 1, where indexing it raised `KeyError` on `French`
    and turned a legitimate repository red. A table that must list every
    language is always one short.
    """
    code = LANGUAGE_CODES.get(language)
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
    """A repository's pull request language, read the way the skill says.

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
            if item == "Pull request language":
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
        "| Item | Value |\n|---|---|\n| Pull request language | Korean |\n",
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
        "| Item | Value |\n|---|---|\n| Pull request language | Korean |\n",
        encoding="utf-8",
    )
    shared = repo / "seal"
    shared.mkdir(parents=True, exist_ok=True)
    (shared / "config.md").write_text(
        "| Item | Value |\n|---|---|\n| Pull request language | Japanese |\n",
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
        "| Pull request language | Korean |\n"
        "|---|---|\n"
        "| Something else | x |\n"
    )
    assert items(text) == [("Pull request language", "Korean")], (
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
        "| Pull request language | Korean |\n"
        "| Item | Value |\n"
        "| Pull request language | English |\n"
    )
    assert items(text) == [("Pull request language", "Korean")], (
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
    text = "| Item | Value |\n|---|---|\n\n| Pull request language | Korean |\n"
    assert items(text) == [("Pull request language", "Korean")]


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


def shipped_templates(root):
    """Every FILE under `<root>/templates/`, at any depth, as a `/` path.

    `**` with `include_hidden`, and files only. Round 2 🟡 4: a plain `*`
    returned a subdirectory as ONE entry whose name nothing names — so
    everything inside it was invisible — and skipped dotfiles entirely.
    """
    return sorted(
        os.path.relpath(path, root).replace(os.sep, "/")
        for path in glob.glob(
            os.path.join(str(root), "templates", "**"),
            recursive=True,
            include_hidden=True,
        )
        if os.path.isfile(path)
    )


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
    listed = subprocess.run(
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
    assert [name for name in listed if name.endswith(".md")], (
        "no shipped prose documents were listed — this case is blind"
    )
    assert shipped_templates(ROOT), "no templates found — this case is blind"
    unreachable = unreachable_templates(ROOT, listed)
    assert not unreachable, (
        "templates no shipped prose document names, so a session "
        f"bootstrapping one has nothing to copy: {unreachable}"
    )


def test_the_templates_check_reads_prose_only_and_descends(tmp_path):
    """tests-todo row 8, from round 2 🟡 4.

    The two narrowings, run against a tree built to have all three shapes.
    A Python comment must NOT count as a reader — that is the whole finding
    — and a template in a subdirectory or behind a dot must not be able to
    hide from the glob.
    """
    (tmp_path / "templates" / "sub").mkdir(parents=True)
    (tmp_path / "templates" / "named.md").write_text("x", encoding="utf-8")
    (tmp_path / "templates" / "sub" / "buried.md").write_text("x", encoding="utf-8")
    (tmp_path / "templates" / ".hidden.md").write_text("x", encoding="utf-8")
    (tmp_path / "doc.md").write_text(
        "start from templates/named.md\n", encoding="utf-8"
    )
    (tmp_path / "code.py").write_text(
        "# see templates/sub/buried.md and templates/.hidden.md\n", encoding="utf-8"
    )

    assert shipped_templates(tmp_path) == [
        "templates/.hidden.md",
        "templates/named.md",
        "templates/sub/buried.md",
    ], "the glob does not descend, or skips dotfiles"

    assert unreachable_templates(tmp_path, ["doc.md", "code.py"]) == [
        "templates/.hidden.md",
        "templates/sub/buried.md",
    ], (
        "a Python comment was accepted as a reader, which is exactly how "
        "`templates/sdd-round.md` passed on four comments in chain_check.py"
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
