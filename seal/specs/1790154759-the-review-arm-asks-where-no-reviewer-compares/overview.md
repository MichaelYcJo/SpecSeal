# the review arm asks where no reviewer compares — overview

📋 implement applied
· spec:     this work item's `routing.md`, `spec.md`, `plan.md`, `questions.md`;
            `hooks/commit-review-gate.py#judge`, `#touches_code` and the
            `DOC_ROOTS` comment; `docs/review-chain-spec.md` §*Review arm* and
            §*Parity arm*; `skills/implement/orchestration.md` wake/quiet table;
            `tests/test_routing_is_recorded.py` declaration cases;
            `seal/config.md` (no `Record language` row, so English); both
            READMEs' `commit-review-gate` rows; the `## Verdicts` tables of
            `1790119502-four-shipped-work-items-wait-unfolded`'s three rounds
· evidence: `seal/ledger/1790154759-the-review-arm-asks-where-no-reviewer-compares.md`
            R1 added. `seal/ledger.md`: four rows re-read and re-verified,
            each with a `Re-read 2026-09-23` marker — the review-chain
            specification's opt-in headings row, two rows anchored on the
            orchestration routing section, and the row anchored on the
            `1788331011` ledger heading, which moved because the first one's
            notes did. S11 did not drift and was left as it is
· verified: **executed** — every mutation named in `phases/phase-1.md` and
            `phases/phase-2.md`, each seen red and restored; the two gate
            modules (139 passed); the 39 modules that read the two edited
            documents (1735 passed, 1 skipped); `evidence-check --strict`
            (0, 1481 ok). **read** — the READMEs, which name no paths for the
            review arm and so did not move. **unverified** — the broad gate,
            which is the sealer's

## Why this work exists

Issue #518 asked whether the commit gate's review arm should skip a change
confined to `docs/` and `seal/`, as the parity arm does; the measurement says
no, and this work writes that answer where the question is met and pins it
with a case, so the gate's behaviour stays the same and stops looking like an
oversight.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| none | | | |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck on this branch | the `sealer`, in its single run after the review rounds settle (`agent-contract` §2). This branch runs narrow slices only |

## Not done

**`questions.md` Q3 was not taken.** M4 is a lower bound, and a fuller count
can only add findings, so it can only strengthen the refusal. The row stays
open with its answerer, `a measurement`, because nothing this work builds
depends on it.

**Both READMEs were left as they are.** Their `commit-review-gate` rows name
no paths for the review arm and call the parity arm's case a code commit, so
both stay true.

## Fed back into the spec

*Inferred during implementation*, so a planner may overturn either:

1. **`questions.md` Q1 took its default.** The review arm's decision table
   gained a row for a `routing.md` declaration, placed between the waiver and
   the mark in the order `judge` evaluates them.
2. **`questions.md` Q2 took its default.** A3 is covered by
   `tests/test_routing_is_recorded.py#test_a_declared_direct_item_commits_without_a_prompt`,
   and no docs-only variant was planted.
