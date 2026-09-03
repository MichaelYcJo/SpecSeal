"""The SDD file set was read two ways at once, and the counts said so.

`seal/specs/` is the root for a work item — its whole lifetime, its whole
contract.
`spec.md` was a file on a ladder keyed to how many files the work touched. Both
readings live in `skills/implement/SKILL.md`, neither is wrong on its own
terms, and under the second one 33 of 35 work items here carry only a closing
memo. That is either correct or a set that quietly fell apart, depending on
which reading a session happens to hold.

Three things settle it, and each is pinned below.

  the condition   `spec.md` is owed when the work alters observable
                  behaviour, not when it touches six files. A count also
                  never said WHEN it was taken (issue #54), and a test with
                  no number has no such moment
  the status      `plan.md` absorbs the task list nobody ever wrote, as a
                  column whose closed value is the commit that closed the
                  phase — a past state, which is what lets it sit inside the
                  contract at all
  the home        `.specseal/tasks/` is described in no shipped document,
                  because no code has ever read it and it has never once been
                  created

These are prose assertions, and prose assertions are worth exactly what their
substrings are chosen to be. Each one below picks a phrase that cannot survive
the drift it is guarding against.
"""

import glob
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


# --- the condition ----------------------------------------------------------


# Keyed BY FILE. A flat set exempts a line in EVERY document, and round 4
# pasted a `SKILL.md` exemption into `templates/sdd-overview.md` — the file a
# session actually types into — and it passed.
#
# What this costs, recorded because round 4 found it unrecorded: re-wrapping
# one of these lines without changing its meaning turns the check red, and the
# message then says `decides by file count`, which is not true. That is the
# price of an allow-list over prose, and no shape was found that keeps the
# property without it.
#
# Every count these four documents hold today, named line by line. A NEW one
# is not in this set, so it raises — which is the whole property, and the one
# a rule for choosing WHICH lines to look at cannot have.
#
# Round 2 replaced a list of four spellings with a pattern, and then chose the
# lines to run it against with a list of three keywords (`rung`, `ladder`,
# `threshold`). Measured in round 3: the pattern matches nine lines across
# these files and the keyword gate inspected ZERO of them. The enumeration had
# not been removed, only moved one axis over, and moving it made the check
# inert rather than merely narrow.
KNOWN_PROSE = {
    ("skills", "implement", "SKILL.md"): frozenset(
        {
            "used to read *6+ files, a new module, or an architectural choice*, and two of",
            "beside the contract. Progress does the same thing one file up, in `plan.md`'s",
            "also the four files that were not committed yet*.",
            "calls, 128 shell edits across 47 files, 2.7 edits per file, and a column",
            "- **One file, and it qualifies.** A change to an agent's persona is two files",
            "finished at eight files with five of them arriving in review rounds 2 and 3.",
            "*six files* was a count, and two people can disagree about a borderline case.",
        }
    ),
    ("agents", "smith.md"): frozenset(
        {
            "A two-file wording change to an agent's persona is over it at the first",
            "call; run the cases from one file in one command. A round is mostly",
        }
    ),
}


def test_the_top_rung_names_behaviour_rather_than_a_count():
    """S6. The rung itself, in the skill and in the agent that reads it.

    A count is the thing being replaced, so `6+ files` may not survive as the
    condition anywhere — a session reading the agent file and a session
    reading the skill would otherwise apply two different tests.
    """
    skill = read("skills", "implement", "SKILL.md")
    smith = read("agents", "smith.md")
    for text, who in ((skill, "implement/SKILL.md"), (smith, "agents/smith.md")):
        assert "observable behaviour" in text, f"{who} lost the condition"
        assert "| 6+ files" not in text, f"{who} still has the count as a rung"

    # Every document a session fills in, not only the two above, and every
    # spelling of the count rather than the one the rung happened to use.
    # `| 6+ files` alone left `6-file line` standing in the same file and
    # the en-dash spelling in the template a session actually types into.
    # Round 1 found both. A past-tense sentence explaining what the rung
    # USED to say is allowed, and is what `used to read` marks.
    #
    # `feature-planner` is deliberately NOT here: its `Use when:` counts
    # files, and that was left standing because it decides when to CALL a
    # skill, not what a work item owes. Round 2 found the reason recorded
    # nowhere, so it is recorded here rather than left as an absence a
    # later reader takes for an oversight.
    for parts in (
        ("skills", "implement", "SKILL.md"),
        ("agents", "smith.md"),
        ("templates", "sdd-overview.md"),
        ("templates", "sdd-plan.md"),
    ):
        text = read(*parts)
        # A PATTERN, not a list of spellings. Round 2 defeated the list three
        # times over -- `six files`, `more than five files`, `6 files` --
        # because it named four spellings and a count has as many as English
        # does. `\u2013` is an EN DASH, escaped rather than typed so a linter
        # does not read a bare one as a typo.
        counted = re.compile(
            r"\b(?:\d+\s*[-\u2013]\s*\d+|\d+\+?|one|two|three|four|five|six|"
            r"seven|eight|nine|ten)[\s-]+files?\b",
            re.I,
        )
        for line in text.splitlines():
            hit = counted.search(line)
            if not hit or line.strip() in KNOWN_PROSE.get(parts, frozenset()):
                continue
            raise AssertionError(
                "/".join(parts)
                + f" decides by file count ({hit.group(0)!r}): {line.strip()}"
            )


