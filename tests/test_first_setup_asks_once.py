"""First setup asks once — shared or local — and every document that a session
or a person reads says the same thing about where the root lives.

The work item is `seal/specs/1788354065-the-tree-that-must-stay-clean-has-no-
way-to-opt-in/`; the clauses named per case are its spec's. The hooks resolve
the root in code (`hooks/optin.py#home_at`) and are pinned by
`tests/test_optin_home.py` and `tests/test_local_mode_resolves_under_the_git_
dir.py`. What is pinned HERE is the text: the one question the `implement`
skill asks, the sentence a session needs, the workflow template shared mode
installs and the reason local mode has none, and the switch the READMEs give.

Every case was executed against the documents as they stood at 7e44106,
before any of them was edited, and every case failed; the output is in the
body of the commit that added this file.
"""

import os
import re

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

COMMON_DIR = "$(git rev-parse --git-common-dir)/seal/"
# The sentence a session reads (Q1 of the work item's `questions.md`): the
# same rule `hooks/optin.py` states, moved to where a session looks.
SESSION_RULE = "`$(git rev-parse --git-common-dir)/seal/` otherwise"


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def section(text, heading, level):
    """The text under HEADING up to the next heading of the same LEVEL."""
    assert heading in text, f"{heading!r} is not a heading any more"
    body = text.split(heading, 1)[1]
    return body.split("\n" + "#" * level + " ", 1)[0]


def paragraph(text, opening):
    """The paragraph whose first words are OPENING, its line breaks folded."""
    i = text.find(opening)
    assert i >= 0, f"no paragraph opens with {opening!r}"
    return flat(text[i:].split("\n\n", 1)[0])


def flat(text):
    """Runs of whitespace folded to one space, so a phrase that a hand-wrap
    splits across two lines still reads as the phrase."""
    return re.sub(r"\s+", " ", text)


def bootstrap():
    return section(read("skills", "implement", "SKILL.md"), "### Bootstrap", 3)


# --- S4: one question, two options, shared first --------------------------


def test_the_two_options_are_named_in_order_with_shared_as_the_default():
    boot = bootstrap()
    assert "AskUserQuestion" in boot
    shared, local = boot.index("**shared**"), boot.index("**local**")
    assert shared < local, "local is offered before shared"
    assert "default" in boot[shared:local], "shared is not marked as the default"


def test_each_option_says_what_it_creates_and_what_it_installs():
    boot = bootstrap()
    shared = paragraph(boot, "**shared**")
    local = paragraph(boot, "**local**")
    assert "creates `<repo>/seal/`" in shared
    assert "routing commit" in shared, (
        "the shared option does not say what carries the root"
    )
    assert "hygiene" in shared, "the shared option does not say what it installs"
    assert f"creates `{COMMON_DIR}`" in local
    assert "installs nothing" in local
    assert "touches nothing in the tree" in local


def test_the_root_is_spelled_through_the_common_dir_never_the_literal():
    """`.git` is a FILE in a linked worktree, so the literal path lands nowhere."""
    skill = read("skills", "implement", "SKILL.md")
    assert "git rev-parse --git-common-dir" in bootstrap()
    assert "`.git/seal/`" not in skill


def test_a_repository_with_the_root_at_either_place_is_never_asked():
    """S4 (d) and S12: the prompt budget is one question, once per repository."""
    never_again = paragraph(bootstrap(), "Ask only here")
    assert "either place" in never_again
    assert "<repo>/seal/" in never_again
    assert "git rev-parse --git-common-dir" in never_again


def test_the_parity_question_follows_the_mode_question():
    boot = bootstrap()
    assert boot.index("port behavior from an existing codebase") > boot.index(
        "**local**"
    )


def test_the_sentence_that_said_nowhere_else_is_gone():
    """The 0.4.0 sentence wraps as "and\nnowhere else", so the words are
    matched one at a time rather than as a phrase a line break can hide."""
    assert "nowhere else" not in read("skills", "implement", "SKILL.md")


def test_an_unmoved_old_layout_is_not_asked_but_told():
    """Q7: a repository that committed the 0.3.x directories chose shared
    already; the session-start hook moves it, and the skill says so instead
    of offering local mode beside a layout the hook will move into the tree."""
    boot = bootstrap()
    assert "0.3.x layout" in boot
    assert boot.index("0.3.x layout") < boot.index("**shared**")
    assert "moves it" in boot


# --- Q1: the sentence a session reads, once in each place -----------------


@pytest.mark.parametrize(
    "parts",
    [
        ("skills", "implement", "SKILL.md"),
        ("agents", "smith.md"),
        ("agents", "warden.md"),
    ],
)
def test_the_session_rule_appears_once(parts):
    text = read(*parts)
    assert text.count(SESSION_RULE) == 1, "/".join(parts)
    assert "means `<repo>/seal/` where" in text, "/".join(parts)


def test_the_session_rule_sits_in_the_layout_section_of_the_skill():
    skill = read("skills", "implement", "SKILL.md")
    assert skill.index(SESSION_RULE) < skill.index("### Bootstrap")


# --- S5 and S7: what shared mode installs, and why local mode has none ------


def template():
    return read("templates", "hygiene.yml")


def test_the_template_runs_the_two_shipped_checks_from_the_plugin_at_its_tag():
    t = template()
    assert "skills/verify/scripts/unverified_check.py" in t
    assert "skills/code-review/scripts/chain_check.py" in t
    assert t.count("--baseline") >= 2
    assert "seal/specs/" in t
    assert "+refs/pull/*/head:refs/remotes/pull/*/head" in t
    assert "v<version>" in t, "the plugin is not pinned to its tag"
    assert "MichaelYcJo/SpecSeal" in t
    assert "RUNNER_TEMP" in t or "runner.temp" in t, "the plugin lands in the tree"


