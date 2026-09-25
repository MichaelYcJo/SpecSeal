# 1788395377-the-release-guard-globs-one-place — routing

<!-- seal/specs/1788395377-the-release-guard-globs-one-place/routing.md — the
answer given before the first edit, in the batch the `implement` skill collects
(§1). Committed, because the check happens at the pull request and CI sees only
what is in the tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | the session |
| Branch | fix/the-release-guard-globs-one-place |

Answered 2026-09-03 by the repository owner, before the first edit.

## Why this way

Issue #96: the release guard globs `seal/specs/*/evidence-todo.md` and two
work items keep that file one directory deeper, so it is blind to two of five.
It blocks the 0.5.0 release preparation, which runs that guard.

The change is four `git mv`s and one test. The session builds it rather than
a smith, because a spawn's cost is its context and this is smaller than the
handoff that would describe it — the whole of the work is named in the
ticket's done-when list. It still goes through the chain: a guard that has
been silent for two of five work items is exactly the kind of change a second
reader should open.
