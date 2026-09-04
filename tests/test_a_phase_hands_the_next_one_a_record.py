"""A build phase had no committed record, and what it discovered reached the
next phase only if the orchestrator retyped it into the next spawn prompt.

Issue #107 is the worked failure: phase 4 of an earlier work item moved a
rule out of `agents/smith.md` into an interim home, and phase 5 removed that
interim home before the rule had actually reached anywhere else — the rule
left the repository with nothing recording that it had gone missing. #121
is the broader version: a phase's discoveries have no durable home at all,
so they live only in a transcript the next phase's session never opens.

`templates/sdd-phase.md` gives the build side the same committed,
per-segment record the review chain already has in `templates/sdd-round.md`
(`docs/review-handoff-protocol.md` §Files). This module pins:

  the field table    `Phase`, `Commit` — nothing more, because a phase has
                     no `Target SHA` to squash away and no `Pass` checkbox
                     to answer
  the three sections  ship outside HTML comments, as placeholders rather
                     than filled claims — a template whose only mention of
                     a section is commented out ships a record that is
                     missing it the moment someone copies the file
  the removal table   a real table (`Removed item` / `Where it must land`),
                     with `none` offered as a valid row, because most
                     phases remove nothing and a blank table must not read
                     the same as `none` does
  the measured story  each section's own comment names the failure it
                     answers, so the template does not ship a blank nobody
                     can trace back to a reason
  the plan's pointer  `templates/sdd-plan.md` names the path a phase record
                     lives at, so a session reading the plan can find the
                     template without guessing

The placeholder check mirrors
`test_the_fixes_name_their_surface.py::test_the_template_rows_are_rows_a_session_can_copy`,
reading through the same `strip_comments` `chain_check.py` itself loads —
counted outside comments, because a row whose only mention is commented out
is absent to any reader that strips comments first, template included.
"""

import importlib.util
import os

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHASE_TEMPLATE = os.path.join(ROOT, "templates", "sdd-phase.md")
PLAN_TEMPLATE = os.path.join(ROOT, "templates", "sdd-plan.md")
SMITH_AGENT = os.path.join(ROOT, "agents", "smith.md")
IMPLEMENT_SKILL = os.path.join(ROOT, "skills", "implement", "SKILL.md")

