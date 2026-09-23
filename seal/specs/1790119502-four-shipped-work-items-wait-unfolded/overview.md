# four shipped work items wait unfolded — overview

📋 implement applied
· spec:     this work item's `routing.md`, `spec.md`, `plan.md`, `questions.md`;
            `skills/settle/SKILL.md` §§1–4 and *What a fold branch owes*;
            the four retiring work items' `spec.md`, each read in full, and
            their `overview.md` §*Not verified*; `CLAUDE.md` §*a change writes
            fragments*, §*A row whose anchor a change removes is REMOVED*,
            §*no real identifiers*; `seal/config.md` (no `Record language`
            row, so these records are English)
· evidence: no fragment — no new claim about code was established. `seal/ledger.md`:
            four rows re-read and re-verified, S9 (phase 2) and C1, C3, C4
            (phase 4); none added, removed or re-pointed
· verified: **executed** — `settle` and `settle --retire` (0);
            `unverified-check --baseline` (0, 4 folded, 0 deletions);
            `chain_check --baseline` on both bases (1, four `retired:`, one
            error — this item's own absent round record); `evidence-check
            --strict` (0, 1468 ok); `survivor-check` (0); `correction-check` (0);
            the 44 real-corpus test modules (0, 2315 passed).
            **unverified** — the broad gate, which is the sealer's

## Why this work exists

The release before this one shipped four work items and folded none of them,
so `settle` names four released directories whose rules live only in a
`spec.md`; this branch writes those rules into `docs/`, gives every open
leftover a home that outlives the directories, and retires the four.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How a citation of a retired file is resolved | `spec.md` G2: *"A citation of a file this branch removes therefore keeps its path and gains `at \`b0cbd34\``"*; phase 2 built exactly that | the path dropped; the work item id named, with the `docs/` section carrying its marker | The orchestrator's decision during the build: the history is rewritten into a new repository after this release, so every SHA changes and one written into a file dangles. Recorded in `spec.md` G2 and `phases/phase-2.md` |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck on the folded tree | the `sealer`, in its single run after the review rounds settle (`agent-contract` §2). This branch runs narrow slices only |
| L2 — `size: now` does not exist on the tracker and the flow-log roll after it was skipped: run `35796513013` failed at `tracker_labels.py --apply` because the label's description is longer than 100 characters. The only record of it was an open row of a retiring `overview.md` | the repository owner, through #515 (`release: 0.13.2` milestone), filed by the orchestrator under `questions.md` Q1's default. This branch does not touch the script or the workflow |

## Not done

**The prose carriers of the depth-exit wording were left as they are.** Documents, agent definitions, skills and `templates/sdd-round.md` still say a leftover is deferred with a named answerer *or becomes an issue*, and not every one of them points at the ladder. They are found by searching for that phrase with whitespace collapsed, which is what L6's paragraph now names instead of a list *(Corrected 2026-09-23 in round 2's fix pass.)*. They are the prose twins of `DEPTH_EXIT`, and L6's new paragraph in `docs/review-chain-spec.md` asks the repository owner to decide that pair; rewording the carriers inside a fold would decide it first. `phases/phase-4.md` has the grep.

## Fed back into the spec

*Inferred during implementation*, so a planner may overturn either:

1. **`spec.md` G2's SHA pin is replaced** by the work item id and the `docs/`
   section carrying its marker — the orchestrator's decision, recorded in G2.
2. **The flow-log command answers five states, not four.** The folded
   paragraph follows `session_cost.py#post`, which also exits 0 posting
   nothing where `gh` cannot run (`phases/phase-4.md`).
