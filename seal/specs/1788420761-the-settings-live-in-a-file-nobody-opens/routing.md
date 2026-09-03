# 1788420761-the-settings-live-in-a-file-nobody-opens — routing

<!-- seal/specs/1788420761-the-settings-live-in-a-file-nobody-opens/routing.md — the answer
given before the first edit, in the batch the `implement` skill collects (§1).
Committed, because the check happens at the pull request and CI sees only what
is in the tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | the session |
| Branch | feat/the-language-rows-and-the-config-command |

Answered 2026-09-03 by the repository owner, before the first edit.

## Why this way

Issue #105 — the front door to every row, routing the ones that have side effects.

**The session implements rather than a smith.** Nothing here is code that
runs: #106 renames and widens two rows of a markdown table and the documents
that read them, and #105 is a skill, which is instructions rather than a
program. The design came out of a conversation with the owner an hour ago and
the session is holding it; a smith would spend its first half rebuilding that
from the issue.

**Both work items share one branch and one review round**, by the owner's
decision. They are one surface — the rows of `seal/config.md` and the command
that asks about them — and the failure mode that matters is the two
disagreeing with each other, which is visible when they are read together and
invisible when they are reviewed apart.
