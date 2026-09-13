# the one script an agent is told to run cannot be typed — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. -->

## Why this work exists

The one script an orchestrator is told to run was the one script no shipped
document gave a way to reach, so four agent segments concluded it does not
ship and hand-wrote the record it generates; now the command resolves, every
document that names it says where it is, and a test enumerates the class
rather than this instance.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many `tests/test_docs_line_wrap.py`-covered files phase 3 edits | `plan.md` phase 3's `Verified by` cell said *the five covered files this phase edits* and then listed four | four, and the four it listed | **Executed** 2026-09-14: the nine documents intersected with that module's own `COVERED` list gives `agents/warden.md`, `agents/sealer.md`, `skills/code-review/SKILL.md` and `skills/code-review/orchestration.md`. The other five — `templates/sdd-round.md`, `agents/smith.md`, `skills/implement/SKILL.md`, `skills/verify/SKILL.md`, `templates/sdd-phase.md` — are in none of it; the module's own docstring records `agents/smith.md` at 148 columns as a reason it is not covered. The number was wrong and the list was right, so the cell now reads *four* and keeps its four names |
| The platform case's shape | `plan.md` names `tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_wrapper_pair_is_run_through_the_twin_the_platform_can_execute` as the form to follow, and that case opens with two `isfile` assertions | the same two assertions, kept | Written without them the case was green against a `bin/` holding neither file, because constructing an argv touches no filesystem. `skills/agent-contract/SKILL.md` §15 — *a new case is not planted until it has been seen red* — and it could not be. Recorded in `phases/phase-2.md` |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the sealer — `skills/agent-contract/SKILL.md` §2 puts the broad gate after the review rounds settle, and no phase here takes it |
| `Ran by` in all three phase records | the orchestrator — the spawn prompt named no model, and `templates/sdd-phase.md` refuses a value a segment sources from its own idea of what it is |

## Not done

Nothing yet.

## Fed back into the spec

none
