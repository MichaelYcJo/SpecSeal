# 1788912166-red-for-following-the-documents-green-for-ignoring-one — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/296-295-297-red-for-following-the-documents |

Answered 2026-09-09 by the owner, before the first edit.

## Why this way

Three of the repository's own pull-request checks are wrong about what they
are reading, and two of them were found by a session doing exactly what a
document told it to do. A change to a gate's verdict is judged by what it
does when it is wrong, so it goes through the chain rather than arriving at
the pull request unreviewed — and the pull request itself is the production
environment for #296, which is about what a draft pull request is allowed to
be.

It runs in a worktree at `SpecSeal-095-gates` because #145's review round is
live in the main checkout. The code surfaces do not overlap: #145 is
`skills/verify/`, this is `skills/code-review/scripts/` and
`.github/workflows/`. `docs/flow.md` is the one file both could touch, and
its row for these three is already committed on its own branch (#298), so
this work item does not touch it at all.
