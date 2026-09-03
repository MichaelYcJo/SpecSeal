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
import subprocess

import pytest
from conftest import local_home, shell_probe

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
        # Phases 3 and 4 of #107 re-pointed both definitions' rows here. The
        # sentence was in two of them verbatim and in the third not at all,
        # and the agent without it is the one that reads `seal/parity.md`. It
        # is §16 of the contract now, which every agent receives at startup.
        ("skills", "agent-contract", "SKILL.md"),
    ],
)
def test_the_session_rule_appears_once(parts):
    text = read(*parts)
    assert text.count(SESSION_RULE) == 1, "/".join(parts)
    assert "means `<repo>/seal/` where" in text, "/".join(parts)


@pytest.mark.parametrize("agent", ["warden.md", "smith.md"])
def test_no_definition_carries_its_own_copy_of_the_root_rule(agent):
    """The move has to be a move. A definition that keeps the sentence beside
    the contract's is the duplication §16 was written to end, and it is
    invisible in a diff that only adds."""
    assert SESSION_RULE not in read("agents", agent), (
        f"agents/{agent} still spells the root rule out, so the tree holds "
        "two homes for it again"
    )


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
    # Both directions, not one. Round 1 of #104 found the header carrying the
    # two exit codes correctly and the conclusion drawn from them wrong: a
    # step that exits 2 is not a green build. `unverified_check.py` is red
    # forever and `chain_check.py` reports a pass it never earned, and the
    # header has to say both or it teaches the milder half.
    assert "red forever" in header
    # And why only red. Round 2 of #104 found the previous wording — "fails in
    # both directions at once" — describing something the workflow does not
    # do: `unverified_check.py` runs before `chain_check.py` and nothing
    # carries `continue-on-error`, so the job stops and the second check never
    # runs at all. Right exit codes, wrong conclusion, for the second time on
    # the same sentence.
    assert "never run" in header
    assert "examined nothing" in header
    assert "exits 2" in header
    assert "seal mode shared" in header, (
        "the header does not name the command that gets CI"
    )


def test_the_skill_writes_the_workflow_only_when_absent_and_local_installs_nothing():
    boot = flat(bootstrap())
    assert "templates/hygiene.yml" in boot
    assert ".github/workflows/hygiene.yml" in boot
    assert "only when" in boot and "absent" in boot
    assert "never overwritten" in boot
    assert "installs nothing" in boot


def test_the_version_is_read_from_the_plugin_root_and_not_from_the_tree():
    """Round 1 of #80, 🟡 4. The bootstrap said to read `version` from "the
    plugin's `.claude-plugin/plugin.json`" with no path. The session sits in
    the user's repository and that file sits in the plugin cache; a wrong read
    leaves `v<version>` in the workflow, and CI's `git clone --branch` fails.
    `skills/update/SKILL.md` already spells the path; the bootstrap does too,
    with the one-line command that reads it."""
    boot = flat(bootstrap())
    assert "$CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json" in boot
    assert "python3 -c" in boot, "no command reads the version"
    assert 'os.environ["CLAUDE_PLUGIN_ROOT"]' in boot


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
    assert f'mv "{COMMON}" "{TOP}"' in body
    assert f'git add "{TOP}"' in body
    assert f'git rm -r --cached "{TOP}"' in body
    assert f'mv "{TOP}" "{COMMON}"' in body
    assert "$CLAUDE_PLUGIN_ROOT/templates/hygiene.yml" in body, (
        "the workflow is installed by hand, from the plugin's cache"
    )
    assert "seal export" in body and "seal import" in body, (
        "the move is only available where both folders are on one machine, so "
        "this section has to point at the pair that works between two (#81). "
        "It named the issue number while the pair was later work"
    )


COMMON = "$(git rev-parse --git-common-dir)/seal"
TOP = "$(git rev-parse --show-toplevel)/seal"