@pytest.mark.parametrize(
    "stays_home", ["plugin.json", "gather_changelog", "fold_ledger", "README.ko.md"]
)
def test_the_rows_that_read_this_repository_do_not_travel(stays_home):
    assert stays_home not in template()


def test_the_template_header_says_why_local_mode_installs_none():
    header = "\n".join(
        line
        for line in template().split("\nname:", 1)[0].splitlines()
        if line.startswith("#")
    )
    assert "local mode" in header
    assert "examined nothing" in header
    assert "exits 0" in header and "exits 2" in header
    assert "shared" in header, "the header does not name the switch that gets CI"


def test_the_skill_writes_the_workflow_only_when_absent_and_local_installs_nothing():
    boot = flat(bootstrap())
    assert "templates/hygiene.yml" in boot
    assert ".github/workflows/hygiene.yml" in boot
    assert "only when" in boot and "absent" in boot
    assert "never overwritten" in boot
    assert "installs nothing" in boot


# --- S8 and S1: the READMEs -----------------------------------------------

READMES = {
    "README.md": ("## First run", "### Shared or local"),
    "README.ko.md": ("## 처음 실행", "### shared 인가 local 인가"),
}


@pytest.mark.parametrize("readme", sorted(READMES))
def test_the_readme_gives_both_moves_under_first_run(readme):
    text = read(readme)
    first_run, subsection = READMES[readme]
    assert text.index(subsection) > text.index(first_run)
    body = section(text, subsection, 3)
    assert 'mv "$(git rev-parse --git-common-dir)/seal" seal' in body
    assert "git add seal" in body
    assert "git rm -r --cached seal" in body
    assert 'mv seal "$(git rev-parse --git-common-dir)/seal"' in body
    assert "hygiene.yml" in body, "the workflow is installed or removed by hand"
    assert "#81" in body, "export/import is later work and is named as such"


@pytest.mark.parametrize("readme", sorted(READMES))
def test_the_gates_table_says_the_root_may_sit_under_the_git_dir(readme):
    rows = [
        line
        for line in read(readme).splitlines()
        if line.startswith("| ") and "`seal/`" in line.rsplit("|", 2)[-2]
    ]
    assert rows, f"{readme}: no gate row's Where cell names `seal/`"
    for row in rows:
        where = row.rsplit("|", 2)[-2]
        assert "local" in where, f"{readme}: {row[:40]}… still says the root only"


# --- S14: the root's own README, and the template it is rendered from ------


@pytest.mark.parametrize(
    "parts", [("seal", "README.md"), ("templates", "seal-README.md")]
)
def test_the_seal_readme_names_both_places(parts):
    text = read(*parts)
    assert "git rev-parse --git-common-dir" in text, "/".join(parts)
    assert "local" in text and "shared" in text, "/".join(parts)
    assert "either" in text, "/".join(parts)


def test_the_seal_readme_is_the_template_verbatim():
    assert read("seal", "README.md") == read("templates", "seal-README.md")


# --- Q8: the design record agrees with the code -----------------------------


@pytest.mark.parametrize(
    "parts, wrong",
    [
        (
            ("docs", "one-root-by-lifetime.md"),
            "would refuse a pull request with no round records",
        ),
        (
            ("docs", "one-root-by-lifetime.ko.md"),
            "라운드 기록이 없는 PR 은 그 워크플로에서",
        ),
    ],
)
def test_the_record_no_longer_says_the_checks_would_refuse(parts, wrong):
    text = read(*parts)
    assert wrong not in text, "/".join(parts)
    assert "examined nothing" in text or "아무것도 보지 않은 채" in text, "/".join(
        parts
    )


@pytest.mark.parametrize(
    "parts, decided, left_open",
    [
        (
            ("docs", "one-root-by-lifetime.md"),
            "## Decided after the thread",
            "## Decisions left open",
        ),
        (
            ("docs", "one-root-by-lifetime.ko.md"),
            "## 스레드 뒤에 정해진 것",
            "## 결정을 남겨 둔 것",
        ),
    ],
)
def test_the_scratch_row_moved_from_left_open_to_decided(parts, decided, left_open):
    text = read(*parts)
    assert "specseal-scratch" in section(text, decided, 2), "/".join(parts)
    assert "scratch" not in section(text, left_open, 2), "/".join(parts)


@pytest.mark.parametrize(
    "parts, decided",
    [
        (("docs", "one-root-by-lifetime.md"), "## Decided after the thread"),
        (("docs", "one-root-by-lifetime.ko.md"), "## 스레드 뒤에 정해진 것"),
    ],
)
def test_the_decided_table_carries_this_work_items_rows(parts, decided):
    body = section(read(*parts), decided, 2)
    rows = [line for line in body.splitlines() if line.startswith("| ")]
    for needle in (
        "templates/hygiene.yml",
        COMMON_DIR,
        "AskUserQuestion",
        "specseal-scratch",
    ):
        assert any(needle in row for row in rows), (
            f"{'/'.join(parts)}: no row names {needle}"
        )
    stamp = [row for row in rows if re.search(r"stamp|스탬프|표시", row)]
    assert stamp, f"{'/'.join(parts)}: the migration hook's stamp rule has no row"
