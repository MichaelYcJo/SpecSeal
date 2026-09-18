"""A root nobody chose a mode for is a state something names.

Issue #151, reported from a monorepo on its first work item under SpecSeal:
the session created `seal/` and started working. Nothing asked about shared or
local mode, and nothing asked the migration question.

Three files each said something correct and the three together left no route
to the question. `hooks/optin.py` says the root's existence IS the
declaration; `skills/implement/orchestration.md` §Bootstrap says the mode
question is asked there and nowhere else; and the preset block — `templates/claude-md-block.md`,
which `install.sh` copies into `~/.claude/CLAUDE.md`, so it loads in every project
on the machine — tells a session to write `seal/specs/<id>/routing.md` before the
first edit. That write creates `seal/`. Creating `seal/` opts the repository
in. The question lived in a skill the session had no reason to load.

This file pins the half that OBSERVES it. `tests/test_first_setup_asks_once.py`
pins the half that points at it — the preset sentence, and the bootstrap the
sentence sends a session to.

The scenario ids are `seal/specs/1788817289-local-mode-from-first-setup-to-
the-gate/spec.md`'s. Every case was written before `hooks/mode-gate.py` and
`hooks/config.py` existed and seen red — as a collection error, which is a
red this file's own first case makes explicit rather than leaving to a reader
to trust.
"""

import importlib.util
import json
import os
import subprocess

import pytest
from conftest import decision_of, load_hook_module, local_home, run_hook

GATE = "mode-gate.py"


@pytest.fixture
def config():
    return load_hook_module("config.py", "specseal_config_for_tests")


def payload(cmd, repo, session="s1", tool="Bash", **extra):
    p = {
        "tool_name": tool,
        "session_id": session,
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }
    p.update(extra)
    return p


