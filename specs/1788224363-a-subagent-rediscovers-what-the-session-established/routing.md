# 1788224363-a-subagent-rediscovers-what-the-session-established — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | chore/a-subagent-rediscovers-what-the-session-established |

Answered 2026-09-01 by the repository owner, before the first edit.

## Why this way

Issue #29 is the cost of a run: what a spawned agent re-derives, what the
orchestrator cannot see, and what the meter for both cannot count. The work
changes `session_cost.py` and the shipped agent contracts, which is code CI
reads and text spawned sessions act on — so it goes through the review chain.
The pull request lands on `release/v0.0.2` as that release's last item.

The owner added one instruction for the run itself: **this work item measures
its own segments with the meter it fixes.** The meter fix lands first; every
later segment — the smith's own run, each review round — is then measured
with corrected counting, and the numbers feed the next spawn. The acceptance
evidence in `overview.md` is this run's own readings.
