# 1788844300-the-guards-cases-cannot-observe-what-they-guard — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | test/209-210-the-guards-cases-cannot-observe-what-they-guard |

Answered 2026-09-08 by the repository owner, before the first edit, in the one
batch that answers every work item of 0.9.2.

## Why this way

Two tickets, one guard, one module of cases. The reader has a failure arm no
case watches, and the parametrized case beside it is a class over two literals
rather than over the passes the reader actually makes — so a third pass added
later is unguarded and silent.

Both are case-strength rather than defect: the arms are present and correct,
and the failure direction of the second is safe. The review chain is still the
route, because a case that cannot observe what it guards is exactly what a
green suite hides, and this branch's own new cases are of that kind.