def test_the_rung_gives_both_directions():
    """S6, the half that makes it usable.

    One direction alone is how a rule gets read as "when in doubt, write
    one" or "when in doubt, don't". The small change that qualifies and the
    large one that does not are both measured cases in this repository, and
    naming them is what stops the rung being re-read as a count.
    """
    skill = read("skills", "implement", "SKILL.md")
    assert "One file, and it qualifies" in skill
    assert "Many files, and it does not" in skill
    assert "warden-persona-accuracy" in skill, (
        "the worked example is a real branch that missed the rung by growing "
        "past it — without it the direction is an assertion"
    )
    assert "issue #35" in skill, (
        "the count never said when it was taken, and that is the half a "
        "reader has to be able to look up"
    )


# --- the home that never existed --------------------------------------------

# Everything a session installing this plugin reads to learn the layout. The
# precedent is `test_the_documents_that_instruct_never_name_the_old_directory`:
# a path may not appear in an instructing document at all, not even hedged,
# because a reader following instructions stops at the first path it sees. The
# reason `tasks/` is gone lives in the changelog and in the work item's memo,
# which are read by people rather than followed by sessions.
INSTRUCTING = (
    ("seal", "README.md"),
    ("templates", "seal-README.md"),
    ("skills", "implement", "SKILL.md"),
    ("skills", "feature-planner", "SKILL.md"),
    ("README.md",),
    ("README.ko.md",),
)


def test_no_shipped_document_still_names_a_task_list_directory():
    """S8. No code has ever read `.specseal/tasks/` and it has never once been
    created — in this repository or in any that installed the plugin."""
    for parts in INSTRUCTING:
        text = read(*parts)
        assert "tasks/" not in text, f"{'/'.join(parts)} still names it"


def test_the_two_layout_trees_no_longer_show_it():
    """The tree is the half a session copies. Prose can be skimmed; a tree
    that lists a directory is read as a directory to create."""
    for parts in (("seal", "README.md"), ("templates", "seal-README.md")):
        text = read(*parts)
        assert "follow-up.md         schedulable items" in text, (
            f"{'/'.join(parts)}: the tree changed shape — re-read it"
        )
        assert "<work-item-slug>.md" not in text


def test_the_plugin_home_is_described_as_permanent_throughout():
    """`mixed — see below` was true only because of `tasks/`. Left behind, it
    sends a reader looking for the part that is not permanent.

    Case-folded, and that is not cosmetic: two of the three documents spelled
    it `Mixed` at the head of a table cell. Written case-sensitively this
    assertion passed against the exact text it was meant to refuse — found by
    mutating the cell back and watching the test stay green.
    """
    for parts in (
        ("seal", "README.md"),
        ("skills", "implement", "SKILL.md"),
        ("README.md",),
        ("README.ko.md",),
    ):
        text = read(*parts).lower()
        assert "mixed — see below" not in text, "/".join(parts)
        assert "안에서 갈림" not in text, "/".join(parts)


# --- the status column ------------------------------------------------------


def test_smith_and_the_skill_list_the_same_second_rung_work():
    """Two documents decide the same rung, and only one is always loaded.

    Round 1 found them split: the skill named four kinds of second-rung work
    and `agents/smith.md` named three, so a change touching only tests was
    decidable by one and not the other. The check above pins the CONDITION;
    nothing pinned the examples, which is where they actually drifted.

    Whitespace-normalised because the two wrap at different widths.
    """

    def flat(*parts):
        return " ".join(read(*parts).split())

    skill, smith = flat("skills", "implement", "SKILL.md"), flat("agents", "smith.md")
    for example in (
        "a refactor",
        "a performance pass",
        "a formatting sweep",
        "a test that pins what already holds",
    ):
        assert example in skill, f"the skill lost `{example}`"
        assert example in smith, f"the smith lost `{example}`"

    # The exception that lifts a default, in both. Naming the value is what
    # moves a change up a rung, and a document that dropped the sentence
    # would silently make the four a closed list again.
    for named in ("a timeout", "a retry count", "a rate", "a size cap"):
        assert named in skill, f"the skill lost `{named}`"
        assert named in smith, f"the smith lost `{named}`"


