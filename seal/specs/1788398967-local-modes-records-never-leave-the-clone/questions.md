# 1788398967-local-modes-records-never-leave-the-clone — questions for the planner

<!-- seal/specs/1788398967-local-modes-records-never-leave-the-clone/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | The reminder counts work items. What about the root-level files — `ledger.md`, `follow-up.md`, `config.md`, `parity.md`? | (a) leave the line as the design writes it: a change confined to `follow-up.md` reports `0 work items changed` and a user who trusts the number skips an export that had something to carry. (b) count them, which needs the line to say something other than *work items* — and the design fixes that wording, so changing it is the owner's call, not this work item's | (a). The line is `N work items changed since the last export`, exactly as `docs/one-root-by-lifetime.md` writes it, and root-level files are not counted. The gap is written into the command's docstring so the next reader meets it there rather than deriving it | ⬜ |
| Q2 | Does `seal` stay at two subcommands? | (a) two, and a later `settle` joins them when it exists. (b) grow it now — `seal status` for the mode and the root, `seal doctor` — which is surface nobody asked for and a second place the mode is explained | (a). Two subcommands and one flag. `seal export` already answers *which mode am I in* when it refuses in shared mode, which is the only status question this work found a use for | ⬜ |
| Q3 | Should a shared-mode `seal export` ever write a zip? | (a) never; exit 1 with the mode, the path and the `mv` that switches to local. (b) write one, for symmetry with import and for a user who wants a snapshot — at the cost of a stale duplicate of committed files and `.incoming` noise wherever it is imported | (a), and `plan.md`'s alternatives table carries the reasoning. If the owner wants (b), it is a flag on the refusal rather than a change of default | ⬜ |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
