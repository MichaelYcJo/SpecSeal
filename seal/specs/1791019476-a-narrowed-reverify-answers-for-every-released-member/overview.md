# 1791019476-a-narrowed-reverify-answers-for-every-released-member — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show, each part written when it happened. -->

📋 implement applied
· spec:     spec.md D1–D5, S1–S9 and §*The class, enumerated*; plan.md's phases; questions.md Q1, Q2, M1, M2, W1, W2
· evidence: seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md
· verified: each phase record carries its runs, labelled executed or read

## Why this work exists

A `--reverify` narrowed to the file holding a folded or a fragment re-read used to write nothing and exit 0 while `--strict` over the same file read that re-read DRIFTED; now it answers for every family a file it read holds a member of, and a `Checked` date the calendar does not have is named as written.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether every family's root is released | D3: "every family's root is released" / a `Corrected ·` row in a fragment, and a citing row whose citation does not resolve, each root a family of their own | the spec's conclusion, unchanged code | Such a family holds no released member, and `released_drift`'s second loop grades released members only, so it owes nothing either way (phase 1, read) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck over the whole repository | the sealer, once the review rounds settle |
| S8's `evidence-check --strict .` at 0 drifted: 9 rows the integration branch re-stamps stay drifted on this branch, and the merge conflicts at lines 17–18 and 29–30 of #736's fragment | the orchestrator, when `origin/release/v0.18.0` is merged in and the strict run repeated |

## Not done

Nothing.

## Fed back into the spec

None.
