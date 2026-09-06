# Questions — 1788661274

## Asked and answered, 2026-09-06, before the first edit

| # | Question | Answer | What it decided |
|---|---|---|---|
| 1 | Routing | **smith · through the review chain · open the pull request** | `routing.md`, the same as #170 and #156 |
| 2 | How far the unattended run goes | to the tag | why nothing here waits for a person |
| 3 | What happens if this chain caps or its broad gate goes red | stop this item, carry on with the rest | the item's state is left in its draft pull request |

## Answered by the issue's own owner comment, 2026-09-05

| # | Question | Answer |
|---|---|---|
| 4 | Of the four sources #155 names, which tells the script what to write | **two halves**: the version comes from `.claude-plugin/plugin.json` in the checked-out tree, and **a roll happens only when the version the open issue names has shipped** — not on every push to `main` |

## Left to this work item, which is what the issue asks it to settle

| # | Question | Why it is not asked |
|---|---|---|
| 5 | How the open log's version is known, and what the next log is called | #155 names three shapes and chooses none: *"Named, not chosen — the trade is what the work item settles."* Different answers change what is built, but the deciding is delegated to the work item in writing, so it is settled in `plan.md` §Alternatives with a failure scenario each rather than put back to a person |

## Assumed, not asked

| # | Assumption | Why it does not wait |
|---|---|---|
| 6 | Closed logs are not retitled, whatever the convention becomes | #155 asks for the mechanism to stop guessing, not for history to be rewritten; and a rewritten title would falsify the comments that reference it |
| 7 | The one-open invariant and its single retry stay exactly as they are | both are correct, and one of them caught a real fault on the run that measured this issue |
