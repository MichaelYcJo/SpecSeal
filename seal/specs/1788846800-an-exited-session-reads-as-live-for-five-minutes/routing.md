# 1788846800-an-exited-session-reads-as-live-for-five-minutes — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/256-an-exited-session-reads-as-live-for-five-minutes |

Answered 2026-09-08 by the repository owner, before the first edit, on the
run's standing answer for the other four items of 0.9.2.

## Why this way

The owner opened #256 mid-run and placed it in 0.9.2 on the grounds that it is
what the earlier worktree friction of this same run actually was. The guard's
verdict ladder was the suspect and is not the defect: the signal underneath it
answers wrongly, so the ladder is reached in a state it was never meant for.

It goes through the review chain because the repair replaces one liveness
signal with another, and the case it must not break — a live session whose host
process is not named `claude` — is the case no local suite covers.
