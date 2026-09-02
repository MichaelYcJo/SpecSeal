# 1788184145-the-gate-stops-the-session-editing-its-tests — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/the-gate-stops-the-session-editing-its-tests |

Answered 2026-08-31 by the repository owner, before the first edit.

## Why this way

Issue #34 changes what the agent files instruct, which is the surface a
spawned session reads and acts on — so it goes through the review chain rather
than straight to the pull request. The pull request lands on `release/v0.0.2`,
cut for this release: the change does not move a gate's verdict, so it waits
for company rather than taking `main` on its own.