def test_the_plan_template_carries_a_status_column():
    """S7. The column has to be in the shipped template, not only in prose:
    a session bootstraps from the template and never reads the argument."""
    tpl = read("templates", "sdd-plan.md")
    assert "| Phase | Delivers | Verified by | Status |" in tpl
    assert "|---|---|---|---|" in tpl


def test_the_template_says_why_a_tick_is_refused():
    """The column is worth nothing if its closed value can be typed.

    A tick and the word `done` assert a present state nobody can check. A
    commit asserts a past one that someone can open, which is the only reason
    mutable-looking progress is allowed inside the contract at all.
    """
    tpl = read("templates", "sdd-plan.md")
    assert "A tick is refused" in tpl
    assert "the commit that closed the phase" in tpl
    assert "past" in tpl, (
        "the reason a hash is accepted where a tick is not is that it asserts "
        "a past state — without it the rule is arbitrary and gets relaxed"
    )


def test_the_skill_stops_sending_task_lists_somewhere_else():
    """The objection that sent them away was about form, and the answer is
    the Status column. If the old sentence survives beside the new one, a
    session gets two destinations and picks the first it reads."""
    skill = read("skills", "implement", "SKILL.md")
    assert "Phases table is the task list" in skill
    assert "Task lists do not live here" not in skill
    assert "belongs in `.specseal/`" not in skill


def test_the_planner_writes_into_the_plan():
    planner = read("skills", "feature-planner", "SKILL.md")
    assert "plan.md`, as its Phases table" in planner
    assert ".specseal/tasks" not in planner


def test_what_the_status_column_gives_up_is_written_down():
    """A phase row is not a dependency graph, and a document that does not
    say so gets a checker built on it."""
    skill = read("skills", "implement", "SKILL.md")
    assert "does not fit in a phase row" in skill
    planner = read("skills", "feature-planner", "SKILL.md")
    assert "do not survive into the file" in planner


def test_the_cost_of_a_judgment_over_a_count_is_stated():
    """A rule that hides its own cost gets reverted by whoever finds it."""
    skill = read("skills", "implement", "SKILL.md")
    assert "two people can disagree" in skill, (
        "the trade is a judgment for a measurement, and a document that does "
        "not say so reads as though nothing was given up"
    )


def test_the_two_todo_files_sit_where_the_release_guard_looks():
    """A glob is a claim about layout, and nothing checked the layout.

    `.github/scripts/fold_ledger.py` refuses a release while any work item
    has an open row in `evidence-todo.md`, and it finds those files with
    `seal/specs/*/evidence-todo.md`. Two work items kept theirs one
    directory deeper, under `rounds/`, so the guard was blind to two of five
    — silently, because a guard that finds nothing and a guard that looks in
    the wrong place say the same thing (issue #96).

    `docs/review-handoff-protocol.md` puts the two todo files at the work
    item's own level and gives the reason: `round-N` is the only member of
    the set that is plural and unbounded, so it gets a directory and they do
    not.

    This pins the layout the glob assumes rather than the glob, because the
    glob is one line and the layout is written by hand once per work item.
    """
    stray = sorted(
        glob.glob(
            os.path.join(ROOT, "seal", "specs", "*", "*", "**", "tests-todo.md"),
            recursive=True,
        )
        + glob.glob(
            os.path.join(ROOT, "seal", "specs", "*", "*", "**", "evidence-todo.md"),
            recursive=True,
        )
    )
    assert not stray, (
        "a todo file sits below the work item's own directory, where "
        "`fold_ledger.py`'s glob cannot see it: "
        f"{[os.path.relpath(p, ROOT) for p in stray]}. The release guard "
        "reads `seal/specs/*/evidence-todo.md`, one level only"
    )
    at_level = glob.glob(
        os.path.join(ROOT, "seal", "specs", "*", "evidence-todo.md")
    ) + glob.glob(os.path.join(ROOT, "seal", "specs", "*", "tests-todo.md"))
    assert at_level, (
        "no evidence-todo file at the work-item level at all — this case is "
        "blind, and would stay green if every one of them moved"
    )
