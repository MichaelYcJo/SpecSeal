# 1788326734-the-ledger-fragments-are-never-gathered — routing

<!-- specs/1788326734-the-ledger-fragments-are-never-gathered/routing.md — the
answer given before the first edit, in the batch the `implement` skill
collects (§1). Committed, because the check happens at the pull request and
CI sees only what is in the tree.

The rows are read by machines and their vocabulary is fixed. Anything else in
this file is for people. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | chore/the-ledger-fragments-are-never-gathered |

Answered 2026-09-02 by the repository owner, before the first edit.

## Why this way

Ticket #78, the first of the 0.4.0 set in `docs/flow.md`: the release step
folds `.specseal/map/<id>.md` into `map.md` and refuses while an
`evidence-todo.md` row is open. It changes what a release does, so it goes
through the chain; the pull request lands on `release/v0.4.0`.
