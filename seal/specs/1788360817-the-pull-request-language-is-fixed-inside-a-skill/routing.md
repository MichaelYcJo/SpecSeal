# 1788360817-the-pull-request-language-is-fixed-inside-a-skill — routing

<!-- seal/specs/1788360817-the-pull-request-language-is-fixed-inside-a-skill/routing.md — the answer
given before the first edit, in the batch the `implement` skill collects
(§1). Committed, because the check happens at the pull request and CI sees
only what is in the tree.

The rows are read by machines and their vocabulary is fixed. Anything else in
this file is for people. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/the-pull-request-language-is-fixed-inside-a-skill |

Answered 2026-09-02 by the repository owner, before the first edit.

## Why this way

Ticket #82, third in 0.5.0's list in `docs/flow.md`: the `commit-pr-convention`
skill fixes English for commit messages and pull requests, and a repository
whose team writes another language has no way to say so. This adds
`seal/config.md`, one table the skills read, with `Pull request language` as
its first row and English as the default when the file or the row is absent.
It changes what a skill reads before every commit and pull request, so it goes
through the chain; the pull request lands on `release/v0.5.0` and is
squash-merged there when CI is green — the owner approved that endgame before
sleeping, with the defaults of `questions.md` taken, and this repository's own
`seal/config.md` staying English. The smith is spawned once per phase of
`plan.md`, and the first spawn writes the spec, plan and questions alone and
stops.
