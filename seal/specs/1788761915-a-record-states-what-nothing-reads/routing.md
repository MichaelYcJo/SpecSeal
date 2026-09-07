# 1788761915-a-record-states-what-nothing-reads — routing

<!-- seal/specs/<unix-epoch-seconds>-<slug>/routing.md — the answer given before the
first edit, in the batch the `implement` skill collects (§1). -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/190-207-a-record-states-what-nothing-reads |

Answered 2026-09-07 by the owner, before the first edit — the same batch that
answered 0.9.0's first work item, carried forward for the release.

## Why this way

#190 names three candidate shapes and argues for one; #207 names three and
argues for one. Both arguments turn on the same clause of `CLAUDE.md` —
whether a design stops to ask a person — and neither is a formatter's call.
The two chains this release has already run are the evidence: between them they
put five false statements into records that nothing read, and the orchestrator
carried the wrong bound into eight spawn prompts because the record it wrote
first knew the right one and did not say it.
