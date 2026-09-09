# 1788936260-a-case-pins-what-it-actually-measures — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/262-310-a-case-pins-what-it-actually-measures |

Answered 2026-09-09 by the owner, before the first edit.

## Why this way

The owner approved a recommendation naming both tickets, the pairing and the
order, so the three axes are the ones answered three times already today and
were not re-asked.

It goes through the chain because #262 adds mechanism — a checker that
enumerates a module's arms from its own source — and this session has watched
four fix passes run that enumeration by hand today, twice finding what the
cases had missed. A checker whose own enumeration is short is worse than no
checker, and the chain is what reads an enumeration.
