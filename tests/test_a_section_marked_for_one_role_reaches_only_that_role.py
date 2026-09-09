"""A section marked for the orchestrator is not in a file an agent preloads.

Issue #292, phase 2. `skills/code-review/SKILL.md` marked the sections
addressed to the session that spawns agents with an `Orchestrator:` heading
prefix, and #265 moved them out to `orchestration.md` — a file no `skills:`
list names, so no spawn pays for it. `implement` had the same kind of
section under no marker at all, and every `smith` spawn read the bootstrap
question, the parity setup and the routing tables: procedure for an act
`agents/smith.md` forbids the agent (asking a person, writing `routing.md`).

The marker is the convention; this module is what makes it a rule. It
derives the agents from the `agents/*.md` glob and each definition's own
`skills:` list — the list `payload_meter.py` measures, read by the same
parser — and fails when

  a heading whose text starts `Orchestrator:` sits in a file that list
  injects (the `SKILL.md` of a listed skill, or the definition itself), at
  `##` or `###` — both levels, because #255's grep read `##` alone and came
  out short (Q2);

  an `orchestration.md` is itself listed under any `skills:`, which would
  inject the orchestrator's half by the front door.

What it does not catch, stated rather than left to be found: a section
written for the orchestrator under a heading that carries no marker. The
check reads the marker, not the meaning, and a paraphrase is the reviewer's
finding — the same limit `test_a_moved_rule_leaves_its_definition.py`
states for itself.

Red-first, per the contract's §15: the planted cases build a temp tree with
the defect in it, and the real-tree case was seen red on this repository at
the commit that marked `implement`'s three sections before moving them —
`seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/phases/phase-2.md`
names it.
"""

import importlib.util
import os
import re

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "verify", "scripts", "payload_meter.py")

MARKER = "Orchestrator:"
HEADING = re.compile(r"^(#{2,3}) (.*)$")
FENCE = re.compile(r"^\s*(```|~~~)")


