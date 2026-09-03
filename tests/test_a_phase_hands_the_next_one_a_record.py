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

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHASE_TEMPLATE = os.path.join(ROOT, "templates", "sdd-phase.md")
PLAN_TEMPLATE = os.path.join(ROOT, "templates", "sdd-plan.md")

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


def test_the_field_table_is_phase_and_commit_only():
    lines = stripped_lines()
    header_idx = next(
        (i for i, l in enumerate(lines) if l.strip().startswith("| Field")), None
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
    rows = [l.strip() for l in table_lines if l.strip().startswith("|")]
    field_rows = [l for l in rows if not set(l.replace("|", "").strip()) <= {"-"}]
    names = [l.split("|")[1].strip() for l in field_rows]
    assert names == ["Phase", "Commit"], (
        f"the field table carries {names}, not just Phase/Commit — a phase "
        "has no Target SHA to squash away and no Pass checkbox to answer"
    )
    for name, row in zip(names, field_rows):
        value = row.split("|")[2].strip()
        assert value.startswith("<") and value.endswith(">"), (
            f"a template must not ship a claim, and `{value}` is one ({name})"
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
        text = " ".join(l.strip() for l in body)
        assert text.startswith("<") and text.endswith(">"), (
            f"`{heading}` ships `{text}` — a template must offer a "
            "placeholder, not a filled-in claim"
        )


def test_removes_section_is_a_table_with_a_none_row():
    lines = stripped_lines()
    body = section_body(lines, "## What this phase removes")
    rows = [l.strip() for l in body if l.strip().startswith("|")]
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
