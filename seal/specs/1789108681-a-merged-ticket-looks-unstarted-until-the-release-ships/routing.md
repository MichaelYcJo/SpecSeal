# 1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Branch | feat/359-a-merged-ticket-looks-unstarted-until-the-release-ships |

Answered 2026-09-11 by the repository owner, before the first edit.

## Why this way

The change adds a gate that can refuse a release pull request, so
`CONTRIBUTING.md` §*What a change to a gate must carry* applies and the chain
runs. `Planning` reads `framer` rather than `the session`: the previous work
item recorded `the session` because `framer` had shipped in 0.11.0 on that
branch's own base and no session had spawned it, and that reason is spent —
0.11.0 is this branch's base and the SDD ladder's `Written by` column says
`spec.md` is the framer's. `Implementation` reads `smith` on the owner's
answer; the diff is two workflow-side scripts, a `hygiene.yml` job, a
checklist line and their cases.
