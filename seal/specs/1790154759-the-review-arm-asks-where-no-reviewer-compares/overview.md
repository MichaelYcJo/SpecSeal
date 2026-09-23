# the review arm asks where no reviewer compares — overview

📋 implement applied
· spec:     this work item's `routing.md`, `spec.md`, `plan.md`, `questions.md`;
            `hooks/commit-review-gate.py#judge`, `#touches_code` and the
            `DOC_ROOTS` comment; `docs/review-chain-spec.md` §*Review arm* and
            §*Parity arm*; `skills/implement/orchestration.md` wake/quiet table;
            `tests/test_routing_is_recorded.py` declaration cases;
            `seal/config.md` (no `Record language` row, so English)
· evidence: to be written in phase 3
· verified: to be written in phase 3

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

Nothing yet.

## Fed back into the spec

None yet.