def git_dir(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def opt_in_shared(repo):
    (repo / "seal").mkdir(exist_ok=True)
    return repo / "seal"


def write_config(home, text):
    with open(os.path.join(str(home), "config.md"), "w", encoding="utf-8") as f:
        f.write(text)


TABLE = "# Repository config\n\n| Item | Value |\n|---|---|\n{rows}"


def reason_of(out):
    return json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


# --- the reader: one parser for the Mode row -------------------------------


def test_the_row_is_read_from_the_root_the_folder_is_at(config, repo):
    """The reader answers for whichever root exists, so a local-mode
    repository is not read as one that declared nothing."""
    home = local_home(repo)
    write_config(home, TABLE.format(rows="| Mode | local |\n"))
    assert config.declared_mode(str(home)) == ("mode", "local")


@pytest.mark.parametrize(
    "text, expected",
    [
        (None, ("none", "")),
        (TABLE.format(rows="| Record language | Korean |\n"), ("none", "")),
        (TABLE.format(rows="| Mode |  |\n"), ("none", "")),
        ("not a table at all\n", ("none", "")),
        (TABLE.format(rows="| Mode | SHARED |\n"), ("mode", "shared")),
        (TABLE.format(rows="| Mode | whatever |\n"), ("unknown", "whatever")),
    ],
)
def test_the_four_spellings_of_undeclared_are_one_answer(config, repo, text, expected):
    """The same four `seal.py#declared` already had, because it is the same
    reader — moved, not rewritten. A row that names no mode is told apart from
    no row, because a claim nobody can act on is not the same as no claim."""
    home = opt_in_shared(repo)
    if text is not None:
        write_config(home, text)
    assert config.declared_mode(str(home)) == expected


def test_rows_above_the_header_are_not_rows_of_this_table(config, repo):
    """A mutation survived here, and the branch it broke is the one the
    docstring's whole claim rests on: the header is this table's furniture
    ABOVE its first row. Without it a `| Mode | local |` written into some
    other table earlier in the file — an example, a comparison — is read as
    the declaration.

    Uncovered because it arrived uncovered. The parser moved here from
    `seal.py`, and the suite that looks like its home,
    `tests/test_the_pull_request_language_is_the_repositorys.py`, carries a
    second copy of the loop rather than calling this one."""
    home = opt_in_shared(repo)
    write_config(
        home,
        "# Repository config\n\n"
        "An example of what NOT to write:\n\n"
        "| Mode | local |\n\n"
        "| Item | Value |\n|---|---|\n| Mode | shared |\n",
    )
    assert config.declared_mode(str(home)) == ("mode", "shared")


def test_the_command_and_the_gate_read_one_parser(config):
    """`seal mode` writes the row and the gate reads it. Two readers of one
    table is how a file passes one and fails the other; `seal.py` re-exports
    this one rather than keeping a copy."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(root, "skills", "implement", "scripts", "seal.py")
    spec = importlib.util.spec_from_file_location("specseal_seal_one_parser", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # By where the code was COMPILED, not by object identity: this test loads
    # `hooks/config.py` under a name of its own, so the two module objects
    # differ while the implementation behind them must not.
    owner = os.path.join("hooks", "config.py")
    for name in ("declared", "config_rows", "config_path"):
        where = getattr(module, name).__code__.co_filename
        assert where.endswith(owner), f"seal.{name} is compiled from {where}"
    assert config.declared_mode.__code__.co_filename.endswith(owner)


# --- #415: a cell carries an escaped pipe, and the rows below it survive ----
#
# The scenario ids are `seal/specs/1789598366-a-piped-broad-gate-row-takes-
# every-config-row-below-it/spec.md`'s.
#
# **A row that parses must come FIRST in every fixture here**, and that is
# load-bearing rather than decorative. `config_rows` breaks on a line it
# cannot parse only once it has found a row; a line it cannot parse with
# nothing found yet is stepped past as furniture. So a piped row written as
# the table's FIRST row loses only itself, and the defect this section is
# about — the rows below vanishing — needs a parseable row above it.
# Measured 2026-09-17, both ways round.

PIPED_TABLE = (
    "# Repository config\n\n"
    "| Item | Value |\n|---|---|\n"
    "| Record language | English |\n"
    "| Broad gate | bin/test -q \\| tee out.txt |\n"
    "| Mode | shared |\n"
    "| Commit and pull request language | English |\n"
)


def test_an_escaped_pipe_is_one_row_and_the_rows_below_it_still_arrive(config):
    """A1. `seal/config.md` is markdown and `\\|` is markdown's own answer for
    a pipe inside a cell (`questions.md` Q1, answered by the repository owner
    on 2026-09-17).

    **The count is asserted before the value, and that ordering is the
    case.** A case that checks the `Broad gate` value alone passes just as
    well when every row under it has vanished, and vanishing is the defect:
    `config_rows` stops at the first line that will not parse, so a piped row
    used to take `Mode` and every later row with it, each falling back to a
    default with no message anywhere (#415).
    """
    rows = config.config_rows(PIPED_TABLE)
    assert len(rows) == 4, (
        f"the table has four rows and {len(rows)} came back: {rows}. A row "
        "the reader refuses ends the table, so what is missing here is every "
        "row written BELOW the piped one"
    )
    assert [item for item, _ in rows] == [
        "Record language",
        "Broad gate",
        "Mode",
        "Commit and pull request language",
    ], rows
    assert dict(rows)["Broad gate"] == "bin/test -q | tee out.txt", (
        "the value reaches its caller with one literal pipe, because the "
        "escape is markdown's and is undone before anything else sees it"
    )
    assert dict(rows)["Mode"] == "shared", (
        "the `Mode` row sits below the piped one, which is what `seal mode` "
        "reads before deciding whether to write one"
    )


def test_a_windows_path_survives_the_reader_exactly_as_written(config):
    """The constraint the repository owner attached to Q1's answer, and it
    decides the implementation rather than the choice: the reduction is
    **exactly the two characters `\\|`**, never a general backslash unescape.

    `C:\\Python\\python.exe -m pytest` is the shape a `Broad gate` row takes
    on Windows, and it reads back with its separators intact today — the
    state this repository has already synced across operating systems. A
    blanket `re.sub(r"\\\\(.)", r"\\1", value)` would hand the gate
    `C:Pythonpython.exe -m pytest`, which is a path to nothing.
    """
    text = (
        "| Item | Value |\n|---|---|\n"
        "| Broad gate | C:\\Users\\x\\Python\\python.exe -m pytest |\n"
    )
    assert config.config_rows(text) == [
        ("Broad gate", "C:\\Users\\x\\Python\\python.exe -m pytest")
    ], "a backslash that is not part of `\\|` is the value's own character"


def test_a_backslash_against_a_pipe_is_the_one_shape_the_escape_narrows(config):
    """Round 1's 🟡 2 of #415. The escape is not free in one direction only:
    a backslash immediately before a cell-ending pipe used to be a plain
    character followed by a delimiter, and it is now one escaped pipe — so
    the line has one pipe fewer than it needs and stops being a row.

    **It is kept rather than repaired, and the narrowing is named rather
    than discovered.** Once `\\|` means an escaped pipe those bytes cannot
    also mean *backslash, then the delimiter*; the old reading was only
    available while a backslash meant nothing. Nothing becomes unwritable —
    a space before the closing pipe gives the value back byte for byte,
    because `config_rows` strips the cell — and one line in the whole tree
    reads differently, in a review report quoting this shape.

    Both members of the class are here. The report named the first; the
    second is the same cause at an INTERNAL pipe, where the line stops being
    a row for the same reason.
    """
    header = "| Item | Value |\n|---|---|\n"
    tight_last = "| Broad gate | C:\\Users\\x\\tools\\|\n"
    tight_first = "| C:\\tools\\| x |\n"
    assert config.config_rows(header + tight_last) == [], (
        "a backslash against the closing pipe is markdown's escaped pipe, so "
        "the line has no closing pipe left and is not a row. If this returns "
        "a row the pattern changed and `spec.md` §*What this repair cannot "
        "see* is now wrong"
    )
    assert config.config_rows(header + tight_first) == [], (
        "the same cause at the pipe BETWEEN the cells — the report named only "
        "the closing one"
    )
    assert config.config_rows(header + "| Broad gate | C:\\Users\\x\\tools\\ |\n") == [
        ("Broad gate", "C:\\Users\\x\\tools\\")
    ], (
        "written with a space before the closing pipe the value comes back "
        "exactly as the old pattern read it, so no value lost a spelling"
    )
    assert config.config_rows(header + "| C:\\tools\\ | x |\n") == [
        ("C:\\tools\\", "x")
    ], "and the same for the item cell"


def test_a_three_column_row_still_ends_the_table(config):
    """The escape widens what a cell may hold and must not widen what a ROW
    is. Round 1 🟡 6 of the reader's own history is this line: a greedy last
    cell reads `| a | b | c |` as the row `('a', 'b | c')`, and then the rows
    of a three-column table written under this one are read as more of this
    one. `templates/config.md` ships three-column tables."""
    text = "| Item | Value |\n|---|---|\n| a | b |\n| x | y | z |\n| c | d |\n"
    assert config.config_rows(text) == [("a", "b")], (
        "the three-cell line is a row of somebody else's table and ends this one"
    )


def test_seal_mode_writes_one_row_where_the_mode_row_sits_below_a_piped_row(
    config, tmp_path
):
    """A3, and `questions.md` M1 — **executed 2026-09-17, and it duplicated.**

    The reader and the writer read one table, so when the reader stopped
    above the `Mode` row the writer stopped there too: `declared_mode`
    answered *none*, `table_span` returned no `Mode` row, and `with_row`
    inserted a second one ABOVE the piped line while the person's own row sat
    below it. Measured on the tree before this change — two `| Mode |` rows in
    a person's file, which `table_span`'s own comment says no command can
    bring back into agreement. It is the worst outcome in this work item and
    the strongest argument for teaching the reader the escape.

    This calls `write_row`, which is the unit `seal mode` calls when the row
    reads as undeclared (`seal.py#mode`), rather than a helper beside it.

    **Nothing is asserted before the write.** What the reader answered is
    read into the failure message instead, because a guard that fires first
    takes the case's own subject — the file two rows deep — off the screen.
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(root, "skills", "implement", "scripts", "seal.py")
    spec = importlib.util.spec_from_file_location("specseal_seal_for_415", path)
    seal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(seal)

    home = tmp_path / "seal"
    home.mkdir()
    write_config(home, PIPED_TABLE)
    read_as = seal.declared(str(home))
    refused = seal.write_row(str(home), "shared")
    written = (home / "config.md").read_text(encoding="utf-8")
    assert written.count("| Mode |") == 1, (
        f"the person's file is {written.count('| Mode |')} `Mode` rows deep, "
        f"and no command brings it back into agreement. The reader answered "
        f"{read_as} for a file whose own row says `shared`:\n{written}"
    )
    assert refused == "", refused
    assert read_as == ("mode", "shared"), (
        "the writer stopped where the reader stopped, which is the agreement "
        "the two keep by reading one parser"
    )


BARE_TABLE = PIPED_TABLE.replace("\\|", "|")


def test_seal_mode_still_writes_a_second_mode_row_for_a_bare_pipe(config, tmp_path):
    """Round 1's 🟡 4 of #415 — the limitation, pinned rather than described.

    Phase 1 closed the duplication for the ESCAPED spelling. Written bare the
    line is still not a row, so the reader still stops above the person's
    `Mode` row, the writer stops where the reader stops, and the file comes
    back two rows deep. Three records read as if the whole thing were closed;
    they say this now, and this case is what keeps the sentence and the tree
    in step — the day the bare spelling is closed, this goes red and the
    records are found by whoever makes it go red.

    **And nothing repairs a file already two rows deep.** The second write
    below sets the FIRST row and leaves the person's own, so the file states
    two modes and every reader takes the first. `table_span`'s own comment
    says no command brings such a file back into agreement; this asserts it
    rather than trusting the comment.
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(root, "skills", "implement", "scripts", "seal.py")
    spec = importlib.util.spec_from_file_location("specseal_seal_for_415_bare", path)
    seal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(seal)

    home = tmp_path / "seal"
    home.mkdir()
    write_config(home, BARE_TABLE)
    assert config.declared_mode(str(home)) == ("none", ""), (
        "the bare pipe is expected to hide the `Mode` row below it; if this "
        "row now reads, the limitation is gone and these four records are "
        "what has to change with this case — the work item's `changelog.md` "
        "bullet saying it is closed for the escaped spelling only, its "
        "`overview.md` §*Not done*, its `spec.md` §*What this repair cannot "
        "see*, and `templates/config.md`. A limitation case's whole value is "
        "the list it hands whoever reddens it, so all four are named here "
        "rather than one and a pointer at the rest"
    )
    assert seal.write_row(str(home), "shared") == ""
    written = (home / "config.md").read_text(encoding="utf-8")
    assert written.count("| Mode |") == 2, (
        f"the bare spelling no longer duplicates:\n{written}"
    )

    assert seal.write_row(str(home), "local") == ""
    again = (home / "config.md").read_text(encoding="utf-8")
    assert again.count("| Mode |") == 2, (
        f"a second run changed how many rows the file has:\n{again}"
    )
    assert [value for item, value in config.config_rows(again) if item == "Mode"] == [
        "local"
    ], "the reader takes the first row, which is the one the writer just set"
    assert "| Mode | shared |" in again, (
        "the person's own row below the bare pipe is still there saying "
        "something else — a file two rows deep is repaired by nothing, and "
        "`overview.md` §*Not done* is where that is recorded"
    )


def test_a_line_that_will_not_parse_is_named_and_the_hook_still_says_nothing(
    config, repo
):
    """A4 and A7 of #415, which are one case because they are one decision.

    `refused_row` reports; it refuses nothing and raises nothing. The caller
    that consults it is `broad-gate`, which already talks to a person.
    `hooks/mode-gate.py` deliberately does not: it is a `PreToolUse` hook, so
    a wrong refusal there stops a session with nobody able to get past it.
    A config whose `Mode` row is hidden below an unparseable line still reads
    as undeclared and the gate still simply asks the mode question again —
    the stated cost of keeping that hook silent (`spec.md` §*What this repair
    cannot see*).
    """
    text = (
        "| Item | Value |\n|---|---|\n"
        "| Record language | English |\n"
        "| Broad gate | bin/test -q | tee out.txt |\n"
        "| Mode | shared |\n"
    )
    assert config.refused_row(text) == "| Broad gate | bin/test -q | tee out.txt |"
    assert config.refused_row(TABLE.format(rows="| Mode | shared |\n")) is None
    assert config.refused_row("# no table here\n\nprose.\n") is None
    assert (
        config.refused_row("| Item | Value |\n|---|---|\n| a | b |\n\nprose.\n") is None
    ), "a blank line is the table ending, not a row somebody wrote"

    gate = load_hook_module(GATE, "specseal_mode_gate_for_415")
    home = opt_in_shared(repo)
    write_config(home, text)
    answer = gate.undeclared(str(repo))
    assert answer == str(home), (
        'the hook\'s answer is the home or `""` and never a message; the '
        f"row below the unparseable line is invisible to it, as before: {answer!r}"
    )


# --- #429: a table inside a code fence is not this repository's answer ------
#
# The scenario ids are `seal/specs/1789721571-the-gate-reads-an-example-and-
# names-rows-nobody-wrote/spec.md`'s. Three walks read this table and the
# fence rule is one rule in front of all three: `config_rows`'s walk and
# `refusal`'s walk here, and `seal.py#table_span`'s — the writer's — below.

FENCED_ABOVE = (
    "# Repository config\n\n"
    "An example of the format, copied out of `templates/config.md`:\n\n"
    "```markdown\n"
    "| Item | Value |\n"
    "|---|---|\n"
    "| Mode | local |\n"
    "| Broad gate | EXAMPLE |\n"
    "```\n\n"
    "| Item | Value |\n"
    "|---|---|\n"
    "| Mode | shared |\n"
    "| Broad gate | bin/test -q |\n"
)

# The same shape with nothing parsed above the fence: the live table's only
# line will not parse, so both walks step past it and read on — and before
# the fence rule the example below supplied the rows.
FENCED_BELOW_A_TABLE_THAT_NEVER_BEGAN = (
    "| Item | Value |\n"
    "|---|---|\n"
    "| Broad gate | bin/test -q | tee out.txt |\n"
    "```markdown\n"
    "| Mode | local |\n"
    "| Broad gate | EXAMPLE |\n"
    "```\n"
)

# A fenced line that will not parse, standing ABOVE the first live row, which
# is where `refusal`'s walk reaches it: it reads on past prose until a row is
# found, so before the fence rule it handed `broad-gate` a line out of an
# example block to quote back at a person as their own malformed row.
FENCED_REFUSAL = (
    "| Item | Value |\n"
    "|---|---|\n"
    "```markdown\n"
    "| Broad gate | bin/test -q | tee out.txt |\n"
    "```\n"
    "| Mode | shared |\n"
)


def crlf(text):
    return text.replace("\n", "\r\n")


def test_a_fenced_table_above_the_live_one_is_not_the_table(config, tmp_path):
    """A1. The live table is the first one outside every fence.

    `config_rows` starts at the first `| Item | Value |` header and never
    looks for another, so an example pasted above the live table WAS the
    table every gate got: the mode, the broad command, every row. The shape
    is invited rather than contrived — `config.md`'s own header comment
    points at `templates/config.md`, and `skills/config/SKILL.md` step 3
    tells a session to copy a block of that template, fenced example row
    included, naming no position for it.
    """
    assert config.config_rows(FENCED_ABOVE) == [
        ("Mode", "shared"),
        ("Broad gate", "bin/test -q"),
    ], config.config_rows(FENCED_ABOVE)
    assert "EXAMPLE" not in [value for _item, value in config.config_rows(FENCED_ABOVE)]
    home = tmp_path / "seal"
    home.mkdir()
    write_config(home, FENCED_ABOVE)
    assert config.declared_mode(str(home)) == ("mode", "shared"), (
        "the mode the gate reads is the example's, not the repository's"
    )


def test_a_fenced_example_below_a_table_that_never_began_is_still_not_the_table(
    config,
):
    """A2. Both walks step past a line they cannot parse until a row is
    found, so with nothing parsed above it a fenced example's rows became the
    live rows — the same defect one shape over, and the one a repair aimed at
    the fenced HEADER alone would have left standing."""
    rows = config.config_rows(FENCED_BELOW_A_TABLE_THAT_NEVER_BEGAN)
    assert rows == [], (
        f"the example inside the fence supplied this repository's rows:\n{rows}"
    )


def test_a_fenced_pipe_line_is_not_a_line_somebody_wrote_as_a_row(config):
    """A3. `refusal`'s walk, which is the one that reads ON past the stopping
    line, treated any line beginning with a pipe as a line somebody wrote as
    a row — so a line inside an example block came back as `refused`, and
    `broad-gate` quotes a refused line back at the person as their own.

    All three fields, because the walk fills three: the fenced line is in
    neither `refused` nor `below`, and it is not what stopped the reader.
    """
    refused, below, stopper = config.refusal(FENCED_REFUSAL)
    assert refused == [], (
        f"a line inside a code fence came back as a refused row:\n{refused}"
    )
    assert below == [], below
    assert stopper is None, f"a fenced line stopped the reader:\n{stopper}"
    assert config.config_rows(FENCED_REFUSAL) == [("Mode", "shared")], (
        "the row outside the fence is what this table holds"
    )


def test_the_writer_and_the_reader_agree_about_which_row_is_the_row(tmp_path):
    """A4. `seal.py#table_span` is the third walk and it is the WRITER: it
    locates the line `with_row` overwrites. Repair the reader alone and
    `seal mode shared` rewrites the `Mode` row inside somebody's pasted
    example while every gate reads the live one — the file two rows deep that
    `table_span`'s own comment says no command can bring into agreement.

    Asserted on the BYTES, not on the reader's answer: what makes this case
    the writer's is that the fenced line comes back byte-identical and
    exactly one line of the file changed.
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(root, "skills", "implement", "scripts", "seal.py")
    spec = importlib.util.spec_from_file_location("specseal_seal_for_429", path)
    seal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(seal)

    before = FENCED_ABOVE.replace("| Mode | shared |", "| Mode | local |")
    home = tmp_path / "seal"
    home.mkdir()
    write_config(home, before)
    assert seal.write_row(str(home), "shared") == ""
    after = (home / "config.md").read_text(encoding="utf-8")

    assert "| Mode | local |\n| Broad gate | EXAMPLE |\n```" in after, (
        f"the writer rewrote the row inside the example block:\n{after}"
    )
    changed = [
        (i, was, now)
        # `strict=True`: a write that INSERTED a row leaves the two files
        # different lengths, and a silent truncation here would hide exactly
        # the outcome this case is about.
        for i, (was, now) in enumerate(
            zip(before.splitlines(), after.splitlines(), strict=True)
        )
        if was != now
    ]
    assert len(changed) == 1, f"the write touched {len(changed)} lines:\n{changed}"
    assert changed[0][2] == "| Mode | shared |", changed
    assert changed[0][0] > after.splitlines().index("```"), (
        "the line that changed is inside the fence, not in the live table"
    )


def test_the_fence_rule_answers_the_same_for_a_crlf_file(config, tmp_path):
    """A7. `config_rows` and `refusal` walk `splitlines()` while
    `table_span` walks `splitlines(keepends=True)` and rstrips each line, so
    the shared rule is the one place the two spellings have to meet. Round 3
    of #415 measured CRLF for the existing walks; this is the same
    measurement for the answers this work item adds."""
    assert config.config_rows(crlf(FENCED_ABOVE)) == config.config_rows(FENCED_ABOVE)
    assert config.config_rows(crlf(FENCED_BELOW_A_TABLE_THAT_NEVER_BEGAN)) == []
    assert config.refusal(crlf(FENCED_REFUSAL)) == ([], [], None)

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(root, "skills", "implement", "scripts", "seal.py")
    spec = importlib.util.spec_from_file_location("specseal_seal_for_429_crlf", path)
    seal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(seal)
    written = seal.with_row(crlf(FENCED_ABOVE), "local")
    assert "| Mode | local |\r\n| Broad gate | EXAMPLE |\r\n```" in written, (
        f"the writer rewrote the fenced row of a CRLF file:\n{written!r}"
    )
    assert written.count("\n") == written.count("\r\n"), (
        f"the write left a file in two endings:\n{written!r}"
    )


def test_what_counts_as_a_fence_is_commonmarks_rule_as_far_as_it_goes(config):
    """Q3 of `questions.md`, decided and pinned. `spec.md` §*Data &
    interfaces* fixes the rule for the shapes that matter; the residue is
    CommonMark's own edge cases, resolved toward *not a fence* wherever the
    specification leaves room, because that is the direction that keeps a
    live table readable.

    Each assertion below is one decision:

      - four spaces of indentation is an indented code block, never a fence,
        so the table under it is still read;
      - a BACKTICK fence's info string may not hold a backtick (CommonMark
        4.5), so that line opens nothing;
      - a closing run may be longer than the one that opened the block;
      - a run of the OTHER character does not close a block, and neither
        does a run carrying an info string;
      - an unclosed fence runs to the end of the file, which lands on
        *nothing is declared* — the direction `hooks/config.py` already
        fails in.
    """
    live = "| Item | Value |\n|---|---|\n| Mode | shared |\n"
    assert config.config_rows("    ```\n" + live) == [("Mode", "shared")], (
        "four spaces is an indented code block and not a fence"
    )
    assert config.config_rows("```` `x` ````\n" + live) == [("Mode", "shared")], (
        "a backtick fence's info string may not hold a backtick, so this "
        "line opens no fence"
    )
    assert config.config_rows(
        "```\n| Item | Value |\n|---|---|\n| Mode | local |\n``````\n" + live
    ) == [("Mode", "shared")], (
        "a closing run longer than the opening one closes the block"
    )
    assert config.config_rows(
        "```\n~~~\n| Item | Value |\n|---|---|\n| Mode | local |\n```\n" + live
    ) == [("Mode", "shared")], "a tilde run does not close a backtick fence"
    assert config.config_rows(
        "````\n```\n| Item | Value |\n|---|---|\n| Mode | local |\n````\n" + live
    ) == [("Mode", "shared")], (
        "a run SHORTER than the opening one does not close the block — this "
        "repository's own records wrap a fenced example in four backticks, "
        "and a rule that knew three only would read the inner fence as the "
        "outer one's close and leave the live table inside a fence"
    )
    assert config.config_rows("```\n```markdown\n" + live) == [], (
        "a run carrying an info string does not close a block, so this file "
        "declares nothing"
    )
    assert config.config_rows("~~~\n" + live) == [], (
        "an unclosed fence runs to the end of the file"
    )
    assert config.config_rows("~~~info ~ string\n" + live + "~~~~\n") == [], (
        "a tilde fence's info string is unrestricted, which is CommonMark's "
        "rule and not an exception to this one"
    )


# --- S7-S10: the gate ------------------------------------------------------


def test_a_root_with_no_recorded_mode_is_named(repo):
    """S7. The state #151 is about: a root exists and nobody was asked."""
    opt_in_shared(repo)
    out = run_hook(GATE, payload("git commit -m x", repo))
    assert decision_of(out) == "deny"
    said = reason_of(out)
    assert "AskUserQuestion" in said
    assert "seal mode" in said
    assert "seal mode local" in said and "seal mode shared" in said


def test_the_prompt_says_what_each_answer_costs(repo):
    """Every answer has to continue (`implement` §1). Both do something and
    the prompt says which — one records where the folder already is, the other
    moves it."""
    opt_in_shared(repo)
    said = reason_of(run_hook(GATE, payload("git commit -m x", repo)))
    assert "committed" in said
    assert str(repo / "seal") in said


def test_a_recorded_mode_is_silent(repo):
    """S8. The row is the answer, so the question stops."""
    write_config(opt_in_shared(repo), TABLE.format(rows="| Mode | shared |\n"))
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "silent"


def test_a_local_root_with_a_recorded_mode_is_silent(repo):
    """The same, read at the other place. A gate that only looked at
    `<repo>/seal/` would nag every local-mode repository forever."""
    write_config(local_home(repo), TABLE.format(rows="| Mode | local |\n"))
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "silent"


def test_a_repository_with_no_root_is_silent(repo):
    """S9. A globally installed plugin must not nag a repository that never
    opted in — the rule `hooks/optin.py` exists to hold."""
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "silent"


def test_the_question_arrives_on_the_first_command_not_at_the_commit(repo):
    """The budget decided this, not the act #151 names. Scoping the gate to a
    commit puts the question beside the review arm's, at minute thirty, on a
    session that may have nobody at the keyboard — and `implement` §1 says the
    cost of a question is when it arrives. The count is the same either way,
    because the budget below is per session rather than per command."""
    opt_in_shared(repo)
    assert decision_of(run_hook(GATE, payload("ls -la", repo))) == "deny"


def test_the_second_attempt_in_a_session_only_asks(repo):
    """S10. A deny that repeats is an outage: nothing in an unattended run can
    get past it. The budget is one deny per session per repository, and `ask`
    is approvable."""
    opt_in_shared(repo)
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "deny"
    out = run_hook(GATE, payload("git commit -m x", repo))
    assert decision_of(out) == "ask"
    assert "seal mode" in reason_of(out)


def test_the_third_command_of_a_session_is_silent(repo):
    """The budget is TWO prompts, and the ask is spent like the deny.

    Round 1 measured what an ask that stands for the rest of the session
    costs on a gate that fires per command rather than per commit: one deny
    and NINE asks over ten ordinary calls, where the sibling gate was silent
    on nine of the same ten. And the way out, `seal mode`, is itself a Bash
    call — so a run with nobody at the keyboard could not reach the command
    that ends the asking, and every command it tried was stopped rather than
    one. That is the outage the module docstring says this cannot become.
    """
    opt_in_shared(repo)
    seen = [decision_of(run_hook(GATE, payload("ls", repo))) for _ in range(6)]
    assert seen == ["deny", "ask", "silent", "silent", "silent", "silent"], seen


def test_the_two_prompts_are_counted_apart(repo):
    """One marker each, so spending the deny does not spend the ask.

    Sharing a directory would collapse the budget to a single prompt and lose
    the approvable retry the deny's own reason tells the model to make.
    """
    gate = load_hook_module(GATE, "specseal_mode_gate_markers")
    assert gate.CHOICE_DIR != gate.RETRY_DIR
    opt_in_shared(repo)
    run_hook(GATE, payload("ls", repo))
    marker = os.path.join(git_dir(repo), gate.CHOICE_DIR, "s1")
    assert os.path.isfile(marker)
    assert not os.path.exists(os.path.join(git_dir(repo), gate.RETRY_DIR, "s1"))


@pytest.mark.parametrize("shape", ["directory", "undecodable", "unreadable"])
def test_a_config_nobody_can_open_is_silence_not_a_deny(repo, shape):
    """`hooks/optin.py`'s rule, which this module's docstring adopts: a
    repository this cannot read is one it says nothing about.

    `hooks/config.py#declared_mode` folds *will not open* into *declared
    nothing*, and that is right for the WRITER — `seal mode` goes on to write
    the row either way. For a gate the two are different states, and treating
    them alike denied a repository whose answer might already be there.

    Reachable, not exotic: `hooks/optin.py#repo_root` already records a
    repository under a path a cp949 console cannot decode, and a row
    hand-edited in a non-UTF-8 locale puts those bytes here. The escape would
    have been `seal mode`, writing a row into the file nothing can parse.
    """
    home = opt_in_shared(repo)
    path = os.path.join(str(home), "config.md")
    if shape == "directory":
        os.mkdir(path)
    elif shape == "undecodable":
        with open(path, "wb") as f:
            f.write(b"| Item | Value |\n|---|---|\n| Mode | \xff\xfe shared |\n")
    else:
        write_config(home, TABLE.format(rows="| Mode | shared |\n"))
        os.chmod(path, 0o000)
    try:
        assert decision_of(run_hook(GATE, payload("ls", repo))) == "silent"
    finally:
        if shape == "unreadable":
            os.chmod(path, 0o600)


def test_one_local_root_is_one_question_for_the_whole_clone(repo, tmp_path):
    """`README.md`'s gate row says once per session per repository, and in
    local mode one folder under the common git directory IS the repository —
    `undeclared()` reads that same root from every work tree.

    Keying the marker to `--absolute-git-dir` keyed it to the TREE, so one
    session was denied once per worktree about one folder. Measured 2026-09-08
    before the fix: main tree deny, linked worktree deny, the same folder both
    times.
    """
    local_home(repo)
    side = tmp_path / "side"
    subprocess.run(
        ["git", "-C", str(repo), "worktree", "add", "-q", "-b", "side", str(side)],
        check=True,
        capture_output=True,
    )
    assert decision_of(run_hook(GATE, payload("ls", repo))) == "deny"
    assert decision_of(run_hook(GATE, payload("ls", side))) == "ask"
    assert decision_of(run_hook(GATE, payload("ls", side))) == "silent"


def test_a_shared_root_is_still_a_question_per_work_tree(repo, tmp_path):
    """The half that must NOT move with it. Each work tree carries its own
    `<repo>/seal/`, so each is a separate root nobody chose a mode for and
    each deserves its own question. A marker keyed to the clone for both modes
    would answer for a root the session has never seen."""
    opt_in_shared(repo)
    side = tmp_path / "side"
    subprocess.run(
        ["git", "-C", str(repo), "worktree", "add", "-q", "-b", "side", str(side)],
        check=True,
        capture_output=True,
    )
    (side / "seal").mkdir()
    assert decision_of(run_hook(GATE, payload("ls", repo))) == "deny"
    assert decision_of(run_hook(GATE, payload("ls", side))) == "deny"


def test_the_marker_directory_is_absolute_for_either_question(repo):
    """`git_dir_of` promises an absolute path and `already_asked` joins
    nothing onto it, so the promise is the whole of what places the marker.

    It is not git's promise. `--absolute-git-dir` is absolute; measured
    2026-09-08, `--git-common-dir` answers `.git` from a main work tree and an
    absolute path from a linked one. A relative answer passed through would
    put the marker under whatever directory the hook process happened to start
    in — a different file each time, which is a question asked again.
    """
    gate = load_hook_module(GATE, "specseal_mode_gate_absolute")
    for which in ("--absolute-git-dir", "--git-common-dir"):
        answer = gate.git_dir_of(str(repo), which)
        assert os.path.isabs(answer), f"{which} answered {answer!r}"
        assert os.path.isdir(answer)


def test_a_different_session_is_asked_too(repo):
    """The budget is per session, like the answer it spends. A session that
    never saw the question has not been asked it."""
    opt_in_shared(repo)
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "deny"
    assert (
        decision_of(run_hook(GATE, payload("git commit -m x", repo, session="s2")))
        == "deny"
    )


def test_an_unwritable_marker_counts_as_already_asked(repo):
    """The rule the chain spec states, and the direction matters: inverted,
    the deny repeats forever in exactly the environments that cannot write."""
    opt_in_shared(repo)
    with open(
        os.path.join(git_dir(repo), "specseal-mode-choice"), "w", encoding="utf-8"
    ) as f:
        f.write("not a directory")
    assert decision_of(run_hook(GATE, payload("git commit -m x", repo))) == "ask"


def test_a_session_id_with_separators_stays_inside_the_git_dir(repo):
    """The id names a file. Measured on a sibling guard: `../../escaped` put
    an empty file at the repository root."""
    opt_in_shared(repo)
    run_hook(GATE, payload("git commit -m x", repo, session="../../escaped"))
    assert not (repo / "escaped").exists()


def test_the_subject_is_the_session_s_repository(repo, tmp_path):
    """`git -C <elsewhere>` moves git and does not move the session. Its
    sibling gate resolves the repository a COMMIT lands in, because a verdict
    about a change has to be about the repository that change reaches. This is
    not a verdict about a change: it is a fact about the workspace the session
    is sitting in, and that workspace is the one with the unrecorded root."""
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "-C", str(other), "init", "-q"], check=True)
    opt_in_shared(repo)
    out = run_hook(GATE, payload(f"git -C {other} commit -m x", repo))
    assert decision_of(out) == "deny", out
    assert str(repo) in reason_of(out)


