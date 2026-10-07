# 1791327652-a-base-session-that-died-part-way-is-not-read-as-finished — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | the session |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/849-a-base-session-that-died-part-way-reads-as-finished |

Answered 2026-10-07 by the repository owner, before the first edit.

## Why this way

#825's second review run ended capped at round 6. That round's three findings were deferred to #849, and the owner chose to fix them in 0.20.0 as their own work item, then pressed `automation` for it.

The frame is the round-6 report's paste-ready fixes: `rounds/round-6-report.md` of work item 1791270161, now in `release/v0.20.0`. So this session writes the short `spec.md` and `plan.md` itself, and no framer runs.
