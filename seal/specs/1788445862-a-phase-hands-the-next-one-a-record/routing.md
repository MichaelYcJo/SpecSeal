# 1788445862-a-phase-hands-the-next-one-a-record — routing

<!-- seal/specs/<unix-epoch-seconds>-<slug>/routing.md — the answer given before the
first edit, in the batch the `implement` skill collects (§1). Committed,
because the check happens at the pull request and CI sees only what is in the
tree.

This is the first file a work item gets, and below the SDD ladder it may be the
only one — a typo fix writes no `spec.md`, and this is what gives it a place to
exist at all.

The rows are read by machines and their vocabulary is fixed. Anything else in
this file is for people. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/a-phase-hands-the-next-one-a-record |

Answered 2026-09-03 by the repository owner, before the first edit.

## Why this way

Issues #121 and #119 land in the same three files
(`templates/sdd-plan.md`/new phase template, `templates/sdd-round.md`,
`agents/smith.md`), so one branch. Owner pre-approved smith · review chain ·
open the pull request into `release/v0.7.0`, and squash-merge automatically
once CI is green, as part of an unattended overnight run of 0.7.0.
