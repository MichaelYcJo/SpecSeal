# 1790745049-the-guard-and-consent-stop-depending-on-the-walks-order — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `routing.md`; `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it* and §*Unknowns resolve conservatively*; `docs/commit-review-gate-spec.md` §*A `cd` the gate cannot read*; 1790660768's ledger rows I2, I9, I12–I15 and changelog; 1790644505's E9, E10, E12, E16
· evidence: `seal/ledger/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order.md` M1–M4 added; I13 corrected and I2, I9, I12, I14, I15 re-read in 1790660768's fragment; E9, E10, E12, E16 re-read in 1790644505's; one row re-read in `seal/releases/0.4.0.md`
· verified: executed — the new cases red at `542f920b`'s hooks and green here, the structural and gate corpora, five mutants, the narrow modules; read — every consumer of `walk_directories`

## Why this work exists

The worktree guard and the consent writer now judge the tree the release base
judged by construction, so no ordering of the commit gate's wider reading can
send them to a directory bash never ran the command in (#689).

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Removing the ordering code | The prompt: "the order rules, and any code that exists only to order the threads for those two consumers, can go" / the rule also sets the order the gate's deny names targets in | Kept, comment rewritten | The prompt's own exception: "If the gate's reason text or deny order depended on that ordering, keep the gate's current behaviour and say how." A mutant without the rule changed 404 of 5,092 reason texts |
| The base thread's unplacing | The prompt: read "exactly the directories `86256492` read, taken from the base thread" / the base thread's reported directories carry I14's second-reading unplacing | `base_directories` takes the thread before that step | That step is #674's, not the base's; where it applies `86256492` read no git in the segment (M3) |
| Where the loop lives | First built as a helper `_walk` / three released ledger rows anchor statements inside `walk_directories` | A `base` flag on `walk_directories` | Keeps those rows resolving rather than re-pointing a released ledger |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, repository-wide lint and typecheck (`unverified` per contract §2) | the orchestrating session, through the sealer's broad gate |
| Windows: the guard's backslash doubling reaches `base_directories` as it reached `walk_directories`; read, not run | the repository owner, on a Windows machine; no runner here, and the RIDER on `_tokenize_with_separators` already records the platform |
| A real shell for the new cases' shapes; bash's behaviour for them is the one #690's rounds executed, not re-run here | the review round |

## Not done

The 0.17.0 redesign of how the gates learn where a command acts is the owner's
next item and out of scope. The guard's reading of a segment only #674 reads
as git (`2>/dev/null git switch`) stays, since it is recognition rather than
a directory. `spec.md` was written by `smith` from the orchestrating session's
spawn prompt; the framer mark says `the session` because that session drew
the frame and `routing.md`'s `Planning` row says so.

## Fed back into the spec

- *Inferred during implementation:* `base_directories` unplaces a segment on
  the as-written reading alone (spec S6, ledger M3). The prompt did not say
  which of the thread's two unplacings the guard takes.
