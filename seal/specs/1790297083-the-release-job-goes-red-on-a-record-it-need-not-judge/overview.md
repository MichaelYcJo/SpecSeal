# 1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge — overview

📋 implement applied
· spec:     this work item's spec.md, plan.md and questions.md; docs/review-chain-spec.md §When the record was written; skills/code-review/scripts/chain_check.py#added_on_branch
· evidence: written at phase 4
· verified: phase 1 — executed; later phases fill this line

## Why this work exists

`chain_check` went red on records it had no claim to judge: a record deleted
and re-added on a side branch was read at its early add (#529), a record a
pull request restored byte-for-byte from the base's history was held to
reachability (#598 instance 1), and `Pass` beside `nobody` failed a draft in
the window the orchestration document orders (#598 instance 4).

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A1's fixture clock | `spec.md` A1 describes the merged side-branch shape with no date; the test's own clock puts every commit in one second | A1 dates the side branch ahead of the early add | In one second the date order is a tie, which is A2's failure and not A1's. `phases/phase-1.md` has the measurement |
| `--full-history` in the restoration predicate | `spec.md` Scope 2: *"answered by one `git log --full-history --find-object=<blob> <fork> -- <rel>`"*; the code drops `--full-history` | the code | Every case stayed green without it, and a probe showed `--find-object` already walks the side line a plain path-limited log simplifies away. A flag with no case behind it was taken out rather than kept unpinned. `phases/phase-2.md` |
| C4, what `close` does in the window | `plan.md` *Technical context*: *"`round_record.py close` runs the check with no payload, so it keeps reporting the refusal after ticking `Pass`"*. `round_record.py#run_check` writes a draft payload unless `gh` says the pull request is ready | the code as it stood; the C4 case now asserts exit 0 and the notice naming the verifying round | The frame's premise is false against `run_check`. Keeping exit 1 would need a second, strict path through the check for one pair. No document states the exit code. `phases/phase-3.md` |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, lint and typecheck over the whole tree | the sealer, once, after the review rounds settle |

## Not done

Written at phase 4.

## Fed back into the spec

Written at phase 4.
