# 1788491830-a-segments-record-says-what-it-cost — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/137-a-segments-record-says-what-it-cost |

Answered 2026-09-04 by the repository owner, before the first edit.

## Why this way

The change alters the shape of a record every segment writes, which is the
rung where a spec and a plan come first.

**Its scope was narrowed in the same batch.** #137 names four facts a segment
should leave and says two are missing — what ran it, and what its output cost
the next reader. This work item builds the first only. The second needs a
format decided against evidence that does not exist yet, and #137's own body
refuses to pick one early; it becomes its own ticket for the next release,
and this branch writes that row, because the flow now says a branch keeps the
rows its own work created or closed.

The deadline is continuous rather than dated: every segment measured before
the record row lands is one nothing can attribute afterwards. #145 cannot get
its fourth band without it, and #84's last line cannot be answered without it.
