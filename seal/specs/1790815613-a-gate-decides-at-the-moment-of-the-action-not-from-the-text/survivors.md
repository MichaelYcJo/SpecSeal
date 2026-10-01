# Survivors — a gate decides at the moment of the action, not from the text

`survivor-check --range cd24f516..HEAD`, run at `c5f650c` by `smith`, reported six
places. The range corrected two comments and one paragraph that described the
text reading as the only reading: the commit gate's comment on the routing
declaration (moved into `hooks/gate.py#arms_missing` and reworded), the rider in
`hooks/cmdline_base.py` (which said #692 would delete the file), and the guard
policy's *the commit gate still reads both*. Each place below shares phrasing with
one of those and states something still true, or is an earlier work item's record
of its own moment.

| Path | Quote | Grounds |
|---|---|---|
| `docs/commit-review-gate-spec.md` | **The gate reads `seal/specs/<work-item-id>/routing.md` before it | the declaration still silences the review arm, now read in `hooks/gate.py#arms_missing` for both the git hooks and the fallback; the statement is true |
| `docs/commit-review-gate-spec.md` | silent — the routing question was answered before the first edit, and CI checks the answer at the pull request. | the decision table's declared row, true for both readings |
| `skills/code-review/scripts/chain_check.py` | It runs on the pull request, where nobody has to be sitting. | the chain check's own docstring, about CI; this range does not touch it |
| `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/overview.md` | the rider in `hooks/cmdline_base.py` says those comments describe `542f920b` and that #692 reconciles them | work item 1790745049's closing memo, a record of what the rider said then |
| `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/overview.md` | several of its comments name the worktree guard or the consent writer as a reader | the same memo's divergence row, a record of its own build |
| `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/spec.md` | the commit gate still reads both. | work item 1790745049's frame, true of the commit gate on the day it was written; the policy now says which reading |
