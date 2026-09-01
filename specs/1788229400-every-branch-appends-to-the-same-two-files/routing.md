# 1788229400-every-branch-appends-to-the-same-two-files — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/every-branch-appends-to-the-same-two-files |

Answered 2026-09-01 by the repository owner, before the first edit.

## Why this way

The work item changes two mechanisms every later branch depends on — where a
change writes its changelog entry, and what a ledger row's drift is measured
from — so it goes through the review chain rather than straight to the pull
request. Issues #46 and #52 are both closed by it, and #52's direction was
settled during the routing batch: the stamp is not written at all, because the
value it carries is one `git blame` already holds.
