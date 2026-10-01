# 1790815611-the-record-arms-run-before-the-sealer-is-spawned — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | b0d5426f |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

The documents. A paragraph before the sealer's spawn in
`skills/code-review/orchestration.md`. The `Grounds` cell and, where the order
section names the spawn, the step in `skills/implement/orchestration.md`. One
sentence in `skills/verify/SKILL.md`. The lint-first example row and the arms
sentence in `templates/config.md`, the owner's answer of 2026-10-01. Pins for
S8, S9 and S10 in `tests/test_broad_gate_rule.py`, seen red first against the
unedited documents.

## What this phase found

**The order step is pinned verbatim in a file the spec did not list.**
`tests/test_the_rules_have_one_owner.py::test_the_order_opens_the_draft_between_the_build_and_the_rounds`
asserts `) → warden rounds → sealer → the pull request is marked ready.`. The
spec asks for the preflight to be written in as the step before the sealer,
which changes those arrows. The pin moved with them, and its other two
assertions are untouched. `overview.md` carries this as a divergence.

**The spawn paragraph's own sentence had to change, not only gain one.** It
read *the sequence has one more step before the draft goes ready, and it is a
spawn rather than a run*. With a run before the spawn that sentence is false,
so it now says two steps, a run that is the orchestrator's and then a spawn.
The bold lead stays word for word, because `skills/verify/SKILL.md` cites it
as a section.

**The template's "Two of those checks" sentence still reads.** The
paragraph after the edited one opens *Two of those checks, the survivor arm and
the correction arm*. With the list gone, *those checks* refers to *the
plugin's own checks*, which the edited paragraph still names. The paragraph is
unchanged.

Seen red, executed: the five new pins against the unedited documents, each
for its own missing sentence. Then three mutations, each restored from kept
bytes with `tests/__pycache__` cleared:

- D1, `section()` reading to the end of the file: the no-heading assertion
  sees the next section's heading.
- D2, the order step without the preflight: both order cases fail.
- D3, the bold step reverted to the spawn alone: the index assertion fails.

Run at the phase's close: `tests/test_broad_gate_rule.py`, the four modules
the plan names, `tests/test_the_rules_have_one_owner.py` and
`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`, 209
passed and 6 skipped. Then every module that reads one of the four edited
documents: 2,707 passed, 9 skipped and one red,
`test_every_spec_directory_that_reached_the_ladder_has_an_overview`, because
this work item's `overview.md` is phase 4's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `templates/config.md`'s hand-typed list of four arms: `evidence-check`, `unverified-check`, `chain_check.py`, `survivor-check` | `skills/verify/scripts/broad_gate.py`'s module docstring, which lists all six in order and is what the sentence now points at |
| the example row's suite-first order | none: the lint-first row replaces it, as the owner answered |