def switch_block(readme):
    """The BY-HAND `bash` block under the README's switch section, comments
    off: two lines, local → shared and then shared → local.

    Bounded at the next `## ` heading and asserted to be there, the way
    `test_the_root_migrates_itself.by_hand_block` reads the coming-up block:
    the lines are run under `bash -c`, so a block that left its section must
    fail here rather than let a later block run in its place.

    The section holds more than one block since #104, which made switching a
    command (`seal mode`) and kept the by-hand pair below it. Taking "the
    first block" would hand `seal mode local` to `bash -c` and fail on a
    PATH this suite does not set up — so the block is chosen by what is IN
    it, and every candidate is read rather than the search stopping at the
    first that parses. A section that stopped carrying the by-hand pair
    fails here, which is the point: those two lines are what the command's
    move has to keep doing.
    """
    text = read(readme)
    _first_run, heading = READMES[readme]
    body = section(text, heading, 3).split("\n## ", 1)[0]
    assert "```bash\n" in body, f"{readme}: the switch block left its section"
    for chunk in body.split("```bash\n")[1:]:
        block = chunk.split("```", 1)[0]
        lines = [ln.split("#", 1)[0].strip() for ln in block.splitlines()]
        lines = [ln for ln in lines if ln]
        if len(lines) == 2 and all("mv " in ln for ln in lines):
            return lines
    raise AssertionError(
        f"{readme}: no bash block in the switch section holds the two by-hand "
        "moves. `seal mode` does that move, and this is where the move itself "
        "is checked against a subdirectory as the working directory"
    )


def porcelain(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.splitlines()


@pytest.mark.parametrize("readme", sorted(READMES))
def test_the_switch_block_lands_the_root_at_the_tree_root_from_a_subdirectory(
    readme, repo
):
    """Round 1 of #80, 🟡 3. The two moves were spelled relative to the
    working directory: run from `src/`, `git rev-parse --git-common-dir`
    answers `../.git` and `mv … seal && git add seal` created and staged
    `src/seal/`, after which neither place held a root and the repository
    was opted OUT. Both paths are asked of git now, so the block read out of
    the document and run from a subdirectory lands the root at `<repo>/seal/`
    one way and back under the common directory the other.

    A bash block, run under `bash -c` line by line; the precondition is
    executed, not assumed (`shell_probe`, for the reason the coming-up test
    gives).
    """
    why = shell_probe("bash")
    if why:
        pytest.skip(f"bash: {why} -- the switch block is a bash block")
    home = local_home(repo)
    (home / "ledger").mkdir()
    (home / "ledger" / "f.md").write_text("# rows\n", encoding="utf-8")
    sub = repo / "src"
    sub.mkdir()
    to_shared, to_local = switch_block(readme)

    r = subprocess.run(["bash", "-c", to_shared], cwd=str(sub), capture_output=True)
    assert r.returncode == 0, r.stderr
    assert (repo / "seal" / "ledger" / "f.md").is_file(), porcelain(repo)
    assert not (sub / "seal").exists(), "the root landed under the subdirectory"
    assert not home.exists(), "the local root was copied, not moved"
    assert porcelain(repo) == ["A  seal/ledger/f.md"], porcelain(repo)

    r = subprocess.run(["bash", "-c", to_local], cwd=str(sub), capture_output=True)
    assert r.returncode == 0, r.stderr
    assert (home / "ledger" / "f.md").is_file(), porcelain(repo)
    assert not (repo / "seal").exists()
    assert not (sub / "seal").exists()
    assert porcelain(repo) == [], porcelain(repo)


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
    # And it says both directions. A workflow left behind after a switch to
    # local is red on every pull request AND reports an unearned pass beside
    # it; a record naming only the green half teaches the milder failure.
    assert "examined nothing" in text or "아무것도 안 본 채" in text, "/".join(parts)
    assert "red forever" in text or "영원히 빨간불" in text, "/".join(parts)


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
