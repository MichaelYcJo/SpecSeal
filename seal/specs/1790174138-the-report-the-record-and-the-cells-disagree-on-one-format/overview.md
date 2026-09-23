# the report, the record and the cells disagree on one format — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `CLAUDE.md` (the goal, the fragment rule, the ledger's REMOVED rule), `CONTRIBUTING.md` §*What a change to a gate must carry*, `docs/review-chain-spec.md` §*The finding id*, §*A verdict row that commissions nothing*, §*The fix range*, §*The reopening* (the `What new prints` table), §*The record generator*, `docs/review-handoff-protocol.md` §record fields, `skills/agent-contract/SKILL.md` §2, `seal/specs/1790174138-…/{routing,spec,plan,questions}.md`, work item 0's `overview.md` and `plan.md`, MichaelYcJo/SpecSeal#218, #505, #382, #436, #217, #174, #503, #437, #366
· evidence: `seal/ledger/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format.md` A1–A4 so far; `seal/ledger.md` rows R3, R4, R1, R9, F1–F5, R3/R4 of the swallow guard, R5, R6, S5, the `### Review arm` row and R5/C2/C6/R7/R8 of the spec-anchored rows re-read with dated notes; work item 0's B1 re-read
· verified: executed — the generator module (126), the target and close modules (110), the pull-request check's `fix_range` selection (13), the records-arm module (61), the precedes module (51), sixteen mutations tabled in `phases/`, the 584-sequence differential, Q3's walk; read — the ledger rows' claims against the edited units; unverified — the broad gate, the sealer's

## Why this work exists

Three reviewers in one release wrote a report the generator refused, and the
cells the generator and the checkers write and read had four other quiet
disagreements — fixes lost under subheadings, a revision written where a
commit belongs, a pending range nothing read back, a comment that silenced
an arm, a bound that un-said itself, a seal that overwrote the run before it.
Now the report standard is where the reviewer copies from, and every cell
means one thing to its writer and its reader.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where A9's case lives | `spec.md` names `tests/test_a_record_precedes_the_fixes_it_commissions.py` | `tests/test_the_record_is_generated.py`, beside every other `bound_line` case | `phases/phase-1.md`; the spec's own alternative, *where 0's phase 2 put A6*, is that file |
| The frame's ledger coordinates | `spec.md` §Data & interfaces wrote four rows as `path#unit@hash` with a short path | the stamps dropped, the units named bare | `evidence-check --strict`'s records arm refuses a short-path stamp as a file not found; `phases/phase-1.md` |

## What a change to a gate must carry — the four answers, for the pull request body

**#436, `chain_check.fix_range`'s pending arm.** Seen red: two cases at
`65195f49`, exit 0 and the row never named. Direction: blocks more — a record
whose `Fix range` still reads the template's pending words beside a
`round-N` is refused, as `fix_surface` already refuses its own rows; the
wrong deny costs one `round-record close`, the wrong allow ships a range
claim false about its own file. Prompt budget: zero, and zero committed
records affected (23 read by the frame). Platform honesty: two cells of one
file, no git, no path, no shell.

**#217, `evidence_check.claim_lines` reading past an unclosed comment.** Seen
red: one case at `65195f49`, exit 0 and `0 names read` over a record naming
a unit the tree lacks. Direction: blocks more — lines an unclosed comment
used to drop are read, so a missing `-->` is no longer a way past the arm.
Prompt budget: zero; Q3 found 0 live records ending inside a comment across
144 files and the three open branches. Platform honesty: lines of one file.

## Not verified

| Item | Who must answer |
|---|---|
| the broad gate — the full suite, `uvx ruff check .` and `uvx ruff format --check .` over the whole tree, taken once after the rounds settle | the sealer, spawned by the orchestrator with the base and the work item |

## Not done

- No new cutoff for #436's arm; `RANGE_FROM` excuses exactly what
  `ORDER_FROM` would (`phases/phase-3.md`).
- `chain_check.py`'s module docstring still inventories `Contract changes`
  and `New units` without a `Fix range` line; the spec's `Fix range` table is
  the policy home and `test_the_module_docstring_names_what_the_checker_refuses`
  pins three other phrases, so the inventory was left as it stood.

## Fed back into the spec

- `docs/review-chain-spec.md` §*The reopening*, the `What new prints` table:
  the two rows rewritten to the condition the code implements (#218) —
  inferred during implementation; a planner may overturn it only with the
  code.
- `docs/review-chain-spec.md` §*The fix range*: the pending-beside-a-`round-N`
  row (#436).
