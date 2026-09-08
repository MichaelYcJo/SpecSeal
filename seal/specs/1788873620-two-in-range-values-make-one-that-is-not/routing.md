# 1788873620-two-in-range-values-make-one-that-is-not — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/192-two-in-range-values-make-one-that-is-not |

Answered 2026-09-08 by the repository owner, before the first edit, in the one
batch that answers every work item of 0.9.3.

## Why this way

A funnel answers which values enter and a site walk answers which operations exist; neither answers what two values that passed make. The owner chose the int-conversion property over the per-operation walk: the class is 'every site converting a derived number to an int carries a guard', enumerated by construction from the module's own source rather than by a list somebody read.

Straight to the PR because the three measured shapes at the base are the case set, and a property-enumerated class is checked by mutation rather than by judgement.

The wrong-number direction — a finite but nonsensical count summed as given — stays out of this branch and stays open on #192's own body.
