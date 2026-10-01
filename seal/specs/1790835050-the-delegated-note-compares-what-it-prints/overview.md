# the delegated note compares what it prints — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `spec.md` (all sections), `plan.md` (both phases, Alternatives A–J), `questions.md` Q1–Q2, `routing.md`; `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file*; contract §1, §2, §5, §12, §14, §15; `seal/specs/1790815612-…/rounds/round-3-report.md` 🟡 10 and its `changelog.md`; issue #701
· evidence: `seal/ledger/1790835050-the-delegated-note-compares-what-it-prints.md` D1 added; `seal/releases/0.9.5.md` rows at lines 11, 13, 14, 16, 45, 46 and `seal/releases/0.11.3.md` line 50 re-stamped to `report_spawns`' new hash, `cd336642`, with a dated re-read note each
· verified: executed — the new case red at the base, seven mutations red, the three named test modules green (210 passed), `evidence-check` and `correction-check` over the tip; read — `--json` never reaching `report_spawns`, the class sweep; unverified — the full suite and the CI interpreter matrix (below)

## Why this work exists

The `--spawns` page printed `1.0m` in the `delegated` column above a note saying the column never reaches a minute; the note is now decided on the minute the column prints, so the two cannot disagree.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A dated re-read note on every drifted row, not only row 13 | `plan.md` phase 2: *the seven rows … re-read against the diff and re-stamped by `evidence-check --reverify`, row 13 of `seal/releases/0.9.5.md` with a `Re-read 2026-10-01` note*. The build wrote a `Re-read 2026-10-01 by work item 1790835050 (#701)` note on all seven | all seven | `CLAUDE.md` §*Repo rule — a change writes fragments*: *an edit drifts the row, which is re-read against that edit and re-stamped there with a dated note*. Policy outranks the plan, and each note says which part of `report_spawns` the edit left alone, which is what the re-read found |
| The frame's stamp of the old hash, corrected in `spec.md` and `plan.md` | `spec.md` §*Grounding* and `plan.md` §*Technical context* wrote the seven rows' anchor as a stamp of `report_spawns` under the bare file name, at hash `15595f59`. Once this work item's ledger fragment existed, `evidence-check`'s records arm read both lines as live claims and refused them at exit 2: the path is not root-relative and the hash is the one this edit moved | each line now names `skills/verify/scripts/session_cost.py#report_spawns` and gives `15595f59` as the hash when framed, outside the stamp form | the records arm is what keeps a live work item's records true of the tree (`evidence_check.py` §*the records arm*), and `spec.md` S5 asks for exit 0. The sentence says what it said; only its spelling stopped asserting a stale anchor. The framer's other words are untouched |
| How the case finds the `delegated` cell | spec S1/S2: *the `delegated` cell reads `1.0m`* | a helper, `delegated_cells`, reading the cell by the header's right edge | spec silent on how. A page-wide search for `1.0m` passes for the wrong reason: the same row's `span` cell prints `1.0m` on the 59.6 s fixture |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, repository-wide lint and format, at the tip | the sealer, spawned by the orchestrator after the review rounds settle |
| `questions.md` Q1 on the CI interpreter matrix — the 57.0 s edge was executed on CPython 3.13.9 (the case) and 3.14.4 (the arithmetic) only | the pull request's CI run |

## Not done

Nothing within reach was left. `:2115`'s `tools_per_turn <= 1.0` was checked and left on `spec.md`'s grounds (Alternative E), and the changelog fragment names it.

## Fed back into the spec

none
