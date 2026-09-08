# 1788817289-local-mode-from-first-setup-to-the-gate — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/225-151-local-mode-from-first-setup-to-the-gate |

Answered 2026-09-07 by the repository owner, before the first edit, in the
batch the `implement` skill §1 collects.

## Why this way

The 0.9.1 run was routed once for all of its work items: `smith` builds, the
review chain runs, and the pull request opens and merges into
`release/v0.9.1`. The one design question this item raises — where a
local-mode root is reported when nothing is committed for `chain_check`'s
`tracked_declarations` to find — was answered in the same batch: the gate and
the preset pointer together, and not `seal/config.md` as the opt-in signal.