def _meter():
    spec = importlib.util.spec_from_file_location("payload_meter_for_marker", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def marked_headings(text):
    """Every `##` / `###` heading whose text starts with the marker, outside
    fenced code. A fence is tracked because a skill quotes headings as
    examples, and an example is not a section."""
    found, fenced = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = HEADING.match(line)
        if match and match.group(2).lstrip().startswith(MARKER):
            found.append(line.rstrip())
    return found


def _names_the_orchestrators_half(entry):
    stem = entry.rstrip("/").rsplit("/", 1)[-1]
    return stem in ("orchestration", "orchestration.md")


def findings(root):
    """One line per defect, each naming the agent, the file and the heading
    or entry. Empty on a clean tree."""
    meter = _meter()
    out = []
    for agent, definition in meter.agents_in(root).items():
        text = _read(os.path.join(root, definition))
        _name, skills = meter.frontmatter(text)
        injected = [(definition, text)]
        for entry in skills:
            if _names_the_orchestrators_half(entry):
                out.append(
                    f"{definition} lists `{entry}` under `skills:` — an "
                    f"`orchestration.md` is the orchestrator's half and is "
                    f"never injected into `{agent}`"
                )
                continue
            rel = f"skills/{entry}/SKILL.md"
            path = os.path.join(root, rel)
            if not os.path.isfile(path):
                out.append(
                    f"{definition} lists `{entry}` under `skills:` and the "
                    f"tree has no {rel} for `{agent}` to receive"
                )
                continue
            injected.append((rel, _read(path)))
        for rel, body in injected:
            for heading in marked_headings(body):
                out.append(
                    f"`{agent}` preloads {rel}, which carries `{heading}` — "
                    f"a section marked for the orchestrator reaches an agent"
                )
    return out


# --- planted trees ------------------------------------------------------------


def _tree(base, skills_of, files):
    """`agents/<name>.md` per entry of `skills_of`, then `files` as
    path → text under `base`."""
    for name, skills in skills_of.items():
        listed = "".join(f"  - {s}\n" for s in skills)
        os.makedirs(os.path.join(base, "agents"), exist_ok=True)
        with open(os.path.join(base, "agents", f"{name}.md"), "w") as handle:
            handle.write(f"---\nname: {name}\nskills:\n{listed}---\n\n# {name}\n")
    for rel, text in files.items():
        path = os.path.join(base, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as handle:
            handle.write(text)
    return str(base)


PLAIN = "---\nname: foo\n---\n\n# foo\n\n## A section\n\nProse.\n"


def test_a_marked_heading_in_an_injected_skill_names_agent_file_and_heading(
    tmp_path,
):
    root = _tree(
        tmp_path,
        {"a": ["foo"]},
        {"skills/foo/SKILL.md": PLAIN + "\n### Orchestrator: how a run ends\n\nX.\n"},
    )
    found = findings(root)
    assert len(found) == 1, found
    assert "`a`" in found[0]
    assert "skills/foo/SKILL.md" in found[0]
    assert "### Orchestrator: how a run ends" in found[0]


def test_both_heading_levels_are_read(tmp_path):
    """Q2: `##` and `###` alike — the grep that read one level came out short."""
    root = _tree(
        tmp_path,
        {"a": ["foo"]},
        {
            "skills/foo/SKILL.md": PLAIN
            + "\n## Orchestrator: two\n\nX.\n\n### Orchestrator: three\n\nY.\n"
        },
    )
    found = findings(root)
    assert len(found) == 2, found
    assert any("## Orchestrator: two" in f for f in found)
    assert any("### Orchestrator: three" in f for f in found)


def test_a_marker_quoted_inside_a_code_fence_is_not_a_section(tmp_path):
    root = _tree(
        tmp_path,
        {"a": ["foo"]},
        {
            "skills/foo/SKILL.md": PLAIN
            + "\n```markdown\n## Orchestrator: an example\n```\n\nProse.\n"
        },
    )
    assert findings(root) == []


def test_the_definition_itself_is_read(tmp_path):
    root = _tree(tmp_path, {"a": []}, {})
    with open(os.path.join(root, "agents", "a.md"), "a") as handle:
        handle.write("\n## Orchestrator: not the agent's\n\nX.\n")
    found = findings(root)
    assert len(found) == 1, found
    assert "agents/a.md" in found[0]


@pytest.mark.parametrize("entry", ["orchestration", "implement/orchestration.md"])
def test_an_orchestration_file_listed_under_skills_is_named(tmp_path, entry):
    root = _tree(
        tmp_path,
        {"a": [entry]},
        {"skills/implement/orchestration.md": "## Orchestrator: x\n"},
    )
    found = findings(root)
    assert len(found) == 1, found
    assert f"`{entry}`" in found[0]
    assert "orchestration.md" in found[0]


def test_a_marked_heading_in_a_file_no_agent_injects_is_allowed(tmp_path):
    """The marker is where the orchestrator's half is SUPPOSED to be."""
    root = _tree(
        tmp_path,
        {"a": ["foo"]},
        {
            "skills/foo/SKILL.md": PLAIN,
            "skills/foo/orchestration.md": "## Orchestrator: a run ends\n\nX.\n",
        },
    )
    assert findings(root) == []


def test_a_listed_skill_the_tree_does_not_ship_is_named(tmp_path):
    root = _tree(tmp_path, {"a": ["missing"]}, {})
    found = findings(root)
    assert len(found) == 1, found
    assert "skills/missing/SKILL.md" in found[0]


# --- the real tree ------------------------------------------------------------


def test_no_agent_preloads_a_section_marked_for_the_orchestrator():
    """Red between the commit that marked `implement`'s three sections and
    the one that moved them (`phases/phase-2.md` names both)."""
    found = findings(ROOT)
    assert found == [], "\n".join(found)