def test_a_session_in_a_subdirectory_is_still_asked(repo):
    """A mutation survived here too, and it is the ordinary case: sessions sit
    in `src/` as often as at the top. Taking `cwd` for the repository root
    makes the gate look for `<cwd>/seal/`, find nothing, and go quiet for
    every session that is not at the top — silence that reads exactly like a
    repository with the row already written."""
    opt_in_shared(repo)
    sub = repo / "src"
    sub.mkdir()
    out = run_hook(GATE, payload("ls", sub))
    assert decision_of(out) == "deny", out
    said = reason_of(out)
    assert str(repo / "seal") in said
    assert str(sub) not in said, "the prompt names the subdirectory as the root"


def test_a_repository_that_is_not_this_one_is_not_judged(repo, tmp_path):
    """The other half of the same rule: a session sitting OUTSIDE an opted-in
    repository hears nothing about it, whatever its commands mention."""
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "-C", str(other), "init", "-q"], check=True)
    opt_in_shared(repo)
    assert (
        decision_of(run_hook(GATE, payload(f"git -C {repo} commit -m x", other)))
        == "silent"
    )


def test_the_gate_is_in_the_pre_bash_group():
    """A gate `hooks/hooks.json` never reaches decides nothing. The dispatch
    group is the wiring, and it is the half a passing gate cannot report on."""
    dispatch = load_hook_module("dispatch.py", "specseal_dispatch_for_mode_gate")
    assert GATE in dispatch.GROUPS["pre-bash"]
