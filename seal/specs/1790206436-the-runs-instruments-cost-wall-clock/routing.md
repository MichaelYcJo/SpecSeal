# 1790206436-the-runs-instruments-cost-wall-clock — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/337-the-runs-instruments-cost-wall-clock |

Answered 2026-09-24 by the repository owner, before the first edit.

## Why this way

The owner pressed the `automation` preset once for the whole `release: 0.15.1`
milestone, asked in one batch before its first work item. This item is the
milestone's step B, the run's instruments: the broad gate ran six suites at
13 minutes each where `-n auto` runs the same suite in 3, parallel wardens
and sealers overwrote each other's clone and capture files, and the sealer's
`broad-gate` resolves to the installed plugin copy — MichaelYcJo/SpecSeal#337,
#544 and #475. Each cost measured wall clock in the 0.15.0 run.
