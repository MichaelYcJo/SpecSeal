# 1789034970-the-contract-is-settled-against-the-agents-that-exist — routing

<!-- seal/specs/<unix-epoch-seconds>-<slug>/routing.md — the answer given before the
first edit, in the batch the `implement` skill collects (§1). Committed,
because the check happens at the pull request and CI sees only what is in the
tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | docs/120-the-contract-is-settled-against-the-agents-that-exist |

Answered 2026-09-10 by the owner, before the first edit.

## Why this way

#120 rewrites two sections of the file every agent receives at startup, so a
wrong sentence is paid on every spawn of every agent — that is the most
expensive place in this repository to be wrong, and it is why the review
chain runs rather than the pull request alone.

Three design answers came with the routing, in the same batch:

- **The contract stays one file, sixteen sections.** Only §2 and §6 are
  settled. The defect is contradiction, not irrelevance: §12–§15 are vacuous
  for the sealer rather than false about it, and a line drawn at four agents
  is redrawn when the framer arrives in 0.11.0. What a split would cost is a
  `§N` citation that no longer names one file, which existing round records
  cannot supply.
- **§7 widens** — a probe leaves nothing behind, whatever kind of thing it
  made. The stray worktree of #30's round was a probe that followed §7 to the
  letter.
- **The routing template gains the criterion** the first comment on #120 asks
  for, so the next release measures the `smith` · `the session` row against
  something rather than against habit. `smith`'s §-by-§ scoping is NOT frozen
  here; that is the one thing this work item defers.
