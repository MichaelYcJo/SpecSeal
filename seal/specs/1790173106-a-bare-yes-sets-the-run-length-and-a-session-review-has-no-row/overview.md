# a bare `yes` sets the run length, and a session review has no row — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `CLAUDE.md` (the goal, the fragment rule, the ledger's REMOVED rule), `CONTRIBUTING.md` §House rules, `docs/review-chain-spec.md` §Review arm and §`Needs a fix`, `docs/release-checklist.md` §4, `skills/implement/orchestration.md` §Question 1 and the four-combinations table, `seal/specs/1790173106-…/{routing,spec,plan,questions}.md`, MichaelYcJo/SpecSeal#138 and #241
· evidence: `seal/ledger/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row.md` B1–B3 (B2 re-founds F8, REMOVED from `seal/ledger.md`); 17 rows of `seal/ledger.md` re-read and re-stamped, each with a dated note
· verified: executed — the floor-and-depth module (76), the two round-record suites (173), the pinning module with the routing, waiver, wrap and one-word modules (128), fifteen document-reading modules (615 passed, 1 failed on the not-yet-written overview), `evidence-check --strict`, the ten mutations in `phases/`; read — the ledger rows' claims against the edited units; unverified — the broad gate, the sealer's

## Why this work exists

One cell with three characters in it bought a review run a round past its own
floor, and seven documents told a session that had checked its own change it
had no honest routing answer; now a bare `yes` is refused at both ends of the
record and the direct answer's documents say what it owes.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The inline reopening read's home | `plan.md` places `== chain.FLOOR_YES` in `round_record.py#bound_line`; the tree has it in `round_record.py#floor_and_fixes`, the helper `bound_line` calls | the edit went to `floor_and_fixes`; `bound_line` is byte-identical | `phases/phase-2.md`; ledger R3 and R4 anchor on both, so the re-read reached both |
| Where A8's pinning case lives | `spec.md` item 10 names the SHAPE (`NO_CHECK_READS`) and `plan.md` says *the new case*; neither names a file | a module of its own, `tests/test_the_direct_answer_owes_the_sealers_record.py`, with the gate prompt's pin in `tests/test_routing_is_recorded.py` | a pin over a file cannot live in that file — the *gone* phrase would be in it as a literal — and the gate's option is a split Python literal a whole-file substring cannot read |
| F8's address | the ticket names `seal/ledger/1788472135-….md`; `plan.md` names `seal/ledger.md` | removed from `seal/ledger.md` line 822, where the fold had put it | `CLAUDE.md`: a row whose anchor a change removes is REMOVED, not re-pointed |

## Not verified

| Item | Who must answer |
|---|---|
| the broad gate — the full suite, `uvx ruff check .` and `uvx ruff format --check .` over the whole tree, taken once after the rounds settle | the sealer, spawned by the orchestrator with the base and the work item |

## Not done

- No third `Review` answer, no rename of `straight to the PR`, no edit to the
  `CLAUDE.md` routing paragraph, `templates/claude-md-block.md` or the routing
  question's box 3 — `spec.md` §Out, each with its grounds.
- No cutoff for the bare-`yes` refusal: Q1 measured zero records at or after
  `NEEDS_FROM`, so `NEEDS_FROM`'s whole-row grandfathering is the only excuse
  the refusal needs.
- `chain_check.py#written_late_reason` still reads its row through
  `yes_or_no` directly rather than through `says_reopened`; its docstring
  already treats a bare `yes` as None, so the reading agrees, and folding it
  in would widen a #138 change into the `Written late` row's unit.

## Fed back into the spec

- `docs/review-chain-spec.md` §*Review arm*: the paragraph *Two answers, and
  not three* — inferred during implementation from the frame's grounds; a
  planner may overturn it by adding the third answer the ticket proposed.
- `docs/review-chain-spec.md` §*`Needs a fix`*: the bare-`yes` row.
