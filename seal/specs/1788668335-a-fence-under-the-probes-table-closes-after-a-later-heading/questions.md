# Questions — 1788668335

## Asked and answered, 2026-09-06, before the first edit

| # | Question | Answer |
|---|---|---|
| 1 | Routing | **smith · through the review chain · open the pull request**, the same as the release's other three |
| 2 | How far the unattended run goes | to the tag |
| 3 | What happens if this chain caps or its broad gate goes red | stop this item, carry on |

## Assumed, not asked

| # | Assumption | Why it does not wait |
|---|---|---|
| 4 | The issue's fix is a proposal, not an instruction | it was written against `da047ab` and the module has moved. `spec.md` makes reproduction at HEAD the first obligation, which is what `implement` §1 means by a ticket being a request rather than an authority |
| 5 | If the shape does not reproduce, the work item closes the issue on the executed evidence rather than adding a guard | a guard for an unreachable state is mechanism nobody can exercise, and this repository refuses a check that cannot fail |