SECTIONS = (
    "## What this phase was asked",
    "## What this phase found",
    "## What this phase removes",
)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def reader_module():
    """`unverified_check.py`'s `strip_comments` — the same reader
    `chain_check.py` loads for `rounds/round-N.md`. A second implementation
    here would be free to drift from what actually reads these records."""
    spec = importlib.util.spec_from_file_location(
        "specseal_phase_reader_for_tests",
        os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py"),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stripped_lines():
    return reader_module().strip_comments(read(PHASE_TEMPLATE).splitlines())


def section_body(lines, heading):
    """The non-blank lines between `heading` and the next `## ` heading (or
    end of file), from lines already run through `strip_comments`."""
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    assert start is not None, f"heading not found outside comments: {heading}"
    body = []
    for line in lines[start:]:
        if line.strip().startswith("## "):
            break
        if line.strip():
            body.append(line)
    return body


# --- the field table ---------------------------------------------------------


def test_the_field_table_is_phase_commit_and_what_ran_it():
    lines = stripped_lines()
    header_idx = next(
        (i for i, line in enumerate(lines) if line.strip().startswith("| Field")), None
    )
    assert header_idx is not None, "no `| Field | Value |` header outside comments"
    # The field table ends at the first `## ` heading — rows past it belong
    # to the removal table further down, not to this one.
    end = next(
        (
            i
            for i in range(header_idx + 1, len(lines))
            if lines[i].strip().startswith("## ")
        ),
        len(lines),
    )
    table_lines = lines[header_idx + 1 : end]
    rows = [line.strip() for line in table_lines if line.strip().startswith("|")]
    field_rows = [
        line for line in rows if not set(line.replace("|", "").strip()) <= {"-"}
    ]
    names = [line.split("|")[1].strip() for line in field_rows]
    assert names == ["Phase", "Commit", "Ran by"], (
        f"the field table carries {names}, not Phase/Commit/Ran by — a phase "
        "has no Target SHA to squash away and no Pass checkbox to answer, and "
        "#137 is why the third row is there: every segment measured before it "
        "landed is one nothing can attribute afterwards"
    )
    for name, row in zip(names, field_rows, strict=True):
        value = row.split("|")[2].strip()
        assert value.startswith("<") and value.endswith(">"), (
            f"a template must not ship a claim, and `{value}` is one ({name})"
        )


def test_the_ran_by_row_offers_both_halves_and_the_unknown_answer():
    """#137. A row naming one of the two is a row that answers neither
    question the flow log has.

    An agent without a model cannot be compared against another run of the
    same agent, and a model without an agent cannot be told from the
    orchestrator's own turns — which is the whole of what #145 is about. So
    the placeholder has to teach BOTH halves, and it has to teach the
    `unknown` answer too: `agents/*.md` pins no model, so a session spawning
    through another harness may genuinely have no name for one, and a
    placeholder offering only the confident answer is what makes the honest
    one look like a failure to fill the row in.
    """
    lines = stripped_lines()
    rows = [line for line in lines if line.strip().startswith("| Ran by")]
    assert len(rows) == 1, f"{len(rows)} `Ran by` rows outside comments"
    value = rows[0].split("|")[2].strip()
    for needle in ("agent on model", "unknown — <why>"):
        assert needle in value, (
            f"the `Ran by` placeholder offers no `{needle}` — it reads "
            f"`{value}`, and a record written from THIS row is refused by "
            "`chain_check.py`"
        )


def test_the_ran_by_row_says_who_fills_it():
    """The row is the SPAWNING session's, and the template is the only place
    a phase record's author reads that.

    An agent is told what it is, so a value the agent writes about itself is
    the value it was told; and the model is a spawn-time argument the
    orchestrator chose. A template that shows the row without saying whose it
    is gets it filled by the subject — which is the one filler whose answer
    cannot be checked against anything.
    """
    raw = read(PHASE_TEMPLATE)
    assert "#137" in raw, (
        "no `#137` anywhere in the template — the row answers that issue's "
        "finding that a measured segment cannot be attributed afterwards"
    )
    flat = " ".join(raw.split())
    assert "never the segment itself" in flat, (
        "the template does not say the row is the spawning session's, so the "
        "one filler whose answer nothing can check is the one it invites"
    )


# --- the three sections exist and ship placeholders, not claims -------------


def test_all_three_sections_exist_outside_comments():
    lines = stripped_lines()
    present = {line.strip() for line in lines}
    for heading in SECTIONS:
        assert heading in present, (
            f"`{heading}` is missing outside HTML comments — a heading only "
            "a comment carries is a heading a copied file does not have"
        )


def test_asked_and_found_sections_ship_a_placeholder():
    lines = stripped_lines()
    for heading in ("## What this phase was asked", "## What this phase found"):
        body = section_body(lines, heading)
        assert body, f"`{heading}` has no content outside comments"
        text = " ".join(line.strip() for line in body)
        assert text.startswith("<") and text.endswith(">"), (
            f"`{heading}` ships `{text}` — a template must offer a "
            "placeholder, not a filled-in claim"
        )


def test_removes_section_is_a_table_with_a_none_row():
    lines = stripped_lines()
    body = section_body(lines, "## What this phase removes")
    rows = [line.strip() for line in body if line.strip().startswith("|")]
    header = next((r for r in rows if "Removed item" in r), None)
    assert header is not None, (
        "`## What this phase removes` has no `Removed item` column — "
        "the removal table must be a real table, not prose"
    )
    assert "Where it must land" in header
    data_rows = [
        r for r in rows if r != header and not set(r.replace("|", "").strip()) <= {"-"}
    ]
    assert len(data_rows) == 1, f"expected one placeholder row, found {data_rows}"
    cells = [c.strip() for c in data_rows[0].strip("|").split("|")]
    assert len(cells) == 2, cells
    for cell in cells:
        assert cell.startswith("<") and cell.endswith(">"), (
            f"a template must not ship a claim, and `{cell}` is one"
        )
    assert "`none`" in cells[0] or "none" in cells[0], (
        "the removed-item cell must offer `none` — most phases remove nothing"
    )


# --- each section's comment names the measured failure it answers -----------


def test_each_section_comment_names_its_measured_failure():
    raw = read(PHASE_TEMPLATE)
    # Comments are read from the RAW file (not stripped) — this is checking
    # the comments exist and say what they must, not that they are absent.
    assert "#119" in raw, (
        "no `#119` anywhere in the template — the asked/found split answers "
        "that issue's finding that neither record said what it was told to do"
    )
    assert "#107" in raw and "#121" in raw, (
        "no `#107`/`#121` — the found/removes sections answer the dropped-"
        "rule failure those issues measured"
    )
    # The removal table's comment specifically must carry the worked #107
    # story (plan.md: "the #107 dropped-rule story for the removal table
    # specifically"), not just the bare issue number.
    removes_idx = raw.index("## What this phase removes")
    tail = raw[removes_idx:]
    assert "agents/smith.md" in tail, (
        "the removal table's comment must carry the #107 worked example "
        "(a rule moved out of agents/smith.md and lost between phases), "
        "not just cite the issue number"
    )
    assert "went missing" in tail or "nothing recording" in tail


# --- the plan points at the path ---------------------------------------------


def test_plan_names_the_phase_record_path():
    plan = read(PLAN_TEMPLATE)
    assert "phases/phase-N.md" in plan, (
        "templates/sdd-plan.md does not name `phases/phase-N.md` — a "
        "session reading the plan has no way to find the phase-record path"
    )
    assert "templates/sdd-phase.md" in plan, (
        "templates/sdd-plan.md does not name the template a phase record starts from"
    )


# --- phase 2: smith is told to write the record, and where ------------------
#
# Phase 1 built the template with nothing pointing a spawned smith at it
# except `plan.md`'s own pointer sentence — which a session reads only if it
# opens `plan.md` at all. `agents/smith.md` phase 3 ("Implement") is read by
# every spawn regardless, so the instruction to write `phases/phase-N.md` at
# each phase's close belongs there, not only in the plan template.


def test_smith_is_told_to_write_the_phase_record():
    smith = read(SMITH_AGENT)
    assert "phases/phase-N.md" in smith, (
        "agents/smith.md does not name `phases/phase-N.md` — a spawned "
        "smith has no instruction pointing it at the file to write"
    )
    assert "templates/sdd-phase.md" in smith, (
        "agents/smith.md does not name the template a phase record starts from"
    )
    assert "each phase's close" in smith or "phase's close" in smith, (
        "agents/smith.md does not say WHEN to write the record — a "
        "session that finds the file but not the timing writes it late or "
        "never"
    )


# --- phase 2: the skill carries the file-set row and the copy instruction ---


def test_skill_file_set_table_carries_the_phase_row():
    skill = read(IMPLEMENT_SKILL)
    assert "phases/phase-N.md" in skill, (
        "skills/implement/SKILL.md's SDD file-set table has no `phases/phase-N.md` row"
    )
    assert "templates/sdd-phase.md" in skill, (
        "skills/implement/SKILL.md does not name the template the "
        "`phases/phase-N.md` row starts from"
    )


def test_skill_says_what_is_copied_into_what_this_phase_was_asked():
    skill = read(IMPLEMENT_SKILL)
    assert "What this phase was asked" in skill, (
        "skills/implement/SKILL.md never names the section the copied content lands in"
    )
    assert "boilerplate" in skill, (
        "skills/implement/SKILL.md does not say that the copied content "
        "excludes the boilerplate the contract, the skill, and "
        "agents/smith.md already carry — without that line, a session "
        "copies the whole spawn prompt in, including what every phase "
        "already gets told"
    )
    assert "agents/smith.md" in skill


# --- phase 2: carrier consistency ---------------------------------------------
#
# The four files phase 1 and 2 touch have to name the record path the same
# way for a reader to find it by grepping any one of them. A template's own
# self-description is one exception: `templates/sdd-phase.md` names its own
# path the way `templates/sdd-round.md` names its own — `round-<N>.md`, the
# angle bracket marking a template placeholder, matching every other
# `<...>` already in that file's path comment (`<unix-epoch-seconds>-<slug>`
# sits in the same sentence). Every file that instead POINTS AT the record
# from prose — `templates/sdd-plan.md`, `agents/smith.md`,
# `skills/implement/SKILL.md` — uses the bracket-free form the file is
# actually created with, `phase-N.md`, matching how those same three files
# already write `round-N.md` for the sibling record
# (`docs/review-handoff-protocol.md`, `skills/code-review/SKILL.md`,
# `agents/warden.md` never write `round-<N>.md` in prose either).

PROSE_CARRIERS = (
    ("templates", "sdd-plan.md"),
    ("agents", "smith.md"),
    ("skills", "implement", "SKILL.md"),
)


@pytest.mark.parametrize("parts", PROSE_CARRIERS)
def test_the_phase_record_path_is_spelled_the_same_in_every_prose_carrier(parts):
    text = read(os.path.join(ROOT, *parts))
    assert "phases/phase-N.md" in text, "/".join(parts)


def test_the_phase_templates_own_path_comment_matches_the_round_templates():
    phase = read(PHASE_TEMPLATE)
    assert "phases/phase-<N>.md" in phase, (
        "templates/sdd-phase.md's own path comment does not spell its path "
        "`phase-<N>.md` — the same templated form `templates/sdd-round.md` "
        "uses for `round-<N>.md`, and the form every OTHER `<...>` in that "
        "same comment already uses"
    )
